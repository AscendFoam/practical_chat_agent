# T408: Memory Lifecycle Apply Executor

## Task ID

T408

## Goal

Implement a local-only memory lifecycle apply executor.

T408 should apply a reviewed `MemoryLifecycleDryRunPlan` to a caller-supplied
`MemoryEventStore` only when final human confirmation, manual apply
eligibility, and apply executor approval all agree. It should update lifecycle
states and return an audit record with rollback evidence.

## Allowed Files

Future T408 worker may create or modify only:

- `src/practical_chat_agent/services/memory_lifecycle_apply_executor.py`
- `tests/test_memory_lifecycle_apply_executor.py`
- `docs/data_contracts/memory_lifecycle_apply_executor_contract.md`
- `docs/tasks/M33_controlled_apply_executor/T409_apply_executor_audit_manifest.md`
- `docs/worker_summary/T408_worker_summary.md`
- `docs/07_handoff.md`

If T408 needs private data, source readers, model-provider calls, local server
routes, package changes, platform adapters, outbound messaging, voice/avatar
runtime, media generation, automatic apply triggers, or persona version writes,
Captain must revise this package before assignment.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not ingest, summarize, transform, quote, or commit real private chat
  records.
- Do not call model providers.
- Do not implement source readers, extraction from real logs, embeddings,
  vector search, semantic ranking, fine-tuning, similarity scoring, persona
  synthesis, final companion reply generation, or runtime persona mutation.
- Do not write PersonaVersionStore.
- Do not add routes, CLIs, schedulers, queues, webhooks, auth, tokens,
  recipient ids, delivery state, or platform persistence behavior.
- Do not implement proactive candidates, automatic outreach, sending,
  scheduling, notifications, platform delivery, microphone, camera, ASR, TTS,
  voice cloning, voice/avatar likeness, Live2D, generated audio, generated
  image, generated video, or media capture.
- Do not modify `docs/04_task_board.md`.

## Expected Outputs

### 1. Executor And Audit Records

Create `memory_lifecycle_apply_executor.py` with records such as:

- `MemoryLifecycleApplyRequest`
- `MemoryLifecycleApplyAudit`
- `MemoryLifecycleApplyExecutor`

The request should include:

- dry-run plan;
- manual eligibility decision;
- apply executor approval decision;
- memory event store;
- reviewer id;
- final confirmation phrase or token.

The audit should include:

- apply id;
- plan id;
- affected memory ids;
- prior lifecycle states;
- new lifecycle states;
- rollback references;
- reviewer id;
- gate ids/outcomes;
- safe summary;
- local-only flags.

### 2. Executor Behavior

The executor should:

- require `final_confirmation="CONFIRM_LOCAL_MEMORY_APPLY"`;
- require manual eligibility outcome `eligible`;
- require apply executor final outcome
  `ready_for_separately_scoped_executor_design`;
- apply only actions present in dry-run effects;
- map delete/archive/freeze/supersede/reject actions to local lifecycle state
  updates;
- write only to the caller-supplied `MemoryEventStore`;
- return an audit record with rollback references;
- reject stale/missing memories, blocked plans, blocked gates, missing
  confirmation, unsupported effects, and empty effects.

### 3. Tests

Create `tests/test_memory_lifecycle_apply_executor.py` proving:

- a safe confirmed memory lifecycle plan updates local lifecycle state;
- prior records remain available as rollback evidence;
- missing confirmation blocks writes;
- blocked manual eligibility blocks writes;
- blocked or needs_review approval blocks writes;
- missing memory ids block writes;
- forbidden private/provider/outbound/media fields are absent from audit
  records;
- executor exposes no provider, outbound, voice/avatar, media, scheduler, or
  platform methods.

### 4. Data Contract

Create `docs/data_contracts/memory_lifecycle_apply_executor_contract.md`.

### 5. Next Task Package

Create
`docs/tasks/M33_controlled_apply_executor/T409_apply_executor_audit_manifest.md`.

### 6. Worker Summary And Handoff

Write `docs/worker_summary/T408_worker_summary.md` and append a T408 worker
record to `docs/07_handoff.md`.

Do not mark T408 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\services\memory_lifecycle_apply_executor.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_memory_lifecycle_apply_executor.py tests\test_memory_event_store.py tests\test_memory_lifecycle_dry_run_apply.py tests\test_apply_executor_approval_gate.py -q
```

```powershell
git diff --check
```

Use project-local pytest cache and basetemp paths if the default user temp
directory is not writable.

## Reviewer Type

Adversarial local mutation review for final confirmation, memory lifecycle
mapping, rollback evidence, auditability, privacy, and no platform/provider
surface expansion.
