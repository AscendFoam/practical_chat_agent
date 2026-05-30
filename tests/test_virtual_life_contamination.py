"""T293 imagined/factual contamination tests.

All inputs are synthetic. These tests prevent imagined virtual life drafts from
becoming factual memory or real-world activity evidence.
"""

from __future__ import annotations

import json

import pytest
from pydantic import ValidationError

from practical_chat_agent.core.models import (
    MemoryEvent,
    MemoryProvenance,
    MemoryRetrievalBundle,
    MemoryRetrievalBundleItem,
    RoleDynamicPost,
)
from practical_chat_agent.services.virtual_life_engine import (
    VirtualLifeEngine,
    VirtualLifeSeedContext,
)


def _post() -> RoleDynamicPost:
    return VirtualLifeEngine().create_post(
        VirtualLifeSeedContext(
            user_id="user_synthetic",
            persona_id="persona_synthetic",
            mood_label="quiet",
            activity_label="reading",
            topic_label="small rituals",
            memory_refs=["mev_inspiration"],
            relationship_context_refs=["relctx_synthetic"],
        )
    )


class TestVirtualLifeContamination:
    def test_imagined_post_cannot_seed_factual_memory_event(self) -> None:
        post = _post()

        with pytest.raises(ValidationError):
            MemoryEvent(
                user_id=post.user_id,
                event_type="factual",
                truth_status="evidence_backed",
                summary=post.content_text,
                provenance=MemoryProvenance(
                    source_type="imagined_generation",
                    evidence_refs=[post.post_id],
                ),
                sensitivity="low",
            )

    def test_memory_refs_remain_inspiration_only(self) -> None:
        post = _post()

        assert post.memory_refs == ["mev_inspiration"]
        assert post.memory_ref_usage == "inspiration_only"
        assert post.content_status == "imagined_ai_generated"

    def test_engine_created_posts_retain_imagined_labels(self) -> None:
        post = _post()

        assert post.truth_disclosure == "imagined_ai_generated_content"
        assert "imagined_content" in post.aigc_metadata.disclosure_labels
        assert "not_real_world_activity" in post.aigc_metadata.disclosure_labels

    def test_serialized_post_has_no_factual_memory_promotion_fields(self) -> None:
        post = _post()
        serialized = json.dumps(post.model_dump(mode="json"), ensure_ascii=False).lower()

        for forbidden in (
            "factual_memory_id",
            "promote_to_memory",
            "evidence_for_factual_memory",
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
        assert "not_real_world_activity" in serialized

    def test_factual_retrieval_bundle_cannot_use_imagined_post_as_evidence(self) -> None:
        post = _post()

        with pytest.raises(ValidationError):
            event = MemoryEvent(
                user_id=post.user_id,
                event_type="factual",
                truth_status="evidence_backed",
                summary=post.content_text,
                provenance=MemoryProvenance(
                    source_type="imagined_generation",
                    evidence_refs=[post.post_id],
                ),
                sensitivity="low",
            )
            MemoryRetrievalBundle(
                purpose="factual_response",
                query_summary="answer using factual memories",
                items=[MemoryRetrievalBundleItem.from_event(event, retrieval_context="factual")],
            )
