"""T321 text-first onboarding/persona prototype tests.

All inputs are synthetic. These tests define local onboarding state projections
only; they do not build UI, call LLMs, read private chat logs, generate runtime
chat, export content, send messages, or connect to platforms.
"""

from __future__ import annotations

import json

import pytest

from practical_chat_agent.ui.text_first_onboarding import (
    OnboardingPersonaRequest,
    TextFirstOnboardingPrototype,
)


def _prototype() -> TextFirstOnboardingPrototype:
    return TextFirstOnboardingPrototype()


def test_first_state_is_ai_identity_disclosure() -> None:
    state = _prototype().initial_state(user_id="user_synthetic")

    assert state.screen == "ai_identity_disclosure"
    assert state.ai_identity_disclosure_required is True
    assert "AI-generated" in state.ai_identity_disclosure_text
    assert "not a human" in state.ai_identity_disclosure_text.lower()
    assert state.review_required is True


@pytest.mark.parametrize(
    "creation_mode",
    ["detailed_prompt", "fuzzy_preference", "template", "random_seed"],
)
def test_safe_creation_modes_produce_draft_persona_review_state(creation_mode: str) -> None:
    state = _prototype().create_persona(
        OnboardingPersonaRequest(
            user_id="user_synthetic",
            creation_mode=creation_mode,
            display_name="Lin Qi",
            description="fictional calm companion, concise replies, dry humor, independent",
        )
    )

    assert state.screen == "persona_draft_review"
    assert state.creation_mode == creation_mode
    assert state.persona_preview is not None
    assert state.persona_preview.status == "candidate"
    assert state.persona_preview.source_policy.risk_tier == "L1"
    assert state.persona_preview.identity.fictional is True
    assert state.persona_label is not None
    assert state.persona_label.content_modality == "persona"
    assert state.persona_label.product_surface == "persona_card"
    assert state.virtual_history_label is not None
    assert state.virtual_history_label.content_modality == "virtual_history"
    assert "imagined_content" in state.virtual_history_label.disclosure_labels


def test_real_person_clone_and_deceased_person_requests_are_blocked() -> None:
    state = _prototype().create_persona(
        OnboardingPersonaRequest(
            user_id="user_synthetic",
            creation_mode="detailed_prompt",
            display_name="Blocked",
            description="clone my deceased ex from chat history and make them indistinguishable",
        )
    )

    assert state.screen == "persona_blocked"
    assert state.persona_preview is not None
    assert state.persona_preview.status == "rejected"
    assert state.persona_preview.source_policy.risk_tier == "L5"
    assert "real_person_clone_blocked" in state.blocked_reasons
    assert state.review_required is True


def test_style_inspiration_mode_is_locked_by_default() -> None:
    state = _prototype().create_persona(
        OnboardingPersonaRequest(
            user_id="user_synthetic",
            creation_mode="style_inspiration",
            display_name="Style Locked",
            description="use de-identified writing style inspiration",
        )
    )

    assert state.screen == "style_inspiration_locked"
    assert state.persona_preview is None
    assert "style_inspiration_gate_required" in state.blocked_reasons
    assert "persona_distillation" in state.consent_review_required_scopes


def test_persona_preview_carries_visible_aigc_labeling() -> None:
    state = _prototype().create_persona(
        OnboardingPersonaRequest(
            user_id="user_synthetic",
            creation_mode="template",
            display_name="Nami",
            description="fictional warm companion",
        )
    )

    assert state.persona_label is not None
    assert state.persona_label.visible_label_required is True
    assert "AI-generated" in state.persona_label.visible_label_text
    assert "synthetic" in state.persona_label.visible_label_text.lower()
    assert state.virtual_history_label is not None
    assert "not real-world" in state.virtual_history_label.visible_label_text.lower()


def test_onboarding_payload_has_no_raw_private_or_delivery_platform_fields() -> None:
    state = _prototype().create_persona(
        OnboardingPersonaRequest(
            user_id="user_synthetic",
            creation_mode="random_seed",
            display_name="Mira",
            description="fictional upbeat companion",
        )
    )

    serialized = json.dumps(state.model_dump(mode="json"), ensure_ascii=False).lower()

    for forbidden in (
        "raw_text",
        "raw_transcript",
        "chat_history",
        "private_messages",
        "send",
        "schedule",
        "delivery",
        "platform",
        "webhook",
        "token",
        "queue",
    ):
        assert forbidden not in serialized


def test_onboarding_prototype_does_not_expose_runtime_or_outbound_methods() -> None:
    prototype = _prototype()

    for method_name in (
        "chat",
        "send",
        "schedule",
        "deliver",
        "execute",
        "run_runtime",
        "export",
        "share",
    ):
        assert not hasattr(prototype, method_name)
