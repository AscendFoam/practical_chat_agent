"""T290 Role dynamic post schema tests.

All inputs are synthetic. These tests define review-only virtual life stream
draft schemas; they do not generate post text, publish posts, send messages, or
connect to external platforms.
"""

from __future__ import annotations

import json

import pytest
from pydantic import ValidationError

from practical_chat_agent.core.models import RoleDynamicPost


def _post(**overrides: object) -> RoleDynamicPost:
    data: dict[str, object] = {
        "user_id": "user_synthetic",
        "persona_id": "persona_synthetic",
        "content_text": "Practiced speaking more slowly while listening to rain.",
        "memory_refs": ["mev_synthetic"],
        "relationship_context_refs": ["relctx_synthetic"],
        "source_prompt_summary": "Synthetic rainy-day virtual life draft.",
    }
    data.update(overrides)
    return RoleDynamicPost(**data)


class TestRoleDynamicPost:
    def test_post_defaults_to_imagined_review_only_draft(self) -> None:
        post = _post()

        assert post.schema_version == "role_dynamic_post_v1"
        assert post.post_id.startswith("rolepost_")
        assert post.content_status == "imagined_ai_generated"
        assert post.truth_disclosure == "imagined_ai_generated_content"
        assert post.review_status == "requires_review"
        assert post.visibility == "local_private_review"
        assert post.memory_refs == ["mev_synthetic"]
        assert post.relationship_context_refs == ["relctx_synthetic"]

    def test_rejects_non_imagined_content_status_or_public_visibility(self) -> None:
        with pytest.raises(ValidationError):
            _post(content_status="factual")

        with pytest.raises(ValidationError):
            _post(visibility="public_feed")

    def test_rejects_empty_content(self) -> None:
        with pytest.raises(ValidationError):
            _post(content_text="")

    def test_factual_claims_require_review_notes_without_fact_promotion(self) -> None:
        with pytest.raises(ValidationError):
            _post(contains_factual_claims=True)

        post = _post(
            contains_factual_claims=True,
            factual_claims_review_notes=["needs_human_fact_review"],
        )

        assert post.contains_factual_claims is True
        assert post.factual_claims_review_notes == ["needs_human_fact_review"]
        assert post.content_status == "imagined_ai_generated"

    def test_serialized_post_has_no_publish_delivery_or_platform_fields(self) -> None:
        post = _post()
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
