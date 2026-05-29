# Task T233: WeCom Customer Service Provider Safety Gate

## Task ID

T233

## Goal

Implement a deterministic local provider-constraint safety gate for the selected
M12 surface: WeCom WeChat Customer Service.

This gate sits after `OutboundSendGate` and before any future dry-run outbound
adapter. It must evaluate whether an already-sendable `OutboundMessageRequest`
is eligible for WeCom Customer Service payload preparation, without preparing
the payload, calling WeCom APIs, loading credentials, registering callbacks, or
sending anything.

## Why Now

T231 passed review as a synthetic inbound contract spike. It proves that
synthetic WeCom Customer Service inbound message/event shapes can normalize to
`InboundEvent`, but it does not solve outbound provider constraints.

T232 remains blocked because WeCom Customer Service outbound has additional
provider-specific constraints: recipient identity, active customer-service
window, 5-message window limit, failure-event semantics, account eligibility,
credential handling, callback verification, and audit redaction. T233 should
define and test the local safety layer first.

## Allowed Files

Worker may edit only:

- `src/practical_chat_agent/services/wecom_customer_service_safety.py`
- `tests/test_wecom_customer_service_safety_gate.py`
- `docs/data_contracts/wecom_customer_service_safety_contract.md`
- `docs/tasks/M12_wechat_adapter/T232_wechat_outbound_adapter.md`
- `docs/worker_summary/T233_worker_summary.md`
- `docs/07_handoff.md`

If another file appears necessary, stop and report the need instead of editing
outside this list.

## Forbidden Scope

- Do not implement a WeCom outbound adapter or prepare WeCom API payloads.
- Do not call WeChat, WeCom, Tencent, Feishu, or any external platform API.
- Do not load or read credentials, environment variables, tokens, cookies,
  QR codes, tenant IDs, app IDs, OpenIDs, external user IDs, `open_kfid`, real
  recipient IDs, callback Token, EncodingAESKey, corpsecret, or app secrets.
- Do not register callback URLs, implement webhook routes, poll/sync messages,
  schedule jobs, add background loops, add CLI commands, or wire `AppContainer`.
- Do not send messages, retry delivery, mutate outbound requests, or treat
  provider eligibility as delivery.
- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not mutate memory, ContactSkill, RelationshipState, feedback logs,
  approved stores, or inbound event stores.
- Do not modify `src/practical_chat_agent/core/models.py`, `OutboundSendGate`,
  inbound connectors, outbound adapters, runtime services, task board, or tests
  outside the allowed test file.
- Do not claim production readiness or live WeCom compatibility.

## Inputs To Read

- `README.md`
- `AGENTS.md`
- `docs/02_experiment_plan.md`
- `docs/04_task_board.md`
- `docs/07_handoff.md`
- `docs/review/T231_review.md`
- `docs/data_contracts/wecom_customer_service_inbound_contract.md`
- `docs/data_contracts/outbound_send_gate_contract.md`
- Existing outbound safety patterns:
  - `src/practical_chat_agent/services/outbound_send_gate.py`
  - `src/practical_chat_agent/services/feishu_outbound_adapter.py`
  - `src/practical_chat_agent/services/outbound_fake_adapter.py`
  - `tests/test_outbound_send_gate.py`
  - `tests/test_feishu_outbound_adapter.py`

Official docs do not need to be fetched for this task unless the worker wants
to recheck them. If rechecked, cite only official Tencent/WeCom documentation
and record retrieval dates in the safety contract. If not rechecked, treat T230
and T231 documentation facts as drift-sensitive.

## Expected Implementation

Create `WeComCustomerServiceSafetyGate` as a pure local evaluator.

Recommended objects:

- `WeComCustomerServiceRecipient`
  - `contact_id: str`
  - `recipient_alias: str`
  - `open_kfid_alias: str`
  - `external_user_alias: str`
  - `service_window_expires_at: datetime | None`
  - `messages_sent_in_window: int = 0`
  - `manual_send_allowed: bool = True`
- `WeComCustomerServiceSafetyConfig`
  - `surface: str = "wecom_customer_service"`
  - `manual_send_only: bool = True`
  - `proactive_send_disabled: bool = True`
  - `provider_kill_switch_enabled: bool = False`
  - `max_messages_per_window: int = 5`
  - validate that `manual_send_only` and `proactive_send_disabled` are true
    for the current mainline
- `WeComCustomerServiceSafetyContext`
  - `now: datetime`
  - `recipient_map: dict[str, WeComCustomerServiceRecipient]`
  - optional `existing_audit: list[str]`
- `WeComCustomerServiceSafetyDecision`
  - `safety_state: "allowed" | "blocked"`
  - `reason_codes: list[str]`
  - `request_id`, `contact_id`, `user_id`
  - `recipient_alias`, `open_kfid_alias`, `external_user_alias` as aliases
  - `audit_notes: list[str]`
  - `provider_surface="wecom_customer_service"`

The gate should accept an `OutboundMessageRequest` or stable mapping that
validates to one. It should not mutate the input request.

Required blocking behavior:

- block if the request is not already `is_sendable()`;
- block if `channel_preference` is not `"wechat"` or a documented explicit
  WeCom Customer Service surface config is missing;
- block if no recipient map entry exists for `request.contact_id`;
- block if `provider_kill_switch_enabled=True`;
- block if recipient `manual_send_allowed=False`;
- block if `service_window_expires_at` is missing or at/before `context.now`;
- block if `messages_sent_in_window >= max_messages_per_window`;
- block if `OutboundMessagePayload.metadata` contains provider identity,
  credential, or recipient-smuggling keys such as:
  - `external_userid`
  - `open_kfid`
  - `open_id`
  - `unionid`
  - `access_token`
  - `corpsecret`
  - `encoding_aes_key`
  - `callback_token`
  - `wecom_external_userid`
  - `wecom_open_kfid`

Required allow behavior:

- allow only when request sendability, channel/surface, recipient mapping,
  service window, message-window quota, kill-switch, and metadata-smuggling
  checks all pass;
- return aliases only, never real provider IDs;
- preserve caller-provided audit notes;
- record that provider eligibility is not delivery.

## Required Tests

Use TDD. Add tests that fail before implementation and then pass.

Minimum test scenarios:

- valid already-sendable request with recipient map and active service window
  returns `allowed`;
- pending human approval or blocked send gate returns blocked before provider
  checks;
- missing recipient map returns blocked;
- expired or missing service window returns blocked;
- 5-message window limit returns blocked at the configured limit;
- provider kill switch returns blocked;
- `manual_send_allowed=False` returns blocked;
- provider identity/credential keys in payload metadata return blocked;
- mapping input validates consistently with model input;
- input `OutboundMessageRequest` is not mutated.

## Expected Output

- `src/practical_chat_agent/services/wecom_customer_service_safety.py`
- `tests/test_wecom_customer_service_safety_gate.py`
- `docs/data_contracts/wecom_customer_service_safety_contract.md`
- Updated `docs/tasks/M12_wechat_adapter/T232_wechat_outbound_adapter.md` so T232 remains blocked until T233 passes review, then may be rewritten as dry-run outbound payload preparation only.
- `docs/worker_summary/T233_worker_summary.md`
- T233 worker completion record appended to `docs/07_handoff.md`

Worker must not update `docs/04_task_board.md`; Captain updates that only after
review.

## Verification

Run at minimum:

```powershell
python -m py_compile src/practical_chat_agent/services/wecom_customer_service_safety.py
pytest tests/test_wecom_customer_service_safety_gate.py -q
pytest tests/test_wecom_customer_service_safety_gate.py tests/test_outbound_message_request_schema.py tests/test_outbound_send_gate.py -q
git diff --check
git status --short
```

Use workspace-local pytest cache/basetemp paths if needed.

The worker summary must record commands, results, explicit non-actions, and
remaining risks.

## Docs To Update

During worker execution:

- `docs/data_contracts/wecom_customer_service_safety_contract.md`
- `docs/tasks/M12_wechat_adapter/T232_wechat_outbound_adapter.md`
- `docs/worker_summary/T233_worker_summary.md`
- `docs/07_handoff.md`

After reviewer approval, Captain will update:

- `docs/00_raw_idea.md`
- `docs/01_feasibility_report.md`
- `docs/03_architecture.md`
- `docs/04_task_board.md`
- `docs/05_decision_log.md`
- `docs/06_eval_protocol.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

## Reviewer Type

adversarial
