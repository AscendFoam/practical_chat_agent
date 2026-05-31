"""Local-only persona growth apply executor."""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from practical_chat_agent.core.ids import new_id
from practical_chat_agent.core.models import PersonaCard, utc_now
from practical_chat_agent.services.apply_executor_approval_gate import (
    ApplyExecutorApprovalDecision,
)
from practical_chat_agent.services.manual_apply_eligibility_gate import (
    ManualApplyEligibilityDecision,
)
from practical_chat_agent.services.persona_growth_dry_run import (
    PersonaGrowthDryRunFieldPreview,
    PersonaGrowthDryRunPlan,
)
from practical_chat_agent.services.persona_version_store import (
    PersonaVersionRecord,
    PersonaVersionStore,
)


PERSONA_GROWTH_APPLY_CONFIRMATION = "CONFIRM_LOCAL_PERSONA_APPLY"
PersonaGrowthApplyConfirmationState = Literal["confirmed"]


class PersonaGrowthApplyError(ValueError):
    """Raised when a local persona growth apply request is not eligible."""


class _PersonaGrowthApplyRecord(BaseModel):
    model_config = ConfigDict(extra="forbid", arbitrary_types_allowed=True)


class PersonaGrowthApplyRequest(_PersonaGrowthApplyRecord):
    schema_version: str = "persona_growth_apply_request_v1"
    plan: PersonaGrowthDryRunPlan
    manual_eligibility: ManualApplyEligibilityDecision
    approval_decision: ApplyExecutorApprovalDecision
    persona_store: PersonaVersionStore
    reviewer_id: str = Field(..., min_length=1)
    final_confirmation: str = ""
    local_only: bool = True
    review_required: bool = True
    automatic_apply: bool = False
    calls_provider: bool = False
    sends_messages: bool = False
    writes_memory_store: bool = False
    writes_persona_version: bool = True
    runtime_ready: bool = False

    @model_validator(mode="after")
    def validate_request(self) -> "PersonaGrowthApplyRequest":
        if not self.local_only:
            raise ValueError("persona growth apply requests must stay local-only")
        if not self.review_required:
            raise ValueError("persona growth apply requests require review")
        if self.automatic_apply:
            raise ValueError("persona growth apply requests cannot be automatic")
        if self.calls_provider:
            raise ValueError("persona growth apply requests cannot call providers")
        if self.sends_messages:
            raise ValueError("persona growth apply requests cannot send messages")
        if self.writes_memory_store:
            raise ValueError("persona growth apply requests cannot write memory stores")
        if not self.writes_persona_version:
            raise ValueError("persona growth apply requests must write a persona version")
        if self.runtime_ready:
            raise ValueError("persona growth apply requests are not runtime-ready")
        return self


class PersonaGrowthApplyAudit(_PersonaGrowthApplyRecord):
    schema_version: str = "persona_growth_apply_audit_v1"
    apply_id: str = Field(default_factory=lambda: new_id("pgapply"))
    persona_id: str = Field(..., min_length=1)
    patch_id: str = Field(..., min_length=1)
    plan_id: str = Field(..., min_length=1)
    review_decision_id: str = Field(..., min_length=1)
    eligibility_id: str = Field(..., min_length=1)
    approval_id: str = Field(..., min_length=1)
    reviewer_id: str = Field(..., min_length=1)
    prior_version_id: str = Field(..., min_length=1)
    new_version_id: str = Field(..., min_length=1)
    rollback_target_version_id: str = Field(..., min_length=1)
    changed_field_paths: list[str] = Field(default_factory=list)
    safe_summary: str = Field(..., min_length=1)
    final_confirmation: PersonaGrowthApplyConfirmationState = "confirmed"
    local_only: bool = True
    review_required: bool = True
    automatic_apply: bool = False
    calls_provider: bool = False
    sends_messages: bool = False
    writes_memory_store: bool = False
    writes_persona_version: bool = True
    runtime_ready: bool = False
    created_at: datetime = Field(default_factory=utc_now)

    @model_validator(mode="after")
    def validate_audit(self) -> "PersonaGrowthApplyAudit":
        if not self.local_only:
            raise ValueError("persona growth apply audits must stay local-only")
        if not self.review_required:
            raise ValueError("persona growth apply audits require review")
        if self.automatic_apply:
            raise ValueError("persona growth apply audits cannot be automatic")
        if self.calls_provider:
            raise ValueError("persona growth apply audits cannot call providers")
        if self.sends_messages:
            raise ValueError("persona growth apply audits cannot send messages")
        if self.writes_memory_store:
            raise ValueError("persona growth apply audits cannot write memory stores")
        if not self.writes_persona_version:
            raise ValueError("persona growth apply audits must record persona version writes")
        if self.runtime_ready:
            raise ValueError("persona growth apply audits are not runtime-ready")
        self.changed_field_paths = _ordered_unique(self.changed_field_paths)
        return self


class PersonaGrowthApplyExecutor:
    """Apply reviewed persona growth to a caller-supplied local version store."""

    def apply(self, request: PersonaGrowthApplyRequest) -> PersonaGrowthApplyAudit:
        _validate_apply_request(request)
        latest = request.persona_store.latest_record(request.plan.persona_id)
        _validate_source_version(request.plan, latest)
        next_card = _apply_plan_to_card(latest.card, request.plan)
        new_record = request.persona_store.save(next_card)
        return PersonaGrowthApplyAudit(
            persona_id=request.plan.persona_id,
            patch_id=request.plan.patch_id,
            plan_id=request.plan.plan_id,
            review_decision_id=request.plan.review_decision_id or request.manual_eligibility.decision_id,
            eligibility_id=request.manual_eligibility.eligibility_id,
            approval_id=request.approval_decision.approval_id,
            reviewer_id=request.reviewer_id,
            prior_version_id=latest.version_id,
            new_version_id=new_record.version_id,
            rollback_target_version_id=latest.version_id,
            changed_field_paths=[preview.field_path for preview in request.plan.field_previews],
            safe_summary="[SYNTHETIC] Local persona growth apply completed.",
        )


def _validate_apply_request(request: PersonaGrowthApplyRequest) -> None:
    if request.final_confirmation != PERSONA_GROWTH_APPLY_CONFIRMATION:
        raise PersonaGrowthApplyError("final confirmation is required")
    if not request.plan.ready_for_later_manual_apply:
        raise PersonaGrowthApplyError("dry-run plan is not ready for manual apply")
    if not request.plan.field_previews:
        raise PersonaGrowthApplyError("dry-run plan has no field previews")
    if request.manual_eligibility.eligibility_outcome != "eligible":
        raise PersonaGrowthApplyError("manual eligibility is not eligible")
    if request.approval_decision.final_outcome != "ready_for_separately_scoped_executor_design":
        raise PersonaGrowthApplyError("apply executor approval is not ready")
    if request.manual_eligibility.decision_id != request.plan.review_decision_id:
        raise PersonaGrowthApplyError("manual eligibility decision does not match plan")
    if request.manual_eligibility.candidate_kind != "persona_growth_patch":
        raise PersonaGrowthApplyError("manual eligibility candidate kind does not match persona growth")
    if request.manual_eligibility.candidate_id != request.plan.patch_id:
        raise PersonaGrowthApplyError("manual eligibility candidate id does not match plan")
    if request.approval_decision.decision_id != request.plan.review_decision_id:
        raise PersonaGrowthApplyError("approval decision does not match plan")
    if request.approval_decision.candidate_kind != "persona_growth_patch":
        raise PersonaGrowthApplyError("approval candidate kind does not match persona growth")
    if request.approval_decision.candidate_id != request.plan.patch_id:
        raise PersonaGrowthApplyError("approval candidate id does not match plan")


def _validate_source_version(
    plan: PersonaGrowthDryRunPlan,
    latest: PersonaVersionRecord,
) -> None:
    if latest.persona_id != plan.persona_id:
        raise PersonaGrowthApplyError("latest persona id does not match plan")
    if latest.version_number != plan.source_persona_version:
        raise PersonaGrowthApplyError("source persona version is stale")


def _apply_plan_to_card(
    card: PersonaCard,
    plan: PersonaGrowthDryRunPlan,
) -> PersonaCard:
    next_card = card.model_copy(deep=True)
    for preview in plan.field_previews:
        _apply_field_preview(next_card, preview)
    return PersonaCard.model_validate(next_card.model_dump(mode="python"))


def _apply_field_preview(
    card: PersonaCard,
    preview: PersonaGrowthDryRunFieldPreview,
) -> None:
    target, field_name = _resolve_parent(card, preview.field_path)
    current_value = getattr(target, field_name)
    if preview.numeric_delta is not None:
        if not isinstance(current_value, int | float):
            raise PersonaGrowthApplyError("numeric delta targets must be numeric")
        next_value = round(float(current_value) + preview.numeric_delta, 6)
    else:
        next_value = preview.proposed_value_summary
    setattr(target, field_name, next_value)


def _resolve_parent(card: PersonaCard, field_path: str) -> tuple[object, str]:
    parts = field_path.split(".")
    if len(parts) < 2:
        raise PersonaGrowthApplyError("field path must target a nested persona field")
    target: object = card
    for part in parts[:-1]:
        if not hasattr(target, part):
            raise PersonaGrowthApplyError(f"unknown persona field path: {field_path}")
        target = getattr(target, part)
    field_name = parts[-1]
    if not hasattr(target, field_name):
        raise PersonaGrowthApplyError(f"unknown persona field path: {field_path}")
    return target, field_name


def _ordered_unique(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value and value not in seen:
            seen.add(value)
            result.append(value)
    return result
