# T224 Review Explanation: Feishu Review Card

## What this task is trying to accomplish

In the project's outbound messaging pipeline (Milestone 11), earlier tasks built:

- **T220**: A schema (`OutboundMessageRequest`) describing "I want to send this message to this person on this channel."
- **T221**: A send gate that evaluates whether the request passes policy rules (quiet hours, risk flags, etc.).
- **T222**: A fake adapter that simulates what "delivery" would look like locally, without actually sending anything.
- **T223**: A Feishu-specific sandbox adapter that prepares a Feishu-shaped payload for testing, still without real delivery.

What was missing: a way for a **human reviewer** to look at an outbound request and see all its state at a glance -- who it's for, whether it's approved, whether the gate allowed it, what the draft text says, and what a sandbox test produced -- plus a set of buttons (approve / request edit / reject / boundary feedback) that encode the reviewer's intent as inert data.

T224 fills that gap by building two things:

1. A **review-card renderer** that takes an outbound request and produces a local Feishu-compatible interactive-card payload -- essentially a rich, structured "card" that shows everything a reviewer needs to see.
2. A **review-intent parser** that takes a synthetic button-click payload (as if a reviewer had pressed a button on the card) and validates it into an inert intent record, or rejects it if it's malformed.

Neither the card nor the parsed intent does anything actionable. The card is presentation data. The intent is "the reviewer said approve" as a data point. No approval is applied, no messages are sent, no stores are mutated.

## What the implementation changed

### New file: `feishu_review_card.py`

This service module contains:

- **`FeishuReviewCardConfig`**: Deterministic configuration for rendering -- renderer name, preview character limit, max gate notes, max sandbox notes. Validates its own fields.
- **`FeishuReviewIntent`**: A frozen dataclass holding `schema_version`, `request_id`, and `action` (one of approve/request_edit/reject/boundary_feedback). This is what gets encoded into each button's value.
- **`FeishuReviewCardRenderResult`**: The render output -- status (rendered or blocked), request identity fields, sendability flag, the full card payload dict, and audit notes.
- **`FeishuReviewIntentParseResult`**: The parse output -- status (parsed or blocked), accepted flag, the validated intent (or None), and audit notes.
- **`FeishuReviewCardBuilder`**: The renderer. Its `render()` method:
  - Rejects `CandidateAction` inputs (the outbound request is a separate concept from behavioral action candidates).
  - Coerces mappings to `OutboundMessageRequest` via Pydantic validation.
  - Builds a card payload with sections for request identity, review state, gate state, risk flags, audit notes, draft preview (truncated for display only), optional sandbox result summary, and four action buttons.
  - Each button value encodes inert intent data with `schema_version`, `request_id`, and `action`.
  - Never calls Feishu, never mutates inputs, never applies decisions.
- **`FeishuReviewIntentParser`**: The parser. Its `parse()` method:
  - Extracts the action value from a synthetic card-action payload.
  - Validates schema version, request id, and action against the allowed set.
  - When an expected request id is provided, rejects cross-request payloads.
  - Returns parsed intent data only.

### New file: `test_feishu_review_card.py`

19 test methods covering:

- Rendering pending/non-sendable requests, sendable requests, blocked-gate requests.
- Rendering with optional sandbox result summary.
- Rejecting direct `CandidateAction` model and candidate-shaped mapping inputs.
- Verifying input request is not mutated.
- Verifying forbidden recipient metadata (open_id, chat_id, etc.) is absent from card output.
- Display truncation at exact boundary.
- Deterministic action values for all four buttons.
- Parsing all four valid actions (parameterized).
- Rejecting malformed payloads, missing request ids, unknown actions, missing schema versions, and cross-request payloads.

### Updated: `outbound_send_gate_contract.md`

Added sections documenting T224 card payload shape, review-intent action values, parser semantics, and the distinction between gate/fake/sandbox/card/parsed-intent states.

### Updated: `07_handoff.md`

Added T224 worker completion record with verification results and explicit non-actions.

## Why the review verdict is PASS

The implementation is clean, focused, and does exactly what the task package asks:

1. **Task completion**: Every required behavior from the task package is implemented -- card rendering for both sendable and non-sendable requests, `CandidateAction` rejection, all four action buttons, deterministic action values, inert intent parsing, and deterministic rejection of malformed/missing/unknown/cross-request inputs.

2. **No fake implementation**: There are no mocks, stubs, or hardcoded outputs. The card payload is built deterministically from the input request fields. The parser validates real field values. The `_FakeTransport` in tests exists only to assert it is never called -- it proves the renderer doesn't trigger transport.

3. **Test coverage is adequate**: 19 tests covering all required scenarios from the task package. The only gaps are minor edge cases (mapping-to-request positive coercion, `char_limit <= 3` boundary) that don't affect correctness.

4. **No over-engineering**: The module is ~410 lines of straightforward Python with clear dataclass boundaries, no unnecessary abstractions, no framework dependencies beyond what T220-T223 already established.

5. **No breakage**: All 84 M11-targeted tests pass. The 16 pre-existing failures in the full suite are unrelated (typer import, LLM CLI tests) and existed before T224.

6. **Documentation is accurate**: The contract doc and handoff record correctly describe what was built and explicitly state what was not built. No planned work is claimed as complete.

The non-blocking issues (`.claude/settings.json` convention noise, duplicated candidate detection pattern, missing config validation tests, mapping coercion fragility) are all minor and consistent with patterns accepted in prior T220-T223 reviews.
