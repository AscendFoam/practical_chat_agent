from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

from practical_chat_agent.connectors.inbound.base import InboundConnector
from practical_chat_agent.core.enums import ChannelType, ContentType, Direction, Platform, SourceType
from practical_chat_agent.core.models import InboundConnectorResult, InboundEvent


class FeishuBotConnector(InboundConnector):
    """Minimal official-style Feishu event callback connector."""

    connector_name = "feishu_bot"

    def can_handle_payload(self, payload: dict[str, Any]) -> bool:
        header = payload.get("header")
        event = payload.get("event")
        message = event.get("message") if isinstance(event, dict) else None
        event_type = header.get("event_type") if isinstance(header, dict) else None
        return (
            event_type == "im.message.receive_v1"
            or (isinstance(message, dict) and "chat_id" in message and "message_id" in message)
        )

    def parse_inbound_payload(self, payload: dict[str, Any]) -> InboundConnectorResult:
        agent_id = str(payload["agent_id"])
        event = payload.get("event", {})
        message = event.get("message", {})
        sender = event.get("sender", {})
        sender_id = sender.get("sender_id", {})

        channel_id = str(message.get("chat_id", "unknown_chat"))
        message_id = str(message.get("message_id", payload.get("uuid", "unknown_message")))
        message_type = str(message.get("message_type", "text"))

        inbound_event = InboundEvent(
            event_id=f"feishu_{channel_id}_{message_id}",
            source_type=SourceType.CHAT_MESSAGE,
            platform=Platform.FEISHU,
            channel_id=channel_id,
            channel_type=self._parse_channel_type(message.get("chat_type")),
            account_id=agent_id,
            actor_id=self._parse_actor_id(sender_id),
            actor_name=sender.get("name") or sender_id.get("open_id") or sender_id.get("user_id"),
            direction=Direction.INBOUND,
            content_type=self._parse_content_type(message_type),
            occurred_at=self._parse_occurred_at(message.get("create_time")),
            text=self._parse_text_body(message.get("content"), message_type),
            raw=payload,
        )
        return InboundConnectorResult(
            connector_name=self.connector_name,
            agent_id=agent_id,
            event=inbound_event,
            raw_payload=payload,
        )

    @staticmethod
    def _parse_actor_id(sender_id: dict[str, Any]) -> str:
        return str(
            sender_id.get("open_id")
            or sender_id.get("user_id")
            or sender_id.get("union_id")
            or "unknown_sender"
        )

    @staticmethod
    def _parse_channel_type(chat_type: Any) -> ChannelType:
        if chat_type in {"group", "chat"}:
            return ChannelType.GROUP
        return ChannelType.DM

    @staticmethod
    def _parse_content_type(message_type: str) -> ContentType:
        mapping = {
            "text": ContentType.TEXT,
            "image": ContentType.IMAGE,
            "file": ContentType.FILE,
            "audio": ContentType.AUDIO,
        }
        return mapping.get(message_type, ContentType.SYSTEM)

    @staticmethod
    def _parse_occurred_at(raw_value: Any) -> datetime:
        if isinstance(raw_value, str) and raw_value.isdigit():
            value = int(raw_value)
            if value > 10_000_000_000:
                return datetime.fromtimestamp(value / 1000, tz=timezone.utc)
            return datetime.fromtimestamp(value, tz=timezone.utc)
        if isinstance(raw_value, (int, float)):
            if raw_value > 10_000_000_000:
                return datetime.fromtimestamp(raw_value / 1000, tz=timezone.utc)
            return datetime.fromtimestamp(raw_value, tz=timezone.utc)
        return datetime.now(timezone.utc)

    @staticmethod
    def _parse_text_body(raw_content: Any, message_type: str) -> str | None:
        if message_type != "text":
            if raw_content is None:
                return None
            return str(raw_content)

        if isinstance(raw_content, dict):
            return raw_content.get("text")

        if isinstance(raw_content, str):
            try:
                parsed = json.loads(raw_content)
            except json.JSONDecodeError:
                return raw_content
            if isinstance(parsed, dict):
                return parsed.get("text") or raw_content

        return None
