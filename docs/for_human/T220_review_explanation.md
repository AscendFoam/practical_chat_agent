# T220 Review Explanation

## What this task is trying to accomplish

T220 is the first task of Milestone 11 (M11), which is about building an "outbound send gate" — a safety checkpoint that controls whether the chat agent is allowed to send messages to real contacts on real platforms like Feishu or WeChat.

Before this task, the project could:
- Analyze your chat history and extract memory facts and contact skills
- Generate candidate reply drafts and proactive behavior suggestions
- Have you review and approve those drafts through a CLI

But all of that was **review-only**. Nothing ever got sent anywhere.

The problem T220 solves is: when the project eventually does need to send messages, how do we make absolutely sure that a reviewed draft doesn't accidentally become a "go ahead and send this" command? T220 creates a **separate data contract** — a new type of record called `OutboundMessageRequest` — that is explicitly designed to be inert until both a human reviewer AND an automated safety gate explicitly approve it.

Think of it like this: previously you had a sticky note with a draft message on it. Now you're creating a formal "outbound request form" that requires two separate sign-offs before anything can happen. The sticky note (CandidateAction) is just evidence attached to the form; it can't authorize sending by itself.

## What the implementation changed

### Code changes (`src/practical_chat_agent/core/models.py`)

The worker added 4 new Pydantic models and 3 new type aliases, totaling about 136 lines:

1. **Type aliases** that define the allowed values for key fields:
   - `OutboundMessageChannel`: can be `"unspecified"`, `"feishu"`, or `"wechat"` — this is just a preference label, not a real platform connection
   - `OutboundRequestSourceType`: either `"candidate_action"` (derived from a reviewed proactive draft) or `"human_authored"` (written directly by you)
   - `OutboundHumanApprovalState` and `OutboundSendGateState`: track the review/gate lifecycle

2. **`OutboundMessagePayload`**: carries the draft text and optional metadata. It has a validator that rejects dangerous metadata keys — things like `send_at`, `access_token`, `adapter_payload`, `raw_transcript`, etc. This prevents someone from smuggling scheduling commands or credentials into what should be a plain text draft.

3. **`OutboundRequestHumanApproval`**: tracks whether a human has reviewed this specific outbound request. Defaults to "pending" with no approval. Has cross-field validators that ensure approved records have a reviewer ID and timestamp, and that pending records don't carry completed-review metadata.

4. **`OutboundRequestSendGate`**: tracks whether the automated safety gate (to be built in T221) has evaluated this request. Defaults to "not evaluated". Has similar cross-field validators for consistency.

5. **`OutboundMessageRequest`**: the top-level record that ties everything together. Key safety features:
   - Requires `contact_id`, `user_id`, and `source_type`
   - If the source is a `CandidateAction`, it must reference the candidate by ID — but this is evidence only, not authorization
   - If the source is `human_authored`, it must NOT reference a candidate (mutual exclusivity)
   - `is_sendable()` returns `False` by default and only returns `True` when BOTH human approval is "approved" AND gate state is "allowed"
   - Has no scheduler fields, no platform adapter objects, no credentials

6. **`_OUTBOUND_MESSAGE_FORBIDDEN_METADATA_FIELDS`**: a superset of the existing candidate-action forbidden fields, adding outbound-specific dangerous keys like `scheduler_id`, `timer_id`, `adapter_payload`, `platform_token`, `bot_token`, `app_secret`, `delivery_connector_name`, etc.

### Test changes (`tests/test_outbound_message_request_schema.py`)

11 tests covering:
- Minimal valid construction (defaults are inert)
- Rich construction with candidate-action evidence references
- JSON round-trip serialization
- Default state is not sendable
- Approved CandidateAction does NOT make the request sendable
- Source-type boundary enforcement
- Incomplete approval/gate states are rejected
- No scheduler or platform adapter fields exist on the model

### Documentation changes

- `docs/data_contracts/outbound_send_gate_contract.md`: describes the T220 contract, its relationship to M10's CandidateAction, the pre-T221 lifecycle, privacy boundaries, and what T220 does NOT authorize
- `docs/worker_summary/T220_worker_summary.md`: records what was changed, verification results, explicit non-actions, and remaining risks
- `docs/07_handoff.md`: appends the T220 worker completion record

### What did NOT change

The implementation did NOT:
- Send any messages or create any scheduling
- Integrate any real platform (Feishu, WeChat, etc.)
- Modify any existing models (CandidateAction, MemoryFact, ContactSkill, etc.)
- Add any runtime loops, CLI commands, or service execution paths
- Call any LLMs or external services
- Read any private chat history
- Update the task board (that's the Captain's job)

## Significance for future development

T220 establishes the **data foundation** for the entire outbound messaging pipeline. Every future M11 task builds on this schema:

- **T221** (OutboundSendGate) will take an `OutboundMessageRequest` as input and evaluate it against safety policies (quiet hours, frequency limits, duplicate suppression, kill switch), producing an `allowed` or `blocked` gate decision
- **T222** (Fake Adapter) will consume sendable `OutboundMessageRequest` records and simulate delivery locally
- **T223** (Feishu Adapter) will eventually connect to real Feishu APIs, but only behind the gate
- **T224** (Review Card) will provide a human-facing review interface for outbound requests

The key architectural decision is the **separation of concerns**: CandidateAction is evidence, OutboundMessageRequest is intent, and the gate is the safety checkpoint. This prevents the dangerous pattern where "approved draft" accidentally means "send now."

This directly addresses risk R093 from the project risk register: "future M11 code could accidentally interpret CandidateAction approval as outbound authorization."

## Why I gave this review result

**Verdict: PASS**

The task does exactly what it says: define a schema-only outbound request contract. The implementation is clean, follows established patterns from T210-T214, and introduces no execution, scheduling, or platform behavior.

**What's good:**
- The models are inert by default — you have to explicitly set human approval AND gate allowance for `is_sendable()` to return True
- The source-type boundary is enforced at the schema level (candidate_action requires a reference, human_authored forbids one)
- The forbidden metadata keys form a proper superset of the existing candidate-action set, adding outbound-specific dangerous fields
- Tests cover the key safety properties (CandidateAction approval doesn't make requests sendable, default state is inert)
- Full test suite passes (791 tests) with no regressions
- Documentation is accurate and does not claim future work as completed

**What's minor but acceptable:**
- A few test gaps: no standalone validator edge-case tests for the human-approval and gate-state models, no test for the `is_sendable()` True path, no test for the outbound-specific forbidden keys beyond what the candidate-action set already covers. These are minor because the validators are simple cross-field checks and the existing tests partially cover them.
- The implementation adds no new functions, services, or runtime behavior — it's purely schema definitions, which is exactly the right scope for this task.

This is a well-scoped, clean schema-only task that creates the right foundation for T221 without overstepping into execution territory.
