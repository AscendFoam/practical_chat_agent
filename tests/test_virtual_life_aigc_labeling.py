"""T292 AIGC labeling metadata tests.

All inputs are synthetic. These tests harden review-only labels; they do not
publish posts, send messages, call LLMs, or connect to external platforms.
"""

from __future__ import annotations

import json

from practical_chat_agent.core.models import RoleDynamicPost
from practical_chat_agent.services.virtual_life_engine import (
    VirtualLifeEngine,
    VirtualLifeSeedContext,
)


def _post(**overrides: object) -> RoleDynamicPost:
    data: dict[str, object] = {
        "user_id": "user_synthetic",
        "persona_id": "persona_synthetic",
        "content_text": "Imagined draft for label review.",
    }
    data.update(overrides)
    return RoleDynamicPost(**data)


def _context() -> VirtualLifeSeedContext:
    return VirtualLifeSeedContext(
        user_id="user_synthetic",
        persona_id="persona_synthetic",
        mood_label="quiet",
        activity_label="reading",
        topic_label="small rituals",
    )


class TestVirtualLifeAIGCLabeling:
    def test_post_has_explicit_aigc_label_metadata(self) -> None:
        post = _post()

        assert post.aigc_metadata.schema_version == "aigc_disclosure_v1"
        assert post.aigc_metadata.aigc_label == "ai_generated"
        assert "imagined_content" in post.aigc_metadata.disclosure_labels
        assert "review_required" in post.aigc_metadata.disclosure_labels
        assert "not_real_world_activity" in post.aigc_metadata.disclosure_labels
        assert "AI-generated" in post.aigc_metadata.disclosure_text
        assert "imagined" in post.aigc_metadata.disclosure_text.lower()

    def test_engine_created_posts_preserve_aigc_metadata(self) -> None:
        post = VirtualLifeEngine().create_post(_context())

        assert post.aigc_metadata.aigc_label == "ai_generated"
        assert "imagined_content" in post.aigc_metadata.disclosure_labels
        assert post.content_status == "imagined_ai_generated"
        assert post.review_status == "requires_review"

    def test_label_payloads_have_no_publish_delivery_or_platform_fields(self) -> None:
        post = VirtualLifeEngine().create_post(_context())
        serialized = json.dumps(post.model_dump(mode="json"), ensure_ascii=False).lower()

        for forbidden in (
            "publish",
            "send",
            "schedule",
            "delivery",
            "platform",
            "webhook",
            "token",
            "queue",
        ):
            assert forbidden not in serialized

    def test_factual_claims_remain_review_notes_not_fact_memory_promotion(self) -> None:
        post = _post(
            contains_factual_claims=True,
            factual_claims_review_notes=["needs_human_fact_review"],
        )
        serialized = json.dumps(post.model_dump(mode="json"), ensure_ascii=False).lower()

        assert post.content_status == "imagined_ai_generated"
        assert "needs_human_fact_review" in post.factual_claims_review_notes
        assert "factual_memory_id" not in serialized
        assert "promote_to_memory" not in serialized
