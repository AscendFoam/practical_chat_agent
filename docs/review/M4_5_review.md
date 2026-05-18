# M4.5 Review: Regression Hardening

Reviewer: Codex Captain
Date: 2026-05-18
Scope: T150-T152, committed reproducibility for ReplyPlanner, direct policy behavior, and feedback CLI flow
Verdict: `Allow`

## 1. Is the current functionality really complete?

Yes, for the intended M4.5 scope.

M4.5 required the repo to turn previously reviewed M3/M4 behavior into committed, deterministic, privacy-safe regression coverage:

- T150 covers review-only `ReplyPlanner` structure, ranking, privacy, contact alignment, thin-context behavior, and documented false-positive / false-negative probes
- T151 covers direct `ReplyPlanPolicyEngine` profile-building and candidate-assessment behavior with synthetic fixtures
- T152 covers the T140-T142 feedback capture / validate / summarize loop, including privacy-safe stdout, corrupted-input surfacing, compact outputs, and non-mutation guarantees

All three tasks passed review. No blocking gap remains inside the stated M4.5 target.

## 2. Can it run from a clean environment?

Yes, sufficiently for this milestone gate.

Committed evidence now exists entirely inside the repository:

- `tests/test_reply_planner.py`
- `tests/test_policy_engine.py`
- `tests/test_feedback_cli.py`

Reviewer evidence in `docs/review/T150_review.md`, `docs/review/T151_review.md`, and `docs/review/T152_review.md` reports:

- `PYTHONPATH='src' pytest tests/`
- 176 passed

This is the first point where M3/M4 behavior is reproducible from committed repo contents alone rather than depending mainly on private/manual verification.

## 3. Is there testing, demo, or experimental evidence?

Yes.

Available evidence now includes:

- 176 committed deterministic tests across T150-T152
- synthetic fixtures only; no private chat content, real names, or private paths are committed
- direct CLI-path regression coverage for append / validate / summarize
- direct service-level coverage for corrupted inputs, privacy-safe outputs, and aggregate summaries

This is enough evidence for the M4.5 gate.

## 4. Is there any pseudo-completion?

No blocking pseudo-completion was found.

The hardening work is real:

- tests exercise real services and real CLI wiring
- privacy guarantees are asserted against actual outputs rather than only described in docs
- feedback remains record / validate / summarize only, with no hidden auto-learning shortcut
- no ContactSkill, MemoryFact, approved-store, or outbound mutation behavior was smuggled in

Some debt remains, but it is documented debt rather than fake completion.

## 5. Is the project allowed to enter the next milestone?

Yes, but only in the narrow M5 opening step.

The project may proceed to:

- `docs/tasks/M5_feedback_to_patch/T160_preference_patch_schema.md`

The project may not yet:

- auto-generate or apply patches without later task approval
- inject patches into runtime context before T164
- use LLMs unless a future task package explicitly allows it
- mutate ContactSkill, MemoryFact, or outbound behavior automatically

## Remaining Risks Carried Forward

- R035: relationship-aware quality is still template-driven
- R037: keyword-only policy limitations remain, though they are now well-instrumented
- R038: feedback must continue to be treated as review input, not automatic learning
- R043: service-level output-path confinement is still by warning/convention rather than hard enforcement
- R044: `reply_plan_id` coherence is not fully cross-checked against loaded plan context
- R045: validation `record_results` can still become verbose on large logs

## Required Next Task

Proceed to `docs/tasks/M5_feedback_to_patch/T160_preference_patch_schema.md`.
