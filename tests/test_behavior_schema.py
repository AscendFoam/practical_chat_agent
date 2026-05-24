"""T210 behavior-planner schema tests.

All fixtures are synthetic and review-safe. These tests define the opening
M10 data contracts only; they do not exercise any planner, scheduler, sender,
platform adapter, memory mutation, or raw transcript path.
"""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from practical_chat_agent.core.models import (
    AgentSelfState,
    BehaviorPolicy,
    CandidateAction,
    CandidateActionPayload,
    DistilledArtifactReviewMetadata,
    ReplyPlanContextRef,
)


def _ref(ref_id: str = "skillstore_synthetic_001") -> ReplyPlanContextRef:
    return ReplyPlanContextRef(
        ref_type="approved_contact_skill_record",
        ref_id=ref_id,
        note="synthetic approved context",
    )


def _reviewed_metadata() -> DistilledArtifactReviewMetadata:
    return DistilledArtifactReviewMetadata(
        review_state="reviewed",
        reviewed_by_human=True,
        last_decision="approved",
        evidence_validation_status="passed",
    )


def _make_self_state(**overrides: object) -> AgentSelfState:
    data: dict[str, object] = {
        "agent_id": "agent_synthetic",
        "user_id": "user_synthetic",
        "contact_id": "contact_synthetic",
        "current_focus": "review safe proactive drafting",
        "approved_context_refs": ["skillstore_synthetic_001"],
        "recent_signal_refs": ["reldelta_synthetic_001"],
        "risk_flags": ["thin_context"],
    }
    data.update(overrides)
    return AgentSelfState(**data)


def _make_policy(**overrides: object) -> BehaviorPolicy:
    data: dict[str, object] = {
        "policy_id": "behpolicy_synthetic_001",
        "allowed_action_types": ["relationship_check_in_draft", "do_nothing"],
        "boundary_rules": ["Never send without explicit human approval."],
    }
    data.update(overrides)
    return BehaviorPolicy(**data)


def _make_action(**overrides: object) -> CandidateAction:
    data: dict[str, object] = {
        "contact_id": "contact_synthetic",
        "user_id": "user_synthetic",
        "action_type": "relationship_check_in_draft",
        "title": "Draft a low-pressure check-in for review",
        "rationale": "Approved context suggests a reviewable check-in may be useful.",
        "supporting_context_refs": [_ref()],
        "risk_flags": ["thin_context"],
        "payload": CandidateActionPayload(
            safe_summary="Suggests a low-pressure check-in draft for human review.",
            draft_text="A short synthetic draft.",
        ),
    }
    data.update(overrides)
    return CandidateAction(**data)


class TestAgentSelfState:
    def test_minimal_valid_state_uses_safe_defaults(self) -> None:
        state = AgentSelfState(agent_id="agent_1", user_id="user_1")
        assert state.schema_version == "agent_self_state_v1"
        assert state.state_id.startswith("agentstate_")
        assert state.contact_id is None
        assert state.availability_state == "unknown"
        assert state.current_focus is None
        assert state.approved_context_refs == []
        assert state.recent_signal_refs == []
        assert state.risk_flags == []

    def test_rich_state_preserves_review_safe_refs(self) -> None:
        state = _make_self_state()
        assert state.contact_id == "contact_synthetic"
        assert state.current_focus == "review safe proactive drafting"
        assert state.approved_context_refs == ["skillstore_synthetic_001"]
        assert state.recent_signal_refs == ["reldelta_synthetic_001"]
        assert state.risk_flags == ["thin_context"]

    def test_required_scope_fields_are_required(self) -> None:
        with pytest.raises(ValidationError):
            AgentSelfState(user_id="user_1")  # type: ignore[call-arg]
        with pytest.raises(ValidationError):
            AgentSelfState(agent_id="agent_1")  # type: ignore[call-arg]

    def test_empty_scope_ids_are_rejected(self) -> None:
        with pytest.raises(ValidationError):
            AgentSelfState(agent_id="", user_id="user_1")
        with pytest.raises(ValidationError):
            AgentSelfState(agent_id="agent_1", user_id="")
        with pytest.raises(ValidationError):
            _make_self_state(contact_id="")

    def test_state_has_no_raw_transcript_fields(self) -> None:
        state = _make_self_state()
        assert not hasattr(state, "raw_text")
        assert not hasattr(state, "transcript")
        assert not hasattr(state, "chat_history")
        assert not hasattr(state, "private_messages")

    def test_state_json_round_trip(self) -> None:
        state = _make_self_state()
        restored = AgentSelfState.model_validate_json(state.model_dump_json())
        assert restored.agent_id == state.agent_id
        assert restored.user_id == state.user_id
        assert restored.approved_context_refs == state.approved_context_refs


class TestBehaviorPolicy:
    def test_default_policy_is_review_only_and_non_executable(self) -> None:
        policy = BehaviorPolicy()
        assert policy.schema_version == "behavior_policy_v1"
        assert policy.policy_id.startswith("behpolicy_")
        assert policy.policy_mode == "draft_only_review_required"
        assert policy.human_review_required is True
        assert policy.auto_send_allowed is False
        assert policy.platform_execution_allowed is False
        assert policy.scheduler_allowed is False
        assert "do_nothing" in policy.allowed_action_types

    def test_rich_policy_preserves_boundaries(self) -> None:
        policy = _make_policy()
        assert policy.allowed_action_types == ["relationship_check_in_draft", "do_nothing"]
        assert policy.boundary_rules == ["Never send without explicit human approval."]
        assert "raw_transcript" in policy.forbidden_payload_fields
        assert "send_at" in policy.forbidden_payload_fields

    def test_policy_rejects_auto_send_or_execution_flags(self) -> None:
        with pytest.raises(ValidationError):
            BehaviorPolicy(auto_send_allowed=True)  # type: ignore[arg-type]
        with pytest.raises(ValidationError):
            BehaviorPolicy(platform_execution_allowed=True)  # type: ignore[arg-type]
        with pytest.raises(ValidationError):
            BehaviorPolicy(scheduler_allowed=True)  # type: ignore[arg-type]
        with pytest.raises(ValidationError):
            BehaviorPolicy(human_review_required=False)  # type: ignore[arg-type]

    def test_policy_rejects_unknown_action_type(self) -> None:
        with pytest.raises(ValidationError):
            BehaviorPolicy(allowed_action_types=["send_platform_message"])  # type: ignore[list-item]

    def test_policy_json_round_trip(self) -> None:
        policy = _make_policy()
        restored = BehaviorPolicy.model_validate_json(policy.model_dump_json())
        assert restored.policy_id == "behpolicy_synthetic_001"
        assert restored.allowed_action_types == policy.allowed_action_types
        assert restored.auto_send_allowed is False


class TestCandidateActionPayload:
    def test_minimal_payload_does_not_require_raw_text_or_draft_text(self) -> None:
        payload = CandidateActionPayload(safe_summary="Review-safe summary only.")
        assert payload.safe_summary == "Review-safe summary only."
        assert payload.draft_text is None
        assert payload.metadata == {}

    def test_payload_preserves_review_safe_metadata(self) -> None:
        payload = CandidateActionPayload(
            safe_summary="Review-safe summary.",
            metadata={"tone": "low_pressure", "max_length": 80},
        )
        assert payload.metadata == {"tone": "low_pressure", "max_length": 80}

    def test_payload_rejects_forbidden_execution_and_private_keys(self) -> None:
        forbidden_keys = [
            "send_at",
            "scheduled_at",
            "platform",
            "channel_id",
            "webhook_url",
            "recipient_address",
            "raw_transcript",
            "chat_history",
            "private_messages",
        ]
        for key in forbidden_keys:
            with pytest.raises(ValidationError):
                CandidateActionPayload(
                    safe_summary="Unsafe metadata should be rejected.",
                    metadata={key: "unsafe"},
                )


class TestCandidateAction:
    def test_minimal_candidate_action_is_draft_only(self) -> None:
        action = _make_action()
        assert action.schema_version == "candidate_action_v1"
        assert action.action_id.startswith("candact_")
        assert action.action_mode == "draft_only_review_required"
        assert action.status == "candidate"
        assert action.human_review_required is True
        assert action.auto_send_allowed is False
        assert action.platform_execution_allowed is False
        assert action.scheduler_allowed is False
        assert action.platform_target is None
        assert not action.is_runtime_visible()

    def test_candidate_preserves_scope_evidence_risk_and_payload(self) -> None:
        action = _make_action()
        assert action.contact_id == "contact_synthetic"
        assert action.user_id == "user_synthetic"
        assert action.supporting_context_refs[0].ref_id == "skillstore_synthetic_001"
        assert action.risk_flags == ["thin_context"]
        assert action.payload.safe_summary.startswith("Suggests")

    def test_required_fields_are_required(self) -> None:
        with pytest.raises(ValidationError):
            CandidateAction(
                user_id="user_1",
                action_type="do_nothing",
                title="No action",
                rationale="Insufficient context.",
                supporting_context_refs=[_ref()],
            )

    def test_empty_core_fields_are_rejected(self) -> None:
        for field_name in ("contact_id", "user_id", "title", "rationale"):
            with pytest.raises(ValidationError):
                _make_action(**{field_name: ""})

    def test_supporting_context_refs_required(self) -> None:
        with pytest.raises(ValidationError):
            _make_action(supporting_context_refs=[])

    def test_invalid_action_type_rejected(self) -> None:
        with pytest.raises(ValidationError):
            _make_action(action_type="send_platform_message")

    def test_action_type_must_be_allowed_by_policy(self) -> None:
        with pytest.raises(ValidationError):
            _make_action(
                action_type="relationship_check_in_draft",
                policy=BehaviorPolicy(allowed_action_types=["do_nothing"]),
            )

    def test_candidate_rejects_execution_flags_and_platform_target(self) -> None:
        with pytest.raises(ValidationError):
            _make_action(auto_send_allowed=True)
        with pytest.raises(ValidationError):
            _make_action(platform_execution_allowed=True)
        with pytest.raises(ValidationError):
            _make_action(scheduler_allowed=True)
        with pytest.raises(ValidationError):
            _make_action(platform_target="wechat")

    def test_status_lifecycle_is_data_only(self) -> None:
        candidate = _make_action(status="candidate")
        rejected = _make_action(status="rejected")
        approved = _make_action(status="approved", review_metadata=_reviewed_metadata())
        assert not candidate.is_runtime_visible()
        assert not rejected.is_runtime_visible()
        assert approved.is_runtime_visible()
        assert approved.auto_send_allowed is False
        assert approved.platform_execution_allowed is False

    def test_candidate_json_round_trip(self) -> None:
        action = _make_action()
        restored = CandidateAction.model_validate_json(action.model_dump_json())
        assert restored.action_id == action.action_id
        assert restored.contact_id == action.contact_id
        assert restored.action_type == action.action_type
        assert restored.supporting_context_refs[0].ref_id == "skillstore_synthetic_001"
        assert restored.payload.safe_summary == action.payload.safe_summary

    def test_candidate_has_no_send_or_mutation_capability(self) -> None:
        action = _make_action()
        assert not hasattr(action, "send")
        assert not hasattr(action, "schedule")
        assert not hasattr(action, "execute")
        assert not hasattr(action, "mutate_memory")
        assert not hasattr(action, "update_contact_skill")
