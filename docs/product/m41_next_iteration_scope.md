# M41 Next Iteration Scope

## Scope

M41 should build a local source-evidence-to-persona-proposal preview layer.

M40 made source evidence visible and reviewable. M41 should show how reviewed
synthetic evidence could become persona proposal candidates without performing
real extraction, reading private sources, retaining raw content, calling
providers, creating embeddings, mutating PersonaCard, writing stores, sending
messages, connecting adapters, or enabling media runtime.

## Product Goal

Bridge the gap between source evidence and persona editing:

- take M40 trait hypotheses as input;
- group them into reviewable persona proposal candidates;
- show proposed persona fields, confidence bands, rationale summaries, source
  evidence refs, risk labels, and rollback notes;
- keep the output preview-only and manually reviewable.

This moves the project closer to the user goal of deep persona customization
and consented distillation, while preserving the distinction between evidence
preview and real persona mutation.

## Proposed T453-T457 Path

- T453: refine M41 scope and create the first implementation package.
- T454: add `source_evidence_persona_proposal` adapter payload and contract
  tests.
- T455: render persona proposal preview in the static web demo.
- T456: link persona proposal cards into Review Workspace.
- T457: harden responsive layouts and create the M41 milestone review task.

## Required Boundaries

M41 must remain:

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

M41 must not:

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

By the end of M41, reviewers should be able to inspect:

- a deterministic proposal payload derived from M40 evidence summaries;
- a static UI section showing persona proposal candidates;
- Review Workspace cards for each proposal/risk/rollback item;
- tests proving preview-only, non-extracting, non-mutating behavior;
- a milestone review that clearly separates source evidence, persona proposal,
  and actual persona apply.

## T454 Implementation Slice

T454 should be payload-only. It should add a deterministic
`source_evidence_persona_proposal` object to `TextFirstWebDemoState` and
`/demo-state.json`.

The payload should derive from existing M40 matrix summaries only, not from
private records or raw source files. It should include:

- `schema_version: m41.source_evidence_persona_proposal.v1`;
- a reference to `m40.persona_source_evidence_matrix.v1`;
- proposal candidates grouped by persona field path;
- source trait hypothesis refs;
- supporting evidence refs;
- confidence band;
- rationale summary;
- risk labels;
- rollback notes;
- review gates;
- proposal outcome labels;
- preview-only apply policy;
- non-execution flags.

Expected initial proposal paths:

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
