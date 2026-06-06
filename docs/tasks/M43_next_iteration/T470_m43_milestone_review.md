# T470: M43 Milestone Review

## Task ID

T470

## Goal

Review M43 end to end and record whether the local persona-draft
apply-readiness preview is coherent, deterministic, reviewable, and bounded.

This task is review/documentation plus verification only. It must not add new
product behavior beyond review findings and the next iteration scope/task
package.

## Context

M43 was scoped to build a local apply-readiness preview layer after M42's
proposal-linked persona draft. The completed M43 slices are:

- T465: M43 scope and first implementation package;
- T466: `source_draft_apply_readiness` payload;
- T467: static readiness UI;
- T468: Review Workspace linkage;
- T469: responsive hardening.

T470 should verify that M43 remains local-only, deterministic, synthetic,
preview-only, review-required, non-extracting, non-mutating, non-sending,
non-platform, and media-runtime disabled.

## Allowed Files

Future T470 worker may create or modify only:

- `docs/review/M43_review.md`
- `docs/product/m44_next_iteration_scope.md`
- `docs/tasks/M44_next_iteration/T471_next_iteration_scope.md`
- `docs/worker_summary/T470_worker_summary.md`
- `docs/07_handoff.md`

If review identifies implementation defects that require code or test changes,
Captain must create a separate implementation task package before editing code.

## Review Inputs

- `docs/product/m43_next_iteration_scope.md`
- `docs/tasks/M43_next_iteration/T465_next_iteration_scope.md`
- `docs/tasks/M43_next_iteration/T466_source_draft_apply_readiness_payload.md`
- `docs/tasks/M43_next_iteration/T467_source_draft_apply_readiness_ui.md`
- `docs/tasks/M43_next_iteration/T468_source_draft_apply_readiness_review_linkage.md`
- `docs/tasks/M43_next_iteration/T469_source_draft_apply_readiness_responsive_hardening.md`
- `docs/contracts/source_draft_apply_readiness_payload.md`
- `docs/worker_summary/T465_worker_summary.md`
- `docs/worker_summary/T466_worker_summary.md`
- `docs/worker_summary/T467_worker_summary.md`
- `docs/worker_summary/T468_worker_summary.md`
- `docs/worker_summary/T469_worker_summary.md`
- `src/practical_chat_agent/ui/text_first_web_demo_adapter.py`
- `src/practical_chat_agent/ui/static/text_first_web_demo.html`
- `src/practical_chat_agent/ui/static/text_first_web_demo.css`
- `src/practical_chat_agent/ui/static/text_first_web_demo.js`
- T466-T469 focused tests.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'; pytest tests\test_source_draft_apply_readiness_payload.py tests\test_static_source_draft_apply_readiness.py tests\test_source_draft_apply_readiness_review_linkage.py tests\test_source_draft_apply_readiness_responsive_hardening.py tests\test_text_first_web_demo_local_server.py tests\test_text_first_web_demo_static.py tests\test_text_first_web_demo_state_switching.py -q -o cache_dir=artifacts\t470_pytest_cache --basetemp=artifacts\t470_pytest_basetemp
```

```powershell
python -m py_compile src\practical_chat_agent\ui\text_first_web_demo_adapter.py
```

```powershell
node --check src\practical_chat_agent\ui\static\text_first_web_demo.js
```

```powershell
git diff --check
```

## Expected Review Output

- A `docs/review/M43_review.md` verdict of `PASS`, `PASS_WITH_WARNINGS`, or
  `BLOCK`.
- A concise list of risks, residual gaps, and evidence.
- M44 next iteration scope and the first M44 task package if the milestone
  passes or passes with warnings.
- Worker summary and handoff record.
