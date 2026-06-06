# M43 Next Iteration Scope

## Scope

M43 should build a local persona-draft apply-readiness preview layer.

M42 made a proposal-linked persona draft visible and reviewable. M43 should
show how that draft would be assessed before any future apply design, without
writing PersonaCard, PersonaVersionStore, memory stores, review stores,
runtime stores, platform adapters, or outbound messaging.

## Product Goal

Move one step closer to controlled deep persona customization:

- take M42 draft field changes as input;
- evaluate draft fields against manual review, conflict, rollback, and policy
  gates;
- produce apply-readiness records that explain why a field is blocked,
  needs review, or can inform a future separately scoped apply design;
- keep the output preview-only and manually reviewable.

This helps the companion demo show not only "what the persona draft would look
like", but also "what must be checked before any reviewed apply executor could
touch persona state".

## Proposed T465-T470 Path

- T465: refine M43 scope and create the first implementation package.
- T466: add `source_draft_apply_readiness` adapter payload and contract tests.
- T467: render apply-readiness preview in the static web demo.
- T468: link apply-readiness records into Review Workspace.
- T469: harden responsive layouts and create the M43 milestone review task.
- T470: M43 milestone review.

## Required Boundaries

M43 must remain:

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

M43 must not:

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

By the end of M43, reviewers should be able to inspect:

- deterministic apply-readiness records derived from M42 draft field changes;
- per-field readiness outcomes such as `blocked`, `needs_manual_review`, and
  `ready_for_future_apply_design`;
- references to draft change ids, conflict note ids, rollback refs, and review
  gates;
- static UI showing readiness reasons and blocked conditions;
- Review Workspace cards for readiness records;
- tests proving preview-only, non-mutating behavior;
- a milestone review that clearly separates draft preview, apply-readiness
  preview, and actual persona apply.

## T466 Implementation Slice

T466 should be payload-only. It should add a deterministic
`source_draft_apply_readiness` object to `TextFirstWebDemoState` and
`/demo-state.json`.

The payload should derive from existing M42 draft fields only, not from private
records, raw source files, providers, embeddings, or extraction.

It should include:

- `schema_version: m43.source_draft_apply_readiness.v1`;
- a reference to `m42.source_proposal_persona_draft.v1`;
- readiness title;
- evaluated draft change ids;
- per-field readiness records;
- blocked condition records;
- required review gate refs;
- rollback dependency refs;
- readiness outcome labels;
- preview-only apply policy;
- non-execution flags.

Initial per-field readiness outcomes should cover:

- `blocked`: fields that cannot proceed because policy, anti-deception, or
  memory-write constraints remain unresolved;
- `needs_manual_review`: fields that are inspectable but still require human
  judgment because conflicts or uncertainty remain;
- `ready_for_future_apply_design`: fields whose shape may inform a later
  separately scoped apply executor, without authorizing mutation in M43.

T466 should derive readiness only from M42 draft ids, conflict ids, rollback
refs, and review gates. It should not read or infer from raw source content.

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
