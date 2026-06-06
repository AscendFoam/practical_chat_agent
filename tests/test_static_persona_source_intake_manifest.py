"""T443 static persona source intake manifest rendering tests.

These tests inspect local static assets only. They do not call providers, read
private data, retain raw source content, extract traits, write stores, send
messages, connect adapters, or enable media runtime.
"""

from __future__ import annotations

from pathlib import Path

from practical_chat_agent.ui.text_first_web_demo_static import TextFirstWebDemoStaticShell


REQUIRED_SOURCE_KINDS = (
    "detailed_description",
    "fuzzy_seed",
    "synthetic_dialogue_excerpt",
    "user_provided_archive_placeholder",
    "third_party_private_source_placeholder",
)

REQUIRED_GATE_CODES = (
    "explicit_consent_required",
    "private_source_minimization_required",
    "real_person_replacement_blocked",
    "deception_blocked",
    "sensitive_data_redaction_required",
    "reviewer_approval_required",
)

REQUIRED_BLOCKED_CODES = (
    "represented_person_consent_missing",
    "third_party_private_chat_material",
    "deceptive_replacement_request",
    "sensitive_data_not_redacted",
    "undisclosed_real_person_impersonation",
)


def _paths() -> dict[str, str]:
    return TextFirstWebDemoStaticShell().asset_paths()


def _asset_text(name: str) -> str:
    return Path(_paths()[name]).read_text(encoding="utf-8")


def test_static_html_exposes_source_intake_manifest_section_and_targets() -> None:
    html = _asset_text("html")

    for expected in (
        'id="persona-source-intake"',
        'id="source-intake-title"',
        'id="source-intake-schema"',
        'id="source-intake-non-execution-list"',
        'id="source-intake-policy-summary"',
        'id="source-intake-candidate-list"',
        'id="source-intake-gate-list"',
        'id="source-intake-blocked-list"',
        'id="source-intake-redaction-list"',
    ):
        assert expected in html


def test_static_js_fallback_contains_source_intake_manifest_contract_values() -> None:
    js = _asset_text("js")

    assert "persona_source_intake_manifest" in js
    assert "m39.persona_source_intake_manifest.v1" in js
    assert "drawPersonaSourceIntakeManifest" in js
    for source_kind in REQUIRED_SOURCE_KINDS:
        assert source_kind in js
    for gate_code in REQUIRED_GATE_CODES:
        assert gate_code in js
    for blocked_code in REQUIRED_BLOCKED_CODES:
        assert blocked_code in js


def test_static_js_renders_source_intake_lists_without_action_controls() -> None:
    js = _asset_text("js")

    for expected in (
        "source-intake-policy-summary",
        "source-intake-candidate-list",
        "source-intake-gate-list",
        "source-intake-blocked-list",
        "source-intake-redaction-list",
        "source-intake-non-execution-list",
        "source-candidate-card",
        "source-gate-card",
        "source-blocked-card",
        "source-redaction-card",
    ):
        assert expected in js

    for forbidden in (
        "sourceImport",
        "sourceUpload",
        "sourceRead",
        "sourceRetain",
        "sourceExtract",
        "sourceEmbed",
        "sourceApply",
        "sourceCommit",
        "sourceMutate",
        "sourceClone",
        "sourceConnect",
        "sourceSend",
        "sourcePublish",
        "sourceGenerateMedia",
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


def test_static_css_has_source_intake_grid_and_responsive_rules() -> None:
    css = _asset_text("css")

    for expected in (
        ".persona-source-intake",
        ".source-intake-layout",
        ".source-candidate-grid",
        ".source-policy-grid",
        ".source-candidate-card",
        ".source-gate-card",
        ".source-blocked-card",
        ".source-redaction-card",
    ):
        assert expected in css

    assert "@media (max-width: 720px)" in css
    assert ".source-intake-layout" in css
    assert ".source-candidate-grid" in css
