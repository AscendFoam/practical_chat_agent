"""T294 Virtual life review card tests.

All inputs are synthetic local posts. These tests render review artifacts only;
they do not publish posts, send messages, call LLMs, or connect to platforms.
"""

from __future__ import annotations

import json

from practical_chat_agent.core.models import RoleDynamicPost
from practical_chat_agent.services.virtual_life_engine import (
    VirtualLifeEngine,
    VirtualLifeSeedContext,
)
from practical_chat_agent.services.virtual_life_review_card import VirtualLifeReviewCardService


def _post(**overrides: object) -> RoleDynamicPost:
    data: dict[str, object] = {
        "user_id": "user_synthetic",
        "persona_id": "persona_synthetic",
        "content_text": "Imagined draft for review card.",
        "memory_refs": ["mev_inspiration"],
        "relationship_context_refs": ["relctx_synthetic"],
        "safety_notes": ["synthetic_test"],
    }
    data.update(overrides)
    return RoleDynamicPost(**data)


class TestVirtualLifeReviewCard:
    def test_card_renders_labels_and_review_status(self) -> None:
        post = VirtualLifeEngine().create_post(
            VirtualLifeSeedContext(
                user_id="user_synthetic",
                persona_id="persona_synthetic",
                mood_label="quiet",
                activity_label="reading",
                topic_label="small rituals",
            )
        )

        card = VirtualLifeReviewCardService().render(post)

        assert card.schema_version == "virtual_life_review_card_v1"
        assert card.card_id.startswith("vlcard_")
        assert card.post_id == post.post_id
        assert card.persona_id == post.persona_id
        assert card.content_text == post.content_text
        assert card.review_status == "requires_review"
        assert card.aigc_label == "ai_generated"
        assert "imagined_content" in card.disclosure_labels
        assert "approve_for_demo" in card.review_actions
        assert "reject" in card.review_actions

    def test_factual_claim_cards_expose_conservative_review_action(self) -> None:
        post = _post(
            contains_factual_claims=True,
            factual_claims_review_notes=["needs_human_fact_review"],
        )

        card = VirtualLifeReviewCardService().render(post)

        assert "flag_factual_claims" in card.review_actions
        assert "approve_for_demo" not in card.review_actions
        assert card.factual_claims_review_notes == ["needs_human_fact_review"]

    def test_memory_refs_remain_inspiration_only(self) -> None:
        card = VirtualLifeReviewCardService().render(_post())

        assert card.memory_refs == ["mev_inspiration"]
        assert card.memory_ref_usage == "inspiration_only"

    def test_card_payload_has_no_publish_delivery_or_platform_fields(self) -> None:
        card = VirtualLifeReviewCardService().render(_post())
        serialized = json.dumps(card.model_dump(mode="json"), ensure_ascii=False).lower()

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

    def test_service_does_not_expose_runtime_or_delivery_methods(self) -> None:
        service = VirtualLifeReviewCardService()

        for method_name in (
            "publish",
            "send",
            "schedule",
            "deliver",
            "execute",
            "run_runtime",
            "call_llm",
        ):
            assert not hasattr(service, method_name)
