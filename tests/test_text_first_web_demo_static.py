"""T342 static text-first web demo shell tests.

All payloads are synthetic. These tests validate local static assets only; they
do not start a server, call model providers, read private chat logs, generate
media, or enable outbound behavior.
"""

from __future__ import annotations

import json
from pathlib import Path

from practical_chat_agent.ui.text_first_web_demo_static import TextFirstWebDemoStaticShell


def _shell() -> TextFirstWebDemoStaticShell:
    return TextFirstWebDemoStaticShell()


def test_static_shell_exposes_existing_asset_paths() -> None:
    paths = _shell().asset_paths()

    assert set(paths) == {"html", "css", "js"}
    for path in paths.values():
        assert Path(path).is_file()


def test_generated_payload_can_be_embedded_in_shell_html() -> None:
    shell = _shell()
    payload_json = shell.build_demo_payload_json(user_id="user_synthetic")
    payload = json.loads(payload_json)
    rendered_html = shell.render_embedded_html(user_id="user_synthetic")

    assert payload["schema_version"] == "text_first_web_demo_state_v1"
    assert payload["voice"]["review_state"]["voice_enabled"] is False
    assert "window.TEXT_FIRST_WEB_DEMO_STATE" in rendered_html
    assert "text_first_web_demo_state_v1" in rendered_html
    assert "AI-generated" in rendered_html


def test_static_html_has_app_container_identity_area_tabs_and_locked_media_surfaces() -> None:
    paths = _shell().asset_paths()
    html = Path(paths["html"]).read_text(encoding="utf-8")

    assert 'id="app"' in html
    assert 'id="identity-strip"' in html
    assert 'data-tab="chat"' in html
    assert 'data-tab="persona"' in html
    assert 'data-tab="memory"' in html
    assert 'data-tab="life"' in html
    assert 'data-tab="controls"' in html
    assert 'data-tab="voice-avatar"' in html
    assert 'id="voice-avatar-panel"' in html


def test_static_assets_have_no_external_provider_media_or_outbound_fields() -> None:
    paths = _shell().asset_paths()
    combined = "\n".join(Path(path).read_text(encoding="utf-8") for path in paths.values()).lower()

    for forbidden in (
        "http://",
        "https://",
        "provider_token",
        "api_key",
        "generated_audio_path",
        "generated_video_path",
        "microphone",
        "camera",
        '"sends_messages": true',
        '"calls_provider": true',
        '"uses_private_source": true',
        '"writes_runtime_store": true',
        '"media_runtime_enabled": true',
        "send_queue",
        "schedule",
        "delivery",
        "platform",
        "webhook",
        "queue",
    ):
        assert forbidden not in combined


def test_static_shell_helper_exposes_no_server_provider_outbound_or_media_methods() -> None:
    shell = _shell()

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
        assert not hasattr(shell, method_name)
