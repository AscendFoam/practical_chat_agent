from __future__ import annotations

import difflib
from datetime import datetime, timezone
import json
from pathlib import Path
from time import sleep
from typing import Annotated, Optional

import typer
from pydantic import ValidationError

from practical_chat_agent.app.config import get_settings
from practical_chat_agent.app.container import AppContainer
from practical_chat_agent.core.enums import (
    ActionStatus,
    ChannelType,
    ContentType,
    Direction,
    MeetingExportTemplate,
    MeetingAudioSource,
    PersonaType,
    SafetyMode,
    SourceType,
)
from practical_chat_agent.core.models import (
    ActionExecutionRecord,
    AgentProfile,
    ChatContext,
    InboundEvent,
    MeetingLivePreview,
    MeetingMinutesDraft,
    MeetingSegmentRecord,
    MeetingSessionRecord,
    MemoryFact,
    MemoryProfileFacet,
    MemoryProfileRecord,
    MemoryProfileSnapshot,
)
from practical_chat_agent.services.chatlog_ingestion import (
    ChatlogIngestionService,
    ChatlogNormalizationError,
)
from practical_chat_agent.services.conversation_chunking import (
    ConversationChunkingError,
    ConversationChunkingService,
)
from practical_chat_agent.services.chatlog_distillation import (
    ChatlogDistillationError,
    ChatlogDistillationService,
)
from practical_chat_agent.services.contact_skill import (
    ContactSkillBuilderError,
    ContactSkillBuilderService,
    ContactSkillStoreReviewError,
    ContactSkillStoreReviewService,
)
from practical_chat_agent.services.evidence_validation import (
    EvidenceValidationError,
    EvidenceValidationService,
)
from practical_chat_agent.services.meeting_live_loop import MeetingLiveLoopRequest
from practical_chat_agent.services.feedback import (
    FeedbackError,
    FeedbackService,
    FeedbackSummaryService,
    FeedbackValidationService,
)
from practical_chat_agent.services.reply_planner import ReplyPlanner, ReplyPlannerError
from practical_chat_agent.ui.live_caption_window import MeetingLiveCaptionWindow

app = typer.Typer(no_args_is_help=True, add_completion=False)

_DECISION_HINTS = (
    "决定",
    "结论",
    "确认",
    "共识",
    "通过",
    "采用",
    "最终",
    "agreed",
    "decided",
    "confirmed",
    "final",
    "approved",
)

_ACTION_HINTS = (
    "待办",
    "行动",
    "跟进",
    "负责",
    "安排",
    "完成",
    "提交",
    "同步",
    "发送",
    "排期",
    "review",
    "follow up",
    "action",
    "todo",
    "owner",
    "deadline",
)

_RISK_HINTS = (
    "风险",
    "问题",
    "阻塞",
    "卡住",
    "异常",
    "延期",
    "不确定",
    "待确认",
    "依赖",
    "缺少",
    "担心",
    "issue",
    "risk",
    "blocker",
    "concern",
    "unknown",
    "pending",
)

_FIXTURE_TARGET_MARKERS = ("fixture", "stage", "test")


def _default_chatlog_output_dir() -> Path:
    run_id = datetime.now(timezone.utc).strftime("weflow_normalize_%Y%m%d_%H%M%S")
    return Path("private") / "distilled" / run_id


def _safe_cli_path(path: Path | None) -> str | None:
    if path is None:
        return None
    try:
        return str(path.resolve().relative_to(Path.cwd().resolve())).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def _parse_datetime_option(value: Optional[str], *, option_name: str) -> datetime | None:
    if value is None:
        return None
    text = value.strip()
    if not text:
        return None
    normalized = text[:-1] + "+00:00" if text.endswith("Z") else text
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise typer.BadParameter(
            f"Invalid {option_name}: {value}. Use ISO-8601 like 2026-04-18T15:30:00+08:00.",
        ) from exc
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed


def _resolve_meeting_session_id(
    *,
    container: AppContainer,
    session_id: Optional[str],
    latest_for_account: Optional[str],
) -> str:
    resolved_session_id = session_id
    if resolved_session_id is None and latest_for_account:
        sessions = container.meeting_repository.list_sessions(account_id=latest_for_account, limit=1)
        if not sessions:
            raise typer.BadParameter(f"No meeting sessions found for account: {latest_for_account}")
        resolved_session_id = sessions[0].session_id
    if resolved_session_id is None:
        raise typer.BadParameter("Provide SESSION_ID or --latest-for-account.")
    return resolved_session_id


def _resolve_meeting_minutes_record(
    *,
    container: AppContainer,
    minutes_id: str,
):
    record = container.meeting_repository.get_minutes(minutes_id=minutes_id)
    if record is None:
        raise typer.BadParameter(f"Unknown meeting minutes version: {minutes_id}")
    return record


def _format_meeting_timestamp(value: datetime | None) -> str:
    if value is None:
        return "-"
    return value.astimezone().strftime("%Y-%m-%d %H:%M:%S %z")


def _format_action_timestamp(value: datetime | None) -> str:
    if value is None:
        return "-"
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.astimezone().strftime("%Y-%m-%d %H:%M:%S %z")


def _render_action_text_line(action: ActionExecutionRecord) -> str:
    text = " ".join((action.message_text or "").replace("\r", " ").replace("\n", " ").split())
    if len(text) > 90:
        text = f"{text[:87].rstrip()}..."
    if not text:
        text = "<empty>"
    return (
        f"{action.action_id} | {action.status.value} | {action.platform.value} | "
        f"channel={action.channel_id} | created={_format_action_timestamp(action.created_at)} | {text}"
    )


def _render_meeting_segment_text_line(segment: MeetingSegmentRecord) -> str:
    timestamp = segment.display_time or _format_meeting_timestamp(segment.started_at or segment.created_at)
    speaker = segment.speaker_name or "Unknown"
    text = (segment.text or "").replace("\r", " ").replace("\n", " ").strip()
    if not text:
        text = "<empty>"
    return f"[{timestamp}] {speaker}: {text}"


def _render_minutes_markdown(record) -> str:
    lines = [
        f"# 会议纪要版本：{record.title or record.minutes_id}",
        "",
        "## 元数据",
        "",
        f"- Minutes ID: `{record.minutes_id}`",
        f"- Session ID: `{record.session_id}`",
        f"- Template: `{record.template.value}`",
        f"- Backend: `{record.backend}`",
        f"- Model: `{record.model}`" if record.model else "- Model: `fallback`",
        f"- Status: `{record.status}`",
        f"- Output Path: `{record.output_path}`" if record.output_path else "- Output Path: `not_saved`",
        f"- Created At: `{_format_meeting_timestamp(record.created_at)}`",
    ]
    return "\n".join(lines + ["", "## Markdown Body", "", record.markdown_body])


def _clean_meeting_text(text: str | None) -> str:
    return " ".join((text or "").replace("\r", " ").replace("\n", " ").split()).strip()


def _normalize_export_sentence(text: str | None) -> str:
    cleaned = _clean_meeting_text(text)
    if not cleaned:
        return ""
    lowered = cleaned.casefold()
    replacements = {
        "there is not enough transcript yet to summarize the meeting.": "当前会议转写仍然较少，暂时无法形成稳定摘要。",
        "not enough transcript yet. keep listening for more meeting context.": "当前会议转写仍然较少，建议继续采集更多上下文。",
        "no tencent meeting desktop window was detected.": "当前未检测到腾讯会议桌面窗口。",
        "make sure tencent meeting is running and its main meeting window is visible.": "请确认腾讯会议正在运行，且主会议窗口处于可见状态。",
        "do you want a one-sentence checkpoint summary to realign the room?": "是否需要补一条一句话阶段性总结，帮助与会者重新对齐讨论焦点？",
        "separate confirmed decisions from open questions in the meeting notes.": "建议在会后纪要中区分已确认结论与待确认问题。",
    }
    return replacements.get(lowered, cleaned)


def _shorten_meeting_text(text: str, *, limit: int = 140) -> str:
    cleaned = _normalize_export_sentence(text)
    if len(cleaned) <= limit:
        return cleaned
    return f"{cleaned[: max(limit - 3, 1)].rstrip()}..."


def _dedupe_text_items(items: list[str], *, limit: int | None = None) -> list[str]:
    results: list[str] = []
    seen: set[str] = set()
    for item in items:
        cleaned = _normalize_export_sentence(item)
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


def _text_matches_any_hint(text: str, hints: tuple[str, ...]) -> bool:
    lowered = text.casefold()
    return any(hint.casefold() in lowered for hint in hints)


def _build_segment_candidates(
    segments: list[MeetingSegmentRecord],
    *,
    hints: tuple[str, ...],
    limit: int,
) -> list[str]:
    collected: list[str] = []
    for segment in reversed(segments):
        cleaned = _clean_meeting_text(segment.text)
        if not cleaned:
            continue
        if _text_matches_any_hint(cleaned, hints):
            collected.append(_shorten_meeting_text(cleaned))
        if len(collected) >= limit * 2:
            break
    collected.reverse()
    return _dedupe_text_items(collected, limit=limit)


def _meeting_segment_bounds(
    segments: list[MeetingSegmentRecord],
) -> tuple[datetime | None, datetime | None]:
    if not segments:
        return None, None
    started_values = [segment.started_at or segment.created_at for segment in segments]
    ended_values = [segment.ended_at or segment.started_at or segment.created_at for segment in segments]
    return min(started_values), max(ended_values)


def _build_export_background_points(
    *,
    session_record: MeetingSessionRecord,
    segments: list[MeetingSegmentRecord],
) -> list[str]:
    items: list[str] = []
    if session_record.meeting_title:
        items.append(f"本次会议主题为“{session_record.meeting_title}”。")
    if session_record.latest_summary:
        items.append(_normalize_export_sentence(session_record.latest_summary))
    if session_record.notes:
        items.extend(f"系统备注：{_normalize_export_sentence(note)}" for note in session_record.notes[:2])
    if segments:
        first_segment = next((segment for segment in segments if _clean_meeting_text(segment.text)), None)
        if first_segment is not None:
            items.append(f"会议开场上下文：{_shorten_meeting_text(first_segment.text)}")
    if not items:
        items.append("当前导出范围内尚无足够上下文，建议继续采集更多会议转写内容。")
    return _dedupe_text_items(items, limit=4)


def _build_export_conclusion_points(
    *,
    session_record: MeetingSessionRecord,
    segments: list[MeetingSegmentRecord],
) -> list[str]:
    items: list[str] = list(session_record.latest_key_points)
    items.extend(_build_segment_candidates(segments, hints=_DECISION_HINTS, limit=4))
    if not items and session_record.latest_summary:
        items.append(_normalize_export_sentence(session_record.latest_summary))
    if not items:
        items.append("当前导出范围内尚未识别出稳定结论，建议继续观察后续讨论。")
    return _dedupe_text_items(items, limit=5)


def _build_export_action_items(
    *,
    session_record: MeetingSessionRecord,
    segments: list[MeetingSegmentRecord],
) -> list[str]:
    items: list[str] = list(session_record.latest_action_items)
    items.extend(_build_segment_candidates(segments, hints=_ACTION_HINTS, limit=4))
    if not items:
        items.append("当前导出范围内未识别出明确 action item。")
    return _dedupe_text_items(items, limit=5)


def _build_export_risk_points(
    *,
    session_record: MeetingSessionRecord,
    segments: list[MeetingSegmentRecord],
) -> list[str]:
    items: list[str] = list(session_record.latest_follow_up_questions)
    items.extend(_build_segment_candidates(segments, hints=_RISK_HINTS, limit=4))
    question_segments = [
        _shorten_meeting_text(segment.text)
        for segment in reversed(segments)
        if "?" in (segment.text or "") or "？" in (segment.text or "")
    ]
    items.extend(reversed(question_segments[:3]))
    if not segments:
        items.append("当前导出范围内没有会议转写片段，存在信息不完整风险。")
    if session_record.notes:
        items.extend(f"采集侧提示：{_normalize_export_sentence(note)}" for note in session_record.notes[:1])
    if not items:
        items.append("当前导出范围内暂无显著风险或待确认事项。")
    return _dedupe_text_items(items, limit=5)


def _build_export_excerpt_segments(
    segments: list[MeetingSegmentRecord],
    *,
    limit: int = 8,
) -> list[MeetingSegmentRecord]:
    if len(segments) <= limit:
        return segments

    scored: list[tuple[int, int, MeetingSegmentRecord]] = []
    for index, segment in enumerate(segments):
        cleaned = _clean_meeting_text(segment.text)
        if not cleaned:
            continue
        score = min(len(cleaned), 180)
        if _text_matches_any_hint(cleaned, _DECISION_HINTS):
            score += 60
        if _text_matches_any_hint(cleaned, _ACTION_HINTS):
            score += 50
        if _text_matches_any_hint(cleaned, _RISK_HINTS):
            score += 40
        if "?" in cleaned or "？" in cleaned:
            score += 20
        scored.append((score, index, segment))

    chosen = sorted(scored, key=lambda item: (-item[0], item[1]))[:limit]
    chosen_indices = {index for _, index, _ in chosen}
    return [segment for index, segment in enumerate(segments) if index in chosen_indices]


def _build_minutes_draft_fallback(
    *,
    session_record: MeetingSessionRecord,
    segments: list[MeetingSegmentRecord],
    template: MeetingExportTemplate,
) -> MeetingMinutesDraft:
    background_points = _build_export_background_points(
        session_record=session_record,
        segments=segments,
    )
    conclusion_points = _build_export_conclusion_points(
        session_record=session_record,
        segments=segments,
    )
    action_items = _build_export_action_items(
        session_record=session_record,
        segments=segments,
    )
    risk_points = _build_export_risk_points(
        session_record=session_record,
        segments=segments,
    )
    excerpt_segments = _build_export_excerpt_segments(segments, limit=8)
    overview = _normalize_export_sentence(session_record.latest_summary)
    if not overview:
        overview = background_points[0] if background_points else "当前导出范围内尚无足够上下文。"
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
    return _build_export_excerpt_segments(segments, limit=fallback_limit)


def _build_meeting_markdown_export(
    *,
    session_record: MeetingSessionRecord,
    segments: list[MeetingSegmentRecord],
    draft: MeetingMinutesDraft,
    started_after: datetime | None = None,
    started_before: datetime | None = None,
) -> str:
    segment_start, segment_end = _meeting_segment_bounds(segments)
    excerpt_segments = _resolve_excerpt_segments(
        segments=segments,
        draft=draft,
    )
    lines: list[str] = [
        f"# 会议纪要：{draft.title or session_record.meeting_title or session_record.meeting_key or session_record.session_id}",
        "",
        "## 基本信息",
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
        f"- 采集起始时间: `{_format_meeting_timestamp(segment_start or session_record.created_at)}`",
        f"- 采集结束时间: `{_format_meeting_timestamp(segment_end or session_record.updated_at)}`",
        f"- 导出片段数: `{len(segments)}`",
        f"- 导出过滤起点: `{_format_meeting_timestamp(started_after)}`" if started_after else "- 导出过滤起点: `未指定`",
        f"- 导出过滤终点: `{_format_meeting_timestamp(started_before)}`" if started_before else "- 导出过滤终点: `未指定`",
        f"- 导出模板: `{draft.template.value}`",
        f"- 纪要生成后端: `{draft.backend}`",
        f"- 纪要模型: `{draft.model}`" if draft.model else "- 纪要模型: `fallback`",
    ]

    if draft.overview:
        lines.extend(["", "## 概览", "", draft.overview])

    if draft.background:
        lines.extend(["", "## 一、背景", ""])
        lines.extend(f"- {item}" for item in draft.background)

    if draft.conclusions:
        lines.extend(["", "## 二、结论", ""])
        lines.extend(f"- {item}" for item in draft.conclusions)

    if draft.action_items:
        lines.extend(["", "## 三、Action Items", ""])
        lines.extend(f"- {item}" for item in draft.action_items)

    if draft.risks:
        lines.extend(["", "## 四、风险与待确认", ""])
        lines.extend(f"- {item}" for item in draft.risks)

    lines.extend(["", "## 五、原始摘录", ""])
    if not excerpt_segments:
        lines.append("_当前导出范围内暂无可展示的原始摘录。_")
    else:
        for segment in excerpt_segments:
            lines.append(f"- {_render_meeting_segment_text_line(segment)}")
            if segment.saved_path:
                lines.append(f"  Source WAV: `{segment.saved_path}`")

    if draft.template in {MeetingExportTemplate.STANDARD, MeetingExportTemplate.FULL}:
        lines.extend(["", "## 附录：完整转写", ""])
        if not segments:
            lines.append("_当前导出范围内没有已落库的会议转写片段。_")
        else:
            transcript_segments = segments if draft.template == MeetingExportTemplate.FULL else segments[-20:]
            for segment in transcript_segments:
                lines.append(f"- {_render_meeting_segment_text_line(segment)}")
                if segment.saved_path:
                    lines.append(f"  Source WAV: `{segment.saved_path}`")
    lines.append("")
    return "\n".join(lines)


def _load_meeting_segments(
    *,
    container: AppContainer,
    session_id: str,
    latest: Optional[int],
    started_after: Optional[str],
    started_before: Optional[str],
) -> tuple[list[MeetingSegmentRecord], datetime | None, datetime | None]:
    started_after_dt = _parse_datetime_option(started_after, option_name="--started-after")
    started_before_dt = _parse_datetime_option(started_before, option_name="--started-before")
    if started_after_dt is not None and started_before_dt is not None and started_after_dt > started_before_dt:
        raise typer.BadParameter("--started-after cannot be later than --started-before.")

    segments = container.meeting_repository.list_segments(
        session_id=session_id,
        limit=None,
        started_after=started_after_dt,
        started_before=started_before_dt,
    )
    if latest is not None:
        segments = segments[-latest:]
    return segments, started_after_dt, started_before_dt


def _render_memory_text_line(memory) -> str:
    return (
        f"[{memory.memory_id}] user={memory.user_id} "
        f"type={memory.memory_type.value} salience={memory.salience:.2f} "
        f"confidence={memory.confidence:.2f} fact={memory.fact}"
    )


def _collect_fixture_records(
    *,
    container: AppContainer,
    agent_id: str,
    user_id: str,
    limit: int,
) -> tuple[list[MemoryFact], list[MemoryProfileRecord]]:
    memories = container.memory_lifecycle_service.list_memories(
        agent_id=agent_id,
        user_id=user_id,
        limit=limit,
    )
    profiles = container.memory_lifecycle_service.list_profile_snapshots(
        agent_id=agent_id,
        user_id=user_id,
        limit=limit,
    )
    return memories, profiles


def _looks_like_fixture_target(user_id: str, memories: list[MemoryFact], profiles: list[MemoryProfileRecord]) -> bool:
    searchable_values = [user_id]
    searchable_values.extend(memory.memory_id for memory in memories)
    searchable_values.extend(ref for memory in memories for ref in memory.evidence_refs)
    searchable_values.extend(profile.profile_id for profile in profiles)
    searchable_values.extend(profile.backend for profile in profiles)
    return any(
        marker in value.casefold()
        for value in searchable_values
        for marker in _FIXTURE_TARGET_MARKERS
    )


def _render_memory_duplicate_group_lines(group) -> list[str]:
    lines = [
        (
            f"group user={group.user_id} type={group.memory_type.value} "
            f"keep={group.canonical_memory_id} similarity={group.similarity_score:.2f}"
        ),
        f"canonical: {group.canonical_fact}",
    ]
    if group.facet_title:
        facet_bits = [f"facet={group.facet_title}"]
        if group.facet_family_key:
            facet_bits.append(f"family={group.facet_family_key}")
        if group.facet_confidence is not None:
            facet_bits.append(f"confidence={group.facet_confidence:.2f}")
        lines.append(" ".join(facet_bits))
    if group.facet_summary:
        lines.append(f"facet_summary: {group.facet_summary}")
    if group.merged_fact_preview:
        lines.append(f"final_preview: {group.merged_fact_preview}")
    if group.canonicalization_strategy:
        lines.append(f"canonicalization_strategy: {group.canonicalization_strategy}")
    if group.canonicalization_reason:
        lines.append(f"canonicalization_reason: {group.canonicalization_reason}")
    if (
        group.baseline_merge_preview
        and group.merged_fact_preview
        and group.baseline_merge_preview != group.merged_fact_preview
    ):
        lines.append(f"baseline_merge_preview: {group.baseline_merge_preview}")
    for memory_id, fact in zip(group.memory_ids, group.facts):
        lines.append(f"- {memory_id}: {fact}")
    return lines


def _emit_memory_consolidation_text(result) -> None:
    typer.echo(
        f"agent={result.agent_id} user={result.user_id or '*'} reviewed={result.reviewed_count} "
        f"merged_groups={result.merged_group_count} dry_run={result.dry_run}",
    )
    for note in result.notes:
        typer.echo(f"note: {note}")
    for group in result.duplicate_groups:
        for line in _render_memory_duplicate_group_lines(group):
            typer.echo(line)
    for memory in result.updated_memories:
        typer.echo(f"upsert: {_render_memory_text_line(memory)}")
    if result.deleted_memory_ids:
        typer.echo(f"delete_ids: {', '.join(result.deleted_memory_ids)}")


def _emit_profile_snapshot_text(profile) -> None:
    typer.echo(
        f"profile_id={profile.profile_id} agent={profile.agent_id} user={profile.user_id} "
        f"backend={profile.backend} model={profile.model or 'fallback'} memories={profile.memory_count}",
    )
    typer.echo(f"created_at: {profile.created_at.astimezone().strftime('%Y-%m-%d %H:%M:%S %z')}")
    if profile.source_event_id:
        typer.echo(f"source_event_id: {profile.source_event_id}")
    if profile.summary:
        typer.echo(f"summary: {profile.summary}")
    if profile.snapshot.facets:
        typer.echo("facets:")
        for facet in profile.snapshot.facets:
            intents = ", ".join(intent.value for intent in facet.preferred_intents) or "general"
            typer.echo(
                f"- [{facet.facet_type}] {facet.title} "
                f"(confidence={facet.confidence:.2f}; intents={intents})",
            )
            typer.echo(f"  summary: {facet.summary}")
            if facet.tags:
                typer.echo(f"  tags: {', '.join(facet.tags)}")
            if facet.evidence_memory_ids:
                typer.echo(f"  evidence_ids: {', '.join(facet.evidence_memory_ids)}")


def _emit_fixture_cleanup_preview(
    *,
    agent_id: str,
    user_id: str,
    memories: list[MemoryFact],
    profiles: list[MemoryProfileRecord],
    dry_run: bool,
) -> None:
    typer.echo(
        f"fixture_cleanup agent={agent_id} user={user_id} dry_run={dry_run} "
        f"memory_count={len(memories)} profile_count={len(profiles)}",
    )
    if not memories and not profiles:
        typer.echo("(no fixture records found)")
        return
    if profiles:
        typer.echo("profiles:")
        for profile in profiles:
            typer.echo(
                f"- {profile.profile_id} created_at={profile.created_at.astimezone().strftime('%Y-%m-%d %H:%M:%S %z')} "
                f"backend={profile.backend} memories={profile.memory_count}",
            )
    if memories:
        typer.echo("memories:")
        for memory in memories:
            typer.echo(f"- {_render_memory_text_line(memory)}")


def _profile_snapshot_collection_map(snapshot: MemoryProfileSnapshot) -> dict[str, list[str]]:
    return {
        "preferences": snapshot.preferences,
        "facts": snapshot.facts,
        "relationships": snapshot.relationships,
        "reflections": snapshot.reflections,
    }


def _facet_identity_key(facet: MemoryProfileFacet) -> tuple[str, str]:
    return (facet.facet_type.casefold(), facet.title.casefold())


def _render_profile_snapshot_diff_lines(
    older: MemoryProfileRecord,
    newer: MemoryProfileRecord,
) -> list[str]:
    change_found = False
    lines = [
        (
            f"profile_diff older={older.profile_id} newer={newer.profile_id} "
            f"user={newer.user_id} agent={newer.agent_id}"
        ),
        (
            f"created_at: {older.created_at.astimezone().strftime('%Y-%m-%d %H:%M:%S %z')} "
            f"-> {newer.created_at.astimezone().strftime('%Y-%m-%d %H:%M:%S %z')}"
        ),
        f"memory_count: {older.memory_count} -> {newer.memory_count}",
    ]
    if older.summary != newer.summary:
        change_found = True
        if older.summary:
            lines.append(f"summary_old: {older.summary}")
        if newer.summary:
            lines.append(f"summary_new: {newer.summary}")
        summary_diff = list(
            difflib.unified_diff(
                (older.summary or "").splitlines() or [""],
                (newer.summary or "").splitlines() or [""],
                fromfile=older.profile_id,
                tofile=newer.profile_id,
                lineterm="",
            ),
        )
        if summary_diff:
            lines.append("summary_diff:")
            lines.extend(summary_diff)

    older_collections = _profile_snapshot_collection_map(older.snapshot)
    newer_collections = _profile_snapshot_collection_map(newer.snapshot)
    for label in ("preferences", "facts", "relationships", "reflections"):
        old_items = older_collections[label]
        new_items = newer_collections[label]
        old_set = {item.casefold(): item for item in old_items}
        new_set = {item.casefold(): item for item in new_items}
        added = [new_set[key] for key in new_set.keys() - old_set.keys()]
        removed = [old_set[key] for key in old_set.keys() - new_set.keys()]
        if not added and not removed:
            continue
        change_found = True
        lines.append(f"{label}:")
        for item in sorted(added, key=str.casefold):
            lines.append(f"+ {item}")
        for item in sorted(removed, key=str.casefold):
            lines.append(f"- {item}")

    older_facets = {_facet_identity_key(facet): facet for facet in older.snapshot.facets}
    newer_facets = {_facet_identity_key(facet): facet for facet in newer.snapshot.facets}
    facet_added_keys = sorted(newer_facets.keys() - older_facets.keys())
    facet_removed_keys = sorted(older_facets.keys() - newer_facets.keys())
    common_facet_keys = sorted(older_facets.keys() & newer_facets.keys())

    facet_lines: list[str] = []
    for key in facet_added_keys:
        change_found = True
        facet = newer_facets[key]
        intents = ", ".join(intent.value for intent in facet.preferred_intents) or "general"
        facet_lines.append(
            f"+ [{facet.facet_type}] {facet.title} | summary={facet.summary} "
            f"| confidence={facet.confidence:.2f} | intents={intents}",
        )
    for key in facet_removed_keys:
        change_found = True
        facet = older_facets[key]
        intents = ", ".join(intent.value for intent in facet.preferred_intents) or "general"
        facet_lines.append(
            f"- [{facet.facet_type}] {facet.title} | summary={facet.summary} "
            f"| confidence={facet.confidence:.2f} | intents={intents}",
        )
    for key in common_facet_keys:
        older_facet = older_facets[key]
        newer_facet = newer_facets[key]
        facet_changes: list[str] = []
        if older_facet.summary != newer_facet.summary:
            facet_changes.append("summary")
        if round(older_facet.confidence, 3) != round(newer_facet.confidence, 3):
            facet_changes.append(
                f"confidence {older_facet.confidence:.2f}->{newer_facet.confidence:.2f}",
            )
        older_tags = sorted(tag.casefold() for tag in older_facet.tags)
        newer_tags = sorted(tag.casefold() for tag in newer_facet.tags)
        if older_tags != newer_tags:
            facet_changes.append("tags")
        older_intents = [intent.value for intent in older_facet.preferred_intents]
        newer_intents = [intent.value for intent in newer_facet.preferred_intents]
        if older_intents != newer_intents:
            facet_changes.append("preferred_intents")
        older_evidence = older_facet.evidence_memory_ids
        newer_evidence = newer_facet.evidence_memory_ids
        if older_evidence != newer_evidence:
            facet_changes.append("evidence_memory_ids")
        if not facet_changes:
            continue
        change_found = True
        facet_lines.append(
            f"~ [{newer_facet.facet_type}] {newer_facet.title}: {', '.join(facet_changes)}",
        )
        if older_facet.summary != newer_facet.summary:
            facet_lines.append(f"  old_summary: {older_facet.summary}")
            facet_lines.append(f"  new_summary: {newer_facet.summary}")
        if older_tags != newer_tags:
            facet_lines.append(
                f"  tags: {', '.join(older_facet.tags) or '-'} -> {', '.join(newer_facet.tags) or '-'}",
            )
        if older_intents != newer_intents:
            facet_lines.append(
                "  preferred_intents: "
                f"{', '.join(older_intents) or 'general'} -> {', '.join(newer_intents) or 'general'}",
            )
        if older_evidence != newer_evidence:
            facet_lines.append(
                "  evidence_ids: "
                f"{', '.join(older_evidence) or '-'} -> {', '.join(newer_evidence) or '-'}",
            )

    if facet_lines:
        lines.append("facets:")
        lines.extend(facet_lines)

    if not change_found and older.memory_count == newer.memory_count:
        lines.append("No profile changes detected.")
    return lines


@app.command("show-config")
def show_config() -> None:
    """Print the effective runtime configuration without secrets."""

    settings = get_settings()
    safe_config = {
        "app_env": settings.app_env,
        "app_name": settings.app_name,
        "mysql_host": settings.mysql_host,
        "mysql_port": settings.mysql_port,
        "mysql_database": settings.mysql_database,
        "mysql_user": settings.mysql_user,
        "mysql_echo": settings.mysql_echo,
        "openai_base_url": settings.openai_base_url,
        "openai_api_key_present": bool(settings.openai_api_key),
        "chat_context_recent_events": settings.chat_context_recent_events,
        "chat_context_memory_hits": settings.chat_context_memory_hits,
        "chat_suggestion_enabled": settings.chat_suggestion_enabled,
        "chat_suggestion_model": settings.chat_suggestion_model,
        "chat_suggestion_timeout_seconds": settings.chat_suggestion_timeout_seconds,
        "chat_memory_enabled": settings.chat_memory_enabled,
        "chat_memory_model": settings.chat_memory_model,
        "chat_memory_timeout_seconds": settings.chat_memory_timeout_seconds,
        "chat_profile_facets_enabled": settings.chat_profile_facets_enabled,
        "chat_profile_facets_model": settings.chat_profile_facets_model,
        "chat_profile_facets_timeout_seconds": settings.chat_profile_facets_timeout_seconds,
        "telegram_delivery_enabled": settings.telegram_delivery_enabled,
        "telegram_bot_token_present": bool(settings.telegram_bot_token),
        "telegram_delivery_timeout_seconds": settings.telegram_delivery_timeout_seconds,
        "outbound_quiet_hours_start": settings.outbound_quiet_hours_start,
        "outbound_quiet_hours_end": settings.outbound_quiet_hours_end,
        "outbound_policy_timezone": settings.outbound_policy_timezone,
        "outbound_frequency_limit_count": settings.outbound_frequency_limit_count,
        "outbound_frequency_limit_window_seconds": settings.outbound_frequency_limit_window_seconds,
        "outbound_group_chat_draft_only": settings.outbound_group_chat_draft_only,
        "meeting_assistant_enabled": settings.meeting_assistant_enabled,
        "meeting_assistant_model": settings.meeting_assistant_model,
        "meeting_assistant_timeout_seconds": settings.meeting_assistant_timeout_seconds,
        "meeting_minutes_rewriter_enabled": settings.meeting_minutes_rewriter_enabled,
        "meeting_minutes_model": settings.meeting_minutes_model,
        "meeting_minutes_timeout_seconds": settings.meeting_minutes_timeout_seconds,
        "meeting_minutes_context_segments": settings.meeting_minutes_context_segments,
        "meeting_assistant_context_segments": settings.meeting_assistant_context_segments,
        "meeting_live_window_alpha": settings.meeting_live_window_alpha,
        "glm_ocr_model": settings.glm_ocr_model,
        "glm_ocr_api_key_present": bool(settings.glm_ocr_api_key),
        "desktop_ocr_enabled": settings.desktop_ocr_enabled,
        "desktop_capture_debug_dir": settings.desktop_capture_debug_dir,
        "meeting_transcribe_model": settings.meeting_transcribe_model,
        "meeting_transcribe_api_key_present": bool(settings.meeting_transcribe_api_key),
        "meeting_transcribe_enabled": settings.meeting_transcribe_enabled,
        "meeting_transcribe_empty_retry_enabled": settings.meeting_transcribe_empty_retry_enabled,
        "meeting_capture_debug_dir": settings.meeting_capture_debug_dir,
        "meeting_audio_silence_threshold": settings.meeting_audio_silence_threshold,
        "meeting_microphone_boost_gain": settings.meeting_microphone_boost_gain,
        "meeting_microphone_peak_target": settings.meeting_microphone_peak_target,
        "meeting_microphone_silence_floor": settings.meeting_microphone_silence_floor,
        "meeting_microphone_highpass_cutoff_hz": settings.meeting_microphone_highpass_cutoff_hz,
        "meeting_microphone_trim_padding_seconds": settings.meeting_microphone_trim_padding_seconds,
        "meeting_microphone_compressor_threshold": settings.meeting_microphone_compressor_threshold,
        "meeting_microphone_compressor_ratio": settings.meeting_microphone_compressor_ratio,
        "meeting_microphone_limiter_ceiling": settings.meeting_microphone_limiter_ceiling,
        "meeting_loopback_preferred_speaker_name": settings.meeting_loopback_preferred_speaker_name,
        "meeting_microphone_preferred_device_name": settings.meeting_microphone_preferred_device_name,
    }
    typer.echo(json.dumps(safe_config, indent=2))


@app.command("init-db")
def init_db() -> None:
    """Create the MySQL database if missing and apply the initial schema."""

    container = AppContainer.build()
    container.init_database()
    typer.echo("Database schema initialized.")


@app.command("create-agent")
def create_agent(
    agent_id: Annotated[str, typer.Argument(help="Stable agent identifier.")],
    display_name: Annotated[str, typer.Argument(help="Display name shown by the agent.")],
    persona_type: Annotated[PersonaType, typer.Option(help="Configured persona flavor.")] = PersonaType.FRIEND,
    safety_mode: Annotated[SafetyMode, typer.Option(help="Safety posture for the agent.")] = SafetyMode.DISCLOSED_AI,
) -> None:
    """Persist a minimal agent profile in the repository."""

    container = AppContainer.build()
    profile = AgentProfile(
        agent_id=agent_id,
        display_name=display_name,
        persona_type=persona_type,
        safety_mode=safety_mode,
    )
    container.agent_repository.upsert(profile)
    typer.echo(f"Agent '{agent_id}' saved.")


@app.command("demo-turn")
def demo_turn(
    payload_path: Annotated[Path, typer.Argument(help="Path to a JSON payload file.")],
    connector_name: Annotated[
        Optional[str],
        typer.Option(help="Inbound connector to use. If omitted, the service resolves it from file metadata or payload shape."),
    ] = None,
) -> None:
    """Load a JSON payload file and run it through the connector-based ingress flow."""

    container = AppContainer.build()
    payload = json.loads(payload_path.read_text(encoding="utf-8"))
    result = container.inbound_service.ingest(connector_name=connector_name, payload=payload)
    typer.echo(json.dumps(result.model_dump(mode="json"), indent=2))


@app.command("replay-payload-dir")
def replay_payload_dir(
    payload_dir: Annotated[Path, typer.Argument(help="Directory containing JSON payload files.")],
    connector_name: Annotated[
        Optional[str],
        typer.Option(help="Fallback connector. Each file can also specify connector_name in payload metadata."),
    ] = None,
) -> None:
    """Replay every JSON payload file in a directory through the ingress flow."""

    container = AppContainer.build()
    json_files = sorted(path for path in payload_dir.iterdir() if path.is_file() and path.suffix.lower() == ".json")
    if not json_files:
        raise typer.BadParameter(f"No JSON payload files found in {payload_dir}")

    results: list[dict[str, object]] = []
    for payload_path in json_files:
        try:
            payload = json.loads(payload_path.read_text(encoding="utf-8"))
            resolved_connector = container.inbound_service.resolve_connector_name(
                payload=payload,
                connector_name=connector_name,
            )
            turn_result = container.inbound_service.ingest(
                connector_name=resolved_connector,
                payload=payload,
            )
            results.append(
                {
                    "file": str(payload_path),
                    "status": "ok",
                    "connector_name": resolved_connector,
                    "event_id": turn_result.event_id,
                    "should_reply": turn_result.should_reply,
                    "action_count": len(turn_result.actions),
                    "suggestion_count": len(turn_result.suggestions),
                    "memory_update_count": len(turn_result.memory_updates),
                    "no_reply_reason": turn_result.no_reply_reason,
                    "suggestion_backend": turn_result.suggestions[0].backend if turn_result.suggestions else None,
                    "suggestion_model": turn_result.suggestions[0].model if turn_result.suggestions else None,
                    "memory_update_ids": [memory.memory_id for memory in turn_result.memory_updates],
                },
            )
        except Exception as exc:  # noqa: BLE001
            results.append(
                {
                    "file": str(payload_path),
                    "status": "error",
                    "error": str(exc),
                },
            )

    typer.echo(
        json.dumps(
            {
                "default_connector_name": connector_name,
                "processed_files": len(results),
                "success_count": sum(1 for item in results if item["status"] == "ok"),
                "error_count": sum(1 for item in results if item["status"] == "error"),
                "results": results,
            },
            indent=2,
        ),
    )


@app.command("action-list")
def action_list(
    agent_id: Annotated[
        Optional[str],
        typer.Option(help="Optional agent id filter."),
    ] = None,
    status: Annotated[
        Optional[ActionStatus],
        typer.Option(help="Optional action status filter."),
    ] = None,
    channel_id: Annotated[
        Optional[str],
        typer.Option(help="Optional channel id filter."),
    ] = None,
    limit: Annotated[
        int,
        typer.Option(help="Maximum number of actions to return."),
    ] = 20,
    text_only: Annotated[
        bool,
        typer.Option("--text-only", help="Print concise action rows instead of JSON."),
    ] = False,
) -> None:
    """List recent outbound action records from the outbox."""

    container = AppContainer.build()
    actions = container.action_repository.list_recent(
        agent_id=agent_id,
        status=status.value if status is not None else None,
        channel_id=channel_id,
        limit=limit,
    )
    if text_only:
        for action in actions:
            typer.echo(_render_action_text_line(action))
        if not actions:
            typer.echo("(no actions)")
        return
    typer.echo(
        json.dumps(
            {
                "agent_id": agent_id,
                "status": status.value if status is not None else None,
                "channel_id": channel_id,
                "count": len(actions),
                "actions": [action.model_dump(mode="json") for action in actions],
            },
            indent=2,
        ),
    )


@app.command("action-show")
def action_show(
    action_id: Annotated[str, typer.Argument(help="Action id to inspect.")],
    text_only: Annotated[
        bool,
        typer.Option("--text-only", help="Print a concise human-readable view instead of JSON."),
    ] = False,
) -> None:
    """Show one outbound action record with policy and delivery metadata."""

    container = AppContainer.build()
    action = container.action_repository.get(action_id)
    if action is None:
        raise typer.BadParameter(f"Unknown action: {action_id}")
    if text_only:
        typer.echo(_render_action_text_line(action))
        typer.echo(f"kind: {action.kind.value}")
        typer.echo(f"requires_approval: {action.requires_approval}")
        typer.echo(f"policy: {action.policy_decision.reason or '-'}")
        if action.policy_decision.risk_flags:
            typer.echo(f"risk_flags: {', '.join(action.policy_decision.risk_flags)}")
        typer.echo("message:")
        typer.echo(action.message_text or "")
        if action.error_message:
            typer.echo(f"error: {action.error_message}")
        return
    typer.echo(json.dumps(action.model_dump(mode="json"), indent=2))


@app.command("action-approve")
def action_approve(
    action_id: Annotated[str, typer.Argument(help="Action id to approve.")],
) -> None:
    """Approve a pending outbound action for later official-platform sending."""

    container = AppContainer.build()
    try:
        action = container.action_delivery_service.approve(action_id=action_id)
    except ValueError as exc:
        raise typer.BadParameter(str(exc)) from exc
    typer.echo(json.dumps(action.model_dump(mode="json"), indent=2))


@app.command("action-send")
def action_send(
    action_id: Annotated[str, typer.Argument(help="Approved action id to send.")],
) -> None:
    """Send an approved outbound action through the registered official platform connector."""

    container = AppContainer.build()
    try:
        action = container.action_delivery_service.send(action_id=action_id)
    except (RuntimeError, ValueError) as exc:
        raise typer.BadParameter(str(exc)) from exc
    typer.echo(json.dumps(action.model_dump(mode="json"), indent=2))


@app.command("memory-list")
def memory_list(
    agent_id: Annotated[str, typer.Argument(help="Agent id whose memories should be listed.")],
    user_id: Annotated[
        Optional[str],
        typer.Option(help="Optional user id filter."),
    ] = None,
    limit: Annotated[
        int,
        typer.Option(help="Maximum number of memory rows to return."),
    ] = 50,
    text_only: Annotated[
        bool,
        typer.Option("--text-only", help="Print concise plain-text memory rows instead of JSON."),
    ] = False,
) -> None:
    """List persisted long-term memories for an agent."""

    container = AppContainer.build()
    memories = container.memory_lifecycle_service.list_memories(
        agent_id=agent_id,
        user_id=user_id,
        limit=limit,
    )
    if text_only:
        typer.echo(f"agent={agent_id} user={user_id or '*'} count={len(memories)}")
        if not memories:
            typer.echo("(no memories)")
            return
        for memory in memories:
            typer.echo(_render_memory_text_line(memory))
        return
    typer.echo(
        json.dumps(
            {
                "agent_id": agent_id,
                "user_id": user_id,
                "count": len(memories),
                "memories": [memory.model_dump(mode="json") for memory in memories],
            },
            indent=2,
        ),
    )


@app.command("memory-review")
def memory_review(
    agent_id: Annotated[str, typer.Argument(help="Agent id whose memories should be reviewed.")],
    user_id: Annotated[
        Optional[str],
        typer.Option(help="Optional user id filter."),
    ] = None,
    limit: Annotated[
        int,
        typer.Option(help="Maximum number of memory rows to scan."),
    ] = 200,
    text_only: Annotated[
        bool,
        typer.Option("--text-only", help="Print a concise duplicate-review summary instead of JSON."),
    ] = False,
) -> None:
    """Review likely duplicate long-term memory records."""

    container = AppContainer.build()
    review = container.memory_lifecycle_service.review(
        agent_id=agent_id,
        user_id=user_id,
        limit=limit,
    )
    if text_only:
        typer.echo(
            f"agent={review.agent_id} user={review.user_id or '*'} "
            f"memories={review.memory_count} duplicate_groups={review.duplicate_group_count}",
        )
        if review.profile_snapshot is not None:
            typer.echo(
                f"profile_snapshot={review.profile_snapshot.profile_id} "
                f"facets={len(review.profile_snapshot.snapshot.facets)}",
            )
        for note in review.notes:
            typer.echo(f"note: {note}")
        for group in review.duplicate_groups:
            for line in _render_memory_duplicate_group_lines(group):
                typer.echo(line)
        return
    typer.echo(json.dumps(review.model_dump(mode="json"), indent=2))


@app.command("memory-profile-show")
def memory_profile_show(
    agent_id: Annotated[str, typer.Argument(help="Agent id whose latest profile snapshot should be shown.")],
    user_id: Annotated[str, typer.Option(help="User id whose profile snapshot should be shown.")],
    profile_id: Annotated[
        Optional[str],
        typer.Option(help="Optional explicit profile snapshot id. If omitted, show the latest snapshot."),
    ] = None,
    text_only: Annotated[
        bool,
        typer.Option("--text-only", help="Print a concise plain-text profile snapshot view instead of JSON."),
    ] = False,
) -> None:
    """Show one persisted memory profile snapshot for a user."""

    container = AppContainer.build()
    if profile_id:
        profile = container.memory_repository.get_profile_snapshot(profile_id)
        if profile is None:
            raise typer.BadParameter(f"Unknown memory profile snapshot: {profile_id}")
        if profile.agent_id != agent_id or profile.user_id != user_id:
            raise typer.BadParameter("The requested profile snapshot does not match the provided agent_id/user_id.")
    else:
        profile = container.memory_lifecycle_service.get_latest_profile_snapshot(
            agent_id=agent_id,
            user_id=user_id,
        )
        if profile is None:
            raise typer.BadParameter(f"No memory profile snapshots found for {agent_id}/{user_id}.")
    if text_only:
        _emit_profile_snapshot_text(profile)
        return
    typer.echo(json.dumps(profile.model_dump(mode="json"), indent=2))


@app.command("memory-profile-history")
def memory_profile_history(
    agent_id: Annotated[str, typer.Argument(help="Agent id whose profile snapshot history should be listed.")],
    user_id: Annotated[str, typer.Option(help="User id whose profile snapshot history should be listed.")],
    limit: Annotated[
        int,
        typer.Option(help="Maximum number of profile snapshots to return."),
    ] = 20,
    diff_latest: Annotated[
        bool,
        typer.Option(help="Also show a diff between the latest two profile snapshots."),
    ] = False,
    compare_profile_ids: Annotated[
        Optional[str],
        typer.Option(
            "--compare-profile-ids",
            help="Explicit pair of profile ids to diff, formatted as OLD_ID,NEW_ID.",
        ),
    ] = None,
    text_only: Annotated[
        bool,
        typer.Option("--text-only", help="Print concise plain-text profile snapshot rows instead of JSON."),
    ] = False,
) -> None:
    """List persisted memory profile snapshot versions for a user."""

    container = AppContainer.build()
    profiles = container.memory_lifecycle_service.list_profile_snapshots(
        agent_id=agent_id,
        user_id=user_id,
        limit=limit,
    )
    diff_profiles: tuple[MemoryProfileRecord, MemoryProfileRecord] | None = None
    if compare_profile_ids:
        raw_parts = [part.strip() for part in compare_profile_ids.split(",")]
        if len(raw_parts) != 2 or not all(raw_parts):
            raise typer.BadParameter("--compare-profile-ids must be formatted as OLD_ID,NEW_ID.")
        older = container.memory_repository.get_profile_snapshot(raw_parts[0])
        newer = container.memory_repository.get_profile_snapshot(raw_parts[1])
        if older is None or newer is None:
            raise typer.BadParameter("One or both profile ids in --compare-profile-ids do not exist.")
        if older.agent_id != agent_id or older.user_id != user_id:
            raise typer.BadParameter("The old profile id does not match the provided agent_id/user_id.")
        if newer.agent_id != agent_id or newer.user_id != user_id:
            raise typer.BadParameter("The new profile id does not match the provided agent_id/user_id.")
        diff_profiles = (older, newer)
    elif diff_latest and len(profiles) >= 2:
        diff_profiles = (profiles[1], profiles[0])

    if text_only:
        typer.echo(f"agent={agent_id} user={user_id} count={len(profiles)}")
        if not profiles:
            typer.echo("(no profile snapshots)")
            return
        for profile in profiles:
            _emit_profile_snapshot_text(profile)
        if diff_latest and len(profiles) < 2 and not compare_profile_ids:
            typer.echo("profile_diff: need at least two snapshots to diff latest versions.")
        if diff_profiles is not None:
            typer.echo("")
            for line in _render_profile_snapshot_diff_lines(*diff_profiles):
                typer.echo(line)
        return
    typer.echo(
        json.dumps(
            {
                "agent_id": agent_id,
                "user_id": user_id,
                "count": len(profiles),
                "profiles": [profile.model_dump(mode="json") for profile in profiles],
                "diff": (
                    {
                        "older_profile_id": diff_profiles[0].profile_id,
                        "newer_profile_id": diff_profiles[1].profile_id,
                        "lines": _render_profile_snapshot_diff_lines(*diff_profiles),
                    }
                    if diff_profiles is not None
                    else None
                ),
            },
            indent=2,
        ),
    )


@app.command("memory-consolidate")
def memory_consolidate(
    agent_id: Annotated[str, typer.Argument(help="Agent id whose memories should be consolidated.")],
    user_id: Annotated[
        Optional[str],
        typer.Option(help="Optional user id filter."),
    ] = None,
    limit: Annotated[
        int,
        typer.Option(help="Maximum number of memory rows to scan."),
    ] = 200,
    apply: bool = typer.Option(
        False,
        "--apply",
        help="Persist consolidation changes after showing a preview and confirmation prompt.",
    ),
    text_only: Annotated[
        bool,
        typer.Option("--text-only", help="Print a concise consolidation summary instead of JSON."),
    ] = False,
) -> None:
    """Consolidate likely duplicate long-term memory records."""

    container = AppContainer.build()
    preview = container.memory_lifecycle_service.consolidate(
        agent_id=agent_id,
        user_id=user_id,
        limit=limit,
        dry_run=True,
    )
    if apply:
        _emit_memory_consolidation_text(preview)
        if not preview.duplicate_groups:
            return
        confirmed = typer.confirm(
            "Apply these consolidation changes to the database?",
            default=False,
            show_default=True,
        )
        if not confirmed:
            typer.echo("Aborted. No memory rows were modified.")
            return
        result = container.memory_lifecycle_service.consolidate(
            agent_id=agent_id,
            user_id=user_id,
            limit=limit,
            dry_run=False,
        )
    else:
        result = preview
    if text_only:
        _emit_memory_consolidation_text(result)
        return
    typer.echo(json.dumps(result.model_dump(mode="json"), indent=2))


@app.command("memory-fixture-cleanup")
def memory_fixture_cleanup(
    agent_id: Annotated[str, typer.Argument(help="Agent id whose fixture data should be cleaned.")],
    user_id: Annotated[str, typer.Option(help="User id whose fixture data should be cleaned.")],
    limit: Annotated[
        int,
        typer.Option(help="Maximum number of memory/profile records to inspect and clean."),
    ] = 200,
    apply: bool = typer.Option(
        False,
        "--apply",
        help="Actually delete the discovered memory rows and profile snapshots.",
    ),
    force: bool = typer.Option(
        False,
        "--force",
        help="Allow cleanup even when the target does not look like fixture/test data.",
    ),
    yes: bool = typer.Option(
        False,
        "--yes",
        help="Skip the interactive confirmation prompt when used with --apply.",
    ),
) -> None:
    """Preview or clean fixture memory/profile records for one test user."""

    container = AppContainer.build()
    memories, profiles = _collect_fixture_records(
        container=container,
        agent_id=agent_id,
        user_id=user_id,
        limit=limit,
    )
    _emit_fixture_cleanup_preview(
        agent_id=agent_id,
        user_id=user_id,
        memories=memories,
        profiles=profiles,
        dry_run=not apply,
    )
    if not apply or (not memories and not profiles):
        return
    if not force and not _looks_like_fixture_target(user_id, memories, profiles):
        raise typer.BadParameter(
            "Refusing to delete records that do not look like fixture/test data. "
            "Use --force only after reviewing the preview.",
        )

    if not yes:
        confirmed = typer.confirm(
            "Delete these fixture memory rows and profile snapshots from the database?",
            default=False,
            show_default=True,
        )
        if not confirmed:
            typer.echo("Aborted. No fixture records were deleted.")
            return

    for profile in profiles:
        container.memory_repository.delete_profile_snapshot(profile.profile_id)
    for memory in memories:
        container.memory_repository.delete(memory.memory_id)

    remaining_memories, remaining_profiles = _collect_fixture_records(
        container=container,
        agent_id=agent_id,
        user_id=user_id,
        limit=limit,
    )
    typer.echo(
        f"Deleted fixture data for {agent_id}/{user_id}. "
        f"remaining_memories={len(remaining_memories)} remaining_profiles={len(remaining_profiles)}",
    )


@app.command("desktop-scan-preview")
def desktop_scan_preview(
    account_id: Annotated[str, typer.Argument(help="Desktop account identifier to associate with the scan.")],
    conversation_hint: Annotated[
        Optional[str],
        typer.Option(help="Optional visible conversation hint, title, or nickname."),
    ] = None,
    connector_name: Annotated[str, typer.Option(help="Desktop connector to use.")] = "wechat_desktop",
    force_ocr: Annotated[
        bool,
        typer.Option("--force-ocr", help="Skip accessible-text extraction and force the OCR screenshot path."),
    ] = False,
    save_capture: Annotated[
        bool,
        typer.Option("--save-capture", help="Persist the OCR screenshot artifact for manual debugging."),
    ] = False,
) -> None:
    """Run the desktop connector skeleton and print its current preview output."""

    container = AppContainer.build()
    result = container.desktop_service.scan(
        connector_name=connector_name,
        account_id=account_id,
        conversation_hint=conversation_hint,
        force_ocr=force_ocr,
        save_capture=save_capture,
    )
    typer.echo(json.dumps(result.model_dump(mode="json"), indent=2))


@app.command("chatlog-normalize")
def chatlog_normalize(
    input_path: Path = typer.Option(
        Path("private/chat_history"),
        "--input",
        help="Input WeFlow JSONL file or directory under private/chat_history.",
    ),
    output_dir: Optional[Path] = typer.Option(
        None,
        "--output",
        help="Output directory under private/distilled. Required unless --dry-run.",
    ),
    limit: Optional[int] = typer.Option(
        None,
        min=1,
        help="Normalize only the first N message rows after filtering.",
    ),
    dry_run: bool = typer.Option(
        False,
        help="Process input and print a safe report without writing normalized outputs.",
    ),
    timezone_name: Optional[str] = typer.Option(
        None,
        help="Timezone used for normalized timestamp rendering. Defaults to configured outbound timezone.",
    ),
) -> None:
    """Normalize WeFlow JSONL exports into private normalized_events.jsonl output."""

    resolved_output_dir = output_dir
    if not dry_run and resolved_output_dir is None:
        resolved_output_dir = _default_chatlog_output_dir()

    settings = get_settings()
    service = ChatlogIngestionService(
        timezone_name=timezone_name or settings.outbound_policy_timezone,
    )
    try:
        result = service.normalize_weflow_exports(
            input_path=input_path,
            output_dir=resolved_output_dir,
            limit=limit,
            dry_run=dry_run,
        )
    except ChatlogNormalizationError as exc:
        raise typer.BadParameter(str(exc)) from exc

    typer.echo(json.dumps(result.report, ensure_ascii=False, indent=2))


@app.command("chatlog-chunk")
def chatlog_chunk(
    input_path: Path = typer.Option(
        Path("private/distilled"),
        "--input",
        help="Input normalized_events.jsonl file or a private/distilled run directory that contains it.",
    ),
    output_dir: Optional[Path] = typer.Option(
        None,
        "--output",
        help="Output directory under private/distilled. Defaults to the input run directory.",
    ),
    limit: Optional[int] = typer.Option(
        None,
        min=1,
        help="Chunk only the first N normalized events after filtering.",
    ),
    dry_run: bool = typer.Option(
        False,
        help="Process input and print a safe report without writing chunk outputs.",
    ),
    max_gap_minutes: int = typer.Option(
        240,
        min=1,
        help="Start a new chunk when the gap between adjacent events reaches this many minutes.",
    ),
    max_messages_per_chunk: int = typer.Option(
        80,
        min=1,
        help="Start a new chunk when the current chunk reaches this many events.",
    ),
) -> None:
    """Chunk normalized chatlog events into private chunks.jsonl output."""

    service = ConversationChunkingService()
    try:
        result = service.chunk_normalized_events(
            input_path=input_path,
            output_dir=output_dir,
            limit=limit,
            dry_run=dry_run,
            max_gap_minutes=max_gap_minutes,
            max_messages_per_chunk=max_messages_per_chunk,
        )
    except ConversationChunkingError as exc:
        raise typer.BadParameter(str(exc)) from exc

    typer.echo(json.dumps(result.report, ensure_ascii=False, indent=2))


@app.command("chatlog-distill")
def chatlog_distill(
    input_path: Path = typer.Option(
        Path("private/distilled"),
        "--input",
        help="Input chunks.jsonl file or a private/distilled run directory that contains chunks.jsonl and normalized_events.jsonl.",
    ),
    output_dir: Optional[Path] = typer.Option(
        None,
        "--output",
        help="Output directory under private/distilled. Defaults to the input run directory.",
    ),
    limit: Optional[int] = typer.Option(
        None,
        min=1,
        help="Distill only the first N selected chunks.",
    ),
    sample: Optional[int] = typer.Option(
        None,
        min=1,
        help="Evenly sample N chunks from the input before applying --limit.",
    ),
    dry_run: bool = typer.Option(
        False,
        help="Process input and print a safe report without writing distillation outputs.",
    ),
) -> None:
    """Distill chat chunks into validated chunk summaries and memory fact candidates."""

    settings = get_settings()
    model_hint = settings.chat_memory_model or settings.chat_suggestion_model
    service = ChatlogDistillationService(
        api_key=settings.openai_api_key,
        base_url=settings.openai_base_url,
        model=model_hint,
        timeout_seconds=max(
            settings.chat_memory_timeout_seconds,
            settings.chat_suggestion_timeout_seconds,
        ),
    )
    try:
        result = service.distill_chunks(
            input_path=input_path,
            output_dir=output_dir,
            limit=limit,
            sample=sample,
            dry_run=dry_run,
        )
    except ChatlogDistillationError as exc:
        raise typer.BadParameter(str(exc)) from exc

    typer.echo(json.dumps(result.report, ensure_ascii=False, indent=2))


@app.command("chatlog-build-contact-skill")
def chatlog_build_contact_skill(
    input_path: Path = typer.Option(
        Path("private/distilled"),
        "--input",
        help="Input chunk_summaries.jsonl file or a private/distilled run directory that contains chunk_summaries.jsonl and memory_facts.jsonl.",
    ),
    output_dir: Optional[Path] = typer.Option(
        None,
        "--output",
        help="Output directory under private/distilled. Defaults to the input run directory.",
    ),
    contact_id: Optional[str] = typer.Option(
        None,
        "--contact-id",
        help="Optional contact id filter. Defaults to the first contact found in the input summaries.",
    ),
    dry_run: bool = typer.Option(
        False,
        help="Process input and print a safe report without writing contact skill outputs.",
    ),
) -> None:
    """Build a candidate ContactSkill and human-review markdown artifact from distillation outputs."""

    service = ContactSkillBuilderService()
    try:
        result = service.build_contact_skill(
            input_path=input_path,
            output_dir=output_dir,
            contact_id=contact_id,
            dry_run=dry_run,
        )
    except ContactSkillBuilderError as exc:
        raise typer.BadParameter(str(exc)) from exc

    typer.echo(json.dumps(result.report, ensure_ascii=False, indent=2))


@app.command("chatlog-validate-evidence")
def chatlog_validate_evidence(
    input_path: Path = typer.Option(
        Path("private/distilled"),
        "--input",
        help="Input private/distilled run directory or store artifact path.",
    ),
    output_path: Optional[Path] = typer.Option(
        None,
        "--output",
        help="Optional report path under private/distilled. Defaults to private/distilled/<run_id>/evidence_validation_report.json.",
    ),
    dry_run: bool = typer.Option(
        False,
        help="Validate evidence refs and print a safe summary without writing a report file.",
    ),
) -> None:
    """Validate evidence refs for memory/contact-skill store records under private/distilled."""

    service = EvidenceValidationService()
    try:
        result = service.validate_evidence(
            input_path=input_path,
            output_path=output_path,
            dry_run=dry_run,
        )
    except EvidenceValidationError as exc:
        raise typer.BadParameter(str(exc)) from exc

    summary = result.report["summary"]
    typer.echo(
        json.dumps(
            {
                "input_path": result.report["input_path"],
                "run_dir": result.report["run_dir"],
                "output_path": result.report["output_path"],
                "evidence_validation_status": summary["evidence_validation_status"],
                "validated_record_count": summary["validated_record_count"],
                "records_with_missing_refs": summary["records_with_missing_refs"],
                "missing_ref_count": summary["missing_ref_count"],
                "approval_blocked_records": summary["approval_blocked_records"],
                "runtime_blocked_records": summary["runtime_blocked_records"],
                "report_written": result.output_path is not None,
            },
            ensure_ascii=False,
            indent=2,
        ),
    )


@app.command("chatlog-review-store")
def chatlog_review_store(
    input_path: Path = typer.Option(
        Path("private/distilled"),
        "--input",
        help="Input private/distilled run directory or store artifact path.",
    ),
    action: str = typer.Option(
        "list",
        "--action",
        help="One of: list, approve, reject, freeze, archive, export.",
    ),
    record_id: Optional[str] = typer.Option(
        None,
        "--record-id",
        help="Record id required for approve/reject/freeze/archive. Optional for export to filter one record.",
    ),
    reviewer_id: Optional[str] = typer.Option(
        None,
        "--reviewer-id",
        help="Reviewer id for human decisions.",
    ),
    reviewer_name: Optional[str] = typer.Option(
        None,
        "--reviewer-name",
        help="Reviewer display name for human decisions.",
    ),
    note: list[str] = typer.Option(
        None,
        "--note",
        help="Repeatable human review note. Safe summaries only.",
    ),
    validation_report: Optional[Path] = typer.Option(
        None,
        "--validation-report",
        help="Optional explicit evidence_validation_report.json path under private/distilled.",
    ),
    output_path: Optional[Path] = typer.Option(
        None,
        "--output",
        help="Optional output path under private/distilled for JSON store write-back or Markdown export.",
    ),
) -> None:
    """List, review, and export private distilled store records with human-review-first gates."""

    service = ContactSkillStoreReviewService()
    normalized_action = action.strip().lower()
    try:
        if normalized_action == "list":
            result = service.list_store_records(
                input_path=input_path,
                validation_report_path=validation_report,
            )
            typer.echo(
                json.dumps(
                    {
                        "action": "list",
                        "input_path": _safe_cli_path(result.input_path),
                        "run_dir": _safe_cli_path(result.run_dir),
                        "validation_report_path": _safe_cli_path(result.validation_report_path),
                        "validation_report_found": result.validation_report_found,
                        "record_count": len(result.records),
                        "records": [
                            {
                                "record_id": record.record_id,
                                "artifact_type": record.artifact_type,
                                "artifact_id": record.artifact_id,
                                "status": record.status,
                                "review_state": record.review_state,
                                "reviewed_by_human": record.reviewed_by_human,
                                "last_decision": record.last_decision,
                                "evidence_validation_status": record.evidence_validation_status,
                                "approval_ready_after_validation": record.approval_ready_after_validation,
                                "runtime_ready_after_validation": record.runtime_ready_after_validation,
                                "missing_ref_count": record.missing_ref_count,
                                "safe_path": record.safe_path,
                            }
                            for record in result.records
                        ],
                    },
                    ensure_ascii=False,
                    indent=2,
                ),
            )
            return

        if normalized_action == "export":
            result = service.export_review_artifact(
                input_path=input_path,
                output_path=output_path,
                record_id=record_id,
                validation_report_path=validation_report,
            )
            typer.echo(
                json.dumps(
                    {
                        "action": "export",
                        "input_path": _safe_cli_path(result.input_path),
                        "run_dir": _safe_cli_path(result.run_dir),
                        "validation_report_path": _safe_cli_path(result.validation_report_path),
                        "output_path": _safe_cli_path(result.output_path),
                        "record_count": result.record_count,
                        "record_ids": result.record_ids,
                    },
                    ensure_ascii=False,
                    indent=2,
                ),
            )
            return

        if normalized_action in {"approve", "reject", "freeze", "archive"}:
            if not record_id:
                raise typer.BadParameter("--record-id is required for review decisions.")
            result = service.apply_record_decision(
                input_path=input_path,
                record_id=record_id,
                decision=normalized_action,
                reviewer_id=reviewer_id,
                reviewer_name=reviewer_name,
                notes=note,
                validation_report_path=validation_report,
                output_path=output_path,
            )
            typer.echo(
                json.dumps(
                    {
                        "action": normalized_action,
                        "decision": result.decision,
                        "input_path": _safe_cli_path(result.input_path),
                        "run_dir": _safe_cli_path(result.run_dir),
                        "validation_report_path": _safe_cli_path(result.validation_report_path),
                        "saved_output_path": _safe_cli_path(result.saved_output_path),
                        "record": {
                            "record_id": result.record.record_id,
                            "artifact_type": result.record.artifact_type,
                            "artifact_id": result.record.artifact_id,
                            "status": result.record.status,
                            "review_state": result.record.review_state,
                            "reviewed_by_human": result.record.reviewed_by_human,
                            "last_decision": result.record.last_decision,
                            "evidence_validation_status": result.record.evidence_validation_status,
                            "approval_ready_after_validation": result.record.approval_ready_after_validation,
                            "runtime_ready_after_validation": result.record.runtime_ready_after_validation,
                            "missing_ref_count": result.record.missing_ref_count,
                            "safe_path": result.record.safe_path,
                        },
                    },
                    ensure_ascii=False,
                    indent=2,
                ),
            )
            return

        raise typer.BadParameter("Unknown action. Use list, approve, reject, freeze, archive, or export.")
    except ContactSkillStoreReviewError as exc:
        raise typer.BadParameter(str(exc)) from exc


@app.command("chat-reply-plan")
def chat_reply_plan(
    input_path: Path = typer.Option(
        ...,
        "--input",
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        help="Input safe synthetic or redacted ChatContext JSON file.",
    ),
    output_path: Optional[Path] = typer.Option(
        None,
        "--output",
        help="Optional ReplyPlan JSON output path.",
    ),
) -> None:
    """Generate a review-only ReplyPlan from safe ChatContext JSON."""

    try:
        context = ChatContext.model_validate_json(input_path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise typer.BadParameter(f"Unable to read input: {input_path}") from exc
    except ValidationError as exc:
        raise typer.BadParameter(f"Invalid ChatContext JSON: {exc}") from exc

    planner = ReplyPlanner()
    try:
        plan = planner.generate(context=context)
    except ReplyPlannerError as exc:
        raise typer.BadParameter(str(exc)) from exc

    payload = json.dumps(plan.model_dump(mode="json"), ensure_ascii=False, indent=2)
    if output_path is None:
        typer.echo(payload)
        return

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(payload, encoding="utf-8")
    typer.echo(
        json.dumps(
            {
                "input_path": _safe_cli_path(input_path),
                "output_path": _safe_cli_path(output_path),
                "contact_id": plan.contact_id,
                "candidate_count": len(plan.candidates),
                "plan_mode": plan.plan_mode,
            },
            ensure_ascii=False,
            indent=2,
        ),
    )


@app.command("chat-reply-feedback")
def chat_reply_feedback(
    plan: Path = typer.Option(
        ...,
        "--plan",
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        help="Input ReplyPlan JSON file to provide feedback on.",
    ),
    candidate_rank: int = typer.Option(
        ...,
        "--candidate-rank",
        min=1,
        help="Priority rank of the candidate to provide feedback on.",
    ),
    action: str = typer.Option(
        ...,
        "--action",
        help="Feedback action: accept, edit, reject, boundary.",
    ),
    output: Path = typer.Option(
        ...,
        "--output",
        help="Output feedback log path under private/.",
    ),
    note: Optional[str] = typer.Option(
        None,
        "--note",
        help="Optional user note.",
    ),
    edited_text: Optional[str] = typer.Option(
        None,
        "--edited-text",
        help="Edited text when action is 'edit'.",
    ),
    boundary_label: Optional[str] = typer.Option(
        None,
        "--boundary-label",
        help="Boundary label when action is 'boundary'.",
    ),
    boundary_note: Optional[str] = typer.Option(
        None,
        "--boundary-note",
        help="Boundary note when action is 'boundary'.",
    ),
) -> None:
    """Record human feedback on a ReplyPlan candidate to a private feedback log."""

    valid_actions = ("accept", "edit", "reject", "boundary")
    normalized_action = action.strip().lower()
    if normalized_action not in valid_actions:
        raise typer.BadParameter(f"Invalid action '{action}'. Must be one of: {', '.join(valid_actions)}.")

    service = FeedbackService()
    try:
        result = service.record_feedback(
            plan_path=plan,
            candidate_rank=candidate_rank,
            action=normalized_action,
            output_path=output,
            user_note=note,
            edited_text=edited_text,
            boundary_label=boundary_label,
            boundary_note=boundary_note,
        )
    except FeedbackError as exc:
        raise typer.BadParameter(str(exc)) from exc

    typer.echo(
        json.dumps(
            {
                "feedback_id": result["feedback_id"],
                "contact_id": result["contact_id"],
                "candidate_id": result["candidate_id"],
                "priority_rank": result["priority_rank"],
                "action": result["action"],
                "total_records": result["total_records"],
                "output_path": _safe_cli_path(Path(result["output_path"])),
            },
            ensure_ascii=False,
            indent=2,
        ),
    )


@app.command("chat-reply-feedback-validate")
def chat_reply_feedback_validate(
    input_path: Path = typer.Option(
        ...,
        "--input",
        help="Input feedback log JSON file to validate.",
    ),
    strict: bool = typer.Option(
        False,
        "--strict",
        help="Return non-zero exit code if any validation issues are found.",
    ),
) -> None:
    """Validate a T140 feedback log and emit a safe summary."""

    service = FeedbackValidationService()
    report = service.validate(input_path=input_path, strict=strict)

    safe_output = {
        "input_path": report["input_path"],
        "is_readable": report["is_readable"],
        "corrupted_input_count": report["corrupted_input_count"],
        "total_records": report["total_records"],
        "valid_record_count": report["valid_record_count"],
        "invalid_record_count": report["invalid_record_count"],
        "counts_by_action": report["counts_by_action"],
        "missing_plan_count": report["missing_plan_count"],
        "missing_candidate_count": report["missing_candidate_count"],
        "contact_mismatch_count": report["contact_mismatch_count"],
        "edit_without_text_count": report["edit_without_text_count"],
        "boundary_without_details_count": report["boundary_without_details_count"],
        "privacy_warnings": report["privacy_warnings"],
        "record_results": report["record_results"],
    }

    if report["corrupted_reason"]:
        safe_output["corrupted_reason"] = report["corrupted_reason"]

    typer.echo(json.dumps(safe_output, ensure_ascii=False, indent=2))

    if not report["is_readable"]:
        raise typer.Exit(code=1)
    if strict and (
        report["invalid_record_count"] > 0 or report["privacy_warnings"]
    ):
        raise typer.Exit(code=1)


@app.command("chat-reply-feedback-summary")
def chat_reply_feedback_summary(
    input_path: Path = typer.Option(
        ...,
        "--input",
        help="Input feedback log JSON file to summarize.",
    ),
    output: Optional[Path] = typer.Option(
        None,
        "--output",
        help="Optional private output path for summary JSON.",
    ),
    validation_report: Optional[Path] = typer.Option(
        None,
        "--validation-report",
        help="Optional T141 validation report JSON to merge aggregate counts from.",
    ),
) -> None:
    """Export aggregate privacy-safe feedback summary over a feedback log."""

    service = FeedbackSummaryService()
    summary = service.summarize(
        input_path=input_path,
        output_path=output,
        validation_report_path=validation_report,
    )

    safe_stdout = {
        "input_path": summary["input_path"],
        "is_readable": summary["is_readable"],
        "total_records": summary["total_records"],
        "counts_by_action": summary["counts_by_action"],
        "distinct_contact_ids": summary["distinct_contact_ids"],
        "distinct_candidate_ids": summary["distinct_candidate_ids"],
        "distinct_reply_plan_ids": summary["distinct_reply_plan_ids"],
        "distinct_source_plan_paths": summary["distinct_source_plan_paths"],
        "records_with_boundary_label": summary["records_with_boundary_label"],
        "records_with_edited_text": summary["records_with_edited_text"],
        "records_with_user_note": summary["records_with_user_note"],
        "counts_by_approach_label": summary["counts_by_approach_label"],
        "time_range": summary["time_range"],
        "validation_summary": summary["validation_summary"],
    }

    if not summary["is_readable"]:
        safe_stdout["corrupted_reason"] = summary["corrupted_reason"]

    if summary.get("output_path"):
        safe_stdout["output_path"] = _safe_cli_path(Path(summary["output_path"]))

    typer.echo(json.dumps(safe_stdout, ensure_ascii=False, indent=2))

    if not summary["is_readable"]:
        raise typer.Exit(code=1)


@app.command("meeting-live-preview")
def meeting_live_preview(
    account_id: Annotated[str, typer.Argument(help="Desktop account identifier to associate with the meeting session.")],
    meeting_hint: Annotated[
        Optional[str],
        typer.Option(help="Optional visible meeting title or window hint."),
    ] = None,
    connector_name: Annotated[str, typer.Option(help="Meeting connector to use.")] = "tencent_meeting_desktop",
    sample_audio_path: Annotated[
        Optional[Path],
        typer.Option(help="Optional local audio file to run through the transcription service for skeleton testing."),
    ] = None,
    agent_id: Annotated[
        Optional[str],
        typer.Option(help="Optional agent id. Successful transcript chunks will be stored and forwarded into this agent runtime."),
    ] = None,
    audio_source: Annotated[
        MeetingAudioSource,
        typer.Option(help="Audio capture source: system output loopback or microphone input."),
    ] = MeetingAudioSource.LOOPBACK,
    capture_seconds: Annotated[
        Optional[float],
        typer.Option(help="Optional duration for live audio capture. Defaults to the configured meeting capture duration."),
    ] = None,
    chunk_seconds: Annotated[
        Optional[float],
        typer.Option(help="Optional chunk size for splitting captured meeting audio into WAV segments."),
    ] = None,
    save_capture: Annotated[
        bool,
        typer.Option(help="Persist captured WAV chunks for manual debugging."),
    ] = False,
    device_name: Annotated[
        Optional[str],
        typer.Option("--device-name", "--speaker-name", help="Optional audio device name override for the selected source."),
    ] = None,
) -> None:
    """Preview the Tencent Meeting desktop transcription flow with loopback or microphone capture."""

    container = AppContainer.build()
    result: MeetingLivePreview = container.meeting_service.preview(
        connector_name=connector_name,
        account_id=account_id,
        meeting_hint=meeting_hint,
        sample_audio_path=sample_audio_path,
        agent_id=agent_id,
        audio_source=audio_source,
        capture_seconds=capture_seconds,
        chunk_seconds=chunk_seconds,
        save_capture=save_capture,
        device_name=device_name,
    )
    typer.echo(json.dumps(result.model_dump(mode="json"), indent=2))


@app.command("meeting-live-window")
def meeting_live_window(
    account_id: Annotated[str, typer.Argument(help="Desktop account identifier to associate with the meeting session.")],
    meeting_hint: Annotated[
        Optional[str],
        typer.Option(help="Optional visible meeting title or window hint."),
    ] = None,
    connector_name: Annotated[str, typer.Option(help="Meeting connector to use.")] = "tencent_meeting_desktop",
    agent_id: Annotated[
        Optional[str],
        typer.Option(help="Optional agent id. Successful transcript chunks will also flow into this agent runtime."),
    ] = None,
    audio_source: Annotated[
        MeetingAudioSource,
        typer.Option(help="Initial audio capture source shown in the window."),
    ] = MeetingAudioSource.LOOPBACK,
    capture_seconds: Annotated[
        Optional[float],
        typer.Option(help="Per-iteration capture duration. Defaults to chunk-seconds or config."),
    ] = None,
    chunk_seconds: Annotated[
        Optional[float],
        typer.Option(help="Per-iteration chunk size used by live capture."),
    ] = 2.0,
    save_capture: Annotated[
        bool,
        typer.Option(help="Persist captured WAV chunks during the live session."),
    ] = False,
    device_name: Annotated[
        Optional[str],
        typer.Option("--device-name", "--speaker-name", help="Optional audio device name override for the selected source."),
    ] = None,
    cooldown_seconds: Annotated[
        float,
        typer.Option(help="Sleep gap between iterations after one capture/transcribe cycle finishes."),
    ] = 0.25,
    window_alpha: Annotated[
        Optional[float],
        typer.Option(help="Optional transparency for the floating copilot window."),
    ] = None,
    assistant_enabled: Annotated[
        bool,
        typer.Option(help="Enable the AI copilot suggestion panel."),
    ] = True,
) -> None:
    """Launch a small always-on-top live caption window for Tencent Meeting."""

    container = AppContainer.build()
    request = MeetingLiveLoopRequest(
        connector_name=connector_name,
        account_id=account_id,
        meeting_hint=meeting_hint,
        agent_id=agent_id,
        audio_source=audio_source,
        capture_seconds=capture_seconds,
        chunk_seconds=chunk_seconds,
        save_capture=save_capture,
        device_name=device_name,
        cooldown_seconds=cooldown_seconds,
    )
    window = MeetingLiveCaptionWindow(
        loop_service=container.meeting_live_loop_service,
        assistant_service=container.meeting_assistant_service,
        minutes_export_service=container.meeting_minutes_export_service,
        initial_request=request,
        window_alpha=window_alpha if window_alpha is not None else container.settings.meeting_live_window_alpha,
        assistant_enabled=assistant_enabled,
    )
    window.run()


@app.command("meeting-session-list")
def meeting_session_list(
    account_id: Annotated[
        Optional[str],
        typer.Option(help="Optional account id filter."),
    ] = None,
    limit: Annotated[
        int,
        typer.Option(help="Maximum number of sessions to return."),
    ] = 20,
) -> None:
    """List recent persisted meeting sessions."""

    container = AppContainer.build()
    sessions = container.meeting_repository.list_sessions(
        account_id=account_id,
        limit=limit,
    )
    typer.echo(
        json.dumps(
            {
                "account_id": account_id,
                "count": len(sessions),
                "sessions": [session.model_dump(mode="json") for session in sessions],
            },
            indent=2,
        ),
    )


@app.command("meeting-session-show")
def meeting_session_show(
    session_id: Annotated[
        Optional[str],
        typer.Argument(help="Meeting session id. Omit when using --latest-for-account."),
    ] = None,
    latest_for_account: Annotated[
        Optional[str],
        typer.Option(help="Load the latest session for a specific account id."),
    ] = None,
    segment_limit: Annotated[
        int,
        typer.Option(help="Number of recent meeting segments to include."),
    ] = 20,
) -> None:
    """Show one meeting session with recent persisted segments."""

    container = AppContainer.build()
    resolved_session_id = _resolve_meeting_session_id(
        container=container,
        session_id=session_id,
        latest_for_account=latest_for_account,
    )

    session_record = container.meeting_repository.get_session(session_id=resolved_session_id)
    if session_record is None:
        raise typer.BadParameter(f"Unknown meeting session: {resolved_session_id}")
    segments = container.meeting_repository.list_recent_segments(
        session_id=resolved_session_id,
        limit=segment_limit,
    )
    typer.echo(
        json.dumps(
            {
                "session": session_record.model_dump(mode="json"),
                "segment_count": len(segments),
                "segments": [segment.model_dump(mode="json") for segment in segments],
            },
            indent=2,
        ),
    )


@app.command("meeting-session-tail")
def meeting_session_tail(
    session_id: Annotated[
        Optional[str],
        typer.Argument(help="Meeting session id. Omit when using --latest-for-account."),
    ] = None,
    latest_for_account: Annotated[
        Optional[str],
        typer.Option(help="Tail the latest session for a specific account id."),
    ] = None,
    limit: Annotated[
        int,
        typer.Option(help="Number of recent segments to fetch each poll."),
    ] = 10,
    interval_seconds: Annotated[
        float,
        typer.Option(help="Polling interval in seconds."),
    ] = 2.0,
    rounds: Annotated[
        int,
        typer.Option(help="How many polling rounds to run before exiting."),
    ] = 15,
    text_only: Annotated[
        bool,
        typer.Option("--text-only", help="Print a concise plain-text tail instead of JSON."),
    ] = False,
) -> None:
    """Poll and print newly persisted meeting segments for one session."""

    container = AppContainer.build()
    resolved_session_id = _resolve_meeting_session_id(
        container=container,
        session_id=session_id,
        latest_for_account=latest_for_account,
    )

    seen_segment_ids: set[str] = set()
    for round_index in range(rounds):
        session_record = container.meeting_repository.get_session(session_id=resolved_session_id)
        if session_record is None:
            raise typer.BadParameter(f"Unknown meeting session: {resolved_session_id}")
        segments = container.meeting_repository.list_recent_segments(
            session_id=resolved_session_id,
            limit=limit,
        )
        new_segments = [segment for segment in segments if segment.segment_id not in seen_segment_ids]
        for segment in new_segments:
            seen_segment_ids.add(segment.segment_id)
        if text_only:
            typer.echo(
                f"[round {round_index + 1}] session={resolved_session_id} new_segments={len(new_segments)}",
            )
            if session_record.latest_summary:
                typer.echo(f"summary: {session_record.latest_summary}")
            for segment in new_segments:
                typer.echo(_render_meeting_segment_text_line(segment))
            if not new_segments:
                typer.echo("(no new segments)")
        else:
            typer.echo(
                json.dumps(
                    {
                        "round": round_index + 1,
                        "session_id": resolved_session_id,
                        "rolling_summary": session_record.latest_summary,
                        "new_segment_count": len(new_segments),
                        "new_segments": [segment.model_dump(mode="json") for segment in new_segments],
                    },
                    indent=2,
                ),
            )
        if round_index + 1 < rounds:
            sleep(max(interval_seconds, 0.1))


@app.command("meeting-session-replay")
def meeting_session_replay(
    session_id: Annotated[str, typer.Argument(help="Meeting session id.")],
    agent_id: Annotated[str, typer.Argument(help="Target agent id for replay into runtime.")],
    limit: Annotated[
        int,
        typer.Option(help="Alias of --latest; maximum number of recent segments to replay."),
    ] = 20,
    latest: Annotated[
        Optional[int],
        typer.Option(help="Replay only the latest N segments after filtering."),
    ] = None,
    started_after: Annotated[
        Optional[str],
        typer.Option(help="Replay segments whose started_at is on or after this ISO-8601 timestamp."),
    ] = None,
    started_before: Annotated[
        Optional[str],
        typer.Option(help="Replay segments whose started_at is on or before this ISO-8601 timestamp."),
    ] = None,
) -> None:
    """Replay persisted meeting segments into the configured agent runtime."""

    container = AppContainer.build()
    session_record = container.meeting_repository.get_session(session_id=session_id)
    if session_record is None:
        raise typer.BadParameter(f"Unknown meeting session: {session_id}")

    latest_count = latest if latest is not None else limit
    segments, started_after_dt, started_before_dt = _load_meeting_segments(
        container=container,
        session_id=session_id,
        latest=latest_count,
        started_after=started_after,
        started_before=started_before,
    )
    replay_results: list[dict[str, object]] = []
    for segment in segments:
        event = _meeting_segment_to_inbound_event(
            session_record=session_record,
            segment=segment,
        )
        turn = container.runtime.handle_inbound_event(
            agent_id=agent_id,
            event=event,
        )
        replay_results.append(
            {
                "segment_id": segment.segment_id,
                "event_id": event.event_id,
                "text": segment.text,
                "should_reply": turn.should_reply,
                "action_count": len(turn.actions),
                "reasoning": turn.reasoning,
            },
        )

    typer.echo(
        json.dumps(
            {
                "session_id": session_id,
                "agent_id": agent_id,
                "started_after": started_after_dt.isoformat() if started_after_dt else None,
                "started_before": started_before_dt.isoformat() if started_before_dt else None,
                "replayed_segments": len(replay_results),
                "results": replay_results,
            },
            indent=2,
        ),
    )


@app.command("meeting-session-export")
def meeting_session_export(
    session_id: Annotated[
        Optional[str],
        typer.Argument(help="Meeting session id. Omit when using --latest-for-account."),
    ] = None,
    output_path: Annotated[
        Optional[Path],
        typer.Option(help="Optional Markdown output path. Defaults to ./exports/<session_id>.md."),
    ] = None,
    latest_for_account: Annotated[
        Optional[str],
        typer.Option(help="Export the latest session for a specific account id."),
    ] = None,
    latest: Annotated[
        Optional[int],
        typer.Option(help="Export only the latest N transcript segments after filtering."),
    ] = None,
    template: Annotated[
        MeetingExportTemplate,
        typer.Option(help="Markdown export style: brief, standard, or full."),
    ] = MeetingExportTemplate.STANDARD,
    started_after: Annotated[
        Optional[str],
        typer.Option(help="Include segments whose started_at is on or after this ISO-8601 timestamp."),
    ] = None,
    started_before: Annotated[
        Optional[str],
        typer.Option(help="Include segments whose started_at is on or before this ISO-8601 timestamp."),
    ] = None,
) -> None:
    """Export one meeting session as a Markdown meeting note file."""

    container = AppContainer.build()
    resolved_session_id = _resolve_meeting_session_id(
        container=container,
        session_id=session_id,
        latest_for_account=latest_for_account,
    )
    session_record = container.meeting_repository.get_session(session_id=resolved_session_id)
    if session_record is None:
        raise typer.BadParameter(f"Unknown meeting session: {resolved_session_id}")

    segments, started_after_dt, started_before_dt = _load_meeting_segments(
        container=container,
        session_id=resolved_session_id,
        latest=latest,
        started_after=started_after,
        started_before=started_before,
    )
    resolved_output_path = output_path or Path("exports") / f"{resolved_session_id}.md"
    export_result = container.meeting_minutes_export_service.export_minutes(
        session_record=session_record,
        segments=segments,
        template=template,
        output_path=resolved_output_path,
        started_after=started_after_dt,
        started_before=started_before_dt,
    )

    typer.echo(
        json.dumps(
            {
                "session_id": resolved_session_id,
                "minutes_id": export_result.record.minutes_id,
                "output_path": str(export_result.output_path),
                "template": template.value,
                "minutes_backend": export_result.draft.backend,
                "minutes_status": export_result.draft.status,
                "segment_count": len(segments),
                "started_after": started_after_dt.isoformat() if started_after_dt else None,
                "started_before": started_before_dt.isoformat() if started_before_dt else None,
            },
            indent=2,
        ),
    )


@app.command("meeting-session-minutes-history")
def meeting_session_minutes_history(
    session_id: Annotated[
        Optional[str],
        typer.Argument(help="Meeting session id. Omit when using --latest-for-account."),
    ] = None,
    latest_for_account: Annotated[
        Optional[str],
        typer.Option(help="Load the latest meeting session for a specific account id."),
    ] = None,
    limit: Annotated[
        int,
        typer.Option(help="Maximum number of historical minutes versions to return."),
    ] = 20,
) -> None:
    """Show persisted meeting minutes export history for one session."""

    container = AppContainer.build()
    resolved_session_id = _resolve_meeting_session_id(
        container=container,
        session_id=session_id,
        latest_for_account=latest_for_account,
    )
    session_record = container.meeting_repository.get_session(session_id=resolved_session_id)
    if session_record is None:
        raise typer.BadParameter(f"Unknown meeting session: {resolved_session_id}")

    minutes_records = container.meeting_repository.list_minutes(
        session_id=resolved_session_id,
        limit=limit,
    )
    typer.echo(
        json.dumps(
            {
                "session_id": resolved_session_id,
                "count": len(minutes_records),
                "minutes": [record.model_dump(mode="json") for record in minutes_records],
            },
            indent=2,
        ),
    )


@app.command("meeting-session-minutes-show")
def meeting_session_minutes_show(
    minutes_id: Annotated[
        str,
        typer.Argument(help="Meeting minutes version id to display."),
    ],
) -> None:
    """Show one archived meeting minutes version in Markdown form."""

    container = AppContainer.build()
    record = _resolve_meeting_minutes_record(
        container=container,
        minutes_id=minutes_id,
    )
    typer.echo(_render_minutes_markdown(record))


@app.command("meeting-session-minutes-diff")
def meeting_session_minutes_diff(
    old_minutes_id: Annotated[
        str,
        typer.Argument(help="Older meeting minutes version id."),
    ],
    new_minutes_id: Annotated[
        str,
        typer.Argument(help="Newer meeting minutes version id."),
    ],
) -> None:
    """Diff two archived meeting minutes versions."""

    container = AppContainer.build()
    old_record = _resolve_meeting_minutes_record(
        container=container,
        minutes_id=old_minutes_id,
    )
    new_record = _resolve_meeting_minutes_record(
        container=container,
        minutes_id=new_minutes_id,
    )

    diff_lines = list(
        difflib.unified_diff(
            old_record.markdown_body.splitlines(),
            new_record.markdown_body.splitlines(),
            fromfile=f"{old_record.minutes_id}:{old_record.template.value}",
            tofile=f"{new_record.minutes_id}:{new_record.template.value}",
            lineterm="",
        ),
    )
    if not diff_lines:
        typer.echo(
            json.dumps(
                {
                    "old_minutes_id": old_record.minutes_id,
                    "new_minutes_id": new_record.minutes_id,
                    "message": "No markdown differences.",
                },
                indent=2,
            ),
        )
        return
    typer.echo("\n".join(diff_lines))


def _meeting_segment_to_inbound_event(
    *,
    session_record: MeetingSessionRecord,
    segment: MeetingSegmentRecord,
) -> InboundEvent:
    actor_id = (
        f"{segment.audio_source.value}:{segment.capture_device_name}"
        if segment.audio_source is not None and segment.capture_device_name
        else (segment.capture_device_name or "meeting_participant")
    )
    return InboundEvent(
        event_id=f"replay_{segment.segment_id}",
        source_type=SourceType.MEETING_SEGMENT,
        platform=session_record.platform,
        channel_id=session_record.channel_id,
        channel_type=ChannelType.MEETING,
        account_id=session_record.account_id,
        actor_id=actor_id,
        actor_name=segment.speaker_name,
        direction=Direction.INBOUND,
        content_type=ContentType.TEXT,
        occurred_at=segment.started_at or segment.created_at,
        text=segment.text,
        attachments=[
            {
                "type": "meeting_segment_replay",
                "session_id": session_record.session_id,
                "segment_id": segment.segment_id,
                "saved_path": segment.saved_path,
                "display_time": segment.display_time,
            },
        ],
        raw={
            "session": session_record.model_dump(mode="json"),
            "segment": segment.model_dump(mode="json"),
            "replayed": True,
        },
    )


if __name__ == "__main__":
    app()
