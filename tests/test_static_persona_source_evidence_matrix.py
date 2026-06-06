"""T449 static persona source evidence matrix rendering tests.

These tests inspect local static assets only. They do not call providers, read
private data, retain raw source content, create embeddings, extract traits,
write stores, send messages, connect adapters, or enable media runtime.
"""

from __future__ import annotations

from pathlib import Path

from practical_chat_agent.ui.text_first_web_demo_static import TextFirstWebDemoStaticShell


REQUIRED_TRAIT_PATHS = (
    "style.tone",
    "style.pacing",
    "style.humor",
    "relationship.boundary_style",
    "memory.use_preference",
    "growth.short_term_hint",
)

REQUIRED_QUALITY_CODES = (
    "strong_synthetic_description",
    "fuzzy_seed",
    "synthetic_dialogue_fixture",
    "blocked_archive_placeholder",
    "blocked_third_party_private_source",
)


def _paths() -> dict[str, str]:
    return TextFirstWebDemoStaticShell().asset_paths()


def _asset_text(name: str) -> str:
    return Path(_paths()[name]).read_text(encoding="utf-8")


def test_static_html_exposes_source_evidence_matrix_section_and_targets() -> None:
    html = _asset_text("html")

    for expected in (
        'id="persona-source-evidence"',
        'id="source-evidence-title"',
        'id="source-evidence-schema"',
        'id="source-evidence-non-execution-list"',
        'id="source-evidence-manifest-summary"',
        'id="source-evidence-eligible-list"',
        'id="source-evidence-excluded-list"',
        'id="source-evidence-row-list"',
        'id="source-evidence-trait-list"',
        'id="source-evidence-quality-list"',
        'id="source-evidence-gate-list"',
    ):
        assert expected in html


def test_static_js_fallback_contains_source_evidence_matrix_contract_values() -> None:
    js = _asset_text("js")

    assert "persona_source_evidence_matrix" in js
    assert "m40.persona_source_evidence_matrix.v1" in js
    assert "drawPersonaSourceEvidenceMatrix" in js
    for trait_path in REQUIRED_TRAIT_PATHS:
        assert trait_path in js
    for quality_code in REQUIRED_QUALITY_CODES:
        assert quality_code in js


def test_static_js_renders_source_evidence_lists_without_action_controls() -> None:
    js = _asset_text("js")

    for expected in (
        "source-evidence-manifest-summary",
        "source-evidence-eligible-list",
        "source-evidence-excluded-list",
        "source-evidence-row-list",
        "source-evidence-trait-list",
        "source-evidence-quality-list",
        "source-evidence-gate-list",
        "source-evidence-non-execution-list",
        "source-evidence-card",
        "source-excluded-card",
        "source-trait-card",
        "source-quality-card",
        "source-gate-result-card",
    ):
        assert expected in js

    for forbidden in (
        "evidenceImport",
        "evidenceUpload",
        "evidenceRead",
        "evidenceRetain",
        "evidenceExtract",
        "evidenceEmbed",
        "evidenceApply",
        "evidenceCommit",
        "evidenceMutate",
        "evidenceClone",
        "evidenceConnect",
        "evidenceSend",
        "evidencePublish",
        "evidenceGenerateMedia",
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


def test_static_css_has_source_evidence_grid_and_responsive_rules() -> None:
    css = _asset_text("css")

    for expected in (
        ".persona-source-evidence",
        ".source-evidence-layout",
        ".source-evidence-grid",
        ".source-evidence-card",
        ".source-excluded-card",
        ".source-trait-card",
        ".source-quality-card",
        ".source-gate-result-card",
    ):
        assert expected in css

    assert "@media (max-width: 720px)" in css
    assert ".source-evidence-layout" in css
    assert ".source-evidence-grid" in css
