# T284: Crisis And Low-Mood Proactive Policy

## Task ID

T284

## Goal

Add deterministic crisis and low-mood safety policy handling for proactive
candidate metadata and review cards. High-risk candidate flags should block
normal proactive behavior and produce support-oriented review notes only.

T284 must not schedule, send, deliver, enqueue, webhook, notify, or call any
platform adapter.

## Why Now

T280-T283 define consent, policy gating, edge tests, and local review cards.
Before M17 can close, the proactive system needs explicit handling for
emotionally vulnerable scenarios so it cannot exploit low mood, dependency, or
crisis-like signals.

## Allowed Files

Future T284 worker may create or modify only:

- `src/practical_chat_agent/services/proactive_policy_gate.py`
- `src/practical_chat_agent/services/proactive_review_card.py`
- `tests/test_proactive_crisis_low_mood_policy.py`
- `docs/data_contracts/proactive_policy_gate_contract.md`
- `docs/data_contracts/proactive_review_card_contract.md`
- `docs/tasks/M17_proactive_engine_consent/T285_m17_gate_review.md`
- `docs/worker_summary/T284_worker_summary.md`
- `docs/07_handoff.md`

If T284 needs model changes, candidate generators, schedulers, delivery
adapters, platform integration, UI, or task-board edits, Captain must revise
this package before assignment.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not call LLMs, model providers, external APIs, browser automation, or
  network services.
- Do not diagnose, triage, or provide medical/mental-health advice.
- Do not generate proactive candidates.
- Do not schedule, send, deliver, enqueue, webhook, notify, create outbound
  requests, or call platform adapters.
- Do not implement production reply generation, voice/avatar/video behavior,
  social feed generation, or web demo.
- Do not implement real-person clone behavior or deceptive impersonation paths.
- Do not modify `docs/04_task_board.md`, `docs/05_decision_log.md`,
  `docs/06_eval_protocol.md`, or `docs/08_risks_and_open_questions.md`.

## Inputs To Read

Required:

- `docs/data_contracts/proactive_policy_gate_contract.md`
- `docs/data_contracts/proactive_review_card_contract.md`
- `src/practical_chat_agent/services/proactive_policy_gate.py`
- `src/practical_chat_agent/services/proactive_review_card.py`
- `tests/test_proactive_policy_gate.py`
- `tests/test_proactive_review_card.py`

## Expected Outputs

### 1. Crisis/Low-Mood Tests

Add `tests/test_proactive_crisis_low_mood_policy.py` covering:

- crisis-like safety flag blocks normal proactive approval;
- low-mood vulnerability flag blocks pressure or dependency-oriented actions;
- review card for high-risk decisions exposes support-oriented conservative
  actions only;
- safety notes are preserved in cards;
- no medical advice, diagnosis, emergency handling claims, or delivery/platform
  fields are introduced.

### 2. Policy Update If Needed

Update `ProactivePolicyGate` only where needed to block high-risk safety flags
with deterministic reasons such as:

- `crisis_safety_review_required`;
- `low_mood_pressure_risk`;
- `dependency_pressure_risk`.

### 3. Review Card Update If Needed

Update `ProactiveReviewCardService` only where needed to surface
support-oriented review actions or notes. It must not add sending, scheduling,
delivery, notification, or external escalation behavior.

### 4. Contracts

Update proactive policy and review-card contracts with any new reason labels,
actions, and non-actions.

### 5. Next Task Package

Create `docs/tasks/M17_proactive_engine_consent/T285_m17_gate_review.md` for
M17 milestone review.

### 6. Worker Summary And Handoff

Write `docs/worker_summary/T284_worker_summary.md` and append a T284 worker
record to `docs/07_handoff.md`.

Do not mark T284 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\services\proactive_policy_gate.py src\practical_chat_agent\services\proactive_review_card.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_proactive_crisis_low_mood_policy.py tests\test_proactive_review_card.py tests\test_proactive_policy_gate.py -q
```

```powershell
git diff --check
```

## Reviewer Type

Adversarial review recommended.

Reviewer should verify that T284 blocks high-risk proactive behavior and does
not create diagnosis, treatment, emergency-response, sending, scheduling,
delivery, notification, platform, or escalation behavior.
