from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Literal

from pydantic import BaseModel, Field

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
