# T436: Persona Version Draft Ledger Payload

## Task ID

T436

## Goal

Add a deterministic local `persona_version_draft_ledger` payload to the
text-first web demo state and cover it with contract tests.

This task is payload-only. It must not render UI, call model providers, read
private data, write stores, apply persona changes, send messages, connect
platform adapters, or enable media runtime.

## Context

M37 added `persona_evolution_preview`: source workbench linkage, before
snapshot, patch candidates, risk labels, rollback notes, blocked source
exclusions, static rendering, Review Workspace cards, and responsive hardening.

M38 should group reviewed evolution patches into auditable persona version
drafts. T436 should prove the payload contract before static ledger UI or
Review Workspace version-draft cards are added.

The payload should show how a future apply milestone could reason about draft
outcomes, conflicts, and rollback refs while remaining local, deterministic,
synthetic-only, review-only, and non-mutating.

## Allowed Files

Future T436 worker may create or modify only:

- `src/practical_chat_agent/ui/text_first_web_demo_adapter.py`
- `tests/test_persona_version_draft_ledger_payload.py`
- `tests/test_persona_evolution_preview_payload.py`
- `tests/test_text_first_web_demo_local_server.py`
- `docs/contracts/persona_version_draft_ledger_payload.md`
- `docs/tasks/M38_next_iteration/T437_persona_version_draft_ledger_ui.md`
- `docs/worker_summary/T436_worker_summary.md`
- `docs/07_handoff.md`

If implementation requires static UI rendering, JavaScript/CSS edits, package
changes, private data, source readers, model providers, runtime stores,
platform adapters, outbound messaging, media runtime, automatic apply, or
task-board edits, Captain must revise this package before assignment.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not ingest, summarize, transform, quote, or commit real private chat
  records.
- Do not call model providers or prompt execution layers.
- Do not add source readers, embeddings, vector search, semantic ranking,
  similarity scoring, fine-tuning, or remote inference.
- Do not modify JavaScript, CSS, HTML, or Browser QA surfaces in this task.
- Do not write PersonaCard, PersonaVersionStore, MemoryEventStore, review
  stores, runtime stores, local databases, queues, schedulers, or files outside
  the allowed docs/test/code files.
- Do not add platform adapters, webhooks, auth, tokens, recipient ids, delivery
  state, automatic outreach, or outbound messaging.
- Do not add microphone, camera, ASR, TTS, voice cloning, Live2D, generated
  audio, generated image, generated video, or media capture.
- Do not add payment processing, production pricing claims, legal advice,
  compliance completion, app-store approval, launch approval, clinical claims,
  regulator acceptance, or user-study validation.
- Do not modify `docs/04_task_board.md`.

## Expected Implementation

### 1. Adapter Payload

Update `TextFirstWebDemoState` so serialized demo state contains
`persona_version_draft_ledger`.

The payload must include:

- `schema_version`, for example `m38.persona_version_draft_ledger.v1`;
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

### 2. Source Evolution Linkage

The ledger must reference the synthetic M37 evolution preview:

- `source_evolution_preview_ref.schema_version` should point to
  `m37.persona_evolution_preview.v1`;
- draft `source_patch_ids` must refer to M37 patch ids;
- draft `risk_label_ids` must refer to M37 risk label ids;
- rollback refs must point to M37 rollback note ids or ledger-local rollback
  ref ids that cite those notes;
- blocked source ids must remain conflict metadata and must not become
  included patch ids.

### 3. Draft Outcomes

Add at least three deterministic draft records:

- `accepted_for_future_apply_review`;
- `deferred_needs_more_evidence`;
- `rejected_boundary_risk`.

Each draft must include:

- stable `draft_id`;
- `draft_kind`;
- non-empty `source_patch_ids` or a clear rejection reason;
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

### 4. Conflict Notes

Conflict notes must cover:

- persona drift;
- boundary weakening or hidden AI identity;
- weak or fuzzy evidence;
- overattachment or dependency reinforcement;
- blocked-source contamination.

Each conflict note should include:

- `conflict_note_id`;
- `conflict_code`;
- severity from `low`, `medium`, or `high`;
- `safe_summary`;
- `mitigation_summary`;
- related patch ids;
- related risk label ids;
- `blocks_auto_apply: true`.

### 5. Rollback Ref Index

`rollback_ref_index` should include rollback refs for draft review:

- stable `rollback_ref_id`;
- related draft ids;
- related patch ids;
- related M37 rollback note ids;
- `prior_summary`;
- `restore_summary`;
- `runtime_rollback_ready: false`.

Rollback refs are metadata only and must not write version stores.

### 6. Non-Execution Flags

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

## Tests

Add tests for:

- payload exists in `TextFirstWebDemoState`;
- source linkage to `persona_evolution_preview`;
- draft outcomes and source patch ids;
- conflict notes and required conflict codes;
- rollback ref index;
- non-execution flags;
- unsafe true states and private/source/provider/media strings are absent;
- `/demo-state.json` includes the ledger.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'; pytest tests\test_persona_version_draft_ledger_payload.py tests\test_persona_evolution_preview_payload.py tests\test_text_first_web_demo_local_server.py -q -o cache_dir=artifacts\t436_pytest_cache --basetemp=artifacts\t436_pytest_basetemp
```

```powershell
python -m py_compile src\practical_chat_agent\ui\text_first_web_demo_adapter.py
```

```powershell
git diff --check
```

## Reviewer Type

Payload contract review for source linkage, draft outcome consistency,
conflict coverage, rollback metadata, non-execution flags, and no private or
provider surfaces.
