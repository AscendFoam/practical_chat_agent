# Task T195: Relationship-Aware Reply Eval

## Task ID

T195

## Goal

Evaluate whether the same inbound scenario produces appropriately different `ReplyPlan` behavior under different approved relationship-state contexts.

## Why Now

T194 is accepted with `PASS_WITH_WARNINGS`: the repo now exposes compact, approved relationship guidance to `ChatContext`, and the final M8 step is to evaluate whether that guidance changes reply behavior in the intended direction.

This is the next safe step because:

- it keeps the milestone evaluation-only
- it compares behavior rather than changing code
- it closes the M8 loop with evidence instead of new implementation

## Allowed Files

- `docs/review/T195_milestone_review.md`
- `docs/07_handoff.md`

## Forbidden Scope

- Do not modify code.
- Do not commit private artifacts.
- Do not add new runtime semantics or context wiring.

## Inputs To Respect

- Compare behavior under approved relationship contexts only.
- Keep the evaluation synthetic or otherwise already-approved for private use.
- Do not treat this as a state-application task.

## Expected Output

Produce:

- a milestone review that compares `ReplyPlan` behavior across approved relationship contexts
- a clear note on whether context changes are visible, conservative, and review-useful
- no code changes and no private artifact commits

## Review Focus

- Does approved relationship context meaningfully change reply behavior?
- Does the change remain review-only and conservative?
- Are the observed differences consistent with the M8 design?

## Reviewer Type

milestone
