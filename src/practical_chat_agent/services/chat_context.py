from __future__ import annotations

from practical_chat_agent.core.models import (
    AgentProfile,
    ChatContext,
    ChatContextEvent,
    InboundEvent,
    MemoryFact,
    MemoryProfileSnapshot,
)


class ChatContextAssembler:
    """Build a compact chat context from recent events and long-term memory hits."""

    def __init__(
        self,
        *,
        recent_events_limit: int = 8,
        memory_hits_limit: int = 8,
    ) -> None:
        self.recent_events_limit = max(int(recent_events_limit), 1)
        self.memory_hits_limit = max(int(memory_hits_limit), 1)

    def assemble(
        self,
        *,
        agent: AgentProfile,
        event: InboundEvent,
        recent_events: list[InboundEvent],
        memory_hits: list[MemoryFact],
        intent,
        memory_candidate_count: int = 0,
        memory_profile: MemoryProfileSnapshot | None = None,
        memory_retrieval_notes: list[str] | None = None,
    ) -> ChatContext:
        rendered_events = [
            ChatContextEvent(
                event_id=item.event_id,
                actor_id=item.actor_id,
                actor_name=item.actor_name,
                direction=item.direction,
                content_type=item.content_type,
                source_type=item.source_type,
                occurred_at=item.occurred_at,
                text=item.text,
            )
            for item in recent_events[-self.recent_events_limit :]
        ]
        selected_memory_hits = memory_hits[: self.memory_hits_limit]
        summary = self._build_summary(
            agent=agent,
            event=event,
            recent_events=rendered_events,
            memory_hits=selected_memory_hits,
            memory_profile=memory_profile or MemoryProfileSnapshot(),
        )
        return ChatContext(
            agent_id=agent.agent_id,
            agent_display_name=agent.display_name,
            persona_type=agent.persona_type,
            relationship_mode=agent.relationship_mode,
            speech_style=agent.speech_style,
            channel_id=event.channel_id,
            channel_type=event.channel_type,
            platform=event.platform,
            user_id=event.actor_id,
            user_name=event.actor_name,
            intent=intent,
            latest_message_text=(event.text or "").strip() or None,
            recent_events=rendered_events,
            memory_hits=selected_memory_hits,
            memory_candidate_count=max(int(memory_candidate_count), len(selected_memory_hits)),
            memory_profile=memory_profile or MemoryProfileSnapshot(),
            memory_retrieval_notes=list(memory_retrieval_notes or []),
            summary=summary,
        )

    @staticmethod
    def _build_summary(
        *,
        agent: AgentProfile,
        event: InboundEvent,
        recent_events: list[ChatContextEvent],
        memory_hits: list[MemoryFact],
        memory_profile: MemoryProfileSnapshot,
    ) -> str:
        user_name = event.actor_name or event.actor_id
        latest_text = (event.text or "").strip()
        if len(latest_text) > 96:
            latest_text = f"{latest_text[:93].rstrip()}..."
        memory_preview = ", ".join(memory.fact for memory in memory_hits[:2] if memory.fact.strip())
        if len(memory_preview) > 120:
            memory_preview = f"{memory_preview[:117].rstrip()}..."
        pieces = [
            f"{agent.display_name} is handling a {event.channel_type.value} chat on {event.platform.value}.",
            f"Latest inbound message from {user_name}: {latest_text or '<empty>'}.",
            f"Recent window contains {len(recent_events)} events.",
        ]
        if memory_hits:
            pieces.append(f"Known memory hints: {memory_preview}.")
        if memory_profile is not None and memory_profile.summary:
            pieces.append(f"User profile snapshot: {memory_profile.summary}.")
        return " ".join(piece for piece in pieces if piece)
