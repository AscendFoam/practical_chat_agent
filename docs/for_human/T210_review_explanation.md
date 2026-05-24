# T210 Review Explanation

## What This Task Is About (In Plain Language)

This project is building a chat assistant that helps you maintain long-term relationships with contacts based on your chat history. One eventual goal is for the assistant to proactively suggest things like "maybe you should check in with this friend" or "here's a draft reply you could send."

But before the assistant can suggest anything, we need to define what a "suggestion" looks like in code. That's what T210 does: it defines the data shapes (schemas) for proactive behavior, without implementing any actual behavior, sending, or automation.

Think of it like designing the form that a suggestion would be written on, before we build the system that fills in the form or the system that acts on it.

## What The Implementation Changed

### Code Changes

**New models added to `src/practical_chat_agent/core/models.py`:**

1. **`AgentSelfState`**: A compact snapshot of what the assistant knows about the current situation (who the agent is, who the user is, what contact is relevant, what approved information is available, any risk flags). It deliberately excludes raw chat text, private messages, or any execution capability.

2. **`BehaviorPolicy`**: A strict safety envelope that defines what kinds of suggestions are allowed. It hardcodes four critical rules that can never be changed:
   - Human review is always required
   - Automatic sending is always forbidden
   - Platform execution is always forbidden
   - Scheduler use is always forbidden

   It also lists the six allowed suggestion types (like "draft a check-in message" or "suggest a conversation topic") and explicitly forbids any other type.

3. **`CandidateActionPayload`**: The content of a suggestion. It has a safe summary, optional draft text, review notes, and metadata. The metadata field is guarded by a validator that rejects dangerous keys like `send_at`, `platform`, `raw_transcript`, `access_token`, etc.

4. **`CandidateAction`**: The complete suggestion artifact. It ties together a contact, a user, an action type, evidence supporting the suggestion, risk flags, a payload, and a policy. It validates that the action type is allowed by the attached policy. It has an `is_runtime_visible()` helper that checks whether the suggestion has been approved through human review.

**New tests added to `tests/test_behavior_schema.py`:**

25 tests covering valid construction, required field enforcement, safety invariant enforcement (no auto-send, no platform execution), forbidden metadata key rejection, lifecycle states as data-only, JSON round-trip fidelity, and confirmation that these models have no send/schedule/execute methods.

**New contract document:**

`docs/data_contracts/behavior_planner_contract.md` describes the allowed action types, forbidden payload fields, lifecycle states, evidence requirements, and the boundary with future OutboundSendGate work.

### What Was NOT Changed

- No existing models, services, CLI commands, or runtime behavior was modified.
- No message sending, scheduling, platform integration, or automation was added.
- No LLM calls, embeddings, vector databases, or external services were introduced.
- No memory, ContactSkill, relationship state, or approved store mutation occurred.
- No raw chat history or private content was read or committed.

## Why This Matters For The Project

This is the opening task of **Milestone 10 (BehaviorPlanner)**, which aims to generate draft-only proactive action candidates. The project roadmap in `docs/04_task_board.md` shows the full M10 plan:

- T210 (this task): Define the data schemas
- T211: Build a rule engine that generates candidates using these schemas
- T212: Generate proactive drafts
- T213: Build a review CLI so humans can approve/reject candidates
- T214: Safety evaluation

T210 is the foundation. By defining the schemas first with hard-coded safety invariants (Literal[True] for human_review_required, Literal[False] for auto_send_allowed), we ensure that every future task in M10 works within a safe, review-first boundary. Even if someone writes code to create a CandidateAction, the type system itself prevents them from making it auto-sendable or bypassing human review.

This follows the same pattern used successfully in earlier milestones:
- M8 (RelationshipState) started with T190 schema before building signal extraction and review
- M9 (MemoryRetrieval) started with T200 contract before building the retriever and evals
- M7 (LLM Planner) started with T180 contract before building the generator

The key architectural decision here is that `CandidateAction` embeds both a `BehaviorPolicy` and a `CandidateActionPayload`, with a cross-validator ensuring the action type is allowed by the policy. This means the policy travels with the action and can be checked at any point in the pipeline, not just at creation time.

## Why I Gave PASS

The task goal is fully met. The worker:

1. **Defined all required schemas** (`AgentSelfState`, `BehaviorPolicy`, `CandidateAction`) plus a supporting `CandidateActionPayload`.

2. **Enforced safety invariants at the type level** using `Literal[True]` and `Literal[False]`, which means these values cannot be changed at runtime through normal Python/Pydantic usage.

3. **Provided comprehensive tests** (25) covering all 10 test categories listed in the task spec: valid construction, required fields, validation failures, review-only defaults, no-auto-send invariants, lifecycle states, JSON round-trip, payload safety, evidence/ref preservation, and stable ID behavior.

4. **Stayed within scope** - no forbidden activities (no sending, scheduling, platform integration, memory mutation, LLM calls, or raw transcript access).

5. **Wrote an accurate contract document** that clearly describes the models, boundaries, and relationship to future milestones without claiming execution capability.

6. **Passed all verification**: compilation, schema tests (25), and full test suite (731 non-typer tests passed; 16 pre-existing typer import failures are unrelated).

There are four minor test coverage gaps (no test for `max_candidates` range validation, no test for `access_token`/`api_key` forbidden keys, no test for nullable `contact_id` round-trip, no test for `review_notes` round-trip), but these are non-blocking because the schema validators are comprehensive and the type system provides strong guarantees.
