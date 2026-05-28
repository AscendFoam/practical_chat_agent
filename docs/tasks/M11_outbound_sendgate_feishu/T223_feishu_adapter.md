# Task T223: Feishu Sandbox Adapter

## Task ID

T223

## Goal

Implement the first Feishu-specific sandbox adapter boundary after T220
`OutboundMessageRequest`, T221 `OutboundSendGate`, and T222
`LocalFakeOutboundAdapter` exist.

The goal is not production delivery. The goal is a reviewable adapter surface
that can transform an already-sendable `OutboundMessageRequest` into a
Feishu-compatible sandbox payload/result while preserving human approval,
send-gate, audit, privacy, and no-autonomy boundaries.

Worker should be ambitious inside this boundary:

- define a typed Feishu sandbox adapter config/result surface
- map sendable outbound requests to a Feishu text-message payload shape
- require explicit recipient mapping/configuration rather than smuggling
  platform targets through `OutboundMessagePayload.metadata`
- support deterministic dry-run behavior by default
- support an injected sandbox/fake transport interface for tests, without
  calling real Feishu APIs in committed tests
- add useful hardening coverage carried forward from T222 review where it
  naturally fits, especially fake-adapter config validation, `existing_audit`,
  and payload-preview boundary tests
- update the outbound send-gate contract and handoff with the new sandbox
  boundary

## Forbidden Scope

- Do not bypass `OutboundMessageRequest.is_sendable()`.
- Do not treat `CandidateAction.status`, `review_state`, or
  `is_runtime_visible()` as adapter authorization.
- Do not accept direct `CandidateAction` input as sendable.
- Do not add production Feishu sending, production credentials, webhook
  registration, event callbacks, bot installation flow, or real platform
  delivery claims.
- Do not call Feishu, webhook, email, browser, desktop, notification, WeChat,
  or any other external API from committed tests.
- Do not read environment secrets or write `.env` / credential files.
- Do not add CLI send commands, runtime delivery hooks, scheduler/timer jobs,
  background workers, automations, or AppContainer wiring.
- Do not use the legacy `ActionDeliveryService` / `ActionExecutionRecord`
  delivery path for this M11 adapter.
- Do not mutate `OutboundMessageRequest`, `CandidateAction`, memory records,
  ContactSkill, RelationshipState, approved stores, or private artifacts.
- Do not read `private/chat_history/` or commit private content.
- Do not rely on `payload_preview` truncation as a privacy boundary for real
  adapter payloads; adapter payloads must be constructed from the approved
  outbound request payload only.
- Do not vendor Feishu SDK code. If a dependency becomes necessary, document it
  and keep the default tests dependency-free.

## Allowed Files

- `src/practical_chat_agent/services/feishu_outbound_adapter.py`
- `src/practical_chat_agent/services/outbound_fake_adapter.py`
- `src/practical_chat_agent/services/outbound_send_gate.py`
- `src/practical_chat_agent/core/models.py`
- `tests/test_feishu_outbound_adapter.py`
- `tests/test_outbound_fake_adapter.py`
- `tests/test_outbound_send_gate.py`
- `docs/data_contracts/outbound_send_gate_contract.md`
- `docs/worker_summary/T223_worker_summary.md`
- `docs/07_handoff.md`

Do not modify `src/practical_chat_agent/app/main.py` in T223. The adapter must
remain a service-level boundary, not an operator-facing send command.

If the worker finds a compelling need for a connector module, stop and report
the proposed path in the worker summary instead of expanding scope
unilaterally.

## Required Behavior

1. `FeishuSandboxOutboundAdapter.deliver()` or equivalent must accept a
   validated `OutboundMessageRequest` or stable mapping that validates to one.
2. It must reject direct `CandidateAction` objects and candidate-shaped
   mappings.
3. It must return a blocked result when `request.is_sendable()` is false.
4. It must require `channel_preference` to be compatible with Feishu, unless
   the design explicitly documents why `unspecified` can be dry-run mapped.
5. It must require explicit Feishu recipient configuration supplied outside the
   outbound payload metadata, such as a safe mapping from `contact_id` to a
   synthetic `open_id` / `chat_id`.
6. It must build a Feishu-compatible text message payload from
   `request.payload.draft_text` only.
7. It must default to dry-run/sandbox behavior that returns a deterministic
   result without network side effects.
8. If an injected transport is supported, tests must use a fake transport and
   assert the adapter sends only after the request is sendable and dry-run is
   disabled.
9. It must preserve audit notes distinguishing:
   - gate allowed
   - local fake simulation from T222
   - Feishu sandbox payload prepared
   - Feishu sandbox/fake transport invoked, if applicable
   - no production delivery
10. It must not mutate the input request.

## Expected Result Surface

Use names that fit the implementation, but the result should expose at least:

- adapter name
- delivery status, such as `feishu_dry_run_ready`,
  `feishu_sandbox_sent`, `blocked_not_sendable`,
  `blocked_invalid_request`, `blocked_missing_recipient`, or
  `blocked_wrong_channel`
- delivered/sent boolean that is false for dry-run and true only for an
  injected sandbox/fake transport success
- request id, contact id, user id, channel preference
- synthetic Feishu recipient id or recipient type, if configured
- prepared Feishu payload or safe payload summary
- provider/sandbox message id only when returned by injected fake transport
- audit notes
- timestamp normalized to aware UTC

## Required Tests

Add committed synthetic tests for:

- rejects non-sendable requests
- rejects direct `CandidateAction` input
- rejects candidate-shaped mappings
- rejects or blocks missing Feishu recipient mapping
- rejects or blocks incompatible channel preference
- dry-run prepares the expected Feishu text payload without invoking transport
- injected fake transport is invoked only for sendable requests when dry-run is
  explicitly disabled
- transport failure returns or raises a deterministic blocked/failed result
  without mutating the request
- audit notes preserve caller-provided `existing_audit`
- payload construction uses approved outbound draft text, not metadata adapter
  payloads
- no credentials, tokens, webhook URLs, or platform targets are accepted through
  payload metadata

Also add T222 hardening tests if still missing:

- `FakeOutboundAdapterConfig` rejects empty `adapter_name`
- `FakeOutboundAdapterConfig` rejects non-positive `preview_char_limit`
- fake adapter preserves `existing_audit`
- preview truncation exact-boundary and `preview_char_limit <= 3` behavior

## Verification Commands

Use workspace-local pytest temp/cache paths as in T220-T222.

Minimum verification:

- `python -m py_compile src/practical_chat_agent/core/models.py src/practical_chat_agent/services/outbound_send_gate.py src/practical_chat_agent/services/outbound_fake_adapter.py src/practical_chat_agent/services/feishu_outbound_adapter.py`
- `pytest tests/test_outbound_message_request_schema.py tests/test_outbound_send_gate.py tests/test_outbound_fake_adapter.py tests/test_feishu_outbound_adapter.py -q -o cache_dir=artifacts\t223_pytest_cache --basetemp=artifacts\t223_pytest_basetemp`
- `pytest tests/ -q -o cache_dir=artifacts\t223_pytest_cache --basetemp=artifacts\t223_pytest_basetemp`

If the full suite still has unrelated pre-existing failures, document the
failing tests and prove the T223-targeted subset passes.

## Deliverables

- Feishu sandbox adapter implementation.
- Synthetic tests covering success, dry-run, block, invalid input, recipient,
  audit, transport, and privacy boundaries.
- Updated outbound send-gate contract with T223 semantics.
- Worker summary with explicit non-actions and verification evidence.
- Handoff entry stating that production Feishu delivery is still not claimed.

## Reviewer Type

adversarial
