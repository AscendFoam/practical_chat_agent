# M44 Next Iteration Scope

## Scope

M44 should build a local reviewed source-draft apply-plan preview layer.

M43 showed how a source-proposal-linked persona draft would be assessed before
any future apply design. M44 should show how readiness records could be
converted into a manual, reviewable apply plan without executing the plan or
writing PersonaCard, PersonaVersionStore, memory stores, review stores,
runtime stores, platform adapters, or outbound messaging.

## Product Goal

Move one step closer to controlled deep persona customization:

- take M43 readiness records as input;
- group eligible, blocked, and review-required draft fields into a plan
  preview;
- show what would be included, deferred, blocked, and rolled back before any
  future apply executor;
- expose reviewer-facing plan cards in Review Workspace;
- keep the plan preview-only, manually reviewable, and non-mutating.

This helps the companion demo show not only "what must be checked before
apply", but also "how a reviewer would structure a safe apply plan if future
executor work were separately approved".

## Proposed T471-T476 Path

- T471: refine M44 scope and create the first implementation package.
- T472: add `source_draft_apply_plan_preview` adapter payload and contract
  tests.
- T473: render apply-plan preview in the static web demo.
- T474: link apply-plan records into Review Workspace.
- T475: harden responsive layouts and create the M44 milestone review task.
- T476: M44 milestone review.

## Required Boundaries

M44 must remain:

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

M44 must not:

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

By the end of M44, reviewers should be able to inspect:

- deterministic apply-plan preview records derived from M43 readiness records;
- included field changes that may inform future separately scoped apply work;
- deferred field changes that still need manual review;
- blocked field changes and blocking conditions;
- rollback dependency summaries;
- manual approval gates;
- static UI showing plan structure and non-execution flags;
- Review Workspace cards for apply-plan records;
- tests proving preview-only, non-mutating behavior;
- a milestone review that clearly separates readiness preview, apply-plan
  preview, and actual persona apply.

## T472 Implementation Slice

T472 should be payload-only. It should add a deterministic
`source_draft_apply_plan_preview` object to `TextFirstWebDemoState` and
`/demo-state.json`.

The payload should derive from existing M43 readiness records only, not from
private records, raw source files, providers, embeddings, or extraction.

It should include:

- `schema_version: m44.source_draft_apply_plan_preview.v1`;
- a reference to `m43.source_draft_apply_readiness.v1`;
- plan title;
- plan status summary;
- included field plan items;
- deferred field plan items;
- blocked field plan items;
- manual approval gate refs;
- rollback plan refs;
- plan outcome labels;
- preview-only apply policy;
- non-execution flags.

Initial plan outcomes should cover:

- `included_for_future_plan_design`: a field can inform later plan design but
  is not applied;
- `deferred_for_manual_review`: a field remains inspectable but needs reviewer
  judgment;
- `blocked_before_apply_plan`: a field cannot enter the plan because blocking
  conditions remain unresolved.

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
