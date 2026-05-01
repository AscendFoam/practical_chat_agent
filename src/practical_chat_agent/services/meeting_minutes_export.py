from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from practical_chat_agent.core.enums import MeetingExportTemplate
from practical_chat_agent.core.models import (
    MeetingMinutesDraft,
    MeetingMinutesRecord,
    MeetingSegmentRecord,
    MeetingSessionRecord,
)
from practical_chat_agent.services.meeting_minutes import MeetingMinutesService
from practical_chat_agent.storage.repositories.base import MeetingRepository

_DECISION_HINTS = (
    "\u51b3\u5b9a",
    "\u7ed3\u8bba",
    "\u786e\u8ba4",
    "\u5171\u8bc6",
    "\u901a\u8fc7",
    "\u91c7\u7528",
    "\u6700\u7ec8",
    "agreed",
    "decided",
    "confirmed",
    "final",
    "approved",
)

_ACTION_HINTS = (
    "\u5f85\u529e",
    "\u884c\u52a8",
    "\u8ddf\u8fdb",
    "\u8d1f\u8d23",
    "\u5b89\u6392",
    "\u5b8c\u6210",
    "\u63d0\u4ea4",
    "\u540c\u6b65",
    "\u53d1\u9001",
    "\u6392\u671f",
    "review",
    "follow up",
    "action",
    "todo",
    "owner",
    "deadline",
)

_RISK_HINTS = (
    "\u98ce\u9669",
    "\u95ee\u9898",
    "\u963b\u585e",
    "\u5361\u4f4f",
    "\u5f02\u5e38",
    "\u5ef6\u671f",
    "\u4e0d\u786e\u5b9a",
    "\u5f85\u786e\u8ba4",
    "\u4f9d\u8d56",
    "\u7f3a\u5c11",
    "\u62c5\u5fc3",
    "issue",
    "risk",
    "blocker",
    "concern",
    "unknown",
    "pending",
)

_NORMALIZED_SENTENCE_REPLACEMENTS = {
    "there is not enough transcript yet to summarize the meeting.": "\u5f53\u524d\u4f1a\u8bae\u8f6c\u5199\u4ecd\u7136\u8f83\u5c11\uff0c\u6682\u65f6\u65e0\u6cd5\u5f62\u6210\u7a33\u5b9a\u6458\u8981\u3002",
    "not enough transcript yet. keep listening for more meeting context.": "\u5f53\u524d\u4f1a\u8bae\u8f6c\u5199\u4ecd\u7136\u8f83\u5c11\uff0c\u5efa\u8bae\u7ee7\u7eed\u91c7\u96c6\u66f4\u591a\u4e0a\u4e0b\u6587\u3002",
    "no tencent meeting desktop window was detected.": "\u5f53\u524d\u672a\u68c0\u6d4b\u5230\u817e\u8baf\u4f1a\u8bae\u684c\u9762\u7a97\u53e3\u3002",
    "make sure tencent meeting is running and its main meeting window is visible.": "\u8bf7\u786e\u8ba4\u817e\u8baf\u4f1a\u8bae\u6b63\u5728\u8fd0\u884c\uff0c\u4e14\u4e3b\u4f1a\u8bae\u7a97\u53e3\u5904\u4e8e\u53ef\u89c1\u72b6\u6001\u3002",
    "do you want a one-sentence checkpoint summary to realign the room?": "\u662f\u5426\u9700\u8981\u8865\u4e00\u6761\u4e00\u53e5\u8bdd\u9636\u6bb5\u6027\u603b\u7ed3\uff0c\u5e2e\u52a9\u4e0e\u4f1a\u8005\u91cd\u65b0\u5bf9\u9f50\u8ba8\u8bba\u7126\u70b9\uff1f",
    "separate confirmed decisions from open questions in the meeting notes.": "\u5efa\u8bae\u5728\u4f1a\u540e\u7eaa\u8981\u4e2d\u533a\u5206\u5df2\u786e\u8ba4\u7ed3\u8bba\u4e0e\u5f85\u786e\u8ba4\u95ee\u9898\u3002",
}


@dataclass(slots=True)
class MeetingMinutesExportResult:
    session_record: MeetingSessionRecord
    segments: list[MeetingSegmentRecord]
    draft: MeetingMinutesDraft
    record: MeetingMinutesRecord
    output_path: Path


class MeetingMinutesExportService:
    """Generate Markdown meeting minutes, persist files, and archive versions."""

    def __init__(
        self,
        *,
        meeting_repository: MeetingRepository,
        meeting_minutes_service: MeetingMinutesService,
    ) -> None:
        self.meeting_repository = meeting_repository
        self.meeting_minutes_service = meeting_minutes_service

    def export_minutes(
        self,
        *,
        session_record: MeetingSessionRecord,
        segments: list[MeetingSegmentRecord],
        template: MeetingExportTemplate,
        output_path: Path,
        started_after: datetime | None = None,
        started_before: datetime | None = None,
    ) -> MeetingMinutesExportResult:
        draft = self.meeting_minutes_service.build_minutes(
            session_record=session_record,
            segments=segments,
            template=template,
            fallback_builder=self._build_minutes_draft_fallback,
        )
        markdown = self._build_meeting_markdown_export(
            session_record=session_record,
            segments=segments,
            draft=draft,
            started_after=started_after,
            started_before=started_before,
        )

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(markdown, encoding="utf-8")

        record = self.meeting_repository.add_minutes(
            MeetingMinutesRecord(
                session_id=session_record.session_id,
                template=template,
                title=draft.title,
                backend=draft.backend,
                model=draft.model,
                status=draft.status,
                output_path=str(output_path),
                markdown_body=markdown,
                overview=draft.overview,
                background=draft.background,
                conclusions=draft.conclusions,
                action_items=draft.action_items,
                risks=draft.risks,
                raw_excerpt_ids=draft.raw_excerpt_ids,
                raw={
                    **draft.raw,
                    "started_after": started_after.isoformat() if started_after is not None else None,
                    "started_before": started_before.isoformat() if started_before is not None else None,
                    "segment_count": len(segments),
                },
            ),
        )
        return MeetingMinutesExportResult(
            session_record=session_record,
            segments=segments,
            draft=draft,
            record=record,
            output_path=output_path,
        )

    @staticmethod
    def _format_meeting_timestamp(value: datetime | None) -> str:
        if value is None:
            return "-"
        return value.astimezone().strftime("%Y-%m-%d %H:%M:%S %z")

    @classmethod
    def _render_meeting_segment_text_line(cls, segment: MeetingSegmentRecord) -> str:
        timestamp = segment.display_time or cls._format_meeting_timestamp(segment.started_at or segment.created_at)
        speaker = segment.speaker_name or "Unknown"
        text = (segment.text or "").replace("\r", " ").replace("\n", " ").strip()
        if not text:
            text = "<empty>"
        return f"[{timestamp}] {speaker}: {text}"

    @staticmethod
    def _clean_meeting_text(text: str | None) -> str:
        return " ".join((text or "").replace("\r", " ").replace("\n", " ").split()).strip()

    @classmethod
    def _normalize_export_sentence(cls, text: str | None) -> str:
        cleaned = cls._clean_meeting_text(text)
        if not cleaned:
            return ""
        return _NORMALIZED_SENTENCE_REPLACEMENTS.get(cleaned.casefold(), cleaned)

    @classmethod
    def _shorten_meeting_text(cls, text: str, *, limit: int = 140) -> str:
        cleaned = cls._normalize_export_sentence(text)
        if len(cleaned) <= limit:
            return cleaned
        return f"{cleaned[: max(limit - 3, 1)].rstrip()}..."

    @classmethod
    def _dedupe_text_items(cls, items: list[str], *, limit: int | None = None) -> list[str]:
        results: list[str] = []
        seen: set[str] = set()
        for item in items:
            cleaned = cls._normalize_export_sentence(item)
            if not cleaned:
                continue
            normalized = cleaned.casefold()
            if normalized in seen:
                continue
            seen.add(normalized)
            results.append(cleaned)
            if limit is not None and len(results) >= limit:
                break
        return results

    @staticmethod
    def _text_matches_any_hint(text: str, hints: tuple[str, ...]) -> bool:
        lowered = text.casefold()
        return any(hint.casefold() in lowered for hint in hints)

    @classmethod
    def _build_segment_candidates(
        cls,
        segments: list[MeetingSegmentRecord],
        *,
        hints: tuple[str, ...],
        limit: int,
    ) -> list[str]:
        collected: list[str] = []
        for segment in reversed(segments):
            cleaned = cls._clean_meeting_text(segment.text)
            if not cleaned:
                continue
            if cls._text_matches_any_hint(cleaned, hints):
                collected.append(cls._shorten_meeting_text(cleaned))
            if len(collected) >= limit * 2:
                break
        collected.reverse()
        return cls._dedupe_text_items(collected, limit=limit)

    @staticmethod
    def _meeting_segment_bounds(
        segments: list[MeetingSegmentRecord],
    ) -> tuple[datetime | None, datetime | None]:
        if not segments:
            return None, None
        started_values = [segment.started_at or segment.created_at for segment in segments]
        ended_values = [segment.ended_at or segment.started_at or segment.created_at for segment in segments]
        return min(started_values), max(ended_values)

    @classmethod
    def _build_export_background_points(
        cls,
        *,
        session_record: MeetingSessionRecord,
        segments: list[MeetingSegmentRecord],
    ) -> list[str]:
        items: list[str] = []
        if session_record.meeting_title:
            items.append(f"\u672c\u6b21\u4f1a\u8bae\u4e3b\u9898\u4e3a\u201c{session_record.meeting_title}\u201d\u3002")
        if session_record.latest_summary:
            items.append(cls._normalize_export_sentence(session_record.latest_summary))
        if session_record.notes:
            items.extend(f"\u7cfb\u7edf\u5907\u6ce8\uff1a{cls._normalize_export_sentence(note)}" for note in session_record.notes[:2])
        if segments:
            first_segment = next((segment for segment in segments if cls._clean_meeting_text(segment.text)), None)
            if first_segment is not None:
                items.append(f"\u4f1a\u8bae\u5f00\u573a\u4e0a\u4e0b\u6587\uff1a{cls._shorten_meeting_text(first_segment.text)}")
        if not items:
            items.append("\u5f53\u524d\u5bfc\u51fa\u8303\u56f4\u5185\u5c1a\u65e0\u8db3\u591f\u4e0a\u4e0b\u6587\uff0c\u5efa\u8bae\u7ee7\u7eed\u91c7\u96c6\u66f4\u591a\u4f1a\u8bae\u8f6c\u5199\u5185\u5bb9\u3002")
        return cls._dedupe_text_items(items, limit=4)

    @classmethod
    def _build_export_conclusion_points(
        cls,
        *,
        session_record: MeetingSessionRecord,
        segments: list[MeetingSegmentRecord],
    ) -> list[str]:
        items: list[str] = list(session_record.latest_key_points)
        items.extend(cls._build_segment_candidates(segments, hints=_DECISION_HINTS, limit=4))
        if not items and session_record.latest_summary:
            items.append(cls._normalize_export_sentence(session_record.latest_summary))
        if not items:
            items.append("\u5f53\u524d\u5bfc\u51fa\u8303\u56f4\u5185\u5c1a\u672a\u8bc6\u522b\u51fa\u7a33\u5b9a\u7ed3\u8bba\uff0c\u5efa\u8bae\u7ee7\u7eed\u89c2\u5bdf\u540e\u7eed\u8ba8\u8bba\u3002")
        return cls._dedupe_text_items(items, limit=5)

    @classmethod
    def _build_export_action_items(
        cls,
        *,
        session_record: MeetingSessionRecord,
        segments: list[MeetingSegmentRecord],
    ) -> list[str]:
        items: list[str] = list(session_record.latest_action_items)
        items.extend(cls._build_segment_candidates(segments, hints=_ACTION_HINTS, limit=4))
        if not items:
            items.append("\u5f53\u524d\u5bfc\u51fa\u8303\u56f4\u5185\u672a\u8bc6\u522b\u51fa\u660e\u786e action item\u3002")
        return cls._dedupe_text_items(items, limit=5)

    @classmethod
    def _build_export_risk_points(
        cls,
        *,
        session_record: MeetingSessionRecord,
        segments: list[MeetingSegmentRecord],
    ) -> list[str]:
        items: list[str] = list(session_record.latest_follow_up_questions)
        items.extend(cls._build_segment_candidates(segments, hints=_RISK_HINTS, limit=4))
        question_segments = [
            cls._shorten_meeting_text(segment.text)
            for segment in reversed(segments)
            if "?" in (segment.text or "") or "\uff1f" in (segment.text or "")
        ]
        items.extend(reversed(question_segments[:3]))
        if not segments:
            items.append("\u5f53\u524d\u5bfc\u51fa\u8303\u56f4\u5185\u6ca1\u6709\u4f1a\u8bae\u8f6c\u5199\u7247\u6bb5\uff0c\u5b58\u5728\u4fe1\u606f\u4e0d\u5b8c\u6574\u98ce\u9669\u3002")
        if session_record.notes:
            items.extend(f"\u91c7\u96c6\u4fa7\u63d0\u793a\uff1a{cls._normalize_export_sentence(note)}" for note in session_record.notes[:1])
        if not items:
            items.append("\u5f53\u524d\u5bfc\u51fa\u8303\u56f4\u5185\u6682\u65e0\u663e\u8457\u98ce\u9669\u6216\u5f85\u786e\u8ba4\u4e8b\u9879\u3002")
        return cls._dedupe_text_items(items, limit=5)

    @classmethod
    def _build_export_excerpt_segments(
        cls,
        segments: list[MeetingSegmentRecord],
        *,
        limit: int = 8,
    ) -> list[MeetingSegmentRecord]:
        if len(segments) <= limit:
            return segments

        scored: list[tuple[int, int, MeetingSegmentRecord]] = []
        for index, segment in enumerate(segments):
            cleaned = cls._clean_meeting_text(segment.text)
            if not cleaned:
                continue
            score = min(len(cleaned), 180)
            if cls._text_matches_any_hint(cleaned, _DECISION_HINTS):
                score += 60
            if cls._text_matches_any_hint(cleaned, _ACTION_HINTS):
                score += 50
            if cls._text_matches_any_hint(cleaned, _RISK_HINTS):
                score += 40
            if "?" in cleaned or "\uff1f" in cleaned:
                score += 20
            scored.append((score, index, segment))

        chosen = sorted(scored, key=lambda item: (-item[0], item[1]))[:limit]
        chosen_indices = {index for _, index, _ in chosen}
        return [segment for index, segment in enumerate(segments) if index in chosen_indices]

    def _build_minutes_draft_fallback(
        self,
        *,
        session_record: MeetingSessionRecord,
        segments: list[MeetingSegmentRecord],
        template: MeetingExportTemplate,
    ) -> MeetingMinutesDraft:
        background_points = self._build_export_background_points(
            session_record=session_record,
            segments=segments,
        )
        conclusion_points = self._build_export_conclusion_points(
            session_record=session_record,
            segments=segments,
        )
        action_items = self._build_export_action_items(
            session_record=session_record,
            segments=segments,
        )
        risk_points = self._build_export_risk_points(
            session_record=session_record,
            segments=segments,
        )
        excerpt_segments = self._build_export_excerpt_segments(segments, limit=8)
        overview = self._normalize_export_sentence(session_record.latest_summary)
        if not overview:
            overview = background_points[0] if background_points else "\u5f53\u524d\u5bfc\u51fa\u8303\u56f4\u5185\u5c1a\u65e0\u8db3\u591f\u4e0a\u4e0b\u6587\u3002"
        title = session_record.meeting_title or session_record.meeting_key or session_record.session_id

        if template == MeetingExportTemplate.BRIEF:
            background_points = background_points[:2]
            conclusion_points = conclusion_points[:3]
            action_items = action_items[:3]
            risk_points = risk_points[:2]
            excerpt_segments = excerpt_segments[:3]
        elif template == MeetingExportTemplate.STANDARD:
            background_points = background_points[:4]
            conclusion_points = conclusion_points[:5]
            action_items = action_items[:5]
            risk_points = risk_points[:4]
            excerpt_segments = excerpt_segments[:5]
        else:
            background_points = background_points[:6]
            conclusion_points = conclusion_points[:6]
            action_items = action_items[:6]
            risk_points = risk_points[:5]
            excerpt_segments = excerpt_segments[:8]

        return MeetingMinutesDraft(
            template=template,
            backend="heuristic_fallback",
            model=None,
            status="ok",
            title=title,
            overview=overview,
            background=background_points,
            conclusions=conclusion_points,
            action_items=action_items,
            risks=risk_points,
            raw_excerpt_ids=[segment.segment_id for segment in excerpt_segments],
            raw={
                "excerpt_segment_ids": [segment.segment_id for segment in excerpt_segments],
                "segment_count": len(segments),
            },
        )

    def _resolve_excerpt_segments(
        self,
        *,
        segments: list[MeetingSegmentRecord],
        draft: MeetingMinutesDraft,
    ) -> list[MeetingSegmentRecord]:
        if not segments:
            return []
        requested_ids = {segment_id for segment_id in draft.raw_excerpt_ids if segment_id}
        if requested_ids:
            matched = [segment for segment in segments if segment.segment_id in requested_ids]
            if matched:
                return matched
        fallback_limit = 3 if draft.template == MeetingExportTemplate.BRIEF else 5
        if draft.template == MeetingExportTemplate.FULL:
            fallback_limit = 8
        return self._build_export_excerpt_segments(segments, limit=fallback_limit)

    def _build_meeting_markdown_export(
        self,
        *,
        session_record: MeetingSessionRecord,
        segments: list[MeetingSegmentRecord],
        draft: MeetingMinutesDraft,
        started_after: datetime | None = None,
        started_before: datetime | None = None,
    ) -> str:
        segment_start, segment_end = self._meeting_segment_bounds(segments)
        excerpt_segments = self._resolve_excerpt_segments(
            segments=segments,
            draft=draft,
        )
        lines: list[str] = [
            f"# \u4f1a\u8bae\u7eaa\u8981\uff1a{draft.title or session_record.meeting_title or session_record.meeting_key or session_record.session_id}",
            "",
            "## \u57fa\u672c\u4fe1\u606f",
            "",
            f"- Session ID: `{session_record.session_id}`",
            f"- Account ID: `{session_record.account_id}`",
            f"- Connector: `{session_record.connector_name}`",
            f"- Platform: `{session_record.platform.value}`",
            f"- Meeting Key: `{session_record.meeting_key}`",
            f"- Channel ID: `{session_record.channel_id}`",
            f"- Audio Source: `{session_record.audio_source.value}`" if session_record.audio_source else "- Audio Source: `unknown`",
            f"- Capture Device: `{session_record.capture_device_name}`" if session_record.capture_device_name else "- Capture Device: `unknown`",
            f"- Transcription Backend: `{session_record.transcription_backend}`" if session_record.transcription_backend else "- Transcription Backend: `unknown`",
            f"- \u91c7\u96c6\u8d77\u59cb\u65f6\u95f4: `{self._format_meeting_timestamp(segment_start or session_record.created_at)}`",
            f"- \u91c7\u96c6\u7ed3\u675f\u65f6\u95f4: `{self._format_meeting_timestamp(segment_end or session_record.updated_at)}`",
            f"- \u5bfc\u51fa\u7247\u6bb5\u6570: `{len(segments)}`",
            f"- \u5bfc\u51fa\u8fc7\u6ee4\u8d77\u70b9: `{self._format_meeting_timestamp(started_after)}`" if started_after else "- \u5bfc\u51fa\u8fc7\u6ee4\u8d77\u70b9: `\u672a\u6307\u5b9a`",
            f"- \u5bfc\u51fa\u8fc7\u6ee4\u7ec8\u70b9: `{self._format_meeting_timestamp(started_before)}`" if started_before else "- \u5bfc\u51fa\u8fc7\u6ee4\u7ec8\u70b9: `\u672a\u6307\u5b9a`",
            f"- \u5bfc\u51fa\u6a21\u677f: `{draft.template.value}`",
            f"- \u7eaa\u8981\u751f\u6210\u540e\u7aef: `{draft.backend}`",
            f"- \u7eaa\u8981\u6a21\u578b: `{draft.model}`" if draft.model else "- \u7eaa\u8981\u6a21\u578b: `fallback`",
        ]

        if draft.overview:
            lines.extend(["", "## \u6982\u89c8", "", draft.overview])

        if draft.background:
            lines.extend(["", "## \u4e00\u3001\u80cc\u666f", ""])
            lines.extend(f"- {item}" for item in draft.background)

        if draft.conclusions:
            lines.extend(["", "## \u4e8c\u3001\u7ed3\u8bba", ""])
            lines.extend(f"- {item}" for item in draft.conclusions)

        if draft.action_items:
            lines.extend(["", "## \u4e09\u3001Action Items", ""])
            lines.extend(f"- {item}" for item in draft.action_items)

        if draft.risks:
            lines.extend(["", "## \u56db\u3001\u98ce\u9669\u4e0e\u5f85\u786e\u8ba4", ""])
            lines.extend(f"- {item}" for item in draft.risks)

        lines.extend(["", "## \u4e94\u3001\u539f\u59cb\u6458\u5f55", ""])
        if not excerpt_segments:
            lines.append("_\u5f53\u524d\u5bfc\u51fa\u8303\u56f4\u5185\u6682\u65e0\u53ef\u5c55\u793a\u7684\u539f\u59cb\u6458\u5f55\u3002_")
        else:
            for segment in excerpt_segments:
                lines.append(f"- {self._render_meeting_segment_text_line(segment)}")
                if segment.saved_path:
                    lines.append(f"  Source WAV: `{segment.saved_path}`")

        if draft.template in {MeetingExportTemplate.STANDARD, MeetingExportTemplate.FULL}:
            lines.extend(["", "## \u9644\u5f55\uff1a\u5b8c\u6574\u8f6c\u5199", ""])
            if not segments:
                lines.append("_\u5f53\u524d\u5bfc\u51fa\u8303\u56f4\u5185\u6ca1\u6709\u5df2\u843d\u5e93\u7684\u4f1a\u8bae\u8f6c\u5199\u7247\u6bb5\u3002_")
            else:
                transcript_segments = segments if draft.template == MeetingExportTemplate.FULL else segments[-20:]
                for segment in transcript_segments:
                    lines.append(f"- {self._render_meeting_segment_text_line(segment)}")
                    if segment.saved_path:
                        lines.append(f"  Source WAV: `{segment.saved_path}`")
        lines.append("")
        return "\n".join(lines)
