"""Non-mutating manual apply preview records.

These records describe what a future manual apply action would need to
inspect. They do not apply decisions, mutate stores, write persona versions,
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
from practical_chat_agent.services.review_decision_impact_preview import (
    ReviewDecisionImpactOutcome,
    ReviewDecisionImpactPreview,
)
from practical_chat_agent.services.review_queue import ReviewCandidateKind


ManualApplyPreviewEffectKind = Literal[
    "memory_store_preview",
    "persona_version_preview",
    "deletion_preview",
    "cache_invalidation_preview",
]


class _ManualApplyPreviewBase(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ManualApplyPreviewGate(_ManualApplyPreviewBase):
    schema_version: str = "manual_apply_preview_gate_v1"
    gate_id: str = Field(default_factory=lambda: new_id("mapgate"))
    gate_code: str = Field(..., min_length=1)
    label: str = Field(..., min_length=1)
    safe_summary: str = Field(..., min_length=1)
    satisfied: bool = False
    blocking_issue_codes: list[str] = Field(default_factory=list)
    source_refs: list[str] = Field(default_factory=list)
    blocks_preview: bool = True
    review_required: bool = True
    preview_only: bool = True
    applies_changes: bool = False
    writes_memory_store: bool = False
    writes_persona_version: bool = False
    runtime_ready: bool = False
    created_at: datetime = Field(default_factory=utc_now)

    @model_validator(mode="after")
    def validate_gate(self) -> "ManualApplyPreviewGate":
        _validate_non_mutating_flags(
            review_required=self.review_required,
            preview_only=self.preview_only,
            applies_changes=self.applies_changes,
            writes_memory_store=self.writes_memory_store,
            writes_persona_version=self.writes_persona_version,
            runtime_ready=self.runtime_ready,
            record_name="manual apply preview gates",
        )
        self.source_refs = _ordered_unique(self.source_refs)
        self.blocking_issue_codes = _ordered_unique(self.blocking_issue_codes)
        if not self.satisfied:
            self.blocks_preview = True
            self.blocking_issue_codes = _ordered_unique(
                [*self.blocking_issue_codes, "manual_apply_gate_unsatisfied"]
            )
        return self


class ManualApplyPreviewEffect(_ManualApplyPreviewBase):
    schema_version: str = "manual_apply_preview_effect_v1"
    effect_id: str = Field(default_factory=lambda: new_id("mapeffect"))
    effect_kind: ManualApplyPreviewEffectKind
    target_ref: str = Field(..., min_length=1)
    safe_summary: str = Field(..., min_length=1)
    artifact_ids: list[str] = Field(default_factory=list)
    source_refs: list[str] = Field(default_factory=list)
    rollback_notes: list[str] = Field(default_factory=list)
    review_required: bool = True
    preview_only: bool = True
    applies_changes: bool = False
    writes_memory_store: bool = False
    writes_persona_version: bool = False
    runtime_ready: bool = False
    created_at: datetime = Field(default_factory=utc_now)

    @model_validator(mode="after")
    def validate_effect(self) -> "ManualApplyPreviewEffect":
        _validate_non_mutating_flags(
            review_required=self.review_required,
            preview_only=self.preview_only,
            applies_changes=self.applies_changes,
            writes_memory_store=self.writes_memory_store,
            writes_persona_version=self.writes_persona_version,
            runtime_ready=self.runtime_ready,
            record_name="manual apply preview effects",
        )
        self.artifact_ids = _ordered_unique(self.artifact_ids)
        self.source_refs = _ordered_unique(self.source_refs)
        self.rollback_notes = _ordered_unique(self.rollback_notes)
        return self


class ManualApplyPreviewRecord(_ManualApplyPreviewBase):
    schema_version: str = "manual_apply_preview_record_v1"
    preview_id: str = Field(default_factory=lambda: new_id("mapprev"))
    bundle_id: str = Field(..., min_length=1)
    decision_id: str = Field(..., min_length=1)
    candidate_kind: ReviewCandidateKind
    candidate_id: str = Field(..., min_length=1)
    preview_outcome: ReviewDecisionImpactOutcome
    safe_summary: str = Field(..., min_length=1)
    reason_labels: list[str] = Field(default_factory=list)
    source_refs: list[str] = Field(default_factory=list)
    artifact_ids: list[str] = Field(default_factory=list)
    required_gates: list[ManualApplyPreviewGate] = Field(default_factory=list)
    effects: list[ManualApplyPreviewEffect] = Field(default_factory=list)
    rollback_notes: list[str] = Field(default_factory=list)
    issue_codes: list[str] = Field(default_factory=list)
    blocking_issue_codes: list[str] = Field(default_factory=list)
    manual_apply_preview_eligible: bool = False
    effect_count: int = 0
    review_required: bool = True
    preview_only: bool = True
    applies_changes: bool = False
    writes_memory_store: bool = False
    writes_persona_version: bool = False
    runtime_ready: bool = False
    created_at: datetime = Field(default_factory=utc_now)

    @classmethod
    def from_impact_preview(
        cls,
        preview: ReviewDecisionImpactPreview,
        *,
        required_gates: Iterable[ManualApplyPreviewGate],
        effects: Iterable[ManualApplyPreviewEffect],
        rollback_notes: Iterable[str],
        applies_changes: bool = False,
        writes_memory_store: bool = False,
        writes_persona_version: bool = False,
        runtime_ready: bool = False,
    ) -> "ManualApplyPreviewRecord":
        artifact_ids = [
            impact.artifact_id for impact in preview.artifact_impacts
        ]
        return cls(
            bundle_id=preview.bundle_id,
            decision_id=preview.decision_id,
            candidate_kind=preview.candidate_kind,
            candidate_id=preview.candidate_id,
            preview_outcome=preview.preview_outcome,
            safe_summary=preview.safe_summary,
            reason_labels=list(preview.reason_labels),
            source_refs=list(preview.source_refs),
            artifact_ids=artifact_ids,
            required_gates=list(required_gates),
            effects=list(effects),
            rollback_notes=list(rollback_notes),
            issue_codes=list(preview.issue_codes),
            blocking_issue_codes=list(preview.blocking_issue_codes),
            applies_changes=applies_changes,
            writes_memory_store=writes_memory_store,
            writes_persona_version=writes_persona_version,
            runtime_ready=runtime_ready,
        )

    @model_validator(mode="after")
    def validate_record(self) -> "ManualApplyPreviewRecord":
        _validate_non_mutating_flags(
            review_required=self.review_required,
            preview_only=self.preview_only,
            applies_changes=self.applies_changes,
            writes_memory_store=self.writes_memory_store,
            writes_persona_version=self.writes_persona_version,
            runtime_ready=self.runtime_ready,
            record_name="manual apply preview records",
        )
        self.reason_labels = _ordered_unique(self.reason_labels)
        self.source_refs = _ordered_unique(self.source_refs)
        self.artifact_ids = _ordered_unique(self.artifact_ids)
        self.rollback_notes = _ordered_unique(self.rollback_notes)
        gate_blockers = [
            code
            for gate in self.required_gates
            for code in gate.blocking_issue_codes
            if gate.blocks_preview
        ]
        self.issue_codes = _ordered_unique([*self.issue_codes, *gate_blockers])
        self.blocking_issue_codes = _ordered_unique(
            [*self.blocking_issue_codes, *gate_blockers]
        )
        self.effect_count = len(self.effects)
        self.manual_apply_preview_eligible = (
            self.preview_outcome == "future_manual_apply_eligible"
            and not self.blocking_issue_codes
            and all(gate.satisfied for gate in self.required_gates)
        )
        return self


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
