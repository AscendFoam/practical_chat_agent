"""T254 Persona version-store tests.

All PersonaCards are synthetic. These tests define local JSON persistence only;
they do not wire personas into dialogue, memory retrieval, proactive behavior,
delivery, or external platforms.
"""

from __future__ import annotations

import json
from pathlib import Path

from practical_chat_agent.core.models import PersonaIdentity
from practical_chat_agent.services.persona_compiler import PersonaCompilerService
from practical_chat_agent.services.persona_review import PersonaReviewService
from practical_chat_agent.services.persona_version_store import PersonaVersionStore


def _store(tmp_path: Path) -> PersonaVersionStore:
    return PersonaVersionStore(tmp_path / "persona_versions.json")


def _card():
    return PersonaCompilerService().compile(
        {
            "user_id": "user_synthetic",
            "display_name": "Lin Qi",
            "creation_mode": "detailed_prompt",
            "description": "fictional calm concise companion with dry humor",
        }
    )


def _approved_card():
    return PersonaReviewService().review(
        _card(),
        decision="approve",
        reviewer_id="human_reviewer_1",
    )


class TestPersonaVersionStoreSaveAndLookup:
    def test_saving_candidate_card_creates_version_one(self, tmp_path: Path) -> None:
        store = _store(tmp_path)
        card = _card()

        record = store.save(card)

        assert record.schema_version == "persona_version_record_v1"
        assert record.version_number == 1
        assert record.operation == "save"
        assert record.card.persona_id == card.persona_id
        assert store.path.is_file()
        assert store.latest_record(card.persona_id).version_id == record.version_id

    def test_saving_approved_review_copy_creates_later_version(self, tmp_path: Path) -> None:
        store = _store(tmp_path)
        first = store.save(_card())
        approved = _approved_card().model_copy(update={"persona_id": first.persona_id})

        second = store.save(approved)

        assert second.version_number == 2
        assert second.parent_version_id == first.version_id
        latest = store.latest_record(first.persona_id)
        assert latest.version_id == second.version_id
        assert latest.card.status == "approved"
        assert latest.card.is_runtime_ready()

    def test_latest_lookup_returns_latest_non_deleted_version(self, tmp_path: Path) -> None:
        store = _store(tmp_path)
        first = store.save(_card())
        edited = first.card.model_copy(
            deep=True,
            update={
                "display_name": "Lin Qi Edited",
                "identity": PersonaIdentity(display_name="Lin Qi Edited", fictional=True),
            },
        )
        second = store.save(edited)

        assert store.latest_record(first.persona_id).version_id == second.version_id
        assert store.latest_card(first.persona_id).display_name == "Lin Qi Edited"


class TestPersonaVersionStoreControlOperations:
    def test_rollback_returns_prior_version_without_mutating_history(self, tmp_path: Path) -> None:
        store = _store(tmp_path)
        first = store.save(_card())
        edited = first.card.model_copy(
            deep=True,
            update={
                "display_name": "Lin Qi Edited",
                "identity": PersonaIdentity(display_name="Lin Qi Edited", fictional=True),
            },
        )
        second = store.save(edited)

        rollback = store.rollback(first.persona_id, first.version_id)

        assert rollback.operation == "rollback"
        assert rollback.version_number == 3
        assert rollback.parent_version_id == second.version_id
        assert rollback.card.display_name == "Lin Qi"
        assert [record.version_id for record in store.list_versions(first.persona_id)] == [
            first.version_id,
            second.version_id,
            rollback.version_id,
        ]

    def test_freeze_and_delete_states_prevent_runtime_readiness(self, tmp_path: Path) -> None:
        store = _store(tmp_path)
        approved = _approved_card()
        saved = store.save(approved)

        frozen = store.freeze(saved.persona_id, reviewer_id="human_reviewer_1")
        deleted = store.delete(saved.persona_id, reason="synthetic user deletion request")

        assert frozen.operation == "freeze"
        assert frozen.card.status == "frozen"
        assert not frozen.card.is_runtime_ready()
        assert deleted.operation == "delete"
        assert deleted.deleted is True
        assert deleted.card.status == "archived"
        assert not deleted.card.is_runtime_ready()

    def test_export_safe_json_omits_private_and_delivery_fields(self, tmp_path: Path) -> None:
        store = _store(tmp_path)
        saved = store.save(_card())

        exported = store.export_persona(saved.persona_id)
        serialized = json.dumps(exported, ensure_ascii=False)

        assert exported["schema_version"] == "persona_version_store_export_v1"
        assert exported["persona_id"] == saved.persona_id
        assert len(exported["versions"]) == 1
        for forbidden in (
            "raw_text",
            "raw_transcript",
            "chat_history",
            "private_messages",
            "send",
            "schedule",
            "delivery",
        ):
            assert forbidden not in serialized


class TestPersonaVersionStoreSurfaceArea:
    def test_store_does_not_expose_delivery_or_runtime_methods(self, tmp_path: Path) -> None:
        store = _store(tmp_path)

        for method_name in (
            "send",
            "schedule",
            "deliver",
            "execute",
            "run_runtime",
            "attach_to_memory_retrieval",
        ):
            assert not hasattr(store, method_name)
