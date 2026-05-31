# T416: M34 Milestone Review

## Task ID

T416

## Goal

Review and close M34 integrated companion demo work.

T416 should perform an adversarial review of T412 through T415 and decide
whether M34 can be closed as `PASS`, `PASS_WITH_WARNINGS`, or `BLOCK`. If M34
passes, T416 should open the next milestone for deeper demo/product iteration.

## Allowed Files

Future T416 worker may create or modify only:

- `docs/review/M34_review.md`
- `docs/product/m35_next_iteration_scope.md`
- `docs/tasks/M35_next_iteration/T417_next_iteration_scope.md`
- `docs/worker_summary/T416_worker_summary.md`
- `docs/07_handoff.md`

If T416 needs code changes, private data, source readers, model-provider calls,
package changes, external system adapters, outbound messaging, voice/avatar
runtime, media generation, automatic apply triggers, PersonaVersionStore
writes, or MemoryEventStore writes, Captain must revise this package before
assignment.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not ingest, summarize, transform, quote, or commit real private chat
  records.
- Do not call model providers.
- Do not modify code.
- Do not write runtime stores.
- Do not add schedulers, queues, webhooks, auth, tokens, recipient ids,
  delivery state, or external-system persistence behavior.
- Do not modify `docs/04_task_board.md`.

## Expected Outputs

### 1. M34 Review

Create `docs/review/M34_review.md` covering:

- integrated scenario spine coherence;
- trust/commercial positioning safety;
- responsive/static UI hardening;
- Browser QA evidence;
- no private/provider/outbound/media surface expansion;
- residual risks and verdict.

### 2. Next Milestone Scope

If verdict is not `BLOCK`, create `docs/product/m35_next_iteration_scope.md`.

### 3. Next Task Package

If verdict is not `BLOCK`, create
`docs/tasks/M35_next_iteration/T417_next_iteration_scope.md`.

### 4. Worker Summary And Handoff

Write `docs/worker_summary/T416_worker_summary.md` and append a T416 worker
record to `docs/07_handoff.md`.

Do not mark T416 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

```powershell
git diff --check
```

Optionally rerun M34 focused UI tests if reviewer confidence requires fresh
evidence.

## Reviewer Type

Adversarial milestone review for demo coherence, commercialization safety,
responsive UI, local-only boundaries, and no provider/outbound/media surface
expansion.
