from __future__ import annotations

import hashlib
import json
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


class ConversationChunkingError(ValueError):
    """Raised when normalized event chunking input or output validation fails."""


@dataclass(frozen=True)
class ConversationChunkingResult:
    output_dir: Path | None
    report: dict[str, Any]


@dataclass(frozen=True)
class _BoundaryDecision:
    reason: str
    flags: tuple[str, ...] = ()


@dataclass
class _ChunkAccumulator:
    conversation_id: str
    contact_id: str
    event_ids: list[str] = field(default_factory=list)
    start_event_id: str | None = None
    end_event_id: str | None = None
    start_timestamp: str | None = None
    end_timestamp: str | None = None
    start_timestamp_epoch_s: int | None = None
    end_timestamp_epoch_s: int | None = None
    source_message_type_counts: Counter[int] = field(default_factory=Counter)
    message_type_counts: Counter[str] = field(default_factory=Counter)
    sender_role_counts: Counter[str] = field(default_factory=Counter)
    status_counts: Counter[str] = field(default_factory=Counter)
    interaction_flag_counts: Counter[str] = field(default_factory=Counter)
    risk_flag_counts: Counter[str] = field(default_factory=Counter)
    events_with_interaction_flags: list[str] = field(default_factory=list)
    events_with_risk_flags: list[str] = field(default_factory=list)

    @property
    def message_count(self) -> int:
        return len(self.event_ids)

    def add_event(self, event: dict[str, Any]) -> None:
        event_id = str(event["event_id"])
        timestamp = event.get("timestamp")
        timestamp_epoch_s = event.get("timestamp_epoch_s")

        if self.start_event_id is None:
            self.start_event_id = event_id
            self.start_timestamp = timestamp if isinstance(timestamp, str) else None
            self.start_timestamp_epoch_s = timestamp_epoch_s if isinstance(timestamp_epoch_s, int) else None

        self.end_event_id = event_id
        self.end_timestamp = timestamp if isinstance(timestamp, str) else self.end_timestamp
        self.end_timestamp_epoch_s = (
            timestamp_epoch_s if isinstance(timestamp_epoch_s, int) else self.end_timestamp_epoch_s
        )
        self.event_ids.append(event_id)

        source_message_type_code = event.get("source_message_type_code")
        if isinstance(source_message_type_code, int):
            self.source_message_type_counts[source_message_type_code] += 1

        message_type = event.get("message_type")
        if isinstance(message_type, str):
            self.message_type_counts[message_type] += 1

        sender_role = event.get("sender_role")
        if isinstance(sender_role, str):
            self.sender_role_counts[sender_role] += 1

        status = event.get("status")
        if isinstance(status, str):
            self.status_counts[status] += 1

        interaction_flags = [flag for flag in event.get("interaction_flags", []) if isinstance(flag, str)]
        if interaction_flags:
            self.interaction_flag_counts.update(interaction_flags)
            self.events_with_interaction_flags.append(event_id)

        risk_flags = [flag for flag in event.get("risk_flags", []) if isinstance(flag, str)]
        if risk_flags:
            self.risk_flag_counts.update(risk_flags)
            self.events_with_risk_flags.append(event_id)

    def to_chunk_record(self, *, chunking_reason: str, boundary_flags: tuple[str, ...]) -> dict[str, Any]:
        if self.start_event_id is None or self.end_event_id is None:
            raise ConversationChunkingError("Cannot finalize an empty chunk.")

        chunk_id = ConversationChunkingService.build_chunk_id(
            conversation_id=self.conversation_id,
            start_event_id=self.start_event_id,
            end_event_id=self.end_event_id,
        )
        return {
            "chunk_id": chunk_id,
            "contact_id": self.contact_id,
            "conversation_id": self.conversation_id,
            "start_event_id": self.start_event_id,
            "end_event_id": self.end_event_id,
            "event_ids": list(self.event_ids),
            "time_range": [self.start_timestamp, self.end_timestamp],
            "message_count": self.message_count,
            "chunking_reason": chunking_reason,
            "boundary_flags": list(boundary_flags),
            "source_message_type_codes": sorted(self.source_message_type_counts),
            "source_message_type_counts": {
                str(code): self.source_message_type_counts[code]
                for code in sorted(self.source_message_type_counts)
            },
            "message_type_counts": _sorted_counter_dict(self.message_type_counts),
            "sender_role_counts": _sorted_counter_dict(self.sender_role_counts),
            "status_counts": _sorted_counter_dict(self.status_counts),
            "interaction_flags": sorted(self.interaction_flag_counts),
            "interaction_flag_counts": _sorted_counter_dict(self.interaction_flag_counts),
            "risk_flags": sorted(self.risk_flag_counts),
            "risk_flag_counts": _sorted_counter_dict(self.risk_flag_counts),
            "events_with_interaction_flags": list(self.events_with_interaction_flags),
            "events_with_risk_flags": list(self.events_with_risk_flags),
        }


def _sorted_counter_dict(counter: Counter[str]) -> dict[str, int]:
    return {key: counter[key] for key in sorted(counter)}


class ConversationChunkingService:
    def __init__(self) -> None:
        self._repo_root = Path.cwd().resolve()
        self._private_distilled_root = (self._repo_root / "private" / "distilled").resolve()

    def chunk_normalized_events(
        self,
        *,
        input_path: Path,
        output_dir: Path | None,
        limit: int | None = None,
        dry_run: bool = False,
        max_gap_minutes: int = 240,
        max_messages_per_chunk: int = 80,
    ) -> ConversationChunkingResult:
        normalized_events_path = self._resolve_input_file(input_path)

        resolved_output_dir: Path | None = None
        if not dry_run:
            resolved_output_dir = self._resolve_output_dir(output_dir or normalized_events_path.parent)
            resolved_output_dir.mkdir(parents=True, exist_ok=True)

        report, chunk_lines = self._chunk_file(
            normalized_events_path=normalized_events_path,
            limit=limit,
            max_gap_minutes=max_gap_minutes,
            max_messages_per_chunk=max_messages_per_chunk,
        )
        report["dry_run"] = dry_run
        report["input_file"] = self._safe_relative_path(normalized_events_path)

        if resolved_output_dir is not None:
            chunks_path = resolved_output_dir / "chunks.jsonl"
            with chunks_path.open("w", encoding="utf-8", newline="\n") as handle:
                for line in chunk_lines:
                    handle.write(line)
                    handle.write("\n")
            report["output_dir"] = self._safe_relative_path(resolved_output_dir)
            report["output_files"] = ["chunks.jsonl", "run_report.json"]
            self._write_run_report(output_dir=resolved_output_dir, chunk_report=report)
        else:
            report["output_dir"] = None
            report["output_files"] = []

        return ConversationChunkingResult(output_dir=resolved_output_dir, report=report)

    def _chunk_file(
        self,
        *,
        normalized_events_path: Path,
        limit: int | None,
        max_gap_minutes: int,
        max_messages_per_chunk: int,
    ) -> tuple[dict[str, Any], list[str]]:
        total_lines = 0
        parsed_lines = 0
        failed_lines = 0
        events_consumed = 0
        chunk_lines: list[str] = []
        warnings: set[str] = set()

        conversation_ids: set[str] = set()
        contact_ids: set[str] = set()
        source_message_type_counts: Counter[int] = Counter()
        message_type_counts: Counter[str] = Counter()
        sender_role_counts: Counter[str] = Counter()
        status_counts: Counter[str] = Counter()
        interaction_flag_counts: Counter[str] = Counter()
        risk_flag_counts: Counter[str] = Counter()
        chunking_reason_counts: Counter[str] = Counter()
        boundary_flag_counts: Counter[str] = Counter()
        message_count_total = 0

        max_gap_seconds = max_gap_minutes * 60
        current_chunk: _ChunkAccumulator | None = None

        with normalized_events_path.open("r", encoding="utf-8") as handle:
            for line_no, raw_line in enumerate(handle, start=1):
                if limit is not None and events_consumed >= limit:
                    break
                total_lines += 1
                line = raw_line.strip()
                if not line:
                    continue
                try:
                    payload = json.loads(line)
                except json.JSONDecodeError:
                    failed_lines += 1
                    warnings.add("invalid_normalized_event_jsonl")
                    continue

                parsed_lines += 1
                event = self._coerce_event(payload=payload, line_no=line_no)
                events_consumed += 1
                message_count_total += 1

                conversation_ids.add(event["conversation_id"])
                contact_ids.add(event["contact_id"])
                source_message_type_counts.update([event["source_message_type_code"]])
                message_type_counts.update([event["message_type"]])
                sender_role_counts.update([event["sender_role"]])
                status_counts.update([event["status"]])
                interaction_flag_counts.update(event["interaction_flags"])
                risk_flag_counts.update(event["risk_flags"])

                if current_chunk is not None:
                    if self._timestamps_non_monotonic(current_chunk=current_chunk, next_event=event):
                        warnings.add("non_monotonic_timestamp_order")
                    boundary = self._detect_boundary(
                        current_chunk=current_chunk,
                        next_event=event,
                        max_gap_seconds=max_gap_seconds,
                        max_messages_per_chunk=max_messages_per_chunk,
                    )
                    if boundary is not None:
                        chunk_lines.append(
                            json.dumps(
                                current_chunk.to_chunk_record(
                                    chunking_reason=boundary.reason,
                                    boundary_flags=boundary.flags,
                                ),
                                ensure_ascii=False,
                            ),
                        )
                        chunking_reason_counts[boundary.reason] += 1
                        boundary_flag_counts.update(boundary.flags)
                        current_chunk = None

                if current_chunk is None:
                    current_chunk = _ChunkAccumulator(
                        conversation_id=event["conversation_id"],
                        contact_id=event["contact_id"],
                    )
                current_chunk.add_event(event)

        if current_chunk is not None:
            final_boundary = _BoundaryDecision(reason="manual", flags=("end_of_input",))
            chunk_lines.append(
                json.dumps(
                    current_chunk.to_chunk_record(
                        chunking_reason=final_boundary.reason,
                        boundary_flags=final_boundary.flags,
                    ),
                    ensure_ascii=False,
                ),
            )
            chunking_reason_counts[final_boundary.reason] += 1
            boundary_flag_counts.update(final_boundary.flags)

        if failed_lines:
            warnings.add("some_input_lines_failed_to_parse")
        if events_consumed == 0:
            warnings.add("no_events_chunked")

        chunk_count = len(chunk_lines)
        report = {
            "tool": "chatlog-chunk",
            "line_stats": {
                "total_lines": total_lines,
                "parsed_lines": parsed_lines,
                "failed_lines": failed_lines,
                "events_consumed": events_consumed,
                "limit": limit,
            },
            "chunk_stats": {
                "chunk_count": chunk_count,
                "conversation_count": len(conversation_ids),
                "contact_count": len(contact_ids),
                "max_gap_minutes": max_gap_minutes,
                "max_messages_per_chunk": max_messages_per_chunk,
                "avg_messages_per_chunk": round(message_count_total / chunk_count, 2) if chunk_count else 0.0,
                "min_messages_per_chunk": min(
                    (json.loads(line)["message_count"] for line in chunk_lines),
                    default=0,
                ),
                "max_messages_in_chunk": max(
                    (json.loads(line)["message_count"] for line in chunk_lines),
                    default=0,
                ),
            },
            "chunking_reason_counts": _sorted_counter_dict(chunking_reason_counts),
            "boundary_flag_counts": _sorted_counter_dict(boundary_flag_counts),
            "source_message_type_counts": {
                str(code): source_message_type_counts[code]
                for code in sorted(source_message_type_counts)
            },
            "message_type_counts": _sorted_counter_dict(message_type_counts),
            "sender_role_counts": _sorted_counter_dict(sender_role_counts),
            "status_counts": _sorted_counter_dict(status_counts),
            "interaction_flag_counts": _sorted_counter_dict(interaction_flag_counts),
            "risk_flag_counts": _sorted_counter_dict(risk_flag_counts),
            "warnings": sorted(warnings),
        }
        return report, chunk_lines

    def _resolve_input_file(self, input_path: Path) -> Path:
        resolved_input = self._resolve_existing_path(input_path)
        self._ensure_within_root(
            candidate=resolved_input,
            root=self._private_distilled_root,
            error_message="Input must stay within private/distilled.",
        )

        if resolved_input.is_dir():
            normalized_events_path = resolved_input / "normalized_events.jsonl"
            if normalized_events_path.is_file():
                return normalized_events_path

            nested_candidates = sorted(
                path.resolve()
                for path in resolved_input.rglob("normalized_events.jsonl")
                if path.is_file()
            )
            if len(nested_candidates) == 1:
                return nested_candidates[0]
            if not nested_candidates:
                raise ConversationChunkingError(
                    "Input directory must contain normalized_events.jsonl.",
                )
            raise ConversationChunkingError(
                "Input directory contains multiple normalized_events.jsonl files; pass a specific run directory or file.",
            )

        if resolved_input.suffix.casefold() != ".jsonl":
            raise ConversationChunkingError("Input file must be a .jsonl file.")
        return resolved_input

    def _resolve_existing_path(self, path: Path) -> Path:
        resolved = (self._repo_root / path).resolve() if not path.is_absolute() else path.resolve()
        if not resolved.exists():
            raise ConversationChunkingError(f"Input path does not exist: {path}")
        return resolved

    def _resolve_output_dir(self, output_dir: Path) -> Path:
        resolved = (self._repo_root / output_dir).resolve() if not output_dir.is_absolute() else output_dir.resolve()
        self._ensure_within_root(
            candidate=resolved,
            root=self._private_distilled_root,
            error_message="Output must stay within private/distilled.",
        )
        return resolved

    @staticmethod
    def _ensure_within_root(*, candidate: Path, root: Path, error_message: str) -> None:
        try:
            candidate.relative_to(root)
        except ValueError as exc:
            raise ConversationChunkingError(error_message) from exc

    def _safe_relative_path(self, path: Path) -> str:
        try:
            return str(path.relative_to(self._repo_root)).replace("\\", "/")
        except ValueError:
            return str(path).replace("\\", "/")

    def _write_run_report(self, *, output_dir: Path, chunk_report: dict[str, Any]) -> None:
        report_path = output_dir / "run_report.json"
        merged_report: dict[str, Any] = {}

        if report_path.exists():
            try:
                existing_report = json.loads(report_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                chunk_report["warnings"] = sorted(set(chunk_report["warnings"]) | {"existing_run_report_invalid_json"})
            else:
                if isinstance(existing_report, dict):
                    merged_report = existing_report
                else:
                    chunk_report["warnings"] = sorted(
                        set(chunk_report["warnings"]) | {"existing_run_report_not_object"},
                    )

        merged_report["chunking"] = chunk_report
        existing_output_files = merged_report.get("output_files")
        output_files = list(existing_output_files) if isinstance(existing_output_files, list) else []
        for filename in ("chunks.jsonl", "run_report.json"):
            if filename not in output_files:
                output_files.append(filename)
        merged_report["output_files"] = output_files

        report_path.write_text(
            json.dumps(merged_report, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    def _coerce_event(self, *, payload: dict[str, Any], line_no: int) -> dict[str, Any]:
        event_id = payload.get("event_id")
        conversation_id = payload.get("conversation_id")
        contact_id = payload.get("contact_id")
        source_message_type_code = payload.get("source_message_type_code")

        if not isinstance(event_id, str) or not event_id:
            raise ConversationChunkingError(f"normalized event line {line_no} is missing event_id.")
        if not isinstance(conversation_id, str) or not conversation_id:
            raise ConversationChunkingError(f"normalized event line {line_no} is missing conversation_id.")
        if not isinstance(contact_id, str) or not contact_id:
            raise ConversationChunkingError(f"normalized event line {line_no} is missing contact_id.")
        if not isinstance(source_message_type_code, int):
            raise ConversationChunkingError(
                f"normalized event line {line_no} is missing source_message_type_code.",
            )

        return {
            "event_id": event_id,
            "conversation_id": conversation_id,
            "contact_id": contact_id,
            "timestamp": payload.get("timestamp") if isinstance(payload.get("timestamp"), str) else None,
            "timestamp_epoch_s": (
                payload.get("timestamp_epoch_s") if isinstance(payload.get("timestamp_epoch_s"), int) else None
            ),
            "source_message_type_code": source_message_type_code,
            "message_type": (
                payload.get("message_type") if isinstance(payload.get("message_type"), str) else "unknown"
            ),
            "sender_role": (
                payload.get("sender_role") if isinstance(payload.get("sender_role"), str) else "unknown"
            ),
            "status": payload.get("status") if isinstance(payload.get("status"), str) else "unknown",
            "interaction_flags": [
                flag for flag in payload.get("interaction_flags", []) if isinstance(flag, str)
            ],
            "risk_flags": [flag for flag in payload.get("risk_flags", []) if isinstance(flag, str)],
        }

    @staticmethod
    def _timestamps_non_monotonic(
        *,
        current_chunk: _ChunkAccumulator,
        next_event: dict[str, Any],
    ) -> bool:
        if current_chunk.end_timestamp_epoch_s is None:
            return False
        next_epoch_s = next_event.get("timestamp_epoch_s")
        return isinstance(next_epoch_s, int) and next_epoch_s < current_chunk.end_timestamp_epoch_s

    @staticmethod
    def _detect_boundary(
        *,
        current_chunk: _ChunkAccumulator,
        next_event: dict[str, Any],
        max_gap_seconds: int,
        max_messages_per_chunk: int,
    ) -> _BoundaryDecision | None:
        boundary_flags: list[str] = []
        if next_event["conversation_id"] != current_chunk.conversation_id:
            boundary_flags.append("conversation_change")
        if next_event["contact_id"] != current_chunk.contact_id:
            boundary_flags.append("contact_change")
        if boundary_flags:
            return _BoundaryDecision(reason="manual", flags=tuple(boundary_flags))

        if current_chunk.message_count >= max_messages_per_chunk:
            return _BoundaryDecision(reason="message_limit", flags=("max_messages_reached",))

        current_epoch_s = current_chunk.end_timestamp_epoch_s
        next_epoch_s = next_event.get("timestamp_epoch_s")
        if isinstance(current_epoch_s, int) and isinstance(next_epoch_s, int):
            if next_epoch_s - current_epoch_s >= max_gap_seconds:
                return _BoundaryDecision(reason="time_gap", flags=("gap_exceeded",))

        return None

    @staticmethod
    def build_chunk_id(*, conversation_id: str, start_event_id: str, end_event_id: str) -> str:
        digest = hashlib.sha1(
            f"chunk|{conversation_id}|{start_event_id}|{end_event_id}".encode("utf-8"),
        ).hexdigest()
        return f"chk_{digest[:16]}"
