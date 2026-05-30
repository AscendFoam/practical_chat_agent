# T322: Chat Plus Memory Explanation Prototype

## Task ID

T322

## Goal

Create a local text-first chat/memory explanation prototype contract that
projects persona, memory viewer items, dialogue context, AIGC labels, and
crisis/dependency decisions into reviewable chat surface states.

## Why Now

T321 provides onboarding/persona creation states. The next M21 workflow should
show how the user experiences chat while still seeing memory provenance,
persona context, AI identity labels, and safety blocks. This should remain a
state/projection prototype before any browser UI or real reply generation.

## Allowed Files

Future T322 worker may create or modify only:

- `src/practical_chat_agent/ui/text_first_chat_memory.py`
- `tests/test_text_first_chat_memory_prototype.py`
- `docs/data_contracts/text_first_chat_memory_contract.md`
- `docs/tasks/M21_text_first_product_ux_prototype/T323_life_stream_prototype.md`
- `docs/worker_summary/T322_worker_summary.md`
- `docs/07_handoff.md`

If T322 needs browser UI, HTML/CSS, model-provider calls, private chat-log
processing, external APIs, platform adapters, outbound messaging, or task-board
edits, Captain must revise this package before assignment.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not call LLMs, model providers, external APIs, browser automation, or
  network services.
- Do not build a real frontend or browser demo in T322.
- Do not generate final companion replies.
- Do not mutate memory, persona, consent, or safety records.
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
- `docs/data_contracts/text_first_onboarding_contract.md`
- `docs/data_contracts/persona_card_v1_contract.md`
- `docs/data_contracts/memory_viewer_contract.md`
- `docs/data_contracts/dialogue_context_plan_contract.md`
- `docs/data_contracts/aigc_labeling_contract.md`
- `docs/data_contracts/crisis_dependency_policy_contract.md`
- `src/practical_chat_agent/core/models.py`
- `src/practical_chat_agent/services/dialogue_context_planner.py`
- `src/practical_chat_agent/services/companion_safety_policy.py`
- `tests/test_memory_viewer_contract.py`
- `tests/test_dialogue_context_planner.py`
- `tests/test_crisis_dependency_policy.py`

## Expected Outputs

### 1. Prototype State Contract

Implement a small local chat/memory state projection. Minimum behavior:

- exposes AI identity label on every chat state;
- includes persona summary and persona review status;
- includes current memory explanation items with truth status and provenance;
- separates factual and imagined memory;
- includes dialogue tone/pacing notes when supplied;
- blocks or de-escalates chat state when `CompanionSafetyPolicy` returns
  crisis/dependency risk;
- never generates final reply text;
- exposes no runtime chat, sending, scheduling, delivery, platform, webhook,
  token, or queue methods.

### 2. Tests

Create `tests/test_text_first_chat_memory_prototype.py` with RED/GREEN coverage
for:

- normal chat state includes AI identity label and persona summary;
- memory explanation includes factual/imagined separation and provenance;
- imagined memory cannot appear as factual evidence;
- crisis/dependency decision creates blocked/de-escalated state;
- payloads contain no raw private chat text and no delivery/platform fields.

### 3. Data Contract

Create `docs/data_contracts/text_first_chat_memory_contract.md` describing
fields, state transitions, invariants, non-actions, and verification.

### 4. Next Task Package

Create
`docs/tasks/M21_text_first_product_ux_prototype/T323_life_stream_prototype.md`
for life-stream prototype work.

### 5. Worker Summary And Handoff

Write `docs/worker_summary/T322_worker_summary.md` and append a T322 worker
record to `docs/07_handoff.md`.

Do not mark T322 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\ui\text_first_chat_memory.py src\practical_chat_agent\core\models.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_text_first_chat_memory_prototype.py tests\test_memory_viewer_contract.py tests\test_dialogue_context_planner.py tests\test_crisis_dependency_policy.py -q
```

```powershell
git diff --check
```

## Reviewer Type

Product/safety UX review recommended.

Reviewer should block if chat hides AI identity, hides memory provenance, treats
imagined memory as fact, generates final replies, or implies runtime/outbound
behavior.
