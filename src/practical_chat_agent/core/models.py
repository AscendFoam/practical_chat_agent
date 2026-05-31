from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Literal

from pydantic import BaseModel, Field, field_validator, model_validator

from practical_chat_agent.core.enums import (
    ActionKind,
    ActionStatus,
    ChannelType,
    ChatIntent,
    ContentType,
    Direction,
    MeetingExportTemplate,
    MeetingAudioSource,
    MemoryScope,
    MemoryType,
    PersonaType,
    Platform,
    SafetyMode,
    SourceType,
)
from practical_chat_agent.core.ids import new_id


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


DistillationStatus = Literal["candidate", "approved", "rejected", "frozen", "archived"]
DistillationReviewState = Literal["pending_human_review", "reviewed", "unknown"]
DistillationSensitivity = Literal["low", "medium", "high"]
DistillationEvidenceValidationStatus = Literal["not_run", "passed", "failed", "partial"]
DistillationMemoryType = Literal["semantic", "episodic", "relationship", "procedural", "reflection"]
MemoryEventType = Literal["factual", "inferred", "relational", "procedural", "imagined"]
MemoryTruthStatus = Literal[
    "evidence_backed",
    "inferred",
    "relationship_state",
    "procedural_preference",
    "imagined",
]
MemoryProvenanceSourceType = Literal[
    "conversation",
    "persona_card",
    "user_edit",
    "system_generated",
    "imagined_generation",
    "synthetic_test",
]
MemoryLifecycleState = Literal["active", "frozen", "deleted", "superseded", "archived"]
MemoryRetrievalContext = Literal["factual", "inferred", "relational", "procedural", "imagined"]
MemoryRetrievalPurpose = Literal[
    "factual_response",
    "inferred_context",
    "relationship_context",
    "procedural_context",
    "imagined_context",
    "review_surface",
]
ContactRelationshipType = Literal["friend", "classmate", "colleague", "family", "unknown"]
ApprovedStoreContextStatus = Literal[
    "not_configured",
    "store_path_missing",
    "validation_report_missing",
    "no_runtime_ready_records",
    "loaded",
]
ReplyPlanMode = Literal["candidate_review_only"]
ReplyPlanContextRefType = Literal[
    "approved_contact_skill_record",
    "approved_memory_fact_record",
    "approved_store_evidence_ref",
    "recent_event",
    "memory_hit",
    "policy_boundary",
]
AgentAvailabilityState = Literal["unknown", "available", "busy", "offline"]
BehaviorActionType = Literal[
    "relationship_check_in_draft",
    "reply_follow_up_draft",
    "topic_suggestion",
    "boundary_review_note",
    "memory_review_prompt",
    "do_nothing",
]
BehaviorPolicyMode = Literal["draft_only_review_required"]
CandidateActionMode = Literal["draft_only_review_required"]
OutboundMessageChannel = Literal["unspecified", "feishu", "wechat"]
OutboundRequestSourceType = Literal["candidate_action", "human_authored"]
OutboundHumanApprovalState = Literal["pending_human_approval", "approved", "rejected"]
OutboundSendGateState = Literal["not_evaluated", "allowed", "blocked"]
PersonaCreationMode = Literal[
    "detailed_prompt",
    "fuzzy_preference",
    "template",
    "random_seed",
    "style_inspiration",
]
PersonaTruthDisclosure = Literal["fictional_ai_persona"]
PersonaSourceType = Literal[
    "original",
    "deidentified_style",
    "self_authorized",
    "third_party_authorized",
    "prohibited",
]
PersonaRiskTier = Literal["L1", "L2", "L3", "L4", "L5"]
PersonaVirtualContentStatus = Literal["imagined_ai_generated"]
PersonaVersionEditProposalState = Literal["draft_review_only"]
PersonaVersionEditReviewDecision = Literal["approved_for_manual_apply", "rejected", "needs_changes"]
ProactiveConsentStatus = Literal["disabled", "enabled", "paused", "revoked"]
ProactiveConsentSurface = Literal["in_app_review_card", "local_sandbox_preview"]
ProactiveConsentIntent = Literal[
    "gentle_check_in",
    "memory_follow_up",
    "care_routine",
    "shared_interest",
    "relationship_repair_note",
]
RoleDynamicPostTruthDisclosure = Literal["imagined_ai_generated_content"]
RoleDynamicPostReviewStatus = Literal["requires_review", "approved_for_demo", "rejected"]
RoleDynamicPostVisibility = Literal["local_private_review"]
AIGCLabel = Literal["ai_generated"]
RoleDynamicMemoryRefUsage = Literal["inspiration_only"]
AIGCContentModality = Literal[
    "text",
    "image",
    "audio",
    "video",
    "virtual_scene",
    "persona",
    "virtual_history",
    "role_dynamic_post",
    "export",
    "shared_content",
]
AIGCProductSurface = Literal[
    "companion_reply",
    "persona_card",
    "virtual_history",
    "role_dynamic_post",
    "export_manifest",
    "shared_content",
    "voice_avatar",
    "web_demo",
]
ControlArtifactType = Literal[
    "memory_event",
    "persona_card",
    "persona_version_record",
    "role_dynamic_post",
    "proactive_consent",
    "proactive_review_card",
]
ControlOperationName = Literal["soft_delete", "hard_delete", "freeze", "unfreeze", "export"]
ControlConfirmationStatus = Literal["dry_run_only", "confirmed", "rejected"]
ControlExportFormat = Literal["manifest_json"]
ConsentFeatureScope = Literal[
    "memory",
    "persona_distillation",
    "proactive_messaging",
    "aigc_export_share",
    "voice_avatar",
    "analytics",
    "model_improvement",
    "payment_marketing",
]
ConsentActorType = Literal["user", "guardian", "reviewer", "system"]
DataRightsRequestType = Literal["access", "correction", "deletion", "export", "withdrawal", "objection"]
DataRightsRequestStatus = Literal["received", "in_review", "fulfilled", "rejected", "cancelled"]
VoiceMode = Literal[
    "disabled",
    "non_real_synthetic_voice",
    "generated_fictional_voice",
    "recorded_user_voice",
    "third_party_authorized_voice",
    "blocked_voice_clone",
]
VoiceSourceRoute = Literal[
    "disabled",
    "non_real_synthetic_voice",
    "generated_fictional_voice",
    "recorded_user_voice",
    "third_party_authorized_voice",
    "blocked_voice_clone",
]
VoiceRequestedLikenessType = Literal[
    "none",
    "self",
    "authorized_voice_talent",
    "real_person",
    "deceased_person",
    "public_figure",
    "family_member",
    "ex_partner",
]
VoiceConsentDecision = Literal["disabled", "blocked", "review_required"]
VoiceSafetyDecisionAction = Literal["allow_for_review", "deescalate_for_review", "block"]


_PERSONA_EDITOR_FORBIDDEN_FIELD_TERMS = frozenset(
    {
        "send",
        "schedule",
        "delivery",
        "platform",
        "webhook",
        "token",
        "queue",
    }
)
_PERSONA_EDITOR_BLOCKING_RISK_LABELS = frozenset(
    {
        "real_person_similarity",
        "unsafe_content",
        "unauthorized_clone_risk",
        "deception_risk",
        "public_person_reference",
    }
)


def _ordered_unique(values: list[str]) -> list[str]:
    seen: set[str] = set()
    unique_values: list[str] = []
    for value in values:
        if value not in seen:
            unique_values.append(value)
            seen.add(value)
    return unique_values


class InboundEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: new_id("evt"))
    tenant_id: str = "default"
    source_type: SourceType
    platform: Platform
    channel_id: str
    channel_type: ChannelType
    account_id: str
    actor_id: str
    actor_name: str | None = None
    direction: Direction
    content_type: ContentType
    occurred_at: datetime = Field(default_factory=utc_now)
    text: str | None = None
    attachments: list[dict[str, Any]] = Field(default_factory=list)
    raw: dict[str, Any] = Field(default_factory=dict)


class InboundConnectorResult(BaseModel):
    connector_name: str
    agent_id: str
    event: InboundEvent
    raw_payload: dict[str, Any] = Field(default_factory=dict)


class DesktopCapturedMessage(BaseModel):
    message_id: str = Field(default_factory=lambda: new_id("desktop_msg"))
    sender_name: str | None = None
    text: str | None = None
    occurred_at: datetime | None = None
    display_time: str | None = None
    bubble_side: str | None = None
    bubble_type: str | None = None
    quoted_text: str | None = None
    quoted_sender_name: str | None = None
    raw: dict[str, Any] = Field(default_factory=dict)


class DesktopScanResult(BaseModel):
    connector_name: str
    platform: Platform
    account_id: str
    conversation_hint: str | None = None
    messages: list[DesktopCapturedMessage] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class OcrTextBlock(BaseModel):
    text: str
    page_index: int = 0
    label: str | None = None
    bbox: list[float] = Field(default_factory=list)


class OcrDocumentResult(BaseModel):
    provider: str
    model: str
    full_text: str = ""
    markdown_text: str | None = None
    blocks: list[OcrTextBlock] = Field(default_factory=list)
    raw: dict[str, Any] = Field(default_factory=dict)


class MeetingCaptureChunkDebug(BaseModel):
    chunk_index: int
    audio_source: MeetingAudioSource
    device_name: str
    display_time: str | None = None
    started_offset_seconds: float
    duration_seconds: float
    sample_rate: int
    channels: int
    rms: float
    peak: float | None = None
    applied_gain: float | None = None
    normalization_gain: float | None = None
    compressor_threshold: float | None = None
    compressor_ratio: float | None = None
    limiter_ceiling: float | None = None
    dc_offset: float | None = None
    highpass_cutoff_hz: float | None = None
    trimmed_start_seconds: float = 0.0
    trimmed_end_seconds: float = 0.0
    silence_threshold: float
    is_silent: bool
    wav_size_bytes: int
    saved_path: str | None = None
    transcription_status: str | None = None
    transcription_text: str | None = None
    transcription_error: str | None = None
    transcription_retry_count: int = 0
    transcription_retry_strategy: str | None = None


class MeetingTranscriptSegment(BaseModel):
    segment_id: str = Field(default_factory=lambda: new_id("meeting_seg"))
    speaker_name: str | None = None
    text: str
    display_time: str | None = None
    started_at: datetime | None = None
    ended_at: datetime | None = None
    is_final: bool = True
    raw: dict[str, Any] = Field(default_factory=dict)


class MeetingAssistantAdvice(BaseModel):
    backend: str
    model: str | None = None
    status: str = "ok"
    summary: str | None = None
    key_points: list[str] = Field(default_factory=list)
    follow_up_questions: list[str] = Field(default_factory=list)
    suggested_reply: str | None = None
    action_items: list[str] = Field(default_factory=list)
    raw: dict[str, Any] = Field(default_factory=dict)


class MeetingMinutesDraft(BaseModel):
    template: MeetingExportTemplate = MeetingExportTemplate.STANDARD
    backend: str = "heuristic_fallback"
    model: str | None = None
    status: str = "ok"
    title: str | None = None
    overview: str | None = None
    background: list[str] = Field(default_factory=list)
    conclusions: list[str] = Field(default_factory=list)
    action_items: list[str] = Field(default_factory=list)
    risks: list[str] = Field(default_factory=list)
    raw_excerpt_ids: list[str] = Field(default_factory=list)
    raw: dict[str, Any] = Field(default_factory=dict)


class MeetingMinutesRecord(BaseModel):
    minutes_id: str = Field(default_factory=lambda: new_id("meeting_minutes"))
    session_id: str
    template: MeetingExportTemplate = MeetingExportTemplate.STANDARD
    title: str | None = None
    backend: str = "heuristic_fallback"
    model: str | None = None
    status: str = "ok"
    output_path: str | None = None
    markdown_body: str
    overview: str | None = None
    background: list[str] = Field(default_factory=list)
    conclusions: list[str] = Field(default_factory=list)
    action_items: list[str] = Field(default_factory=list)
    risks: list[str] = Field(default_factory=list)
    raw_excerpt_ids: list[str] = Field(default_factory=list)
    raw: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=utc_now)


class MeetingSessionRecord(BaseModel):
    session_id: str = Field(default_factory=lambda: new_id("meeting_session"))
    connector_name: str
    platform: Platform = Platform.TENCENT_MEETING
    account_id: str
    meeting_key: str
    meeting_title: str | None = None
    channel_id: str
    audio_source: MeetingAudioSource | None = None
    capture_backend: str | None = None
    capture_device_name: str | None = None
    transcription_backend: str | None = None
    detected_window: dict[str, Any] = Field(default_factory=dict)
    notes: list[str] = Field(default_factory=list)
    latest_summary: str | None = None
    latest_key_points: list[str] = Field(default_factory=list)
    latest_action_items: list[str] = Field(default_factory=list)
    latest_follow_up_questions: list[str] = Field(default_factory=list)
    last_segment_at: datetime | None = None
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)


class MeetingSegmentRecord(BaseModel):
    segment_id: str = Field(default_factory=lambda: new_id("meeting_segment"))
    session_id: str
    connector_name: str
    platform: Platform = Platform.TENCENT_MEETING
    account_id: str
    chunk_index: int | None = None
    speaker_name: str | None = None
    display_time: str | None = None
    text: str
    started_at: datetime | None = None
    ended_at: datetime | None = None
    audio_source: MeetingAudioSource | None = None
    capture_device_name: str | None = None
    saved_path: str | None = None
    raw: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=utc_now)


class MeetingLivePreview(BaseModel):
    connector_name: str
    platform: Platform = Platform.TENCENT_MEETING
    account_id: str
    runtime_agent_id: str | None = None
    meeting_session_id: str | None = None
    rolling_summary: str | None = None
    rolling_key_points: list[str] = Field(default_factory=list)
    rolling_action_items: list[str] = Field(default_factory=list)
    rolling_follow_up_questions: list[str] = Field(default_factory=list)
    meeting_title: str | None = None
    audio_source: MeetingAudioSource | None = None
    capture_backend: str | None = None
    capture_device_name: str | None = None
    transcription_backend: str | None = None
    notes: list[str] = Field(default_factory=list)
    detected_window: dict[str, Any] = Field(default_factory=dict)
    capture_chunks: list[MeetingCaptureChunkDebug] = Field(default_factory=list)
    segments: list[MeetingTranscriptSegment] = Field(default_factory=list)
    runtime_turns: list[AgentTurnResult] = Field(default_factory=list)


class AgentProfile(BaseModel):
    agent_id: str
    display_name: str
    persona_type: PersonaType = PersonaType.FRIEND
    system_identity: str = "virtual_ai_persona"
    public_disclosure: str = "This account is operated by an AI persona."
    core_traits: list[str] = Field(default_factory=lambda: ["kind", "curious", "steady"])
    speech_style: dict[str, Any] = Field(
        default_factory=lambda: {
            "tone": "warm",
            "message_length": "short_to_medium",
            "emoji_level": "low",
        },
    )
    interests: list[str] = Field(default_factory=list)
    relationship_mode: str = "friend"
    safety_mode: SafetyMode = SafetyMode.DISCLOSED_AI
    do_not_do: list[str] = Field(
        default_factory=lambda: ["pretend_to_be_a_specific_real_person", "spam"],
    )
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)


class MemoryFact(BaseModel):
    memory_id: str = Field(default_factory=lambda: new_id("mem"))
    agent_id: str
    user_id: str
    memory_type: MemoryType = MemoryType.FACT
    scope: MemoryScope = MemoryScope.LONG_TERM
    salience: float = 0.5
    confidence: float = 0.5
    fact: str
    evidence_refs: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)


class DistillationClaim(BaseModel):
    claim: str
    evidence_refs: list[str] = Field(..., min_length=1)
    confidence: float = Field(..., ge=0.0, le=1.0)
    sensitivity: DistillationSensitivity
    status: DistillationStatus
    rationale: str | None = None


class ChunkSummaryObservation(DistillationClaim):
    observation_type: str = "general"


class ChunkSummary(BaseModel):
    chunk_id: str
    contact_id: str
    conversation_id: str
    time_range: list[str | None] = Field(default_factory=list)
    event_ids: list[str] = Field(default_factory=list)
    message_count: int = Field(default=0, ge=0)
    chunking_reason: str
    summary: str
    topics: list[str] = Field(default_factory=list)
    evidence_refs: list[str] = Field(..., min_length=1)
    confidence: float = Field(..., ge=0.0, le=1.0)
    sensitivity: DistillationSensitivity
    status: DistillationStatus
    important_facts: list[DistillationClaim] = Field(default_factory=list)
    communication_observations: list[ChunkSummaryObservation] = Field(default_factory=list)
    risk_notes: list[str] = Field(default_factory=list)
    source_message_type_codes: list[int] = Field(default_factory=list)
    interaction_flags: list[str] = Field(default_factory=list)
    risk_flags: list[str] = Field(default_factory=list)


class MemoryFactCandidate(BaseModel):
    memory_id: str = Field(default_factory=lambda: new_id("mem"))
    memory_type: DistillationMemoryType
    subject_id: str
    claim: str
    evidence_refs: list[str] = Field(..., min_length=1)
    confidence: float = Field(..., ge=0.0, le=1.0)
    importance: float = Field(..., ge=0.0, le=1.0)
    sensitivity: DistillationSensitivity
    status: DistillationStatus
    rationale: str | None = None
    conflicts_with: list[str] = Field(default_factory=list)
    source_chunk_ids: list[str] = Field(default_factory=list)

    def to_runtime_memory_type(self) -> MemoryType:
        mapping: dict[DistillationMemoryType, MemoryType] = {
            "semantic": MemoryType.FACT,
            "episodic": MemoryType.FACT,
            "relationship": MemoryType.RELATIONSHIP,
            "procedural": MemoryType.PREFERENCE,
            "reflection": MemoryType.REFLECTION,
        }
        return mapping[self.memory_type]

    def to_memory_fact(
        self,
        *,
        agent_id: str,
        user_id: str,
        scope: MemoryScope = MemoryScope.LONG_TERM,
    ) -> MemoryFact:
        return MemoryFact(
            memory_id=self.memory_id,
            agent_id=agent_id,
            user_id=user_id,
            memory_type=self.to_runtime_memory_type(),
            scope=scope,
            salience=self.importance,
            confidence=self.confidence,
            fact=self.claim,
            evidence_refs=list(self.evidence_refs),
        )


class MemoryProvenance(BaseModel):
    source_type: MemoryProvenanceSourceType
    evidence_refs: list[str] = Field(default_factory=list)
    source_event_ids: list[str] = Field(default_factory=list)
    source_memory_ids: list[str] = Field(default_factory=list)
    source_persona_ids: list[str] = Field(default_factory=list)
    source_summary: str | None = None


class MemoryRetrievalPermission(BaseModel):
    allow_factual_retrieval: bool = False
    allow_inferred_retrieval: bool = False
    allow_relational_retrieval: bool = False
    allow_procedural_retrieval: bool = False
    allow_imagined_retrieval: bool = False
    review_required: bool = False

    def has_any_route(self) -> bool:
        return any(
            [
                self.allow_factual_retrieval,
                self.allow_inferred_retrieval,
                self.allow_relational_retrieval,
                self.allow_procedural_retrieval,
                self.allow_imagined_retrieval,
            ],
        )


class MemoryEvent(BaseModel):
    schema_version: str = "memory_event_v2"
    event_id: str = Field(default_factory=lambda: new_id("mev"))
    user_id: str = Field(..., min_length=1)
    agent_id: str | None = None
    persona_id: str | None = None
    event_type: MemoryEventType
    truth_status: MemoryTruthStatus
    summary: str = Field(..., min_length=1)
    provenance: MemoryProvenance
    sensitivity: DistillationSensitivity = "low"
    lifecycle_state: MemoryLifecycleState = "active"
    retrieval_permission: MemoryRetrievalPermission = Field(default_factory=MemoryRetrievalPermission)
    salience: float = Field(default=0.5, ge=0.0, le=1.0)
    confidence: float | None = Field(default=None, ge=0.0, le=1.0)
    inference_rationale: str | None = None
    relationship_dimensions: list[str] = Field(default_factory=list)
    preference_labels: list[str] = Field(default_factory=list)
    imagined_context_label: str | None = None
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)

    @model_validator(mode="after")
    def validate_memory_event(self) -> "MemoryEvent":
        expected_truth_by_type: dict[MemoryEventType, MemoryTruthStatus] = {
            "factual": "evidence_backed",
            "inferred": "inferred",
            "relational": "relationship_state",
            "procedural": "procedural_preference",
            "imagined": "imagined",
        }
        expected_truth = expected_truth_by_type[self.event_type]
        if self.truth_status != expected_truth:
            raise ValueError(f"{self.event_type} memory must use truth_status={expected_truth}")

        if self.event_type == "factual" and not self.provenance.evidence_refs:
            raise ValueError("factual memory requires evidence_refs")
        if self.event_type == "factual" and self.provenance.source_type == "imagined_generation":
            raise ValueError("factual memory cannot use imagined generation provenance")
        if self.event_type == "inferred":
            if self.confidence is None:
                raise ValueError("inferred memory requires confidence")
            if not self.inference_rationale:
                raise ValueError("inferred memory requires inference_rationale")
        if self.event_type == "relational" and not self.relationship_dimensions:
            raise ValueError("relational memory requires relationship_dimensions")
        if self.event_type == "procedural" and not self.preference_labels:
            raise ValueError("procedural memory requires preference_labels")
        if self.event_type == "imagined" and not self.imagined_context_label:
            raise ValueError("imagined memory requires imagined_context_label")

        self._apply_default_retrieval_permission()
        if self.event_type == "imagined" and self.retrieval_permission.allow_factual_retrieval:
            raise ValueError("imagined memory cannot be retrieved as factual evidence")
        return self

    def _apply_default_retrieval_permission(self) -> None:
        if not self.retrieval_permission.has_any_route():
            if self.event_type == "factual":
                self.retrieval_permission.allow_factual_retrieval = True
            elif self.event_type == "inferred":
                self.retrieval_permission.allow_inferred_retrieval = True
            elif self.event_type == "relational":
                self.retrieval_permission.allow_relational_retrieval = True
            elif self.event_type == "procedural":
                self.retrieval_permission.allow_procedural_retrieval = True
            elif self.event_type == "imagined":
                self.retrieval_permission.allow_imagined_retrieval = True

        if self.sensitivity in {"medium", "high"}:
            self.retrieval_permission.review_required = True

    def is_retrieval_eligible(self, context: MemoryRetrievalContext) -> bool:
        if self.lifecycle_state in {"frozen", "deleted", "archived"}:
            return False
        if self.retrieval_permission.review_required:
            return False
        if context == "factual":
            return self.retrieval_permission.allow_factual_retrieval
        if context == "inferred":
            return self.retrieval_permission.allow_inferred_retrieval
        if context == "relational":
            return self.retrieval_permission.allow_relational_retrieval
        if context == "procedural":
            return self.retrieval_permission.allow_procedural_retrieval
        return self.retrieval_permission.allow_imagined_retrieval


class MemoryRetrievalBundleItem(BaseModel):
    schema_version: str = "memory_retrieval_bundle_item_v2"
    event_id: str
    event_type: MemoryEventType
    truth_status: MemoryTruthStatus
    summary: str
    provenance_refs: list[str] = Field(default_factory=list)
    retrieval_context: MemoryRetrievalContext
    sensitivity: DistillationSensitivity
    lifecycle_state: MemoryLifecycleState
    review_required: bool = False

    @classmethod
    def from_event(
        cls,
        event: MemoryEvent,
        *,
        retrieval_context: MemoryRetrievalContext,
    ) -> "MemoryRetrievalBundleItem":
        provenance_refs = [
            *event.provenance.evidence_refs,
            *event.provenance.source_event_ids,
            *event.provenance.source_memory_ids,
            *event.provenance.source_persona_ids,
        ]
        return cls(
            event_id=event.event_id,
            event_type=event.event_type,
            truth_status=event.truth_status,
            summary=event.summary,
            provenance_refs=provenance_refs,
            retrieval_context=retrieval_context,
            sensitivity=event.sensitivity,
            lifecycle_state=event.lifecycle_state,
            review_required=event.retrieval_permission.review_required,
        )


class MemoryRetrievalBundle(BaseModel):
    schema_version: str = "memory_retrieval_bundle_v2"
    bundle_id: str = Field(default_factory=lambda: new_id("memrb"))
    purpose: MemoryRetrievalPurpose
    query_summary: str = Field(..., min_length=1)
    items: list[MemoryRetrievalBundleItem] = Field(default_factory=list)
    selected_memory_ids: list[str] = Field(default_factory=list)
    excluded_memory_ids: list[str] = Field(default_factory=list)
    exclusion_reasons: dict[str, str] = Field(default_factory=dict)
    truth_status_counts: dict[str, int] = Field(default_factory=dict)
    imagined_memory_count: int = 0
    safety_warnings: list[str] = Field(default_factory=list)
    include_review_required: bool = False
    generated_at: datetime = Field(default_factory=utc_now)

    @model_validator(mode="after")
    def validate_bundle(self) -> "MemoryRetrievalBundle":
        if self.purpose == "factual_response":
            for item in self.items:
                if item.event_type == "imagined" or item.truth_status == "imagined":
                    raise ValueError("factual_response bundles cannot include imagined memory as evidence")

        inactive_items = [
            item.event_id
            for item in self.items
            if item.lifecycle_state in {"deleted", "frozen", "archived"}
        ]
        if inactive_items:
            raise ValueError("deleted, frozen, or archived memory cannot be included in retrieval bundles")

        review_required_items = [item.event_id for item in self.items if item.review_required]
        if review_required_items and not self.include_review_required:
            raise ValueError("review-required memory requires include_review_required=true")

        self.selected_memory_ids = [item.event_id for item in self.items]
        counts: dict[str, int] = {}
        for item in self.items:
            counts[item.truth_status] = counts.get(item.truth_status, 0) + 1
        self.truth_status_counts = counts
        self.imagined_memory_count = counts.get("imagined", 0)
        return self


class MemoryViewerItem(BaseModel):
    schema_version: str = "memory_viewer_item_v1"
    memory_id: str
    user_id: str
    event_type: MemoryEventType
    truth_status: MemoryTruthStatus
    sensitivity: DistillationSensitivity
    lifecycle_state: MemoryLifecycleState
    review_required: bool
    summary: str
    provenance_refs: list[str] = Field(default_factory=list)
    is_retrieval_eligible: bool
    is_factual_evidence: bool = False
    can_edit: bool = True
    can_delete: bool = True
    can_freeze: bool = True
    can_export: bool = True
    safety_notes: list[str] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_event(cls, event: MemoryEvent) -> "MemoryViewerItem":
        context_by_event_type: dict[MemoryEventType, MemoryRetrievalContext] = {
            "factual": "factual",
            "inferred": "inferred",
            "relational": "relational",
            "procedural": "procedural",
            "imagined": "imagined",
        }
        provenance_refs = [
            *event.provenance.evidence_refs,
            *event.provenance.source_event_ids,
            *event.provenance.source_memory_ids,
            *event.provenance.source_persona_ids,
        ]
        is_retrieval_eligible = event.is_retrieval_eligible(context_by_event_type[event.event_type])
        safety_notes: list[str] = []
        if event.event_type == "imagined":
            safety_notes.append("imagined_memory")
        if event.retrieval_permission.review_required:
            safety_notes.append("review_required")
        if not is_retrieval_eligible:
            safety_notes.append("not_retrieval_eligible")
        return cls(
            memory_id=event.event_id,
            user_id=event.user_id,
            event_type=event.event_type,
            truth_status=event.truth_status,
            sensitivity=event.sensitivity,
            lifecycle_state=event.lifecycle_state,
            review_required=event.retrieval_permission.review_required,
            summary=event.summary,
            provenance_refs=provenance_refs,
            is_retrieval_eligible=is_retrieval_eligible,
            is_factual_evidence=event.event_type == "factual" and event.is_retrieval_eligible("factual"),
            can_edit=event.lifecycle_state not in {"deleted", "archived"},
            can_delete=event.lifecycle_state != "deleted",
            can_freeze=event.lifecycle_state == "active",
            can_export=event.lifecycle_state != "deleted",
            safety_notes=safety_notes,
            created_at=event.created_at,
            updated_at=event.updated_at,
        )


class MemoryViewerFilter(BaseModel):
    schema_version: str = "memory_viewer_filter_v1"
    event_types: list[MemoryEventType] = Field(default_factory=list)
    truth_statuses: list[MemoryTruthStatus] = Field(default_factory=list)
    lifecycle_states: list[MemoryLifecycleState] = Field(default_factory=list)
    sensitivities: list[DistillationSensitivity] = Field(default_factory=list)
    include_deleted: bool = False


class MemoryViewerPage(BaseModel):
    schema_version: str = "memory_viewer_page_v1"
    items: list[MemoryViewerItem] = Field(default_factory=list)
    filters: MemoryViewerFilter = Field(default_factory=MemoryViewerFilter)
    total_count: int = Field(default=0, ge=0)
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1)
    generated_at: datetime = Field(default_factory=utc_now)


class ContactSkillTopicPreference(DistillationClaim):
    topic: str
    reason: str | None = None


class ContactSkillPattern(DistillationClaim):
    pattern: str


class ContactSkillImportantEvent(DistillationClaim):
    event: str
    date: str | None = None
    importance: float = Field(default=0.5, ge=0.0, le=1.0)


class ContactSkillRelationshipState(BaseModel):
    current_status: str = "unknown"
    closeness: float = Field(default=0.0, ge=0.0, le=1.0)
    trust_level: float = Field(default=0.0, ge=0.0, le=1.0)
    interaction_frequency: str = "unknown"
    initiative_balance: str = "unknown"
    confidence: float = Field(..., ge=0.0, le=1.0)
    evidence_refs: list[str] = Field(..., min_length=1)
    sensitivity: DistillationSensitivity
    status: DistillationStatus


class ContactSkillCommunicationStyle(BaseModel):
    message_length: str = "unknown"
    tone: str = "unknown"
    response_latency: str = "unknown"
    directness: str = "unknown"
    confidence: float = Field(..., ge=0.0, le=1.0)
    evidence_refs: list[str] = Field(..., min_length=1)
    sensitivity: DistillationSensitivity
    status: DistillationStatus


class ContactSkillUserSidePreferences(BaseModel):
    user_goal: str | None = None
    boundaries: list[str] = Field(default_factory=list)
    preferred_reply_style: str | None = None


class ContactSkillReplyStrategy(BaseModel):
    default: str | None = None
    when_contact_is_cold: str | None = None
    when_contact_opens_topic: str | None = None
    for_sensitive_topics: str | None = None


class ContactSkillUsageBoundary(BaseModel):
    allowed_uses: list[str] = Field(
        default_factory=lambda: [
            "reply_assistance",
            "context_retrieval",
            "human_review",
        ],
    )
    disallowed_uses: list[str] = Field(
        default_factory=lambda: [
            "persona_clone",
            "impersonation",
            "autonomous_contact_simulation",
        ],
    )
    notes: list[str] = Field(
        default_factory=lambda: [
            "ContactSkillCandidate exists to help the user communicate with better context and boundaries.",
            "It must not be used to imitate, replace, or autonomously speak as the real contact.",
        ],
    )


class ContactSkillRedactionPolicy(BaseModel):
    store_raw_quotes: bool = False
    max_quote_length: int = Field(default=30, ge=0)
    mask_names: bool = True
    mask_phone_numbers: bool = True


class ContactSkillCandidate(BaseModel):
    schema_version: str = "contact_skill_candidate_v1"
    contact_id: str
    relationship_type: ContactRelationshipType
    status: DistillationStatus
    confidence: float = Field(..., ge=0.0, le=1.0)
    sensitivity: DistillationSensitivity
    evidence_refs: list[str] = Field(..., min_length=1)
    source_chunk_ids: list[str] = Field(default_factory=list)
    source_memory_ids: list[str] = Field(default_factory=list)
    relationship_state: ContactSkillRelationshipState
    communication_style: ContactSkillCommunicationStyle
    preferred_topics: list[ContactSkillTopicPreference] = Field(default_factory=list)
    avoid_topics: list[ContactSkillTopicPreference] = Field(default_factory=list)
    important_events: list[ContactSkillImportantEvent] = Field(default_factory=list)
    stable_preferences: list[ContactSkillPattern] = Field(default_factory=list)
    emotional_patterns: list[ContactSkillPattern] = Field(default_factory=list)
    user_side_preferences: ContactSkillUserSidePreferences = Field(default_factory=ContactSkillUserSidePreferences)
    reply_strategy: ContactSkillReplyStrategy = Field(default_factory=ContactSkillReplyStrategy)
    usage_boundary: ContactSkillUsageBoundary = Field(default_factory=ContactSkillUsageBoundary)
    review_notes: list[str] = Field(default_factory=list)
    redaction_policy: ContactSkillRedactionPolicy = Field(default_factory=ContactSkillRedactionPolicy)


class DistilledArtifactReviewDecision(BaseModel):
    review_id: str = Field(default_factory=lambda: new_id("review"))
    status: DistillationStatus
    reviewer_id: str | None = None
    reviewer_name: str | None = None
    reviewed_at: datetime = Field(default_factory=utc_now)
    notes: list[str] = Field(default_factory=list)
    evidence_validation_status: DistillationEvidenceValidationStatus = "not_run"


class DistilledArtifactReviewMetadata(BaseModel):
    review_state: DistillationReviewState = "pending_human_review"
    reviewed_by_human: bool = False
    last_decision: DistillationStatus | None = None
    last_reviewed_at: datetime | None = None
    last_reviewer_id: str | None = None
    last_reviewer_name: str | None = None
    evidence_validation_status: DistillationEvidenceValidationStatus = "not_run"
    decision_notes: list[str] = Field(default_factory=list)
    history: list[DistilledArtifactReviewDecision] = Field(default_factory=list)

    def is_runtime_ready(self, *, status: DistillationStatus) -> bool:
        return status == "approved" and self.reviewed_by_human and self.last_decision == "approved"


class DistilledArtifactSourceMetadata(BaseModel):
    source_run_id: str | None = None
    source_artifact_path: str | None = None
    review_artifact_path: str | None = None
    source_chunk_ids: list[str] = Field(default_factory=list)
    source_memory_ids: list[str] = Field(default_factory=list)
    source_event_ids: list[str] = Field(default_factory=list)


class PersonaSourcePolicy(BaseModel):
    source_type: PersonaSourceType = "original"
    risk_tier: PersonaRiskTier = "L1"
    consent_artifact_ids: list[str] = Field(default_factory=list)
    blocked_real_person_similarity: bool = False
    deidentification_notes: list[str] = Field(default_factory=list)
    prohibited_reason: str | None = None

    @model_validator(mode="after")
    def validate_source_policy(self) -> "PersonaSourcePolicy":
        expected_tier_by_source = {
            "original": "L1",
            "deidentified_style": "L2",
            "self_authorized": "L3",
            "third_party_authorized": "L4",
            "prohibited": "L5",
        }
        expected_tier = expected_tier_by_source[self.source_type]
        if self.risk_tier != expected_tier:
            raise ValueError(f"{self.source_type} source must use risk tier {expected_tier}")
        if self.source_type not in {"original", "prohibited"} and not self.consent_artifact_ids:
            raise ValueError("non-original persona sources require consent_artifact_ids")
        if self.source_type == "prohibited" and not self.prohibited_reason:
            raise ValueError("prohibited persona sources require prohibited_reason")
        return self


class PersonaIdentity(BaseModel):
    display_name: str = Field(..., min_length=1)
    fictional: bool = True
    age_range: str | None = None
    world_setting: str | None = None
    public_person_or_real_person_reference: bool = False

    @model_validator(mode="after")
    def validate_fictional_identity(self) -> "PersonaIdentity":
        if not self.fictional:
            raise ValueError("PersonaCard v1 supports fictional identities only")
        if self.public_person_or_real_person_reference:
            raise ValueError("PersonaCard v1 cannot reference a public or real person")
        return self


class PersonaTraitProfile(BaseModel):
    warmth: float = Field(default=0.5, ge=0.0, le=1.0)
    directness: float = Field(default=0.5, ge=0.0, le=1.0)
    humor: float = Field(default=0.5, ge=0.0, le=1.0)
    independence: float = Field(default=0.5, ge=0.0, le=1.0)
    jealousy: float = Field(default=0.0, ge=0.0, le=1.0)
    emotional_stability: float = Field(default=0.5, ge=0.0, le=1.0)


class PersonaSpeechStyle(BaseModel):
    sentence_length: str | None = None
    emoji_frequency: str | None = None
    punctuation_style: str | None = None
    dialect: str | None = None
    humor_type: str | None = None
    pet_names: str | None = None
    taboo_phrases: list[str] = Field(default_factory=list)


class PersonaEmotionModel(BaseModel):
    baseline_mood: str | None = None
    stress_response: str | None = None
    comforting_style: str | None = None
    conflict_style: str | None = None


class PersonaRelationshipModel(BaseModel):
    attachment_style: str | None = None
    trust_growth_rate: float = Field(default=0.0, ge=0.0, le=1.0)
    intimacy_growth_rate: float = Field(default=0.0, ge=0.0, le=1.0)
    boundary_sensitivity: float = Field(default=0.5, ge=0.0, le=1.0)


class PersonaVirtualHistory(BaseModel):
    background: str | None = None
    daily_routine: list[str] = Field(default_factory=list)
    current_goals: list[str] = Field(default_factory=list)
    virtual_social_circle: list[str] = Field(default_factory=list)
    content_status: PersonaVirtualContentStatus = "imagined_ai_generated"
    factual_claims_allowed: bool = False
    source_memory_ids: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_imagined_only(self) -> "PersonaVirtualHistory":
        if self.factual_claims_allowed:
            raise ValueError("virtual history is imagined content and cannot make factual claims")
        return self


class PersonaGrowthPolicy(BaseModel):
    frozen_fields: list[str] = Field(default_factory=list)
    mutable_fields: list[str] = Field(default_factory=list)
    max_weekly_trait_delta: float = Field(default=0.05, ge=0.0, le=0.2)
    requires_user_review_for: list[str] = Field(
        default_factory=lambda: [
            "romantic_intensity",
            "dependency_language",
            "real_person_similarity",
        ],
    )

    @model_validator(mode="after")
    def validate_field_sets(self) -> "PersonaGrowthPolicy":
        overlap = set(self.frozen_fields).intersection(self.mutable_fields)
        if overlap:
            raise ValueError("frozen_fields and mutable_fields must not overlap")
        return self


class PersonaProactivePreferences(BaseModel):
    default_enabled: bool = False
    allowed_message_types: list[str] = Field(default_factory=list)
    max_daily_messages: int = Field(default=0, ge=0, le=3)
    quiet_hours: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_review_first_defaults(self) -> "PersonaProactivePreferences":
        if self.default_enabled:
            raise ValueError("proactive behavior must not be enabled by default")
        return self


class PersonaSafetyPolicy(BaseModel):
    minor_mode_allowed: bool = False
    self_harm_response_style: str = "supportive_redirect"
    dependency_guardrails: bool = True
    no_deception: bool = True
    no_unauthorized_clone: bool = True
    no_paid_intimacy_escalation: bool = True

    @model_validator(mode="after")
    def validate_required_safety_flags(self) -> "PersonaSafetyPolicy":
        if not self.dependency_guardrails:
            raise ValueError("dependency_guardrails must remain enabled")
        if not self.no_deception:
            raise ValueError("no_deception must remain enabled")
        if not self.no_unauthorized_clone:
            raise ValueError("no_unauthorized_clone must remain enabled")
        if not self.no_paid_intimacy_escalation:
            raise ValueError("no_paid_intimacy_escalation must remain enabled")
        return self


class PersonaCard(BaseModel):
    schema_version: str = "persona_card_v1"
    persona_id: str = Field(default_factory=lambda: new_id("persona"))
    version: int = Field(default=1, ge=1)
    user_id: str = Field(..., min_length=1)
    display_name: str = Field(..., min_length=1)
    creation_mode: PersonaCreationMode
    truth_disclosure: PersonaTruthDisclosure = "fictional_ai_persona"
    source_policy: PersonaSourcePolicy = Field(default_factory=PersonaSourcePolicy)
    identity: PersonaIdentity
    core_traits: PersonaTraitProfile = Field(default_factory=PersonaTraitProfile)
    speech_style: PersonaSpeechStyle = Field(default_factory=PersonaSpeechStyle)
    emotion_model: PersonaEmotionModel = Field(default_factory=PersonaEmotionModel)
    relationship_model: PersonaRelationshipModel = Field(default_factory=PersonaRelationshipModel)
    virtual_history: PersonaVirtualHistory = Field(default_factory=PersonaVirtualHistory)
    growth_policy: PersonaGrowthPolicy = Field(default_factory=PersonaGrowthPolicy)
    proactive_preferences: PersonaProactivePreferences = Field(default_factory=PersonaProactivePreferences)
    safety_policy: PersonaSafetyPolicy = Field(default_factory=PersonaSafetyPolicy)
    status: DistillationStatus = "candidate"
    review_metadata: DistilledArtifactReviewMetadata = Field(default_factory=DistilledArtifactReviewMetadata)
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)

    @model_validator(mode="after")
    def validate_persona_card(self) -> "PersonaCard":
        if self.creation_mode == "style_inspiration" and self.source_policy.source_type != "deidentified_style":
            raise ValueError("style_inspiration creation requires deidentified_style source policy")
        if self.source_policy.source_type == "original" and self.creation_mode == "style_inspiration":
            raise ValueError("original source cannot use style_inspiration creation mode")
        if self.source_policy.risk_tier == "L5" and not self.source_policy.blocked_real_person_similarity:
            raise ValueError("L5 persona requests must record blocked_real_person_similarity")
        return self

    def is_runtime_ready(self) -> bool:
        if not self.review_metadata.is_runtime_ready(status=self.status):
            return False
        if self.source_policy.risk_tier not in {"L1", "L2"}:
            return False
        if self.source_policy.source_type == "prohibited":
            return False
        if self.source_policy.blocked_real_person_similarity:
            return False
        if not self.identity.fictional or self.identity.public_person_or_real_person_reference:
            return False
        if not self.safety_policy.no_deception or not self.safety_policy.no_unauthorized_clone:
            return False
        return True


class PersonaEditFieldChange(BaseModel):
    schema_version: str = "persona_edit_field_change_v1"
    field_path: str = Field(..., min_length=1)
    old_value_summary: str = Field(..., min_length=1)
    proposed_value_summary: str = Field(..., min_length=1)
    reason: str = Field(..., min_length=1)
    risk_labels: list[str] = Field(default_factory=list)
    requires_review: bool = False
    review_required_reasons: list[str] = Field(default_factory=list)
    blocks_auto_approval: bool = False
    blocking_risk_labels: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_review_flags(self) -> "PersonaEditFieldChange":
        field_path = self.field_path.strip()
        lowered_path = field_path.lower()
        if any(term in lowered_path for term in _PERSONA_EDITOR_FORBIDDEN_FIELD_TERMS):
            raise ValueError("persona edit field_path cannot target delivery or platform surfaces")

        review_reasons = list(self.review_required_reasons)
        if field_path == "display_name" or field_path.startswith("identity."):
            review_reasons.append("identity_field_change")
        if field_path == "source_policy" or field_path.startswith("source_policy."):
            review_reasons.append("source_policy_change")
        if field_path == "safety_policy" or field_path.startswith("safety_policy."):
            review_reasons.append("safety_policy_change")

        blocking_labels = [
            label
            for label in self.risk_labels
            if label in _PERSONA_EDITOR_BLOCKING_RISK_LABELS
        ]
        if blocking_labels:
            review_reasons.append("blocking_risk_label")

        self.field_path = field_path
        self.review_required_reasons = _ordered_unique(review_reasons)
        self.blocking_risk_labels = _ordered_unique(blocking_labels)
        self.blocks_auto_approval = bool(self.blocking_risk_labels)
        self.requires_review = self.requires_review or bool(self.review_required_reasons)
        return self


class PersonaVersionEditProposal(BaseModel):
    schema_version: str = "persona_version_edit_proposal_v1"
    proposal_id: str = Field(default_factory=lambda: new_id("personaedit"))
    user_id: str = Field(..., min_length=1)
    source_persona_id: str = Field(..., min_length=1)
    source_persona_version: int = Field(..., ge=1)
    source_persona_schema_version: str = "persona_card_v1"
    requested_by: str = Field(..., min_length=1)
    proposal_reason: str = Field(..., min_length=1)
    changes: list[PersonaEditFieldChange] = Field(..., min_length=1)
    proposal_state: PersonaVersionEditProposalState = "draft_review_only"
    human_review_required: Literal[True] = True
    auto_approval_allowed: Literal[False] = False
    auto_approval_blocked: bool = True
    auto_apply_allowed: Literal[False] = False
    writes_persona_version: Literal[False] = False
    blocking_risk_labels: list[str] = Field(default_factory=list)
    review_required_reasons: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=utc_now)

    @classmethod
    def from_persona_card(
        cls,
        persona: PersonaCard,
        *,
        requested_by: str,
        changes: list[PersonaEditFieldChange],
        proposal_reason: str,
    ) -> "PersonaVersionEditProposal":
        return cls(
            user_id=persona.user_id,
            source_persona_id=persona.persona_id,
            source_persona_version=persona.version,
            source_persona_schema_version=persona.schema_version,
            requested_by=requested_by,
            proposal_reason=proposal_reason,
            changes=changes,
        )

    @model_validator(mode="after")
    def validate_draft_only_review_contract(self) -> "PersonaVersionEditProposal":
        blocking_labels: list[str] = []
        review_reasons: list[str] = []
        for change in self.changes:
            blocking_labels.extend(change.blocking_risk_labels)
            review_reasons.extend(change.review_required_reasons)
            if change.requires_review:
                review_reasons.append("field_change_requires_review")

        self.blocking_risk_labels = _ordered_unique(blocking_labels)
        self.review_required_reasons = _ordered_unique(review_reasons)
        self.auto_approval_blocked = True
        return self


class PersonaVersionEditReview(BaseModel):
    schema_version: str = "persona_version_edit_review_v1"
    review_id: str = Field(default_factory=lambda: new_id("personaeditreview"))
    proposal_id: str = Field(..., min_length=1)
    reviewer_id: str = Field(..., min_length=1)
    decision: PersonaVersionEditReviewDecision
    notes: list[str] = Field(default_factory=list)
    blocking_risk_labels: list[str] = Field(default_factory=list)
    auto_apply_allowed: Literal[False] = False
    approved_for_auto_apply: Literal[False] = False
    writes_persona_version: Literal[False] = False
    reviewed_at: datetime = Field(default_factory=utc_now)

    @classmethod
    def from_proposal(
        cls,
        proposal: PersonaVersionEditProposal,
        *,
        reviewer_id: str,
        decision: PersonaVersionEditReviewDecision,
        notes: list[str] | None = None,
    ) -> "PersonaVersionEditReview":
        return cls(
            proposal_id=proposal.proposal_id,
            reviewer_id=reviewer_id,
            decision=decision,
            notes=notes or [],
            blocking_risk_labels=proposal.blocking_risk_labels,
        )

    @model_validator(mode="after")
    def validate_review_only_contract(self) -> "PersonaVersionEditReview":
        self.blocking_risk_labels = _ordered_unique(self.blocking_risk_labels)
        if self.decision == "approved_for_manual_apply" and self.blocking_risk_labels:
            raise ValueError("blocking risk labels cannot be approved for manual apply")
        return self


class ControlOperationTarget(BaseModel):
    schema_version: str = "control_operation_target_v1"
    artifact_type: ControlArtifactType
    artifact_id: str = Field(..., min_length=1)
    user_id: str = Field(..., min_length=1)
    persona_id: str | None = None
    current_state: str = Field(default="active", min_length=1)
    review_required: bool = False
    retrieval_eligible: bool = True
    runtime_eligible: bool = False
    provenance_refs: list[str] = Field(default_factory=list)
    safety_labels: list[str] = Field(default_factory=list)


class ControlOperationPreview(BaseModel):
    schema_version: str = "control_operation_preview_v1"
    preview_id: str = Field(default_factory=lambda: new_id("controlpreview"))
    operation: ControlOperationName
    target: ControlOperationTarget
    reason: str = Field(..., min_length=1)
    dry_run: Literal[True] = True
    requires_confirmation: Literal[True] = True
    hard_delete: bool = False
    would_change_state_to: str | None = None
    retrieval_eligible_after: bool = True
    runtime_eligible_after: bool = False
    source_files_untouched: Literal[True] = True
    writes_records: Literal[False] = False
    writes_export_files: Literal[False] = False
    safety_flags: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=utc_now)

    @classmethod
    def for_target(
        cls,
        *,
        operation: ControlOperationName,
        target: ControlOperationTarget,
        reason: str,
    ) -> "ControlOperationPreview":
        if operation in {"soft_delete", "hard_delete"}:
            safety_flags = ["delete_requires_confirmation", "retrieval_blocked_after_operation"]
            if operation == "hard_delete":
                safety_flags.extend(["hard_delete_preview_only", "high_impact_control"])
            return cls(
                operation=operation,
                target=target,
                reason=reason,
                hard_delete=operation == "hard_delete",
                would_change_state_to="deleted",
                retrieval_eligible_after=False,
                runtime_eligible_after=False,
                safety_flags=safety_flags,
            )
        if operation == "freeze":
            return cls(
                operation=operation,
                target=target,
                reason=reason,
                would_change_state_to="frozen",
                retrieval_eligible_after=False,
                runtime_eligible_after=False,
                safety_flags=["freeze_requires_confirmation", "retrieval_blocked_after_operation"],
            )
        if operation == "unfreeze":
            return cls(
                operation=operation,
                target=target,
                reason=reason,
                would_change_state_to="active",
                retrieval_eligible_after=target.retrieval_eligible,
                runtime_eligible_after=target.runtime_eligible,
                safety_flags=["unfreeze_requires_confirmation"],
            )
        return cls(
            operation=operation,
            target=target,
            reason=reason,
            would_change_state_to=target.current_state,
            retrieval_eligible_after=target.retrieval_eligible,
            runtime_eligible_after=target.runtime_eligible,
            safety_flags=["export_requires_confirmation", "manifest_only"],
        )

    @model_validator(mode="after")
    def validate_preview_flags(self) -> "ControlOperationPreview":
        if self.operation == "hard_delete":
            self.hard_delete = True
            self.safety_flags.extend(["hard_delete_preview_only", "high_impact_control"])
        elif self.hard_delete:
            raise ValueError("hard_delete flag is only valid for hard_delete operation")

        if self.operation in {"soft_delete", "hard_delete"}:
            self.would_change_state_to = "deleted"
            self.retrieval_eligible_after = False
            self.runtime_eligible_after = False
        elif self.operation == "freeze":
            self.would_change_state_to = "frozen"
            self.retrieval_eligible_after = False
            self.runtime_eligible_after = False
        elif self.operation == "unfreeze":
            self.would_change_state_to = self.would_change_state_to or "active"
        else:
            self.would_change_state_to = self.would_change_state_to or self.target.current_state
        self.safety_flags = _ordered_unique(self.safety_flags)
        return self


class ControlOperationConfirmation(BaseModel):
    schema_version: str = "control_operation_confirmation_v1"
    confirmation_id: str = Field(default_factory=lambda: new_id("controlconfirm"))
    preview_id: str = Field(..., min_length=1)
    operation: ControlOperationName
    target: ControlOperationTarget
    actor_id: str = Field(..., min_length=1)
    confirmed: bool
    confirmation_phrase: str = ""
    confirmation_status: ControlConfirmationStatus = "rejected"
    reason: str = Field(..., min_length=1)
    executes_operation: Literal[False] = False
    writes_records: Literal[False] = False
    writes_export_files: Literal[False] = False
    created_at: datetime = Field(default_factory=utc_now)

    @classmethod
    def from_preview(
        cls,
        preview: ControlOperationPreview,
        *,
        actor_id: str,
        confirmed: bool,
        confirmation_phrase: str,
        reason: str,
    ) -> "ControlOperationConfirmation":
        return cls(
            preview_id=preview.preview_id,
            operation=preview.operation,
            target=preview.target,
            actor_id=actor_id,
            confirmed=confirmed,
            confirmation_phrase=confirmation_phrase,
            reason=reason,
        )

    @model_validator(mode="after")
    def validate_confirmation_status(self) -> "ControlOperationConfirmation":
        if self.confirmed and not self.confirmation_phrase.strip():
            raise ValueError("confirmed control operation requires confirmation_phrase")
        self.confirmation_status = "confirmed" if self.confirmed else "rejected"
        return self


class ControlAuditEvent(BaseModel):
    schema_version: str = "control_audit_event_v1"
    audit_id: str = Field(default_factory=lambda: new_id("controlaudit"))
    actor_id: str = Field(..., min_length=1)
    user_id: str = Field(..., min_length=1)
    target: ControlOperationTarget
    operation: ControlOperationName
    before_summary: str = Field(..., min_length=1)
    after_summary: str = Field(..., min_length=1)
    reason: str = Field(..., min_length=1)
    confirmation_status: ControlConfirmationStatus = "dry_run_only"
    safety_flags: list[str] = Field(default_factory=list)
    source_surface: str = "local_control_surface"
    redacted_content_only: Literal[True] = True
    executes_operation: Literal[False] = False
    writes_records: Literal[False] = False
    writes_export_files: Literal[False] = False
    created_at: datetime = Field(default_factory=utc_now)

    @classmethod
    def from_preview(
        cls,
        preview: ControlOperationPreview,
        *,
        actor_id: str,
        before_summary: str,
        after_summary: str,
        confirmation: ControlOperationConfirmation | None = None,
        safety_flags: list[str] | None = None,
    ) -> "ControlAuditEvent":
        confirmation_status: ControlConfirmationStatus = "dry_run_only"
        if confirmation is not None:
            confirmation_status = confirmation.confirmation_status
        return cls(
            actor_id=actor_id,
            user_id=preview.target.user_id,
            target=preview.target,
            operation=preview.operation,
            before_summary=before_summary,
            after_summary=after_summary,
            reason=preview.reason,
            confirmation_status=confirmation_status,
            safety_flags=safety_flags or [],
        )

    @model_validator(mode="after")
    def normalize_safety_flags(self) -> "ControlAuditEvent":
        self.safety_flags = _ordered_unique(self.safety_flags)
        return self


class ControlExportManifest(BaseModel):
    schema_version: str = "control_export_manifest_v1"
    export_id: str = Field(default_factory=lambda: new_id("controlexport"))
    user_id: str = Field(..., min_length=1)
    format: ControlExportFormat = "manifest_json"
    reason: str = Field(..., min_length=1)
    targets: list[ControlOperationTarget] = Field(..., min_length=1)
    target_count: int = Field(default=0, ge=0)
    include_provenance: bool = True
    provenance_refs: list[str] = Field(default_factory=list)
    contains_imagined_content: bool = False
    contains_aigc_content: bool = False
    contains_review_required_items: bool = False
    imagined_target_ids: list[str] = Field(default_factory=list)
    aigc_target_ids: list[str] = Field(default_factory=list)
    review_required_target_ids: list[str] = Field(default_factory=list)
    redacted_content_only: Literal[True] = True
    source_files_untouched: Literal[True] = True
    writes_export_files: Literal[False] = False
    generated_at: datetime = Field(default_factory=utc_now)

    @classmethod
    def from_targets(
        cls,
        *,
        user_id: str,
        targets: list[ControlOperationTarget],
        reason: str,
    ) -> "ControlExportManifest":
        return cls(user_id=user_id, targets=targets, reason=reason)

    @model_validator(mode="after")
    def derive_manifest_labels(self) -> "ControlExportManifest":
        provenance_refs: list[str] = []
        imagined_target_ids: list[str] = []
        aigc_target_ids: list[str] = []
        review_required_target_ids: list[str] = []

        for target in self.targets:
            provenance_refs.extend(target.provenance_refs)
            safety_labels = set(target.safety_labels)
            if safety_labels.intersection({"imagined_content", "imagined_memory", "not_real_world_activity"}):
                imagined_target_ids.append(target.artifact_id)
            if safety_labels.intersection({"ai_generated", "aigc", "imagined_ai_generated_content"}):
                aigc_target_ids.append(target.artifact_id)
            if target.review_required or "review_required" in safety_labels:
                review_required_target_ids.append(target.artifact_id)

        self.target_count = len(self.targets)
        self.provenance_refs = _ordered_unique(provenance_refs)
        self.imagined_target_ids = _ordered_unique(imagined_target_ids)
        self.aigc_target_ids = _ordered_unique(aigc_target_ids)
        self.review_required_target_ids = _ordered_unique(review_required_target_ids)
        self.contains_imagined_content = bool(self.imagined_target_ids)
        self.contains_aigc_content = bool(self.aigc_target_ids)
        self.contains_review_required_items = bool(self.review_required_target_ids)
        return self


class ConsentGrantRecord(BaseModel):
    schema_version: str = "consent_grant_record_v1"
    grant_id: str = Field(default_factory=lambda: new_id("consentgrant"))
    user_id: str = Field(..., min_length=1)
    feature_scope: ConsentFeatureScope
    policy_version: str = Field(..., min_length=1)
    actor_id: str = Field(..., min_length=1)
    actor_type: ConsentActorType = "user"
    granted: Literal[True] = True
    granted_at: datetime = Field(default_factory=utc_now)
    expires_at: datetime | None = None
    evidence_refs: list[str] = Field(default_factory=list)
    review_required: bool = True


class ConsentWithdrawalRecord(BaseModel):
    schema_version: str = "consent_withdrawal_record_v1"
    withdrawal_id: str = Field(default_factory=lambda: new_id("consentwithdrawal"))
    user_id: str = Field(..., min_length=1)
    feature_scope: ConsentFeatureScope
    supersedes_grant_ids: list[str] = Field(default_factory=list)
    actor_id: str = Field(..., min_length=1)
    actor_type: ConsentActorType = "user"
    reason: str = Field(..., min_length=1)
    withdrawn_at: datetime = Field(default_factory=utc_now)
    evidence_refs: list[str] = Field(default_factory=list)


class ConsentCenterState(BaseModel):
    schema_version: str = "consent_center_state_v1"
    user_id: str = Field(..., min_length=1)
    grants: list[ConsentGrantRecord] = Field(default_factory=list)
    withdrawals: list[ConsentWithdrawalRecord] = Field(default_factory=list)
    is_minor: bool = False
    guardian_actor_id: str | None = None
    guardian_consent_required: bool = True
    minor_access_allowed: Literal[False] = False
    active_feature_scopes: list[ConsentFeatureScope] = Field(default_factory=list)
    withdrawn_feature_scopes: list[ConsentFeatureScope] = Field(default_factory=list)
    generated_at: datetime = Field(default_factory=utc_now)

    def has_active_consent(self, feature_scope: ConsentFeatureScope) -> bool:
        return feature_scope in self.active_feature_scopes

    @model_validator(mode="after")
    def derive_active_scopes(self) -> "ConsentCenterState":
        for grant in self.grants:
            if grant.user_id != self.user_id:
                raise ValueError("consent grant user_id must match consent center user_id")
        for withdrawal in self.withdrawals:
            if withdrawal.user_id != self.user_id:
                raise ValueError("consent withdrawal user_id must match consent center user_id")

        withdrawn_feature_scopes = _ordered_unique([withdrawal.feature_scope for withdrawal in self.withdrawals])
        superseded_grant_ids: set[str] = set()
        latest_withdrawal_by_scope: dict[ConsentFeatureScope, datetime] = {}
        for withdrawal in self.withdrawals:
            superseded_grant_ids.update(withdrawal.supersedes_grant_ids)
            current = latest_withdrawal_by_scope.get(withdrawal.feature_scope)
            if current is None or withdrawal.withdrawn_at > current:
                latest_withdrawal_by_scope[withdrawal.feature_scope] = withdrawal.withdrawn_at

        active_scopes: list[ConsentFeatureScope] = []
        for grant in self.grants:
            if grant.grant_id in superseded_grant_ids:
                continue
            latest_withdrawal = latest_withdrawal_by_scope.get(grant.feature_scope)
            if latest_withdrawal is not None and grant.granted_at <= latest_withdrawal:
                continue
            active_scopes.append(grant.feature_scope)

        self.active_feature_scopes = _ordered_unique(active_scopes)
        self.withdrawn_feature_scopes = withdrawn_feature_scopes
        return self


class DataRightsRequestRecord(BaseModel):
    schema_version: str = "data_rights_request_record_v1"
    request_id: str = Field(default_factory=lambda: new_id("datarights"))
    user_id: str = Field(..., min_length=1)
    request_type: DataRightsRequestType
    status: DataRightsRequestStatus = "received"
    actor_id: str = Field(..., min_length=1)
    actor_type: ConsentActorType = "user"
    reason: str = Field(..., min_length=1)
    target_scopes: list[ConsentFeatureScope] = Field(default_factory=list)
    review_required: bool = True
    submitted_at: datetime = Field(default_factory=utc_now)
    due_at: datetime | None = None
    completed_at: datetime | None = None
    result_summary: str | None = None
    audit_refs: list[str] = Field(default_factory=list)


class MemoryFactStoreRecord(BaseModel):
    schema_version: str = "memory_fact_store_record_v1"
    record_id: str = Field(default_factory=lambda: new_id("memstore"))
    artifact_type: Literal["memory_fact"] = "memory_fact"
    memory_fact: MemoryFactCandidate
    source_metadata: DistilledArtifactSourceMetadata = Field(default_factory=DistilledArtifactSourceMetadata)
    review_metadata: DistilledArtifactReviewMetadata = Field(default_factory=DistilledArtifactReviewMetadata)
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)

    def is_runtime_ready(self) -> bool:
        return self.review_metadata.is_runtime_ready(status=self.memory_fact.status)


class MemoryFactStoreFile(BaseModel):
    schema_version: str = "memory_fact_store_v1"
    generated_at: datetime = Field(default_factory=utc_now)
    records: list[MemoryFactStoreRecord] = Field(default_factory=list)


class ContactSkillStoreRecord(BaseModel):
    schema_version: str = "contact_skill_store_record_v1"
    record_id: str = Field(default_factory=lambda: new_id("skillstore"))
    artifact_type: Literal["contact_skill"] = "contact_skill"
    contact_skill: ContactSkillCandidate
    source_metadata: DistilledArtifactSourceMetadata = Field(default_factory=DistilledArtifactSourceMetadata)
    review_metadata: DistilledArtifactReviewMetadata = Field(default_factory=DistilledArtifactReviewMetadata)
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)

    def is_runtime_ready(self) -> bool:
        return self.review_metadata.is_runtime_ready(status=self.contact_skill.status)


class ContactSkillStoreFile(BaseModel):
    schema_version: str = "contact_skill_store_v1"
    generated_at: datetime = Field(default_factory=utc_now)
    records: list[ContactSkillStoreRecord] = Field(default_factory=list)


class MemoryProfileFacet(BaseModel):
    facet_id: str = Field(default_factory=lambda: new_id("facet"))
    facet_type: str = "general"
    title: str
    summary: str
    confidence: float = 0.5
    evidence_memory_ids: list[str] = Field(default_factory=list)
    evidence_facts: list[str] = Field(default_factory=list)
    memory_types: list[MemoryType] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    preferred_intents: list[ChatIntent] = Field(default_factory=list)


class MemoryProfileSnapshot(BaseModel):
    preferences: list[str] = Field(default_factory=list)
    facts: list[str] = Field(default_factory=list)
    relationships: list[str] = Field(default_factory=list)
    reflections: list[str] = Field(default_factory=list)
    facets: list[MemoryProfileFacet] = Field(default_factory=list)
    summary: str | None = None


class MemoryProfileRecord(BaseModel):
    profile_id: str = Field(default_factory=lambda: new_id("profile"))
    agent_id: str
    user_id: str
    source_event_id: str | None = None
    backend: str = "memory_retrieval"
    model: str | None = None
    summary: str | None = None
    snapshot: MemoryProfileSnapshot = Field(default_factory=MemoryProfileSnapshot)
    memory_count: int = 0
    created_at: datetime = Field(default_factory=utc_now)


class ApprovedMemoryFactBrief(BaseModel):
    record_id: str
    memory_id: str
    memory_type: DistillationMemoryType
    claim: str
    evidence_refs: list[str] = Field(default_factory=list)


class ApprovedContactSkillBrief(BaseModel):
    record_id: str
    contact_id: str
    relationship_type: ContactRelationshipType
    relationship_summary: str
    strategy_hints: list[str] = Field(default_factory=list)
    boundary_reminders: list[str] = Field(default_factory=list)
    evidence_refs: list[str] = Field(default_factory=list)


class ApprovedStoreContext(BaseModel):
    status: ApprovedStoreContextStatus = "not_configured"
    source_path: str | None = None
    validation_report_path: str | None = None
    contact_id: str | None = None
    contact_skill: ApprovedContactSkillBrief | None = None
    memory_facts: list[ApprovedMemoryFactBrief] = Field(default_factory=list)
    source_record_ids: list[str] = Field(default_factory=list)
    evidence_refs: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class ApprovedPatchBrief(BaseModel):
    patch_id: str
    patch_type: str
    compact_instruction: str
    sensitivity: DistillationSensitivity
    supporting_feedback_count: int = 0
    supporting_cluster_ids: list[str] = Field(default_factory=list)


class ApprovedPatchContext(BaseModel):
    status: ApprovedStoreContextStatus = "not_configured"
    source_path: str | None = None
    contact_id: str | None = None
    patches: list[ApprovedPatchBrief] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class DerivedBriefContext(BaseModel):
    status: ApprovedStoreContextStatus = "not_configured"
    persona: PartnerPersonaBrief | None = None
    policy: CommunicationPolicyBrief | None = None
    boundary: BoundaryProfileBrief | None = None
    source_skill_record_id: str | None = None
    notes: list[str] = Field(default_factory=list)


class ApprovedRelationshipDeltaBrief(BaseModel):
    """Compact summary of one approved relationship delta for ChatContext.

    Carries only the reviewer-safe surface: dimension direction text,
    a compact delta summary, and evidence refs.  No raw signal history,
    no raw review history, and no raw private text.
    """

    delta_id: str = Field(..., min_length=1)
    contact_id: str = Field(..., min_length=1)
    dimension_changes: list[str] = Field(default_factory=list)
    delta_summary: str = Field(default="", max_length=200)
    evidence_refs: list[str] = Field(default_factory=list)


class ApprovedRelationshipContext(BaseModel):
    """Compact, approval-gated relationship-state guidance for ChatContext.

    Only runtime-ready (approved + human-reviewed) RelationshipDeltaCandidates
    are consumed.  Candidate, rejected, frozen, and archived deltas are excluded.
    """

    status: ApprovedStoreContextStatus = "not_configured"
    source_path: str | None = None
    contact_id: str | None = None
    deltas: list[ApprovedRelationshipDeltaBrief] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class ChatContextEvent(BaseModel):
    event_id: str
    actor_id: str
    actor_name: str | None = None
    direction: Direction
    content_type: ContentType
    source_type: SourceType
    occurred_at: datetime
    text: str | None = None


class ChatContext(BaseModel):
    agent_id: str
    agent_display_name: str
    persona_type: PersonaType
    relationship_mode: str
    speech_style: dict[str, Any] = Field(default_factory=dict)
    channel_id: str
    channel_type: ChannelType
    platform: Platform
    user_id: str
    user_name: str | None = None
    intent: ChatIntent = ChatIntent.GENERAL
    latest_message_text: str | None = None
    recent_events: list[ChatContextEvent] = Field(default_factory=list)
    memory_hits: list[MemoryFact] = Field(default_factory=list)
    memory_candidate_count: int = 0
    memory_profile: MemoryProfileSnapshot = Field(default_factory=MemoryProfileSnapshot)
    memory_retrieval_notes: list[str] = Field(default_factory=list)
    approved_store_context: ApprovedStoreContext = Field(default_factory=ApprovedStoreContext)
    approved_patch_context: ApprovedPatchContext = Field(default_factory=ApprovedPatchContext)
    derived_brief_context: DerivedBriefContext = Field(default_factory=DerivedBriefContext)
    relationship_context: ApprovedRelationshipContext = Field(default_factory=ApprovedRelationshipContext)
    summary: str | None = None


class ReplyPlanContextRef(BaseModel):
    ref_type: ReplyPlanContextRefType
    ref_id: str = Field(..., min_length=1)
    note: str | None = None


class ReplyPlanSourceContext(BaseModel):
    approved_store_status: ApprovedStoreContextStatus = "not_configured"
    chat_context_summary: str | None = None
    recent_event_ids: list[str] = Field(default_factory=list)
    memory_hit_ids: list[str] = Field(default_factory=list)
    approved_contact_skill_record_id: str | None = None
    approved_memory_record_ids: list[str] = Field(default_factory=list)
    approved_store_evidence_refs: list[str] = Field(default_factory=list)


class ReplyPlanCandidate(BaseModel):
    candidate_id: str = Field(default_factory=lambda: new_id("replycand"))
    approach_label: str = Field(..., min_length=1)
    priority_rank: int = Field(..., ge=1)
    draft_text: str = Field(..., min_length=1)
    rationale: str = Field(..., min_length=1)
    supporting_context_refs: list[ReplyPlanContextRef] = Field(..., min_length=1)
    risk_flags: list[str] = Field(default_factory=list)
    boundary_reminders: list[str] = Field(..., min_length=1)
    confidence: float | None = Field(default=None, ge=0.0, le=1.0)


class ReplyPlan(BaseModel):
    schema_version: str = "reply_plan_v1"
    plan_mode: ReplyPlanMode = "candidate_review_only"
    contact_id: str = Field(..., min_length=1)
    source_context: ReplyPlanSourceContext
    policy_boundary_summary: list[str] = Field(..., min_length=1)
    notes_on_candidate_differences: list[str] = Field(..., min_length=1)
    candidates: list[ReplyPlanCandidate] = Field(..., min_length=3)


LLMGeneratorType = Literal["template_deterministic", "llm_generated"]


class LLMGenerationMetadata(BaseModel):
    provider: str = "unknown"
    model: str = "unknown"
    temperature: float = 0.7
    prompt_template_hash: str | None = None
    generated_at: datetime = Field(default_factory=utc_now)
    latency_ms: int | None = None


class LLMReplyPlanRefusal(BaseModel):
    refusal_code: Literal[
        "PROVIDER_ERROR",
        "INPUT_TOO_LARGE",
        "MISSING_REQUIRED_CONTEXT",
        "SAFETY_FILTER",
        "INVALID_OUTPUT_SCHEMA",
    ]
    refusal_reason: str = Field(..., min_length=1)
    is_retryable: bool


class LLMReplyPlanCandidate(ReplyPlanCandidate):
    generator_type: LLMGeneratorType = "llm_generated"


class LLMReplyPlan(BaseModel):
    schema_version: str = "llm_reply_plan_v1"
    generator_type: LLMGeneratorType = "llm_generated"
    generator_id: str = Field(default_factory=lambda: new_id("llm_gen"))
    contact_id: str | None = None
    source_context_snapshot: dict[str, Any] = Field(default_factory=dict)
    generation_metadata: LLMGenerationMetadata | None = None
    candidates: list[LLMReplyPlanCandidate] = Field(default_factory=list)
    refusal: LLMReplyPlanRefusal | None = None


class AgentSelfState(BaseModel):
    """Compact review-safe state for future proactive behavior drafting.

    This model intentionally stores identifiers, safe summaries, and artifact
    refs only. It is not a transcript cache and has no execution capability.
    """

    schema_version: str = "agent_self_state_v1"
    state_id: str = Field(default_factory=lambda: new_id("agentstate"))
    agent_id: str = Field(..., min_length=1)
    user_id: str = Field(..., min_length=1)
    contact_id: str | None = Field(default=None, min_length=1)
    availability_state: AgentAvailabilityState = "unknown"
    current_focus: str | None = None
    approved_context_refs: list[str] = Field(default_factory=list)
    recent_signal_refs: list[str] = Field(default_factory=list)
    risk_flags: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)


_CANDIDATE_ACTION_FORBIDDEN_PAYLOAD_FIELDS = frozenset(
    {
        "send_at",
        "scheduled_at",
        "platform",
        "channel_id",
        "webhook_url",
        "recipient_address",
        "raw_transcript",
        "chat_history",
        "private_messages",
        "access_token",
        "api_key",
    },
)
_OUTBOUND_MESSAGE_FORBIDDEN_METADATA_FIELDS = frozenset(
    set(_CANDIDATE_ACTION_FORBIDDEN_PAYLOAD_FIELDS).union(
        {
            "scheduler_id",
            "schedule_id",
            "timer_id",
            "reminder_id",
            "adapter_payload",
            "adapter_config",
            "platform_target",
            "platform_token",
            "bot_token",
            "app_secret",
            "open_id",
            "chat_id",
            "receive_id",
            "receive_id_type",
            "feishu_open_id",
            "feishu_chat_id",
            "delivery_connector_name",
            "delivery_response",
            "send_result",
        },
    ),
)


class BehaviorPolicy(BaseModel):
    """Draft-only policy envelope for future CandidateAction artifacts."""

    schema_version: str = "behavior_policy_v1"
    policy_id: str = Field(default_factory=lambda: new_id("behpolicy"))
    policy_mode: BehaviorPolicyMode = "draft_only_review_required"
    human_review_required: Literal[True] = True
    auto_send_allowed: Literal[False] = False
    platform_execution_allowed: Literal[False] = False
    scheduler_allowed: Literal[False] = False
    allowed_action_types: list[BehaviorActionType] = Field(
        default_factory=lambda: [
            "relationship_check_in_draft",
            "reply_follow_up_draft",
            "topic_suggestion",
            "boundary_review_note",
            "memory_review_prompt",
            "do_nothing",
        ],
        min_length=1,
    )
    forbidden_payload_fields: list[str] = Field(
        default_factory=lambda: sorted(_CANDIDATE_ACTION_FORBIDDEN_PAYLOAD_FIELDS),
    )
    boundary_rules: list[str] = Field(
        default_factory=lambda: [
            "Candidate actions are review artifacts only.",
            "Do not send, schedule, or execute without a later explicit send-gate milestone.",
        ],
    )
    max_candidates: int = Field(default=5, ge=1)
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)


class CandidateActionPayload(BaseModel):
    """Non-executable payload carried by a CandidateAction.

    `metadata` is deliberately restricted from transport, scheduling, platform,
    credential, and raw transcript keys.
    """

    safe_summary: str = Field(..., min_length=1)
    draft_text: str | None = None
    review_notes: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator("metadata")
    @classmethod
    def reject_forbidden_metadata_keys(cls, value: dict[str, Any]) -> dict[str, Any]:
        forbidden = _CANDIDATE_ACTION_FORBIDDEN_PAYLOAD_FIELDS.intersection(value)
        if forbidden:
            keys = ", ".join(sorted(forbidden))
            raise ValueError(f"CandidateActionPayload metadata contains forbidden key(s): {keys}")
        return value


class CandidateAction(BaseModel):
    """Review-only proactive behavior candidate.

    Approval may make the artifact visible to later review/runtime surfaces, but
    this schema never permits sending, scheduling, platform execution, or store
    mutation by itself.
    """

    schema_version: str = "candidate_action_v1"
    action_id: str = Field(default_factory=lambda: new_id("candact"))
    action_mode: CandidateActionMode = "draft_only_review_required"
    contact_id: str = Field(..., min_length=1)
    user_id: str = Field(..., min_length=1)
    action_type: BehaviorActionType
    title: str = Field(..., min_length=1)
    rationale: str = Field(..., min_length=1)
    supporting_context_refs: list[ReplyPlanContextRef] = Field(..., min_length=1)
    risk_flags: list[str] = Field(default_factory=list)
    payload: CandidateActionPayload = Field(
        default_factory=lambda: CandidateActionPayload(safe_summary="No action."),
    )
    policy: BehaviorPolicy = Field(default_factory=BehaviorPolicy)
    status: DistillationStatus = "candidate"
    review_metadata: DistilledArtifactReviewMetadata = Field(
        default_factory=DistilledArtifactReviewMetadata,
    )
    human_review_required: Literal[True] = True
    auto_send_allowed: Literal[False] = False
    platform_execution_allowed: Literal[False] = False
    scheduler_allowed: Literal[False] = False
    platform_target: None = None
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)

    @model_validator(mode="after")
    def action_type_is_allowed_by_policy(self) -> CandidateAction:
        if self.action_type not in self.policy.allowed_action_types:
            raise ValueError("CandidateAction action_type is not allowed by its BehaviorPolicy.")
        return self

    def is_runtime_visible(self) -> bool:
        return self.review_metadata.is_runtime_ready(status=self.status)


class OutboundMessagePayload(BaseModel):
    """Draft-only outbound payload for later send-gate evaluation.

    `metadata` is deliberately restricted from scheduling, adapter, credential,
    transport, and raw transcript keys so the request remains inert in T220.
    """

    draft_text: str = Field(..., min_length=1)
    safe_summary: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator("metadata")
    @classmethod
    def reject_forbidden_metadata_keys(cls, value: dict[str, Any]) -> dict[str, Any]:
        forbidden = _OUTBOUND_MESSAGE_FORBIDDEN_METADATA_FIELDS.intersection(value)
        if forbidden:
            keys = ", ".join(sorted(forbidden))
            raise ValueError(f"OutboundMessagePayload metadata contains forbidden key(s): {keys}")
        return value


class OutboundRequestHumanApproval(BaseModel):
    """Explicit human-review state for an outbound request.

    This review is separate from any CandidateAction review status. A reviewed
    behavior artifact may serve as evidence, but a send request still needs its
    own approval metadata.
    """

    review_state: OutboundHumanApprovalState = "pending_human_approval"
    approved_by_human: bool = False
    reviewer_id: str | None = None
    reviewed_at: datetime | None = None
    review_notes: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_review_state(self) -> OutboundRequestHumanApproval:
        has_reviewer = self.reviewer_id is not None and self.reviewer_id.strip() != ""
        if self.review_state == "pending_human_approval":
            if self.approved_by_human or has_reviewer or self.reviewed_at is not None:
                raise ValueError("Pending outbound human approval must not carry completed review metadata.")
            return self
        if not has_reviewer or self.reviewed_at is None:
            raise ValueError("Reviewed outbound requests must record reviewer_id and reviewed_at.")
        if self.review_state == "approved" and not self.approved_by_human:
            raise ValueError("Approved outbound requests must set approved_by_human=True.")
        if self.review_state == "rejected" and self.approved_by_human:
            raise ValueError("Rejected outbound requests must set approved_by_human=False.")
        return self


class OutboundRequestSendGate(BaseModel):
    """Snapshot of later send-gate evaluation state.

    T220 keeps the request non-sendable by default through `not_evaluated`.
    T221 may later populate `allowed` or `blocked` with explicit audit data.
    """

    gate_state: OutboundSendGateState = "not_evaluated"
    evaluator_id: str | None = None
    evaluated_at: datetime | None = None
    gate_notes: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_gate_state(self) -> OutboundRequestSendGate:
        has_evaluator = self.evaluator_id is not None and self.evaluator_id.strip() != ""
        if self.gate_state == "not_evaluated":
            if has_evaluator or self.evaluated_at is not None:
                raise ValueError("Unevaluated outbound send-gate state must not carry evaluator metadata.")
            return self
        if not has_evaluator or self.evaluated_at is None:
            raise ValueError("Evaluated outbound send-gate state must record evaluator_id and evaluated_at.")
        return self


class OutboundMessageRequest(BaseModel):
    """Schema-only outbound request boundary for later send-gate work.

    The request is inert until it has its own explicit human approval and a
    later send-gate decision. CandidateAction review status is evidence only.
    """

    schema_version: str = "outbound_message_request_v1"
    request_id: str = Field(default_factory=lambda: new_id("outreq"))
    contact_id: str = Field(..., min_length=1)
    user_id: str = Field(..., min_length=1)
    source_type: OutboundRequestSourceType
    source_candidate_action_id: str | None = Field(default=None, min_length=1)
    source_context_refs: list[ReplyPlanContextRef] = Field(default_factory=list)
    payload: OutboundMessagePayload
    channel_preference: OutboundMessageChannel = "unspecified"
    risk_flags: list[str] = Field(default_factory=list)
    human_approval: OutboundRequestHumanApproval = Field(default_factory=OutboundRequestHumanApproval)
    send_gate: OutboundRequestSendGate = Field(default_factory=OutboundRequestSendGate)
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)

    @model_validator(mode="after")
    def validate_source_boundary(self) -> OutboundMessageRequest:
        if self.source_type == "candidate_action" and not self.source_candidate_action_id:
            raise ValueError("Candidate-action outbound requests must include source_candidate_action_id.")
        if self.source_type == "human_authored" and self.source_candidate_action_id is not None:
            raise ValueError("Human-authored outbound requests must not include source_candidate_action_id.")
        return self

    def is_sendable(self) -> bool:
        return (
            self.human_approval.review_state == "approved"
            and self.human_approval.approved_by_human
            and self.send_gate.gate_state == "allowed"
        )


class ChatSuggestion(BaseModel):
    backend: str
    model: str | None = None
    status: str = "ok"
    should_reply: bool = True
    summary: str | None = None
    reply_draft: str | None = None
    alternatives: list[str] = Field(default_factory=list)
    rationale: str | None = None
    risk_flags: list[str] = Field(default_factory=list)
    raw: dict[str, Any] = Field(default_factory=dict)


class ChatMemoryCandidate(BaseModel):
    agent_id: str
    user_id: str
    memory_type: MemoryType = MemoryType.FACT
    fact: str
    salience: float = 0.5
    confidence: float = 0.5
    evidence_refs: list[str] = Field(default_factory=list)
    merge_with_memory_id: str | None = None
    rationale: str | None = None


class MemoryDuplicateGroup(BaseModel):
    user_id: str
    memory_type: MemoryType
    canonical_memory_id: str | None = None
    canonical_fact: str
    memory_ids: list[str] = Field(default_factory=list)
    facts: list[str] = Field(default_factory=list)
    merged_fact_preview: str | None = None
    baseline_merge_preview: str | None = None
    similarity_score: float = 1.0
    facet_family_key: str | None = None
    facet_title: str | None = None
    facet_summary: str | None = None
    facet_confidence: float | None = None
    canonicalization_strategy: str | None = None
    canonicalization_reason: str | None = None


class MemoryReviewResult(BaseModel):
    agent_id: str
    user_id: str | None = None
    memory_count: int = 0
    duplicate_group_count: int = 0
    duplicate_groups: list[MemoryDuplicateGroup] = Field(default_factory=list)
    profile_snapshot: MemoryProfileRecord | None = None
    notes: list[str] = Field(default_factory=list)


class MemoryConsolidationResult(BaseModel):
    agent_id: str
    user_id: str | None = None
    reviewed_count: int = 0
    merged_group_count: int = 0
    dry_run: bool = True
    updated_memories: list[MemoryFact] = Field(default_factory=list)
    deleted_memory_ids: list[str] = Field(default_factory=list)
    duplicate_groups: list[MemoryDuplicateGroup] = Field(default_factory=list)
    profile_snapshot: MemoryProfileRecord | None = None
    notes: list[str] = Field(default_factory=list)


class MemoryRetrievalResult(BaseModel):
    user_id: str
    intent: ChatIntent = ChatIntent.GENERAL
    candidate_count: int = 0
    selected_hits: list[MemoryFact] = Field(default_factory=list)
    profile: MemoryProfileSnapshot = Field(default_factory=MemoryProfileSnapshot)
    retrieval_notes: list[str] = Field(default_factory=list)


MemoryRetrieverStatus = Literal["success", "not_configured", "error"]


class MemoryHit(BaseModel):
    """Review-safe retrieval result from a MemoryRetriever.

    Carries only the reviewer-safe surface: a memory fact, its type,
    a retrieval relevance score, evidence refs, and source provenance.
    No raw transcript content, no private metadata, no embedding vectors.
    """

    hit_id: str = Field(default_factory=lambda: new_id("mhit"))
    memory_id: str = Field(..., min_length=1)
    fact: str = Field(..., min_length=1)
    memory_type: MemoryType = MemoryType.FACT
    score: float = Field(default=0.0, ge=0.0, le=1.0)
    evidence_refs: list[str] = Field(default_factory=list)
    source: str = Field(..., min_length=1)


class MemoryRetrieverResult(BaseModel):
    """Contract-level result from a MemoryRetriever.retrieve() call.

    Contains selected MemoryHit items and retrieval metadata.
    This is the protocol-level counterpart to MemoryRetrievalResult
    (which is the service-level result from MemoryRetrievalService).
    """

    status: MemoryRetrieverStatus = "success"
    contact_id: str | None = None
    hits: list[MemoryHit] = Field(default_factory=list)
    candidate_count: int = 0
    notes: list[str] = Field(default_factory=list)


class ActionPlan(BaseModel):
    action_id: str = Field(default_factory=lambda: new_id("act"))
    kind: ActionKind
    channel_id: str
    message_text: str | None = None
    requires_approval: bool = True
    metadata: dict[str, Any] = Field(default_factory=dict)


class PolicyDecision(BaseModel):
    allowed: bool = True
    requires_approval: bool = True
    draft_only: bool = False
    risk_flags: list[str] = Field(default_factory=list)
    reason: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class ActionExecutionRecord(BaseModel):
    action_id: str = Field(default_factory=lambda: new_id("act"))
    agent_id: str
    event_id: str | None = None
    kind: ActionKind
    status: ActionStatus = ActionStatus.PENDING_APPROVAL
    platform: Platform
    channel_id: str
    channel_type: ChannelType
    account_id: str
    actor_id: str | None = None
    connector_name: str | None = None
    message_text: str | None = None
    requires_approval: bool = True
    policy_decision: PolicyDecision = Field(default_factory=PolicyDecision)
    delivery_connector_name: str | None = None
    delivery_response: dict[str, Any] = Field(default_factory=dict)
    error_message: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)
    approved_at: datetime | None = None
    sent_at: datetime | None = None


class AgentTurnResult(BaseModel):
    agent_id: str
    event_id: str
    should_reply: bool
    context: ChatContext | None = None
    suggestions: list[ChatSuggestion] = Field(default_factory=list)
    actions: list[ActionPlan] = Field(default_factory=list)
    memory_hits: list[MemoryFact] = Field(default_factory=list)
    memory_updates: list[MemoryFact] = Field(default_factory=list)
    no_reply_reason: str | None = None
    reasoning: str


class AuditLogEntry(BaseModel):
    audit_id: str = Field(default_factory=lambda: new_id("aud"))
    agent_id: str | None = None
    action: str
    status: str
    details: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=utc_now)


ReplyFeedbackAction = Literal["accept", "edit", "reject", "boundary"]


class ReplyFeedbackRecord(BaseModel):
    feedback_id: str = Field(default_factory=lambda: new_id("fb"))
    created_at: datetime = Field(default_factory=utc_now)
    contact_id: str = Field(..., min_length=1)
    reply_plan_id: str | None = None
    candidate_id: str = Field(..., min_length=1)
    priority_rank: int = Field(..., ge=1)
    action: ReplyFeedbackAction
    user_note: str | None = None
    edited_text: str | None = None
    boundary_label: str | None = None
    boundary_note: str | None = None
    source_plan_path: str | None = None


class ReplyFeedbackLog(BaseModel):
    schema_version: str = "reply_feedback_log_v1"
    generated_at: datetime = Field(default_factory=utc_now)
    records: list[ReplyFeedbackRecord] = Field(default_factory=list)


PreferencePatchType = Literal[
    "tone_preference",
    "length_preference",
    "boundary_preference",
    "topic_preference",
    "question_style",
    "humor_style",
    "repair_style",
    "proactivity_preference",
]


class PreferencePatchCandidate(BaseModel):
    schema_version: str = "preference_patch_candidate_v1"
    patch_id: str = Field(default_factory=lambda: new_id("patch"))
    contact_id: str = Field(..., min_length=1)
    patch_type: PreferencePatchType
    instruction_scope: str = "per_contact"
    claim: str = Field(..., min_length=1)
    behavior_instruction: str = Field(..., min_length=1)
    rationale_summary: str | None = None
    supporting_feedback_ids: list[str] = Field(..., min_length=1)
    supporting_cluster_ids: list[str] = Field(default_factory=list)
    positive_examples: list[str] = Field(default_factory=list)
    negative_examples: list[str] = Field(default_factory=list)
    affected_candidate_types: list[str] = Field(default_factory=list)
    status: DistillationStatus = "candidate"
    confidence: float = Field(..., ge=0.0, le=1.0)
    sensitivity: DistillationSensitivity
    review_metadata: DistilledArtifactReviewMetadata = Field(
        default_factory=DistilledArtifactReviewMetadata,
    )
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)

    def is_runtime_ready(self) -> bool:
        return self.review_metadata.is_runtime_ready(status=self.status)


class CommunicationStyleSnapshot(BaseModel):
    message_length: str | None = None
    tone: str | None = None
    response_latency: str | None = None
    directness: str | None = None


class PartnerPersonaBrief(BaseModel):
    contact_id: str = Field(..., min_length=1)
    relationship_type: ContactRelationshipType
    relationship_state_summary: str = Field(..., min_length=1)
    communication_style_snapshot: CommunicationStyleSnapshot = Field(default_factory=CommunicationStyleSnapshot)
    preferred_topics: list[str] = Field(default_factory=list)
    emotional_pattern_labels: list[str] = Field(default_factory=list)
    evidence_refs: list[str] = Field(default_factory=list)
    source_skill_record_id: str = Field(..., min_length=1)


class CommunicationPolicyBrief(BaseModel):
    contact_id: str = Field(..., min_length=1)
    default_approach: str | None = None
    cold_contact_approach: str | None = None
    topic_opener_approach: str | None = None
    sensitive_topic_approach: str | None = None
    user_goal: str | None = None
    preferred_reply_style: str | None = None
    stable_preference_hints: list[str] = Field(default_factory=list)
    approved_patch_hints: list[ApprovedPatchBrief] = Field(default_factory=list)
    evidence_refs: list[str] = Field(default_factory=list)
    source_skill_record_id: str = Field(..., min_length=1)


class BoundaryProfileBrief(BaseModel):
    contact_id: str = Field(..., min_length=1)
    avoid_topics: list[str] = Field(default_factory=list)
    boundary_rules: list[str] = Field(default_factory=list)
    disallowed_uses: list[str] = Field(default_factory=list)
    usage_notes: list[str] = Field(default_factory=list)
    important_event_summaries: list[str] = Field(default_factory=list)
    sensitivity_summary: DistillationSensitivity = "low"
    evidence_refs: list[str] = Field(default_factory=list)
    source_skill_record_id: str = Field(..., min_length=1)


InteractionTemperature = Literal["warm", "neutral", "cold", "mixed", "unknown"]

RelationshipDeltaDirection = Literal["increase", "decrease", "stable", "unknown"]

RELATIONSHIP_DIMENSION_NAMES = Literal[
    "familiarity",
    "trust",
    "warmth",
    "reciprocity",
    "conflict_level",
    "boundary_risk",
    "initiative_allowance",
    "intimacy_level",
]


class RelationshipState(BaseModel):
    schema_version: str = "relationship_state_v1"
    state_id: str = Field(default_factory=lambda: new_id("relstate"))
    contact_id: str = Field(..., min_length=1)

    familiarity: float = Field(..., ge=0.0, le=1.0)
    trust: float = Field(..., ge=0.0, le=1.0)
    warmth: float = Field(..., ge=0.0, le=1.0)
    reciprocity: float = Field(..., ge=0.0, le=1.0)
    conflict_level: float = Field(..., ge=0.0, le=1.0)
    boundary_risk: float = Field(..., ge=0.0, le=1.0)
    initiative_allowance: float = Field(..., ge=0.0, le=1.0)
    intimacy_level: float = Field(..., ge=0.0, le=1.0)

    uncertainty: float = Field(..., ge=0.0, le=1.0)
    recent_interaction_temperature: InteractionTemperature = "unknown"

    first_interaction_at: datetime | None = None
    last_interaction_at: datetime | None = None
    assessed_at: datetime = Field(default_factory=utc_now)

    evidence_refs: list[str] = Field(..., min_length=1)
    assessment_rationale: str | None = None

    source_type: Literal["heuristic", "signal_extractor", "manual", "unknown"] = "unknown"
    source_skill_record_id: str | None = None

    status: DistillationStatus = "candidate"
    review_metadata: DistilledArtifactReviewMetadata = Field(
        default_factory=DistilledArtifactReviewMetadata,
    )

    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)

    def is_runtime_ready(self) -> bool:
        return self.review_metadata.is_runtime_ready(status=self.status)

    def dimension_snapshot(self) -> dict[str, float]:
        return {
            "familiarity": self.familiarity,
            "trust": self.trust,
            "warmth": self.warmth,
            "reciprocity": self.reciprocity,
            "conflict_level": self.conflict_level,
            "boundary_risk": self.boundary_risk,
            "initiative_allowance": self.initiative_allowance,
            "intimacy_level": self.intimacy_level,
        }


class RelationshipContextPersonaSnapshot(BaseModel):
    persona_id: str
    display_name: str
    truth_disclosure: PersonaTruthDisclosure = "fictional_ai_persona"
    source_risk_tier: PersonaRiskTier
    runtime_ready: bool = False
    safety_warnings: list[str] = Field(default_factory=list)

    @classmethod
    def from_persona_card(cls, persona: PersonaCard) -> "RelationshipContextPersonaSnapshot":
        warnings: list[str] = []
        if persona.source_policy.blocked_real_person_similarity:
            warnings.append("blocked_real_person_similarity")
        if persona.source_policy.source_type == "prohibited":
            warnings.append("prohibited_persona_source")
        return cls(
            persona_id=persona.persona_id,
            display_name=persona.display_name,
            truth_disclosure=persona.truth_disclosure,
            source_risk_tier=persona.source_policy.risk_tier,
            runtime_ready=persona.is_runtime_ready(),
            safety_warnings=warnings,
        )


class RelationshipContextMemorySnapshot(BaseModel):
    bundle_id: str
    purpose: MemoryRetrievalPurpose
    selected_memory_ids: list[str] = Field(default_factory=list)
    truth_status_counts: dict[str, int] = Field(default_factory=dict)
    imagined_memory_count: int = 0
    safety_warnings: list[str] = Field(default_factory=list)

    @classmethod
    def from_memory_bundle(cls, memory_bundle: MemoryRetrievalBundle) -> "RelationshipContextMemorySnapshot":
        return cls(
            bundle_id=memory_bundle.bundle_id,
            purpose=memory_bundle.purpose,
            selected_memory_ids=list(memory_bundle.selected_memory_ids),
            truth_status_counts=dict(memory_bundle.truth_status_counts),
            imagined_memory_count=memory_bundle.imagined_memory_count,
            safety_warnings=list(memory_bundle.safety_warnings),
        )


class RelationshipContextBundle(BaseModel):
    schema_version: str = "relationship_context_bundle_v1"
    context_bundle_id: str = Field(default_factory=lambda: new_id("relctx"))
    user_id: str = Field(..., min_length=1)
    persona: RelationshipContextPersonaSnapshot
    relationship_dimensions: dict[str, float] = Field(default_factory=dict)
    memory: RelationshipContextMemorySnapshot
    safety_warnings: list[str] = Field(default_factory=list)
    source_persona_id: str
    source_relationship_state_id: str
    source_memory_bundle_id: str
    generated_at: datetime = Field(default_factory=utc_now)

    @classmethod
    def from_sources(
        cls,
        *,
        user_id: str,
        persona: PersonaCard,
        relationship_state: RelationshipState,
        memory_bundle: MemoryRetrievalBundle,
    ) -> "RelationshipContextBundle":
        return cls(
            user_id=user_id,
            persona=RelationshipContextPersonaSnapshot.from_persona_card(persona),
            relationship_dimensions=relationship_state.dimension_snapshot(),
            memory=RelationshipContextMemorySnapshot.from_memory_bundle(memory_bundle),
            safety_warnings=list(memory_bundle.safety_warnings),
            source_persona_id=persona.persona_id,
            source_relationship_state_id=relationship_state.state_id,
            source_memory_bundle_id=memory_bundle.bundle_id,
        )

    @model_validator(mode="after")
    def validate_relationship_context_bundle(self) -> "RelationshipContextBundle":
        if not self.persona.runtime_ready:
            raise ValueError("relationship context bundle requires runtime-ready PersonaCard")
        if self.memory.purpose == "factual_response" and self.memory.imagined_memory_count:
            raise ValueError("factual relationship context cannot include imagined memory")
        forbidden_dimension_names = {"retention_score", "manipulation_score", "engagement_score"}
        if forbidden_dimension_names.intersection(self.relationship_dimensions):
            raise ValueError("relationship dimensions must not include retention or manipulation scores")
        return self


class ProactiveQuietHours(BaseModel):
    timezone: str = Field(default="UTC", min_length=1)
    start: str | None = None
    end: str | None = None


class ProactiveConsent(BaseModel):
    schema_version: str = "proactive_consent_v1"
    consent_id: str = Field(default_factory=lambda: new_id("proconsent"))
    user_id: str = Field(..., min_length=1)
    status: ProactiveConsentStatus = "disabled"
    allowed_surfaces: list[ProactiveConsentSurface] = Field(default_factory=list)
    allowed_intents: list[ProactiveConsentIntent] = Field(default_factory=list)
    quiet_hours: ProactiveQuietHours = Field(default_factory=ProactiveQuietHours)
    max_suggestions_per_day: int = Field(default=0, ge=0, le=3)
    min_interval_hours: float = Field(default=24.0, ge=0.0)
    requires_human_review: bool = True
    pause_reasons: list[str] = Field(default_factory=list)
    revoked_at: datetime | None = None
    safety_notes: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)

    @model_validator(mode="after")
    def validate_proactive_consent(self) -> "ProactiveConsent":
        if not self.requires_human_review:
            raise ValueError("proactive consent requires human review")
        if self.status == "enabled":
            if not self.allowed_surfaces:
                raise ValueError("enabled proactive consent requires at least one local review surface")
            if not self.allowed_intents:
                raise ValueError("enabled proactive consent requires at least one low-pressure intent")
        if self.status == "revoked" and self.revoked_at is None:
            raise ValueError("revoked proactive consent requires revoked_at")
        return self


class AIGCDisclosureMetadata(BaseModel):
    schema_version: str = "aigc_disclosure_v1"
    aigc_label: AIGCLabel = "ai_generated"
    disclosure_text: str = "AI-generated imagined companion content for review."
    disclosure_labels: list[str] = Field(
        default_factory=lambda: [
            "ai_generated",
            "imagined_content",
            "review_required",
            "not_real_world_activity",
        ],
    )

    @model_validator(mode="after")
    def validate_aigc_disclosure_metadata(self) -> "AIGCDisclosureMetadata":
        required_labels = {"ai_generated", "imagined_content", "review_required", "not_real_world_activity"}
        if not required_labels.issubset(set(self.disclosure_labels)):
            raise ValueError("AIGC disclosure metadata missing required labels")
        if "AI-generated" not in self.disclosure_text or "imagined" not in self.disclosure_text.lower():
            raise ValueError("AIGC disclosure text must mention AI-generated imagined content")
        return self


class AIGCLabelingRequirement(BaseModel):
    schema_version: str = "aigc_labeling_requirement_v1"
    requirement_id: str = Field(default_factory=lambda: new_id("aigclabel"))
    user_id: str = Field(..., min_length=1)
    content_id: str = Field(..., min_length=1)
    content_modality: AIGCContentModality
    product_surface: AIGCProductSurface
    visible_label_required: Literal[True] = True
    visible_label_text: str = "AI-generated synthetic content."
    disclosure_labels: list[str] = Field(
        default_factory=lambda: [
            "ai_generated",
            "synthetic_content",
            "review_required",
        ],
    )
    metadata_label_required: bool = False
    metadata_labels: list[str] = Field(default_factory=list)
    copy_download_export_share_requires_metadata: bool = False
    review_required: Literal[True] = True
    source_refs: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=utc_now)

    @classmethod
    def from_disclosure_labels(
        cls,
        *,
        user_id: str,
        content_id: str,
        content_modality: AIGCContentModality,
        product_surface: AIGCProductSurface,
        disclosure_labels: list[str],
        source_refs: list[str] | None = None,
    ) -> "AIGCLabelingRequirement":
        return cls(
            user_id=user_id,
            content_id=content_id,
            content_modality=content_modality,
            product_surface=product_surface,
            disclosure_labels=disclosure_labels,
            source_refs=source_refs or [],
        )

    @model_validator(mode="after")
    def validate_aigc_labeling_requirement(self) -> "AIGCLabelingRequirement":
        labels = set(self.disclosure_labels)
        labels.update({"ai_generated", "synthetic_content", "review_required"})
        is_imagined_role_life = self.content_modality in {
            "virtual_history",
            "role_dynamic_post",
        } or self.product_surface in {
            "virtual_history",
            "role_dynamic_post",
        }
        if is_imagined_role_life:
            labels.update({"imagined_content", "not_real_world_activity"})
            self.visible_label_text = "AI-generated synthetic imagined companion content. Not real-world activity."

        ordered_labels = [
            label
            for label in [
                "ai_generated",
                "synthetic_content",
                "imagined_content",
                "review_required",
                "not_real_world_activity",
            ]
            if label in labels
        ]
        ordered_labels.extend(label for label in self.disclosure_labels if label not in ordered_labels)
        self.disclosure_labels = _ordered_unique(ordered_labels)

        if self.content_modality in {"image", "audio", "video", "virtual_scene", "export", "shared_content"} or (
            self.product_surface in {"export_manifest", "shared_content", "voice_avatar"}
        ):
            self.metadata_label_required = True
            self.copy_download_export_share_requires_metadata = True
            self.metadata_labels = _ordered_unique([*self.metadata_labels, "implicit_metadata_label"])

        if "AI-generated" not in self.visible_label_text or "synthetic" not in self.visible_label_text.lower():
            raise ValueError("AIGC visible label text must mention AI-generated synthetic content")
        return self


class VoicePreferenceState(BaseModel):
    schema_version: str = "voice_preference_state_v1"
    preference_id: str = Field(default_factory=lambda: new_id("voicepref"))
    user_id: str = Field(..., min_length=1)
    voice_mode: VoiceMode = "disabled"
    source_route: VoiceSourceRoute = "disabled"
    requested_likeness_type: VoiceRequestedLikenessType = "none"
    required_consent_scope: Literal["voice_avatar"] = "voice_avatar"
    has_active_voice_avatar_consent: bool = False
    decision: VoiceConsentDecision = "disabled"
    voice_enabled: Literal[False] = False
    review_required: Literal[True] = True
    visible_label_text: str = "AI-generated synthetic voice. Not a human voice."
    disclosure_labels: list[str] = Field(
        default_factory=lambda: [
            "ai_generated",
            "synthetic_content",
            "audio",
            "voice_avatar",
            "review_required",
        ],
    )
    metadata_label_required: bool = True
    metadata_labels: list[str] = Field(default_factory=lambda: ["implicit_metadata_label"])
    copy_download_export_share_requires_metadata: bool = True
    aigc_labeling_requirement: AIGCLabelingRequirement | None = None
    safety_decision_action: VoiceSafetyDecisionAction = "allow_for_review"
    safety_reason_labels: list[str] = Field(default_factory=list)
    blocked_reason_labels: list[str] = Field(default_factory=list)
    consent_evidence_refs: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=utc_now)

    @model_validator(mode="after")
    def validate_voice_preference_state(self) -> "VoicePreferenceState":
        labels = _ordered_unique(
            [
                *self.disclosure_labels,
                "ai_generated",
                "synthetic_content",
                "audio",
                "voice_avatar",
                "review_required",
                "implicit_metadata_label",
            ]
        )
        self.disclosure_labels = labels
        self.metadata_label_required = True
        self.metadata_labels = _ordered_unique([*self.metadata_labels, "implicit_metadata_label"])
        self.copy_download_export_share_requires_metadata = True

        blocked_reasons = list(self.blocked_reason_labels)
        if not self.has_active_voice_avatar_consent:
            blocked_reasons.append("voice_avatar_consent_required")

        blocked_likeness_types = {
            "real_person",
            "deceased_person",
            "public_figure",
            "family_member",
            "ex_partner",
        }
        if self.requested_likeness_type in blocked_likeness_types:
            blocked_reasons.append("real_person_voice_likeness_blocked")

        if self.source_route == "blocked_voice_clone":
            blocked_reasons.append("voice_clone_blocked")

        if self.source_route in {
            "generated_fictional_voice",
            "recorded_user_voice",
            "third_party_authorized_voice",
        }:
            blocked_reasons.append("future_voice_route_requires_policy_review")

        if self.safety_decision_action in {"block", "deescalate_for_review"}:
            blocked_reasons.append("voice_blocked_by_safety_decision")

        self.blocked_reason_labels = _ordered_unique(blocked_reasons)

        if self.source_route == "disabled":
            self.voice_mode = "disabled"
            self.decision = "disabled"
        elif self.blocked_reason_labels:
            self.voice_mode = self.source_route
            self.decision = "blocked"
        elif self.source_route == "non_real_synthetic_voice":
            self.voice_mode = "non_real_synthetic_voice"
            self.decision = "review_required"
        else:
            self.voice_mode = self.source_route
            self.decision = "blocked"
            self.blocked_reason_labels = _ordered_unique(
                [*self.blocked_reason_labels, "unsupported_voice_route"]
            )

        if self.source_route != "disabled" and self.aigc_labeling_requirement is None:
            self.aigc_labeling_requirement = AIGCLabelingRequirement(
                user_id=self.user_id,
                content_id=f"voice_content_{self.preference_id}",
                content_modality="audio",
                product_surface="voice_avatar",
                visible_label_text=self.visible_label_text,
                disclosure_labels=[
                    "ai_generated",
                    "synthetic_content",
                    "review_required",
                ],
                source_refs=[self.preference_id],
            )

        if "AI-generated" not in self.visible_label_text or "synthetic" not in self.visible_label_text.lower():
            raise ValueError("voice visible label text must mention AI-generated synthetic voice")
        return self


class VoiceConsentPolicy(BaseModel):
    schema_version: str = "voice_consent_policy_v1"
    policy_id: str = Field(default_factory=lambda: new_id("voicepolicy"))
    required_consent_scope: Literal["voice_avatar"] = "voice_avatar"
    allowed_source_routes: list[VoiceSourceRoute] = Field(default_factory=lambda: ["non_real_synthetic_voice"])
    deferred_source_routes: list[VoiceSourceRoute] = Field(
        default_factory=lambda: [
            "generated_fictional_voice",
            "recorded_user_voice",
            "third_party_authorized_voice",
        ],
    )
    blocked_source_routes: list[VoiceSourceRoute] = Field(default_factory=lambda: ["blocked_voice_clone"])
    blocked_likeness_types: list[VoiceRequestedLikenessType] = Field(
        default_factory=lambda: [
            "real_person",
            "deceased_person",
            "public_figure",
            "family_member",
            "ex_partner",
        ],
    )
    visible_label_text: str = "AI-generated synthetic voice. Not a human voice."
    review_required: Literal[True] = True

    def evaluate(
        self,
        *,
        user_id: str,
        source_route: VoiceSourceRoute,
        consent_state: ConsentCenterState | None = None,
        requested_likeness_type: VoiceRequestedLikenessType = "none",
        safety_decision_action: VoiceSafetyDecisionAction = "allow_for_review",
        safety_reasons: list[str] | None = None,
    ) -> VoicePreferenceState:
        has_voice_consent = (
            consent_state is not None
            and consent_state.user_id == user_id
            and consent_state.has_active_consent(self.required_consent_scope)
        )
        consent_refs: list[str] = []
        if consent_state is not None and consent_state.user_id == user_id:
            consent_refs = [
                ref
                for grant in consent_state.grants
                if grant.feature_scope == self.required_consent_scope
                for ref in grant.evidence_refs
            ]

        blocked_reasons: list[str] = []
        if consent_state is not None and consent_state.user_id != user_id:
            blocked_reasons.append("voice_consent_user_mismatch")
        if source_route in self.blocked_source_routes:
            blocked_reasons.append("voice_clone_blocked")
        if requested_likeness_type in self.blocked_likeness_types:
            blocked_reasons.append("real_person_voice_likeness_blocked")
        if source_route in self.deferred_source_routes:
            blocked_reasons.append("future_voice_route_requires_policy_review")

        return VoicePreferenceState(
            user_id=user_id,
            voice_mode=source_route,
            source_route=source_route,
            requested_likeness_type=requested_likeness_type,
            has_active_voice_avatar_consent=has_voice_consent,
            visible_label_text=self.visible_label_text,
            safety_decision_action=safety_decision_action,
            safety_reason_labels=safety_reasons or [],
            blocked_reason_labels=blocked_reasons,
            consent_evidence_refs=_ordered_unique(consent_refs),
        )


class RoleDynamicPost(BaseModel):
    schema_version: str = "role_dynamic_post_v1"
    post_id: str = Field(default_factory=lambda: new_id("rolepost"))
    user_id: str = Field(..., min_length=1)
    persona_id: str = Field(..., min_length=1)
    content_text: str = Field(..., min_length=1)
    content_status: PersonaVirtualContentStatus = "imagined_ai_generated"
    truth_disclosure: RoleDynamicPostTruthDisclosure = "imagined_ai_generated_content"
    review_status: RoleDynamicPostReviewStatus = "requires_review"
    visibility: RoleDynamicPostVisibility = "local_private_review"
    memory_refs: list[str] = Field(default_factory=list)
    memory_ref_usage: RoleDynamicMemoryRefUsage = "inspiration_only"
    relationship_context_refs: list[str] = Field(default_factory=list)
    source_prompt_summary: str | None = None
    aigc_metadata: AIGCDisclosureMetadata = Field(default_factory=AIGCDisclosureMetadata)
    contains_factual_claims: bool = False
    factual_claims_review_notes: list[str] = Field(default_factory=list)
    safety_notes: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)

    @model_validator(mode="after")
    def validate_role_dynamic_post(self) -> "RoleDynamicPost":
        if self.contains_factual_claims and not self.factual_claims_review_notes:
            raise ValueError("factual claims in imagined posts require review notes")
        return self


class RelationshipDeltaDimension(BaseModel):
    dimension_name: RELATIONSHIP_DIMENSION_NAMES
    current_value: float = Field(..., ge=0.0, le=1.0)
    proposed_value: float = Field(..., ge=0.0, le=1.0)
    direction: RelationshipDeltaDirection = "unknown"
    magnitude: float = Field(default=0.0, ge=0.0, le=1.0)
    rationale: str | None = None


class RelationshipDeltaCandidate(BaseModel):
    schema_version: str = "relationship_delta_candidate_v1"
    delta_id: str = Field(default_factory=lambda: new_id("reldelta"))
    contact_id: str = Field(..., min_length=1)
    source_state_id: str = Field(..., min_length=1)

    dimension_changes: list[RelationshipDeltaDimension] = Field(..., min_length=1)
    delta_rationale: str = Field(..., min_length=1)

    evidence_refs: list[str] = Field(..., min_length=1)
    signal_refs: list[str] = Field(default_factory=list)

    status: DistillationStatus = "candidate"
    review_metadata: DistilledArtifactReviewMetadata = Field(
        default_factory=DistilledArtifactReviewMetadata,
    )

    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)

    def is_runtime_ready(self) -> bool:
        return self.review_metadata.is_runtime_ready(status=self.status)


RelationshipSignalProvenance = Literal[
    "feedback_boundary",
    "feedback_action",
    "metadata_derived",
    "unknown",
]


class RelationshipSignal(BaseModel):
    signal_id: str = Field(default_factory=lambda: new_id("relsig"))
    contact_id: str = Field(..., min_length=1)
    dimension_name: RELATIONSHIP_DIMENSION_NAMES
    direction: RelationshipDeltaDirection = "unknown"
    strength: float = Field(..., ge=0.0, le=1.0)
    evidence_refs: list[str] = Field(..., min_length=1)
    provenance: RelationshipSignalProvenance = "unknown"
    signal_description: str | None = None
    status: DistillationStatus = "candidate"
    review_metadata: DistilledArtifactReviewMetadata = Field(
        default_factory=DistilledArtifactReviewMetadata,
    )
    created_at: datetime = Field(default_factory=utc_now)

    def is_runtime_ready(self) -> bool:
        return self.review_metadata.is_runtime_ready(status=self.status)


ChatContext.model_rebuild()
AgentTurnResult.model_rebuild()
MeetingLivePreview.model_rebuild()
