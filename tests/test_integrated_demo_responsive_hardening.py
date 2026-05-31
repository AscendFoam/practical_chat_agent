"""T415 integrated demo responsive hardening tests.

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


def _read(asset: str) -> str:
    return Path(_assets()[asset]).read_text(encoding="utf-8")


def test_css_has_mobile_constraints_for_integrated_and_commercial_sections() -> None:
    css = _read("css")
    mobile_block = css.split("@media (max-width: 720px)", maxsplit=1)[1]

    assert ".scenario-spine,\n  .trust-commercial" in mobile_block
    assert ".scenario-promise-grid,\n  .scenario-spine-grid,\n  .trust-commercial-grid,\n  .review-grid" in mobile_block
    assert "grid-template-columns: minmax(0, 1fr);" in mobile_block
    assert "min-width: 0;" in css
    assert "overflow-wrap: anywhere;" in css
    assert "word-break: normal;" in css


def test_html_keeps_accessible_labels_for_new_sections() -> None:
    html = _read("html")

    assert 'id="integrated-scenario"' in html
    assert 'aria-label="Integrated scenario spine"' in html
    assert 'id="trust-commercial-panel"' in html
    assert 'aria-label="Trust and commercial positioning"' in html
    assert 'id="scenario-title"' in html
    assert 'id="trust-pricing-list"' in html
    assert 'id="unacceptable-pattern-list"' in html


def test_javascript_has_no_forbidden_action_controls() -> None:
    js = _read("js")
    normalized = js.lower()

    for forbidden in (
        'data-action="approve"',
        'data-action="reject"',
        'data-action="deliver"',
        'data-action="publish"',
        "callprovider",
        "openwebhook",
        "connect_platform",
        "generate_audio",
        "generate_video",
    ):
        assert forbidden not in normalized


def test_served_demo_remains_free_of_forbidden_private_provider_outbound_media_fields() -> None:
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
        "raw_text",
        "raw_transcript",
        "chat_history",
        "private_messages",
        "provider_credentials",
        "platform_recipient",
        "send_queue",
        "schedule",
        "webhook",
        "token",
        "microphone",
        "camera",
        "audio_bytes",
        "image_bytes",
        "video_bytes",
        "generated_audio",
        "generated_image",
        "generated_video",
    ):
        assert forbidden not in combined
