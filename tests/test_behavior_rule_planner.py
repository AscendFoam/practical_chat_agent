"""T211 deterministic behavior rule planner tests.

All inputs are synthetic and review-safe. The planner must produce
CandidateAction artifacts only; it must not send, schedule, call providers,
wire runtime hooks, or mutate stores.
"""

from __future__ import annotations

import inspect

from practical_chat_agent.core.models import (
    AgentSelfState,
    BehaviorPolicy,
    CandidateAction,
)
from practical_chat_agent.services.behavior_planner import BehaviorRulePlanner


def _state(**overrides: object) -> AgentSelfState:
    data: dict[str, object] = {
        "agent_id": "agent_synthetic",
        "user_id": "user_synthetic",
        "contact_id": "contact_synthetic",
        "approved_context_refs": [],
        "recent_signal_refs": [],
        "risk_flags": [],
    }
    data.update(overrides)
    return AgentSelfState(**data)


def _policy(**overrides: object) -> BehaviorPolicy:
    data: dict[str, object] = {}
    data.update(overrides)
    return BehaviorPolicy(**data)


class TestBehaviorRulePlannerFallback:
    def test_thin_context_returns_do_nothing_candidate(self) -> None:
        planner = BehaviorRulePlanner()

        actions = planner.plan(self_state=_state())

        assert [a.action_type for a in actions] == ["do_nothing"]
        action = actions[0]
        assert action.payload.safe_summary == "No proactive candidate: context is too thin."
        assert action.supporting_context_refs[0].ref_id == "behavior_rule_no_action"

    def test_returns_empty_when_no_rule_fires_and_do_nothing_disallowed(self) -> None:
        planner = BehaviorRulePlanner()

        actions = planner.plan(
            self_state=_state(),
            policy=_policy(allowed_action_types=["relationship_check_in_draft"]),
        )

        assert actions == []


class TestBehaviorRulePlannerRules:
    def test_boundary_sensitive_input_emits_boundary_review_note(self) -> None:
        planner = BehaviorRulePlanner()

        actions = planner.plan(
            self_state=_state(
                approved_context_refs=["skillstore_safe_001"],
                risk_flags=["boundary_sensitive"],
            ),
        )

        assert actions[0].action_type == "boundary_review_note"
        assert "boundary-sensitive" in actions[0].rationale
        assert actions[0].payload.metadata["rule_id"] == "boundary_review_note"

    def test_recent_signal_refs_emit_memory_review_prompt(self) -> None:
        planner = BehaviorRulePlanner()

        actions = planner.plan(
            self_state=_state(recent_signal_refs=["relsig_safe_001"]),
        )

        assert actions[0].action_type == "memory_review_prompt"
        assert actions[0].supporting_context_refs[0].ref_id == "relsig_safe_001"
        assert actions[0].payload.metadata["rule_id"] == "memory_review_prompt"

    def test_relationship_check_in_requires_approved_context_ref(self) -> None:
        planner = BehaviorRulePlanner()

        without_context = planner.plan(self_state=_state())
        with_context = planner.plan(
            self_state=_state(approved_context_refs=["skillstore_safe_001"]),
        )

        assert [a.action_type for a in without_context] == ["do_nothing"]
        assert [a.action_type for a in with_context] == ["relationship_check_in_draft"]
        assert with_context[0].supporting_context_refs[0].ref_id == "skillstore_safe_001"

    def test_hard_risk_blocks_relationship_check_in(self) -> None:
        planner = BehaviorRulePlanner()

        actions = planner.plan(
            self_state=_state(
                approved_context_refs=["skillstore_safe_001"],
                risk_flags=["privacy_risk"],
            ),
        )

        assert "relationship_check_in_draft" not in [a.action_type for a in actions]
        assert [a.action_type for a in actions] == ["do_nothing"]


class TestBehaviorRulePlannerOrderingAndPolicy:
    def test_candidate_order_is_deterministic_when_multiple_rules_fire(self) -> None:
        planner = BehaviorRulePlanner()
        state = _state(
            approved_context_refs=["skillstore_safe_001"],
            recent_signal_refs=["relsig_safe_001"],
            risk_flags=["boundary_sensitive"],
        )

        actions = planner.plan(self_state=state)
        repeated = planner.plan(self_state=state)

        assert [a.action_type for a in actions] == [
            "boundary_review_note",
            "memory_review_prompt",
        ]
        assert [a.action_id for a in actions] == [a.action_id for a in repeated]

    def test_max_candidates_limit_is_respected(self) -> None:
        planner = BehaviorRulePlanner()

        actions = planner.plan(
            self_state=_state(
                approved_context_refs=["skillstore_safe_001"],
                recent_signal_refs=["relsig_safe_001"],
                risk_flags=["boundary_sensitive"],
            ),
            policy=_policy(max_candidates=1),
        )

        assert len(actions) == 1
        assert actions[0].action_type == "boundary_review_note"

    def test_policy_disallows_rule_and_planner_falls_back_safely(self) -> None:
        planner = BehaviorRulePlanner()

        actions = planner.plan(
            self_state=_state(risk_flags=["boundary_sensitive"]),
            policy=_policy(allowed_action_types=["do_nothing"]),
        )

        assert [a.action_type for a in actions] == ["do_nothing"]
        assert actions[0].payload.metadata["rule_id"] == "do_nothing"

    def test_policy_disallows_do_nothing_so_disallowed_rules_are_skipped(self) -> None:
        planner = BehaviorRulePlanner()

        actions = planner.plan(
            self_state=_state(risk_flags=["boundary_sensitive"]),
            policy=_policy(allowed_action_types=["relationship_check_in_draft"]),
        )

        assert actions == []


class TestBehaviorRulePlannerCandidateSafety:
    def test_emitted_candidates_validate_as_candidate_action(self) -> None:
        planner = BehaviorRulePlanner()

        actions = planner.plan(
            self_state=_state(
                approved_context_refs=["skillstore_safe_001"],
                recent_signal_refs=["relsig_safe_001"],
            ),
        )

        assert actions
        assert all(isinstance(action, CandidateAction) for action in actions)

    def test_emitted_candidates_preserve_no_execution_invariants(self) -> None:
        planner = BehaviorRulePlanner()

        actions = planner.plan(
            self_state=_state(
                approved_context_refs=["skillstore_safe_001"],
                recent_signal_refs=["relsig_safe_001"],
                risk_flags=["boundary_sensitive"],
            ),
        )

        for action in actions:
            assert action.human_review_required is True
            assert action.auto_send_allowed is False
            assert action.platform_execution_allowed is False
            assert action.scheduler_allowed is False
            assert action.platform_target is None
            assert action.status == "candidate"
            assert not action.is_runtime_visible()

    def test_no_forbidden_payload_metadata_is_emitted(self) -> None:
        planner = BehaviorRulePlanner()
        forbidden = set(BehaviorPolicy().forbidden_payload_fields)

        actions = planner.plan(
            self_state=_state(
                approved_context_refs=["skillstore_safe_001"],
                recent_signal_refs=["relsig_safe_001"],
                risk_flags=["boundary_sensitive"],
            ),
        )

        for action in actions:
            assert not forbidden.intersection(action.payload.metadata)

    def test_supporting_refs_are_required_and_preserved(self) -> None:
        planner = BehaviorRulePlanner()

        actions = planner.plan(
            self_state=_state(
                approved_context_refs=["skillstore_safe_001"],
                recent_signal_refs=["relsig_safe_001"],
            ),
        )

        refs_by_type = {
            action.action_type: [ref.ref_id for ref in action.supporting_context_refs]
            for action in actions
        }
        assert refs_by_type["memory_review_prompt"] == ["relsig_safe_001"]
        assert refs_by_type["relationship_check_in_draft"] == ["skillstore_safe_001"]

    def test_public_plan_api_does_not_accept_raw_private_text_fields(self) -> None:
        signature = inspect.signature(BehaviorRulePlanner.plan)

        forbidden_parameter_names = {
            "raw_text",
            "transcript",
            "chat_history",
            "private_messages",
            "message_text",
        }

        assert forbidden_parameter_names.isdisjoint(signature.parameters)

