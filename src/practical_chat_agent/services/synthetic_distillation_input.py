"""Synthetic-only distillation input candidate records.

These records model de-identified style inspiration inputs. They do not read
private logs, call providers, compute embeddings, synthesize personas, generate
media, or connect to outbound/platform delivery.
"""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from practical_chat_agent.core.ids import new_id
from practical_chat_agent.core.models import DistillationSensitivity, utc_now


SyntheticInputMode = Literal[
    "synthetic_style_notes",
    "synthetic_chat_segments",
    "synthetic_mixed_fixture",
]
SyntheticTargetMode = Literal["deidentified_style_inspiration"]
SyntheticOutputIntent = Literal["new_fictional_persona"]
SyntheticSourceCategory = Literal["synthetic", "blocked_real_person_request", "user_supplied_future"]
SyntheticSegmentKind = Literal["message", "style_note", "system_event", "review_note"]
SyntheticSpeakerRole = Literal["user_self", "style_subject", "third_party", "system"]
SyntheticModality = Literal["text"]
DistillationFeatureScope = Literal[
    "persona_distillation",
    "memory",
    "aigc_export_share",
    "voice_avatar",
    "model_improvement",
]
DistillationActorType = Literal["user", "guardian", "reviewer", "system"]
StyleFeatureFamily = Literal[
    "tone",
    "length",
    "directness",
    "humor",
    "latency",
    "comfort",
    "conflict",
    "boundary",
    "topic_preference",
]
CloneRiskLevel = Literal["low", "medium", "high", "blocked"]
CloneRiskDecisionAction = Literal["allow_l2_review", "needs_review", "block"]

_HIGH_RISK_FLAGS = frozenset(
    {
        "voice_biometric",
        "face_biometric",
        "image_biometric",
        "real_person_avatar",
        "clone_intent",
        "hidden_impersonation",
        "public_figure",
        "ex_partner",
        "family_member",
        "deceased_person",
        "minor_risk",
        "withdrawn_consent",
    }
)
_MEDIUM_RISK_FLAGS = frozenset(
    {
        "direct_identifier",
        "contact_identifier",
        "location_identifier",
        "org_school_identifier",
        "handle_identifier",
        "exact_biography",
        "private_event",
        "distinctive_catchphrase",
        "third_party_unminimized",
    }
)
_FORBIDDEN_TEXT_MARKERS = (
    "private/chat_history",
    "private\\chat_history",
    "private/distilled",
    "private\\distilled",
    "voice sample",
    "audio sample",
    "face image",
    "photo attached",
    "video attached",
)
_FORBIDDEN_FEATURE_LABEL_MARKERS = (
    '"',
    "'",
    "real name",
    "exact phrase",
    "private event",
    "voice",
    "face",
    "avatar",
    "account",
)


class _SyntheticDistillationRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")


class SyntheticSpeakerAlias(_SyntheticDistillationRecord):
    schema_version: str = "synthetic_speaker_alias_v1"
    speaker_alias: str = Field(..., min_length=1)
    speaker_role: SyntheticSpeakerRole
    is_target_style_subject: bool = False
    real_identity_retained: bool = False
    third_party_minimized: bool = False
    consent_ref_ids: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_alias_boundary(self) -> "SyntheticSpeakerAlias":
        if self.real_identity_retained:
            raise ValueError("speaker aliases must not retain real identity")
        if self.speaker_role == "third_party":
            self.third_party_minimized = True
            if self.is_target_style_subject:
                raise ValueError("third parties cannot be target style subjects by default")
        return self


class DistillationConsentRef(_SyntheticDistillationRecord):
    schema_version: str = "distillation_consent_ref_v1"
    consent_ref_id: str = Field(default_factory=lambda: new_id("sdconsent"))
    feature_scope: DistillationFeatureScope
    policy_version: str = Field(..., min_length=1)
    actor_type: DistillationActorType
    granted: bool = False
    withdrawn: bool = False
    evidence_ref: str = Field(..., min_length=1)

    @model_validator(mode="after")
    def validate_consent_scope(self) -> "DistillationConsentRef":
        if self.feature_scope == "voice_avatar" and self.granted:
            raise ValueError("voice_avatar consent cannot be granted in synthetic text distillation scope")
        if self.withdrawn and self.granted:
            raise ValueError("withdrawn consent cannot remain granted")
        return self


class SyntheticDistillationSourceSegment(_SyntheticDistillationRecord):
    schema_version: str = "synthetic_distillation_source_segment_v1"
    segment_id: str = Field(default_factory=lambda: new_id("sdseg"))
    speaker_alias: str = Field(..., min_length=1)
    segment_kind: SyntheticSegmentKind
    synthetic_text: str = Field(..., min_length=1)
    source_ref: str = Field(..., min_length=1)
    contains_raw_private_text: bool = False
    modality: SyntheticModality = "text"
    sensitivity: DistillationSensitivity = "low"
    redaction_labels: list[str] = Field(default_factory=list)
    allowed_feature_families: list[StyleFeatureFamily] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_synthetic_segment(self) -> "SyntheticDistillationSourceSegment":
        if "[SYNTHETIC]" not in self.synthetic_text:
            raise ValueError("synthetic source segments must include [SYNTHETIC]")
        if self.contains_raw_private_text:
            raise ValueError("synthetic source segments cannot contain raw private text")
        lowered = self.synthetic_text.lower()
        if any(marker in lowered for marker in _FORBIDDEN_TEXT_MARKERS):
            raise ValueError("synthetic source segment contains forbidden private or media reference")
        self.redaction_labels = _ordered_unique(self.redaction_labels)
        self.allowed_feature_families = _ordered_unique(self.allowed_feature_families)
        return self


class DistillationRedactionRef(_SyntheticDistillationRecord):
    schema_version: str = "distillation_redaction_ref_v1"
    redaction_ref_id: str = Field(default_factory=lambda: new_id("sdredact"))
    segment_id: str = Field(..., min_length=1)
    redaction_labels: list[str] = Field(default_factory=list)
    safe_to_use_for_style: bool = True
    blocked_reason: str | None = None

    @model_validator(mode="after")
    def validate_redaction_ref(self) -> "DistillationRedactionRef":
        if not self.safe_to_use_for_style and not self.blocked_reason:
            raise ValueError("unsafe redaction refs require blocked_reason")
        self.redaction_labels = _ordered_unique(self.redaction_labels)
        return self


class CloneRiskDecision(_SyntheticDistillationRecord):
    schema_version: str = "clone_risk_decision_v1"
    decision_id: str = Field(default_factory=lambda: new_id("sdclone"))
    manifest_id: str = Field(..., min_length=1)
    risk_level: CloneRiskLevel
    risk_flags: list[str] = Field(default_factory=list)
    decision: CloneRiskDecisionAction
    safe_transformation_allowed: bool = False
    blocked_reason: str | None = None
    review_required: bool = True

    @classmethod
    def from_flags(
        cls,
        *,
        manifest_id: str,
        risk_flags: list[str],
    ) -> "CloneRiskDecision":
        unique_flags = _ordered_unique(risk_flags)
        high_risk = _HIGH_RISK_FLAGS.intersection(unique_flags)
        medium_risk = _MEDIUM_RISK_FLAGS.intersection(unique_flags)
        if high_risk:
            return cls(
                manifest_id=manifest_id,
                risk_level="blocked",
                risk_flags=unique_flags,
                decision="block",
                safe_transformation_allowed=False,
                blocked_reason="blocked_clone_or_likeness_risk",
            )
        if medium_risk:
            return cls(
                manifest_id=manifest_id,
                risk_level="medium",
                risk_flags=unique_flags,
                decision="needs_review",
                safe_transformation_allowed=False,
                blocked_reason="identifier_or_third_party_review_required",
            )
        return cls(
            manifest_id=manifest_id,
            risk_level="low",
            risk_flags=unique_flags,
            decision="allow_l2_review",
            safe_transformation_allowed=True,
        )

    @model_validator(mode="after")
    def validate_decision(self) -> "CloneRiskDecision":
        if not self.review_required:
            raise ValueError("clone-risk decisions are always review-required")
        if self.decision == "block" and self.safe_transformation_allowed:
            raise ValueError("blocked clone-risk decisions cannot allow safe transformation")
        self.risk_flags = _ordered_unique(self.risk_flags)
        return self


class DeidentifiedStyleFeatureCandidate(_SyntheticDistillationRecord):
    schema_version: str = "deidentified_style_feature_candidate_v1"
    feature_id: str = Field(default_factory=lambda: new_id("sdfeat"))
    manifest_id: str = Field(..., min_length=1)
    feature_family: StyleFeatureFamily
    feature_label: str = Field(..., min_length=1)
    value_summary: str = Field(..., min_length=1)
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    evidence_segment_ids: list[str] = Field(default_factory=list)
    source_speaker_aliases: list[str] = Field(default_factory=list)
    source_text_retained: bool = False
    review_required: bool = True
    blocked_from_persona_synthesis: bool = False
    blocking_reasons: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_abstract_feature(self) -> "DeidentifiedStyleFeatureCandidate":
        if self.source_text_retained:
            raise ValueError("style features must not retain source text")
        if not self.review_required:
            raise ValueError("style features are always review-required")
        lowered_label = self.feature_label.lower()
        if any(marker in lowered_label for marker in _FORBIDDEN_FEATURE_LABEL_MARKERS):
            raise ValueError("style feature labels must be abstract and non-identifying")
        self.evidence_segment_ids = _ordered_unique(self.evidence_segment_ids)
        self.source_speaker_aliases = _ordered_unique(self.source_speaker_aliases)
        self.blocking_reasons = _ordered_unique(self.blocking_reasons)
        return self


class FictionalPersonaSynthesisInput(_SyntheticDistillationRecord):
    schema_version: str = "fictional_persona_synthesis_input_v1"
    input_id: str = Field(default_factory=lambda: new_id("sdpinput"))
    manifest_id: str = Field(..., min_length=1)
    style_feature_ids: list[str] = Field(default_factory=list)
    required_disclosures: list[str] = Field(
        default_factory=lambda: ["ai_generated", "fictional", "deidentified"],
    )
    must_not_include: list[str] = Field(
        default_factory=lambda: [
            "names",
            "faces",
            "voices",
            "biography",
            "exact_phrases",
            "private_events",
            "source_identity",
        ],
    )
    review_required: bool = True
    runtime_ready: bool = False

    @model_validator(mode="after")
    def validate_fictional_input(self) -> "FictionalPersonaSynthesisInput":
        if not self.review_required:
            raise ValueError("fictional persona synthesis inputs are review-required")
        if self.runtime_ready:
            raise ValueError("fictional persona synthesis inputs are never runtime-ready")
        self.required_disclosures = _ordered_unique(self.required_disclosures)
        self.must_not_include = _ordered_unique(self.must_not_include)
        return self


class SyntheticDistillationInputManifest(_SyntheticDistillationRecord):
    schema_version: str = "synthetic_distillation_input_manifest_v1"
    manifest_id: str = Field(default_factory=lambda: new_id("sdmanifest"))
    user_id: str = Field(..., min_length=1)
    input_mode: SyntheticInputMode
    target_mode: SyntheticTargetMode = "deidentified_style_inspiration"
    output_intent: SyntheticOutputIntent = "new_fictional_persona"
    source_category: SyntheticSourceCategory = "synthetic"
    consent_refs: list[DistillationConsentRef] = Field(default_factory=list)
    speaker_map: list[SyntheticSpeakerAlias] = Field(default_factory=list)
    segments: list[SyntheticDistillationSourceSegment] = Field(default_factory=list)
    redaction_refs: list[DistillationRedactionRef] = Field(default_factory=list)
    clone_risk_decision: CloneRiskDecision
    review_required: bool = True
    blocking_reasons: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=utc_now)

    @model_validator(mode="after")
    def validate_manifest(self) -> "SyntheticDistillationInputManifest":
        if self.source_category == "user_supplied_future":
            raise ValueError("user_supplied_future is not runtime-allowed in synthetic fixtures")
        if not self.review_required:
            raise ValueError("synthetic distillation manifests are always review-required")

        blocking_reasons = list(self.blocking_reasons)
        persona_distillation_consents = [
            consent
            for consent in self.consent_refs
            if consent.feature_scope == "persona_distillation"
        ]
        if not persona_distillation_consents or not any(
            consent.granted and not consent.withdrawn for consent in persona_distillation_consents
        ):
            blocking_reasons.append("persona_distillation_consent_missing_or_withdrawn")
        if any(consent.withdrawn for consent in self.consent_refs):
            blocking_reasons.append("withdrawn_consent")
        if not self.clone_risk_decision.safe_transformation_allowed:
            blocking_reasons.append("clone_risk_blocked")
        if any(
            alias.speaker_role == "third_party" and not alias.third_party_minimized
            for alias in self.speaker_map
        ):
            blocking_reasons.append("third_party_unminimized")

        self.blocking_reasons = _ordered_unique(blocking_reasons)
        return self

    def is_feature_extraction_allowed(self) -> bool:
        return not self.blocking_reasons and self.clone_risk_decision.safe_transformation_allowed


def _ordered_unique(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return result
