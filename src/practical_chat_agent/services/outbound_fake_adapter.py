from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Literal, Mapping, Sequence

from pydantic import ValidationError

from practical_chat_agent.core.models import CandidateAction, OutboundMessageRequest, utc_now


FakeOutboundDeliveryStatus = Literal[
    "fake_delivered",
    "blocked_not_sendable",
    "blocked_invalid_request",
]


@dataclass
class FakeOutboundAdapterConfig:
    """Deterministic config for the local fake outbound adapter."""

    adapter_name: str = "local_fake_outbound_adapter"
    preview_char_limit: int = 80

    def __post_init__(self) -> None:
        if not self.adapter_name.strip():
            raise ValueError("FakeOutboundAdapterConfig.adapter_name must be non-empty.")
        if self.preview_char_limit <= 0:
            raise ValueError("FakeOutboundAdapterConfig.preview_char_limit must be > 0.")


@dataclass
class FakeOutboundDeliveryResult:
    """Local synthetic delivery result for already-sendable outbound requests."""

    adapter_name: str
    delivery_status: FakeOutboundDeliveryStatus
    delivered: bool
    request_id: str | None = None
    contact_id: str | None = None
    user_id: str | None = None
    channel_preference: str | None = None
    delivered_at: datetime | None = None
    payload_preview: str | None = None
    audit_notes: list[str] = field(default_factory=list)


class LocalFakeOutboundAdapter:
    """Pure local adapter that simulates delivery without platform side effects."""

    def __init__(self, *, config: FakeOutboundAdapterConfig | None = None) -> None:
        self.config = config or FakeOutboundAdapterConfig()

    def deliver(
        self,
        request: OutboundMessageRequest | CandidateAction | Mapping[str, Any],
        *,
        now: datetime | None = None,
        existing_audit: Sequence[str] | None = None,
    ) -> FakeOutboundDeliveryResult:
        if self._is_candidate_action_input(request):
            return self._blocked_invalid_request(
                request_id=None,
                contact_id=self._mapping_value(request, "contact_id"),
                user_id=self._mapping_value(request, "user_id"),
                channel_preference=None,
                audit_notes=[*self._clean_audit(existing_audit), "candidate_action_input_rejected"],
            )

        try:
            outbound_request = self._coerce_request(request)
        except ValidationError:
            return self._blocked_invalid_request(
                request_id=None,
                contact_id=self._mapping_value(request, "contact_id"),
                user_id=self._mapping_value(request, "user_id"),
                channel_preference=self._mapping_value(request, "channel_preference"),
                audit_notes=[*self._clean_audit(existing_audit), "request_validation_failed"],
            )

        if not outbound_request.is_sendable():
            audit_notes = [*self._clean_audit(existing_audit), "request_not_sendable"]
            if not (
                outbound_request.human_approval.review_state == "approved"
                and outbound_request.human_approval.approved_by_human
            ):
                audit_notes.append("human_approval_not_approved")
            if outbound_request.send_gate.gate_state != "allowed":
                audit_notes.append("send_gate_not_allowed")
            audit_notes.append("local_fake_delivery_blocked")
            return self._result_from_request(
                outbound_request,
                delivery_status="blocked_not_sendable",
                delivered=False,
                delivered_at=None,
                audit_notes=audit_notes,
            )

        delivered_at = self._as_aware_utc(now or utc_now())
        audit_notes = [
            *self._clean_audit(existing_audit),
            "request_validated",
            "request_sendable_verified",
            "local_fake_delivery_only",
            "fake_delivery_recorded",
        ]
        return self._result_from_request(
            outbound_request,
            delivery_status="fake_delivered",
            delivered=True,
            delivered_at=delivered_at,
            audit_notes=audit_notes,
        )

    @staticmethod
    def _coerce_request(
        request: OutboundMessageRequest | Mapping[str, Any],
    ) -> OutboundMessageRequest:
        if isinstance(request, OutboundMessageRequest):
            return request
        return OutboundMessageRequest.model_validate(dict(request))

    @staticmethod
    def _is_candidate_action_input(
        request: OutboundMessageRequest | CandidateAction | Mapping[str, Any],
    ) -> bool:
        if isinstance(request, CandidateAction):
            return True
        if not isinstance(request, Mapping):
            return False
        return (
            request.get("schema_version") == "candidate_action_v1"
            or "action_id" in request
            or "action_type" in request
        )

    def _result_from_request(
        self,
        request: OutboundMessageRequest,
        *,
        delivery_status: FakeOutboundDeliveryStatus,
        delivered: bool,
        delivered_at: datetime | None,
        audit_notes: Sequence[str],
    ) -> FakeOutboundDeliveryResult:
        return FakeOutboundDeliveryResult(
            adapter_name=self.config.adapter_name,
            delivery_status=delivery_status,
            delivered=delivered,
            request_id=request.request_id,
            contact_id=request.contact_id,
            user_id=request.user_id,
            channel_preference=request.channel_preference,
            delivered_at=delivered_at,
            payload_preview=self._build_preview(request.payload.draft_text),
            audit_notes=self._dedupe(audit_notes),
        )

    def _blocked_invalid_request(
        self,
        *,
        request_id: str | None,
        contact_id: str | None,
        user_id: str | None,
        channel_preference: str | None,
        audit_notes: Sequence[str],
    ) -> FakeOutboundDeliveryResult:
        return FakeOutboundDeliveryResult(
            adapter_name=self.config.adapter_name,
            delivery_status="blocked_invalid_request",
            delivered=False,
            request_id=request_id,
            contact_id=contact_id,
            user_id=user_id,
            channel_preference=channel_preference,
            delivered_at=None,
            payload_preview=None,
            audit_notes=self._dedupe([*audit_notes, "local_fake_delivery_blocked"]),
        )

    def _build_preview(self, draft_text: str) -> str:
        preview = " ".join(draft_text.split())
        if len(preview) <= self.config.preview_char_limit:
            return preview
        if self.config.preview_char_limit <= 3:
            return "." * self.config.preview_char_limit
        cutoff = self.config.preview_char_limit - 3
        return f"{preview[:cutoff]}..."

    @staticmethod
    def _as_aware_utc(value: datetime) -> datetime:
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc)

    @staticmethod
    def _dedupe(values: Sequence[str]) -> list[str]:
        seen: set[str] = set()
        result: list[str] = []
        for value in values:
            text = value.strip()
            if not text or text in seen:
                continue
            seen.add(text)
            result.append(text)
        return result

    @staticmethod
    def _clean_audit(values: Sequence[str] | None) -> list[str]:
        if values is None:
            return []
        return LocalFakeOutboundAdapter._dedupe(list(values))

    @staticmethod
    def _mapping_value(
        request: OutboundMessageRequest | CandidateAction | Mapping[str, Any],
        key: str,
    ) -> str | None:
        if isinstance(request, Mapping):
            value = request.get(key)
            if isinstance(value, str) and value.strip():
                return value
        return None
