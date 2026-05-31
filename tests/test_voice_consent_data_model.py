"""T331 Voice consent data model tests.

All records are synthetic. These tests define local voice consent and labeling
state only; they do not generate audio, capture microphone input, clone voices,
call model providers, or enable external/platform behavior.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone

from practical_chat_agent.core.models import (
    ConsentCenterState,
    ConsentGrantRecord,
    VoiceConsentPolicy,
    VoicePreferenceState,
    VoiceRequestedLikenessType,
)


def _voice_consent_state() -> ConsentCenterState:
    return ConsentCenterState(
        user_id="user_synthetic",
        grants=[
            ConsentGrantRecord(
                user_id="user_synthetic",
                feature_scope="voice_avatar",
                policy_version="voice_policy_v1",
                actor_id="user_synthetic",
                granted_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
                evidence_refs=["synthetic_voice_consent_001"],
            )
        ],
    )


def test_voice_preference_defaults_to_disabled_and_requires_voice_avatar_consent() -> None:
    preference = VoicePreferenceState(user_id="user_synthetic")

    assert preference.schema_version == "voice_preference_state_v1"
    assert preference.preference_id.startswith("voicepref_")
    assert preference.user_id == "user_synthetic"
    assert preference.voice_mode == "disabled"
    assert preference.source_route == "disabled"
    assert preference.required_consent_scope == "voice_avatar"
    assert preference.decision == "disabled"
    assert preference.voice_enabled is False
    assert preference.has_active_voice_avatar_consent is False
    assert "voice_avatar_consent_required" in preference.blocked_reason_labels


def test_non_real_synthetic_voice_requires_active_separate_consent_and_labels() -> None:
    state = VoiceConsentPolicy().evaluate(
        user_id="user_synthetic",
        source_route="non_real_synthetic_voice",
        consent_state=_voice_consent_state(),
    )

    assert state.voice_mode == "non_real_synthetic_voice"
    assert state.source_route == "non_real_synthetic_voice"
    assert state.decision == "review_required"
    assert state.voice_enabled is False
    assert state.has_active_voice_avatar_consent is True
    assert state.review_required is True
    assert state.visible_label_text == "AI-generated synthetic voice. Not a human voice."
    assert state.aigc_labeling_requirement is not None
    assert state.aigc_labeling_requirement.content_modality == "audio"
    assert state.aigc_labeling_requirement.product_surface == "voice_avatar"
    assert state.aigc_labeling_requirement.metadata_label_required is True
    assert state.copy_download_export_share_requires_metadata is True
    for label in (
        "ai_generated",
        "synthetic_content",
        "audio",
        "voice_avatar",
        "review_required",
        "implicit_metadata_label",
    ):
        assert label in state.disclosure_labels


def test_non_real_synthetic_voice_without_consent_is_blocked() -> None:
    state = VoiceConsentPolicy().evaluate(
        user_id="user_synthetic",
        source_route="non_real_synthetic_voice",
        consent_state=ConsentCenterState(user_id="user_synthetic"),
    )

    assert state.decision == "blocked"
    assert state.voice_enabled is False
    assert state.has_active_voice_avatar_consent is False
    assert "voice_avatar_consent_required" in state.blocked_reason_labels


def test_real_person_deceased_public_family_and_ex_partner_likeness_are_blocked() -> None:
    likeness_types: list[VoiceRequestedLikenessType] = [
        "real_person",
        "deceased_person",
        "public_figure",
        "family_member",
        "ex_partner",
    ]

    states = [
        VoiceConsentPolicy().evaluate(
            user_id="user_synthetic",
            source_route="blocked_voice_clone",
            requested_likeness_type=likeness_type,
            consent_state=_voice_consent_state(),
        )
        for likeness_type in likeness_types
    ]

    assert [state.requested_likeness_type for state in states] == likeness_types
    for state in states:
        assert state.voice_mode == "blocked_voice_clone"
        assert state.decision == "blocked"
        assert state.voice_enabled is False
        assert "real_person_voice_likeness_blocked" in state.blocked_reason_labels
        assert "voice_clone_blocked" in state.blocked_reason_labels


def test_recorded_user_and_third_party_authorized_voice_routes_are_deferred() -> None:
    states = [
        VoiceConsentPolicy().evaluate(
            user_id="user_synthetic",
            source_route=source_route,
            consent_state=_voice_consent_state(),
        )
        for source_route in ("recorded_user_voice", "third_party_authorized_voice")
    ]

    for state in states:
        assert state.decision == "blocked"
        assert state.voice_enabled is False
        assert "future_voice_route_requires_policy_review" in state.blocked_reason_labels


def test_crisis_dependency_safety_blocks_voice_output() -> None:
    state = VoiceConsentPolicy().evaluate(
        user_id="user_synthetic",
        source_route="non_real_synthetic_voice",
        consent_state=_voice_consent_state(),
        safety_decision_action="block",
        safety_reasons=["crisis_safety_review_required", "proactive_outreach_blocked"],
    )

    assert state.decision == "blocked"
    assert state.voice_enabled is False
    assert "voice_blocked_by_safety_decision" in state.blocked_reason_labels
    assert "crisis_safety_review_required" in state.safety_reason_labels


def test_voice_payloads_have_no_audio_raw_private_provider_delivery_or_platform_fields() -> None:
    state = VoiceConsentPolicy().evaluate(
        user_id="user_synthetic",
        source_route="non_real_synthetic_voice",
        consent_state=_voice_consent_state(),
    )

    serialized = json.dumps(state.model_dump(mode="json"), ensure_ascii=False).lower()

    for forbidden in (
        "audio_bytes",
        "voice_sample",
        "microphone",
        "raw_text",
        "raw_transcript",
        "transcript",
        "chat_history",
        "private_messages",
        "provider_token",
        "api_key",
        "generated_audio_path",
        "send",
        "schedule",
        "delivery",
        "platform",
        "webhook",
        "queue",
    ):
        assert forbidden not in serialized
