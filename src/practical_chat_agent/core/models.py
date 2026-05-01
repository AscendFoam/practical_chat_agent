from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

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
    summary: str | None = None


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


ChatContext.model_rebuild()
AgentTurnResult.model_rebuild()
MeetingLivePreview.model_rebuild()
