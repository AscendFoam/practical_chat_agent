# Persona Source Evidence Matrix Payload Contract

Status: introduced by T448 for M40

## Purpose

`persona_source_evidence_matrix` is a deterministic local payload for the
text-first web demo. It links eligible synthetic source intake candidates to
reviewable evidence rows and cautious trait hypotheses without reading private
records, retaining raw source content, calling providers, creating embeddings,
extracting traits from real content, writing stores, applying persona changes,
sending messages, connecting adapters, or enabling media runtime.

## Top-Level Shape

The payload is exposed from `TextFirstWebDemoState` as
`persona_source_evidence_matrix`.

Required fields:

- `schema_version`: `m40.persona_source_evidence_matrix.v1`;
- `matrix_title`;
- `source_intake_manifest_ref`;
- `eligible_source_ids`;
- `excluded_source_refs`;
- `evidence_rows`;
- `trait_hypotheses`;
- `quality_labels`;
- `review_gate_results`;
- `review_required: true`;
- `apply_policy`;
- `non_execution_flags`.

## Source Intake Linkage

`source_intake_manifest_ref.schema_version` must point to
`m39.persona_source_intake_manifest.v1`.

`eligible_source_ids` must match M39 source candidates with
`extraction_eligible: true`. Evidence rows may cite only eligible source ids.

`excluded_source_refs` must cover every ineligible M39 source candidate and
must include:

- `source_id`;
- `source_kind`;
- `blocked_reason_ids`;
- `safe_summary`;
- `excluded_from_evidence: true`;
- `raw_content_retained: false`;
- `mutation_allowed: false`.

## Evidence Rows

Each evidence row must include:

- `evidence_row_id`;
- `source_id`;
- `source_kind`;
- `evidence_kind`;
- `safe_summary`;
- `quality_label_id`;
- `supports_trait_paths`;
- `uncertainty_notes`;
- `review_gate_result_ids`;
- `raw_content_retained: false`;
- `review_required: true`.

Evidence rows are deterministic fixture summaries. They are not model
extraction outputs and do not retain raw source content.

## Trait Hypotheses

Required trait paths:

- `style.tone`;
- `style.pacing`;
- `style.humor`;
- `relationship.boundary_style`;
- `memory.use_preference`;
- `growth.short_term_hint`.

Each trait hypothesis must include:

- `trait_hypothesis_id`;
- `trait_path`;
- `hypothesis_summary`;
- `supporting_evidence_row_ids`;
- `conflicting_evidence_row_ids`;
- confidence band from `low`, `medium`, or `high`;
- `uncertainty_summary`;
- `review_gate_result_ids`;
- `apply_status: preview_only`;
- `mutation_allowed: false`.

## Quality Labels

Required quality codes:

- `strong_synthetic_description`;
- `fuzzy_seed`;
- `synthetic_dialogue_fixture`;
- `blocked_archive_placeholder`;
- `blocked_third_party_private_source`.

Each quality label must include:

- `quality_label_id`;
- `quality_code`;
- severity from `low`, `medium`, or `high`;
- `safe_summary`;
- `blocks_unreviewed_extraction`.

## Review Gate Results

Required gate codes:

- `consent`;
- `minimization`;
- `redaction`;
- `uncertainty`;
- `anti_deception`.

Each review gate result must include:

- `review_gate_result_id`;
- `gate_code`;
- status from `passed`, `needs_review`, or `blocked`;
- `safe_summary`;
- `blocks_extraction_when_failed: true`.

## Apply Policy

`apply_policy` must stay preview-only and non-extracting:

- `mode: preview_only`;
- `source_files_read: false`;
- `raw_content_retained: false`;
- `creates_embeddings: false`;
- `performs_extraction: false`;
- `writes_persona_card: false`;
- `writes_persona_version_store: false`;
- `writes_memory_store: false`;
- `writes_review_store: false`;
- `writes_runtime_store: false`.

The matrix never mutates PersonaCard, PersonaVersionStore, memory stores,
review stores, or runtime state.

## Non-Execution Flags

Required flags:

- `local_only: true`;
- `synthetic_fixture: true`;
- `uses_model_provider: false`;
- `reads_private_sources: false`;
- `retains_raw_source_content: false`;
- `creates_embeddings: false`;
- `performs_extraction: false`;
- `writes_persona_store: false`;
- `writes_persona_version_store: false`;
- `writes_memory_store: false`;
- `writes_review_store: false`;
- `writes_runtime_store: false`;
- `automatic_apply: false`;
- `sends_messages: false`;
- `uses_platform_adapter: false`;
- `uses_media_runtime: false`.

Tests must fail if a risky execution flag is missing or set to an unsafe state.

## Verification Anchors

`tests/test_persona_source_evidence_matrix_payload.py` verifies the contract.
`tests/test_text_first_web_demo_local_server.py` verifies the payload is
present in served demo JSON without unsafe execution states.

## Static Rendering Anchors

T449 renders this payload in the static text-first web demo under
`#persona-source-evidence`.

Required anchors:

- `#source-evidence-title`;
- `#source-evidence-schema`;
- `#source-evidence-non-execution-list`;
- `#source-evidence-manifest-summary`;
- `#source-evidence-eligible-list`;
- `#source-evidence-excluded-list`;
- `#source-evidence-row-list`;
- `#source-evidence-trait-list`;
- `#source-evidence-quality-list`;
- `#source-evidence-gate-list`.

The UI renders:

- source intake manifest linkage;
- eligible source ids;
- excluded source refs;
- evidence rows;
- trait hypotheses;
- quality labels;
- review gate results;
- non-execution labels.

The static renderer must work from both embedded state and JavaScript fallback
state. It must not render action controls that imply source import, upload,
read, retain, extract, embed, apply, commit, mutate, clone, connect, send,
publish, media generation, adapter activation, store-write, or runtime
enablement.

## Review Workspace Linkage

T450 exposes deterministic matrix records as
`review_workspace.source_evidence_review_cards`.

The card count must equal:

- number of `excluded_source_refs`;
- plus number of `evidence_rows`;
- plus number of `trait_hypotheses`;
- plus number of `quality_labels`;
- plus number of `review_gate_results`.

Required card contract:

- `schema_version: review_workspace_persona_source_evidence_card_v1`;
- `source_surface: persona_source_evidence_matrix`;
- `filter_keys` includes `source` and `evidence`;
- `review_required: true`;
- `preview_only: true`;
- `changes_state: false`;
- `mutation_allowed: false`;
- `automatic_apply: false`;
- `sends_messages: false`;
- `runtime_ready: false`.

Required card kinds:

- `persona_source_evidence_exclusion_review`;
- `persona_source_evidence_row_review`;
- `persona_source_trait_hypothesis_review`;
- `persona_source_quality_label_review`;
- `persona_source_review_gate_result_review`.

Review Workspace filter tabs must include:

- `source`: source intake review card count plus source evidence review card
  count;
- `evidence`: source evidence review card count.

Evidence review cards remain local deterministic previews. They must not read
source files, retain raw content, run extraction, create embeddings, apply
persona mutations, write stores, send messages, connect adapters, or enable
media runtime.
