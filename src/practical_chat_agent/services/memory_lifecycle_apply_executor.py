"""Local-only memory lifecycle apply executor."""

from __future__ import annotations

from collections.abc import Iterable
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from practical_chat_agent.core.ids import new_id
from practical_chat_agent.core.models import MemoryLifecycleState, utc_now
from practical_chat_agent.services.apply_executor_approval_gate import (
    ApplyExecutorApprovalDecision,
)
from practical_chat_agent.services.manual_apply_eligibility_gate import (
    ManualApplyEligibilityDecision,
)
from practical_chat_agent.services.memory_event_store import (
    MemoryEventStore,
    MemoryEventStoreRecord,
)
from practical_chat_agent.services.memory_lifecycle_dry_run import (
    MemoryLifecycleDryRunAction,
    MemoryLifecycleDryRunPlan,
)


MEMORY_LIFECYCLE_APPLY_CONFIRMATION = "CONFIRM_LOCAL_MEMORY_APPLY"
MemoryLifecycleApplyConfirmationState = Literal["confirmed"]


class MemoryLifecycleApplyError(ValueError):
    """Raised when a local memory lifecycle apply request is not eligible."""


class _MemoryLifecycleApplyRecord(BaseModel):
    model_config = ConfigDict(extra="forbid", arbitrary_types_allowed=True)


class MemoryLifecycleApplyRequest(_MemoryLifecycleApplyRecord):
    schema_version: str = "memory_lifecycle_apply_request_v1"
    plan: MemoryLifecycleDryRunPlan
    manual_eligibility: ManualApplyEligibilityDecision
    approval_decision: ApplyExecutorApprovalDecision
    memory_store: MemoryEventStore
    reviewer_id: str = Field(..., min_length=1)
    final_confirmation: str = ""
    local_only: bool = True
    review_required: bool = True
    automatic_apply: bool = False
    calls_provider: bool = False
    sends_messages: bool = False
    writes_memory_store: bool = True
    writes_persona_version: bool = False
    runtime_ready: bool = False

    @model_validator(mode="after")
    def validate_request(self) -> "MemoryLifecycleApplyRequest":
        if not self.local_only:
            raise ValueError("memory lifecycle apply requests must stay local-only")
        if not self.review_required:
            raise ValueError("memory lifecycle apply requests require review")
        if self.automatic_apply:
            raise ValueError("memory lifecycle apply requests cannot be automatic")
        if self.calls_provider:
            raise ValueError("memory lifecycle apply requests cannot call providers")
        if self.sends_messages:
            raise ValueError("memory lifecycle apply requests cannot send messages")
        if not self.writes_memory_store:
            raise ValueError("memory lifecycle apply requests must write a memory store")
        if self.writes_persona_version:
            raise ValueError("memory lifecycle apply requests cannot write persona versions")
        if self.runtime_ready:
            raise ValueError("memory lifecycle apply requests are not runtime-ready")
        return self


class MemoryLifecycleApplyAudit(_MemoryLifecycleApplyRecord):
    schema_version: str = "memory_lifecycle_apply_audit_v1"
    apply_id: str = Field(default_factory=lambda: new_id("mlapply"))
    plan_id: str = Field(..., min_length=1)
    source_candidate_kind: str = Field(..., min_length=1)
    source_candidate_id: str = Field(..., min_length=1)
    review_decision_id: str = Field(..., min_length=1)
    eligibility_id: str = Field(..., min_length=1)
    approval_id: str = Field(..., min_length=1)
    reviewer_id: str = Field(..., min_length=1)
    affected_memory_ids: list[str] = Field(default_factory=list)
    prior_lifecycle_states: dict[str, MemoryLifecycleState] = Field(default_factory=dict)
    new_lifecycle_states: dict[str, MemoryLifecycleState] = Field(default_factory=dict)
    rollback_record_ids: dict[str, str] = Field(default_factory=dict)
    applied_record_ids: dict[str, str] = Field(default_factory=dict)
    safe_summary: str = Field(..., min_length=1)
    final_confirmation: MemoryLifecycleApplyConfirmationState = "confirmed"
    local_only: bool = True
    review_required: bool = True
    automatic_apply: bool = False
    calls_provider: bool = False
    sends_messages: bool = False
    writes_memory_store: bool = True
    writes_persona_version: bool = False
    runtime_ready: bool = False
    created_at: datetime = Field(default_factory=utc_now)

    @model_validator(mode="after")
    def validate_audit(self) -> "MemoryLifecycleApplyAudit":
        if not self.local_only:
            raise ValueError("memory lifecycle apply audits must stay local-only")
        if not self.review_required:
            raise ValueError("memory lifecycle apply audits require review")
        if self.automatic_apply:
            raise ValueError("memory lifecycle apply audits cannot be automatic")
        if self.calls_provider:
            raise ValueError("memory lifecycle apply audits cannot call providers")
        if self.sends_messages:
            raise ValueError("memory lifecycle apply audits cannot send messages")
        if not self.writes_memory_store:
            raise ValueError("memory lifecycle apply audits must record memory store writes")
        if self.writes_persona_version:
            raise ValueError("memory lifecycle apply audits cannot write persona versions")
        if self.runtime_ready:
            raise ValueError("memory lifecycle apply audits are not runtime-ready")
        self.affected_memory_ids = _ordered_unique(self.affected_memory_ids)
        return self


class MemoryLifecycleApplyExecutor:
    """Apply reviewed lifecycle effects to a caller-supplied local store."""

    def apply(self, request: MemoryLifecycleApplyRequest) -> MemoryLifecycleApplyAudit:
        _validate_apply_request(request)
        planned_updates = _planned_updates(request.plan)
        prior_records = _load_prior_records(request.memory_store, planned_updates)
        applied_records: dict[str, MemoryEventStoreRecord] = {}
        for memory_id, next_state in planned_updates.items():
            applied_records[memory_id] = request.memory_store.update_lifecycle(
                memory_id,
                next_state,
            )

        affected_memory_ids = list(planned_updates)
        return MemoryLifecycleApplyAudit(
            plan_id=request.plan.plan_id,
            source_candidate_kind=request.plan.source_candidate_kind,
            source_candidate_id=request.plan.source_candidate_id,
            review_decision_id=request.plan.review_decision_id
            or request.manual_eligibility.decision_id,
            eligibility_id=request.manual_eligibility.eligibility_id,
            approval_id=request.approval_decision.approval_id,
            reviewer_id=request.reviewer_id,
            affected_memory_ids=affected_memory_ids,
            prior_lifecycle_states={
                memory_id: prior_records[memory_id].event.lifecycle_state
                for memory_id in affected_memory_ids
            },
            new_lifecycle_states={
                memory_id: applied_records[memory_id].event.lifecycle_state
                for memory_id in affected_memory_ids
            },
            rollback_record_ids={
                memory_id: prior_records[memory_id].record_id
                for memory_id in affected_memory_ids
            },
            applied_record_ids={
                memory_id: applied_records[memory_id].record_id
                for memory_id in affected_memory_ids
            },
            safe_summary="[SYNTHETIC] Local memory lifecycle apply completed.",
        )


def _validate_apply_request(request: MemoryLifecycleApplyRequest) -> None:
    if request.final_confirmation != MEMORY_LIFECYCLE_APPLY_CONFIRMATION:
        raise MemoryLifecycleApplyError("final confirmation is required")
    if request.plan.review_decision != "approve":
        raise MemoryLifecycleApplyError("memory lifecycle plan is not approved")
    if not request.plan.review_decision_id:
        raise MemoryLifecycleApplyError("memory lifecycle plan has no review decision")
    if not request.plan.effects:
        raise MemoryLifecycleApplyError("memory lifecycle plan has no effects")
    if request.manual_eligibility.eligibility_outcome != "eligible":
        raise MemoryLifecycleApplyError("manual eligibility is not eligible")
    if (
        request.approval_decision.final_outcome
        != "ready_for_separately_scoped_executor_design"
    ):
        raise MemoryLifecycleApplyError("apply executor approval is not ready")
    if request.manual_eligibility.decision_id != request.plan.review_decision_id:
        raise MemoryLifecycleApplyError("manual eligibility decision does not match plan")
    if request.manual_eligibility.candidate_kind != request.plan.source_candidate_kind:
        raise MemoryLifecycleApplyError("manual eligibility candidate kind does not match plan")
    if request.manual_eligibility.candidate_id != request.plan.source_candidate_id:
        raise MemoryLifecycleApplyError("manual eligibility candidate id does not match plan")
    if request.approval_decision.decision_id != request.plan.review_decision_id:
        raise MemoryLifecycleApplyError("approval decision does not match plan")
    if request.approval_decision.candidate_kind != request.plan.source_candidate_kind:
        raise MemoryLifecycleApplyError("approval candidate kind does not match plan")
    if request.approval_decision.candidate_id != request.plan.source_candidate_id:
        raise MemoryLifecycleApplyError("approval candidate id does not match plan")


def _planned_updates(plan: MemoryLifecycleDryRunPlan) -> dict[str, MemoryLifecycleState]:
    updates: dict[str, MemoryLifecycleState] = {}
    for effect in plan.effects:
        next_state = _state_for_action(effect.action)
        current_state = updates.get(effect.memory_id)
        updates[effect.memory_id] = (
            next_state if current_state is None else _stronger_state(current_state, next_state)
        )
    if not updates:
        raise MemoryLifecycleApplyError("memory lifecycle plan has no applicable effects")
    return updates


def _load_prior_records(
    store: MemoryEventStore,
    planned_updates: dict[str, MemoryLifecycleState],
) -> dict[str, MemoryEventStoreRecord]:
    records: dict[str, MemoryEventStoreRecord] = {}
    for memory_id in planned_updates:
        try:
            records[memory_id] = store.get_record(memory_id)
        except ValueError as exc:
            raise MemoryLifecycleApplyError(f"memory event not found: {memory_id}") from exc
    return records


def _state_for_action(action: MemoryLifecycleDryRunAction) -> MemoryLifecycleState:
    if action == "delete":
        return "deleted"
    if action == "archive" or action == "reject_new":
        return "archived"
    if action == "freeze" or action == "suppress_retrieval" or action == "training_exclusion":
        return "frozen"
    if action == "supersede":
        return "superseded"
    raise MemoryLifecycleApplyError(f"unsupported memory lifecycle action: {action}")


def _stronger_state(
    first: MemoryLifecycleState,
    second: MemoryLifecycleState,
) -> MemoryLifecycleState:
    priority: dict[MemoryLifecycleState, int] = {
        "active": 0,
        "frozen": 1,
        "archived": 2,
        "superseded": 3,
        "deleted": 4,
    }
    return first if priority[first] >= priority[second] else second


def _ordered_unique(values: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value and value not in seen:
            seen.add(value)
            result.append(value)
    return result
