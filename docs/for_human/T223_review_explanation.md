# T223 Review Explanation

## 1. What T223 Is Trying To Do

The project is building a chat agent that can help you reply to contacts. By this point (M11), the system already has multiple safety layers:

- **T220** defined `OutboundMessageRequest` - a "draft envelope" holding a message draft, who it's for, and approval metadata.
- **T221** added a "send gate" - a policy checker that evaluates whether a request passes safety rules (quiet hours, frequency limits, duplicate detection, etc). The gate says "allowed" or "blocked" but does NOT send anything.
- **T222** added a "local fake adapter" - a practice delivery service that takes gate-approved requests and records "fake delivered" without any real delivery.

T223 is the next step: a **Feishu sandbox adapter**. Think of it as a Feishu-specific practice delivery service. It takes gate-approved requests and transforms them into Feishu-compatible message payloads, but still doesn't actually send anything to Feishu. This proves the system can correctly handle the boundary between "gate approved" and "Feishu-ready payload" without any risk of real message delivery.

The analogy: T220 is the letter, T221 is the mailroom security check, T222 is a generic practice mailroom, and T223 is a Feishu-specific practice mailroom that formats the letter for Feishu's envelope standard and records "ready for Feishu" without actually putting anything in a Feishu mailbox.

## 2. What The Implementation Changed

### New files

**`src/practical_chat_agent/services/feishu_outbound_adapter.py`** - The core Feishu sandbox adapter:

- `FeishuSandboxRecipient` - a frozen dataclass holding a Feishu recipient type (`open_id` or `chat_id`) and a recipient ID. Validates that both fields are non-empty.
- `FeishuSandboxAdapterConfig` - adapter configuration including: adapter name, whether dry-run is the default (yes, for safety), and a recipient map that maps `contact_id` to `FeishuSandboxRecipient`. The recipient map is explicit configuration outside the outbound payload metadata.
- `FeishuSandboxTransportResponse` - a synthetic response from a fake/sandbox transport, holding a provider message ID and audit notes.
- `FeishuSandboxTransport` - a Protocol (interface) that any injected transport must implement. This allows tests to inject a fake transport without calling real Feishu APIs.
- `FeishuSandboxDeliveryResult` - the result record with: adapter name, delivery status (8 possible statuses like `feishu_dry_run_ready`, `feishu_sandbox_sent`, various blocked states), request metadata, recipient info, the prepared Feishu payload, provider message ID, timestamp, and audit notes.
- `FeishuSandboxOutboundAdapter` - the adapter itself. Its `deliver()` method:
  1. Rejects `CandidateAction` inputs directly.
  2. Validates that the input is a proper `OutboundMessageRequest` (or can be converted to one).
  3. Checks `is_sendable()` - if the request hasn't passed both human approval AND gate approval, returns a blocked result.
  4. Checks `channel_preference` must be `"feishu"` - rejects `"unspecified"` and `"wechat"`.
  5. Looks up the recipient in the config's explicit recipient map - blocks if missing.
  6. Builds a Feishu-compatible text payload from `request.payload.draft_text` only.
  7. By default, returns `feishu_dry_run_ready` without invoking any transport.
  8. If dry-run is explicitly disabled AND a transport is injected, calls the transport and returns success or failure.
  9. Never mutates the input, never reads secrets, never writes to disk, never makes real API calls.

**`tests/test_feishu_outbound_adapter.py`** - 11 tests (including parametrized) covering:
- Rejection of non-sendable requests (without invoking transport)
- Rejection of direct `CandidateAction` model instances
- Rejection of candidate-shaped mappings
- Blocking of missing Feishu recipient mapping
- Blocking of incompatible channel preferences (`unspecified`, `wechat`)
- Dry-run payload preparation without transport invocation
- Fake transport invocation only when dry-run is disabled
- Transport failure returning deterministic blocked result without request mutation
- Payload construction using only approved draft text (not metadata)
- Forbidden metadata keys preventing Feishu target smuggling

### Modified files

**`src/practical_chat_agent/core/models.py`** - Extended the `_OUTBOUND_MESSAGE_FORBIDDEN_METADATA_FIELDS` frozenset with 6 new Feishu-specific keys: `open_id`, `chat_id`, `receive_id`, `receive_id_type`, `feishu_open_id`, `feishu_chat_id`. This prevents anyone from sneaking Feishu recipient targets or platform identifiers through the outbound payload's metadata field.

**`tests/test_outbound_fake_adapter.py`** - Added 4 T222 hardening tests requested by the T223 task package:
- `FakeOutboundAdapterConfig` rejects empty adapter name
- `FakeOutboundAdapterConfig` rejects non-positive preview char limit
- Fake adapter preserves caller-provided `existing_audit` notes
- Preview truncation exact-boundary (text length equals limit, no truncation)
- Preview char limit <= 3 returns only `"..."`

**`docs/data_contracts/outbound_send_gate_contract.md`** - Updated with T223 sections documenting: Feishu sandbox adapter inputs, config shape, result shape, lifecycle, the distinction between gate `allowed` vs fake `fake_delivered` vs Feishu `feishu_dry_run_ready` vs real delivery, and what T223 still does not authorize.

**`docs/worker_summary/T223_worker_summary.md`** - Worker's summary of what changed and verification results.

**`docs/07_handoff.md`** - T223 completion record appended.

### What was NOT changed

- `src/practical_chat_agent/app/main.py` - no CLI/runtime wiring. The adapter remains a service-level boundary.
- `docs/04_task_board.md` - no task board update (worker correctly deferred to Captain).
- `src/practical_chat_agent/services/outbound_send_gate.py` - no gate logic changes.
- `pyproject.toml` - no new dependencies.
- No real Feishu SDK vendored or imported.

### Significance for future development

T223 establishes the **Feishu adapter boundary pattern** that all future Feishu production work must follow:

1. Only accept `OutboundMessageRequest` inputs (never raw `CandidateAction`)
2. Check `is_sendable()` as the hard boundary
3. Validate channel preference explicitly
4. Require explicit recipient mapping from config, not from payload metadata
5. Build payloads from approved draft text only
6. Default to dry-run (no side effects)
7. Support injected transport for testing without real API calls
8. Return structured results with full audit trails

When future tasks implement production Feishu delivery, they should replace the fake transport with a real Feishu SDK adapter while preserving all the boundary checks, audit trails, and safety patterns established here.

The forbidden metadata key expansion in `models.py` is particularly important: it prevents a common security anti-pattern where platform-specific targets (Feishu open_id, chat_id) could be smuggled through generic metadata fields, bypassing the explicit recipient mapping requirement.

## 3. Why The Review Verdict Is PASS

The implementation is clean, correct, properly scoped, and follows the patterns established by T220-T222:

- **No fake completion**: The adapter does real validation work (Pydantic validation, sendability checks, channel verification, recipient resolution). It's not a stub that always returns success.
- **No forbidden behavior**: No external calls in committed code, no disk writes, no scheduler, no runtime loops, no platform integration, no CLI wiring.
- **Good test coverage**: 11 Feishu adapter tests + 4 T222 hardening tests = 15 new tests. All 65 targeted tests pass. Full suite passes with only pre-existing typer/LLM failures.
- **Correct boundaries**: `is_sendable()` is respected. `CandidateAction` inputs are rejected. Channel must be `"feishu"`. Recipient must be explicit config. Dry-run is default. Gate `allowed` is not treated as delivery.
- **Security hardening**: New forbidden metadata keys prevent Feishu target smuggling through payload metadata.
- **Documentation matches reality**: The contract, worker summary, and handoff accurately describe what was implemented without overstating capabilities.

The non-blocking issues are all minor: duplicated candidate detection heuristic between T222/T223 (both correct), redundant type validation in `FeishuSandboxRecipient`, mutable result dataclasses, and unvalidated payload key naming against real Feishu API docs. None affect correctness or safety. The missing tests are for config validation, recipient validation, and the `blocked_transport_unavailable` path - useful hardening but not required for the current sandbox-only scope.
