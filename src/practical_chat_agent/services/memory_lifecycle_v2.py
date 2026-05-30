"""Deterministic lifecycle policy recommendations for MemoryEvent v2."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from practical_chat_agent.core.models import MemoryEvent, MemoryLifecycleState, MemoryRetrievalContext


MemoryLifecycleAction = Literal[
    "keep",
    "review_required",
    "freeze",
    "delete",
    "archive",
    "decay",
    "compress",
]


class MemoryLifecycleRecommendation(BaseModel):
    schema_version: str = "memory_lifecycle_recommendation_v2"
    event_id: str
    action: MemoryLifecycleAction
    retrieval_allowed: bool = False
    retrieval_context: MemoryRetrievalContext | None = None
    allowed_contexts: list[MemoryRetrievalContext] = Field(default_factory=list)
    suggested_lifecycle_state: MemoryLifecycleState | None = None
    reason_flags: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class MemoryLifecyclePolicyService:
    """Return lifecycle recommendations without mutating memory stores."""

    def recommend(
        self,
        event: MemoryEvent,
        *,
        age_days: int = 0,
        user_delete_requested: bool = False,
    ) -> MemoryLifecycleRecommendation:
        if user_delete_requested:
            return self._recommend(
                event,
                action="delete",
                suggested_lifecycle_state="deleted",
                reason_flags=["user_delete_requested"],
            )

        inactive_action_by_state: dict[str, MemoryLifecycleAction] = {
            "deleted": "delete",
            "frozen": "freeze",
            "archived": "archive",
        }
        if event.lifecycle_state in inactive_action_by_state:
            return self._recommend(
                event,
                action=inactive_action_by_state[event.lifecycle_state],
                suggested_lifecycle_state=event.lifecycle_state,
                reason_flags=["inactive_lifecycle_state"],
            )

        if event.retrieval_permission.review_required or event.sensitivity in {"medium", "high"}:
            return self._recommend(
                event,
                action="review_required",
                reason_flags=["sensitive_memory_review_required"],
            )

        if event.event_type == "imagined":
            return self._recommend(
                event,
                action="keep",
                retrieval_context="imagined",
                reason_flags=["imagined_memory_isolated"],
            )

        if event.salience <= 0.2 and age_days >= 180:
            return self._recommend(
                event,
                action="compress",
                retrieval_context=self._default_context(event),
                reason_flags=["low_salience_old_memory", "compression_candidate"],
            )
        if event.salience <= 0.2 and age_days >= 30:
            return self._recommend(
                event,
                action="decay",
                retrieval_context=self._default_context(event),
                reason_flags=["low_salience_old_memory"],
            )

        return self._recommend(
            event,
            action="keep",
            retrieval_context=self._default_context(event),
            reason_flags=["active_memory"],
        )

    def _recommend(
        self,
        event: MemoryEvent,
        *,
        action: MemoryLifecycleAction,
        retrieval_context: MemoryRetrievalContext | None = None,
        suggested_lifecycle_state: MemoryLifecycleState | None = None,
        reason_flags: list[str],
    ) -> MemoryLifecycleRecommendation:
        allowed_contexts = self._allowed_contexts(event)
        retrieval_allowed = (
            retrieval_context is not None
            and retrieval_context in allowed_contexts
            and event.is_retrieval_eligible(retrieval_context)
        )
        if action in {"delete", "freeze", "archive", "review_required"}:
            retrieval_allowed = False
            allowed_contexts = []

        return MemoryLifecycleRecommendation(
            event_id=event.event_id,
            action=action,
            retrieval_allowed=retrieval_allowed,
            retrieval_context=retrieval_context,
            allowed_contexts=allowed_contexts,
            suggested_lifecycle_state=suggested_lifecycle_state,
            reason_flags=reason_flags,
        )

    @staticmethod
    def _default_context(event: MemoryEvent) -> MemoryRetrievalContext:
        if event.event_type == "factual":
            return "factual"
        if event.event_type == "inferred":
            return "inferred"
        if event.event_type == "relational":
            return "relational"
        if event.event_type == "procedural":
            return "procedural"
        return "imagined"

    @staticmethod
    def _allowed_contexts(event: MemoryEvent) -> list[MemoryRetrievalContext]:
        contexts: list[MemoryRetrievalContext] = []
        if event.retrieval_permission.allow_factual_retrieval:
            contexts.append("factual")
        if event.retrieval_permission.allow_inferred_retrieval:
            contexts.append("inferred")
        if event.retrieval_permission.allow_relational_retrieval:
            contexts.append("relational")
        if event.retrieval_permission.allow_procedural_retrieval:
            contexts.append("procedural")
        if event.retrieval_permission.allow_imagined_retrieval:
            contexts.append("imagined")
        return contexts
