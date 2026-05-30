# Review: T233

Verdict: PASS

## Blocking Issues

None.

## Non-Blocking Issues

N01 The smuggling-key check at line 287–291 uses `casefold()` for key comparison, but the frozenset `_PROVIDER_METADATA_SMUGGLING_KEYS` stores the original lowercase strings. Because all keys in the set are ASCII lowercase, `casefold()` is equivalent to `lower()` here and the comparison is correct. However, if future keys were added with non-ASCII characters, `casefold()` might normalize differently than expected. This is not a practical concern with the current key set.

N02 The `evaluate` method performs early-return blocking before all checks are evaluated in some paths (e.g., missing recipient map returns at line 185–190 before checking `manual_send_allowed`, `service_window`, or `message_window`). This means a single decision may not report all applicable reason codes. This is an acceptable short-circuit design for a safety gate — it reports the first gate-specific blocking reason rather than accumulating all possible reasons — but it differs from the `OutboundSendGate` pattern which evaluates all checks before returning. The data contract does not explicitly commit to either full-accumulation or short-circuit semantics.

N03 `WeComCustomerServiceSafetyConfig.surface` is validated only by a runtime `strip()` comparison against `WECom_CUSTOMER_SERVICE_SURFACE` inside `evaluate()` (line 162). The config dataclass does not enforce this in `__post_init__`, meaning an invalid surface config can be constructed silently and only fails at evaluation time. The test at line 172–183 creates `WeComCustomerServiceSafetyConfig(surface="")` to exercise this path, but a more robust approach would validate surface in `__post_init__` similar to how `manual_send_only` and `proactive_send_disabled` are validated there.

N04 The `_coerce_context` method (lines 246–260) instantiates a new `WeComCustomerServiceSafetyContext` from a raw mapping, but does not validate that `data["now"]` is present or is a valid `datetime`. A missing `"now"` key would raise a `KeyError` rather than the `ValueError` raised by `WeComCustomerServiceSafetyContext.__post_init__`. This is a minor error-type inconsistency; it does not affect correctness for valid inputs.

N05 The `_as_aware_utc` method (lines 294–297) assumes naive datetimes are UTC, consistent with the `OutboundSendGate` pattern. However, `OutboundSendGate._as_aware_utc` uses `ZoneInfo("UTC")` while T233 uses `timezone.utc`. Both produce UTC-aware datetimes, but the T233 approach is simpler and does not depend on `zoneinfo`/`tzdata`. This inconsistency is harmless but worth noting for future unification.

N06 The smuggling-key detection (line 287–291) compares metadata keys after `casefold()` and `strip()`, but the existing `OutboundMessagePayload.reject_forbidden_metadata_keys` validator in `models.py` (line 925–997) already rejects `open_id` and `access_token` at model construction time. This means those two keys can never reach the T233 gate through a valid `OutboundMessageRequest` — they would fail at Pydantic validation. The T233 check is therefore partially redundant for model inputs but still useful for mapping inputs that bypass Pydantic validation. The data contract correctly does not claim the smuggling check replaces model validation.

N07 Minor test-coverage gaps that are non-blocking for the task scope:
- no test for `WeComCustomerServiceRecipient` validation of negative `messages_sent_in_window` or empty string fields
- no test for `WeComCustomerServiceSafetyContext` validation of mismatched `recipient_map` key vs `recipient.contact_id`
- no test for `_coerce_context` with missing `"now"` key
- no test for a valid `surface` config value that differs from the default (e.g., only the default `"wecom_customer_service"` is tested in the allow path)
- no test for `max_messages_per_window` with a non-default value
- no test for multiple provider-smuggling keys in the same metadata dict
- no test verifying that `_coerce_request` with an invalid mapping returns blocked (only `ValidationError` is caught, but no test creates an invalid mapping that triggers it)

N08 The `_PROVIDER_METADATA_SMUGGLING_KEYS` frozenset uses `WECom_CUSTOMER_SERVICE_SURFACE` with an unusual capitalization (`WECom` rather than `WECOM` or `Wecom`). This appears to be a minor naming inconsistency in the constant. The variable `_PROVIDER_METADATA_SMUGGLING_KEYS` itself uses standard Python naming. This is purely cosmetic.

## Missing Tests

None required beyond the non-blocking coverage gaps noted in N07. The task package requires minimum test scenarios for: valid allow path, pending/blocked send gate, missing recipient map, expired/missing service window, 5-message window limit, provider kill switch, manual_send disallowed, provider identity/credential metadata smuggling, mapping input parity, and input non-mutation. All 10 required scenarios are covered by the 25 committed tests.

## Suspicious Implementation Details

None. The gate is a genuine, deterministic, local evaluator. Every blocked reason code is derived from explicit inputs (request fields, config values, recipient map entries, context timestamp). No mock, stub, hardcoded output, random value, or hidden state exists. The `allowed` path correctly records `provider_eligible_not_delivery` and `provider_payload_not_prepared` in audit notes. The decision is a new in-memory dataclass; the input request is not mutated.

## Allowed Files Verification

Files changed by T233 worker:

- `src/practical_chat_agent/services/wecom_customer_service_safety.py` — new file, within allowed scope
- `tests/test_wecom_customer_service_safety_gate.py` — new file, within allowed scope
- `docs/data_contracts/wecom_customer_service_safety_contract.md` — new file, within allowed scope
- `docs/tasks/M12_wechat_adapter/T232_wechat_outbound_adapter.md` — modified, within allowed scope
- `docs/worker_summary/T233_worker_summary.md` — new file, within allowed scope
- `docs/07_handoff.md` — modified, within allowed scope

No `src/practical_chat_agent/core/models.py`, `OutboundSendGate`, inbound connectors, outbound adapters, runtime services, CLI commands, or `docs/04_task_board.md` were modified.

## Task Goal Verification

The task package required:

1. `WeComCustomerServiceSafetyGate` as a pure local evaluator — implemented.
2. `WeComCustomerServiceRecipient` with `contact_id`, `recipient_alias`, `open_kfid_alias`, `external_user_alias`, `service_window_expires_at`, `messages_sent_in_window`, `manual_send_allowed` — implemented with validation.
3. `WeComCustomerServiceSafetyConfig` with `surface`, `manual_send_only`, `proactive_send_disabled`, `provider_kill_switch_enabled`, `max_messages_per_window` — implemented with enforcement that `manual_send_only=True` and `proactive_send_disabled=True`.
4. `WeComCustomerServiceSafetyContext` with `now`, `recipient_map`, optional `existing_audit` — implemented with key-consistency validation.
5. `WeComCustomerServiceSafetyDecision` with `safety_state`, `reason_codes`, `request_id`, `contact_id`, `user_id`, `recipient_alias`, `open_kfid_alias`, `external_user_alias`, `audit_notes`, `provider_surface` — implemented.
6. Required blocking behaviors: non-sendable request, non-wechat channel, missing surface config, missing recipient map, kill switch, manual_send disallowed, missing/expired service window, 5-message limit, provider metadata smuggling — all implemented and tested.
7. Required allow behavior: all checks pass returns `allowed` with aliases only, preserved audit notes, and `provider_eligible_not_delivery` / `provider_payload_not_prepared` — implemented and tested.
8. Input `OutboundMessageRequest` not mutated — tested.
9. Mapping input validates consistently with model input — tested.
10. Data contract document with required sections — present and complete.
11. T232 task update to keep T232 blocked — present.
12. Worker summary with required sections — present.
13. Handoff record with required fields — present.

Verification commands documented in the worker summary:
- `py_compile` passed.
- 25 focused T233 tests passed.
- 61 combined tests (T233 + outbound schema + send gate) passed.
- `git diff --check` passed (line-ending warnings only).
- `git status --short` shows only T233 allowed-file changes.

## Recommended Next Action

T233 is complete as a deterministic local provider safety gate.

Captain should:

1. Accept T233 as complete.
2. Update `docs/04_task_board.md` to mark T233 as passed.
3. Rewrite T232 as a dry-run outbound payload-preparation task for WeCom Customer Service, gated by T233's safety gate, using synthetic fixtures, explicit reviewed recipient aliases, and requiring no live credentials, no delivery, and no provider API calls.
4. Ensure the rewritten T232 consumes only `WeComCustomerServiceSafetyDecision` with `safety_state="allowed"` and never bypasses the T233 safety gate.
