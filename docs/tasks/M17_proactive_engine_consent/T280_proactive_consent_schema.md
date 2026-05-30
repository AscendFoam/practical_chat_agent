# T280: Proactive Consent Schema

## Task ID

T280

## Goal

Define a local `ProactiveConsent` schema for explicit, review-first proactive
companionship permissions. The schema should capture whether proactive
suggestions are allowed, where they may appear, quiet hours, frequency caps,
allowed intent categories, pause/revocation state, and review requirements.

T280 must not generate proactive candidates, schedule messages, send messages,
or integrate with any external platform.

## Why Now

M16 created local relationship/dialogue context and review-only draft stubs.
Before any proactive companion behavior can exist, the project needs a consent
contract that makes proactive behavior opt-in, rate-limited, pauseable,
revocable, and restricted to in-app review surfaces.

## Allowed Files

Future T280 worker may create or modify only:

- `src/practical_chat_agent/core/models.py`
- `tests/test_proactive_consent_schema.py`
- `docs/data_contracts/proactive_consent_contract.md`
- `docs/tasks/M17_proactive_engine_consent/T281_proactive_policy_gate.md`
- `docs/worker_summary/T280_worker_summary.md`
- `docs/07_handoff.md`

If T280 needs services, schedulers, candidate generators, platform adapters, UI,
or task-board edits, Captain must revise this package before assignment.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not call LLMs, model providers, external APIs, browser automation, or
  network services.
- Do not implement proactive candidate generation.
- Do not implement scheduling, delivery, automatic sending, outbound requests,
  push notifications, webhook calls, platform adapters, or message queues.
- Do not implement production reply generation, voice/avatar/video behavior,
  social feed generation, or web demo.
- Do not implement real-person clone behavior, deceased-person simulation,
  public-figure simulation, or deceptive impersonation paths.
- Do not modify `docs/04_task_board.md`, `docs/05_decision_log.md`,
  `docs/06_eval_protocol.md`, or `docs/08_risks_and_open_questions.md`.

## Inputs To Read

Required:

- `docs/review/M16_review.md`
- `docs/data_contracts/dialogue_draft_stub_contract.md`
- `src/practical_chat_agent/core/models.py`
- `docs/04_task_board.md` M17 section only

Optional:

- `docs/worker_summary/T270_worker_summary.md`
- `docs/worker_summary/T271_worker_summary.md`
- `docs/worker_summary/T272_worker_summary.md`

## Expected Outputs

### 1. Schema And Tests

Add `ProactiveConsent` to `src/practical_chat_agent/core/models.py`.

Minimum expected fields:

- `schema_version`;
- `consent_id`;
- `user_id`;
- `status` such as `disabled`, `enabled`, or `paused`;
- `allowed_surfaces`, restricted to local in-app review surfaces for now;
- `allowed_intents`, restricted to low-pressure companion intent labels;
- `quiet_hours`;
- `max_suggestions_per_day`;
- `min_interval_hours`;
- `requires_human_review`, defaulting to true;
- `pause_reasons`;
- `revoked_at`;
- `safety_notes`.

Minimum invariants:

- outbound/platform surfaces are rejected;
- `requires_human_review=false` is rejected;
- negative frequency or interval values are rejected;
- enabled consent must include at least one allowed intent;
- paused/revoked consent must remain representable without enabling runtime
  behavior;
- serialized consent contains no send, schedule, delivery, platform, webhook,
  token, or queue fields.

### 2. Data Contract

Create `docs/data_contracts/proactive_consent_contract.md` describing the schema,
invariants, explicit non-actions, and verification.

### 3. Next Task Package

Create `docs/tasks/M17_proactive_engine_consent/T281_proactive_policy_gate.md`.
T281 should consume `ProactiveConsent` and make deterministic allow/block/review
decisions for already-provided candidate metadata. It should not create
candidates or send messages.

### 4. Worker Summary And Handoff

Write `docs/worker_summary/T280_worker_summary.md` and append a T280 worker
record to `docs/07_handoff.md`.

Do not mark T280 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\core\models.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_proactive_consent_schema.py -q
```

```powershell
git diff --check
```

## Reviewer Type

Adversarial review recommended.

Reviewer should verify that T280 defines consent and review boundaries only,
not proactive generation, scheduling, delivery, automatic sending, platform
integration, or UI behavior.
