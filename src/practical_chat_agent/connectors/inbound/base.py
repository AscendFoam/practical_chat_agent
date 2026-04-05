from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from practical_chat_agent.core.models import InboundConnectorResult


class InboundConnector(ABC):
    """Base abstraction for official or semi-official inbound connectors."""

    connector_name: str

    @abstractmethod
    def can_handle_payload(self, payload: dict[str, Any]) -> bool:
        """Return whether this connector can parse the payload shape."""

    @abstractmethod
    def parse_inbound_payload(self, payload: dict[str, Any]) -> InboundConnectorResult:
        """Convert a raw platform payload into a normalized inbound event."""
