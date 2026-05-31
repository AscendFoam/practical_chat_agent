# T384: Review Workspace Snapshot Store

## Task ID

T384

## Goal

Implement a local JSON snapshot store for review workspace bundles.

T384 should persist and reload safe `ReviewWorkspaceBundle` records for local
prototype review workflows. It must not persist raw private chat text, apply
review decisions, mutate memory/persona state, call providers, create UI,
send messages, or connect to platforms/media.

## Why Now

T383 adds explicit candidate and artifact bindings. M28 next needs local
snapshot storage so later review surfaces can inspect stable, safe workspace
bundles without recomputing or trusting mismatched refs.

## Allowed Files

Future T384 worker may create or modify only:

- `src/practical_chat_agent/services/review_workspace_store.py`
- `tests/test_review_workspace_snapshot_store.py`
- `docs/data_contracts/review_workspace_snapshot_store_contract.md`
- `docs/tasks/M28_local_review_workspace/T385_review_decision_impact_preview.md`
- `docs/worker_summary/T384_worker_summary.md`
- `docs/07_handoff.md`

If T384 needs other source files, fixtures, task-board edits, private data,
Browser runs, model-provider calls, package changes, routes, CLIs, platform
adapters, outbound messaging, voice/avatar runtime, or media generation,
Captain must revise this package before assignment.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not ingest, summarize, transform, quote, or commit real private chat
  records.
- Do not call model providers.
- Do not implement source readers, extraction from real logs, embeddings,
  vector search, semantic ranking, fine-tuning, similarity scoring, persona
  synthesis, final companion reply generation, runtime persona mutation, or
  runtime memory mutation.
- Do not apply review decisions or dry-run plans.
- Do not mutate memory stores, PersonaCard objects, or PersonaVersionStore.
- Do not create UI, routes, CLIs, schedulers, queues, webhooks, auth, tokens,
  recipient ids, delivery state, or platform persistence behavior.
- Do not implement proactive candidates, automatic outreach, sending,
  scheduling, notifications, platform delivery, microphone, camera, ASR, TTS,
  voice cloning, voice/avatar likeness, Live2D, generated audio, generated
  image, generated video, or media capture.
- Do not modify `docs/04_task_board.md`.
- Do not claim launch approval, legal compliance, app-store acceptance,
  clinical validation, regulator acceptance, user-study validation, or real
  user evidence.

## Inputs To Read

Required:

- `docs/product/m28_local_review_workspace_scope.md`
- `docs/data_contracts/review_workspace_binding_contract.md`
- `src/practical_chat_agent/services/review_workspace.py`
- `tests/test_review_workspace_bindings.py`

## Expected Outputs

### 1. Store Records And Service

Create `src/practical_chat_agent/services/review_workspace_store.py` with:

- `ReviewWorkspaceSnapshotStore`
- helper methods to `save_bundle`, `load_bundle`, `list_bundles`, and
  `filter_bundles`

Required behavior:

- store bundles as JSON in a caller-supplied local path;
- create parent directories as needed;
- reload bundles through Pydantic validation;
- list bundles sorted by creation time and bundle id;
- filter by candidate kind, owner user id, persona id, priority band, and
  blocker status;
- reject paths outside the caller-supplied store root;
- store only the safe fields already present on `ReviewWorkspaceBundle`;
- never apply decisions or mutate source stores.

### 2. Tests

Create `tests/test_review_workspace_snapshot_store.py` with synthetic-only
tests that prove:

- bundles can be saved and loaded without losing issue/readiness state;
- listing is deterministic;
- filtering by candidate kind, owner user id, persona id, priority band, and
  blocker status works;
- path traversal is rejected;
- serialized files do not contain forbidden private/provider/outbound/media
  fields;
- store exposes no send/schedule/deliver/provider/mutation/apply/synthesis or
  media methods.

### 3. Data Contract

Create `docs/data_contracts/review_workspace_snapshot_store_contract.md`
describing implemented records, invariants, forbidden fields, tests,
verification, non-actions, and residual risks.

### 4. Next Task Package

Create
`docs/tasks/M28_local_review_workspace/T385_review_decision_impact_preview.md`
for deterministic review decision impact previews.

### 5. Worker Summary And Handoff

Write `docs/worker_summary/T384_worker_summary.md` and append a T384 worker
record to `docs/07_handoff.md`.

Do not mark T384 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\services\review_workspace_store.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_review_workspace_snapshot_store.py tests\test_review_workspace_bindings.py -q
```

```powershell
git diff --check
```

Use project-local pytest cache and basetemp paths if the default user temp
directory is not writable.

## Reviewer Type

Adversarial review workspace storage, path-safety, privacy, dry-run safety,
product-safety, and documentation-accuracy review.
