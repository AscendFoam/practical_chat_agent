# T417: M35 Next Iteration Scope

## Task ID

T417

## Goal

Refine M35 into a concrete local companion session-loop milestone and create
the first implementation-facing task package.

T417 should convert `docs/product/m35_next_iteration_scope.md` into precise
payload, UI, and verification requirements for a deterministic synthetic
session loop. The task should not implement code; it should prepare the next
worker to add a safe local simulator.

## Allowed Files

Future T417 worker may create or modify only:

- `docs/product/m35_next_iteration_scope.md`
- `docs/tasks/M35_next_iteration/T418_local_companion_session_simulator.md`
- `docs/worker_summary/T417_worker_summary.md`
- `docs/07_handoff.md`

If T417 needs code, tests, private data, model providers, package changes,
runtime stores, source readers, platform adapters, outbound messaging,
voice/avatar runtime, media generation, automatic apply, or task-board edits,
Captain must revise this package before assignment.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not ingest, summarize, transform, quote, or commit real private chat
  records.
- Do not call model providers.
- Do not modify code or tests.
- Do not write runtime stores.
- Do not add embeddings, vector search, semantic ranking, similarity scoring,
  fine-tuning, source readers, or real chat distillation.
- Do not add schedulers, queues, webhooks, auth, tokens, recipient ids,
  delivery state, platform adapters, automatic outreach, or outbound messaging.
- Do not add microphone, camera, ASR, TTS, voice cloning, Live2D, generated
  audio, generated image, generated video, or media capture.
- Do not add payment processing, production pricing claims, legal advice,
  compliance completion, app-store approval, launch approval, clinical claims,
  or regulator acceptance.
- Do not modify `docs/04_task_board.md`.

## Expected Outputs

### 1. Refined M35 Scope

Update `docs/product/m35_next_iteration_scope.md` with concrete requirements
for:

- local synthetic session payload fields;
- static UI session-loop layout expectations;
- post-session memory/persona/proactive candidate linkage;
- explicit non-execution flags;
- Browser QA expectations for any future UI task;
- review standards for local-only and no-private-data boundaries.

### 2. T418 Task Package

Create `docs/tasks/M35_next_iteration/T418_local_companion_session_simulator.md`
as the first code-facing task for M35.

T418 should be scoped to adding the deterministic synthetic session payload and
tests only. It should not render UI unless T417 explicitly decides a combined
payload/UI slice is safer and small enough.

### 3. Worker Summary And Handoff

Write `docs/worker_summary/T417_worker_summary.md` and append a T417 worker
record to `docs/07_handoff.md`.

Do not mark T417 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

```powershell
git diff --check
```

## Reviewer Type

Product-scope review for local session-loop clarity, synthetic-only
boundaries, and readiness for a code-facing companion session simulator task.
