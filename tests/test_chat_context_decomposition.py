"""Tests for T174: derived briefs context integration in ChatContextAssembler."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from practical_chat_agent.core.enums import (
    ChannelType,
    ChatIntent,
    ContentType,
    Direction,
    Platform,
    SourceType,
)
from practical_chat_agent.core.models import (
    ApprovedPatchBrief,
    ApprovedStoreContext,
    BoundaryProfileBrief,
    ChatContext,
    CommunicationPolicyBrief,
    ContactSkillCandidate,
    ContactSkillCommunicationStyle,
    ContactSkillImportantEvent,
    ContactSkillPattern,
    ContactSkillRelationshipState,
    ContactSkillReplyStrategy,
    ContactSkillStoreFile,
    ContactSkillStoreRecord,
    ContactSkillTopicPreference,
    ContactSkillUserSidePreferences,
    ContactSkillUsageBoundary,
    DerivedBriefContext,
    DistilledArtifactReviewMetadata,
    PartnerPersonaBrief,
    AgentProfile,
    InboundEvent,
)
from practical_chat_agent.services.chat_context import ChatContextAssembler


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_relationship_state(**overrides) -> ContactSkillRelationshipState:
    defaults = {
        "current_status": "low_frequency_but_continuing",
        "closeness": 0.45,
        "trust_level": 0.50,
        "interaction_frequency": "low",
        "initiative_balance": "user_leads_more",
        "confidence": 0.7,
        "evidence_refs": ["evt_rel_1"],
        "sensitivity": "low",
        "status": "approved",
    }
    defaults.update(overrides)
    return ContactSkillRelationshipState(**defaults)


def _make_communication_style(**overrides) -> ContactSkillCommunicationStyle:
    defaults = {
        "message_length": "short",
        "tone": "casual",
        "response_latency": "fast",
        "directness": "medium",
        "confidence": 0.7,
        "evidence_refs": ["evt_comm_1"],
        "sensitivity": "low",
        "status": "approved",
    }
    defaults.update(overrides)
    return ContactSkillCommunicationStyle(**defaults)


def _make_topic(topic: str = "hiking", sensitivity: str = "low") -> ContactSkillTopicPreference:
    return ContactSkillTopicPreference(
        topic=topic,
        claim=f"likes {topic}",
        evidence_refs=[f"evt_topic_{topic}"],
        confidence=0.7,
        sensitivity=sensitivity,
        status="approved",
    )


def _make_pattern(pattern: str = "warm greetings") -> ContactSkillPattern:
    return ContactSkillPattern(
        pattern=pattern,
        claim=f"shows {pattern}",
        evidence_refs=[f"evt_pat_{pattern[:4]}"],
        confidence=0.6,
        sensitivity="low",
        status="approved",
    )


def _make_event(
    event: str = "Birthday",
    date: str | None = "2024-06",
    sensitivity: str = "low",
) -> ContactSkillImportantEvent:
    return ContactSkillImportantEvent(
        event=event,
        date=date,
        claim=f"important: {event}",
        evidence_refs=[f"evt_ev_{event[:3]}"],
        confidence=0.8,
        sensitivity=sensitivity,
        status="approved",
    )


def _make_approved_review_metadata() -> DistilledArtifactReviewMetadata:
    return DistilledArtifactReviewMetadata(
        review_state="reviewed",
        reviewed_by_human=True,
        last_decision="approved",
        last_reviewed_at="2026-01-01T00:00:00+00:00",
        evidence_validation_status="passed",
    )


def _make_runtime_ready_skill_record(
    contact_id: str = "contact_test",
    **skill_overrides,
) -> ContactSkillStoreRecord:
    skill_defaults: dict = {
        "contact_id": contact_id,
        "relationship_type": "friend",
        "status": "approved",
        "confidence": 0.7,
        "sensitivity": "low",
        "evidence_refs": ["evt_skill_1", "evt_skill_2"],
        "relationship_state": _make_relationship_state(),
        "communication_style": _make_communication_style(),
        "preferred_topics": [_make_topic("hiking"), _make_topic("music")],
        "avoid_topics": [_make_topic("politics", sensitivity="medium")],
        "important_events": [_make_event("Birthday", "2024-06")],
        "stable_preferences": [_make_pattern("prefers short replies")],
        "emotional_patterns": [_make_pattern("warm greetings")],
        "reply_strategy": ContactSkillReplyStrategy(
            default="keep warm but low pressure",
            when_contact_is_cold="give space",
        ),
        "user_side_preferences": ContactSkillUserSidePreferences(
            user_goal="maintain friendship",
            boundaries=["do not discuss finances"],
            preferred_reply_style="casual",
        ),
        "usage_boundary": ContactSkillUsageBoundary(),
    }
    skill_defaults.update(skill_overrides)
    skill = ContactSkillCandidate(**skill_defaults)
    return ContactSkillStoreRecord(
        record_id="skillstore_test001",
        contact_skill=skill,
        review_metadata=_make_approved_review_metadata(),
    )


def _write_store_files(
    tmp_path: Path,
    skill_record: ContactSkillStoreRecord | None = None,
    contact_id: str = "contact_test",
) -> Path:
    store_dir = tmp_path / "store"
    store_dir.mkdir()
    if skill_record is None:
        skill_record = _make_runtime_ready_skill_record(contact_id=contact_id)
    skill_store = ContactSkillStoreFile(records=[skill_record])
    (store_dir / "contact_skill_store.json").write_text(
        skill_store.model_dump_json(indent=2),
        encoding="utf-8",
    )
    report = {
        "records": [
            {
                "record_id": skill_record.record_id,
                "checked_ref_count": 2,
                "missing_ref_count": 0,
            },
        ],
    }
    (store_dir / "evidence_validation_report.json").write_text(
        json.dumps(report),
        encoding="utf-8",
    )
    return store_dir


def _write_patch_report(
    tmp_path: Path,
    contact_id: str = "contact_test",
) -> Path:
    patch_dir = tmp_path / "patches"
    patch_dir.mkdir()
    patch_report = {
        "schema_version": "patch_proposal_v1",
        "candidates": [
            {
                "patch": {
                    "schema_version": "preference_patch_candidate_v1",
                    "patch_id": "patch_001",
                    "contact_id": contact_id,
                    "patch_type": "tone_preference",
                    "instruction_scope": "per_contact",
                    "claim": "Contact prefers concise replies",
                    "behavior_instruction": "Keep replies short and direct",
                    "supporting_feedback_ids": ["fb_001", "fb_002"],
                    "status": "approved",
                    "confidence": 0.8,
                    "sensitivity": "low",
                    "review_metadata": {
                        "review_state": "reviewed",
                        "reviewed_by_human": True,
                        "last_decision": "approved",
                        "evidence_validation_status": "not_run",
                    },
                },
            },
        ],
    }
    patch_file = patch_dir / "patch_report.json"
    patch_file.write_text(json.dumps(patch_report), encoding="utf-8")
    return patch_file


def _make_agent() -> AgentProfile:
    return AgentProfile(agent_id="agent_test", display_name="TestAgent")


def _make_inbound_event(contact_id: str = "contact_test") -> InboundEvent:
    return InboundEvent(
        event_id="evt_test_1",
        source_type=SourceType.CHAT_MESSAGE,
        platform=Platform.WECHAT,
        channel_id="ch_test",
        channel_type=ChannelType.DM,
        account_id="acct_test",
        actor_id=contact_id,
        actor_name="Test Contact",
        direction=Direction.INBOUND,
        content_type=ContentType.TEXT,
        text="hello there",
    )


def _assemble(
    store_path: Path | None = None,
    patch_path: Path | None = None,
    contact_id: str = "contact_test",
    distilled_root: Path | None = None,
) -> ChatContext:
    assembler = ChatContextAssembler(
        approved_store_path=store_path,
        approved_patch_path=patch_path,
    )
    # For testing: override the private/distilled confinement root so that
    # temp directories pass the _ensure_within_private_distilled check.
    if distilled_root is not None:
        assembler._private_distilled_root = distilled_root.resolve()
    return assembler.assemble(
        agent=_make_agent(),
        event=_make_inbound_event(contact_id=contact_id),
        recent_events=[],
        memory_hits=[],
        intent=ChatIntent.GENERAL,
    )


# ---------------------------------------------------------------------------
# Test: derived-brief context load success
# ---------------------------------------------------------------------------

class TestDerivedBriefLoadSuccess:
    """When an eligible skill record exists, derived briefs are loaded."""

    def test_status_loaded(self, tmp_path: Path):
        store_dir = _write_store_files(tmp_path)
        ctx = _assemble(store_path=store_dir, distilled_root=tmp_path)
        assert ctx.derived_brief_context.status == "loaded"

    def test_persona_brief_populated(self, tmp_path: Path):
        store_dir = _write_store_files(tmp_path)
        ctx = _assemble(store_path=store_dir, distilled_root=tmp_path)
        persona = ctx.derived_brief_context.persona
        assert persona is not None
        assert persona.contact_id == "contact_test"
        assert persona.relationship_type == "friend"

    def test_policy_brief_populated(self, tmp_path: Path):
        store_dir = _write_store_files(tmp_path)
        ctx = _assemble(store_path=store_dir, distilled_root=tmp_path)
        policy = ctx.derived_brief_context.policy
        assert policy is not None
        assert policy.default_approach == "keep warm but low pressure"
        assert policy.cold_contact_approach == "give space"

    def test_boundary_brief_populated(self, tmp_path: Path):
        store_dir = _write_store_files(tmp_path)
        ctx = _assemble(store_path=store_dir, distilled_root=tmp_path)
        boundary = ctx.derived_brief_context.boundary
        assert boundary is not None
        assert "politics" in boundary.avoid_topics
        assert "do not discuss finances" in boundary.boundary_rules

    def test_source_skill_record_id(self, tmp_path: Path):
        store_dir = _write_store_files(tmp_path)
        ctx = _assemble(store_path=store_dir, distilled_root=tmp_path)
        assert ctx.derived_brief_context.source_skill_record_id == "skillstore_test001"


# ---------------------------------------------------------------------------
# Test: fallback when projection is unavailable
# ---------------------------------------------------------------------------

class TestDerivedBriefFallbackNotConfigured:
    """No store path configured → derived briefs stay not_configured."""

    def test_status_not_configured(self):
        ctx = _assemble(store_path=None)
        assert ctx.derived_brief_context.status == "not_configured"

    def test_all_briefs_none(self):
        ctx = _assemble(store_path=None)
        assert ctx.derived_brief_context.persona is None
        assert ctx.derived_brief_context.policy is None
        assert ctx.derived_brief_context.boundary is None

    def test_approved_store_context_also_not_configured(self):
        ctx = _assemble(store_path=None)
        assert ctx.approved_store_context.status == "not_configured"


class TestDerivedBriefFallbackNoRuntimeReady:
    """Store exists but no runtime-ready records → no derived briefs."""

    def _make_candidate_store(self, tmp_path: Path) -> Path:
        record = _make_runtime_ready_skill_record()
        candidate_skill = record.contact_skill.model_copy(update={"status": "candidate"})
        candidate_record = record.model_copy(update={
            "contact_skill": candidate_skill,
            "review_metadata": DistilledArtifactReviewMetadata(reviewed_by_human=False),
        })
        return _write_store_files(tmp_path, skill_record=candidate_record)

    def test_status_not_configured(self, tmp_path: Path):
        store_dir = self._make_candidate_store(tmp_path)
        ctx = _assemble(store_path=store_dir, distilled_root=tmp_path)
        # No eligible record → derived brief context stays not_configured
        assert ctx.derived_brief_context.status == "not_configured"

    def test_all_briefs_none(self, tmp_path: Path):
        store_dir = self._make_candidate_store(tmp_path)
        ctx = _assemble(store_path=store_dir, distilled_root=tmp_path)
        assert ctx.derived_brief_context.persona is None
        assert ctx.derived_brief_context.policy is None
        assert ctx.derived_brief_context.boundary is None

    def test_approved_store_also_no_records(self, tmp_path: Path):
        store_dir = self._make_candidate_store(tmp_path)
        ctx = _assemble(store_path=store_dir, distilled_root=tmp_path)
        assert ctx.approved_store_context.status == "no_runtime_ready_records"


class TestDerivedBriefFallbackContactMismatch:
    """Runtime-ready record exists but for a different contact_id."""

    def test_status_no_runtime_ready_records(self, tmp_path: Path):
        store_dir = _write_store_files(tmp_path, contact_id="contact_other")
        ctx = _assemble(store_path=store_dir, contact_id="contact_test", distilled_root=tmp_path)
        assert ctx.derived_brief_context.status == "not_configured"

    def test_approved_store_also_no_match(self, tmp_path: Path):
        store_dir = _write_store_files(tmp_path, contact_id="contact_other")
        ctx = _assemble(store_path=store_dir, contact_id="contact_test", distilled_root=tmp_path)
        assert ctx.approved_store_context.contact_skill is None


# ---------------------------------------------------------------------------
# Test: partial derived-brief behavior (no patches, store-only)
# ---------------------------------------------------------------------------

class TestDerivedBriefWithoutPatches:
    """Derived briefs loaded but approved-patch context not configured."""

    def test_derived_briefs_loaded_without_patches(self, tmp_path: Path):
        store_dir = _write_store_files(tmp_path)
        ctx = _assemble(store_path=store_dir, distilled_root=tmp_path)
        assert ctx.derived_brief_context.status == "loaded"
        assert ctx.approved_patch_context.status == "not_configured"

    def test_policy_has_empty_patch_hints(self, tmp_path: Path):
        store_dir = _write_store_files(tmp_path)
        ctx = _assemble(store_path=store_dir, distilled_root=tmp_path)
        policy = ctx.derived_brief_context.policy
        assert policy is not None
        assert policy.approved_patch_hints == []

    def test_personality_and_boundary_still_populated(self, tmp_path: Path):
        store_dir = _write_store_files(tmp_path)
        ctx = _assemble(store_path=store_dir, distilled_root=tmp_path)
        assert ctx.derived_brief_context.persona is not None
        assert ctx.derived_brief_context.boundary is not None


# ---------------------------------------------------------------------------
# Test: coexistence with approved-patch compact context path
# ---------------------------------------------------------------------------

class TestDerivedBriefPatchCoexistence:
    """Derived briefs and approved-patch context coexist independently."""

    def test_both_contexts_loaded(self, tmp_path: Path):
        store_dir = _write_store_files(tmp_path)
        patch_file = _write_patch_report(tmp_path)
        ctx = _assemble(store_path=store_dir, patch_path=patch_file, distilled_root=tmp_path)
        assert ctx.derived_brief_context.status == "loaded"
        assert ctx.approved_patch_context.status == "loaded"
        assert ctx.approved_store_context.status == "loaded"

    def test_policy_brief_receives_patch_hints(self, tmp_path: Path):
        store_dir = _write_store_files(tmp_path)
        patch_file = _write_patch_report(tmp_path)
        ctx = _assemble(store_path=store_dir, patch_path=patch_file, distilled_root=tmp_path)
        policy = ctx.derived_brief_context.policy
        assert policy is not None
        assert len(policy.approved_patch_hints) == 1
        assert policy.approved_patch_hints[0].patch_id == "patch_001"

    def test_patch_context_patches_same_count(self, tmp_path: Path):
        store_dir = _write_store_files(tmp_path)
        patch_file = _write_patch_report(tmp_path)
        ctx = _assemble(store_path=store_dir, patch_path=patch_file, distilled_root=tmp_path)
        patch_brief = ctx.approved_patch_context.patches[0]
        policy_hint = ctx.derived_brief_context.policy.approved_patch_hints[0]
        assert patch_brief.patch_id == policy_hint.patch_id

    def test_approved_store_brief_still_loaded(self, tmp_path: Path):
        store_dir = _write_store_files(tmp_path)
        patch_file = _write_patch_report(tmp_path)
        ctx = _assemble(store_path=store_dir, patch_path=patch_file, distilled_root=tmp_path)
        assert ctx.approved_store_context.contact_skill is not None
        assert ctx.approved_store_context.contact_skill.record_id == "skillstore_test001"

    def test_patch_context_independent_of_derived_briefs(self, tmp_path: Path):
        """Patches load even when derived briefs are not available."""
        patch_file = _write_patch_report(tmp_path)
        ctx = _assemble(store_path=None, patch_path=patch_file, distilled_root=tmp_path)
        assert ctx.approved_patch_context.status == "loaded"
        assert ctx.derived_brief_context.status == "not_configured"


# ---------------------------------------------------------------------------
# Test: preservation of projection outputs without assembler rewriting
# ---------------------------------------------------------------------------

class TestDerivedBriefPreservesProjectionOutputs:
    """Assembler preserves projected values as-is without reformatting."""

    def test_relationship_state_summary_preserved(self, tmp_path: Path):
        store_dir = _write_store_files(tmp_path)
        ctx = _assemble(store_path=store_dir, distilled_root=tmp_path)
        persona = ctx.derived_brief_context.persona
        assert persona is not None
        assert "low_frequency_but_continuing" in persona.relationship_state_summary
        assert "closeness=" in persona.relationship_state_summary
        assert "trust=" in persona.relationship_state_summary

    def test_important_event_summaries_format_preserved(self, tmp_path: Path):
        store_dir = _write_store_files(tmp_path)
        ctx = _assemble(store_path=store_dir, distilled_root=tmp_path)
        boundary = ctx.derived_brief_context.boundary
        assert boundary is not None
        assert any(
            "Birthday" in s and "2024-06" in s
            for s in boundary.important_event_summaries
        )

    def test_sensitivity_summary_explicitly_computed(self, tmp_path: Path):
        """sensitivity_summary is the projected value, not the schema default."""
        store_dir = _write_store_files(tmp_path)
        ctx = _assemble(store_path=store_dir, distilled_root=tmp_path)
        boundary = ctx.derived_brief_context.boundary
        assert boundary is not None
        # avoid_topics has "politics" with sensitivity="medium", parent is "low"
        # So sensitivity_summary must be "medium" (max), not schema default "low"
        assert boundary.sensitivity_summary == "medium"

    def test_communication_style_unknown_to_none(self, tmp_path: Path):
        record = _make_runtime_ready_skill_record()
        unknown_style = _make_communication_style(
            message_length="unknown",
            tone="unknown",
            response_latency="unknown",
            directness="unknown",
        )
        updated_record = record.model_copy(update={
            "contact_skill": record.contact_skill.model_copy(update={
                "communication_style": unknown_style,
            }),
        })
        store_dir = _write_store_files(tmp_path, skill_record=updated_record)
        ctx = _assemble(store_path=store_dir, distilled_root=tmp_path)
        persona = ctx.derived_brief_context.persona
        assert persona is not None
        assert persona.communication_style_snapshot.message_length is None
        assert persona.communication_style_snapshot.tone is None
        assert persona.communication_style_snapshot.response_latency is None
        assert persona.communication_style_snapshot.directness is None

    def test_thin_policy_evidence_preserved(self, tmp_path: Path):
        """evidence_refs only from stable_preferences, not backfilled."""
        store_dir = _write_store_files(tmp_path)
        ctx = _assemble(store_path=store_dir, distilled_root=tmp_path)
        policy = ctx.derived_brief_context.policy
        assert policy is not None
        # All evidence refs should come from stable_preferences patterns
        assert len(policy.evidence_refs) > 0
        for ref in policy.evidence_refs:
            assert "pat_" in ref


# ---------------------------------------------------------------------------
# Test: derived brief notes in retrieval notes
# ---------------------------------------------------------------------------

class TestDerivedBriefNotesInRetrieval:
    """Derived brief notes appear in memory_retrieval_notes when loaded."""

    def test_notes_present_when_loaded(self, tmp_path: Path):
        store_dir = _write_store_files(tmp_path)
        ctx = _assemble(store_path=store_dir, distilled_root=tmp_path)
        assert any("derived_brief_context" in n for n in ctx.memory_retrieval_notes)

    def test_notes_absent_when_not_configured(self):
        ctx = _assemble(store_path=None)
        assert not any("derived_brief_context" in n for n in ctx.memory_retrieval_notes)

    def test_persona_summary_in_notes(self, tmp_path: Path):
        store_dir = _write_store_files(tmp_path)
        ctx = _assemble(store_path=store_dir, distilled_root=tmp_path)
        assert any("derived_persona_summary" in n for n in ctx.memory_retrieval_notes)

    def test_boundary_sensitivity_in_notes(self, tmp_path: Path):
        store_dir = _write_store_files(tmp_path)
        ctx = _assemble(store_path=store_dir, distilled_root=tmp_path)
        assert any("derived_boundary_sensitivity" in n for n in ctx.memory_retrieval_notes)


# ---------------------------------------------------------------------------
# Test: summary includes derived brief info
# ---------------------------------------------------------------------------

class TestDerivedBriefSummaryInclusion:
    """Context summary includes derived brief info when loaded."""

    def test_summary_includes_derived_persona(self, tmp_path: Path):
        store_dir = _write_store_files(tmp_path)
        ctx = _assemble(store_path=store_dir, distilled_root=tmp_path)
        assert ctx.summary is not None
        assert "Derived persona brief" in ctx.summary

    def test_summary_includes_boundary_sensitivity(self, tmp_path: Path):
        store_dir = _write_store_files(tmp_path)
        ctx = _assemble(store_path=store_dir, distilled_root=tmp_path)
        assert ctx.summary is not None
        assert "Derived boundary sensitivity" in ctx.summary

    def test_summary_excludes_derived_when_not_loaded(self):
        ctx = _assemble(store_path=None)
        if ctx.summary:
            assert "Derived persona brief" not in ctx.summary
            assert "Derived boundary sensitivity" not in ctx.summary


# ---------------------------------------------------------------------------
# Test: ApprovedContactSkillBrief fallback coexistence
# ---------------------------------------------------------------------------

class TestApprovedBriefFallbackCoexistence:
    """ApprovedContactSkillBrief remains loaded alongside derived briefs."""

    def test_approved_brief_still_present(self, tmp_path: Path):
        store_dir = _write_store_files(tmp_path)
        ctx = _assemble(store_path=store_dir, distilled_root=tmp_path)
        assert ctx.approved_store_context.status == "loaded"
        assert ctx.approved_store_context.contact_skill is not None
        assert ctx.approved_store_context.contact_skill.record_id == "skillstore_test001"

    def test_both_summaries_exist(self, tmp_path: Path):
        store_dir = _write_store_files(tmp_path)
        ctx = _assemble(store_path=store_dir, distilled_root=tmp_path)
        flat_brief = ctx.approved_store_context.contact_skill
        derived_persona = ctx.derived_brief_context.persona
        assert flat_brief is not None
        assert derived_persona is not None
        assert flat_brief.relationship_summary
        assert derived_persona.relationship_state_summary

    def test_approved_brief_notes_still_present(self, tmp_path: Path):
        store_dir = _write_store_files(tmp_path)
        ctx = _assemble(store_path=store_dir, distilled_root=tmp_path)
        assert any("approved_store_context" in n for n in ctx.memory_retrieval_notes)

    def test_approved_brief_strategy_hints_preserved(self, tmp_path: Path):
        store_dir = _write_store_files(tmp_path)
        ctx = _assemble(store_path=store_dir, distilled_root=tmp_path)
        brief = ctx.approved_store_context.contact_skill
        assert brief is not None
        assert len(brief.strategy_hints) > 0
        assert any("warm" in h for h in brief.strategy_hints)


# ---------------------------------------------------------------------------
# Test: determinism and no disk writes
# ---------------------------------------------------------------------------

class TestDerivedBriefDeterminism:
    """Same input produces same derived briefs; no disk writes."""

    def test_same_result_twice(self, tmp_path: Path):
        store_dir = _write_store_files(tmp_path)
        ctx1 = _assemble(store_path=store_dir, distilled_root=tmp_path)
        ctx2 = _assemble(store_path=store_dir, distilled_root=tmp_path)
        p1 = ctx1.derived_brief_context.persona
        p2 = ctx2.derived_brief_context.persona
        assert p1 is not None and p2 is not None
        assert p1.relationship_state_summary == p2.relationship_state_summary
        assert p1.communication_style_snapshot == p2.communication_style_snapshot

    def test_no_disk_writes(self, tmp_path: Path):
        store_dir = _write_store_files(tmp_path)
        files_before = set(store_dir.rglob("*"))
        contents_before = {
            f: f.read_text(encoding="utf-8") for f in files_before if f.is_file()
        }
        _assemble(store_path=store_dir, distilled_root=tmp_path)
        files_after = set(store_dir.rglob("*"))
        contents_after = {
            f: f.read_text(encoding="utf-8") for f in files_after if f.is_file()
        }
        assert contents_before == contents_after
