from __future__ import annotations

from datetime import datetime, timezone
import hashlib
from typing import Any

from practical_chat_agent.connectors.inbound.base import InboundConnector
from practical_chat_agent.core.enums import ChannelType, ContentType, Direction, Platform, SourceType
from practical_chat_agent.core.models import InboundConnectorResult, InboundEvent


class WeComCustomerServiceInboundConnector(InboundConnector):
    """Synthetic-only WeCom WeChat Customer Service inbound normalizer."""

    connector_name = "wecom_customer_service"

    def can_handle_payload(self, payload: dict[str, Any]) -> bool:
        if not isinstance(payload, dict):
            return False

        if self._payload_connector_name(payload) == self.connector_name:
            return True

        msg_list = payload.get("msg_list")
        if isinstance(msg_list, list) and msg_list:
            first_message = msg_list[0]
            return isinstance(first_message, dict) and {
                "open_kfid",
                "external_userid",
                "msgtype",
            }.issubset(first_message)

        event = payload.get("event")
        if isinstance(event, dict):
            return {"event_type", "open_kfid", "external_userid"}.issubset(event)

        return False

    def parse_inbound_payload(self, payload: dict[str, Any]) -> InboundConnectorResult:
        if not self.can_handle_payload(payload):
            raise ValueError("not a WeCom Customer Service inbound payload")

        if isinstance(payload.get("msg_list"), list):
            return self._parse_message_payload(payload)

        if isinstance(payload.get("event"), dict):
            return self._parse_event_payload(payload)

        raise ValueError("not a WeCom Customer Service inbound payload")

    def _parse_message_payload(self, payload: dict[str, Any]) -> InboundConnectorResult:
        msg_list = payload.get("msg_list")
        if not isinstance(msg_list, list) or not msg_list or not isinstance(msg_list[0], dict):
            raise ValueError("missing required WeCom Customer Service message fields: msg_list")

        message = msg_list[0]
        self._require_fields(
            message,
            required=("msgid", "open_kfid", "external_userid", "msgtype"),
            label="message",
        )

        open_kfid = str(message["open_kfid"])
        external_userid = str(message["external_userid"])
        msgid = str(message["msgid"])
        msgtype = str(message["msgtype"])
        account_id = self._account_id(open_kfid)
        agent_id = self._agent_id(payload=payload, open_kfid=open_kfid)

        content_type = ContentType.TEXT if msgtype == "text" else ContentType.SYSTEM
        text = self._text_body(message) if msgtype == "text" else (
            f"Unsupported WeCom Customer Service message type: {msgtype}"
        )

        contract: dict[str, Any] = self._contract_metadata(payload_kind="message")
        if msgtype != "text":
            contract["unsupported_msgtype"] = msgtype

        event = InboundEvent(
            event_id=self._event_id("message", open_kfid, external_userid, msgid, msgtype),
            source_type=SourceType.CHAT_MESSAGE,
            platform=Platform.WECHAT,
            channel_id=self._channel_id(open_kfid=open_kfid, external_userid=external_userid),
            channel_type=ChannelType.DM,
            account_id=account_id,
            actor_id=external_userid,
            actor_name=self._optional_str(message.get("external_user_alias")),
            direction=Direction.INBOUND,
            content_type=content_type,
            occurred_at=self._parse_occurred_at(message.get("send_time")),
            text=text,
            raw={
                "contract": contract,
                "payload": payload,
            },
        )
        return InboundConnectorResult(
            connector_name=self.connector_name,
            agent_id=agent_id,
            event=event,
            raw_payload=payload,
        )

    def _parse_event_payload(self, payload: dict[str, Any]) -> InboundConnectorResult:
        event_payload = payload.get("event")
        if not isinstance(event_payload, dict):
            raise ValueError("missing required WeCom Customer Service event fields: event")

        self._require_fields(
            event_payload,
            required=("event_type", "open_kfid", "external_userid"),
            label="event",
        )

        open_kfid = str(event_payload["open_kfid"])
        external_userid = str(event_payload["external_userid"])
        event_type = str(event_payload["event_type"])
        agent_id = self._agent_id(payload=payload, open_kfid=open_kfid)
        fail_type = event_payload.get("fail_type")
        text = f"WeCom Customer Service event: {event_type}"
        if fail_type is not None:
            text = f"{text}; fail_type={fail_type}"

        event = InboundEvent(
            event_id=self._event_id(
                "event",
                open_kfid,
                external_userid,
                event_type,
                str(event_payload.get("fail_msgid", "")),
                str(fail_type or ""),
            ),
            source_type=SourceType.SYSTEM_EVENT,
            platform=Platform.WECHAT,
            channel_id=self._channel_id(open_kfid=open_kfid, external_userid=external_userid),
            channel_type=ChannelType.DM,
            account_id=self._account_id(open_kfid),
            actor_id=external_userid,
            actor_name=self._optional_str(event_payload.get("external_user_alias")),
            direction=Direction.INBOUND,
            content_type=ContentType.SYSTEM,
            occurred_at=self._parse_occurred_at(
                event_payload.get("event_time") or event_payload.get("send_time"),
            ),
            text=text,
            raw={
                "contract": self._contract_metadata(payload_kind="event"),
                "payload": payload,
            },
        )
        return InboundConnectorResult(
            connector_name=self.connector_name,
            agent_id=agent_id,
            event=event,
            raw_payload=payload,
        )

    @classmethod
    def _require_fields(
        cls,
        value: dict[str, Any],
        *,
        required: tuple[str, ...],
        label: str,
    ) -> None:
        missing = [field for field in required if field not in value or value[field] in {None, ""}]
        if missing:
            fields = ", ".join(missing)
            raise ValueError(f"missing required WeCom Customer Service {label} fields: {fields}")

    @classmethod
    def _payload_connector_name(cls, payload: dict[str, Any]) -> str | None:
        direct = payload.get("connector_name")
        if isinstance(direct, str) and direct:
            return direct

        meta = payload.get("_meta")
        if isinstance(meta, dict):
            meta_name = meta.get("connector_name")
            if isinstance(meta_name, str) and meta_name:
                return meta_name

        return None

    @staticmethod
    def _agent_id(*, payload: dict[str, Any], open_kfid: str) -> str:
        agent_id = payload.get("agent_id")
        if isinstance(agent_id, str) and agent_id:
            return agent_id
        return f"wecom_kf:{open_kfid}"

    @staticmethod
    def _account_id(open_kfid: str) -> str:
        return f"wecom_kf:{open_kfid}"

    @staticmethod
    def _channel_id(*, open_kfid: str, external_userid: str) -> str:
        return f"wecom_cs:{open_kfid}:{external_userid}"

    @staticmethod
    def _contract_metadata(*, payload_kind: str) -> dict[str, Any]:
        return {
            "surface": "wecom_customer_service",
            "payload_kind": payload_kind,
            "synthetic_only": True,
            "official_docs_rechecked": "2026-05-28",
        }

    @staticmethod
    def _event_id(*parts: str) -> str:
        stable = "|".join(parts)
        digest = hashlib.sha256(stable.encode("utf-8")).hexdigest()[:20]
        return f"wecom_cs_{digest}"

    @staticmethod
    def _optional_str(raw_value: Any) -> str | None:
        if raw_value is None:
            return None
        value = str(raw_value)
        return value or None

    @staticmethod
    def _parse_occurred_at(raw_value: Any) -> datetime:
        if isinstance(raw_value, (int, float)):
            if raw_value > 10_000_000_000:
                return datetime.fromtimestamp(raw_value / 1000, tz=timezone.utc)
            return datetime.fromtimestamp(raw_value, tz=timezone.utc)

        if isinstance(raw_value, str):
            if raw_value.isdigit():
                value = int(raw_value)
                if value > 10_000_000_000:
                    return datetime.fromtimestamp(value / 1000, tz=timezone.utc)
                return datetime.fromtimestamp(value, tz=timezone.utc)
            try:
                parsed = datetime.fromisoformat(raw_value)
            except ValueError:
                pass
            else:
                if parsed.tzinfo is None:
                    return parsed.replace(tzinfo=timezone.utc)
                return parsed

        return datetime.fromtimestamp(0, tz=timezone.utc)

    @staticmethod
    def _text_body(message: dict[str, Any]) -> str | None:
        text = message.get("text")
        if isinstance(text, dict):
            raw_content = text.get("content")
            if raw_content is not None:
                return str(raw_content)
        return None
