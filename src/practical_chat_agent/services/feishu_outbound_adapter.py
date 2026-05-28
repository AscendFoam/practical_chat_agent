from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Literal, Mapping, Protocol, Sequence

from pydantic import ValidationError

from practical_chat_agent.core.models import CandidateAction, OutboundMessageRequest, utc_now


FeishuRecipientType = Literal["open_id", "chat_id"]
FeishuSandboxDeliveryStatus = Literal[
    "feishu_dry_run_ready",
    "feishu_sandbox_sent",
    "blocked_not_sendable",
    "blocked_invalid_request",
    "blocked_missing_recipient",
    "blocked_wrong_channel",
    "blocked_transport_error",
    "blocked_transport_unavailable",
]


@dataclass(frozen=True)
class FeishuSandboxRecipient:
    """Explicit sandbox recipient mapping outside outbound payload metadata."""

    recipient_type: FeishuRecipientType
    recipient_id: str

    def __post_init__(self) -> None:
        if self.recipient_type not in ("open_id", "chat_id"):
            raise ValueError("FeishuSandboxRecipient.recipient_type must be 'open_id' or 'chat_id'.")
        if not self.recipient_id.strip():
            raise ValueError("FeishuSandboxRecipient.recipient_id must be non-empty.")


@dataclass
class FeishuSandboxAdapterConfig:
    """Deterministic config for the Feishu sandbox outbound adapter."""

    adapter_name: str = "feishu_sandbox_outbound_adapter"
    dry_run_by_default: bool = True
    recipient_map: dict[str, FeishuSandboxRecipient] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.adapter_name.strip():
            raise ValueError("FeishuSandboxAdapterConfig.adapter_name must be non-empty.")
        normalized: dict[str, FeishuSandboxRecipient] = {}
        for contact_id, recipient in self.recipient_map.items():
            if not contact_id.strip():
                raise ValueError("FeishuSandboxAdapterConfig.recipient_map keys must be non-empty.")
            normalized[contact_id] = recipient
        self.recipient_map = normalized


@dataclass
class FeishuSandboxTransportResponse:
    """Synthetic sandbox transport response used in tests or later dry-run flows."""

    provider_message_id: str | None = None
    audit_notes: list[str] = field(default_factory=list)


class FeishuSandboxTransport(Protocol):
    def send(self, payload: dict[str, object]) -> FeishuSandboxTransportResponse: ...


@dataclass
class FeishuSandboxDeliveryResult:
    """Feishu sandbox adapter result for dry-run or injected fake transport flows."""

    adapter_name: str
    delivery_status: FeishuSandboxDeliveryStatus
    delivered: bool
    request_id: str | None = None
    contact_id: str | None = None
    user_id: str | None = None
    channel_preference: str | None = None
    recipient_type: str | None = None
    recipient_id: str | None = None
    prepared_payload: dict[str, object] | None = None
    provider_message_id: str | None = None
    result_at: datetime = field(default_factory=utc_now)
    audit_notes: list[str] = field(default_factory=list)


class FeishuSandboxOutboundAdapter:
    """Prepare Feishu-compatible sandbox payloads from already-sendable requests."""

    def __init__(
        self,
        *,
        config: FeishuSandboxAdapterConfig | None = None,
        transport: FeishuSandboxTransport | None = None,
    ) -> None:
        self.config = config or FeishuSandboxAdapterConfig()
        self.transport = transport

    def deliver(
        self,
        request: OutboundMessageRequest | CandidateAction | Mapping[str, Any],
        *,
        dry_run: bool | None = None,
        now: datetime | None = None,
        existing_audit: Sequence[str] | None = None,
    ) -> FeishuSandboxDeliveryResult:
        result_at = self._as_aware_utc(now or utc_now())

        if self._is_candidate_action_input(request):
            return self._blocked_invalid_request(
                result_at=result_at,
                contact_id=self._mapping_value(request, "contact_id"),
                user_id=self._mapping_value(request, "user_id"),
                channel_preference=self._mapping_value(request, "channel_preference"),
                audit_notes=[*self._clean_audit(existing_audit), "candidate_action_input_rejected"],
            )

        try:
            outbound_request = self._coerce_request(request)
        except ValidationError:
            return self._blocked_invalid_request(
                result_at=result_at,
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
            return self._result_from_request(
                outbound_request,
                delivery_status="blocked_not_sendable",
                delivered=False,
                result_at=result_at,
                audit_notes=audit_notes,
            )

        audit_notes = [
            *self._clean_audit(existing_audit),
            "request_validated",
            "request_sendable_verified",
            "gate_allowed_verified",
        ]

        if outbound_request.channel_preference != "feishu":
            audit_notes.append("feishu_channel_incompatible")
            return self._result_from_request(
                outbound_request,
                delivery_status="blocked_wrong_channel",
                delivered=False,
                result_at=result_at,
                audit_notes=audit_notes,
            )
        audit_notes.append("feishu_channel_verified")

        recipient = self.config.recipient_map.get(outbound_request.contact_id)
        if recipient is None:
            audit_notes.append("feishu_recipient_missing")
            return self._result_from_request(
                outbound_request,
                delivery_status="blocked_missing_recipient",
                delivered=False,
                result_at=result_at,
                audit_notes=audit_notes,
            )
        audit_notes.append("feishu_recipient_resolved")

        prepared_payload = self._build_payload(outbound_request, recipient)
        audit_notes.extend(["feishu_sandbox_payload_prepared", "no_production_delivery"])

        effective_dry_run = self.config.dry_run_by_default if dry_run is None else dry_run
        if effective_dry_run:
            audit_notes.append("feishu_dry_run_only")
            return self._result_from_request(
                outbound_request,
                delivery_status="feishu_dry_run_ready",
                delivered=False,
                result_at=result_at,
                audit_notes=audit_notes,
                recipient=recipient,
                prepared_payload=prepared_payload,
            )

        if self.transport is None:
            audit_notes.append("feishu_sandbox_transport_unavailable")
            return self._result_from_request(
                outbound_request,
                delivery_status="blocked_transport_unavailable",
                delivered=False,
                result_at=result_at,
                audit_notes=audit_notes,
                recipient=recipient,
                prepared_payload=prepared_payload,
            )

        try:
            transport_response = self.transport.send(prepared_payload)
        except Exception as exc:
            audit_notes.extend(
                [
                    "feishu_sandbox_transport_invoked",
                    "feishu_sandbox_transport_failed",
                    f"transport_exception_{exc.__class__.__name__.casefold()}",
                ],
            )
            return self._result_from_request(
                outbound_request,
                delivery_status="blocked_transport_error",
                delivered=False,
                result_at=result_at,
                audit_notes=audit_notes,
                recipient=recipient,
                prepared_payload=prepared_payload,
            )

        audit_notes.extend(
            [
                "feishu_sandbox_transport_invoked",
                *transport_response.audit_notes,
            ],
        )
        return self._result_from_request(
            outbound_request,
            delivery_status="feishu_sandbox_sent",
            delivered=True,
            result_at=result_at,
            audit_notes=audit_notes,
            recipient=recipient,
            prepared_payload=prepared_payload,
            provider_message_id=transport_response.provider_message_id,
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

    @staticmethod
    def _build_payload(
        request: OutboundMessageRequest,
        recipient: FeishuSandboxRecipient,
    ) -> dict[str, object]:
        return {
            "receive_id_type": recipient.recipient_type,
            "receive_id": recipient.recipient_id,
            "msg_type": "text",
            "content": {
                "text": request.payload.draft_text,
            },
        }

    def _result_from_request(
        self,
        request: OutboundMessageRequest,
        *,
        delivery_status: FeishuSandboxDeliveryStatus,
        delivered: bool,
        result_at: datetime,
        audit_notes: Sequence[str],
        recipient: FeishuSandboxRecipient | None = None,
        prepared_payload: dict[str, object] | None = None,
        provider_message_id: str | None = None,
    ) -> FeishuSandboxDeliveryResult:
        return FeishuSandboxDeliveryResult(
            adapter_name=self.config.adapter_name,
            delivery_status=delivery_status,
            delivered=delivered,
            request_id=request.request_id,
            contact_id=request.contact_id,
            user_id=request.user_id,
            channel_preference=request.channel_preference,
            recipient_type=None if recipient is None else recipient.recipient_type,
            recipient_id=None if recipient is None else recipient.recipient_id,
            prepared_payload=prepared_payload,
            provider_message_id=provider_message_id,
            result_at=result_at,
            audit_notes=self._dedupe(audit_notes),
        )

    def _blocked_invalid_request(
        self,
        *,
        result_at: datetime,
        contact_id: str | None,
        user_id: str | None,
        channel_preference: str | None,
        audit_notes: Sequence[str],
    ) -> FeishuSandboxDeliveryResult:
        return FeishuSandboxDeliveryResult(
            adapter_name=self.config.adapter_name,
            delivery_status="blocked_invalid_request",
            delivered=False,
            contact_id=contact_id,
            user_id=user_id,
            channel_preference=channel_preference,
            result_at=result_at,
            audit_notes=self._dedupe(audit_notes),
        )

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
        return FeishuSandboxOutboundAdapter._dedupe(list(values))

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
