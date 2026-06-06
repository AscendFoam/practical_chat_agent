"""T427 persona workbench responsive hardening tests.

These tests inspect static CSS only. They do not call providers, read private
data, write stores, apply traits, send messages, connect adapters, or enable
media runtime.
"""

from __future__ import annotations

from pathlib import Path

from practical_chat_agent.ui.text_first_web_demo_static import TextFirstWebDemoStaticShell


def _css() -> str:
    path = TextFirstWebDemoStaticShell().asset_paths()["css"]
    return Path(path).read_text(encoding="utf-8")


def test_workbench_cards_wrap_long_trait_evidence_and_request_values() -> None:
    css = _css()

    for selector in (
        ".persona-workbench .item",
        ".workbench-layout > div",
        "#workbench-non-execution-list",
        ".workbench-trait-card .item-meta",
        ".workbench-blocked-card .item-meta",
        ".persona-workbench-review-card .item-meta",
        ".persona-workbench-review-card .review-detail-list",
    ):
        assert selector in css

    assert css.count("overflow-wrap: anywhere;") >= 8
    assert css.count("min-width: 0;") >= 8


def test_mobile_media_aligns_workbench_headers_labels_and_review_cards() -> None:
    css = _css()
    media_start = css.index("@media (max-width: 720px)")
    media = css[media_start:]

    for selector in (
        ".workbench-section-head",
        "#workbench-non-execution-list",
        ".persona-workbench-review-card .status-badges",
    ):
        assert selector in media

    assert "align-items: flex-start;" in media


def test_workbench_grids_keep_single_column_mobile_tracks() -> None:
    css = _css()
    media_start = css.index("@media (max-width: 720px)")
    media = css[media_start:]

    for selector in (
        ".workbench-layout",
        ".workbench-trait-grid",
        ".workbench-blocked-grid",
    ):
        assert selector in media

    assert "grid-template-columns: minmax(0, 1fr);" in media
