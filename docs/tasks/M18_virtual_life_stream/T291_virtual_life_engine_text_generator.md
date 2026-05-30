# T291: Virtual Life Engine Text Generator

## Task ID

T291

## Goal

Implement a deterministic local `VirtualLifeEngine` text stub that creates
review-only `RoleDynamicPost` drafts from already-provided persona/context
metadata. The engine should not call LLMs and should not publish posts.

## Why Now

T290 defines the virtual life stream draft schema. T291 can provide a minimal
deterministic generator stub so future review-card and contamination tests have
objects to consume, while keeping all generated content explicitly imagined and
review-only.

## Allowed Files

Future T291 worker may create or modify only:

- `src/practical_chat_agent/services/virtual_life_engine.py`
- `tests/test_virtual_life_engine_text_generator.py`
- `docs/data_contracts/virtual_life_engine_contract.md`
- `docs/tasks/M18_virtual_life_stream/T292_aigc_labeling_metadata.md`
- `docs/worker_summary/T291_worker_summary.md`
- `docs/07_handoff.md`

If T291 needs model changes, LLM calls, schedulers, publishers, platform
adapters, UI, or task-board edits, Captain must revise this package before
assignment.

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
- `src/practical_chat_agent/core/models.py` RoleDynamicPost section
- `tests/test_role_dynamic_post_schema.py`

## Expected Outputs

### 1. Deterministic Text Stub

Create `src/practical_chat_agent/services/virtual_life_engine.py`.

Minimum expected objects:

- `VirtualLifeSeedContext` or equivalent input model with persona id, user id,
  mood/activity/topic labels, memory refs, and relationship context refs;
- `VirtualLifeEngine.create_post(context) -> RoleDynamicPost`;
- deterministic text templates that produce imagined review-only drafts.

Minimum expected behavior:

- generated posts use `RoleDynamicPost`;
- generated posts are imagined AI-generated content;
- generated posts require review;
- generated posts remain local/private review only;
- memory refs are copied as inspiration references only;
- engine payloads contain no publish, send, schedule, delivery, platform,
  webhook, token, or queue fields;
- engine exposes no publish/send/schedule/delivery/runtime methods.

### 2. Tests

Add `tests/test_virtual_life_engine_text_generator.py` covering:

- deterministic post text from seed context;
- memory/context refs preserved;
- imagined labels and review status preserved;
- no publishing/delivery fields;
- service exposes no publish/send/schedule/delivery/runtime methods.

### 3. Data Contract

Create `docs/data_contracts/virtual_life_engine_contract.md` describing input,
output, deterministic rules, non-actions, and verification.

### 4. Next Task Package

Create `docs/tasks/M18_virtual_life_stream/T292_aigc_labeling_metadata.md`.
T292 should harden AIGC labels and disclosure metadata without publishing.

### 5. Worker Summary And Handoff

Write `docs/worker_summary/T291_worker_summary.md` and append a T291 worker
record to `docs/07_handoff.md`.

Do not mark T291 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\services\virtual_life_engine.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_virtual_life_engine_text_generator.py tests\test_role_dynamic_post_schema.py -q
```

```powershell
git diff --check
```

## Reviewer Type

Adversarial review recommended.

Reviewer should verify that T291 creates deterministic local review-only post
drafts and cannot publish, send, schedule, deliver, or call LLMs.
