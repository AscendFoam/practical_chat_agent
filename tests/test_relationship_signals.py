"""Tests for relationship signal extraction (T191)."""
from __future__ import annotations

import pytest

from practical_chat_agent.core.models import (
    RelationshipSignal,
    ReplyFeedbackLog,
    ReplyFeedbackRecord,
)
from practical_chat_agent.services.feedback import RelationshipSignalExtractor


def _make_record(
    *,
    feedback_id: str = "fb_test_001",
    contact_id: str = "contact_test",
    action: str = "boundary",
    boundary_label: str | None = None,
    boundary_note: str | None = None,
    edited_text: str | None = None,
) -> ReplyFeedbackRecord:
    return ReplyFeedbackRecord(
        feedback_id=feedback_id,
        contact_id=contact_id,
        reply_plan_id="plan_test_001",
        candidate_id="cand_test_001",
        priority_rank=1,
        action=action,
        boundary_label=boundary_label,
        boundary_note=boundary_note,
        edited_text=edited_text,
    )


def _make_log(records: list[ReplyFeedbackRecord]) -> ReplyFeedbackLog:
    return ReplyFeedbackLog(
        schema_version="reply_feedback_log_v1",
        records=records,
    )


class TestRelationshipSignalExtractor:
    def setup_method(self):
        self.extractor = RelationshipSignalExtractor()

    # -- clear boundary patterns produce signals --

    def test_boundary_violation_produces_boundary_risk_signal(self):
        record = _make_record(boundary_label="boundary_violation")
        signals = self.extractor.extract_from_feedback(
            feedback_log=_make_log([record]),
        )
        assert len(signals) >= 1
        sig = signals[0]
        assert sig.dimension_name == "boundary_risk"
        assert sig.direction == "increase"
        assert sig.strength > 0.0
        assert sig.provenance == "feedback_boundary"
        assert record.feedback_id in sig.evidence_refs

    def test_too_intimate_produces_multiple_signals(self):
        record = _make_record(boundary_label="too_intimate")
        signals = self.extractor.extract_from_feedback(
            feedback_log=_make_log([record]),
        )
        dims = {s.dimension_name for s in signals}
        assert "boundary_risk" in dims
        assert "intimacy_level" in dims
        assert len(signals) == 2

    def test_too_eager_produces_initiative_signal(self):
        record = _make_record(boundary_label="too_eager")
        signals = self.extractor.extract_from_feedback(
            feedback_log=_make_log([record]),
        )
        assert len(signals) == 1
        assert signals[0].dimension_name == "initiative_allowance"
        assert signals[0].direction == "decrease"

    # -- ambiguous / unsupported inputs produce no signals --

    def test_accept_action_no_signal(self):
        record = _make_record(action="accept")
        signals = self.extractor.extract_from_feedback(
            feedback_log=_make_log([record]),
        )
        assert signals == []

    def test_reject_action_no_signal(self):
        record = _make_record(action="reject")
        signals = self.extractor.extract_from_feedback(
            feedback_log=_make_log([record]),
        )
        assert signals == []

    def test_edit_action_no_signal(self):
        record = _make_record(action="edit", edited_text="some edited text")
        signals = self.extractor.extract_from_feedback(
            feedback_log=_make_log([record]),
        )
        assert signals == []

    def test_boundary_without_label_no_signal(self):
        record = _make_record(boundary_label=None, boundary_note="some note")
        signals = self.extractor.extract_from_feedback(
            feedback_log=_make_log([record]),
        )
        assert signals == []

    def test_unknown_boundary_label_no_signal(self):
        record = _make_record(boundary_label="custom_unknown_label")
        signals = self.extractor.extract_from_feedback(
            feedback_log=_make_log([record]),
        )
        assert signals == []

    def test_empty_log_no_signal(self):
        signals = self.extractor.extract_from_feedback(
            feedback_log=_make_log([]),
        )
        assert signals == []

    # -- evidence ref preservation --

    def test_evidence_refs_contain_feedback_id(self):
        record = _make_record(
            feedback_id="fb_ev_test",
            boundary_label="boundary_violation",
        )
        signals = self.extractor.extract_from_feedback(
            feedback_log=_make_log([record]),
        )
        for sig in signals:
            assert "fb_ev_test" in sig.evidence_refs

    # -- valid_record_ids filter --

    def test_valid_record_ids_filter(self):
        r1 = _make_record(
            feedback_id="fb_valid", boundary_label="boundary_violation",
        )
        r2 = _make_record(
            feedback_id="fb_excluded", boundary_label="too_eager",
        )
        signals = self.extractor.extract_from_feedback(
            feedback_log=_make_log([r1, r2]),
            valid_record_ids={"fb_valid"},
        )
        for sig in signals:
            assert "fb_valid" in sig.evidence_refs
            assert "fb_excluded" not in sig.evidence_refs

    def test_none_valid_ids_considers_all(self):
        r1 = _make_record(
            feedback_id="fb_a", boundary_label="boundary_violation",
        )
        r2 = _make_record(
            feedback_id="fb_b", boundary_label="too_eager",
        )
        signals = self.extractor.extract_from_feedback(
            feedback_log=_make_log([r1, r2]),
            valid_record_ids=None,
        )
        assert len(signals) >= 2

    # -- no raw text stored in signals --

    def test_no_raw_private_text_in_signals(self):
        record = _make_record(
            boundary_label="boundary_violation",
            boundary_note="This is a sensitive private note about boundaries",
        )
        signals = self.extractor.extract_from_feedback(
            feedback_log=_make_log([record]),
        )
        for sig in signals:
            assert "sensitive private note" not in (sig.signal_description or "")
            assert "sensitive private note" not in str(sig.evidence_refs)
            assert sig.signal_description is not None

    # -- multiple contacts --

    def test_multiple_contacts(self):
        r1 = _make_record(
            feedback_id="fb_alice",
            contact_id="contact_alice",
            boundary_label="boundary_violation",
        )
        r2 = _make_record(
            feedback_id="fb_bob",
            contact_id="contact_bob",
            boundary_label="too_eager",
        )
        signals = self.extractor.extract_from_feedback(
            feedback_log=_make_log([r1, r2]),
        )
        contacts = {s.contact_id for s in signals}
        assert "contact_alice" in contacts
        assert "contact_bob" in contacts


class TestRelationshipSignalModel:
    """Test RelationshipSignal model validation."""

    def test_valid_signal(self):
        sig = RelationshipSignal(
            contact_id="contact_test",
            dimension_name="trust",
            direction="increase",
            strength=0.5,
            evidence_refs=["fb_001"],
            provenance="feedback_boundary",
            signal_description="Test signal",
        )
        assert sig.status == "candidate"
        assert sig.provenance == "feedback_boundary"
        assert sig.dimension_name == "trust"
        assert not sig.is_runtime_ready()

    def test_rejects_empty_evidence_refs(self):
        with pytest.raises(Exception):
            RelationshipSignal(
                contact_id="contact_test",
                dimension_name="trust",
                strength=0.5,
                evidence_refs=[],
            )

    def test_rejects_invalid_dimension(self):
        with pytest.raises(Exception):
            RelationshipSignal(
                contact_id="contact_test",
                dimension_name="not_a_dimension",
                strength=0.5,
                evidence_refs=["fb_001"],
            )

    def test_rejects_out_of_range_strength(self):
        with pytest.raises(Exception):
            RelationshipSignal(
                contact_id="contact_test",
                dimension_name="trust",
                strength=1.5,
                evidence_refs=["fb_001"],
            )

    def test_rejects_negative_strength(self):
        with pytest.raises(Exception):
            RelationshipSignal(
                contact_id="contact_test",
                dimension_name="trust",
                strength=-0.1,
                evidence_refs=["fb_001"],
            )

    def test_default_status_is_candidate(self):
        sig = RelationshipSignal(
            contact_id="contact_test",
            dimension_name="trust",
            strength=0.3,
            evidence_refs=["fb_001"],
        )
        assert sig.status == "candidate"
        assert not sig.is_runtime_ready()

    def test_default_direction_is_unknown(self):
        sig = RelationshipSignal(
            contact_id="contact_test",
            dimension_name="trust",
            strength=0.3,
            evidence_refs=["fb_001"],
        )
        assert sig.direction == "unknown"
