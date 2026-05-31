"""T351 local text-first web demo server tests.

All responses are local and synthetic. These tests do not keep a server alive,
call model providers, read private chat logs, generate media, or enable
outbound behavior.
"""

from __future__ import annotations

import json

from practical_chat_agent.ui.text_first_web_demo_local_server import (
    TextFirstWebDemoLocalServer,
)


def _server() -> TextFirstWebDemoLocalServer:
    return TextFirstWebDemoLocalServer()


def test_root_route_returns_adapter_backed_html_with_review_required_state() -> None:
    response = _server().route("/", user_id="reviewer_synthetic")
    html = response.text

    assert response.status_code == 200
    assert response.content_type == "text/html; charset=utf-8"
    assert "window.TEXT_FIRST_WEB_DEMO_STATE = {" in html
    assert "window.TEXT_FIRST_WEB_DEMO_STATE = null;" not in html
    assert "text_first_web_demo_state_v1" in html
    assert '"user_id": "reviewer_synthetic"' in html
    assert '"review_required": true' in html
    assert "AI-generated synthetic companion" in html


def test_static_asset_routes_return_local_css_and_javascript_content_types() -> None:
    server = _server()

    css = server.route("/text_first_web_demo.css")
    js = server.route("/text_first_web_demo.js")

    assert css.status_code == 200
    assert css.content_type == "text/css; charset=utf-8"
    assert ":root" in css.text
    assert "http://" not in css.text
    assert "https://" not in css.text

    assert js.status_code == 200
    assert js.content_type == "application/javascript; charset=utf-8"
    assert "setScenario" in js.text
    assert "fetch(" not in js.text
    assert "XMLHttpRequest" not in js.text


def test_demo_state_json_route_returns_synthetic_review_payload() -> None:
    response = _server().route("/demo-state.json", user_id="json_synthetic")
    payload = json.loads(response.text)

    assert response.status_code == 200
    assert response.content_type == "application/json; charset=utf-8"
    assert payload["schema_version"] == "text_first_web_demo_state_v1"
    assert payload["user_id"] == "json_synthetic"
    assert payload["review_required"] is True
    assert payload["voice"]["disabled_state"]["voice_enabled"] is False
    assert payload["voice"]["review_state"]["voice_enabled"] is False
    assert payload["voice"]["blocked_state"]["voice_enabled"] is False
    assert payload["avatar"]["avatar_enabled"] is False
    assert (
        payload["persona_distillation_workbench"]["schema_version"]
        == "m36.persona_distillation_workbench.v1"
    )
    assert payload["persona_distillation_workbench"]["review_required"] is True


def test_unknown_paths_and_path_traversal_are_rejected() -> None:
    server = _server()

    assert server.route("/missing").status_code == 404
    assert server.route("/../text_first_web_demo.js").status_code == 403
    assert server.route("/%2e%2e/text_first_web_demo.js").status_code == 403
    assert server.route("/..\\text_first_web_demo.js").status_code == 403


def test_local_server_responses_have_no_private_provider_media_or_outbound_surfaces() -> None:
    server = _server()
    combined = "\n".join(
        response.text
        for response in (
            server.route("/"),
            server.route("/demo-state.json"),
            server.route("/text_first_web_demo.css"),
            server.route("/text_first_web_demo.js"),
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
        "api_key",
        "generated_audio_path",
        "generated_video_path",
        '"sends_messages": true',
        '"calls_provider": true',
        '"uses_model_provider": true',
        '"uses_private_source": true',
        '"reads_private_sources": true',
        '"writes_runtime_store": true',
        '"automatic_apply": true',
        '"uses_platform_adapter": true',
        '"media_runtime_enabled": true',
        '"uses_media_runtime": true',
        "send_queue",
        "schedule",
        "delivery",
        "webhook",
        "queue",
    ):
        assert forbidden not in combined


def test_local_server_helper_exposes_no_model_provider_media_or_platform_methods() -> None:
    server = _server()

    for method_name in (
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
        "connect_platform",
    ):
        assert not hasattr(server, method_name)
