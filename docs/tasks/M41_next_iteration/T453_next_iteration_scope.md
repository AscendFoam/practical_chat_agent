# T453: M41 Next Iteration Scope

## Task ID

T453

## Goal

Refine M41 into a concrete first implementation task for local
source-evidence-to-persona-proposal preview work.

This task is docs-only. It must not change product code, tests, static assets,
adapter payloads, source readers, model providers, stores, outbound messaging,
platform integrations, media runtime, payment processing, or task board state.

## Context

M40 completed a local source evidence matrix. M41 should not jump to real
source extraction or PersonaCard mutation. The next safe slice is a
deterministic proposal payload that translates already-reviewed synthetic
evidence summaries into reviewable persona proposal candidates.

## Allowed Files

Future T453 worker may create or modify only:

- `docs/product/m41_next_iteration_scope.md`
- `docs/tasks/M41_next_iteration/T454_source_evidence_persona_proposal_payload.md`
- `docs/worker_summary/T453_worker_summary.md`
- `docs/07_handoff.md`

If implementation requires product code, tests, static assets, source readers,
model providers, private data, runtime stores, platform adapters, outbound
messaging, media runtime, automatic apply, package changes, or task-board
edits, Captain must revise this package before assignment.

## Expected Output

- Refined M41 scope with the first implementation slice.
- A T454 task package for `source_evidence_persona_proposal` payload and
  contract tests.
- Worker summary and handoff record.

## Constraints

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not claim real persona distillation, source extraction, provider
  inference, embeddings, store writes, runtime mutation, automatic apply,
  outbound messaging, platform integration, media generation, launch readiness,
  or compliance completion.

## Verification

Minimum command:

```powershell
git diff --check
```

## Reviewer Type

Scope review for M41 proposal-preview direction and safe T454 packaging.
