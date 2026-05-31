# T407: Persona Growth Apply Executor

## Task ID

T407

## Goal

Implement a local-only persona growth apply executor.

T407 should apply a reviewed `PersonaGrowthDryRunPlan` to a caller-supplied
`PersonaVersionStore` only when final human confirmation, manual apply
eligibility, and apply executor approval all agree. It should write a new
persona version and return an audit record with rollback references.

## Allowed Files

Future T407 worker may create or modify only:

- `src/practical_chat_agent/services/persona_growth_apply_executor.py`
- `tests/test_persona_growth_apply_executor.py`
- `docs/data_contracts/persona_growth_apply_executor_contract.md`
- `docs/tasks/M33_controlled_apply_executor/T408_memory_lifecycle_apply_executor.md`
- `docs/worker_summary/T407_worker_summary.md`
- `docs/07_handoff.md`

If T407 needs private data, source readers, model-provider calls, local server
routes, package changes, platform adapters, outbound messaging, voice/avatar
runtime, media generation, automatic apply triggers, or memory lifecycle
mutation, Captain must revise this package before assignment.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not ingest, summarize, transform, quote, or commit real private chat
  records.
- Do not call model providers.
- Do not implement source readers, extraction from real logs, embeddings,
  vector search, semantic ranking, fine-tuning, similarity scoring, persona
  synthesis, final companion reply generation, or runtime memory mutation.
- Do not mutate memory stores.
- Do not add routes, CLIs, schedulers, queues, webhooks, auth, tokens,
  recipient ids, delivery state, or platform persistence behavior.
- Do not implement proactive candidates, automatic outreach, sending,
  scheduling, notifications, platform delivery, microphone, camera, ASR, TTS,
  voice cloning, voice/avatar likeness, Live2D, generated audio, generated
  image, generated video, or media capture.
- Do not modify `docs/04_task_board.md`.

## Expected Outputs

### 1. Executor And Audit Records

Create `persona_growth_apply_executor.py` with records such as:

- `PersonaGrowthApplyRequest`
- `PersonaGrowthApplyAudit`
- `PersonaGrowthApplyExecutor`

The request should include:

- dry-run plan;
- manual eligibility decision;
- apply executor approval decision;
- persona version store;
- reviewer id;
- final confirmation phrase or token.

The audit should include:

- apply id;
- persona id;
- patch id;
- prior version id;
- new version id;
- changed field paths;
- rollback target version id;
- reviewer id;
- gate ids/outcomes;
- safe summary;
- local-only flags.

### 2. Executor Behavior

The executor should:

- require `final_confirmation="CONFIRM_LOCAL_PERSONA_APPLY"`;
- require manual eligibility outcome `eligible`;
- require apply executor final outcome
  `ready_for_separately_scoped_executor_design`;
- require the latest store version to match the dry-run source persona version;
- apply only field paths present in the dry-run plan previews;
- cap numeric trait movement by the already-reviewed dry-run plan;
- write exactly one new `PersonaVersionStore` record;
- return an audit record with rollback target id;
- reject stale source versions, blocked plans, blocked gates, missing
  confirmation, unknown fields, and empty field previews.

### 3. Tests

Create `tests/test_persona_growth_apply_executor.py` proving:

- a safe confirmed persona growth plan writes one new persona version;
- the original version remains available as rollback target;
- missing confirmation blocks writes;
- blocked manual eligibility blocks writes;
- blocked or needs_review approval blocks writes;
- stale source version blocks writes;
- forbidden private/provider/outbound/media fields are absent from audit
  records;
- executor exposes no provider, outbound, voice/avatar, media, scheduler, or
  platform methods.

### 4. Data Contract

Create `docs/data_contracts/persona_growth_apply_executor_contract.md`.

### 5. Next Task Package

Create
`docs/tasks/M33_controlled_apply_executor/T408_memory_lifecycle_apply_executor.md`.

### 6. Worker Summary And Handoff

Write `docs/worker_summary/T407_worker_summary.md` and append a T407 worker
record to `docs/07_handoff.md`.

Do not mark T407 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\services\persona_growth_apply_executor.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_persona_growth_apply_executor.py tests\test_persona_version_store.py tests\test_persona_growth_dry_run_apply.py tests\test_apply_executor_approval_gate.py -q
```

```powershell
git diff --check
```

Use project-local pytest cache and basetemp paths if the default user temp
directory is not writable.

## Reviewer Type

Adversarial local mutation review for final confirmation, stale-version
blocking, rollback evidence, auditability, privacy, and no platform/provider
surface expansion.
