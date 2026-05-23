"""Committed synthetic validation tests for ContactSkillProjectionService (T173).

All fixtures are synthetic. No private data, no real contact names,
no real platform IDs, and no raw transcript text.
"""

import pytest

from practical_chat_agent.core.models import (
    ApprovedPatchBrief,
    BoundaryProfileBrief,
    CommunicationPolicyBrief,
    CommunicationStyleSnapshot,
    ContactSkillCandidate,
    ContactSkillCommunicationStyle,
    ContactSkillImportantEvent,
    ContactSkillPattern,
    ContactSkillRelationshipState,
    ContactSkillReplyStrategy,
    ContactSkillStoreRecord,
    ContactSkillTopicPreference,
    ContactSkillUsageBoundary,
    ContactSkillUserSidePreferences,
    DistilledArtifactReviewMetadata,
    PartnerPersonaBrief,
)
from practical_chat_agent.services.contact_skill import (
    ContactSkillProjectionResult,
    ContactSkillProjectionService,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_relationship_state(
    *,
    current_status: str = "low_frequency_but_continuing",
    closeness: float = 0.45,
    trust_level: float = 0.50,
    interaction_frequency: str = "low",
    initiative_balance: str = "user_leads_more",
    confidence: float = 0.70,
    evidence_refs: list[str] | None = None,
    sensitivity: str = "low",
    status: str = "approved",
) -> ContactSkillRelationshipState:
    return ContactSkillRelationshipState(
        current_status=current_status,
        closeness=closeness,
        trust_level=trust_level,
        interaction_frequency=interaction_frequency,
        initiative_balance=initiative_balance,
        confidence=confidence,
        evidence_refs=evidence_refs or ["evt_r01"],
        sensitivity=sensitivity,
        status=status,
    )


def _make_communication_style(
    *,
    message_length: str = "short",
    tone: str = "casual",
    response_latency: str = "unknown",
    directness: str = "medium",
    confidence: float = 0.60,
    evidence_refs: list[str] | None = None,
    sensitivity: str = "low",
    status: str = "approved",
) -> ContactSkillCommunicationStyle:
    return ContactSkillCommunicationStyle(
        message_length=message_length,
        tone=tone,
        response_latency=response_latency,
        directness=directness,
        confidence=confidence,
        evidence_refs=evidence_refs or ["evt_c01"],
        sensitivity=sensitivity,
        status=status,
    )


def _make_topic(
    *,
    topic: str = "study_progress",
    sensitivity: str = "low",
    evidence_refs: list[str] | None = None,
) -> ContactSkillTopicPreference:
    return ContactSkillTopicPreference(
        topic=topic,
        reason="Synthetic reason.",
        claim=f"Synthetic claim about {topic}.",
        evidence_refs=evidence_refs or ["evt_t01"],
        confidence=0.70,
        sensitivity=sensitivity,
        status="approved",
    )


def _make_pattern(
    *,
    pattern: str = "Keep replies concise.",
    sensitivity: str = "low",
    evidence_refs: list[str] | None = None,
) -> ContactSkillPattern:
    return ContactSkillPattern(
        pattern=pattern,
        claim=f"Synthetic claim: {pattern}",
        evidence_refs=evidence_refs or ["evt_p01"],
        confidence=0.65,
        sensitivity=sensitivity,
        status="approved",
    )


def _make_event(
    *,
    event: str = "Graduation ceremony",
    date: str | None = "2024-06",
    sensitivity: str = "medium",
    evidence_refs: list[str] | None = None,
) -> ContactSkillImportantEvent:
    return ContactSkillImportantEvent(
        event=event,
        date=date,
        claim=f"Synthetic claim about {event}.",
        evidence_refs=evidence_refs or ["evt_e01"],
        confidence=0.75,
        sensitivity=sensitivity,
        status="approved",
        importance=0.80,
    )


def _make_store_record(
    *,
    contact_id: str = "contact_synthetic",
    record_id: str = "skillstore_synthetic_001",
    runtime_ready: bool = True,
    candidate_status: str | None = None,
    sensitivity: str = "low",
    relationship_state: ContactSkillRelationshipState | None = None,
    communication_style: ContactSkillCommunicationStyle | None = None,
    preferred_topics: list[ContactSkillTopicPreference] | None = None,
    avoid_topics: list[ContactSkillTopicPreference] | None = None,
    important_events: list[ContactSkillImportantEvent] | None = None,
    stable_preferences: list[ContactSkillPattern] | None = None,
    emotional_patterns: list[ContactSkillPattern] | None = None,
    user_side_preferences: ContactSkillUserSidePreferences | None = None,
    reply_strategy: ContactSkillReplyStrategy | None = None,
    usage_boundary: ContactSkillUsageBoundary | None = None,
) -> ContactSkillStoreRecord:
    if runtime_ready:
        status = "approved"
        review_metadata = DistilledArtifactReviewMetadata(
            review_state="reviewed",
            reviewed_by_human=True,
            last_decision="approved",
        )
    else:
        status = candidate_status or "candidate"
        review_metadata = DistilledArtifactReviewMetadata()
    candidate = ContactSkillCandidate(
        contact_id=contact_id,
        relationship_type="friend",
        status=status,
        confidence=0.70,
        sensitivity=sensitivity,
        evidence_refs=["evt_agg01", "evt_agg02"],
        relationship_state=relationship_state or _make_relationship_state(),
        communication_style=communication_style or _make_communication_style(),
        preferred_topics=preferred_topics or [],
        avoid_topics=avoid_topics or [],
        important_events=important_events or [],
        stable_preferences=stable_preferences or [],
        emotional_patterns=emotional_patterns or [],
        user_side_preferences=user_side_preferences or ContactSkillUserSidePreferences(),
        reply_strategy=reply_strategy or ContactSkillReplyStrategy(),
        usage_boundary=usage_boundary or ContactSkillUsageBoundary(),
    )
    return ContactSkillStoreRecord(
        record_id=record_id,
        contact_skill=candidate,
        review_metadata=review_metadata,
    )


def _project(**kwargs) -> ContactSkillProjectionResult:
    svc = ContactSkillProjectionService()
    record = _make_store_record(**kwargs)
    return svc.project_all(record=record)


# ===================================================================
# Approved / runtime-ready projection success
# ===================================================================


class TestApprovedProjectionSuccess:
    def test_all_three_briefs_produced(self):
        result = _project(runtime_ready=True)
        assert result.runtime_ready is True
        assert result.persona is not None
        assert result.policy is not None
        assert result.boundary is not None

    def test_persona_is_partner_persona_brief(self):
        result = _project(runtime_ready=True)
        assert isinstance(result.persona, PartnerPersonaBrief)

    def test_policy_is_communication_policy_brief(self):
        result = _project(runtime_ready=True)
        assert isinstance(result.policy, CommunicationPolicyBrief)

    def test_boundary_is_boundary_profile_brief(self):
        result = _project(runtime_ready=True)
        assert isinstance(result.boundary, BoundaryProfileBrief)


# ===================================================================
# Non-runtime-ready exclusion
# ===================================================================


class TestNonRuntimeReadyExclusion:
    def test_candidate_excluded(self):
        result = _project(runtime_ready=False, candidate_status="candidate")
        assert result.runtime_ready is False
        assert result.persona is None
        assert result.policy is None
        assert result.boundary is None

    def test_rejected_excluded(self):
        result = _project(runtime_ready=False, candidate_status="rejected")
        assert result.runtime_ready is False
        assert result.persona is None

    def test_frozen_excluded(self):
        result = _project(runtime_ready=False, candidate_status="frozen")
        assert result.runtime_ready is False
        assert result.policy is None

    def test_archived_excluded(self):
        result = _project(runtime_ready=False, candidate_status="archived")
        assert result.runtime_ready is False
        assert result.boundary is None

    def test_approved_without_human_review_excluded(self):
        record = _make_store_record(runtime_ready=False)
        record.contact_skill.status = "approved"
        svc = ContactSkillProjectionService()
        result = svc.project_all(record=record)
        assert result.runtime_ready is False


# ===================================================================
# Contact-id / traceability preservation
# ===================================================================


class TestContactIdTraceability:
    def test_contact_id_in_result(self):
        result = _project(contact_id="contact_lin")
        assert result.contact_id == "contact_lin"

    def test_source_skill_record_id_in_all_briefs(self):
        result = _project(record_id="skillstore_abc123")
        assert result.persona is not None
        assert result.policy is not None
        assert result.boundary is not None
        assert result.persona.source_skill_record_id == "skillstore_abc123"
        assert result.policy.source_skill_record_id == "skillstore_abc123"
        assert result.boundary.source_skill_record_id == "skillstore_abc123"

    def test_record_id_in_result(self):
        result = _project(record_id="skillstore_xyz")
        assert result.record_id == "skillstore_xyz"

    def test_contact_id_in_each_brief(self):
        result = _project(contact_id="contact_test")
        assert result.persona is not None
        assert result.persona.contact_id == "contact_test"
        assert result.policy is not None
        assert result.policy.contact_id == "contact_test"
        assert result.boundary is not None
        assert result.boundary.contact_id == "contact_test"


# ===================================================================
# "unknown" -> None communication-style conversion
# ===================================================================


class TestUnknownToNoneCommunicationStyle:
    def test_all_unknown_produces_all_none(self):
        result = _project(
            runtime_ready=True,
            communication_style=_make_communication_style(
                message_length="unknown",
                tone="unknown",
                response_latency="unknown",
                directness="unknown",
            ),
        )
        assert result.persona is not None
        snap = result.persona.communication_style_snapshot
        assert snap.message_length is None
        assert snap.tone is None
        assert snap.response_latency is None
        assert snap.directness is None

    def test_mixed_unknown_known(self):
        result = _project(
            runtime_ready=True,
            communication_style=_make_communication_style(
                message_length="short",
                tone="unknown",
                response_latency="fast",
                directness="unknown",
            ),
        )
        assert result.persona is not None
        snap = result.persona.communication_style_snapshot
        assert snap.message_length == "short"
        assert snap.tone is None
        assert snap.response_latency == "fast"
        assert snap.directness is None

    def test_all_known_preserved(self):
        result = _project(
            runtime_ready=True,
            communication_style=_make_communication_style(
                message_length="long",
                tone="warm",
                response_latency="slow",
                directness="high",
            ),
        )
        assert result.persona is not None
        snap = result.persona.communication_style_snapshot
        assert snap.message_length == "long"
        assert snap.tone == "warm"
        assert snap.response_latency == "slow"
        assert snap.directness == "high"


# ===================================================================
# relationship_state_summary projection rule
# ===================================================================


class TestRelationshipStateSummary:
    def test_summary_contains_all_dimensions(self):
        result = _project(
            runtime_ready=True,
            relationship_state=_make_relationship_state(
                current_status="active_exchange",
                closeness=0.72,
                trust_level=0.65,
                interaction_frequency="high",
                initiative_balance="balanced",
            ),
        )
        assert result.persona is not None
        summary = result.persona.relationship_state_summary
        assert "active_exchange" in summary
        assert "closeness=0.72" in summary
        assert "trust=0.65" in summary
        assert "freq=high" in summary
        assert "initiative=balanced" in summary

    def test_summary_deterministic(self):
        state = _make_relationship_state(current_status="warm_period", closeness=0.50)
        result_a = _project(runtime_ready=True, relationship_state=state)
        result_b = _project(runtime_ready=True, relationship_state=state)
        assert result_a.persona is not None
        assert result_b.persona is not None
        assert result_a.persona.relationship_state_summary == result_b.persona.relationship_state_summary

    def test_summary_never_empty(self):
        result = _project(runtime_ready=True)
        assert result.persona is not None
        assert len(result.persona.relationship_state_summary) > 0


# ===================================================================
# Thin policy evidence (CommunicationPolicyBrief)
# ===================================================================


class TestThinPolicyEvidence:
    def test_empty_when_no_stable_preferences(self):
        result = _project(runtime_ready=True, stable_preferences=[])
        assert result.policy is not None
        assert result.policy.evidence_refs == []

    def test_only_stable_preference_refs(self):
        prefs = [
            _make_pattern(pattern="Be concise.", evidence_refs=["evt_sp01", "evt_sp02"]),
            _make_pattern(pattern="Stay practical.", evidence_refs=["evt_sp03"]),
        ]
        result = _project(runtime_ready=True, stable_preferences=prefs)
        assert result.policy is not None
        assert set(result.policy.evidence_refs) == {"evt_sp01", "evt_sp02", "evt_sp03"}

    def test_reply_strategy_contributes_no_evidence(self):
        result = _project(
            runtime_ready=True,
            reply_strategy=ContactSkillReplyStrategy(
                default="Warm reply.",
                when_contact_is_cold="Gentle check-in.",
            ),
            stable_preferences=[],
        )
        assert result.policy is not None
        assert result.policy.default_approach == "Warm reply."
        assert result.policy.cold_contact_approach == "Gentle check-in."
        assert result.policy.evidence_refs == []


# ===================================================================
# Explicit sensitivity_summary computation
# ===================================================================


class TestSensitivitySummaryComputation:
    def test_default_is_parent_aggregate(self):
        result = _project(
            runtime_ready=True,
            sensitivity="medium",
            avoid_topics=[],
            important_events=[],
        )
        assert result.boundary is not None
        assert result.boundary.sensitivity_summary == "medium"

    def test_avoid_topics_raises_sensitivity(self):
        avoid = [_make_topic(topic="politics", sensitivity="high")]
        result = _project(
            runtime_ready=True,
            sensitivity="low",
            avoid_topics=avoid,
        )
        assert result.boundary is not None
        assert result.boundary.sensitivity_summary == "high"

    def test_important_events_raises_sensitivity(self):
        events = [_make_event(event="Hospitalization", sensitivity="high")]
        result = _project(
            runtime_ready=True,
            sensitivity="low",
            important_events=events,
        )
        assert result.boundary is not None
        assert result.boundary.sensitivity_summary == "high"

    def test_max_of_all_areas(self):
        avoid = [_make_topic(topic="salary", sensitivity="medium")]
        events = [_make_event(event="Layoff", sensitivity="high")]
        result = _project(
            runtime_ready=True,
            sensitivity="low",
            avoid_topics=avoid,
            important_events=events,
        )
        assert result.boundary is not None
        assert result.boundary.sensitivity_summary == "high"

    def test_parent_floor_prevents_under_reporting(self):
        result = _project(
            runtime_ready=True,
            sensitivity="high",
            avoid_topics=[_make_topic(topic="minor_topic", sensitivity="low")],
            important_events=[_make_event(event="Minor event", sensitivity="low")],
        )
        assert result.boundary is not None
        assert result.boundary.sensitivity_summary == "high"


# ===================================================================
# Deterministic important_event_summaries formatting
# ===================================================================


class TestImportantEventSummariesFormatting:
    def test_with_date(self):
        events = [_make_event(event="Graduation ceremony", date="2024-06")]
        result = _project(runtime_ready=True, important_events=events)
        assert result.boundary is not None
        assert result.boundary.important_event_summaries == [
            "Graduation ceremony (2024-06)",
        ]

    def test_without_date(self):
        events = [_make_event(event="Career change", date=None)]
        result = _project(runtime_ready=True, important_events=events)
        assert result.boundary is not None
        assert result.boundary.important_event_summaries == ["Career change"]

    def test_mixed(self):
        events = [
            _make_event(event="Graduation", date="2024-06"),
            _make_event(event="Relocation", date=None),
            _make_event(event="Wedding", date="2025-03"),
        ]
        result = _project(runtime_ready=True, important_events=events)
        assert result.boundary is not None
        assert result.boundary.important_event_summaries == [
            "Graduation (2024-06)",
            "Relocation",
            "Wedding (2025-03)",
        ]

    def test_empty_events(self):
        result = _project(runtime_ready=True, important_events=[])
        assert result.boundary is not None
        assert result.boundary.important_event_summaries == []


# ===================================================================
# Policy-field mapping
# ===================================================================


class TestPolicyFieldMapping:
    def test_reply_strategy_fields(self):
        result = _project(
            runtime_ready=True,
            reply_strategy=ContactSkillReplyStrategy(
                default="Warm and supportive.",
                when_contact_is_cold="Gentle check-in.",
                when_contact_opens_topic="Stay on topic.",
                for_sensitive_topics="Listen, do not push.",
            ),
        )
        assert result.policy is not None
        assert result.policy.default_approach == "Warm and supportive."
        assert result.policy.cold_contact_approach == "Gentle check-in."
        assert result.policy.topic_opener_approach == "Stay on topic."
        assert result.policy.sensitive_topic_approach == "Listen, do not push."

    def test_user_side_preference_fields(self):
        result = _project(
            runtime_ready=True,
            user_side_preferences=ContactSkillUserSidePreferences(
                user_goal="Maintain friendship",
                preferred_reply_style="Casual and supportive",
            ),
        )
        assert result.policy is not None
        assert result.policy.user_goal == "Maintain friendship"
        assert result.policy.preferred_reply_style == "Casual and supportive"

    def test_stable_preference_hints(self):
        prefs = [
            _make_pattern(pattern="prefers morning texts"),
            _make_pattern(pattern="dislikes long voice notes"),
        ]
        result = _project(runtime_ready=True, stable_preferences=prefs)
        assert result.policy is not None
        assert result.policy.stable_preference_hints == [
            "prefers morning texts",
            "dislikes long voice notes",
        ]


# ===================================================================
# Boundary-field mapping
# ===================================================================


class TestBoundaryFieldMapping:
    def test_avoid_topics(self):
        avoid = [
            _make_topic(topic="politics"),
            _make_topic(topic="salary"),
        ]
        result = _project(runtime_ready=True, avoid_topics=avoid)
        assert result.boundary is not None
        assert result.boundary.avoid_topics == ["politics", "salary"]

    def test_boundary_rules(self):
        result = _project(
            runtime_ready=True,
            user_side_preferences=ContactSkillUserSidePreferences(
                boundaries=["Do not push for personal details", "Keep it light"],
            ),
        )
        assert result.boundary is not None
        assert result.boundary.boundary_rules == [
            "Do not push for personal details",
            "Keep it light",
        ]

    def test_disallowed_uses(self):
        result = _project(
            runtime_ready=True,
            usage_boundary=ContactSkillUsageBoundary(
                disallowed_uses=["persona_clone", "impersonation"],
            ),
        )
        assert result.boundary is not None
        assert result.boundary.disallowed_uses == ["persona_clone", "impersonation"]

    def test_usage_notes(self):
        result = _project(
            runtime_ready=True,
            usage_boundary=ContactSkillUsageBoundary(
                notes=["Handle family topics carefully"],
            ),
        )
        assert result.boundary is not None
        assert result.boundary.usage_notes == ["Handle family topics carefully"]


# ===================================================================
# Approved-patch-hints passthrough
# ===================================================================


class TestApprovedPatchHintsPassthrough:
    def test_empty_by_default(self):
        result = _project(runtime_ready=True)
        assert result.policy is not None
        assert result.policy.approved_patch_hints == []

    def test_patches_passed_through(self):
        patches = [
            ApprovedPatchBrief(
                patch_id="patch_001",
                patch_type="tone_preference",
                compact_instruction="Keep replies concise.",
                sensitivity="low",
            ),
        ]
        svc = ContactSkillProjectionService()
        record = _make_store_record(runtime_ready=True)
        result = svc.project_all(record=record, approved_patch_hints=patches)
        assert result.policy is not None
        assert len(result.policy.approved_patch_hints) == 1
        assert result.policy.approved_patch_hints[0].patch_id == "patch_001"

    def test_patches_only_in_policy_not_boundary(self):
        patches = [
            ApprovedPatchBrief(
                patch_id="patch_002",
                patch_type="length_preference",
                compact_instruction="Short replies.",
                sensitivity="low",
            ),
        ]
        svc = ContactSkillProjectionService()
        record = _make_store_record(runtime_ready=True)
        result = svc.project_all(record=record, approved_patch_hints=patches)
        assert result.policy is not None
        assert len(result.policy.approved_patch_hints) == 1
        assert not hasattr(result.boundary, "approved_patch_hints") or not isinstance(
            getattr(result.boundary, "approved_patch_hints", None), list,
        )


# ===================================================================
# Persona evidence-ref union
# ===================================================================


class TestPersonaEvidenceRefUnion:
    def test_union_from_all_sources(self):
        result = _project(
            runtime_ready=True,
            relationship_state=_make_relationship_state(evidence_refs=["evt_r1"]),
            communication_style=_make_communication_style(evidence_refs=["evt_c1"]),
            preferred_topics=[_make_topic(topic="hobbies", evidence_refs=["evt_t1"])],
            emotional_patterns=[_make_pattern(pattern="warm tone", evidence_refs=["evt_p1"])],
        )
        assert result.persona is not None
        refs = set(result.persona.evidence_refs)
        assert "evt_r1" in refs
        assert "evt_c1" in refs
        assert "evt_t1" in refs
        assert "evt_p1" in refs

    def test_deduped(self):
        result = _project(
            runtime_ready=True,
            relationship_state=_make_relationship_state(evidence_refs=["evt_shared"]),
            communication_style=_make_communication_style(evidence_refs=["evt_shared"]),
        )
        assert result.persona is not None
        assert result.persona.evidence_refs.count("evt_shared") == 1


# ===================================================================
# Boundary evidence-ref union
# ===================================================================


class TestBoundaryEvidenceRefUnion:
    def test_union_from_both_sources(self):
        result = _project(
            runtime_ready=True,
            avoid_topics=[_make_topic(topic="politics", evidence_refs=["evt_at1"])],
            important_events=[_make_event(event="Move", evidence_refs=["evt_ie1"])],
        )
        assert result.boundary is not None
        refs = set(result.boundary.evidence_refs)
        assert "evt_at1" in refs
        assert "evt_ie1" in refs

    def test_empty_when_no_sources(self):
        result = _project(
            runtime_ready=True,
            avoid_topics=[],
            important_events=[],
        )
        assert result.boundary is not None
        assert result.boundary.evidence_refs == []


# ===================================================================
# Projection is deterministic (same input → same output)
# ===================================================================


class TestDeterminism:
    def test_same_record_same_result(self):
        record = _make_store_record(
            runtime_ready=True,
            contact_id="contact_lin",
            record_id="skillstore_det_001",
            preferred_topics=[_make_topic(topic="music")],
            avoid_topics=[_make_topic(topic="salary")],
            important_events=[_make_event(event="Wedding", date="2025-03")],
            stable_preferences=[_make_pattern(pattern="Be brief.")],
            emotional_patterns=[_make_pattern(pattern="warm tone")],
        )
        svc = ContactSkillProjectionService()
        a = svc.project_all(record=record)
        b = svc.project_all(record=record)
        assert a.persona is not None and b.persona is not None
        assert a.persona.model_dump() == b.persona.model_dump()
        assert a.policy is not None and b.policy is not None
        assert a.policy.model_dump() == b.policy.model_dump()
        assert a.boundary is not None and b.boundary is not None
        assert a.boundary.model_dump() == b.boundary.model_dump()

    def test_projection_writes_nothing_to_disk(self, tmp_path):
        before = set(tmp_path.iterdir())
        svc = ContactSkillProjectionService()
        record = _make_store_record(runtime_ready=True)
        svc.project_all(record=record)
        after = set(tmp_path.iterdir())
        assert before == after
