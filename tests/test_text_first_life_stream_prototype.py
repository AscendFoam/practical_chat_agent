"""T323 text-first life-stream prototype tests.

All records are synthetic. These tests define local private review feed states
only; they do not publish, share, export, schedule, send, or connect to
platforms.
"""

from __future__ import annotations

import json

from practical_chat_agent.core.models import RoleDynamicPost
from practical_chat_agent.services.virtual_life_engine import (
    VirtualLifeEngine,
    VirtualLifeSeedContext,
)
from practical_chat_agent.ui.text_first_life_stream import (
    TextFirstLifeStreamPrototype,
    TextFirstLifeStreamRequest,
)


def _post(**overrides: object) -> RoleDynamicPost:
    context = VirtualLifeSeedContext(
        user_id="user_synthetic",
        persona_id="persona_synthetic",
        mood_label="quiet",
        activity_label="listening to rain",
        topic_label="speaking slowly",
        memory_refs=["mev_synthetic"],
        relationship_context_refs=["relctx_synthetic"],
    )
    post = VirtualLifeEngine().create_post(context)
    if not overrides:
        return post
    data = post.model_dump(mode="python")
    data.update(overrides)
    return RoleDynamicPost(**data)


def _state(**overrides: object):
    data: dict[str, object] = {
        "user_id": "user_synthetic",
        "posts": [_post()],
    }
    data.update(overrides)
    return TextFirstLifeStreamPrototype().project(TextFirstLifeStreamRequest(**data))


def test_generated_post_appears_as_review_only_private_feed_item() -> None:
    state = _state()

    assert state.screen == "life_stream_review"
    assert len(state.items) == 1
    item = state.items[0]
    assert item.review_status == "requires_review"
    assert item.visibility == "local_private_review"
    assert item.truth_disclosure == "imagined_ai_generated_content"
    assert item.content_status == "imagined_ai_generated"
    assert item.review_required is True


def test_visible_aigc_label_includes_imagined_not_real_world_disclosure() -> None:
    item = _state().items[0]

    assert item.aigc_label.visible_label_required is True
    assert "AI-generated" in item.aigc_label.visible_label_text
    assert "imagined" in item.aigc_label.visible_label_text.lower()
    assert "not real-world" in item.aigc_label.visible_label_text.lower()
    assert "imagined_content" in item.aigc_label.disclosure_labels
    assert "not_real_world_activity" in item.aigc_label.disclosure_labels


def test_memory_refs_remain_inspiration_only() -> None:
    item = _state().items[0]

    assert item.memory_refs == ["mev_synthetic"]
    assert item.memory_ref_usage == "inspiration_only"
    assert "memory_refs_are_inspiration_only" in item.review_notes


def test_factual_claim_posts_preserve_review_notes_without_fact_promotion() -> None:
    post = _post(
        contains_factual_claims=True,
        factual_claims_review_notes=["needs_human_fact_review"],
    )
    item = _state(posts=[post]).items[0]

    assert item.contains_factual_claims is True
    assert item.factual_claims_review_notes == ["needs_human_fact_review"]
    assert item.content_status == "imagined_ai_generated"
    assert "factual_claim_review_required" in item.review_notes


def test_leaving_local_review_is_blocked_without_consent_or_metadata() -> None:
    item = _state(aigc_export_share_consent_active=False, metadata_label_ready=False).items[0]

    assert item.leaving_local_review_blocked is True
    assert "aigc_export_share_consent_required" in item.block_reasons
    assert "implicit_metadata_label_required" in item.block_reasons


def test_life_stream_payload_has_no_publish_delivery_or_platform_fields() -> None:
    state = _state()

    serialized = json.dumps(state.model_dump(mode="json"), ensure_ascii=False).lower()

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


def test_life_stream_prototype_does_not_expose_runtime_or_outbound_methods() -> None:
    prototype = TextFirstLifeStreamPrototype()

    for method_name in (
        "publish",
        "share",
        "export",
        "send",
        "schedule",
        "deliver",
        "execute",
        "run_runtime",
    ):
        assert not hasattr(prototype, method_name)
