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


class FeedbackValidationService:
    """Read-only validator for T140 feedback logs."""

    def validate(self, *, input_path: Path, strict: bool = False) -> dict:
        report = self._init_report(input_path, strict)

        if not input_path.exists():
            report["corrupted_reason"] = "file_not_found"
            report["corrupted_input_count"] = 1
            return report

        if not self._is_private_path(input_path):
            report["privacy_warnings"].append(
                "W_PRIVACY_INPUT: input path is outside expected private/ directory"
            )

        try:
            raw_text = input_path.read_text(encoding="utf-8")
        except OSError as exc:
            report["corrupted_reason"] = f"read_error: {exc}"
            report["corrupted_input_count"] = 1
            return report

        try:
            data = json.loads(raw_text)
        except json.JSONDecodeError as exc:
            report["corrupted_reason"] = (
                f"json_decode_error: line {exc.lineno} column {exc.colno}"
            )
            report["corrupted_input_count"] = 1
            return report

        try:
            log = ReplyFeedbackLog.model_validate(data)
        except ValidationError as exc:
            report["corrupted_reason"] = (
                f"schema_error: {exc.error_count()} validation failure(s)"
            )
            report["corrupted_input_count"] = 1
            return report

        report["is_readable"] = True
        report["total_records"] = len(log.records)

        for record in log.records:
            rec_result = self._validate_record(record, input_path, report)
            report["record_results"].append(rec_result)
            report["counts_by_action"][record.action] = (
                report["counts_by_action"].get(record.action, 0) + 1
            )
            if rec_result["is_valid"]:
                report["valid_record_count"] += 1
            else:
                report["invalid_record_count"] += 1

        return report

    def _init_report(self, input_path: Path, strict: bool) -> dict:
        return {
            "input_path": str(input_path),
            "is_readable": False,
            "corrupted_reason": None,
            "corrupted_input_count": 0,
            "total_records": 0,
            "valid_record_count": 0,
            "invalid_record_count": 0,
            "counts_by_action": {},
            "missing_plan_count": 0,
            "missing_candidate_count": 0,
            "contact_mismatch_count": 0,
            "edit_without_text_count": 0,
            "boundary_without_details_count": 0,
            "privacy_warnings": [],
            "record_results": [],
            "strict_mode": strict,
        }

    def _is_private_path(self, path: Path) -> bool:
        try:
            resolved = path.resolve()
            return any(p.casefold() == "private" for p in resolved.parts)
        except (OSError, ValueError):
            return False

    def _resolve_plan_path(self, source_plan_path: str, log_dir: Path) -> Path | None:
        candidate = Path(source_plan_path)
        if candidate.is_absolute():
            return candidate if candidate.exists() else None
        if candidate.exists():
            return candidate.resolve()
        resolved = (log_dir / candidate).resolve()
        return resolved if resolved.exists() else None

    def _load_plan_safe(self, plan_path: Path) -> ReplyPlan | None:
        try:
            raw = plan_path.read_text(encoding="utf-8")
            return ReplyPlan.model_validate_json(raw)
        except (OSError, json.JSONDecodeError, ValidationError):
            return None

    def _validate_record(
        self, record: ReplyFeedbackRecord, input_path: Path, report: dict,
    ) -> dict:
        issues: list[str] = []

        if record.action == "edit" and not record.edited_text:
            issues.append("edit_without_text")
            report["edit_without_text_count"] += 1

        if record.action == "boundary":
            if not record.boundary_label and not record.boundary_note:
                issues.append("boundary_without_details")
                report["boundary_without_details_count"] += 1

        if record.source_plan_path:
            resolved = self._resolve_plan_path(
                record.source_plan_path, input_path.parent,
            )

            if resolved is not None and not self._is_private_path(resolved):
                report["privacy_warnings"].append(
                    f"W_PRIVACY_REF: source_plan_path for {record.feedback_id} "
                    "resolves outside private/"
                )

            if resolved is None:
                issues.append("missing_plan")
                report["missing_plan_count"] += 1
            else:
                plan = self._load_plan_safe(resolved)
                if plan is None:
                    issues.append("missing_plan")
                    report["missing_plan_count"] += 1
                else:
                    found = any(
                        c.candidate_id == record.candidate_id
                        and c.priority_rank == record.priority_rank
                        for c in plan.candidates
                    )
                    if not found:
                        issues.append("missing_candidate")
                        report["missing_candidate_count"] += 1

                    if plan.contact_id != record.contact_id:
                        issues.append("contact_mismatch")
                        report["contact_mismatch_count"] += 1

        return {
            "feedback_id": record.feedback_id,
            "candidate_id": record.candidate_id,
            "priority_rank": record.priority_rank,
            "action": record.action,
            "is_valid": len(issues) == 0,
            "issues": issues,
        }
