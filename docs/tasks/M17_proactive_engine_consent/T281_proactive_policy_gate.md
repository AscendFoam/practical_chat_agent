# T281: Proactive Policy Gate

## Task ID

T281

## Goal

Implement a deterministic local `ProactivePolicyGate` that consumes
`ProactiveConsent` plus already-provided proactive candidate metadata and
returns an allow/block/review decision. The gate must enforce consent status,
local review surfaces, low-pressure intents, quiet-hours metadata, frequency
caps, minimum intervals, and required human review.

T281 must not create proactive candidates, schedule messages, send messages, or
integrate with external platforms.

## Why Now

T280 defines consent boundaries. The next step is a local policy gate that can
evaluate candidate metadata before any future review card or UI work. This
keeps proactive behavior opt-in, review-first, rate-limited, and blocked from
outbound delivery.

## Allowed Files

Future T281 worker may create or modify only:

- `src/practical_chat_agent/services/proactive_policy_gate.py`
- `tests/test_proactive_policy_gate.py`
- `docs/data_contracts/proactive_policy_gate_contract.md`
- `docs/tasks/M17_proactive_engine_consent/T282_quiet_hours_frequency_tests.md`
- `docs/worker_summary/T281_worker_summary.md`
- `docs/07_handoff.md`

If T281 needs model changes, candidate generators, schedulers, delivery
adapters, UI, or task-board edits, Captain must revise this package before
assignment.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not call LLMs, model providers, external APIs, browser automation, or
  network services.
- Do not generate proactive candidates.
- Do not schedule messages, send messages, create outbound requests, push
  notifications, webhooks, queues, or platform adapter calls.
- Do not implement production reply generation, voice/avatar/video behavior,
  social feed generation, or web demo.
- Do not implement real-person clone behavior or deceptive impersonation paths.
- Do not modify `docs/04_task_board.md`, `docs/05_decision_log.md`,
  `docs/06_eval_protocol.md`, or `docs/08_risks_and_open_questions.md`.

## Inputs To Read

Required:

- `docs/data_contracts/proactive_consent_contract.md`
- `docs/review/M16_review.md`
- `src/practical_chat_agent/core/models.py` ProactiveConsent section
- `tests/test_proactive_consent_schema.py`

## Expected Outputs

### 1. Policy Gate

Create `src/practical_chat_agent/services/proactive_policy_gate.py`.

Minimum expected objects:

- candidate metadata model or typed input accepted by the gate;
- decision model with `decision`, `reasons`, `review_required`, and
  `allowed_surface`;
- `ProactivePolicyGate.evaluate(consent, candidate, recent_sent_count,
  hours_since_last_suggestion, is_quiet_hours)` or equivalent deterministic
  entry point.

Minimum expected behavior:

- disabled, paused, and revoked consent block;
- unknown or outbound surfaces block;
- disallowed intents block;
- quiet hours block or defer;
- frequency caps block;
- minimum interval violations block;
- all allowed decisions still require human review;
- decision payload contains no send, schedule, delivery, platform, webhook,
  token, or queue fields.

### 2. Tests

Add `tests/test_proactive_policy_gate.py` covering:

- enabled consent with low-pressure candidate yields review-required allow;
- disabled/paused/revoked consent blocks;
- outbound surface and disallowed intent block;
- quiet-hours, frequency-cap, and minimum-interval cases block;
- gate exposes no send/schedule/delivery/runtime methods.

### 3. Data Contract

Create `docs/data_contracts/proactive_policy_gate_contract.md` describing the
gate input/output, deterministic rules, non-actions, and verification.

### 4. Next Task Package

Create
`docs/tasks/M17_proactive_engine_consent/T282_quiet_hours_frequency_tests.md`
for expanded edge-case tests around quiet hours, no-response windows, and
frequency limits.

### 5. Worker Summary And Handoff

Write `docs/worker_summary/T281_worker_summary.md` and append a T281 worker
record to `docs/07_handoff.md`.

Do not mark T281 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\services\proactive_policy_gate.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_proactive_policy_gate.py tests\test_proactive_consent_schema.py -q
```

```powershell
git diff --check
```

## Reviewer Type

Adversarial review recommended.

Reviewer should verify that T281 is policy gating only and cannot create,
schedule, send, or deliver proactive messages.
