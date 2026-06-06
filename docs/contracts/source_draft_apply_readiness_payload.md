# Source Draft Apply Readiness Payload Contract

Status: introduced by T466 for M43

## Purpose

`source_draft_apply_readiness` is a deterministic local payload for the
text-first web demo. It evaluates M42 persona draft fields for future
apply-readiness without writing PersonaCard, PersonaVersionStore, memory
stores, review stores, runtime stores, platform adapters, outbound messaging,
or media runtime.

This contract keeps three surfaces separate:

- M42 persona draft: what an inspectable draft snapshot could look like;
- M43 apply-readiness preview: what would need review before future apply
  design;
- future apply executor: actual mutation, not authorized by this payload.

## Top-Level Shape

The payload is exposed from `TextFirstWebDemoState` as
`source_draft_apply_readiness`.

Required fields:

- `schema_version`: `m43.source_draft_apply_readiness.v1`;
- `readiness_title`;
- `source_draft_ref`;
- `evaluated_draft_change_ids`;
- `field_readiness_records`;
- `blocked_condition_records`;
- `required_review_gate_refs`;
- `rollback_dependency_refs`;
- `readiness_outcome_labels`;
- `review_required: true`;
- `apply_policy`;
- `non_execution_flags`.

`source_draft_ref.schema_version` must point to
`m42.source_proposal_persona_draft.v1`.

## Field Readiness Records

Required persona field paths:

- `style.tone`;
- `style.pacing`;
- `style.humor`;
- `relationship.boundary_style`;
- `memory.use_preference`;
- `growth.short_term_hint`.

Each field readiness record must include:

- `readiness_record_id`;
- `draft_change_id`;
- `persona_field_path`;
- `readiness_outcome` from `blocked`, `needs_manual_review`, or
  `ready_for_future_apply_design`;
- `safe_summary`;
- `blocking_condition_ids`;
- `required_review_gate_result_ids`;
- `rollback_ref_ids`;
- `future_apply_design_notes`;
- `preview_only: true`;
- `mutation_allowed: false`;
- `review_required: true`.

Readiness records may cite only M42 draft change ids, review gate ids, rollback
refs, and blocked condition ids. They do not authorize mutation.

## Blocked Conditions

Each blocked condition must include:

- `blocked_condition_id`;
- `condition_code`;
- severity from `low`, `medium`, or `high`;
- `safe_summary`;
- `affected_draft_change_ids`;
- `blocks_apply: true`.

Blocked conditions are review labels only. They do not execute policy checks,
write stores, send messages, or connect platforms.

## Review Gate Refs

Each required review gate ref must include:

- `review_gate_result_id`;
- `gate_code`;
- status from `passed`, `needs_review`, or `blocked`;
- `safe_summary`;
- `required_before_apply: true`.

At least one gate may remain `needs_review`, because T466 does not authorize
applying draft fields to PersonaCard or runtime state.

## Rollback Dependencies

Each rollback dependency must include:

- `rollback_ref_id`;
- `dependent_draft_change_ids`;
- `restore_summary`;
- `runtime_rollback_ready: false`.

Rollback dependencies describe reversibility required for future apply design.
They are not executable rollback operations in T466.

## Readiness Outcome Labels

Required outcomes:

- `blocked`;
- `needs_manual_review`;
- `ready_for_future_apply_design`.

Outcome labels are planning and review metadata only. They do not mark a draft
as applied, launch-ready, compliant, or production-ready.

## Apply Policy

`apply_policy` must stay preview-only:

- `mode: preview_only`;
- `apply_executor_enabled: false`;
- `writes_persona_card: false`;
- `writes_persona_version_store: false`;
- `writes_memory_store: false`;
- `writes_review_store: false`;
- `writes_runtime_store: false`;
- `automatic_apply: false`.

The readiness payload never mutates PersonaCard, PersonaVersionStore, memory
stores, review stores, or runtime state.

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

T467 renders the payload in the text-first static web demo without adding
source readers, provider calls, extraction, store writes, apply controls,
outbound messaging, platform adapters, or media runtime.

Required static anchors:

- `#source-draft-apply-readiness`;
- `#source-readiness-title`;
- `#source-readiness-schema`;
- `#source-readiness-non-execution-list`;
- `#source-readiness-draft-summary`;
- `#source-readiness-apply-policy-summary`;
- `#source-readiness-evaluated-change-list`;
- `#source-readiness-field-record-list`;
- `#source-readiness-blocked-condition-list`;
- `#source-readiness-gate-ref-list`;
- `#source-readiness-rollback-list`;
- `#source-readiness-outcome-list`.

Static cards must remain read-only review surfaces. They may show draft change
ids, readiness outcomes, blocked condition refs, review gate refs, rollback
refs, future apply design notes, preview-only status, and non-execution labels.
They must not expose action controls that imply importing, uploading, reading,
retaining, extracting, embedding, applying, committing, mutating, cloning,
connecting, sending, publishing, media generation, adapter activation, store
writes, or runtime enablement.

## Review Workspace Linkage

T468 links `source_draft_apply_readiness` into the local Review Workspace as
`review_workspace.source_readiness_review_cards`.

Required linkage:

- add a `Readiness` filter tab;
- create `source_readiness_field_record_review` cards for field readiness
  records;
- create `source_readiness_blocked_condition_review` cards for blocked
  condition records;
- create `source_readiness_gate_ref_review` cards for required review gate
  refs;
- create `source_readiness_rollback_dependency_review` cards for rollback
  dependency refs;
- create `source_readiness_outcome_review` cards for readiness outcome labels;
- keep every card on `source_surface: source_draft_apply_readiness`;
- include `readiness` in every card's `filter_keys`;
- render static fallback cards through the same Review Workspace card
  component.

Each readiness review card must stay review-only:

- `review_required: true`;
- `preview_only: true`;
- `changes_state: false`;
- `mutation_allowed: false`;
- `automatic_apply: false`;
- `sends_messages: false`;
- `runtime_ready: false`;
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
- `uses_platform_adapter: false`;
- `uses_media_runtime: false`;
- `apply_executor_enabled: false`.

Readiness cards may copy only safe ids, labels, summaries, outcomes, gate
refs, rollback refs, blocking condition ids, and future apply design notes
from the deterministic readiness payload. They must not expose raw source
content, private paths, provider credentials, recipient ids, webhook state,
media bytes, generated media, action buttons, or runtime apply affordances.

## Verification Anchors

`tests/test_source_draft_apply_readiness_payload.py` verifies the contract.
`tests/test_text_first_web_demo_local_server.py` verifies the payload is
present in served demo JSON.
`tests/test_source_draft_apply_readiness_review_linkage.py` verifies Review
Workspace linkage, filter counts, static fallback card generation, safe detail
rows, and non-execution flags.

T466 focused verification command:

```powershell
$env:PYTHONPATH='src'; pytest tests\test_source_draft_apply_readiness_payload.py tests\test_source_proposal_persona_draft_payload.py tests\test_text_first_web_demo_local_server.py -q -o cache_dir=artifacts\t466_pytest_cache --basetemp=artifacts\t466_pytest_basetemp
```

The payload remains local, deterministic, synthetic, preview-only, manually
reviewable, non-extracting, non-mutating, non-sending, non-platform, and
media-runtime disabled.
