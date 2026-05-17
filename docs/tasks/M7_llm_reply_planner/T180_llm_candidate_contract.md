# Task T180: LLM Candidate Generator Contract

## Task ID

T180

## Goal

Define the input/output contract for optional LLM-assisted reply candidate generation.

This task does not call an LLM and does not replace the template ReplyPlanner.

## Allowed Files

- `docs/data_contracts/llm_candidate_generator_contract.md`
- `docs/07_handoff.md`

## Forbidden Scope

- Do not implement LLM calls.
- Do not modify current ReplyPlanner behavior.
- Do not add sending, platform integration, DB, vector DB, or UI.

## Expected Output

Contract must require:

- `ReplyPlanCandidate` compatible output
- candidate type
- rationale
- supporting refs
- boundary reminders
- privacy/no-impersonation rules
- schema validation expectations

## Reviewer Type

normal
