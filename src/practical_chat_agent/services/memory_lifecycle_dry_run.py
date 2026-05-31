"""Preview-only memory lifecycle dry-run plans.

The records in this module describe proposed memory lifecycle effects without
applying them. They do not mutate stores, delete records, enable retrieval,
call providers, generate replies, send messages, or connect to platform/media
runtimes.
"""

from __future__ import annotations

from collections.abc import Iterable
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from practical_chat_agent.core.ids import new_id
from practical_chat_agent.core.models import utc_now
from practical_chat_agent.services.memory_governance import (
    MemoryContradictionCandidate,
    MemoryDeletionCascadePlan,
    MemorySupersessionCandidate,
)
from practical_chat_agent.services.review_queue import ReviewQueueDecisionRecord


MemoryLifecycleDryRunAction = Literal[
    "suppress_retrieval",
    "training_exclusion",
    "delete",
    "freeze",
    "archive",
    "supersede",
    "keep_both",
    "request_clarification",
    "reject_new",
]
MemoryLifecycleDryRunSourceKind = Literal[
    "memory_deletion_cascade",
    "memory_supersession",
    "memory_contradiction",
]


class _MemoryLifecycleDryRunRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")


class MemoryLifecycleDryRunEffect(_MemoryLifecycleDryRunRecord):
    schema_version: str = "memory_lifecycle_dry_run_effect_v1"
    effect_id: str = Field(default_factory=lambda: new_id("mldeff"))
    action: MemoryLifecycleDryRunAction
    memory_id: str = Field(..., min_length=1)
    replacement_memory_id: str | None = None
    safe_summary: str = Field(..., min_length=1)
    source_refs: list[str] = Field(default_factory=list)
    preview_only: bool = True
    applies_changes: bool = False
    writes_memory_store: bool = False
    retrieval_enabled_after: bool = False
    created_at: datetime = Field(default_factory=utc_now)

    @model_validator(mode="after")
    def validate_preview_effect(self) -> "MemoryLifecycleDryRunEffect":
        if not self.preview_only:
            raise ValueError("memory lifecycle dry-run effects are preview-only")
        if self.applies_changes:
            raise ValueError("memory lifecycle dry-run effects cannot apply changes")
        if self.writes_memory_store:
            raise ValueError("memory lifecycle dry-run effects cannot write memory stores")
        if self.retrieval_enabled_after:
            raise ValueError("memory lifecycle dry-run effects cannot enable retrieval")
        self.source_refs = _ordered_unique(self.source_refs)
        return self


class MemoryLifecycleDryRunPlan(_MemoryLifecycleDryRunRecord):
    schema_version: str = "memory_lifecycle_dry_run_plan_v1"
    plan_id: str = Field(default_factory=lambda: new_id("mldplan"))
    source_candidate_kind: MemoryLifecycleDryRunSourceKind
    source_candidate_id: str = Field(..., min_length=1)
    source_schema_version: str | None = None
    review_decision_id: str | None = None
    review_decision: str | None = None
    safe_summary: str = Field(..., min_length=1)
    affected_memory_ids: list[str] = Field(default_factory=list)
    effects: list[MemoryLifecycleDryRunEffect] = Field(default_factory=list)
    blocked_reasons: list[str] = Field(default_factory=list)
    preview_only: bool = True
    review_required: bool = True
    applies_changes: bool = False
    writes_memory_store: bool = False
    created_at: datetime = Field(default_factory=utc_now)

    def effect_by_memory_id(self, memory_id: str) -> MemoryLifecycleDryRunEffect:
        for effect in self.effects:
            if effect.memory_id == memory_id:
                return effect
        raise KeyError(memory_id)

    @model_validator(mode="after")
    def validate_preview_plan(self) -> "MemoryLifecycleDryRunPlan":
        if not self.preview_only:
            raise ValueError("memory lifecycle dry-run plans are preview-only")
        if not self.review_required:
            raise ValueError("memory lifecycle dry-run plans require review")
        if self.applies_changes:
            raise ValueError("memory lifecycle dry-run plans cannot apply changes")
        if self.writes_memory_store:
            raise ValueError("memory lifecycle dry-run plans cannot write memory stores")
        self.affected_memory_ids = _ordered_unique(
            [
                *self.affected_memory_ids,
                *(effect.memory_id for effect in self.effects),
                *(effect.replacement_memory_id for effect in self.effects if effect.replacement_memory_id),
            ]
        )
        self.blocked_reasons = _ordered_unique(
            [*self.blocked_reasons, "retrieval_not_enabled_by_dry_run"]
        )
        return self


class MemoryLifecycleDryRunService:
    """Create preview-only plans from memory governance candidates."""

    def plan_from_candidate(
        self,
        candidate: object,
        *,
        decision_record: ReviewQueueDecisionRecord | None = None,
    ) -> MemoryLifecycleDryRunPlan:
        if isinstance(candidate, MemoryDeletionCascadePlan):
            return self._from_deletion(candidate, decision_record=decision_record)
        if isinstance(candidate, MemorySupersessionCandidate):
            return self._from_supersession(candidate, decision_record=decision_record)
        if isinstance(candidate, MemoryContradictionCandidate):
            return self._from_contradiction(candidate, decision_record=decision_record)
        raise TypeError(f"unsupported memory lifecycle candidate type: {type(candidate).__name__}")

    def _from_deletion(
        self,
        candidate: MemoryDeletionCascadePlan,
        *,
        decision_record: ReviewQueueDecisionRecord | None,
    ) -> MemoryLifecycleDryRunPlan:
        effects = [
            MemoryLifecycleDryRunEffect(
                action=action,
                memory_id=memory_id,
                safe_summary=f"[SYNTHETIC] Preview {action} for {candidate.trigger_type}.",
                source_refs=[
                    candidate.plan_id,
                    *candidate.affected_artifact_refs,
                ],
            )
            for memory_id in candidate.target_memory_ids
            for action in candidate.recommended_actions
        ]
        return _make_plan(
            source_candidate_kind="memory_deletion_cascade",
            source_candidate_id=candidate.plan_id,
            source_schema_version=candidate.schema_version,
            decision_record=decision_record,
            safe_summary=f"[SYNTHETIC] Preview {candidate.trigger_type} deletion cascade.",
            affected_memory_ids=candidate.target_memory_ids,
            effects=effects,
            blocked_reasons=[candidate.trigger_type],
        )

    def _from_supersession(
        self,
        candidate: MemorySupersessionCandidate,
        *,
        decision_record: ReviewQueueDecisionRecord | None,
    ) -> MemoryLifecycleDryRunPlan:
        effect = MemoryLifecycleDryRunEffect(
            action="supersede",
            memory_id=candidate.source_memory_id,
            replacement_memory_id=candidate.replacement_memory_id,
            safe_summary=candidate.reason,
            source_refs=[candidate.candidate_id],
        )
        return _make_plan(
            source_candidate_kind="memory_supersession",
            source_candidate_id=candidate.candidate_id,
            source_schema_version=candidate.schema_version,
            decision_record=decision_record,
            safe_summary=candidate.reason,
            affected_memory_ids=[candidate.source_memory_id, candidate.replacement_memory_id],
            effects=[effect],
            blocked_reasons=["lifecycle_write_not_applied"],
        )

    def _from_contradiction(
        self,
        candidate: MemoryContradictionCandidate,
        *,
        decision_record: ReviewQueueDecisionRecord | None,
    ) -> MemoryLifecycleDryRunPlan:
        action = _action_for_resolution(candidate.proposed_resolution)
        effects = [
            MemoryLifecycleDryRunEffect(
                action=action,
                memory_id=memory_id,
                replacement_memory_id=(
                    candidate.memory_ids[1]
                    if action == "supersede" and index == 0 and len(candidate.memory_ids) > 1
                    else None
                ),
                safe_summary=candidate.safe_summary,
                source_refs=[candidate.candidate_id, *candidate.new_evidence_refs],
            )
            for index, memory_id in enumerate(candidate.memory_ids)
        ]
        return _make_plan(
            source_candidate_kind="memory_contradiction",
            source_candidate_id=candidate.candidate_id,
            source_schema_version=candidate.schema_version,
            decision_record=decision_record,
            safe_summary=candidate.safe_summary,
            affected_memory_ids=candidate.memory_ids,
            effects=effects,
            blocked_reasons=["conflict_resolution_not_applied"],
        )


def _make_plan(
    *,
    source_candidate_kind: MemoryLifecycleDryRunSourceKind,
    source_candidate_id: str,
    safe_summary: str,
    effects: Iterable[MemoryLifecycleDryRunEffect],
    source_schema_version: str | None = None,
    decision_record: ReviewQueueDecisionRecord | None = None,
    affected_memory_ids: Iterable[str] = (),
    blocked_reasons: Iterable[str] = (),
) -> MemoryLifecycleDryRunPlan:
    return MemoryLifecycleDryRunPlan(
        source_candidate_kind=source_candidate_kind,
        source_candidate_id=source_candidate_id,
        source_schema_version=source_schema_version,
        review_decision_id=decision_record.decision_id if decision_record else None,
        review_decision=decision_record.decision if decision_record else None,
        safe_summary=safe_summary,
        affected_memory_ids=_ordered_unique(affected_memory_ids),
        effects=list(effects),
        blocked_reasons=_ordered_unique(blocked_reasons),
    )


def _action_for_resolution(resolution: str) -> MemoryLifecycleDryRunAction:
    if resolution == "supersede_old":
        return "supersede"
    if resolution == "archive_old":
        return "archive"
    if resolution == "reject_new":
        return "reject_new"
    if resolution == "keep_both":
        return "keep_both"
    return "request_clarification"


def _ordered_unique(values: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value and value not in seen:
            seen.add(value)
            result.append(value)
    return result
