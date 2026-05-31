# T412: Integrated Companion Demo Scope

## Task ID

T412

## Goal

Refine M34 into concrete integrated demo requirements.

T412 should convert `docs/product/m34_integrated_companion_demo_scope.md` into
a more specific task package for the first M34 implementation step: an
integrated scenario spine for the local text-first web demo.

## Allowed Files

Future T412 worker may create or modify only:

- `docs/product/m34_integrated_companion_demo_scope.md`
- `docs/tasks/M34_integrated_companion_demo/T413_integrated_demo_scenario_spine.md`
- `docs/worker_summary/T412_worker_summary.md`
- `docs/07_handoff.md`

If T412 needs code changes, private data, source readers, model-provider calls,
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

### 1. Scope Refinement

Update `docs/product/m34_integrated_companion_demo_scope.md` if needed with
clear implementation requirements for:

- integrated scenario spine;
- reviewer-facing product readiness summary;
- trust and control explanation;
- commercialization surface;
- Browser QA expectations.

### 2. Next Task Package

Create
`docs/tasks/M34_integrated_companion_demo/T413_integrated_demo_scenario_spine.md`.

The T413 package should be code-facing and should likely allow:

- `src/practical_chat_agent/ui/text_first_web_demo_adapter.py`
- `src/practical_chat_agent/ui/static/text_first_web_demo.js`
- `src/practical_chat_agent/ui/static/text_first_web_demo.css`
- focused tests for the integrated scenario spine.

### 3. Worker Summary And Handoff

Write `docs/worker_summary/T412_worker_summary.md` and append a T412 worker
record to `docs/07_handoff.md`.

Do not mark T412 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

```powershell
git diff --check
```

## Reviewer Type

Product-scope review for demo coherence, local-only boundaries, and readiness
for a code-facing integrated scenario task.
