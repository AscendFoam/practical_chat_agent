"""Local JSON version store for PersonaCard records."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field

from practical_chat_agent.core.models import PersonaCard, utc_now
from practical_chat_agent.services.persona_review import PersonaReviewService


PersonaVersionOperation = Literal["save", "rollback", "freeze", "delete"]


class PersonaVersionRecord(BaseModel):
    schema_version: str = "persona_version_record_v1"
    version_id: str
    persona_id: str
    version_number: int = Field(..., ge=1)
    operation: PersonaVersionOperation = "save"
    card: PersonaCard
    parent_version_id: str | None = None
    deleted: bool = False
    created_at: datetime = Field(default_factory=utc_now)


class PersonaVersionStoreFile(BaseModel):
    schema_version: str = "persona_version_store_v1"
    records: list[PersonaVersionRecord] = Field(default_factory=list)


class PersonaVersionStore:
    """File-backed append-only PersonaCard version store."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

    def save(self, card: PersonaCard) -> PersonaVersionRecord:
        return self._append(card=card, operation="save", deleted=False)

    def list_versions(self, persona_id: str) -> list[PersonaVersionRecord]:
        store_file = self._load()
        return [record for record in store_file.records if record.persona_id == persona_id]

    def latest_record(self, persona_id: str, *, include_deleted: bool = False) -> PersonaVersionRecord:
        records = self.list_versions(persona_id)
        if not include_deleted:
            records = [record for record in records if not record.deleted]
        if not records:
            raise ValueError(f"no PersonaCard versions found for {persona_id}")
        return max(records, key=lambda record: record.version_number)

    def latest_card(self, persona_id: str) -> PersonaCard:
        return self.latest_record(persona_id).card

    def rollback(self, persona_id: str, version_id: str) -> PersonaVersionRecord:
        target = self._find_record(persona_id=persona_id, version_id=version_id)
        latest = self.latest_record(persona_id, include_deleted=True)
        card = target.card.model_copy(deep=True, update={"updated_at": utc_now()})
        return self._append(
            card=card,
            operation="rollback",
            deleted=False,
            parent_version_id=latest.version_id,
        )

    def freeze(self, persona_id: str, *, reviewer_id: str) -> PersonaVersionRecord:
        latest = self.latest_record(persona_id)
        frozen = PersonaReviewService().review(
            latest.card,
            decision="freeze",
            reviewer_id=reviewer_id,
            notes=["frozen by persona version store"],
        )
        return self._append(
            card=frozen,
            operation="freeze",
            deleted=False,
            parent_version_id=latest.version_id,
        )

    def delete(self, persona_id: str, *, reason: str) -> PersonaVersionRecord:
        latest = self.latest_record(persona_id, include_deleted=True)
        archived = latest.card.model_copy(
            deep=True,
            update={
                "status": "archived",
                "updated_at": utc_now(),
            },
        )
        return self._append(
            card=archived,
            operation="delete",
            deleted=True,
            parent_version_id=latest.version_id,
            notes=[reason],
        )

    def export_persona(self, persona_id: str) -> dict[str, object]:
        return {
            "schema_version": "persona_version_store_export_v1",
            "persona_id": persona_id,
            "versions": [
                record.model_dump(mode="json")
                for record in self.list_versions(persona_id)
            ],
        }

    def _append(
        self,
        *,
        card: PersonaCard,
        operation: PersonaVersionOperation,
        deleted: bool,
        parent_version_id: str | None = None,
        notes: list[str] | None = None,
    ) -> PersonaVersionRecord:
        store_file = self._load()
        persona_records = [record for record in store_file.records if record.persona_id == card.persona_id]
        version_number = max([record.version_number for record in persona_records], default=0) + 1
        if parent_version_id is None and persona_records:
            parent_version_id = max(persona_records, key=lambda record: record.version_number).version_id

        stored_card = card.model_copy(
            deep=True,
            update={
                "version": version_number,
                "updated_at": utc_now(),
            },
        )
        if notes:
            stored_card.review_metadata.decision_notes.extend(notes)

        record = PersonaVersionRecord(
            version_id=f"{card.persona_id}_v{version_number}",
            persona_id=card.persona_id,
            version_number=version_number,
            operation=operation,
            card=stored_card,
            parent_version_id=parent_version_id,
            deleted=deleted,
        )
        store_file.records.append(record)
        self._save(store_file)
        return record

    def _find_record(self, *, persona_id: str, version_id: str) -> PersonaVersionRecord:
        for record in self.list_versions(persona_id):
            if record.version_id == version_id:
                return record
        raise ValueError(f"version {version_id} not found for {persona_id}")

    def _load(self) -> PersonaVersionStoreFile:
        if not self.path.exists():
            return PersonaVersionStoreFile()
        return PersonaVersionStoreFile.model_validate_json(self.path.read_text(encoding="utf-8"))

    def _save(self, store_file: PersonaVersionStoreFile) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(store_file.model_dump_json(indent=2), encoding="utf-8")
