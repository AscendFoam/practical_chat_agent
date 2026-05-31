# T423: M36 Next Iteration Scope

## Task ID

T423

## Goal

Refine M36 into a concrete persona intake and distillation workbench milestone
and create the first implementation-facing task package.

T423 should convert `docs/product/m36_next_iteration_scope.md` into precise
payload, safety, UI, and verification requirements for a deterministic local
workbench. The task should not implement code; it should prepare the next
worker to add a safe local persona distillation contract.

## Allowed Files

Future T423 worker may create or modify only:

- `docs/product/m36_next_iteration_scope.md`
- `docs/tasks/M36_next_iteration/T424_persona_distillation_workbench_payload.md`
- `docs/worker_summary/T423_worker_summary.md`
- `docs/07_handoff.md`

If T423 needs code, tests, private data, source readers, model providers,
package changes, runtime stores, platform adapters, outbound messaging,
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

### 1. Refined M36 Scope

Update `docs/product/m36_next_iteration_scope.md` with concrete requirements
for:

- synthetic input modes;
- trait candidate categories;
- evidence refs and no-raw-private-data policy;
- blocked clone/deception request records;
- non-execution flags;
- later UI and Browser QA expectations.

### 2. T424 Task Package

Create
`docs/tasks/M36_next_iteration/T424_persona_distillation_workbench_payload.md`
as the first code-facing M36 task.

T424 should be scoped to adding the deterministic synthetic workbench payload
and tests only. It should not render UI unless T423 explicitly decides a
combined payload/UI slice is safer and small enough.

### 3. Worker Summary And Handoff

Write `docs/worker_summary/T423_worker_summary.md` and append a T423 worker
record to `docs/07_handoff.md`.

Do not mark T423 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

```powershell
git diff --check
```

## Reviewer Type

Product-scope review for persona intake/distillation clarity, synthetic-only
boundaries, clone/deception blocking, and readiness for a code-facing
workbench payload task.
