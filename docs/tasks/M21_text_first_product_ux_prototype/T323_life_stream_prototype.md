# T323: Life Stream Prototype

## Task ID

T323

## Goal

Create a local text-first life-stream prototype contract that projects
AI-generated imagined `RoleDynamicPost` records into reviewable private feed
states with visible AIGC labels, not-real-world disclosure, memory inspiration
refs, and export/share blocks.

## Why Now

T322 establishes chat plus memory explanation states. The next M21 surface is
the virtual life stream, which is central to the desired companion experience
but carries deception risk if it is not clearly labeled as imagined synthetic
content.

## Allowed Files

Future T323 worker may create or modify only:

- `src/practical_chat_agent/ui/text_first_life_stream.py`
- `tests/test_text_first_life_stream_prototype.py`
- `docs/data_contracts/text_first_life_stream_contract.md`
- `docs/tasks/M21_text_first_product_ux_prototype/T324_proactive_settings_prototype.md`
- `docs/worker_summary/T323_worker_summary.md`
- `docs/07_handoff.md`

If T323 needs browser UI, HTML/CSS, model-provider calls, private chat-log
processing, external APIs, platform adapters, outbound messaging, or task-board
edits, Captain must revise this package before assignment.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not call LLMs, model providers, external APIs, browser automation, or
  network services.
- Do not build a real frontend or browser demo in T323.
- Do not publish, share, export, schedule, or send life-stream content.
- Do not mutate memory, persona, consent, or safety records.
- Do not generate factual real-world activity claims.
- Do not claim legal advice, compliance completion, crisis-safety sufficiency,
  clinical validation, launch approval, app-store approval, or regulator
  acceptance.
- Do not modify `docs/04_task_board.md`, `docs/05_decision_log.md`,
  `docs/06_eval_protocol.md`, or `docs/08_risks_and_open_questions.md`.

## Inputs To Read

Required:

- `docs/product/text_first_ux_information_architecture.md`
- `docs/data_contracts/role_dynamic_post_contract.md`
- `docs/data_contracts/virtual_life_engine_contract.md`
- `docs/data_contracts/aigc_labeling_contract.md`
- `docs/data_contracts/consent_center_contract.md`
- `src/practical_chat_agent/core/models.py`
- `src/practical_chat_agent/services/virtual_life_engine.py`
- `tests/test_role_dynamic_post_schema.py`
- `tests/test_virtual_life_engine_text_generator.py`
- `tests/test_aigc_labeling_plan_contract.py`

## Expected Outputs

### 1. Prototype State Contract

Implement a small local life-stream projection. Minimum behavior:

- projects `RoleDynamicPost` records into private review feed items;
- preserves AI-generated imagined/not-real-world labels;
- preserves memory refs as inspiration only;
- preserves review status and factual-claim review notes;
- blocks export/share/download when consent or metadata labels are missing;
- never publishes, shares, exports, sends, schedules, or connects to platforms.

### 2. Tests

Create `tests/test_text_first_life_stream_prototype.py` with RED/GREEN coverage
for:

- generated post appears as review-only private feed item;
- visible AIGC label includes imagined/not-real-world disclosure;
- memory refs remain inspiration-only;
- factual-claim posts require review notes;
- export/share/download state is blocked without consent/metadata;
- payloads contain no publish, send, schedule, delivery, platform, webhook,
  token, or queue fields.

### 3. Data Contract

Create `docs/data_contracts/text_first_life_stream_contract.md` describing
fields, state transitions, invariants, non-actions, and verification.

### 4. Next Task Package

Create
`docs/tasks/M21_text_first_product_ux_prototype/T324_proactive_settings_prototype.md`
for proactive settings prototype work.

### 5. Worker Summary And Handoff

Write `docs/worker_summary/T323_worker_summary.md` and append a T323 worker
record to `docs/07_handoff.md`.

Do not mark T323 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\ui\text_first_life_stream.py src\practical_chat_agent\core\models.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_text_first_life_stream_prototype.py tests\test_role_dynamic_post_schema.py tests\test_virtual_life_engine_text_generator.py tests\test_aigc_labeling_plan_contract.py -q
```

```powershell
git diff --check
```

## Reviewer Type

Product/safety UX review recommended.

Reviewer should block if life-stream items hide AIGC labels, imply real-world
activity, treat imagined memory as factual, or expose publish/share/export/send
behavior.
