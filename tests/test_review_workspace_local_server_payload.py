"""T391 review workspace local server payload tests.

All fixtures are synthetic. These tests do not read private chat history, call
providers, apply decisions, mutate stores, generate media, or enable outbound
behavior.
"""

from __future__ import annotations

import json
from pathlib import Path

from practical_chat_agent.ui.text_first_web_demo_adapter import TextFirstWebDemoAdapter
from practical_chat_agent.ui.text_first_web_demo_local_server import (
    TextFirstWebDemoLocalServer,
)
from practical_chat_agent.ui.text_first_web_demo_static import TextFirstWebDemoStaticShell


def _payload() -> dict[str, object]:
    state = TextFirstWebDemoAdapter().build_synthetic_demo_state(user_id="user_synthetic")
    return state.model_dump(mode="json")


def test_adapter_emits_review_workspace_section_from_presentation_records() -> None:
    payload = _payload()

    review = payload["review_workspace"]
    assert review["schema_version"] == "review_workspace_presentation_panel_v1"
    assert [tab["key"] for tab in review["filter_tabs"]] == [
        "all",
        "blocked",
        "eligible",
        "memory",
        "persona",
        "distillation",
    ]

    cards = review["cards"]
    assert {card["card_kind"] for card in cards} == {
        "workspace_item",
        "decision_impact",
        "export_summary",
    }
    assert any(
        badge["tone"] == "blocked"
        for card in cards
        for badge in card["status_badges"]
    )
    assert any(
        badge["tone"] == "eligible"
        for card in cards
        for badge in card["status_badges"]
    )
    assert all(card["review_required"] is True for card in cards)
    assert all(card["preview_only"] is True for card in cards)
    assert all(card["changes_state"] is False for card in cards)


def test_local_server_payload_includes_review_workspace_fields() -> None:
    response = TextFirstWebDemoLocalServer().route(
        "/demo-state.json",
        user_id="json_synthetic",
    )
    payload = json.loads(response.text)

    assert response.status_code == 200
    assert payload["user_id"] == "json_synthetic"
    assert "review_workspace" in payload
    assert payload["review_workspace"]["cards"]
    assert payload["review_workspace"]["filter_tabs"]


def test_embedded_html_includes_server_provided_review_workspace_payload() -> None:
    html = TextFirstWebDemoLocalServer().route("/", user_id="embedded_synthetic").text

    assert "window.TEXT_FIRST_WEB_DEMO_STATE = {" in html
    assert '"review_workspace": {' in html
    assert '"schema_version": "review_workspace_presentation_panel_v1"' in html
    assert "window.TEXT_FIRST_WEB_DEMO_STATE = null;" not in html


def test_static_javascript_keeps_safe_fallback_when_server_payload_is_absent() -> None:
    js_path = TextFirstWebDemoStaticShell().asset_paths()["js"]
    js = Path(js_path).read_text(encoding="utf-8")

    assert "fallbackState" in js
    assert "review_workspace" in js
    assert "data.review_workspace ||" in js
    assert "function drawReviewWorkspace" in js


def test_review_workspace_payload_has_no_private_provider_outbound_media_or_internal_queue_fields() -> None:
    server = TextFirstWebDemoLocalServer()
    combined = "\n".join(
        response.text
        for response in (
            server.route("/"),
            server.route("/demo-state.json"),
        )
    ).lower()

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
        "provider_credentials",
        "api_key",
        "generated_audio_path",
        "generated_video_path",
        "send",
        "schedule",
        "delivery",
        "platform",
        "webhook",
        "queue",
        "apply_decision",
        "mutate_store",
        "write_persona_version",
    ):
        assert forbidden not in combined


def test_adapter_and_server_expose_no_provider_outbound_mutation_or_media_methods() -> None:
    adapter = TextFirstWebDemoAdapter()
    server = TextFirstWebDemoLocalServer()

    for target in (adapter, server):
        for method_name in (
            "call_provider",
            "call_model",
            "generate_reply",
            "send",
            "schedule",
            "deliver",
            "publish",
            "open_webhook",
            "mutate_store",
            "mutate_persona",
            "apply_decision",
            "write_persona_version",
            "capture_microphone",
            "capture_camera",
            "synthesize_audio",
            "generate_video",
        ):
            assert not hasattr(target, method_name)
