"""Review-first persona growth candidate records.

The records in this module model bounded persona growth proposals. They do not
mutate PersonaCard objects, write version stores, call providers, generate
dialogue, send messages, or connect to platform delivery.
"""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from practical_chat_agent.core.ids import new_id
from practical_chat_agent.core.models import PersonaCard, utc_now
from practical_chat_agent.services.memory_governance import PersonaGrowthEvidenceBundle


PersonaGrowthTriggerType = Literal[
    "user_preference",
    "user_correction",
    "memory_pattern",
    "relationship_signal",
    "reviewer_note",
    "manual_edit",
]
PersonaGrowthPatchStatus = Literal[
    "candidate",
    "approved_for_manual_apply",
    "rejected",
    "frozen",
    "needs_changes",
    "applied",
    "superseded",
    "archived",
]
PersonaGrowthReviewDecision = Literal[
    "approve_for_manual_apply",
    "reject",
    "freeze",
    "request_changes",
]

_GLOBAL_SINGLE_TRAIT_DELTA_CAP = 0.2
_FROZEN_FIELD_PREFIXES = (
    "schema_version",
    "persona_id",
    "user_id",
    "truth_disclosure",
    "source_policy",
    "identity",
    "safety_policy",
    "proactive_preferences.default_enabled",
)
_MUTABLE_FIELD_PATHS = frozenset(
    {
        "core_traits.warmth",
        "core_traits.directness",
        "core_traits.humor",
        "core_traits.independence",
        "core_traits.emotional_stability",
        "core_traits.jealousy",
        "speech_style.sentence_length",
        "speech_style.emoji_frequency",
        "speech_style.punctuation_style",
        "speech_style.humor_type",
        "speech_style.pet_names",
        "speech_style.taboo_phrases",
        "emotion_model.baseline_mood",
        "emotion_model.stress_response",
        "emotion_model.comforting_style",
        "emotion_model.conflict_style",
        "relationship_model.trust_growth_rate",
        "relationship_model.intimacy_growth_rate",
        "relationship_model.boundary_sensitivity",
        "virtual_history.daily_routine",
        "virtual_history.current_goals",
        "virtual_history.virtual_social_circle",
    }
)
_BLOCKING_RISK_LABELS = frozenset(
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


class _PersonaGrowthRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")


class PersonaGrowthFieldChange(_PersonaGrowthRecord):
    schema_version: str = "persona_growth_field_change_v1"
    field_path: str = Field(..., min_length=1)
    old_value_summary: str = Field(..., min_length=1)
    proposed_value_summary: str = Field(..., min_length=1)
    numeric_delta: float | None = None
    change_reason: str = Field(..., min_length=1)
    source_memory_ids: list[str] = Field(default_factory=list)
    source_review_refs: list[str] = Field(default_factory=list)
    risk_labels: list[str] = Field(default_factory=list)
    requires_user_review: bool = True
    blocks_approval: bool = False

    @model_validator(mode="after")
    def validate_growth_field(self) -> "PersonaGrowthFieldChange":
        field_path = self.field_path.strip()
        if _is_frozen_field(field_path):
            raise ValueError("persona growth cannot change frozen or identity/safety fields")
        if field_path not in _MUTABLE_FIELD_PATHS:
            raise ValueError("persona growth field_path is not in the mutable field set")
        if self.numeric_delta is not None:
            if abs(self.numeric_delta) > _GLOBAL_SINGLE_TRAIT_DELTA_CAP:
                raise ValueError("numeric_delta exceeds global single-trait cap")
            if field_path == "core_traits.jealousy" and self.numeric_delta > 0:
                raise ValueError("core_traits.jealousy cannot increase by default")

        self.field_path = field_path
        self.risk_labels = _ordered_unique(self.risk_labels)
        self.requires_user_review = True
        self.blocks_approval = bool(_BLOCKING_RISK_LABELS.intersection(self.risk_labels))
        return self


class PersonaGrowthPatchCandidate(_PersonaGrowthRecord):
    schema_version: str = "persona_growth_patch_candidate_v1"
    patch_id: str = Field(default_factory=lambda: new_id("pgpatch"))
    user_id: str = Field(..., min_length=1)
    persona_id: str = Field(..., min_length=1)
    source_persona_version: int = Field(..., ge=1)
    trigger_type: PersonaGrowthTriggerType
    trigger_summary: str = Field(..., min_length=1)
    changes: list[PersonaGrowthFieldChange] = Field(..., min_length=1)
    evidence_memory_ids: list[str] = Field(default_factory=list)
    relationship_context_refs: list[str] = Field(default_factory=list)
    consent_scope_refs: list[str] = Field(default_factory=list)
    user_facing_explanation: str = Field(..., min_length=1)
    safety_warnings: list[str] = Field(default_factory=list)
    clone_similarity_warnings: list[str] = Field(default_factory=list)
    patch_status: PersonaGrowthPatchStatus = "candidate"
    review_required: bool = True
    auto_apply_allowed: bool = False
    writes_persona_version: bool = False
    blocking_risk_labels: list[str] = Field(default_factory=list)
    weekly_trait_delta_by_field: dict[str, float] = Field(default_factory=dict)
    max_weekly_trait_delta: float = Field(default=_GLOBAL_SINGLE_TRAIT_DELTA_CAP, ge=0.0, le=0.2)
    created_at: datetime = Field(default_factory=utc_now)

    @classmethod
    def from_persona_card(
        cls,
        persona: PersonaCard,
        *,
        trigger_type: PersonaGrowthTriggerType,
        trigger_summary: str,
        changes: list[PersonaGrowthFieldChange],
        user_facing_explanation: str,
        evidence_bundle: PersonaGrowthEvidenceBundle | None = None,
        relationship_context_refs: list[str] | None = None,
        consent_scope_refs: list[str] | None = None,
        safety_warnings: list[str] | None = None,
        clone_similarity_warnings: list[str] | None = None,
        weekly_trait_delta_by_field: dict[str, float] | None = None,
        patch_status: PersonaGrowthPatchStatus = "candidate",
    ) -> "PersonaGrowthPatchCandidate":
        evidence_memory_ids = list(evidence_bundle.memory_ids) if evidence_bundle else []
        bundle_warnings = list(evidence_bundle.safety_warnings) if evidence_bundle else []
        for change in changes:
            evidence_memory_ids.extend(change.source_memory_ids)

        return cls(
            user_id=persona.user_id,
            persona_id=persona.persona_id,
            source_persona_version=persona.version,
            trigger_type=trigger_type,
            trigger_summary=trigger_summary,
            changes=changes,
            evidence_memory_ids=_ordered_unique(evidence_memory_ids),
            relationship_context_refs=list(relationship_context_refs or []),
            consent_scope_refs=list(consent_scope_refs or []),
            user_facing_explanation=user_facing_explanation,
            safety_warnings=_ordered_unique([*bundle_warnings, *(safety_warnings or [])]),
            clone_similarity_warnings=_ordered_unique(clone_similarity_warnings or []),
            weekly_trait_delta_by_field=dict(weekly_trait_delta_by_field or {}),
            max_weekly_trait_delta=persona.growth_policy.max_weekly_trait_delta,
            patch_status=patch_status,
        )

    @model_validator(mode="after")
    def validate_patch_candidate(self) -> "PersonaGrowthPatchCandidate":
        if not self.review_required:
            raise ValueError("persona growth patches are always review-required")
        if self.auto_apply_allowed:
            raise ValueError("persona growth patches cannot auto-apply")
        if self.writes_persona_version:
            raise ValueError("persona growth patch candidates must not write persona versions")

        blocking_labels: list[str] = list(self.blocking_risk_labels)
        for change in self.changes:
            if change.blocks_approval:
                blocking_labels.extend(
                    label for label in change.risk_labels if label in _BLOCKING_RISK_LABELS
                )
            if change.numeric_delta is not None:
                used_delta = abs(self.weekly_trait_delta_by_field.get(change.field_path, 0.0))
                next_delta = used_delta + abs(change.numeric_delta)
                if next_delta > self.max_weekly_trait_delta:
                    raise ValueError("weekly trait movement exceeds persona growth policy cap")
        blocking_labels.extend(
            label for label in self.clone_similarity_warnings if label in _BLOCKING_RISK_LABELS
        )

        self.evidence_memory_ids = _ordered_unique(self.evidence_memory_ids)
        self.safety_warnings = _ordered_unique(self.safety_warnings)
        self.clone_similarity_warnings = _ordered_unique(self.clone_similarity_warnings)
        self.blocking_risk_labels = _ordered_unique(blocking_labels)
        return self


class PersonaGrowthPatchReview(_PersonaGrowthRecord):
    schema_version: str = "persona_growth_patch_review_v1"
    review_id: str = Field(default_factory=lambda: new_id("pgreview"))
    patch_id: str = Field(..., min_length=1)
    reviewer_id: str = Field(..., min_length=1)
    decision: PersonaGrowthReviewDecision
    decision_notes: list[str] = Field(default_factory=list)
    blocking_risk_labels: list[str] = Field(default_factory=list)
    approved_field_paths: list[str] = Field(default_factory=list)
    rejected_field_paths: list[str] = Field(default_factory=list)
    auto_apply_allowed: bool = False
    writes_persona_version: bool = False
    reviewed_at: datetime = Field(default_factory=utc_now)

    @classmethod
    def from_patch(
        cls,
        patch: PersonaGrowthPatchCandidate,
        *,
        reviewer_id: str,
        decision: PersonaGrowthReviewDecision,
        decision_notes: list[str] | None = None,
    ) -> "PersonaGrowthPatchReview":
        field_paths = [change.field_path for change in patch.changes]
        return cls(
            patch_id=patch.patch_id,
            reviewer_id=reviewer_id,
            decision=decision,
            decision_notes=list(decision_notes or []),
            blocking_risk_labels=list(patch.blocking_risk_labels),
            approved_field_paths=field_paths if decision == "approve_for_manual_apply" else [],
            rejected_field_paths=field_paths if decision == "reject" else [],
        )

    @model_validator(mode="after")
    def validate_review_record(self) -> "PersonaGrowthPatchReview":
        if self.auto_apply_allowed:
            raise ValueError("persona growth reviews cannot allow auto-apply")
        if self.writes_persona_version:
            raise ValueError("persona growth reviews must not write persona versions")
        self.blocking_risk_labels = _ordered_unique(self.blocking_risk_labels)
        if self.decision == "approve_for_manual_apply" and self.blocking_risk_labels:
            raise ValueError("blocking risk labels cannot be approved for manual apply")
        return self


class PersonaGrowthJournalEntry(_PersonaGrowthRecord):
    schema_version: str = "persona_growth_journal_entry_v1"
    journal_id: str = Field(default_factory=lambda: new_id("pgjournal"))
    persona_id: str = Field(..., min_length=1)
    source_patch_id: str = Field(..., min_length=1)
    source_version_id: str = Field(..., min_length=1)
    summary: str = Field(..., min_length=1)
    changed_field_paths: list[str] = Field(default_factory=list)
    safety_warnings: list[str] = Field(default_factory=list)
    writes_persona_version: bool = False
    created_at: datetime = Field(default_factory=utc_now)

    @model_validator(mode="after")
    def validate_journal_record(self) -> "PersonaGrowthJournalEntry":
        if self.writes_persona_version:
            raise ValueError("growth journal entries must not write persona versions")
        self.changed_field_paths = _ordered_unique(self.changed_field_paths)
        self.safety_warnings = _ordered_unique(self.safety_warnings)
        return self


def _is_frozen_field(field_path: str) -> bool:
    return any(
        field_path == frozen or field_path.startswith(f"{frozen}.")
        for frozen in _FROZEN_FIELD_PREFIXES
    )


def _ordered_unique(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return result
