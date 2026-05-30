"""T260 MemoryEvent v2 schema tests.

All examples are synthetic. These tests define schema invariants only; they do
not read private chat history, implement retrieval ranking, generate dialogue,
schedule proactive messages, or connect to external platforms.
"""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from practical_chat_agent.core.models import (
    MemoryEvent,
    MemoryProvenance,
    MemoryRetrievalPermission,
)


def _provenance(**overrides: object) -> MemoryProvenance:
    data: dict[str, object] = {
        "source_type": "synthetic_test",
        "evidence_refs": ["synthetic_event_001"],
    }
    data.update(overrides)
    return MemoryProvenance(**data)


class TestFactualMemoryEvent:
    def test_factual_memory_requires_evidence_refs_and_is_factual_retrieval_eligible(self) -> None:
        event = MemoryEvent(
            user_id="user_synthetic",
            event_type="factual",
            truth_status="evidence_backed",
            summary="User said they prefer concise evening check-ins.",
            provenance=_provenance(),
            sensitivity="low",
        )

        assert event.schema_version == "memory_event_v2"
        assert event.event_id.startswith("mev_")
        assert event.event_type == "factual"
        assert event.provenance.evidence_refs == ["synthetic_event_001"]
        assert event.is_retrieval_eligible("factual")
        assert not hasattr(event, "raw_text")
        assert not hasattr(event, "raw_transcript")
        assert not hasattr(event, "chat_history")
        assert not hasattr(event, "private_messages")

    def test_factual_memory_rejects_missing_evidence(self) -> None:
        with pytest.raises(ValidationError):
            MemoryEvent(
                user_id="user_synthetic",
                event_type="factual",
                truth_status="evidence_backed",
                summary="User likes concise replies.",
                provenance=MemoryProvenance(source_type="synthetic_test"),
                sensitivity="low",
            )


class TestInferredRelationalProceduralMemoryEvent:
    def test_inferred_memory_requires_confidence_and_rationale(self) -> None:
        with pytest.raises(ValidationError):
            MemoryEvent(
                user_id="user_synthetic",
                event_type="inferred",
                truth_status="inferred",
                summary="User may prefer practical comfort.",
                provenance=_provenance(),
                sensitivity="medium",
            )

        event = MemoryEvent(
            user_id="user_synthetic",
            event_type="inferred",
            truth_status="inferred",
            summary="User may prefer practical comfort.",
            provenance=_provenance(),
            sensitivity="medium",
            confidence=0.72,
            inference_rationale="Synthetic repeated preference signal.",
        )
        assert event.confidence == 0.72
        assert event.inference_rationale == "Synthetic repeated preference signal."
        assert event.retrieval_permission.review_required is True
        assert not event.is_retrieval_eligible("inferred")

    def test_relational_memory_requires_relationship_dimensions(self) -> None:
        with pytest.raises(ValidationError):
            MemoryEvent(
                user_id="user_synthetic",
                event_type="relational",
                truth_status="relationship_state",
                summary="Trust increased after a repair conversation.",
                provenance=_provenance(),
                sensitivity="low",
            )

        event = MemoryEvent(
            user_id="user_synthetic",
            event_type="relational",
            truth_status="relationship_state",
            summary="Trust increased after a repair conversation.",
            provenance=_provenance(),
            sensitivity="low",
            relationship_dimensions=["trust", "repair_state"],
        )
        assert event.relationship_dimensions == ["trust", "repair_state"]
        assert event.is_retrieval_eligible("relational")

    def test_procedural_memory_records_preferences_without_becoming_factual(self) -> None:
        event = MemoryEvent(
            user_id="user_synthetic",
            event_type="procedural",
            truth_status="procedural_preference",
            summary="Use concise replies and ask before giving advice.",
            provenance=_provenance(),
            sensitivity="low",
            preference_labels=["concise_reply", "ask_before_advice"],
        )

        assert event.truth_status == "procedural_preference"
        assert event.preference_labels == ["concise_reply", "ask_before_advice"]
        assert event.is_retrieval_eligible("procedural")
        assert not event.is_retrieval_eligible("factual")


class TestImaginedMemoryEvent:
    def test_imagined_memory_cannot_be_retrieved_as_factual_evidence(self) -> None:
        event = MemoryEvent(
            user_id="user_synthetic",
            event_type="imagined",
            truth_status="imagined",
            summary="Fictional persona dreamed about a quiet bookstore.",
            provenance=MemoryProvenance(source_type="imagined_generation"),
            sensitivity="low",
            imagined_context_label="dream_log",
        )

        assert event.event_type == "imagined"
        assert event.truth_status == "imagined"
        assert event.retrieval_permission.allow_factual_retrieval is False
        assert event.retrieval_permission.allow_imagined_retrieval is True
        assert not event.is_retrieval_eligible("factual")
        assert event.is_retrieval_eligible("imagined")

    def test_imagined_memory_rejects_factual_truth_or_factual_retrieval(self) -> None:
        with pytest.raises(ValidationError):
            MemoryEvent(
                user_id="user_synthetic",
                event_type="imagined",
                truth_status="evidence_backed",
                summary="Fictional dream incorrectly marked factual.",
                provenance=MemoryProvenance(source_type="imagined_generation"),
                sensitivity="low",
                imagined_context_label="dream_log",
            )

        with pytest.raises(ValidationError):
            MemoryEvent(
                user_id="user_synthetic",
                event_type="imagined",
                truth_status="imagined",
                summary="Fictional dream incorrectly available as fact.",
                provenance=MemoryProvenance(source_type="imagined_generation"),
                sensitivity="low",
                imagined_context_label="dream_log",
                retrieval_permission=MemoryRetrievalPermission(allow_factual_retrieval=True),
            )


class TestLifecycleAndSensitivity:
    @pytest.mark.parametrize("lifecycle_state", ["frozen", "deleted"])
    def test_frozen_or_deleted_memory_is_not_retrieval_eligible(self, lifecycle_state: str) -> None:
        event = MemoryEvent(
            user_id="user_synthetic",
            event_type="factual",
            truth_status="evidence_backed",
            summary="User likes concise replies.",
            provenance=_provenance(),
            sensitivity="low",
            lifecycle_state=lifecycle_state,
        )

        assert not event.is_retrieval_eligible("factual")

    def test_sensitive_memory_defaults_to_review_required(self) -> None:
        event = MemoryEvent(
            user_id="user_synthetic",
            event_type="factual",
            truth_status="evidence_backed",
            summary="Synthetic high sensitivity preference.",
            provenance=_provenance(),
            sensitivity="high",
        )

        assert event.retrieval_permission.review_required is True
        assert not event.is_retrieval_eligible("factual")
