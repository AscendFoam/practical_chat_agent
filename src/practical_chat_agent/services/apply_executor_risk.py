"""Non-executing risk records for future apply executor design."""

from __future__ import annotations

from collections.abc import Iterable
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from practical_chat_agent.core.ids import new_id
from practical_chat_agent.core.models import utc_now
from practical_chat_agent.services.review_queue import ReviewCandidateKind


ApplyExecutorRiskSeverity = Literal["low", "medium", "high", "critical"]
ApplyExecutorRiskRecommendation = Literal[
    "blocked",
    "needs_review",
    "ready_for_separately_scoped_executor_design",
]


class _ApplyExecutorRiskRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ApplyExecutorRiskFactor(_ApplyExecutorRiskRecord):
    schema_version: str = "apply_executor_risk_factor_v1"
    risk_id: str = Field(default_factory=lambda: new_id("aerisk"))
    risk_code: str = Field(..., min_length=1)
    severity: ApplyExecutorRiskSeverity
    safe_summary: str = Field(..., min_length=1)
    source_refs: list[str] = Field(default_factory=list)
    risk_assessment_only: bool = True
    executor_ready: bool = False
    review_required: bool = True
    applies_changes: bool = False
    writes_memory_store: bool = False
    writes_persona_version: bool = False
    runtime_ready: bool = False
    created_at: datetime = Field(default_factory=utc_now)

    @model_validator(mode="after")
    def validate_factor(self) -> "ApplyExecutorRiskFactor":
        _validate_non_executing_flags(
            risk_assessment_only=self.risk_assessment_only,
            executor_ready=self.executor_ready,
            review_required=self.review_required,
            applies_changes=self.applies_changes,
            writes_memory_store=self.writes_memory_store,
            writes_persona_version=self.writes_persona_version,
            runtime_ready=self.runtime_ready,
            record_name="apply executor risk factors",
        )
        self.source_refs = _ordered_unique(self.source_refs)
        return self


class ApplyExecutorApprovalGate(_ApplyExecutorRiskRecord):
    schema_version: str = "apply_executor_approval_gate_v1"
    gate_id: str = Field(default_factory=lambda: new_id("aegate"))
    gate_code: str = Field(..., min_length=1)
    label: str = Field(..., min_length=1)
    safe_summary: str = Field(..., min_length=1)
    satisfied: bool = False
    source_refs: list[str] = Field(default_factory=list)
    risk_assessment_only: bool = True
    executor_ready: bool = False
    review_required: bool = True
    applies_changes: bool = False
    writes_memory_store: bool = False
    writes_persona_version: bool = False
    runtime_ready: bool = False
    created_at: datetime = Field(default_factory=utc_now)

    @model_validator(mode="after")
    def validate_gate(self) -> "ApplyExecutorApprovalGate":
        _validate_non_executing_flags(
            risk_assessment_only=self.risk_assessment_only,
            executor_ready=self.executor_ready,
            review_required=self.review_required,
            applies_changes=self.applies_changes,
            writes_memory_store=self.writes_memory_store,
            writes_persona_version=self.writes_persona_version,
            runtime_ready=self.runtime_ready,
            record_name="apply executor approval gates",
        )
        self.source_refs = _ordered_unique(self.source_refs)
        return self


class ApplyExecutorRollbackRequirement(_ApplyExecutorRiskRecord):
    schema_version: str = "apply_executor_rollback_requirement_v1"
    requirement_id: str = Field(default_factory=lambda: new_id("aerollback"))
    requirement_code: str = Field(..., min_length=1)
    safe_summary: str = Field(..., min_length=1)
    covered: bool = False
    source_refs: list[str] = Field(default_factory=list)
    risk_assessment_only: bool = True
    executor_ready: bool = False
    review_required: bool = True
    applies_changes: bool = False
    writes_memory_store: bool = False
    writes_persona_version: bool = False
    runtime_ready: bool = False
    created_at: datetime = Field(default_factory=utc_now)

    @model_validator(mode="after")
    def validate_requirement(self) -> "ApplyExecutorRollbackRequirement":
        _validate_non_executing_flags(
            risk_assessment_only=self.risk_assessment_only,
            executor_ready=self.executor_ready,
            review_required=self.review_required,
            applies_changes=self.applies_changes,
            writes_memory_store=self.writes_memory_store,
            writes_persona_version=self.writes_persona_version,
            runtime_ready=self.runtime_ready,
            record_name="apply executor rollback requirements",
        )
        self.source_refs = _ordered_unique(self.source_refs)
        return self


class ApplyExecutorAuditRequirement(_ApplyExecutorRiskRecord):
    schema_version: str = "apply_executor_audit_requirement_v1"
    requirement_id: str = Field(default_factory=lambda: new_id("aeaudit"))
    event_code: str = Field(..., min_length=1)
    safe_summary: str = Field(..., min_length=1)
    covered: bool = False
    source_refs: list[str] = Field(default_factory=list)
    risk_assessment_only: bool = True
    executor_ready: bool = False
    review_required: bool = True
    applies_changes: bool = False
    writes_memory_store: bool = False
    writes_persona_version: bool = False
    runtime_ready: bool = False
    created_at: datetime = Field(default_factory=utc_now)

    @model_validator(mode="after")
    def validate_requirement(self) -> "ApplyExecutorAuditRequirement":
        _validate_non_executing_flags(
            risk_assessment_only=self.risk_assessment_only,
            executor_ready=self.executor_ready,
            review_required=self.review_required,
            applies_changes=self.applies_changes,
            writes_memory_store=self.writes_memory_store,
            writes_persona_version=self.writes_persona_version,
            runtime_ready=self.runtime_ready,
            record_name="apply executor audit requirements",
        )
        self.source_refs = _ordered_unique(self.source_refs)
        return self


class ApplyExecutorRiskAssessment(_ApplyExecutorRiskRecord):
    schema_version: str = "apply_executor_risk_assessment_v1"
    assessment_id: str = Field(default_factory=lambda: new_id("aeassess"))
    preview_id: str = Field(..., min_length=1)
    decision_id: str = Field(..., min_length=1)
    candidate_kind: ReviewCandidateKind
    candidate_id: str = Field(..., min_length=1)
    safe_summary: str = Field(..., min_length=1)
    risk_factors: list[ApplyExecutorRiskFactor] = Field(default_factory=list)
    approval_gates: list[ApplyExecutorApprovalGate] = Field(default_factory=list)
    rollback_requirements: list[ApplyExecutorRollbackRequirement] = Field(default_factory=list)
    audit_requirements: list[ApplyExecutorAuditRequirement] = Field(default_factory=list)
    blocking_issue_codes: list[str] = Field(default_factory=list)
    final_recommendation: ApplyExecutorRiskRecommendation = "blocked"
    risk_assessment_only: bool = True
    executor_ready: bool = False
    review_required: bool = True
    applies_changes: bool = False
    writes_memory_store: bool = False
    writes_persona_version: bool = False
    runtime_ready: bool = False
    created_at: datetime = Field(default_factory=utc_now)

    @model_validator(mode="after")
    def validate_assessment(self) -> "ApplyExecutorRiskAssessment":
        _validate_non_executing_flags(
            risk_assessment_only=self.risk_assessment_only,
            executor_ready=self.executor_ready,
            review_required=self.review_required,
            applies_changes=self.applies_changes,
            writes_memory_store=self.writes_memory_store,
            writes_persona_version=self.writes_persona_version,
            runtime_ready=self.runtime_ready,
            record_name="apply executor risk assessments",
        )
        blockers = _assessment_blockers(
            risk_factors=self.risk_factors,
            approval_gates=self.approval_gates,
            rollback_requirements=self.rollback_requirements,
            audit_requirements=self.audit_requirements,
        )
        self.blocking_issue_codes = _ordered_unique(
            [*self.blocking_issue_codes, *blockers]
        )
        self.final_recommendation = _recommendation(
            risk_factors=self.risk_factors,
            blocking_issue_codes=self.blocking_issue_codes,
        )
        self.executor_ready = False
        return self


def _assessment_blockers(
    *,
    risk_factors: Iterable[ApplyExecutorRiskFactor],
    approval_gates: Iterable[ApplyExecutorApprovalGate],
    rollback_requirements: Iterable[ApplyExecutorRollbackRequirement],
    audit_requirements: Iterable[ApplyExecutorAuditRequirement],
) -> list[str]:
    blockers: list[str] = []
    for factor in risk_factors:
        if factor.severity == "critical":
            blockers.append(f"critical_risk:{factor.risk_code}")
    for gate in approval_gates:
        if not gate.satisfied:
            blockers.append(f"approval_gate_unsatisfied:{gate.gate_code}")
    for requirement in rollback_requirements:
        if not requirement.covered:
            blockers.append(f"rollback_requirement_uncovered:{requirement.requirement_code}")
    for requirement in audit_requirements:
        if not requirement.covered:
            blockers.append(f"audit_requirement_uncovered:{requirement.event_code}")
    return _ordered_unique(blockers)


def _recommendation(
    *,
    risk_factors: Iterable[ApplyExecutorRiskFactor],
    blocking_issue_codes: list[str],
) -> ApplyExecutorRiskRecommendation:
    if blocking_issue_codes:
        return "blocked"
    if any(factor.severity == "high" for factor in risk_factors):
        return "needs_review"
    return "ready_for_separately_scoped_executor_design"


def _validate_non_executing_flags(
    *,
    risk_assessment_only: bool,
    executor_ready: bool,
    review_required: bool,
    applies_changes: bool,
    writes_memory_store: bool,
    writes_persona_version: bool,
    runtime_ready: bool,
    record_name: str,
) -> None:
    if not risk_assessment_only:
        raise ValueError(f"{record_name} must remain risk-assessment-only")
    if executor_ready:
        raise ValueError(f"{record_name} cannot mark executors ready")
    if not review_required:
        raise ValueError(f"{record_name} require review")
    if applies_changes:
        raise ValueError(f"{record_name} cannot apply changes")
    if writes_memory_store:
        raise ValueError(f"{record_name} cannot write memory stores")
    if writes_persona_version:
        raise ValueError(f"{record_name} cannot write persona versions")
    if runtime_ready:
        raise ValueError(f"{record_name} are never runtime-ready")


def _ordered_unique(values: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value and value not in seen:
            seen.add(value)
            result.append(value)
    return result
