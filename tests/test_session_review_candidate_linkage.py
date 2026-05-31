"""T420 session review candidate linkage tests.

All examples are synthetic. Session candidates are linked into review surfaces
without model calls, private data, runtime store writes, automatic apply, or
outbound behavior.
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


def _review_workspace() -> dict[str, object]:
    return _payload()["review_workspace"]


def _assets() -> dict[str, str]:
    return TextFirstWebDemoStaticShell().asset_paths()


def test_review_workspace_includes_session_candidate_cards() -> None:
    review = _review_workspace()
    cards = review["session_candidate_cards"]
    kinds = {card["candidate_kind"] for card in cards}

    assert len(cards) >= 3
    assert {"memory_candidate", "persona_growth_patch", "proactive_suggestion"}.issubset(kinds)
    assert any(tab["key"] == "session" for tab in review["filter_tabs"])
    assert all(card["schema_version"] == "review_workspace_session_candidate_card_v1" for card in cards)
    assert all(card["card_kind"] == "session_candidate_review" for card in cards)
    assert all(card["source_surface"] == "companion_session" for card in cards)


def test_session_candidate_cards_are_review_only_and_traceable() -> None:
    for card in _review_workspace()["session_candidate_cards"]:
        assert card["candidate_id"].startswith("session_candidate_")
        assert card["originating_turn_id"].startswith("turn_")
        assert card["safe_summary"]
        assert card["review_required"] is True
        assert card["preview_only"] is True
        assert card["changes_state"] is False
        assert card["automatic_apply"] is False
        assert card["sends_messages"] is False
        assert "session" in card["filter_keys"]


def test_static_assets_render_session_candidate_review_cards() -> None:
    paths = _assets()
    js = Path(paths["js"]).read_text(encoding="utf-8")
    css = Path(paths["css"]).read_text(encoding="utf-8")

    assert "session_candidate_cards" in js
    assert "appendSessionCandidateReviewDetails" in js
    assert "session-candidate-review-card" in js
    assert ".session-candidate-review-card" in css


def test_local_server_session_linkage_has_no_dangerous_enabled_states() -> None:
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


def test_existing_apply_audit_cards_remain_available() -> None:
    review = _review_workspace()

    assert len(review["apply_audit_entries"]) == 2
    assert {
        card["apply_type"]
        for card in review["apply_audit_entries"]
    } == {"persona_growth", "memory_lifecycle"}
    assert all(card["card_kind"] == "apply_audit_manifest_entry" for card in review["apply_audit_entries"])
