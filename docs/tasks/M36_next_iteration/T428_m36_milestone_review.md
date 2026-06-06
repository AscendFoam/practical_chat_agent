# T428: M36 Milestone Review

## Task ID

T428

## Goal

Review M36 end to end and decide whether the persona intake/distillation
workbench milestone can close.

T428 should inspect T423 through T427 and produce a milestone verdict plus the
next iteration scope. It should be adversarial about synthetic-only boundaries,
clone/deception blocking, review-only semantics, static UI safety, Browser QA,
and readiness for the next product slice.

## Allowed Files

Future T428 worker may create or modify only:

- `docs/review/M36_review.md`
- `docs/product/m37_next_iteration_scope.md`
- `docs/tasks/M37_next_iteration/T429_next_iteration_scope.md`
- `docs/worker_summary/T428_worker_summary.md`
- `docs/07_handoff.md`

If review requires code, tests, private data, source readers, model providers,
package changes, runtime stores, platform adapters, outbound messaging, media
runtime, automatic apply, or task-board edits, Captain must revise this package
before assignment.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not ingest, summarize, transform, quote, or commit real private chat
  records.
- Do not call model providers or prompt execution layers.
- Do not modify code or tests.
- Do not write runtime stores.
- Do not add source readers, embeddings, vector search, semantic ranking,
  similarity scoring, fine-tuning, platform adapters, schedulers, queues,
  webhooks, auth, tokens, recipient ids, delivery state, automatic outreach, or
  outbound messaging.
- Do not add microphone, camera, ASR, TTS, voice cloning, Live2D, generated
  audio, generated image, generated video, or media capture.
- Do not add payment processing, production pricing claims, legal advice,
  compliance completion, app-store approval, launch approval, clinical claims,
  regulator acceptance, or user-study validation.
- Do not modify `docs/04_task_board.md`.

## Review Inputs

Review at least:

- `docs/product/m36_next_iteration_scope.md`;
- `docs/contracts/persona_distillation_workbench_payload.md`;
- `docs/worker_summary/T423_worker_summary.md`;
- `docs/worker_summary/T424_worker_summary.md`;
- `docs/worker_summary/T425_worker_summary.md`;
- `docs/worker_summary/T426_worker_summary.md`;
- `docs/worker_summary/T427_worker_summary.md`;
- relevant tests introduced in T424 through T427;
- relevant static/demo files changed in T424 through T427.

## Expected Outputs

### 1. M36 Review

Create `docs/review/M36_review.md` with:

- verdict: `PASS`, `PASS_WITH_WARNINGS`, or `BLOCK`;
- scope reviewed;
- findings ordered by severity;
- verification evidence;
- explicit non-actions;
- remaining risks;
- recommendation for M37.

### 2. M37 Scope

Create `docs/product/m37_next_iteration_scope.md`.

Recommended next direction: controlled persona evolution preview. M37 should
show how reviewed workbench trait candidates can become proposed persona
version patches without writing PersonaCard or runtime stores.

### 3. T429 Task Package

Create `docs/tasks/M37_next_iteration/T429_next_iteration_scope.md` as the
first M37 task.

### 4. Worker Summary And Handoff

Write `docs/worker_summary/T428_worker_summary.md` and append a T428 worker
record to `docs/07_handoff.md`.

Do not mark T428 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'; pytest tests\test_persona_distillation_workbench_payload.py tests\test_static_persona_distillation_workbench.py tests\test_persona_workbench_review_linkage.py tests\test_persona_workbench_responsive_hardening.py tests\test_text_first_web_demo_static.py tests\test_text_first_web_demo_state_switching.py tests\test_text_first_web_demo_local_server.py -q -o cache_dir=artifacts\t428_pytest_cache --basetemp=artifacts\t428_pytest_basetemp
```

```powershell
python -m py_compile src\practical_chat_agent\ui\text_first_web_demo_adapter.py
```

```powershell
node --check src\practical_chat_agent\ui\static\text_first_web_demo.js
```

```powershell
git diff --check
```

## Reviewer Type

Milestone review for product safety, deterministic local behavior,
synthetic-only boundaries, review-only semantics, and readiness for M37.
