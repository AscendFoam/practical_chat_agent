"""Tests for T194: RelationshipState compact context in ChatContextAssembler."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from practical_chat_agent.core.enums import (
    ChannelType,
    ChatIntent,
    ContentType,
    Direction,
    Platform,
    SourceType,
)
from practical_chat_agent.core.models import (
    AgentProfile,
    ApprovedRelationshipContext,
    ChatContext,
    DistilledArtifactReviewMetadata,
    InboundEvent,
    RelationshipDeltaCandidate,
    RelationshipDeltaDimension,
)
from practical_chat_agent.services.chat_context import ChatContextAssembler


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_approved_delta(
    *,
    delta_id: str = "delta_test_001",
    contact_id: str = "contact_test",
    dim_name: str = "boundary_risk",
    current_value: float = 0.3,
    proposed_value: float = 0.44,
    direction: str = "increase",
    magnitude: float = 0.14,
    rationale: str = "Proposed based on signal evidence.",
    evidence_refs: list[str] | None = None,
) -> RelationshipDeltaCandidate:
    now = datetime.now(timezone.utc)
    dc = RelationshipDeltaDimension(
        dimension_name=dim_name,
        current_value=current_value,
        proposed_value=proposed_value,
        direction=direction,
        magnitude=magnitude,
        rationale=f"{dim_name} change rationale",
    )
    return RelationshipDeltaCandidate(
        delta_id=delta_id,
        contact_id=contact_id,
        source_state_id="state_test_001",
        dimension_changes=[dc],
        delta_rationale=rationale,
        evidence_refs=evidence_refs or ["evt_001", "evt_002"],
        signal_refs=["sig_001"],
        status="approved",
        review_metadata=DistilledArtifactReviewMetadata(
            review_state="reviewed",
            reviewed_by_human=True,
            last_decision="approved",
        ),
        created_at=now,
        updated_at=now,
    )


def _make_candidate_delta(
    *,
    contact_id: str = "contact_test",
) -> RelationshipDeltaCandidate:
    now = datetime.now(timezone.utc)
    dc = RelationshipDeltaDimension(
        dimension_name="warmth",
        current_value=0.5,
        proposed_value=0.6,
        direction="increase",
        magnitude=0.10,
    )
    return RelationshipDeltaCandidate(
        delta_id="delta_candidate",
        contact_id=contact_id,
        source_state_id="state_test_001",
        dimension_changes=[dc],
        delta_rationale="Unreviewed proposal.",
        evidence_refs=["evt_003"],
        signal_refs=["sig_002"],
        status="candidate",
        created_at=now,
        updated_at=now,
    )


def _write_delta_json(
    delta_dir: Path,
    delta: RelationshipDeltaCandidate,
    filename: str | None = None,
) -> Path:
    """Write a RelationshipDeltaCandidate to a JSON file and return the path."""
    delta_dir.mkdir(parents=True, exist_ok=True)
    name = filename or f"delta_{delta.delta_id}.json"
    path = delta_dir / name
    path.write_text(
        delta.model_dump_json(indent=2),
        encoding="utf-8",
    )
    return path


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
    relationship_delta_path: Path | None = None,
    contact_id: str = "contact_test",
    distilled_root: Path | None = None,
) -> ChatContext:
    assembler = ChatContextAssembler(
        approved_relationship_delta_path=relationship_delta_path,
    )
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
# Test: approved relationship context load success
# ---------------------------------------------------------------------------


class TestRelationshipContextLoadSuccess:
    """Runtime-ready deltas produce loaded relationship context."""

    def test_status_loaded(self, tmp_path: Path):
        delta = _make_approved_delta()
        _write_delta_json(tmp_path, delta)
        ctx = _assemble(relationship_delta_path=tmp_path, distilled_root=tmp_path)
        assert ctx.relationship_context.status == "loaded"

    def test_dimension_changes_populated(self, tmp_path: Path):
        delta = _make_approved_delta()
        _write_delta_json(tmp_path, delta)
        ctx = _assemble(relationship_delta_path=tmp_path, distilled_root=tmp_path)
        assert len(ctx.relationship_context.deltas) == 1
        brief = ctx.relationship_context.deltas[0]
        assert len(brief.dimension_changes) == 1
        assert "boundary_risk" in brief.dimension_changes[0]
        assert "0.30" in brief.dimension_changes[0]
        assert "0.44" in brief.dimension_changes[0]

    def test_delta_summary_preserved(self, tmp_path: Path):
        delta = _make_approved_delta(rationale="Approved after review.")
        _write_delta_json(tmp_path, delta)
        ctx = _assemble(relationship_delta_path=tmp_path, distilled_root=tmp_path)
        brief = ctx.relationship_context.deltas[0]
        assert "Approved after review." in brief.delta_summary

    def test_evidence_refs_preserved(self, tmp_path: Path):
        delta = _make_approved_delta(evidence_refs=["fb_001", "fb_002", "fb_003"])
        _write_delta_json(tmp_path, delta)
        ctx = _assemble(relationship_delta_path=tmp_path, distilled_root=tmp_path)
        brief = ctx.relationship_context.deltas[0]
        assert "fb_001" in brief.evidence_refs
        assert "fb_002" in brief.evidence_refs

    def test_delta_id_preserved(self, tmp_path: Path):
        delta = _make_approved_delta(delta_id="delta_custom_001")
        _write_delta_json(tmp_path, delta)
        ctx = _assemble(relationship_delta_path=tmp_path, distilled_root=tmp_path)
        assert ctx.relationship_context.deltas[0].delta_id == "delta_custom_001"

    def test_contact_id_preserved(self, tmp_path: Path):
        delta = _make_approved_delta(contact_id="contact_lin")
        _write_delta_json(tmp_path, delta)
        ctx = _assemble(
            relationship_delta_path=tmp_path,
            contact_id="contact_lin",
            distilled_root=tmp_path,
        )
        assert ctx.relationship_context.deltas[0].contact_id == "contact_lin"

    def test_multi_dimension_delta(self, tmp_path: Path):
        dc1 = RelationshipDeltaDimension(
            dimension_name="boundary_risk",
            current_value=0.3,
            proposed_value=0.44,
            direction="increase",
            magnitude=0.14,
        )
        dc2 = RelationshipDeltaDimension(
            dimension_name="intimacy_level",
            current_value=0.6,
            proposed_value=0.4,
            direction="decrease",
            magnitude=0.20,
        )
        now = datetime.now(timezone.utc)
        delta = RelationshipDeltaCandidate(
            delta_id="delta_multi",
            contact_id="contact_test",
            source_state_id="state_test_001",
            dimension_changes=[dc1, dc2],
            delta_rationale="Multi-dimension update.",
            evidence_refs=["evt_001"],
            signal_refs=["sig_001"],
            status="approved",
            review_metadata=DistilledArtifactReviewMetadata(
                review_state="reviewed",
                reviewed_by_human=True,
                last_decision="approved",
            ),
            created_at=now,
            updated_at=now,
        )
        _write_delta_json(tmp_path, delta)
        ctx = _assemble(relationship_delta_path=tmp_path, distilled_root=tmp_path)
        assert len(ctx.relationship_context.deltas) == 1
        brief = ctx.relationship_context.deltas[0]
        assert len(brief.dimension_changes) == 2
        assert any("boundary_risk" in d for d in brief.dimension_changes)
        assert any("intimacy_level" in d for d in brief.dimension_changes)


# ---------------------------------------------------------------------------
# Test: fallback when no approved relationship data is available
# ---------------------------------------------------------------------------


class TestRelationshipContextFallbackNotConfigured:
    """No delta path configured -> relationship context stays not_configured."""

    def test_status_not_configured(self):
        ctx = _assemble(relationship_delta_path=None)
        assert ctx.relationship_context.status == "not_configured"

    def test_deltas_empty(self):
        ctx = _assemble(relationship_delta_path=None)
        assert ctx.relationship_context.deltas == []

    def test_approved_store_context_also_ok(self):
        ctx = _assemble(relationship_delta_path=None)
        # Existing approved_store_context is not affected
        assert ctx.approved_store_context.status == "not_configured"


class TestRelationshipContextFallbackPathMissing:
    """Configured path does not exist -> status store_path_missing."""

    def test_status_store_path_missing(self, tmp_path: Path):
        missing = tmp_path / "does_not_exist"
        ctx = _assemble(relationship_delta_path=missing, distilled_root=tmp_path)
        assert ctx.relationship_context.status == "store_path_missing"


class TestRelationshipContextFallbackNoRuntimeReady:
    """Deltas exist but none are runtime-ready -> no_runtime_ready_records."""

    def test_candidate_delta_not_loaded(self, tmp_path: Path):
        delta = _make_candidate_delta()
        _write_delta_json(tmp_path, delta)
        ctx = _assemble(relationship_delta_path=tmp_path, distilled_root=tmp_path)
        assert ctx.relationship_context.status == "no_runtime_ready_records"
        assert ctx.relationship_context.deltas == []

    def test_empty_directory(self, tmp_path: Path):
        ctx = _assemble(relationship_delta_path=tmp_path, distilled_root=tmp_path)
        assert ctx.relationship_context.status == "no_runtime_ready_records"
        assert ctx.relationship_context.deltas == []

    def test_mixed_candidate_and_approved_filtered(self, tmp_path: Path):
        approved = _make_approved_delta(contact_id="contact_other")
        candidate = _make_candidate_delta(contact_id="contact_test")
        _write_delta_json(tmp_path, approved, filename="delta_approved_other.json")
        _write_delta_json(tmp_path, candidate, filename="delta_candidate.json")
        ctx = _assemble(
            relationship_delta_path=tmp_path,
            contact_id="contact_test",
            distilled_root=tmp_path,
        )
        # Only candidate matches contact_id, but it's not runtime-ready
        assert ctx.relationship_context.status == "no_runtime_ready_records"
        assert ctx.relationship_context.deltas == []

    def test_approved_other_contact_not_loaded(self, tmp_path: Path):
        """Approved delta for a different contact_id is excluded."""
        delta = _make_approved_delta(contact_id="contact_other")
        _write_delta_json(tmp_path, delta)
        ctx = _assemble(
            relationship_delta_path=tmp_path,
            contact_id="contact_test",
            distilled_root=tmp_path,
        )
        assert ctx.relationship_context.status == "no_runtime_ready_records"
        assert ctx.relationship_context.deltas == []

    def test_approved_not_human_reviewed(self, tmp_path: Path):
        """Approved but not human-reviewed delta is excluded."""
        now = datetime.now(timezone.utc)
        dc = RelationshipDeltaDimension(
            dimension_name="trust",
            current_value=0.5,
            proposed_value=0.6,
            direction="increase",
            magnitude=0.10,
        )
        delta = RelationshipDeltaCandidate(
            delta_id="delta_no_human",
            contact_id="contact_test",
            source_state_id="state_test_001",
            dimension_changes=[dc],
            delta_rationale="No human review yet.",
            evidence_refs=["evt_003"],
            signal_refs=["sig_002"],
            status="approved",
            review_metadata=DistilledArtifactReviewMetadata(
                review_state="pending_human_review",
                reviewed_by_human=False,
                last_decision=None,
            ),
            created_at=now,
            updated_at=now,
        )
        _write_delta_json(tmp_path, delta)
        ctx = _assemble(
            relationship_delta_path=tmp_path,
            contact_id="contact_test",
            distilled_root=tmp_path,
        )
        assert ctx.relationship_context.status == "no_runtime_ready_records"


# ---------------------------------------------------------------------------
# Test: no raw signal / review history leakage
# ---------------------------------------------------------------------------


class TestRelationshipContextNoRawLeakage:
    """Raw signal history and raw review history do not appear in context."""

    def test_no_signal_refs_in_brief(self, tmp_path: Path):
        delta = _make_approved_delta()
        _write_delta_json(tmp_path, delta)
        ctx = _assemble(relationship_delta_path=tmp_path, distilled_root=tmp_path)
        brief = ctx.relationship_context.deltas[0]
        for field_name in ("signal_refs", "review_metadata"):
            assert not hasattr(brief, field_name)

    def test_no_review_history_in_context(self, tmp_path: Path):
        delta = _make_approved_delta()
        _write_delta_json(tmp_path, delta)
        ctx = _assemble(relationship_delta_path=tmp_path, distilled_root=tmp_path)
        # The context model itself should not carry review_metadata
        assert not hasattr(ctx.relationship_context, "review_metadata")

    def test_no_raw_rationale_overflow(self, tmp_path: Path):
        long_rationale = "x" * 1000
        delta = _make_approved_delta(rationale=long_rationale)
        _write_delta_json(tmp_path, delta)
        ctx = _assemble(relationship_delta_path=tmp_path, distilled_root=tmp_path)
        brief = ctx.relationship_context.deltas[0]
        # delta_summary is capped at 200 characters
        assert len(brief.delta_summary) <= 200

    def test_evidence_refs_limited(self, tmp_path: Path):
        many_refs = [f"evt_{i:04d}" for i in range(20)]
        delta = _make_approved_delta(evidence_refs=many_refs)
        _write_delta_json(tmp_path, delta)
        ctx = _assemble(relationship_delta_path=tmp_path, distilled_root=tmp_path)
        brief = ctx.relationship_context.deltas[0]
        assert len(brief.evidence_refs) <= 6


# ---------------------------------------------------------------------------
# Test: coexistence with existing context paths
# ---------------------------------------------------------------------------


class TestRelationshipContextCoexistence:
    """Relationship context coexists with approved-store, patch, and
    derived-brief contexts."""

    def test_coexists_with_approved_store(self, tmp_path: Path):
        delta = _make_approved_delta()
        _write_delta_json(tmp_path, delta)
        ctx = _assemble(relationship_delta_path=tmp_path, distilled_root=tmp_path)
        assert ctx.relationship_context.status == "loaded"
        assert ctx.approved_store_context.status == "not_configured"
        assert ctx.approved_patch_context.status == "not_configured"
        assert ctx.derived_brief_context.status == "not_configured"

    def test_relationship_loaded_others_not_configured(self, tmp_path: Path):
        delta = _make_approved_delta()
        _write_delta_json(tmp_path, delta)
        ctx = _assemble(relationship_delta_path=tmp_path, distilled_root=tmp_path)
        assert ctx.relationship_context.status == "loaded"
        assert ctx.approved_store_context.status == "not_configured"
        assert ctx.approved_patch_context.status == "not_configured"


# ---------------------------------------------------------------------------
# Test: relationship context notes in retrieval notes
# ---------------------------------------------------------------------------


class TestRelationshipContextNotesInRetrieval:
    """Relationship context notes appear in memory_retrieval_notes when loaded."""

    def test_notes_present_when_loaded(self, tmp_path: Path):
        delta = _make_approved_delta()
        _write_delta_json(tmp_path, delta)
        ctx = _assemble(relationship_delta_path=tmp_path, distilled_root=tmp_path)
        assert any("relationship_context" in n for n in ctx.memory_retrieval_notes)

    def test_notes_absent_when_not_configured(self):
        ctx = _assemble(relationship_delta_path=None)
        assert not any("relationship_context" in n for n in ctx.memory_retrieval_notes)

    def test_delta_hint_in_notes(self, tmp_path: Path):
        delta = _make_approved_delta()
        _write_delta_json(tmp_path, delta)
        ctx = _assemble(relationship_delta_path=tmp_path, distilled_root=tmp_path)
        assert any("relationship_delta" in n for n in ctx.memory_retrieval_notes)
        assert any("boundary_risk" in n for n in ctx.memory_retrieval_notes)

    def test_notes_absent_when_no_runtime_ready(self, tmp_path: Path):
        delta = _make_candidate_delta()
        _write_delta_json(tmp_path, delta)
        ctx = _assemble(relationship_delta_path=tmp_path, distilled_root=tmp_path)
        assert not any("relationship_context" in n for n in ctx.memory_retrieval_notes)


# ---------------------------------------------------------------------------
# Test: summary includes relationship guidance
# ---------------------------------------------------------------------------


class TestRelationshipContextSummaryInclusion:
    """Context summary includes approved relationship guidance when loaded."""

    def test_summary_includes_relationship_guidance(self, tmp_path: Path):
        delta = _make_approved_delta()
        _write_delta_json(tmp_path, delta)
        ctx = _assemble(relationship_delta_path=tmp_path, distilled_root=tmp_path)
        assert ctx.summary is not None
        assert "Approved relationship guidance" in ctx.summary
        assert "boundary_risk" in ctx.summary

    def test_summary_excludes_when_not_loaded(self):
        ctx = _assemble(relationship_delta_path=None)
        if ctx.summary:
            assert "Approved relationship guidance" not in ctx.summary

    def test_summary_excludes_when_no_runtime_ready(self, tmp_path: Path):
        delta = _make_candidate_delta()
        _write_delta_json(tmp_path, delta)
        ctx = _assemble(relationship_delta_path=tmp_path, distilled_root=tmp_path)
        if ctx.summary:
            assert "Approved relationship guidance" not in ctx.summary


# ---------------------------------------------------------------------------
# Test: determinism and no disk writes
# ---------------------------------------------------------------------------


class TestRelationshipContextDeterminism:
    """Same input produces same relationship context; no disk writes."""

    def test_same_result_twice(self, tmp_path: Path):
        delta = _make_approved_delta()
        _write_delta_json(tmp_path, delta)
        ctx1 = _assemble(relationship_delta_path=tmp_path, distilled_root=tmp_path)
        ctx2 = _assemble(relationship_delta_path=tmp_path, distilled_root=tmp_path)
        r1 = ctx1.relationship_context
        r2 = ctx2.relationship_context
        assert r1.status == r2.status
        assert len(r1.deltas) == len(r2.deltas)
        if r1.deltas and r2.deltas:
            assert r1.deltas[0].delta_id == r2.deltas[0].delta_id
            assert r1.deltas[0].dimension_changes == r2.deltas[0].dimension_changes

    def test_no_disk_writes(self, tmp_path: Path):
        delta = _make_approved_delta()
        _write_delta_json(tmp_path, delta)
        files_before = {
            f: f.read_bytes() for f in sorted(tmp_path.rglob("*")) if f.is_file()
        }
        _assemble(relationship_delta_path=tmp_path, distilled_root=tmp_path)
        files_after = {
            f: f.read_bytes() for f in sorted(tmp_path.rglob("*")) if f.is_file()
        }
        assert files_before == files_after
