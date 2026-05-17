from __future__ import annotations

import json
from pathlib import Path

from pydantic import ValidationError

from practical_chat_agent.core.models import (
    ReplyFeedbackAction,
    ReplyFeedbackLog,
    ReplyFeedbackRecord,
    ReplyPlan,
)


class FeedbackError(Exception):
    pass


class FeedbackService:
    def record_feedback(
        self,
        *,
        plan_path: Path,
        candidate_rank: int,
        action: ReplyFeedbackAction,
        output_path: Path,
        user_note: str | None = None,
        edited_text: str | None = None,
        boundary_label: str | None = None,
        boundary_note: str | None = None,
    ) -> dict:
        plan = self._load_plan(plan_path)
        candidate = self._resolve_candidate(plan, candidate_rank)

        if action == "edit" and not edited_text:
            raise FeedbackError("--edited-text is required when action is 'edit'.")
        if action == "boundary" and not boundary_label and not boundary_note:
            raise FeedbackError(
                "At least one of --boundary-label or --boundary-note is required when action is 'boundary'."
            )

        record = ReplyFeedbackRecord(
            contact_id=plan.contact_id,
            reply_plan_id=plan.source_context.approved_contact_skill_record_id,
            candidate_id=candidate.candidate_id,
            priority_rank=candidate.priority_rank,
            action=action,
            user_note=user_note,
            edited_text=edited_text if action == "edit" else None,
            boundary_label=boundary_label if action == "boundary" else None,
            boundary_note=boundary_note if action == "boundary" else None,
            source_plan_path=str(plan_path),
        )

        self._append_record(output_path, record)

        return {
            "plan_path": str(plan_path),
            "output_path": str(output_path),
            "contact_id": plan.contact_id,
            "candidate_id": candidate.candidate_id,
            "priority_rank": candidate.priority_rank,
            "action": action,
            "feedback_id": record.feedback_id,
            "total_records": self._count_records(output_path),
        }

    def _load_plan(self, plan_path: Path) -> ReplyPlan:
        if not plan_path.exists():
            raise FeedbackError(f"ReplyPlan file not found: {plan_path}")
        try:
            raw = plan_path.read_text(encoding="utf-8")
        except OSError as exc:
            raise FeedbackError(f"Unable to read ReplyPlan file: {exc}") from exc
        try:
            return ReplyPlan.model_validate_json(raw)
        except ValidationError as exc:
            raise FeedbackError(f"Invalid ReplyPlan JSON: {exc}") from exc

    def _resolve_candidate(self, plan: ReplyPlan, candidate_rank: int):
        for candidate in plan.candidates:
            if candidate.priority_rank == candidate_rank:
                return candidate
        valid_ranks = sorted(c.priority_rank for c in plan.candidates)
        raise FeedbackError(
            f"No candidate with priority_rank={candidate_rank}. "
            f"Valid ranks: {valid_ranks}"
        )

    def _append_record(self, output_path: Path, record: ReplyFeedbackRecord) -> None:
        output_path.parent.mkdir(parents=True, exist_ok=True)

        log: ReplyFeedbackLog
        if output_path.exists():
            try:
                existing = json.loads(output_path.read_text(encoding="utf-8"))
                log = ReplyFeedbackLog.model_validate(existing)
            except (OSError, json.JSONDecodeError, ValidationError):
                log = ReplyFeedbackLog()
        else:
            log = ReplyFeedbackLog()

        log.records.append(record)
        output_path.write_text(
            json.dumps(log.model_dump(mode="json"), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def _count_records(self, output_path: Path) -> int:
        if not output_path.exists():
            return 0
        try:
            existing = json.loads(output_path.read_text(encoding="utf-8"))
            log = ReplyFeedbackLog.model_validate(existing)
            return len(log.records)
        except (OSError, json.JSONDecodeError, ValidationError):
            return 0
