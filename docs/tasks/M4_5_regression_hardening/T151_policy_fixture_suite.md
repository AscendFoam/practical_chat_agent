# Task T151: Policy Fixture Suite

## Task ID

T151

## Goal

Turn the T132/T133 inline and private synthetic policy scenarios into committed safe fixtures and tests.

T151 complements T150 by making the policy scenario set explicit, reviewable, and reusable across future template, LLM, or retrieval changes.

## Why Now

The updated design direction says to harden deterministic regression tests before any LLM-assisted planner, feedback-to-patch, RelationshipState, or platform work. T133 already identified false-positive and subtle false-negative probes; they need stable committed coverage.

## Inputs To Read

- `docs/review/M3_review.md`
- `docs/review/T133_review.md`
- `docs/review/T133_milestone_review.md`
- `docs/review/T150_review.md`
- T150 tests and fixtures
- `src/practical_chat_agent/services/policy.py`
- `src/practical_chat_agent/services/reply_planner.py`

## Allowed Files

- `tests/**`
- `examples/payloads/**` only for safe synthetic/redacted fixtures
- `pyproject.toml` if test config is required
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

## Forbidden Scope

- Do not copy private T133 artifacts into committed directories.
- Do not use private chat history.
- Do not call an LLM.
- Do not modify planner/policy behavior unless Captain explicitly opens a bug-fix task.
- Do not add platform integration, auto-send, DB, vector DB, or UI.

## Required Fixture Coverage

Create safe synthetic fixtures for:

- baseline friend
- practical colleague
- explicit sensitive boundary
- thin context
- false-positive policy probe
- subtle false-negative policy probe
- impersonation-risk probe if not already covered by T150
- over-proactivity probe

Also add explicit coverage for the following T150 follow-ups when useful:

- direct `ReplyPlanPolicyEngine` expectations, not only planner-through-policy coverage
- a clearer distinction between generic `thin_context` and a loaded-but-skill-missing or otherwise degraded store scenario
- `notes_on_candidate_differences` when policy state should cause it to be populated

Each fixture should avoid real names, raw chat text, real platform IDs, or private file paths.

## Verification

Run pytest over the policy fixture suite:

```powershell
$env:PYTHONPATH='src'
pytest tests
```

Expected checks:

- fixtures load in a clean environment
- each fixture produces the expected policy profile or risk flag pattern
- privacy-safe fixtures do not contain forbidden raw/private markers
- at least one test exercises policy behavior without relying only on `ReplyPlanner.generate()`

## Expected Handoff Update

Append a T151 implementation record to `docs/07_handoff.md` with:

- fixture list
- test command/result
- current known false-positive/false-negative limitations
- whether R037 can be narrowed or remains open

## Reviewer Focus

Reviewer type: adversarial.

Reviewer should verify:

- committed fixtures are truly synthetic/redacted
- false-positive and false-negative cases are not hand-waved
- direct policy-engine assertions are present where they improve auditability
- test expectations do not overclaim relationship-aware maturity
