from __future__ import annotations

from practical_chat_agent.core.bus import InMemoryEventBus
from practical_chat_agent.core.enums import ActionKind, ContentType, Direction, SourceType
from practical_chat_agent.core.events import RuntimeEvent
from practical_chat_agent.core.models import (
    ActionExecutionRecord,
    ActionPlan,
    AgentTurnResult,
    AuditLogEntry,
    ChatSuggestion,
    ChatContext,
    InboundEvent,
    MemoryFact,
    MemoryProfileRecord,
    MemoryRetrievalResult,
)
from practical_chat_agent.services.chat_context import ChatContextAssembler
from practical_chat_agent.services.chat_memory import ChatMemoryExtractionService
from practical_chat_agent.services.chat_suggestions import ChatSuggestionService
from practical_chat_agent.services.memory_retrieval import MemoryRetrievalService
from practical_chat_agent.services.policy import PolicyEngine
from practical_chat_agent.storage.repositories.base import (
    ActionRepository,
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
        action_repository: ActionRepository,
        chat_context_assembler: ChatContextAssembler,
        memory_retrieval_service: MemoryRetrievalService,
        chat_suggestion_service: ChatSuggestionService,
        chat_memory_service: ChatMemoryExtractionService,
        policy_engine: PolicyEngine,
        event_bus: InMemoryEventBus | None = None,
    ) -> None:
        self.agent_repository = agent_repository
        self.event_repository = event_repository
        self.memory_repository = memory_repository
        self.audit_repository = audit_repository
        self.action_repository = action_repository
        self.chat_context_assembler = chat_context_assembler
        self.memory_retrieval_service = memory_retrieval_service
        self.chat_suggestion_service = chat_suggestion_service
        self.chat_memory_service = chat_memory_service
        self.policy_engine = policy_engine
        self.event_bus = event_bus

    def handle_inbound_event(self, *, agent_id: str, event: InboundEvent) -> AgentTurnResult:
        agent = self.agent_repository.get(agent_id)
        if agent is None:
            raise ValueError(f"Unknown agent: {agent_id}")

        self.event_repository.add(event)
        recent_events = self.event_repository.list_recent_for_channel(
            event.channel_id,
            limit=self.chat_context_assembler.recent_events_limit,
        )
        memory_candidates = self.memory_repository.list_for_user(
            agent_id=agent_id,
            user_id=event.actor_id,
            limit=self.chat_context_assembler.memory_hits_limit * 4,
        )
        memory_retrieval = self.memory_retrieval_service.retrieve(
            agent=agent,
            event=event,
            candidate_memories=memory_candidates,
        )
        context = self._assemble_context(
            agent=agent,
            event=event,
            recent_events=recent_events,
            retrieval=memory_retrieval,
        )
        memory_hits = list(memory_retrieval.selected_hits)

        should_process_text = (
            event.direction == Direction.INBOUND
            and event.content_type == ContentType.TEXT
            and event.source_type != SourceType.MEETING_SEGMENT
            and bool((event.text or "").strip())
        )

        suggestions: list[ChatSuggestion] = []
        memory_updates: list[MemoryFact] = []
        no_reply_reason: str | None = None

        if event.source_type == SourceType.MEETING_SEGMENT:
            should_reply = False
            no_reply_reason = "Meeting transcript segment stored for future agent context. No reply draft generated."
        elif should_process_text:
            extracted_candidates = self.chat_memory_service.extract(
                agent=agent,
                event=event,
                context=context,
            )
            memory_updates = self.chat_memory_service.materialize(
                candidates=extracted_candidates,
                existing_memories=memory_candidates,
            )

            refreshed_candidate_memories = self._merge_memory_candidates(
                persisted_memories=memory_candidates,
                pending_updates=memory_updates,
            )
            refreshed_retrieval = self.memory_retrieval_service.retrieve(
                agent=agent,
                event=event,
                candidate_memories=refreshed_candidate_memories,
            )
            refreshed_notes = list(refreshed_retrieval.retrieval_notes)
            if memory_updates:
                refreshed_notes.append(
                    f"same-turn refresh included {len(memory_updates)} newly extracted memory updates",
                )
            else:
                refreshed_notes.append("same-turn refresh found no new durable memory updates")
            refreshed_retrieval = refreshed_retrieval.model_copy(
                update={"retrieval_notes": refreshed_notes},
            )
            context = self._assemble_context(
                agent=agent,
                event=event,
                recent_events=recent_events,
                retrieval=refreshed_retrieval,
            )
            memory_hits = list(refreshed_retrieval.selected_hits)
            self.memory_repository.add_profile_snapshot(
                MemoryProfileRecord(
                    agent_id=agent.agent_id,
                    user_id=event.actor_id,
                    source_event_id=event.event_id,
                    backend=self.memory_retrieval_service.backend_name,
                    model=self.memory_retrieval_service.resolved_model,
                    summary=context.memory_profile.summary,
                    snapshot=context.memory_profile,
                    memory_count=len(refreshed_candidate_memories),
                ),
            )

            suggestion = self.chat_suggestion_service.generate(agent=agent, context=context)
            suggestions.append(suggestion)
            should_reply = suggestion.should_reply and bool((suggestion.reply_draft or "").strip())
            if not should_reply:
                no_reply_reason = suggestion.rationale or "Suggestion service recommended no reply."
            for memory in memory_updates:
                self.memory_repository.upsert(memory)
        else:
            should_reply = False
            suggestions.append(
                ChatSuggestion(
                    backend="heuristic_fallback",
                    status="skipped",
                    should_reply=False,
                    summary="Inbound event did not qualify for a chat suggestion.",
                    rationale="Non-text or non-inbound event.",
                ),
            )

        actions: list[ActionPlan] = []
        reasoning = "Inbound event stored. No reply generated."

        if should_reply:
            draft = suggestions[0].reply_draft if suggestions else None
            if not draft:
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
                        "suggestion_backend": suggestions[0].backend if suggestions else None,
                        "suggestion_status": suggestions[0].status if suggestions else None,
                    },
                ),
            )
            self._persist_action_plans(
                agent=agent,
                event=event,
                actions=actions,
            )
            reasoning = "Inbound text message matched reply conditions and produced a draft reply."
        elif no_reply_reason:
            reasoning = no_reply_reason

        self.audit_repository.add(
            AuditLogEntry(
                agent_id=agent_id,
                action="agent_turn",
                status="processed",
                details={
                    "event_id": event.event_id,
                    "should_reply": should_reply,
                    "suggestion_count": len(suggestions),
                    "memory_update_count": len(memory_updates),
                    "actions": [action.kind for action in actions],
                    "action_ids": [action.action_id for action in actions],
                },
            ),
        )

        result = AgentTurnResult(
            agent_id=agent_id,
            event_id=event.event_id,
            should_reply=should_reply,
            context=context,
            suggestions=suggestions,
            actions=actions,
            memory_hits=memory_hits,
            memory_updates=memory_updates,
            no_reply_reason=no_reply_reason,
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

    def _assemble_context(
        self,
        *,
        agent,
        event: InboundEvent,
        recent_events: list[InboundEvent],
        retrieval: MemoryRetrievalResult,
    ) -> ChatContext:
        return self.chat_context_assembler.assemble(
            agent=agent,
            event=event,
            recent_events=recent_events,
            memory_hits=retrieval.selected_hits,
            intent=retrieval.intent,
            memory_candidate_count=retrieval.candidate_count,
            memory_profile=retrieval.profile,
            memory_retrieval_notes=retrieval.retrieval_notes,
        )

    @staticmethod
    def _merge_memory_candidates(
        *,
        persisted_memories: list[MemoryFact],
        pending_updates: list[MemoryFact],
    ) -> list[MemoryFact]:
        merged_by_id: dict[str, MemoryFact] = {memory.memory_id: memory for memory in persisted_memories}
        for memory in pending_updates:
            merged_by_id[memory.memory_id] = memory
        return sorted(
            merged_by_id.values(),
            key=lambda memory: memory.updated_at,
            reverse=True,
        )

    def _persist_action_plans(self, *, agent, event: InboundEvent, actions: list[ActionPlan]) -> None:
        for action in actions:
            record = ActionExecutionRecord(
                action_id=action.action_id,
                agent_id=agent.agent_id,
                event_id=event.event_id,
                kind=action.kind,
                platform=event.platform,
                channel_id=action.channel_id,
                channel_type=event.channel_type,
                account_id=event.account_id,
                actor_id=event.actor_id,
                connector_name=self._raw_connector_name(event),
                message_text=action.message_text,
                requires_approval=action.requires_approval,
                metadata=action.metadata,
            )
            decision = self.policy_engine.review_outbound_action(
                action=record,
                agent=agent,
                event=event,
            )
            stored_record = record.model_copy(
                update={
                    "requires_approval": decision.requires_approval,
                    "policy_decision": decision,
                    "status": self.policy_engine.initial_status(decision),
                },
            )
            self.action_repository.add(stored_record)
            self.audit_repository.add(
                AuditLogEntry(
                    agent_id=agent.agent_id,
                    action="action_plan_created",
                    status=stored_record.status.value,
                    details={
                        "action_id": stored_record.action_id,
                        "event_id": event.event_id,
                        "kind": stored_record.kind.value,
                        "platform": stored_record.platform.value,
                        "channel_id": stored_record.channel_id,
                        "policy_decision": decision.model_dump(mode="json"),
                    },
                ),
            )

    @staticmethod
    def _raw_connector_name(event: InboundEvent) -> str | None:
        direct = event.raw.get("connector_name")
        if isinstance(direct, str) and direct:
            return direct
        meta = event.raw.get("_meta")
        if isinstance(meta, dict):
            meta_name = meta.get("connector_name")
            if isinstance(meta_name, str) and meta_name:
                return meta_name
        return None

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
