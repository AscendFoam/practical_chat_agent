# T292: AIGC Labeling Metadata

## Task ID

T292

## Goal

Harden AIGC labeling and disclosure metadata for virtual life stream drafts.
Every `RoleDynamicPost` produced for review should carry explicit AI-generated,
imagined-content, review-only labels that downstream review cards or UI can
display without inference.

T292 must not publish posts, send messages, call LLMs, or integrate with any
platform.

## Why Now

T290 defines post schema and T291 creates deterministic drafts. T292 should make
disclosure metadata more explicit before contamination tests and review card
work, so imagined virtual life content cannot be mistaken for factual memory or
real social activity.

## Allowed Files

Future T292 worker may create or modify only:

- `src/practical_chat_agent/core/models.py`
- `src/practical_chat_agent/services/virtual_life_engine.py`
- `tests/test_virtual_life_aigc_labeling.py`
- `docs/data_contracts/role_dynamic_post_contract.md`
- `docs/data_contracts/virtual_life_engine_contract.md`
- `docs/tasks/M18_virtual_life_stream/T293_imagined_factual_contamination_tests.md`
- `docs/worker_summary/T292_worker_summary.md`
- `docs/07_handoff.md`

If T292 needs LLM calls, publishers, platform adapters, UI, or task-board edits,
Captain must revise this package before assignment.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not call LLMs, model providers, external APIs, browser automation, or
  network services.
- Do not publish, send, deliver, enqueue, webhook, notify, or call platform
  adapters.
- Do not implement real social-feed integration, voice/avatar/video behavior,
  Live2D, web demo, or product UI.
- Do not implement real-person clone behavior, deceased-person simulation, or
  deceptive impersonation paths.
- Do not modify `docs/04_task_board.md`, `docs/05_decision_log.md`,
  `docs/06_eval_protocol.md`, or `docs/08_risks_and_open_questions.md`.

## Inputs To Read

Required:

- `docs/data_contracts/role_dynamic_post_contract.md`
- `docs/data_contracts/virtual_life_engine_contract.md`
- `src/practical_chat_agent/core/models.py` RoleDynamicPost section
- `src/practical_chat_agent/services/virtual_life_engine.py`
- `tests/test_role_dynamic_post_schema.py`
- `tests/test_virtual_life_engine_text_generator.py`

## Expected Outputs

### 1. AIGC Labeling Tests

Add `tests/test_virtual_life_aigc_labeling.py` covering:

- post has explicit AIGC label metadata;
- post has imagined-content disclosure text/labels;
- engine-created posts preserve those labels;
- label payloads contain no publish/send/schedule/delivery/platform fields;
- factual claims remain review notes, not factual-memory promotion.

### 2. Schema Or Engine Update If Needed

Update `RoleDynamicPost` and/or `VirtualLifeEngine` only where needed to make
label metadata explicit and deterministic.

### 3. Contract Updates

Update role dynamic post and virtual life engine contracts with the new label
metadata and invariants.

### 4. Next Task Package

Create
`docs/tasks/M18_virtual_life_stream/T293_imagined_factual_contamination_tests.md`
for contamination tests between imagined virtual life content and factual
memory.

### 5. Worker Summary And Handoff

Write `docs/worker_summary/T292_worker_summary.md` and append a T292 worker
record to `docs/07_handoff.md`.

Do not mark T292 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\core\models.py src\practical_chat_agent\services\virtual_life_engine.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_virtual_life_aigc_labeling.py tests\test_virtual_life_engine_text_generator.py tests\test_role_dynamic_post_schema.py -q
```

```powershell
git diff --check
```

## Reviewer Type

Adversarial review recommended.

Reviewer should verify that T292 strengthens labels only and cannot publish,
send, schedule, deliver, call LLMs, or integrate with platforms.
