# M32 Apply Executor Risk Scope

Task: T401 Apply Executor Risk Scope
Status: worker draft for review

## Objective

M32 defines non-executing risk assessment records and approval gates that must
exist before any future apply executor can be considered.

M32 does not implement an executor. It models risk, approval prerequisites,
rollback requirements, audit requirements, and final human confirmation for
future memory/persona mutation work.

## Why This Milestone Is Next

M31 closed with manual apply preview records, a non-mutating eligibility gate,
and read-only UI cards. The next high-risk boundary is not mutation itself; it
is proving that the project can represent executor risk and approval gates
without accidentally creating an executor.

## Product Rationale

Human-like companions eventually need controlled memory/persona evolution, but
unsafe mutation can damage trust. An executor-risk layer gives reviewers a
clear record of:

- what could change;
- why the change is risky;
- which approvals are required;
- how rollback or cache/index invalidation would be handled;
- what evidence must exist before execution can be separately scoped.

## Non-Executing Boundary

M32 records must preserve:

- `review_required=true`
- `risk_assessment_only=true`
- `executor_ready=false`
- `applies_changes=false`
- `writes_memory_store=false`
- `writes_persona_version=false`
- `runtime_ready=false`

No M32 task may implement memory store writes, PersonaCard mutation,
PersonaVersionStore writes, deletion execution, retrieval index mutation,
provider calls, outbound messaging, or platform/media behavior.

## Implementation Sequence

### T402 Apply Executor Risk Records

Create Pydantic records for executor risk assessment: risk factors,
approval gates, rollback requirements, audit requirements, and final
recommendation. Records must be non-executing and test-covered.

### T403 Apply Executor Approval Gate

Create a deterministic non-executing gate that evaluates risk records and
manual apply eligibility decisions, returning blocked, needs_review, or
ready_for_separately_scoped_executor_design. It must not execute anything.

### T404 Apply Risk Review Panel

Expose risk records in local review workspace UI as read-only risk cards.

### T405 M32 Milestone Review

Perform adversarial review before any future mutation-executor design.

## M32 Exit Criteria

M32 can close when:

- non-executing risk records exist and are test-covered;
- approval gate exists and is non-executing;
- local UI can inspect risk records as read-only cards;
- forbidden private/provider/outbound/media/mutation fields are absent;
- residual risks are documented before any future executor milestone.

## Residual Risks

- M32 still does not mutate memory/persona state.
- M32 still does not prove real-data import/de-identification quality.
- M32 still does not prove user trust for real apply flows.
- Any future executor remains high-risk and must be separately scoped.
