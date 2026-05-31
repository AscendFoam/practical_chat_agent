# T422: M35 Milestone Review

## Task ID

T422

## Goal

Review and close M35 local companion session-loop work.

T422 should perform an adversarial review of T417 through T421 and decide
whether M35 can be closed as `PASS`, `PASS_WITH_WARNINGS`, or `BLOCK`. If M35
passes, T422 should open the next milestone for deeper companion product
iteration.

## Allowed Files

Future T422 worker may create or modify only:

- `docs/review/M35_review.md`
- `docs/product/m36_next_iteration_scope.md`
- `docs/tasks/M36_next_iteration/T423_next_iteration_scope.md`
- `docs/worker_summary/T422_worker_summary.md`
- `docs/07_handoff.md`

If T422 needs code changes, tests, private data, source readers, model-provider
calls, package changes, platform adapters, outbound messaging, voice/avatar
runtime, media generation, automatic apply, PersonaVersionStore writes,
MemoryEventStore writes, runtime store writes, or task-board edits, Captain
must revise this package before assignment.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not ingest, summarize, transform, quote, or commit real private chat
  records.
- Do not call model providers.
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
  or regulator acceptance.
- Do not modify `docs/04_task_board.md`.

## Expected Outputs

### 1. M35 Review

Create `docs/review/M35_review.md` covering:

- local companion session payload coherence;
- static session loop readability;
- session candidate review linkage;
- responsive/browser QA evidence;
- no private/provider/outbound/media surface expansion;
- residual risks and verdict.

### 2. Next Milestone Scope

If verdict is not `BLOCK`, create `docs/product/m36_next_iteration_scope.md`.

### 3. Next Task Package

If verdict is not `BLOCK`, create
`docs/tasks/M36_next_iteration/T423_next_iteration_scope.md`.

### 4. Worker Summary And Handoff

Write `docs/worker_summary/T422_worker_summary.md` and append a T422 worker
record to `docs/07_handoff.md`.

Do not mark T422 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

```powershell
git diff --check
```

Optionally rerun M35 focused UI tests if reviewer confidence requires fresh
evidence.

## Reviewer Type

Adversarial milestone review for local session-loop coherence, review-first
candidate linkage, responsive UI, synthetic-only boundaries, and no
provider/outbound/media surface expansion.
