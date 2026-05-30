# T293: Imagined/Factual Contamination Tests

## Task ID

T293

## Goal

Add tests that ensure imagined virtual life stream content cannot be treated as
factual memory, factual retrieval context, or real-world activity. The tests
should cover `RoleDynamicPost`, `VirtualLifeEngine`, and memory/retrieval
contracts where relevant.

T293 must not publish posts, send messages, call LLMs, or integrate with any
platform.

## Why Now

T290-T292 define and label imagined virtual life stream drafts. Before review
card work, M18 needs adversarial contamination tests so imagined posts cannot
leak into factual memory or be presented as real social activity.

## Allowed Files

Future T293 worker may create or modify only:

- `src/practical_chat_agent/core/models.py`
- `src/practical_chat_agent/services/virtual_life_engine.py`
- `tests/test_virtual_life_contamination.py`
- `docs/data_contracts/role_dynamic_post_contract.md`
- `docs/data_contracts/virtual_life_engine_contract.md`
- `docs/tasks/M18_virtual_life_stream/T294_dynamic_review_card.md`
- `docs/worker_summary/T293_worker_summary.md`
- `docs/07_handoff.md`

If T293 needs LLM calls, publishers, platform adapters, UI, or task-board edits,
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
- `src/practical_chat_agent/core/models.py` RoleDynamicPost and memory sections
- `src/practical_chat_agent/services/virtual_life_engine.py`
- `tests/test_memory_retrieval_bundle_schema.py`
- `tests/test_virtual_life_aigc_labeling.py`

## Expected Outputs

### 1. Contamination Tests

Add `tests/test_virtual_life_contamination.py` covering:

- `RoleDynamicPost` cannot be converted into factual memory without explicit
  review notes;
- imagined post refs remain inspiration refs only;
- engine-created posts retain imagined labels;
- serialized post payloads contain no factual-memory promotion fields;
- factual retrieval bundles cannot include imagined post content as evidence.

### 2. Schema Or Engine Update If Needed

Update `RoleDynamicPost` or `VirtualLifeEngine` only where needed to make the
contamination tests pass.

### 3. Contract Updates

Update role dynamic post and virtual life engine contracts with any new
contamination invariants.

### 4. Next Task Package

Create `docs/tasks/M18_virtual_life_stream/T294_dynamic_review_card.md` for
review-card work around dynamic posts.

### 5. Worker Summary And Handoff

Write `docs/worker_summary/T293_worker_summary.md` and append a T293 worker
record to `docs/07_handoff.md`.

Do not mark T293 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\core\models.py src\practical_chat_agent\services\virtual_life_engine.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_virtual_life_contamination.py tests\test_virtual_life_aigc_labeling.py tests\test_memory_retrieval_bundle_schema.py -q
```

```powershell
git diff --check
```

## Reviewer Type

Adversarial review recommended.

Reviewer should verify that T293 prevents imagined/factual contamination and
cannot publish, send, schedule, deliver, call LLMs, or integrate with platforms.
