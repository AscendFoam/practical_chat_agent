from __future__ import annotations

import json
from pathlib import Path

import pytest

from practical_chat_agent.connectors.inbound.wecom_customer_service import (
    WeComCustomerServiceInboundConnector,
)
from practical_chat_agent.core.enums import ChannelType, ContentType, Direction, Platform, SourceType


FIXTURE_DIR = Path(__file__).parent / "fixtures" / "wecom_customer_service_inbound"


def _fixture(name: str) -> dict:
    return json.loads((FIXTURE_DIR / name).read_text(encoding="utf-8"))


def test_can_handle_synthetic_fixture_wrapper_and_documented_msg_list_shape() -> None:
    connector = WeComCustomerServiceInboundConnector()
    payload = _fixture("inbound_text_message.json")
    documented_shape = {key: value for key, value in payload.items() if key != "_meta"}

    assert connector.connector_name == "wecom_customer_service"
    assert connector.can_handle_payload(payload)
    assert connector.can_handle_payload(documented_shape)


def test_parse_inbound_text_message_to_review_safe_inbound_event() -> None:
    connector = WeComCustomerServiceInboundConnector()
    payload = _fixture("inbound_text_message.json")

    result = connector.parse_inbound_payload(payload)
    repeat = connector.parse_inbound_payload(payload)

    assert result.connector_name == "wecom_customer_service"
    assert result.agent_id == "wecom_kf_account_support"
    assert result.event.event_id == repeat.event.event_id
    assert result.event.platform == Platform.WECHAT
    assert result.event.source_type == SourceType.CHAT_MESSAGE
    assert result.event.direction == Direction.INBOUND
    assert result.event.channel_type == ChannelType.DM
    assert result.event.content_type == ContentType.TEXT
    assert result.event.channel_id == "wecom_cs:kf_alias_support:customer_alias_001"
    assert result.event.account_id == "wecom_kf:kf_alias_support"
    assert result.event.actor_id == "customer_alias_001"
    assert result.event.text == "Hello, I need help with my appointment."
    assert result.event.occurred_at.isoformat() == "2024-05-28T08:00:00+00:00"
    assert result.event.raw["contract"]["surface"] == "wecom_customer_service"
    assert result.event.raw["contract"]["payload_kind"] == "message"
    assert result.event.raw["payload"]["msg_list"][0]["external_userid"] == "customer_alias_001"


def test_non_text_message_maps_to_system_event_without_private_identity_inference() -> None:
    connector = WeComCustomerServiceInboundConnector()

    result = connector.parse_inbound_payload(_fixture("non_text_message.json"))

    assert result.event.platform == Platform.WECHAT
    assert result.event.source_type == SourceType.CHAT_MESSAGE
    assert result.event.content_type == ContentType.SYSTEM
    assert result.event.actor_id == "customer_alias_001"
    assert result.event.text == "Unsupported WeCom Customer Service message type: image"
    assert "contact_id" not in result.event.raw
    assert result.event.raw["contract"]["unsupported_msgtype"] == "image"


def test_provider_failure_event_maps_to_system_inbound_event() -> None:
    connector = WeComCustomerServiceInboundConnector()

    result = connector.parse_inbound_payload(_fixture("send_failure_event.json"))

    assert result.event.platform == Platform.WECHAT
    assert result.event.source_type == SourceType.SYSTEM_EVENT
    assert result.event.content_type == ContentType.SYSTEM
    assert result.event.channel_id == "wecom_cs:kf_alias_support:customer_alias_001"
    assert result.event.account_id == "wecom_kf:kf_alias_support"
    assert result.event.actor_id == "customer_alias_001"
    assert result.event.text == "WeCom Customer Service event: msg_send_fail; fail_type=4"
    assert result.event.raw["contract"]["payload_kind"] == "event"
    assert result.event.raw["payload"]["event"]["fail_msgid"] == "msg_alias_outbound_001"


def test_malformed_payload_is_rejected_deterministically() -> None:
    connector = WeComCustomerServiceInboundConnector()
    payload = _fixture("malformed_missing_identity.json")

    assert connector.can_handle_payload(payload)
    with pytest.raises(ValueError, match="missing required WeCom Customer Service message fields"):
        connector.parse_inbound_payload(payload)


def test_personal_wechat_desktop_like_payload_is_not_accepted() -> None:
    connector = WeComCustomerServiceInboundConnector()
    payload = _fixture("personal_wechat_desktop_like.json")

    assert not connector.can_handle_payload(payload)
    with pytest.raises(ValueError, match="not a WeCom Customer Service inbound payload"):
        connector.parse_inbound_payload(payload)
