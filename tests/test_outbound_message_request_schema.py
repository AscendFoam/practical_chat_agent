"""T220 outbound request schema tests.

All fixtures are synthetic and review-safe. These tests define the opening
M11 outbound request boundary only; they do not exercise send-gate logic,
platform adapters, scheduling, runtime loops, or private transcript access.
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


def _approved_candidate_action() -> CandidateAction:
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


def _make_request(**overrides: object) -> OutboundMessageRequest:
    data: dict[str, object] = {
        "contact_id": "contact_synthetic",
        "user_id": "user_synthetic",
        "source_type": "human_authored",
        "payload": OutboundMessagePayload(
            draft_text="Synthetic outbound draft for human review.",
            safe_summary="A review-safe summary of the draft request.",
        ),
    }
    data.update(overrides)
    return OutboundMessageRequest(**data)


def _approved_outbound_human_approval() -> OutboundRequestHumanApproval:
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


class TestOutboundMessagePayload:
    def test_minimal_payload_requires_only_draft_text(self) -> None:
        payload = OutboundMessagePayload(draft_text="Synthetic outbound draft.")
        assert payload.draft_text == "Synthetic outbound draft."
        assert payload.safe_summary is None
        assert payload.metadata == {}

    def test_payload_preserves_review_safe_metadata(self) -> None:
        payload = OutboundMessagePayload(
            draft_text="Synthetic outbound draft.",
            metadata={"tone": "polite", "length_hint": "short"},
        )
        assert payload.metadata == {"tone": "polite", "length_hint": "short"}

    def test_payload_rejects_execution_scheduler_and_private_keys(self) -> None:
        forbidden_keys = [
            "send_at",
            "scheduled_at",
            "scheduler_id",
            "timer_id",
            "adapter_payload",
            "platform_target",
            "bot_token",
            "app_secret",
            "delivery_connector_name",
            "delivery_response",
            "send_result",
            "channel_id",
            "webhook_url",
            "access_token",
            "api_key",
            "raw_transcript",
            "chat_history",
            "private_messages",
        ]
        for key in forbidden_keys:
            with pytest.raises(ValidationError):
                OutboundMessagePayload(
                    draft_text="Synthetic outbound draft.",
                    metadata={key: "unsafe"},
                )


class TestOutboundRequestHumanApproval:
    def test_approved_review_requires_reviewer_metadata(self) -> None:
        with pytest.raises(ValidationError):
            OutboundRequestHumanApproval(
                review_state="approved",
                approved_by_human=True,
            )

    def test_rejected_review_requires_reviewer_metadata(self) -> None:
        with pytest.raises(ValidationError):
            OutboundRequestHumanApproval(
                review_state="rejected",
                approved_by_human=False,
            )


class TestOutboundRequestSendGate:
    def test_allowed_gate_requires_evaluator_metadata(self) -> None:
        with pytest.raises(ValidationError):
            OutboundRequestSendGate(gate_state="allowed")

    def test_blocked_gate_requires_evaluator_metadata(self) -> None:
        with pytest.raises(ValidationError):
            OutboundRequestSendGate(gate_state="blocked")


class TestOutboundMessageRequest:
    def test_minimal_request_is_inert_until_human_approval_and_gate(self) -> None:
        request = _make_request()
        assert request.schema_version == "outbound_message_request_v1"
        assert request.request_id.startswith("outreq_")
        assert request.channel_preference == "unspecified"
        assert request.source_type == "human_authored"
        assert request.source_candidate_action_id is None
        assert request.human_approval.review_state == "pending_human_approval"
        assert request.human_approval.approved_by_human is False
        assert request.send_gate.gate_state == "not_evaluated"
        assert request.is_sendable() is False

    def test_request_becomes_sendable_only_with_explicit_approval_and_gate_allow(self) -> None:
        request = _make_request(
            human_approval=_approved_outbound_human_approval(),
            send_gate=_allowed_send_gate(),
        )
        assert request.is_sendable() is True

    def test_rich_request_preserves_candidate_action_evidence_and_safe_refs(self) -> None:
        candidate = _approved_candidate_action()
        request = _make_request(
            source_type="candidate_action",
            source_candidate_action_id=candidate.action_id,
            source_context_refs=[_ref("approved_evidence_001"), _ref("approved_evidence_002")],
            channel_preference="feishu",
            risk_flags=["boundary_sensitive"],
            payload=OutboundMessagePayload(
                draft_text="Synthetic reviewed draft text.",
                safe_summary="Carries synthetic approved evidence refs.",
                metadata={"tone": "low_pressure"},
            ),
        )
        assert request.source_candidate_action_id == candidate.action_id
        assert [ref.ref_id for ref in request.source_context_refs] == [
            "approved_evidence_001",
            "approved_evidence_002",
        ]
        assert request.channel_preference == "feishu"
        assert request.risk_flags == ["boundary_sensitive"]
        assert request.is_sendable() is False

    def test_candidate_action_approval_is_not_enough_to_make_request_sendable(self) -> None:
        candidate = _approved_candidate_action()
        assert candidate.is_runtime_visible() is True
        request = _make_request(
            source_type="candidate_action",
            source_candidate_action_id=candidate.action_id,
            payload=OutboundMessagePayload(draft_text="Synthetic outbound draft from reviewed candidate."),
        )
        assert request.human_approval.review_state == "pending_human_approval"
        assert request.send_gate.gate_state == "not_evaluated"
        assert request.is_sendable() is False

    def test_candidate_action_source_requires_candidate_action_id(self) -> None:
        with pytest.raises(ValidationError):
            _make_request(source_type="candidate_action", source_candidate_action_id=None)

    def test_human_authored_source_rejects_candidate_action_id(self) -> None:
        with pytest.raises(ValidationError):
            _make_request(
                source_type="human_authored",
                source_candidate_action_id="candact_synthetic_001",
            )

    def test_request_rejects_fake_sendable_state_without_human_approval_and_gate(self) -> None:
        with pytest.raises(ValidationError):
            _make_request(
                human_approval={
                    "review_state": "approved",
                    "approved_by_human": True,
                },
            )
        with pytest.raises(ValidationError):
            _make_request(
                send_gate={
                    "gate_state": "allowed",
                },
            )

    def test_request_json_round_trip(self) -> None:
        request = _make_request(
            source_context_refs=[_ref("approved_evidence_010")],
            payload=OutboundMessagePayload(
                draft_text="Synthetic outbound draft.",
                safe_summary="Synthetic safe summary.",
                metadata={"tone": "polite"},
            ),
        )
        restored = OutboundMessageRequest.model_validate_json(request.model_dump_json())
        assert restored.request_id == request.request_id
        assert restored.contact_id == request.contact_id
        assert restored.user_id == request.user_id
        assert restored.payload.draft_text == request.payload.draft_text
        assert restored.source_context_refs[0].ref_id == "approved_evidence_010"
        assert restored.created_at == request.created_at
        assert restored.updated_at == request.updated_at

    @pytest.mark.parametrize("channel", ["unspecified", "feishu", "wechat"])
    def test_request_accepts_all_supported_channel_preferences(self, channel: str) -> None:
        request = _make_request(channel_preference=channel)
        assert request.channel_preference == channel

    def test_request_has_no_scheduler_or_platform_adapter_fields(self) -> None:
        request = _make_request()
        assert not hasattr(request, "send_at")
        assert not hasattr(request, "scheduled_at")
        assert not hasattr(request, "channel_id")
        assert not hasattr(request, "platform_target")
        assert not hasattr(request, "adapter_payload")
