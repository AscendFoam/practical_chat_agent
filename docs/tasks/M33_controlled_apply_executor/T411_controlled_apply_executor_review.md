# T411: Controlled Apply Executor Review

## Task ID

T411

## Goal

Review and close M33 controlled apply executor work.

T411 should perform an adversarial documentation-level review of T407 through
T410 and decide whether M33 can be closed as `PASS`, `PASS_WITH_WARNINGS`, or
`BLOCK`. If M33 passes, T411 should open the next milestone for integrated
companion demo polish.

## Allowed Files

Future T411 worker may create or modify only:

- `docs/review/M33_review.md`
- `docs/product/m34_integrated_companion_demo_scope.md`
- `docs/tasks/M34_integrated_companion_demo/T412_integrated_companion_demo_scope.md`
- `docs/worker_summary/T411_worker_summary.md`
- `docs/07_handoff.md`

If T411 needs code changes, private data, source readers, model-provider calls,
package changes, platform adapters, outbound messaging, voice/avatar runtime,
media generation, automatic apply triggers, PersonaVersionStore writes, or
MemoryEventStore writes, Captain must revise this package before assignment.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not ingest, summarize, transform, quote, or commit real private chat
  records.
- Do not call model providers.
- Do not modify code.
- Do not write PersonaVersionStore or MemoryEventStore.
- Do not add routes, CLIs, schedulers, queues, webhooks, auth, tokens,
  recipient ids, delivery state, or platform persistence behavior.
- Do not modify `docs/04_task_board.md`.

## Expected Outputs

### 1. M33 Review

Create `docs/review/M33_review.md` covering:

- local-only apply boundaries;
- final confirmation gates;
- manual eligibility gates;
- apply executor approval gates;
- persona version rollback evidence;
- memory lifecycle rollback evidence;
- audit manifest completeness;
- review workspace projection safety;
- forbidden private/provider/outbound/media surface checks;
- residual risks and verdict.

### 2. Next Milestone Scope

If verdict is not `BLOCK`, create
`docs/product/m34_integrated_companion_demo_scope.md` describing the next
milestone for polishing the integrated local web demo across persona, memory,
review, proactive, life stream, voice/avatar locked states, and commercial
positioning surfaces.

### 3. Next Task Package

If verdict is not `BLOCK`, create
`docs/tasks/M34_integrated_companion_demo/T412_integrated_companion_demo_scope.md`.

### 4. Worker Summary And Handoff

Write `docs/worker_summary/T411_worker_summary.md` and append a T411 worker
record to `docs/07_handoff.md`.

Do not mark T411 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

```powershell
git diff --check
```

Optionally rerun the M33 focused test suites if reviewer confidence requires
fresh code evidence.

## Reviewer Type

Adversarial milestone review for mutation safety, rollback auditability,
privacy, local-only boundaries, and no platform/provider/media surface
expansion.
