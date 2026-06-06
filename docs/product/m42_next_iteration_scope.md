# M42 Next Iteration Scope

## Scope

M42 should build a local proposal-to-persona-draft preview layer.

M41 made persona proposal candidates visible and reviewable. M42 should show
how a selected set of reviewed proposal candidates could become an inspectable
PersonaCard draft without writing PersonaCard, PersonaVersionStore, memory
stores, review stores, runtime stores, platform adapters, or outbound
messaging.

## Product Goal

Move one step closer to deep persona customization:

- take M41 proposal candidates as input;
- group selected proposals into a draft persona snapshot;
- show changed persona fields, unchanged fields, conflict notes, rollback refs,
  and reviewer gates;
- keep the output preview-only and manually reviewable.

This helps the companion demo show not only "what evidence suggests" and "what
proposal might change", but also "what the persona would look like if a
reviewer accepted the proposal set".

## Proposed T459-T464 Path

- T459: refine M42 scope and create the first implementation package.
- T460: add `source_proposal_persona_draft` adapter payload and contract tests.
- T461: render persona draft preview in the static web demo.
- T462: link persona draft records into Review Workspace.
- T463: harden responsive layouts and create the M42 milestone review task.
- T464: M42 milestone review.

## Required Boundaries

M42 must remain:

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

M42 must not:

- read `private/chat_history/`, `private/distilled/`, or private artifacts;
- ingest uploaded files;
- retain raw source content;
- infer traits from real records;
- call model providers;
- create embeddings or vector indexes;
- write PersonaCard, PersonaVersionStore, MemoryEventStore, review stores,
  runtime stores, queues, schedulers, or databases;
- automatically apply persona changes;
- send outbound messages;
- connect platform adapters;
- enable voice, avatar, camera, microphone, generated audio, generated image,
  or generated video;
- claim launch readiness, legal compliance, clinical validity, app-store
  approval, or user-study validation.

## Acceptance Direction

By the end of M42, reviewers should be able to inspect:

- a deterministic persona draft payload derived from M41 proposal candidates;
- a static UI section showing draft persona fields and unchanged fields;
- Review Workspace cards for draft field changes, conflicts, rollback refs,
  and review gates;
- tests proving preview-only, non-extracting, non-mutating behavior;
- a milestone review that clearly separates proposal preview, draft preview,
  and actual persona apply.

## T460 Implementation Slice

T460 should be payload-only. It should add a deterministic
`source_proposal_persona_draft` object to `TextFirstWebDemoState` and
`/demo-state.json`.

The payload should derive from existing M41 proposal candidates only, not from
private records, raw source files, providers, embeddings, or extraction.

It should include:

- `schema_version: m42.source_proposal_persona_draft.v1`;
- a reference to `m41.source_evidence_persona_proposal.v1`;
- draft title;
- base persona snapshot summary;
- selected proposal refs;
- draft field changes;
- unchanged field summaries;
- conflict notes;
- rollback refs;
- review gate results;
- draft outcome labels;
- preview-only apply policy;
- non-execution flags.

Expected initial draft field paths:

- `style.tone`;
- `style.pacing`;
- `style.humor`;
- `relationship.boundary_style`;
- `memory.use_preference`;
- `growth.short_term_hint`.

The payload must not:

- read sources;
- run extraction;
- call providers;
- create embeddings;
- write persona cards;
- write persona version store;
- write memory store;
- write review store;
- write runtime store;
- automatically apply;
- send messages;
- connect adapters;
- enable media runtime.
