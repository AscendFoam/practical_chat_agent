from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path

from practical_chat_agent.app.config import Settings, get_settings
from practical_chat_agent.connectors.delivery.base import DeliveryConnector
from practical_chat_agent.connectors.delivery.telegram_bot import TelegramBotDeliveryConnector
from practical_chat_agent.connectors.desktop.base import DesktopConnector
from practical_chat_agent.connectors.desktop.wechat_desktop import WeChatDesktopConnector
from practical_chat_agent.connectors.inbound.base import InboundConnector
from practical_chat_agent.connectors.inbound.feishu_bot import FeishuBotConnector
from practical_chat_agent.connectors.inbound.telegram_bot import TelegramBotConnector
from practical_chat_agent.connectors.meeting.base import MeetingConnector
from practical_chat_agent.connectors.meeting.tencent_meeting_desktop import TencentMeetingDesktopConnector
from practical_chat_agent.core.bus import InMemoryEventBus
from practical_chat_agent.core.enums import Platform
from practical_chat_agent.runtime.agent_runtime import AgentRuntime
from practical_chat_agent.services.audio_transcription import ZhipuAudioTranscriptionService
from practical_chat_agent.services.chat_context import ChatContextAssembler
from practical_chat_agent.services.chat_memory import ChatMemoryExtractionService
from practical_chat_agent.services.memory_retrieval import MemoryRetrievalService
from practical_chat_agent.services.chat_suggestions import ChatSuggestionService
from practical_chat_agent.services.delivery import ActionDeliveryService
from practical_chat_agent.services.desktop import DesktopScanService
from practical_chat_agent.services.inbound import InboundEventService
from practical_chat_agent.services.meeting_assistant import MeetingAssistantService
from practical_chat_agent.services.meeting import MeetingMonitorService
from practical_chat_agent.services.meeting_audio_capture import WindowsAudioCaptureService
from practical_chat_agent.services.meeting_live_loop import MeetingLiveLoopService
from practical_chat_agent.services.meeting_minutes import MeetingMinutesService
from practical_chat_agent.services.meeting_minutes_export import MeetingMinutesExportService
from practical_chat_agent.services.memory_lifecycle import MemoryLifecycleService
from practical_chat_agent.services.ocr import GlmOcrService
from practical_chat_agent.services.policy import PolicyEngine
from practical_chat_agent.storage.mysql.models import create_schema
from practical_chat_agent.storage.mysql.repositories import (
    SqlAlchemyActionRepository,
    SqlAlchemyAgentRepository,
    SqlAlchemyAuditRepository,
    SqlAlchemyEventRepository,
    SqlAlchemyMeetingRepository,
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
    delivery_connectors: dict[Platform, DeliveryConnector]
    desktop_connectors: dict[str, DesktopConnector]
    meeting_connectors: dict[str, MeetingConnector]
    inbound_service: InboundEventService
    desktop_service: DesktopScanService
    meeting_service: MeetingMonitorService
    meeting_live_loop_service: MeetingLiveLoopService
    meeting_assistant_service: MeetingAssistantService
    meeting_minutes_service: MeetingMinutesService
    meeting_minutes_export_service: MeetingMinutesExportService
    chat_context_assembler: ChatContextAssembler
    memory_retrieval_service: MemoryRetrievalService
    chat_suggestion_service: ChatSuggestionService
    chat_memory_service: ChatMemoryExtractionService
    memory_lifecycle_service: MemoryLifecycleService
    policy_engine: PolicyEngine
    action_delivery_service: ActionDeliveryService
    ocr_service: GlmOcrService
    audio_transcription_service: ZhipuAudioTranscriptionService
    meeting_audio_capture_service: WindowsAudioCaptureService
    agent_repository: SqlAlchemyAgentRepository
    event_repository: SqlAlchemyEventRepository
    memory_repository: SqlAlchemyMemoryRepository
    action_repository: SqlAlchemyActionRepository
    audit_repository: SqlAlchemyAuditRepository
    meeting_repository: SqlAlchemyMeetingRepository
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
        delivery_connectors: dict[Platform, DeliveryConnector] = {
            Platform.TELEGRAM: TelegramBotDeliveryConnector(
                bot_token=resolved_settings.telegram_bot_token,
                enabled=resolved_settings.telegram_delivery_enabled,
                timeout_seconds=resolved_settings.telegram_delivery_timeout_seconds,
            ),
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
            empty_retry_enabled=resolved_settings.meeting_transcribe_empty_retry_enabled,
            empty_retry_prompt=resolved_settings.meeting_transcribe_empty_retry_prompt,
        )
        meeting_assistant_service = MeetingAssistantService(
            api_key=resolved_settings.openai_api_key,
            base_url=resolved_settings.openai_base_url,
            model=resolved_settings.meeting_assistant_model,
            timeout_seconds=resolved_settings.meeting_assistant_timeout_seconds,
            enabled=resolved_settings.meeting_assistant_enabled,
            context_segments=resolved_settings.meeting_assistant_context_segments,
        )
        meeting_minutes_service = MeetingMinutesService(
            api_key=resolved_settings.openai_api_key,
            base_url=resolved_settings.openai_base_url,
            model=resolved_settings.meeting_minutes_model,
            timeout_seconds=resolved_settings.meeting_minutes_timeout_seconds,
            enabled=resolved_settings.meeting_minutes_rewriter_enabled,
            context_segments=resolved_settings.meeting_minutes_context_segments,
        )
        meeting_audio_capture_service = WindowsAudioCaptureService(
            sample_rate=resolved_settings.meeting_loopback_sample_rate,
            default_capture_seconds=resolved_settings.meeting_loopback_default_capture_seconds,
            default_chunk_seconds=resolved_settings.meeting_loopback_default_chunk_seconds,
            preferred_speaker_name=resolved_settings.meeting_loopback_preferred_speaker_name,
            preferred_microphone_name=resolved_settings.meeting_microphone_preferred_device_name,
            silence_threshold=resolved_settings.meeting_audio_silence_threshold,
            microphone_boost_gain=resolved_settings.meeting_microphone_boost_gain,
            microphone_peak_target=resolved_settings.meeting_microphone_peak_target,
            microphone_silence_floor=resolved_settings.meeting_microphone_silence_floor,
            microphone_highpass_cutoff_hz=resolved_settings.meeting_microphone_highpass_cutoff_hz,
            microphone_trim_padding_seconds=resolved_settings.meeting_microphone_trim_padding_seconds,
            microphone_compressor_threshold=resolved_settings.meeting_microphone_compressor_threshold,
            microphone_compressor_ratio=resolved_settings.meeting_microphone_compressor_ratio,
            microphone_limiter_ceiling=resolved_settings.meeting_microphone_limiter_ceiling,
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
        action_repository = SqlAlchemyActionRepository(session_factory)
        audit_repository = SqlAlchemyAuditRepository(session_factory)
        meeting_repository = SqlAlchemyMeetingRepository(session_factory)
        approved_store_path = os.environ.get("PRACTICAL_CHAT_APPROVED_STORE_PATH")
        approved_memory_limit_raw = os.environ.get("PRACTICAL_CHAT_APPROVED_MEMORY_LIMIT")
        approved_memory_limit = 4
        if approved_memory_limit_raw:
            try:
                approved_memory_limit = max(int(approved_memory_limit_raw), 1)
            except ValueError:
                approved_memory_limit = 4
        chat_context_assembler = ChatContextAssembler(
            recent_events_limit=resolved_settings.chat_context_recent_events,
            memory_hits_limit=resolved_settings.chat_context_memory_hits,
            approved_store_path=Path(approved_store_path) if approved_store_path else None,
            approved_memory_limit=approved_memory_limit,
        )
        memory_retrieval_service = MemoryRetrievalService(
            selection_limit=resolved_settings.chat_context_memory_hits,
            candidate_multiplier=4,
            api_key=resolved_settings.openai_api_key,
            base_url=resolved_settings.openai_base_url,
            model=resolved_settings.chat_profile_facets_model,
            timeout_seconds=resolved_settings.chat_profile_facets_timeout_seconds,
            enabled=resolved_settings.chat_profile_facets_enabled,
        )
        chat_suggestion_service = ChatSuggestionService(
            api_key=resolved_settings.openai_api_key,
            base_url=resolved_settings.openai_base_url,
            model=resolved_settings.chat_suggestion_model,
            timeout_seconds=resolved_settings.chat_suggestion_timeout_seconds,
            enabled=resolved_settings.chat_suggestion_enabled,
        )
        chat_memory_service = ChatMemoryExtractionService(
            api_key=resolved_settings.openai_api_key,
            base_url=resolved_settings.openai_base_url,
            model=resolved_settings.chat_memory_model,
            timeout_seconds=resolved_settings.chat_memory_timeout_seconds,
            enabled=resolved_settings.chat_memory_enabled,
        )
        memory_lifecycle_service = MemoryLifecycleService(
            memory_repository=memory_repository,
        )
        policy_engine = PolicyEngine(
            action_repository=action_repository,
            quiet_hours_start=resolved_settings.outbound_quiet_hours_start,
            quiet_hours_end=resolved_settings.outbound_quiet_hours_end,
            timezone_name=resolved_settings.outbound_policy_timezone,
            frequency_limit_count=resolved_settings.outbound_frequency_limit_count,
            frequency_limit_window_seconds=resolved_settings.outbound_frequency_limit_window_seconds,
            group_chat_draft_only=resolved_settings.outbound_group_chat_draft_only,
        )
        action_delivery_service = ActionDeliveryService(
            action_repository=action_repository,
            agent_repository=agent_repository,
            audit_repository=audit_repository,
            delivery_connectors=delivery_connectors,
            policy_engine=policy_engine,
        )

        runtime = AgentRuntime(
            agent_repository=agent_repository,
            event_repository=event_repository,
            memory_repository=memory_repository,
            audit_repository=audit_repository,
            action_repository=action_repository,
            chat_context_assembler=chat_context_assembler,
            memory_retrieval_service=memory_retrieval_service,
            chat_suggestion_service=chat_suggestion_service,
            chat_memory_service=chat_memory_service,
            policy_engine=policy_engine,
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
            runtime=runtime,
            event_bus=bus,
            meeting_repository=meeting_repository,
            assistant_service=meeting_assistant_service,
        )
        meeting_live_loop_service = MeetingLiveLoopService(
            meeting_service=meeting_service,
        )
        meeting_minutes_export_service = MeetingMinutesExportService(
            meeting_repository=meeting_repository,
            meeting_minutes_service=meeting_minutes_service,
        )

        return cls(
            settings=resolved_settings,
            bus=bus,
            inbound_connectors=inbound_connectors,
            delivery_connectors=delivery_connectors,
            desktop_connectors=desktop_connectors,
            meeting_connectors=meeting_connectors,
            inbound_service=inbound_service,
            desktop_service=desktop_service,
            meeting_service=meeting_service,
            meeting_live_loop_service=meeting_live_loop_service,
            meeting_assistant_service=meeting_assistant_service,
            meeting_minutes_service=meeting_minutes_service,
            meeting_minutes_export_service=meeting_minutes_export_service,
            chat_context_assembler=chat_context_assembler,
            memory_retrieval_service=memory_retrieval_service,
            chat_suggestion_service=chat_suggestion_service,
            chat_memory_service=chat_memory_service,
            memory_lifecycle_service=memory_lifecycle_service,
            policy_engine=policy_engine,
            action_delivery_service=action_delivery_service,
            ocr_service=ocr_service,
            audio_transcription_service=audio_transcription_service,
            meeting_audio_capture_service=meeting_audio_capture_service,
            agent_repository=agent_repository,
            event_repository=event_repository,
            memory_repository=memory_repository,
            action_repository=action_repository,
            audit_repository=audit_repository,
            meeting_repository=meeting_repository,
            runtime=runtime,
        )

    def init_database(self) -> None:
        create_database_if_missing(self.settings)
        engine = create_engine_from_settings(self.settings)
        create_schema(engine)
