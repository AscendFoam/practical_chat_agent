# T213 Review Explanation

## 1. What This Task Is About (In Plain Language)

In T211, the project built a rule engine that generates proactive behavior suggestions — things like "maybe check in with this friend" or "review the boundary-sensitive context first." In T212, those suggestions got enriched with short draft text so a human can read what the suggestion actually says.

But nobody has reviewed those suggestions yet. They are still in a "pending_human_review" state. This is a problem because:

- Nobody has decided whether the suggestion is actually a good idea.
- Nobody has explicitly said "yes, this is fine" or "no, this is wrong."
- The system has no record of *who* reviewed what, *when*, or *why*.

T213 fixes this by adding a **manual review workflow**: a human can now look at a candidate action and mark it as **approved**, **rejected**, **frozen** (pause it for later), or **archived** (set it aside permanently). Every review decision is recorded with the reviewer's identity, a timestamp, and an optional note.

Critically: **approval does not mean "go ahead and send it."** It just means "a human looked at this and decided it's acceptable for further consideration." The candidate action remains non-sendable, non-schedulable, and non-executable. Real sending stays behind a future OutboundSendGate milestone that hasn't been built yet.

## 2. Implementation Details

### 2.1 Task Goal

Add a manual review service and CLI command for `CandidateAction` records. The service should:

- Accept a candidate action and a review decision (approve/reject/freeze/archive).
- Record who reviewed it, when, and optionally why.
- Return a *new* reviewed object without modifying the original.
- Preserve all safety invariants (no auto-send, no platform execution, no scheduler).

### 2.2 Code Changes

#### `src/practical_chat_agent/services/behavior_planner.py`

Two new classes were added:

1. **`CandidateActionReviewError`** — a custom `ValueError` subclass for invalid review operations.

2. **`CandidateActionReviewService`** — the core review service with one public method:
   - `review_candidate(candidate, decision, reviewer_id, note=None)` — validates the decision, deep-copies the candidate, applies the review metadata, and returns the new object.

   The service uses `model_copy(deep=True)` to ensure the original candidate is never mutated. It normalizes the decision string (strip + lowercase), validates it against a closed set of four options, and enforces a non-empty reviewer ID.

   The `_apply_decision` method updates:
   - `status` → the normalized status (approved/rejected/frozen/archived)
   - `review_metadata.review_state` → "reviewed"
   - `review_metadata.reviewed_by_human` → True
   - `review_metadata.last_decision` → the status
   - `review_metadata.last_reviewed_at` → current UTC timestamp
   - `review_metadata.last_reviewer_id` → the reviewer
   - `review_metadata.history` → appends a new `DistilledArtifactReviewDecision`
   - `review_metadata.decision_notes` → appends the note if provided
   - `updated_at` → current UTC timestamp

   It does **not** touch `payload`, `action_type`, `supporting_context_refs`, `risk_flags`, `policy`, or any of the no-send/no-platform/no-scheduler invariant fields.

#### `src/practical_chat_agent/app/main.py`

A new CLI command `chat-behavior-review-action` was added. It:

- Reads a JSON file containing one `CandidateAction`.
- Validates it with `CandidateAction.model_validate_json()`.
- Applies the review decision via `CandidateActionReviewService`.
- Writes the reviewed candidate JSON to a file (defaults to overwriting the input).
- Prints only safe metadata to stdout (action_id, contact_id, action_type, status, review_state, reviewer, history_count, file paths) — **never** the full draft text.

#### `tests/test_behavior_rule_planner.py`

Added `TestCandidateActionReviewService` with 6 tests:
- Approve updates all review metadata fields correctly.
- Reject/freeze/archive all produce correct statuses.
- Invalid decision strings raise errors.
- Empty/whitespace reviewer IDs are rejected.
- Payload, supporting refs, risk flags, policy, and all no-send invariants are preserved after review.
- The original candidate object is not mutated.
- Mapping inputs (dicts) are accepted and validated.

#### `tests/test_behavior_review_cli.py` (new file)

Added `TestCandidateActionReviewCLI` with 4 tests:
- Full approve flow: reads JSON, reviews, writes output, validates stdout safety (no draft text).
- Invalid JSON input is rejected with a clear error message.
- Missing input file produces a clear error.
- Invalid decision string ("send") is rejected.

#### `docs/data_contracts/behavior_planner_contract.md`

Added the "T213 Review Scope" section documenting:
- Supported decisions and their semantics.
- Review metadata field updates.
- The "approved is not sendable" boundary.
- CLI safe-output expectations.
- Relationship to future OutboundSendGate milestones.

#### `docs/worker_summary/T213_worker_summary.md` (new file)

Worker completion summary with files changed, service behavior, verification results, explicit non-actions, and remaining risks.

#### `docs/07_handoff.md`

Appended the T213 worker completion record and the T212 captain close-out record.

### 2.3 Significance for Future Development

T213 completes the M10 manual review layer. The progression is now:

```
T210: Define the schema (what a candidate action looks like)
T211: Generate candidates deterministically (rule engine proposes actions)
T212: Enrich candidates with draft text (so humans can read them)
T213: Let humans review candidates (approve/reject/freeze/archive)
T214: Evaluate behavior safety (next task, not yet started)
```

After T213, the project has a complete human-in-the-loop review pipeline for proactive behavior suggestions. The next task (T214) should evaluate whether reviewed candidates are behaviorally safe, not whether they should be executed.

The key invariant preserved across T210-T213: **no candidate action, even an approved one, is sendable, schedulable, or executable.** Real outbound behavior stays behind the M11 OutboundSendGate milestone.

## 3. Why This Review Result

**Verdict: PASS**

The task goal is fully met:

1. **The service works correctly.** `CandidateActionReviewService` handles all four decisions, validates inputs, returns new objects, and preserves all safety invariants. No mock, stub, or hardcoded behavior.

2. **The CLI works correctly.** It reads JSON, applies decisions, writes output, and keeps stdout safe (draft text excluded).

3. **Tests are adequate.** 6 service-level tests + 4 CLI tests cover the core paths, error handling, invariant preservation, and stdout safety. The test gap is minor (no CLI-level tests for freeze/archive/reject decisions specifically, no multi-review history growth test).

4. **No forbidden scope violations.** No message sending, no platform integration, no LLM calls, no store mutations, no task board updates. The worker stayed within allowed files.

5. **Documentation matches reality.** The contract doc accurately describes the review scope, metadata semantics, and the approved-is-not-sendable boundary.

6. **No existing functionality is broken.** The changes are purely additive. `ProactiveDraftGenerator` and `BehaviorRulePlanner` are unchanged.

Non-blocking observations (N01-N05, M01-M03) are conventional noise, minor coverage notes, or pre-existing project-wide patterns. None warrant a downgrade from PASS.

## 4. Worker Review and Explanation Assessment

The worker did not write a `docs/review/T213_review.md` or `docs/for_human/T213_review_explanation.md` — those are the reviewer's responsibility, not the worker's. The worker correctly wrote the worker summary (`docs/worker_summary/T213_worker_summary.md`) which accurately describes the changes, verification, and non-actions. No factual errors were found in the worker summary.
