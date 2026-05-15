from __future__ import annotations

import re
from typing import Any

from practical_chat_agent.core.models import (
    ChunkSummary,
    ContactSkillCandidate,
    ContactSkillImportantEvent,
    ContactSkillPattern,
    ContactSkillTopicPreference,
    MemoryFactCandidate,
)


def render_contact_skill_review_markdown(
    *,
    candidate: ContactSkillCandidate,
    chunk_summaries: list[ChunkSummary],
    memory_facts: list[MemoryFactCandidate],
) -> str:
    contact_facts = [fact for fact in memory_facts if fact.subject_id == candidate.contact_id]
    user_facts = [fact for fact in memory_facts if fact.subject_id == "user"]
    lines = [
        "# ContactSkill Review",
        "",
        "Candidate only. Human review is required before any downstream planner use.",
        "",
        "## Overview",
        "",
        f"- Contact ID: `{candidate.contact_id}`",
        f"- Relationship type: `{candidate.relationship_type}`",
        f"- Status: `{candidate.status}`",
        f"- Confidence: `{candidate.confidence:.2f}`",
        f"- Sensitivity: `{candidate.sensitivity}`",
        f"- Source chunk ids: {', '.join(f'`{item}`' for item in candidate.source_chunk_ids) or '`none`'}",
        f"- Source memory ids: {', '.join(f'`{item}`' for item in candidate.source_memory_ids) or '`none`'}",
        f"- Evidence refs: {_format_refs(candidate.evidence_refs)}",
        "",
        "## Relationship State",
        "",
        f"- Current status: `{candidate.relationship_state.current_status}`",
        f"- Closeness: `{candidate.relationship_state.closeness:.2f}`",
        f"- Trust level: `{candidate.relationship_state.trust_level:.2f}`",
        f"- Interaction frequency: `{candidate.relationship_state.interaction_frequency}`",
        f"- Initiative balance: `{candidate.relationship_state.initiative_balance}`",
        f"- Confidence: `{candidate.relationship_state.confidence:.2f}`",
        f"- Sensitivity: `{candidate.relationship_state.sensitivity}`",
        f"- Evidence refs: {_format_refs(candidate.relationship_state.evidence_refs)}",
        "",
        "## Communication Style",
        "",
        f"- Message length: `{candidate.communication_style.message_length}`",
        f"- Tone: `{candidate.communication_style.tone}`",
        f"- Response latency: `{candidate.communication_style.response_latency}`",
        f"- Directness: `{candidate.communication_style.directness}`",
        f"- Confidence: `{candidate.communication_style.confidence:.2f}`",
        f"- Sensitivity: `{candidate.communication_style.sensitivity}`",
        f"- Evidence refs: {_format_refs(candidate.communication_style.evidence_refs)}",
        "",
        "## Preferred Topics",
        "",
    ]
    lines.extend(_render_topic_preferences(candidate.preferred_topics, empty_message="No preferred topics proposed from the current sample."))
    lines.extend(
        [
            "",
            "## Avoid Topics",
            "",
        ],
    )
    lines.extend(_render_topic_preferences(candidate.avoid_topics, empty_message="No avoid-topic candidate was strong enough from the current sample."))
    lines.extend(
        [
            "",
            "## Important Events",
            "",
        ],
    )
    lines.extend(_render_important_events(candidate.important_events))
    lines.extend(
        [
            "",
            "## Stable Preferences",
            "",
        ],
    )
    lines.extend(_render_patterns(candidate.stable_preferences, empty_message="No stable communication preference was strong enough to propose yet."))
    lines.extend(
        [
            "",
            "## Emotional Patterns",
            "",
        ],
    )
    lines.extend(_render_patterns(candidate.emotional_patterns, empty_message="No emotional pattern was strong enough to propose yet."))

    user_refs = _unique_refs(user_facts)
    strategy_refs = _unique_refs(user_facts + contact_facts)
    lines.extend(
        [
            "",
            "## User-Side Preferences",
            "",
            f"- User goal: {_safe_text(candidate.user_side_preferences.user_goal or 'not set')}",
            f"- Preferred reply style: {_safe_text(candidate.user_side_preferences.preferred_reply_style or 'not set')}",
        ],
    )
    for boundary in candidate.user_side_preferences.boundaries:
        lines.append(f"- Boundary: {_safe_text(boundary)}")
    lines.append(f"- Supporting refs: {_format_refs(user_refs)}")

    lines.extend(
        [
            "",
            "## Reply Strategy",
            "",
            f"- Default: {_safe_text(candidate.reply_strategy.default or 'not set')}",
            f"- When contact is cold: {_safe_text(candidate.reply_strategy.when_contact_is_cold or 'not set')}",
            f"- When contact opens topic: {_safe_text(candidate.reply_strategy.when_contact_opens_topic or 'not set')}",
            f"- For sensitive topics: {_safe_text(candidate.reply_strategy.for_sensitive_topics or 'not set')}",
            f"- Supporting refs: {_format_refs(strategy_refs)}",
            "",
            "## Usage Boundary",
            "",
            f"- Allowed uses: {', '.join(f'`{item}`' for item in candidate.usage_boundary.allowed_uses) or '`none`'}",
            f"- Disallowed uses: {', '.join(f'`{item}`' for item in candidate.usage_boundary.disallowed_uses) or '`none`'}",
        ],
    )
    for note in candidate.usage_boundary.notes:
        lines.append(f"- Boundary note: {_safe_text(note)}")
    lines.append("- Reviewer reminder: Do not use this artifact to simulate how the contact would speak.")

    lines.extend(
        [
            "",
            "## Review Notes",
            "",
        ],
    )
    if candidate.review_notes:
        for note in candidate.review_notes:
            lines.append(f"- {_safe_text(note)}")
    else:
        lines.append("- No extra review notes were generated.")

    lines.extend(
        [
            "",
            "## Source Snapshot",
            "",
            f"- Chunk summaries loaded: `{len(chunk_summaries)}`",
            f"- Contact memory facts loaded: `{len(contact_facts)}`",
            f"- User memory facts used for strategy only: `{len(user_facts)}`",
        ],
    )
    for summary in chunk_summaries[:3]:
        lines.append(
            "- "
            f"`{summary.chunk_id}` | messages=`{summary.message_count}` | reason=`{summary.chunking_reason}` | "
            f"confidence=`{summary.confidence:.2f}` | sensitivity=`{summary.sensitivity}` | refs={_format_refs(summary.evidence_refs)} | "
            f"summary={_safe_text(summary.summary, max_length=140)}"
        )
    if not chunk_summaries:
        lines.append("- No chunk summary snapshot available.")

    lines.extend(
        [
            "",
            "## Reference Facts",
            "",
        ],
    )
    if contact_facts:
        for fact in contact_facts[:6]:
            lines.append(
                "- "
                f"`{fact.memory_id}` | type=`{fact.memory_type}` | confidence=`{fact.confidence:.2f}` | "
                f"importance=`{fact.importance:.2f}` | sensitivity=`{fact.sensitivity}` | refs={_format_refs(fact.evidence_refs)} | "
                f"claim={_safe_text(fact.claim, max_length=140)}"
            )
    else:
        lines.append("- No contact-specific memory facts available after filtering.")

    return "\n".join(lines).rstrip() + "\n"


def render_store_review_markdown(
    *,
    input_path: str,
    run_dir: str,
    validation_report_path: str | None,
    validation_report_found: bool,
    records: list[dict[str, Any]],
) -> str:
    lines = [
        "# Store Review Export",
        "",
        "Candidate-only / human-review-first workflow snapshot.",
        "",
        "## Overview",
        "",
        f"- Input path: `{input_path}`",
        f"- Run dir: `{run_dir}`",
        f"- Validation report found: `{validation_report_found}`",
        f"- Validation report path: `{validation_report_path or 'not_found'}`",
        f"- Record count: `{len(records)}`",
        "",
        "## Records",
        "",
    ]
    if not records:
        lines.append("- No records matched the requested scope.")
        return "\n".join(lines).rstrip() + "\n"

    for record in records:
        approval_ready = _render_gate_value(record.get("approval_ready_after_validation"))
        runtime_ready = _render_gate_value(record.get("runtime_ready_after_validation"))
        missing_ref_count = record.get("missing_ref_count")
        missing_ref_text = "`unknown`" if missing_ref_count is None else f"`{missing_ref_count}`"
        lines.extend(
            [
                f"### `{record.get('record_id', 'unknown_record')}`",
                "",
                f"- Artifact type: `{record.get('artifact_type', 'unknown')}`",
                f"- Artifact id: `{record.get('artifact_id', 'unknown')}`",
                f"- Status: `{record.get('status', 'unknown')}`",
                f"- Review state: `{record.get('review_state', 'unknown')}`",
                f"- Reviewed by human: `{bool(record.get('reviewed_by_human', False))}`",
                f"- Last decision: `{record.get('last_decision') or 'none'}`",
                f"- Evidence validation status: `{record.get('evidence_validation_status', 'not_run')}`",
                f"- Approval ready after validation: {approval_ready}",
                f"- Runtime ready after validation: {runtime_ready}",
                f"- Missing ref count: {missing_ref_text}",
                f"- Safe path: `{record.get('safe_path', 'unknown')}`",
                f"- Review artifact path: `{record.get('review_artifact_path') or 'none'}`",
            ],
        )
        approval_block_reasons = record.get("approval_block_reasons") or []
        runtime_block_reasons = record.get("runtime_block_reasons") or []
        lines.append(
            f"- Approval block reasons: {_format_reason_list(approval_block_reasons)}",
        )
        lines.append(
            f"- Runtime block reasons: {_format_reason_list(runtime_block_reasons)}",
        )
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def _render_topic_preferences(
    items: list[ContactSkillTopicPreference],
    *,
    empty_message: str,
) -> list[str]:
    if not items:
        return [f"- {empty_message}"]
    return [
        "- "
        f"`{item.topic}` | confidence=`{item.confidence:.2f}` | sensitivity=`{item.sensitivity}` | refs={_format_refs(item.evidence_refs)} | "
        f"claim={_safe_text(item.claim, max_length=140)} | reason={_safe_text(item.reason or 'not provided', max_length=100)}"
        for item in items
    ]


def _render_patterns(
    items: list[ContactSkillPattern],
    *,
    empty_message: str,
) -> list[str]:
    if not items:
        return [f"- {empty_message}"]
    return [
        "- "
        f"confidence=`{item.confidence:.2f}` | sensitivity=`{item.sensitivity}` | refs={_format_refs(item.evidence_refs)} | "
        f"pattern={_safe_text(item.pattern, max_length=140)} | claim={_safe_text(item.claim, max_length=140)}"
        for item in items
    ]


def _render_important_events(items: list[ContactSkillImportantEvent]) -> list[str]:
    if not items:
        return ["- No important event was strong enough to propose yet."]
    return [
        "- "
        f"importance=`{item.importance:.2f}` | confidence=`{item.confidence:.2f}` | sensitivity=`{item.sensitivity}` | "
        f"refs={_format_refs(item.evidence_refs)} | event={_safe_text(item.event, max_length=140)} | "
        f"claim={_safe_text(item.claim, max_length=110)}"
        for item in items
    ]


def _unique_refs(memory_facts: list[MemoryFactCandidate]) -> list[str]:
    seen: set[str] = set()
    refs: list[str] = []
    for fact in memory_facts:
        for ref in fact.evidence_refs:
            if ref in seen:
                continue
            seen.add(ref)
            refs.append(ref)
    return refs


def _format_refs(refs: list[str], *, limit: int = 8) -> str:
    if not refs:
        return "`none`"
    shown = refs[:limit]
    suffix = "" if len(refs) <= limit else f" (+{len(refs) - limit} more)"
    return ", ".join(f"`{ref}`" for ref in shown) + suffix


def _format_reason_list(reasons: list[str]) -> str:
    if not reasons:
        return "`none`"
    return ", ".join(f"`{reason}`" for reason in reasons)


def _render_gate_value(value: bool | None) -> str:
    if value is None:
        return "`unknown`"
    return f"`{value}`"


def _safe_text(text: str, *, max_length: int = 120) -> str:
    cleaned = " ".join(text.split()).strip()
    if not cleaned:
        return "-"
    patterns = [
        (re.compile(r"\b[A-Z0-9._%+\-]+@[A-Z0-9.\-]+\.[A-Z]{2,}\b", re.IGNORECASE), "[EMAIL]"),
        (re.compile(r"(?<!\w)(?:\+?\d[\d\-\s]{6,}\d)(?!\w)"), "[PHONE]"),
        (re.compile(r"\b(?:https?://|www\.)\S+\b", re.IGNORECASE), "[URL]"),
        (re.compile(r"\b\d{6,}\b"), "[NUMBER]"),
        (
            re.compile(
                r"(introduces (?:self|themselves) as:?\s*)(?:['\"]?)([^,.;'\"\n]+)(?:['\"]?)",
                re.IGNORECASE,
            ),
            r"\1[NAME]",
        ),
        (re.compile(r"(name is\s+)([^,.;]+)", re.IGNORECASE), r"\1[NAME]"),
    ]
    redacted = cleaned
    for pattern, replacement in patterns:
        redacted = pattern.sub(replacement, redacted)
    if len(redacted) <= max_length:
        return redacted
    return f"{redacted[: max_length - 3].rstrip()}..."
