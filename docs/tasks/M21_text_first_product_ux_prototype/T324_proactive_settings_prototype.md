# T324: Proactive Settings Prototype

## Task ID

T324

## Goal

Create a local text-first proactive settings prototype contract that projects
`ProactiveConsent`, proactive policy decisions, quiet-hours/frequency state,
and crisis/dependency blocks into a reviewable settings surface.

## Why Now

T323 covers the virtual life stream. The next M21 surface is proactive
settings, because proactive companionship is a key product goal but must remain
consented, local-review-only, rate-limited, easy to pause/revoke, and blocked
under crisis/dependency risk.

## Allowed Files

Future T324 worker may create or modify only:

- `src/practical_chat_agent/ui/text_first_proactive_settings.py`
- `tests/test_text_first_proactive_settings_prototype.py`
- `docs/data_contracts/text_first_proactive_settings_contract.md`
- `docs/tasks/M21_text_first_product_ux_prototype/T325_user_study_protocol.md`
- `docs/worker_summary/T324_worker_summary.md`
- `docs/07_handoff.md`

If T324 needs browser UI, HTML/CSS, model-provider calls, private chat-log
processing, external APIs, platform adapters, outbound messaging, or task-board
edits, Captain must revise this package before assignment.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not call LLMs, model providers, external APIs, browser automation, or
  network services.
- Do not build a real frontend or browser demo in T324.
- Do not generate proactive candidates.
- Do not schedule, send, deliver, enqueue, webhook, notify, or call platform
  adapters.
- Do not mutate consent records.
- Do not claim legal advice, compliance completion, crisis-safety sufficiency,
  clinical validation, launch approval, app-store approval, or regulator
  acceptance.
- Do not modify `docs/04_task_board.md`, `docs/05_decision_log.md`,
  `docs/06_eval_protocol.md`, or `docs/08_risks_and_open_questions.md`.

## Inputs To Read

Required:

- `docs/product/text_first_ux_information_architecture.md`
- `docs/data_contracts/proactive_consent_contract.md`
- `docs/data_contracts/proactive_policy_gate_contract.md`
- `docs/data_contracts/crisis_dependency_policy_contract.md`
- `src/practical_chat_agent/core/models.py`
- `src/practical_chat_agent/services/proactive_policy_gate.py`
- `src/practical_chat_agent/services/companion_safety_policy.py`
- `tests/test_proactive_consent_schema.py`
- `tests/test_proactive_policy_gate.py`
- `tests/test_crisis_dependency_policy.py`

## Expected Outputs

### 1. Prototype State Contract

Implement a small local proactive settings projection. Minimum behavior:

- shows disabled, enabled, paused, and revoked consent states;
- shows allowed local review surfaces and low-pressure intents;
- shows quiet hours, max suggestions per day, minimum interval, and
  no-response pressure guard;
- projects proactive policy decisions into allowed-for-review, blocked, or
  deferred states;
- blocks/de-emphasizes proactive behavior under crisis/dependency risk;
- exposes no candidate generation, scheduling, sending, delivery, platform,
  webhook, token, or queue methods.

### 2. Tests

Create `tests/test_text_first_proactive_settings_prototype.py` with RED/GREEN
coverage for:

- disabled/paused/revoked consent appears as disabled or blocked settings;
- enabled consent displays allowed review surfaces, intents, quiet hours, and
  frequency limits;
- policy gate block/defer/allow decisions are reflected without sending;
- crisis/dependency reasons keep proactive outreach blocked;
- payloads contain no raw private chat text and no delivery/platform fields.

### 3. Data Contract

Create `docs/data_contracts/text_first_proactive_settings_contract.md`
describing fields, state transitions, invariants, non-actions, and
verification.

### 4. Next Task Package

Create
`docs/tasks/M21_text_first_product_ux_prototype/T325_user_study_protocol.md`
for user study protocol work.

### 5. Worker Summary And Handoff

Write `docs/worker_summary/T324_worker_summary.md` and append a T324 worker
record to `docs/07_handoff.md`.

Do not mark T324 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\ui\text_first_proactive_settings.py src\practical_chat_agent\core\models.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_text_first_proactive_settings_prototype.py tests\test_proactive_consent_schema.py tests\test_proactive_policy_gate.py tests\test_crisis_dependency_policy.py -q
```

```powershell
git diff --check
```

## Reviewer Type

Product/safety UX review recommended.

Reviewer should block if settings imply automatic sending, hide consent state,
hide crisis/dependency blocks, or expose outbound/runtime behavior.
