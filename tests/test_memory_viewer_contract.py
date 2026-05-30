"""T301 Memory viewer data contract tests.

All records are synthetic. These tests define read-only viewer objects only;
they do not build UI, mutate records, delete records, export records, or
connect to external platforms.
"""

from __future__ import annotations

import json

from practical_chat_agent.core.models import (
    MemoryEvent,
    MemoryProvenance,
    MemoryViewerFilter,
    MemoryViewerItem,
    MemoryViewerPage,
)


def _factual(**overrides: object) -> MemoryEvent:
    data: dict[str, object] = {
        "user_id": "user_synthetic",
        "event_type": "factual",
        "truth_status": "evidence_backed",
        "summary": "User prefers concise check-ins.",
        "provenance": MemoryProvenance(source_type="synthetic_test", evidence_refs=["synthetic_event_001"]),
        "sensitivity": "low",
    }
    data.update(overrides)
    return MemoryEvent(**data)


def _imagined(**overrides: object) -> MemoryEvent:
    data: dict[str, object] = {
        "user_id": "user_synthetic",
        "event_type": "imagined",
        "truth_status": "imagined",
        "summary": "Fictional persona imagined a quiet bookstore.",
        "provenance": MemoryProvenance(source_type="imagined_generation"),
        "sensitivity": "low",
        "imagined_context_label": "virtual_life",
    }
    data.update(overrides)
    return MemoryEvent(**data)


class TestMemoryViewerItem:
    def test_from_event_preserves_read_only_memory_fields(self) -> None:
        event = _factual()

        item = MemoryViewerItem.from_event(event)

        assert item.schema_version == "memory_viewer_item_v1"
        assert item.memory_id == event.event_id
        assert item.user_id == "user_synthetic"
        assert item.event_type == "factual"
        assert item.truth_status == "evidence_backed"
        assert item.sensitivity == "low"
        assert item.lifecycle_state == "active"
        assert item.review_required is False
        assert item.summary == event.summary
        assert item.provenance_refs == ["synthetic_event_001"]
        assert item.is_retrieval_eligible is True
        assert item.is_factual_evidence is True

    def test_inactive_memory_is_visible_but_not_retrieval_eligible(self) -> None:
        item = MemoryViewerItem.from_event(_factual(lifecycle_state="frozen"))

        assert item.lifecycle_state == "frozen"
        assert item.is_retrieval_eligible is False
        assert item.can_freeze is False
        assert item.can_export is True
        assert "not_retrieval_eligible" in item.safety_notes

    def test_imagined_memory_is_labeled_and_not_factual_evidence(self) -> None:
        item = MemoryViewerItem.from_event(_imagined())

        assert item.event_type == "imagined"
        assert item.truth_status == "imagined"
        assert item.is_factual_evidence is False
        assert "imagined_memory" in item.safety_notes

    def test_viewer_payload_has_no_raw_private_delivery_or_platform_fields(self) -> None:
        page = MemoryViewerPage(
            items=[MemoryViewerItem.from_event(_factual())],
            filters=MemoryViewerFilter(event_types=["factual"], truth_statuses=["evidence_backed"]),
            total_count=1,
            page=1,
            page_size=20,
        )
        serialized = json.dumps(page.model_dump(mode="json"), ensure_ascii=False).lower()

        for forbidden in (
            "raw_text",
            "raw_transcript",
            "chat_history",
            "private_messages",
            "send",
            "schedule",
            "delivery",
            "platform",
            "webhook",
            "token",
            "queue",
        ):
            assert forbidden not in serialized


class TestMemoryViewerPage:
    def test_page_preserves_filters_and_counts(self) -> None:
        item = MemoryViewerItem.from_event(_factual())
        filters = MemoryViewerFilter(
            event_types=["factual"],
            truth_statuses=["evidence_backed"],
            lifecycle_states=["active"],
            include_deleted=False,
        )

        page = MemoryViewerPage(items=[item], filters=filters, total_count=1, page=1, page_size=20)

        assert page.schema_version == "memory_viewer_page_v1"
        assert page.items == [item]
        assert page.filters.event_types == ["factual"]
        assert page.total_count == 1
        assert page.page == 1
        assert page.page_size == 20
