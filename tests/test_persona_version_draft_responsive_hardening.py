"""T439 static responsive hardening tests for persona version draft UI.

These tests inspect CSS only. They do not call providers, read private data,
write stores, apply persona changes, send messages, connect adapters, or enable
media runtime.
"""

from __future__ import annotations

import re
from pathlib import Path

from practical_chat_agent.ui.text_first_web_demo_static import TextFirstWebDemoStaticShell


def _css() -> str:
    css_path = TextFirstWebDemoStaticShell().asset_paths()["css"]
    return Path(css_path).read_text(encoding="utf-8")


def _block_for(css: str, selector: str) -> str:
    escaped = re.escape(selector)
    match = re.search(rf"{escaped}\s*\{{(?P<body>[^}}]+)\}}", css)
    assert match, f"Missing CSS selector: {selector}"
    return match.group("body")


def test_version_cards_have_long_text_wrapping_guards() -> None:
    css = _css()

    for selector in (
        ".version-draft-card .item-title",
        ".version-conflict-card .item-title",
        ".version-rollback-card .item-title",
        ".version-outcome-card .item-title",
        ".persona-version-review-card .item-title",
        ".persona-version-review-card .status-badges",
        ".persona-version-review-card .review-detail-list",
    ):
        block = _block_for(css, selector)
        assert "min-width: 0;" in block
        assert "overflow-wrap: anywhere;" in block


def test_version_ledger_uses_stable_card_and_label_constraints() -> None:
    css = _css()

    for selector in (
        "#version-ledger-draft-list",
        "#version-ledger-conflict-list",
        "#version-ledger-rollback-list",
        "#version-ledger-outcome-list",
        ".persona-version-ledger .label",
        ".persona-version-review-card",
    ):
        block = _block_for(css, selector)
        assert "min-width: 0;" in block
        assert "max-width: 100%;" in block


def test_mobile_rules_cover_version_review_details() -> None:
    css = _css()
    media_match = re.search(r"@media \(max-width: 720px\)\s*\{(?P<body>[\s\S]+)\}\s*$", css)
    assert media_match, "Missing max-width 720px media block"
    media = media_match.group("body")

    for expected in (
        ".persona-version-ledger",
        ".version-ledger-layout",
        ".version-draft-grid",
        ".version-conflict-grid",
        ".version-rollback-grid",
        "#version-ledger-source-summary",
        "#version-ledger-base-snapshot",
        ".persona-version-ledger .label",
        ".persona-version-review-card .status-badges",
        ".persona-version-review-card .review-detail-list",
    ):
        assert expected in media

    assert "grid-template-columns: minmax(0, 1fr);" in media
    assert "align-items: flex-start;" in media
