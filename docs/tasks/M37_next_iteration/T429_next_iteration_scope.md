# T429: M37 Next Iteration Scope

## Task ID

T429

## Goal

Refine M37 into a concrete controlled persona evolution preview milestone and
create the first implementation-facing task package.

T429 should convert `docs/product/m37_next_iteration_scope.md` into precise
payload, safety, UI, and verification requirements for a deterministic local
persona evolution preview. The task should not implement code.

## Allowed Files

Future T429 worker may create or modify only:

- `docs/product/m37_next_iteration_scope.md`
- `docs/tasks/M37_next_iteration/T430_persona_evolution_preview_payload.md`
- `docs/worker_summary/T429_worker_summary.md`
- `docs/07_handoff.md`

If T429 needs code, tests, private data, source readers, model providers,
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
  regulator acceptance, or user-study validation.
- Do not modify `docs/04_task_board.md`.

## Expected Outputs

### 1. Refined M37 Scope

Update `docs/product/m37_next_iteration_scope.md` with concrete requirements
for:

- source trait candidate refs;
- persona snapshot before/after summaries;
- patch candidate fields;
- risk labels;
- rollback notes;
- blocked request exclusion;
- non-execution flags;
- later UI and Browser QA expectations.

### 2. T430 Task Package

Create
`docs/tasks/M37_next_iteration/T430_persona_evolution_preview_payload.md`.

T430 should be scoped to adding the deterministic synthetic
`persona_evolution_preview` adapter payload and tests only. It should not render
UI unless T429 explicitly decides a combined payload/UI slice is safer and
small enough.

### 3. Worker Summary And Handoff

Write `docs/worker_summary/T429_worker_summary.md` and append a T429 worker
record to `docs/07_handoff.md`.

Do not mark T429 complete in `docs/04_task_board.md`.

## Verification

Minimum command:

```powershell
git diff --check
```

## Reviewer Type

Product-scope review for persona evolution clarity, review-only semantics,
rollback/risk requirements, and readiness for a code-facing evolution preview
payload task.
