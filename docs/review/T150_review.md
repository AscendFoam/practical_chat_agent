# Review: T150

Verdict: PASS_WITH_WARNINGS

## Task Goal

Add committed deterministic regression tests for the M3 ReplyPlanner and policy layer, covering candidate structure, privacy leakage, contact alignment, ranking invariants, thin-context behavior, boundary/sensitive behavior, false-positive boundedness, false-negative documentation, not-configured store path, and non-approved record id isolation.

## Blocking Issues

None.

## Non-Blocking Issues

### N01: `TestNotConfiguredPath` reuses `thin_context` fixture

`TestNotConfiguredPath` (coverage area 9) uses the `thin_context` fixture, which is identical to the fixture used in `TestThinContext` (coverage area 3). Both test classes exercise the same `status="not_configured"` code path. The tests are not wrong — they verify different assertions — but they do not test a separate "missing store path" scenario distinct from "thin context". A fixture with `status="loaded"` but with a corrupted or empty store (e.g. `contact_skill=None` with `status="loaded"`) would provide more distinct coverage. Accepted as-is because the two classes still validate different invariants; the overlap is minor.

### N02: No direct `ReplyPlanPolicyEngine` unit tests

All 49 tests exercise `ReplyPlanner.generate()` as the entry point. The policy engine (`ReplyPlanPolicyEngine.build_profile`, `assess_candidate`) is tested only indirectly through the planner. This means policy-layer changes that do not surface in planner output (e.g. changing `confidence_penalty` values, adding new risk flags that the planner does not propagate) could regress silently. Accepted for T150 because the task package says "add committed deterministic tests for the M3 ReplyPlanner and policy layer" and the policy layer is exercised through the planner. T151 (policy fixture suite) can add dedicated policy engine unit tests.

### N03: `test_colleague_triggers_practical_tone` asserts on summary text

The test asserts `"practical" in summary_text` by checking `plan.policy_boundary_summary` joined text. This works because the current policy engine emits `"Keep the wording brief, practical, and low-drama."` when `practical_tone` is true. If the wording changes, the test breaks. The assertion is fragile but intentional — it encodes current expected behavior as a regression guard, which is the correct T150 posture.

### N04: `TestFalseNegativeProbe` asserts absence of flags rather than presence of a documented gap marker

The false-negative tests assert `boundary_sensitive not in all_flags` and `thin_context not in all_flags`. These assertions pass because current keyword detection misses the subtle pacing cue. If a future semantic classifier closes this gap, these tests will break — which is actually desirable as a regression signal. Accepted as-is; the docstrings clearly explain the current-limitation context.

### N05: `helpers.py` `_dedupe` not tested independently

The `helpers.py` module is thin and correct, but `context()`, `event()`, `memory()` etc. are never unit-tested in isolation. If a helper introduces a bug (e.g. wrong default value), it would surface as cryptic planner test failures rather than clear fixture failures. Low risk since helpers are simple constructors; not blocking.

### N06: No test for `notes_on_candidate_differences`

The `ReplyPlan.notes_on_candidate_differences` field is never asserted in any test. If this field regresses to empty or loses the conditional notes about thin/sensitive context, no test would catch it. This is a minor coverage gap; the field is informational and does not affect safety. Can be added in T151 if desired.

## Missing Tests

None beyond the non-blocking notes above. All 11 required coverage areas from the T150 task package have at least one committed test:

1. Baseline friend -> valid 3-candidate plan: `TestBaselineFriendContext` (7 tests)
2. Practical colleague -> valid 3-candidate plan: `TestColleagueContext` (4 tests)
3. Thin context -> `thin_context` risk + conservative confidence: `TestThinContext` (5 tests)
4. Sensitive/boundary -> boundary reminders + risk flags: `TestSensitiveContext` (4 tests)
5. False-positive boundedness: `TestFalsePositiveProbe` (4 tests)
6. False-negative documentation: `TestFalseNegativeProbe` (3 tests)
7. Privacy leakage: `TestPrivacyLeakage` (5 tests)
8. Contact_id mismatch: `TestContactIdMismatch` (2 tests)
9. Not_configured path: `TestNotConfiguredPath` (5 tests)
10. Priority_rank unique and stable: `TestPriorityRank` (4 tests)
11. Non-approved record id isolation: `TestNonApprovedRecordIdIsolation` (2 tests)

Minimum acceptance bar is met:
- `test_candidate_structure_regression_guard` fails on candidate structure regression
- `test_privacy_regression_guard` fails on privacy leakage
- `test_contact_alignment_regression_guard` fails on contact alignment regression
- `test_ranking_invariant_regression_guard` fails on ranking invariant regression

## Suspicious Implementation Details

### S01: Verified — tests call real `ReplyPlanner` and `ReplyPlanPolicyEngine`, no mocks

All tests instantiate `ReplyPlanner()` (with default `ReplyPlanPolicyEngine()`) and call `.generate(context=...)`. The planner runs its full deterministic pipeline: contact alignment validation, policy profile building, source context building, candidate generation, plan validation. No `unittest.mock`, no stubs, no hardcoded outputs. Fixtures construct real Pydantic model instances.

### S02: Verified — fixtures contain no private data

Grep for private paths, real names, and private markers confirms: all fixture content is synthetic domain-neutral text (`"synthetic inbound message"`, `"hey, how have you been?"`, etc.). The privacy probe uses invented markers (`abcdef9876`, `zyxwv6543`, `qprstu3210`, `xyzzy123`) that do not appear anywhere in `src/`.

### S03: Verified — no implementation files modified

`git diff HEAD` shows changes only in `tests/`, `pyproject.toml`, `docs/07_handoff.md`, and `docs/08_risks_and_open_questions.md`. The `.claude/settings.json` change is pre-existing and unrelated to T150. No `src/` files were touched.

### S04: Verified — `pyproject.toml` change is minimal and correct

Only `[tool.pytest.ini_options]` with `pythonpath = ["src"]` and `testpaths = ["tests"]` was added. No dependency changes, no build system changes.

## Verification

Ran: `PYTHONPATH='src' pytest tests -v`

Result: 49 passed in 0.07s, 0 failures.

No LLM calls, no network access, no private file reads. Tests are fully deterministic and reproducible from committed repo contents alone.

## Documentation Assessment

- `docs/07_handoff.md` section 44 accurately records files changed, fixture shape, test count, coverage mapping, and remaining risks.
- `docs/08_risks_and_open_questions.md` accurately updates risk states (R036/R034/R037/R046 narrowed, R035 remains active) and closes Q129.
- Q125-Q128 additions are factual record-keeping of prior T140-T142/M4 decisions.
- No document claims planned work as completed. R035 (naturalness) and R037 (keyword-only limitation) are honestly described as remaining open.

## Recommended Next Action

T150 is complete. Captain should:
1. Mark T150 as complete in `docs/04_task_board.md`.
2. Move Current Unique Task to T151 (policy fixture suite).
3. T151 should consider: dedicated `ReplyPlanPolicyEngine` unit tests (N02), `notes_on_candidate_differences` assertions (N06), and a `status="loaded"` + `contact_skill=None` fixture to separate thin-context from missing-store coverage (N01).
