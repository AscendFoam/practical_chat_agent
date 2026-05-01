from __future__ import annotations

import json
from urllib import error, request

from practical_chat_agent.connectors.delivery.base import DeliveryConnector, DeliveryResult
from practical_chat_agent.core.models import ActionExecutionRecord


class TelegramBotDeliveryConnector(DeliveryConnector):
    """Official Telegram Bot API delivery connector for approved text actions."""

    connector_name = "telegram_bot_delivery"
    platform = "telegram"

    def __init__(
        self,
        *,
        bot_token: str | None,
        enabled: bool = True,
        timeout_seconds: float = 20.0,
    ) -> None:
        self.bot_token = bot_token
        self.enabled = enabled
        self.timeout_seconds = timeout_seconds

    def send_text_draft(self, action: ActionExecutionRecord) -> DeliveryResult:
        return DeliveryResult(
            connector_name=self.connector_name,
            status="draft",
            raw={
                "chat_id": action.channel_id,
                "text": action.message_text or "",
                "note": "Telegram Bot API does not expose a remote draft primitive; draft retained in local outbox.",
            },
        )

    def send_text(self, action: ActionExecutionRecord) -> DeliveryResult:
        if not self.enabled:
            raise RuntimeError("Telegram delivery is disabled by TELEGRAM_DELIVERY_ENABLED=false.")
        if not self.bot_token:
            raise RuntimeError("TELEGRAM_BOT_TOKEN is not configured.")
        text = (action.message_text or "").strip()
        if not text:
            raise ValueError("Cannot send an empty Telegram text message.")

        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        payload = {
            "chat_id": action.channel_id,
            "text": text,
        }
        encoded = json.dumps(payload).encode("utf-8")
        req = request.Request(
            url,
            data=encoded,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with request.urlopen(req, timeout=self.timeout_seconds) as response:
                body = response.read().decode("utf-8")
        except error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"Telegram sendMessage failed: HTTP {exc.code} {detail}") from exc
        except error.URLError as exc:
            raise RuntimeError(f"Telegram sendMessage failed: {exc.reason}") from exc

        raw = json.loads(body) if body else {}
        if not raw.get("ok", False):
            raise RuntimeError(f"Telegram sendMessage returned failure: {raw}")
        provider_message_id = None
        result = raw.get("result")
        if isinstance(result, dict) and result.get("message_id") is not None:
            provider_message_id = str(result["message_id"])
        return DeliveryResult(
            connector_name=self.connector_name,
            status="sent",
            provider_message_id=provider_message_id,
            raw=raw,
        )
