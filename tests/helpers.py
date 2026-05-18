"""Shared helper functions for T150 test fixtures.

All helpers construct synthetic objects with domain-neutral content.
No real chat text, real names, real platform IDs, or private paths.
"""
from __future__ import annotations

from datetime import datetime, timezone

from practical_chat_agent.core.enums import (
    ChannelType,
    ChatIntent,
    ContentType,
    Direction,
    MemoryScope,
    MemoryType,
    PersonaType,
    Platform,
    SourceType,
)
from practical_chat_agent.core.models import (
    ApprovedContactSkillBrief,
    ApprovedMemoryFactBrief,
    ApprovedStoreContext,
    ChatContext,
    ChatContextEvent,
    MemoryFact,
)


def event(
    event_id: str,
    text: str,
    direction: Direction = Direction.INBOUND,
) -> ChatContextEvent:
    return ChatContextEvent(
        event_id=event_id,
        actor_id="actor_synthetic",
        direction=direction,
        content_type=ContentType.TEXT,
        source_type=SourceType.CHAT_MESSAGE,
        occurred_at=datetime(2026, 1, 15, 10, 0, 0, tzinfo=timezone.utc),
        text=text,
    )


def memory(memory_id: str, fact: str) -> MemoryFact:
    return MemoryFact(
        memory_id=memory_id,
        agent_id="agent_synthetic",
        user_id="contact_synthetic",
        memory_type=MemoryType.FACT,
        scope=MemoryScope.LONG_TERM,
        fact=fact,
    )


def skill_brief(
    record_id: str = "approved_skill_001",
    contact_id: str = "contact_synthetic",
    relationship_type: str = "friend",
    relationship_summary: str = "synthetic casual contact",
    strategy_hints: list[str] | None = None,
    boundary_reminders: list[str] | None = None,
    evidence_refs: list[str] | None = None,
) -> ApprovedContactSkillBrief:
    return ApprovedContactSkillBrief(
        record_id=record_id,
        contact_id=contact_id,
        relationship_type=relationship_type,
        relationship_summary=relationship_summary,
        strategy_hints=strategy_hints or [],
        boundary_reminders=boundary_reminders or [],
        evidence_refs=evidence_refs or ["ev_synthetic_001"],
    )


def memory_brief(
    record_id: str = "approved_mem_001",
    claim: str = "synthetic approved fact",
    evidence_refs: list[str] | None = None,
) -> ApprovedMemoryFactBrief:
    return ApprovedMemoryFactBrief(
        record_id=record_id,
        memory_id="mem_synthetic_001",
        memory_type="semantic",
        claim=claim,
        evidence_refs=evidence_refs or ["ev_synthetic_002"],
    )


def context(
    contact_id: str = "contact_synthetic",
    latest_message_text: str | None = "synthetic inbound message",
    recent_events: list[ChatContextEvent] | None = None,
    memory_hits: list[MemoryFact] | None = None,
    intent: ChatIntent = ChatIntent.GENERAL,
    approved_store_context: ApprovedStoreContext | None = None,
) -> ChatContext:
    return ChatContext(
        agent_id="agent_synthetic",
        agent_display_name="Synthetic Agent",
        persona_type=PersonaType.FRIEND,
        relationship_mode="friend",
        channel_id="ch_synthetic",
        channel_type=ChannelType.DM,
        platform=Platform.WECHAT,
        user_id=contact_id,
        intent=intent,
        latest_message_text=latest_message_text,
        recent_events=recent_events or [],
        memory_hits=memory_hits or [],
        approved_store_context=approved_store_context or ApprovedStoreContext(),
    )
