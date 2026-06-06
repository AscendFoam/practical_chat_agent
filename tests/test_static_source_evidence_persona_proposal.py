"""T455 static source evidence persona proposal rendering tests.

These tests inspect local static assets only. They do not call providers, read
private data, retain raw source content, create embeddings, extract traits,
write stores, apply persona changes, send messages, connect adapters, or enable
media runtime.
"""

from __future__ import annotations

from pathlib import Path

from practical_chat_agent.ui.text_first_web_demo_static import TextFirstWebDemoStaticShell


REQUIRED_PROPOSAL_PATHS = (
    "style.tone",
    "style.pacing",
    "style.humor",
    "relationship.boundary_style",
    "memory.use_preference",
    "growth.short_term_hint",
)

REQUIRED_OUTCOMES = (
    "needs_manual_review",
    "blocked_by_policy",
    "ready_for_future_apply_design",
)


def _paths() -> dict[str, str]:
    return TextFirstWebDemoStaticShell().asset_paths()


def _asset_text(name: str) -> str:
    return Path(_paths()[name]).read_text(encoding="utf-8")


def test_static_html_exposes_source_evidence_persona_proposal_section_and_targets() -> None:
    html = _asset_text("html")

    for expected in (
        'id="source-evidence-persona-proposal"',
        'id="source-proposal-title"',
        'id="source-proposal-schema"',
        'id="source-proposal-non-execution-list"',
        'id="source-proposal-matrix-summary"',
        'id="source-proposal-candidate-list"',
        'id="source-proposal-risk-list"',
        'id="source-proposal-rollback-list"',
        'id="source-proposal-gate-list"',
        'id="source-proposal-outcome-list"',
    ):
        assert expected in html


def test_static_js_fallback_contains_source_evidence_persona_proposal_contract_values() -> None:
    js = _asset_text("js")

    assert "source_evidence_persona_proposal" in js
    assert "m41.source_evidence_persona_proposal.v1" in js
    assert "drawSourceEvidencePersonaProposal" in js
    for field_path in REQUIRED_PROPOSAL_PATHS:
        assert field_path in js
    for outcome in REQUIRED_OUTCOMES:
        assert outcome in js


def test_static_js_renders_proposal_lists_without_action_controls() -> None:
    js = _asset_text("js")

    for expected in (
        "source-proposal-matrix-summary",
        "source-proposal-candidate-list",
        "source-proposal-risk-list",
        "source-proposal-rollback-list",
        "source-proposal-gate-list",
        "source-proposal-outcome-list",
        "source-proposal-non-execution-list",
        "source-proposal-card",
        "source-proposal-risk-card",
        "source-proposal-rollback-card",
        "source-proposal-gate-card",
        "source-proposal-outcome-card",
    ):
        assert expected in js

    for forbidden in (
        "proposalImport",
        "proposalUpload",
        "proposalRead",
        "proposalRetain",
        "proposalExtract",
        "proposalEmbed",
        "proposalApply",
        "proposalCommit",
        "proposalMutate",
        "proposalClone",
        "proposalConnect",
        "proposalSend",
        "proposalPublish",
        "proposalGenerateMedia",
        '"uses_model_provider": true',
        '"reads_private_sources": true',
        '"retains_raw_source_content": true',
        '"creates_embeddings": true',
        '"performs_extraction": true',
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


def test_static_css_has_source_proposal_grid_and_responsive_rules() -> None:
    css = _asset_text("css")

    for expected in (
        ".source-evidence-persona-proposal",
        ".source-proposal-layout",
        ".source-proposal-grid",
        ".source-proposal-card",
        ".source-proposal-risk-card",
        ".source-proposal-rollback-card",
        ".source-proposal-gate-card",
        ".source-proposal-outcome-card",
    ):
        assert expected in css

    assert "@media (max-width: 720px)" in css
    assert ".source-proposal-layout" in css
    assert ".source-proposal-grid" in css
