from __future__ import annotations

from abc import ABC, abstractmethod

from practical_chat_agent.core.models import DesktopScanResult


class DesktopConnector(ABC):
    """Base abstraction for desktop UI automation connectors."""

    connector_name: str

    @abstractmethod
    def scan_current_conversation(
        self,
        *,
        account_id: str,
        conversation_hint: str | None = None,
        force_ocr: bool = False,
        save_capture: bool = False,
    ) -> DesktopScanResult:
        """Scan the currently visible desktop conversation."""
