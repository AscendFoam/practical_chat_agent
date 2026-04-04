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


def create_schema(engine: Engine) -> None:
    Base.metadata.create_all(bind=engine)

