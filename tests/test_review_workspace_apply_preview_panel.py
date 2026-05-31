"""T399 review workspace apply preview panel tests.

All payloads are synthetic and read-only. These tests do not apply decisions,
mutate stores, call providers, generate media, or enable outbound behavior.
"""

from __future__ import annotations

import json
from pathlib import Path

from practical_chat_agent.ui.text_first_web_demo_local_server import (
    TextFirstWebDemoLocalServer,
)
from practical_chat_agent.ui.text_first_web_demo_static import TextFirstWebDemoStaticShell


def _payload() -> dict[str, object]:
    response = TextFirstWebDemoLocalServer().route("/demo-state.json")
    return json.loads(response.text)


def _asset(name: str) -> str:
    path = TextFirstWebDemoStaticShell().asset_paths()[name]
    return Path(path).read_text(encoding="utf-8")


def test_server_payload_includes_manual_apply_preview_cards() -> None:
    review = _payload()["review_workspace"]
    previews = review["manual_apply_previews"]

    assert previews
    first = previews[0]
    assert first["card_kind"] == "manual_apply_preview"
    assert first["title"] == "Manual apply preview"
    assert first["eligibility_outcome"] == "eligible"
    assert first["manual_apply_preview_eligible"] is True
    assert first["review_required"] is True
    assert first["preview_only"] is True
    assert first["changes_state"] is False
    assert first["required_gates"]
    assert first["effects"]
    assert first["rollback_notes"]


def test_static_panel_knows_how_to_render_manual_apply_preview_details() -> None:
    js = _asset("js")
    css = _asset("css")

    assert "manual_apply_previews" in js
    assert "function appendReviewPreviewDetails" in js
    assert "eligibility_outcome" in js
    assert "required_gates" in js
    assert "effects" in js
    assert "rollback_notes" in js
    assert ".review-detail-list" in css


def test_manual_apply_preview_panel_exposes_no_action_controls() -> None:
    combined = "\n".join(
        [
            TextFirstWebDemoLocalServer().route("/").text,
            TextFirstWebDemoLocalServer().route("/demo-state.json").text,
            _asset("html"),
            _asset("js"),
        ]
    ).lower()

    for blocked_control in (
        "data-action=\"approve\"",
        "data-action=\"reject\"",
        "data-action=\"deliver\"",
        "data-action=\"publish\"",
        "data-action=\"mutate\"",
        "callprovider",
        "openwebhook",
        "apply_decision",
        "mutate_store",
        "write_persona_version",
        "generate_audio",
        "generate_image",
        "generate_video",
    ):
        assert blocked_control not in combined
