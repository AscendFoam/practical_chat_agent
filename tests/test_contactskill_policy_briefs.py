"""Committed synthetic validation tests for CommunicationPolicyBrief and
BoundaryProfileBrief (T172).

All fixtures are synthetic. No private data, no real contact names,
no real platform IDs, and no raw transcript text.
"""

import pytest
from pydantic import ValidationError

from practical_chat_agent.core.models import (
    ApprovedPatchBrief,
    BoundaryProfileBrief,
    CommunicationPolicyBrief,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_policy_brief(
    *,
    contact_id: str = "contact_synthetic",
    default_approach: str | None = None,
    cold_contact_approach: str | None = None,
    topic_opener_approach: str | None = None,
    sensitive_topic_approach: str | None = None,
    user_goal: str | None = None,
    preferred_reply_style: str | None = None,
    stable_preference_hints: list[str] | None = None,
    approved_patch_hints: list[ApprovedPatchBrief] | None = None,
    evidence_refs: list[str] | None = None,
    source_skill_record_id: str = "skillstore_synthetic_001",
) -> CommunicationPolicyBrief:
    return CommunicationPolicyBrief(
        contact_id=contact_id,
        default_approach=default_approach,
        cold_contact_approach=cold_contact_approach,
        topic_opener_approach=topic_opener_approach,
        sensitive_topic_approach=sensitive_topic_approach,
        user_goal=user_goal,
        preferred_reply_style=preferred_reply_style,
        stable_preference_hints=stable_preference_hints or [],
        approved_patch_hints=approved_patch_hints or [],
        evidence_refs=evidence_refs or [],
        source_skill_record_id=source_skill_record_id,
    )


def _make_boundary_brief(
    *,
    contact_id: str = "contact_synthetic",
    avoid_topics: list[str] | None = None,
    boundary_rules: list[str] | None = None,
    disallowed_uses: list[str] | None = None,
    usage_notes: list[str] | None = None,
    important_event_summaries: list[str] | None = None,
    sensitivity_summary: str = "low",
    evidence_refs: list[str] | None = None,
    source_skill_record_id: str = "skillstore_synthetic_001",
) -> BoundaryProfileBrief:
    return BoundaryProfileBrief(
        contact_id=contact_id,
        avoid_topics=avoid_topics or [],
        boundary_rules=boundary_rules or [],
        disallowed_uses=disallowed_uses or [],
        usage_notes=usage_notes or [],
        important_event_summaries=important_event_summaries or [],
        sensitivity_summary=sensitivity_summary,
        evidence_refs=evidence_refs or [],
        source_skill_record_id=source_skill_record_id,
    )


def _make_patch_brief(
    *,
    patch_id: str = "patch_synthetic_001",
    patch_type: str = "tone_preference",
    compact_instruction: str = "Keep replies concise.",
    sensitivity: str = "low",
) -> ApprovedPatchBrief:
    return ApprovedPatchBrief(
        patch_id=patch_id,
        patch_type=patch_type,
        compact_instruction=compact_instruction,
        sensitivity=sensitivity,
    )


# ===================================================================
# CommunicationPolicyBrief — valid construction
# ===================================================================


class TestPolicyBriefConstruction:
    def test_minimal_valid_policy_brief(self):
        brief = _make_policy_brief()
        assert brief.contact_id == "contact_synthetic"
        assert brief.default_approach is None
        assert brief.cold_contact_approach is None
        assert brief.topic_opener_approach is None
        assert brief.sensitive_topic_approach is None
        assert brief.user_goal is None
        assert brief.preferred_reply_style is None
        assert brief.stable_preference_hints == []
        assert brief.approved_patch_hints == []
        assert brief.evidence_refs == []
        assert brief.source_skill_record_id == "skillstore_synthetic_001"

    def test_full_policy_brief(self):
        patch = _make_patch_brief()
        brief = CommunicationPolicyBrief(
            contact_id="contact_lin",
            default_approach="Warm but respectful",
            cold_contact_approach="Gentle check-in, no pressure",
            topic_opener_approach="Show interest, ask follow-up",
            sensitive_topic_approach="Listen, do not push",
            user_goal="Maintain friendship",
            preferred_reply_style="Casual and supportive",
            stable_preference_hints=["prefers morning texts", "dislikes long voice notes"],
            approved_patch_hints=[patch],
            evidence_refs=["evt_a1", "chk_b2"],
            source_skill_record_id="skillstore_abc123",
        )
        assert brief.contact_id == "contact_lin"
        assert brief.default_approach == "Warm but respectful"
        assert brief.cold_contact_approach == "Gentle check-in, no pressure"
        assert brief.topic_opener_approach == "Show interest, ask follow-up"
        assert brief.sensitive_topic_approach == "Listen, do not push"
        assert brief.user_goal == "Maintain friendship"
        assert brief.preferred_reply_style == "Casual and supportive"
        assert brief.stable_preference_hints == ["prefers morning texts", "dislikes long voice notes"]
        assert len(brief.approved_patch_hints) == 1
        assert brief.approved_patch_hints[0].patch_id == "patch_synthetic_001"
        assert brief.evidence_refs == ["evt_a1", "chk_b2"]


class TestPolicyBriefRequiredFields:
    def test_contact_id_required(self):
        with pytest.raises(ValidationError):
            CommunicationPolicyBrief(
                source_skill_record_id="skillstore_001",
            )

    def test_contact_id_nonempty(self):
        with pytest.raises(ValidationError):
            _make_policy_brief(contact_id="")

    def test_source_skill_record_id_required(self):
        with pytest.raises(ValidationError):
            CommunicationPolicyBrief(
                contact_id="contact_001",
            )

    def test_source_skill_record_id_nonempty(self):
        with pytest.raises(ValidationError):
            _make_policy_brief(source_skill_record_id="")


class TestPolicyBriefSafeDefaults:
    def test_approach_fields_default_none(self):
        brief = _make_policy_brief()
        assert brief.default_approach is None
        assert brief.cold_contact_approach is None
        assert brief.topic_opener_approach is None
        assert brief.sensitive_topic_approach is None

    def test_user_fields_default_none(self):
        brief = _make_policy_brief()
        assert brief.user_goal is None
        assert brief.preferred_reply_style is None

    def test_list_fields_default_empty(self):
        brief = _make_policy_brief()
        assert brief.stable_preference_hints == []
        assert brief.approved_patch_hints == []
        assert brief.evidence_refs == []


class TestPolicyBriefPatchHintEnrichment:
    def test_patch_hint_is_approved_patch_brief(self):
        patch = _make_patch_brief()
        brief = _make_policy_brief(approved_patch_hints=[patch])
        assert isinstance(brief.approved_patch_hints[0], ApprovedPatchBrief)

    def test_multiple_patch_hints(self):
        patches = [
            _make_patch_brief(patch_id=f"patch_{i}", patch_type="tone_preference")
            for i in range(3)
        ]
        brief = _make_policy_brief(approved_patch_hints=patches)
        assert len(brief.approved_patch_hints) == 3

    def test_empty_patch_hints_is_valid(self):
        brief = _make_policy_brief(approved_patch_hints=[])
        assert brief.approved_patch_hints == []


class TestPolicyBriefSerialization:
    def test_round_trip(self):
        patch = _make_patch_brief()
        brief = CommunicationPolicyBrief(
            contact_id="contact_lin",
            default_approach="Warm",
            stable_preference_hints=["prefers brevity"],
            approved_patch_hints=[patch],
            evidence_refs=["evt_001"],
            source_skill_record_id="skillstore_abc",
        )
        data = brief.model_dump()
        restored = CommunicationPolicyBrief.model_validate(data)
        assert restored.contact_id == "contact_lin"
        assert restored.default_approach == "Warm"
        assert restored.stable_preference_hints == ["prefers brevity"]
        assert len(restored.approved_patch_hints) == 1
        assert restored.evidence_refs == ["evt_001"]

    def test_none_fields_excluded(self):
        brief = _make_policy_brief()
        data = brief.model_dump(exclude_none=True)
        assert "default_approach" not in data
        assert "cold_contact_approach" not in data
        assert "contact_id" in data


# ===================================================================
# BoundaryProfileBrief — valid construction
# ===================================================================


class TestBoundaryBriefConstruction:
    def test_minimal_valid_boundary_brief(self):
        brief = _make_boundary_brief()
        assert brief.contact_id == "contact_synthetic"
        assert brief.avoid_topics == []
        assert brief.boundary_rules == []
        assert brief.disallowed_uses == []
        assert brief.usage_notes == []
        assert brief.important_event_summaries == []
        assert brief.sensitivity_summary == "low"
        assert brief.evidence_refs == []
        assert brief.source_skill_record_id == "skillstore_synthetic_001"

    def test_full_boundary_brief(self):
        brief = BoundaryProfileBrief(
            contact_id="contact_lin",
            avoid_topics=["politics", "salary"],
            boundary_rules=["Do not push for personal details"],
            disallowed_uses=["persona_clone", "impersonation"],
            usage_notes=["Handle family topics carefully"],
            important_event_summaries=["Graduation ceremony (2024-06)", "Hospitalization (2025-03)"],
            sensitivity_summary="high",
            evidence_refs=["evt_c1", "evt_c2", "chk_d1"],
            source_skill_record_id="skillstore_abc123",
        )
        assert brief.contact_id == "contact_lin"
        assert brief.avoid_topics == ["politics", "salary"]
        assert brief.boundary_rules == ["Do not push for personal details"]
        assert brief.disallowed_uses == ["persona_clone", "impersonation"]
        assert brief.usage_notes == ["Handle family topics carefully"]
        assert brief.important_event_summaries == ["Graduation ceremony (2024-06)", "Hospitalization (2025-03)"]
        assert brief.sensitivity_summary == "high"
        assert len(brief.evidence_refs) == 3


class TestBoundaryBriefRequiredFields:
    def test_contact_id_required(self):
        with pytest.raises(ValidationError):
            BoundaryProfileBrief(
                source_skill_record_id="skillstore_001",
            )

    def test_contact_id_nonempty(self):
        with pytest.raises(ValidationError):
            _make_boundary_brief(contact_id="")

    def test_source_skill_record_id_required(self):
        with pytest.raises(ValidationError):
            BoundaryProfileBrief(
                contact_id="contact_001",
            )

    def test_source_skill_record_id_nonempty(self):
        with pytest.raises(ValidationError):
            _make_boundary_brief(source_skill_record_id="")


class TestBoundaryBriefSensitivitySummary:
    def test_default_is_low(self):
        brief = _make_boundary_brief()
        assert brief.sensitivity_summary == "low"

    def test_all_valid_sensitivity_values(self):
        for level in ("low", "medium", "high"):
            brief = _make_boundary_brief(sensitivity_summary=level)
            assert brief.sensitivity_summary == level

    def test_invalid_sensitivity_rejected(self):
        with pytest.raises(ValidationError):
            _make_boundary_brief(sensitivity_summary="critical")


class TestBoundaryBriefSafeDefaults:
    def test_all_list_fields_default_empty(self):
        brief = _make_boundary_brief()
        assert brief.avoid_topics == []
        assert brief.boundary_rules == []
        assert brief.disallowed_uses == []
        assert brief.usage_notes == []
        assert brief.important_event_summaries == []
        assert brief.evidence_refs == []

    def test_minimal_brief_serializes_compactly(self):
        brief = _make_boundary_brief()
        data = brief.model_dump()
        assert data["avoid_topics"] == []
        assert data["sensitivity_summary"] == "low"


class TestBoundaryBriefSerialization:
    def test_round_trip(self):
        brief = BoundaryProfileBrief(
            contact_id="contact_lin",
            avoid_topics=["politics"],
            boundary_rules=["Give space"],
            important_event_summaries=["Job change (2024-09)"],
            sensitivity_summary="medium",
            evidence_refs=["evt_e1"],
            source_skill_record_id="skillstore_def",
        )
        data = brief.model_dump()
        restored = BoundaryProfileBrief.model_validate(data)
        assert restored.contact_id == "contact_lin"
        assert restored.avoid_topics == ["politics"]
        assert restored.boundary_rules == ["Give space"]
        assert restored.important_event_summaries == ["Job change (2024-09)"]
        assert restored.sensitivity_summary == "medium"
        assert restored.evidence_refs == ["evt_e1"]


# ===================================================================
# Cross-brief and shared contract tests
# ===================================================================


class TestCrossBriefSharedContract:
    def test_both_briefs_share_source_skill_record_id(self):
        policy = _make_policy_brief(source_skill_record_id="skillstore_shared")
        boundary = _make_boundary_brief(source_skill_record_id="skillstore_shared")
        assert policy.source_skill_record_id == boundary.source_skill_record_id

    def test_evidence_refs_flat_in_both_briefs(self):
        policy = _make_policy_brief(evidence_refs=["evt_001", "evt_002"])
        boundary = _make_boundary_brief(evidence_refs=["evt_003"])
        assert isinstance(policy.evidence_refs, list)
        assert isinstance(boundary.evidence_refs, list)
        assert len(policy.evidence_refs) == 2
        assert len(boundary.evidence_refs) == 1

    def test_contact_id_shared_across_briefs(self):
        policy = _make_policy_brief(contact_id="contact_lin")
        boundary = _make_boundary_brief(contact_id="contact_lin")
        assert policy.contact_id == boundary.contact_id

    def test_no_schema_version_field(self):
        policy = _make_policy_brief()
        boundary = _make_boundary_brief()
        assert not hasattr(policy, "schema_version")
        assert not hasattr(boundary, "schema_version")

    def test_no_approval_status_field(self):
        policy = _make_policy_brief()
        boundary = _make_boundary_brief()
        assert not hasattr(policy, "status")
        assert not hasattr(boundary, "status")
