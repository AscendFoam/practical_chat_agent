from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.mysql import JSON
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class AgentModel(Base):
    __tablename__ = "agents"

    agent_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    display_name: Mapped[str] = mapped_column(String(255))
    persona_type: Mapped[str] = mapped_column(String(32))
    system_identity: Mapped[str] = mapped_column(String(64))
    public_disclosure: Mapped[str | None] = mapped_column(Text(), nullable=True)
    relationship_mode: Mapped[str] = mapped_column(String(64))
    safety_mode: Mapped[str] = mapped_column(String(32))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class AgentProfileModel(Base):
    __tablename__ = "agent_profiles"

    agent_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("agents.agent_id", ondelete="CASCADE"),
        primary_key=True,
    )
    core_traits: Mapped[list[str]] = mapped_column(JSON)
    speech_style: Mapped[dict[str, Any]] = mapped_column(JSON)
    interests: Mapped[list[str]] = mapped_column(JSON)
    do_not_do: Mapped[list[str]] = mapped_column(JSON)


class EventModel(Base):
    __tablename__ = "events"

    event_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(64), index=True)
    source_type: Mapped[str] = mapped_column(String(32))
    platform: Mapped[str] = mapped_column(String(32))
    channel_id: Mapped[str] = mapped_column(String(128), index=True)
    channel_type: Mapped[str] = mapped_column(String(32))
    account_id: Mapped[str] = mapped_column(String(128))
    actor_id: Mapped[str] = mapped_column(String(128), index=True)
    actor_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    direction: Mapped[str] = mapped_column(String(16))
    content_type: Mapped[str] = mapped_column(String(32))
    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    text_body: Mapped[str | None] = mapped_column(Text(), nullable=True)
    attachments: Mapped[list[dict[str, Any]]] = mapped_column(JSON)
    raw_payload: Mapped[dict[str, Any]] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class MemoryModel(Base):
    __tablename__ = "memories"

    memory_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    agent_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("agents.agent_id", ondelete="CASCADE"),
        index=True,
    )
    user_id: Mapped[str] = mapped_column(String(128), index=True)
    memory_type: Mapped[str] = mapped_column(String(32))
    scope: Mapped[str] = mapped_column(String(32))
    salience: Mapped[float]
    confidence: Mapped[float]
    fact: Mapped[str] = mapped_column(Text())
    evidence_refs: Mapped[list[str]] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class MemoryProfileModel(Base):
    __tablename__ = "memory_profiles"

    profile_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    agent_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("agents.agent_id", ondelete="CASCADE"),
        index=True,
    )
    user_id: Mapped[str] = mapped_column(String(128), index=True)
    source_event_id: Mapped[str | None] = mapped_column(
        String(64),
        ForeignKey("events.event_id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    backend: Mapped[str] = mapped_column(String(128), index=True)
    model: Mapped[str | None] = mapped_column(String(128), nullable=True)
    summary: Mapped[str | None] = mapped_column(Text(), nullable=True)
    memory_count: Mapped[int]
    snapshot_payload: Mapped[dict[str, Any]] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)


class AuditLogModel(Base):
    __tablename__ = "audit_logs"

    audit_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    agent_id: Mapped[str | None] = mapped_column(
        String(64),
        ForeignKey("agents.agent_id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    action: Mapped[str] = mapped_column(String(64))
    status: Mapped[str] = mapped_column(String(32))
    details: Mapped[dict[str, Any]] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)


class ActionExecutionModel(Base):
    __tablename__ = "action_executions"

    action_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    agent_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("agents.agent_id", ondelete="CASCADE"),
        index=True,
    )
    event_id: Mapped[str | None] = mapped_column(
        String(64),
        ForeignKey("events.event_id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    kind: Mapped[str] = mapped_column(String(32), index=True)
    status: Mapped[str] = mapped_column(String(32), index=True)
    platform: Mapped[str] = mapped_column(String(32), index=True)
    channel_id: Mapped[str] = mapped_column(String(128), index=True)
    channel_type: Mapped[str] = mapped_column(String(32))
    account_id: Mapped[str] = mapped_column(String(128), index=True)
    actor_id: Mapped[str | None] = mapped_column(String(128), nullable=True, index=True)
    connector_name: Mapped[str | None] = mapped_column(String(64), nullable=True)
    message_text: Mapped[str | None] = mapped_column(Text(), nullable=True)
    requires_approval: Mapped[bool]
    policy_decision: Mapped[dict[str, Any]] = mapped_column(JSON)
    delivery_connector_name: Mapped[str | None] = mapped_column(String(64), nullable=True)
    delivery_response: Mapped[dict[str, Any]] = mapped_column(JSON)
    error_message: Mapped[str | None] = mapped_column(Text(), nullable=True)
    metadata_payload: Mapped[dict[str, Any]] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    approved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    sent_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, index=True)


class MeetingSessionModel(Base):
    __tablename__ = "meeting_sessions"

    session_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    connector_name: Mapped[str] = mapped_column(String(64), index=True)
    platform: Mapped[str] = mapped_column(String(32), index=True)
    account_id: Mapped[str] = mapped_column(String(128), index=True)
    meeting_key: Mapped[str] = mapped_column(String(255), index=True)
    meeting_title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    channel_id: Mapped[str] = mapped_column(String(255), index=True)
    audio_source: Mapped[str | None] = mapped_column(String(32), nullable=True)
    capture_backend: Mapped[str | None] = mapped_column(String(128), nullable=True)
    capture_device_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    transcription_backend: Mapped[str | None] = mapped_column(String(128), nullable=True)
    detected_window: Mapped[dict[str, Any]] = mapped_column(JSON)
    notes: Mapped[list[str]] = mapped_column(JSON)
    latest_summary: Mapped[str | None] = mapped_column(Text(), nullable=True)
    latest_key_points: Mapped[list[str]] = mapped_column(JSON)
    latest_action_items: Mapped[list[str]] = mapped_column(JSON)
    latest_follow_up_questions: Mapped[list[str]] = mapped_column(JSON)
    last_segment_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)


class MeetingSegmentModel(Base):
    __tablename__ = "meeting_segments"

    segment_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    session_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("meeting_sessions.session_id", ondelete="CASCADE"),
        index=True,
    )
    connector_name: Mapped[str] = mapped_column(String(64), index=True)
    platform: Mapped[str] = mapped_column(String(32), index=True)
    account_id: Mapped[str] = mapped_column(String(128), index=True)
    chunk_index: Mapped[int | None] = mapped_column(nullable=True)
    speaker_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    display_time: Mapped[str | None] = mapped_column(String(64), nullable=True)
    text_body: Mapped[str] = mapped_column(Text())
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, index=True)
    ended_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    audio_source: Mapped[str | None] = mapped_column(String(32), nullable=True)
    capture_device_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    saved_path: Mapped[str | None] = mapped_column(String(512), nullable=True)
    raw_payload: Mapped[dict[str, Any]] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)


class MeetingMinutesModel(Base):
    __tablename__ = "meeting_minutes"

    minutes_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    session_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("meeting_sessions.session_id", ondelete="CASCADE"),
        index=True,
    )
    template: Mapped[str] = mapped_column(String(32), index=True)
    title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    backend: Mapped[str] = mapped_column(String(128), index=True)
    model: Mapped[str | None] = mapped_column(String(128), nullable=True)
    status: Mapped[str] = mapped_column(String(32), index=True)
    output_path: Mapped[str | None] = mapped_column(String(512), nullable=True)
    markdown_body: Mapped[str] = mapped_column(Text())
    overview: Mapped[str | None] = mapped_column(Text(), nullable=True)
    background: Mapped[list[str]] = mapped_column(JSON)
    conclusions: Mapped[list[str]] = mapped_column(JSON)
    action_items: Mapped[list[str]] = mapped_column(JSON)
    risks: Mapped[list[str]] = mapped_column(JSON)
    raw_excerpt_ids: Mapped[list[str]] = mapped_column(JSON)
    raw_payload: Mapped[dict[str, Any]] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)


def create_schema(engine: Engine) -> None:
    Base.metadata.create_all(bind=engine)
