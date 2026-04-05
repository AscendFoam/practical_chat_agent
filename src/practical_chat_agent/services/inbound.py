from __future__ import annotations

from typing import Any

from practical_chat_agent.connectors.inbound.base import InboundConnector
from practical_chat_agent.core.bus import InMemoryEventBus
from practical_chat_agent.core.events import RuntimeEvent
from practical_chat_agent.core.models import AgentTurnResult
from practical_chat_agent.runtime.agent_runtime import AgentRuntime


class InboundEventService:
    """Normalizes connector payloads and forwards them into the runtime."""

    def __init__(
        self,
        *,
        connectors: dict[str, InboundConnector],
        runtime: AgentRuntime,
        event_bus: InMemoryEventBus | None = None,
    ) -> None:
        self.connectors = connectors
        self.runtime = runtime
        self.event_bus = event_bus

    def resolve_connector_name(
        self,
        *,
        payload: dict[str, Any],
        connector_name: str | None = None,
    ) -> str:
        explicit = connector_name or self._payload_connector_name(payload)
        if explicit is not None:
            if explicit not in self.connectors:
                raise ValueError(f"Unknown inbound connector: {explicit}")
            return explicit

        matches = [
            name
            for name, candidate in self.connectors.items()
            if candidate.can_handle_payload(payload)
        ]
        if len(matches) == 1:
            return matches[0]
        if len(matches) > 1:
            raise ValueError(
                "Payload matched multiple inbound connectors. Add connector_name to the file metadata.",
            )
        raise ValueError(
            "Unable to resolve inbound connector from payload. Add connector_name to the file metadata.",
        )

    def ingest(self, *, connector_name: str | None = None, payload: dict[str, Any]) -> AgentTurnResult:
        resolved_connector_name = self.resolve_connector_name(
            payload=payload,
            connector_name=connector_name,
        )
        connector = self.connectors.get(resolved_connector_name)
        if connector is None:
            raise ValueError(f"Unknown inbound connector: {resolved_connector_name}")

        inbound = connector.parse_inbound_payload(payload)

        if self.event_bus is not None:
            self.event_bus.publish(
                RuntimeEvent(
                    topic="inbound.event.received",
                    payload={
                        "connector_name": inbound.connector_name,
                        "agent_id": inbound.agent_id,
                        "event_id": inbound.event.event_id,
                        "platform": inbound.event.platform.value,
                    },
                ),
            )

        return self.runtime.handle_inbound_event(agent_id=inbound.agent_id, event=inbound.event)

    @staticmethod
    def _payload_connector_name(payload: dict[str, Any]) -> str | None:
        direct = payload.get("connector_name")
        if isinstance(direct, str) and direct:
            return direct

        meta = payload.get("_meta")
        if isinstance(meta, dict):
            meta_name = meta.get("connector_name")
            if isinstance(meta_name, str) and meta_name:
                return meta_name

        return None
