# T133 Review: Holdout Eval (Milestone)

Reviewer: Claude Code (milestone review)
Date: 2026-05-16

## Scope

Files changed (committed):
- `docs/review/T133_milestone_review.md` (new)
- `docs/07_handoff.md` (section 29 appended)

Private artifacts produced (not committed):
- `private/distilled/t133_holdout_eval/contexts/H01-H06.context.json`
- `private/distilled/t133_holdout_eval/plans/H01-H06.reply_plan.json`
- `private/distilled/t133_holdout_eval/eval_summary.json`

No `src/**` files changed. Confirmed via `git diff --name-only -- src`.

## Task Completion Check

| Requirement | Status |
|---|---|
| Only docs/private outputs, no `src/**` changes | Met |
| No raw holdout text, real contact names, real platform IDs, or identifying private content in committed docs | Met (spot-checked H03 context/plan: all synthetic IDs like "holdout_sensitive", "Anon Contact", "????" redacted text) |
| Answer whether M3 scope is functionally complete | Met (yes: T130-T132 wiring + policy is structurally complete) |
| Assess whether ReplyPlanner runs in current environment | Met (6/6 plans generated successfully via `chat-reply-plan` CLI) |
| Distinguish inline synthetic verification from private eval from committed tests | Met (milestone review explicitly notes "只有私有 synthetic holdout，没有 committed regression tests") |
| Check for pseudo-completion (template baseline written as strong relationship-awareness) | Met (naturalness_rating = 3/5, explicitly states "整体还是模板驱动，关系感知偏浅") |
| Gate M3 verdict provided with executable conditions | Met (`Conditional` with 3 conditions) |
| Privacy leakage in committed diff | None found |

## Privacy Safety

- Committed diff contains no raw chat text, no real contact names, no real platform IDs, no real file paths.
- Private eval artifacts stay under `private/distilled/t133_holdout_eval/` with synthetic/anonymized content.
- Contexts use placeholder IDs ("holdout_sensitive", "Anon Contact", "holdout_colleague") and redacted text ("???????????????????").
- `eval_summary.json` uses anonymized notes only.

## Evaluation Quality Assessment

### Positive Findings

P01: **6-scenario coverage is well-designed.** The scenarios cover the critical axes: baseline friend (H01), practical colleague (H02), explicit sensitive boundary (H03), thin context (H04), false-positive probe (H05), false-negative probe (H06). This tests both happy paths and edge cases.

P02: **H03 plan correctly shows conservative behavior.** The spot-checked plan shows:
- Conservative draft templates ("你不用现在展开")
- `boundary_sensitive` risk flag on all candidates
- `over_proactive` flag on candidate 2 (optional follow-up)
- Confidence reduced from baseline 0.78/0.71/0.66 to 0.72/0.57/0.60
- Explicit boundary reminders about not pushing for disclosure

P03: **Honest ratings.** Naturalness 3/5, boundary adherence 4/5, evidence usage 3/5. These are not inflated. The worker correctly identifies that template-driven drafts limit naturalness.

P04: **False-positive/negative probes are valuable.** Including dedicated probes for policy over-sensitivity and under-detection is a methodological strength. The eval doesn't just test happy paths.

P05: **Gate M3 verdict is appropriately conservative.** `Conditional` rather than `Allow` is the correct call given the known limitations (template-driven, no committed tests, keyword-based policy).

P06: **Conditions are specific and executable.** The three conditions (keep review-only, T150 must add committed tests, recalibrate before claiming maturity) are actionable.

### Non-blocking Issues

N01: **Metrics are self-reported, not independently reproducible.** The ratings (3/5, 4/5, 3/5) are the worker's own assessment. There is no independent human rater or inter-rater agreement. For MVP milestone evaluation this is acceptable, but it should be noted as a limitation.

**Why non-blocking:** T133 is a docs-only eval task. The ratings serve as a structured self-assessment, not a statistical claim. The conditions explicitly defer further validation to T150.

N02: **Sample count is small (6).** All 6 are synthetic scenarios. No real holdout data from `private/chat_history/` was used (by design, since T133 is not allowed to read raw transcripts). This means the eval proves contract wiring and safety behavior, not real-world naturalness.

**Why non-blocking:** The task explicitly limits eval to "synthetic or redacted input." 6 scenarios covering the critical axes is reasonable for a milestone gate.

N03: **`naturalness_rating` of 3/5 is barely adequate.** A 3/5 suggests the drafts are "acceptable but not impressive." Combined with the template-driven nature, this means the planner produces safe but generic responses.

**Why non-blocking:** The milestone review correctly identifies this limitation and does not claim strong naturalness. The `Conditional` verdict and explicit condition 3 ("在更广的样本上重新校准") acknowledge this gap.

N04: **`evidence_usage_rating` of 3/5 is below the ideal.** This suggests the refs and rationales are present but not always informative. T131/T132 already acknowledged that `strategy_hints` and `relationship_summary` are consumed only for keyword detection, not for content generation.

**Why non-blocking:** The structural wiring for evidence refs is correct. The content quality limitation is already tracked. T133 does not falsely claim high evidence quality.

N05: **No mention of H01/H02 specific findings in the milestone review.** The review discusses H03-H06 but does not include anonymized findings for the baseline scenarios (H01 baseline friend, H02 practical colleague). These presumably passed without issues, but the absence is notable.

**Why non-blocking:** The `eval_summary.json` confirms all 6 scenarios produced valid plans. The milestone review focuses on the interesting findings (safety edge cases).

## Verdict

**PASS_WITH_WARNINGS**

T133 is a well-structured docs-only milestone evaluation. It uses 6 synthetic anonymized scenarios covering baseline, practical, sensitive, thin-context, false-positive, and false-negative cases. The eval correctly identifies that:
- T130-T132 wiring and safety behavior are structurally sound (6/6 valid plans, correct risk flags)
- Naturalness is limited by template-driven drafts (3/5)
- Policy false positives and false negatives exist
- No committed regression tests exist yet

The Gate M3 verdict of `Conditional` is appropriately conservative. The three conditions are specific and executable. No privacy leakage was found in committed artifacts. No code was modified.

## Warning Disposition (Captain action required)

- N01: **accepted** — self-reported ratings are acceptable for MVP milestone; T150 can add independent review.
- N02: **accepted** — 6 synthetic scenarios are reasonable given task constraints.
- N03: **accepted** — 3/5 naturalness is honestly reported; condition 3 addresses recalibration.
- N04: **accepted** — 3/5 evidence usage is honestly reported; structural wiring is correct.
- N05: **accepted** — baseline scenario findings omission is minor; summary data confirms success.

## Gate M3 Confirmation

The reviewer confirms the worker's Gate M3 verdict of **`Conditional`**.

M4/T140 may proceed only with the following conditions carried forward:
1. ReplyPlanner remains review-only. No auto-send, no realtime platform, no LLM drafting.
2. T150 must add committed regression tests covering structure, boundary sensitivity, thin context, false positives, and subtle false negatives.
3. "Relationship-aware maturity" must not be claimed until broader sample recalibration is done.
