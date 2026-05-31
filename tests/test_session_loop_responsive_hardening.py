"""T421 session loop responsive hardening tests.

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


def test_css_hardens_session_and_review_cards_for_wrapping() -> None:
    css = _read("css")
    mobile_block = css[css.index("@media (max-width: 720px)") :]

    assert ".session-turn-list .item,\n.session-candidate-review-card,\n.review-card" in css
    assert "min-width: 0;" in css
    assert "overflow-wrap: anywhere;" in css
    assert ".session-turn-head,\n  .status-badges,\n  .session-chip-row" in mobile_block
    assert "align-items: flex-start;" in mobile_block


def test_html_keeps_accessible_session_and_review_sections() -> None:
    html = _read("html")

    assert '<section id="companion-session" class="companion-session" aria-label="Companion session loop">' in html
    assert '<aside class="session-context" aria-label="Session context">' in html
    assert '<section id="review-panel" class="panel" data-panel="review" role="tabpanel"' in html
    assert 'aria-labelledby="tab-review"' in html


def test_javascript_has_no_forbidden_session_or_review_action_controls() -> None:
    js = _read("js").lower()

    for forbidden in (
        'data-action="approve"',
        'data-action="apply"',
        'data-action="send"',
        'data-action="schedule"',
        "call_model",
        "connect_platform",
        "capture_microphone",
        "capture_camera",
        "synthesize_audio",
        "generate_audio",
        "generate_image",
        "generate_video",
    ):
        assert forbidden not in js


def test_served_demo_remains_free_of_dangerous_enabled_states() -> None:
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
