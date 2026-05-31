"""T390 review workspace static panel tests.

These tests inspect local static assets only. They do not call model providers,
read private data, generate media, mutate stores, or enable outbound behavior.
"""

from __future__ import annotations

from pathlib import Path

from practical_chat_agent.ui.text_first_web_demo_static import TextFirstWebDemoStaticShell


def _assets() -> dict[str, str]:
    return TextFirstWebDemoStaticShell().asset_paths()


def _read(asset: str) -> str:
    return Path(_assets()[asset]).read_text(encoding="utf-8")


def test_static_assets_include_review_workspace_panel_target() -> None:
    html = _read("html")

    assert 'id="tab-review"' in html
    assert 'data-tab="review"' in html
    assert 'aria-controls="review-panel"' in html
    assert 'id="review-panel"' in html
    assert 'id="review-filters"' in html
    assert 'id="review-workspace-list"' in html
    assert 'id="review-export-summary"' in html


def test_javascript_fixture_contains_review_workspace_cards_and_filters() -> None:
    js = _read("js")

    assert "review_workspace" in js
    assert "filter_tabs" in js
    assert "status_badges" in js
    assert "Blocked before state change" in js
    assert "Eligible for later manual review" in js
    assert "Safe export summary" in js
    assert "function drawReviewWorkspace" in js


def test_blocked_and_eligible_states_are_renderable() -> None:
    js = _read("js")
    css = _read("css")

    assert "tone-blocked" in js
    assert "tone-eligible" in js
    assert ".status-badge.tone-blocked" in css
    assert ".status-badge.tone-eligible" in css
    assert ".review-card" in css


def test_review_workspace_assets_have_no_private_provider_outbound_or_media_fields() -> None:
    combined = "\n".join(Path(path).read_text(encoding="utf-8") for path in _assets().values()).lower()

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
        "apply_decision",
        "mutate_store",
        "write_persona_version",
        "generate_audio",
        "generate_image",
        "generate_video",
    ):
        assert forbidden not in combined


def test_review_workspace_panel_exposes_no_action_controls() -> None:
    html = _read("html").lower()
    js = _read("js").lower()

    for blocked_control in (
        "data-action=\"approve\"",
        "data-action=\"reject\"",
        "data-action=\"deliver\"",
        "data-action=\"publish\"",
        "data-action=\"mutate\"",
        "callprovider",
        "openwebhook",
    ):
        assert blocked_control not in html
        assert blocked_control not in js


def test_review_workspace_renderer_uses_dom_text_nodes_for_payload_fields() -> None:
    js = _read("js")

    assert "function appendReviewWorkspaceCard" in js
    assert "listNode.appendChild(appendReviewWorkspaceCard(card));" in js
    assert 'items("#review-workspace-list"' not in js
    assert "summary.textContent = card.safe_summary || \"\";" in js
    assert "title.textContent = card.title || \"Review item\";" in js
