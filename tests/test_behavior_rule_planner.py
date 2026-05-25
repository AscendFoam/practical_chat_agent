"""T211 deterministic behavior rule planner tests.

All inputs are synthetic and review-safe. The planner must produce
CandidateAction artifacts only; it must not send, schedule, call providers,
wire runtime hooks, or mutate stores.
"""

from __future__ import annotations

import inspect

import pytest

from practical_chat_agent.core.models import (
    AgentSelfState,
    BehaviorPolicy,
    CandidateAction,
    CandidateActionPayload,
    DistilledArtifactReviewMetadata,
    ReplyPlanContextRef,
)
from practical_chat_agent.services.behavior_planner import (
    BehaviorRulePlanner,
    CandidateActionReviewError,
    CandidateActionReviewService,
    ProactiveDraftGenerator,
)


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


def _candidate_action(action_type: str, **overrides: object) -> CandidateAction:
    data: dict[str, object] = {
        "contact_id": "contact_synthetic",
        "user_id": "user_synthetic",
        "action_type": action_type,
        "title": f"Synthetic {action_type}",
        "rationale": "Synthetic review-safe rationale.",
        "supporting_context_refs": [
            ReplyPlanContextRef(
                ref_type="policy_boundary",
                ref_id=f"ref_{action_type}",
                note="synthetic review-safe ref",
            ),
        ],
        "payload": CandidateActionPayload(
            safe_summary="Synthetic review-safe summary.",
            metadata={"rule_id": action_type},
        ),
    }
    data.update(overrides)
    return CandidateAction(**data)


def _review_metadata() -> DistilledArtifactReviewMetadata:
    return DistilledArtifactReviewMetadata(
        review_state="pending_human_review",
        reviewed_by_human=False,
        last_decision=None,
        decision_notes=[],
        history=[],
    )


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


class TestProactiveDraftGenerator:
    def test_enriches_all_supported_candidate_types_with_draft_text(self) -> None:
        generator = ProactiveDraftGenerator()
        action_types = [
            "relationship_check_in_draft",
            "reply_follow_up_draft",
            "topic_suggestion",
            "boundary_review_note",
            "memory_review_prompt",
            "do_nothing",
        ]

        enriched = [generator.enrich(_candidate_action(action_type)) for action_type in action_types]

        assert [action.action_type for action in enriched] == action_types
        assert all(action.payload.draft_text for action in enriched)
        assert all("review" in action.payload.draft_text.casefold() for action in enriched)

    def test_enrich_is_deterministic_for_same_input(self) -> None:
        generator = ProactiveDraftGenerator()
        planner = BehaviorRulePlanner()
        action = planner.plan(
            self_state=_state(approved_context_refs=["skillstore_safe_001"]),
        )[0]

        enriched_one = generator.enrich(action)
        enriched_two = generator.enrich(action.model_dump())

        assert enriched_one.payload.draft_text == enriched_two.payload.draft_text
        assert enriched_one.action_id == enriched_two.action_id
        assert enriched_one.action_type == enriched_two.action_type
        assert enriched_one.supporting_context_refs == enriched_two.supporting_context_refs

    def test_enrich_preserves_candidate_invariants_and_payload_fields(self) -> None:
        generator = ProactiveDraftGenerator()
        planner = BehaviorRulePlanner()
        action = planner.plan(self_state=_state())[0]

        enriched = generator.enrich(action)

        assert enriched.action_id == action.action_id
        assert enriched.action_type == action.action_type
        assert enriched.supporting_context_refs == action.supporting_context_refs
        assert enriched.risk_flags == action.risk_flags
        assert enriched.policy == action.policy
        assert enriched.status == action.status
        assert enriched.payload.safe_summary == action.payload.safe_summary
        assert enriched.human_review_required is True
        assert enriched.auto_send_allowed is False
        assert enriched.platform_execution_allowed is False
        assert enriched.scheduler_allowed is False
        assert enriched.platform_target is None
        assert enriched.payload.draft_text is not None
        assert "send" not in enriched.payload.draft_text.casefold()
        assert "schedule" not in enriched.payload.draft_text.casefold()
        assert "platform" not in enriched.payload.draft_text.casefold()
        assert not set(BehaviorPolicy().forbidden_payload_fields).intersection(enriched.payload.metadata)

    def test_enrich_does_not_echo_private_or_raw_text_from_input(self) -> None:
        generator = ProactiveDraftGenerator()
        private_sentinel = "SECRET_RAW_PRIVATE_TEXT_DO_NOT_ECHO"
        action = _candidate_action(
            "relationship_check_in_draft",
            payload=CandidateActionPayload(
                safe_summary=f"Synthetic summary with {private_sentinel}.",
                review_notes=[f"Reviewer note mentions {private_sentinel}."],
                metadata={"rule_id": "relationship_check_in_draft"},
            ),
        )

        enriched = generator.enrich(action)

        assert enriched.payload.draft_text is not None
        assert private_sentinel not in enriched.payload.draft_text
        assert "raw" not in enriched.payload.draft_text.casefold()
        assert "private" not in enriched.payload.draft_text.casefold()

    def test_boundary_sensitive_candidates_stay_conservative(self) -> None:
        generator = ProactiveDraftGenerator()
        action = BehaviorRulePlanner().plan(
            self_state=_state(
                approved_context_refs=["skillstore_safe_001"],
                risk_flags=["boundary_sensitive"],
            ),
        )[0]

        enriched = generator.enrich(action)

        assert enriched.action_type == "boundary_review_note"
        assert "boundary-sensitive" in enriched.payload.draft_text.casefold()
        assert "proactive wording" in enriched.payload.draft_text.casefold()

    def test_do_nothing_candidate_remains_review_only(self) -> None:
        generator = ProactiveDraftGenerator()
        action = BehaviorRulePlanner().plan(self_state=_state())[0]

        enriched = generator.enrich(action)

        assert enriched.action_type == "do_nothing"
        assert enriched.payload.draft_text == "Review only: no proactive action is recommended for now."
        assert enriched.payload.safe_summary == "No proactive candidate: context is too thin."

    def test_relationship_check_in_remains_low_pressure_and_non_committal(self) -> None:
        generator = ProactiveDraftGenerator()
        action = BehaviorRulePlanner().plan(
            self_state=_state(approved_context_refs=["skillstore_safe_001"]),
        )[0]

        enriched = generator.enrich(action)

        assert enriched.action_type == "relationship_check_in_draft"
        assert "low-pressure" in enriched.payload.draft_text.casefold()
        assert "optional" in enriched.payload.draft_text.casefold()
        assert "non-committal" in enriched.payload.draft_text.casefold()

    def test_enrich_accepts_stable_mapping_inputs_without_private_text_fields(self) -> None:
        generator = ProactiveDraftGenerator()
        action = BehaviorRulePlanner().plan(
            self_state=_state(approved_context_refs=["skillstore_safe_001"]),
        )[0]

        enriched = generator.enrich(action.model_dump(mode="python"))

        assert enriched.payload.draft_text is not None
        assert not hasattr(enriched, "raw_transcript")
        assert not hasattr(enriched.payload, "raw_transcript")


class TestCandidateActionReviewService:
    def test_approve_candidate_updates_review_metadata(self) -> None:
        service = CandidateActionReviewService()
        candidate = _candidate_action(
            "relationship_check_in_draft",
            status="candidate",
            review_metadata=_review_metadata(),
        )

        reviewed = service.review_candidate(
            candidate=candidate,
            decision="approve",
            reviewer_id="reviewer_001",
            note="Looks fine.",
        )

        assert reviewed is not candidate
        assert reviewed.status == "approved"
        assert reviewed.review_metadata.review_state == "reviewed"
        assert reviewed.review_metadata.reviewed_by_human is True
        assert reviewed.review_metadata.last_decision == "approved"
        assert reviewed.review_metadata.last_reviewer_id == "reviewer_001"
        assert reviewed.review_metadata.history[-1].status == "approved"
        assert "Looks fine." in reviewed.review_metadata.decision_notes

    def test_reject_freeze_archive_are_supported(self) -> None:
        service = CandidateActionReviewService()
        candidate = _candidate_action(
            "do_nothing",
            status="candidate",
            review_metadata=_review_metadata(),
        )

        rejected = service.review_candidate(candidate=candidate, decision="reject", reviewer_id="r1")
        frozen = service.review_candidate(candidate=candidate, decision="freeze", reviewer_id="r2")
        archived = service.review_candidate(candidate=candidate, decision="archive", reviewer_id="r3")

        assert rejected.status == "rejected"
        assert frozen.status == "frozen"
        assert archived.status == "archived"

    def test_invalid_decision_rejected(self) -> None:
        service = CandidateActionReviewService()

        with pytest.raises(CandidateActionReviewError):
            service.review_candidate(
                candidate=_candidate_action("do_nothing", review_metadata=_review_metadata()),
                decision="send",
                reviewer_id="reviewer_001",
            )

    def test_reviewer_id_required(self) -> None:
        service = CandidateActionReviewService()

        with pytest.raises(CandidateActionReviewError):
            service.review_candidate(
                candidate=_candidate_action("do_nothing", review_metadata=_review_metadata()),
                decision="approve",
                reviewer_id=" ",
            )

    def test_review_preserves_payload_and_invariants(self) -> None:
        service = CandidateActionReviewService()
        candidate = _candidate_action(
            "relationship_check_in_draft",
            status="candidate",
            review_metadata=_review_metadata(),
        )

        reviewed = service.review_candidate(
            candidate=candidate,
            decision="approve",
            reviewer_id="reviewer_001",
        )

        assert reviewed.payload.safe_summary == candidate.payload.safe_summary
        assert reviewed.payload.draft_text == candidate.payload.draft_text
        assert reviewed.supporting_context_refs == candidate.supporting_context_refs
        assert reviewed.risk_flags == candidate.risk_flags
        assert reviewed.policy == candidate.policy
        assert reviewed.human_review_required is True
        assert reviewed.auto_send_allowed is False
        assert reviewed.platform_execution_allowed is False
        assert reviewed.scheduler_allowed is False
        assert reviewed.platform_target is None
        assert candidate.status == "candidate"
        assert candidate.review_metadata.review_state == "pending_human_review"

    def test_review_accepts_mapping_input(self) -> None:
        service = CandidateActionReviewService()
        reviewed = service.review_candidate(
            candidate=_candidate_action(
                "relationship_check_in_draft",
                review_metadata=_review_metadata(),
            ).model_dump(mode="python"),
            decision="approve",
            reviewer_id="reviewer_001",
        )

        assert reviewed.status == "approved"
        assert reviewed.review_metadata.last_reviewer_id == "reviewer_001"
