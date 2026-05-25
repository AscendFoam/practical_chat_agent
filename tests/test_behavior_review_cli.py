"""Tests for CandidateAction review CLI (T213)."""

from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from practical_chat_agent.app.main import app
from practical_chat_agent.core.models import (
    CandidateAction,
    CandidateActionPayload,
    DistilledArtifactReviewMetadata,
    ReplyPlanContextRef,
)


def _review_metadata() -> DistilledArtifactReviewMetadata:
    return DistilledArtifactReviewMetadata(
        review_state="pending_human_review",
        reviewed_by_human=False,
        last_decision=None,
        decision_notes=[],
        history=[],
    )


def _candidate() -> CandidateAction:
    return CandidateAction(
        contact_id="contact_cli",
        user_id="user_cli",
        action_type="relationship_check_in_draft",
        title="Review a low-pressure check-in",
        rationale="Synthetic candidate for CLI testing.",
        supporting_context_refs=[
            ReplyPlanContextRef(
                ref_type="policy_boundary",
                ref_id="ref_cli_001",
                note="synthetic review-safe ref",
            ),
        ],
        payload=CandidateActionPayload(
            safe_summary="Review-safe summary.",
            draft_text="Review-only draft: keep it optional.",
            metadata={"rule_id": "relationship_check_in_draft"},
        ),
        review_metadata=_review_metadata(),
    )


def _write_candidate(tmp_path: Path) -> Path:
    path = tmp_path / "candidate.json"
    path.write_text(_candidate().model_dump_json(indent=2), encoding="utf-8")
    return path


class TestCandidateActionReviewCLI:
    def test_cli_approve_candidate(self, tmp_path: Path) -> None:
        input_path = _write_candidate(tmp_path)
        output_path = tmp_path / "reviewed.json"

        runner = CliRunner()
        result = runner.invoke(
            app,
            [
                "chat-behavior-review-action",
                "--input",
                str(input_path),
                "--output",
                str(output_path),
                "--decision",
                "approve",
                "--reviewer",
                "reviewer_001",
                "--note",
                "safe review note",
            ],
        )

        assert result.exit_code == 0
        safe_stdout = json.loads(result.output)
        assert safe_stdout["action"] == "review"
        assert safe_stdout["decision"] == "approve"
        assert safe_stdout["action_type"] == "relationship_check_in_draft"
        assert safe_stdout["status"] == "approved"
        assert safe_stdout["review_metadata"]["review_state"] == "reviewed"
        assert safe_stdout["review_metadata"]["history_count"] == 1
        assert "Review-only draft" not in result.output

        reviewed = CandidateAction.model_validate_json(output_path.read_text(encoding="utf-8"))
        assert reviewed.status == "approved"
        assert reviewed.review_metadata.last_reviewer_id == "reviewer_001"
        assert reviewed.payload.draft_text == "Review-only draft: keep it optional."

    def test_cli_reject_invalid_json(self, tmp_path: Path) -> None:
        input_path = tmp_path / "bad.json"
        input_path.write_text("{not valid json", encoding="utf-8")

        runner = CliRunner()
        result = runner.invoke(
            app,
            [
                "chat-behavior-review-action",
                "--input",
                str(input_path),
                "--decision",
                "approve",
                "--reviewer",
                "reviewer_001",
            ],
        )

        assert result.exit_code != 0
        assert "Invalid CandidateAction JSON" in result.output

    def test_cli_reject_missing_input(self, tmp_path: Path) -> None:
        input_path = tmp_path / "missing.json"

        runner = CliRunner()
        result = runner.invoke(
            app,
            [
                "chat-behavior-review-action",
                "--input",
                str(input_path),
                "--decision",
                "approve",
                "--reviewer",
                "reviewer_001",
            ],
        )

        assert result.exit_code != 0
        assert "does not exist" in result.output or "No such file" in result.output

    def test_cli_reject_invalid_decision(self, tmp_path: Path) -> None:
        input_path = _write_candidate(tmp_path)

        runner = CliRunner()
        result = runner.invoke(
            app,
            [
                "chat-behavior-review-action",
                "--input",
                str(input_path),
                "--decision",
                "send",
                "--reviewer",
                "reviewer_001",
            ],
        )

        assert result.exit_code != 0
        assert "Invalid decision" in result.output

