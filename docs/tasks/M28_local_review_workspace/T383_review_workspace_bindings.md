# T383: Review Workspace Binding Records

## Task ID

T383

## Goal

Implement local deterministic review workspace binding records that connect
review queue items to their source candidates and related dry-run/readiness
artifacts.

T383 should make candidate-kind and candidate-id matching explicit before a
queue item can be grouped with memory lifecycle dry-run plans, persona growth
dry-run plans, or distillation readiness summaries. It must not apply review
decisions, mutate stores, write persona versions, read private data, call
providers, generate replies, synthesize personas, create UI, persist data, send
messages, or connect to platforms/media.

## Why Now

M27 review warning W2 noted that distillation readiness preserves supplied
review queue refs without matching them to candidate ids. M28 starts by adding
a local binding layer that can reject mismatched refs before later workspace
snapshots, UI surfaces, or apply previews rely on them.

## Allowed Files

Future T383 worker may create or modify only:

- `src/practical_chat_agent/services/review_workspace.py`
- `tests/test_review_workspace_bindings.py`
- `docs/data_contracts/review_workspace_binding_contract.md`
- `docs/tasks/M28_local_review_workspace/T384_review_workspace_snapshot_store.md`
- `docs/worker_summary/T383_worker_summary.md`
- `docs/07_handoff.md`

If T383 needs other source files, fixtures, task-board edits, private data,
Browser runs, model-provider calls, package changes, persistence, routes,
stores, CLIs, platform adapters, outbound messaging, voice/avatar runtime, or
media generation, Captain must revise this package before assignment.

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
  recipient ids, delivery state, or persistence behavior.
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
- `docs/review/M27_review.md`
- `docs/data_contracts/review_queue_candidate_contract.md`
- `docs/data_contracts/memory_lifecycle_dry_run_apply_contract.md`
- `docs/data_contracts/persona_growth_dry_run_apply_contract.md`
- `docs/data_contracts/distillation_review_readiness_contract.md`
- `src/practical_chat_agent/services/review_queue.py`
- `src/practical_chat_agent/services/memory_lifecycle_dry_run.py`
- `src/practical_chat_agent/services/persona_growth_dry_run.py`
- `src/practical_chat_agent/services/distillation_review_readiness.py`
- relevant M27 tests.

## Expected Outputs

### 1. Binding Records And Service

Create `src/practical_chat_agent/services/review_workspace.py` with:

- `ReviewWorkspaceBindingIssue`
- `ReviewWorkspaceCandidateBinding`
- `ReviewWorkspaceArtifactBinding`
- `ReviewWorkspaceBundle`
- `ReviewWorkspaceService`

Required behavior:

- bind a `ReviewQueueItem` to a matching supported source candidate;
- preserve only ids, candidate kinds, schema versions, owner user id,
  persona id, safe summaries, reason labels, source refs, issue codes, and
  review flags;
- produce blocker issues for candidate-kind mismatch and candidate-id mismatch;
- bind memory lifecycle dry-run plans to matching review queue decision refs
  and source candidate ids;
- bind persona growth dry-run plans to matching patch ids and optional review
  decision refs;
- bind distillation readiness summaries to matching manifest ids and supplied
  review queue item ids;
- keep `workspace_ready=false` when any blocker issue exists;
- keep all records review-required, preview-only where applicable, and
  non-runtime-ready.

### 2. Tests

Create `tests/test_review_workspace_bindings.py` with synthetic-only tests
that prove:

- matching queue items and source candidates produce ready bindings;
- candidate-kind mismatch blocks workspace readiness;
- candidate-id mismatch blocks workspace readiness;
- memory lifecycle dry-run plans attach only to matching source candidate ids;
- persona growth dry-run plans attach only to matching patch ids;
- distillation readiness summaries preserve queue refs while reporting
  mismatched refs as blocker issues;
- models reject forbidden private/provider/outbound/media fields;
- service exposes no send/schedule/deliver/provider/mutation/apply/synthesis
  or media methods.

### 3. Data Contract

Create `docs/data_contracts/review_workspace_binding_contract.md` describing
implemented records, invariants, forbidden fields, tests, verification,
non-actions, and residual risks.

### 4. Next Task Package

Create
`docs/tasks/M28_local_review_workspace/T384_review_workspace_snapshot_store.md`
for local JSON snapshot storage.

### 5. Worker Summary And Handoff

Write `docs/worker_summary/T383_worker_summary.md` and append a T383 worker
record to `docs/07_handoff.md`.

Do not mark T383 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\services\review_workspace.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_review_workspace_bindings.py tests\test_review_queue_candidates.py tests\test_memory_lifecycle_dry_run_apply.py tests\test_persona_growth_dry_run_apply.py tests\test_distillation_review_readiness.py -q
```

```powershell
git diff --check
```

Use project-local pytest cache and basetemp paths if the default user temp
directory is not writable.

## Reviewer Type

Adversarial review workspace, binding safety, privacy, dry-run safety,
distillation safety, product-safety, and documentation-accuracy review.

Reviewer should block if T383 allows mismatched queue refs to appear ready,
reads private data, applies decisions, mutates memory/persona state, calls
providers, exposes send/schedule/deliver/runtime methods, allows
private/provider/outbound/media fields, or implies launch or production
readiness.
