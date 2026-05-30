from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Literal, Mapping, Sequence

from pydantic import ValidationError

from practical_chat_agent.core.models import OutboundMessageRequest


WeComCustomerServiceSafetyState = Literal["allowed", "blocked"]

WECom_CUSTOMER_SERVICE_SURFACE = "wecom_customer_service"
_PROVIDER_METADATA_SMUGGLING_KEYS = frozenset(
    {
        "external_userid",
        "open_kfid",
        "open_id",
        "unionid",
        "access_token",
        "corpsecret",
        "encoding_aes_key",
        "callback_token",
        "wecom_external_userid",
        "wecom_open_kfid",
    },
)


@dataclass(frozen=True)
class WeComCustomerServiceRecipient:
    """Reviewed recipient alias record for provider safety checks."""

    contact_id: str
    recipient_alias: str
    open_kfid_alias: str
    external_user_alias: str
    service_window_expires_at: datetime | None
    messages_sent_in_window: int = 0
    manual_send_allowed: bool = True

    def __post_init__(self) -> None:
        if not self.contact_id.strip():
            raise ValueError("WeComCustomerServiceRecipient.contact_id must be non-empty.")
        if not self.recipient_alias.strip():
            raise ValueError("WeComCustomerServiceRecipient.recipient_alias must be non-empty.")
        if not self.open_kfid_alias.strip():
            raise ValueError("WeComCustomerServiceRecipient.open_kfid_alias must be non-empty.")
        if not self.external_user_alias.strip():
            raise ValueError("WeComCustomerServiceRecipient.external_user_alias must be non-empty.")
        if self.messages_sent_in_window < 0:
            raise ValueError("messages_sent_in_window must be >= 0.")


@dataclass(frozen=True)
class WeComCustomerServiceSafetyConfig:
    """Local provider-safety settings for WeCom Customer Service."""

    surface: str = WECom_CUSTOMER_SERVICE_SURFACE
    manual_send_only: bool = True
    proactive_send_disabled: bool = True
    provider_kill_switch_enabled: bool = False
    max_messages_per_window: int = 5

    def __post_init__(self) -> None:
        if not self.manual_send_only:
            raise ValueError("WeCom Customer Service safety requires manual_send_only=True.")
        if not self.proactive_send_disabled:
            raise ValueError("WeCom Customer Service safety requires proactive_send_disabled=True.")
        if self.max_messages_per_window < 0:
            raise ValueError("max_messages_per_window must be >= 0.")


@dataclass(frozen=True)
class WeComCustomerServiceSafetyContext:
    """Provider-safety inputs that remain outside outbound payload metadata."""

    now: datetime
    recipient_map: dict[str, WeComCustomerServiceRecipient]
    existing_audit: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.now is None:
            raise ValueError("WeComCustomerServiceSafetyContext.now is required.")
        for contact_id, recipient in self.recipient_map.items():
            if not contact_id.strip():
                raise ValueError("recipient_map keys must be non-empty.")
            if contact_id != recipient.contact_id:
                raise ValueError("recipient_map key must match recipient.contact_id.")


@dataclass(frozen=True)
class WeComCustomerServiceSafetyDecision:
    """Deterministic provider eligibility decision; this is not delivery."""

    safety_state: WeComCustomerServiceSafetyState
    reason_codes: list[str] = field(default_factory=list)
    request_id: str | None = None
    contact_id: str | None = None
    user_id: str | None = None
    recipient_alias: str | None = None
    open_kfid_alias: str | None = None
    external_user_alias: str | None = None
    audit_notes: list[str] = field(default_factory=list)
    provider_surface: str = WECom_CUSTOMER_SERVICE_SURFACE


class WeComCustomerServiceSafetyGate:
    """Pure local provider-constraint gate for WeCom Customer Service."""

    def __init__(self, *, config: WeComCustomerServiceSafetyConfig | None = None) -> None:
        self.config = config or WeComCustomerServiceSafetyConfig()

    def evaluate(
        self,
        request: OutboundMessageRequest | Mapping[str, Any],
        *,
        context: WeComCustomerServiceSafetyContext | Mapping[str, Any],
        existing_audit: Sequence[str] | None = None,
    ) -> WeComCustomerServiceSafetyDecision:
        safety_context = self._coerce_context(context)
        audit_notes = self._dedupe(
            [
                *safety_context.existing_audit,
                *self._clean_audit(existing_audit),
            ],
        )

        try:
            outbound_request = self._coerce_request(request)
        except ValidationError:
            audit_notes.extend(["request_validation_failed", "provider_safety_blocked"])
            return WeComCustomerServiceSafetyDecision(
                safety_state="blocked",
                reason_codes=["request_validation_failed"],
                contact_id=self._mapping_value(request, "contact_id"),
                user_id=self._mapping_value(request, "user_id"),
                audit_notes=self._dedupe(audit_notes),
                provider_surface=self.config.surface,
            )

        audit_notes.append("request_validated")
        if not outbound_request.is_sendable():
            audit_notes.extend(["request_not_sendable", "provider_safety_blocked"])
            return self._decision_from_request(
                outbound_request,
                safety_state="blocked",
                reason_codes=["request_not_sendable"],
                audit_notes=audit_notes,
            )

        audit_notes.append("request_sendable_verified")
        reason_codes: list[str] = []

        if outbound_request.channel_preference != "wechat":
            reason_codes.append("wechat_channel_required")
            audit_notes.append("wechat_channel_required")
        else:
            audit_notes.append("wechat_channel_verified")

        if self.config.surface.strip() != WECom_CUSTOMER_SERVICE_SURFACE:
            reason_codes.append("provider_surface_missing")
            audit_notes.append("provider_surface_missing")
        else:
            audit_notes.append("provider_surface_configured")

        if self.config.provider_kill_switch_enabled:
            reason_codes.append("provider_kill_switch_enabled")
            audit_notes.append("provider_kill_switch_enabled")
        else:
            audit_notes.append("provider_kill_switch_clear")

        smuggled_keys = self._provider_metadata_smuggling_keys(outbound_request)
        if smuggled_keys:
            reason_codes.append("provider_metadata_smuggling")
            audit_notes.append("provider_metadata_smuggling_blocked")
        else:
            audit_notes.append("provider_metadata_clear")

        recipient = safety_context.recipient_map.get(outbound_request.contact_id)
        if recipient is None:
            reason_codes.append("missing_recipient_mapping")
            audit_notes.append("missing_recipient_mapping")
            return self._decision_from_request(
                outbound_request,
                safety_state="blocked",
                reason_codes=reason_codes,
                audit_notes=[*audit_notes, "provider_safety_blocked"],
            )

        audit_notes.append("recipient_mapping_verified")
        if not recipient.manual_send_allowed:
            reason_codes.append("manual_send_not_allowed")
            audit_notes.append("manual_send_not_allowed")
        else:
            audit_notes.append("manual_send_allowed")

        if recipient.service_window_expires_at is None:
            reason_codes.append("service_window_missing")
            audit_notes.append("service_window_missing")
        elif self._as_aware_utc(recipient.service_window_expires_at) <= self._as_aware_utc(
            safety_context.now,
        ):
            reason_codes.append("service_window_expired")
            audit_notes.append("service_window_expired")
        else:
            audit_notes.append("service_window_active")

        if recipient.messages_sent_in_window >= self.config.max_messages_per_window:
            reason_codes.append("message_window_limit_reached")
            audit_notes.append("message_window_limit_reached")
        else:
            audit_notes.append("message_window_quota_clear")

        reason_codes = self._dedupe(reason_codes)
        safety_state: WeComCustomerServiceSafetyState = "blocked" if reason_codes else "allowed"
        if safety_state == "allowed":
            audit_notes.extend(
                [
                    "provider_eligible_not_delivery",
                    "provider_payload_not_prepared",
                    "provider_safety_allowed",
                ],
            )
        else:
            audit_notes.extend(["provider_payload_not_prepared", "provider_safety_blocked"])

        return self._decision_from_request(
            outbound_request,
            safety_state=safety_state,
            reason_codes=reason_codes,
            audit_notes=audit_notes,
            recipient=recipient,
        )

    @staticmethod
    def _coerce_request(request: OutboundMessageRequest | Mapping[str, Any]) -> OutboundMessageRequest:
        if isinstance(request, OutboundMessageRequest):
            return request
        return OutboundMessageRequest.model_validate(dict(request))

    @staticmethod
    def _coerce_context(
        context: WeComCustomerServiceSafetyContext | Mapping[str, Any],
    ) -> WeComCustomerServiceSafetyContext:
        if isinstance(context, WeComCustomerServiceSafetyContext):
            return context
        data = dict(context)
        recipient_map = {
            contact_id: recipient
            if isinstance(recipient, WeComCustomerServiceRecipient)
            else WeComCustomerServiceRecipient(**dict(recipient))
            for contact_id, recipient in dict(data.get("recipient_map", {})).items()
        }
        return WeComCustomerServiceSafetyContext(
            now=data["now"],
            recipient_map=recipient_map,
            existing_audit=list(data.get("existing_audit", [])),
        )

    def _decision_from_request(
        self,
        request: OutboundMessageRequest,
        *,
        safety_state: WeComCustomerServiceSafetyState,
        reason_codes: Sequence[str],
        audit_notes: Sequence[str],
        recipient: WeComCustomerServiceRecipient | None = None,
    ) -> WeComCustomerServiceSafetyDecision:
        return WeComCustomerServiceSafetyDecision(
            safety_state=safety_state,
            reason_codes=self._dedupe(list(reason_codes)),
            request_id=request.request_id,
            contact_id=request.contact_id,
            user_id=request.user_id,
            recipient_alias=None if recipient is None else recipient.recipient_alias,
            open_kfid_alias=None if recipient is None else recipient.open_kfid_alias,
            external_user_alias=None if recipient is None else recipient.external_user_alias,
            audit_notes=self._dedupe(list(audit_notes)),
            provider_surface=self.config.surface,
        )

    @staticmethod
    def _provider_metadata_smuggling_keys(request: OutboundMessageRequest) -> list[str]:
        keys = {
            str(key).casefold()
            for key in request.payload.metadata
            if isinstance(key, str) and key.strip()
        }
        return sorted(_PROVIDER_METADATA_SMUGGLING_KEYS.intersection(keys))

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
        return WeComCustomerServiceSafetyGate._dedupe(list(values))

    @staticmethod
    def _mapping_value(request: OutboundMessageRequest | Mapping[str, Any], key: str) -> str | None:
        if isinstance(request, Mapping):
            value = request.get(key)
            if isinstance(value, str) and value.strip():
                return value
        return None
