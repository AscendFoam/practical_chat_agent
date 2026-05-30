"""T232 WeCom Customer Service dry-run outbound adapter tests.

All fixtures are synthetic and review-safe. These tests validate only local
dry-run payload preparation behind OutboundSendGate and the T233 safety gate;
they do not call provider APIs, load credentials, add transports, or send.
"""

from __future__ import annotations

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
from practical_chat_agent.services.wecom_customer_service_outbound_adapter import (
    WeComCustomerServiceDryRunConfig,
    WeComCustomerServiceDryRunOutboundAdapter,
)
from practical_chat_agent.services.wecom_customer_service_safety import (
    WeComCustomerServiceSafetyDecision,
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
        gate_notes=["synthetic gate blocked"],
    )


def _sendable_request(**overrides: object) -> OutboundMessageRequest:
    data: dict[str, object] = {
        "contact_id": "contact_synthetic",
        "user_id": "user_synthetic",
        "source_type": "human_authored",
        "payload": OutboundMessagePayload(
            draft_text="Synthetic outbound draft for WeCom dry run.",
            safe_summary="A review-safe summary of the outbound draft.",
            metadata={"tone": "polite", "do_not_copy": "metadata must stay outside payload"},
        ),
        "human_approval": _approved_human_approval(),
        "send_gate": _allowed_send_gate(),
        "channel_preference": "wechat",
    }
    data.update(overrides)
    return OutboundMessageRequest(**data)


def _allowed_safety_decision(**overrides: object) -> WeComCustomerServiceSafetyDecision:
    data: dict[str, object] = {
        "safety_state": "allowed",
        "reason_codes": [],
        "request_id": "request-id-replaced-by-helper",
        "contact_id": "contact_synthetic",
        "user_id": "user_synthetic",
        "recipient_alias": "recipient_alias_synthetic",
        "open_kfid_alias": "kf_alias_synthetic",
        "external_user_alias": "external_user_alias_synthetic",
        "audit_notes": [
            "caller_safety_note",
            "provider_eligible_not_delivery",
            "provider_payload_not_prepared",
        ],
        "provider_surface": "wecom_customer_service",
    }
    data.update(overrides)
    return WeComCustomerServiceSafetyDecision(**data)


def _matching_safety_decision(
    request: OutboundMessageRequest,
    **overrides: object,
) -> WeComCustomerServiceSafetyDecision:
    data: dict[str, object] = {
        "request_id": request.request_id,
        "contact_id": request.contact_id,
        "user_id": request.user_id,
    }
    data.update(overrides)
    return _allowed_safety_decision(**data)


class TestWeComCustomerServiceDryRunOutboundAdapter:
    def test_config_requires_dry_run_only(self) -> None:
        with pytest.raises(ValueError):
            WeComCustomerServiceDryRunConfig(dry_run_only=False)

    def test_allowed_request_and_safety_decision_prepare_expected_dry_run_payload(self) -> None:
        adapter = WeComCustomerServiceDryRunOutboundAdapter()
        request = _sendable_request()
        safety_decision = _matching_safety_decision(request)

        result = adapter.prepare_dry_run(
            request,
            safety_decision=safety_decision,
            existing_audit=["caller_note", "caller_safety_note"],
        )

        assert result.delivery_status == "wecom_dry_run_ready"
        assert result.delivered is False
        assert result.request_id == request.request_id
        assert result.contact_id == "contact_synthetic"
        assert result.user_id == "user_synthetic"
        assert result.provider_surface == "wecom_customer_service"
        assert result.recipient_alias == "recipient_alias_synthetic"
        assert result.open_kfid_alias == "kf_alias_synthetic"
        assert result.external_user_alias == "external_user_alias_synthetic"
        assert result.prepared_payload == {
            "provider_surface": "wecom_customer_service",
            "dry_run": True,
            "request_id": request.request_id,
            "contact_id": "contact_synthetic",
            "user_id": "user_synthetic",
            "recipient_aliases": {
                "recipient_alias": "recipient_alias_synthetic",
                "open_kfid_alias": "kf_alias_synthetic",
                "external_user_alias": "external_user_alias_synthetic",
            },
            "message": {
                "msg_type": "text",
                "text": "Synthetic outbound draft for WeCom dry run.",
            },
            "safe_summary": "A review-safe summary of the outbound draft.",
            "source": {
                "source_type": "human_authored",
                "source_candidate_action_id": None,
            },
        }
        assert "caller_note" in result.audit_notes
        assert result.audit_notes.count("caller_safety_note") == 1
        assert "provider_eligible_not_delivery" in result.audit_notes
        assert "provider_payload_not_prepared" in result.audit_notes
        assert "request_sendable_verified" in result.audit_notes
        assert "wecom_safety_decision_verified" in result.audit_notes
        assert "wecom_dry_run_payload_prepared" in result.audit_notes
        assert "wecom_dry_run_only" in result.audit_notes
        assert "no_provider_delivery" in result.audit_notes

    @pytest.mark.parametrize(
        "outbound_request",
        [
            _sendable_request(human_approval=OutboundRequestHumanApproval()),
            _sendable_request(send_gate=_blocked_send_gate()),
        ],
    )
    def test_non_sendable_request_blocks(
        self,
        outbound_request: OutboundMessageRequest,
    ) -> None:
        result = WeComCustomerServiceDryRunOutboundAdapter().prepare_dry_run(
            outbound_request,
            safety_decision=None,
        )

        assert result.delivery_status == "blocked_not_sendable"
        assert result.delivered is False
        assert result.prepared_payload is None
        assert "request_not_sendable" in result.audit_notes

    def test_missing_safety_decision_blocks(self) -> None:
        request = _sendable_request()

        result = WeComCustomerServiceDryRunOutboundAdapter().prepare_dry_run(
            request,
            safety_decision=None,
        )

        assert result.delivery_status == "blocked_safety_missing"
        assert result.prepared_payload is None

    def test_blocked_safety_decision_blocks(self) -> None:
        request = _sendable_request()
        safety_decision = _matching_safety_decision(
            request,
            safety_state="blocked",
            reason_codes=["service_window_expired"],
        )

        result = WeComCustomerServiceDryRunOutboundAdapter().prepare_dry_run(
            request,
            safety_decision=safety_decision,
        )

        assert result.delivery_status == "blocked_safety_not_allowed"
        assert result.prepared_payload is None
        assert "service_window_expired" in result.audit_notes

    @pytest.mark.parametrize(
        "safety_overrides",
        [
            {"request_id": "outreq_other"},
            {"contact_id": "contact_other"},
            {"user_id": "user_other"},
        ],
    )
    def test_mismatched_safety_decision_identity_blocks(
        self,
        safety_overrides: dict[str, object],
    ) -> None:
        request = _sendable_request()
        safety_decision = _matching_safety_decision(request, **safety_overrides)

        result = WeComCustomerServiceDryRunOutboundAdapter().prepare_dry_run(
            request,
            safety_decision=safety_decision,
        )

        assert result.delivery_status == "blocked_safety_mismatch"
        assert result.prepared_payload is None

    def test_wrong_safety_provider_surface_blocks(self) -> None:
        request = _sendable_request()
        safety_decision = _matching_safety_decision(
            request,
            provider_surface="other_surface",
        )

        result = WeComCustomerServiceDryRunOutboundAdapter().prepare_dry_run(
            request,
            safety_decision=safety_decision,
        )

        assert result.delivery_status == "blocked_safety_mismatch"
        assert result.prepared_payload is None

    @pytest.mark.parametrize(
        "safety_overrides",
        [
            {"recipient_alias": None},
            {"open_kfid_alias": ""},
            {"external_user_alias": "   "},
        ],
    )
    def test_missing_safety_aliases_block(
        self,
        safety_overrides: dict[str, object],
    ) -> None:
        request = _sendable_request()
        safety_decision = _matching_safety_decision(request, **safety_overrides)

        result = WeComCustomerServiceDryRunOutboundAdapter().prepare_dry_run(
            request,
            safety_decision=safety_decision,
        )

        assert result.delivery_status == "blocked_missing_safety_aliases"
        assert result.prepared_payload is None

    def test_missing_t233_boundary_audit_notes_blocks(self) -> None:
        request = _sendable_request()
        safety_decision = _matching_safety_decision(
            request,
            audit_notes=["provider_eligible_not_delivery"],
        )

        result = WeComCustomerServiceDryRunOutboundAdapter().prepare_dry_run(
            request,
            safety_decision=safety_decision,
        )

        assert result.delivery_status == "blocked_safety_mismatch"
        assert result.prepared_payload is None

    @pytest.mark.parametrize("channel_preference", ["unspecified", "feishu"])
    def test_non_wechat_channel_preference_blocks(self, channel_preference: str) -> None:
        request = _sendable_request(channel_preference=channel_preference)

        result = WeComCustomerServiceDryRunOutboundAdapter().prepare_dry_run(
            request,
            safety_decision=_matching_safety_decision(request),
        )

        assert result.delivery_status == "blocked_channel_mismatch"
        assert result.prepared_payload is None

    def test_rejects_direct_candidate_action_model(self) -> None:
        result = WeComCustomerServiceDryRunOutboundAdapter().prepare_dry_run(
            _candidate_action(),
            safety_decision=None,
        )

        assert result.delivery_status == "blocked_candidate_action_input"
        assert result.delivered is False
        assert "candidate_action_input_rejected" in result.audit_notes

    def test_rejects_candidate_shaped_mapping(self) -> None:
        result = WeComCustomerServiceDryRunOutboundAdapter().prepare_dry_run(
            _candidate_action().model_dump(),
            safety_decision=None,
        )

        assert result.delivery_status == "blocked_candidate_action_input"
        assert result.delivered is False
        assert "candidate_action_input_rejected" in result.audit_notes

    def test_invalid_request_mapping_blocks(self) -> None:
        result = WeComCustomerServiceDryRunOutboundAdapter().prepare_dry_run(
            {"draft_text": "not an outbound request"},
            safety_decision=None,
        )

        assert result.delivery_status == "blocked_invalid_request"
        assert result.prepared_payload is None
        assert "request_validation_failed" in result.audit_notes

    def test_mapping_input_validates_same_as_model_for_request_and_safety(self) -> None:
        adapter = WeComCustomerServiceDryRunOutboundAdapter()
        request = _sendable_request()
        safety_decision = _matching_safety_decision(request)

        model_result = adapter.prepare_dry_run(request, safety_decision=safety_decision)
        mapping_result = adapter.prepare_dry_run(
            request.model_dump(mode="json"),
            safety_decision=safety_decision.__dict__,
        )

        assert mapping_result.delivery_status == model_result.delivery_status
        assert mapping_result.prepared_payload == model_result.prepared_payload
        assert mapping_result.audit_notes == model_result.audit_notes

    def test_payload_metadata_is_not_copied_to_prepared_payload(self) -> None:
        request = _sendable_request(
            payload=OutboundMessagePayload(
                draft_text="Approved outbound draft text wins.",
                safe_summary="Review-safe summary wins.",
                metadata={
                    "tone": "polite",
                    "text": "metadata override must not appear",
                    "custom_context": {"nested": "do not copy"},
                },
            ),
        )

        result = WeComCustomerServiceDryRunOutboundAdapter().prepare_dry_run(
            request,
            safety_decision=_matching_safety_decision(request),
        )

        assert result.prepared_payload is not None
        payload_text = repr(result.prepared_payload)
        assert "metadata" not in result.prepared_payload
        assert "metadata override must not appear" not in payload_text
        assert "custom_context" not in payload_text
        assert result.prepared_payload["message"] == {
            "msg_type": "text",
            "text": "Approved outbound draft text wins.",
        }

    def test_input_request_and_safety_decision_are_not_mutated(self) -> None:
        request = _sendable_request()
        safety_decision = _matching_safety_decision(request)
        request_before = request.model_dump()
        safety_before = safety_decision.__dict__.copy()

        result = WeComCustomerServiceDryRunOutboundAdapter().prepare_dry_run(
            request,
            safety_decision=safety_decision,
        )

        assert result.delivery_status == "wecom_dry_run_ready"
        assert request.model_dump() == request_before
        assert safety_decision.__dict__ == safety_before

    def test_adapter_has_no_transport_or_api_call_seam(self) -> None:
        adapter = WeComCustomerServiceDryRunOutboundAdapter()

        assert not hasattr(adapter, "transport")
        assert not hasattr(adapter, "send")
        assert not hasattr(adapter, "deliver")
