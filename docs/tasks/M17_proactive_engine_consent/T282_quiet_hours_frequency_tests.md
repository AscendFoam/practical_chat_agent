# T282: Quiet-Hours And Frequency Edge Tests

## Task ID

T282

## Goal

Expand proactive policy test coverage for quiet hours, frequency caps,
minimum intervals, and no-response windows using deterministic synthetic
scenarios. T282 should strengthen the policy boundary before review-card work.

T282 must not generate proactive candidates, schedule messages, send messages,
or integrate with external platforms.

## Why Now

T281 adds the first deterministic policy gate. Before creating review cards,
M17 needs more adversarial edge coverage for the cases most likely to create
unwanted pressure: late-night prompts, too-frequent check-ins, repeated
follow-ups after no response, and rapid retries.

## Allowed Files

Future T282 worker may create or modify only:

- `src/practical_chat_agent/services/proactive_policy_gate.py`
- `tests/test_proactive_policy_gate.py`
- `tests/test_proactive_quiet_hours_frequency.py`
- `docs/data_contracts/proactive_policy_gate_contract.md`
- `docs/tasks/M17_proactive_engine_consent/T283_proactive_review_card.md`
- `docs/worker_summary/T282_worker_summary.md`
- `docs/07_handoff.md`

If T282 needs model changes, candidate generators, schedulers, delivery
adapters, UI, or task-board edits, Captain must revise this package before
assignment.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not call LLMs, model providers, external APIs, browser automation, or
  network services.
- Do not create proactive candidate generators.
- Do not schedule, send, deliver, enqueue, webhook, notify, or call platform
  adapters.
- Do not implement production reply generation, voice/avatar/video behavior,
  social feed generation, or web demo.
- Do not implement real-person clone behavior or deceptive impersonation paths.
- Do not modify `docs/04_task_board.md`, `docs/05_decision_log.md`,
  `docs/06_eval_protocol.md`, or `docs/08_risks_and_open_questions.md`.

## Inputs To Read

Required:

- `docs/data_contracts/proactive_consent_contract.md`
- `docs/data_contracts/proactive_policy_gate_contract.md`
- `src/practical_chat_agent/services/proactive_policy_gate.py`
- `tests/test_proactive_policy_gate.py`
- `tests/test_proactive_consent_schema.py`

## Expected Outputs

### 1. Expanded Tests

Add or update tests covering:

- quiet hours defer allowed candidates;
- daily cap exact-boundary behavior;
- daily cap below-boundary behavior;
- minimum interval exact-boundary behavior;
- minimum interval below-boundary behavior;
- no-response follow-up count or no-response window blocks pressure;
- all decisions still require review;
- decision payloads remain free of delivery/platform fields.

### 2. Policy Gate Update If Needed

Update `ProactivePolicyGate` only where needed to make the expanded tests pass.
Any added behavior must remain deterministic and local.

### 3. Contract Update

Update `docs/data_contracts/proactive_policy_gate_contract.md` to describe any
new no-response or edge-case reason labels.

### 4. Next Task Package

Create `docs/tasks/M17_proactive_engine_consent/T283_proactive_review_card.md`
for review-card schema/service work. T283 should render policy decisions for
human review only and must not send messages.

### 5. Worker Summary And Handoff

Write `docs/worker_summary/T282_worker_summary.md` and append a T282 worker
record to `docs/07_handoff.md`.

Do not mark T282 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\services\proactive_policy_gate.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_proactive_policy_gate.py tests\test_proactive_quiet_hours_frequency.py tests\test_proactive_consent_schema.py -q
```

```powershell
git diff --check
```

## Reviewer Type

Adversarial review recommended.

Reviewer should verify that T282 expands safety tests and local deterministic
policy only, without candidate generation, scheduling, delivery, automatic
sending, platform integration, or UI behavior.
