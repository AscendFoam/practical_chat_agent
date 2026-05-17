# Task T161: Feedback Clusterer

## Task ID

T161

## Goal

Implement a deterministic, review-only feedback clusterer that groups similar T140 feedback records into safe clusters for later patch proposal.

## Why Now

One edit/reject should not directly update long-term communication policy. Clustering creates a conservative intermediate step: repeated similar feedback can become a candidate for review.

## Allowed Files

- `src/practical_chat_agent/services/feedback.py`
- `src/practical_chat_agent/app/main.py`
- `docs/07_handoff.md`

## Forbidden Scope

- Do not generate `PreferencePatchCandidate` yet.
- Do not call an LLM.
- Do not modify ContactSkill, MemoryFact, approved store records, or planner templates.
- Do not auto-approve or apply anything.
- Do not read private chat history.

## Expected Output

Support rule-based cluster labels such as:

- `too_long`
- `too_cold`
- `too_eager`
- `too_formal`
- `too_intimate`
- `boundary_violation`
- `not_like_me`
- `good_tone`

CLI should emit safe aggregate clusters only, not full notes or edited text.

## Verification

- Run on synthetic feedback log.
- Confirm repeated reason tags/actions form stable clusters.
- Confirm stdout does not leak full draft/edit/note text.

## Reviewer Type

adversarial
