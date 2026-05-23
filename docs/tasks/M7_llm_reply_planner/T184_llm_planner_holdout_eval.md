# Task T184: LLM Planner Holdout Eval

## Task ID

T184

## Goal

Evaluate template vs hybrid planner behavior against anonymized holdout scenarios and record whether the hybrid path improves or regresses review-only quality without compromising safety.

## Why Now

T183 is accepted with `PASS_WITH_WARNINGS`: the hybrid planner surface now exists, but quality evidence is still missing. The next safe step is evaluation, not more planner code.

This task should answer:

- does hybrid mode improve naturalness or evidence usage enough to justify the added complexity?
- does it preserve boundary adherence and privacy safety?
- is candidate diversity meaningfully better than template-only mode?

## Allowed Files

- `docs/review/T184_milestone_review.md`
- `docs/07_handoff.md`
- private holdout/eval outputs under `private/distilled/**`

## Forbidden Scope

- Do not modify planner code.
- Do not commit private artifacts or raw prompts/responses.
- Do not claim maturity without evidence.
- Do not read or emit raw private chat history in committed artifacts.
- Do not add new tests, fixtures, or code changes as part of this task.

## Inputs To Read

- `docs/review/T183_review.md`
- `docs/review/T133_milestone_review.md`
- `docs/06_eval_protocol.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`
- Any existing private smoke or holdout outputs under `private/distilled/**` relevant to T183/T133 style evaluation.

## Expected Output

Create `docs/review/T184_milestone_review.md` with:

- scope and anonymized input summary
- evaluation method
- concise results table or metric summary
- findings grouped by quality, safety, and testing gaps
- Gate M7 verdict for the holdout evaluation stage
- explicit recommendation for the next worker task, but do not execute it

Compare template vs hybrid mode on:

- naturalness
- evidence usage
- boundary adherence
- privacy safety
- candidate diversity
- stability of the merged rank order

## Verification

- Confirm the review document contains no raw private chat content.
- Confirm any private outputs stay under `private/distilled/**`.
- Confirm `docs/review/T184_milestone_review.md` exists.
- Inspect the new review file for privacy leakage before reporting completion.

## Reviewer Type

milestone
