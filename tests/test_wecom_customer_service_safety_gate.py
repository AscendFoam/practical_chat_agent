"""T233 WeCom Customer Service provider safety gate tests.

All fixtures are synthetic and review-safe. These tests validate only a local
provider-constraint decision after OutboundSendGate; they do not prepare
provider payloads, call APIs, load credentials, register callbacks, or send.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from practical_chat_agent.core.models import (
    OutboundMessagePayload,
    OutboundMessageRequest,
    OutboundRequestHumanApproval,
    OutboundRequestSendGate,
)
from practical_chat_agent.services.wecom_customer_service_safety import (
    WeComCustomerServiceRecipient,
    WeComCustomerServiceSafetyConfig,
    WeComCustomerServiceSafetyContext,
    WeComCustomerServiceSafetyGate,
)


NOW = datetime(2026, 5, 28, 12, 30, tzinfo=timezone.utc)


def _approved_human_approval() -> OutboundRequestHumanApproval:
    return OutboundRequestHumanApproval(
        review_state="approved",
        approved_by_human=True,
        reviewer_id="reviewer_synthetic",
        reviewed_at=datetime(2026, 5, 28, 9, 0, tzinfo=timezone.utc),
        review_notes=["synthetic outbound approval"],
    )


def _allowed_send_gate() -> OutboundRequestSendGate:
    return OutboundRequestSendGate(
        gate_state="allowed",
        evaluator_id="send_gate_synthetic",
        evaluated_at=datetime(2026, 5, 28, 9, 5, tzinfo=timezone.utc),
        gate_notes=["synthetic gate allowed"],
    )


def _blocked_send_gate() -> OutboundRequestSendGate:
    return OutboundRequestSendGate(
        gate_state="blocked",
        evaluator_id="send_gate_synthetic",
        evaluated_at=datetime(2026, 5, 28, 9, 5, tzinfo=timezone.utc),
        gate_notes=["synthetic gate blocked"],
    )


def _sendable_request(**overrides: object) -> OutboundMessageRequest:
    data: dict[str, object] = {
        "contact_id": "contact_synthetic",
        "user_id": "user_synthetic",
        "source_type": "human_authored",
        "payload": OutboundMessagePayload(
            draft_text="Synthetic outbound draft for WeCom Customer Service review.",
            safe_summary="A review-safe summary of the outbound draft.",
            metadata={"tone": "polite"},
        ),
        "human_approval": _approved_human_approval(),
        "send_gate": _allowed_send_gate(),
        "channel_preference": "wechat",
    }
    data.update(overrides)
    return OutboundMessageRequest(**data)


def _recipient(**overrides: object) -> WeComCustomerServiceRecipient:
    data: dict[str, object] = {
        "contact_id": "contact_synthetic",
        "recipient_alias": "recipient_alias_synthetic",
        "open_kfid_alias": "kf_alias_synthetic",
        "external_user_alias": "external_user_alias_synthetic",
        "service_window_expires_at": NOW + timedelta(hours=1),
        "messages_sent_in_window": 0,
        "manual_send_allowed": True,
    }
    data.update(overrides)
    return WeComCustomerServiceRecipient(**data)


def _context(
    *,
    recipient: WeComCustomerServiceRecipient | None = None,
    existing_audit: list[str] | None = None,
) -> WeComCustomerServiceSafetyContext:
    return WeComCustomerServiceSafetyContext(
        now=NOW,
        recipient_map={} if recipient is None else {recipient.contact_id: recipient},
        existing_audit=existing_audit or [],
    )


class TestWeComCustomerServiceSafetyGate:
    def test_allows_valid_sendable_request_with_active_window(self) -> None:
        gate = WeComCustomerServiceSafetyGate()
        request = _sendable_request()

        decision = gate.evaluate(
            request,
            context=_context(
                recipient=_recipient(),
                existing_audit=["caller_preserved_note"],
            ),
        )

        assert decision.safety_state == "allowed"
        assert decision.reason_codes == []
        assert decision.provider_surface == "wecom_customer_service"
        assert decision.request_id == request.request_id
        assert decision.contact_id == "contact_synthetic"
        assert decision.user_id == "user_synthetic"
        assert decision.recipient_alias == "recipient_alias_synthetic"
        assert decision.open_kfid_alias == "kf_alias_synthetic"
        assert decision.external_user_alias == "external_user_alias_synthetic"
        assert "caller_preserved_note" in decision.audit_notes
        assert "request_sendable_verified" in decision.audit_notes
        assert "provider_eligible_not_delivery" in decision.audit_notes
        assert "provider_payload_not_prepared" in decision.audit_notes

    @pytest.mark.parametrize(
        "outbound_request",
        [
            _sendable_request(human_approval=OutboundRequestHumanApproval()),
            _sendable_request(send_gate=_blocked_send_gate()),
        ],
    )
    def test_non_sendable_request_blocks_before_provider_checks(
        self,
        outbound_request: OutboundMessageRequest,
    ) -> None:
        gate = WeComCustomerServiceSafetyGate(
            config=WeComCustomerServiceSafetyConfig(provider_kill_switch_enabled=True),
        )

        decision = gate.evaluate(outbound_request, context=_context())

        assert decision.safety_state == "blocked"
        assert decision.reason_codes == ["request_not_sendable"]
        assert "missing_recipient_mapping" not in decision.reason_codes
        assert "provider_kill_switch_enabled" not in decision.reason_codes

    def test_missing_recipient_map_blocks(self) -> None:
        decision = WeComCustomerServiceSafetyGate().evaluate(
            _sendable_request(),
            context=_context(),
        )

        assert decision.safety_state == "blocked"
        assert "missing_recipient_mapping" in decision.reason_codes
        assert decision.recipient_alias is None

    @pytest.mark.parametrize("channel_preference", ["unspecified", "feishu"])
    def test_non_wechat_channel_preference_blocks(self, channel_preference: str) -> None:
        decision = WeComCustomerServiceSafetyGate().evaluate(
            _sendable_request(channel_preference=channel_preference),
            context=_context(recipient=_recipient()),
        )

        assert decision.safety_state == "blocked"
        assert "wechat_channel_required" in decision.reason_codes

    def test_missing_wecom_customer_service_surface_config_blocks(self) -> None:
        gate = WeComCustomerServiceSafetyGate(
            config=WeComCustomerServiceSafetyConfig(surface=""),
        )

        decision = gate.evaluate(
            _sendable_request(),
            context=_context(recipient=_recipient()),
        )

        assert decision.safety_state == "blocked"
        assert "provider_surface_missing" in decision.reason_codes

    @pytest.mark.parametrize(
        "config_kwargs",
        [
            {"manual_send_only": False},
            {"proactive_send_disabled": False},
        ],
    )
    def test_config_requires_manual_only_non_proactive_mode(
        self,
        config_kwargs: dict[str, object],
    ) -> None:
        with pytest.raises(ValueError):
            WeComCustomerServiceSafetyConfig(**config_kwargs)

    @pytest.mark.parametrize(
        ("recipient", "reason_code"),
        [
            (_recipient(service_window_expires_at=None), "service_window_missing"),
            (_recipient(service_window_expires_at=NOW), "service_window_expired"),
            (
                _recipient(service_window_expires_at=NOW - timedelta(seconds=1)),
                "service_window_expired",
            ),
        ],
    )
    def test_expired_or_missing_service_window_blocks(
        self,
        recipient: WeComCustomerServiceRecipient,
        reason_code: str,
    ) -> None:
        decision = WeComCustomerServiceSafetyGate().evaluate(
            _sendable_request(),
            context=_context(recipient=recipient),
        )

        assert decision.safety_state == "blocked"
        assert reason_code in decision.reason_codes

    def test_five_message_window_limit_blocks(self) -> None:
        decision = WeComCustomerServiceSafetyGate().evaluate(
            _sendable_request(),
            context=_context(recipient=_recipient(messages_sent_in_window=5)),
        )

        assert decision.safety_state == "blocked"
        assert "message_window_limit_reached" in decision.reason_codes

    def test_provider_kill_switch_blocks(self) -> None:
        gate = WeComCustomerServiceSafetyGate(
            config=WeComCustomerServiceSafetyConfig(provider_kill_switch_enabled=True),
        )

        decision = gate.evaluate(
            _sendable_request(),
            context=_context(recipient=_recipient()),
        )

        assert decision.safety_state == "blocked"
        assert "provider_kill_switch_enabled" in decision.reason_codes

    def test_manual_send_disallowed_blocks(self) -> None:
        decision = WeComCustomerServiceSafetyGate().evaluate(
            _sendable_request(),
            context=_context(recipient=_recipient(manual_send_allowed=False)),
        )

        assert decision.safety_state == "blocked"
        assert "manual_send_not_allowed" in decision.reason_codes

    @pytest.mark.parametrize(
        "metadata_key",
        [
            "external_userid",
            "open_kfid",
            "unionid",
            "corpsecret",
            "encoding_aes_key",
            "callback_token",
            "wecom_external_userid",
            "wecom_open_kfid",
        ],
    )
    def test_provider_identity_or_credential_metadata_keys_block(
        self,
        metadata_key: str,
    ) -> None:
        request = _sendable_request(
            payload=OutboundMessagePayload(
                draft_text="Synthetic outbound draft.",
                metadata={metadata_key: "unsafe-provider-value"},
            ),
        )

        decision = WeComCustomerServiceSafetyGate().evaluate(
            request,
            context=_context(recipient=_recipient()),
        )

        assert decision.safety_state == "blocked"
        assert "provider_metadata_smuggling" in decision.reason_codes
        assert "unsafe-provider-value" not in " ".join(decision.audit_notes)

    def test_mapping_input_validates_same_as_model(self) -> None:
        gate = WeComCustomerServiceSafetyGate()
        request = _sendable_request()
        context = _context(recipient=_recipient())

        model_decision = gate.evaluate(request, context=context)
        mapping_decision = gate.evaluate(request.model_dump(mode="json"), context=context)

        assert mapping_decision.safety_state == model_decision.safety_state
        assert mapping_decision.reason_codes == model_decision.reason_codes
        assert mapping_decision.request_id == model_decision.request_id
        assert mapping_decision.audit_notes == model_decision.audit_notes

    def test_input_outbound_message_request_is_not_mutated(self) -> None:
        gate = WeComCustomerServiceSafetyGate()
        request = _sendable_request()
        before = request.model_dump()

        decision = gate.evaluate(request, context=_context(recipient=_recipient()))

        assert decision.safety_state == "allowed"
        assert request.model_dump() == before
