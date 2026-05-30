# T321: Onboarding And Persona Creation Prototype

## Task ID

T321

## Goal

Create a local, text-first onboarding/persona creation prototype contract that
turns the T320 information architecture into executable state transitions for
safe persona creation modes.

## Why Now

T320 defines the navigation and state model for M21. The first user-facing
workflow should be onboarding and persona creation because every later surface
depends on a reviewed persona card, AI identity disclosure, source/risk policy,
consent state, and blocked-real-person boundaries.

## Allowed Files

Future T321 worker may create or modify only:

- `src/practical_chat_agent/ui/text_first_onboarding.py`
- `tests/test_text_first_onboarding_prototype.py`
- `docs/data_contracts/text_first_onboarding_contract.md`
- `docs/tasks/M21_text_first_product_ux_prototype/T322_chat_memory_explanation_prototype.md`
- `docs/worker_summary/T321_worker_summary.md`
- `docs/07_handoff.md`

If T321 needs browser UI, HTML/CSS, model-provider calls, private chat-log
processing, external APIs, platform adapters, outbound messaging, or task-board
edits, Captain must revise this package before assignment.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not call LLMs, model providers, external APIs, browser automation, or
  network services.
- Do not build a real frontend or browser demo in T321.
- Do not generate real companion replies.
- Do not process real persona distillation from private chat logs.
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

- `docs/product/text_first_ux_information_architecture.md`
- `docs/data_contracts/persona_card_v1_contract.md`
- `docs/data_contracts/persona_compiler_contract.md`
- `docs/data_contracts/consent_center_contract.md`
- `docs/data_contracts/aigc_labeling_contract.md`
- `docs/data_contracts/crisis_dependency_policy_contract.md`
- `src/practical_chat_agent/services/persona_compiler.py`
- `src/practical_chat_agent/core/models.py`
- `tests/test_persona_compiler.py`
- `tests/test_consent_center_data_model.py`
- `tests/test_aigc_labeling_plan_contract.py`

## Expected Outputs

### 1. Prototype State Contract

Implement a small local onboarding state/projection module. Minimum behavior:

- exposes AI identity disclosure as the first state;
- supports detailed description, fuzzy preference, template, and random seed
  creation modes;
- keeps de-identified style inspiration locked unless future consent and
  deidentification gates are present;
- uses existing `PersonaCompilerService` for safe synthetic persona drafts;
- surfaces rejected real-person/clone requests as blocked states;
- attaches AIGC label requirements to persona/virtual-history preview;
- requires consent review for memory/proactive/export-share scopes;
- exposes no runtime chat, sending, scheduling, delivery, platform, webhook,
  token, or queue methods.

### 2. Tests

Create `tests/test_text_first_onboarding_prototype.py` with RED/GREEN coverage
for:

- first state is AI identity disclosure;
- safe creation modes produce draft persona review state;
- clone/deceased/public-figure style requests produce blocked state;
- style inspiration mode is locked by default;
- persona preview carries visible AIGC labeling;
- payloads contain no raw private chat text and no delivery/platform fields.

### 3. Data Contract

Create `docs/data_contracts/text_first_onboarding_contract.md` describing
fields, state transitions, invariants, non-actions, and verification.

### 4. Next Task Package

Create
`docs/tasks/M21_text_first_product_ux_prototype/T322_chat_memory_explanation_prototype.md`
for chat plus memory explanation prototype work.

### 5. Worker Summary And Handoff

Write `docs/worker_summary/T321_worker_summary.md` and append a T321 worker
record to `docs/07_handoff.md`.

Do not mark T321 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\ui\text_first_onboarding.py src\practical_chat_agent\services\persona_compiler.py src\practical_chat_agent\core\models.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_text_first_onboarding_prototype.py tests\test_persona_compiler.py tests\test_aigc_labeling_plan_contract.py tests\test_consent_center_data_model.py -q
```

```powershell
git diff --check
```

## Reviewer Type

Product/safety UX review recommended.

Reviewer should block if onboarding hides AI identity, allows real-person clone
requests, unlocks style inspiration without gates, omits AIGC labels, or implies
runtime chat/outbound behavior.
