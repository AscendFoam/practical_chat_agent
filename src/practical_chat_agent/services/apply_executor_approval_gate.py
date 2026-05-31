"""Non-executing approval gate for future apply executor design."""

from __future__ import annotations

from collections.abc import Iterable
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from practical_chat_agent.core.ids import new_id
from practical_chat_agent.core.models import utc_now
from practical_chat_agent.services.apply_executor_risk import (
    ApplyExecutorRiskAssessment,
    ApplyExecutorRiskRecommendation,
)
from practical_chat_agent.services.manual_apply_eligibility_gate import (
    ManualApplyEligibilityDecision,
)
from practical_chat_agent.services.review_queue import ReviewCandidateKind


ManualEligibilityState = Literal["eligible", "blocked", "stale", "not_supplied"]
ApplyExecutorApprovalOutcome = ApplyExecutorRiskRecommendation


class _ApplyExecutorApprovalRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ApplyExecutorApprovalDecision(_ApplyExecutorApprovalRecord):
    schema_version: str = "apply_executor_approval_decision_v1"
    approval_id: str = Field(default_factory=lambda: new_id("aeapproval"))
    assessment_id: str = Field(..., min_length=1)
    preview_id: str = Field(..., min_length=1)
    decision_id: str = Field(..., min_length=1)
    candidate_kind: ReviewCandidateKind
    candidate_id: str = Field(..., min_length=1)
    risk_recommendation: ApplyExecutorRiskRecommendation
    manual_eligibility_outcome: ManualEligibilityState = "not_supplied"
    safe_summary: str = Field(..., min_length=1)
    required_approval_gate_codes: list[str] = Field(default_factory=list)
    satisfied_approval_gate_codes: list[str] = Field(default_factory=list)
    missing_approval_gate_codes: list[str] = Field(default_factory=list)
    stale_reasons: list[str] = Field(default_factory=list)
    issue_codes: list[str] = Field(default_factory=list)
    risk_blocking_issue_codes: list[str] = Field(default_factory=list)
    manual_blocking_issue_codes: list[str] = Field(default_factory=list)
    blocking_issue_codes: list[str] = Field(default_factory=list)
    final_outcome: ApplyExecutorApprovalOutcome = "blocked"
    review_required: bool = True
    risk_assessment_only: bool = True
    executor_ready: bool = False
    applies_changes: bool = False
    writes_memory_store: bool = False
    writes_persona_version: bool = False
    runtime_ready: bool = False
    created_at: datetime = Field(default_factory=utc_now)

    @model_validator(mode="after")
    def validate_decision(self) -> "ApplyExecutorApprovalDecision":
        _validate_non_executing_flags(
            review_required=self.review_required,
            risk_assessment_only=self.risk_assessment_only,
            executor_ready=self.executor_ready,
            applies_changes=self.applies_changes,
            writes_memory_store=self.writes_memory_store,
            writes_persona_version=self.writes_persona_version,
            runtime_ready=self.runtime_ready,
            record_name="apply executor approval decisions",
        )
        self.required_approval_gate_codes = _ordered_unique(
            self.required_approval_gate_codes
        )
        self.satisfied_approval_gate_codes = _ordered_unique(
            self.satisfied_approval_gate_codes
        )
        self.missing_approval_gate_codes = _ordered_unique(
            self.missing_approval_gate_codes
        )
        self.stale_reasons = _ordered_unique(self.stale_reasons)
        self.issue_codes = _ordered_unique(self.issue_codes)
        self.risk_blocking_issue_codes = _ordered_unique(
            self.risk_blocking_issue_codes
        )
        self.manual_blocking_issue_codes = _ordered_unique(
            self.manual_blocking_issue_codes
        )
        self.blocking_issue_codes = _ordered_unique(self.blocking_issue_codes)
        self.executor_ready = False
        return self


class ApplyExecutorApprovalGate:
    """Evaluate future apply-executor approval without applying changes."""

    def evaluate(
        self,
        risk_assessment: ApplyExecutorRiskAssessment,
        *,
        manual_eligibility: ManualApplyEligibilityDecision | None = None,
        required_approval_gate_codes: Iterable[str] | None = None,
    ) -> ApplyExecutorApprovalDecision:
        required_codes = _ordered_unique(
            required_approval_gate_codes
            if required_approval_gate_codes is not None
            else [gate.gate_code for gate in risk_assessment.approval_gates]
        )
        satisfied_codes = _ordered_unique(
            gate.gate_code for gate in risk_assessment.approval_gates if gate.satisfied
        )
        missing_codes = [code for code in required_codes if code not in satisfied_codes]
        risk_blockers = list(risk_assessment.blocking_issue_codes)
        manual_state, manual_blockers, stale_reasons = _manual_eligibility_state(
            risk_assessment,
            manual_eligibility,
        )
        gate_blockers = [
            f"missing_approval_gate:{code}" for code in missing_codes
        ]
        blocking_codes = _ordered_unique(
            [*risk_blockers, *manual_blockers, *gate_blockers]
        )
        final_outcome = _final_outcome(
            risk_recommendation=risk_assessment.final_recommendation,
            blocking_issue_codes=blocking_codes,
        )

        return ApplyExecutorApprovalDecision(
            assessment_id=risk_assessment.assessment_id,
            preview_id=risk_assessment.preview_id,
            decision_id=risk_assessment.decision_id,
            candidate_kind=risk_assessment.candidate_kind,
            candidate_id=risk_assessment.candidate_id,
            risk_recommendation=risk_assessment.final_recommendation,
            manual_eligibility_outcome=manual_state,
            safe_summary=_safe_summary(final_outcome),
            required_approval_gate_codes=required_codes,
            satisfied_approval_gate_codes=satisfied_codes,
            missing_approval_gate_codes=missing_codes,
            stale_reasons=stale_reasons,
            issue_codes=_ordered_unique([*risk_blockers, *manual_blockers, *gate_blockers]),
            risk_blocking_issue_codes=risk_blockers,
            manual_blocking_issue_codes=manual_blockers,
            blocking_issue_codes=blocking_codes,
            final_outcome=final_outcome,
        )


def _manual_eligibility_state(
    risk_assessment: ApplyExecutorRiskAssessment,
    manual_eligibility: ManualApplyEligibilityDecision | None,
) -> tuple[ManualEligibilityState, list[str], list[str]]:
    if manual_eligibility is None:
        return "not_supplied", [], []

    blockers: list[str] = []
    stale_reasons = _manual_context_mismatches(
        risk_assessment,
        manual_eligibility,
    )

    if manual_eligibility.eligibility_outcome == "blocked":
        blockers.append("manual_apply_eligibility_blocked")
        blockers.extend(manual_eligibility.blocking_issue_codes)
    if manual_eligibility.eligibility_outcome == "stale":
        blockers.append("manual_apply_eligibility_stale")
        stale_reasons.extend(manual_eligibility.stale_reasons)
        blockers.extend(manual_eligibility.blocking_issue_codes)
    if stale_reasons:
        blockers.append("manual_apply_eligibility_context_mismatch")

    return (
        manual_eligibility.eligibility_outcome,
        _ordered_unique(blockers),
        _ordered_unique(stale_reasons),
    )


def _manual_context_mismatches(
    risk_assessment: ApplyExecutorRiskAssessment,
    manual_eligibility: ManualApplyEligibilityDecision,
) -> list[str]:
    reasons: list[str] = []
    if manual_eligibility.preview_id != risk_assessment.preview_id:
        reasons.append("manual_preview_id_mismatch")
    if manual_eligibility.decision_id != risk_assessment.decision_id:
        reasons.append("manual_decision_id_mismatch")
    if manual_eligibility.candidate_kind != risk_assessment.candidate_kind:
        reasons.append("manual_candidate_kind_mismatch")
    if manual_eligibility.candidate_id != risk_assessment.candidate_id:
        reasons.append("manual_candidate_id_mismatch")
    return reasons


def _final_outcome(
    *,
    risk_recommendation: ApplyExecutorRiskRecommendation,
    blocking_issue_codes: list[str],
) -> ApplyExecutorApprovalOutcome:
    if blocking_issue_codes or risk_recommendation == "blocked":
        return "blocked"
    if risk_recommendation == "needs_review":
        return "needs_review"
    return "ready_for_separately_scoped_executor_design"


def _safe_summary(final_outcome: ApplyExecutorApprovalOutcome) -> str:
    if final_outcome == "blocked":
        return "[SYNTHETIC] Future apply executor approval is blocked."
    if final_outcome == "needs_review":
        return "[SYNTHETIC] Future apply executor approval needs review."
    return "[SYNTHETIC] Future apply executor design can be separately scoped."


def _validate_non_executing_flags(
    *,
    review_required: bool,
    risk_assessment_only: bool,
    executor_ready: bool,
    applies_changes: bool,
    writes_memory_store: bool,
    writes_persona_version: bool,
    runtime_ready: bool,
    record_name: str,
) -> None:
    if not review_required:
        raise ValueError(f"{record_name} require review")
    if not risk_assessment_only:
        raise ValueError(f"{record_name} must remain risk-assessment-only")
    if executor_ready:
        raise ValueError(f"{record_name} cannot mark executors ready")
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
