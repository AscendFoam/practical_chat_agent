# T325: User Study Protocol

## Task ID

T325

## Goal

Create a text-first prototype user study protocol for M21 that evaluates
whether the onboarding, persona, chat/memory, life stream, proactive settings,
and controls concepts are understandable, desirable, and safe enough for later
web-demo work.

## Why Now

T320-T324 define M21 product states. Before building a browser demo, the project
needs a study protocol that tests whether users understand AI identity,
persona-source boundaries, memory provenance, AIGC labels, proactive consent,
and crisis/dependency safety states.

## Allowed Files

Future T325 worker may create or modify only:

- `docs/product/text_first_user_study_protocol.md`
- `docs/tasks/M21_text_first_product_ux_prototype/T326_m21_milestone_review.md`
- `docs/worker_summary/T325_worker_summary.md`
- `docs/07_handoff.md`

If T325 needs code, UI implementation, browser automation, model-provider
calls, real user recruitment, private data processing, external surveys,
platform adapters, outbound messaging, or task-board edits, Captain must revise
this package before assignment.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not call LLMs, model providers, external APIs, browser automation, or
  network services.
- Do not run a real user study or collect participant data.
- Do not build UI or a browser demo.
- Do not generate real companion replies.
- Do not publish, send, deliver, enqueue, webhook, notify, or call platform
  adapters.
- Do not claim legal advice, compliance completion, crisis-safety sufficiency,
  clinical validation, launch approval, app-store approval, or regulator
  acceptance.
- Do not modify `docs/04_task_board.md`, `docs/05_decision_log.md`,
  `docs/06_eval_protocol.md`, or `docs/08_risks_and_open_questions.md`.

## Inputs To Read

Required:

- `docs/product/text_first_ux_information_architecture.md`
- `docs/data_contracts/text_first_onboarding_contract.md`
- `docs/data_contracts/text_first_chat_memory_contract.md`
- `docs/data_contracts/text_first_life_stream_contract.md`
- `docs/data_contracts/text_first_proactive_settings_contract.md`
- `docs/data_contracts/consent_center_contract.md`
- `docs/data_contracts/aigc_labeling_contract.md`
- `docs/data_contracts/crisis_dependency_policy_contract.md`
- `docs/review/M20_review.md`

## Expected Outputs

### 1. Study Protocol

Create `docs/product/text_first_user_study_protocol.md` with:

- study goals;
- target participant assumptions;
- prototype surfaces to test;
- tasks/scenarios;
- comprehension checks for AI identity, persona boundaries, memory provenance,
  AIGC labels, proactive consent, and crisis/dependency states;
- qualitative interview questions;
- quantitative success metrics;
- safety stop criteria;
- data collection boundaries;
- explicit non-actions.

### 2. Next Task Package

Create
`docs/tasks/M21_text_first_product_ux_prototype/T326_m21_milestone_review.md`
for M21 milestone review.

### 3. Worker Summary And Handoff

Write `docs/worker_summary/T325_worker_summary.md` and append a T325 worker
record to `docs/07_handoff.md`.

Do not mark T325 complete in `docs/04_task_board.md`.

## Verification

Minimum command:

```powershell
git diff --check
```

## Reviewer Type

Product/safety research review recommended.

Reviewer should block if the protocol collects private chat data, recruits real
participants without approval, hides AI identity/safety comprehension checks, or
claims clinical/legal validation.
