# Review: T223

Verdict: PASS

## Blocking Issues

None.

## Non-Blocking Issues

N01: `_is_candidate_action_input` heuristic is duplicated from T222's `LocalFakeOutboundAdapter` with identical logic (`action_id`, `action_type`, `schema_version=="candidate_action_v1"` fingerprints). This is conservative and safe but the duplication between the two adapters could be extracted into a shared utility in a future refactor. Not blocking because both copies are correct independently.

N02: `FeishuSandboxRecipient.__post_init__` checks `recipient_type not in ("open_id", "chat_id")` even though the type annotation is `Literal["open_id", "chat_id"]`. The runtime check is redundant for static-type-checked code but provides defensive safety for dynamic construction. Acceptable for current scope.

N03: `FeishuSandboxAdapterConfig.__post_init__` normalizes `recipient_map` in-place by reassigning `self.recipient_map = normalized`. Because the dataclass is mutable (not frozen), the original dict reference is discarded. This is functionally correct but could surprise callers who hold a reference to the pre-normalization dict. Low risk in current synthetic scope.

N04: `_build_payload` constructs the Feishu payload as `{"receive_id_type": ..., "receive_id": ..., "msg_type": "text", "content": {"text": ...}}`. This shape matches the Feishu open API `POST /im/v1/messages` body, but no test validates that the key names match the actual API contract. The payload shape is a reasonable sandbox approximation but should be validated against the real Feishu API docs when production work begins.

N05: `FeishuSandboxDeliveryResult` is a mutable dataclass while `FakeOutboundDeliveryResult` from T222 is also mutable. Neither uses `frozen=True`. Acceptable for current scope but both result types would benefit from immutability guarantees to prevent post-delivery tampering if they enter production paths.

## Missing Tests

M01: No test exercises `FeishuSandboxAdapterConfig` validation: empty `adapter_name` and empty `recipient_map` keys should raise `ValueError` per `__post_init__`. The config validation path exists but is untested.

M02: No test exercises `FeishuSandboxRecipient` validation: invalid `recipient_type` and empty `recipient_id` should raise `ValueError`. These are defensive checks that lack coverage.

M03: No test exercises `dry_run=True` explicitly overriding `dry_run_by_default=False` in config. The current test uses default `dry_run_by_default=True`, so explicit override of the effective dry-run flag is covered only by the `dry_run=False` case.

M04: No test verifies that `_FakeTransport.calls` is empty after a blocked path other than `blocked_not_sendable` (e.g., `blocked_wrong_channel` or `blocked_missing_recipient`). The non-sendable test checks this, but the channel/recipient block paths do not assert transport isolation.

M05: No test covers the `blocked_transport_unavailable` path: dry-run disabled but no transport injected. This is a valid status (`feishu_sandbox_sent` requires transport, but what happens when config says `dry_run_by_default=False` and no transport is provided). The code handles this at line 194-204 but no test exercises it.

M06: No test verifies `existing_audit` deduplication when the caller passes duplicate notes (e.g., `existing_audit=["caller_note", "caller_note"]`). The `_dedupe` path is simple and correct but untested for the Feishu adapter specifically. The fake adapter test covers similar ground.

## Suspicious Implementation Details

None. The implementation is straightforward, deterministic, and well-structured. Key observations:

- The adapter correctly delegates sendability to `OutboundMessageRequest.is_sendable()` without reimplementation.
- `CandidateAction` inputs are rejected before Pydantic coercion, preventing accidental conversion.
- Channel validation is strict: only `"feishu"` is accepted, `"unspecified"` is not auto-mapped.
- Recipient resolution is explicit configuration, not extracted from payload metadata.
- Dry-run is the default; transport is only invoked when dry-run is explicitly disabled.
- Transport errors are caught and produce deterministic blocked results without mutating the request.
- The `_build_payload` method uses only `request.payload.draft_text`, not metadata or other fields.
- New forbidden metadata keys in `models.py` prevent Feishu target smuggling through `OutboundMessagePayload.metadata`.

## Verification

- `python -m py_compile` for all four source files: passed.
- `pytest tests/test_outbound_message_request_schema.py tests/test_outbound_send_gate.py tests/test_outbound_fake_adapter.py tests/test_feishu_outbound_adapter.py`: 65 passed.
- Full suite (excluding typer-dependent collection errors): 825 passed, 16 pre-existing failures (typer/LLM/CLI-dependent). No new failures from T223.
- Worker reported 845 passed; the discrepancy is explained by the typer collection error excluding test files that would otherwise pass or fail. The 825 count from `--ignore` is consistent with expected baseline.

## Allowed Files Check

All changed files are within the T223 allowed list:

- `src/practical_chat_agent/services/feishu_outbound_adapter.py` (new)
- `src/practical_chat_agent/core/models.py` (forbidden metadata keys expanded)
- `tests/test_feishu_outbound_adapter.py` (new)
- `tests/test_outbound_fake_adapter.py` (T222 hardening tests added)
- `docs/data_contracts/outbound_send_gate_contract.md` (T223 sections)
- `docs/worker_summary/T223_worker_summary.md` (new)
- `docs/07_handoff.md` (T223 completion record)

No forbidden files modified. `src/practical_chat_agent/app/main.py`, `docs/04_task_board.md`, and `src/practical_chat_agent/services/outbound_send_gate.py` were not modified.

## Forbidden Scope Check

- No production Feishu sending.
- No real Feishu, webhook, email, browser, desktop, notification, WeChat, or other external API calls in committed code/tests.
- No production credentials, webhook registration, event callbacks, bot installation flow, or environment-secret reads.
- No CLI send path, AppContainer wiring, scheduler, timer, background job, automation, or runtime delivery hook.
- No mutation of `OutboundMessageRequest`, `CandidateAction`, memory records, ContactSkill, RelationshipState, approved stores, or private artifacts.
- No `private/chat_history/` reads and no committed private content.
- No task-board update.
- `CandidateAction` inputs are explicitly rejected at the adapter boundary.
- `is_sendable()` is respected as the adapter boundary.
- Gate `allowed` is not treated as delivery completion.
- Recipient mapping is explicit configuration, not smuggled through payload metadata.
- Payload construction uses approved outbound draft text only.
- No vendored Feishu SDK code.

## Recommended Next Action

T223 is review-complete. Captain may mark T223 as complete and advance to T224 (Feishu review card). The Feishu sandbox adapter boundary, injected transport protocol, explicit recipient mapping, and audit trail established here should serve as the reference pattern for future real adapter tasks.
