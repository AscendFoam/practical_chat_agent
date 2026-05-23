# Task T180: LLM Candidate Generator Contract

## Task ID

T180

## Goal

Define the input/output contract for optional LLM-assisted reply candidate generation.

This task does not call an LLM and does not replace the template ReplyPlanner.

## Why Now

M6 has now closed with `Allow`. The next smallest safe step is to define the optional LLM candidate contract before introducing any model-calling path or hybrid planner behavior. This keeps M7 narrow and review-first.

## Read First

- `docs/04_task_board.md`
- `docs/03_architecture.md`
- `docs/06_eval_protocol.md`
- `docs/07_handoff.md`
- `docs/review/M6_review.md`
- `docs/reference/AI_coding_workflow.md`

## Inputs To Respect

- T180 is contract-only. No model call path is authorized in this task.
- The contract must preserve the existing T130 `ReplyPlan` and T123/T164/T174 compact-context boundaries.
- M7 must remain review-only and no-impersonation by default.
- Any future LLM-generated candidate must still be validatable, attributable, and rejectable without bypassing policy/boundary review.

## Allowed Files

- `docs/data_contracts/llm_candidate_generator_contract.md`
- `docs/07_handoff.md`

## Forbidden Scope

- Do not implement LLM calls.
- Do not modify current ReplyPlanner behavior.
- Do not add sending, platform integration, DB, vector DB, or UI.
- Do not change policy-engine rules, approved-store semantics, or context-assembly behavior.
- Do not claim that LLM candidates are enabled, production-ready, or quality-proven.

## Expected Output

Contract must require:

- `ReplyPlanCandidate` compatible output
- candidate type
- rationale
- supporting refs
- boundary reminders
- privacy/no-impersonation rules
- schema validation expectations
- failure / refusal shape
- deterministic validation boundary between "candidate generation" and "candidate acceptance"
- explicit statement that generated candidates remain review-only inputs

## Verification

- Contract is specific enough that T181 can implement an offline CLI without reopening core semantics.
- Contract does not require any repo code changes in this task.
- Handoff explicitly states what later M7 tasks may assume and what remains forbidden.

## Expected Handoff Update

Append a T180 implementation record to `docs/07_handoff.md` that captures:

- the candidate contract shape
- required safety / privacy / no-impersonation constraints
- what T181 may implement next
- what is still intentionally forbidden after T180

## Reviewer Type

normal

## Reviewer Focus

- Is the contract additive and narrow enough for a contract-only M7 opening?
- Does it preserve review-only mode, privacy boundaries, and no-impersonation constraints?
- Is it concrete enough that T181 can implement an offline CLI without reopening semantics?
