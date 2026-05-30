"""Review-only cards for virtual life stream drafts."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from practical_chat_agent.core.ids import new_id
from practical_chat_agent.core.models import RoleDynamicPost


VirtualLifeReviewAction = Literal["approve_for_demo", "reject", "request_changes", "flag_factual_claims"]


class VirtualLifeReviewCard(BaseModel):
    schema_version: str = "virtual_life_review_card_v1"
    card_id: str = Field(default_factory=lambda: new_id("vlcard"))
    post_id: str
    user_id: str
    persona_id: str
    content_text: str
    content_status: str
    truth_disclosure: str
    review_status: str
    aigc_label: str
    disclosure_labels: list[str] = Field(default_factory=list)
    disclosure_text: str
    memory_refs: list[str] = Field(default_factory=list)
    memory_ref_usage: str
    factual_claims_review_notes: list[str] = Field(default_factory=list)
    safety_notes: list[str] = Field(default_factory=list)
    review_actions: list[VirtualLifeReviewAction] = Field(default_factory=list)


class VirtualLifeReviewCardService:
    """Render virtual life posts into local human-review artifacts."""

    def render(self, post: RoleDynamicPost) -> VirtualLifeReviewCard:
        return VirtualLifeReviewCard(
            post_id=post.post_id,
            user_id=post.user_id,
            persona_id=post.persona_id,
            content_text=post.content_text,
            content_status=post.content_status,
            truth_disclosure=post.truth_disclosure,
            review_status=post.review_status,
            aigc_label=post.aigc_metadata.aigc_label,
            disclosure_labels=list(post.aigc_metadata.disclosure_labels),
            disclosure_text=post.aigc_metadata.disclosure_text,
            memory_refs=list(post.memory_refs),
            memory_ref_usage=post.memory_ref_usage,
            factual_claims_review_notes=list(post.factual_claims_review_notes),
            safety_notes=list(post.safety_notes),
            review_actions=self._review_actions(post),
        )

    @staticmethod
    def _review_actions(post: RoleDynamicPost) -> list[VirtualLifeReviewAction]:
        if post.contains_factual_claims:
            return ["flag_factual_claims", "reject", "request_changes"]
        return ["approve_for_demo", "reject", "request_changes"]
