"""T263 Memory retrieval bundle schema tests.

All memory events are synthetic. These tests define packaging invariants only;
they do not implement search, ranking, vector indexing, dialogue generation,
proactive behavior, or platform integration.
"""

from __future__ import annotations

import json

import pytest
from pydantic import ValidationError

from practical_chat_agent.core.models import (
    MemoryEvent,
    MemoryProvenance,
    MemoryRetrievalBundle,
    MemoryRetrievalBundleItem,
)


def _provenance(**overrides: object) -> MemoryProvenance:
    data: dict[str, object] = {
        "source_type": "synthetic_test",
        "evidence_refs": ["synthetic_event_001"],
    }
    data.update(overrides)
    return MemoryProvenance(**data)


def _factual(**overrides: object) -> MemoryEvent:
    data: dict[str, object] = {
        "user_id": "user_synthetic",
        "event_type": "factual",
        "truth_status": "evidence_backed",
        "summary": "User said they prefer concise check-ins.",
        "provenance": _provenance(),
        "sensitivity": "low",
    }
    data.update(overrides)
    return MemoryEvent(**data)


def _imagined(**overrides: object) -> MemoryEvent:
    data: dict[str, object] = {
        "user_id": "user_synthetic",
        "event_type": "imagined",
        "truth_status": "imagined",
        "summary": "Fictional persona dreamed about a quiet bookstore.",
        "provenance": MemoryProvenance(source_type="imagined_generation"),
        "sensitivity": "low",
        "imagined_context_label": "dream_log",
    }
    data.update(overrides)
    return MemoryEvent(**data)


class TestMemoryRetrievalBundleItem:
    def test_bundle_item_preserves_event_type_truth_provenance_and_context(self) -> None:
        event = _factual()
        item = MemoryRetrievalBundleItem.from_event(event, retrieval_context="factual")

        assert item.event_id == event.event_id
        assert item.event_type == "factual"
        assert item.truth_status == "evidence_backed"
        assert item.provenance_refs == ["synthetic_event_001"]
        assert item.retrieval_context == "factual"
        assert item.review_required is False


class TestMemoryRetrievalBundleInvariants:
    def test_factual_purpose_cannot_include_imagined_memory_as_evidence(self) -> None:
        with pytest.raises(ValidationError):
            MemoryRetrievalBundle(
                purpose="factual_response",
                query_summary="answer with factual memories",
                items=[MemoryRetrievalBundleItem.from_event(_imagined(), retrieval_context="imagined")],
            )

    @pytest.mark.parametrize("lifecycle_state", ["deleted", "frozen", "archived"])
    def test_inactive_memory_cannot_be_included(self, lifecycle_state: str) -> None:
        with pytest.raises(ValidationError):
            MemoryRetrievalBundle(
                purpose="review_surface",
                query_summary="inspect memory",
                items=[
                    MemoryRetrievalBundleItem.from_event(
                        _factual(lifecycle_state=lifecycle_state),
                        retrieval_context="factual",
                    )
                ],
            )

    def test_review_required_memory_requires_explicit_review_flag(self) -> None:
        item = MemoryRetrievalBundleItem.from_event(_factual(sensitivity="high"), retrieval_context="factual")

        with pytest.raises(ValidationError):
            MemoryRetrievalBundle(
                purpose="review_surface",
                query_summary="inspect sensitive memory",
                items=[item],
            )

        bundle = MemoryRetrievalBundle(
            purpose="review_surface",
            query_summary="inspect sensitive memory",
            items=[item],
            include_review_required=True,
        )
        assert bundle.include_review_required is True
        assert bundle.truth_status_counts["evidence_backed"] == 1

    def test_bundle_records_counts_exclusions_and_safety_warnings(self) -> None:
        bundle = MemoryRetrievalBundle(
            purpose="review_surface",
            query_summary="inspect mixed memories",
            items=[
                MemoryRetrievalBundleItem.from_event(_factual(), retrieval_context="factual"),
                MemoryRetrievalBundleItem.from_event(_imagined(), retrieval_context="imagined"),
            ],
            excluded_memory_ids=["mev_excluded_001"],
            exclusion_reasons={"mev_excluded_001": "deleted"},
            safety_warnings=["contains_imagined_memory"],
        )

        assert bundle.selected_memory_ids == [item.event_id for item in bundle.items]
        assert bundle.imagined_memory_count == 1
        assert bundle.truth_status_counts == {"evidence_backed": 1, "imagined": 1}
        assert bundle.exclusion_reasons["mev_excluded_001"] == "deleted"
        assert bundle.safety_warnings == ["contains_imagined_memory"]

    def test_bundle_has_no_raw_private_delivery_or_runtime_fields(self) -> None:
        bundle = MemoryRetrievalBundle(
            purpose="review_surface",
            query_summary="inspect memory",
            items=[MemoryRetrievalBundleItem.from_event(_factual(), retrieval_context="factual")],
        )
        serialized = json.dumps(bundle.model_dump(mode="json"), ensure_ascii=False)

        for forbidden in (
            "raw_text",
            "raw_transcript",
            "chat_history",
            "private_messages",
            "send",
            "schedule",
            "delivery",
            "runtime",
        ):
            assert forbidden not in serialized
