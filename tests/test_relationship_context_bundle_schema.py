"""T270 Relationship context bundle schema tests.

All fixtures are synthetic. These tests define local context packaging only;
they do not call LLMs, generate replies, schedule proactive messages, send
messages, or connect to external platforms.
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
    RelationshipContextBundle,
    RelationshipContextMemorySnapshot,
    RelationshipState,
)
from practical_chat_agent.services.persona_compiler import PersonaCompilerService
from practical_chat_agent.services.persona_review import PersonaReviewService


def _candidate_persona():
    return PersonaCompilerService().compile(
        {
            "user_id": "user_synthetic",
            "display_name": "Lin Qi",
            "creation_mode": "detailed_prompt",
            "description": "fictional calm concise companion with dry humor",
        }
    )


def _approved_persona():
    return PersonaReviewService().review(
        _candidate_persona(),
        decision="approve",
        reviewer_id="human_reviewer_1",
    )


def _relationship_state() -> RelationshipState:
    return RelationshipState(
        contact_id="user_synthetic",
        familiarity=0.6,
        trust=0.58,
        warmth=0.7,
        reciprocity=0.52,
        conflict_level=0.12,
        boundary_risk=0.2,
        initiative_allowance=0.4,
        intimacy_level=0.35,
        uncertainty=0.25,
        recent_interaction_temperature="warm",
        evidence_refs=["synthetic_event_001"],
        assessment_rationale="Synthetic relationship state for context bundle tests.",
        source_type="manual",
    )


def _factual_memory_bundle() -> MemoryRetrievalBundle:
    event = MemoryEvent(
        user_id="user_synthetic",
        event_type="factual",
        truth_status="evidence_backed",
        summary="User said they prefer concise check-ins.",
        provenance=MemoryProvenance(source_type="synthetic_test", evidence_refs=["synthetic_event_001"]),
        sensitivity="low",
    )
    return MemoryRetrievalBundle(
        purpose="factual_response",
        query_summary="build factual context",
        items=[MemoryRetrievalBundleItem.from_event(event, retrieval_context="factual")],
    )


class TestRelationshipContextBundle:
    def test_from_sources_builds_reviewable_local_context_bundle(self) -> None:
        persona = _approved_persona()
        relationship_state = _relationship_state()
        memory_bundle = _factual_memory_bundle()

        bundle = RelationshipContextBundle.from_sources(
            user_id="user_synthetic",
            persona=persona,
            relationship_state=relationship_state,
            memory_bundle=memory_bundle,
        )

        assert bundle.schema_version == "relationship_context_bundle_v1"
        assert bundle.user_id == "user_synthetic"
        assert bundle.persona.persona_id == persona.persona_id
        assert bundle.persona.truth_disclosure == "fictional_ai_persona"
        assert bundle.persona.runtime_ready is True
        assert bundle.relationship_dimensions["trust"] == 0.58
        assert bundle.relationship_dimensions["boundary_risk"] == 0.2
        assert bundle.memory.bundle_id == memory_bundle.bundle_id
        assert bundle.memory.purpose == "factual_response"
        assert bundle.source_persona_id == persona.persona_id
        assert bundle.source_relationship_state_id == relationship_state.state_id
        assert bundle.source_memory_bundle_id == memory_bundle.bundle_id

    def test_bundle_rejects_non_runtime_ready_persona(self) -> None:
        with pytest.raises(ValidationError):
            RelationshipContextBundle.from_sources(
                user_id="user_synthetic",
                persona=_candidate_persona(),
                relationship_state=_relationship_state(),
                memory_bundle=_factual_memory_bundle(),
            )

    def test_bundle_rejects_imagined_memory_as_factual_context(self) -> None:
        with pytest.raises(ValidationError):
            RelationshipContextBundle(
                user_id="user_synthetic",
                persona=RelationshipContextBundle.from_sources(
                    user_id="user_synthetic",
                    persona=_approved_persona(),
                    relationship_state=_relationship_state(),
                    memory_bundle=_factual_memory_bundle(),
                ).persona,
                relationship_dimensions=_relationship_state().dimension_snapshot(),
                memory=RelationshipContextMemorySnapshot(
                    bundle_id="memrb_synthetic",
                    purpose="factual_response",
                    selected_memory_ids=["mev_imagined"],
                    truth_status_counts={"imagined": 1},
                    imagined_memory_count=1,
                ),
                source_persona_id="persona_synthetic",
                source_relationship_state_id="relstate_synthetic",
                source_memory_bundle_id="memrb_synthetic",
            )

    def test_relationship_dimensions_reject_retention_or_manipulation_scores(self) -> None:
        base = RelationshipContextBundle.from_sources(
            user_id="user_synthetic",
            persona=_approved_persona(),
            relationship_state=_relationship_state(),
            memory_bundle=_factual_memory_bundle(),
        )

        with pytest.raises(ValidationError):
            data = base.model_dump()
            data["relationship_dimensions"] = {**base.relationship_dimensions, "retention_score": 0.9}
            RelationshipContextBundle(
                **data,
            )
        with pytest.raises(ValidationError):
            data = base.model_dump()
            data["relationship_dimensions"] = {**base.relationship_dimensions, "manipulation_score": 0.9}
            RelationshipContextBundle(
                **data,
            )

    def test_bundle_has_no_reply_delivery_or_platform_fields(self) -> None:
        bundle = RelationshipContextBundle.from_sources(
            user_id="user_synthetic",
            persona=_approved_persona(),
            relationship_state=_relationship_state(),
            memory_bundle=_factual_memory_bundle(),
        )
        serialized = json.dumps(bundle.model_dump(mode="json"), ensure_ascii=False)

        for forbidden in (
            "draft_reply",
            "reply_text",
            "send",
            "schedule",
            "delivery",
            "platform",
            "webhook",
        ):
            assert forbidden not in serialized
