"""T150: ReplyPlanner regression tests.

Deterministic tests covering M3 Conditional obligations for ReplyPlanner
and policy layer behavior.  All fixtures are synthetic and contain no
private chat content, real names, real platform IDs, or private paths.

Required coverage areas (indexed by T150 task package):
  1. baseline friend context -> valid 3-candidate ReplyPlan
  2. practical colleague context -> valid 3-candidate ReplyPlan
  3. thin context -> thin_context risk + conservative confidence
  4. sensitive/boundary context -> boundary reminders + risk flags
  5. false-positive probe -> does not over-escalate
  6. false-negative probe -> documents accepted limitation
  7. privacy leakage -> raw inbound text not echoed
  8. contact_id mismatch -> rejected
  9. not_configured store -> still emits safe candidates
 10. priority_rank -> unique and stable
 11. non-approved record ids -> do not leak into candidate refs
"""
from __future__ import annotations

import pytest

from practical_chat_agent.core.enums import (
    ChannelType,
    ChatIntent,
    ContentType,
    Direction,
    PersonaType,
    Platform,
    SourceType,
)
from practical_chat_agent.core.models import (
    ApprovedContactSkillBrief,
    ApprovedMemoryFactBrief,
    ApprovedStoreContext,
    ChatContext,
    ChatContextEvent,
    ReplyPlan,
)
from practical_chat_agent.services.reply_planner import ReplyPlanner, ReplyPlannerError

from tests.helpers import context, event


# ---------------------------------------------------------------------------
# 1. Baseline friend context
# ---------------------------------------------------------------------------


class TestBaselineFriendContext:
    """Baseline friend context emits valid 3-candidate ReplyPlan."""

    def test_emits_three_candidates(self, baseline_friend_context):
        plan = ReplyPlanner().generate(context=baseline_friend_context)
        assert len(plan.candidates) == 3

    def test_contact_id_matches(self, baseline_friend_context):
        plan = ReplyPlanner().generate(context=baseline_friend_context)
        assert plan.contact_id == "contact_friend"

    def test_candidates_have_required_fields(self, baseline_friend_context):
        plan = ReplyPlanner().generate(context=baseline_friend_context)
        for c in plan.candidates:
            assert c.draft_text, "draft_text must be non-empty"
            assert c.rationale, "rationale must be non-empty"
            assert len(c.supporting_context_refs) >= 1
            assert len(c.boundary_reminders) >= 1
            assert c.approach_label

    def test_source_context_loaded(self, baseline_friend_context):
        plan = ReplyPlanner().generate(context=baseline_friend_context)
        assert plan.source_context.approved_store_status == "loaded"

    def test_policy_boundary_summary_non_empty(self, baseline_friend_context):
        plan = ReplyPlanner().generate(context=baseline_friend_context)
        assert len(plan.policy_boundary_summary) >= 1

    def test_approved_skill_ref_in_source(self, baseline_friend_context):
        plan = ReplyPlanner().generate(context=baseline_friend_context)
        assert plan.source_context.approved_contact_skill_record_id == "approved_skill_friend_001"

    def test_approved_memory_ref_in_source(self, baseline_friend_context):
        plan = ReplyPlanner().generate(context=baseline_friend_context)
        assert "mem_friend_001" in plan.source_context.approved_memory_record_ids


# ---------------------------------------------------------------------------
# 2. Practical colleague context
# ---------------------------------------------------------------------------


class TestColleagueContext:
    """Practical colleague context emits valid 3-candidate ReplyPlan."""

    def test_emits_three_candidates(self, colleague_context):
        plan = ReplyPlanner().generate(context=colleague_context)
        assert len(plan.candidates) == 3

    def test_colleague_triggers_practical_tone(self, colleague_context):
        plan = ReplyPlanner().generate(context=colleague_context)
        summary_text = " ".join(plan.policy_boundary_summary).lower()
        assert "practical" in summary_text

    def test_colleague_contact_id(self, colleague_context):
        plan = ReplyPlanner().generate(context=colleague_context)
        assert plan.contact_id == "contact_colleague"

    def test_colleague_candidates_valid(self, colleague_context):
        plan = ReplyPlanner().generate(context=colleague_context)
        for c in plan.candidates:
            assert c.draft_text
            assert c.rationale
            assert len(c.supporting_context_refs) >= 1


# ---------------------------------------------------------------------------
# 3. Thin context
# ---------------------------------------------------------------------------


class TestThinContext:
    """Thin context produces thin_context risk and conservative confidence."""

    def test_emits_three_candidates(self, thin_context):
        plan = ReplyPlanner().generate(context=thin_context)
        assert len(plan.candidates) == 3

    def test_thin_context_risk_flag(self, thin_context):
        plan = ReplyPlanner().generate(context=thin_context)
        all_flags = [f for c in plan.candidates for f in c.risk_flags]
        assert "thin_context" in all_flags

    def test_conservative_confidence(self, thin_context):
        plan = ReplyPlanner().generate(context=thin_context)
        for c in plan.candidates:
            assert c.confidence is not None
            assert c.confidence < 0.70

    def test_thin_context_boundary_summary(self, thin_context):
        plan = ReplyPlanner().generate(context=thin_context)
        summary_text = " ".join(plan.policy_boundary_summary).lower()
        assert "thin" in summary_text

    def test_no_approved_skill_ref(self, thin_context):
        plan = ReplyPlanner().generate(context=thin_context)
        assert plan.source_context.approved_contact_skill_record_id is None


# ---------------------------------------------------------------------------
# 4. Sensitive/boundary context
# ---------------------------------------------------------------------------


class TestSensitiveContext:
    """Sensitive/boundary context produces boundary reminders and risk flags."""

    def test_emits_three_candidates(self, sensitive_context):
        plan = ReplyPlanner().generate(context=sensitive_context)
        assert len(plan.candidates) == 3

    def test_boundary_sensitive_risk_flag(self, sensitive_context):
        plan = ReplyPlanner().generate(context=sensitive_context)
        all_flags = [f for c in plan.candidates for f in c.risk_flags]
        assert "boundary_sensitive" in all_flags

    def test_boundary_reminders_present(self, sensitive_context):
        plan = ReplyPlanner().generate(context=sensitive_context)
        all_reminders = " ".join(
            r for c in plan.candidates for r in c.boundary_reminders
        ).lower()
        has_sensitive_cue = any(
            w in all_reminders
            for w in ["sensitive", "boundary", "push", "pressure", "disclosure"]
        )
        assert has_sensitive_cue

    def test_conservative_mode_drafts(self, sensitive_context):
        plan = ReplyPlanner().generate(context=sensitive_context)
        drafts = " ".join(c.draft_text for c in plan.candidates)
        assert len(drafts) > 0


# ---------------------------------------------------------------------------
# 5. False-positive probe
# ---------------------------------------------------------------------------


class TestFalsePositiveProbe:
    """False-positive probe: incidental 'money' in work text should not
    over-escalate to boundary_sensitive when intent is GENERAL and
    no boundary cues are present."""

    def test_store_status_loaded(self, false_positive_probe_context):
        plan = ReplyPlanner().generate(context=false_positive_probe_context)
        assert plan.source_context.approved_store_status == "loaded"

    def test_no_boundary_sensitive_flag(self, false_positive_probe_context):
        plan = ReplyPlanner().generate(context=false_positive_probe_context)
        all_flags = [f for c in plan.candidates for f in c.risk_flags]
        assert "boundary_sensitive" not in all_flags

    def test_no_thin_context_flag(self, false_positive_probe_context):
        plan = ReplyPlanner().generate(context=false_positive_probe_context)
        all_flags = [f for c in plan.candidates for f in c.risk_flags]
        assert "thin_context" not in all_flags

    def test_still_emits_valid_plan(self, false_positive_probe_context):
        plan = ReplyPlanner().generate(context=false_positive_probe_context)
        assert len(plan.candidates) == 3
        for c in plan.candidates:
            assert c.draft_text
            assert c.confidence is not None


# ---------------------------------------------------------------------------
# 6. False-negative probe (accepted limitation)
# ---------------------------------------------------------------------------


class TestFalseNegativeProbe:
    """False-negative probe: subtle inbound pacing pressure ("you should
    really call me sometime soon") is not detected by the current
    keyword-only policy layer.

    This is a documented accepted limitation under M3 Conditional.
    The test asserts current expected behavior rather than ideal behavior.
    """

    def test_emits_three_candidates(self, false_negative_probe_context):
        plan = ReplyPlanner().generate(context=false_negative_probe_context)
        assert len(plan.candidates) == 3

    def test_no_boundary_sensitive_flag_current_behavior(self, false_negative_probe_context):
        """Current behavior: subtle pacing pressure does not trigger
        boundary_sensitive because "you should really call me sometime
        soon" does not match any _BOUNDARY_CUE_KEYWORDS and the intent
        is GENERAL (not EMOTION/RELATIONSHIP).

        This is a known false-negative limitation of keyword-based
        detection.  A future semantic classifier could close this gap."""
        plan = ReplyPlanner().generate(context=false_negative_probe_context)
        all_flags = [f for c in plan.candidates for f in c.risk_flags]
        assert "boundary_sensitive" not in all_flags

    def test_no_thin_context_flag(self, false_negative_probe_context):
        plan = ReplyPlanner().generate(context=false_negative_probe_context)
        all_flags = [f for c in plan.candidates for f in c.risk_flags]
        assert "thin_context" not in all_flags


# ---------------------------------------------------------------------------
# 7. Privacy leakage probe
# ---------------------------------------------------------------------------


class TestPrivacyLeakage:
    """Privacy leakage: raw inbound text is not echoed in ReplyPlan."""

    def test_latest_message_text_not_in_plan(self, privacy_probe_context):
        plan = ReplyPlanner().generate(context=privacy_probe_context)
        plan_json = plan.model_dump_json()
        assert "abcdef9876" not in plan_json

    def test_event_text_not_echoed(self, privacy_probe_context):
        plan = ReplyPlanner().generate(context=privacy_probe_context)
        plan_json = plan.model_dump_json()
        assert "zyxwv6543" not in plan_json

    def test_memory_hit_text_not_echoed(self, privacy_probe_context):
        plan = ReplyPlanner().generate(context=privacy_probe_context)
        plan_json = plan.model_dump_json()
        assert "qprstu3210" not in plan_json

    def test_claim_text_not_leaked(self, privacy_probe_context):
        plan = ReplyPlanner().generate(context=privacy_probe_context)
        plan_json = plan.model_dump_json()
        assert "xyzzy123" not in plan_json

    def test_safe_context_summary_not_raw(self, privacy_probe_context):
        """source_context.chat_context_summary is a safe count/status
        string, not raw message text."""
        plan = ReplyPlanner().generate(context=privacy_probe_context)
        summary = plan.source_context.chat_context_summary
        assert summary is not None
        assert "unique private marker" not in summary


# ---------------------------------------------------------------------------
# 8. contact_id mismatch rejected
# ---------------------------------------------------------------------------


class TestContactIdMismatch:
    """contact_id mismatch between ChatContext.user_id and approved store
    is rejected with ReplyPlannerError."""

    def test_store_contact_id_mismatch(self):
        skill = ApprovedContactSkillBrief(
            record_id="skill_mismatch_store",
            contact_id="contact_WRONG",
            relationship_type="friend",
            relationship_summary="mismatched",
            evidence_refs=["ev_mm_001"],
        )
        store = ApprovedStoreContext(
            status="loaded",
            contact_id="contact_WRONG",
            contact_skill=skill,
            evidence_refs=["ev_mm_001"],
        )
        ctx = context(
            contact_id="contact_correct",
            latest_message_text="hello",
            approved_store_context=store,
        )
        with pytest.raises(ReplyPlannerError, match="contact_id"):
            ReplyPlanner().generate(context=ctx)

    def test_skill_contact_id_mismatch(self):
        skill = ApprovedContactSkillBrief(
            record_id="skill_mismatch_skill",
            contact_id="contact_WRONG",
            relationship_type="friend",
            relationship_summary="mismatched skill",
            evidence_refs=["ev_mm_002"],
        )
        store = ApprovedStoreContext(
            status="loaded",
            contact_id="contact_correct",
            contact_skill=skill,
            evidence_refs=["ev_mm_002"],
        )
        ctx = context(
            contact_id="contact_correct",
            latest_message_text="hello",
            approved_store_context=store,
        )
        with pytest.raises(ReplyPlannerError, match="contact_id"):
            ReplyPlanner().generate(context=ctx)


# ---------------------------------------------------------------------------
# 9. Not_configured / missing store path
# ---------------------------------------------------------------------------


class TestNotConfiguredPath:
    """approved-store not_configured path still emits safe candidates."""

    def test_emits_valid_plan(self, thin_context):
        plan = ReplyPlanner().generate(context=thin_context)
        assert len(plan.candidates) == 3

    def test_source_status_not_configured(self, thin_context):
        plan = ReplyPlanner().generate(context=thin_context)
        assert plan.source_context.approved_store_status == "not_configured"

    def test_no_skill_ref(self, thin_context):
        plan = ReplyPlanner().generate(context=thin_context)
        assert plan.source_context.approved_contact_skill_record_id is None

    def test_safe_confidence(self, thin_context):
        plan = ReplyPlanner().generate(context=thin_context)
        for c in plan.candidates:
            assert c.confidence is not None
            assert c.confidence < 0.75

    def test_boundary_reminders_present(self, thin_context):
        plan = ReplyPlanner().generate(context=thin_context)
        for c in plan.candidates:
            assert len(c.boundary_reminders) >= 1


# ---------------------------------------------------------------------------
# 10. priority_rank unique and stable
# ---------------------------------------------------------------------------


class TestPriorityRank:
    """candidate priority_rank is unique and forms a stable 1..N sequence."""

    def test_unique_ranks(self, baseline_friend_context):
        plan = ReplyPlanner().generate(context=baseline_friend_context)
        ranks = [c.priority_rank for c in plan.candidates]
        assert len(ranks) == len(set(ranks))

    def test_stable_one_to_n(self, baseline_friend_context):
        plan = ReplyPlanner().generate(context=baseline_friend_context)
        ranks = sorted(c.priority_rank for c in plan.candidates)
        assert ranks == [1, 2, 3]

    def test_deterministic_across_calls(self, baseline_friend_context):
        plan1 = ReplyPlanner().generate(context=baseline_friend_context)
        plan2 = ReplyPlanner().generate(context=baseline_friend_context)
        r1 = [c.priority_rank for c in plan1.candidates]
        r2 = [c.priority_rank for c in plan2.candidates]
        assert r1 == r2

    def test_colleague_ranks_stable(self, colleague_context):
        plan = ReplyPlanner().generate(context=colleague_context)
        ranks = sorted(c.priority_rank for c in plan.candidates)
        assert ranks == [1, 2, 3]


# ---------------------------------------------------------------------------
# 11. Non-approved record ids do not leak
# ---------------------------------------------------------------------------


class TestNonApprovedRecordIdIsolation:
    """source_record_ids containing candidate/rejected/frozen record ids
    are not exposed in the output ReplyPlan."""

    def test_source_record_ids_not_in_plan(self):
        skill = ApprovedContactSkillBrief(
            record_id="approved_skill_iso_001",
            contact_id="contact_iso",
            relationship_type="friend",
            relationship_summary="test contact",
            evidence_refs=["ev_iso_001"],
        )
        store = ApprovedStoreContext(
            status="loaded",
            contact_id="contact_iso",
            contact_skill=skill,
            memory_facts=[
                ApprovedMemoryFactBrief(
                    record_id="approved_mem_iso_001",
                    memory_id="mem_iso_001",
                    memory_type="semantic",
                    claim="synthetic fact",
                    evidence_refs=["ev_iso_002"],
                ),
            ],
            source_record_ids=["candidate_record_999", "rejected_record_888"],
            evidence_refs=["ev_iso_001", "ev_iso_002"],
        )
        ctx = context(
            contact_id="contact_iso",
            latest_message_text="hello there",
            recent_events=[event("evt_iso_1", "test event")],
            approved_store_context=store,
        )
        plan = ReplyPlanner().generate(context=ctx)
        plan_json = plan.model_dump_json()
        assert "candidate_record_999" not in plan_json
        assert "rejected_record_888" not in plan_json

    def test_frozen_record_id_not_in_plan(self):
        skill = ApprovedContactSkillBrief(
            record_id="approved_skill_iso_002",
            contact_id="contact_iso2",
            relationship_type="friend",
            relationship_summary="test contact 2",
            evidence_refs=["ev_iso2_001"],
        )
        store = ApprovedStoreContext(
            status="loaded",
            contact_id="contact_iso2",
            contact_skill=skill,
            source_record_ids=["frozen_record_777"],
            evidence_refs=["ev_iso2_001"],
        )
        ctx = context(
            contact_id="contact_iso2",
            latest_message_text="hi",
            approved_store_context=store,
        )
        plan = ReplyPlanner().generate(context=ctx)
        plan_json = plan.model_dump_json()
        assert "frozen_record_777" not in plan_json


# ---------------------------------------------------------------------------
# Structure regression guards (minimum acceptance bar)
# ---------------------------------------------------------------------------


class TestStructureRegression:
    """Minimum acceptance bar: committed tests that fail on structural
    regression of candidate shape, privacy, contact alignment, or
    ranking invariants."""

    def test_candidate_structure_regression_guard(self, baseline_friend_context):
        """Fails if candidate structure regresses (missing fields, wrong types)."""
        plan = ReplyPlanner().generate(context=baseline_friend_context)
        assert isinstance(plan, ReplyPlan)
        assert plan.schema_version == "reply_plan_v1"
        assert plan.plan_mode == "candidate_review_only"
        for c in plan.candidates:
            assert isinstance(c.priority_rank, int)
            assert isinstance(c.confidence, float)
            assert 0.0 <= c.confidence <= 1.0
            assert isinstance(c.supporting_context_refs, list)
            assert isinstance(c.risk_flags, list)
            assert isinstance(c.boundary_reminders, list)

    def test_privacy_regression_guard(self, privacy_probe_context):
        """Fails if private inbound text appears in ReplyPlan output."""
        plan = ReplyPlanner().generate(context=privacy_probe_context)
        plan_json = plan.model_dump_json()
        private_markers = ["abcdef9876", "zyxwv6543", "qprstu3210", "xyzzy123"]
        for marker in private_markers:
            assert marker not in plan_json, f"Private marker {marker} leaked into ReplyPlan"

    def test_contact_alignment_regression_guard(self):
        """Fails if contact alignment check is bypassed."""
        skill = ApprovedContactSkillBrief(
            record_id="skill_reg_guard",
            contact_id="contact_OTHER",
            relationship_type="friend",
            relationship_summary="mismatched",
            evidence_refs=["ev_guard_001"],
        )
        store = ApprovedStoreContext(
            status="loaded",
            contact_id="contact_OTHER",
            contact_skill=skill,
            evidence_refs=["ev_guard_001"],
        )
        ctx = context(
            contact_id="contact_main",
            latest_message_text="hello",
            approved_store_context=store,
        )
        with pytest.raises(ReplyPlannerError):
            ReplyPlanner().generate(context=ctx)

    def test_ranking_invariant_regression_guard(self, baseline_friend_context):
        """Fails if ranking invariants (unique, 1..N) regress."""
        plan = ReplyPlanner().generate(context=baseline_friend_context)
        ranks = [c.priority_rank for c in plan.candidates]
        assert sorted(ranks) == list(range(1, len(ranks) + 1))
