"""Synthetic integration tests for T164 Approved Patch Compact Context."""
from __future__ import annotations

import json
import tempfile
from datetime import datetime, timezone
from pathlib import Path

import pytest

from practical_chat_agent.core.models import (
    ApprovedPatchBrief,
    ApprovedPatchContext,
)
from practical_chat_agent.services.feedback import ApprovedPatchContextService


NOW = datetime.now(timezone.utc).isoformat()


def _approved_patch_data(patch_id="patch_approved_1", contact_id="contact_x"):
    return {
        "schema_version": "preference_patch_candidate_v1",
        "patch_id": patch_id,
        "contact_id": contact_id,
        "patch_type": "tone_preference",
        "instruction_scope": "per_contact",
        "claim": "Contact prefers warm tone.",
        "behavior_instruction": "Use a warm but not overly casual tone.",
        "rationale_summary": "Based on 3 feedback records.",
        "supporting_feedback_ids": ["fb_1", "fb_2", "fb_3"],
        "supporting_cluster_ids": ["cluster_abc123"],
        "positive_examples": [],
        "negative_examples": [],
        "affected_candidate_types": ["warm_casual"],
        "status": "approved",
        "confidence": 0.6,
        "sensitivity": "low",
        "review_metadata": {
            "review_state": "reviewed",
            "reviewed_by_human": True,
            "last_decision": "approved",
            "last_reviewed_at": NOW,
            "last_reviewer_id": "reviewer_1",
            "last_reviewer_name": None,
            "evidence_validation_status": "not_run",
            "decision_notes": [],
            "history": [
                {
                    "review_id": "review_xxx",
                    "status": "approved",
                    "reviewer_id": "reviewer_1",
                    "reviewer_name": None,
                    "reviewed_at": NOW,
                    "notes": ["Approved."],
                    "evidence_validation_status": "not_run",
                }
            ],
        },
        "created_at": NOW,
        "updated_at": NOW,
    }


def _rejected_patch_data():
    return {
        "schema_version": "preference_patch_candidate_v1",
        "patch_id": "patch_rejected_2",
        "contact_id": "contact_x",
        "patch_type": "length_preference",
        "instruction_scope": "per_contact",
        "claim": "Contact prefers short replies.",
        "behavior_instruction": "Keep replies brief, under 3 lines.",
        "rationale_summary": None,
        "supporting_feedback_ids": ["fb_4", "fb_5"],
        "supporting_cluster_ids": [],
        "positive_examples": [],
        "negative_examples": [],
        "affected_candidate_types": [],
        "status": "rejected",
        "confidence": 0.45,
        "sensitivity": "low",
        "review_metadata": {
            "review_state": "reviewed",
            "reviewed_by_human": True,
            "last_decision": "rejected",
            "last_reviewed_at": NOW,
            "last_reviewer_id": "reviewer_1",
            "last_reviewer_name": None,
            "evidence_validation_status": "not_run",
            "decision_notes": [],
            "history": [],
        },
        "created_at": NOW,
        "updated_at": NOW,
    }


def _candidate_patch_data():
    return {
        "schema_version": "preference_patch_candidate_v1",
        "patch_id": "patch_candidate_3",
        "contact_id": "contact_x",
        "patch_type": "question_style",
        "instruction_scope": "per_contact",
        "claim": "Contact prefers open-ended questions.",
        "behavior_instruction": "Use open-ended questions.",
        "rationale_summary": None,
        "supporting_feedback_ids": ["fb_6"],
        "supporting_cluster_ids": [],
        "positive_examples": [],
        "negative_examples": [],
        "affected_candidate_types": [],
        "status": "candidate",
        "confidence": 0.3,
        "sensitivity": "low",
        "review_metadata": {
            "review_state": "pending_human_review",
            "reviewed_by_human": False,
            "last_decision": None,
            "last_reviewed_at": None,
            "last_reviewer_id": None,
            "last_reviewer_name": None,
            "evidence_validation_status": "not_run",
            "decision_notes": [],
            "history": [],
        },
        "created_at": NOW,
        "updated_at": NOW,
    }


def _make_report(candidates):
    return {
        "schema_version": "patch_proposal_v1",
        "generated_at": NOW,
        "input_path": "private/synthetic/cluster_report.json",
        "candidate_count": len(candidates),
        "skipped_cluster_count": 0,
        "candidates": candidates,
        "skipped_clusters": [],
    }


def _write_report(tmpdir, report):
    rp = Path(tmpdir) / "proposal_report.json"
    rp.write_text(json.dumps(report), encoding="utf-8")
    return rp


class TestNotConfigured:
    def test_default_status(self):
        ctx = ApprovedPatchContext()
        assert ctx.status == "not_configured"
        assert ctx.patches == []

    def test_store_path_missing(self):
        svc = ApprovedPatchContextService()
        result = svc.load_approved_patches(
            report_path=Path("/nonexistent/path.json"), contact_id="contact_x"
        )
        assert result.status == "store_path_missing"


class TestApprovedPatchLoading:
    def test_approved_patch_loaded_rejected_and_candidate_excluded(self):
        svc = ApprovedPatchContextService()
        report = _make_report([
            {"patch": _approved_patch_data(), "source_cluster_id": "cluster_abc123"},
            {"patch": _rejected_patch_data(), "source_cluster_id": "cluster_def456"},
            {"patch": _candidate_patch_data(), "source_cluster_id": "cluster_ghi789"},
        ])
        with tempfile.TemporaryDirectory() as tmpdir:
            rp = _write_report(tmpdir, report)
            result = svc.load_approved_patches(report_path=rp, contact_id="contact_x")
        assert result.status == "loaded"
        assert len(result.patches) == 1
        brief = result.patches[0]
        assert brief.patch_id == "patch_approved_1"
        assert brief.patch_type == "tone_preference"
        assert brief.sensitivity == "low"
        assert brief.supporting_feedback_count == 3
        assert brief.supporting_cluster_ids == ["cluster_abc123"]
        assert len(brief.compact_instruction) > 0
        assert "warm" in brief.compact_instruction.lower()

    def test_brief_excludes_review_history(self):
        svc = ApprovedPatchContextService()
        report = _make_report([
            {"patch": _approved_patch_data(), "source_cluster_id": "c1"},
        ])
        with tempfile.TemporaryDirectory() as tmpdir:
            rp = _write_report(tmpdir, report)
            result = svc.load_approved_patches(report_path=rp, contact_id="contact_x")
        brief = result.patches[0]
        # The brief should NOT have review_metadata or history fields
        assert not hasattr(brief, "review_metadata")
        assert not hasattr(brief, "claim")


class TestExclusionFilters:
    def test_wrong_contact_id_excluded(self):
        svc = ApprovedPatchContextService()
        report = _make_report([
            {"patch": _approved_patch_data(), "source_cluster_id": "c1"},
        ])
        with tempfile.TemporaryDirectory() as tmpdir:
            rp = _write_report(tmpdir, report)
            result = svc.load_approved_patches(report_path=rp, contact_id="contact_y")
        assert result.status == "no_runtime_ready_records"

    def test_no_runtime_ready_when_only_rejected(self):
        svc = ApprovedPatchContextService()
        report = _make_report([
            {"patch": _rejected_patch_data(), "source_cluster_id": "c1"},
        ])
        with tempfile.TemporaryDirectory() as tmpdir:
            rp = _write_report(tmpdir, report)
            result = svc.load_approved_patches(report_path=rp, contact_id="contact_x")
        assert result.status == "no_runtime_ready_records"
        assert result.patches == []

    def test_approved_but_not_human_reviewed_excluded(self):
        """A patch with status=approved but reviewed_by_human=False is not runtime-ready."""
        data = _approved_patch_data()
        data["review_metadata"]["reviewed_by_human"] = False
        data["review_metadata"]["last_decision"] = "approved"
        svc = ApprovedPatchContextService()
        report = _make_report([
            {"patch": data, "source_cluster_id": "c1"},
        ])
        with tempfile.TemporaryDirectory() as tmpdir:
            rp = _write_report(tmpdir, report)
            result = svc.load_approved_patches(report_path=rp, contact_id="contact_x")
        assert result.status == "no_runtime_ready_records"


class TestErrorHandling:
    def test_invalid_schema_version(self):
        svc = ApprovedPatchContextService()
        with tempfile.TemporaryDirectory() as tmpdir:
            rp = Path(tmpdir) / "bad.json"
            rp.write_text(json.dumps({"schema_version": "wrong", "candidates": []}), encoding="utf-8")
            result = svc.load_approved_patches(report_path=rp, contact_id="contact_x")
        assert result.status == "store_path_missing"

    def test_invalid_json(self):
        svc = ApprovedPatchContextService()
        with tempfile.TemporaryDirectory() as tmpdir:
            rp = Path(tmpdir) / "bad.json"
            rp.write_text("not json", encoding="utf-8")
            result = svc.load_approved_patches(report_path=rp, contact_id="contact_x")
        assert result.status == "store_path_missing"

    def test_bad_patch_data_handled_gracefully(self):
        svc = ApprovedPatchContextService()
        report = {
            "schema_version": "patch_proposal_v1",
            "generated_at": NOW,
            "candidates": [
                {"patch": {"patch_id": "bad", "contact_id": "", "patch_type": "invalid"}, "source_cluster_id": "c1"},
            ],
            "skipped_clusters": [],
        }
        with tempfile.TemporaryDirectory() as tmpdir:
            rp = _write_report(tmpdir, report)
            result = svc.load_approved_patches(report_path=rp, contact_id="contact_x")
        assert result.status in ("no_runtime_ready_records", "store_path_missing")


class TestCompactInstruction:
    def test_truncation_at_160_chars(self):
        long_instr = "Be " + "very " * 100 + "careful."
        svc = ApprovedPatchContextService()
        truncated = svc._compact_text(long_instr, max_length=160)
        assert len(truncated) <= 160
        assert truncated.endswith("...")

    def test_short_text_not_truncated(self):
        short = "Keep it short."
        svc = ApprovedPatchContextService()
        result = svc._compact_text(short, max_length=160)
        assert result == short

    def test_whitespace_normalized(self):
        messy = "   spaces   everywhere    "
        svc = ApprovedPatchContextService()
        result = svc._compact_text(messy, max_length=160)
        assert result == "spaces everywhere"
