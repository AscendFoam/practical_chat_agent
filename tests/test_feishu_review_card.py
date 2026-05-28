"""T224 Feishu review card tests.

All fixtures are synthetic and review-safe. These tests validate review-card
rendering and inert review-intent parsing only; they do not apply approval,
invoke adapters, or perform any platform delivery.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone

import pytest

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
)
from practical_chat_agent.services.feishu_review_card import (
    FeishuReviewCardBuilder,
    FeishuReviewCardConfig,
    FeishuReviewIntentParser,
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


def _blocked_send_gate() -> OutboundRequestSendGate:
    return OutboundRequestSendGate(
        gate_state="blocked",
        evaluator_id="send_gate_synthetic",
        evaluated_at=datetime(2026, 5, 28, 9, 5, tzinfo=timezone.utc),
        gate_notes=["gate_blocked", "quiet_hours_blocked"],
    )


def _request(**overrides: object) -> OutboundMessageRequest:
    data: dict[str, object] = {
        "contact_id": "contact_synthetic",
        "user_id": "user_synthetic",
        "source_type": "human_authored",
        "payload": OutboundMessagePayload(
            draft_text="Synthetic outbound draft for review-card rendering.",
            safe_summary="A review-safe summary of the outbound draft.",
        ),
        "channel_preference": "feishu",
    }
    data.update(overrides)
    return OutboundMessageRequest(**data)


def _adapter_config() -> FeishuSandboxAdapterConfig:
    return FeishuSandboxAdapterConfig(
        adapter_name="feishu_sandbox_adapter_t223",
        dry_run_by_default=True,
        recipient_map={
            "contact_synthetic": FeishuSandboxRecipient(
                recipient_type="open_id",
                recipient_id="ou_synthetic_001",
            ),
        },
    )


class _FakeTransport:
    def __init__(self) -> None:
        self.calls: list[dict[str, object]] = []

    def send(self, payload: dict[str, object]) -> object:
        self.calls.append(payload)
        raise AssertionError("review-card rendering must not call transport")


def _button_values(card_payload: dict[str, object]) -> dict[str, dict[str, str]]:
    for element in card_payload["elements"]:
        if element["tag"] != "action":
            continue
        return {
            action["text"]["content"]: action["value"]
            for action in element["actions"]
        }
    raise AssertionError("action button group not found")


class TestFeishuReviewCardBuilder:
    def test_renders_pending_non_sendable_request_card(self) -> None:
        builder = FeishuReviewCardBuilder()

        result = builder.render(_request())

        assert result.render_status == "card_rendered"
        assert result.rendered is True
        assert result.sendable is False
        assert result.card_payload is not None
        serialized = json.dumps(result.card_payload, ensure_ascii=False)
        assert "pending_human_approval" in serialized
        assert "not_evaluated" in serialized
        assert "false" in serialized

    def test_renders_sendable_feishu_outbound_request_card(self) -> None:
        builder = FeishuReviewCardBuilder()
        request = _request(
            human_approval=_approved_human_approval(),
            send_gate=_allowed_send_gate(),
            risk_flags=["boundary_sensitive"],
        )

        result = builder.render(request)

        assert result.render_status == "card_rendered"
        assert result.rendered is True
        assert result.sendable is True
        serialized = json.dumps(result.card_payload, ensure_ascii=False)
        assert request.request_id in serialized
        assert "approved" in serialized
        assert "allowed" in serialized
        assert "boundary_sensitive" in serialized

    def test_renders_blocked_gate_state_without_implying_delivery(self) -> None:
        builder = FeishuReviewCardBuilder()
        request = _request(
            human_approval=_approved_human_approval(),
            send_gate=_blocked_send_gate(),
        )

        result = builder.render(request)

        assert result.render_status == "card_rendered"
        assert result.sendable is False
        serialized = json.dumps(result.card_payload, ensure_ascii=False)
        assert "blocked" in serialized
        assert "quiet_hours_blocked" in serialized
        assert "feishu_sandbox_sent" not in serialized

    def test_renders_optional_feishu_sandbox_result_summary(self) -> None:
        transport = _FakeTransport()
        adapter = FeishuSandboxOutboundAdapter(
            config=_adapter_config(),
            transport=transport,
        )
        request = _request(
            human_approval=_approved_human_approval(),
            send_gate=_allowed_send_gate(),
        )
        sandbox_result = adapter.deliver(request)
        builder = FeishuReviewCardBuilder()

        result = builder.render(request, sandbox_result=sandbox_result)

        assert transport.calls == []
        serialized = json.dumps(result.card_payload, ensure_ascii=False)
        assert "feishu_dry_run_ready" in serialized
        assert "Sandbox Result" in serialized
        assert "no_production_delivery" in serialized

    def test_rejects_direct_candidate_action_input(self) -> None:
        builder = FeishuReviewCardBuilder()

        result = builder.render(_candidate_action())

        assert result.render_status == "blocked_invalid_request"
        assert result.rendered is False
        assert "candidate_action_input_rejected" in result.audit_notes

    def test_rejects_candidate_shaped_mapping(self) -> None:
        builder = FeishuReviewCardBuilder()

        result = builder.render(_candidate_action().model_dump())

        assert result.render_status == "blocked_invalid_request"
        assert result.rendered is False
        assert "candidate_action_input_rejected" in result.audit_notes

    def test_rendering_does_not_mutate_input_request(self) -> None:
        builder = FeishuReviewCardBuilder()
        request = _request(
            human_approval=_approved_human_approval(),
            send_gate=_allowed_send_gate(),
        )
        original_updated_at = request.updated_at
        original_gate_notes = list(request.send_gate.gate_notes)

        builder.render(request)

        assert request.updated_at == original_updated_at
        assert request.send_gate.gate_notes == original_gate_notes

    def test_forbidden_recipient_metadata_keys_are_absent_from_card_output(self) -> None:
        builder = FeishuReviewCardBuilder()
        request = _request(
            payload=OutboundMessagePayload(
                draft_text="Synthetic outbound draft for review-card rendering.",
                safe_summary="Review-safe summary.",
                metadata={"tone": "polite", "length_hint": "short"},
            ),
        )

        result = builder.render(request)

        serialized = json.dumps(result.card_payload, ensure_ascii=False)
        assert "open_id" not in serialized
        assert "chat_id" not in serialized
        assert "receive_id" not in serialized
        assert "feishu_open_id" not in serialized
        assert "feishu_chat_id" not in serialized
        assert '"metadata"' not in serialized

    def test_display_truncation_and_exact_boundary_behavior(self) -> None:
        builder = FeishuReviewCardBuilder(
            config=FeishuReviewCardConfig(draft_preview_char_limit=10),
        )
        exact_request = _request(
            payload=OutboundMessagePayload(draft_text="1234567890"),
        )
        long_request = _request(
            payload=OutboundMessagePayload(draft_text="12345678901"),
        )

        exact_result = builder.render(exact_request)
        long_result = builder.render(long_request)

        exact_serialized = json.dumps(exact_result.card_payload, ensure_ascii=False)
        long_serialized = json.dumps(long_result.card_payload, ensure_ascii=False)
        assert "1234567890" in exact_serialized
        assert "1234567..." in long_serialized

    def test_action_values_are_deterministic_for_all_review_buttons(self) -> None:
        builder = FeishuReviewCardBuilder()
        request = _request()

        result = builder.render(request)
        button_values = _button_values(result.card_payload)

        assert button_values == {
            "Approve": {
                "schema_version": "feishu_review_intent_v1",
                "request_id": request.request_id,
                "action": "approve",
            },
            "Request Edit": {
                "schema_version": "feishu_review_intent_v1",
                "request_id": request.request_id,
                "action": "request_edit",
            },
            "Reject": {
                "schema_version": "feishu_review_intent_v1",
                "request_id": request.request_id,
                "action": "reject",
            },
            "Boundary Feedback": {
                "schema_version": "feishu_review_intent_v1",
                "request_id": request.request_id,
                "action": "boundary_feedback",
            },
        }


class TestFeishuReviewIntentParser:
    @pytest.mark.parametrize(
        "action",
        ["approve", "request_edit", "reject", "boundary_feedback"],
    )
    def test_parses_valid_review_actions(self, action: str) -> None:
        parser = FeishuReviewIntentParser()
        request = _request()
        action_payload = {
            "action": {
                "value": {
                    "schema_version": "feishu_review_intent_v1",
                    "request_id": request.request_id,
                    "action": action,
                },
            },
        }

        result = parser.parse(action_payload, expected_request_id=request.request_id)

        assert result.parse_status == "intent_parsed"
        assert result.accepted is True
        assert result.intent is not None
        assert result.intent.request_id == request.request_id
        assert result.intent.action == action

    def test_rejects_malformed_action_payload(self) -> None:
        parser = FeishuReviewIntentParser()

        result = parser.parse({"action": {"value": "not-a-mapping"}})

        assert result.parse_status == "blocked_invalid_action"
        assert result.accepted is False
        assert "malformed_action_value" in result.audit_notes

    def test_rejects_missing_request_id(self) -> None:
        parser = FeishuReviewIntentParser()

        result = parser.parse(
            {
                "action": {
                    "value": {
                        "schema_version": "feishu_review_intent_v1",
                        "action": "approve",
                    },
                },
            },
        )

        assert result.parse_status == "blocked_invalid_action"
        assert result.accepted is False
        assert "missing_request_id" in result.audit_notes

    def test_rejects_unknown_action(self) -> None:
        parser = FeishuReviewIntentParser()

        result = parser.parse(
            {
                "action": {
                    "value": {
                        "schema_version": "feishu_review_intent_v1",
                        "request_id": "outreq_synthetic",
                        "action": "send_now",
                    },
                },
            },
        )

        assert result.parse_status == "blocked_invalid_action"
        assert result.accepted is False
        assert "unknown_review_action" in result.audit_notes

    def test_rejects_missing_schema_version(self) -> None:
        parser = FeishuReviewIntentParser()

        result = parser.parse(
            {
                "action": {
                    "value": {
                        "request_id": "outreq_synthetic",
                        "action": "approve",
                    },
                },
            },
        )

        assert result.parse_status == "blocked_invalid_action"
        assert result.accepted is False
        assert "missing_schema_version" in result.audit_notes

    def test_rejects_cross_request_action_payload(self) -> None:
        parser = FeishuReviewIntentParser()
        request = _request()

        result = parser.parse(
            {
                "action": {
                    "value": {
                        "schema_version": "feishu_review_intent_v1",
                        "request_id": "outreq_other",
                        "action": "approve",
                    },
                },
            },
            expected_request_id=request.request_id,
        )

        assert result.parse_status == "blocked_invalid_action"
        assert result.accepted is False
        assert "request_id_mismatch" in result.audit_notes
