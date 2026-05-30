"""Deterministic consolidation candidates for MemoryEvent v2."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from practical_chat_agent.core.ids import new_id
from practical_chat_agent.core.models import MemoryEvent, MemoryEventType
from practical_chat_agent.services.memory_lifecycle_v2 import MemoryLifecyclePolicyService


MemoryConsolidationOperation = Literal["keep", "review", "decay", "compress", "separate_imagined"]


class MemoryConsolidationCandidate(BaseModel):
    schema_version: str = "memory_consolidation_candidate_v2"
    group_id: str = Field(default_factory=lambda: new_id("memcon"))
    event_ids: list[str] = Field(..., min_length=1)
    event_type: MemoryEventType
    proposed_operation: MemoryConsolidationOperation
    rationale: str
    safety_warnings: list[str] = Field(default_factory=list)


class MemoryConsolidationService:
    """Group synthetic MemoryEvents into consolidation candidates."""

    def __init__(self, lifecycle_policy: MemoryLifecyclePolicyService | None = None) -> None:
        self.lifecycle_policy = lifecycle_policy or MemoryLifecyclePolicyService()

    def propose(
        self,
        events: list[MemoryEvent],
        *,
        age_days_by_event_id: dict[str, int] | None = None,
    ) -> list[MemoryConsolidationCandidate]:
        age_days_by_event_id = age_days_by_event_id or {}
        grouped: dict[tuple[str, str, str | None], dict[str, object]] = {}

        for event in events:
            age_days = age_days_by_event_id.get(event.event_id, 0)
            recommendation = self.lifecycle_policy.recommend(event, age_days=age_days)
            operation = self._operation_for(event=event, recommendation_action=recommendation.action)
            singleton_key = event.event_id if operation in {"review", "decay", "compress", "separate_imagined"} else None
            key = (event.event_type, operation, singleton_key)
            bucket = grouped.setdefault(
                key,
                {
                    "event_ids": [],
                    "event_type": event.event_type,
                    "operation": operation,
                    "warnings": [],
                },
            )
            bucket["event_ids"].append(event.event_id)  # type: ignore[union-attr]
            bucket["warnings"].extend(recommendation.reason_flags)  # type: ignore[union-attr]
            if event.event_type == "imagined":
                bucket["warnings"].append("imagined_memory_isolated")  # type: ignore[union-attr]

        return [
            MemoryConsolidationCandidate(
                event_ids=list(bucket["event_ids"]),  # type: ignore[arg-type]
                event_type=bucket["event_type"],  # type: ignore[arg-type]
                proposed_operation=bucket["operation"],  # type: ignore[arg-type]
                rationale=self._rationale(
                    event_type=bucket["event_type"],  # type: ignore[arg-type]
                    operation=bucket["operation"],  # type: ignore[arg-type]
                ),
                safety_warnings=self._dedupe_strings(list(bucket["warnings"])),  # type: ignore[arg-type]
            )
            for bucket in grouped.values()
        ]

    @staticmethod
    def _operation_for(
        *,
        event: MemoryEvent,
        recommendation_action: str,
    ) -> MemoryConsolidationOperation:
        if event.event_type == "imagined":
            return "separate_imagined"
        if recommendation_action == "review_required":
            return "review"
        if recommendation_action in {"decay", "compress"}:
            return recommendation_action  # type: ignore[return-value]
        return "keep"

    @staticmethod
    def _rationale(
        *,
        event_type: MemoryEventType,
        operation: MemoryConsolidationOperation,
    ) -> str:
        if operation == "separate_imagined":
            return "Imagined memory must remain separate from factual consolidation."
        if operation == "review":
            return "Memory requires human review before consolidation."
        if operation == "decay":
            return "Low-salience old memory is a decay candidate."
        if operation == "compress":
            return "Low-salience old memory is a compression candidate."
        return f"Keep active {event_type} memory grouped by type."

    @staticmethod
    def _dedupe_strings(values: list[str]) -> list[str]:
        seen: set[str] = set()
        result: list[str] = []
        for value in values:
            if value not in seen:
                seen.add(value)
                result.append(value)
        return result
