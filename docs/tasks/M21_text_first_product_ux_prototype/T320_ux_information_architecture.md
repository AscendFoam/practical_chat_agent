# T320: UX Information Architecture

## Task ID

T320

## Goal

Define the text-first product UX information architecture for the companion
prototype before building screens. The IA should connect persona creation,
chat, memory explanation, virtual life stream, proactive settings, consent/data
controls, AIGC labels, and crisis/dependency safety states into one coherent
review-first product flow.

## Why Now

M13-M19 established positioning, persona, memory, dialogue, virtual life,
proactive, and control contracts. M20 added compliance and safety baselines.
M21 can now begin user-facing product UX work, but the first step should be a
clear navigation/state model so the prototype does not bury consent, AI identity
labels, safety gates, or data controls.

## Allowed Files

Future T320 worker may create or modify only:

- `docs/product/text_first_ux_information_architecture.md`
- `docs/tasks/M21_text_first_product_ux_prototype/T321_onboarding_persona_creation_prototype.md`
- `docs/worker_summary/T320_worker_summary.md`
- `docs/07_handoff.md`

If T320 needs code, UI implementation, screenshots, browser automation, model
calls, platform adapters, outbound messaging, or task-board edits, Captain must
revise this package before assignment.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not call LLMs, model providers, external APIs, browser automation, or
  network services.
- Do not build UI or frontend code.
- Do not generate real companion messages from private data.
- Do not export/share/download content.
- Do not publish, send, deliver, enqueue, webhook, notify, or call platform
  adapters.
- Do not claim legal advice, compliance completion, crisis-safety sufficiency,
  clinical validation, launch approval, app-store approval, or regulator
  acceptance.
- Do not modify `docs/04_task_board.md`, `docs/05_decision_log.md`,
  `docs/06_eval_protocol.md`, or `docs/08_risks_and_open_questions.md`.

## Inputs To Read

Required:

- `docs/product/M13_commercial_companion_positioning.md`
- `docs/product/M13_competitor_matrix.md`
- `docs/review/M20_review.md`
- `docs/data_contracts/persona_card_v1_contract.md`
- `docs/data_contracts/persona_compiler_contract.md`
- `docs/data_contracts/memory_viewer_contract.md`
- `docs/data_contracts/dialogue_context_plan_contract.md`
- `docs/data_contracts/reply_plan_contract.md`
- `docs/data_contracts/virtual_life_engine_contract.md`
- `docs/data_contracts/proactive_consent_contract.md`
- `docs/data_contracts/proactive_policy_gate_contract.md`
- `docs/data_contracts/consent_center_contract.md`
- `docs/data_contracts/aigc_labeling_contract.md`
- `docs/data_contracts/crisis_dependency_policy_contract.md`

Optional:

- `docs/reference/和gpt-pro的对话.md`
- `docs/reference/gpt-pro关于后续从M13开始的计划分析.md`

## Expected Outputs

### 1. UX Information Architecture

Create `docs/product/text_first_ux_information_architecture.md` with:

- target user and product mode assumptions;
- top-level navigation;
- first-run onboarding flow;
- persona creation and persona evolution states;
- chat surface and memory explanation states;
- virtual life/social-feed surface states;
- proactive settings and review states;
- consent/data-control states;
- AIGC and synthetic-content label placement;
- crisis/dependency safety states;
- empty/loading/error/review-blocked states;
- explicit non-actions.

### 2. M21 Next Task Package

Create
`docs/tasks/M21_text_first_product_ux_prototype/T321_onboarding_persona_creation_prototype.md`
for onboarding/persona creation prototype work.

### 3. Worker Summary And Handoff

Write `docs/worker_summary/T320_worker_summary.md` and append a T320 worker
record to `docs/07_handoff.md`.

Do not mark T320 complete in `docs/04_task_board.md`.

## Verification

Minimum command:

```powershell
git diff --check
```

## Reviewer Type

Product/safety UX review recommended.

Reviewer should block if IA hides AI identity, consent/data controls, AIGC
labels, memory provenance, or crisis/dependency safety states.
