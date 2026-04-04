from __future__ import annotations

from dataclasses import dataclass

from practical_chat_agent.app.config import Settings, get_settings
from practical_chat_agent.core.bus import InMemoryEventBus
from practical_chat_agent.runtime.agent_runtime import AgentRuntime
from practical_chat_agent.storage.mysql.models import create_schema
from practical_chat_agent.storage.mysql.repositories import (
    SqlAlchemyAgentRepository,
    SqlAlchemyAuditRepository,
    SqlAlchemyEventRepository,
    SqlAlchemyMemoryRepository,
)
from practical_chat_agent.storage.mysql.session import (
    create_database_if_missing,
    create_engine_from_settings,
    create_session_factory,
)


@dataclass(slots=True)
class AppContainer:
    settings: Settings
    bus: InMemoryEventBus
    agent_repository: SqlAlchemyAgentRepository
    event_repository: SqlAlchemyEventRepository
    memory_repository: SqlAlchemyMemoryRepository
    audit_repository: SqlAlchemyAuditRepository
    runtime: AgentRuntime

    @classmethod
    def build(cls, settings: Settings | None = None) -> "AppContainer":
        resolved_settings = settings or get_settings()
        engine = create_engine_from_settings(resolved_settings)
        session_factory = create_session_factory(engine)

        bus = InMemoryEventBus()
        agent_repository = SqlAlchemyAgentRepository(session_factory)
        event_repository = SqlAlchemyEventRepository(session_factory)
        memory_repository = SqlAlchemyMemoryRepository(session_factory)
        audit_repository = SqlAlchemyAuditRepository(session_factory)

        runtime = AgentRuntime(
            agent_repository=agent_repository,
            event_repository=event_repository,
            memory_repository=memory_repository,
            audit_repository=audit_repository,
            event_bus=bus,
        )

        return cls(
            settings=resolved_settings,
            bus=bus,
            agent_repository=agent_repository,
            event_repository=event_repository,
            memory_repository=memory_repository,
            audit_repository=audit_repository,
            runtime=runtime,
        )

    def init_database(self) -> None:
        create_database_if_missing(self.settings)
        engine = create_engine_from_settings(self.settings)
        create_schema(engine)

