"""Non-mutating eligibility gate for manual apply previews."""

from __future__ import annotations

from collections.abc import Iterable
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from practical_chat_agent.core.ids import new_id
from practical_chat_agent.core.models import utc_now
from practical_chat_agent.services.manual_apply_preview import ManualApplyPreviewRecord
from practical_chat_agent.services.review_decision_impact_preview import (
    ReviewDecisionImpactOutcome,
)
from practical_chat_agent.services.review_queue import ReviewCandidateKind


ManualApplyEligibilityOutcome = Literal["eligible", "blocked", "stale"]


class _ManualApplyEligibilityRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ManualApplyEligibilityDecision(_ManualApplyEligibilityRecord):
    schema_version: str = "manual_apply_eligibility_decision_v1"
    eligibility_id: str = Field(default_factory=lambda: new_id("mapelig"))
    preview_id: str = Field(..., min_length=1)
    bundle_id: str = Field(..., min_length=1)
    decision_id: str = Field(..., min_length=1)
    candidate_kind: ReviewCandidateKind
    candidate_id: str = Field(..., min_length=1)
    preview_outcome: ReviewDecisionImpactOutcome
    eligibility_outcome: ManualApplyEligibilityOutcome
    safe_summary: str = Field(..., min_length=1)
    required_gate_codes: list[str] = Field(default_factory=list)
    satisfied_gate_codes: list[str] = Field(default_factory=list)
    missing_gate_codes: list[str] = Field(default_factory=list)
    stale_reasons: list[str] = Field(default_factory=list)
    issue_codes: list[str] = Field(default_factory=list)
    blocking_issue_codes: list[str] = Field(default_factory=list)
    effect_count: int = Field(default=0, ge=0)
    review_required: bool = True
    preview_only: bool = True
    applies_changes: bool = False
    writes_memory_store: bool = False
    writes_persona_version: bool = False
    runtime_ready: bool = False
    created_at: datetime = Field(default_factory=utc_now)

    @model_validator(mode="after")
    def validate_decision(self) -> "ManualApplyEligibilityDecision":
        _validate_non_mutating_flags(
            review_required=self.review_required,
            preview_only=self.preview_only,
            applies_changes=self.applies_changes,
            writes_memory_store=self.writes_memory_store,
            writes_persona_version=self.writes_persona_version,
            runtime_ready=self.runtime_ready,
            record_name="manual apply eligibility decisions",
        )
        self.required_gate_codes = _ordered_unique(self.required_gate_codes)
        self.satisfied_gate_codes = _ordered_unique(self.satisfied_gate_codes)
        self.missing_gate_codes = _ordered_unique(self.missing_gate_codes)
        self.stale_reasons = _ordered_unique(self.stale_reasons)
        self.issue_codes = _ordered_unique(self.issue_codes)
        self.blocking_issue_codes = _ordered_unique(self.blocking_issue_codes)
        return self


class ManualApplyEligibilityGate:
    """Evaluate manual apply preview eligibility without applying changes."""

    def evaluate(
        self,
        preview: ManualApplyPreviewRecord,
        *,
        expected_decision_id: str | None = None,
        expected_candidate_id: str | None = None,
        expected_preview_outcome: ReviewDecisionImpactOutcome | None = None,
        required_gate_codes: Iterable[str] | None = None,
    ) -> ManualApplyEligibilityDecision:
        stale_reasons = _stale_reasons(
            preview,
            expected_decision_id=expected_decision_id,
            expected_candidate_id=expected_candidate_id,
            expected_preview_outcome=expected_preview_outcome,
        )
        required_codes = _ordered_unique(
            required_gate_codes
            if required_gate_codes is not None
            else [gate.gate_code for gate in preview.required_gates]
        )
        satisfied_codes = _ordered_unique(
            gate.gate_code for gate in preview.required_gates if gate.satisfied
        )
        missing_codes = [
            code for code in required_codes if code not in satisfied_codes
        ]
        blocking_codes = _ordered_unique(
            [
                *preview.blocking_issue_codes,
                *(
                    f"missing_required_gate:{code}"
                    for code in missing_codes
                ),
            ]
        )

        if stale_reasons:
            return _decision(
                preview,
                eligibility_outcome="stale",
                safe_summary="[SYNTHETIC] Manual apply preview is stale.",
                required_gate_codes=required_codes,
                satisfied_gate_codes=satisfied_codes,
                missing_gate_codes=missing_codes,
                stale_reasons=stale_reasons,
                issue_codes=[*preview.issue_codes, "manual_apply_preview_stale"],
                blocking_issue_codes=["manual_apply_preview_stale"],
            )

        if blocking_codes or not preview.manual_apply_preview_eligible:
            return _decision(
                preview,
                eligibility_outcome="blocked",
                safe_summary="[SYNTHETIC] Manual apply preview is blocked.",
                required_gate_codes=required_codes,
                satisfied_gate_codes=satisfied_codes,
                missing_gate_codes=missing_codes,
                issue_codes=[*preview.issue_codes, *blocking_codes],
                blocking_issue_codes=blocking_codes or ["manual_apply_preview_not_eligible"],
            )

        return _decision(
            preview,
            eligibility_outcome="eligible",
            safe_summary="[SYNTHETIC] Manual apply preview is eligible.",
            required_gate_codes=required_codes,
            satisfied_gate_codes=satisfied_codes,
            missing_gate_codes=[],
            issue_codes=list(preview.issue_codes),
            blocking_issue_codes=[],
        )


def _decision(
    preview: ManualApplyPreviewRecord,
    *,
    eligibility_outcome: ManualApplyEligibilityOutcome,
    safe_summary: str,
    required_gate_codes: Iterable[str],
    satisfied_gate_codes: Iterable[str],
    missing_gate_codes: Iterable[str],
    issue_codes: Iterable[str],
    blocking_issue_codes: Iterable[str],
    stale_reasons: Iterable[str] = (),
) -> ManualApplyEligibilityDecision:
    return ManualApplyEligibilityDecision(
        preview_id=preview.preview_id,
        bundle_id=preview.bundle_id,
        decision_id=preview.decision_id,
        candidate_kind=preview.candidate_kind,
        candidate_id=preview.candidate_id,
        preview_outcome=preview.preview_outcome,
        eligibility_outcome=eligibility_outcome,
        safe_summary=safe_summary,
        required_gate_codes=list(required_gate_codes),
        satisfied_gate_codes=list(satisfied_gate_codes),
        missing_gate_codes=list(missing_gate_codes),
        stale_reasons=list(stale_reasons),
        issue_codes=list(issue_codes),
        blocking_issue_codes=list(blocking_issue_codes),
        effect_count=preview.effect_count,
    )


def _stale_reasons(
    preview: ManualApplyPreviewRecord,
    *,
    expected_decision_id: str | None,
    expected_candidate_id: str | None,
    expected_preview_outcome: ReviewDecisionImpactOutcome | None,
) -> list[str]:
    reasons: list[str] = []
    if expected_decision_id is not None and expected_decision_id != preview.decision_id:
        reasons.append("decision_id_mismatch")
    if expected_candidate_id is not None and expected_candidate_id != preview.candidate_id:
        reasons.append("candidate_id_mismatch")
    if (
        expected_preview_outcome is not None
        and expected_preview_outcome != preview.preview_outcome
    ):
        reasons.append("preview_outcome_mismatch")
    return reasons


def _validate_non_mutating_flags(
    *,
    review_required: bool,
    preview_only: bool,
    applies_changes: bool,
    writes_memory_store: bool,
    writes_persona_version: bool,
    runtime_ready: bool,
    record_name: str,
) -> None:
    if not review_required:
        raise ValueError(f"{record_name} require review")
    if not preview_only:
        raise ValueError(f"{record_name} are preview-only")
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
