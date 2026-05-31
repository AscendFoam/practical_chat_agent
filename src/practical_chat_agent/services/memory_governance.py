"""Review-first memory governance candidate records.

The models in this module are local, deterministic, and synthetic-friendly.
They do not mutate memory stores, call providers, rank retrieval, generate
dialogue, send messages, or connect to platform delivery.
"""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from practical_chat_agent.core.ids import new_id
from practical_chat_agent.core.models import MemoryEvent, MemoryTruthStatus, utc_now


MemoryConflictType = Literal[
    "fact_conflict",
    "preference_change",
    "relationship_change",
    "source_dispute",
    "imagined_fact_boundary",
]
MemoryResolution = Literal[
    "keep_both",
    "supersede_old",
    "archive_old",
    "request_clarification",
    "reject_new",
]
MemoryDeletionTrigger = Literal[
    "user_delete",
    "consent_withdrawal",
    "data_rights_request",
    "safety_block",
]
MemoryDeletionAction = Literal[
    "delete",
    "freeze",
    "archive",
    "suppress_retrieval",
    "training_exclusion",
]
MemoryExplanationSurface = Literal[
    "viewer",
    "chat_review",
    "retrieval_bundle",
    "persona_growth_patch",
    "distillation_review",
]
PersonaGrowthEvidencePurpose = Literal[
    "factual_persona_growth",
    "virtual_continuity_growth",
    "review_only",
]

_BLOCKING_PERSONA_GROWTH_WARNINGS = frozenset(
    {
        "dependency_language",
        "relationship_replacement_risk",
        "crisis_safety_review_required",
        "exclusive_attachment",
        "isolation_prompt",
        "guilt_based_retention",
        "paid_intimacy_escalation",
        "real_person_similarity",
        "public_figure_similarity",
        "ex_partner_similarity",
        "family_member_similarity",
        "deceased_person_similarity",
        "minor_risk",
        "voice_likeness",
        "avatar_likeness",
        "unsafe_content",
    }
)


class _GovernanceRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")


class MemoryContradictionCandidate(_GovernanceRecord):
    schema_version: str = "memory_contradiction_candidate_v1"
    candidate_id: str = Field(default_factory=lambda: new_id("memctr"))
    user_id: str = Field(..., min_length=1)
    memory_ids: list[str] = Field(..., min_length=2)
    new_evidence_refs: list[str] = Field(default_factory=list)
    conflict_type: MemoryConflictType
    safe_summary: str = Field(..., min_length=1)
    proposed_resolution: MemoryResolution
    review_required: bool = True
    safety_warnings: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=utc_now)

    @classmethod
    def from_events(
        cls,
        events: list[MemoryEvent],
        *,
        new_evidence_refs: list[str] | None = None,
        conflict_type: MemoryConflictType,
        safe_summary: str,
        proposed_resolution: MemoryResolution,
        safety_warnings: list[str] | None = None,
    ) -> "MemoryContradictionCandidate":
        if not events:
            raise ValueError("contradiction candidates require memory events")
        return cls(
            user_id=events[0].user_id,
            memory_ids=[event.event_id for event in events],
            new_evidence_refs=list(new_evidence_refs or []),
            conflict_type=conflict_type,
            safe_summary=safe_summary,
            proposed_resolution=proposed_resolution,
            safety_warnings=_ordered_unique(safety_warnings or []),
        )

    @model_validator(mode="after")
    def validate_review_gate(self) -> "MemoryContradictionCandidate":
        if not self.review_required:
            raise ValueError("contradiction candidates are always review-required")
        return self


class MemorySupersessionCandidate(_GovernanceRecord):
    schema_version: str = "memory_supersession_candidate_v1"
    candidate_id: str = Field(default_factory=lambda: new_id("memsup"))
    source_memory_id: str = Field(..., min_length=1)
    replacement_memory_id: str = Field(..., min_length=1)
    reason: str = Field(..., min_length=1)
    review_required: bool = True
    applies_lifecycle_update: bool = False
    created_at: datetime = Field(default_factory=utc_now)

    @classmethod
    def from_memory_ids(
        cls,
        *,
        source_memory_id: str,
        replacement_memory_id: str,
        reason: str,
    ) -> "MemorySupersessionCandidate":
        return cls(
            source_memory_id=source_memory_id,
            replacement_memory_id=replacement_memory_id,
            reason=reason,
        )

    @model_validator(mode="after")
    def validate_no_direct_apply(self) -> "MemorySupersessionCandidate":
        if not self.review_required:
            raise ValueError("supersession candidates are always review-required")
        if self.applies_lifecycle_update:
            raise ValueError("supersession candidates must not apply lifecycle updates")
        return self


class MemoryDeletionCascadePlan(_GovernanceRecord):
    schema_version: str = "memory_deletion_cascade_plan_v1"
    plan_id: str = Field(default_factory=lambda: new_id("memdel"))
    user_id: str = Field(..., min_length=1)
    trigger_type: MemoryDeletionTrigger
    target_memory_ids: list[str] = Field(..., min_length=1)
    affected_artifact_refs: list[str] = Field(default_factory=list)
    recommended_actions: list[MemoryDeletionAction] = Field(default_factory=list)
    review_required: bool = True
    completed: bool = False
    created_at: datetime = Field(default_factory=utc_now)

    @classmethod
    def for_consent_withdrawal(
        cls,
        *,
        user_id: str,
        target_memory_ids: list[str],
        affected_artifact_refs: list[str] | None = None,
    ) -> "MemoryDeletionCascadePlan":
        return cls(
            user_id=user_id,
            trigger_type="consent_withdrawal",
            target_memory_ids=target_memory_ids,
            affected_artifact_refs=list(affected_artifact_refs or []),
            recommended_actions=["suppress_retrieval", "training_exclusion"],
        )

    @model_validator(mode="after")
    def validate_candidate_state(self) -> "MemoryDeletionCascadePlan":
        if not self.review_required:
            raise ValueError("deletion cascade plans are always review-required")
        if self.completed:
            raise ValueError("deletion cascade plans are candidates and cannot be completed")
        self.recommended_actions = _ordered_unique(self.recommended_actions)
        return self


class MemoryExplanationTrace(_GovernanceRecord):
    schema_version: str = "memory_explanation_trace_v1"
    trace_id: str = Field(default_factory=lambda: new_id("memxpl"))
    memory_id: str = Field(..., min_length=1)
    surface: MemoryExplanationSurface
    included: bool
    reason: str = Field(..., min_length=1)
    provenance_refs: list[str] = Field(default_factory=list)
    truth_status: MemoryTruthStatus
    safety_warnings: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=utc_now)

    @classmethod
    def included_from_event(
        cls,
        event: MemoryEvent,
        *,
        surface: MemoryExplanationSurface,
        reason: str,
        safety_warnings: list[str] | None = None,
    ) -> "MemoryExplanationTrace":
        return cls._from_event(
            event,
            surface=surface,
            included=True,
            reason=reason,
            safety_warnings=safety_warnings,
        )

    @classmethod
    def excluded_from_event(
        cls,
        event: MemoryEvent,
        *,
        surface: MemoryExplanationSurface,
        reason: str,
        safety_warnings: list[str] | None = None,
    ) -> "MemoryExplanationTrace":
        return cls._from_event(
            event,
            surface=surface,
            included=False,
            reason=reason,
            safety_warnings=safety_warnings,
        )

    @classmethod
    def _from_event(
        cls,
        event: MemoryEvent,
        *,
        surface: MemoryExplanationSurface,
        included: bool,
        reason: str,
        safety_warnings: list[str] | None,
    ) -> "MemoryExplanationTrace":
        return cls(
            memory_id=event.event_id,
            surface=surface,
            included=included,
            reason=reason,
            provenance_refs=_memory_provenance_refs(event),
            truth_status=event.truth_status,
            safety_warnings=_ordered_unique(safety_warnings or []),
        )


class PersonaGrowthEvidenceBundle(_GovernanceRecord):
    schema_version: str = "persona_growth_evidence_bundle_v1"
    bundle_id: str = Field(default_factory=lambda: new_id("pgeb"))
    persona_id: str = Field(..., min_length=1)
    evidence_purpose: PersonaGrowthEvidencePurpose = "factual_persona_growth"
    memory_ids: list[str] = Field(default_factory=list)
    safe_summaries: dict[str, str] = Field(default_factory=dict)
    blocked_memory_ids: list[str] = Field(default_factory=list)
    exclusion_reasons: dict[str, str] = Field(default_factory=dict)
    review_required: bool = True
    safety_warnings: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=utc_now)

    @classmethod
    def from_events(
        cls,
        *,
        persona_id: str,
        events: list[MemoryEvent],
        evidence_purpose: PersonaGrowthEvidencePurpose = "factual_persona_growth",
        safety_warnings_by_memory_id: dict[str, list[str]] | None = None,
    ) -> "PersonaGrowthEvidenceBundle":
        warnings_by_memory_id = safety_warnings_by_memory_id or {}
        memory_ids: list[str] = []
        safe_summaries: dict[str, str] = {}
        blocked_memory_ids: list[str] = []
        exclusion_reasons: dict[str, str] = {}
        collected_warnings: list[str] = []

        for event in events:
            warnings = warnings_by_memory_id.get(event.event_id, [])
            collected_warnings.extend(warnings)
            blocking_warnings = _BLOCKING_PERSONA_GROWTH_WARNINGS.intersection(warnings)

            if blocking_warnings:
                blocked_memory_ids.append(event.event_id)
                exclusion_reasons[event.event_id] = "blocking_safety_warning"
                continue

            if evidence_purpose == "factual_persona_growth" and event.event_type == "imagined":
                blocked_memory_ids.append(event.event_id)
                exclusion_reasons[event.event_id] = "imagined_memory_not_valid_for_factual_growth"
                continue

            if event.lifecycle_state != "active":
                blocked_memory_ids.append(event.event_id)
                exclusion_reasons[event.event_id] = "inactive_memory_not_valid_for_growth"
                continue

            if event.retrieval_permission.review_required:
                blocked_memory_ids.append(event.event_id)
                exclusion_reasons[event.event_id] = "review_required_memory"
                continue

            memory_ids.append(event.event_id)
            safe_summaries[event.event_id] = event.summary

        return cls(
            persona_id=persona_id,
            evidence_purpose=evidence_purpose,
            memory_ids=memory_ids,
            safe_summaries=safe_summaries,
            blocked_memory_ids=blocked_memory_ids,
            exclusion_reasons=exclusion_reasons,
            safety_warnings=_ordered_unique(collected_warnings),
        )

    @model_validator(mode="after")
    def validate_review_gate(self) -> "PersonaGrowthEvidenceBundle":
        if not self.review_required:
            raise ValueError("persona growth evidence bundles are always review-required")
        return self


def _memory_provenance_refs(event: MemoryEvent) -> list[str]:
    return _ordered_unique(
        [
            *event.provenance.evidence_refs,
            *event.provenance.source_event_ids,
            *event.provenance.source_memory_ids,
            *event.provenance.source_persona_ids,
        ],
    )


def _ordered_unique(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return result
