"""T404 review workspace apply risk panel tests.

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


def test_server_payload_includes_read_only_apply_risk_cards() -> None:
    review = _payload()["review_workspace"]
    risk_cards = review["apply_risk_reviews"]

    assert risk_cards
    first = risk_cards[0]
    assert first["schema_version"] == "review_workspace_apply_risk_card_v1"
    assert first["card_kind"] == "apply_risk_review"
    assert first["title"] == "Apply risk review"
    assert first["risk_recommendation"] == "ready_for_separately_scoped_executor_design"
    assert first["final_outcome"] == "ready_for_separately_scoped_executor_design"
    assert first["manual_eligibility_outcome"] == "eligible"
    assert first["required_approval_gate_codes"] == ["final_human_confirmation"]
    assert first["satisfied_approval_gate_codes"] == ["final_human_confirmation"]
    assert first["missing_approval_gate_codes"] == []
    assert first["blocking_issue_codes"] == []
    assert first["risk_factors"]
    assert first["review_required"] is True
    assert first["preview_only"] is True
    assert first["risk_assessment_only"] is True
    assert first["executor_ready"] is False
    assert first["changes_state"] is False
    assert first["runtime_ready"] is False


def test_apply_risk_payload_contains_no_forbidden_fields() -> None:
    serialized = json.dumps(_payload()["review_workspace"], ensure_ascii=False).lower()

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
        "queue_item_id",
        "applies_changes",
        "writes_memory_store",
        "writes_persona_version",
        "apply_decision",
        "mutate_store",
        "write_persona_version",
        "generate_audio",
        "generate_image",
        "generate_video",
    ):
        assert forbidden not in serialized


def test_static_renderer_knows_how_to_render_apply_risk_details() -> None:
    js = _asset("js")
    css = _asset("css")

    assert "apply_risk_reviews" in js
    assert "apply_risk_review" in js
    assert "function appendApplyRiskDetails" in js
    assert "risk_recommendation" in js
    assert "final_outcome" in js
    assert "executor_ready" in js
    assert "required_approval_gate_codes" in js
    assert ".apply-risk-card" in css


def test_apply_risk_panel_keeps_existing_review_cards_and_manual_previews() -> None:
    review = _payload()["review_workspace"]
    js = _asset("js")

    assert review["cards"]
    assert review["manual_apply_previews"]
    assert review["apply_risk_reviews"]
    assert "(review.cards || [])" in js
    assert "review.manual_apply_previews" in js
    assert "review.apply_risk_reviews" in js


def test_apply_risk_panel_exposes_no_action_controls() -> None:
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
