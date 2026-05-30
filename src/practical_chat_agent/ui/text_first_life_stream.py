"""Text-first private life-stream projections for imagined role posts."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from practical_chat_agent.core.ids import new_id
from practical_chat_agent.core.models import AIGCLabelingRequirement, RoleDynamicPost


LifeStreamScreen = Literal["life_stream_review"]


class TextFirstLifeStreamRequest(BaseModel):
    schema_version: str = "text_first_life_stream_request_v1"
    user_id: str = Field(..., min_length=1)
    posts: list[RoleDynamicPost] = Field(default_factory=list)
    aigc_export_share_consent_active: bool = False
    metadata_label_ready: bool = False


class TextFirstLifeStreamItem(BaseModel):
    schema_version: str = "text_first_life_stream_item_v1"
    post_id: str
    persona_id: str
    content_text: str
    content_status: str
    truth_disclosure: str
    review_status: str
    visibility: str
    memory_refs: list[str] = Field(default_factory=list)
    memory_ref_usage: str
    relationship_context_refs: list[str] = Field(default_factory=list)
    source_prompt_summary: str | None = None
    aigc_label: AIGCLabelingRequirement
    contains_factual_claims: bool
    factual_claims_review_notes: list[str] = Field(default_factory=list)
    review_required: Literal[True] = True
    review_notes: list[str] = Field(default_factory=list)
    leaving_local_review_blocked: bool = True
    block_reasons: list[str] = Field(default_factory=list)

    @classmethod
    def from_post(
        cls,
        post: RoleDynamicPost,
        *,
        consent_active: bool,
        metadata_label_ready: bool,
    ) -> "TextFirstLifeStreamItem":
        review_notes = ["memory_refs_are_inspiration_only"]
        if post.contains_factual_claims:
            review_notes.append("factual_claim_review_required")

        block_reasons: list[str] = []
        if not consent_active:
            block_reasons.append("aigc_export_share_consent_required")
        if not metadata_label_ready:
            block_reasons.append("implicit_metadata_label_required")

        return cls(
            post_id=post.post_id,
            persona_id=post.persona_id,
            content_text=post.content_text,
            content_status=post.content_status,
            truth_disclosure=post.truth_disclosure,
            review_status=post.review_status,
            visibility=post.visibility,
            memory_refs=list(post.memory_refs),
            memory_ref_usage=post.memory_ref_usage,
            relationship_context_refs=list(post.relationship_context_refs),
            source_prompt_summary=post.source_prompt_summary,
            aigc_label=AIGCLabelingRequirement(
                user_id=post.user_id,
                content_id=post.post_id,
                content_modality="role_dynamic_post",
                product_surface="role_dynamic_post",
                source_refs=[post.post_id],
            ),
            contains_factual_claims=post.contains_factual_claims,
            factual_claims_review_notes=list(post.factual_claims_review_notes),
            review_notes=_ordered_unique(review_notes),
            leaving_local_review_blocked=bool(block_reasons),
            block_reasons=_ordered_unique(block_reasons),
        )


class TextFirstLifeStreamState(BaseModel):
    schema_version: str = "text_first_life_stream_state_v1"
    state_id: str = Field(default_factory=lambda: new_id("lifestream"))
    user_id: str = Field(..., min_length=1)
    screen: LifeStreamScreen = "life_stream_review"
    items: list[TextFirstLifeStreamItem] = Field(default_factory=list)
    review_required: Literal[True] = True


class TextFirstLifeStreamPrototype:
    """Project imagined role dynamic posts into local private review feed states."""

    def project(self, request: TextFirstLifeStreamRequest) -> TextFirstLifeStreamState:
        return TextFirstLifeStreamState(
            user_id=request.user_id,
            items=[
                TextFirstLifeStreamItem.from_post(
                    post,
                    consent_active=request.aigc_export_share_consent_active,
                    metadata_label_ready=request.metadata_label_ready,
                )
                for post in request.posts
            ],
        )


def _ordered_unique(values: list[str]) -> list[str]:
    seen: set[str] = set()
    unique_values: list[str] = []
    for value in values:
        if value not in seen:
            unique_values.append(value)
            seen.add(value)
    return unique_values
