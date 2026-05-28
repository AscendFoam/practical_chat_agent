"""T222 local fake outbound adapter tests.

All fixtures are synthetic and review-safe. These tests validate the adapter
boundary after T220/T221 without exercising any real platform delivery path.
"""

from __future__ import annotations

from datetime import datetime, timezone

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
from practical_chat_agent.services.outbound_fake_adapter import (
    FakeOutboundAdapterConfig,
    LocalFakeOutboundAdapter,
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
            draft_text="Synthetic outbound draft for fake delivery verification.",
            safe_summary="A review-safe summary of the outbound draft.",
        ),
        "human_approval": _approved_human_approval(),
        "send_gate": _allowed_send_gate(),
        "channel_preference": "feishu",
    }
    data.update(overrides)
    return OutboundMessageRequest(**data)


class TestLocalFakeOutboundAdapter:
    def test_delivers_sendable_request_without_mutation(self) -> None:
        adapter = LocalFakeOutboundAdapter(
            config=FakeOutboundAdapterConfig(
                adapter_name="local_fake_adapter_t222",
                preview_char_limit=24,
            ),
        )
        request = _sendable_request()
        original_updated_at = request.updated_at
        delivered_at = datetime(2026, 5, 28, 12, 0, tzinfo=timezone.utc)

        result = adapter.deliver(request, now=delivered_at)

        assert result.delivery_status == "fake_delivered"
        assert result.delivered is True
        assert result.adapter_name == "local_fake_adapter_t222"
        assert result.request_id == request.request_id
        assert result.contact_id == request.contact_id
        assert result.user_id == request.user_id
        assert result.channel_preference == "feishu"
        assert result.delivered_at == delivered_at
        assert result.payload_preview == "Synthetic outbound dr..."
        assert "request_sendable_verified" in result.audit_notes
        assert "local_fake_delivery_only" in result.audit_notes
        assert request.send_gate.gate_state == "allowed"
        assert request.updated_at == original_updated_at

    def test_accepts_stable_mapping_input(self) -> None:
        adapter = LocalFakeOutboundAdapter()

        result = adapter.deliver(_sendable_request().model_dump())

        assert result.delivery_status == "fake_delivered"
        assert result.delivered is True

    def test_blocks_non_sendable_request(self) -> None:
        adapter = LocalFakeOutboundAdapter()
        request = _sendable_request(send_gate=OutboundRequestSendGate())

        result = adapter.deliver(request)

        assert result.delivery_status == "blocked_not_sendable"
        assert result.delivered is False
        assert "request_not_sendable" in result.audit_notes
        assert "send_gate_not_allowed" in result.audit_notes

    def test_blocks_request_without_explicit_human_approval(self) -> None:
        adapter = LocalFakeOutboundAdapter()
        request = _sendable_request(human_approval=OutboundRequestHumanApproval())

        result = adapter.deliver(request)

        assert result.delivery_status == "blocked_not_sendable"
        assert result.delivered is False
        assert "request_not_sendable" in result.audit_notes
        assert "human_approval_not_approved" in result.audit_notes

    def test_rejects_direct_candidate_action_model(self) -> None:
        adapter = LocalFakeOutboundAdapter()

        result = adapter.deliver(_candidate_action())

        assert result.delivery_status == "blocked_invalid_request"
        assert result.delivered is False
        assert "candidate_action_input_rejected" in result.audit_notes

    def test_rejects_direct_candidate_action_mapping(self) -> None:
        adapter = LocalFakeOutboundAdapter()

        result = adapter.deliver(_candidate_action().model_dump())

        assert result.delivery_status == "blocked_invalid_request"
        assert result.delivered is False
        assert "candidate_action_input_rejected" in result.audit_notes

    def test_rejects_invalid_mapping(self) -> None:
        adapter = LocalFakeOutboundAdapter()

        result = adapter.deliver({"draft_text": "not a request"})

        assert result.delivery_status == "blocked_invalid_request"
        assert result.delivered is False
        assert "request_validation_failed" in result.audit_notes
