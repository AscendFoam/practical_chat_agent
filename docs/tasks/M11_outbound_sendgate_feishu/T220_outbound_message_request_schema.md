# Task T220: OutboundMessageRequest Schema

## Task ID

T220

## Goal

Define the first M11 outbound-send contract as a schema-only boundary.

T220 must create a separate `OutboundMessageRequest` model that can later be evaluated by an `OutboundSendGate`, without reusing `CandidateAction` as an executable request and without introducing any real sending, scheduling, platform adapter, runtime loop, or background job.

## Why Now

M10 is complete with `Gate M10 Allow`: the project can create, enrich, manually review, and safety-evaluate review-only `CandidateAction` artifacts.

The next safe step is not a platform adapter. It is a contract that separates:

- review-only behavior evidence: `CandidateAction`
- future outbound intent: `OutboundMessageRequest`
- later gate decision: T221 `OutboundSendGate`

This separation prevents reviewed proactive candidates from becoming implicit send authorization.

## Inputs To Read

- `AGENTS.md`
- `docs/04_task_board.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`
- `docs/review/M10_review.md`
- `docs/review/T214_behavior_safety_eval.md`
- `docs/data_contracts/behavior_planner_contract.md`
- `src/practical_chat_agent/core/models.py`
- `tests/test_behavior_schema.py`

## Forbidden Scope

- Do not send messages.
- Do not schedule messages, create timers, create reminders, create background jobs, or create automations.
- Do not integrate Feishu, WeChat, browser, desktop, notification, email, webhook, or any platform adapter.
- Do not add runtime loops, app-container wiring, CLI commands, or service execution paths.
- Do not call LLM/provider APIs, embeddings, vector DBs, Mem0/Zep, web services, or external systems.
- Do not mutate `MemoryFact`, `ContactSkill`, `RelationshipState`, `CandidateAction`, approved stores, private artifacts, or review metadata.
- Do not read `private/chat_history/` or commit private content.
- Do not treat `CandidateAction.status="approved"`, `review_state="reviewed"`, or `is_runtime_visible()` as send/schedule/platform authorization.
- Do not implement T221 send-gate policy, T222 fake adapter, T223 Feishu adapter, or T224 review card behavior.

## Allowed Files

- `src/practical_chat_agent/core/models.py`
- `tests/test_outbound_message_request_schema.py`
- `docs/data_contracts/outbound_send_gate_contract.md`
- `docs/worker_summary/T220_worker_summary.md`
- `docs/07_handoff.md`

## Expected Output

Add schema-only outbound request contracts in `src/practical_chat_agent/core/models.py`.

Recommended model surface:

- `OutboundMessageRequest`
- optional small supporting models/enums only if they keep the contract clearer, such as `OutboundMessageChannel`, `OutboundMessagePayload`, or `OutboundRequestSource`

The schema must include:

- stable `request_id`
- `contact_id`
- `source_candidate_action_id` or equivalent optional evidence reference
- explicit `source_type` that distinguishes `candidate_action` evidence from direct human-authored requests
- message payload text or draft body, clearly still not sent
- channel/platform preference as data only, with no adapter target object
- review/gate state that defaults to not approved for sending
- human approval fields that are explicit and separate from `CandidateAction` review
- no-send defaults that make the request inert until T221 evaluates it
- audit-friendly timestamps/refs where consistent with existing model patterns
- metadata validation that rejects credential keys, scheduler keys, platform tokens, `send_at`, adapter payloads, or other execution fields

Tests should cover:

- minimal valid construction
- rich construction with candidate-action evidence refs
- JSON round-trip
- default state is not sendable
- `CandidateAction` approval/status is not enough to make an outbound request sendable
- forbidden metadata/execution fields are rejected
- private/raw transcript fields are not required and are not accepted as special privileged fields
- no platform adapter object or scheduler field exists
- schema preserves contact/request/source ids and safe refs

Update `docs/data_contracts/outbound_send_gate_contract.md` with:

- T220 schema scope
- relationship to M10 `CandidateAction`
- explicit statement that `CandidateAction` is evidence only
- lifecycle before T221 gate evaluation
- forbidden fields and privacy boundaries
- what T220 does not authorize

Write `docs/worker_summary/T220_worker_summary.md` with:

- files changed
- schema behavior added
- verification commands/results
- explicit non-actions
- remaining risks

Append a T220 implementation record to `docs/07_handoff.md`.

## Verification

Run:

```powershell
python -m py_compile src/practical_chat_agent/core/models.py
pytest tests/test_outbound_message_request_schema.py -q
pytest tests/test_behavior_schema.py tests/test_outbound_message_request_schema.py -q
pytest tests/ -q
```

If the Windows default temp directory is inaccessible in this sandbox, set `TEMP` and `TMP` to a workspace-local temp directory before running pytest and record that fact in `docs/07_handoff.md`.

## Docs To Update

- `docs/data_contracts/outbound_send_gate_contract.md`
- `docs/worker_summary/T220_worker_summary.md`
- `docs/07_handoff.md`

Do not update `docs/04_task_board.md`; Captain will mark completion after review.

## Reviewer Type

adversarial
