# Persona Version Draft Ledger Payload Contract

Status: introduced by T436 for M38

## Purpose

`persona_version_draft_ledger` is a deterministic local payload for the
text-first web demo. It groups reviewed synthetic evolution patch candidates
into persona version draft records with review outcomes, conflict notes, and
rollback refs without reading private records, calling providers, writing
stores, applying persona changes, sending messages, connecting adapters, or
enabling media runtime.

## Top-Level Shape

The payload is exposed from `TextFirstWebDemoState` as
`persona_version_draft_ledger`.

Required fields:

- `schema_version`: `m38.persona_version_draft_ledger.v1`;
- `ledger_title`;
- `source_evolution_preview_ref`;
- `base_persona_snapshot_ref`;
- `drafts`;
- `conflict_notes`;
- `review_outcome_labels`;
- `rollback_ref_index`;
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

The ledger never mutates PersonaCard, PersonaVersionStore, memory stores,
review stores, or runtime state.

## Source Evolution Linkage

`source_evolution_preview_ref.schema_version` must point to
`m37.persona_evolution_preview.v1`.

Draft `source_patch_ids`, `excluded_patch_ids`, and rollback ref
`related_patch_ids` must refer to M37 evolution patch ids. Draft
`risk_label_ids` and conflict note `related_risk_label_ids` must refer to M37
risk label ids. Rollback refs must cite M37 rollback note ids.

Blocked-source material must remain conflict/exclusion metadata and must not
become an included patch set.

## Draft Records

Required draft outcomes:

- `accepted_for_future_apply_review`;
- `deferred_needs_more_evidence`;
- `rejected_boundary_risk`.

Each draft must include:

- `draft_id`;
- `draft_kind`;
- `source_patch_ids`;
- `excluded_patch_ids`;
- `risk_label_ids`;
- `before_snapshot_summary`;
- `after_version_summary`;
- `reviewer_outcome`;
- `conflict_note_ids`;
- `rollback_ref_ids`;
- `review_required: true`;
- `apply_status: preview_only`;
- `mutation_allowed: false`.

Rejected drafts must include a non-empty `rejection_reason` and no included
`source_patch_ids`.

## Conflict Notes

Required conflict codes:

- `persona_drift`;
- `boundary_weakening`;
- `weak_evidence`;
- `overattachment_risk`;
- `blocked_source_contamination`.

Each conflict note must include:

- `conflict_note_id`;
- `conflict_code`;
- severity from `low`, `medium`, or `high`;
- `safe_summary`;
- `mitigation_summary`;
- `related_patch_ids`;
- `related_risk_label_ids`;
- `blocks_auto_apply: true`.

## Rollback Ref Index

Each rollback ref must include:

- `rollback_ref_id`;
- non-empty `related_draft_ids`;
- `related_patch_ids`;
- `related_m37_rollback_note_ids`;
- `prior_summary`;
- `restore_summary`;
- `runtime_rollback_ready: false`.

Rollback refs are preview metadata only. They are not executable rollback
records and do not write version stores.

## Non-Execution Flags

Required flags:

- `local_only: true`;
- `synthetic_fixture: true`;
- `uses_model_provider: false`;
- `reads_private_sources: false`;
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

`tests/test_persona_version_draft_ledger_payload.py` verifies the contract.
`tests/test_text_first_web_demo_local_server.py` verifies the payload is
present in served demo JSON without unsafe execution states.

## Static Rendering Direction

T436 does not render this payload. A later UI task should render:

- source evolution preview linkage;
- base persona snapshot ref;
- accepted, deferred, and rejected drafts;
- included and excluded patch ids;
- conflict notes;
- rollback refs;
- non-execution labels.

The UI must not render action controls that imply apply, commit, mutate,
clone, import, upload, record, connect, send, publish, media generation, or
runtime enablement.

## Static Rendering Anchors

T437 renders the payload in the static text-first web demo without adding
action controls. Required DOM anchors:

- `#persona-version-ledger`;
- `#version-ledger-title`;
- `#version-ledger-schema`;
- `#version-ledger-non-execution-list`;
- `#version-ledger-source-summary`;
- `#version-ledger-base-snapshot`;
- `#version-ledger-draft-list`;
- `#version-ledger-conflict-list`;
- `#version-ledger-rollback-list`;
- `#version-ledger-outcome-list`.

Required rendered card classes:

- `.version-draft-card`;
- `.version-conflict-card`;
- `.version-rollback-card`;
- `.version-outcome-card`.

The static UI must render from both
`window.TEXT_FIRST_WEB_DEMO_STATE.persona_version_draft_ledger` and the
JavaScript fallback state. The section must remain preview-only: no apply,
commit, mutate, clone, import, upload, record, connect, send, publish, media
generation, adapter activation, store-write, or runtime-enable controls may be
introduced.

## Review Workspace Linkage

T438 exposes deterministic review cards at
`review_workspace.version_review_cards`. The count must equal:

- number of `drafts`;
- plus number of `conflict_notes`;
- plus number of `rollback_ref_index` entries;
- plus number of `review_outcome_labels`.

Required card contract:

- `schema_version: review_workspace_persona_version_card_v1`;
- `source_surface: persona_version_draft_ledger`;
- `filter_keys` includes `version`;
- `review_required: true`;
- `preview_only: true`;
- `changes_state: false`;
- `mutation_allowed: false`;
- `automatic_apply: false`;
- `sends_messages: false`;
- `runtime_ready: false`.

Required card kinds:

- `persona_version_draft_review`;
- `persona_version_conflict_review`;
- `persona_version_rollback_review`;
- `persona_version_outcome_review`.

The Review Workspace filter tabs must include
`{ key: version, label: Version, count: len(version_review_cards) }`. Static
fallback rendering must include `.persona-version-review-card` entries and
detail rows for draft outcomes, included/excluded patch ids, conflict
mitigations, rollback refs, and outcome labels.
