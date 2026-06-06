# T436 Worker Summary

Task: Persona Version Draft Ledger Payload

## Files Changed

- `src/practical_chat_agent/ui/text_first_web_demo_adapter.py`
- `tests/test_persona_version_draft_ledger_payload.py`
- `tests/test_text_first_web_demo_local_server.py`
- `docs/contracts/persona_version_draft_ledger_payload.md`
- `docs/tasks/M38_next_iteration/T437_persona_version_draft_ledger_ui.md`
- `docs/worker_summary/T436_worker_summary.md`
- `docs/07_handoff.md`

## TDD Evidence

RED:

```powershell
$env:PYTHONPATH='src'; pytest tests\test_persona_version_draft_ledger_payload.py tests\test_persona_evolution_preview_payload.py tests\test_text_first_web_demo_local_server.py -q -o cache_dir=artifacts\t436_pytest_cache --basetemp=artifacts\t436_pytest_basetemp
```

Result: failed with `7 failed, 12 passed` because
`persona_version_draft_ledger` was not present in adapter state or served JSON.

GREEN:

```powershell
$env:PYTHONPATH='src'; pytest tests\test_persona_version_draft_ledger_payload.py tests\test_persona_evolution_preview_payload.py tests\test_text_first_web_demo_local_server.py -q -o cache_dir=artifacts\t436_pytest_cache --basetemp=artifacts\t436_pytest_basetemp
```

Result: passed, `19 passed`.

## Implementation Result

- Added `persona_version_draft_ledger` to `TextFirstWebDemoState`.
- Added deterministic local ledger payload with:
  - source M37 evolution preview ref;
  - base persona snapshot ref;
  - accepted/deferred/rejected version drafts;
  - conflict notes for persona drift, boundary weakening, weak evidence,
    overattachment risk, and blocked-source contamination;
  - rollback ref index;
  - review outcome labels;
  - preview-only apply policy;
  - non-execution flags.
- Added contract tests for source linkage, draft outcomes, conflict notes,
  rollback refs, blocked-source exclusion behavior, and unsafe-state scanning.
- Updated local server JSON test to require the ledger payload.
- Added `docs/contracts/persona_version_draft_ledger_payload.md`.
- Created the T437 static UI task package.

## Verification

```powershell
$env:PYTHONPATH='src'; pytest tests\test_persona_version_draft_ledger_payload.py tests\test_persona_evolution_preview_payload.py tests\test_text_first_web_demo_local_server.py -q -o cache_dir=artifacts\t436_pytest_cache --basetemp=artifacts\t436_pytest_basetemp
```

Result: passed, `19 passed`.

## Explicit Non-Actions

- No static UI rendering, JavaScript/CSS edits, package dependencies, source
  readers, model-provider calls, embeddings, vector search, semantic ranking,
  similarity scoring, fine-tuning, runtime store writes, PersonaCard
  synthesis, platform adapters, schedulers, queues, webhooks, tokens,
  recipient ids, delivery state, outbound messaging, automatic outreach,
  voice/avatar runtime, media generation, payment processing, or task-board
  edits were added.
- No legal advice, compliance completion, app-store approval, launch approval,
  user-study validation, pricing validation, clinical claims, real user
  evidence, or regulator acceptance was claimed.
- No `private/chat_history/`, `private/distilled/`, or private artifact content
  was read, quoted, summarized, transformed, or committed.

## Remaining Risks

- T437 still needs static ledger rendering.
- Version drafts remain deterministic synthetic previews and do not apply
  persona changes or write stores.
