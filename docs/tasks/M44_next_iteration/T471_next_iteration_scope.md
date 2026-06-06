# T471: M44 Next Iteration Scope

## Task ID

T471

## Goal

Refine M44 into an implementation-ready package for a local
`source_draft_apply_plan_preview` payload.

This task is planning/docs only. It must not add runtime behavior, source
readers, private data access, model providers, embeddings, real extraction,
store writes, persona apply, outbound messaging, platform adapters, or media
runtime.

## Context

M43 produced `source_draft_apply_readiness`, static readiness UI, readiness
Review Workspace cards, and responsive hardening. M44 should take the next
local-only step by converting readiness records into a manual apply-plan
preview. The preview should explain which draft fields would be included,
deferred, or blocked before any future separately scoped executor.

## Allowed Files

Future T471 worker may create or modify only:

- `docs/product/m44_next_iteration_scope.md`
- `docs/tasks/M44_next_iteration/T472_source_draft_apply_plan_preview_payload.md`
- `docs/worker_summary/T471_worker_summary.md`
- `docs/07_handoff.md`

If implementation requires code, tests, package changes, private data,
provider calls, source readers, store writes, platform adapters, outbound
messaging, media runtime, or task-board edits, Captain must create a separate
task package.

## Expected Output

- Clarify the M44 implementation sequence.
- Define T472 as a payload-only task for
  `source_draft_apply_plan_preview`.
- Preserve the distinction between:
  - M42 persona draft preview;
  - M43 apply-readiness preview;
  - M44 apply-plan preview;
  - future reviewed apply executor.

## Verification

Minimum command:

```powershell
git diff --check
```

## Reviewer Type

Planning review for scope clarity, safety boundaries, and implementation
readiness.
