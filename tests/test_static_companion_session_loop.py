"""T419 static companion session loop tests.

All checks inspect local static assets and synthetic local responses. They do
not read private chat history, call providers, write stores, send messages, or
connect to external platforms/media.
"""

from __future__ import annotations

from pathlib import Path

from practical_chat_agent.ui.text_first_web_demo_local_server import (
    TextFirstWebDemoLocalServer,
)
from practical_chat_agent.ui.text_first_web_demo_static import (
    TextFirstWebDemoStaticShell,
)


def _assets() -> dict[str, str]:
    return TextFirstWebDemoStaticShell().asset_paths()


def _read(asset_name: str) -> str:
    return Path(_assets()[asset_name]).read_text(encoding="utf-8")


def test_html_contains_companion_session_loop_hooks() -> None:
    html = _read("html")

    assert 'id="companion-session"' in html
    assert 'aria-label="Companion session loop"' in html
    assert 'id="session-title"' in html
    assert 'id="session-summary"' in html
    assert 'id="session-turn-list"' in html
    assert 'id="session-memory-list"' in html
    assert 'id="session-persona-cue-list"' in html
    assert 'id="session-safety-list"' in html
    assert 'id="session-candidate-list"' in html
    assert 'id="session-non-execution"' in html


def test_javascript_renders_companion_session_payload() -> None:
    js = _read("js")

    assert "companion_session" in js
    assert "drawCompanionSession" in js
    assert "appendSessionTurn" in js
    assert "session_candidate_memory_001" in js
    assert "local_companion_session_v1" in js
    assert "sends_messages: false" in js


def test_css_contains_responsive_session_loop_rules() -> None:
    css = _read("css")
    mobile_block = css[css.index("@media (max-width: 720px)") :]

    assert ".companion-session" in css
    assert ".session-layout" in css
    assert ".session-turn-list" in css
    assert ".session-candidate-grid" in css
    assert ".session-chip-row" in css
    assert ".companion-session" in mobile_block
    assert ".session-layout" in mobile_block
    assert "grid-template-columns: minmax(0, 1fr);" in mobile_block
    assert "min-width: 0;" in css


def test_static_assets_have_no_companion_session_action_controls() -> None:
    combined = "\n".join(_read(name) for name in ("html", "css", "js")).lower()

    for forbidden in (
        'data-action="send"',
        'data-action="schedule"',
        'data-action="connect"',
        'data-action="approve"',
        'data-action="auto-apply"',
        "call_model",
        "generate_reply",
        "connect_platform",
        "send_queue",
        "delivery_state",
        "capture_microphone",
        "capture_camera",
        "synthesize_audio",
        "generate_audio",
        "generate_image",
        "generate_video",
    ):
        assert forbidden not in combined


def test_served_session_loop_has_no_dangerous_enabled_states() -> None:
    server = TextFirstWebDemoLocalServer()
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
        '"sends_messages": true',
        '"calls_provider": true',
        '"uses_private_source": true',
        '"writes_runtime_store": true',
        '"media_runtime_enabled": true',
        "raw_text",
        "raw_transcript",
        "private_messages",
        "provider_credentials",
        "platform_recipient",
        "send_queue",
        "schedule",
        "webhook",
        "audio_bytes",
        "image_bytes",
        "video_bytes",
        "generated_audio",
        "generated_image",
        "generated_video",
    ):
        assert forbidden not in combined
