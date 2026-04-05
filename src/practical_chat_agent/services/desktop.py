from __future__ import annotations

from practical_chat_agent.connectors.desktop.base import DesktopConnector
from practical_chat_agent.core.bus import InMemoryEventBus
from practical_chat_agent.core.events import RuntimeEvent
from practical_chat_agent.core.models import DesktopScanResult


class DesktopScanService:
    """Coordinates desktop connector scans and emits lightweight runtime events."""

    def __init__(
        self,
        *,
        connectors: dict[str, DesktopConnector],
        event_bus: InMemoryEventBus | None = None,
    ) -> None:
        self.connectors = connectors
        self.event_bus = event_bus

    def scan(
        self,
        *,
        connector_name: str,
        account_id: str,
        conversation_hint: str | None = None,
        force_ocr: bool = False,
        save_capture: bool = False,
    ) -> DesktopScanResult:
        connector = self.connectors.get(connector_name)
        if connector is None:
            raise ValueError(f"Unknown desktop connector: {connector_name}")

        result = connector.scan_current_conversation(
            account_id=account_id,
            conversation_hint=conversation_hint,
            force_ocr=force_ocr,
            save_capture=save_capture,
        )

        if self.event_bus is not None:
            self.event_bus.publish(
                RuntimeEvent(
                    topic="desktop.scan.completed",
                    payload={
                        "connector_name": result.connector_name,
                        "platform": result.platform.value,
                        "account_id": result.account_id,
                        "message_count": len(result.messages),
                    },
                ),
            )

        return result
