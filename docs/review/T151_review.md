# Review: T151

Verdict: PASS_WITH_WARNINGS

## Task Goal

Turn T132/T133 inline and private synthetic policy scenarios into committed safe fixtures and tests. Complement T150 by adding direct `ReplyPlanPolicyEngine` unit tests, separating loaded-but-no-skill from generic thin-context coverage, and asserting `notes_on_candidate_differences` when policy state should populate them.

## Blocking Issues

None.

## Non-Blocking Issues

### N01: `_candidate_is_over_proactive` final fallback branch not independently tested

The method at `policy.py:495` returns `self._contains_any([candidate_text], self._OVER_PROACTIVE_DRAFT_CUES)` when `conservative_mode` is True, `approach_label` is neither `"optional_follow_up"` nor `"paced_next_step"`, and the candidate text has no no-pressure cues. The positive case (proactive cues present in this branch) is not tested directly — only the negative case (`TestAssessCandidateOverProactiveConservativeMode::test_conservative_acknowledgment_safe_without_cues`). Since this branch duplicates the `"paced_next_step"` branch logic, the functional gap is minor. The planner integration test may exercise it indirectly through generated candidates.

### N02: Confidence penalty coverage is not fully additive

`TestAssessCandidateConfidencePenalty` verifies individual penalties (thin 0.10, boundary 0.06, impersonation 0.15, clean 0.0) and one pairwise combination (thin+boundary >= 0.16). The over_proactive penalty (+0.08 from `assess_candidate`) is not independently tested for its penalty contribution, and the triple/quadruple combinations are not tested. Since all penalties are deterministic and additive, this is a minor coverage gap. A future refactor that changes penalty values or adds conditional interactions would benefit from fuller combination tests.

### N03: `baseline_friend_context` fixture correction highlights a T150 limitation

The original T150 `baseline_friend_context` contained `"low pressure"` and `"do not push"` in `strategy_hints` and `boundary_reminders`, which are members of `_BOUNDARY_CUE_KEYWORDS` and `_AVOID_FOLLOW_UP_KEYWORDS`. This meant the "baseline" fixture was not actually a clean baseline — it triggered `boundary_sensitive=True` and `conservative_mode=True`. The T150 tests did not catch this because they only asserted planner output structure, not policy profile state. T151's direct `build_profile()` tests exposed the contamination, and the worker corrected the fixture. This is a positive finding — it demonstrates the value of direct policy engine tests over planner-only tests. Not blocking; noted for the record.

## Missing Tests

None beyond the non-blocking notes above. All 8 required fixture coverage areas from the T151 task package have committed tests:

1. Baseline friend -> `TestBuildProfileBaselineFriend` (6 tests)
2. Practical colleague -> `TestBuildProfileColleague` (5 tests)
3. Explicit sensitive boundary -> `TestBuildProfileSensitive` (5 tests)
4. Thin context -> `TestBuildProfileThinContext` (5 tests)
5. False-positive policy probe -> `TestBuildProfileFalsePositive` (4 tests)
6. Subtle false-negative probe -> `TestBuildProfileFalseNegative` (3 tests)
7. Impersonation-risk probe -> `TestAssessCandidateImpersonationRisk` (5 tests)
8. Over-proactivity probe -> `TestBuildProfileOverProactivity` (4 tests) + `TestOverProactivityPlannerIntegration` (2 tests)

T150 follow-ups also covered:

- Loaded-but-skill-missing -> `TestBuildProfileLoadedNoSkill` (4 tests)
- Degraded store (store_path_missing) -> `TestBuildProfileDegradedStore` (4 tests)
- notes_on_candidate_differences -> `TestNotesOnCandidateDifferences` (5 tests)
- Direct assess_candidate coverage -> `TestAssessCandidateActionPush` (4) + `TestAssessCandidateOverProactiveConservativeMode` (3) + `TestAssessCandidateNoPressureExemption` (3) + `TestAssessCandidateConfidencePenalty` (5)

Minimum acceptance bar is met:
- At least one test exercises policy behavior without relying only on `ReplyPlanner.generate()`: 65 of 67 T151 tests call `_engine.build_profile()` or `_engine.assess_candidate()` directly.
- Direct policy engine assertions are present for all major detection paths.
- Fixtures are truly synthetic/redacted.

## Suspicious Implementation Details

### S01: Verified — tests call real `ReplyPlanPolicyEngine` methods directly

All `TestBuildProfile*` tests instantiate `ReplyPlanPolicyEngine()` via module-level `_engine` and call `_engine.build_profile(context=...)` with real `ChatContext` fixtures. All `TestAssessCandidate*` tests call `_engine.assess_candidate(policy_profile=..., candidate_text=..., approach_label=...)` with real `ReplyPlanPolicyProfile` objects. No mocks, no stubs, no hardcoded outputs. The engine is stateless (no `__init__` parameters, no mutable state), so the module-level singleton is safe.

### S02: Verified — fixtures contain no private data

All fixture content is synthetic domain-neutral text. The loaded_no_skill_context, degraded_store_context, and over_proactivity_probe_context follow the same pattern as T150 fixtures. No private paths, real names, real platform IDs, or real chat content.

### S03: Verified — no implementation files modified

`git diff HEAD -- src/` shows no changes. The diff is limited to `tests/conftest.py`, `tests/test_policy_engine.py` (new), `docs/07_handoff.md`, and `docs/08_risks_and_open_questions.md`. The `.claude/settings.json` change is pre-existing and unrelated to T151.

### S04: Verified — `baseline_friend_context` fix is correct and backward-compatible

The old fixture had `strategy_hints=["keep warm but low pressure"]` and `boundary_reminders=["do not push for details"]`. Both "low pressure" and "do not push" are in `_BOUNDARY_CUE_KEYWORDS` and `_AVOID_FOLLOW_UP_KEYWORDS`, contaminating the baseline. The fix changed them to `["keep warm"]` and `["stay friendly and relaxed"]` respectively, which contain no keyword matches. All 116 tests (49 T150 + 67 T151) pass with the corrected fixture, confirming backward compatibility.

### S05: Verified — `loaded_no_skill_context` correctly separates from `thin_context`

The `loaded_no_skill_context` has `status="loaded"` and `contact_skill=None`. In `build_profile`, `thin_context = (status != "loaded") or (contact_skill is None)` evaluates to `(False) or (True) = True`. The `test_loaded_no_skill_conservative_without_thin_note` correctly asserts that the "Approved store context is thin" note is NOT appended (because `status != "loaded"` is False), even though `conservative_mode` is True. This precisely distinguishes loaded-but-no-skill from not_configured thin context.

## Verification

Ran: `PYTHONPATH='src' pytest tests -v`

Result: 116 passed in 0.16s (49 T150 + 67 T151), 0 failures.

No LLM calls, no network access, no private file reads. Tests are fully deterministic and reproducible from committed repo contents alone.

## Documentation Assessment

- `docs/07_handoff.md` section 47 accurately records: files changed, fixture corrections, test count, coverage mapping to T151 requirements, and remaining risks.
- `docs/08_risks_and_open_questions.md` accurately updates risk states (R036 further narrowed, R037 further documented, R046 further narrowed, R035 remains active) and closes Q130.
- The `baseline_friend_context` fixture correction is honestly documented as a fixture fix rather than a behavior change.
- No document claims planned work as completed. R035 and R037 are honestly described as remaining open.

## Recommended Next Action

T151 is complete. Captain should:

1. Mark T151 as complete in `docs/04_task_board.md`.
2. Move Current Unique Task to T152 (feedback CLI regression tests).
3. T152 should cover: T140 feedback log recording, T141 feedback log validation, T142 feedback summary export. When T152 is done, R046 can be narrowed further and M4.5 will be substantially complete.
