# T212 Review Explanation

## What This Task Is About (In Plain Language)

In T211, the project built a rule engine that decides what proactive suggestions to create — things like "maybe check in with this friend" or "review the boundary-sensitive context first." But those suggestions were still skeletal: they had a title and a rationale, but no actual draft text that a human reviewer could read and evaluate.

T212 fills in that missing piece. It adds a "draft text generator" that takes each candidate action and attaches a short, review-only text snippet. Think of it like the difference between a form that says "Type: check-in suggestion" and one that actually shows you the suggested message: "Review-only draft: consider a brief, low-pressure check-in; keep it optional and non-committal."

The key constraint is that these drafts are **for human eyes only**. They are not messages to be sent, not conversation turns to be delivered, and not actions to be scheduled. They are review artifacts — text that helps a human reviewer understand what the system is proposing before they approve or reject it.

## What The Implementation Changed

### Code Changes

**New class added to `src/practical_chat_agent/services/behavior_planner.py`: `ProactiveDraftGenerator`**

This class has one public method: `enrich()`. It takes a `CandidateAction` (or a dictionary that can be validated into one) and returns a **new** `CandidateAction` with `payload.draft_text` populated.

The implementation is intentionally simple:

1. A static dictionary `_PROACTIVE_DRAFT_TEXTS` maps each of the six `BehaviorActionType` values to a short, deterministic draft text string.
2. The `enrich()` method looks up the draft text by action type and creates a new candidate with that text in the payload.
3. If the input is a mapping (dictionary) instead of a `CandidateAction` object, it is first validated through `CandidateAction.model_validate()`.

The six draft texts are:

- **`relationship_check_in_draft`**: "Review-only draft: consider a brief, low-pressure check-in; keep it optional and non-committal."
- **`reply_follow_up_draft`**: "Review-only draft: consider a concise, gentle follow-up that stays optional."
- **`topic_suggestion`**: "Review only: suggest a simple topic the user could raise if it feels natural."
- **`boundary_review_note`**: "Review only: check boundary-sensitive context before drafting any proactive wording."
- **`memory_review_prompt`**: "Review only: verify recent memory or relationship signals before deciding whether to reply."
- **`do_nothing`**: "Review only: no proactive action is recommended for now."

All drafts explicitly frame themselves as review-only. None attempt to be actual conversation messages.

**New tests added to `tests/test_behavior_rule_planner.py`**: 8 tests in class `TestProactiveDraftGenerator`

1. **`test_enriches_all_supported_candidate_types_with_draft_text`**: All six action types get draft text populated; all contain "review".
2. **`test_enrich_is_deterministic_for_same_input`**: Same input produces same draft text, action_id, action_type, and refs. Works for both object and mapping inputs.
3. **`test_enrich_preserves_candidate_invariants_and_payload_fields`**: After enrichment, all T210 safety invariants hold (human_review_required=True, auto_send_allowed=False, etc.), safe_summary is preserved, and no forbidden metadata appears.
4. **`test_enrich_does_not_echo_private_or_raw_text_from_input`**: If the input candidate contains private text in safe_summary or review_notes, the draft text does not echo it.
5. **`test_boundary_sensitive_candidates_stay_conservative`**: Boundary review notes mention "boundary-sensitive" and "proactive wording".
6. **`test_do_nothing_candidate_remains_review_only`**: Do-nothing produces the exact expected review-only text.
7. **`test_relationship_check_in_remains_low_pressure_and_non_committal`**: Check-in drafts contain "low-pressure", "optional", and "non-committal".
8. **`test_enrich_accepts_stable_mapping_inputs_without_private_text_fields`**: Mapping inputs work and the output has no raw_transcript attribute.

### What Was NOT Changed

- `src/practical_chat_agent/core/models.py` was not modified.
- `tests/test_behavior_schema.py` was not modified.
- The existing `BehaviorRulePlanner` class is completely unchanged.
- No existing models, services, CLI commands, or runtime behavior was modified.
- No message sending, scheduling, platform integration, or automation was added.
- No LLM calls, embeddings, vector databases, or external services were introduced.
- No memory, ContactSkill, relationship state, or approved store mutation occurred.

## Why This Matters For The Project

T212 is the bridge between **candidate proposal** and **candidate review** in M10 (BehaviorPlanner). The M10 roadmap shows:

- T210 (done): Define the data schemas
- T211 (done): Build the rule engine that generates candidates
- **T212 (this task)**: Add draft text to make candidates reviewable
- T213 (next): Build a review CLI so humans can approve/reject candidates
- T214: Safety evaluation

Without draft text, a human reviewer looking at a `CandidateAction` would see a structured record with fields like `action_type`, `rationale`, and `safe_summary`, but no concrete text to evaluate. T212 makes each candidate self-contained and inspectable — the reviewer can see exactly what wording is being proposed.

The design follows the project's established pattern of building in small, safe increments:
- The draft texts are deterministic (same input always produces the same output)
- They are explicitly review-only (every text mentions "review")
- They are conservative and non-committal (check-in texts emphasize "low-pressure" and "optional")
- They do not attempt to be engaging, persuasive, or conversational
- The generator does not call any LLM or external service

This is deliberately simpler than what a production proactive-messaging system would need. The current drafts are template-like review notes, not personalized conversation drafts. Future milestones could enhance draft quality through LLM-assisted generation, but only behind explicit gates and review controls.

## Why I Gave PASS

The task goal is fully met. The worker:

1. **Implemented the draft generator** with `ProactiveDraftGenerator.enrich()` that accepts both `CandidateAction` objects and stable mappings, populates `draft_text`, and returns a new immutable candidate.

2. **Preserved all T210/T211 safety invariants** on every enriched candidate through the immutable copy pattern. The enriched candidate has the same `human_review_required=True`, `auto_send_allowed=False`, `platform_execution_allowed=False`, `scheduler_allowed=False`, `platform_target=None` values.

3. **Provided adequate test coverage** (8 new tests, 48 total for T210+T211+T212) covering all 10 test categories from the task spec: draft text populated for all types, short and review-safe, deterministic, no raw text echoing, no send/schedule/platform fields, invariants intact, do_nothing safe, boundary conservative, memory-review safe, relationship check-in non-committal.

4. **Stayed within scope** — no forbidden activities (no sending, scheduling, platform integration, memory mutation, LLM calls, raw transcript access, models.py changes, or existing file modifications). The `BehaviorRulePlanner` class is completely untouched.

5. **Updated the contract document** with T212 scope, input/output shapes, draft safety constraints, and the T213/T214 boundary.

6. **Passed all verification**: compilation, 48 combined T210+T211+T212 tests, and a full test suite (770 tests passed, no regressions).

There are three minor test coverage gaps (M01-M03): no test for mapping input with pre-existing draft_text, no end-to-end pipeline test for `reply_follow_up_draft`/`topic_suggestion`, and no test for idempotent double-enrichment. These are non-blocking because the implementation is correct, simple, and deterministic, and the gaps can be closed in a later hardening slice.
