"""T223 Feishu sandbox outbound adapter tests.

All fixtures are synthetic and review-safe. These tests validate a Feishu-
specific sandbox adapter boundary without any real platform delivery.
"""

from __future__ import annotations

from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from practical_chat_agent.core.models import (
    CandidateAction,
    CandidateActionPayload,
    DistilledArtifactReviewMetadata,
    OutboundMessagePayload,
    OutboundMessageRequest,
    OutboundRequestHumanApproval,
    OutboundRequestSendGate,
    ReplyPlanContextRef,
)
from practical_chat_agent.services.feishu_outbound_adapter import (
    FeishuSandboxAdapterConfig,
    FeishuSandboxOutboundAdapter,
    FeishuSandboxRecipient,
    FeishuSandboxTransportResponse,
)


def _ref(ref_id: str = "memstore_synthetic_001") -> ReplyPlanContextRef:
    return ReplyPlanContextRef(
        ref_type="approved_memory_fact_record",
        ref_id=ref_id,
        note="synthetic approved evidence",
    )


def _reviewed_candidate_metadata() -> DistilledArtifactReviewMetadata:
    return DistilledArtifactReviewMetadata(
        review_state="reviewed",
        reviewed_by_human=True,
        last_decision="approved",
        evidence_validation_status="passed",
    )


def _candidate_action() -> CandidateAction:
    return CandidateAction(
        contact_id="contact_synthetic",
        user_id="user_synthetic",
        action_type="relationship_check_in_draft",
        title="Review-safe check-in draft",
        rationale="Approved context suggests a low-pressure check-in draft.",
        supporting_context_refs=[_ref("skillstore_synthetic_001")],
        payload=CandidateActionPayload(
            safe_summary="Synthetic review-safe check-in idea.",
            draft_text="A short synthetic draft.",
        ),
        status="approved",
        review_metadata=_reviewed_candidate_metadata(),
    )


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


def _sendable_request(**overrides: object) -> OutboundMessageRequest:
    data: dict[str, object] = {
        "contact_id": "contact_synthetic",
        "user_id": "user_synthetic",
        "source_type": "human_authored",
        "payload": OutboundMessagePayload(
            draft_text="Synthetic outbound draft for Feishu sandbox delivery.",
            safe_summary="A review-safe summary of the outbound draft.",
        ),
        "human_approval": _approved_human_approval(),
        "send_gate": _allowed_send_gate(),
        "channel_preference": "feishu",
    }
    data.update(overrides)
    return OutboundMessageRequest(**data)


def _config(**overrides: object) -> FeishuSandboxAdapterConfig:
    data: dict[str, object] = {
        "adapter_name": "feishu_sandbox_adapter_t223",
        "dry_run_by_default": True,
        "recipient_map": {
            "contact_synthetic": FeishuSandboxRecipient(
                recipient_type="open_id",
                recipient_id="ou_synthetic_001",
            ),
        },
    }
    data.update(overrides)
    return FeishuSandboxAdapterConfig(**data)


class _FakeTransport:
    def __init__(
        self,
        *,
        response: FeishuSandboxTransportResponse | None = None,
        error: Exception | None = None,
    ) -> None:
        self.calls: list[dict[str, object]] = []
        self.response = response or FeishuSandboxTransportResponse(
            provider_message_id="msg_sandbox_001",
            audit_notes=["fake_transport_acknowledged"],
        )
        self.error = error

    def send(self, payload: dict[str, object]) -> FeishuSandboxTransportResponse:
        self.calls.append(payload)
        if self.error is not None:
            raise self.error
        return self.response


class TestFeishuSandboxOutboundAdapter:
    def test_rejects_non_sendable_request_without_invoking_transport(self) -> None:
        transport = _FakeTransport()
        adapter = FeishuSandboxOutboundAdapter(config=_config(), transport=transport)
        request = _sendable_request(send_gate=OutboundRequestSendGate())

        result = adapter.deliver(request, dry_run=False)

        assert result.delivery_status == "blocked_not_sendable"
        assert result.delivered is False
        assert transport.calls == []
        assert "request_not_sendable" in result.audit_notes

    def test_rejects_direct_candidate_action_input(self) -> None:
        adapter = FeishuSandboxOutboundAdapter(config=_config())

        result = adapter.deliver(_candidate_action())

        assert result.delivery_status == "blocked_invalid_request"
        assert result.delivered is False
        assert "candidate_action_input_rejected" in result.audit_notes

    def test_rejects_candidate_shaped_mapping(self) -> None:
        adapter = FeishuSandboxOutboundAdapter(config=_config())

        result = adapter.deliver(_candidate_action().model_dump())

        assert result.delivery_status == "blocked_invalid_request"
        assert result.delivered is False
        assert "candidate_action_input_rejected" in result.audit_notes

    def test_blocks_missing_feishu_recipient_mapping(self) -> None:
        adapter = FeishuSandboxOutboundAdapter(
            config=_config(recipient_map={}),
        )

        result = adapter.deliver(_sendable_request())

        assert result.delivery_status == "blocked_missing_recipient"
        assert result.delivered is False
        assert "feishu_recipient_missing" in result.audit_notes

    @pytest.mark.parametrize("channel", ["unspecified", "wechat"])
    def test_blocks_incompatible_channel_preference(self, channel: str) -> None:
        adapter = FeishuSandboxOutboundAdapter(config=_config())

        result = adapter.deliver(_sendable_request(channel_preference=channel))

        assert result.delivery_status == "blocked_wrong_channel"
        assert result.delivered is False
        assert "feishu_channel_incompatible" in result.audit_notes

    def test_dry_run_prepares_expected_payload_without_invoking_transport(self) -> None:
        transport = _FakeTransport()
        adapter = FeishuSandboxOutboundAdapter(config=_config(), transport=transport)
        request = _sendable_request()
        now = datetime(2026, 5, 28, 12, 30, tzinfo=timezone.utc)

        result = adapter.deliver(
            request,
            now=now,
            existing_audit=["caller_note", "local_fake_delivery_only"],
        )

        assert result.delivery_status == "feishu_dry_run_ready"
        assert result.delivered is False
        assert result.result_at == now
        assert result.recipient_type == "open_id"
        assert result.recipient_id == "ou_synthetic_001"
        assert result.provider_message_id is None
        assert transport.calls == []
        assert result.prepared_payload == {
            "receive_id_type": "open_id",
            "receive_id": "ou_synthetic_001",
            "msg_type": "text",
            "content": {"text": "Synthetic outbound draft for Feishu sandbox delivery."},
        }
        assert "caller_note" in result.audit_notes
        assert "local_fake_delivery_only" in result.audit_notes
        assert "gate_allowed_verified" in result.audit_notes
        assert "feishu_sandbox_payload_prepared" in result.audit_notes
        assert "feishu_dry_run_only" in result.audit_notes
        assert "no_production_delivery" in result.audit_notes
        assert request.send_gate.gate_state == "allowed"

    def test_fake_transport_is_invoked_only_when_dry_run_disabled(self) -> None:
        transport = _FakeTransport()
        adapter = FeishuSandboxOutboundAdapter(config=_config(), transport=transport)

        result = adapter.deliver(_sendable_request(), dry_run=False)

        assert result.delivery_status == "feishu_sandbox_sent"
        assert result.delivered is True
        assert result.provider_message_id == "msg_sandbox_001"
        assert len(transport.calls) == 1
        assert transport.calls[0]["msg_type"] == "text"
        assert "feishu_sandbox_transport_invoked" in result.audit_notes
        assert "fake_transport_acknowledged" in result.audit_notes

    def test_transport_failure_returns_deterministic_blocked_result_without_mutation(self) -> None:
        transport = _FakeTransport(error=RuntimeError("synthetic transport failure"))
        adapter = FeishuSandboxOutboundAdapter(config=_config(), transport=transport)
        request = _sendable_request()
        original_updated_at = request.updated_at

        result = adapter.deliver(request, dry_run=False)

        assert result.delivery_status == "blocked_transport_error"
        assert result.delivered is False
        assert result.provider_message_id is None
        assert len(transport.calls) == 1
        assert "feishu_sandbox_transport_failed" in result.audit_notes
        assert request.updated_at == original_updated_at

    def test_payload_construction_uses_outbound_draft_text_not_safe_metadata(self) -> None:
        adapter = FeishuSandboxOutboundAdapter(config=_config())
        request = _sendable_request(
            payload=OutboundMessagePayload(
                draft_text="Approved outbound draft text wins.",
                metadata={"text": "unsafe metadata override"},
            ),
        )

        result = adapter.deliver(request)

        assert result.prepared_payload is not None
        assert result.prepared_payload["content"] == {"text": "Approved outbound draft text wins."}

    @pytest.mark.parametrize(
        "forbidden_key",
        [
            "adapter_payload",
            "bot_token",
            "webhook_url",
            "platform_target",
            "open_id",
            "chat_id",
            "receive_id",
        ],
    )
    def test_payload_metadata_rejects_feishu_target_and_secret_fields(self, forbidden_key: str) -> None:
        with pytest.raises(ValidationError):
            OutboundMessagePayload(
                draft_text="Synthetic outbound draft.",
                metadata={forbidden_key: "unsafe"},
            )
