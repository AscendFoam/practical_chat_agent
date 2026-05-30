"""T262 Memory lifecycle policy tests.

All events are synthetic. These tests define recommendation behavior only; they
do not mutate stores, rank retrieval, generate dialogue, schedule proactive
messages, or connect to external platforms.
"""

from __future__ import annotations

from pathlib import Path

from practical_chat_agent.core.models import MemoryEvent, MemoryProvenance
from practical_chat_agent.services.memory_event_store import MemoryEventStore
from practical_chat_agent.services.memory_lifecycle_v2 import MemoryLifecyclePolicyService


def _policy() -> MemoryLifecyclePolicyService:
    return MemoryLifecyclePolicyService()


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


class TestMemoryLifecyclePolicySafety:
    def test_high_sensitivity_memory_requires_review(self) -> None:
        recommendation = _policy().recommend(_factual(sensitivity="high"))

        assert recommendation.action == "review_required"
        assert recommendation.retrieval_allowed is False
        assert "sensitive_memory_review_required" in recommendation.reason_flags

    def test_deleted_frozen_and_archived_memory_is_never_recommended_for_retrieval(self) -> None:
        for state, expected_action in (
            ("deleted", "delete"),
            ("frozen", "freeze"),
            ("archived", "archive"),
        ):
            recommendation = _policy().recommend(_factual(lifecycle_state=state))

            assert recommendation.action == expected_action
            assert recommendation.suggested_lifecycle_state == state
            assert recommendation.retrieval_allowed is False
            assert "inactive_lifecycle_state" in recommendation.reason_flags

    def test_imagined_memory_can_only_be_kept_as_imagined_memory(self) -> None:
        recommendation = _policy().recommend(_imagined())

        assert recommendation.action == "keep"
        assert recommendation.retrieval_context == "imagined"
        assert recommendation.retrieval_allowed is True
        assert "imagined_memory_isolated" in recommendation.reason_flags
        assert "factual" not in recommendation.allowed_contexts


class TestMemoryLifecyclePolicyAging:
    def test_low_salience_old_memory_recommends_decay_or_compression(self) -> None:
        decay = _policy().recommend(_factual(salience=0.12), age_days=45)
        compress = _policy().recommend(_factual(salience=0.12), age_days=210)

        assert decay.action == "decay"
        assert "low_salience_old_memory" in decay.reason_flags
        assert decay.retrieval_allowed is True
        assert compress.action == "compress"
        assert "compression_candidate" in compress.reason_flags
        assert compress.retrieval_allowed is True

    def test_explicit_user_delete_signal_recommends_delete(self) -> None:
        recommendation = _policy().recommend(
            _factual(),
            user_delete_requested=True,
        )

        assert recommendation.action == "delete"
        assert recommendation.suggested_lifecycle_state == "deleted"
        assert recommendation.retrieval_allowed is False
        assert "user_delete_requested" in recommendation.reason_flags


class TestMemoryLifecyclePolicyBoundaries:
    def test_policy_returns_recommendations_without_mutating_store(self, tmp_path: Path) -> None:
        event = _factual()
        store = MemoryEventStore(tmp_path / "memory_events.json")
        store.append(event)

        recommendation = _policy().recommend(event, user_delete_requested=True)

        assert recommendation.action == "delete"
        assert store.get(event.event_id).lifecycle_state == "active"

    def test_policy_service_does_not_expose_runtime_or_delivery_methods(self) -> None:
        policy = _policy()

        for method_name in (
            "send",
            "schedule",
            "deliver",
            "execute",
            "run_runtime",
            "rank_for_dialogue",
            "mutate_store",
        ):
            assert not hasattr(policy, method_name)
