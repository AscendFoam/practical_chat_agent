"""T414 trust/commercial positioning panel tests.

All examples are synthetic. The panel is a local product-review surface and
does not read private chat history, call providers, write stores, send
messages, or connect to external platforms/media.
"""

from __future__ import annotations

import json
from pathlib import Path

from practical_chat_agent.ui.text_first_web_demo_adapter import (
    TextFirstWebDemoAdapter,
)
from practical_chat_agent.ui.text_first_web_demo_local_server import (
    TextFirstWebDemoLocalServer,
)
from practical_chat_agent.ui.text_first_web_demo_static import (
    TextFirstWebDemoStaticShell,
)


def _payload() -> dict[str, object]:
    return TextFirstWebDemoAdapter().build_synthetic_demo_state().model_dump(mode="json")


def _assets() -> dict[str, str]:
    return TextFirstWebDemoStaticShell().asset_paths()


def test_payload_contains_trust_and_commercial_positioning() -> None:
    payload = _payload()
    trust = payload["trust_commercial"]

    assert trust["schema_version"] == "trust_commercial_positioning_v1"
    assert len(trust["pricing_hypotheses"]) >= 3
    assert len(trust["value_pillars"]) >= 4
    assert len(trust["trust_controls"]) >= 4
    assert len(trust["readiness_gaps"]) >= 3
    assert len(trust["safety_notes"]) >= 3


def test_unacceptable_monetization_patterns_are_explicit_and_safe() -> None:
    trust = _payload()["trust_commercial"]
    unacceptable = trust["unacceptable_patterns"]
    combined = json.dumps(unacceptable, ensure_ascii=False).lower()

    assert "guilt-based retention" in combined
    assert "impersonation claims" in combined
    assert "crisis paywalls" in combined
    assert "hidden private-data use" in combined
    for forbidden in (
        "dependency_pressure",
        "private_messages",
        "provider_credentials",
        "platform_recipient",
        "send_queue",
        "generated_audio",
        "generated_video",
    ):
        assert forbidden not in combined


def test_static_assets_include_trust_commercial_panel_hooks() -> None:
    paths = _assets()
    html = Path(paths["html"]).read_text(encoding="utf-8")
    js = Path(paths["js"]).read_text(encoding="utf-8")
    css = Path(paths["css"]).read_text(encoding="utf-8")

    assert 'id="trust-commercial-panel"' in html
    assert 'id="trust-pricing-list"' in html
    assert 'id="trust-control-list"' in html
    assert 'id="unacceptable-pattern-list"' in html
    assert 'id="readiness-gap-list"' in html
    assert "drawTrustCommercial" in js
    assert "trust_commercial" in js
    assert ".trust-commercial-grid" in css


def test_served_trust_commercial_surface_has_no_forbidden_fields() -> None:
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
