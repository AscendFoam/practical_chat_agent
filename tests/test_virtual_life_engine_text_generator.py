"""T291 Virtual life engine text generator tests.

All inputs are synthetic seed metadata. These tests define deterministic local
post draft creation only; they do not call LLMs, publish posts, send messages,
or connect to external platforms.
"""

from __future__ import annotations

import json

from practical_chat_agent.services.virtual_life_engine import (
    VirtualLifeEngine,
    VirtualLifeSeedContext,
)


def _context(**overrides: object) -> VirtualLifeSeedContext:
    data: dict[str, object] = {
        "user_id": "user_synthetic",
        "persona_id": "persona_synthetic",
        "mood_label": "quiet",
        "activity_label": "listening to rain",
        "topic_label": "speaking slowly",
        "memory_refs": ["mev_synthetic"],
        "relationship_context_refs": ["relctx_synthetic"],
    }
    data.update(overrides)
    return VirtualLifeSeedContext(**data)


class TestVirtualLifeEngine:
    def test_post_text_is_deterministic_from_seed_context(self) -> None:
        engine = VirtualLifeEngine()
        context = _context()

        post_a = engine.create_post(context)
        post_b = engine.create_post(context)

        assert post_a.content_text == post_b.content_text
        assert "quiet" in post_a.content_text
        assert "listening to rain" in post_a.content_text
        assert "speaking slowly" in post_a.content_text

    def test_memory_and_relationship_refs_are_preserved(self) -> None:
        post = VirtualLifeEngine().create_post(_context())

        assert post.memory_refs == ["mev_synthetic"]
        assert post.relationship_context_refs == ["relctx_synthetic"]
        assert post.source_prompt_summary == "quiet | listening to rain | speaking slowly"

    def test_generated_post_preserves_imagined_review_only_labels(self) -> None:
        post = VirtualLifeEngine().create_post(_context())

        assert post.content_status == "imagined_ai_generated"
        assert post.truth_disclosure == "imagined_ai_generated_content"
        assert post.review_status == "requires_review"
        assert post.visibility == "local_private_review"

    def test_payloads_have_no_publish_delivery_or_platform_fields(self) -> None:
        context = _context()
        post = VirtualLifeEngine().create_post(context)
        serialized = json.dumps(
            {
                "context": context.model_dump(mode="json"),
                "post": post.model_dump(mode="json"),
            },
            ensure_ascii=False,
        ).lower()

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

    def test_engine_does_not_expose_runtime_or_delivery_methods(self) -> None:
        engine = VirtualLifeEngine()

        for method_name in (
            "publish",
            "send",
            "schedule",
            "deliver",
            "execute",
            "run_runtime",
            "call_llm",
        ):
            assert not hasattr(engine, method_name)
