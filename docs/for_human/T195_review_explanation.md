# T195 Review Explanation

## What T195 Is Trying to Do

T195 is the final task of Milestone 8 (M8). The M8 goal was to build a multi-dimensional relationship state system — instead of a single "like/dislike" score, track relationship on 8 dimensions (trust, warmth, boundary_risk, etc.), with human review of any changes.

The pipeline was:

```
T190: Schema (define the data structures)
T191: Signal extraction (extract relationship signals from feedback)
T192: Delta generation (propose relationship changes)
T193: Delta review CLI (let a human approve/reject changes)
T194: Compact context (make approved changes available to ChatContext)
T195: EVALUATION (do the approved changes actually affect how replies are generated?)
```

T195 is the final check: "We've wired all this relationship data into the system — does it actually make a difference in the replies?"

## What the Worker Found (and Where the Error Is)

The worker traced the data flow from the relationship context through the reply planner. They correctly identified several things:

1. The dimension-change values (`boundary_risk: 0.30→0.44`, etc.) exist in `ChatContext` but are **not read** by the reply planner or policy engine.
2. The `chat_context_summary` field carries relationship guidance text, but **no decision point uses it**.
3. Dimension-aware reply planning is **not implemented**.

However, the worker claimed that relationship context has an **indirect** effect: the notes added by T194 contain the word "relationship", and this allegedly matches a Chinese keyword "关系" (guanxi) in the policy engine's sensitive-topic list, triggering conservative mode.

**This is wrong.** The actual code check is a substring match: does the Chinese character "关系" appear in the note text? The notes are in English — "relationship_context source=...", "relationship_delta_count=N" — and Chinese "关系" is NOT a substring of English "relationship_context". They're completely different Unicode characters.

**The correct finding is: the T194 relationship context has ZERO behavioral impact on replies.** The data is present in `ChatContext` but completely inert. No code path consumes it.

### What This Means for M8

M8 achieved its structural goals:
- Relationship state can be represented on 8 dimensions ✓
- Signals can be extracted from feedback ✓
- Deltas can be proposed ✓
- Humans can review and approve deltas ✓
- Approved deltas enter ChatContext as compact briefs ✓

But the **behavioral link** — approved relationship deltas producing different, appropriate replies — was not implemented. The relationship context is structurally available but semantically unused by the reply planner.

This is not surprising for an evaluation-only task. T195 was designed to surface exactly this gap.

## Why My Verdict Is PASS_WITH_WARNINGS

**PASS**: The worker completed the evaluation, documented it, and did not modify any code. The task goal was met.

**WARNINGS**:
1. The central claim about keyword matching is factually wrong and needs correction.
2. The handoff document should be updated to reflect the correct finding (zero impact, not indirect impact).
3. The practical conclusion (dimension-aware consumption is absent) remains valid, but the error undermines trust in the analysis.

I chose not to BLOCK because:
- No code was modified (a BLOCK would be for code changes or scope violations)
- The overall verdict (dimension-aware planning is missing) is directionally correct
- The error can be fixed in documentation without redoing the evaluation

## What Should Happen Next

1. **Fix the handoff**: `docs/07_handoff.md` currently describes a keyword-match mechanism that doesn't exist. This should be corrected.

2. **Fix the milestone review**: `docs/review/T195_milestone_review.md` should remove the incorrect impact chain diagram that claims keyword matching.

3. **Post-M8 planning**: The gap is clear — relationship dimension data exists but is not consumed. If the project wants truly relationship-aware reply planning, the next milestone should add explicit consumption of `ChatContext.relationship_context.deltas` in the policy engine and reply planner.

### Why This Error Happened

The worker appears to have traced the code paths correctly but made an incorrect assumption about keyword matching. They saw that:
- Relationship notes contain "relationship_context" (English)
- The keyword list has "关系" (Chinese for "relationship")
- They assumed these match because "relationship" ≈ "关系" semantically

But `_contains_any` does substring matching, not semantic matching. The English "relationship_context" doesn't contain Chinese "关系". This is an easy mistake to make when working in a bilingual codebase and writing analysis in English — the reviewer's brain maps "relationship" → "关系" and assumes the code does too, but it doesn't.

### Relationship to the Broader Project

This project (see `docs/02_experiment_plan.md`) is building a "long-term relationship-aware chat agent" that can learn relationship dynamics from exported chat records. M8 was a key architectural milestone: defining relationship state in multiple dimensions rather than a single scalar. While the wiring is now in place, the actual "relationship-aware" reply behavior is still future work. The project has built the vocabulary (relationship dimensions) and grammar (delta lifecycle) but hasn't yet written sentences (dimension-aware replies).
