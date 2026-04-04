from __future__ import annotations

from sqlalchemy import desc, select
from sqlalchemy.orm import Session, sessionmaker

from practical_chat_agent.core.enums import (
    ChannelType,
    ContentType,
    Direction,
    MemoryScope,
    MemoryType,
    PersonaType,
    Platform,
    SafetyMode,
    SourceType,
)
from practical_chat_agent.core.models import AgentProfile, AuditLogEntry, InboundEvent, MemoryFact
from practical_chat_agent.storage.mysql.models import (
    AgentModel,
    AgentProfileModel,
    AuditLogModel,
    EventModel,
    MemoryModel,
)
from practical_chat_agent.storage.repositories.base import (
    AgentRepository,
    AuditRepository,
    EventRepository,
    MemoryRepository,
)


class SqlAlchemyEventRepository(EventRepository):
    def __init__(self, session_factory: sessionmaker[Session]) -> None:
        self.session_factory = session_factory

    def add(self, event: InboundEvent) -> None:
        with self.session_factory() as session:
            model = EventModel(
                event_id=event.event_id,
                tenant_id=event.tenant_id,
                source_type=event.source_type.value,
                platform=event.platform.value,
                channel_id=event.channel_id,
                channel_type=event.channel_type.value,
                account_id=event.account_id,
                actor_id=event.actor_id,
                actor_name=event.actor_name,
                direction=event.direction.value,
                content_type=event.content_type.value,
                occurred_at=event.occurred_at,
                text_body=event.text,
                attachments=event.attachments,
                raw_payload=event.raw,
                created_at=event.occurred_at,
            )
            session.merge(model)
            session.commit()

    def get(self, event_id: str) -> InboundEvent | None:
        with self.session_factory() as session:
            model = session.get(EventModel, event_id)
            return None if model is None else _to_event(model)

    def list_recent_for_channel(self, channel_id: str, *, limit: int = 20) -> list[InboundEvent]:
        with self.session_factory() as session:
            rows = session.scalars(
                select(EventModel)
                .where(EventModel.channel_id == channel_id)
                .order_by(desc(EventModel.occurred_at))
                .limit(limit),
            ).all()
            return [_to_event(row) for row in reversed(rows)]


class SqlAlchemyAgentRepository(AgentRepository):
    def __init__(self, session_factory: sessionmaker[Session]) -> None:
        self.session_factory = session_factory

    def upsert(self, profile: AgentProfile) -> None:
        with self.session_factory() as session:
            session.merge(
                AgentModel(
                    agent_id=profile.agent_id,
                    display_name=profile.display_name,
                    persona_type=profile.persona_type.value,
                    system_identity=profile.system_identity,
                    public_disclosure=profile.public_disclosure,
                    relationship_mode=profile.relationship_mode,
                    safety_mode=profile.safety_mode.value,
                    created_at=profile.created_at,
                    updated_at=profile.updated_at,
                ),
            )
            session.merge(
                AgentProfileModel(
                    agent_id=profile.agent_id,
                    core_traits=profile.core_traits,
                    speech_style=profile.speech_style,
                    interests=profile.interests,
                    do_not_do=profile.do_not_do,
                ),
            )
            session.commit()

    def get(self, agent_id: str) -> AgentProfile | None:
        with self.session_factory() as session:
            agent = session.get(AgentModel, agent_id)
            profile = session.get(AgentProfileModel, agent_id)
            if agent is None or profile is None:
                return None
            return AgentProfile(
                agent_id=agent.agent_id,
                display_name=agent.display_name,
                persona_type=PersonaType(agent.persona_type),
                system_identity=agent.system_identity,
                public_disclosure=agent.public_disclosure
                or "This account is operated by an AI persona.",
                core_traits=profile.core_traits,
                speech_style=profile.speech_style,
                interests=profile.interests,
                relationship_mode=agent.relationship_mode,
                safety_mode=SafetyMode(agent.safety_mode),
                do_not_do=profile.do_not_do,
                created_at=agent.created_at,
                updated_at=agent.updated_at,
            )


class SqlAlchemyMemoryRepository(MemoryRepository):
    def __init__(self, session_factory: sessionmaker[Session]) -> None:
        self.session_factory = session_factory

    def upsert(self, memory: MemoryFact) -> None:
        with self.session_factory() as session:
            session.merge(
                MemoryModel(
                    memory_id=memory.memory_id,
                    agent_id=memory.agent_id,
                    user_id=memory.user_id,
                    memory_type=memory.memory_type.value,
                    scope=memory.scope.value,
                    salience=memory.salience,
                    confidence=memory.confidence,
                    fact=memory.fact,
                    evidence_refs=memory.evidence_refs,
                    created_at=memory.created_at,
                    updated_at=memory.updated_at,
                ),
            )
            session.commit()

    def list_for_user(self, *, agent_id: str, user_id: str, limit: int = 10) -> list[MemoryFact]:
        with self.session_factory() as session:
            rows = session.scalars(
                select(MemoryModel)
                .where(MemoryModel.agent_id == agent_id, MemoryModel.user_id == user_id)
                .order_by(desc(MemoryModel.updated_at))
                .limit(limit),
            ).all()
            return [
                MemoryFact(
                    memory_id=row.memory_id,
                    agent_id=row.agent_id,
                    user_id=row.user_id,
                    memory_type=MemoryType(row.memory_type),
                    scope=MemoryScope(row.scope),
                    salience=row.salience,
                    confidence=row.confidence,
                    fact=row.fact,
                    evidence_refs=row.evidence_refs,
                    created_at=row.created_at,
                    updated_at=row.updated_at,
                )
                for row in rows
            ]


class SqlAlchemyAuditRepository(AuditRepository):
    def __init__(self, session_factory: sessionmaker[Session]) -> None:
        self.session_factory = session_factory

    def add(self, entry: AuditLogEntry) -> None:
        with self.session_factory() as session:
            session.merge(
                AuditLogModel(
                    audit_id=entry.audit_id,
                    agent_id=entry.agent_id,
                    action=entry.action,
                    status=entry.status,
                    details=entry.details,
                    created_at=entry.created_at,
                ),
            )
            session.commit()


def _to_event(model: EventModel) -> InboundEvent:
    return InboundEvent(
        event_id=model.event_id,
        tenant_id=model.tenant_id,
        source_type=SourceType(model.source_type),
        platform=Platform(model.platform),
        channel_id=model.channel_id,
        channel_type=ChannelType(model.channel_type),
        account_id=model.account_id,
        actor_id=model.actor_id,
        actor_name=model.actor_name,
        direction=Direction(model.direction),
        content_type=ContentType(model.content_type),
        occurred_at=model.occurred_at,
        text=model.text_body,
        attachments=model.attachments,
        raw=model.raw_payload,
    )
