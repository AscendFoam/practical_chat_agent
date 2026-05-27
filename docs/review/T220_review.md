# Review: T220

Verdict: PASS

## Blocking Issues

None.

## Non-Blocking Issues

N01 `_OUTBOUND_MESSAGE_FORBIDDEN_METADATA_FIELDS` uses `set().union()` with a `frozenset`, producing a `frozenset` result at runtime but slightly surprising intermediate type mixing. This is harmless but could be cleaner as `frozenset(_CANDIDATE_ACTION_FORBIDDEN_PAYLOAD_FIELDS) | frozenset({...})`.

N02 The `_OUTBOUND_MESSAGE_FORBIDDEN_METADATA_FIELDS` superset adds outbound-specific forbidden keys (scheduler_id, timer_id, adapter_payload, platform_target, bot_token, app_secret, etc.) on top of the existing `_CANDIDATE_ACTION_FORBIDDEN_PAYLOAD_FIELDS`. This is the correct approach — the outbound boundary is strictly narrower — but the contract doc does not enumerate the full superset explicitly. Future developers may need to consult the code to see the complete list.

N03 `OutboundMessagePayload.draft_text` uses `min_length=1` but no `max_length`. This is consistent with `CandidateActionPayload.safe_summary` (which also has no max), and is acceptable for a schema-only contract. Later tasks may want to enforce length bounds.

N04 `OutboundMessageRequest.source_candidate_action_id` uses `min_length=1` when present but cannot enforce that the referenced id actually exists in a store. This is consistent with how `ReplyPlanContextRef` works and is expected for a schema-only task.

N05 `OutboundRequestHumanApproval` and `OutboundRequestSendGate` both use `model_validator(mode="after")` with manual `self` return. This is correct Pydantic v2 usage. The validators enforce cross-field invariants (pending state must not carry completed review metadata; evaluated state must carry evaluator data) which is appropriate defensive design.

N06 The `docs/data_contracts/outbound_send_gate_contract.md` and `docs/worker_summary/T220_worker_summary.md` files are not in the task's `Allowed files` list — the allowed list names `docs/data_contracts/outbound_send_gate_contract.md` and `docs/worker_summary/T220_worker_summary.md` explicitly, so this is fine. Both are within the allowed scope.

N07 `artifacts/t220_pytest_basetemp/` contains a large number of untracked test temp files. This is established convention noise from prior tasks' pytest basetemp usage and is not a T220-specific concern.

## Missing Tests

M01 No explicit test for `OutboundRequestHumanApproval` and `OutboundRequestSendGate` as standalone model validators (e.g., verifying that `approved` state with missing `reviewer_id` raises ValidationError, or that `allowed` gate state with missing `evaluator_id` raises ValidationError). The existing test `test_request_rejects_fake_sendable_state_without_human_approval_and_gate` partially covers this by asserting that incomplete approval/gate dicts raise ValidationError, but standalone validator edge cases are not independently tested.

M02 No test for `OutboundMessageRequest.is_sendable()` returning `True` when both human approval is approved and gate state is allowed. Currently `is_sendable()` is only tested returning `False` (the default). Testing the `True` path would confirm the combined-condition logic is correct and guard against regressions when T221 starts populating these fields.

M03 No test for `OutboundMessagePayload` with the additional outbound-specific forbidden keys that go beyond `_CANDIDATE_ACTION_FORBIDDEN_PAYLOAD_FIELDS` (e.g., `scheduler_id`, `timer_id`, `adapter_payload`, `platform_target`, `bot_token`, `app_secret`, `delivery_connector_name`, `delivery_response`, `send_result`). The existing test only checks keys present in the original `_CANDIDATE_ACTION_FORBIDDEN_PAYLOAD_FIELDS` set.

M04 No test verifying that `OutboundMessageRequest` preserves `created_at` and `updated_at` through JSON round-trip. The existing round-trip test checks `request_id`, `contact_id`, `user_id`, `payload`, and `source_context_refs` but not timestamps.

M05 No test verifying `channel_preference` accepts all three valid values (`unspecified`, `feishu`, `wechat`). The existing test only checks `"unspecified"` (default) and `"feishu"`.

## Suspicious Implementation Details

None. The implementation is clean, minimal, and follows established patterns from T210-T214. The schema models are inert by default, the forbidden-key validation is a proper superset of the candidate-action set, the source-type boundary validator correctly enforces mutual exclusivity, and `is_sendable()` requires both human approval and gate allowance.

## Verification

- `python -m py_compile src/practical_chat_agent/core/models.py`: passed
- `pytest tests/test_outbound_message_request_schema.py -q`: 11 passed
- `pytest tests/test_behavior_schema.py tests/test_outbound_message_request_schema.py -q`: 36 passed
- Full suite: 791 passed (16 pre-existing failures in LLM/typer-dependent tests, not related to T220)

All verification commands used workspace-local temp/cache paths as documented.

## Allowed Files Compliance

Changed files:
- `src/practical_chat_agent/core/models.py` — in allowed list
- `tests/test_outbound_message_request_schema.py` — in allowed list
- `docs/data_contracts/outbound_send_gate_contract.md` — in allowed list
- `docs/worker_summary/T220_worker_summary.md` — in allowed list
- `docs/07_handoff.md` — in allowed list

No forbidden files were modified. No forbidden scope was entered.

## Forbidden Scope Compliance

- No message sending, scheduling, timers, reminders, background jobs, or automations.
- No Feishu, WeChat, webhook, email, browser, desktop, or platform adapter integration.
- No runtime loops, CLI execution paths, app-container wiring, or service execution.
- No LLM/provider API calls, embeddings, vector DB, Mem0/Zep, web services, or external systems.
- No mutation of `MemoryFact`, `ContactSkill`, `RelationshipState`, `CandidateAction`, approved stores, private artifacts, or review metadata.
- No `CandidateAction` approval/status/runtime-visibility treated as send/schedule/platform authorization.
- No implementation of T221 send-gate policy, T222 fake adapter, T223 Feishu adapter, or T224 review card.
- No `private/chat_history/` reads or committed private content.
- No `docs/04_task_board.md` update.

## Recommended Next Action

T220 is complete as a schema-only outbound request boundary. The next task should be T221 `OutboundSendGate`, which will implement the gate policy (quiet hours, frequency limits, duplicate suppression, kill switch, audit decisions) using the T220 schema as its input contract.

The missing tests (M01-M05) are minor and do not block acceptance. M02 (`is_sendable()` true path) is the most valuable to add early in T221 when the gate logic starts populating these fields.
