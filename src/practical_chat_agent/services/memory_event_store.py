"""Local JSON store for MemoryEvent v2 records."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field

from practical_chat_agent.core.ids import new_id
from practical_chat_agent.core.models import (
    MemoryEvent,
    MemoryEventType,
    MemoryLifecycleState,
    utc_now,
)


MemoryEventStoreOperation = Literal["append", "lifecycle_update"]


class MemoryEventStoreRecord(BaseModel):
    schema_version: str = "memory_event_store_record_v2"
    record_id: str = Field(default_factory=lambda: new_id("memrec"))
    event: MemoryEvent
    operation: MemoryEventStoreOperation = "append"
    parent_record_id: str | None = None
    created_at: datetime = Field(default_factory=utc_now)

    @property
    def event_id(self) -> str:
        return self.event.event_id


class MemoryEventStoreFile(BaseModel):
    schema_version: str = "memory_event_store_v2"
    records: list[MemoryEventStoreRecord] = Field(default_factory=list)


class MemoryEventStore:
    """Caller-path local JSON store for MemoryEvent records."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

    def append(self, event: MemoryEvent) -> MemoryEventStoreRecord:
        return self._append(event=event, operation="append")

    def list_records(self, *, include_history: bool = False) -> list[MemoryEventStoreRecord]:
        records = self._load().records
        if include_history:
            return records
        latest_by_event_id: dict[str, MemoryEventStoreRecord] = {}
        for record in records:
            latest_by_event_id[record.event_id] = record
        return list(latest_by_event_id.values())

    def list_events(self) -> list[MemoryEvent]:
        return [record.event for record in self.list_records()]

    def list_by_user(self, user_id: str) -> list[MemoryEvent]:
        return [event for event in self.list_events() if event.user_id == user_id]

    def list_by_event_type(self, event_type: MemoryEventType) -> list[MemoryEvent]:
        return [event for event in self.list_events() if event.event_type == event_type]

    def list_factual_events(self, *, user_id: str | None = None) -> list[MemoryEvent]:
        events = self.list_by_event_type("factual")
        if user_id is not None:
            events = [event for event in events if event.user_id == user_id]
        return events

    def get(self, event_id: str) -> MemoryEvent:
        return self.get_record(event_id).event

    def get_record(self, event_id: str) -> MemoryEventStoreRecord:
        for record in reversed(self._load().records):
            if record.event_id == event_id:
                return record
        raise ValueError(f"memory event not found: {event_id}")

    def update_lifecycle(
        self,
        event_id: str,
        lifecycle_state: MemoryLifecycleState,
    ) -> MemoryEventStoreRecord:
        latest_record = self.get_record(event_id)
        updated_event = latest_record.event.model_copy(
            deep=True,
            update={
                "lifecycle_state": lifecycle_state,
                "updated_at": utc_now(),
            },
        )
        return self._append(
            event=updated_event,
            operation="lifecycle_update",
            parent_record_id=latest_record.record_id,
        )

    def export_safe_json(self) -> dict[str, object]:
        return {
            "schema_version": "memory_event_store_export_v2",
            "records": [
                record.model_dump(mode="json")
                for record in self.list_records(include_history=True)
            ],
        }

    def _append(
        self,
        *,
        event: MemoryEvent,
        operation: MemoryEventStoreOperation,
        parent_record_id: str | None = None,
    ) -> MemoryEventStoreRecord:
        store_file = self._load()
        record = MemoryEventStoreRecord(
            event=event,
            operation=operation,
            parent_record_id=parent_record_id,
        )
        store_file.records.append(record)
        self._save(store_file)
        return record

    def _load(self) -> MemoryEventStoreFile:
        if not self.path.exists():
            return MemoryEventStoreFile()
        return MemoryEventStoreFile.model_validate_json(self.path.read_text(encoding="utf-8"))

    def _save(self, store_file: MemoryEventStoreFile) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(store_file.model_dump_json(indent=2), encoding="utf-8")
