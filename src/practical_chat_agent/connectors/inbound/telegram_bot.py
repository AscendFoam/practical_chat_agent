from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from practical_chat_agent.connectors.inbound.base import InboundConnector
from practical_chat_agent.core.enums import ChannelType, ContentType, Direction, Platform, SourceType
from practical_chat_agent.core.models import InboundConnectorResult, InboundEvent


class TelegramBotConnector(InboundConnector):
    """Minimal official-style Telegram bot connector."""

    connector_name = "telegram_bot"

    def can_handle_payload(self, payload: dict[str, Any]) -> bool:
        message = payload.get("message")
        chat = payload.get("chat")
        sender = payload.get("from")
        return isinstance(message, dict) and isinstance(chat, dict) and isinstance(sender, dict)

    def parse_inbound_payload(self, payload: dict[str, Any]) -> InboundConnectorResult:
        agent_id = str(payload["agent_id"])
        chat = payload["chat"]
        sender = payload["from"]
        message = payload["message"]
        message_id = str(message.get("message_id", payload.get("update_id", "unknown")))

        event = InboundEvent(
            event_id=f"tg_{chat['id']}_{message_id}",
            source_type=SourceType.CHAT_MESSAGE,
            platform=Platform.TELEGRAM,
            channel_id=str(chat["id"]),
            channel_type=self._parse_channel_type(chat.get("type")),
            account_id=agent_id,
            actor_id=str(sender["id"]),
            actor_name=sender.get("username") or sender.get("first_name"),
            direction=Direction.INBOUND,
            content_type=ContentType.TEXT,
            occurred_at=self._parse_occurred_at(message.get("date")),
            text=message.get("text"),
            raw=payload,
        )
        return InboundConnectorResult(
            connector_name=self.connector_name,
            agent_id=agent_id,
            event=event,
            raw_payload=payload,
        )

    @staticmethod
    def _parse_channel_type(chat_type: Any) -> ChannelType:
        if chat_type in {"group", "supergroup"}:
            return ChannelType.GROUP
        return ChannelType.DM

    @staticmethod
    def _parse_occurred_at(raw_value: Any) -> datetime:
        if isinstance(raw_value, (int, float)):
            return datetime.fromtimestamp(raw_value, tz=timezone.utc)
        if isinstance(raw_value, str):
            try:
                return datetime.fromisoformat(raw_value)
            except ValueError:
                pass
        return datetime.now(timezone.utc)
