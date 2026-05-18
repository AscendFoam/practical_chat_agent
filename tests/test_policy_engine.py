"""T151: ReplyPlanPolicyEngine direct policy fixture suite.

Deterministic tests covering policy layer behavior directly,
complementing T150's planner-through-policy coverage.

Required coverage areas (indexed by T151 task package):
  1. direct ReplyPlanPolicyEngine.build_profile() expectations per fixture
  2. direct ReplyPlanPolicyEngine.assess_candidate() for over-proactivity
  3. direct ReplyPlanPolicyEngine.assess_candidate() for impersonation risk
  4. loaded-but-no-skill thin context vs not_configured thin context
  5. degraded store status (store_path_missing)
  6. notes_on_candidate_differences when policy state should populate them
  7. false-positive probe: sensitive keyword without boundary escalation
  8. false-negative probe: documented accepted limitation
  9. over-proactivity probe: conservative mode + avoid_follow_up interaction
 10. confidence penalty accumulation
 11. no-pressure cue exemption from over-proactive

All fixtures are synthetic and contain no private chat content,
real names, real platform IDs, or private paths.
"""
from __future__ import annotations

from practical_chat_agent.services.policy import (
    ReplyCandidatePolicyAssessment,
    ReplyPlanPolicyEngine,
    ReplyPlanPolicyProfile,
)

from tests.helpers import context, event, memory_brief, skill_brief


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

_engine = ReplyPlanPolicyEngine()


def _profile(**kwargs) -> ReplyPlanPolicyProfile:
    """Shorthand for constructing a policy profile for assess_candidate tests."""
    return ReplyPlanPolicyProfile(**kwargs)


# ---------------------------------------------------------------------------
# 1. Build profile: baseline friend
# ---------------------------------------------------------------------------


class TestBuildProfileBaselineFriend:
    """baseline_friend_context should produce a clean, non-conservative profile."""

    def test_thin_context_is_false(self, baseline_friend_context):
        profile = _engine.build_profile(context=baseline_friend_context)
        assert profile.thin_context is False

    def test_boundary_sensitive_is_false(self, baseline_friend_context):
        profile = _engine.build_profile(context=baseline_friend_context)
        assert profile.boundary_sensitive is False

    def test_conservative_mode_is_false(self, baseline_friend_context):
        profile = _engine.build_profile(context=baseline_friend_context)
        assert profile.conservative_mode is False

    def test_practical_tone_is_false(self, baseline_friend_context):
        profile = _engine.build_profile(context=baseline_friend_context)
        assert profile.practical_tone is False

    def test_context_risk_flags_empty(self, baseline_friend_context):
        profile = _engine.build_profile(context=baseline_friend_context)
        assert profile.context_risk_flags == []

    def test_avoid_follow_up_is_false(self, baseline_friend_context):
        profile = _engine.build_profile(context=baseline_friend_context)
        assert profile.avoid_follow_up is False


# ---------------------------------------------------------------------------
# 2. Build profile: colleague
# ---------------------------------------------------------------------------


class TestBuildProfileColleague:
    """colleague_context should activate practical_tone."""

    def test_practical_tone_is_true(self, colleague_context):
        profile = _engine.build_profile(context=colleague_context)
        assert profile.practical_tone is True

    def test_thin_context_is_false(self, colleague_context):
        profile = _engine.build_profile(context=colleague_context)
        assert profile.thin_context is False

    def test_conservative_mode_is_false(self, colleague_context):
        profile = _engine.build_profile(context=colleague_context)
        assert profile.conservative_mode is False

    def test_context_risk_flags_empty(self, colleague_context):
        profile = _engine.build_profile(context=colleague_context)
        assert profile.context_risk_flags == []

    def test_policy_summary_mentions_practical(self, colleague_context):
        profile = _engine.build_profile(context=colleague_context)
        text = " ".join(profile.policy_boundary_summary).lower()
        assert "practical" in text


# ---------------------------------------------------------------------------
# 3. Build profile: thin context (not_configured)
# ---------------------------------------------------------------------------


class TestBuildProfileThinContext:
    """thin_context fixture produces thin_context and conservative_mode."""

    def test_thin_context_is_true(self, thin_context):
        profile = _engine.build_profile(context=thin_context)
        assert profile.thin_context is True

    def test_conservative_mode_is_true(self, thin_context):
        profile = _engine.build_profile(context=thin_context)
        assert profile.conservative_mode is True

    def test_context_risk_flags_contains_thin_context(self, thin_context):
        profile = _engine.build_profile(context=thin_context)
        assert "thin_context" in profile.context_risk_flags

    def test_policy_summary_mentions_thin(self, thin_context):
        profile = _engine.build_profile(context=thin_context)
        text = " ".join(profile.policy_boundary_summary).lower()
        assert "thin" in text

    def test_shared_boundary_reminders_non_empty(self, thin_context):
        profile = _engine.build_profile(context=thin_context)
        assert len(profile.shared_boundary_reminders) >= 1


# ---------------------------------------------------------------------------
# 4. Build profile: loaded but no skill
# ---------------------------------------------------------------------------


class TestBuildProfileLoadedNoSkill:
    """loaded_no_skill_context: status='loaded' but contact_skill is None.

    This produces thin_context=True despite loaded status, because the
    skill brief is absent.  This is distinct from the generic thin_context
    fixture which uses status='not_configured'.
    """

    def test_thin_context_true_despite_loaded(self, loaded_no_skill_context):
        profile = _engine.build_profile(context=loaded_no_skill_context)
        assert profile.thin_context is True

    def test_conservative_mode_is_true(self, loaded_no_skill_context):
        profile = _engine.build_profile(context=loaded_no_skill_context)
        assert profile.conservative_mode is True

    def test_context_risk_flags_contains_thin(self, loaded_no_skill_context):
        profile = _engine.build_profile(context=loaded_no_skill_context)
        assert "thin_context" in profile.context_risk_flags

    def test_boundary_sensitive_is_false(self, loaded_no_skill_context):
        """No boundary cues or sensitive content, so boundary_sensitive stays False."""
        profile = _engine.build_profile(context=loaded_no_skill_context)
        assert profile.boundary_sensitive is False


# ---------------------------------------------------------------------------
# 5. Build profile: degraded store (store_path_missing)
# ---------------------------------------------------------------------------


class TestBuildProfileDegradedStore:
    """degraded_store_context: status='store_path_missing'.

    Any non-loaded status produces thin_context=True, even if it is not
    the generic 'not_configured' value.
    """

    def test_thin_context_is_true(self, degraded_store_context):
        profile = _engine.build_profile(context=degraded_store_context)
        assert profile.thin_context is True

    def test_conservative_mode_is_true(self, degraded_store_context):
        profile = _engine.build_profile(context=degraded_store_context)
        assert profile.conservative_mode is True

    def test_context_risk_flags_contains_thin(self, degraded_store_context):
        profile = _engine.build_profile(context=degraded_store_context)
        assert "thin_context" in profile.context_risk_flags

    def test_boundary_sensitive_is_false(self, degraded_store_context):
        """No boundary keywords or sensitive content, so boundary_sensitive stays False."""
        profile = _engine.build_profile(context=degraded_store_context)
        assert profile.boundary_sensitive is False


# ---------------------------------------------------------------------------
# 6. Build profile: sensitive/boundary
# ---------------------------------------------------------------------------


class TestBuildProfileSensitive:
    """sensitive_context produces boundary_sensitive, avoid_follow_up, conservative_mode."""

    def test_boundary_sensitive_is_true(self, sensitive_context):
        profile = _engine.build_profile(context=sensitive_context)
        assert profile.boundary_sensitive is True

    def test_conservative_mode_is_true(self, sensitive_context):
        profile = _engine.build_profile(context=sensitive_context)
        assert profile.conservative_mode is True

    def test_avoid_follow_up_is_true(self, sensitive_context):
        profile = _engine.build_profile(context=sensitive_context)
        assert profile.avoid_follow_up is True

    def test_context_risk_flags_contains_boundary_sensitive(self, sensitive_context):
        profile = _engine.build_profile(context=sensitive_context)
        assert "boundary_sensitive" in profile.context_risk_flags

    def test_policy_summary_mentions_sensitive(self, sensitive_context):
        profile = _engine.build_profile(context=sensitive_context)
        text = " ".join(profile.policy_boundary_summary).lower()
        assert "sensitive" in text


# ---------------------------------------------------------------------------
# 7. Build profile: false-positive probe
# ---------------------------------------------------------------------------


class TestBuildProfileFalsePositive:
    """false_positive_probe_context: 'money' in work context should not
    trigger boundary_sensitive because intent is GENERAL and no boundary
    cues are present."""

    def test_boundary_sensitive_is_false(self, false_positive_probe_context):
        profile = _engine.build_profile(context=false_positive_probe_context)
        assert profile.boundary_sensitive is False

    def test_thin_context_is_false(self, false_positive_probe_context):
        profile = _engine.build_profile(context=false_positive_probe_context)
        assert profile.thin_context is False

    def test_conservative_mode_is_false(self, false_positive_probe_context):
        profile = _engine.build_profile(context=false_positive_probe_context)
        assert profile.conservative_mode is False

    def test_no_unexpected_risk_flags(self, false_positive_probe_context):
        profile = _engine.build_profile(context=false_positive_probe_context)
        assert profile.context_risk_flags == []


# ---------------------------------------------------------------------------
# 8. Build profile: false-negative probe (accepted limitation)
# ---------------------------------------------------------------------------


class TestBuildProfileFalseNegative:
    """false_negative_probe_context: subtle pacing pressure not detected.

    "you should really call me sometime soon" does not match any
    _BOUNDARY_CUE_KEYWORDS, and intent is GENERAL, so boundary_sensitive
    stays False.  This is a documented accepted limitation of
    keyword-based policy detection.
    """

    def test_boundary_sensitive_is_false(self, false_negative_probe_context):
        profile = _engine.build_profile(context=false_negative_probe_context)
        assert profile.boundary_sensitive is False

    def test_thin_context_is_false(self, false_negative_probe_context):
        profile = _engine.build_profile(context=false_negative_probe_context)
        assert profile.thin_context is False

    def test_conservative_mode_is_false(self, false_negative_probe_context):
        profile = _engine.build_profile(context=false_negative_probe_context)
        assert profile.conservative_mode is False


# ---------------------------------------------------------------------------
# 9. Build profile: over-proactivity probe context
# ---------------------------------------------------------------------------


class TestBuildProfileOverProactivity:
    """over_proactivity_probe_context: skill boundary reminders carry
    'do not push' and 'low pressure' cues, triggering both
    boundary_sensitive and avoid_follow_up via explicit keyword matching."""

    def test_avoid_follow_up_is_true(self, over_proactivity_probe_context):
        profile = _engine.build_profile(context=over_proactivity_probe_context)
        assert profile.avoid_follow_up is True

    def test_boundary_sensitive_is_true(self, over_proactivity_probe_context):
        profile = _engine.build_profile(context=over_proactivity_probe_context)
        assert profile.boundary_sensitive is True

    def test_conservative_mode_is_true(self, over_proactivity_probe_context):
        profile = _engine.build_profile(context=over_proactivity_probe_context)
        assert profile.conservative_mode is True

    def test_thin_context_is_false(self, over_proactivity_probe_context):
        """Store is loaded with a skill, so thin_context is False."""
        profile = _engine.build_profile(context=over_proactivity_probe_context)
        assert profile.thin_context is False


# ---------------------------------------------------------------------------
# 10. Assess candidate: action push cues
# ---------------------------------------------------------------------------


class TestAssessCandidateActionPush:
    """Action push cues always trigger over_proactive, even in
    non-conservative mode."""

    def test_call_always_over_proactive(self):
        neutral_profile = _profile()
        result = _engine.assess_candidate(
            policy_profile=neutral_profile,
            candidate_text="we should call to discuss this",
            approach_label="conservative_acknowledgment",
        )
        assert "over_proactive" in result.risk_flags

    def test_meet_always_over_proactive(self):
        neutral_profile = _profile()
        result = _engine.assess_candidate(
            policy_profile=neutral_profile,
            candidate_text="let's meet up and talk",
            approach_label="conservative_acknowledgment",
        )
        assert "over_proactive" in result.risk_flags

    def test_chinese_action_push_over_proactive(self):
        neutral_profile = _profile()
        result = _engine.assess_candidate(
            policy_profile=neutral_profile,
            candidate_text="我们打电话聊聊吧",
            approach_label="conservative_acknowledgment",
        )
        assert "over_proactive" in result.risk_flags

    def test_schedule_always_over_proactive(self):
        neutral_profile = _profile()
        result = _engine.assess_candidate(
            policy_profile=neutral_profile,
            candidate_text="can we schedule a time to catch up",
            approach_label="conservative_acknowledgment",
        )
        assert "over_proactive" in result.risk_flags


# ---------------------------------------------------------------------------
# 11. Assess candidate: over-proactive in conservative mode
# ---------------------------------------------------------------------------


class TestAssessCandidateOverProactiveConservativeMode:
    """In conservative/avoid_follow_up mode, optional_follow_up approach
    label always triggers over_proactive, and paced_next_step with
    over-proactive draft cues also triggers."""

    def test_optional_follow_up_over_proactive_in_conservative(self):
        conservative_profile = _profile(conservative_mode=True, avoid_follow_up=True)
        result = _engine.assess_candidate(
            policy_profile=conservative_profile,
            candidate_text="if you want, you can share more later",
            approach_label="optional_follow_up",
        )
        assert "over_proactive" in result.risk_flags

    def test_paced_next_step_with_proactive_cues(self):
        conservative_profile = _profile(conservative_mode=True, avoid_follow_up=True)
        result = _engine.assess_candidate(
            policy_profile=conservative_profile,
            candidate_text="let's follow up on this next week",
            approach_label="paced_next_step",
        )
        assert "over_proactive" in result.risk_flags

    def test_conservative_acknowledgment_safe_without_cues(self):
        """conservative_acknowledgment without action/proactive cues stays clean."""
        conservative_profile = _profile(conservative_mode=True, avoid_follow_up=True)
        result = _engine.assess_candidate(
            policy_profile=conservative_profile,
            candidate_text="got it, I'll keep this in mind",
            approach_label="conservative_acknowledgment",
        )
        assert "over_proactive" not in result.risk_flags


# ---------------------------------------------------------------------------
# 12. Assess candidate: no-pressure exemption
# ---------------------------------------------------------------------------


class TestAssessCandidateNoPressureExemption:
    """No-pressure cues exempt a candidate from over_proactive even in
    conservative mode, unless an action push cue is also present."""

    def test_no_rush_exempted(self):
        conservative_profile = _profile(conservative_mode=True, avoid_follow_up=True)
        result = _engine.assess_candidate(
            policy_profile=conservative_profile,
            candidate_text="no rush, whenever you feel ready",
            approach_label="paced_next_step",
        )
        assert "over_proactive" not in result.risk_flags

    def test_chinese_no_pressure_exempted(self):
        conservative_profile = _profile(conservative_mode=True, avoid_follow_up=True)
        result = _engine.assess_candidate(
            policy_profile=conservative_profile,
            candidate_text="先不往前推，等你方便的时候再继续",
            approach_label="paced_next_step",
        )
        assert "over_proactive" not in result.risk_flags

    def test_action_push_overrides_no_pressure(self):
        """Action push cues take precedence over no-pressure cues."""
        conservative_profile = _profile(conservative_mode=True, avoid_follow_up=True)
        result = _engine.assess_candidate(
            policy_profile=conservative_profile,
            candidate_text="no rush, but let's call when you're free",
            approach_label="paced_next_step",
        )
        assert "over_proactive" in result.risk_flags


# ---------------------------------------------------------------------------
# 13. Assess candidate: impersonation risk
# ---------------------------------------------------------------------------


class TestAssessCandidateImpersonationRisk:
    """Impersonation cues in candidate text trigger impersonation_risk flag."""

    def test_he_would_say_detected(self):
        neutral_profile = _profile()
        result = _engine.assess_candidate(
            policy_profile=neutral_profile,
            candidate_text="he would say something like this",
            approach_label="conservative_acknowledgment",
        )
        assert "impersonation_risk" in result.risk_flags

    def test_she_would_say_detected(self):
        neutral_profile = _profile()
        result = _engine.assess_candidate(
            policy_profile=neutral_profile,
            candidate_text="she would say something like that",
            approach_label="conservative_acknowledgment",
        )
        assert "impersonation_risk" in result.risk_flags

    def test_chinese_impersonation_detected(self):
        neutral_profile = _profile()
        result = _engine.assess_candidate(
            policy_profile=neutral_profile,
            candidate_text="对方会怎么想呢",
            approach_label="conservative_acknowledgment",
        )
        assert "impersonation_risk" in result.risk_flags

    def test_impersonation_adds_boundary_reminder(self):
        neutral_profile = _profile()
        result = _engine.assess_candidate(
            policy_profile=neutral_profile,
            candidate_text="he would say that to you",
            approach_label="conservative_acknowledgment",
        )
        all_reminders = " ".join(result.boundary_reminders).lower()
        assert "voice" in all_reminders or "impersonat" in all_reminders or "predict" in all_reminders

    def test_clean_text_no_impersonation(self):
        neutral_profile = _profile()
        result = _engine.assess_candidate(
            policy_profile=neutral_profile,
            candidate_text="sounds good, I'll get back to you later",
            approach_label="conservative_acknowledgment",
        )
        assert "impersonation_risk" not in result.risk_flags


# ---------------------------------------------------------------------------
# 14. Assess candidate: confidence penalty
# ---------------------------------------------------------------------------


class TestAssessCandidateConfidencePenalty:
    """Confidence penalties accumulate from thin_context, boundary_sensitive,
    over_proactive, and impersonation_risk."""

    def test_thin_context_penalty(self):
        thin_profile = _profile(thin_context=True)
        result = _engine.assess_candidate(
            policy_profile=thin_profile,
            candidate_text="acknowledged",
            approach_label="conservative_acknowledgment",
        )
        assert result.confidence_penalty >= 0.10

    def test_boundary_sensitive_penalty(self):
        sensitive_profile = _profile(boundary_sensitive=True)
        result = _engine.assess_candidate(
            policy_profile=sensitive_profile,
            candidate_text="acknowledged",
            approach_label="conservative_acknowledgment",
        )
        assert result.confidence_penalty >= 0.06

    def test_combined_thin_and_boundary_penalty(self):
        both_profile = _profile(thin_context=True, boundary_sensitive=True)
        result = _engine.assess_candidate(
            policy_profile=both_profile,
            candidate_text="acknowledged",
            approach_label="conservative_acknowledgment",
        )
        assert result.confidence_penalty >= 0.16

    def test_impersonation_penalty_larger(self):
        neutral_profile = _profile()
        result = _engine.assess_candidate(
            policy_profile=neutral_profile,
            candidate_text="he would say this",
            approach_label="conservative_acknowledgment",
        )
        assert result.confidence_penalty >= 0.15

    def test_no_penalty_for_clean_candidate(self):
        neutral_profile = _profile()
        result = _engine.assess_candidate(
            policy_profile=neutral_profile,
            candidate_text="got it, thanks for letting me know",
            approach_label="conservative_acknowledgment",
        )
        assert result.confidence_penalty == 0.0


# ---------------------------------------------------------------------------
# 15. Notes on candidate differences (through planner)
# ---------------------------------------------------------------------------


class TestNotesOnCandidateDifferences:
    """notes_on_candidate_differences populated based on policy state."""

    def test_baseline_default_notes(self, baseline_friend_context):
        from practical_chat_agent.services.reply_planner import ReplyPlanner

        plan = ReplyPlanner().generate(context=baseline_friend_context)
        notes = plan.notes_on_candidate_differences
        assert len(notes) >= 3
        assert any("Candidate 1" in n for n in notes)
        assert any("Candidate 2" in n for n in notes)
        assert any("Candidate 3" in n for n in notes)

    def test_conservative_mode_shifts_notes(self, sensitive_context):
        from practical_chat_agent.services.reply_planner import ReplyPlanner

        plan = ReplyPlanner().generate(context=sensitive_context)
        notes = plan.notes_on_candidate_differences
        notes_text = " ".join(notes).lower()
        assert "no-pressure" in notes_text or "avoiding" in notes_text

    def test_thin_not_loaded_adds_extra_note(self, thin_context):
        from practical_chat_agent.services.reply_planner import ReplyPlanner

        plan = ReplyPlanner().generate(context=thin_context)
        notes = plan.notes_on_candidate_differences
        notes_text = " ".join(notes).lower()
        assert "thin" in notes_text

    def test_loaded_no_skill_conservative_without_thin_note(self, loaded_no_skill_context):
        """loaded_no_skill is conservative but status IS loaded, so the
        'thin store context' extra note should NOT appear."""
        from practical_chat_agent.services.reply_planner import ReplyPlanner

        plan = ReplyPlanner().generate(context=loaded_no_skill_context)
        notes = plan.notes_on_candidate_differences
        notes_text = " ".join(notes).lower()
        assert "approved store context is thin" not in notes_text
        assert "no-pressure" in notes_text or "avoiding" in notes_text

    def test_boundary_sensitive_adds_extra_note(self, sensitive_context):
        from practical_chat_agent.services.reply_planner import ReplyPlanner

        plan = ReplyPlanner().generate(context=sensitive_context)
        notes = plan.notes_on_candidate_differences
        notes_text = " ".join(notes).lower()
        assert "sensitive" in notes_text or "boundary" in notes_text


# ---------------------------------------------------------------------------
# 16. Planner-through-policy integration for over-proactivity probe
# ---------------------------------------------------------------------------


class TestOverProactivityPlannerIntegration:
    """Over-proactivity probe context produces a plan where at least one
    candidate carries over_proactive risk flag."""

    def test_at_least_one_over_proactive_flag(self, over_proactivity_probe_context):
        from practical_chat_agent.services.reply_planner import ReplyPlanner

        plan = ReplyPlanner().generate(context=over_proactivity_probe_context)
        all_flags = [f for c in plan.candidates for f in c.risk_flags]
        assert "over_proactive" in all_flags

    def test_conservative_mode_candidates_valid(self, over_proactivity_probe_context):
        from practical_chat_agent.services.reply_planner import ReplyPlanner

        plan = ReplyPlanner().generate(context=over_proactivity_probe_context)
        assert len(plan.candidates) == 3
        for c in plan.candidates:
            assert c.draft_text
            assert c.rationale
