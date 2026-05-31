"""Local review queue records for review-first candidate artifacts.

This module only wraps existing candidate records for human review. It does
not apply decisions, mutate stores, write persona versions, call providers,
generate replies, send messages, or connect to platform/media runtimes.
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
    PersonaGrowthEvidenceBundle,
)
from practical_chat_agent.services.memory_retrieval_explanation import (
    MemoryRetrievalExplanationResult,
)
from practical_chat_agent.services.persona_growth import PersonaGrowthPatchCandidate
from practical_chat_agent.services.synthetic_distillation_input import (
    DeidentifiedStyleFeatureCandidate,
    SyntheticDistillationInputManifest,
)


ReviewCandidateKind = Literal[
    "memory_contradiction",
    "memory_supersession",
    "memory_deletion_cascade",
    "persona_growth_evidence",
    "persona_growth_patch",
    "synthetic_distillation_manifest",
    "deidentified_style_feature",
    "memory_retrieval_explanation",
]
ReviewPriorityBand = Literal["critical", "high", "normal", "low"]
ReviewStatus = Literal["queued", "decided"]
ReviewDecision = Literal["approve", "reject", "freeze", "request_changes"]


class _ReviewQueueRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ReviewQueueItem(_ReviewQueueRecord):
    schema_version: str = "review_queue_item_v1"
    item_id: str = Field(default_factory=lambda: new_id("rqitem"))
    candidate_kind: ReviewCandidateKind
    candidate_id: str = Field(..., min_length=1)
    source_schema_version: str | None = None
    owner_user_id: str | None = None
    persona_id: str | None = None
    title: str = Field(..., min_length=1)
    safe_summary: str = Field(..., min_length=1)
    reason_labels: list[str] = Field(default_factory=list)
    source_refs: list[str] = Field(default_factory=list)
    priority_score: int = Field(default=50, ge=0, le=100)
    priority_band: ReviewPriorityBand = "normal"
    review_required: bool = True
    review_status: ReviewStatus = "queued"
    blocks_auto_apply: bool = True
    candidate_created_at: datetime | None = None
    created_at: datetime = Field(default_factory=utc_now)

    @model_validator(mode="after")
    def validate_review_item(self) -> "ReviewQueueItem":
        if not self.review_required:
            raise ValueError("review queue items are always review-required")
        if not self.blocks_auto_apply:
            raise ValueError("review queue items cannot allow auto-apply")
        self.reason_labels = _ordered_unique(self.reason_labels)
        self.source_refs = _ordered_unique(self.source_refs)
        self.priority_band = _priority_band(self.priority_score)
        return self


class ReviewQueueSnapshot(_ReviewQueueRecord):
    schema_version: str = "review_queue_snapshot_v1"
    snapshot_id: str = Field(default_factory=lambda: new_id("rqsnap"))
    items: list[ReviewQueueItem] = Field(default_factory=list)
    counts_by_kind: dict[str, int] = Field(default_factory=dict)
    high_priority_item_ids: list[str] = Field(default_factory=list)
    review_required: bool = True
    generated_at: datetime = Field(default_factory=utc_now)

    @classmethod
    def from_items(cls, items: Iterable[ReviewQueueItem]) -> "ReviewQueueSnapshot":
        ordered = sorted(
            list(items),
            key=lambda item: (
                -item.priority_score,
                item.candidate_created_at or item.created_at,
                item.item_id,
            ),
        )
        return cls(items=ordered)

    @model_validator(mode="after")
    def validate_snapshot(self) -> "ReviewQueueSnapshot":
        if not self.review_required:
            raise ValueError("review queue snapshots are always review-required")
        counts: dict[str, int] = {}
        high_ids: list[str] = []
        for item in self.items:
            counts[item.candidate_kind] = counts.get(item.candidate_kind, 0) + 1
            if item.priority_score >= 70:
                high_ids.append(item.item_id)
        self.counts_by_kind = counts
        self.high_priority_item_ids = high_ids
        return self


class ReviewQueueDecisionRecord(_ReviewQueueRecord):
    schema_version: str = "review_queue_decision_record_v1"
    decision_id: str = Field(default_factory=lambda: new_id("rqdec"))
    item_id: str = Field(..., min_length=1)
    candidate_kind: ReviewCandidateKind
    candidate_id: str = Field(..., min_length=1)
    reviewer_id: str = Field(..., min_length=1)
    decision: ReviewDecision
    decision_notes: list[str] = Field(default_factory=list)
    applies_changes: bool = False
    writes_memory_store: bool = False
    writes_persona_version: bool = False
    decided_at: datetime = Field(default_factory=utc_now)

    @classmethod
    def from_item(
        cls,
        item: ReviewQueueItem,
        *,
        reviewer_id: str,
        decision: ReviewDecision,
        decision_notes: list[str] | None = None,
    ) -> "ReviewQueueDecisionRecord":
        return cls(
            item_id=item.item_id,
            candidate_kind=item.candidate_kind,
            candidate_id=item.candidate_id,
            reviewer_id=reviewer_id,
            decision=decision,
            decision_notes=list(decision_notes or []),
        )

    @model_validator(mode="after")
    def validate_decision_record(self) -> "ReviewQueueDecisionRecord":
        if self.applies_changes:
            raise ValueError("review queue decision records cannot apply changes")
        if self.writes_memory_store:
            raise ValueError("review queue decision records cannot write memory stores")
        if self.writes_persona_version:
            raise ValueError("review queue decision records cannot write persona versions")
        self.decision_notes = _ordered_unique(self.decision_notes)
        return self


class ReviewQueueService:
    """Wrap review-first candidate records into queue items."""

    def item_from_candidate(self, candidate: object) -> ReviewQueueItem:
        if isinstance(candidate, MemoryContradictionCandidate):
            return self._from_memory_contradiction(candidate)
        if isinstance(candidate, MemorySupersessionCandidate):
            return self._from_memory_supersession(candidate)
        if isinstance(candidate, MemoryDeletionCascadePlan):
            return self._from_memory_deletion(candidate)
        if isinstance(candidate, PersonaGrowthEvidenceBundle):
            return self._from_persona_growth_evidence(candidate)
        if isinstance(candidate, PersonaGrowthPatchCandidate):
            return self._from_persona_growth_patch(candidate)
        if isinstance(candidate, SyntheticDistillationInputManifest):
            return self._from_distillation_manifest(candidate)
        if isinstance(candidate, DeidentifiedStyleFeatureCandidate):
            return self._from_style_feature(candidate)
        if isinstance(candidate, MemoryRetrievalExplanationResult):
            return self._from_retrieval_result(candidate)
        raise TypeError(f"unsupported review queue candidate type: {type(candidate).__name__}")

    def build_snapshot(self, items: Iterable[ReviewQueueItem]) -> ReviewQueueSnapshot:
        return ReviewQueueSnapshot.from_items(items)

    def record_decision(
        self,
        item: ReviewQueueItem,
        *,
        reviewer_id: str,
        decision: ReviewDecision,
        decision_notes: list[str] | None = None,
    ) -> ReviewQueueDecisionRecord:
        return ReviewQueueDecisionRecord.from_item(
            item,
            reviewer_id=reviewer_id,
            decision=decision,
            decision_notes=decision_notes,
        )

    def _from_memory_contradiction(
        self,
        candidate: MemoryContradictionCandidate,
    ) -> ReviewQueueItem:
        return _make_item(
            candidate_kind="memory_contradiction",
            candidate_id=candidate.candidate_id,
            source_schema_version=candidate.schema_version,
            owner_user_id=candidate.user_id,
            title="[SYNTHETIC] Review memory contradiction",
            safe_summary=candidate.safe_summary,
            reason_labels=[
                candidate.conflict_type,
                candidate.proposed_resolution,
                *candidate.safety_warnings,
            ],
            source_refs=[*candidate.memory_ids, *candidate.new_evidence_refs],
            priority_score=80 if candidate.safety_warnings else 70,
            candidate_created_at=candidate.created_at,
        )

    def _from_memory_supersession(
        self,
        candidate: MemorySupersessionCandidate,
    ) -> ReviewQueueItem:
        return _make_item(
            candidate_kind="memory_supersession",
            candidate_id=candidate.candidate_id,
            source_schema_version=candidate.schema_version,
            title="[SYNTHETIC] Review memory supersession",
            safe_summary=candidate.reason,
            reason_labels=["supersession_candidate"],
            source_refs=[candidate.source_memory_id, candidate.replacement_memory_id],
            priority_score=75,
            candidate_created_at=candidate.created_at,
        )

    def _from_memory_deletion(self, candidate: MemoryDeletionCascadePlan) -> ReviewQueueItem:
        trigger_priority = 100 if candidate.trigger_type in {"consent_withdrawal", "data_rights_request"} else 90
        return _make_item(
            candidate_kind="memory_deletion_cascade",
            candidate_id=candidate.plan_id,
            source_schema_version=candidate.schema_version,
            owner_user_id=candidate.user_id,
            title="[SYNTHETIC] Review memory deletion cascade",
            safe_summary=f"[SYNTHETIC] Review {candidate.trigger_type} memory cascade.",
            reason_labels=[candidate.trigger_type, *candidate.recommended_actions],
            source_refs=[*candidate.target_memory_ids, *candidate.affected_artifact_refs],
            priority_score=trigger_priority,
            candidate_created_at=candidate.created_at,
        )

    def _from_persona_growth_evidence(
        self,
        candidate: PersonaGrowthEvidenceBundle,
    ) -> ReviewQueueItem:
        score = 70 if candidate.blocked_memory_ids or candidate.safety_warnings else 55
        return _make_item(
            candidate_kind="persona_growth_evidence",
            candidate_id=candidate.bundle_id,
            source_schema_version=candidate.schema_version,
            persona_id=candidate.persona_id,
            title="[SYNTHETIC] Review persona growth evidence",
            safe_summary="[SYNTHETIC] Review memory evidence for persona growth.",
            reason_labels=[
                candidate.evidence_purpose,
                *candidate.exclusion_reasons.values(),
                *candidate.safety_warnings,
            ],
            source_refs=[*candidate.memory_ids, *candidate.blocked_memory_ids],
            priority_score=score,
            candidate_created_at=candidate.created_at,
        )

    def _from_persona_growth_patch(
        self,
        candidate: PersonaGrowthPatchCandidate,
    ) -> ReviewQueueItem:
        score = 85 if candidate.blocking_risk_labels or candidate.clone_similarity_warnings else 60
        return _make_item(
            candidate_kind="persona_growth_patch",
            candidate_id=candidate.patch_id,
            source_schema_version=candidate.schema_version,
            owner_user_id=candidate.user_id,
            persona_id=candidate.persona_id,
            title="[SYNTHETIC] Review persona growth patch",
            safe_summary=candidate.user_facing_explanation,
            reason_labels=[
                candidate.trigger_type,
                candidate.patch_status,
                *candidate.safety_warnings,
                *candidate.clone_similarity_warnings,
                *candidate.blocking_risk_labels,
            ],
            source_refs=[
                *candidate.evidence_memory_ids,
                *candidate.relationship_context_refs,
                *candidate.consent_scope_refs,
            ],
            priority_score=score,
            candidate_created_at=candidate.created_at,
        )

    def _from_distillation_manifest(
        self,
        candidate: SyntheticDistillationInputManifest,
    ) -> ReviewQueueItem:
        source_refs = [
            *(consent.consent_ref_id for consent in candidate.consent_refs),
            *(segment.segment_id for segment in candidate.segments),
            *(redaction.redaction_ref_id for redaction in candidate.redaction_refs),
            candidate.clone_risk_decision.decision_id,
        ]
        score = 90 if candidate.blocking_reasons else 55
        return _make_item(
            candidate_kind="synthetic_distillation_manifest",
            candidate_id=candidate.manifest_id,
            source_schema_version=candidate.schema_version,
            owner_user_id=candidate.user_id,
            title="[SYNTHETIC] Review synthetic distillation input",
            safe_summary="[SYNTHETIC] Review synthetic de-identified style input.",
            reason_labels=[
                candidate.input_mode,
                candidate.target_mode,
                candidate.output_intent,
                *candidate.blocking_reasons,
            ],
            source_refs=source_refs,
            priority_score=score,
            candidate_created_at=candidate.created_at,
        )

    def _from_style_feature(
        self,
        candidate: DeidentifiedStyleFeatureCandidate,
    ) -> ReviewQueueItem:
        score = 80 if candidate.blocked_from_persona_synthesis or candidate.blocking_reasons else 45
        return _make_item(
            candidate_kind="deidentified_style_feature",
            candidate_id=candidate.feature_id,
            source_schema_version=candidate.schema_version,
            title="[SYNTHETIC] Review de-identified style feature",
            safe_summary=candidate.value_summary,
            reason_labels=[
                candidate.feature_family,
                candidate.feature_label,
                *candidate.blocking_reasons,
            ],
            source_refs=[*candidate.evidence_segment_ids, *candidate.source_speaker_aliases],
            priority_score=score,
        )

    def _from_retrieval_result(
        self,
        candidate: MemoryRetrievalExplanationResult,
    ) -> ReviewQueueItem:
        score = 85 if candidate.deletion_cascade_plan else (70 if candidate.bundle.safety_warnings else 40)
        deletion_refs = (
            [candidate.deletion_cascade_plan.plan_id]
            if candidate.deletion_cascade_plan is not None
            else []
        )
        return _make_item(
            candidate_kind="memory_retrieval_explanation",
            candidate_id=candidate.bundle.bundle_id,
            source_schema_version=candidate.schema_version,
            title="[SYNTHETIC] Review retrieval explanation",
            safe_summary=candidate.bundle.query_summary,
            reason_labels=[
                candidate.bundle.purpose,
                *candidate.bundle.exclusion_reasons.values(),
                *candidate.bundle.safety_warnings,
            ],
            source_refs=[
                *candidate.bundle.selected_memory_ids,
                *candidate.bundle.excluded_memory_ids,
                *deletion_refs,
            ],
            priority_score=score,
            candidate_created_at=candidate.bundle.generated_at,
        )


def _make_item(
    *,
    candidate_kind: ReviewCandidateKind,
    candidate_id: str,
    title: str,
    safe_summary: str,
    source_schema_version: str | None = None,
    owner_user_id: str | None = None,
    persona_id: str | None = None,
    reason_labels: Iterable[str] = (),
    source_refs: Iterable[str] = (),
    priority_score: int = 50,
    candidate_created_at: datetime | None = None,
) -> ReviewQueueItem:
    return ReviewQueueItem(
        candidate_kind=candidate_kind,
        candidate_id=candidate_id,
        source_schema_version=source_schema_version,
        owner_user_id=owner_user_id,
        persona_id=persona_id,
        title=title,
        safe_summary=safe_summary,
        reason_labels=_ordered_unique(reason_labels),
        source_refs=_ordered_unique(source_refs),
        priority_score=priority_score,
        candidate_created_at=candidate_created_at,
    )


def _priority_band(score: int) -> ReviewPriorityBand:
    if score >= 90:
        return "critical"
    if score >= 70:
        return "high"
    if score >= 50:
        return "normal"
    return "low"


def _ordered_unique(values: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value and value not in seen:
            seen.add(value)
            result.append(value)
    return result
