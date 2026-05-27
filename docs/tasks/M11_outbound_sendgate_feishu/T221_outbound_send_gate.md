# Task T221: OutboundSendGate

## Task ID

T221

## Goal

Implement the first deterministic outbound send gate over T220 `OutboundMessageRequest`.

T221 must decide whether a request is currently allowed or blocked by policy and write an auditable gate snapshot. It must not deliver the message, schedule delivery, call any platform, or create a fake adapter. Gate allowance is policy state only, not a send side effect.

## Why Now

T220 passed review with `PASS` and created an inert outbound request contract:

- `OutboundMessageRequest`
- `OutboundMessagePayload`
- `OutboundRequestHumanApproval`
- `OutboundRequestSendGate`

The next safe step is a platform-independent gate that evaluates this request before T222 fake adapter work or any Feishu/WeChat adapter work. T221 must preserve the separation between:

- M10 review-only evidence: `CandidateAction`
- T220 outbound draft intent: `OutboundMessageRequest`
- T221 gate policy/audit decision: `OutboundRequestSendGate`
- later adapter delivery: T222+

## Inputs To Read

- `AGENTS.md`
- `docs/04_task_board.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`
- `docs/review/T220_review.md`
- `docs/data_contracts/outbound_send_gate_contract.md`
- `src/practical_chat_agent/core/models.py`
- `src/practical_chat_agent/services/policy.py`
- `tests/test_outbound_message_request_schema.py`
- `tests/test_policy_engine.py`

## Forbidden Scope

- Do not send messages.
- Do not schedule messages, create timers, create reminders, create background jobs, or create automations.
- Do not implement a fake adapter, Feishu adapter, WeChat adapter, browser/desktop adapter, notification adapter, email/webhook adapter, or review card.
- Do not add CLI send commands, runtime loops, app-container wiring, daemon behavior, or delivery execution paths.
- Do not call LLM/provider APIs, embeddings, vector DBs, Mem0/Zep, web services, Feishu/WeChat APIs, webhook URLs, or external systems.
- Do not mutate `CandidateAction`, `MemoryFact`, `ContactSkill`, `RelationshipState`, approved stores, private artifacts, or review metadata.
- Do not read `private/chat_history/` or commit private content.
- Do not treat `CandidateAction.status="approved"`, `review_state="reviewed"`, or `is_runtime_visible()` as send/schedule/platform authorization.
- Do not treat `OutboundMessageRequest.channel_preference` as an adapter target or delivery connector.
- Do not implement T222, T223, T224, or M12 behavior.

## Allowed Files

- `src/practical_chat_agent/core/models.py`
- `src/practical_chat_agent/services/outbound_send_gate.py`
- `tests/test_outbound_send_gate.py`
- `tests/test_outbound_message_request_schema.py`
- `docs/data_contracts/outbound_send_gate_contract.md`
- `docs/worker_summary/T221_worker_summary.md`
- `docs/07_handoff.md`

If a small import/export update is required for package ergonomics, the worker may also modify:

- `src/practical_chat_agent/services/__init__.py`

Do not update `docs/04_task_board.md`; Captain will mark completion after review.

## Expected Output

Add a deterministic send-gate service, preferably in `src/practical_chat_agent/services/outbound_send_gate.py`.

Recommended public surface:

- `OutboundSendGateConfig`
- `OutboundSendGateDecision`
- `OutboundSendGate.evaluate(request, now=None, recent_requests=None, existing_audit=None)`

Equivalent names are acceptable if the contract is clear and well tested.

The service must:

- accept a validated `OutboundMessageRequest` or stable mapping that validates to one
- return a new request or decision object without mutating the input in place
- set `send_gate.gate_state` to `allowed` only when every required policy condition passes
- set `send_gate.gate_state` to `blocked` when any blocking rule fails
- include `evaluator_id`, `evaluated_at`, and gate notes/audit reasons on evaluated gate state
- require explicit outbound human approval on `OutboundMessageRequest.human_approval`
- reject pending or rejected outbound human approval
- reject empty/whitespace payload text defensively even though schema has `min_length`
- preserve request ids, contact/user ids, source refs, timestamps, channel preference, and risk flags
- keep `channel_preference` as data only
- keep `source_candidate_action_id` as evidence only

Policy rules must include:

- **manual-only mode:** no request can become allowed unless `human_approval.review_state=="approved"` and `approved_by_human=True`
- **kill switch:** config can block all requests with a clear gate note such as `kill_switch_enabled`
- **quiet hours:** configurable timezone and HH:MM quiet-hours window; requests during quiet hours are blocked
- **frequency limit:** configurable max allowed/evaluated/sent-equivalent requests per contact/user/channel window using only synthetic/local request history supplied to the gate
- **duplicate suppression:** configurable duplicate window that blocks matching normalized draft text for the same contact/user/channel preference
- **self-echo prevention:** block requests whose normalized draft text is identical to a supplied latest inbound/user text or explicit self-echo reference in the gate context
- **audit log:** deterministic notes/reasons should make it clear which checks passed or blocked the request

Do not require a repository, database, queue, scheduler, platform client, or adapter object. If recent history is needed, pass it as explicit in-memory synthetic data to `evaluate()`.

Address the most valuable T220 review coverage while implementing T221:

- add an `is_sendable()` true-path test using explicit outbound human approval plus gate `allowed`
- add standalone validator tests for incomplete approval/gate metadata
- add tests for outbound-specific forbidden metadata keys such as `scheduler_id`, `timer_id`, `adapter_payload`, `platform_target`, `bot_token`, `app_secret`, `delivery_connector_name`, `delivery_response`, and `send_result`

Update `docs/data_contracts/outbound_send_gate_contract.md` with:

- T221 gate lifecycle
- config/input/output shape
- allowed vs blocked semantics
- audit note conventions
- explicit statement that gate allowance is not delivery
- policy rule list and what each rule blocks
- forbidden platform/adapter/scheduler boundaries

Write `docs/worker_summary/T221_worker_summary.md` with:

- files changed
- gate behavior added
- policy rules implemented
- verification commands/results
- explicit non-actions
- remaining risks

Append a T221 implementation record to `docs/07_handoff.md`.

## Verification

Run:

```powershell
python -m py_compile src/practical_chat_agent/core/models.py src/practical_chat_agent/services/outbound_send_gate.py
pytest tests/test_outbound_message_request_schema.py tests/test_outbound_send_gate.py -q
pytest tests/test_behavior_schema.py tests/test_outbound_message_request_schema.py tests/test_outbound_send_gate.py -q
pytest tests/ -q
```

If the Windows default temp directory is inaccessible in this sandbox, set `TEMP` and `TMP` to a workspace-local temp directory before running pytest and record that fact in `docs/07_handoff.md`.

## Acceptance Criteria

- Fresh outbound requests remain non-sendable by default.
- Approved `CandidateAction` artifacts still do not make an outbound request sendable.
- A request becomes sendable only when outbound human approval is approved and T221 gate state is allowed.
- Pending/rejected outbound approval blocks the gate.
- Kill switch blocks all requests.
- Quiet hours block requests in the configured local window, including overnight windows.
- Frequency limit blocks excess requests using supplied synthetic history.
- Duplicate suppression blocks repeated draft text in the configured window.
- Self-echo prevention blocks echoing the latest supplied user/inbound text.
- Gate decisions are auditable through evaluator id, evaluated timestamp, and gate notes.
- No adapter, scheduler, CLI send command, runtime loop, or external service path is introduced.

## Docs To Update

- `docs/data_contracts/outbound_send_gate_contract.md`
- `docs/worker_summary/T221_worker_summary.md`
- `docs/07_handoff.md`

## Reviewer Type

adversarial
