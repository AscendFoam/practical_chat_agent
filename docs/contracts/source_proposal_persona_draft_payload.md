# Source Proposal Persona Draft Payload Contract

Status: introduced by T460 for M42

## Purpose

`source_proposal_persona_draft` is a deterministic local payload for the
text-first web demo. It converts already-visible M41 proposal candidates into
an inspectable PersonaCard draft preview without writing PersonaCard,
PersonaVersionStore, memory stores, review stores, runtime stores, platform
adapters, outbound messaging, or media runtime.

This contract keeps three surfaces separate:

- M41 persona proposal: what persona field might be proposed for review;
- M42 persona draft: what an inspectable draft snapshot could look like;
- future apply executor: actual mutation, not authorized by this payload.

## Top-Level Shape

The payload is exposed from `TextFirstWebDemoState` as
`source_proposal_persona_draft`.

Required fields:

- `schema_version`: `m42.source_proposal_persona_draft.v1`;
- `draft_title`;
- `source_proposal_ref`;
- `base_persona_snapshot`;
- `selected_proposal_ids`;
- `draft_field_changes`;
- `unchanged_field_summaries`;
- `conflict_notes`;
- `rollback_refs`;
- `review_gate_results`;
- `draft_outcome_labels`;
- `review_required: true`;
- `apply_policy`;
- `non_execution_flags`.

`source_proposal_ref.schema_version` must point to
`m41.source_evidence_persona_proposal.v1`.

## Draft Field Changes

Required persona field paths:

- `style.tone`;
- `style.pacing`;
- `style.humor`;
- `relationship.boundary_style`;
- `memory.use_preference`;
- `growth.short_term_hint`.

Each draft field change must include:

- `draft_change_id`;
- `persona_field_path`;
- `before_summary`;
- `after_summary`;
- `source_proposal_ids`;
- `source_trait_hypothesis_ids`;
- `supporting_evidence_row_ids`;
- confidence band from `low`, `medium`, or `high`;
- `risk_label_ids`;
- `conflict_note_ids`;
- `rollback_ref_ids`;
- `review_gate_result_ids`;
- `draft_status: preview_only`;
- `mutation_allowed: false`;
- `review_required: true`.

Draft changes may cite only M41 proposal ids. Trait and evidence ids are
carried through from the cited M41 proposals.

## Conflict Notes

Each conflict note must include:

- `conflict_note_id`;
- `conflict_code`;
- severity from `low`, `medium`, or `high`;
- `safe_summary`;
- `blocks_auto_apply: true`.

Conflict notes are review labels only. They do not authorize automatic apply,
runtime writes, outbound messaging, source extraction, or provider calls.

## Rollback Refs

Each rollback ref must include:

- `rollback_ref_id`;
- `safe_summary`;
- `restore_summary`;
- `runtime_rollback_ready: false`.

Rollback refs describe reversibility for future reviewed apply design. They
are not executable rollback operations in T460.

## Review Gate Results

Each review gate result must include:

- `review_gate_result_id`;
- `gate_code`;
- status from `passed`, `needs_review`, or `blocked`;
- `safe_summary`;
- `blocks_apply_when_failed: true`.

At least one manual review gate must remain `needs_review`, because T460 does
not authorize applying draft fields to PersonaCard or runtime state.

## Draft Outcome Labels

Required outcomes:

- `needs_manual_review`;
- `blocked_by_policy`;
- `ready_for_future_apply_design`.

Outcome labels are planning and review metadata only. They do not mark the
draft as applied, launch-ready, compliant, or production-ready.

## Apply Policy

`apply_policy` must stay preview-only:

- `mode: preview_only`;
- `writes_persona_card: false`;
- `writes_persona_version_store: false`;
- `writes_memory_store: false`;
- `writes_review_store: false`;
- `writes_runtime_store: false`;
- `automatic_apply: false`.

The draft never mutates PersonaCard, PersonaVersionStore, memory stores,
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

## Static Rendering Anchors

T461 renders the payload in the text-first static web demo without adding
source readers, provider calls, extraction, store writes, apply controls,
outbound messaging, platform adapters, or media runtime.

Required static anchors:

- `#source-proposal-persona-draft`;
- `#source-draft-title`;
- `#source-draft-schema`;
- `#source-draft-non-execution-list`;
- `#source-draft-proposal-summary`;
- `#source-draft-base-snapshot`;
- `#source-draft-selected-proposal-list`;
- `#source-draft-field-change-list`;
- `#source-draft-unchanged-field-list`;
- `#source-draft-conflict-list`;
- `#source-draft-rollback-list`;
- `#source-draft-gate-list`;
- `#source-draft-outcome-list`.

Static cards must remain read-only review surfaces. They may show proposal
refs, trait refs, evidence refs, conflicts, rollback refs, gates, outcomes,
preview-only status, and non-execution labels. They must not expose action
controls that imply importing, uploading, reading, retaining, extracting,
embedding, applying, committing, mutating, cloning, connecting, sending,
publishing, media generation, adapter activation, store writes, or runtime
enablement.

## Review Workspace Linkage

T462 exposes draft records as `review_workspace.source_draft_review_cards`.
The Review Workspace must include a `Draft` filter tab whose count matches the
number of generated draft review cards.

Card schema:

- `review_workspace_source_proposal_persona_draft_card_v1`.

Required card kinds:

- `source_persona_draft_field_change_review`;
- `source_persona_draft_unchanged_field_review`;
- `source_persona_draft_conflict_review`;
- `source_persona_draft_rollback_review`;
- `source_persona_draft_gate_review`;
- `source_persona_draft_outcome_review`.

All draft review cards must keep:

- `source_surface: source_proposal_persona_draft`;
- `review_required: true`;
- `preview_only: true`;
- `changes_state: false`;
- `mutation_allowed: false`;
- `automatic_apply: false`;
- `sends_messages: false`;
- `runtime_ready: false`.

Review cards may duplicate safe summaries and ids from the payload for
inspection. They must not authorize source ingestion, extraction, store writes,
runtime mutation, outbound messaging, platform delivery, or media runtime.

## Verification Anchors

`tests/test_source_proposal_persona_draft_payload.py` verifies the contract.
`tests/test_text_first_web_demo_local_server.py` verifies the payload is
present in served demo JSON.

T460 focused verification command:

```powershell
$env:PYTHONPATH='src'; pytest tests\test_source_proposal_persona_draft_payload.py tests\test_source_evidence_persona_proposal_payload.py tests\test_text_first_web_demo_local_server.py -q -o cache_dir=artifacts\t460_pytest_cache --basetemp=artifacts\t460_pytest_basetemp
```

The payload remains local, deterministic, synthetic, preview-only, manually
reviewable, non-extracting, non-mutating, non-sending, non-platform, and
media-runtime disabled.
