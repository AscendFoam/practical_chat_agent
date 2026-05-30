from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal, Mapping, Sequence

from pydantic import ValidationError

from practical_chat_agent.core.models import CandidateAction, OutboundMessageRequest
from practical_chat_agent.services.wecom_customer_service_safety import (
    WECom_CUSTOMER_SERVICE_SURFACE,
    WeComCustomerServiceSafetyDecision,
)


WeComCustomerServiceDryRunStatus = Literal[
    "wecom_dry_run_ready",
    "blocked_invalid_request",
    "blocked_candidate_action_input",
    "blocked_not_sendable",
    "blocked_channel_mismatch",
    "blocked_safety_missing",
    "blocked_safety_not_allowed",
    "blocked_safety_mismatch",
    "blocked_missing_safety_aliases",
]


@dataclass(frozen=True)
class WeComCustomerServiceDryRunConfig:
    """Deterministic config for local WeCom Customer Service dry runs."""

    provider_surface: str = WECom_CUSTOMER_SERVICE_SURFACE
    dry_run_only: bool = True

    def __post_init__(self) -> None:
        if not self.provider_surface.strip():
            raise ValueError("provider_surface must be non-empty.")
        if not self.dry_run_only:
            raise ValueError("T232 only supports dry_run_only=True.")


@dataclass(frozen=True)
class WeComCustomerServiceDryRunResult:
    """In-memory dry-run result; this is never provider delivery."""

    delivery_status: WeComCustomerServiceDryRunStatus
    delivered: bool = False
    request_id: str | None = None
    contact_id: str | None = None
    user_id: str | None = None
    provider_surface: str = WECom_CUSTOMER_SERVICE_SURFACE
    recipient_alias: str | None = None
    open_kfid_alias: str | None = None
    external_user_alias: str | None = None
    prepared_payload: dict[str, object] | None = None
    audit_notes: list[str] = field(default_factory=list)


class WeComCustomerServiceDryRunOutboundAdapter:
    """Prepare review-safe WeCom Customer Service dry-run payloads locally."""

    def __init__(self, *, config: WeComCustomerServiceDryRunConfig | None = None) -> None:
        self.config = config or WeComCustomerServiceDryRunConfig()

    def prepare_dry_run(
        self,
        request: OutboundMessageRequest | CandidateAction | Mapping[str, Any],
        *,
        safety_decision: WeComCustomerServiceSafetyDecision | Mapping[str, Any] | None,
        existing_audit: Sequence[str] | None = None,
    ) -> WeComCustomerServiceDryRunResult:
        audit_notes = self._clean_audit(existing_audit)

        if self._is_candidate_action_input(request):
            return self._blocked_invalid_request(
                delivery_status="blocked_candidate_action_input",
                request_id=None,
                contact_id=self._mapping_value(request, "contact_id"),
                user_id=self._mapping_value(request, "user_id"),
                audit_notes=[*audit_notes, "candidate_action_input_rejected"],
            )

        try:
            outbound_request = self._coerce_request(request)
        except ValidationError:
            return self._blocked_invalid_request(
                delivery_status="blocked_invalid_request",
                request_id=None,
                contact_id=self._mapping_value(request, "contact_id"),
                user_id=self._mapping_value(request, "user_id"),
                audit_notes=[*audit_notes, "request_validation_failed"],
            )

        audit_notes.append("request_validated")
        if not outbound_request.is_sendable():
            audit_notes.append("request_not_sendable")
            if not (
                outbound_request.human_approval.review_state == "approved"
                and outbound_request.human_approval.approved_by_human
            ):
                audit_notes.append("human_approval_not_approved")
            if outbound_request.send_gate.gate_state != "allowed":
                audit_notes.append("send_gate_not_allowed")
            audit_notes.append("wecom_dry_run_blocked")
            return self._result_from_request(
                outbound_request,
                delivery_status="blocked_not_sendable",
                audit_notes=audit_notes,
            )

        audit_notes.append("request_sendable_verified")
        if outbound_request.channel_preference != "wechat":
            audit_notes.extend(["wecom_channel_mismatch", "wecom_dry_run_blocked"])
            return self._result_from_request(
                outbound_request,
                delivery_status="blocked_channel_mismatch",
                audit_notes=audit_notes,
            )
        audit_notes.append("wechat_channel_verified")

        if safety_decision is None:
            audit_notes.extend(["wecom_safety_decision_missing", "wecom_dry_run_blocked"])
            return self._result_from_request(
                outbound_request,
                delivery_status="blocked_safety_missing",
                audit_notes=audit_notes,
            )

        try:
            safety = self._coerce_safety_decision(safety_decision)
        except (TypeError, ValueError):
            audit_notes.extend(["wecom_safety_decision_invalid", "wecom_dry_run_blocked"])
            return self._result_from_request(
                outbound_request,
                delivery_status="blocked_safety_mismatch",
                audit_notes=audit_notes,
            )

        audit_notes.extend(safety.audit_notes)
        if safety.safety_state != "allowed":
            audit_notes.extend(safety.reason_codes)
            audit_notes.extend(["wecom_safety_decision_not_allowed", "wecom_dry_run_blocked"])
            return self._result_from_request(
                outbound_request,
                delivery_status="blocked_safety_not_allowed",
                audit_notes=audit_notes,
                safety_decision=safety,
            )

        if not self._safety_matches_request(outbound_request, safety):
            audit_notes.extend(["wecom_safety_decision_mismatch", "wecom_dry_run_blocked"])
            return self._result_from_request(
                outbound_request,
                delivery_status="blocked_safety_mismatch",
                audit_notes=audit_notes,
                safety_decision=safety,
            )

        if not self._has_required_safety_audit(safety):
            audit_notes.extend(["wecom_safety_boundary_audit_missing", "wecom_dry_run_blocked"])
            return self._result_from_request(
                outbound_request,
                delivery_status="blocked_safety_mismatch",
                audit_notes=audit_notes,
                safety_decision=safety,
            )

        if not self._has_required_aliases(safety):
            audit_notes.extend(["wecom_safety_alias_missing", "wecom_dry_run_blocked"])
            return self._result_from_request(
                outbound_request,
                delivery_status="blocked_missing_safety_aliases",
                audit_notes=audit_notes,
                safety_decision=safety,
            )

        audit_notes.extend(
            [
                "wecom_safety_decision_verified",
                "wecom_dry_run_payload_prepared",
                "wecom_dry_run_only",
                "no_provider_delivery",
            ],
        )
        prepared_payload = self._build_payload(outbound_request, safety)
        return self._result_from_request(
            outbound_request,
            delivery_status="wecom_dry_run_ready",
            audit_notes=audit_notes,
            safety_decision=safety,
            prepared_payload=prepared_payload,
        )

    @staticmethod
    def _coerce_request(request: OutboundMessageRequest | Mapping[str, Any]) -> OutboundMessageRequest:
        if isinstance(request, OutboundMessageRequest):
            return request
        return OutboundMessageRequest.model_validate(dict(request))

    @staticmethod
    def _coerce_safety_decision(
        safety_decision: WeComCustomerServiceSafetyDecision | Mapping[str, Any],
    ) -> WeComCustomerServiceSafetyDecision:
        if isinstance(safety_decision, WeComCustomerServiceSafetyDecision):
            return safety_decision
        return WeComCustomerServiceSafetyDecision(**dict(safety_decision))

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

    def _safety_matches_request(
        self,
        request: OutboundMessageRequest,
        safety: WeComCustomerServiceSafetyDecision,
    ) -> bool:
        return (
            safety.provider_surface == self.config.provider_surface
            and safety.provider_surface == WECom_CUSTOMER_SERVICE_SURFACE
            and safety.request_id == request.request_id
            and safety.contact_id == request.contact_id
            and safety.user_id == request.user_id
        )

    @staticmethod
    def _has_required_safety_audit(safety: WeComCustomerServiceSafetyDecision) -> bool:
        notes = set(safety.audit_notes)
        return {
            "provider_eligible_not_delivery",
            "provider_payload_not_prepared",
        }.issubset(notes)

    @staticmethod
    def _has_required_aliases(safety: WeComCustomerServiceSafetyDecision) -> bool:
        return all(
            isinstance(value, str) and value.strip()
            for value in (
                safety.recipient_alias,
                safety.open_kfid_alias,
                safety.external_user_alias,
            )
        )

    def _build_payload(
        self,
        request: OutboundMessageRequest,
        safety: WeComCustomerServiceSafetyDecision,
    ) -> dict[str, object]:
        payload: dict[str, object] = {
            "provider_surface": WECom_CUSTOMER_SERVICE_SURFACE,
            "dry_run": True,
            "request_id": request.request_id,
            "contact_id": request.contact_id,
            "user_id": request.user_id,
            "recipient_aliases": {
                "recipient_alias": safety.recipient_alias,
                "open_kfid_alias": safety.open_kfid_alias,
                "external_user_alias": safety.external_user_alias,
            },
            "message": {
                "msg_type": "text",
                "text": request.payload.draft_text,
            },
            "source": {
                "source_type": request.source_type,
                "source_candidate_action_id": request.source_candidate_action_id,
            },
        }
        if request.payload.safe_summary is not None:
            payload["safe_summary"] = request.payload.safe_summary
        return payload

    def _result_from_request(
        self,
        request: OutboundMessageRequest,
        *,
        delivery_status: WeComCustomerServiceDryRunStatus,
        audit_notes: Sequence[str],
        safety_decision: WeComCustomerServiceSafetyDecision | None = None,
        prepared_payload: dict[str, object] | None = None,
    ) -> WeComCustomerServiceDryRunResult:
        return WeComCustomerServiceDryRunResult(
            delivery_status=delivery_status,
            delivered=False,
            request_id=request.request_id,
            contact_id=request.contact_id,
            user_id=request.user_id,
            provider_surface=self.config.provider_surface,
            recipient_alias=None if safety_decision is None else safety_decision.recipient_alias,
            open_kfid_alias=None if safety_decision is None else safety_decision.open_kfid_alias,
            external_user_alias=None if safety_decision is None else safety_decision.external_user_alias,
            prepared_payload=prepared_payload,
            audit_notes=self._dedupe(audit_notes),
        )

    def _blocked_invalid_request(
        self,
        *,
        delivery_status: Literal["blocked_invalid_request", "blocked_candidate_action_input"],
        request_id: str | None,
        contact_id: str | None,
        user_id: str | None,
        audit_notes: Sequence[str],
    ) -> WeComCustomerServiceDryRunResult:
        return WeComCustomerServiceDryRunResult(
            delivery_status=delivery_status,
            delivered=False,
            request_id=request_id,
            contact_id=contact_id,
            user_id=user_id,
            provider_surface=self.config.provider_surface,
            prepared_payload=None,
            audit_notes=self._dedupe([*audit_notes, "wecom_dry_run_blocked"]),
        )

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
        return WeComCustomerServiceDryRunOutboundAdapter._dedupe(list(values))

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
