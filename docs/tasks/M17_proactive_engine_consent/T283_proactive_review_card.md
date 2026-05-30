# T283: Proactive Review Card

## Task ID

T283

## Goal

Create a local review-card schema/service for displaying proactive policy
decisions to a human reviewer. The review card should show candidate metadata,
policy decision, consent state, reason labels, and explicit review actions.

T283 must not schedule, send, deliver, enqueue, webhook, notify, or call any
platform adapter.

## Why Now

T280-T282 define consent and policy gates. The next step is a review artifact
that makes proactive suggestions inspectable before any future UI/demo work,
while preserving the invariant that proactive behavior is review-first and
cannot bypass human approval.

## Allowed Files

Future T283 worker may create or modify only:

- `src/practical_chat_agent/services/proactive_review_card.py`
- `tests/test_proactive_review_card.py`
- `docs/data_contracts/proactive_review_card_contract.md`
- `docs/tasks/M17_proactive_engine_consent/T284_crisis_low_mood_policy.md`
- `docs/worker_summary/T283_worker_summary.md`
- `docs/07_handoff.md`

If T283 needs model changes, candidate generators, schedulers, delivery
adapters, platform integration, UI, or task-board edits, Captain must revise
this package before assignment.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not call LLMs, model providers, external APIs, browser automation, or
  network services.
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

- `docs/data_contracts/proactive_consent_contract.md`
- `docs/data_contracts/proactive_policy_gate_contract.md`
- `src/practical_chat_agent/services/proactive_policy_gate.py`
- `tests/test_proactive_policy_gate.py`
- `tests/test_proactive_quiet_hours_frequency.py`

## Expected Outputs

### 1. Review Card

Create `src/practical_chat_agent/services/proactive_review_card.py`.

Minimum expected objects:

- review card model with `card_id`, candidate id, decision id, decision,
  reasons, review actions, consent status, and safety notes;
- service that renders a review card from `ProactiveConsent`,
  `ProactiveCandidateMetadata`, and `ProactivePolicyDecision`;
- review actions such as `approve_for_draft`, `reject`, `pause_consent`, and
  `request_changes`.

Minimum expected behavior:

- allow-for-review decisions show approval-oriented review actions;
- block/defer decisions do not expose direct approval as a final-send action;
- all cards state that human review is required;
- card payload contains no send, schedule, delivery, platform, webhook, token,
  or queue fields;
- service exposes no send/schedule/delivery/runtime methods.

### 2. Tests

Add `tests/test_proactive_review_card.py` covering:

- allow-for-review decision renders review-required card;
- block/defer decisions render conservative actions;
- policy reasons and consent status are preserved;
- forbidden delivery/platform fields are absent;
- service exposes no send/schedule/delivery/runtime methods.

### 3. Data Contract

Create `docs/data_contracts/proactive_review_card_contract.md` describing card
fields, rendering rules, non-actions, and verification.

### 4. Next Task Package

Create `docs/tasks/M17_proactive_engine_consent/T284_crisis_low_mood_policy.md`
for crisis/low-mood scenario policy. T284 should block manipulation and route
high-risk scenarios to support-oriented review notes only.

### 5. Worker Summary And Handoff

Write `docs/worker_summary/T283_worker_summary.md` and append a T283 worker
record to `docs/07_handoff.md`.

Do not mark T283 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\services\proactive_review_card.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_proactive_review_card.py tests\test_proactive_policy_gate.py tests\test_proactive_quiet_hours_frequency.py -q
```

```powershell
git diff --check
```

## Reviewer Type

Adversarial review recommended.

Reviewer should verify that T283 creates review artifacts only and cannot
schedule, send, deliver, enqueue, webhook, notify, or integrate with platforms.
