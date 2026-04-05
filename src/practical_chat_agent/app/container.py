from __future__ import annotations

from dataclasses import dataclass

from practical_chat_agent.app.config import Settings, get_settings
from practical_chat_agent.connectors.desktop.base import DesktopConnector
from practical_chat_agent.connectors.desktop.wechat_desktop import WeChatDesktopConnector
from practical_chat_agent.connectors.inbound.base import InboundConnector
from practical_chat_agent.connectors.inbound.feishu_bot import FeishuBotConnector
from practical_chat_agent.connectors.inbound.telegram_bot import TelegramBotConnector
from practical_chat_agent.connectors.meeting.base import MeetingConnector
from practical_chat_agent.connectors.meeting.tencent_meeting_desktop import TencentMeetingDesktopConnector
from practical_chat_agent.core.bus import InMemoryEventBus
from practical_chat_agent.runtime.agent_runtime import AgentRuntime
from practical_chat_agent.services.audio_transcription import ZhipuAudioTranscriptionService
from practical_chat_agent.services.desktop import DesktopScanService
from practical_chat_agent.services.inbound import InboundEventService
from practical_chat_agent.services.meeting import MeetingMonitorService
from practical_chat_agent.services.meeting_audio_capture import WindowsLoopbackAudioCaptureService
from practical_chat_agent.services.ocr import GlmOcrService
from practical_chat_agent.storage.mysql.models import create_schema
from practical_chat_agent.storage.mysql.repositories import (
    SqlAlchemyAgentRepository,
    SqlAlchemyAuditRepository,
    SqlAlchemyEventRepository,
    SqlAlchemyMemoryRepository,
)
from practical_chat_agent.storage.mysql.session import (
    create_database_if_missing,
    create_engine_from_settings,
    create_session_factory,
)


@dataclass(slots=True)
class AppContainer:
    settings: Settings
    bus: InMemoryEventBus
    inbound_connectors: dict[str, InboundConnector]
    desktop_connectors: dict[str, DesktopConnector]
    meeting_connectors: dict[str, MeetingConnector]
    inbound_service: InboundEventService
    desktop_service: DesktopScanService
    meeting_service: MeetingMonitorService
    ocr_service: GlmOcrService
    audio_transcription_service: ZhipuAudioTranscriptionService
    meeting_audio_capture_service: WindowsLoopbackAudioCaptureService
    agent_repository: SqlAlchemyAgentRepository
    event_repository: SqlAlchemyEventRepository
    memory_repository: SqlAlchemyMemoryRepository
    audit_repository: SqlAlchemyAuditRepository
    runtime: AgentRuntime

    @classmethod
    def build(cls, settings: Settings | None = None) -> "AppContainer":
        resolved_settings = settings or get_settings()
        engine = create_engine_from_settings(resolved_settings)
        session_factory = create_session_factory(engine)

        bus = InMemoryEventBus()
        inbound_connectors: dict[str, InboundConnector] = {
            FeishuBotConnector.connector_name: FeishuBotConnector(),
            TelegramBotConnector.connector_name: TelegramBotConnector(),
        }
        ocr_service = GlmOcrService(
            api_key=resolved_settings.glm_ocr_api_key,
            model=resolved_settings.glm_ocr_model,
            timeout_seconds=resolved_settings.desktop_ocr_timeout_seconds,
            enabled=resolved_settings.desktop_ocr_enabled,
        )
        audio_transcription_service = ZhipuAudioTranscriptionService(
            api_key=resolved_settings.meeting_transcribe_api_key,
            model=resolved_settings.meeting_transcribe_model,
            timeout_seconds=resolved_settings.meeting_transcribe_timeout_seconds,
            enabled=resolved_settings.meeting_transcribe_enabled,
        )
        meeting_audio_capture_service = WindowsLoopbackAudioCaptureService(
            sample_rate=resolved_settings.meeting_loopback_sample_rate,
            default_capture_seconds=resolved_settings.meeting_loopback_default_capture_seconds,
            default_chunk_seconds=resolved_settings.meeting_loopback_default_chunk_seconds,
            preferred_speaker_name=resolved_settings.meeting_loopback_preferred_speaker_name,
            debug_dir=resolved_settings.meeting_capture_debug_dir,
        )
        desktop_connectors: dict[str, DesktopConnector] = {
            WeChatDesktopConnector.connector_name: WeChatDesktopConnector(
                ocr_service=ocr_service,
                capture_debug_dir=resolved_settings.desktop_capture_debug_dir,
            ),
        }
        meeting_connectors: dict[str, MeetingConnector] = {
            TencentMeetingDesktopConnector.connector_name: TencentMeetingDesktopConnector(
                transcription_service=audio_transcription_service,
                audio_capture_service=meeting_audio_capture_service,
                capture_debug_dir=resolved_settings.meeting_capture_debug_dir,
            ),
        }
        agent_repository = SqlAlchemyAgentRepository(session_factory)
        event_repository = SqlAlchemyEventRepository(session_factory)
        memory_repository = SqlAlchemyMemoryRepository(session_factory)
        audit_repository = SqlAlchemyAuditRepository(session_factory)

        runtime = AgentRuntime(
            agent_repository=agent_repository,
            event_repository=event_repository,
            memory_repository=memory_repository,
            audit_repository=audit_repository,
            event_bus=bus,
        )
        inbound_service = InboundEventService(
            connectors=inbound_connectors,
            runtime=runtime,
            event_bus=bus,
        )
        desktop_service = DesktopScanService(
            connectors=desktop_connectors,
            event_bus=bus,
        )
        meeting_service = MeetingMonitorService(
            connectors=meeting_connectors,
            event_bus=bus,
        )

        return cls(
            settings=resolved_settings,
            bus=bus,
            inbound_connectors=inbound_connectors,
            desktop_connectors=desktop_connectors,
            meeting_connectors=meeting_connectors,
            inbound_service=inbound_service,
            desktop_service=desktop_service,
            meeting_service=meeting_service,
            ocr_service=ocr_service,
            audio_transcription_service=audio_transcription_service,
            meeting_audio_capture_service=meeting_audio_capture_service,
            agent_repository=agent_repository,
            event_repository=event_repository,
            memory_repository=memory_repository,
            audit_repository=audit_repository,
            runtime=runtime,
        )

    def init_database(self) -> None:
        create_database_if_missing(self.settings)
        engine = create_engine_from_settings(self.settings)
        create_schema(engine)
