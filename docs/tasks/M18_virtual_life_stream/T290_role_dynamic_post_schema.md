# T290: Role Dynamic Post Schema

## Task ID

T290

## Goal

Define a text-first `RoleDynamicPost` schema for virtual life stream drafts.
The schema should support persona-authored imagined posts, review status,
memory/provenance references, and explicit imagined-content disclosure.

T290 must not generate posts with LLMs, publish posts, send messages, or
integrate with any platform.

## Why Now

M17 completed a local review-first proactive consent foundation. M18 begins the
virtual life stream layer: companion objects can have reviewable, imagined
life-stream drafts, but those drafts must remain labeled, private/review-first,
and isolated from factual memory and platform publishing.

## Allowed Files

Future T290 worker may create or modify only:

- `src/practical_chat_agent/core/models.py`
- `tests/test_role_dynamic_post_schema.py`
- `docs/data_contracts/role_dynamic_post_contract.md`
- `docs/tasks/M18_virtual_life_stream/T291_virtual_life_engine_text_generator.md`
- `docs/worker_summary/T290_worker_summary.md`
- `docs/07_handoff.md`

If T290 needs generators, schedulers, publishers, platform adapters, UI, or
task-board edits, Captain must revise this package before assignment.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not call LLMs, model providers, external APIs, browser automation, or
  network services.
- Do not generate post text.
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

- `docs/review/M17_review.md`
- `docs/data_contracts/proactive_review_card_contract.md`
- `src/practical_chat_agent/core/models.py`
- `docs/04_task_board.md` M18 section only

## Expected Outputs

### 1. Schema And Tests

Add `RoleDynamicPost` to `src/practical_chat_agent/core/models.py`.

Minimum expected fields:

- `schema_version`;
- `post_id`;
- `user_id`;
- `persona_id`;
- `content_text`;
- `content_status`, fixed to imagined AI-generated content;
- `truth_disclosure`;
- `review_status`;
- `visibility`;
- `memory_refs`;
- `relationship_context_refs`;
- `source_prompt_summary`;
- `safety_notes`;
- `created_at`;
- `updated_at`.

Minimum invariants:

- content is explicitly imagined AI-generated content;
- review status defaults to review required;
- visibility is local/private review only;
- empty content is rejected;
- factual truth claims require external review notes rather than factual memory
  promotion;
- serialized post contains no publish, send, schedule, delivery, platform,
  webhook, token, or queue fields.

### 2. Data Contract

Create `docs/data_contracts/role_dynamic_post_contract.md` describing the
schema, invariants, explicit non-actions, and verification.

### 3. Next Task Package

Create
`docs/tasks/M18_virtual_life_stream/T291_virtual_life_engine_text_generator.md`.
T291 may implement a deterministic local text stub from already-provided
persona/context metadata, but it must not call LLMs or publish posts.

### 4. Worker Summary And Handoff

Write `docs/worker_summary/T290_worker_summary.md` and append a T290 worker
record to `docs/07_handoff.md`.

Do not mark T290 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\core\models.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_role_dynamic_post_schema.py -q
```

```powershell
git diff --check
```

## Reviewer Type

Adversarial review recommended.

Reviewer should verify that T290 defines review-only virtual life stream schema
only and cannot generate, publish, send, schedule, or integrate with platforms.
