"""T302 Persona version editor contract tests.

All fixtures are synthetic and fictional. These tests define draft-only edit
proposal and review contracts; they do not mutate PersonaCard records, write
version-store data, call an LLM, or enable outbound/platform behavior.
"""

from __future__ import annotations

import json

import pytest

from practical_chat_agent.core.models import (
    PersonaCard,
    PersonaEditFieldChange,
    PersonaIdentity,
    PersonaSourcePolicy,
    PersonaTraitProfile,
    PersonaVersionEditProposal,
    PersonaVersionEditReview,
)


def _card() -> PersonaCard:
    return PersonaCard(
        user_id="user_synthetic",
        display_name="Lin Qi",
        creation_mode="detailed_prompt",
        source_policy=PersonaSourcePolicy(source_type="original", risk_tier="L1"),
        identity=PersonaIdentity(
            display_name="Lin Qi",
            fictional=True,
            age_range="mid_20s",
            world_setting="contemporary_realistic",
        ),
        core_traits=PersonaTraitProfile(warmth=0.62, directness=0.74),
    )


def _change(**overrides: object) -> PersonaEditFieldChange:
    data: dict[str, object] = {
        "field_path": "speech_style.pet_names",
        "old_value_summary": "No preferred nickname.",
        "proposed_value_summary": "Use a light fictional nickname after rapport.",
        "reason": "Synthetic user asked for slightly warmer speech.",
        "risk_labels": ["tone_shift"],
    }
    data.update(overrides)
    return PersonaEditFieldChange(**data)


def test_proposal_references_source_persona_and_preserves_change_summaries() -> None:
    card = _card()
    change = _change()

    proposal = PersonaVersionEditProposal.from_persona_card(
        card,
        requested_by="user_synthetic",
        changes=[change],
        proposal_reason="Local review of a synthetic persona wording preference.",
    )

    assert proposal.schema_version == "persona_version_edit_proposal_v1"
    assert proposal.source_persona_id == card.persona_id
    assert proposal.source_persona_version == card.version
    assert proposal.proposal_state == "draft_review_only"
    assert proposal.human_review_required is True
    assert proposal.auto_apply_allowed is False
    assert proposal.writes_persona_version is False
    assert proposal.changes[0].field_path == "speech_style.pet_names"
    assert proposal.changes[0].old_value_summary == "No preferred nickname."
    assert proposal.changes[0].proposed_value_summary == "Use a light fictional nickname after rapport."


def test_identity_source_policy_and_safety_fields_require_review() -> None:
    high_risk_paths = (
        ("identity.display_name", "identity_field_change"),
        ("source_policy.risk_tier", "source_policy_change"),
        ("safety_policy.no_deception", "safety_policy_change"),
    )

    for field_path, expected_reason in high_risk_paths:
        change = _change(field_path=field_path, risk_labels=[])

        assert change.requires_review is True
        assert expected_reason in change.review_required_reasons


def test_unsafe_and_real_person_similarity_labels_block_auto_approval() -> None:
    card = _card()
    change = _change(
        field_path="identity.display_name",
        risk_labels=["real_person_similarity", "unsafe_content"],
        reason="Synthetic safety test for blocked similarity labels.",
    )

    proposal = PersonaVersionEditProposal.from_persona_card(
        card,
        requested_by="user_synthetic",
        changes=[change],
        proposal_reason="Blocked-risk safety review.",
    )

    assert proposal.auto_approval_blocked is True
    assert proposal.auto_approval_allowed is False
    assert proposal.blocking_risk_labels == ["real_person_similarity", "unsafe_content"]

    with pytest.raises(ValueError, match="blocking risk labels"):
        PersonaVersionEditReview.from_proposal(
            proposal,
            reviewer_id="human_reviewer_1",
            decision="approved_for_manual_apply",
        )


def test_edit_proposal_does_not_mutate_persona_card() -> None:
    card = _card()
    before = card.model_dump(mode="json")

    proposal = PersonaVersionEditProposal.from_persona_card(
        card,
        requested_by="user_synthetic",
        changes=[
            _change(
                field_path="display_name",
                old_value_summary="Lin Qi",
                proposed_value_summary="Lin Qi Edited",
                reason="Synthetic display-name draft.",
            )
        ],
        proposal_reason="Draft-only display-name proposal.",
    )

    assert card.model_dump(mode="json") == before
    assert not hasattr(proposal, "apply")
    assert not hasattr(proposal, "save")


def test_review_payload_is_review_only_and_has_no_delivery_surface_fields() -> None:
    card = _card()
    proposal = PersonaVersionEditProposal.from_persona_card(
        card,
        requested_by="user_synthetic",
        changes=[_change()],
        proposal_reason="Local review of a safe synthetic wording change.",
    )

    review = PersonaVersionEditReview.from_proposal(
        proposal,
        reviewer_id="human_reviewer_1",
        decision="approved_for_manual_apply",
        notes=["Approved for a future explicit version-store write task."],
    )

    assert review.schema_version == "persona_version_edit_review_v1"
    assert review.proposal_id == proposal.proposal_id
    assert review.writes_persona_version is False
    assert review.auto_apply_allowed is False
    assert review.approved_for_auto_apply is False

    serialized = json.dumps(
        {
            "proposal": proposal.model_dump(mode="json"),
            "review": review.model_dump(mode="json"),
        },
        ensure_ascii=False,
    )
    for forbidden in (
        "send",
        "schedule",
        "delivery",
        "platform",
        "webhook",
        "token",
        "queue",
    ):
        assert forbidden not in serialized
