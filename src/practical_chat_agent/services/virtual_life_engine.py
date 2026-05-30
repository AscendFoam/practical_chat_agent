"""Deterministic local virtual life stream draft engine."""

from __future__ import annotations

from pydantic import BaseModel, Field

from practical_chat_agent.core.models import RoleDynamicPost


class VirtualLifeSeedContext(BaseModel):
    user_id: str = Field(..., min_length=1)
    persona_id: str = Field(..., min_length=1)
    mood_label: str = Field(..., min_length=1)
    activity_label: str = Field(..., min_length=1)
    topic_label: str = Field(..., min_length=1)
    memory_refs: list[str] = Field(default_factory=list)
    relationship_context_refs: list[str] = Field(default_factory=list)
    safety_notes: list[str] = Field(default_factory=list)


class VirtualLifeEngine:
    """Create deterministic review-only virtual life stream drafts."""

    def create_post(self, context: VirtualLifeSeedContext) -> RoleDynamicPost:
        return RoleDynamicPost(
            user_id=context.user_id,
            persona_id=context.persona_id,
            content_text=self._content_text(context),
            memory_refs=list(context.memory_refs),
            relationship_context_refs=list(context.relationship_context_refs),
            source_prompt_summary=self._source_prompt_summary(context),
            safety_notes=["imagined_virtual_life_draft", *context.safety_notes],
        )

    @staticmethod
    def _content_text(context: VirtualLifeSeedContext) -> str:
        return (
            f"Imagined moment: feeling {context.mood_label} while "
            f"{context.activity_label}, thinking about {context.topic_label}."
        )

    @staticmethod
    def _source_prompt_summary(context: VirtualLifeSeedContext) -> str:
        return f"{context.mood_label} | {context.activity_label} | {context.topic_label}"
