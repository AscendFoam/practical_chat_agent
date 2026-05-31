# M33 Controlled Apply Executor Scope

Task: T406 Controlled Apply Executor Scope
Status: worker draft for review

## Objective

M33 begins the first narrowly scoped local apply executor after M31/M32
preview, eligibility, risk, and approval gates.

The milestone does not create an autonomous mutation engine. It creates
explicitly confirmed, local-only executors that can apply already-reviewed
synthetic/persona or memory plans to caller-supplied local stores, with audit
records and rollback references.

## Why This Milestone Is Next

M31 made manual apply previews inspectable. M32 added executor-risk records,
approval gates, and read-only risk UI. The next product gap is proving that
reviewed changes can be applied locally without bypassing:

- final human confirmation;
- fresh eligibility and risk decisions;
- source-version checks;
- rollback references;
- audit records;
- server-safe UI projection boundaries.

## Product Rationale

Human-like companion agents need controlled growth. If the persona or memory
never changes, the product feels static. If it changes without explicit gates,
it becomes untrustworthy. M33 introduces a small, auditable apply path for
local development so future companion behavior can evolve while preserving user
control.

## Scope Boundary

M33 may implement local executor code only when all of these are true:

- the input plan is synthetic or caller-supplied test data;
- a manual apply eligibility decision is `eligible`;
- an apply executor approval decision is
  `ready_for_separately_scoped_executor_design`;
- the source store version matches the plan;
- final human confirmation is supplied as an explicit value;
- an audit record and rollback reference are produced;
- no platform, provider, voice/avatar, media, scheduling, or outbound behavior
  is added.

M33 must not read `private/chat_history/`, call model providers, ingest real
chat logs, send messages, schedule outreach, connect to platforms, or create
automatic apply triggers.

## Implementation Sequence

### T407 Persona Growth Apply Executor

Implement a local-only executor for `PersonaGrowthDryRunPlan` that writes a new
version to `PersonaVersionStore` only after final confirmation and fresh
M31/M32 gate records. It should return an audit record with previous and new
version ids.

### T408 Memory Lifecycle Apply Executor

Implement a local-only executor for `MemoryLifecycleDryRunPlan` that updates a
caller-supplied `MemoryEventStore` only after final confirmation and fresh gate
records. It should produce audit and rollback evidence.

### T409 Apply Executor Audit Manifest

Create a shared audit manifest that can summarize persona and memory apply
events for review workspace display.

### T410 Apply Executor Review Panel

Expose local synthetic apply audit results in the review workspace as read-only
cards. It must not add apply buttons or platform controls.

### T411 M33 Milestone Review

Perform adversarial review before any future executor can be broadened beyond
local synthetic/caller-supplied stores.

## M33 Exit Criteria

M33 can close when:

- local persona growth apply is explicit, audited, and rollback-referenced;
- local memory lifecycle apply is explicit, audited, and rollback-referenced;
- no automatic apply path exists;
- no platform/provider/outbound/media behavior exists;
- review workspace can inspect apply audit results as read-only cards;
- residual risks are documented before any broader runtime mutation work.

## Residual Risks

- M33 still does not prove real-data import/de-identification quality.
- M33 still does not prove production-scale conflict resolution.
- M33 still does not authorize automatic mutation.
- M33 still does not authorize platform delivery or proactive sending.
