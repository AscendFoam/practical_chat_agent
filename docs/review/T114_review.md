# T114 Review: M1 Milestone Sample Run

## Reviewer

Claude Code (milestone review, adversarial posture)

## Verdict

**PASS_WITH_WARNINGS**

Worker draft Gate M1 verdict of `Conditional` is **confirmed**.

## Scope Check

Worker modified only the 3 allowed files plus one new review document:

- `docs/review/T114_milestone_review.md` (new)
- `docs/07_handoff.md` (status update only)
- `docs/08_risks_and_open_questions.md` (risk/question update only)

No code files were modified. No `private/distilled/**` files were committed. No real names or chat excerpts entered docs.

## Independent Evidence Verification

I independently read the raw `normalized_events.jsonl` and cross-checked all 7 memory facts against their `evidence_refs`. Results:

| Fact | Claim vs Evidence | My assessment |
|---|---|---|
| `mem_010fed51a04f41c0` | "introduces self as: power" vs event text "我是power" | **PASS** — direct, literal match |
| `mem_118225641f834d7d` | Long study-background paraphrase vs one `type=7` mixed/forwarded event with 73 sub-records | **PASS_WITH_CAUTION** — supported but heavily compressed from a single forwarded blob |
| `mem_f09f04bda56d4e36` | "target school is Shanghai University of Technology" vs event text "目标院校上海理工大学" | **PASS** — direct match |
| `mem_5b038fa2fb4a49b1` | "estimated score 300-310, 320 unreachable" vs two events confirming both parts | **PASS** — two-event composite, well supported |
| `mem_56a52ebb66b54f91` | "fears not passing national line" vs event text "过不了国家线了" | **PASS** — direct match |
| `mem_b4731b7a6ce349ba` | "User offered tutoring support" vs event text "辅导的话，需要先了解下你的基础..." | **PASS_WITH_CAUTION** — the user *proposed* evaluating for tutoring, not yet *offered* it; slight overstatement |
| `mem_240b70cbad024a8e` | "User said they would review the materials first" vs event text "欧克欧克，我先看看[捂脸]" | **PASS_WITH_CAUTION** — "我先看看" (I'll take a look first) is casual and non-committal; the claim elevates it to a specific "review the materials first" intention |

### My verification agrees with worker's audit

- All 7 facts have at least one event-level `evidence_ref`. Confirmed.
- No fact relies only on chunk-level evidence. Confirmed.
- No fact has a missing evidence ref. Confirmed.
- Worker correctly identified the two caution items (`mem_118225641f834d7d` and `mem_240b70cbad024a8e`).
- I additionally flag `mem_b4731b7a6ce349ba` as slightly overstating the user's intent ("offered tutoring support" vs "asked for foundation info to evaluate tutoring possibility"). This is a minor semantic elevation, not a hallucination.

## Gate M1 Checklist Verification

Per `docs/06_eval_protocol.md` Gate M1:

| Requirement | Evidence | My check |
|---|---|---|
| Generate chunks for one selected contact | `chunks.jsonl` present | **PASS** |
| Chunk summaries output as JSON and traceable | `chunk_summaries.jsonl` with `chunk_id`, `event_ids`, `evidence_refs` | **PASS** |
| Memory facts all carry `evidence_refs` | 7/7 facts checked independently | **PASS** |
| ContactSkill candidate has review Markdown | Both `candidate.json` and `review.md` present | **PASS** |
| Human audit of at least 5 facts with evidence support | 7 facts audited by worker + 7 verified independently by reviewer | **PASS** |
| No private raw chat text enters submit-able directories | Only docs updated; no raw excerpts in diff | **PASS** |

All 6 Gate M1 hard requirements are met.

## T113 Warnings Follow-up

### W1: Heuristic generalization

**Still unproven.** The entire sample is a single 12-message exam-prep conversation with 1 contact. `_extract_topic`, `_CONCERN_TOKENS`, `_PRACTICAL_SUPPORT_TOKENS` all produce reasonable results here, but only because the sample perfectly matches these patterns. No evidence of generalization yet.

### W2: Confidence/closeness/trust numbers appear overly precise

**Confirmed.** The candidate JSON contains values like `0.77`, `0.82`, `0.62`, `0.61` — these are formulaic (`0.22 + min(len(facts), 6) * 0.08` style), not calibrated. The review artifact shows them with two decimal places, which may mislead human reviewers into treating them as measured values.

### W3: Topic extraction coverage is narrow

**Confirmed.** Only one preferred topic and three avoid topics were produced. The `_extract_topic` mapping returned results for 4-5 of the 7 facts, and returned `None` for the rest. This is expected given the narrow keyword list, but it means the ContactSkill is incomplete for any domain outside exam prep.

## Blocking Issues

None. All Gate M1 hard requirements are satisfied.

## Non-blocking Issues

### N01: `mem_b4731b7a6ce349ba` slightly overstates user intent

**Severity**: Low  
**Detail**: Claim says "User offered tutoring support" but the actual event is "辅导的话，需要先了解下你的基础..." — a conditional proposal to evaluate, not an offer of support. The LLM generated a reasonable but slightly elevated paraphrase.  
**Recommendation**: Acceptable as candidate-only. Flag for T114 human review. Not a blocking hallucination.

### N02: `mem_240b70cbad024a8e` elevates casual acknowledgment to specific intent

**Severity**: Low  
**Detail**: "我先看看[捂脸]" (casual "I'll take a look") becomes "User said they would review the materials first." The [捂脸] emoji and casual tone suggest non-commitment, but the fact presents it as a concrete plan.  
**Recommendation**: Acceptable as candidate-only. This is the kind of "compression" R030 was raised to track.

### N03: Sample is too small to justify any generalization claims

**Severity**: Low (structural, not worker error)  
**Detail**: 1 chunk, 12 events, 7 facts, 1 contact — this is a proof-of-concept, not a representative sample. The worker's `Conditional` verdict correctly reflects this.  
**Recommendation**: M2 should still proceed conditionally. Any larger-sample validation should happen before T130+.

### N04: `run_report.json` was not independently validated for consistency

**Severity**: Negligible  
**Detail**: Worker read the report but I did not verify that every field in `run_report.json` is consistent with the artifacts. The numbers cited in the milestone review (12 events, 1 chunk, 1 summary, 7 facts) match my independent reading.  
**Recommendation**: No action needed.

## Forbidden Scope Check

| Forbidden action | Status |
|---|---|
| Submit `private/distilled/**` | NOT present |
| Write real names to docs | NOT present |
| Modify code | NOT present |

## Warnings Classification

| ID | Classification | Rationale |
|---|---|---|
| N01 | Accepted | Minor semantic elevation in candidate-only fact; human reviewer can adjust |
| N02 | Accepted | Same class as R030; already tracked |
| N03 | Accepted | Structural limitation acknowledged by worker's `Conditional` verdict |
| N04 | Accepted | No inconsistency found; low priority |

## Gate M1 Verdict Confirmation

**`Conditional` — confirmed.**

The M1 artifact chain runs end-to-end on a real private sample. Evidence refs point to real events. ContactSkill is candidate-only with anti-impersonation boundaries. However:

- Heuristic generalization is unproven beyond this single exam-prep sample.
- Confidence/closeness/trust numbers are formulaic but presented with false precision.
- At least 2 of 7 facts show "short evidence -> polished paraphrase" compression.
- The sample size (1 contact, 12 events, 1 chunk) is too small to claim robustness.

M2 may proceed only in `Conditional` mode, carrying forward:
1. All T113 warnings (R028, R029) remain active.
2. R030 (paraphrase compression) is a new confirmed risk.
3. ContactSkill numeric values must be treated as reviewer-facing heuristics, not calibrated scores.
4. Candidate-only / human-review-first must remain until a broader sample validates the heuristics.

## Recommended Next Action

Proceed to T120 in `Conditional` mode. Captain should:
1. Update `04_task_board.md` to mark T114 complete and set T120 as current.
2. Preserve all M1 conditions in the M2 task descriptions.
3. Not collapse M1 into unconditional success in any governance document.
