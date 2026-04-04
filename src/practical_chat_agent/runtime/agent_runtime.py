from __future__ import annotations

from practical_chat_agent.core.bus import InMemoryEventBus
from practical_chat_agent.core.enums import ActionKind, ContentType, Direction
from practical_chat_agent.core.events import RuntimeEvent
from practical_chat_agent.core.models import (
    ActionPlan,
    AgentTurnResult,
    AuditLogEntry,
    InboundEvent,
    MemoryFact,
)
from practical_chat_agent.storage.repositories.base import (
    AgentRepository,
    AuditRepository,
    EventRepository,
    MemoryRepository,
)


class AgentRuntime:
    """Minimal runtime loop that persists inbound events and builds reply drafts."""

    def __init__(
        self,
        *,
        agent_repository: AgentRepository,
        event_repository: EventRepository,
        memory_repository: MemoryRepository,
        audit_repository: AuditRepository,
        event_bus: InMemoryEventBus | None = None,
    ) -> None:
        self.agent_repository = agent_repository
        self.event_repository = event_repository
        self.memory_repository = memory_repository
        self.audit_repository = audit_repository
        self.event_bus = event_bus

    def handle_inbound_event(self, *, agent_id: str, event: InboundEvent) -> AgentTurnResult:
        agent = self.agent_repository.get(agent_id)
        if agent is None:
            raise ValueError(f"Unknown agent: {agent_id}")

        self.event_repository.add(event)
        recent_events = self.event_repository.list_recent_for_channel(event.channel_id, limit=6)
        memory_hits = self.memory_repository.list_for_user(agent_id=agent_id, user_id=event.actor_id, limit=5)

        should_reply = (
            event.direction == Direction.INBOUND
            and event.content_type == ContentType.TEXT
            and bool((event.text or "").strip())
        )

        memory_updates: list[MemoryFact] = []
        if should_reply and len((event.text or "").split()) >= 6:
            memory_updates.append(
                MemoryFact(
                    agent_id=agent_id,
                    user_id=event.actor_id,
                    fact=f"User recently said: {(event.text or '').strip()}",
                    evidence_refs=[event.event_id],
                ),
            )
            for memory in memory_updates:
                self.memory_repository.upsert(memory)

        actions: list[ActionPlan] = []
        reasoning = "Inbound event stored. No reply generated."

        if should_reply:
            draft = self._build_reply_draft(
                agent_name=agent.display_name,
                event=event,
                recent_events_count=len(recent_events),
                memory_hits_count=len(memory_hits),
            )
            actions.append(
                ActionPlan(
                    kind=ActionKind.REPLY_DRAFT,
                    channel_id=event.channel_id,
                    message_text=draft,
                    metadata={
                        "recent_events_count": len(recent_events),
                        "memory_hits_count": len(memory_hits),
                    },
                ),
            )
            reasoning = "Inbound text message matched reply conditions and produced a draft reply."

        self.audit_repository.add(
            AuditLogEntry(
                agent_id=agent_id,
                action="agent_turn",
                status="processed",
                details={
                    "event_id": event.event_id,
                    "should_reply": should_reply,
                    "actions": [action.kind for action in actions],
                },
            ),
        )

        result = AgentTurnResult(
            agent_id=agent_id,
            event_id=event.event_id,
            should_reply=should_reply,
            actions=actions,
            memory_updates=memory_updates,
            reasoning=reasoning,
        )

        if self.event_bus is not None:
            self.event_bus.publish(
                RuntimeEvent(
                    topic="agent.turn.completed",
                    payload=result.model_dump(mode="json"),
                ),
            )

        return result

    @staticmethod
    def _build_reply_draft(
        *,
        agent_name: str,
        event: InboundEvent,
        recent_events_count: int,
        memory_hits_count: int,
    ) -> str:
        user_name = event.actor_name or event.actor_id
        text = (event.text or "").strip()
        return (
            f"{agent_name} draft reply to {user_name}: I saw your message "
            f"('{text}'). I am keeping {recent_events_count} recent events and "
            f"{memory_hits_count} memory hits in context for the next generation step."
        )
