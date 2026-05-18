# T151 Review Explained: Policy Fixture Suite

## 1. What This Task Is About (In Plain Language)

Imagine you're building a smart reply assistant that helps you draft messages to your contacts. This assistant has a "policy engine" — a safety checker that looks at the conversation context and decides things like:

- "This conversation is about a sensitive topic — be extra careful with wording"
- "You don't know much about this contact yet — don't assume familiarity"
- "This reply draft is pushing too hard for a meeting — that's too proactive"
- "This draft is trying to predict what the other person would say — that's impersonating them"

Before T151, this policy engine was tested **indirectly** — only through the full reply planner. That's like testing a car's brakes by driving the whole car and checking if it stops, rather than testing the brake pads directly. T150 (the previous task) did this indirect testing well, but it had a limitation: if the policy engine had a bug that didn't affect the final planner output, nobody would notice.

T151 adds **direct tests** for the policy engine itself — 67 new tests that call the policy checker directly and verify each detection rule works correctly. Think of it like installing a diagnostic panel that tests each safety sensor individually, not just checking whether the alarm sounds at the end.

## 2. Implementation Details

### Goal

Turn policy behavior into an explicit committed fixture suite on top of T150. Add direct policy-layer assertions where planner-only coverage is too indirect. Keep all fixtures synthetic/redacted and keep the task non-mutating.

### What Changed

| File | Change |
|------|--------|
| `tests/conftest.py` | Added 3 new fixtures (`loaded_no_skill_context`, `degraded_store_context`, `over_proactivity_probe_context`). Fixed `baseline_friend_context` which inadvertently contained boundary cue keywords. |
| `tests/test_policy_engine.py` | New file: 67 direct policy engine tests in 16 test classes |
| `docs/07_handoff.md` | Added Section 47: T151 Implementation Record |
| `docs/08_risks_and_open_questions.md` | Added Captain Update 2026-05-18 (T151) documenting risk state changes and Q130 |

No planner or policy implementation files (`src/`) were modified.

### How the New Tests Work

The tests follow two patterns:

**Pattern 1: Direct `build_profile()` tests** (45 tests across 9 classes)

These construct a synthetic `ChatContext` and call `_engine.build_profile(context=...)` directly. The test then checks each field of the returned `ReplyPlanPolicyProfile`:

```python
def test_boundary_sensitive_is_true(self, sensitive_context):
    profile = _engine.build_profile(context=sensitive_context)
    assert profile.boundary_sensitive is True
```

This directly verifies that a context with emotional boundary cues triggers the `boundary_sensitive` flag. The T150 tests could only check this indirectly through the planner's output candidates.

**Pattern 2: Direct `assess_candidate()` tests** (20 tests across 5 classes)

These construct a `ReplyPlanPolicyProfile` manually and call `_engine.assess_candidate(policy_profile=..., candidate_text=..., approach_label=...)`:

```python
def test_call_always_over_proactive(self):
    neutral_profile = _profile()
    result = _engine.assess_candidate(
        policy_profile=neutral_profile,
        candidate_text="we should call to discuss this",
        approach_label="conservative_acknowledgment",
    )
    assert "over_proactive" in result.risk_flags
```

This directly verifies that action-pushing language ("call") always triggers over-proactive detection, regardless of the context.

**Pattern 3: Planner-through-policy integration tests** (2 tests)

A few tests still use the full `ReplyPlanner().generate()` to verify end-to-end behavior where policy affects the final plan output.

### Key Test Scenarios

- **Baseline friend**: Policy engine returns clean profile — no flags, no conservative mode, no sensitivity.
- **Colleague**: Activates `practical_tone=True` based on relationship type.
- **Thin context (not_configured)**: Triggers `thin_context=True`, `conservative_mode=True`, risk flag, and boundary summary.
- **Loaded but no skill**: Even though the store says "loaded", the absent skill brief still triggers `thin_context=True` — but does NOT add the "thin store context" note that `not_configured` would add. This is a subtle and important distinction.
- **Degraded store (store_path_missing)**: A non-loaded, non-not_configured status also triggers `thin_context=True`.
- **Sensitive/boundary**: Emotional intent + boundary cues trigger `boundary_sensitive=True`, `avoid_follow_up=True`, and `conservative_mode=True`.
- **False-positive probe**: "Money" in a work context triggers the sensitive keyword at the keyword level but does NOT escalate to `boundary_sensitive` because no boundary cues exist and intent is GENERAL.
- **False-negative probe**: Subtle pacing pressure ("you should really call me sometime soon") is not detected. This is documented as an accepted limitation.
- **Over-proactivity**: Skill boundary reminders with "do not push" and "low pressure" trigger both `boundary_sensitive` and `avoid_follow_up`, making over-proactive detection more sensitive.
- **Action push cues**: Words like "call", "meet", "打电话", "schedule" always trigger `over_proactive`, even in non-conservative mode.
- **No-pressure exemption**: Phrases like "no rush" and Chinese "先不往前推" exempt a candidate from `over_proactive` detection. But action push cues override the exemption.
- **Impersonation risk**: Phrases like "he would say", "she would say", "对方会" trigger `impersonation_risk` and add a boundary reminder.
- **Confidence penalty**: Thin context adds 0.10, boundary sensitivity adds 0.06, impersonation adds 0.15. A clean candidate gets 0.0.

### The Baseline Fixture Correction

An important discovery during T151 implementation: the original T150 `baseline_friend_context` fixture contained `"low pressure"` and `"do not push"` in its skill brief's strategy hints and boundary reminders. These are members of the policy engine's keyword lists (`_BOUNDARY_CUE_KEYWORDS` and `_AVOID_FOLLOW_UP_KEYWORDS`), meaning the "baseline" fixture was accidentally triggering `boundary_sensitive=True` and `conservative_mode=True` — making it not a clean baseline at all.

The T150 tests didn't catch this because they only checked the planner's final output structure (3 candidates, required fields, etc.) and didn't assert anything about the policy profile state. T151's direct `build_profile()` tests immediately exposed the problem because they explicitly assert `profile.boundary_sensitive is False` for the baseline fixture.

The fix was simple: change the strategy hints and boundary reminders to text that doesn't contain keyword matches (e.g., "keep warm" and "stay friendly and relaxed"). All 116 tests pass with the corrected fixture.

### Significance for Future Development

1. **Policy layer changes are now regression-guarded directly**: If someone modifies the keyword lists, confidence penalties, or detection logic in `policy.py`, the 67 direct tests will catch regressions immediately — even if the planner output doesn't change.

2. **T152 completes the M4.5 hardening trilogy**: T150 covered the planner surface, T151 covers the policy layer, and T152 will cover the feedback CLI. Once all three are done, M4.5 regression hardening is substantially complete.

3. **The loaded-no-skill distinction is now testable**: T150 had one non-blocking warning (N01) about overlapping `not_configured` and `thin_context` coverage. T151 cleanly separates these with dedicated fixtures and tests.

4. **`notes_on_candidate_differences` is now covered**: T150 warning N06 about this field never being asserted is now resolved by `TestNotesOnCandidateDifferences`.

### What's Still Not Covered

T151 tests the **policy detection wiring and safety surface** — does the policy engine correctly identify risks, apply penalties, and generate boundary reminders? It does NOT test:

- **Naturalness**: Whether conservative-mode drafts actually sound better (that's a human judgment)
- **Semantic detection**: Whether replacing keyword matching with semantic classification would improve false-positive/false-negative rates
- **Feedback CLI**: T152 will cover that separately
- **Full additive penalty combinations**: Thin + boundary + over_proactive + impersonation simultaneously

## 3. Why the Review Result Is PASS_WITH_WARNINGS

### Why PASS (not BLOCK)

The task fully meets its goal:

- All 8 required fixture coverage areas have committed tests.
- Direct policy engine tests are genuinely encoded — 65 of 67 T151 tests call `build_profile()` or `assess_candidate()` directly, not through the planner.
- All fixtures are synthetic — no real names, real messages, real platform IDs, or private paths.
- The `baseline_friend_context` fixture contamination was discovered and fixed.
- The loaded-no-skill vs not_configured thin-context distinction is now clearly tested.
- `notes_on_candidate_differences` is now asserted in 5 tests.
- No implementation files were modified — policy and planner behavior is unchanged.
- All 116 tests pass (49 T150 + 67 T151) in 0.16s.
- Documentation is honest about what was accomplished and what remains open.

### Why WITH_WARNINGS (not plain PASS)

Three non-blocking issues were noted:

1. **`_candidate_is_over_proactive` fallback branch not independently tested**: The final fallback at `policy.py:495` (when conservative mode is on, approach label is non-standard, and no no-pressure cues exist) is not tested in its positive case. Since it duplicates the `paced_next_step` branch logic, the gap is minor.

2. **Confidence penalty coverage is not fully additive**: The tests verify individual penalties and one pairwise combination (thin+boundary), but don't test triple or quadruple combinations. Since penalties are deterministic and additive, this is a minor coverage gap.

3. **The baseline fixture correction highlights a T150 limitation**: T150's planner-only tests couldn't detect that the baseline fixture was contaminated with boundary cue keywords. T151's direct policy tests caught it. This is a positive finding that validates T151's approach, but it means T150's coverage was weaker than it appeared.

None of these are serious enough to block. The core deliverable — 67 committed direct policy engine tests covering all major detection paths — is solid and materially reduces the remaining reproducibility risk for M4.5.
