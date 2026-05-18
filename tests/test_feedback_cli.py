"""T152: Feedback CLI Regression Tests.

Deterministic tests covering T140-T142 feedback capture, validation, and
summary CLI loop.  All fixtures are synthetic and contain no private chat
content, real names, real platform IDs, or private paths.

Required coverage areas (indexed by T152 task package):
  1. accept feedback append
  2. edit feedback append
  3. reject feedback append
  4. boundary feedback append
  5. invalid candidate rank/id rejected
  6. invalid plan path rejected or reported safely
  7. validator catches invalid action-specific fields
  8. summary exporter reports aggregate counts
  9. validator report merge into summary is surfaced aggregate-only
 10. stdout does not print full draft text, edited text, user note,
     boundary note, raw transcript, or private chat path contents
 11. feedback flow does not mutate memory/ContactSkill/store records
 12. private output confinement behavior is enforced or explicitly validated
 13. corrupted or unreadable log input is surfaced explicitly rather than
     silently normalized away
 14. compact validation/summary behavior remains readable without relying
     on verbose per-record payloads
 15. at least one end-to-end CLI-path regression for append, validate,
     and summarize behavior
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from practical_chat_agent.core.models import (
    ReplyFeedbackAction,
    ReplyFeedbackLog,
    ReplyFeedbackRecord,
    ReplyPlan,
    ReplyPlanCandidate,
    ReplyPlanContextRef,
    ReplyPlanSourceContext,
)
from practical_chat_agent.services.feedback import (
    FeedbackError,
    FeedbackService,
    FeedbackSummaryService,
    FeedbackValidationService,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _synthetic_reply_plan(
    contact_id: str = "contact_test",
    skill_record_id: str = "approved_skill_test_001",
) -> ReplyPlan:
    """Create a minimal synthetic ReplyPlan for feedback testing."""
    return ReplyPlan(
        contact_id=contact_id,
        source_context=ReplyPlanSourceContext(
            approved_store_status="loaded",
            chat_context_summary="synthetic test context",
            approved_contact_skill_record_id=skill_record_id,
            approved_memory_record_ids=["approved_mem_test_001"],
        ),
        policy_boundary_summary=["synthetic policy boundary"],
        notes_on_candidate_differences=["synthetic note a", "synthetic note b"],
        candidates=[
            ReplyPlanCandidate(
                candidate_id="replycand_test_001",
                approach_label="conservative_acknowledgment",
                priority_rank=1,
                draft_text="synthetic draft text candidate one",
                rationale="synthetic rationale one",
                supporting_context_refs=[
                    ReplyPlanContextRef(
                        ref_type="recent_event",
                        ref_id="evt_test_001",
                    ),
                ],
                boundary_reminders=["synthetic boundary reminder"],
            ),
            ReplyPlanCandidate(
                candidate_id="replycand_test_002",
                approach_label="light_follow_up",
                priority_rank=2,
                draft_text="synthetic draft text candidate two",
                rationale="synthetic rationale two",
                supporting_context_refs=[
                    ReplyPlanContextRef(
                        ref_type="approved_contact_skill_record",
                        ref_id="approved_skill_test_001",
                    ),
                ],
                boundary_reminders=["synthetic boundary reminder"],
            ),
            ReplyPlanCandidate(
                candidate_id="replycand_test_003",
                approach_label="warm_but_guarded",
                priority_rank=3,
                draft_text="synthetic draft text candidate three",
                rationale="synthetic rationale three",
                supporting_context_refs=[
                    ReplyPlanContextRef(
                        ref_type="memory_hit",
                        ref_id="mem_test_001",
                    ),
                ],
                boundary_reminders=["synthetic boundary reminder"],
            ),
        ],
    )


def _write_plan(tmp_path: Path, plan: ReplyPlan | None = None) -> Path:
    """Write a synthetic ReplyPlan to a temp file and return the path."""
    plan = plan or _synthetic_reply_plan()
    plan_path = tmp_path / "synthetic_reply_plan.json"
    plan_path.write_text(
        plan.model_dump_json(indent=2), encoding="utf-8",
    )
    return plan_path


def _write_feedback_log(
    tmp_path: Path,
    records: list[ReplyFeedbackRecord],
    filename: str = "feedback_log.json",
) -> Path:
    """Write a synthetic feedback log to a temp file."""
    log = ReplyFeedbackLog(records=records)
    log_path = tmp_path / filename
    log_path.write_text(
        json.dumps(log.model_dump(mode="json"), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return log_path


def _make_record(
    *,
    action: ReplyFeedbackAction = "accept",
    contact_id: str = "contact_test",
    candidate_id: str = "replycand_test_001",
    priority_rank: int = 1,
    reply_plan_id: str | None = "approved_skill_test_001",
    source_plan_path: str | None = None,
    user_note: str | None = None,
    edited_text: str | None = None,
    boundary_label: str | None = None,
    boundary_note: str | None = None,
) -> ReplyFeedbackRecord:
    return ReplyFeedbackRecord(
        contact_id=contact_id,
        reply_plan_id=reply_plan_id,
        candidate_id=candidate_id,
        priority_rank=priority_rank,
        action=action,
        user_note=user_note,
        edited_text=edited_text,
        boundary_label=boundary_label,
        boundary_note=boundary_note,
        source_plan_path=source_plan_path,
    )


# ---------------------------------------------------------------------------
# 1-4. Feedback append (accept / edit / reject / boundary)
# ---------------------------------------------------------------------------


class TestFeedbackAppendAccept:
    """Accept feedback is appended to the feedback log."""

    def test_accept_record_appended(self, tmp_path: Path):
        plan_path = _write_plan(tmp_path)
        output_path = tmp_path / "feedback.json"
        svc = FeedbackService()
        result = svc.record_feedback(
            plan_path=plan_path,
            candidate_rank=1,
            action="accept",
            output_path=output_path,
        )
        assert result["action"] == "accept"
        assert result["priority_rank"] == 1
        assert result["total_records"] == 1

    def test_accept_log_readable(self, tmp_path: Path):
        plan_path = _write_plan(tmp_path)
        output_path = tmp_path / "feedback.json"
        svc = FeedbackService()
        svc.record_feedback(
            plan_path=plan_path,
            candidate_rank=1,
            action="accept",
            output_path=output_path,
        )
        log_data = json.loads(output_path.read_text(encoding="utf-8"))
        log = ReplyFeedbackLog.model_validate(log_data)
        assert len(log.records) == 1
        assert log.records[0].action == "accept"
        assert log.records[0].edited_text is None
        assert log.records[0].boundary_label is None


class TestFeedbackAppendEdit:
    """Edit feedback is appended with edited_text preserved in log only."""

    def test_edit_record_appended(self, tmp_path: Path):
        plan_path = _write_plan(tmp_path)
        output_path = tmp_path / "feedback.json"
        svc = FeedbackService()
        result = svc.record_feedback(
            plan_path=plan_path,
            candidate_rank=2,
            action="edit",
            output_path=output_path,
            edited_text="synthetic edited replacement text abcxyz789",
        )
        assert result["action"] == "edit"
        assert result["priority_rank"] == 2
        assert result["total_records"] == 1

    def test_edit_text_in_log_not_in_service_result(self, tmp_path: Path):
        plan_path = _write_plan(tmp_path)
        output_path = tmp_path / "feedback.json"
        svc = FeedbackService()
        result = svc.record_feedback(
            plan_path=plan_path,
            candidate_rank=2,
            action="edit",
            output_path=output_path,
            edited_text="synthetic edited replacement text abcxyz789",
        )
        assert "edited_text" not in result
        assert "abcxyz789" not in json.dumps(result)

        log_data = json.loads(output_path.read_text(encoding="utf-8"))
        log = ReplyFeedbackLog.model_validate(log_data)
        assert log.records[0].edited_text == "synthetic edited replacement text abcxyz789"

    def test_edit_without_text_rejected(self, tmp_path: Path):
        plan_path = _write_plan(tmp_path)
        output_path = tmp_path / "feedback.json"
        svc = FeedbackService()
        with pytest.raises(FeedbackError, match="edited-text"):
            svc.record_feedback(
                plan_path=plan_path,
                candidate_rank=1,
                action="edit",
                output_path=output_path,
            )


class TestFeedbackAppendReject:
    """Reject feedback is appended with optional note preserved in log only."""

    def test_reject_record_appended(self, tmp_path: Path):
        plan_path = _write_plan(tmp_path)
        output_path = tmp_path / "feedback.json"
        svc = FeedbackService()
        result = svc.record_feedback(
            plan_path=plan_path,
            candidate_rank=3,
            action="reject",
            output_path=output_path,
            user_note="synthetic user note defghij456",
        )
        assert result["action"] == "reject"
        assert result["priority_rank"] == 3

    def test_reject_note_in_log_not_in_service_result(self, tmp_path: Path):
        plan_path = _write_plan(tmp_path)
        output_path = tmp_path / "feedback.json"
        svc = FeedbackService()
        result = svc.record_feedback(
            plan_path=plan_path,
            candidate_rank=1,
            action="reject",
            output_path=output_path,
            user_note="synthetic user note defghij456",
        )
        assert "user_note" not in result
        assert "defghij456" not in json.dumps(result)

        log_data = json.loads(output_path.read_text(encoding="utf-8"))
        log = ReplyFeedbackLog.model_validate(log_data)
        assert log.records[0].user_note == "synthetic user note defghij456"


class TestFeedbackAppendBoundary:
    """Boundary feedback is appended with label/note preserved in log only."""

    def test_boundary_record_appended(self, tmp_path: Path):
        plan_path = _write_plan(tmp_path)
        output_path = tmp_path / "feedback.json"
        svc = FeedbackService()
        result = svc.record_feedback(
            plan_path=plan_path,
            candidate_rank=1,
            action="boundary",
            output_path=output_path,
            boundary_label="synthetic_label",
            boundary_note="synthetic boundary note pqrstu123",
        )
        assert result["action"] == "boundary"

    def test_boundary_note_not_in_service_result(self, tmp_path: Path):
        plan_path = _write_plan(tmp_path)
        output_path = tmp_path / "feedback.json"
        svc = FeedbackService()
        result = svc.record_feedback(
            plan_path=plan_path,
            candidate_rank=1,
            action="boundary",
            output_path=output_path,
            boundary_label="synthetic_label",
            boundary_note="synthetic boundary note pqrstu123",
        )
        assert "boundary_note" not in result
        assert "pqrstu123" not in json.dumps(result)

        log_data = json.loads(output_path.read_text(encoding="utf-8"))
        log = ReplyFeedbackLog.model_validate(log_data)
        assert log.records[0].boundary_note == "synthetic boundary note pqrstu123"
        assert log.records[0].boundary_label == "synthetic_label"

    def test_boundary_without_label_or_note_rejected(self, tmp_path: Path):
        plan_path = _write_plan(tmp_path)
        output_path = tmp_path / "feedback.json"
        svc = FeedbackService()
        with pytest.raises(FeedbackError, match="boundary"):
            svc.record_feedback(
                plan_path=plan_path,
                candidate_rank=1,
                action="boundary",
                output_path=output_path,
            )


# ---------------------------------------------------------------------------
# 5-6. Invalid candidate rank / invalid plan path
# ---------------------------------------------------------------------------


class TestFeedbackInvalidInputs:
    """Invalid candidate rank and plan path are rejected safely."""

    def test_invalid_candidate_rank_rejected(self, tmp_path: Path):
        plan_path = _write_plan(tmp_path)
        output_path = tmp_path / "feedback.json"
        svc = FeedbackService()
        with pytest.raises(FeedbackError, match="Valid ranks"):
            svc.record_feedback(
                plan_path=plan_path,
                candidate_rank=99,
                action="accept",
                output_path=output_path,
            )

    def test_missing_plan_file_rejected(self, tmp_path: Path):
        plan_path = tmp_path / "nonexistent_plan.json"
        output_path = tmp_path / "feedback.json"
        svc = FeedbackService()
        with pytest.raises(FeedbackError, match="not found"):
            svc.record_feedback(
                plan_path=plan_path,
                candidate_rank=1,
                action="accept",
                output_path=output_path,
            )

    def test_invalid_plan_json_rejected(self, tmp_path: Path):
        plan_path = tmp_path / "bad_plan.json"
        plan_path.write_text("not valid json{{{", encoding="utf-8")
        output_path = tmp_path / "feedback.json"
        svc = FeedbackService()
        with pytest.raises(FeedbackError, match="Invalid ReplyPlan"):
            svc.record_feedback(
                plan_path=plan_path,
                candidate_rank=1,
                action="accept",
                output_path=output_path,
            )

    def test_zero_rank_rejected(self, tmp_path: Path):
        plan_path = _write_plan(tmp_path)
        output_path = tmp_path / "feedback.json"
        svc = FeedbackService()
        with pytest.raises(FeedbackError, match="Valid ranks"):
            svc.record_feedback(
                plan_path=plan_path,
                candidate_rank=0,
                action="accept",
                output_path=output_path,
            )


# ---------------------------------------------------------------------------
# 7. Validator catches invalid action-specific fields
# ---------------------------------------------------------------------------


class TestValidationActionSpecific:
    """Validator detects edit-without-text and boundary-without-details."""

    def _make_bad_log(self, tmp_path: Path) -> Path:
        records = [
            _make_record(action="edit", edited_text=None),
            _make_record(action="boundary", boundary_label=None, boundary_note=None),
        ]
        return _write_feedback_log(tmp_path, records)

    def test_edit_without_text_detected(self, tmp_path: Path):
        log_path = self._make_bad_log(tmp_path)
        svc = FeedbackValidationService()
        report = svc.validate(input_path=log_path)
        assert report["edit_without_text_count"] == 1
        assert report["invalid_record_count"] >= 1

    def test_boundary_without_details_detected(self, tmp_path: Path):
        log_path = self._make_bad_log(tmp_path)
        svc = FeedbackValidationService()
        report = svc.validate(input_path=log_path)
        assert report["boundary_without_details_count"] == 1
        assert report["invalid_record_count"] >= 1

    def test_valid_records_counted(self, tmp_path: Path):
        records = [
            _make_record(action="edit", edited_text="synthetic edited"),
            _make_record(action="boundary", boundary_label="syn_label"),
        ]
        log_path = _write_feedback_log(tmp_path, records)
        svc = FeedbackValidationService()
        report = svc.validate(input_path=log_path)
        assert report["valid_record_count"] == 2
        assert report["invalid_record_count"] == 0


class TestValidationPlanReference:
    """Validator detects missing plans, missing candidates, and contact
    mismatch when source_plan_path references a plan file."""

    def test_missing_plan_reported(self, tmp_path: Path):
        records = [
            _make_record(source_plan_path="/nonexistent/plan.json"),
        ]
        log_path = _write_feedback_log(tmp_path, records)
        svc = FeedbackValidationService()
        report = svc.validate(input_path=log_path)
        assert report["missing_plan_count"] == 1

    def test_missing_candidate_reported(self, tmp_path: Path):
        plan_path = _write_plan(tmp_path)
        records = [
            _make_record(
                candidate_id="nonexistent_candidate",
                priority_rank=99,
                source_plan_path=str(plan_path),
            ),
        ]
        log_path = _write_feedback_log(tmp_path, records)
        svc = FeedbackValidationService()
        report = svc.validate(input_path=log_path)
        assert report["missing_candidate_count"] == 1

    def test_contact_mismatch_reported(self, tmp_path: Path):
        plan_path = _write_plan(tmp_path)
        records = [
            _make_record(
                contact_id="contact_WRONG",
                source_plan_path=str(plan_path),
            ),
        ]
        log_path = _write_feedback_log(tmp_path, records)
        svc = FeedbackValidationService()
        report = svc.validate(input_path=log_path)
        assert report["contact_mismatch_count"] == 1


# ---------------------------------------------------------------------------
# 8. Summary exporter reports aggregate counts
# ---------------------------------------------------------------------------


class TestSummaryAggregateCounts:
    """Summary exporter reports correct aggregate counts over a good log."""

    def _make_good_log(self, tmp_path: Path, plan_path: Path) -> Path:
        records = [
            _make_record(action="accept", source_plan_path=str(plan_path)),
            _make_record(
                action="edit",
                priority_rank=2,
                candidate_id="replycand_test_002",
                edited_text="synthetic edited",
                source_plan_path=str(plan_path),
                user_note="synthetic note",
            ),
            _make_record(
                action="reject",
                priority_rank=3,
                candidate_id="replycand_test_003",
                source_plan_path=str(plan_path),
            ),
            _make_record(
                action="boundary",
                boundary_label="syn_label",
                boundary_note="syn note",
                source_plan_path=str(plan_path),
            ),
        ]
        return _write_feedback_log(tmp_path, records)

    def test_total_records(self, tmp_path: Path):
        plan_path = _write_plan(tmp_path)
        log_path = self._make_good_log(tmp_path, plan_path)
        svc = FeedbackSummaryService()
        summary = svc.summarize(input_path=log_path)
        assert summary["total_records"] == 4

    def test_counts_by_action(self, tmp_path: Path):
        plan_path = _write_plan(tmp_path)
        log_path = self._make_good_log(tmp_path, plan_path)
        svc = FeedbackSummaryService()
        summary = svc.summarize(input_path=log_path)
        assert summary["counts_by_action"] == {
            "accept": 1, "edit": 1, "reject": 1, "boundary": 1,
        }

    def test_distinct_counts(self, tmp_path: Path):
        plan_path = _write_plan(tmp_path)
        log_path = self._make_good_log(tmp_path, plan_path)
        svc = FeedbackSummaryService()
        summary = svc.summarize(input_path=log_path)
        assert summary["distinct_contact_ids"] == 1
        assert summary["distinct_candidate_ids"] == 3

    def test_boundary_and_edited_counts(self, tmp_path: Path):
        plan_path = _write_plan(tmp_path)
        log_path = self._make_good_log(tmp_path, plan_path)
        svc = FeedbackSummaryService()
        summary = svc.summarize(input_path=log_path)
        assert summary["records_with_boundary_label"] == 1
        assert summary["records_with_edited_text"] == 1
        assert summary["records_with_user_note"] == 1

    def test_approach_labels_loaded(self, tmp_path: Path):
        plan_path = _write_plan(tmp_path)
        log_path = self._make_good_log(tmp_path, plan_path)
        svc = FeedbackSummaryService()
        summary = svc.summarize(input_path=log_path)
        labels = summary["counts_by_approach_label"]
        assert "conservative_acknowledgment" in labels
        assert labels["conservative_acknowledgment"] == 2


# ---------------------------------------------------------------------------
# 9. Validation report merge into summary
# ---------------------------------------------------------------------------


class TestSummaryValidationMerge:
    """T141 validation report merge surfaces aggregate counts only."""

    def test_merge_success(self, tmp_path: Path):
        plan_path = _write_plan(tmp_path)
        records = [_make_record(action="accept", source_plan_path=str(plan_path))]
        log_path = _write_feedback_log(tmp_path, records)

        validation_svc = FeedbackValidationService()
        report = validation_svc.validate(input_path=log_path)
        report_path = tmp_path / "validation_report.json"
        report_path.write_text(
            json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8",
        )

        summary_svc = FeedbackSummaryService()
        summary = summary_svc.summarize(
            input_path=log_path,
            validation_report_path=report_path,
        )
        vs = summary["validation_summary"]
        assert vs["status"] == "merged"
        assert "valid_record_count" in vs
        assert "invalid_record_count" in vs
        assert "privacy_warning_count" in vs

    def test_merge_does_not_echo_raw_record_results(self, tmp_path: Path):
        plan_path = _write_plan(tmp_path)
        records = [_make_record(action="accept", source_plan_path=str(plan_path))]
        log_path = _write_feedback_log(tmp_path, records)

        validation_svc = FeedbackValidationService()
        report = validation_svc.validate(input_path=log_path)
        report_path = tmp_path / "validation_report.json"
        report_path.write_text(
            json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8",
        )

        summary_svc = FeedbackSummaryService()
        summary = summary_svc.summarize(
            input_path=log_path,
            validation_report_path=report_path,
        )
        vs = summary["validation_summary"]
        assert "record_results" not in vs

    def test_missing_validation_report(self, tmp_path: Path):
        records = [_make_record(action="accept")]
        log_path = _write_feedback_log(tmp_path, records)
        missing_report = tmp_path / "missing_report.json"

        svc = FeedbackSummaryService()
        summary = svc.summarize(
            input_path=log_path,
            validation_report_path=missing_report,
        )
        assert summary["validation_summary"]["status"] == "report_not_found"


# ---------------------------------------------------------------------------
# 10. stdout / output privacy
# ---------------------------------------------------------------------------


class TestPrivacySafety:
    """Service results and summary output do not leak private text."""

    PRIVATE_DRAFT = "unique_private_draft_marker_qwerty111"
    PRIVATE_EDITED = "unique_private_edited_marker_asdfgh222"
    PRIVATE_NOTE = "unique_private_note_marker_zxcvbn333"
    PRIVATE_BOUNDARY_NOTE = "unique_private_boundary_marker_yuiop444"

    def test_service_result_no_draft_text(self, tmp_path: Path):
        plan = _synthetic_reply_plan()
        plan.candidates[0].draft_text = self.PRIVATE_DRAFT
        plan_path = _write_plan(tmp_path, plan)
        output_path = tmp_path / "feedback.json"
        svc = FeedbackService()
        result = svc.record_feedback(
            plan_path=plan_path,
            candidate_rank=1,
            action="accept",
            output_path=output_path,
        )
        result_json = json.dumps(result)
        assert self.PRIVATE_DRAFT not in result_json

    def test_service_result_no_edited_text(self, tmp_path: Path):
        plan_path = _write_plan(tmp_path)
        output_path = tmp_path / "feedback.json"
        svc = FeedbackService()
        result = svc.record_feedback(
            plan_path=plan_path,
            candidate_rank=1,
            action="edit",
            output_path=output_path,
            edited_text=self.PRIVATE_EDITED,
        )
        result_json = json.dumps(result)
        assert self.PRIVATE_EDITED not in result_json

    def test_service_result_no_user_note(self, tmp_path: Path):
        plan_path = _write_plan(tmp_path)
        output_path = tmp_path / "feedback.json"
        svc = FeedbackService()
        result = svc.record_feedback(
            plan_path=plan_path,
            candidate_rank=1,
            action="reject",
            output_path=output_path,
            user_note=self.PRIVATE_NOTE,
        )
        result_json = json.dumps(result)
        assert self.PRIVATE_NOTE not in result_json

    def test_service_result_no_boundary_note(self, tmp_path: Path):
        plan_path = _write_plan(tmp_path)
        output_path = tmp_path / "feedback.json"
        svc = FeedbackService()
        result = svc.record_feedback(
            plan_path=plan_path,
            candidate_rank=1,
            action="boundary",
            output_path=output_path,
            boundary_label="syn_label",
            boundary_note=self.PRIVATE_BOUNDARY_NOTE,
        )
        result_json = json.dumps(result)
        assert self.PRIVATE_BOUNDARY_NOTE not in result_json

    def test_summary_output_no_private_text(self, tmp_path: Path):
        records = [
            _make_record(
                action="edit",
                edited_text=self.PRIVATE_EDITED,
                user_note=self.PRIVATE_NOTE,
            ),
            _make_record(
                action="boundary",
                boundary_label="syn_label",
                boundary_note=self.PRIVATE_BOUNDARY_NOTE,
            ),
        ]
        log_path = _write_feedback_log(tmp_path, records)
        output_path = tmp_path / "summary.json"

        svc = FeedbackSummaryService()
        summary = svc.summarize(input_path=log_path, output_path=output_path)
        summary_json = json.dumps(summary)
        assert self.PRIVATE_EDITED not in summary_json
        assert self.PRIVATE_NOTE not in summary_json
        assert self.PRIVATE_BOUNDARY_NOTE not in summary_json

    def test_validation_report_no_private_text(self, tmp_path: Path):
        records = [
            _make_record(
                action="edit",
                edited_text=self.PRIVATE_EDITED,
            ),
            _make_record(
                action="boundary",
                boundary_note=self.PRIVATE_BOUNDARY_NOTE,
            ),
        ]
        log_path = _write_feedback_log(tmp_path, records)

        svc = FeedbackValidationService()
        report = svc.validate(input_path=log_path)
        report_json = json.dumps(report)
        assert self.PRIVATE_EDITED not in report_json
        assert self.PRIVATE_BOUNDARY_NOTE not in report_json

    def test_log_file_still_contains_private_text(self, tmp_path: Path):
        """Confirm that the privacy guard does not strip from the private
        log file itself — the private log is meant to store this data."""
        plan_path = _write_plan(tmp_path)
        output_path = tmp_path / "feedback.json"
        svc = FeedbackService()
        svc.record_feedback(
            plan_path=plan_path,
            candidate_rank=1,
            action="edit",
            output_path=output_path,
            edited_text=self.PRIVATE_EDITED,
        )
        log_text = output_path.read_text(encoding="utf-8")
        assert self.PRIVATE_EDITED in log_text


# ---------------------------------------------------------------------------
# 11. Non-mutation: feedback does not alter planner/store/memory
# ---------------------------------------------------------------------------


class TestNonMutation:
    """Feedback flow does not mutate memory, ContactSkill, or store records."""

    def test_feedback_does_not_modify_plan_file(self, tmp_path: Path):
        plan_path = _write_plan(tmp_path)
        output_path = tmp_path / "feedback.json"
        plan_before = plan_path.read_text(encoding="utf-8")

        svc = FeedbackService()
        svc.record_feedback(
            plan_path=plan_path,
            candidate_rank=1,
            action="accept",
            output_path=output_path,
        )
        plan_after = plan_path.read_text(encoding="utf-8")
        assert plan_before == plan_after

    def test_validation_is_read_only(self, tmp_path: Path):
        records = [_make_record(action="accept")]
        log_path = _write_feedback_log(tmp_path, records)
        log_before = log_path.read_text(encoding="utf-8")

        svc = FeedbackValidationService()
        svc.validate(input_path=log_path)
        log_after = log_path.read_text(encoding="utf-8")
        assert log_before == log_after

    def test_summary_is_read_only(self, tmp_path: Path):
        records = [_make_record(action="accept")]
        log_path = _write_feedback_log(tmp_path, records)
        log_before = log_path.read_text(encoding="utf-8")

        svc = FeedbackSummaryService()
        svc.summarize(input_path=log_path)
        log_after = log_path.read_text(encoding="utf-8")
        assert log_before == log_after

    def test_append_does_not_mutate_existing_records(self, tmp_path: Path):
        plan_path = _write_plan(tmp_path)
        output_path = tmp_path / "feedback.json"
        svc = FeedbackService()

        svc.record_feedback(
            plan_path=plan_path,
            candidate_rank=1,
            action="accept",
            output_path=output_path,
        )
        log_data_1 = json.loads(output_path.read_text(encoding="utf-8"))
        first_record_id = log_data_1["records"][0]["feedback_id"]

        svc.record_feedback(
            plan_path=plan_path,
            candidate_rank=2,
            action="reject",
            output_path=output_path,
        )
        log_data_2 = json.loads(output_path.read_text(encoding="utf-8"))
        assert len(log_data_2["records"]) == 2
        assert log_data_2["records"][0]["feedback_id"] == first_record_id
        assert log_data_2["records"][0]["action"] == "accept"
        assert log_data_2["records"][1]["action"] == "reject"


# ---------------------------------------------------------------------------
# 12. Private output confinement
# ---------------------------------------------------------------------------


class TestPrivateOutputConfinement:
    """Private-path confinement is validated or warned, not enforced."""

    def test_validator_warns_on_non_private_input(self, tmp_path: Path):
        """When the input log is outside private/, a privacy warning is
        surfaced.  The validator does not enforce confinement, only warns."""
        records = [_make_record(action="accept")]
        log_path = _write_feedback_log(tmp_path, records)

        svc = FeedbackValidationService()
        report = svc.validate(input_path=log_path)
        assert len(report["privacy_warnings"]) >= 1
        assert any("W_PRIVACY_INPUT" in w for w in report["privacy_warnings"])

    def test_validator_warns_on_non_private_plan_ref(self, tmp_path: Path):
        """When source_plan_path resolves outside private/, a privacy
        warning is surfaced for the record."""
        plan_path = _write_plan(tmp_path)
        records = [
            _make_record(source_plan_path=str(plan_path)),
        ]
        log_path = _write_feedback_log(tmp_path, records)

        svc = FeedbackValidationService()
        report = svc.validate(input_path=log_path)
        assert any("W_PRIVACY_REF" in w for w in report["privacy_warnings"])

    def test_service_allows_any_output_path(self, tmp_path: Path):
        """FeedbackService does not enforce output path confinement;
        it writes wherever the caller requests.  This is by design for
        the single-user offline workflow."""
        plan_path = _write_plan(tmp_path)
        output_path = tmp_path / "outside_private" / "feedback.json"
        svc = FeedbackService()
        result = svc.record_feedback(
            plan_path=plan_path,
            candidate_rank=1,
            action="accept",
            output_path=output_path,
        )
        assert result["total_records"] == 1
        assert output_path.exists()


# ---------------------------------------------------------------------------
# 13. Corrupted / unreadable input is surfaced explicitly
# ---------------------------------------------------------------------------


class TestCorruptedInput:
    """Corrupted or unreadable log input is surfaced explicitly rather than
    silently normalized away."""

    def test_corrupted_json_surfaceed_by_validator(self, tmp_path: Path):
        bad_log = tmp_path / "corrupted.json"
        bad_log.write_text("{bad json content!!!", encoding="utf-8")
        svc = FeedbackValidationService()
        report = svc.validate(input_path=bad_log)
        assert report["is_readable"] is False
        assert report["corrupted_input_count"] == 1
        assert "json_decode_error" in report["corrupted_reason"]

    def test_schema_invalid_log_surfaceed_by_validator(self, tmp_path: Path):
        bad_log = tmp_path / "schema_invalid.json"
        bad_log.write_text(
            json.dumps({
                "schema_version": "reply_feedback_log_v1",
                "records": [{"action": "invalid_action"}],
            }),
            encoding="utf-8",
        )
        svc = FeedbackValidationService()
        report = svc.validate(input_path=bad_log)
        assert report["is_readable"] is False
        assert report["corrupted_input_count"] == 1
        assert "schema_error" in report["corrupted_reason"]

    def test_missing_file_surfaceed_by_validator(self, tmp_path: Path):
        missing = tmp_path / "nonexistent.json"
        svc = FeedbackValidationService()
        report = svc.validate(input_path=missing)
        assert report["is_readable"] is False
        assert report["corrupted_reason"] == "file_not_found"

    def test_corrupted_json_surfaceed_by_summary(self, tmp_path: Path):
        bad_log = tmp_path / "corrupted.json"
        bad_log.write_text("not valid json{{{", encoding="utf-8")
        svc = FeedbackSummaryService()
        summary = svc.summarize(input_path=bad_log)
        assert summary["is_readable"] is False
        assert "json_decode_error" in summary["corrupted_reason"]

    def test_missing_file_surfaceed_by_summary(self, tmp_path: Path):
        missing = tmp_path / "nonexistent.json"
        svc = FeedbackSummaryService()
        summary = svc.summarize(input_path=missing)
        assert summary["is_readable"] is False
        assert summary["corrupted_reason"] == "file_not_found"

    def test_corrupted_output_with_output_path(self, tmp_path: Path):
        """Even when output_path is set, corrupted input produces a summary
        with is_readable=False and corrupted_reason."""
        bad_log = tmp_path / "corrupted.json"
        bad_log.write_text("{{invalid", encoding="utf-8")
        output_path = tmp_path / "summary_output.json"
        svc = FeedbackSummaryService()
        summary = svc.summarize(
            input_path=bad_log, output_path=output_path,
        )
        assert summary["is_readable"] is False
        assert output_path.exists()


# ---------------------------------------------------------------------------
# 14. Compact validation/summary output
# ---------------------------------------------------------------------------


class TestCompactOutput:
    """Validation and summary output is compact and does not echo verbose
    per-record private text payloads."""

    def test_validation_report_has_no_edited_text(self, tmp_path: Path):
        records = [
            _make_record(
                action="edit",
                edited_text="verbose edited text that should not appear in report",
            ),
        ]
        log_path = _write_feedback_log(tmp_path, records)
        svc = FeedbackValidationService()
        report = svc.validate(input_path=log_path)
        report_json = json.dumps(report)
        assert "verbose edited text" not in report_json

    def test_validation_report_has_no_user_note(self, tmp_path: Path):
        records = [
            _make_record(
                action="reject",
                user_note="verbose user note that should not appear in report",
            ),
        ]
        log_path = _write_feedback_log(tmp_path, records)
        svc = FeedbackValidationService()
        report = svc.validate(input_path=log_path)
        report_json = json.dumps(report)
        assert "verbose user note" not in report_json

    def test_validation_report_has_no_boundary_note(self, tmp_path: Path):
        records = [
            _make_record(
                action="boundary",
                boundary_label="syn",
                boundary_note="verbose boundary note not in report",
            ),
        ]
        log_path = _write_feedback_log(tmp_path, records)
        svc = FeedbackValidationService()
        report = svc.validate(input_path=log_path)
        report_json = json.dumps(report)
        assert "verbose boundary note" not in report_json

    def test_summary_is_compact(self, tmp_path: Path):
        records = [
            _make_record(action="accept"),
            _make_record(action="edit", edited_text="edited text"),
            _make_record(action="boundary", boundary_label="syn"),
        ]
        log_path = _write_feedback_log(tmp_path, records)
        svc = FeedbackSummaryService()
        summary = svc.summarize(input_path=log_path)
        summary_json = json.dumps(summary)
        assert "edited text" not in summary_json
        assert summary["total_records"] == 3
        assert len(summary["counts_by_action"]) == 3


# ---------------------------------------------------------------------------
# 15. End-to-end CLI-path regression tests
# ---------------------------------------------------------------------------


class TestCLIAppendRegression:
    """End-to-end CLI regression for chat-reply-feedback append."""

    def test_cli_accept(self, tmp_path: Path):
        from typer.testing import CliRunner
        from practical_chat_agent.app.main import app

        plan_path = _write_plan(tmp_path)
        output_path = tmp_path / "cli_feedback.json"

        runner = CliRunner()
        result = runner.invoke(app, [
            "chat-reply-feedback",
            "--plan", str(plan_path),
            "--candidate-rank", "1",
            "--action", "accept",
            "--output", str(output_path),
        ])
        assert result.exit_code == 0
        output = json.loads(result.output)
        assert output["action"] == "accept"
        assert output["feedback_id"]

        # Privacy: output JSON should not contain draft text
        assert "synthetic draft text candidate one" not in result.output

    def test_cli_edit(self, tmp_path: Path):
        from typer.testing import CliRunner
        from practical_chat_agent.app.main import app

        plan_path = _write_plan(tmp_path)
        output_path = tmp_path / "cli_feedback.json"

        runner = CliRunner()
        result = runner.invoke(app, [
            "chat-reply-feedback",
            "--plan", str(plan_path),
            "--candidate-rank", "2",
            "--action", "edit",
            "--edited-text", "cli edited text marker abc123def",
            "--output", str(output_path),
        ])
        assert result.exit_code == 0
        output = json.loads(result.output)
        assert output["action"] == "edit"

        # Privacy: edited text must not appear in stdout
        assert "abc123def" not in result.output

    def test_cli_invalid_rank(self, tmp_path: Path):
        from typer.testing import CliRunner
        from practical_chat_agent.app.main import app

        plan_path = _write_plan(tmp_path)
        output_path = tmp_path / "cli_feedback.json"

        runner = CliRunner()
        result = runner.invoke(app, [
            "chat-reply-feedback",
            "--plan", str(plan_path),
            "--candidate-rank", "99",
            "--action", "accept",
            "--output", str(output_path),
        ])
        assert result.exit_code != 0


class TestCLIValidateRegression:
    """End-to-end CLI regression for chat-reply-feedback-validate."""

    def test_cli_good_log(self, tmp_path: Path):
        from typer.testing import CliRunner
        from practical_chat_agent.app.main import app

        plan_path = _write_plan(tmp_path)
        records = [
            _make_record(action="accept", source_plan_path=str(plan_path)),
            _make_record(action="edit", edited_text="syn", source_plan_path=str(plan_path)),
        ]
        log_path = _write_feedback_log(tmp_path, records)

        runner = CliRunner()
        result = runner.invoke(app, [
            "chat-reply-feedback-validate",
            "--input", str(log_path),
        ])
        assert result.exit_code == 0
        output = json.loads(result.output)
        assert output["is_readable"] is True
        assert output["valid_record_count"] == 2
        assert output["invalid_record_count"] == 0

    def test_cli_corrupted_log(self, tmp_path: Path):
        from typer.testing import CliRunner
        from practical_chat_agent.app.main import app

        bad_log = tmp_path / "corrupted.json"
        bad_log.write_text("{{invalid", encoding="utf-8")

        runner = CliRunner()
        result = runner.invoke(app, [
            "chat-reply-feedback-validate",
            "--input", str(bad_log),
        ])
        assert result.exit_code == 1
        output = json.loads(result.output)
        assert output["is_readable"] is False
        assert output["corrupted_input_count"] == 1


class TestCLISummarizeRegression:
    """End-to-end CLI regression for chat-reply-feedback-summary."""

    def test_cli_summary(self, tmp_path: Path):
        from typer.testing import CliRunner
        from practical_chat_agent.app.main import app

        records = [
            _make_record(action="accept"),
            _make_record(action="reject", priority_rank=2, candidate_id="replycand_test_002"),
        ]
        log_path = _write_feedback_log(tmp_path, records)

        runner = CliRunner()
        result = runner.invoke(app, [
            "chat-reply-feedback-summary",
            "--input", str(log_path),
        ])
        assert result.exit_code == 0
        output = json.loads(result.output)
        assert output["is_readable"] is True
        assert output["total_records"] == 2
        assert output["counts_by_action"]["accept"] == 1
        assert output["counts_by_action"]["reject"] == 1

    def test_cli_corrupted_summary(self, tmp_path: Path):
        from typer.testing import CliRunner
        from practical_chat_agent.app.main import app

        bad_log = tmp_path / "bad.json"
        bad_log.write_text("not json", encoding="utf-8")

        runner = CliRunner()
        result = runner.invoke(app, [
            "chat-reply-feedback-summary",
            "--input", str(bad_log),
        ])
        assert result.exit_code == 1

    def test_cli_summary_with_output_file(self, tmp_path: Path):
        from typer.testing import CliRunner
        from practical_chat_agent.app.main import app

        records = [_make_record(action="accept")]
        log_path = _write_feedback_log(tmp_path, records)
        output_file = tmp_path / "summary_output.json"

        runner = CliRunner()
        result = runner.invoke(app, [
            "chat-reply-feedback-summary",
            "--input", str(log_path),
            "--output", str(output_file),
        ])
        assert result.exit_code == 0
        assert output_file.exists()
        file_data = json.loads(output_file.read_text(encoding="utf-8"))
        assert file_data["total_records"] == 1
