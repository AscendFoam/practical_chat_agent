"""Tests for relationship delta review (T193)."""
from __future__ import annotations

from datetime import datetime, timezone

from practical_chat_agent.core.models import (
    RelationshipDeltaCandidate,
    RelationshipDeltaDimension,
)
from practical_chat_agent.services.feedback import (
    FeedbackError,
    RelationshipDeltaReviewService,
)


def _make_delta(
    *,
    delta_id: str = "delta_test_001",
    contact_id: str = "contact_test",
    status: str = "candidate",
) -> RelationshipDeltaCandidate:
    now = datetime.now(timezone.utc)
    dc = RelationshipDeltaDimension(
        dimension_name="boundary_risk",
        current_value=0.3,
        proposed_value=0.44,
        direction="increase",
        magnitude=0.14,
        rationale="boundary risk increase",
    )
    return RelationshipDeltaCandidate(
        delta_id=delta_id,
        contact_id=contact_id,
        source_state_id="state_test_001",
        dimension_changes=[dc],
        delta_rationale="Proposed based on 1 signal(s) across 1 dimension(s).",
        evidence_refs=["fb_001", "fb_002"],
        signal_refs=["sig_001"],
        status=status,
        created_at=now,
        updated_at=now,
    )


class TestRelationshipDeltaReviewService:
    def setup_method(self):
        self.service = RelationshipDeltaReviewService()

    # -- valid review actions --

    def test_approve_delta(self):
        delta = _make_delta()
        reviewed = self.service.review_delta(
            delta=delta, decision="approve", reviewer="reviewer_01",
        )
        assert reviewed.status == "approved"
        assert reviewed.delta_id == delta.delta_id
        assert reviewed.is_runtime_ready()

    def test_reject_delta(self):
        delta = _make_delta()
        reviewed = self.service.review_delta(
            delta=delta, decision="reject", reviewer="reviewer_01",
        )
        assert reviewed.status == "rejected"
        assert not reviewed.is_runtime_ready()

    def test_freeze_delta(self):
        delta = _make_delta()
        reviewed = self.service.review_delta(
            delta=delta, decision="freeze", reviewer="reviewer_01",
        )
        assert reviewed.status == "frozen"
        assert not reviewed.is_runtime_ready()

    def test_archive_delta(self):
        delta = _make_delta()
        reviewed = self.service.review_delta(
            delta=delta, decision="archive", reviewer="reviewer_01",
        )
        assert reviewed.status == "archived"
        assert not reviewed.is_runtime_ready()

    def test_approve_with_note(self):
        delta = _make_delta()
        reviewed = self.service.review_delta(
            delta=delta, decision="approve", reviewer="reviewer_01",
            note="Looks reasonable.",
        )
        assert reviewed.status == "approved"
        assert "Looks reasonable." in reviewed.review_metadata.decision_notes

    # -- invalid action handling --

    def test_invalid_decision_raises_error(self):
        delta = _make_delta()
        try:
            self.service.review_delta(
                delta=delta, decision="invalid", reviewer="reviewer_01",
            )
            assert False, "Expected FeedbackError"
        except FeedbackError:
            pass

    def test_case_insensitive_decision(self):
        delta = _make_delta()
        reviewed = self.service.review_delta(
            delta=delta, decision="APPROVE", reviewer="reviewer_01",
        )
        assert reviewed.status == "approved"

    def test_whitespace_decision(self):
        delta = _make_delta()
        reviewed = self.service.review_delta(
            delta=delta, decision="  approve  ", reviewer="reviewer_01",
        )
        assert reviewed.status == "approved"

    # -- runtime-ready approval path --

    def test_approved_delta_is_runtime_ready(self):
        delta = _make_delta()
        reviewed = self.service.review_delta(
            delta=delta, decision="approve", reviewer="reviewer_01",
        )
        assert reviewed.is_runtime_ready()
        assert reviewed.review_metadata.reviewed_by_human is True
        assert reviewed.review_metadata.last_decision == "approved"

    def test_candidate_not_runtime_ready(self):
        delta = _make_delta()
        assert not delta.is_runtime_ready()
        assert delta.review_metadata.reviewed_by_human is False

    def test_rejected_not_runtime_ready(self):
        delta = _make_delta()
        reviewed = self.service.review_delta(
            delta=delta, decision="reject", reviewer="reviewer_01",
        )
        assert not reviewed.is_runtime_ready()

    # -- preservation through review --

    def test_evidence_refs_preserved(self):
        delta = _make_delta()
        reviewed = self.service.review_delta(
            delta=delta, decision="approve", reviewer="reviewer_01",
        )
        assert reviewed.evidence_refs == ["fb_001", "fb_002"]

    def test_signal_refs_preserved(self):
        delta = _make_delta()
        reviewed = self.service.review_delta(
            delta=delta, decision="approve", reviewer="reviewer_01",
        )
        assert reviewed.signal_refs == ["sig_001"]

    def test_dimension_changes_preserved(self):
        delta = _make_delta()
        reviewed = self.service.review_delta(
            delta=delta, decision="approve", reviewer="reviewer_01",
        )
        assert len(reviewed.dimension_changes) == 1
        dc = reviewed.dimension_changes[0]
        assert dc.dimension_name == "boundary_risk"
        assert dc.current_value == 0.3
        assert dc.proposed_value == 0.44
        assert dc.direction == "increase"
        assert dc.magnitude == 0.14

    def test_contact_id_preserved(self):
        delta = _make_delta()
        reviewed = self.service.review_delta(
            delta=delta, decision="approve", reviewer="reviewer_01",
        )
        assert reviewed.contact_id == "contact_test"
        assert reviewed.source_state_id == "state_test_001"

    def test_delta_rationale_preserved(self):
        delta = _make_delta()
        reviewed = self.service.review_delta(
            delta=delta, decision="approve", reviewer="reviewer_01",
        )
        assert "Proposed based on" in reviewed.delta_rationale

    # -- review metadata updates --

    def test_review_metadata_updated_on_approve(self):
        delta = _make_delta()
        reviewed = self.service.review_delta(
            delta=delta, decision="approve", reviewer="reviewer_01",
        )
        meta = reviewed.review_metadata
        assert meta.review_state == "reviewed"
        assert meta.reviewed_by_human is True
        assert meta.last_decision == "approved"
        assert meta.last_reviewer_id == "reviewer_01"
        assert meta.last_reviewed_at is not None
        assert len(meta.history) == 1
        assert meta.history[0].status == "approved"
        assert meta.history[0].reviewer_id == "reviewer_01"

    def test_review_metadata_updated_on_reject(self):
        delta = _make_delta()
        reviewed = self.service.review_delta(
            delta=delta, decision="reject", reviewer="reviewer_02",
        )
        meta = reviewed.review_metadata
        assert meta.review_state == "reviewed"
        assert meta.reviewed_by_human is True
        assert meta.last_decision == "rejected"
        assert meta.last_reviewer_id == "reviewer_02"

    def test_updated_at_advanced(self):
        delta = _make_delta()
        original_updated = delta.updated_at
        reviewed = self.service.review_delta(
            delta=delta, decision="approve", reviewer="reviewer_01",
        )
        assert reviewed.updated_at >= original_updated

    # -- no state mutation / deep copy --

    def test_original_delta_not_mutated(self):
        delta = _make_delta()
        original_status = delta.status
        original_review_state = delta.review_metadata.review_state
        self.service.review_delta(
            delta=delta, decision="approve", reviewer="reviewer_01",
        )
        assert delta.status == original_status
        assert delta.review_metadata.review_state == original_review_state

    def test_multiple_reviews_accumulate_history(self):
        delta = _make_delta()
        r1 = self.service.review_delta(
            delta=delta, decision="freeze", reviewer="reviewer_01",
            note="Freezing for now.",
        )
        assert len(r1.review_metadata.history) == 1

        r2 = self.service.review_delta(
            delta=r1, decision="approve", reviewer="reviewer_02",
            note="Unfreezing and approving.",
        )
        assert len(r2.review_metadata.history) == 2
        assert r2.review_metadata.history[0].status == "frozen"
        assert r2.review_metadata.history[1].status == "approved"
        assert r2.status == "approved"
        assert r2.is_runtime_ready()

    # -- all-or-nothing semantics --

    def test_all_dimensions_reviewed_together(self):
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
        delta = RelationshipDeltaCandidate(
            contact_id="contact_test",
            source_state_id="state_test_001",
            dimension_changes=[dc1, dc2],
            delta_rationale="Multi-dimension proposal.",
            evidence_refs=["fb_001"],
        )
        reviewed = self.service.review_delta(
            delta=delta, decision="approve", reviewer="reviewer_01",
        )
        assert reviewed.status == "approved"
        assert len(reviewed.dimension_changes) == 2
