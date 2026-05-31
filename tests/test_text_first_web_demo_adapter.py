"""T341 text-first web demo adapter tests.

All fixtures are synthetic. These tests define local demo payload assembly
only; they do not build UI, start a server, call model providers, read private
chat logs, generate media, or enable outbound behavior.
"""

from __future__ import annotations

import json

from practical_chat_agent.ui.text_first_web_demo_adapter import (
    TextFirstWebDemoAdapter,
    TextFirstWebDemoState,
)


def _state() -> TextFirstWebDemoState:
    return TextFirstWebDemoAdapter().build_synthetic_demo_state(user_id="user_synthetic")


def test_adapter_returns_one_serializable_state_with_required_sections() -> None:
    state = _state()
    payload = state.model_dump(mode="json")

    json.dumps(payload, ensure_ascii=False)

    assert state.schema_version == "text_first_web_demo_state_v1"
    assert state.demo_id.startswith("webdemo_")
    assert state.user_id == "user_synthetic"
    assert state.review_required is True
    for section in (
        "onboarding",
        "persona",
        "chat_memory",
        "life_stream",
        "proactive",
        "controls",
        "voice",
        "avatar",
    ):
        assert section in payload


def test_sections_preserve_ai_synthetic_and_review_labels() -> None:
    state = _state()

    assert "AI-generated" in state.onboarding["ai_identity_disclosure_text"]
    assert state.persona["safe_persona_state"]["persona_label"]["visible_label_required"] is True
    assert "ai_generated" in state.persona["safe_persona_state"]["persona_label"]["disclosure_labels"]
    assert state.chat_memory["review_state"]["ai_identity_label"]["visible_label_required"] is True
    assert state.life_stream["items"][0]["aigc_label"]["visible_label_required"] is True
    assert "not_real_world_activity" in state.life_stream["items"][0]["aigc_label"]["disclosure_labels"]
    assert state.proactive["enabled_state"]["review_required"] is True
    assert state.controls["aigc_label"]["visible_label_required"] is True
    assert state.voice["review_state"]["review_required"] is True
    assert state.avatar["review_required"] is True


def test_blocked_real_person_clone_and_crisis_dependency_scenarios_are_represented() -> None:
    state = _state()

    blocked_persona = state.persona["blocked_persona_state"]
    assert blocked_persona["screen"] == "persona_blocked"
    assert "real_person_clone_blocked" in blocked_persona["blocked_reasons"]

    blocked_chat = state.chat_memory["blocked_state"]
    assert blocked_chat["screen"] == "chat_blocked"
    assert "crisis_safety_review_required" in blocked_chat["safety_reasons"]

    blocked_proactive = state.proactive["blocked_state"]
    assert blocked_proactive["screen"] == "proactive_blocked"
    assert "proactive_outreach_blocked" in blocked_proactive["safety_reasons"]


def test_voice_and_avatar_are_not_enabled_for_runtime_behavior() -> None:
    state = _state()

    assert state.voice["disabled_state"]["decision"] == "disabled"
    assert state.voice["disabled_state"]["voice_enabled"] is False
    assert state.voice["review_state"]["decision"] == "review_required"
    assert state.voice["review_state"]["voice_enabled"] is False
    assert state.voice["blocked_state"]["decision"] == "blocked"
    assert state.voice["blocked_state"]["voice_enabled"] is False
    assert state.avatar["state"] == "locked_research_only"
    assert state.avatar["avatar_enabled"] is False
    assert "avatar_runtime_not_implemented" in state.avatar["blocked_reasons"]


def test_payload_has_no_private_media_provider_or_outbound_fields() -> None:
    state = _state()
    serialized = json.dumps(state.model_dump(mode="json"), ensure_ascii=False).lower()

    for forbidden in (
        "audio_bytes",
        "voice_sample",
        "microphone",
        "camera",
        "raw_text",
        "raw_transcript",
        "transcript",
        "chat_history",
        "private_messages",
        "provider_token",
        "api_key",
        "generated_audio_path",
        "generated_video_path",
        "send",
        "schedule",
        "delivery",
        "platform",
        "webhook",
        "queue",
    ):
        assert forbidden not in serialized


def test_adapter_does_not_expose_server_model_provider_or_outbound_methods() -> None:
    adapter = TextFirstWebDemoAdapter()

    for method_name in (
        "start_server",
        "call_model",
        "generate_reply",
        "send",
        "schedule",
        "deliver",
        "publish",
        "capture_microphone",
        "capture_camera",
        "synthesize_audio",
        "generate_video",
    ):
        assert not hasattr(adapter, method_name)
