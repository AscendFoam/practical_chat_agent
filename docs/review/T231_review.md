# Review: T231

Verdict: PASS

## Blocking Issues

None.

## Non-Blocking Issues

N01 `__init__.py` exports only `WeComCustomerServiceInboundConnector` in `__all__`. The existing `FeishuBotConnector` and `TelegramBotConnector` are imported directly by `container.py` rather than through `__init__.py`, so this does not break anything. It is a minor inconsistency in how connectors are exposed from the package namespace but is consistent with the prior state where `__init__.py` exported nothing.

N02 `_parse_occurred_at` silently falls back to `datetime.fromtimestamp(0, tz=timezone.utc)` (1970-01-01 epoch) when the timestamp field is missing, None, or unparseable. For synthetic-only scope this is acceptable, but a future live adapter should either require a valid timestamp or use an explicit sentinel that downstream consumers can distinguish from a real timestamp. The `send_failure_event` fixture exercises this fallback path implicitly because it contains no `event_time` or `send_time` field, but no test asserts the epoch value.

N03 Only the first message from `msg_list` is parsed. The current inbound abstraction returns one `InboundEvent` per `parse_inbound_payload` call, and the data contract correctly notes that batching is undefined. For a synthetic spike this is correct scope, but a future task must address multi-message sync responses before any live `sync_msg` integration.

N04 Minor test-coverage gaps that are non-blocking for spike scope:
- no test for `_parse_occurred_at` edge cases (ISO-8601 strings, string-digit timestamps above the millisecond threshold, negative timestamps, `None`, empty string)
- no test for `_text_body` returning `None` when `text` exists but has no `content` key or a non-dict `text` field on a `msgtype="text"` message
- no test for the `_optional_str` helper with non-string, non-None values
- no test verifying `agent_id` fallback when the top-level `agent_id` field is missing from a message payload

N05 The `_parse_occurred_at` method treats any integer greater than 10 billion as milliseconds, which is a reasonable heuristic but could misclassify a far-future seconds-since-epoch timestamp after approximately year 2286. This is not a practical concern for current or near-term use.

## Missing Tests

None required beyond the non-blocking coverage gaps noted in N04. The task package requires "focused tests" for can-handle behavior, successful text normalization, unsupported/event behavior, malformed rejection, and personal-WeChat rejection. All six required scenarios are covered by the six committed tests.

## Suspicious Implementation Details

None. The connector is a real, deterministic parser — not a mock, stub, or hardcoded output generator. Event IDs are derived from SHA-256 hashes of stable synthetic fields, field mapping is explicit, and all outputs are derived from inputs rather than fabricated.

The raw payload is carried into `InboundEvent.raw` alongside contract metadata. This is acceptable because the fixtures are purely synthetic and contain no real identifiers or private content. The data contract correctly notes that a future live adapter must define redaction rules before storing real provider payloads.

## Allowed Files Verification

Files changed by T231 worker:

- `src/practical_chat_agent/connectors/inbound/wecom_customer_service.py` — new file, within allowed scope
- `src/practical_chat_agent/connectors/inbound/__init__.py` — modified, within allowed scope
- `tests/test_wecom_customer_service_inbound.py` — new file, within allowed scope
- `tests/fixtures/wecom_customer_service_inbound/inbound_text_message.json` — new file, within allowed scope
- `tests/fixtures/wecom_customer_service_inbound/non_text_message.json` — new file, within allowed scope
- `tests/fixtures/wecom_customer_service_inbound/send_failure_event.json` — new file, within allowed scope
- `tests/fixtures/wecom_customer_service_inbound/malformed_missing_identity.json` — new file, within allowed scope
- `tests/fixtures/wecom_customer_service_inbound/personal_wechat_desktop_like.json` — new file, within allowed scope
- `docs/data_contracts/wecom_customer_service_inbound_contract.md` — new file, within allowed scope
- `docs/worker_summary/T231_worker_summary.md` — new file, within allowed scope
- `docs/07_handoff.md` — modified, within allowed scope

No `src/practical_chat_agent/core/models.py`, outbound adapters, send-gate behavior, CLI commands, runtime services, or task-board files were modified.

## Task Goal Verification

The task package required:

1. `WeComCustomerServiceInboundConnector` with `connector_name = "wecom_customer_service"` — present.
2. `can_handle_payload(payload)` for synthetic fixture wrapper and documented WeCom Customer Service shaped payloads — implemented, tested.
3. `parse_inbound_payload(payload)` returning `InboundConnectorResult` — implemented, tested.
4. Text messages mapped to `InboundEvent` with `platform=Platform.WECHAT`, `source_type=SourceType.CHAT_MESSAGE`, `direction=Direction.INBOUND`, `channel_type=ChannelType.DM`, `content_type=ContentType.TEXT`, deterministic `event_id`, scoped `channel_id`/`account_id`/`actor_id`, synthetic `text`, and `raw` with contract metadata — all present and verified by test assertions.
5. Non-text/provider-event shapes mapped to conservative `ContentType.SYSTEM` — implemented, tested.
6. Never infer repo `contact_id` or memory identity — no `contact_id` inference exists; test asserts `"contact_id" not in result.event.raw`.
7. Never inspect private files or environment variables — no such access exists.

Fixture set required: inbound text, non-text, provider event/failure, malformed, personal-WeChat/desktop — all five present.

Data contract document required sections: surface selection rationale, fixture field documentation, mapping table, unresolved constraints, why T232 remains blocked — all present.

Worker summary required sections: what changed, TDD evidence, official docs, explicit non-actions, verification, remaining risks — all present.

`docs/07_handoff.md` updated with T231 worker completion record containing all required fields.

Verification commands all passed as documented in the worker summary.

## Recommended Next Action

T231 is complete as a synthetic inbound contract spike.

Captain should:

1. Accept T231 as complete.
2. Update `docs/04_task_board.md` to mark T231 as passed.
3. Decide whether to rewrite T232 as a dry-run outbound adapter (similar to T223 Feishu sandbox) or keep it blocked until tenant/credential prerequisites are resolved.
4. If T232 proceeds, rewrite it as a synthetic-only outbound contract spike for WeCom Customer Service, gated by T231's inbound contract, and requiring no live credentials, no delivery, and no provider API calls.
5. Rewrite T233 as provider-constraint safety design (service-window checks, quota enforcement, manual-send-only defaults, recipient-map ownership, audit redaction, kill-switch behavior) before any live outbound work.
