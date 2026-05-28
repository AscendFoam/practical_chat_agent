from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, time, timedelta
from typing import Any, Mapping, Sequence
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from practical_chat_agent.core.models import (
    OutboundMessageRequest,
    OutboundRequestSendGate,
    utc_now,
)


@dataclass
class OutboundSendGateConfig:
    """Deterministic config for the review-only outbound send gate."""

    evaluator_id: str = "outbound_send_gate"
    manual_only_mode: bool = True
    kill_switch_enabled: bool = False
    quiet_hours_start: str | None = "23:00"
    quiet_hours_end: str | None = "08:00"
    timezone_name: str = "Asia/Shanghai"
    frequency_limit_count: int = 3
    frequency_limit_window_seconds: int = 600
    duplicate_window_seconds: int = 600

    def __post_init__(self) -> None:
        if not self.manual_only_mode:
            raise ValueError("T221 only supports manual_only_mode=True.")
        if not self.evaluator_id.strip():
            raise ValueError("OutboundSendGateConfig.evaluator_id must be non-empty.")
        if self.frequency_limit_count < 0:
            raise ValueError("frequency_limit_count must be >= 0.")
        if self.frequency_limit_window_seconds < 0:
            raise ValueError("frequency_limit_window_seconds must be >= 0.")
        if self.duplicate_window_seconds < 0:
            raise ValueError("duplicate_window_seconds must be >= 0.")
        self._parse_hhmm(self.quiet_hours_start)
        self._parse_hhmm(self.quiet_hours_end)

    @staticmethod
    def _parse_hhmm(value: str | None) -> time | None:
        if value is None or not value.strip():
            return None
        hour_text, minute_text = value.strip().split(":", maxsplit=1)
        return time(hour=int(hour_text), minute=int(minute_text))


@dataclass
class OutboundSendGateContext:
    """Optional review-safe context used for duplicate and self-echo checks."""

    latest_inbound_text: str | None = None
    latest_user_text: str | None = None
    self_echo_reference_texts: list[str] = field(default_factory=list)


@dataclass
class OutboundSendGateDecision:
    """Deterministic gate decision with an updated audited request copy."""

    evaluated_request: OutboundMessageRequest
    allowed: bool
    blocked_reasons: list[str] = field(default_factory=list)
    passed_checks: list[str] = field(default_factory=list)
    gate_notes: list[str] = field(default_factory=list)


class OutboundSendGate:
    """Pure local policy gate over T220 OutboundMessageRequest artifacts."""

    def __init__(self, *, config: OutboundSendGateConfig | None = None) -> None:
        self.config = config or OutboundSendGateConfig()

    def evaluate(
        self,
        request: OutboundMessageRequest | Mapping[str, Any],
        *,
        now: datetime | None = None,
        recent_requests: Sequence[OutboundMessageRequest | Mapping[str, Any]] | None = None,
        context: OutboundSendGateContext | Mapping[str, Any] | None = None,
        existing_audit: Sequence[str] | None = None,
    ) -> OutboundSendGateDecision:
        outbound_request = self._coerce_request(request)
        history = [self._coerce_request(item) for item in (recent_requests or [])]
        gate_context = self._coerce_context(context)
        evaluated_at = self._as_aware_utc(now or utc_now())

        passed_checks: list[str] = []
        blocked_reasons: list[str] = []
        gate_notes: list[str] = [note.strip() for note in (existing_audit or []) if note.strip()]

        passed_checks.append("manual_only_mode_enabled")
        approval_reason = self._approval_reason(outbound_request)
        if approval_reason is None:
            passed_checks.append("human_approval_approved")
        else:
            blocked_reasons.append(approval_reason)

        if self.config.kill_switch_enabled:
            blocked_reasons.append("kill_switch_enabled")
        else:
            passed_checks.append("kill_switch_disabled")

        normalized_text = self._normalize_text(outbound_request.payload.draft_text)
        if normalized_text:
            passed_checks.append("payload_text_present")
        else:
            blocked_reasons.append("empty_draft_text")

        if self._is_quiet_hours(evaluated_at):
            blocked_reasons.append("quiet_hours_blocked")
        else:
            passed_checks.append("quiet_hours_clear")

        if self._exceeds_frequency_limit(
            request=outbound_request,
            recent_requests=history,
            evaluated_at=evaluated_at,
        ):
            blocked_reasons.append("frequency_limit_exceeded")
        else:
            passed_checks.append("frequency_limit_clear")

        if self._is_duplicate(
            request=outbound_request,
            normalized_text=normalized_text,
            recent_requests=history,
            evaluated_at=evaluated_at,
        ):
            blocked_reasons.append("duplicate_suppressed")
        else:
            passed_checks.append("duplicate_check_clear")

        if self._is_self_echo(normalized_text=normalized_text, context=gate_context):
            blocked_reasons.append("self_echo_prevention")
        else:
            passed_checks.append("self_echo_clear")

        blocked_reasons = self._dedupe(blocked_reasons)
        passed_checks = self._dedupe(passed_checks)
        gate_state = "allowed" if not blocked_reasons else "blocked"
        gate_notes.extend(passed_checks)
        gate_notes.extend(blocked_reasons)
        gate_notes.append("gate_allowed" if gate_state == "allowed" else "gate_blocked")
        gate_notes = self._dedupe(gate_notes)

        evaluated_request = outbound_request.model_copy(
            update={
                "send_gate": OutboundRequestSendGate(
                    gate_state=gate_state,
                    evaluator_id=self.config.evaluator_id,
                    evaluated_at=evaluated_at,
                    gate_notes=gate_notes,
                ),
                "updated_at": evaluated_at,
            },
        )
        return OutboundSendGateDecision(
            evaluated_request=evaluated_request,
            allowed=gate_state == "allowed",
            blocked_reasons=blocked_reasons,
            passed_checks=passed_checks,
            gate_notes=gate_notes,
        )

    @staticmethod
    def _coerce_request(request: OutboundMessageRequest | Mapping[str, Any]) -> OutboundMessageRequest:
        if isinstance(request, OutboundMessageRequest):
            return request
        return OutboundMessageRequest.model_validate(dict(request))

    @staticmethod
    def _coerce_context(
        context: OutboundSendGateContext | Mapping[str, Any] | None,
    ) -> OutboundSendGateContext:
        if context is None:
            return OutboundSendGateContext()
        if isinstance(context, OutboundSendGateContext):
            return context
        return OutboundSendGateContext(**dict(context))

    def _approval_reason(self, request: OutboundMessageRequest) -> str | None:
        approval = request.human_approval
        if approval.review_state == "approved" and approval.approved_by_human:
            return None
        if approval.review_state == "pending_human_approval":
            return "human_approval_pending"
        return "human_approval_rejected"

    def _is_quiet_hours(self, now: datetime) -> bool:
        quiet_start = self.config._parse_hhmm(self.config.quiet_hours_start)
        quiet_end = self.config._parse_hhmm(self.config.quiet_hours_end)
        if quiet_start is None or quiet_end is None:
            return False
        local_now = self._local_now(now)
        current_time = local_now.time()
        if quiet_start < quiet_end:
            return quiet_start <= current_time < quiet_end
        return current_time >= quiet_start or current_time < quiet_end

    def _exceeds_frequency_limit(
        self,
        *,
        request: OutboundMessageRequest,
        recent_requests: Sequence[OutboundMessageRequest],
        evaluated_at: datetime,
    ) -> bool:
        if self.config.frequency_limit_count <= 0 or self.config.frequency_limit_window_seconds <= 0:
            return False
        cutoff = evaluated_at - timedelta(seconds=self.config.frequency_limit_window_seconds)
        recent_allowed_count = sum(
            1
            for history_request in recent_requests
            if self._is_same_scope(request, history_request)
            and history_request.send_gate.gate_state == "allowed"
            and self._history_timestamp(history_request) >= cutoff
        )
        return recent_allowed_count >= self.config.frequency_limit_count

    def _is_duplicate(
        self,
        *,
        request: OutboundMessageRequest,
        normalized_text: str,
        recent_requests: Sequence[OutboundMessageRequest],
        evaluated_at: datetime,
    ) -> bool:
        if not normalized_text or self.config.duplicate_window_seconds <= 0:
            return False
        cutoff = evaluated_at - timedelta(seconds=self.config.duplicate_window_seconds)
        for history_request in recent_requests:
            if not self._is_same_scope(request, history_request):
                continue
            if history_request.send_gate.gate_state != "allowed":
                continue
            if self._history_timestamp(history_request) < cutoff:
                continue
            if self._normalize_text(history_request.payload.draft_text) == normalized_text:
                return True
        return False

    @staticmethod
    def _is_self_echo(*, normalized_text: str, context: OutboundSendGateContext) -> bool:
        if not normalized_text:
            return False
        candidates = [
            context.latest_inbound_text,
            context.latest_user_text,
            *context.self_echo_reference_texts,
        ]
        return any(OutboundSendGate._normalize_text(value) == normalized_text for value in candidates)

    @staticmethod
    def _is_same_scope(request: OutboundMessageRequest, history_request: OutboundMessageRequest) -> bool:
        return (
            request.contact_id == history_request.contact_id
            and request.user_id == history_request.user_id
            and request.channel_preference == history_request.channel_preference
        )

    @staticmethod
    def _history_timestamp(request: OutboundMessageRequest) -> datetime:
        if request.send_gate.evaluated_at is not None:
            return OutboundSendGate._as_aware_utc(request.send_gate.evaluated_at)
        return OutboundSendGate._as_aware_utc(request.created_at)

    def _local_now(self, now: datetime) -> datetime:
        current = self._as_aware_utc(now)
        try:
            zone = ZoneInfo(self.config.timezone_name)
        except ZoneInfoNotFoundError:
            zone = ZoneInfo("UTC")
        return current.astimezone(zone)

    @staticmethod
    def _as_aware_utc(value: datetime) -> datetime:
        if value.tzinfo is None:
            return value.replace(tzinfo=ZoneInfo("UTC"))
        return value.astimezone(ZoneInfo("UTC"))

    @staticmethod
    def _normalize_text(value: str | None) -> str:
        if value is None:
            return ""
        return " ".join(value.casefold().split())

    @staticmethod
    def _dedupe(values: list[str]) -> list[str]:
        seen: set[str] = set()
        result: list[str] = []
        for value in values:
            text = value.strip()
            if not text or text in seen:
                continue
            seen.add(text)
            result.append(text)
        return result
