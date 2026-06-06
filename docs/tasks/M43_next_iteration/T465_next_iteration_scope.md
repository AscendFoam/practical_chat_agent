# T465: M43 Next Iteration Scope

## Task ID

T465

## Goal

Refine M43 into an implementable payload-first task package for local
persona-draft apply-readiness preview.

This task is documentation-only. It must not add product code, tests, source
readers, private data access, model providers, embeddings, extraction, store
writes, persona apply, outbound messaging, platform adapters, or media
runtime.

## Context

M42 produced a proposal-linked persona draft preview. M43 should evaluate that
draft for future apply-readiness while preserving the current preview-only
boundary.

The first implementation task after T465 should likely add
`source_draft_apply_readiness` to `TextFirstWebDemoState` and
`/demo-state.json`.

## Allowed Files

Future T465 worker may create or modify only:

- `docs/product/m43_next_iteration_scope.md`
- `docs/tasks/M43_next_iteration/T466_source_draft_apply_readiness_payload.md`
- `docs/worker_summary/T465_worker_summary.md`
- `docs/07_handoff.md`

Do not modify `docs/04_task_board.md`.

## Expected Output

- Refined M43 scope with a concrete T466 implementation slice.
- T466 task package for payload and contract tests.
- Worker summary and handoff entry.

## Required Boundaries

T465 must preserve M43 as:

- local-only;
- deterministic;
- synthetic-fixture-based;
- preview-only;
- review-required;
- non-extracting;
- non-mutating;
- non-sending;
- non-platform;
- media-runtime disabled.

T465 must not authorize real source extraction, private chat reading,
provider calls, embeddings, PersonaCard writes, runtime store writes,
automatic apply, outbound messaging, platform adapters, or media runtime.

## Verification

Minimum command:

```powershell
git diff --check
```

## Reviewer Type

Documentation scope review for M43 readiness and T466 package clarity.
