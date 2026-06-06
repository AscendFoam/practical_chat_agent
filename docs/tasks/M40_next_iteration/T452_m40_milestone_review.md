# T452: M40 Milestone Review

## Task ID

T452

## Goal

Review M40 as the persona source evidence matrix milestone.

This task is review-only. It may evaluate T447 through T451 evidence, create
the M40 review artifact, define the next milestone scope, create the next task
package, write worker summary, and update handoff. It must not change product
code, tests, adapters, runtime behavior, source readers, model providers,
stores, outbound messaging, platform integrations, media runtime, payment
processing, or task board state.

## Context

M40 currently covers:

- T447 M40 scope refinement;
- T448 `persona_source_evidence_matrix` payload;
- T449 static evidence matrix UI;
- T450 Review Workspace evidence linkage;
- T451 responsive hardening for source evidence matrix and evidence cards.

The milestone should decide whether M40 safely demonstrates a local,
deterministic, synthetic, preview-only source evidence matrix for future
consented persona distillation work.

## Allowed Files

Future T452 worker may create or modify only:

- `docs/review/M40_review.md`
- `docs/product/m41_next_iteration_scope.md`
- `docs/tasks/M41_next_iteration/T453_next_iteration_scope.md`
- `docs/worker_summary/T452_worker_summary.md`
- `docs/07_handoff.md`

If review requires product code, tests, static assets, adapter payload changes,
source readers, model providers, private data, runtime stores, platform
adapters, outbound messaging, media runtime, automatic apply, package changes,
or task-board edits, Captain must revise this package before assignment.

## Review Questions

- Does M40 expose a deterministic source evidence matrix linked to M39 source
  intake manifest?
- Are eligible and excluded sources visible and reviewable?
- Do evidence rows, trait hypotheses, quality labels, and review gates remain
  local synthetic previews?
- Are source evidence records visible in Review Workspace with safe detail
  rows and filter tabs?
- Do responsive rules cover long ids and narrow viewports?
- Do tests prove no private-source reads, provider calls, raw retention,
  extraction, embeddings, store writes, persona mutation, automatic apply,
  outbound messaging, platform adapters, or media runtime?
- Is the next milestone scoped without pretending that real persona
  distillation or source extraction is already implemented?

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'; pytest tests\test_persona_source_evidence_matrix_payload.py tests\test_static_persona_source_evidence_matrix.py tests\test_persona_source_evidence_review_linkage.py tests\test_persona_source_evidence_responsive_hardening.py tests\test_text_first_web_demo_local_server.py tests\test_text_first_web_demo_static.py tests\test_text_first_web_demo_state_switching.py -q -o cache_dir=artifacts\t452_pytest_cache --basetemp=artifacts\t452_pytest_basetemp
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

## Reviewer Type

Milestone review for source-evidence matrix completeness, safety boundaries,
test evidence, and next-iteration scoping.
