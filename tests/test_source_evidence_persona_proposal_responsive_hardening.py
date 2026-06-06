"""T457 responsive hardening tests for source proposal UI.

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


def test_css_hardens_source_proposal_cards_and_labels() -> None:
    css = _asset_text("css")

    for expected in (
        ".source-evidence-persona-proposal",
        ".source-evidence-persona-proposal .label",
        ".source-proposal-layout > div",
        "#source-proposal-non-execution-list",
        "#source-proposal-matrix-summary",
        ".source-proposal-card .item-title",
        ".source-proposal-risk-card .item-title",
        ".source-proposal-rollback-card .item-title",
        ".source-proposal-gate-card .item-title",
        ".source-proposal-outcome-card .item-title",
        ".source-proposal-card .item-meta",
        ".source-proposal-risk-card .item-meta",
        ".source-proposal-rollback-card .item-meta",
        ".source-proposal-gate-card .item-meta",
        ".source-proposal-outcome-card .item-meta",
    ):
        assert expected in css


def test_css_hardens_review_workspace_source_proposal_cards() -> None:
    css = _asset_text("css")

    for expected in (
        ".source-proposal-review-card",
        ".source-proposal-review-card .item-title",
        ".source-proposal-review-card .status-badges",
        ".source-proposal-review-card .review-detail-list",
        ".source-proposal-review-card .item-meta",
    ):
        assert expected in css

    assert "overflow-wrap: anywhere" in css
    assert "min-width: 0" in css


def test_mobile_rules_include_source_proposal_and_review_cards() -> None:
    css = _asset_text("css")

    assert "@media (max-width: 720px)" in css
    for expected in (
        ".source-proposal-section-head",
        "#source-proposal-non-execution-list",
        "#source-proposal-matrix-summary",
        ".source-evidence-persona-proposal .label",
        ".source-proposal-review-card .status-badges",
        ".source-proposal-review-card .review-detail-list",
    ):
        assert expected in css


def test_source_proposal_review_static_assets_keep_non_execution_details_visible() -> None:
    js = _asset_text("js")

    for expected in (
        "appendSourceEvidencePersonaProposalReviewDetails",
        "Source traits",
        "Evidence rows",
        "Risk labels",
        "Rollback notes",
        "Mutation allowed:",
        "Automatic apply:",
        "Sends messages:",
    ):
        assert expected in js
