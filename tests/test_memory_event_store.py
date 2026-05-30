"""T261 MemoryEvent local store tests.

All memory events are synthetic. These tests define file-backed storage only;
they do not implement retrieval ranking, dialogue generation, proactive
behavior, delivery, or external platform integration.
"""

from __future__ import annotations

import json
from pathlib import Path

from practical_chat_agent.core.models import MemoryEvent, MemoryProvenance
from practical_chat_agent.services.memory_event_store import MemoryEventStore


def _store(tmp_path: Path) -> MemoryEventStore:
    return MemoryEventStore(tmp_path / "memory_events.json")


def _provenance(**overrides: object) -> MemoryProvenance:
    data: dict[str, object] = {
        "source_type": "synthetic_test",
        "evidence_refs": ["synthetic_event_001"],
    }
    data.update(overrides)
    return MemoryProvenance(**data)


def _event(event_type: str, *, user_id: str = "user_synthetic") -> MemoryEvent:
    if event_type == "factual":
        return MemoryEvent(
            user_id=user_id,
            event_type="factual",
            truth_status="evidence_backed",
            summary="User said they prefer concise check-ins.",
            provenance=_provenance(),
            sensitivity="low",
        )
    if event_type == "inferred":
        return MemoryEvent(
            user_id=user_id,
            event_type="inferred",
            truth_status="inferred",
            summary="User may prefer practical comfort.",
            provenance=_provenance(),
            sensitivity="low",
            confidence=0.72,
            inference_rationale="Synthetic repeated preference signal.",
        )
    if event_type == "relational":
        return MemoryEvent(
            user_id=user_id,
            event_type="relational",
            truth_status="relationship_state",
            summary="Trust increased after a repair conversation.",
            provenance=_provenance(),
            sensitivity="low",
            relationship_dimensions=["trust", "repair_state"],
        )
    if event_type == "procedural":
        return MemoryEvent(
            user_id=user_id,
            event_type="procedural",
            truth_status="procedural_preference",
            summary="Use concise replies and ask before giving advice.",
            provenance=_provenance(),
            sensitivity="low",
            preference_labels=["concise_reply", "ask_before_advice"],
        )
    return MemoryEvent(
        user_id=user_id,
        event_type="imagined",
        truth_status="imagined",
        summary="Fictional persona dreamed about a quiet bookstore.",
        provenance=MemoryProvenance(source_type="imagined_generation"),
        sensitivity="low",
        imagined_context_label="dream_log",
    )


class TestMemoryEventStoreAppendAndQuery:
    def test_store_preserves_type_and_truth_separation(self, tmp_path: Path) -> None:
        store = _store(tmp_path)
        events = [_event(event_type) for event_type in ("factual", "inferred", "relational", "procedural", "imagined")]

        records = [store.append(event) for event in events]

        assert store.path.is_file()
        assert [record.operation for record in records] == ["append"] * 5
        assert len(store.list_events()) == 5
        assert [event.truth_status for event in store.list_events()] == [
            "evidence_backed",
            "inferred",
            "relationship_state",
            "procedural_preference",
            "imagined",
        ]
        assert store.list_by_event_type("factual")[0].truth_status == "evidence_backed"
        assert store.list_by_event_type("imagined")[0].truth_status == "imagined"

    def test_list_by_user_and_get_event_use_latest_record(self, tmp_path: Path) -> None:
        store = _store(tmp_path)
        first = store.append(_event("factual", user_id="user_a"))
        store.append(_event("procedural", user_id="user_b"))

        assert [event.user_id for event in store.list_by_user("user_a")] == ["user_a"]
        assert store.get(first.event_id).event_id == first.event_id


class TestMemoryEventStoreLifecycleAndExport:
    def test_lifecycle_updates_make_memory_retrieval_ineligible(self, tmp_path: Path) -> None:
        store = _store(tmp_path)
        saved = store.append(_event("factual"))

        frozen = store.update_lifecycle(saved.event_id, "frozen")
        deleted = store.update_lifecycle(saved.event_id, "deleted")

        assert frozen.operation == "lifecycle_update"
        assert frozen.event.lifecycle_state == "frozen"
        assert not frozen.event.is_retrieval_eligible("factual")
        assert deleted.event.lifecycle_state == "deleted"
        assert not deleted.event.is_retrieval_eligible("factual")
        assert len(store.list_records(include_history=True)) == 3

    def test_imagined_events_are_never_returned_by_factual_helpers(self, tmp_path: Path) -> None:
        store = _store(tmp_path)
        factual = store.append(_event("factual")).event
        store.append(_event("imagined"))

        factual_events = store.list_factual_events()

        assert [event.event_id for event in factual_events] == [factual.event_id]
        assert all(event.event_type == "factual" for event in factual_events)
        assert all(event.truth_status == "evidence_backed" for event in factual_events)

    def test_export_safe_json_omits_private_and_delivery_fields(self, tmp_path: Path) -> None:
        store = _store(tmp_path)
        store.append(_event("factual"))
        store.append(_event("imagined"))

        exported = store.export_safe_json()
        serialized = json.dumps(exported, ensure_ascii=False)

        assert exported["schema_version"] == "memory_event_store_export_v2"
        assert len(exported["records"]) == 2
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


class TestMemoryEventStoreSurfaceArea:
    def test_store_does_not_expose_runtime_or_delivery_methods(self, tmp_path: Path) -> None:
        store = _store(tmp_path)

        for method_name in (
            "send",
            "schedule",
            "deliver",
            "execute",
            "run_runtime",
            "rank_for_dialogue",
            "attach_to_dialogue_engine",
        ):
            assert not hasattr(store, method_name)
