# T386: Review Workspace Safe Export Manifest

## Task ID

T386

## Goal

Implement safe local export manifests for selected review workspace snapshots
and review decision impact previews.

T386 should package only safe ids, safe summaries, reason labels, source refs,
issue codes, and preview flags so a later local review UI or audit tool can
inspect a workspace export without raw private text, provider metadata,
platform delivery state, media payloads, or generated media paths. It must not
apply review decisions, mutate memory/persona state, call providers, create
UI, send messages, or connect to platforms/media.

## Why Now

T383 added explicit workspace bindings, T384 added safe local snapshot
storage, and T385 added decision impact previews. M28 next needs a safe export
manifest before milestone review, so prototype review records can be handed to
future UI/audit work without expanding privacy or runtime scope.

## Allowed Files

Future T386 worker may create or modify only:

- `src/practical_chat_agent/services/review_workspace_export.py`
- `tests/test_review_workspace_safe_export.py`
- `docs/data_contracts/review_workspace_safe_export_contract.md`
- `docs/tasks/M28_local_review_workspace/T387_m28_milestone_review.md`
- `docs/worker_summary/T386_worker_summary.md`
- `docs/07_handoff.md`

If T386 needs other source files, fixtures, task-board edits, private data,
Browser runs, model-provider calls, package changes, routes, CLIs, platform
adapters, outbound messaging, voice/avatar runtime, media generation,
persistence outside local export records, or apply executors, Captain must
revise this package before assignment.

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
- `docs/data_contracts/review_workspace_snapshot_store_contract.md`
- `docs/data_contracts/review_decision_impact_preview_contract.md`
- `src/practical_chat_agent/services/review_workspace.py`
- `src/practical_chat_agent/services/review_workspace_store.py`
- `src/practical_chat_agent/services/review_decision_impact_preview.py`
- relevant M28 tests.

## Expected Outputs

### 1. Export Manifest Records And Service

Create `src/practical_chat_agent/services/review_workspace_export.py` with:

- `ReviewWorkspaceExportItem`
- `ReviewWorkspaceImpactExportItem`
- `ReviewWorkspaceSafeExportManifest`
- `ReviewWorkspaceSafeExportService`

Required behavior:

- accept one or more `ReviewWorkspaceBundle` records and optional
  `ReviewDecisionImpactPreview` records;
- include only safe ids, candidate kinds, artifact kinds, decision labels,
  safe summaries, reason labels, source refs, issue codes, blocker codes, and
  review/preview/non-apply flags;
- compute deterministic counts by candidate kind, artifact kind, decision
  outcome, and blocker code;
- support deterministic ordering by bundle id, queue item id, candidate id,
  artifact id, decision id, and preview id;
- optionally write the manifest to a caller-supplied local JSON path;
- reject paths outside the caller-supplied export root when writing JSON;
- keep all export records review-required, preview-only, non-applying,
  non-mutating, and non-runtime-ready.

### 2. Tests

Create `tests/test_review_workspace_safe_export.py` with synthetic-only tests
that prove:

- safe export manifests include workspace bundle summaries and impact preview
  summaries without raw private content;
- counts by candidate kind, artifact kind, decision outcome, and blocker code
  are deterministic;
- ordering is deterministic;
- optional JSON writing rejects path traversal;
- serialized exports do not contain forbidden private/provider/outbound/media
  fields;
- export service exposes no send/schedule/deliver/provider/mutation/apply/
  synthesis or media methods.

### 3. Data Contract

Create `docs/data_contracts/review_workspace_safe_export_contract.md`
describing implemented records, invariants, forbidden fields, tests,
verification, non-actions, and residual risks.

### 4. Next Task Package

Create
`docs/tasks/M28_local_review_workspace/T387_m28_milestone_review.md`
for adversarial milestone review of M28.

### 5. Worker Summary And Handoff

Write `docs/worker_summary/T386_worker_summary.md` and append a T386 worker
record to `docs/07_handoff.md`.

Do not mark T386 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\services\review_workspace_export.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_review_workspace_safe_export.py tests\test_review_decision_impact_preview.py tests\test_review_workspace_snapshot_store.py tests\test_review_workspace_bindings.py -q
```

```powershell
git diff --check
```

Use project-local pytest cache and basetemp paths if the default user temp
directory is not writable.

## Reviewer Type

Adversarial safe export, privacy, non-apply safety, binding correctness,
product-safety, and documentation-accuracy review.

Reviewer should block if T386 exports raw private text, provider credentials,
platform delivery state, media payloads, generated media paths, applies
decisions, mutates memory/persona state, writes PersonaVersionStore, calls
providers, exposes send/schedule/deliver/runtime methods, or implies launch
or production readiness.
