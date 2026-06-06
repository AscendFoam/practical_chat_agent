"""T445 responsive hardening tests for source intake manifest UI.

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


def test_css_hardens_source_intake_manifest_cards_and_labels() -> None:
    css = _asset_text("css")

    for expected in (
        ".persona-source-intake .item",
        ".persona-source-intake .label",
        ".source-intake-layout > div",
        "#source-intake-non-execution-list",
        "#source-intake-policy-summary",
        ".source-candidate-card .item-title",
        ".source-gate-card .item-title",
        ".source-blocked-card .item-title",
        ".source-redaction-card .item-title",
        ".source-candidate-card .item-meta",
        ".source-gate-card .item-meta",
        ".source-blocked-card .item-meta",
        ".source-redaction-card .item-meta",
    ):
        assert expected in css


def test_css_hardens_review_workspace_source_cards_and_detail_rows() -> None:
    css = _asset_text("css")

    for expected in (
        ".persona-source-review-card",
        ".persona-source-review-card .item-title",
        ".persona-source-review-card .status-badges",
        ".persona-source-review-card .review-detail-list",
        ".persona-source-review-card .item-meta",
    ):
        assert expected in css

    assert "overflow-wrap: anywhere" in css
    assert "min-width: 0" in css


def test_mobile_rules_include_source_intake_and_source_review_cards() -> None:
    css = _asset_text("css")

    assert "@media (max-width: 720px)" in css
    for expected in (
        ".source-intake-section-head",
        "#source-intake-non-execution-list",
        "#source-intake-policy-summary",
        ".persona-source-intake .label",
        ".persona-source-review-card .status-badges",
        ".persona-source-review-card .review-detail-list",
    ):
        assert expected in css


def test_source_review_static_assets_keep_non_execution_details_visible() -> None:
    js = _asset_text("js")

    for expected in (
        "appendPersonaSourceIntakeReviewDetails",
        "Extraction eligible:",
        "Blocked reasons",
        "Review gates",
        "Mutation allowed:",
        "Automatic apply:",
        "Sends messages:",
    ):
        assert expected in js
