from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel, Field

from practical_chat_agent.core.models import ActionExecutionRecord


class DeliveryResult(BaseModel):
    connector_name: str
    status: str = "ok"
    provider_message_id: str | None = None
    raw: dict[str, Any] = Field(default_factory=dict)


class DeliveryConnector(ABC):
    connector_name: str
    platform: str

    @abstractmethod
    def send_text_draft(self, action: ActionExecutionRecord) -> DeliveryResult: ...

    @abstractmethod
    def send_text(self, action: ActionExecutionRecord) -> DeliveryResult: ...
