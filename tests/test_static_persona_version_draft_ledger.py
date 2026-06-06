"""T437 static persona version draft ledger rendering tests.

These tests inspect local static assets only. They do not call providers, read
private data, write stores, apply persona changes, send messages, connect
adapters, or enable media runtime.
"""

from __future__ import annotations

from pathlib import Path

from practical_chat_agent.ui.text_first_web_demo_static import TextFirstWebDemoStaticShell


REQUIRED_OUTCOMES = (
    "accepted_for_future_apply_review",
    "deferred_needs_more_evidence",
    "rejected_boundary_risk",
)

REQUIRED_CONFLICT_CODES = (
    "persona_drift",
    "boundary_weakening",
    "weak_evidence",
    "overattachment_risk",
    "blocked_source_contamination",
)


def _paths() -> dict[str, str]:
    return TextFirstWebDemoStaticShell().asset_paths()


def _asset_text(name: str) -> str:
    return Path(_paths()[name]).read_text(encoding="utf-8")


def test_static_html_exposes_version_draft_ledger_section_and_targets() -> None:
    html = _asset_text("html")

    for expected in (
        'id="persona-version-ledger"',
        'id="version-ledger-title"',
        'id="version-ledger-schema"',
        'id="version-ledger-non-execution-list"',
        'id="version-ledger-source-summary"',
        'id="version-ledger-base-snapshot"',
        'id="version-ledger-draft-list"',
        'id="version-ledger-conflict-list"',
        'id="version-ledger-rollback-list"',
        'id="version-ledger-outcome-list"',
    ):
        assert expected in html


def test_static_js_fallback_contains_version_ledger_contract_values() -> None:
    js = _asset_text("js")

    assert "persona_version_draft_ledger" in js
    assert "m38.persona_version_draft_ledger.v1" in js
    assert "drawPersonaVersionDraftLedger" in js
    for outcome in REQUIRED_OUTCOMES:
        assert outcome in js
    for conflict_code in REQUIRED_CONFLICT_CODES:
        assert conflict_code in js


def test_static_js_renders_version_ledger_lists_without_action_controls() -> None:
    js = _asset_text("js")

    for expected in (
        "version-ledger-source-summary",
        "version-ledger-base-snapshot",
        "version-ledger-draft-list",
        "version-ledger-conflict-list",
        "version-ledger-rollback-list",
        "version-ledger-outcome-list",
        "version-ledger-non-execution-list",
        "version-draft-card",
        "version-conflict-card",
        "version-rollback-card",
        "version-outcome-card",
    ):
        assert expected in js

    for forbidden in (
        "versionApply",
        "versionCommit",
        "versionMutate",
        "versionClone",
        "versionUpload",
        "versionRecord",
        "versionConnect",
        "versionSend",
        "versionPublish",
        "versionGenerateMedia",
        '"uses_model_provider": true',
        '"reads_private_sources": true',
        '"writes_persona_store": true',
        '"writes_persona_version_store": true',
        '"writes_memory_store": true',
        '"writes_review_store": true',
        '"writes_runtime_store": true',
        '"automatic_apply": true',
        '"sends_messages": true',
        '"uses_platform_adapter": true',
        '"uses_media_runtime": true',
    ):
        assert forbidden not in js


def test_static_css_has_version_ledger_grid_and_responsive_rules() -> None:
    css = _asset_text("css")

    for expected in (
        ".persona-version-ledger",
        ".version-ledger-layout",
        ".version-draft-grid",
        ".version-conflict-grid",
        ".version-draft-card",
        ".version-conflict-card",
        ".version-rollback-card",
        ".version-outcome-card",
    ):
        assert expected in css

    assert "@media (max-width: 720px)" in css
    assert ".version-ledger-layout" in css
    assert ".version-draft-grid" in css
