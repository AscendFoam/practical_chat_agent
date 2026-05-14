from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from practical_chat_agent.core.models import ContactSkillStoreRecord, MemoryFactStoreRecord
from practical_chat_agent.services.contact_skill import ContactSkillFileStoreService


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class EvidenceValidationError(ValueError):
    """Raised when evidence validation inputs or outputs are invalid."""


@dataclass(frozen=True)
class ValidationTargets:
    memory_path: Path | None = None
    contact_skill_path: Path | None = None


@dataclass(frozen=True)
class EvidenceValidationResult:
    output_path: Path | None
    report: dict[str, Any]


class EvidenceValidationService:
    """Validate evidence refs for offline store artifacts under private/distilled."""

    REPORT_FILENAME = "evidence_validation_report.json"
    NORMALIZED_EVENTS_FILENAME = "normalized_events.jsonl"
    CHUNKS_FILENAME = "chunks.jsonl"
    CHUNK_SUMMARIES_FILENAME = "chunk_summaries.jsonl"
    MEMORY_FACTS_FILENAME = "memory_facts.jsonl"
    CONTACT_SKILL_CANDIDATE_FILENAME = "contact_skill.candidate.json"

    def __init__(self) -> None:
        self._repo_root = Path.cwd().resolve()
        self._private_distilled_root = (self._repo_root / "private" / "distilled").resolve()
        self._store_service = ContactSkillFileStoreService()

    def validate_evidence(
        self,
        *,
        input_path: Path,
        output_path: Path | None,
        dry_run: bool = False,
    ) -> EvidenceValidationResult:
        resolved_input = self._resolve_existing_path(input_path)
        self._ensure_within_root(
            candidate=resolved_input,
            root=self._private_distilled_root,
            error_message="Input must stay within private/distilled.",
        )
        run_dir = self._resolve_run_dir(candidate=resolved_input)
        anchor_dir = resolved_input if resolved_input.is_dir() else resolved_input.parent
        targets = self._resolve_validation_targets(
            resolved_input=resolved_input,
            anchor_dir=anchor_dir,
        )
        if targets.memory_path is None and targets.contact_skill_path is None:
            raise EvidenceValidationError(
                "Input must contain or point to memory_fact_store.json, memory_facts.jsonl, "
                "contact_skill_store.json, or contact_skill.candidate.json.",
            )

        memory_store = (
            self._store_service.load_memory_store(input_path=targets.memory_path)
            if targets.memory_path is not None
            else None
        )
        contact_skill_store = (
            self._store_service.load_contact_skill_store(input_path=targets.contact_skill_path)
            if targets.contact_skill_path is not None
            else None
        )

        evidence_index = self._build_evidence_index(
            run_dir=run_dir,
            memory_path=targets.memory_path,
            memory_store=memory_store,
            contact_skill_path=targets.contact_skill_path,
            contact_skill_store=contact_skill_store,
        )

        record_results: list[dict[str, Any]] = []
        if memory_store is not None:
            for record in memory_store.records:
                record_results.append(
                    self._validate_memory_record(
                        record=record,
                        evidence_index=evidence_index,
                    ),
                )
        if contact_skill_store is not None:
            for record in contact_skill_store.records:
                record_results.append(
                    self._validate_contact_skill_record(
                        record=record,
                        evidence_index=evidence_index,
                    ),
                )
        if not record_results:
            raise EvidenceValidationError("No store records were available for evidence validation.")

        report = self._build_report(
            resolved_input=resolved_input,
            run_dir=run_dir,
            targets=targets,
            evidence_index=evidence_index,
            record_results=record_results,
            dry_run=dry_run,
        )

        resolved_output: Path | None = None
        if not dry_run:
            resolved_output = self._resolve_output_path(
                output_path=output_path,
                run_dir=run_dir,
            )
            report["output_path"] = self._safe_relative_path(resolved_output)
            resolved_output.parent.mkdir(parents=True, exist_ok=True)
            self._write_json(output_path=resolved_output, payload=report)

        return EvidenceValidationResult(output_path=resolved_output, report=report)

    def _validate_memory_record(
        self,
        *,
        record: MemoryFactStoreRecord,
        evidence_index: dict[str, Any],
    ) -> dict[str, Any]:
        return self._validate_record_payload(
            record_id=record.record_id,
            artifact_type=record.artifact_type,
            artifact_id=record.memory_fact.memory_id,
            status=record.memory_fact.status,
            payload=record.memory_fact.model_dump(mode="json"),
            evidence_index=evidence_index,
            source_metadata=record.source_metadata.model_dump(mode="json"),
            review_metadata=record.review_metadata.model_dump(mode="json"),
            store_runtime_gate_ready=record.is_runtime_ready(),
        )

    def _validate_contact_skill_record(
        self,
        *,
        record: ContactSkillStoreRecord,
        evidence_index: dict[str, Any],
    ) -> dict[str, Any]:
        artifact_payload = record.contact_skill.model_dump(mode="json")
        artifact_id = self._extract_contact_skill_ids(artifact_payload)
        resolved_artifact_id = artifact_id[0] if artifact_id else record.contact_skill.contact_id
        return self._validate_record_payload(
            record_id=record.record_id,
            artifact_type=record.artifact_type,
            artifact_id=resolved_artifact_id,
            status=record.contact_skill.status,
            payload=artifact_payload,
            evidence_index=evidence_index,
            source_metadata=record.source_metadata.model_dump(mode="json"),
            review_metadata=record.review_metadata.model_dump(mode="json"),
            store_runtime_gate_ready=record.is_runtime_ready(),
        )

    def _validate_record_payload(
        self,
        *,
        record_id: str,
        artifact_type: str,
        artifact_id: str,
        status: str,
        payload: dict[str, Any],
        evidence_index: dict[str, Any],
        source_metadata: dict[str, Any],
        review_metadata: dict[str, Any],
        store_runtime_gate_ready: bool,
    ) -> dict[str, Any]:
        ref_locations = self._collect_evidence_ref_locations(value=payload)
        checked_refs = self._unique_strings(
            ref
            for location in ref_locations
            for ref in location["refs"]
        )
        missing_refs = [ref for ref in checked_refs if ref not in evidence_index["refs"]]

        for location in ref_locations:
            location["missing_refs"] = [ref for ref in location["refs"] if ref in missing_refs]

        approval_block_reasons: list[str] = []
        runtime_block_reasons: list[str] = []
        if not checked_refs:
            approval_block_reasons.append("no_evidence_refs_found")
            runtime_block_reasons.append("no_evidence_refs_found")
        if missing_refs:
            approval_block_reasons.append("missing_evidence_refs")
            runtime_block_reasons.append("missing_evidence_refs")
        if status == "candidate":
            approval_block_reasons.append("candidate_not_approval_ready_by_default")
            runtime_block_reasons.append("candidate_not_runtime_ready")
        elif status in {"rejected", "frozen", "archived"}:
            approval_block_reasons.append(f"status_{status}_not_approval_ready")
            runtime_block_reasons.append(f"status_{status}_never_runtime_ready")
        elif status == "approved" and not store_runtime_gate_ready:
            runtime_block_reasons.append("human_review_runtime_gate_not_satisfied")

        approval_block_reasons = self._unique_strings(approval_block_reasons)
        runtime_block_reasons = self._unique_strings(runtime_block_reasons)
        approval_ready = status == "approved" and not approval_block_reasons
        runtime_ready = status == "approved" and not missing_refs and store_runtime_gate_ready

        return {
            "record_id": record_id,
            "artifact_type": artifact_type,
            "artifact_id": artifact_id,
            "status": status,
            "checked_refs": checked_refs,
            "missing_refs": missing_refs,
            "checked_ref_count": len(checked_refs),
            "missing_ref_count": len(missing_refs),
            "ref_locations": ref_locations,
            "ref_sources": {
                ref: evidence_index["ref_sources"].get(ref, [])
                for ref in checked_refs
            },
            "provenance": {
                "source_run_id": source_metadata.get("source_run_id"),
                "source_artifact_path": source_metadata.get("source_artifact_path"),
                "review_artifact_path": source_metadata.get("review_artifact_path"),
                "source_chunk_ids": source_metadata.get("source_chunk_ids", []),
                "source_memory_ids": source_metadata.get("source_memory_ids", []),
                "source_event_ids": source_metadata.get("source_event_ids", []),
            },
            "review_metadata_snapshot": {
                "review_state": review_metadata.get("review_state"),
                "reviewed_by_human": review_metadata.get("reviewed_by_human"),
                "last_decision": review_metadata.get("last_decision"),
                "last_reviewed_at": review_metadata.get("last_reviewed_at"),
                "last_reviewer_id": review_metadata.get("last_reviewer_id"),
                "last_reviewer_name": review_metadata.get("last_reviewer_name"),
                "evidence_validation_status": review_metadata.get("evidence_validation_status"),
            },
            "store_runtime_gate_ready": store_runtime_gate_ready,
            "approval_ready_after_validation": approval_ready,
            "runtime_ready_after_validation": runtime_ready,
            "approval_blocked": not approval_ready,
            "runtime_blocked": not runtime_ready,
            "approval_block_reasons": approval_block_reasons,
            "runtime_block_reasons": runtime_block_reasons,
        }

    def _build_report(
        self,
        *,
        resolved_input: Path,
        run_dir: Path,
        targets: ValidationTargets,
        evidence_index: dict[str, Any],
        record_results: list[dict[str, Any]],
        dry_run: bool,
    ) -> dict[str, Any]:
        missing_record_count = sum(1 for result in record_results if result["missing_refs"])
        missing_ref_count = sum(len(result["missing_refs"]) for result in record_results)
        records_without_evidence_refs = sum(1 for result in record_results if result["checked_ref_count"] == 0)
        approval_ready_count = sum(1 for result in record_results if result["approval_ready_after_validation"])
        runtime_ready_count = sum(1 for result in record_results if result["runtime_ready_after_validation"])
        approval_blocked_count = sum(1 for result in record_results if result["approval_blocked"])
        runtime_blocked_count = sum(1 for result in record_results if result["runtime_blocked"])
        memory_record_count = sum(1 for result in record_results if result["artifact_type"] == "memory_fact")
        contact_skill_record_count = sum(1 for result in record_results if result["artifact_type"] == "contact_skill")
        candidate_record_count = sum(1 for result in record_results if result["status"] == "candidate")
        approved_record_count = sum(1 for result in record_results if result["status"] == "approved")
        validation_failed = missing_ref_count > 0 or records_without_evidence_refs > 0

        return {
            "schema_version": "evidence_validation_report_v1",
            "generated_at": utc_now().isoformat().replace("+00:00", "Z"),
            "input_path": self._safe_relative_path(resolved_input),
            "run_dir": self._safe_relative_path(run_dir),
            "output_path": None,
            "dry_run": dry_run,
            "validated_inputs": [
                item
                for item in [
                    self._build_target_summary(
                        artifact_type="memory_store",
                        path=targets.memory_path,
                    ),
                    self._build_target_summary(
                        artifact_type="contact_skill_store",
                        path=targets.contact_skill_path,
                    ),
                ]
                if item is not None
            ],
            "available_evidence_artifacts": evidence_index["artifacts"],
            "missing_optional_evidence_artifacts": evidence_index["missing_artifacts"],
            "indexed_ref_counts": {
                **evidence_index["counts"],
                "total_refs": len(evidence_index["refs"]),
            },
            "summary": {
                "evidence_validation_status": "failed" if validation_failed else "passed",
                "validated_record_count": len(record_results),
                "memory_record_count": memory_record_count,
                "contact_skill_record_count": contact_skill_record_count,
                "candidate_record_count": candidate_record_count,
                "approved_record_count": approved_record_count,
                "records_with_missing_refs": missing_record_count,
                "records_without_evidence_refs": records_without_evidence_refs,
                "missing_ref_count": missing_ref_count,
                "approval_ready_records": approval_ready_count,
                "runtime_ready_records": runtime_ready_count,
                "approval_blocked_records": approval_blocked_count,
                "runtime_blocked_records": runtime_blocked_count,
            },
            "records": record_results,
        }

    def _build_evidence_index(
        self,
        *,
        run_dir: Path,
        memory_path: Path | None,
        memory_store: Any,
        contact_skill_path: Path | None,
        contact_skill_store: Any,
    ) -> dict[str, Any]:
        index = {
            "refs": set(),
            "ref_sources": {},
            "counts": {
                "event_ids": 0,
                "chunk_ids": 0,
                "summary_ids": 0,
                "memory_ids": 0,
                "contact_skill_ids": 0,
            },
            "artifacts": [],
            "missing_artifacts": [],
        }

        self._index_normalized_events(run_dir=run_dir, index=index)
        self._index_chunks(run_dir=run_dir, index=index)
        self._index_chunk_summaries(run_dir=run_dir, index=index)
        self._index_memory_facts(run_dir=run_dir, index=index)
        self._index_contact_skill_candidate(run_dir=run_dir, index=index)
        self._index_memory_store_records(
            memory_path=memory_path,
            memory_store=memory_store,
            index=index,
        )
        self._index_contact_skill_store_records(
            contact_skill_path=contact_skill_path,
            contact_skill_store=contact_skill_store,
            index=index,
        )
        return index

    def _index_normalized_events(self, *, run_dir: Path, index: dict[str, Any]) -> None:
        path = run_dir / self.NORMALIZED_EVENTS_FILENAME
        if not path.is_file():
            index["missing_artifacts"].append(self.NORMALIZED_EVENTS_FILENAME)
            return
        rows = self._load_jsonl_objects(path)
        added = 0
        for row in rows:
            if self._add_index_ref(
                index=index,
                ref=row.get("event_id"),
                category="event_ids",
                source=f"{self.NORMALIZED_EVENTS_FILENAME}:event_id",
            ):
                added += 1
        index["artifacts"].append(
            self._build_artifact_summary(
                artifact_type="normalized_events",
                path=path,
                record_count=len(rows),
                indexed_ref_count=added,
            ),
        )

    def _index_chunks(self, *, run_dir: Path, index: dict[str, Any]) -> None:
        path = run_dir / self.CHUNKS_FILENAME
        if not path.is_file():
            index["missing_artifacts"].append(self.CHUNKS_FILENAME)
            return
        rows = self._load_jsonl_objects(path)
        added = 0
        for row in rows:
            if self._add_index_ref(
                index=index,
                ref=row.get("chunk_id"),
                category="chunk_ids",
                source=f"{self.CHUNKS_FILENAME}:chunk_id",
            ):
                added += 1
            for event_id in row.get("event_ids", []):
                if self._add_index_ref(
                    index=index,
                    ref=event_id,
                    category="event_ids",
                    source=f"{self.CHUNKS_FILENAME}:event_ids",
                ):
                    added += 1
        index["artifacts"].append(
            self._build_artifact_summary(
                artifact_type="chunks",
                path=path,
                record_count=len(rows),
                indexed_ref_count=added,
            ),
        )

    def _index_chunk_summaries(self, *, run_dir: Path, index: dict[str, Any]) -> None:
        path = run_dir / self.CHUNK_SUMMARIES_FILENAME
        if not path.is_file():
            index["missing_artifacts"].append(self.CHUNK_SUMMARIES_FILENAME)
            return
        rows = self._load_jsonl_objects(path)
        added = 0
        for row in rows:
            if self._add_index_ref(
                index=index,
                ref=row.get("summary_id"),
                category="summary_ids",
                source=f"{self.CHUNK_SUMMARIES_FILENAME}:summary_id",
            ):
                added += 1
            if self._add_index_ref(
                index=index,
                ref=row.get("chunk_id"),
                category="chunk_ids",
                source=f"{self.CHUNK_SUMMARIES_FILENAME}:chunk_id",
            ):
                added += 1
            for event_id in row.get("event_ids", []):
                if self._add_index_ref(
                    index=index,
                    ref=event_id,
                    category="event_ids",
                    source=f"{self.CHUNK_SUMMARIES_FILENAME}:event_ids",
                ):
                    added += 1
        index["artifacts"].append(
            self._build_artifact_summary(
                artifact_type="chunk_summaries",
                path=path,
                record_count=len(rows),
                indexed_ref_count=added,
            ),
        )

    def _index_memory_facts(self, *, run_dir: Path, index: dict[str, Any]) -> None:
        path = run_dir / self.MEMORY_FACTS_FILENAME
        if not path.is_file():
            index["missing_artifacts"].append(self.MEMORY_FACTS_FILENAME)
            return
        rows = self._load_jsonl_objects(path)
        added = 0
        for row in rows:
            if self._add_index_ref(
                index=index,
                ref=row.get("memory_id"),
                category="memory_ids",
                source=f"{self.MEMORY_FACTS_FILENAME}:memory_id",
            ):
                added += 1
        index["artifacts"].append(
            self._build_artifact_summary(
                artifact_type="memory_facts",
                path=path,
                record_count=len(rows),
                indexed_ref_count=added,
            ),
        )

    def _index_contact_skill_candidate(self, *, run_dir: Path, index: dict[str, Any]) -> None:
        path = run_dir / self.CONTACT_SKILL_CANDIDATE_FILENAME
        if not path.is_file():
            index["missing_artifacts"].append(self.CONTACT_SKILL_CANDIDATE_FILENAME)
            return
        payload = self._read_json_object(path)
        added = 0
        for ref in self._extract_contact_skill_ids(payload):
            if self._add_index_ref(
                index=index,
                ref=ref,
                category="contact_skill_ids",
                source=f"{self.CONTACT_SKILL_CANDIDATE_FILENAME}:id",
            ):
                added += 1
        index["artifacts"].append(
            self._build_artifact_summary(
                artifact_type="contact_skill_candidate",
                path=path,
                record_count=1,
                indexed_ref_count=added,
            ),
        )

    def _index_memory_store_records(
        self,
        *,
        memory_path: Path | None,
        memory_store: Any,
        index: dict[str, Any],
    ) -> None:
        if memory_path is None or memory_store is None:
            return
        added = 0
        for record in memory_store.records:
            if self._add_index_ref(
                index=index,
                ref=record.memory_fact.memory_id,
                category="memory_ids",
                source=f"{memory_path.name}:memory_fact.memory_id",
            ):
                added += 1
        index["artifacts"].append(
            self._build_artifact_summary(
                artifact_type="memory_store_records",
                path=memory_path,
                record_count=len(memory_store.records),
                indexed_ref_count=added,
            ),
        )

    def _index_contact_skill_store_records(
        self,
        *,
        contact_skill_path: Path | None,
        contact_skill_store: Any,
        index: dict[str, Any],
    ) -> None:
        if contact_skill_path is None or contact_skill_store is None:
            return
        added = 0
        for record in contact_skill_store.records:
            payload = record.contact_skill.model_dump(mode="json")
            for ref in self._extract_contact_skill_ids(payload):
                if self._add_index_ref(
                    index=index,
                    ref=ref,
                    category="contact_skill_ids",
                    source=f"{contact_skill_path.name}:contact_skill_id",
                ):
                    added += 1
        index["artifacts"].append(
            self._build_artifact_summary(
                artifact_type="contact_skill_store_records",
                path=contact_skill_path,
                record_count=len(contact_skill_store.records),
                indexed_ref_count=added,
            ),
        )

    def _resolve_validation_targets(
        self,
        *,
        resolved_input: Path,
        anchor_dir: Path,
    ) -> ValidationTargets:
        if resolved_input.is_file():
            if resolved_input.name in {
                self._store_service.MEMORY_STORE_FILENAME,
                self._store_service.MEMORY_FACTS_FILENAME,
            }:
                return ValidationTargets(memory_path=resolved_input)
            if resolved_input.name in {
                self._store_service.CONTACT_SKILL_STORE_FILENAME,
                self._store_service.CONTACT_SKILL_CANDIDATE_FILENAME,
            }:
                return ValidationTargets(contact_skill_path=resolved_input)
            raise EvidenceValidationError(
                f"Unsupported input file for evidence validation: {resolved_input.name}",
            )

        memory_path = self._first_existing_path(
            anchor_dir / self._store_service.MEMORY_STORE_FILENAME,
            anchor_dir / self._store_service.MEMORY_FACTS_FILENAME,
        )
        contact_skill_path = self._first_existing_path(
            anchor_dir / self._store_service.CONTACT_SKILL_STORE_FILENAME,
            anchor_dir / self._store_service.CONTACT_SKILL_CANDIDATE_FILENAME,
        )
        return ValidationTargets(
            memory_path=memory_path,
            contact_skill_path=contact_skill_path,
        )

    def _resolve_existing_path(self, path: Path) -> Path:
        resolved = (self._repo_root / path).resolve() if not path.is_absolute() else path.resolve()
        if not resolved.exists():
            raise EvidenceValidationError(f"Input path does not exist: {path}")
        return resolved

    def _resolve_run_dir(self, *, candidate: Path) -> Path:
        try:
            relative = candidate.relative_to(self._private_distilled_root)
        except ValueError as exc:
            raise EvidenceValidationError("Input must stay within private/distilled.") from exc
        if not relative.parts:
            raise EvidenceValidationError(
                "Input must point to a specific private/distilled/<run_id> directory or artifact.",
            )
        return self._private_distilled_root / relative.parts[0]

    def _resolve_output_path(self, *, output_path: Path | None, run_dir: Path) -> Path:
        if output_path is None:
            resolved = run_dir / self.REPORT_FILENAME
        else:
            resolved = (self._repo_root / output_path).resolve() if not output_path.is_absolute() else output_path.resolve()
            if resolved.suffix.casefold() != ".json":
                resolved = resolved / self.REPORT_FILENAME
        self._ensure_within_root(
            candidate=resolved,
            root=self._private_distilled_root,
            error_message="Output must stay within private/distilled.",
        )
        return resolved

    def _load_jsonl_objects(self, path: Path) -> list[dict[str, Any]]:
        rows: list[dict[str, Any]] = []
        with path.open("r", encoding="utf-8") as handle:
            for line_no, raw_line in enumerate(handle, start=1):
                line = raw_line.strip()
                if line_no == 1:
                    line = line.lstrip("\ufeff")
                if not line:
                    continue
                try:
                    payload = json.loads(line)
                except json.JSONDecodeError as exc:
                    raise EvidenceValidationError(f"{path.name} line {line_no} is invalid JSON.") from exc
                if not isinstance(payload, dict):
                    raise EvidenceValidationError(
                        f"{path.name} line {line_no} must contain a JSON object.",
                    )
                rows.append(payload)
        return rows

    def _read_json_object(self, path: Path) -> dict[str, Any]:
        try:
            payload = json.loads(path.read_text(encoding="utf-8").lstrip("\ufeff"))
        except json.JSONDecodeError as exc:
            raise EvidenceValidationError(f"{path.name} is invalid JSON.") from exc
        if not isinstance(payload, dict):
            raise EvidenceValidationError(f"{path.name} must contain a JSON object.")
        return payload

    def _write_json(self, *, output_path: Path, payload: dict[str, Any]) -> None:
        output_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    def _collect_evidence_ref_locations(
        self,
        *,
        value: Any,
        path: str = "",
    ) -> list[dict[str, Any]]:
        if isinstance(value, dict):
            locations: list[dict[str, Any]] = []
            for key, item in value.items():
                next_path = f"{path}.{key}" if path else key
                if key == "evidence_refs" and isinstance(item, list):
                    refs = self._unique_strings(item)
                    locations.append(
                        {
                            "path": next_path,
                            "refs": refs,
                        },
                    )
                    continue
                locations.extend(self._collect_evidence_ref_locations(value=item, path=next_path))
            return locations
        if isinstance(value, list):
            locations = []
            for index, item in enumerate(value):
                next_path = f"{path}[{index}]"
                locations.extend(self._collect_evidence_ref_locations(value=item, path=next_path))
            return locations
        return []

    def _add_index_ref(
        self,
        *,
        index: dict[str, Any],
        ref: Any,
        category: str,
        source: str,
    ) -> bool:
        if not isinstance(ref, str) or not ref:
            return False
        existing_sources = index["ref_sources"].setdefault(ref, [])
        if source not in existing_sources:
            existing_sources.append(source)
        if ref in index["refs"]:
            return False
        index["refs"].add(ref)
        index["counts"][category] += 1
        return True

    @staticmethod
    def _extract_contact_skill_ids(payload: dict[str, Any]) -> list[str]:
        return EvidenceValidationService._unique_strings(
            payload.get("contact_skill_id"),
            payload.get("skill_id"),
            payload.get("candidate_id"),
        )

    def _safe_relative_path(self, path: Path | None) -> str | None:
        if path is None:
            return None
        try:
            return str(path.relative_to(self._repo_root)).replace("\\", "/")
        except ValueError:
            return str(path).replace("\\", "/")

    def _build_artifact_summary(
        self,
        *,
        artifact_type: str,
        path: Path,
        record_count: int,
        indexed_ref_count: int,
    ) -> dict[str, Any]:
        return {
            "artifact_type": artifact_type,
            "path": self._safe_relative_path(path),
            "record_count": record_count,
            "indexed_ref_count": indexed_ref_count,
        }

    def _build_target_summary(self, *, artifact_type: str, path: Path | None) -> dict[str, Any] | None:
        if path is None:
            return None
        return {
            "artifact_type": artifact_type,
            "path": self._safe_relative_path(path),
        }

    @staticmethod
    def _first_existing_path(*paths: Path) -> Path | None:
        for path in paths:
            if path.is_file():
                return path
        return None

    @staticmethod
    def _ensure_within_root(*, candidate: Path, root: Path, error_message: str) -> None:
        try:
            candidate.relative_to(root)
        except ValueError as exc:
            raise EvidenceValidationError(error_message) from exc

    @staticmethod
    def _unique_strings(*values: Any) -> list[str]:
        seen: set[str] = set()
        ordered: list[str] = []
        for value in values:
            if isinstance(value, (list, tuple, set)):
                iterable = value
            elif hasattr(value, "__iter__") and not isinstance(value, (str, bytes, dict)):
                iterable = value
            else:
                iterable = [value]
            for item in iterable:
                if not isinstance(item, str) or not item:
                    continue
                if item in seen:
                    continue
                seen.add(item)
                ordered.append(item)
        return ordered
