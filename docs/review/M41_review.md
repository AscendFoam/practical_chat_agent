# M41 Milestone Review

Status: `PASS_WITH_WARNINGS`

Review date: 2026-06-02

## Scope Reviewed

M41 reviewed the local source-evidence-to-persona-proposal preview layer:

- T453: M41 scope refinement and T454 task package.
- T454: `source_evidence_persona_proposal` payload and contract tests.
- T455: static web demo rendering for proposal candidates.
- T456: Review Workspace linkage for proposal records.
- T457: responsive hardening for proposal UI and proposal review cards.

## Verdict

M41 passes as a deterministic, local, synthetic, preview-only bridge from M40
source evidence matrix records to reviewable persona proposal candidates.

The milestone proves that the demo can show:

- source evidence matrix linkage;
- proposal candidates for persona field paths;
- M40 trait hypothesis refs;
- M40 evidence row refs;
- confidence bands;
- rationale summaries;
- risk labels;
- rollback notes;
- review gate results;
- proposal outcome labels;
- static proposal UI;
- Review Workspace proposal cards;
- responsive wrapping for dense proposal ids and refs.

M41 does not prove real source extraction, private-source ingestion, model
provider inference, embeddings, PersonaCard mutation, memory writes, review
store writes, runtime writes, outbound messaging, platform adapters, or media
runtime.

## Evidence

Verification command:

```powershell
$env:PYTHONPATH='src'; pytest tests\test_source_evidence_persona_proposal_payload.py tests\test_static_source_evidence_persona_proposal.py tests\test_source_evidence_persona_proposal_review_linkage.py tests\test_source_evidence_persona_proposal_responsive_hardening.py tests\test_text_first_web_demo_local_server.py tests\test_text_first_web_demo_static.py tests\test_text_first_web_demo_state_switching.py -q -o cache_dir=artifacts\t458_pytest_cache --basetemp=artifacts\t458_pytest_basetemp
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

## What M41 Adds

### Payload

M41 adds `source_evidence_persona_proposal` to `TextFirstWebDemoState` and
`/demo-state.json`.

The payload includes:

- `schema_version: m41.source_evidence_persona_proposal.v1`;
- source evidence matrix ref;
- proposal candidates;
- risk labels;
- rollback notes;
- review gate results;
- proposal outcome labels;
- preview-only apply policy;
- strict non-execution flags.

Required proposal paths are covered:

- `style.tone`;
- `style.pacing`;
- `style.humor`;
- `relationship.boundary_style`;
- `memory.use_preference`;
- `growth.short_term_hint`.

### Static UI

M41 adds the `#source-evidence-persona-proposal` section to the static
text-first web demo. It renders proposal candidates, risk labels, rollback
notes, gates, outcomes, matrix linkage, and non-execution labels from embedded
state or JavaScript fallback state.

### Review Workspace

M41 adds `review_workspace.source_proposal_review_cards` and a `Proposal`
filter tab. Review cards cover:

- proposal candidates;
- proposal risk labels;
- rollback notes;
- proposal review gates;
- proposal outcome labels.

Each card remains review-required, preview-only, non-mutating, non-sending,
and runtime-not-ready.

## Boundaries Preserved

M41 preserves these boundaries:

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

- Browser-level layout QA was not claimed for T455-T457 because no callable
  in-app browser DOM inspection tool was exposed in the turn.
- M41 remains synthetic-fixture-only. It does not ingest real user-provided
  files or chat archives.
- M41 proposals are not applied to PersonaCard or runtime persona state.
- The current static fallback mirrors the deterministic payload by hand. Future
  larger payload families may need a more systematic fixture generation path.

## Gate Decision

`PASS_WITH_WARNINGS`

M41 is safe to use as evidence for the next local prototype milestone:
turning reviewed proposal candidates into an inspectable persona draft preview.

M41 does not authorize real source extraction, automatic persona mutation,
platform delivery, outbound messaging, or media runtime.
