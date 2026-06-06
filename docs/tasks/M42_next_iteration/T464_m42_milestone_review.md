# T464: M42 Milestone Review

## Task ID

T464

## Goal

Review M42 as a local proposal-to-persona-draft preview milestone.

M42 should prove that deterministic M41 source-evidence persona proposal
candidates can be converted into an inspectable M42 persona draft preview,
rendered in the static text-first demo, linked into Review Workspace, and
hardened for static responsive behavior.

This task is review/documentation only. It must not add product behavior,
source readers, private data access, model providers, embeddings, extraction,
store writes, persona apply, outbound messaging, platform adapters, or media
runtime.

## Scope To Review

- T459: M42 next-iteration scope.
- T460: `source_proposal_persona_draft` payload and contract tests.
- T461: static source proposal persona draft UI.
- T462: source proposal persona draft Review Workspace linkage.
- T463: source proposal persona draft responsive hardening.

## Allowed Files

Future T464 reviewer may create or modify only:

- `docs/review/M42_review.md`
- `docs/product/m43_next_iteration_scope.md`
- `docs/tasks/M43_next_iteration/T465_next_iteration_scope.md`
- `docs/worker_summary/T464_worker_summary.md`
- `docs/07_handoff.md`

If review discovers a blocker requiring implementation fixes, stop and create
a follow-up task package instead of changing product code inside T464.

## Expected Review Questions

- Does M42 expose `source_proposal_persona_draft` in adapter state and served
  demo JSON?
- Does the draft payload link back to `m41.source_evidence_persona_proposal.v1`?
- Are required field paths covered: `style.tone`, `style.pacing`,
  `style.humor`, `relationship.boundary_style`, `memory.use_preference`, and
  `growth.short_term_hint`?
- Are draft field changes linked to proposal ids, trait hypothesis ids, and
  evidence row ids?
- Are unchanged fields, conflicts, rollback refs, gates, outcomes, apply
  policy, and non-execution flags visible?
- Does the static UI render draft payload details without action controls?
- Does Review Workspace expose draft review cards and a `Draft` filter?
- Do responsive hardening tests cover long ids and narrow viewports?
- Does M42 remain local, deterministic, synthetic, preview-only,
  non-extracting, non-mutating, non-sending, non-platform, and
  media-runtime disabled?

## Verification

Minimum command:

```powershell
$env:PYTHONPATH='src'; pytest tests\test_source_proposal_persona_draft_payload.py tests\test_static_source_proposal_persona_draft.py tests\test_source_proposal_persona_draft_review_linkage.py tests\test_source_proposal_persona_draft_responsive_hardening.py tests\test_text_first_web_demo_local_server.py tests\test_text_first_web_demo_static.py tests\test_text_first_web_demo_state_switching.py -q -o cache_dir=artifacts\t464_pytest_cache --basetemp=artifacts\t464_pytest_basetemp
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

## Expected Output

- `docs/review/M42_review.md` with `PASS`, `PASS_WITH_WARNINGS`, or `BLOCK`.
- If passing, `docs/product/m43_next_iteration_scope.md`.
- If passing, `docs/tasks/M43_next_iteration/T465_next_iteration_scope.md`.
- `docs/worker_summary/T464_worker_summary.md`.
- Updated `docs/07_handoff.md`.
