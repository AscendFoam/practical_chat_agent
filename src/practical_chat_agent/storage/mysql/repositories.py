from __future__ import annotations

from datetime import datetime

from sqlalchemy import desc, select
from sqlalchemy.orm import Session, sessionmaker

from practical_chat_agent.core.enums import (
    ActionKind,
    ActionStatus,
    ChannelType,
    ContentType,
    Direction,
    MeetingAudioSource,
    MemoryScope,
    MemoryType,
    PersonaType,
    Platform,
    SafetyMode,
    SourceType,
)
from practical_chat_agent.core.models import (
    ActionExecutionRecord,
    AgentProfile,
    AuditLogEntry,
    InboundEvent,
    MemoryFact,
    PolicyDecision,
)
from practical_chat_agent.core.models import (
    MeetingMinutesRecord,
    MeetingSegmentRecord,
    MeetingSessionRecord,
    MemoryProfileRecord,
    MemoryProfileSnapshot,
)
from practical_chat_agent.storage.mysql.models import (
    ActionExecutionModel,
    AgentModel,
    AgentProfileModel,
    AuditLogModel,
    EventModel,
    MeetingMinutesModel,
    MeetingSegmentModel,
    MeetingSessionModel,
    MemoryModel,
    MemoryProfileModel,
)
from practical_chat_agent.storage.repositories.base import (
    ActionRepository,
    AgentRepository,
    AuditRepository,
    EventRepository,
    MeetingRepository,
    MemoryRepository,
)


class SqlAlchemyEventRepository(EventRepository):
    def __init__(self, session_factory: sessionmaker[Session]) -> None:
        self.session_factory = session_factory

    def add(self, event: InboundEvent) -> None:
        with self.session_factory() as session:
            model = EventModel(
                event_id=event.event_id,
                tenant_id=event.tenant_id,
                source_type=event.source_type.value,
                platform=event.platform.value,
                channel_id=event.channel_id,
                channel_type=event.channel_type.value,
                account_id=event.account_id,
                actor_id=event.actor_id,
                actor_name=event.actor_name,
                direction=event.direction.value,
                content_type=event.content_type.value,
                occurred_at=event.occurred_at,
                text_body=event.text,
                attachments=event.attachments,
                raw_payload=event.raw,
                created_at=event.occurred_at,
            )
            session.merge(model)
            session.commit()

    def get(self, event_id: str) -> InboundEvent | None:
        with self.session_factory() as session:
            model = session.get(EventModel, event_id)
            return None if model is None else _to_event(model)

    def list_recent_for_channel(self, channel_id: str, *, limit: int = 20) -> list[InboundEvent]:
        with self.session_factory() as session:
            rows = session.scalars(
                select(EventModel)
                .where(EventModel.channel_id == channel_id)
                .order_by(desc(EventModel.occurred_at))
                .limit(limit),
            ).all()
            return [_to_event(row) for row in reversed(rows)]


class SqlAlchemyAgentRepository(AgentRepository):
    def __init__(self, session_factory: sessionmaker[Session]) -> None:
        self.session_factory = session_factory

    def upsert(self, profile: AgentProfile) -> None:
        with self.session_factory() as session:
            session.merge(
                AgentModel(
                    agent_id=profile.agent_id,
                    display_name=profile.display_name,
                    persona_type=profile.persona_type.value,
                    system_identity=profile.system_identity,
                    public_disclosure=profile.public_disclosure,
                    relationship_mode=profile.relationship_mode,
                    safety_mode=profile.safety_mode.value,
                    created_at=profile.created_at,
                    updated_at=profile.updated_at,
                ),
            )
            session.merge(
                AgentProfileModel(
                    agent_id=profile.agent_id,
                    core_traits=profile.core_traits,
                    speech_style=profile.speech_style,
                    interests=profile.interests,
                    do_not_do=profile.do_not_do,
                ),
            )
            session.commit()

    def get(self, agent_id: str) -> AgentProfile | None:
        with self.session_factory() as session:
            agent = session.get(AgentModel, agent_id)
            profile = session.get(AgentProfileModel, agent_id)
            if agent is None or profile is None:
                return None
            return AgentProfile(
                agent_id=agent.agent_id,
                display_name=agent.display_name,
                persona_type=PersonaType(agent.persona_type),
                system_identity=agent.system_identity,
                public_disclosure=agent.public_disclosure
                or "This account is operated by an AI persona.",
                core_traits=profile.core_traits,
                speech_style=profile.speech_style,
                interests=profile.interests,
                relationship_mode=agent.relationship_mode,
                safety_mode=SafetyMode(agent.safety_mode),
                do_not_do=profile.do_not_do,
                created_at=agent.created_at,
                updated_at=agent.updated_at,
            )


class SqlAlchemyMemoryRepository(MemoryRepository):
    def __init__(self, session_factory: sessionmaker[Session]) -> None:
        self.session_factory = session_factory

    def upsert(self, memory: MemoryFact) -> None:
        with self.session_factory() as session:
            session.merge(
                MemoryModel(
                    memory_id=memory.memory_id,
                    agent_id=memory.agent_id,
                    user_id=memory.user_id,
                    memory_type=memory.memory_type.value,
                    scope=memory.scope.value,
                    salience=memory.salience,
                    confidence=memory.confidence,
                    fact=memory.fact,
                    evidence_refs=memory.evidence_refs,
                    created_at=memory.created_at,
                    updated_at=memory.updated_at,
                ),
            )
            session.commit()

    def get(self, memory_id: str) -> MemoryFact | None:
        with self.session_factory() as session:
            row = session.get(MemoryModel, memory_id)
            return None if row is None else _to_memory(row)

    def list_for_user(self, *, agent_id: str, user_id: str, limit: int = 10) -> list[MemoryFact]:
        with self.session_factory() as session:
            rows = session.scalars(
                select(MemoryModel)
                .where(MemoryModel.agent_id == agent_id, MemoryModel.user_id == user_id)
                .order_by(desc(MemoryModel.updated_at))
                .limit(limit),
            ).all()
            return [_to_memory(row) for row in rows]

    def list_for_agent(
        self,
        *,
        agent_id: str,
        user_id: str | None = None,
        limit: int = 100,
    ) -> list[MemoryFact]:
        with self.session_factory() as session:
            statement = (
                select(MemoryModel)
                .where(MemoryModel.agent_id == agent_id)
                .order_by(desc(MemoryModel.updated_at))
                .limit(limit)
            )
            if user_id is not None:
                statement = (
                    select(MemoryModel)
                    .where(MemoryModel.agent_id == agent_id, MemoryModel.user_id == user_id)
                    .order_by(desc(MemoryModel.updated_at))
                    .limit(limit)
                )
            rows = session.scalars(statement).all()
            return [_to_memory(row) for row in rows]

    def delete(self, memory_id: str) -> None:
        with self.session_factory() as session:
            row = session.get(MemoryModel, memory_id)
            if row is not None:
                session.delete(row)
                session.commit()

    def add_profile_snapshot(self, profile: MemoryProfileRecord) -> MemoryProfileRecord:
        with self.session_factory() as session:
            session.merge(
                MemoryProfileModel(
                    profile_id=profile.profile_id,
                    agent_id=profile.agent_id,
                    user_id=profile.user_id,
                    source_event_id=profile.source_event_id,
                    backend=profile.backend,
                    model=profile.model,
                    summary=profile.summary,
                    memory_count=profile.memory_count,
                    snapshot_payload=profile.snapshot.model_dump(mode="json"),
                    created_at=profile.created_at,
                ),
            )
            session.commit()
            row = session.get(MemoryProfileModel, profile.profile_id)
            assert row is not None
            return _to_memory_profile(row)

    def get_profile_snapshot(self, profile_id: str) -> MemoryProfileRecord | None:
        with self.session_factory() as session:
            row = session.get(MemoryProfileModel, profile_id)
            return None if row is None else _to_memory_profile(row)

    def delete_profile_snapshot(self, profile_id: str) -> None:
        with self.session_factory() as session:
            row = session.get(MemoryProfileModel, profile_id)
            if row is not None:
                session.delete(row)
                session.commit()

    def get_latest_profile_snapshot(self, *, agent_id: str, user_id: str) -> MemoryProfileRecord | None:
        with self.session_factory() as session:
            row = session.scalars(
                select(MemoryProfileModel)
                .where(MemoryProfileModel.agent_id == agent_id, MemoryProfileModel.user_id == user_id)
                .order_by(desc(MemoryProfileModel.created_at))
                .limit(1),
            ).first()
            return None if row is None else _to_memory_profile(row)

    def list_profile_snapshots(
        self,
        *,
        agent_id: str,
        user_id: str,
        limit: int = 20,
    ) -> list[MemoryProfileRecord]:
        with self.session_factory() as session:
            rows = session.scalars(
                select(MemoryProfileModel)
                .where(MemoryProfileModel.agent_id == agent_id, MemoryProfileModel.user_id == user_id)
                .order_by(desc(MemoryProfileModel.created_at))
                .limit(limit),
            ).all()
            return [_to_memory_profile(row) for row in rows]


class SqlAlchemyAuditRepository(AuditRepository):
    def __init__(self, session_factory: sessionmaker[Session]) -> None:
        self.session_factory = session_factory

    def add(self, entry: AuditLogEntry) -> None:
        with self.session_factory() as session:
            session.merge(
                AuditLogModel(
                    audit_id=entry.audit_id,
                    agent_id=entry.agent_id,
                    action=entry.action,
                    status=entry.status,
                    details=entry.details,
                    created_at=entry.created_at,
                ),
            )
            session.commit()


class SqlAlchemyActionRepository(ActionRepository):
    def __init__(self, session_factory: sessionmaker[Session]) -> None:
        self.session_factory = session_factory

    def add(self, record: ActionExecutionRecord) -> ActionExecutionRecord:
        with self.session_factory() as session:
            session.merge(_to_action_model(record))
            session.commit()
            row = session.get(ActionExecutionModel, record.action_id)
            assert row is not None
            return _to_action_record(row)

    def get(self, action_id: str) -> ActionExecutionRecord | None:
        with self.session_factory() as session:
            row = session.get(ActionExecutionModel, action_id)
            return None if row is None else _to_action_record(row)

    def update(self, record: ActionExecutionRecord) -> ActionExecutionRecord:
        with self.session_factory() as session:
            session.merge(_to_action_model(record))
            session.commit()
            row = session.get(ActionExecutionModel, record.action_id)
            assert row is not None
            return _to_action_record(row)

    def list_recent(
        self,
        *,
        agent_id: str | None = None,
        status: str | None = None,
        channel_id: str | None = None,
        limit: int = 20,
    ) -> list[ActionExecutionRecord]:
        with self.session_factory() as session:
            statement = select(ActionExecutionModel).order_by(desc(ActionExecutionModel.created_at)).limit(limit)
            if agent_id is not None:
                statement = statement.where(ActionExecutionModel.agent_id == agent_id)
            if status is not None:
                statement = statement.where(ActionExecutionModel.status == status)
            if channel_id is not None:
                statement = statement.where(ActionExecutionModel.channel_id == channel_id)
            rows = session.scalars(statement).all()
            return [_to_action_record(row) for row in rows]


class SqlAlchemyMeetingRepository(MeetingRepository):
    def __init__(self, session_factory: sessionmaker[Session]) -> None:
        self.session_factory = session_factory

    def get_session_by_key(self, *, channel_id: str, meeting_key: str) -> MeetingSessionRecord | None:
        with self.session_factory() as session:
            row = session.scalars(
                select(MeetingSessionModel)
                .where(
                    MeetingSessionModel.channel_id == channel_id,
                    MeetingSessionModel.meeting_key == meeting_key,
                )
                .order_by(desc(MeetingSessionModel.updated_at))
                .limit(1),
            ).first()
            return None if row is None else _to_meeting_session(row)

    def get_session(self, *, session_id: str) -> MeetingSessionRecord | None:
        with self.session_factory() as session:
            row = session.get(MeetingSessionModel, session_id)
            return None if row is None else _to_meeting_session(row)

    def upsert_session(self, session_record: MeetingSessionRecord) -> MeetingSessionRecord:
        with self.session_factory() as session:
            session.merge(
                MeetingSessionModel(
                    session_id=session_record.session_id,
                    connector_name=session_record.connector_name,
                    platform=session_record.platform.value,
                    account_id=session_record.account_id,
                    meeting_key=session_record.meeting_key,
                    meeting_title=session_record.meeting_title,
                    channel_id=session_record.channel_id,
                    audio_source=session_record.audio_source.value if session_record.audio_source is not None else None,
                    capture_backend=session_record.capture_backend,
                    capture_device_name=session_record.capture_device_name,
                    transcription_backend=session_record.transcription_backend,
                    detected_window=session_record.detected_window,
                    notes=session_record.notes,
                    latest_summary=session_record.latest_summary,
                    latest_key_points=session_record.latest_key_points,
                    latest_action_items=session_record.latest_action_items,
                    latest_follow_up_questions=session_record.latest_follow_up_questions,
                    last_segment_at=session_record.last_segment_at,
                    created_at=session_record.created_at,
                    updated_at=session_record.updated_at,
                ),
            )
            session.commit()
            row = session.get(MeetingSessionModel, session_record.session_id)
            assert row is not None
            return _to_meeting_session(row)

    def add_segments(self, segments: list[MeetingSegmentRecord]) -> None:
        if not segments:
            return
        with self.session_factory() as session:
            for segment in segments:
                session.merge(
                    MeetingSegmentModel(
                        segment_id=segment.segment_id,
                        session_id=segment.session_id,
                        connector_name=segment.connector_name,
                        platform=segment.platform.value,
                        account_id=segment.account_id,
                        chunk_index=segment.chunk_index,
                        speaker_name=segment.speaker_name,
                        display_time=segment.display_time,
                        text_body=segment.text,
                        started_at=segment.started_at,
                        ended_at=segment.ended_at,
                        audio_source=segment.audio_source.value if segment.audio_source is not None else None,
                        capture_device_name=segment.capture_device_name,
                        saved_path=segment.saved_path,
                        raw_payload=segment.raw,
                        created_at=segment.created_at,
                    ),
                )
            session.commit()

    def list_segments(
        self,
        *,
        session_id: str,
        limit: int | None = None,
        started_after: datetime | None = None,
        started_before: datetime | None = None,
    ) -> list[MeetingSegmentRecord]:
        with self.session_factory() as session:
            statement = (
                select(MeetingSegmentModel)
                .where(MeetingSegmentModel.session_id == session_id)
                .order_by(MeetingSegmentModel.created_at.asc())
            )
            if started_after is not None:
                statement = statement.where(MeetingSegmentModel.started_at >= started_after)
            if started_before is not None:
                statement = statement.where(MeetingSegmentModel.started_at <= started_before)
            if limit is not None:
                statement = statement.limit(limit)
            rows = session.scalars(statement).all()
            return [_to_meeting_segment(row) for row in rows]

    def list_recent_segments(self, *, session_id: str, limit: int = 20) -> list[MeetingSegmentRecord]:
        with self.session_factory() as session:
            rows = session.scalars(
                select(MeetingSegmentModel)
                .where(MeetingSegmentModel.session_id == session_id)
                .order_by(desc(MeetingSegmentModel.created_at))
                .limit(limit),
            ).all()
            return [_to_meeting_segment(row) for row in reversed(rows)]

    def list_sessions(self, *, account_id: str | None = None, limit: int = 20) -> list[MeetingSessionRecord]:
        with self.session_factory() as session:
            statement = select(MeetingSessionModel).order_by(desc(MeetingSessionModel.updated_at)).limit(limit)
            if account_id:
                statement = (
                    select(MeetingSessionModel)
                    .where(MeetingSessionModel.account_id == account_id)
                    .order_by(desc(MeetingSessionModel.updated_at))
                    .limit(limit)
                )
            rows = session.scalars(statement).all()
            return [_to_meeting_session(row) for row in rows]

    def add_minutes(self, minutes: MeetingMinutesRecord) -> MeetingMinutesRecord:
        with self.session_factory() as session:
            session.merge(
                MeetingMinutesModel(
                    minutes_id=minutes.minutes_id,
                    session_id=minutes.session_id,
                    template=minutes.template.value,
                    title=minutes.title,
                    backend=minutes.backend,
                    model=minutes.model,
                    status=minutes.status,
                    output_path=minutes.output_path,
                    markdown_body=minutes.markdown_body,
                    overview=minutes.overview,
                    background=minutes.background,
                    conclusions=minutes.conclusions,
                    action_items=minutes.action_items,
                    risks=minutes.risks,
                    raw_excerpt_ids=minutes.raw_excerpt_ids,
                    raw_payload=minutes.raw,
                    created_at=minutes.created_at,
                ),
            )
            session.commit()
            row = session.get(MeetingMinutesModel, minutes.minutes_id)
            assert row is not None
            return _to_meeting_minutes(row)

    def get_minutes(self, *, minutes_id: str) -> MeetingMinutesRecord | None:
        with self.session_factory() as session:
            row = session.get(MeetingMinutesModel, minutes_id)
            if row is None:
                return None
            return _to_meeting_minutes(row)

    def list_minutes(self, *, session_id: str, limit: int = 20) -> list[MeetingMinutesRecord]:
        with self.session_factory() as session:
            rows = session.scalars(
                select(MeetingMinutesModel)
                .where(MeetingMinutesModel.session_id == session_id)
                .order_by(desc(MeetingMinutesModel.created_at))
                .limit(limit),
            ).all()
            return [_to_meeting_minutes(row) for row in rows]


def _to_event(model: EventModel) -> InboundEvent:
    return InboundEvent(
        event_id=model.event_id,
        tenant_id=model.tenant_id,
        source_type=SourceType(model.source_type),
        platform=Platform(model.platform),
        channel_id=model.channel_id,
        channel_type=ChannelType(model.channel_type),
        account_id=model.account_id,
        actor_id=model.actor_id,
        actor_name=model.actor_name,
        direction=Direction(model.direction),
        content_type=ContentType(model.content_type),
        occurred_at=model.occurred_at,
        text=model.text_body,
        attachments=model.attachments,
        raw=model.raw_payload,
    )


def _to_memory(model: MemoryModel) -> MemoryFact:
    return MemoryFact(
        memory_id=model.memory_id,
        agent_id=model.agent_id,
        user_id=model.user_id,
        memory_type=MemoryType(model.memory_type),
        scope=MemoryScope(model.scope),
        salience=model.salience,
        confidence=model.confidence,
        fact=model.fact,
        evidence_refs=model.evidence_refs,
        created_at=model.created_at,
        updated_at=model.updated_at,
    )


def _to_memory_profile(model: MemoryProfileModel) -> MemoryProfileRecord:
    payload = model.snapshot_payload or {}
    if isinstance(payload, MemoryProfileSnapshot):
        snapshot = payload
    else:
        snapshot = MemoryProfileSnapshot.model_validate(payload)
    return MemoryProfileRecord(
        profile_id=model.profile_id,
        agent_id=model.agent_id,
        user_id=model.user_id,
        source_event_id=model.source_event_id,
        backend=model.backend,
        model=model.model,
        summary=model.summary,
        snapshot=snapshot,
        memory_count=model.memory_count,
        created_at=model.created_at,
    )


def _to_action_model(record: ActionExecutionRecord) -> ActionExecutionModel:
    return ActionExecutionModel(
        action_id=record.action_id,
        agent_id=record.agent_id,
        event_id=record.event_id,
        kind=record.kind.value,
        status=record.status.value,
        platform=record.platform.value,
        channel_id=record.channel_id,
        channel_type=record.channel_type.value,
        account_id=record.account_id,
        actor_id=record.actor_id,
        connector_name=record.connector_name,
        message_text=record.message_text,
        requires_approval=record.requires_approval,
        policy_decision=record.policy_decision.model_dump(mode="json"),
        delivery_connector_name=record.delivery_connector_name,
        delivery_response=record.delivery_response,
        error_message=record.error_message,
        metadata_payload=record.metadata,
        created_at=record.created_at,
        updated_at=record.updated_at,
        approved_at=record.approved_at,
        sent_at=record.sent_at,
    )


def _to_action_record(model: ActionExecutionModel) -> ActionExecutionRecord:
    policy_payload = model.policy_decision or {}
    if isinstance(policy_payload, PolicyDecision):
        policy_decision = policy_payload
    else:
        policy_decision = PolicyDecision.model_validate(policy_payload)
    return ActionExecutionRecord(
        action_id=model.action_id,
        agent_id=model.agent_id,
        event_id=model.event_id,
        kind=ActionKind(model.kind),
        status=ActionStatus(model.status),
        platform=Platform(model.platform),
        channel_id=model.channel_id,
        channel_type=ChannelType(model.channel_type),
        account_id=model.account_id,
        actor_id=model.actor_id,
        connector_name=model.connector_name,
        message_text=model.message_text,
        requires_approval=model.requires_approval,
        policy_decision=policy_decision,
        delivery_connector_name=model.delivery_connector_name,
        delivery_response=model.delivery_response or {},
        error_message=model.error_message,
        metadata=model.metadata_payload or {},
        created_at=model.created_at,
        updated_at=model.updated_at,
        approved_at=model.approved_at,
        sent_at=model.sent_at,
    )


def _to_meeting_session(model: MeetingSessionModel) -> MeetingSessionRecord:
    return MeetingSessionRecord(
        session_id=model.session_id,
        connector_name=model.connector_name,
        platform=Platform(model.platform),
        account_id=model.account_id,
        meeting_key=model.meeting_key,
        meeting_title=model.meeting_title,
        channel_id=model.channel_id,
        audio_source=MeetingAudioSource(model.audio_source) if model.audio_source else None,
        capture_backend=model.capture_backend,
        capture_device_name=model.capture_device_name,
        transcription_backend=model.transcription_backend,
        detected_window=model.detected_window,
        notes=model.notes,
        latest_summary=model.latest_summary,
        latest_key_points=model.latest_key_points,
        latest_action_items=model.latest_action_items,
        latest_follow_up_questions=model.latest_follow_up_questions,
        last_segment_at=model.last_segment_at,
        created_at=model.created_at,
        updated_at=model.updated_at,
    )


def _to_meeting_segment(model: MeetingSegmentModel) -> MeetingSegmentRecord:
    return MeetingSegmentRecord(
        segment_id=model.segment_id,
        session_id=model.session_id,
        connector_name=model.connector_name,
        platform=Platform(model.platform),
        account_id=model.account_id,
        chunk_index=model.chunk_index,
        speaker_name=model.speaker_name,
        display_time=model.display_time,
        text=model.text_body,
        started_at=model.started_at,
        ended_at=model.ended_at,
        audio_source=MeetingAudioSource(model.audio_source) if model.audio_source else None,
        capture_device_name=model.capture_device_name,
        saved_path=model.saved_path,
        raw=model.raw_payload,
        created_at=model.created_at,
    )


def _to_meeting_minutes(model: MeetingMinutesModel) -> MeetingMinutesRecord:
    from practical_chat_agent.core.enums import MeetingExportTemplate

    return MeetingMinutesRecord(
        minutes_id=model.minutes_id,
        session_id=model.session_id,
        template=MeetingExportTemplate(model.template),
        title=model.title,
        backend=model.backend,
        model=model.model,
        status=model.status,
        output_path=model.output_path,
        markdown_body=model.markdown_body,
        overview=model.overview,
        background=model.background,
        conclusions=model.conclusions,
        action_items=model.action_items,
        risks=model.risks,
        raw_excerpt_ids=model.raw_excerpt_ids,
        raw=model.raw_payload,
        created_at=model.created_at,
    )
