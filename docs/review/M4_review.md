# M4 Review: Feedback Capture

Reviewer: Codex Captain
Date: 2026-05-17
Scope: T140-T142, review-only feedback record / validate / summarize flow
Verdict: `Conditional`

## 1. Is the current functionality really complete?

Yes, for the intended M4 scope.

M4 required a review-only feedback loop over `ReplyPlan` candidates:

- T140 records accept/edit/reject/boundary feedback into a private log
- T141 validates that log read-only and surfaces malformed references or malformed actions safely
- T142 exports aggregate summaries without exposing private text or mutating downstream state

All three tasks have now passed review. No blocking issue indicates missing core functionality inside this milestone's intended scope.

## 2. Can it run from a clean environment?

Not yet proven.

The implementation exists and private/manual verification was substantial, but committed reproducibility is still incomplete:

- no committed regression suite yet proves M3/M4 behavior end to end
- no committed synthetic fixture set yet demonstrates the planner/policy/feedback paths from repo contents alone
- current evidence still depends too much on private/manual verification

This is the main reason the milestone stays `Conditional`.

## 3. Is there testing, demo, or experimental evidence?

Yes, but it is uneven.

Available evidence:

- T140/T141/T142 each include concrete implementation records and manual verification notes
- T142 supports both stdout summary and optional JSON export
- reviewer checks confirmed privacy-safe, read-only behavior for the M4 tasks

Missing evidence:

- committed automated regression tests
- committed synthetic fixtures for the M4 feedback flow
- a clean-environment command path that reproduces the M3/M4 guarantees from public repo contents alone

## 4. Is there any pseudo-completion?

No blocking pseudo-completion was found.

The functionality is real:

- feedback is actually written, not mocked
- validation actually parses and checks records and referenced plans
- summary export actually aggregates counts and optional validation totals
- privacy protections are implemented in the actual output path, not only described in docs
- no hidden mutation, no auto-send, no realtime integration, and no feedback-to-learning shortcut was introduced

There is technical debt and missing reproducibility, but not fake completion.

## 5. Is the project allowed to enter the next milestone?

Not M5.

The project may proceed only to M4.5 regression hardening:

- allowed next task: `docs/tasks/M4_5_regression_hardening/T150_replyplanner_regression_tests.md`
- required follow-ups after that: T151 and T152

M5 feedback-to-patch remains blocked until committed regression coverage proves the current M3/M4 safety contract in a clean environment.

## Required Next Task

Proceed to `docs/tasks/M4_5_regression_hardening/T150_replyplanner_regression_tests.md`.
