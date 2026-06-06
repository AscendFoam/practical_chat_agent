# Source Evidence Persona Proposal Payload Contract

Status: introduced by T454 for M41

## Purpose

`source_evidence_persona_proposal` is a deterministic local payload for the
text-first web demo. It converts already-visible M40 source evidence matrix
trait hypotheses into reviewable persona proposal candidates without reading
private records, retaining source content, calling providers, creating
embeddings, extracting traits from real content, writing stores, applying
persona changes, sending messages, connecting adapters, or enabling media
runtime.

This contract keeps three surfaces separate:

- M40 evidence matrix: what synthetic evidence appears to support;
- M41 persona proposal: what persona field could be proposed for review;
- future apply executor: actual mutation, not authorized by this payload.

## Top-Level Shape

The payload is exposed from `TextFirstWebDemoState` as
`source_evidence_persona_proposal`.

Required fields:

- `schema_version`: `m41.source_evidence_persona_proposal.v1`;
- `proposal_title`;
- `source_evidence_matrix_ref`;
- `proposal_candidates`;
- `risk_labels`;
- `rollback_notes`;
- `review_gate_results`;
- `proposal_outcome_labels`;
- `review_required: true`;
- `apply_policy`;
- `non_execution_flags`.

`source_evidence_matrix_ref.schema_version` must point to
`m40.persona_source_evidence_matrix.v1`.

## Proposal Candidates

Required persona field paths:

- `style.tone`;
- `style.pacing`;
- `style.humor`;
- `relationship.boundary_style`;
- `memory.use_preference`;
- `growth.short_term_hint`.

Each proposal candidate must include:

- `proposal_id`;
- `persona_field_path`;
- `proposed_value_summary`;
- `rationale_summary`;
- `source_trait_hypothesis_ids`;
- `supporting_evidence_row_ids`;
- confidence band from `low`, `medium`, or `high`;
- `risk_label_ids`;
- `rollback_note_ids`;
- `review_gate_result_ids`;
- `proposal_status: preview_only`;
- `mutation_allowed: false`;
- `review_required: true`.

Candidate trait ids must exist in M40 `trait_hypotheses`. Candidate evidence
row ids must exist in M40 `evidence_rows`. Candidate risk, rollback, and gate
refs must exist in this proposal payload.

## Risk Labels

Each risk label must include:

- `risk_label_id`;
- `risk_code`;
- severity from `low`, `medium`, or `high`;
- `safe_summary`;
- `blocks_auto_apply: true`.

Risk labels are review labels only. They do not authorize automatic apply,
runtime writes, outbound messaging, source extraction, or provider calls.

## Rollback Notes

Each rollback note must include:

- `rollback_note_id`;
- `safe_summary`;
- `restore_summary`;
- `runtime_rollback_ready: false`.

Rollback notes describe how a future reviewed apply design could stay
reversible. They are not executable rollback operations in T454.

## Review Gate Results

Each review gate result must include:

- `review_gate_result_id`;
- `gate_code`;
- status from `passed`, `needs_review`, or `blocked`;
- `safe_summary`;
- `blocks_apply_when_failed: true`.

At least one manual review gate must remain `needs_review`, because T454 does
not authorize applying proposal candidates to PersonaCard or runtime state.

## Proposal Outcome Labels

Required outcomes:

- `needs_manual_review`;
- `blocked_by_policy`;
- `ready_for_future_apply_design`.

Outcome labels are planning and review metadata only. They do not mark the
proposal as applied, launch-ready, compliant, or production-ready.

## Apply Policy

`apply_policy` must stay preview-only:

- `mode: preview_only`;
- `writes_persona_card: false`;
- `writes_persona_version_store: false`;
- `writes_memory_store: false`;
- `writes_review_store: false`;
- `writes_runtime_store: false`;
- `automatic_apply: false`.

The proposal never mutates PersonaCard, PersonaVersionStore, memory stores,
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

`tests/test_source_evidence_persona_proposal_payload.py` verifies the contract.
`tests/test_text_first_web_demo_local_server.py` verifies the payload is
present in served demo JSON.

T454 focused verification command:

```powershell
$env:PYTHONPATH='src'; pytest tests\test_source_evidence_persona_proposal_payload.py tests\test_persona_source_evidence_matrix_payload.py tests\test_text_first_web_demo_local_server.py -q -o cache_dir=artifacts\t454_pytest_cache --basetemp=artifacts\t454_pytest_basetemp
```

The payload remains local, deterministic, synthetic, preview-only, manually
reviewable, non-extracting, non-mutating, non-sending, non-platform, and
media-runtime disabled.

## Static Rendering Anchors

T455 renders this payload in the static text-first web demo under
`#source-evidence-persona-proposal`.

Required anchors:

- `#source-proposal-title`;
- `#source-proposal-schema`;
- `#source-proposal-non-execution-list`;
- `#source-proposal-matrix-summary`;
- `#source-proposal-candidate-list`;
- `#source-proposal-risk-list`;
- `#source-proposal-rollback-list`;
- `#source-proposal-gate-list`;
- `#source-proposal-outcome-list`.

The UI renders:

- source evidence matrix linkage;
- proposal candidates;
- risk labels;
- rollback notes;
- review gate results;
- proposal outcome labels;
- non-execution labels.

The static renderer must work from both embedded state and JavaScript fallback
state. It must not render action controls that imply source import, upload,
read, retain, extract, embed, apply, commit, mutate, clone, connect, send,
publish, media generation, adapter activation, store-write, or runtime
enablement.

## Review Workspace Linkage

T456 exposes deterministic proposal records as
`review_workspace.source_proposal_review_cards`.

The card count must equal:

- number of `proposal_candidates`;
- plus number of `risk_labels`;
- plus number of `rollback_notes`;
- plus number of `review_gate_results`;
- plus number of `proposal_outcome_labels`.

Required card contract:

- `schema_version: review_workspace_source_evidence_persona_proposal_card_v1`;
- `source_surface: source_evidence_persona_proposal`;
- `filter_keys` includes `proposal`;
- `review_required: true`;
- `preview_only: true`;
- `changes_state: false`;
- `mutation_allowed: false`;
- `automatic_apply: false`;
- `sends_messages: false`;
- `runtime_ready: false`.

Required card kinds:

- `source_persona_proposal_candidate_review`;
- `source_persona_proposal_risk_review`;
- `source_persona_proposal_rollback_review`;
- `source_persona_proposal_gate_review`;
- `source_persona_proposal_outcome_review`.

Review Workspace filter tabs must include:

- `proposal`: source proposal review card count.

Proposal review cards remain local deterministic previews. They must not read
source files, retain raw content, run extraction, create embeddings, apply
persona mutations, write stores, send messages, connect adapters, or enable
media runtime.
