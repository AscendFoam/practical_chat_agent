# Persona Evolution Preview Payload Contract

Status: introduced by T430 for M37

## Purpose

`persona_evolution_preview` is a deterministic local payload for the text-first
web demo. It shows how reviewed synthetic workbench trait candidates can become
preview-only persona patch proposals without reading private records, calling
providers, writing stores, applying persona changes, sending messages,
connecting adapters, or enabling media runtime.

## Top-Level Shape

The payload is exposed from `TextFirstWebDemoState` as
`persona_evolution_preview`.

Required fields:

- `schema_version`: `m37.persona_evolution_preview.v1`;
- `preview_title`;
- `source_workbench_ref`;
- `source_trait_candidate_ids`;
- `persona_snapshot_before`;
- `proposed_patch_candidates`;
- `blocked_source_exclusions`;
- `risk_labels`;
- `rollback_notes`;
- `review_required: true`;
- `apply_policy`;
- `non_execution_flags`.

## Apply Policy

`apply_policy` must stay preview-only:

- `mode: preview_only`;
- `mutation_allowed: false`;
- `writes_persona_card: false`;
- `writes_persona_version_store: false`;
- `writes_memory_store: false`;
- `writes_review_store: false`;
- `writes_runtime_store: false`.

The preview never mutates PersonaCard, PersonaVersionStore, memory stores,
review stores, or runtime state.

## Source Workbench Linkage

`source_workbench_ref.schema_version` must point to
`m36.persona_distillation_workbench.v1`.

`source_trait_candidate_ids` and every patch candidate
`source_trait_candidate_ids` value must refer to M36 workbench trait candidate
ids. Blocked request ids must appear only in `blocked_source_exclusions`.

## Persona Snapshot Before

`persona_snapshot_before` must include:

- `persona_id`;
- `display_name`;
- `ai_identity_disclosure`;
- `current_trait_summaries`;
- `current_boundary_summary`;
- `current_memory_use_summary`;
- `source_label: synthetic_fixture`;
- `real_person_claim: false`;
- `runtime_state_ref: none`.

## Patch Candidates

Required changed field paths:

- `style.tone`;
- `style.pacing`;
- `style.humor`;
- `relationship.boundary_style`;
- `memory.use_preference`;
- `growth.short_term_hint`.

Each patch candidate must include:

- `patch_id`;
- `patch_kind`;
- non-empty `source_trait_candidate_ids`;
- `changed_field_path`;
- `before_summary`;
- `after_summary`;
- `rationale_summary`;
- `confidence_band`: one of `low`, `medium`, or `high`;
- non-empty `evidence_ref_ids`;
- non-empty `risk_label_ids`;
- non-empty `rollback_note_ids`;
- `review_status: needs_review`;
- `apply_status: preview_only`;
- `mutation_allowed: false`.

## Risk Labels

Required risk codes:

- `persona_drift`;
- `overattachment_risk`;
- `unclear_evidence`;
- `boundary_weakening`;
- `blocked_source_excluded`.

Each risk label must include:

- `risk_label_id`;
- `risk_code`;
- severity from `low`, `medium`, or `high`;
- `safe_summary`;
- `mitigation_summary`;
- `blocks_auto_apply: true`.

## Rollback Notes

Each rollback note must include:

- `rollback_note_id`;
- non-empty `target_patch_ids`;
- `prior_summary`;
- `rollback_summary`;
- `required_reviewer_action`;
- `runtime_rollback_ready: false`.

Rollback notes are preview metadata only. They are not executable rollback
records.

## Blocked Source Exclusions

Each blocked source exclusion must include:

- `blocked_request_id`;
- `request_type`;
- `exclusion_reason`;
- `safe_summary`;
- `excluded_from_patch_generation: true`;
- `mutation_allowed: false`.

## Non-Execution Flags

Required flags:

- `local_only: true`;
- `synthetic_fixture: true`;
- `uses_model_provider: false`;
- `reads_private_sources: false`;
- `writes_persona_store: false`;
- `writes_memory_store: false`;
- `writes_review_store: false`;
- `writes_runtime_store: false`;
- `automatic_apply: false`;
- `sends_messages: false`;
- `uses_platform_adapter: false`;
- `uses_media_runtime: false`.

Tests must fail if a risky execution flag is missing or set to an unsafe state.

## Verification Anchors

`tests/test_persona_evolution_preview_payload.py` verifies the contract.
`tests/test_text_first_web_demo_local_server.py` verifies the payload is present
in served demo JSON without unsafe execution states.

## Static Rendering Anchors

T431 renders the payload in the static text-first web demo without adding action
controls. Required DOM anchors:

- `#persona-evolution`;
- `#evolution-title`;
- `#evolution-schema`;
- `#evolution-non-execution-list`;
- `#evolution-source-summary`;
- `#evolution-snapshot`;
- `#evolution-patch-list`;
- `#evolution-risk-list`;
- `#evolution-rollback-list`;
- `#evolution-exclusion-list`.

Required rendered card classes:

- `.evolution-patch-card`;
- `.evolution-risk-card`;
- `.evolution-rollback-card`;
- `.evolution-exclusion-card`.

The static UI must render from both
`window.TEXT_FIRST_WEB_DEMO_STATE.persona_evolution_preview` and the JavaScript
fallback state. The section must remain preview-only: no apply, commit, mutate,
clone, import, upload, record, connect, send, publish, media generation, adapter
activation, store-write, or runtime-enable controls may be introduced.

## Review Workspace Linkage

T432 exposes deterministic review cards at
`review_workspace.evolution_review_cards`. The count must equal:

- number of `proposed_patch_candidates`;
- plus number of `risk_labels`;
- plus number of `rollback_notes`;
- plus number of `blocked_source_exclusions`.

Required card contract:

- `schema_version: review_workspace_persona_evolution_card_v1`;
- `source_surface: persona_evolution_preview`;
- `filter_keys` includes `evolution`;
- `review_required: true`;
- `preview_only: true`;
- `changes_state: false`;
- `mutation_allowed: false`;
- `automatic_apply: false`;
- `sends_messages: false`;
- `runtime_ready: false`.

Required card kinds:

- `persona_evolution_patch_review`;
- `persona_evolution_risk_review`;
- `persona_evolution_rollback_review`;
- `persona_evolution_blocked_source_exclusion`.

The Review Workspace filter tabs must include
`{ key: evolution, label: Evolution, count: len(evolution_review_cards) }`.
Static fallback rendering must include `.persona-evolution-review-card` entries
and detail rows for changed field paths, before/after summaries, risk
mitigations, rollback metadata, and blocked source exclusions.
