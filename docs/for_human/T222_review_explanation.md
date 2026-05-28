# T222 Review Explanation

## 1. What T222 Is Trying To Do

The project is building a chat agent that can help you reply to contacts. But before the agent can actually send any message, the system needs multiple safety gates to prevent accidental or unwanted sending.

By this point (M11), the project already has:

- **T220** defined a data structure called `OutboundMessageRequest` - essentially a "draft envelope" that holds a message draft, who it's for, and metadata about approvals.
- **T221** added a "send gate" - a policy checker that evaluates whether a request passes safety rules (quiet hours, frequency limits, duplicate detection, self-echo prevention, etc). The gate can say "allowed" or "blocked", but it does NOT actually send anything.

T222 is the next step: a **local fake adapter**. Think of it as a practice delivery service. It takes gate-approved requests and pretends to deliver them, producing a local record that says "fake delivered". This proves the system can correctly handle the adapter boundary between "gate approved" and "adapter received" without any risk of real message sending.

The analogy: T220 is the letter, T221 is the mailroom security check, and T222 is a practice mailroom that records "letter received" without actually putting anything in a mailbox.

## 2. What The Implementation Changed

### New files

**`src/practical_chat_agent/services/outbound_fake_adapter.py`** - The core fake adapter:

- `FakeOutboundAdapterConfig` - simple settings (adapter name, how much of the draft text to preview).
- `FakeOutboundDeliveryResult` - a result record showing what happened: status (`fake_delivered`, `blocked_not_sendable`, `blocked_invalid_request`), who the request was for, timestamps, and audit notes.
- `LocalFakeOutboundAdapter` - the adapter itself. Its `deliver()` method:
  1. Rejects `CandidateAction` inputs directly (those are review-only artifacts, not sendable requests).
  2. Validates that the input is a proper `OutboundMessageRequest` (or can be converted to one).
  3. Checks `is_sendable()` - if the request hasn't passed both human approval AND gate approval, it returns a blocked result.
  4. For sendable requests, returns a deterministic local result with `fake_delivered` status.
  5. Never mutates the input, never calls external services, never writes to disk.

**`tests/test_outbound_fake_adapter.py`** - 7 tests covering:
- Successful fake delivery of a sendable request
- Acceptance of dictionary-format requests (stable mapping)
- Blocking of non-sendable requests (gate not allowed)
- Blocking of requests without explicit human approval
- Rejection of direct CandidateAction model instances
- Rejection of CandidateAction-style dictionaries
- Rejection of completely invalid dictionaries

### Modified files

**`tests/test_outbound_send_gate.py`** - Added 6 new T221 tests that T222's task package requested:
- Quiet-hours clear path (request outside quiet window passes)
- Frequency-limit clear path (below threshold passes)
- Duplicate-suppression clear path (distinct text passes)
- Self-echo clear path (non-matching text passes)
- Combined blocking (kill switch + pending approval both recorded)

These are "positive path" tests - they verify that the gate correctly records "all clear" notes when requests pass, not just when they fail.

**`docs/data_contracts/outbound_send_gate_contract.md`** - Updated with T222 sections documenting the fake adapter lifecycle, result shape, the distinction between gate `allowed` vs fake `fake_delivered` vs real delivery, and what T222 still does not authorize.

**`docs/worker_summary/T222_worker_summary.md`** - Worker's summary of what changed and verification results.

**`docs/07_handoff.md`** - T222 completion record appended.

### What was NOT changed

- `pyproject.toml` - no `tzdata` dependency added. Tests use UTC only. The Windows named-timezone portability risk (R097) remains open.
- `src/practical_chat_agent/services/__init__.py` - no package export changes needed.
- No core models, no existing send gate logic, no runtime paths, no platform integrations.

### Significance for future development

T222 establishes the **adapter boundary pattern** that all future real adapters (Feishu T223, WeChat T230+) must follow:

1. Only accept `OutboundMessageRequest` inputs
2. Check `is_sendable()` as the hard boundary
3. Return structured results with audit trails
4. Never mutate inputs
5. Keep results review-safe (truncated previews, no raw transcripts)

When T223 implements the real Feishu adapter, it should follow this same structure but replace the `fake_delivered` result with a real API call and platform-specific result. The contract, tests, and audit patterns from T222 will serve as the template.

## 3. Why The Review Verdict Is PASS

The implementation is clean, correct, and properly scoped:

- **No fake completion**: The adapter does real validation work (Pydantic validation, sendability checks, CandidateAction rejection). It's not a stub that always returns success.
- **No forbidden behavior**: No external calls, no disk writes, no scheduler, no runtime loops, no platform integration.
- **Good test coverage**: 7 adapter tests + 6 T221 clear-path tests = 13 new tests. All pass. The full suite (762 non-LLM/typer tests) passes with no new failures.
- **Correct boundary**: `is_sendable()` is the adapter boundary. `CandidateAction` inputs are rejected. Gate `allowed` is not treated as delivery.
- **Documentation matches reality**: The contract, worker summary, and handoff accurately describe what was implemented without overstating capabilities.

The only notes are minor test gaps (config validation, audit passthrough, preview boundary) that don't affect correctness or safety. These can be addressed later if they become relevant.
