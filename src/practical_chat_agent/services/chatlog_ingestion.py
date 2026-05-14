from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


class ChatlogNormalizationError(ValueError):
    """Raised when chatlog normalization input or output validation fails."""


@dataclass(frozen=True)
class ChatlogNormalizationResult:
    output_dir: Path | None
    report: dict[str, Any]


@dataclass(frozen=True)
class _ScanResult:
    file_aliases: dict[Path, str]
    total_lines: int
    parsed_lines: int
    failed_lines: int
    header_rows: int
    member_rows: int
    message_rows: int
    files_summary: list[dict[str, Any]]
    self_pair: tuple[str, str] | None
    file_contact_pairs: dict[str, tuple[str, str] | None]
    event_ids_by_file_and_message_id: dict[tuple[str, str], str]


class ChatlogIngestionService:
    def __init__(self, *, timezone_name: str = "Asia/Shanghai") -> None:
        self.timezone_name = timezone_name
        self._timezone = self._resolve_timezone(timezone_name)
        self._repo_root = Path.cwd().resolve()
        self._private_chat_history_root = (self._repo_root / "private" / "chat_history").resolve()
        self._private_distilled_root = (self._repo_root / "private" / "distilled").resolve()

    def normalize_weflow_exports(
        self,
        *,
        input_path: Path,
        output_dir: Path | None,
        limit: int | None = None,
        dry_run: bool = False,
    ) -> ChatlogNormalizationResult:
        resolved_input = self._resolve_existing_path(input_path)
        self._ensure_within_root(
            candidate=resolved_input,
            root=self._private_chat_history_root,
            error_message="Input must stay within private/chat_history.",
        )
        input_files = self._resolve_input_files(resolved_input)
        scan_result = self._scan_inputs(input_files)

        resolved_output_dir: Path | None = None
        if not dry_run:
            if output_dir is None:
                raise ChatlogNormalizationError("output_dir is required unless dry_run is enabled.")
            resolved_output_dir = self._resolve_output_dir(output_dir)
            resolved_output_dir.mkdir(parents=True, exist_ok=True)

        report, normalized_lines = self._normalize_messages(
            input_files=input_files,
            scan_result=scan_result,
            limit=limit,
        )
        report["dry_run"] = dry_run
        report["timezone_name"] = self.timezone_name
        report["input_root"] = "private/chat_history"

        if resolved_output_dir is not None:
            normalized_path = resolved_output_dir / "normalized_events.jsonl"
            with normalized_path.open("w", encoding="utf-8", newline="\n") as handle:
                for line in normalized_lines:
                    handle.write(line)
                    handle.write("\n")
            report["output_dir"] = self._safe_relative_path(resolved_output_dir)
            report["output_files"] = ["normalized_events.jsonl", "run_report.json"]
            report_path = resolved_output_dir / "run_report.json"
            report_path.write_text(
                json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
        else:
            report["output_dir"] = None
            report["output_files"] = []

        return ChatlogNormalizationResult(output_dir=resolved_output_dir, report=report)

    def _resolve_existing_path(self, path: Path) -> Path:
        resolved = (self._repo_root / path).resolve() if not path.is_absolute() else path.resolve()
        if not resolved.exists():
            raise ChatlogNormalizationError(f"Input path does not exist: {path}")
        return resolved

    def _resolve_input_files(self, input_path: Path) -> list[Path]:
        if input_path.is_file():
            if input_path.suffix.casefold() != ".jsonl":
                raise ChatlogNormalizationError("Input file must be a .jsonl file.")
            return [input_path]

        files = sorted(path.resolve() for path in input_path.glob("*.jsonl") if path.is_file())
        if not files:
            raise ChatlogNormalizationError(f"No JSONL files found under: {input_path}")
        return files

    def _resolve_output_dir(self, output_dir: Path) -> Path:
        resolved = (self._repo_root / output_dir).resolve() if not output_dir.is_absolute() else output_dir.resolve()
        self._ensure_within_root(
            candidate=resolved,
            root=self._private_distilled_root,
            error_message="Output must stay within private/distilled.",
        )
        return resolved

    @staticmethod
    def _resolve_timezone(timezone_name: str) -> ZoneInfo:
        try:
            return ZoneInfo(timezone_name)
        except ZoneInfoNotFoundError:
            return ZoneInfo("UTC")

    @staticmethod
    def _sha1_hex(value: str) -> str:
        return hashlib.sha1(value.encode("utf-8")).hexdigest()

    @classmethod
    def _hash_alias(cls, prefix: str, value: str, *, length: int = 12) -> str:
        return f"{prefix}_{cls._sha1_hex(value)[:length]}"

    @staticmethod
    def _ensure_within_root(*, candidate: Path, root: Path, error_message: str) -> None:
        try:
            candidate.relative_to(root)
        except ValueError as exc:
            raise ChatlogNormalizationError(error_message) from exc

    def _safe_relative_path(self, path: Path) -> str:
        try:
            return str(path.relative_to(self._repo_root)).replace("\\", "/")
        except ValueError:
            return str(path).replace("\\", "/")

    def _scan_inputs(self, input_files: list[Path]) -> _ScanResult:
        file_aliases = {path: f"file_{index:02d}" for index, path in enumerate(input_files, start=1)}
        total_lines = 0
        parsed_lines = 0
        failed_lines = 0
        header_rows = 0
        member_rows = 0
        message_rows = 0
        files_summary: list[dict[str, Any]] = []
        member_pair_file_coverage: defaultdict[tuple[str, str], set[str]] = defaultdict(set)
        member_pair_totals: Counter[tuple[str, str]] = Counter()
        message_pair_file_coverage: defaultdict[tuple[str, str], set[str]] = defaultdict(set)
        file_message_pairs: dict[str, Counter[tuple[str, str]]] = {}
        event_ids_by_file_and_message_id: dict[tuple[str, str], str] = {}

        for path in input_files:
            file_alias = file_aliases[path]
            row_counts = Counter()
            reply_rows = 0
            chat_records_rows = 0
            message_type_counts: Counter[int] = Counter()
            message_pair_counts: Counter[tuple[str, str]] = Counter()

            with path.open("r", encoding="utf-8") as handle:
                for line_no, raw_line in enumerate(handle, start=1):
                    total_lines += 1
                    line = raw_line.strip()
                    if not line:
                        continue
                    try:
                        payload = json.loads(line)
                    except json.JSONDecodeError:
                        failed_lines += 1
                        continue
                    parsed_lines += 1
                    row_type = str(payload.get("_type", "unknown"))
                    row_counts[row_type] += 1

                    if row_type == "header":
                        header_rows += 1
                        continue
                    if row_type == "member":
                        member_rows += 1
                        platform_id = payload.get("platformId")
                        account_name = payload.get("accountName")
                        if isinstance(platform_id, str) and isinstance(account_name, str):
                            pair = (platform_id, account_name)
                            member_pair_file_coverage[pair].add(file_alias)
                            member_pair_totals[pair] += 1
                        continue
                    if row_type != "message":
                        continue

                    message_rows += 1
                    sender = payload.get("sender")
                    account_name = payload.get("accountName")
                    message_type_code = payload.get("type")
                    platform_message_id = payload.get("platformMessageId")
                    if isinstance(sender, str) and isinstance(account_name, str):
                        pair = (sender, account_name)
                        message_pair_counts[pair] += 1
                        message_pair_file_coverage[pair].add(file_alias)
                    if isinstance(message_type_code, int):
                        message_type_counts[message_type_code] += 1
                    if "replyToMessageId" in payload:
                        reply_rows += 1
                    if "chatRecords" in payload:
                        chat_records_rows += 1
                    if isinstance(platform_message_id, str):
                        event_ids_by_file_and_message_id[(file_alias, platform_message_id)] = self._build_event_id(
                            file_alias=file_alias,
                            line_no=line_no,
                            platform_message_id=platform_message_id,
                        )

            file_message_pairs[file_alias] = message_pair_counts
            files_summary.append(
                {
                    "file_alias": file_alias,
                    "size_bytes": path.stat().st_size,
                    "header_rows": row_counts.get("header", 0),
                    "member_rows": row_counts.get("member", 0),
                    "message_rows": row_counts.get("message", 0),
                    "reply_rows": reply_rows,
                    "chat_records_rows": chat_records_rows,
                    "message_type_counts": {str(key): value for key, value in sorted(message_type_counts.items())},
                },
            )

        self_pair = self._resolve_self_pair(
            member_pair_file_coverage=member_pair_file_coverage,
            member_pair_totals=member_pair_totals,
            message_pair_file_coverage=message_pair_file_coverage,
            file_message_pairs=file_message_pairs,
        )
        file_contact_pairs = self._resolve_file_contact_pairs(
            self_pair=self_pair,
            file_message_pairs=file_message_pairs,
            message_pair_file_coverage=message_pair_file_coverage,
        )
        return _ScanResult(
            file_aliases=file_aliases,
            total_lines=total_lines,
            parsed_lines=parsed_lines,
            failed_lines=failed_lines,
            header_rows=header_rows,
            member_rows=member_rows,
            message_rows=message_rows,
            files_summary=files_summary,
            self_pair=self_pair,
            file_contact_pairs=file_contact_pairs,
            event_ids_by_file_and_message_id=event_ids_by_file_and_message_id,
        )

    @staticmethod
    def _resolve_self_pair(
        *,
        member_pair_file_coverage: dict[tuple[str, str], set[str]],
        member_pair_totals: Counter[tuple[str, str]],
        message_pair_file_coverage: dict[tuple[str, str], set[str]],
        file_message_pairs: dict[str, Counter[tuple[str, str]]],
    ) -> tuple[str, str] | None:
        member_candidates = [
            (len(file_aliases), member_pair_totals[pair], pair)
            for pair, file_aliases in member_pair_file_coverage.items()
            if len(file_aliases) >= 2
        ]
        if member_candidates:
            member_candidates.sort(key=lambda item: (-item[0], -item[1], item[2]))
            return member_candidates[0][2]

        message_totals: Counter[tuple[str, str]] = Counter()
        for counter in file_message_pairs.values():
            message_totals.update(counter)
        message_candidates = [
            (len(file_aliases), message_totals[pair], pair)
            for pair, file_aliases in message_pair_file_coverage.items()
            if len(file_aliases) >= 2
        ]
        if not message_candidates:
            return None
        message_candidates.sort(key=lambda item: (-item[0], -item[1], item[2]))
        return message_candidates[0][2]

    @staticmethod
    def _resolve_file_contact_pairs(
        *,
        self_pair: tuple[str, str] | None,
        file_message_pairs: dict[str, Counter[tuple[str, str]]],
        message_pair_file_coverage: dict[tuple[str, str], set[str]],
    ) -> dict[str, tuple[str, str] | None]:
        result: dict[str, tuple[str, str] | None] = {}
        for file_alias, message_pairs in file_message_pairs.items():
            candidates = [
                (count, -len(message_pair_file_coverage.get(pair, set())), pair)
                for pair, count in message_pairs.items()
                if pair != self_pair
            ]
            if candidates:
                candidates.sort(key=lambda item: (-item[0], item[1], item[2]))
                result[file_alias] = candidates[0][2]
                continue
            result[file_alias] = None
        return result

    def _normalize_messages(
        self,
        *,
        input_files: list[Path],
        scan_result: _ScanResult,
        limit: int | None,
    ) -> tuple[dict[str, Any], list[str]]:
        normalized_lines: list[str] = []
        normalized_count = 0
        skipped_non_message_rows = 0
        reply_ref_total = 0
        reply_ref_resolved = 0
        reply_ref_unresolved = 0
        forwarded_records_events = 0
        unsupported_message_type_counts: Counter[str] = Counter()
        normalized_message_type_counts: Counter[str] = Counter()
        status_counts: Counter[str] = Counter()
        warnings: list[str] = []

        for path in input_files:
            file_alias = scan_result.file_aliases[path]
            contact_pair = scan_result.file_contact_pairs.get(file_alias)
            conversation_id = self._build_conversation_id(file_alias=file_alias, contact_pair=contact_pair)
            contact_id = self._build_contact_id(file_alias=file_alias, contact_pair=contact_pair)

            with path.open("r", encoding="utf-8") as handle:
                for line_no, raw_line in enumerate(handle, start=1):
                    if limit is not None and normalized_count >= limit:
                        break

                    line = raw_line.strip()
                    if not line:
                        continue
                    try:
                        payload = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    if payload.get("_type") != "message":
                        skipped_non_message_rows += 1
                        continue

                    normalized_event, message_warning_flags = self._normalize_message_row(
                        payload=payload,
                        file_alias=file_alias,
                        line_no=line_no,
                        self_pair=scan_result.self_pair,
                        contact_pair=contact_pair,
                        conversation_id=conversation_id,
                        contact_id=contact_id,
                        event_ids_by_file_and_message_id=scan_result.event_ids_by_file_and_message_id,
                    )
                    normalized_lines.append(json.dumps(normalized_event, ensure_ascii=False))
                    normalized_count += 1
                    normalized_message_type_counts[normalized_event["message_type"]] += 1
                    status_counts[normalized_event["status"]] += 1
                    if "reply" in normalized_event["interaction_flags"]:
                        reply_ref_total += 1
                        if normalized_event.get("reply_to_event_id"):
                            reply_ref_resolved += 1
                        else:
                            reply_ref_unresolved += 1
                    if normalized_event["forwarded_records"]:
                        forwarded_records_events += 1
                    if normalized_event["message_type"] in {"mixed", "unknown"}:
                        unsupported_message_type_counts[str(normalized_event["source_message_type_code"])] += 1
                    warnings.extend(message_warning_flags)
                else:
                    continue
                break

        if scan_result.self_pair is None:
            warnings.append("self_identity_unresolved")
        if any(pair is None for pair in scan_result.file_contact_pairs.values()):
            warnings.append("contact_identity_unresolved_for_some_files")
        if reply_ref_unresolved:
            warnings.append("reply_target_missing_for_some_messages")

        report = {
            "tool": "chatlog-normalize",
            "source": "weflow_jsonl",
            "file_count": len(input_files),
            "files": scan_result.files_summary,
            "line_stats": {
                "total_lines": scan_result.total_lines,
                "parsed_lines": scan_result.parsed_lines,
                "failed_lines": scan_result.failed_lines,
                "header_rows": scan_result.header_rows,
                "member_rows": scan_result.member_rows,
                "message_rows": scan_result.message_rows,
                "normalized_events_written": normalized_count,
                "skipped_non_message_rows": skipped_non_message_rows,
                "limit": limit,
            },
            "message_type_counts": self._aggregate_file_message_type_counts(scan_result.files_summary),
            "normalized_message_type_counts": dict(normalized_message_type_counts),
            "status_counts": dict(status_counts),
            "reply_ref_stats": {
                "with_reply_field": reply_ref_total,
                "resolved": reply_ref_resolved,
                "unresolved": reply_ref_unresolved,
            },
            "chat_records_stats": {
                "forwarded_records_events": forwarded_records_events,
            },
            "unsupported_type_counts": dict(unsupported_message_type_counts),
            "identity_summary": {
                "self_identity_resolved": scan_result.self_pair is not None,
                "self_identity_hash": (
                    self._hash_alias("sender", "|".join(scan_result.self_pair))
                    if scan_result.self_pair is not None
                    else None
                ),
                "contact_files_with_resolved_primary_contact": sum(
                    1 for pair in scan_result.file_contact_pairs.values() if pair is not None
                ),
            },
            "warnings": sorted(set(warnings)),
        }
        return report, normalized_lines

    @staticmethod
    def _aggregate_file_message_type_counts(files_summary: list[dict[str, Any]]) -> dict[str, int]:
        combined: Counter[str] = Counter()
        for file_summary in files_summary:
            combined.update(file_summary["message_type_counts"])
        return dict(sorted(combined.items(), key=lambda item: int(item[0])))

    def _normalize_message_row(
        self,
        *,
        payload: dict[str, Any],
        file_alias: str,
        line_no: int,
        self_pair: tuple[str, str] | None,
        contact_pair: tuple[str, str] | None,
        conversation_id: str,
        contact_id: str,
        event_ids_by_file_and_message_id: dict[tuple[str, str], str],
    ) -> tuple[dict[str, Any], list[str]]:
        sender = str(payload["sender"])
        account_name = str(payload["accountName"])
        sender_pair = (sender, account_name)
        platform_message_id = str(payload["platformMessageId"])
        reply_to_message_id = payload.get("replyToMessageId")
        message_type_code = int(payload["type"])
        content = str(payload["content"])
        timestamp_epoch_s = int(payload["timestamp"])

        event_id = self._build_event_id(
            file_alias=file_alias,
            line_no=line_no,
            platform_message_id=platform_message_id,
        )
        reply_to_event_id = None
        if isinstance(reply_to_message_id, str):
            reply_to_event_id = event_ids_by_file_and_message_id.get((file_alias, reply_to_message_id))

        sender_role = self._resolve_sender_role(
            sender_pair=sender_pair,
            self_pair=self_pair,
            contact_pair=contact_pair,
            message_type_code=message_type_code,
            content=content,
        )
        message_type, content_kind_hint, interaction_flags = self._map_message_type(
            message_type_code=message_type_code,
            has_reply=isinstance(reply_to_message_id, str),
            has_chat_records=isinstance(payload.get("chatRecords"), list),
            content=content,
        )
        status = self._resolve_status(message_type_code=message_type_code, content=content)
        media_refs = self._build_media_refs(message_type_code=message_type_code, content=content)
        forwarded_records = self._build_forwarded_records(
            records=payload.get("chatRecords"),
            self_pair=self_pair,
            contact_pair=contact_pair,
        )
        risk_flags = self._build_risk_flags(
            sender_role=sender_role,
            message_type=message_type,
            reply_to_message_id=reply_to_message_id,
            reply_to_event_id=reply_to_event_id,
            has_chat_records=bool(forwarded_records),
        )
        warnings = [flag for flag in risk_flags if flag.endswith("unresolved") or flag.startswith("message_type_")]

        source_ref = {
            "file_alias": file_alias,
            "line_no": line_no,
            "platform_message_id_hash": self._hash_alias("pmid", platform_message_id, length=8),
        }
        if isinstance(reply_to_message_id, str):
            source_ref["reply_to_platform_message_id_hash"] = self._hash_alias(
                "pmid",
                reply_to_message_id,
                length=8,
            )

        normalized_event = {
            "event_id": event_id,
            "platform": "wechat",
            "source": "weflow_jsonl",
            "source_row_type": "message",
            "source_message_type_code": message_type_code,
            "source_ref": source_ref,
            "raw_ref": f"weflow:{file_alias}:{line_no}",
            "conversation_id": conversation_id,
            "contact_id": contact_id,
            "sender_id": self._build_sender_id(sender_pair),
            "sender_alias": sender_role,
            "sender_role": sender_role,
            "timestamp": self._format_timestamp(timestamp_epoch_s),
            "timestamp_epoch_s": timestamp_epoch_s,
            "timezone_assumption": self.timezone_name,
            "text": content,
            "message_type": message_type,
            "content_kind_hint": content_kind_hint,
            "interaction_flags": interaction_flags,
            "status": status,
            "reply_to_event_id": reply_to_event_id,
            "media_refs": media_refs,
            "forwarded_records": forwarded_records,
            "risk_flags": risk_flags,
        }
        return normalized_event, warnings

    def _resolve_sender_role(
        self,
        *,
        sender_pair: tuple[str, str],
        self_pair: tuple[str, str] | None,
        contact_pair: tuple[str, str] | None,
        message_type_code: int,
        content: str,
    ) -> str:
        if message_type_code == 80 and self._looks_like_system_notice(content):
            return "system"
        if self_pair is not None and sender_pair == self_pair:
            return "user"
        if contact_pair is not None and sender_pair == contact_pair:
            return "contact"
        return "unknown"

    @staticmethod
    def _looks_like_system_notice(content: str) -> bool:
        markers = ("撤回", "红包", "位置共享", "打招呼", "已添加", "加入了群聊", "领取")
        return any(marker in content for marker in markers)

    @staticmethod
    def _looks_like_recall_notice(content: str) -> bool:
        return "撤回" in content

    @classmethod
    def _map_message_type(
        cls,
        *,
        message_type_code: int,
        has_reply: bool,
        has_chat_records: bool,
        content: str,
    ) -> tuple[str, str | None, list[str]]:
        interaction_flags: list[str] = []
        if has_reply:
            interaction_flags.append("reply")
        if has_chat_records:
            interaction_flags.append("forwarded_records")

        if message_type_code == 0:
            return "text", None, interaction_flags
        if message_type_code == 25:
            return "text", "quoted_reply", interaction_flags
        if message_type_code == 80:
            interaction_flags.append("system_notice")
            if cls._looks_like_recall_notice(content):
                interaction_flags.append("recalled_notice")
                return "system", "recalled_notice", interaction_flags
            return "system", "system_notice", interaction_flags
        if message_type_code == 7:
            if has_chat_records:
                return "mixed", "forwarded_records", interaction_flags
            if content.startswith("../images/"):
                return "mixed", "image_placeholder", interaction_flags
            return "mixed", "unsupported_media_like", interaction_flags
        return "unknown", "unmapped_type_code", interaction_flags

    @classmethod
    def _resolve_status(cls, *, message_type_code: int, content: str) -> str:
        if message_type_code == 80 and cls._looks_like_recall_notice(content):
            return "recalled"
        return "normal"

    @staticmethod
    def _build_media_refs(*, message_type_code: int, content: str) -> list[dict[str, Any]]:
        if message_type_code == 7 and content.startswith("../images/"):
            return [{"kind": "image_placeholder", "path_hint": "redacted_in_private_output"}]
        return []

    def _build_forwarded_records(
        self,
        *,
        records: Any,
        self_pair: tuple[str, str] | None,
        contact_pair: tuple[str, str] | None,
    ) -> list[dict[str, Any]]:
        if not isinstance(records, list):
            return []
        normalized_records: list[dict[str, Any]] = []
        for index, record in enumerate(records):
            if not isinstance(record, dict):
                continue
            sender = record.get("sender")
            account_name = record.get("accountName")
            timestamp_epoch_s = record.get("timestamp")
            if not isinstance(sender, str) or not isinstance(account_name, str):
                continue
            sender_pair = (sender, account_name)
            normalized_records.append(
                {
                    "record_index": index,
                    "sender_id": self._build_sender_id(sender_pair),
                    "sender_alias": self._resolve_nested_sender_alias(
                        sender_pair=sender_pair,
                        self_pair=self_pair,
                        contact_pair=contact_pair,
                    ),
                    "timestamp": (
                        self._format_timestamp(int(timestamp_epoch_s))
                        if isinstance(timestamp_epoch_s, int)
                        else None
                    ),
                    "timestamp_epoch_s": int(timestamp_epoch_s) if isinstance(timestamp_epoch_s, int) else None,
                    "source_message_type_code": int(record["type"]) if isinstance(record.get("type"), int) else None,
                    "content": str(record.get("content", "")),
                    "avatar_present": bool(record.get("avatar")),
                },
            )
        return normalized_records

    @staticmethod
    def _resolve_nested_sender_alias(
        *,
        sender_pair: tuple[str, str],
        self_pair: tuple[str, str] | None,
        contact_pair: tuple[str, str] | None,
    ) -> str:
        if self_pair is not None and sender_pair == self_pair:
            return "user"
        if contact_pair is not None and sender_pair == contact_pair:
            return "contact"
        return "unknown"

    @staticmethod
    def _build_risk_flags(
        *,
        sender_role: str,
        message_type: str,
        reply_to_message_id: Any,
        reply_to_event_id: str | None,
        has_chat_records: bool,
    ) -> list[str]:
        risk_flags: list[str] = []
        if sender_role == "unknown":
            risk_flags.append("sender_role_unresolved")
        if isinstance(reply_to_message_id, str) and reply_to_event_id is None:
            risk_flags.append("reply_target_unresolved")
        if message_type in {"mixed", "unknown"}:
            risk_flags.append(f"message_type_{message_type}")
        if has_chat_records:
            risk_flags.append("forwarded_records_present")
        return risk_flags

    def _format_timestamp(self, timestamp_epoch_s: int) -> str:
        return datetime.fromtimestamp(timestamp_epoch_s, tz=timezone.utc).astimezone(self._timezone).isoformat()

    @classmethod
    def _build_event_id(cls, *, file_alias: str, line_no: int, platform_message_id: str) -> str:
        digest = cls._sha1_hex(f"weflow|{file_alias}|{line_no}|{platform_message_id}")
        return f"evt_{digest[:16]}"

    @classmethod
    def _build_sender_id(cls, sender_pair: tuple[str, str]) -> str:
        return cls._hash_alias("sender", f"{sender_pair[0]}|{sender_pair[1]}", length=12)

    @classmethod
    def _build_contact_id(cls, *, file_alias: str, contact_pair: tuple[str, str] | None) -> str:
        if contact_pair is None:
            return cls._hash_alias("contact", f"weflow|{file_alias}|unknown_contact", length=12)
        return cls._hash_alias("contact", f"{contact_pair[0]}|{contact_pair[1]}", length=12)

    @classmethod
    def _build_conversation_id(cls, *, file_alias: str, contact_pair: tuple[str, str] | None) -> str:
        if contact_pair is None:
            return cls._hash_alias("conv", f"weflow|{file_alias}|unknown_conversation", length=12)
        return cls._hash_alias("conv", f"weflow|{file_alias}|{contact_pair[0]}|{contact_pair[1]}", length=12)
