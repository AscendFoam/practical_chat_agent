"""T451 responsive hardening tests for source evidence matrix UI.

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


def test_css_hardens_source_evidence_matrix_cards_and_labels() -> None:
    css = _asset_text("css")

    for expected in (
        ".persona-source-evidence .item",
        ".persona-source-evidence .label",
        ".source-evidence-layout > div",
        "#source-evidence-non-execution-list",
        "#source-evidence-manifest-summary",
        "#source-evidence-eligible-list",
        ".source-evidence-card .item-title",
        ".source-excluded-card .item-title",
        ".source-trait-card .item-title",
        ".source-quality-card .item-title",
        ".source-gate-result-card .item-title",
        ".source-evidence-card .item-meta",
        ".source-excluded-card .item-meta",
        ".source-trait-card .item-meta",
        ".source-quality-card .item-meta",
        ".source-gate-result-card .item-meta",
    ):
        assert expected in css


def test_css_hardens_review_workspace_source_evidence_cards() -> None:
    css = _asset_text("css")

    for expected in (
        ".persona-source-evidence-review-card",
        ".persona-source-evidence-review-card .item-title",
        ".persona-source-evidence-review-card .status-badges",
        ".persona-source-evidence-review-card .review-detail-list",
        ".persona-source-evidence-review-card .item-meta",
    ):
        assert expected in css

    assert "overflow-wrap: anywhere" in css
    assert "min-width: 0" in css


def test_mobile_rules_include_source_evidence_and_review_cards() -> None:
    css = _asset_text("css")

    assert "@media (max-width: 720px)" in css
    for expected in (
        ".source-evidence-section-head",
        "#source-evidence-non-execution-list",
        "#source-evidence-manifest-summary",
        "#source-evidence-eligible-list",
        ".persona-source-evidence .label",
        ".persona-source-evidence-review-card .status-badges",
        ".persona-source-evidence-review-card .review-detail-list",
    ):
        assert expected in css


def test_source_evidence_review_static_assets_keep_non_execution_details_visible() -> None:
    js = _asset_text("js")

    for expected in (
        "appendPersonaSourceEvidenceReviewDetails",
        "Evidence kind:",
        "Supporting evidence",
        "Conflicting evidence",
        "Raw retained:",
        "Mutation allowed:",
        "Automatic apply:",
        "Sends messages:",
    ):
        assert expected in js
