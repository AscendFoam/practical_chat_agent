from __future__ import annotations

from abc import ABC, abstractmethod

from practical_chat_agent.core.models import AgentProfile, AuditLogEntry, InboundEvent, MemoryFact


class EventRepository(ABC):
    @abstractmethod
    def add(self, event: InboundEvent) -> None: ...

    @abstractmethod
    def get(self, event_id: str) -> InboundEvent | None: ...

    @abstractmethod
    def list_recent_for_channel(self, channel_id: str, *, limit: int = 20) -> list[InboundEvent]: ...


class AgentRepository(ABC):
    @abstractmethod
    def upsert(self, profile: AgentProfile) -> None: ...

    @abstractmethod
    def get(self, agent_id: str) -> AgentProfile | None: ...


class MemoryRepository(ABC):
    @abstractmethod
    def upsert(self, memory: MemoryFact) -> None: ...

    @abstractmethod
    def list_for_user(self, *, agent_id: str, user_id: str, limit: int = 10) -> list[MemoryFact]: ...


class AuditRepository(ABC):
    @abstractmethod
    def add(self, entry: AuditLogEntry) -> None: ...

