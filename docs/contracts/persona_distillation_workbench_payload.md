# Persona Distillation Workbench Payload Contract

Status: introduced by T424 for M36

## Purpose

`persona_distillation_workbench` is a deterministic local payload for the
text-first web demo. It shows how synthetic persona inputs can become
reviewable trait candidates without reading private records, calling providers,
writing stores, applying traits, sending messages, connecting platform
adapters, or enabling media runtime.

## Top-Level Shape

The payload is exposed from `TextFirstWebDemoState` as
`persona_distillation_workbench`.

Required fields:

- `schema_version`: `m36.persona_distillation_workbench.v1`;
- `workbench_title`;
- `review_required: true`;
- `apply_policy`;
- `input_modes`;
- `synthetic_inputs`;
- `evidence_refs`;
- `extracted_trait_candidates`;
- `blocked_requests`;
- `safety_gates`;
- `non_execution_flags`.

## Apply Policy

`apply_policy` must stay preview-only:

- `mode: preview_only`;
- `mutation_allowed: false`;
- `writes_persona_card: false`;
- `writes_memory_store: false`;
- `writes_review_store: false`.

The workbench never mutates PersonaCard, memory stores, review stores, or
runtime state.

## Input Modes

Required `mode_id` values:

- `detailed_description`;
- `fuzzy_seed`;
- `synthetic_dialogue_excerpt`;
- `random_fictional_seed`.

Each mode must include a label, description, source policy, accepted fixture
kind, `requires_review: true`, and `private_source_allowed: false`.

## Synthetic Inputs

The payload must include at least one synthetic input for every required input
mode.

Each input must include:

- `input_id`;
- `mode_id`;
- `fixture_label`;
- `safe_summary`;
- `detail_level`;
- `contains_private_content: false`;
- `real_person_reference: false`;
- `raw_content_retained: false`.

Synthetic inputs are safe summaries. They are not private records and do not
preserve raw source content.

## Evidence References

Each evidence ref must include:

- `evidence_id`;
- `source_input_id`;
- `source_mode_id`;
- `source_kind: synthetic_fixture`;
- `safe_summary`;
- `raw_private_content_included: false`.

Trait candidates may reference evidence ids. They must not embed private raw
content, contact ids, source file paths, platform handles, or provider output.

## Trait Candidates

Required categories:

- `tone`;
- `pacing`;
- `attachment_style`;
- `humor_style`;
- `boundary_style`;
- `topic_affinity`;
- `taboo_pattern`;
- `memory_use_preference`;
- `growth_hint`.

Each candidate must include:

- `trait_id`;
- `category`;
- `candidate_value`;
- `confidence_band`: one of `low`, `medium`, or `high`;
- non-empty `evidence_ref_ids`;
- `safe_summary`;
- `review_status: needs_review`;
- `apply_status: preview_only`;
- `mutation_allowed: false`.

## Blocked Requests

Required blocked request types:

- `real_person_clone_or_replacement`;
- `deception_or_impersonation`;
- `private_import_without_consent`.

Each blocked request must include:

- `blocked_request_id`;
- `request_type`;
- `risk_reason`;
- `safe_summary`;
- `user_facing_explanation`;
- `source_mode_id`;
- `status: blocked`;
- `raw_private_content_included: false`;
- `mutation_allowed: false`.

## Safety Gates

Required gate ids:

- `synthetic_only_gate`;
- `clone_deception_blocker`;
- `private_source_blocker`;
- `human_review_gate`;
- `non_mutation_gate`;
- `outbound_blocker`.

Each gate must include `enabled: true`, a label, and a safe summary.

## Non-Execution Flags

Required flags:

- `local_only: true`;
- `synthetic_fixture: true`;
- `uses_model_provider: false`;
- `reads_private_sources: false`;
- `writes_runtime_store: false`;
- `automatic_apply: false`;
- `sends_messages: false`;
- `uses_platform_adapter: false`;
- `uses_media_runtime: false`.

Tests must fail if a risky execution flag is missing or set to an unsafe state.

## Verification Anchors

`tests/test_persona_distillation_workbench_payload.py` verifies the contract.
`tests/test_text_first_web_demo_local_server.py` verifies the payload is present
in served demo JSON without unsafe execution states.
`tests/test_static_persona_distillation_workbench.py` verifies the static demo
renders the workbench section, fallback payload, trait cards, blocked request
cards, safety gates, and non-execution badges.

## Static Rendering Anchors

T425 renders the payload into these static DOM targets:

- `#persona-workbench`;
- `#workbench-title`;
- `#workbench-schema`;
- `#workbench-mode-list`;
- `#workbench-input-list`;
- `#workbench-evidence-list`;
- `#workbench-trait-list`;
- `#workbench-blocked-list`;
- `#workbench-gate-list`;
- `#workbench-non-execution-list`.

The static UI must not render action controls for apply, clone, import, upload,
record, connect, send, publish, media generation, or runtime enablement.

## Review Workspace Linkage

T426 links workbench outputs into the Review Workspace as
`workbench_review_cards`.

Trait candidate cards use:

- `schema_version: review_workspace_persona_workbench_card_v1`;
- `card_kind: persona_workbench_trait_review`;
- `candidate_kind: persona_distillation_trait`;
- `source_surface: persona_distillation_workbench`;
- `filter_keys` including `distillation`;
- `review_required: true`;
- `preview_only: true`;
- `changes_state: false`;
- `mutation_allowed: false`;
- `automatic_apply: false`;
- `sends_messages: false`.

Blocked request cards use:

- `schema_version: review_workspace_persona_workbench_card_v1`;
- `card_kind: persona_workbench_blocked_request`;
- `source_surface: persona_distillation_workbench`;
- `filter_keys` including `distillation` and `blocked`;
- `blocked_status: blocked`;
- `review_required: true`;
- `preview_only: true`;
- `changes_state: false`;
- `mutation_allowed: false`;
- `automatic_apply: false`;
- `sends_messages: false`.

The Review Workspace `distillation` filter count must match the number of
workbench review cards. T426 expects 12 cards from the deterministic fixture: 9
trait candidate cards and 3 blocked request cards.
