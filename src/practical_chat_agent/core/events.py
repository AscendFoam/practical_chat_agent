from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from practical_chat_agent.core.models import utc_now


class RuntimeEvent(BaseModel):
    topic: str
    payload: dict[str, Any] = Field(default_factory=dict)
    emitted_at: datetime = Field(default_factory=utc_now)

