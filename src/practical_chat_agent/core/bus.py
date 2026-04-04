from __future__ import annotations

from collections import defaultdict
from typing import Callable

from practical_chat_agent.core.events import RuntimeEvent

EventHandler = Callable[[RuntimeEvent], None]


class InMemoryEventBus:
    """Minimal synchronous event bus for P0 wiring."""

    def __init__(self) -> None:
        self._handlers: dict[str, list[EventHandler]] = defaultdict(list)

    def subscribe(self, topic: str, handler: EventHandler) -> None:
        self._handlers[topic].append(handler)

    def publish(self, event: RuntimeEvent) -> None:
        for handler in self._handlers.get(event.topic, []):
            handler(event)

