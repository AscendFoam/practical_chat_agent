# M42 Milestone Review

Status: `PASS_WITH_WARNINGS`

Review date: 2026-06-02

## Scope Reviewed

M42 reviewed the local proposal-to-persona-draft preview layer:

- T459: M42 scope refinement and T460 task package.
- T460: `source_proposal_persona_draft` payload and contract tests.
- T461: static web demo rendering for persona draft preview.
- T462: Review Workspace linkage for draft records.
- T463: responsive hardening for draft UI and draft review cards.

## Verdict

M42 passes as a deterministic, local, synthetic, preview-only bridge from M41
source-evidence persona proposal candidates to an inspectable persona draft
preview.

The milestone proves that the demo can show:

- source proposal linkage;
- selected proposal ids;
- base persona snapshot;
- draft field changes for required persona paths;
- unchanged field summaries;
- conflict notes;
- rollback refs;
- review gate results;
- draft outcome labels;
- static draft UI;
- Review Workspace draft cards;
- responsive wrapping for dense draft ids and refs.

M42 does not prove real source extraction, private-source ingestion, model
provider inference, embeddings, PersonaCard mutation, memory writes, review
store writes, runtime writes, outbound messaging, platform adapters, or media
runtime.

## Evidence

Verification command:

```powershell
$env:PYTHONPATH='src'; pytest tests\test_source_proposal_persona_draft_payload.py tests\test_static_source_proposal_persona_draft.py tests\test_source_proposal_persona_draft_review_linkage.py tests\test_source_proposal_persona_draft_responsive_hardening.py tests\test_text_first_web_demo_local_server.py tests\test_text_first_web_demo_static.py tests\test_text_first_web_demo_state_switching.py -q -o cache_dir=artifacts\t464_pytest_cache --basetemp=artifacts\t464_pytest_basetemp
```

Result: `33 passed`.

Additional checks:

```powershell
python -m py_compile src\practical_chat_agent\ui\text_first_web_demo_adapter.py
```

Result: passed.

```powershell
node --check src\practical_chat_agent\ui\static\text_first_web_demo.js
```

Result: passed.

## What M42 Adds

### Payload

M42 adds `source_proposal_persona_draft` to `TextFirstWebDemoState` and
`/demo-state.json`.

The payload includes:

- `schema_version: m42.source_proposal_persona_draft.v1`;
- source proposal ref;
- base persona snapshot;
- selected proposal ids;
- draft field changes;
- unchanged field summaries;
- conflict notes;
- rollback refs;
- review gate results;
- draft outcome labels;
- preview-only apply policy;
- strict non-execution flags.

Required draft paths are covered:

- `style.tone`;
- `style.pacing`;
- `style.humor`;
- `relationship.boundary_style`;
- `memory.use_preference`;
- `growth.short_term_hint`.

### Static UI

M42 adds the `#source-proposal-persona-draft` section to the static text-first
web demo. It renders proposal linkage, base snapshot, selected proposal ids,
field changes, unchanged fields, conflicts, rollback refs, gates, outcomes,
and non-execution labels from embedded state or JavaScript fallback state.

### Review Workspace

M42 adds `review_workspace.source_draft_review_cards` and a `Draft` filter
tab. Review cards cover:

- draft field changes;
- unchanged field summaries;
- conflict notes;
- rollback refs;
- draft review gates;
- draft outcome labels.

Each card remains review-required, preview-only, non-mutating, non-sending,
and runtime-not-ready.

## Boundaries Preserved

M42 preserves these boundaries:

- no `private/chat_history/` or private artifact reads;
- no source reader or upload flow;
- no raw content retention;
- no trait extraction from real content;
- no provider calls;
- no embeddings or vector indexes;
- no PersonaCard write;
- no PersonaVersionStore write;
- no memory-store write;
- no review-store write;
- no runtime-store write;
- no automatic apply;
- no outbound messaging;
- no platform adapter;
- no voice/avatar/media runtime.

## Warnings

- Browser-level layout QA was not claimed for T461-T463 because no callable
  in-app browser DOM inspection tool was exposed in those turns.
- M42 remains synthetic-fixture-only. It does not ingest real user-provided
  files or chat archives.
- M42 drafts are not applied to PersonaCard or runtime persona state.
- The current static fallback mirrors the deterministic payload by hand. Future
  larger payload families may need a more systematic fixture generation path.

## Gate Decision

`PASS_WITH_WARNINGS`

M42 is safe to use as evidence for the next local prototype milestone:
reviewing persona draft apply-readiness before any actual apply executor work.

M42 does not authorize real source extraction, automatic persona mutation,
platform delivery, outbound messaging, or media runtime.
