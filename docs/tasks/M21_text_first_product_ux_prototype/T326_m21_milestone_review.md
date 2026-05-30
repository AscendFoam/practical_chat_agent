# T326: M21 Milestone Review

## Task ID

T326

## Goal

Perform an adversarial M21 milestone review for the Text-First Product UX
Prototype work. The review should verify that M21 provides information
architecture, local onboarding/persona states, chat/memory states, life-stream
states, proactive settings states, and user-study protocol without claiming
browser-demo readiness, launch readiness, platform integration, or real user
validation.

## Why Now

T320-T325 complete the planned M21 text-first UX prototype contracts. M21 needs
a gate review before entering M22 voice/avatar exploration because voice/avatar
work raises consent, biometric, synthetic media, labeling, and deception risk.

## Allowed Files

Future T326 worker may create or modify only:

- `docs/review/M21_review.md`
- `docs/tasks/M22_voice_and_avatar_exploration/T330_voice_technology_survey.md`
- `docs/worker_summary/T326_worker_summary.md`
- `docs/07_handoff.md`

If T326 needs code, tests, UI implementation, browser automation,
model-provider calls, private data processing, external surveys, platform
adapters, outbound messaging, or task-board edits, Captain must revise this
package before assignment.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not call LLMs, model providers, external APIs, browser automation, or
  network services.
- Do not build UI or a browser demo.
- Do not run a real user study or collect participant data.
- Do not publish, send, deliver, enqueue, webhook, notify, or call platform
  adapters.
- Do not claim legal advice, compliance completion, crisis-safety sufficiency,
  clinical validation, user-study validation, launch approval, app-store
  approval, or regulator acceptance.
- Do not modify `docs/04_task_board.md`, `docs/05_decision_log.md`,
  `docs/06_eval_protocol.md`, or `docs/08_risks_and_open_questions.md`.

## Inputs To Read

Required:

- `docs/product/text_first_ux_information_architecture.md`
- `docs/product/text_first_user_study_protocol.md`
- `docs/data_contracts/text_first_onboarding_contract.md`
- `docs/data_contracts/text_first_chat_memory_contract.md`
- `docs/data_contracts/text_first_life_stream_contract.md`
- `docs/data_contracts/text_first_proactive_settings_contract.md`
- `docs/worker_summary/T320_worker_summary.md`
- `docs/worker_summary/T321_worker_summary.md`
- `docs/worker_summary/T322_worker_summary.md`
- `docs/worker_summary/T323_worker_summary.md`
- `docs/worker_summary/T324_worker_summary.md`
- `docs/worker_summary/T325_worker_summary.md`
- `tests/test_text_first_onboarding_prototype.py`
- `tests/test_text_first_chat_memory_prototype.py`
- `tests/test_text_first_life_stream_prototype.py`
- `tests/test_text_first_proactive_settings_prototype.py`

## Expected Outputs

### 1. M21 Review

Create `docs/review/M21_review.md` with:

- gate recommendation: `PASS`, `PASS_WITH_WARNINGS`, or `BLOCK`;
- task coverage table for T320-T325;
- implemented code and data contracts;
- verification evidence;
- UX/safety boundary assessment;
- explicit non-actions;
- residual risks;
- M22 entry recommendation.

### 2. M22 Entry Task Package

Create
`docs/tasks/M22_voice_and_avatar_exploration/T330_voice_technology_survey.md`
for voice technology survey work.

### 3. Worker Summary And Handoff

Write `docs/worker_summary/T326_worker_summary.md` and append a T326 worker
record to `docs/07_handoff.md`.

Do not mark T326 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'
pytest tests\test_text_first_onboarding_prototype.py tests\test_text_first_chat_memory_prototype.py tests\test_text_first_life_stream_prototype.py tests\test_text_first_proactive_settings_prototype.py -q
```

```powershell
git diff --check
```

## Reviewer Type

Adversarial product/safety UX review required.

Reviewer should mark M21 as `PASS_WITH_WARNINGS` only if the work remains local,
review-first, test-covered, and explicit about no browser demo or launch
readiness. Reviewer should `BLOCK` if a later diff hides AI identity, memory
provenance, AIGC labels, consent controls, crisis/dependency blocks, or implies
runtime/outbound behavior.
