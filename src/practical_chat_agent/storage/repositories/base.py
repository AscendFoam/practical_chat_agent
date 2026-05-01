from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime

from practical_chat_agent.core.models import (
    ActionExecutionRecord,
    AgentProfile,
    AuditLogEntry,
    InboundEvent,
    MeetingMinutesRecord,
    MeetingSegmentRecord,
    MeetingSessionRecord,
    MemoryFact,
    MemoryProfileRecord,
)


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

    @abstractmethod
    def get(self, memory_id: str) -> MemoryFact | None: ...

    @abstractmethod
    def list_for_agent(
        self,
        *,
        agent_id: str,
        user_id: str | None = None,
        limit: int = 100,
    ) -> list[MemoryFact]: ...

    @abstractmethod
    def delete(self, memory_id: str) -> None: ...

    @abstractmethod
    def add_profile_snapshot(self, profile: MemoryProfileRecord) -> MemoryProfileRecord: ...

    @abstractmethod
    def get_profile_snapshot(self, profile_id: str) -> MemoryProfileRecord | None: ...

    @abstractmethod
    def delete_profile_snapshot(self, profile_id: str) -> None: ...

    @abstractmethod
    def get_latest_profile_snapshot(self, *, agent_id: str, user_id: str) -> MemoryProfileRecord | None: ...

    @abstractmethod
    def list_profile_snapshots(
        self,
        *,
        agent_id: str,
        user_id: str,
        limit: int = 20,
    ) -> list[MemoryProfileRecord]: ...


class AuditRepository(ABC):
    @abstractmethod
    def add(self, entry: AuditLogEntry) -> None: ...


class ActionRepository(ABC):
    @abstractmethod
    def add(self, record: ActionExecutionRecord) -> ActionExecutionRecord: ...

    @abstractmethod
    def get(self, action_id: str) -> ActionExecutionRecord | None: ...

    @abstractmethod
    def update(self, record: ActionExecutionRecord) -> ActionExecutionRecord: ...

    @abstractmethod
    def list_recent(
        self,
        *,
        agent_id: str | None = None,
        status: str | None = None,
        channel_id: str | None = None,
        limit: int = 20,
    ) -> list[ActionExecutionRecord]: ...


class MeetingRepository(ABC):
    @abstractmethod
    def get_session_by_key(self, *, channel_id: str, meeting_key: str) -> MeetingSessionRecord | None: ...

    @abstractmethod
    def get_session(self, *, session_id: str) -> MeetingSessionRecord | None: ...

    @abstractmethod
    def upsert_session(self, session: MeetingSessionRecord) -> MeetingSessionRecord: ...

    @abstractmethod
    def add_segments(self, segments: list[MeetingSegmentRecord]) -> None: ...

    @abstractmethod
    def list_segments(
        self,
        *,
        session_id: str,
        limit: int | None = None,
        started_after: datetime | None = None,
        started_before: datetime | None = None,
    ) -> list[MeetingSegmentRecord]: ...

    @abstractmethod
    def list_recent_segments(self, *, session_id: str, limit: int = 20) -> list[MeetingSegmentRecord]: ...

    @abstractmethod
    def list_sessions(self, *, account_id: str | None = None, limit: int = 20) -> list[MeetingSessionRecord]: ...

    @abstractmethod
    def add_minutes(self, minutes: MeetingMinutesRecord) -> MeetingMinutesRecord: ...

    @abstractmethod
    def get_minutes(self, *, minutes_id: str) -> MeetingMinutesRecord | None: ...

    @abstractmethod
    def list_minutes(self, *, session_id: str, limit: int = 20) -> list[MeetingMinutesRecord]: ...
