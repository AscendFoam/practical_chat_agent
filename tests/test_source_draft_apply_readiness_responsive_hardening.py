"""T469 responsive hardening tests for source draft apply-readiness UI.

These tests inspect local static CSS/JS only. They do not call providers, read
private data, retain raw source content, extract traits, write stores, apply
persona changes, send messages, connect adapters, or enable media runtime.
"""

from __future__ import annotations

from pathlib import Path

from practical_chat_agent.ui.text_first_web_demo_static import TextFirstWebDemoStaticShell


def _asset_text(name: str) -> str:
    return Path(TextFirstWebDemoStaticShell().asset_paths()[name]).read_text(
        encoding="utf-8"
    )


def test_css_hardens_source_readiness_cards_and_labels() -> None:
    css = _asset_text("css")

    for expected in (
        ".source-draft-apply-readiness",
        ".source-draft-apply-readiness .label",
        ".source-readiness-layout > div",
        "#source-readiness-non-execution-list",
        "#source-readiness-draft-summary",
        "#source-readiness-apply-policy-summary",
        "#source-readiness-evaluated-change-list",
        "#source-readiness-field-record-list",
        "#source-readiness-blocked-condition-list",
        "#source-readiness-gate-ref-list",
        "#source-readiness-rollback-list",
        "#source-readiness-outcome-list",
        ".source-readiness-card .item-title",
        ".source-readiness-condition-card .item-title",
        ".source-readiness-gate-card .item-title",
        ".source-readiness-rollback-card .item-title",
        ".source-readiness-outcome-card .item-title",
        ".source-readiness-card .item-meta",
        ".source-readiness-condition-card .item-meta",
        ".source-readiness-gate-card .item-meta",
        ".source-readiness-rollback-card .item-meta",
        ".source-readiness-outcome-card .item-meta",
    ):
        assert expected in css


def test_css_hardens_review_workspace_source_readiness_cards() -> None:
    css = _asset_text("css")

    for expected in (
        ".source-readiness-review-card",
        ".source-readiness-review-card .item-title",
        ".source-readiness-review-card .status-badges",
        ".source-readiness-review-card .review-detail-list",
        ".source-readiness-review-card .item-meta",
    ):
        assert expected in css

    assert "overflow-wrap: anywhere" in css
    assert "min-width: 0" in css


def test_mobile_rules_include_source_readiness_and_review_cards() -> None:
    css = _asset_text("css")

    assert "@media (max-width: 720px)" in css
    for expected in (
        ".source-readiness-section-head",
        "#source-readiness-non-execution-list",
        "#source-readiness-draft-summary",
        "#source-readiness-apply-policy-summary",
        "#source-readiness-evaluated-change-list",
        "#source-readiness-field-record-list",
        "#source-readiness-blocked-condition-list",
        "#source-readiness-gate-ref-list",
        "#source-readiness-rollback-list",
        "#source-readiness-outcome-list",
        ".source-draft-apply-readiness .label",
        ".source-readiness-review-card .status-badges",
        ".source-readiness-review-card .review-detail-list",
    ):
        assert expected in css


def test_source_readiness_review_static_assets_keep_non_execution_details_visible() -> None:
    js = _asset_text("js")

    for expected in (
        "appendSourceDraftApplyReadinessReviewDetails",
        "Blocking conditions",
        "Required gates",
        "Rollback refs",
        "Mutation allowed:",
        "Automatic apply:",
        "Sends messages:",
        "Runtime ready:",
    ):
        assert expected in js
