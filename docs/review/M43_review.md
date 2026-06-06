# M43 Milestone Review

Status: `PASS_WITH_WARNINGS`

Review date: 2026-06-06

## Scope Reviewed

M43 reviewed the local persona-draft apply-readiness preview layer:

- T465: M43 scope refinement and T466 task package.
- T466: `source_draft_apply_readiness` payload and contract tests.
- T467: static web demo rendering for apply-readiness records.
- T468: Review Workspace linkage for readiness records.
- T469: responsive hardening for readiness UI and readiness review cards.

## Verdict

M43 passes as a deterministic, local, synthetic, preview-only bridge from M42
persona draft preview to a reviewable apply-readiness preview.

The milestone proves that the demo can show:

- evaluated M42 draft change ids;
- per-field readiness records;
- readiness outcomes `blocked`, `needs_manual_review`, and
  `ready_for_future_apply_design`;
- blocked condition records;
- required review gate refs;
- rollback dependency refs;
- readiness outcome labels;
- static readiness UI;
- Review Workspace readiness cards;
- responsive wrapping for dense readiness ids, gate refs, rollback refs, and
  review detail rows.

M43 does not prove real source extraction, private-source ingestion, model
provider inference, embeddings, PersonaCard mutation, PersonaVersionStore
writes, memory writes, review store writes, runtime writes, outbound
messaging, platform adapters, media runtime, or a reviewed apply executor.

## Evidence

Verification command:

```powershell
$env:PYTHONPATH='src'; pytest tests\test_source_draft_apply_readiness_payload.py tests\test_static_source_draft_apply_readiness.py tests\test_source_draft_apply_readiness_review_linkage.py tests\test_source_draft_apply_readiness_responsive_hardening.py tests\test_text_first_web_demo_local_server.py tests\test_text_first_web_demo_static.py tests\test_text_first_web_demo_state_switching.py -q -o cache_dir=artifacts\t470_pytest_cache --basetemp=artifacts\t470_pytest_basetemp
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

## What M43 Adds

### Payload

M43 adds `source_draft_apply_readiness` to `TextFirstWebDemoState` and
`/demo-state.json`.

The payload includes:

- `schema_version: m43.source_draft_apply_readiness.v1`;
- source draft ref;
- evaluated draft change ids;
- field readiness records;
- blocked condition records;
- required review gate refs;
- rollback dependency refs;
- readiness outcome labels;
- preview-only apply policy;
- strict non-execution flags.

Required readiness fields are covered:

- `style.tone`;
- `style.pacing`;
- `style.humor`;
- `relationship.boundary_style`;
- `memory.use_preference`;
- `growth.short_term_hint`.

### Static UI

M43 adds the `#source-draft-apply-readiness` section to the static text-first
web demo. It renders draft linkage, apply policy, evaluated change ids, field
readiness records, blocked conditions, gate refs, rollback dependencies,
outcome labels, and non-execution labels from embedded state or JavaScript
fallback state.

### Review Workspace

M43 adds `review_workspace.source_readiness_review_cards` and a `Readiness`
filter tab. Review cards cover:

- field readiness records;
- blocked condition records;
- required review gate refs;
- rollback dependency refs;
- readiness outcome labels.

Each card remains review-required, preview-only, non-mutating, non-sending,
runtime-not-ready, provider-disabled, private-source-disabled,
non-extracting, non-embedding, non-platform, and media-runtime disabled.

### Responsive Hardening

M43 adds static CSS coverage for:

- readiness section layout children;
- readiness record cards;
- readiness condition/gate/rollback/outcome cards;
- readiness review cards;
- mobile wrapping for readiness lists, status badges, and detail rows.

## Boundaries Preserved

M43 preserves these boundaries:

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

- Browser-level layout QA was not claimed for M43 because no callable in-app
  browser DOM inspection tool was exposed in these turns.
- M43 remains synthetic-fixture-only. It does not ingest real user-provided
  files or chat archives.
- Readiness outcomes are planning and review labels only. They do not
  authorize persona mutation or memory writes.
- `ready_for_future_apply_design` means the draft shape can inform later
  design. It is not an apply-ready runtime state.
- The static fallback mirrors deterministic payloads by hand. Future larger
  payload families may need a more systematic fixture generation path.

## Gate Decision

`PASS_WITH_WARNINGS`

M43 is safe to use as evidence for the next local prototype milestone:
building a reviewed source-draft apply-plan preview before any actual
PersonaCard, PersonaVersionStore, memory, or runtime mutation.

M43 does not authorize real source extraction, automatic persona mutation,
platform delivery, outbound messaging, or media runtime.
