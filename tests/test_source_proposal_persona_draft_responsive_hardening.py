"""T463 responsive hardening tests for source proposal persona draft UI.

These tests inspect local static CSS/JS only. They do not call providers, read
private data, retain raw source content, extract traits, write stores, send
messages, connect adapters, or enable media runtime.
"""

from __future__ import annotations

from pathlib import Path

from practical_chat_agent.ui.text_first_web_demo_static import TextFirstWebDemoStaticShell


def _asset_text(name: str) -> str:
    return Path(TextFirstWebDemoStaticShell().asset_paths()[name]).read_text(
        encoding="utf-8"
    )


def test_css_hardens_source_draft_cards_and_labels() -> None:
    css = _asset_text("css")

    for expected in (
        ".source-proposal-persona-draft",
        ".source-proposal-persona-draft .label",
        ".source-draft-layout > div",
        "#source-draft-non-execution-list",
        "#source-draft-proposal-summary",
        "#source-draft-base-snapshot",
        "#source-draft-selected-proposal-list",
        ".source-draft-card .item-title",
        ".source-draft-unchanged-card .item-title",
        ".source-draft-conflict-card .item-title",
        ".source-draft-rollback-card .item-title",
        ".source-draft-gate-card .item-title",
        ".source-draft-outcome-card .item-title",
        ".source-draft-card .item-meta",
        ".source-draft-unchanged-card .item-meta",
        ".source-draft-conflict-card .item-meta",
        ".source-draft-rollback-card .item-meta",
        ".source-draft-gate-card .item-meta",
        ".source-draft-outcome-card .item-meta",
    ):
        assert expected in css


def test_css_hardens_review_workspace_source_draft_cards() -> None:
    css = _asset_text("css")

    for expected in (
        ".source-draft-review-card",
        ".source-draft-review-card .item-title",
        ".source-draft-review-card .status-badges",
        ".source-draft-review-card .review-detail-list",
        ".source-draft-review-card .item-meta",
    ):
        assert expected in css

    assert "overflow-wrap: anywhere" in css
    assert "min-width: 0" in css


def test_mobile_rules_include_source_draft_and_review_cards() -> None:
    css = _asset_text("css")

    assert "@media (max-width: 720px)" in css
    for expected in (
        ".source-draft-section-head",
        "#source-draft-non-execution-list",
        "#source-draft-proposal-summary",
        "#source-draft-base-snapshot",
        "#source-draft-selected-proposal-list",
        ".source-proposal-persona-draft .label",
        ".source-draft-review-card .status-badges",
        ".source-draft-review-card .review-detail-list",
    ):
        assert expected in css


def test_source_draft_review_static_assets_keep_non_execution_details_visible() -> None:
    js = _asset_text("js")

    for expected in (
        "appendSourceProposalPersonaDraftReviewDetails",
        "Source proposals",
        "Evidence rows",
        "Risk labels",
        "Rollback refs",
        "Mutation allowed:",
        "Automatic apply:",
        "Sends messages:",
    ):
        assert expected in js
