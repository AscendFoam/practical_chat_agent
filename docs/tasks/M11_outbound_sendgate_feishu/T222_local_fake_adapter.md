# Task T222: Local Fake Adapter

## Task ID

T222

## Goal

Implement a local fake outbound adapter that consumes only already-sendable T220/T221 `OutboundMessageRequest` records and produces synthetic local delivery results.

T222 must validate the adapter boundary after the send gate without contacting any real platform. A fake-delivery result is local test evidence only; it is not Feishu, WeChat, webhook, email, desktop, browser, scheduler, or runtime delivery.

## Why Now

T220 created an inert outbound request contract and T221 added deterministic send-gate policy. The next safe step is a local fake adapter that proves the adapter boundary can consume gate-approved requests while still avoiding real delivery.

This task must preserve the sequence:

- M10 `CandidateAction`: review-only evidence
- T220 `OutboundMessageRequest`: outbound draft intent
- T221 `OutboundSendGate`: explicit policy/audit gate
- T222 local fake adapter: synthetic local delivery simulation only
- T223+ real platform adapter work: still forbidden until later reviewed tasks

## Inputs To Read

- `AGENTS.md`
- `docs/04_task_board.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`
- `docs/review/T221_review.md`
- `docs/data_contracts/outbound_send_gate_contract.md`
- `src/practical_chat_agent/core/models.py`
- `src/practical_chat_agent/services/outbound_send_gate.py`
- `tests/test_outbound_message_request_schema.py`
- `tests/test_outbound_send_gate.py`

## Forbidden Scope

- Do not send real messages.
- Do not call Feishu, WeChat, webhook, email, browser, desktop, notification, SMS, or any external delivery API.
- Do not add scheduler, timer, reminder, background job, automation, daemon, or runtime loop behavior.
- Do not add a user-facing send CLI or app-container/runtime delivery wiring.
- Do not call LLM/provider APIs, embeddings, vector DBs, Mem0/Zep, web services, or external systems.
- Do not mutate `CandidateAction`, `MemoryFact`, `ContactSkill`, `RelationshipState`, approved stores, private artifacts, or review metadata.
- Do not read `private/chat_history/` or commit private content.
- Do not treat `CandidateAction.status="approved"`, `review_state="reviewed"`, or `is_runtime_visible()` as adapter authorization.
- Do not bypass `OutboundMessageRequest.is_sendable()`.
- Do not implement T223 Feishu adapter, T224 review card, or M12 WeChat adapter behavior.

## Allowed Files

- `src/practical_chat_agent/services/outbound_fake_adapter.py`
- `src/practical_chat_agent/services/outbound_send_gate.py`
- `src/practical_chat_agent/core/models.py`
- `tests/test_outbound_fake_adapter.py`
- `tests/test_outbound_send_gate.py`
- `docs/data_contracts/outbound_send_gate_contract.md`
- `docs/worker_summary/T222_worker_summary.md`
- `docs/07_handoff.md`

If needed for clean package exports, the worker may also modify:

- `src/practical_chat_agent/services/__init__.py`

If the worker chooses to resolve the T221 Windows named-timezone portability risk by declaring the dependency, the worker may also modify:

- `pyproject.toml`

No other files are allowed. Do not update `docs/04_task_board.md`; Captain will mark completion after review.

## Expected Output

Add a local fake adapter service, preferably in `src/practical_chat_agent/services/outbound_fake_adapter.py`.

Recommended public surface:

- `LocalFakeOutboundAdapter`
- `FakeOutboundDeliveryResult`
- optional `FakeOutboundAdapterConfig`

Equivalent names are acceptable if the boundary is clear and well tested.

The fake adapter must:

- accept a validated `OutboundMessageRequest` or stable mapping that validates to one
- reject any request where `request.is_sendable()` is false
- reject requests whose `human_approval` is not approved or whose `send_gate.gate_state` is not `allowed`
- reject direct `CandidateAction` inputs entirely
- return a deterministic local result object without mutating the input request
- record `request_id`, `contact_id`, `user_id`, `channel_preference`, adapter name, fake delivery status, fake delivery timestamp, and safe audit notes
- avoid storing full raw/private transcript fields
- keep payload handling synthetic and local; if a preview is useful, cap it to a small safe length and document that committed tests use only synthetic text
- not write to disk unless the task explicitly documents a synthetic local artifact under an allowed path; in-memory results are preferred

Suggested result statuses:

- `fake_delivered`
- `blocked_not_sendable`
- `blocked_invalid_request`

Keep these local to the fake adapter unless a core model is clearly justified.

Also harden the most valuable T221 review coverage while implementing T222:

- add quiet-hours clear-path test (`quiet_hours_clear`)
- add frequency-limit clear-path test (`frequency_limit_clear`)
- add duplicate-suppression clear-path test (`duplicate_check_clear`)
- add self-echo clear-path test (`self_echo_clear`)
- add at least one combined-blocking test where multiple reasons are preserved, e.g. `kill_switch_enabled` plus `human_approval_pending`

For the T221 `tzdata` portability note, make one explicit choice and document it in the worker summary:

- either add `tzdata` to `pyproject.toml` for Windows named-timezone reproducibility
- or keep T222 tests/config on UTC-only paths and leave R097 open

Update `docs/data_contracts/outbound_send_gate_contract.md` with:

- T222 fake adapter lifecycle
- fake delivery result shape
- requirement that `is_sendable()` is the adapter boundary
- statement that fake delivery is local simulation only
- distinction between gate `allowed`, fake `fake_delivered`, and real platform delivery
- forbidden external/platform/scheduler behavior

Write `docs/worker_summary/T222_worker_summary.md` with:

- files changed
- fake adapter behavior added
- T221 clear-path tests added
- timezone portability decision
- verification commands/results
- explicit non-actions
- remaining risks

Append a T222 implementation record to `docs/07_handoff.md`.

## Verification

Run:

```powershell
python -m py_compile src/practical_chat_agent/core/models.py src/practical_chat_agent/services/outbound_send_gate.py src/practical_chat_agent/services/outbound_fake_adapter.py
pytest tests/test_outbound_send_gate.py tests/test_outbound_fake_adapter.py -q
pytest tests/test_outbound_message_request_schema.py tests/test_outbound_send_gate.py tests/test_outbound_fake_adapter.py -q
pytest tests/ -q
```

If the Windows default temp directory is inaccessible in this sandbox, set `TEMP` and `TMP` to a workspace-local temp directory before running pytest and record that fact in `docs/07_handoff.md`.

If the full suite still has pre-existing LLM/typer-dependent failures, record the exact failure count and prove the T222-targeted commands pass.

## Acceptance Criteria

- Fake adapter accepts only `OutboundMessageRequest` inputs, not `CandidateAction`.
- Non-sendable requests are rejected locally with a clear result or exception.
- Sendable requests produce a deterministic local fake-delivery result.
- The adapter does not mutate the input request.
- The adapter does not call external services or real platform APIs.
- The adapter does not create scheduler/background/runtime delivery behavior.
- Fake result metadata distinguishes local simulation from real delivery.
- T221 pass-through tests cover clear paths for quiet hours, frequency, duplicate suppression, and self-echo checks.
- The `tzdata` portability choice is documented.

## Docs To Update

- `docs/data_contracts/outbound_send_gate_contract.md`
- `docs/worker_summary/T222_worker_summary.md`
- `docs/07_handoff.md`

## Reviewer Type

adversarial
