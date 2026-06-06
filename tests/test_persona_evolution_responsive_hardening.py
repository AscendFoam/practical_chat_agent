"""T433 static responsive hardening tests for persona evolution UI.

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


def test_evolution_cards_have_long_text_wrapping_guards() -> None:
    css = _css()

    for selector in (
        ".evolution-patch-card .item-title",
        ".evolution-risk-card .item-title",
        ".evolution-rollback-card .item-title",
        ".evolution-exclusion-card .item-title",
        ".persona-evolution-review-card .item-title",
        ".persona-evolution-review-card .status-badges",
        ".persona-evolution-review-card .review-detail-list",
    ):
        block = _block_for(css, selector)
        assert "min-width: 0;" in block
        assert "overflow-wrap: anywhere;" in block


def test_evolution_preview_uses_stable_card_and_label_constraints() -> None:
    css = _css()

    for selector in (
        "#evolution-patch-list",
        "#evolution-risk-list",
        "#evolution-rollback-list",
        "#evolution-exclusion-list",
        ".persona-evolution .label",
        ".persona-evolution-review-card",
    ):
        block = _block_for(css, selector)
        assert "min-width: 0;" in block
        assert "max-width: 100%;" in block


def test_mobile_rules_cover_evolution_review_details() -> None:
    css = _css()
    media_match = re.search(r"@media \(max-width: 720px\)\s*\{(?P<body>[\s\S]+)\}\s*$", css)
    assert media_match, "Missing max-width 720px media block"
    media = media_match.group("body")

    for expected in (
        ".persona-evolution",
        ".evolution-layout",
        ".evolution-patch-grid",
        ".evolution-risk-grid",
        ".evolution-exclusion-grid",
        "#evolution-source-summary",
        "#evolution-snapshot",
        ".persona-evolution .label",
        ".persona-evolution-review-card .status-badges",
        ".persona-evolution-review-card .review-detail-list",
    ):
        assert expected in media

    assert "grid-template-columns: minmax(0, 1fr);" in media
    assert "align-items: flex-start;" in media
