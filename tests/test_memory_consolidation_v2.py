"""T264 Memory consolidation stub tests.

All memory events are synthetic. These tests define candidate grouping only;
they do not call LLMs, mutate stores, rank retrieval, generate dialogue,
schedule proactive messages, or connect to external platforms.
"""

from __future__ import annotations

from pathlib import Path

from practical_chat_agent.core.models import MemoryEvent, MemoryProvenance
from practical_chat_agent.services.memory_consolidation_v2 import MemoryConsolidationService
from practical_chat_agent.services.memory_event_store import MemoryEventStore


def _service() -> MemoryConsolidationService:
    return MemoryConsolidationService()


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
        "salience": 0.6,
    }
    data.update(overrides)
    return MemoryEvent(**data)


def _procedural() -> MemoryEvent:
    return MemoryEvent(
        user_id="user_synthetic",
        event_type="procedural",
        truth_status="procedural_preference",
        summary="Use concise replies and ask before giving advice.",
        provenance=_provenance(),
        sensitivity="low",
        preference_labels=["concise_reply", "ask_before_advice"],
    )


def _imagined() -> MemoryEvent:
    return MemoryEvent(
        user_id="user_synthetic",
        event_type="imagined",
        truth_status="imagined",
        summary="Fictional persona dreamed about a quiet bookstore.",
        provenance=MemoryProvenance(source_type="imagined_generation"),
        sensitivity="low",
        imagined_context_label="dream_log",
    )


class TestMemoryConsolidationGrouping:
    def test_factual_events_group_only_with_factual_events(self) -> None:
        factual_a = _factual()
        factual_b = _factual(summary="User said they prefer evening check-ins.")
        procedural = _procedural()

        candidates = _service().propose([factual_a, factual_b, procedural])
        factual_groups = [candidate for candidate in candidates if candidate.event_type == "factual"]

        assert len(factual_groups) == 1
        assert factual_groups[0].proposed_operation == "keep"
        assert factual_groups[0].event_ids == [factual_a.event_id, factual_b.event_id]
        assert procedural.event_id not in factual_groups[0].event_ids

    def test_imagined_events_stay_separate_from_factual_groups(self) -> None:
        factual = _factual()
        imagined = _imagined()

        candidates = _service().propose([factual, imagined])
        imagined_groups = [candidate for candidate in candidates if candidate.event_type == "imagined"]
        factual_groups = [candidate for candidate in candidates if candidate.event_type == "factual"]

        assert len(imagined_groups) == 1
        assert imagined_groups[0].proposed_operation == "separate_imagined"
        assert imagined_groups[0].event_ids == [imagined.event_id]
        assert "imagined_memory_isolated" in imagined_groups[0].safety_warnings
        assert imagined.event_id not in factual_groups[0].event_ids


class TestMemoryConsolidationPolicySignals:
    def test_review_required_or_high_sensitivity_events_recommend_review(self) -> None:
        high = _factual(sensitivity="high")

        candidates = _service().propose([high])

        assert candidates[0].proposed_operation == "review"
        assert candidates[0].event_ids == [high.event_id]
        assert "sensitive_memory_review_required" in candidates[0].safety_warnings

    def test_low_salience_old_events_recommend_decay_or_compress(self) -> None:
        decay_event = _factual(salience=0.12)
        compress_event = _factual(salience=0.12)

        candidates = _service().propose(
            [decay_event, compress_event],
            age_days_by_event_id={
                decay_event.event_id: 45,
                compress_event.event_id: 210,
            },
        )

        operation_by_event_id = {
            candidate.event_ids[0]: candidate.proposed_operation
            for candidate in candidates
        }
        assert operation_by_event_id[decay_event.event_id] == "decay"
        assert operation_by_event_id[compress_event.event_id] == "compress"


class TestMemoryConsolidationBoundaries:
    def test_service_returns_candidates_without_mutating_store(self, tmp_path: Path) -> None:
        event = _factual(salience=0.12)
        store = MemoryEventStore(tmp_path / "memory_events.json")
        store.append(event)

        candidates = _service().propose([event], age_days_by_event_id={event.event_id: 210})

        assert candidates[0].proposed_operation == "compress"
        assert store.get(event.event_id).lifecycle_state == "active"

    def test_service_does_not_expose_runtime_or_delivery_methods(self) -> None:
        service = _service()

        for method_name in (
            "send",
            "schedule",
            "deliver",
            "execute",
            "run_runtime",
            "rank_for_dialogue",
            "mutate_store",
        ):
            assert not hasattr(service, method_name)
