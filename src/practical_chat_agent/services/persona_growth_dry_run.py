"""Preview-only persona growth dry-run plans.

These records describe how a persona growth patch would look if later applied
by a separate reviewed path. They do not mutate PersonaCard objects, write
persona versions, apply decisions, call providers, generate replies, send
messages, or connect to platform/media runtimes.
"""

from __future__ import annotations

from collections.abc import Iterable
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator

from practical_chat_agent.core.ids import new_id
from practical_chat_agent.core.models import PersonaCard, utc_now
from practical_chat_agent.services.persona_growth import (
    PersonaGrowthFieldChange,
    PersonaGrowthPatchCandidate,
)
from practical_chat_agent.services.review_queue import ReviewQueueDecisionRecord


class _PersonaGrowthDryRunRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")


class PersonaGrowthDryRunFieldPreview(_PersonaGrowthDryRunRecord):
    schema_version: str = "persona_growth_dry_run_field_preview_v1"
    preview_id: str = Field(default_factory=lambda: new_id("pgdfield"))
    field_path: str = Field(..., min_length=1)
    old_value_summary: str = Field(..., min_length=1)
    proposed_value_summary: str = Field(..., min_length=1)
    numeric_delta: float | None = None
    change_reason: str = Field(..., min_length=1)
    source_memory_ids: list[str] = Field(default_factory=list)
    source_review_refs: list[str] = Field(default_factory=list)
    risk_labels: list[str] = Field(default_factory=list)
    blocks_apply: bool = False
    preview_only: bool = True
    applies_changes: bool = False
    writes_persona_version: bool = False
    created_at: datetime = Field(default_factory=utc_now)

    @classmethod
    def from_change(cls, change: PersonaGrowthFieldChange) -> "PersonaGrowthDryRunFieldPreview":
        return cls(
            field_path=change.field_path,
            old_value_summary=change.old_value_summary,
            proposed_value_summary=change.proposed_value_summary,
            numeric_delta=change.numeric_delta,
            change_reason=change.change_reason,
            source_memory_ids=list(change.source_memory_ids),
            source_review_refs=list(change.source_review_refs),
            risk_labels=list(change.risk_labels),
            blocks_apply=change.blocks_approval,
        )

    @model_validator(mode="after")
    def validate_preview(self) -> "PersonaGrowthDryRunFieldPreview":
        if not self.preview_only:
            raise ValueError("persona growth dry-run field previews are preview-only")
        if self.applies_changes:
            raise ValueError("persona growth dry-run field previews cannot apply changes")
        if self.writes_persona_version:
            raise ValueError("persona growth dry-run field previews cannot write persona versions")
        self.source_memory_ids = _ordered_unique(self.source_memory_ids)
        self.source_review_refs = _ordered_unique(self.source_review_refs)
        self.risk_labels = _ordered_unique(self.risk_labels)
        self.blocks_apply = bool(self.blocks_apply or self.risk_labels)
        return self


class PersonaGrowthDryRunPlan(_PersonaGrowthDryRunRecord):
    schema_version: str = "persona_growth_dry_run_plan_v1"
    plan_id: str = Field(default_factory=lambda: new_id("pgdplan"))
    patch_id: str = Field(..., min_length=1)
    user_id: str = Field(..., min_length=1)
    persona_id: str = Field(..., min_length=1)
    source_persona_version: int = Field(..., ge=1)
    review_decision_id: str | None = None
    review_decision: str | None = None
    trigger_type: str
    safe_summary: str = Field(..., min_length=1)
    field_previews: list[PersonaGrowthDryRunFieldPreview] = Field(default_factory=list)
    blocked_field_paths: list[str] = Field(default_factory=list)
    blocking_risk_labels: list[str] = Field(default_factory=list)
    weekly_trait_delta_by_field: dict[str, float] = Field(default_factory=dict)
    weekly_trait_delta_after: dict[str, float] = Field(default_factory=dict)
    max_weekly_trait_delta: float = Field(default=0.2, ge=0.0, le=0.2)
    ready_for_later_manual_apply: bool = True
    blocked_reasons: list[str] = Field(default_factory=list)
    preview_only: bool = True
    review_required: bool = True
    applies_changes: bool = False
    writes_persona_version: bool = False
    created_at: datetime = Field(default_factory=utc_now)

    @model_validator(mode="after")
    def validate_plan(self) -> "PersonaGrowthDryRunPlan":
        if not self.preview_only:
            raise ValueError("persona growth dry-run plans are preview-only")
        if not self.review_required:
            raise ValueError("persona growth dry-run plans require review")
        if self.applies_changes:
            raise ValueError("persona growth dry-run plans cannot apply changes")
        if self.writes_persona_version:
            raise ValueError("persona growth dry-run plans cannot write persona versions")

        blocked_fields = list(self.blocked_field_paths)
        blocking_labels = list(self.blocking_risk_labels)
        for preview in self.field_previews:
            if preview.blocks_apply:
                blocked_fields.append(preview.field_path)
                blocking_labels.extend(preview.risk_labels)

        blocked_reasons = list(self.blocked_reasons)
        if blocking_labels:
            blocked_reasons.append("blocking_risk_labels")
        if self.review_decision and self.review_decision != "approve":
            blocked_reasons.append("review_decision_not_applied_by_dry_run")

        self.blocked_field_paths = _ordered_unique(blocked_fields)
        self.blocking_risk_labels = _ordered_unique(blocking_labels)
        self.blocked_reasons = _ordered_unique(blocked_reasons)
        self.ready_for_later_manual_apply = not self.blocked_field_paths and (
            self.review_decision in {None, "approve"}
        )
        return self


class PersonaGrowthDryRunService:
    """Create preview-only plans for persona growth patches."""

    def plan_from_patch(
        self,
        patch: PersonaGrowthPatchCandidate,
        *,
        source_persona: PersonaCard | None = None,
        decision_record: ReviewQueueDecisionRecord | None = None,
    ) -> PersonaGrowthDryRunPlan:
        if source_persona is not None and source_persona.persona_id != patch.persona_id:
            raise ValueError("source_persona does not match patch persona_id")

        field_previews = [
            PersonaGrowthDryRunFieldPreview.from_change(change)
            for change in patch.changes
        ]
        weekly_after = _weekly_delta_after(
            patch.weekly_trait_delta_by_field,
            patch.changes,
        )
        return PersonaGrowthDryRunPlan(
            patch_id=patch.patch_id,
            user_id=patch.user_id,
            persona_id=patch.persona_id,
            source_persona_version=patch.source_persona_version,
            review_decision_id=decision_record.decision_id if decision_record else None,
            review_decision=decision_record.decision if decision_record else None,
            trigger_type=patch.trigger_type,
            safe_summary=patch.user_facing_explanation,
            field_previews=field_previews,
            blocking_risk_labels=list(patch.blocking_risk_labels),
            weekly_trait_delta_by_field=dict(patch.weekly_trait_delta_by_field),
            weekly_trait_delta_after=weekly_after,
            max_weekly_trait_delta=patch.max_weekly_trait_delta,
            blocked_reasons=["persona_version_write_not_enabled_by_dry_run"],
        )


def _weekly_delta_after(
    weekly_trait_delta_by_field: dict[str, float],
    changes: Iterable[PersonaGrowthFieldChange],
) -> dict[str, float]:
    result = dict(weekly_trait_delta_by_field)
    for change in changes:
        if change.numeric_delta is None:
            continue
        result[change.field_path] = abs(result.get(change.field_path, 0.0)) + abs(change.numeric_delta)
    return result


def _ordered_unique(values: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value and value not in seen:
            seen.add(value)
            result.append(value)
    return result
