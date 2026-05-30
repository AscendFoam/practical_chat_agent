# T272: Dialogue Draft Stub

## Task ID

T272

## Goal

Implement a deterministic local dialogue draft stub that uses a
`DialogueContextPlan` to produce review-only draft metadata and a clearly
synthetic draft string. It must not call LLMs, send messages, schedule
proactive behavior, or integrate with external platforms.

## Why Now

T270 packages relationship context and T271 plans tone/pacing/memory-use
metadata. A deterministic draft stub can give later UI/demo work something
visible to render while preserving review-first boundaries.

## Allowed Files

Future T272 worker may create or modify only:

- `src/practical_chat_agent/services/dialogue_draft_stub.py`
- `tests/test_dialogue_draft_stub.py`
- `docs/data_contracts/dialogue_draft_stub_contract.md`
- `docs/tasks/M16_relationship_dialogue_consumption/T273_relationship_dialogue_m16_gate_review.md`
- `docs/worker_summary/T272_worker_summary.md`
- `docs/07_handoff.md`

If the task needs LLM calls, UI, proactive behavior, outbound requests,
platform integration, or private readers, Captain must revise this package
before assignment.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not call LLMs, model providers, external APIs, browser automation, or
  network services.
- Do not send, schedule, or deliver messages.
- Do not implement proactive candidates or external platform integration.
- Do not implement real-person style extraction, clone behavior, voice/face
  work, Live2D/video simulation, or web demo.
- Do not modify `docs/04_task_board.md`, `docs/05_decision_log.md`,
  `docs/06_eval_protocol.md`, or `docs/08_risks_and_open_questions.md`.

## Inputs To Read

Required:

- `src/practical_chat_agent/services/dialogue_context_planner.py`
- `tests/test_dialogue_context_planner.py`
- `docs/data_contracts/dialogue_context_plan_contract.md`

## Expected Outputs

### 1. Draft Stub

Return a review-only object with:

- plan id;
- draft id;
- generator type `deterministic_stub`;
- draft text;
- tone guidance;
- boundary reminders;
- memory-use notes;
- safety warnings;
- `requires_review=true`.

### 2. Tests

Add focused tests proving:

- draft is deterministic from plan metadata;
- draft carries review-required status;
- dependency/manipulation phrases are absent;
- imagined memory warnings remain visible;
- service exposes no send/schedule/runtime methods.

### 3. Contract Doc

Create `docs/data_contracts/dialogue_draft_stub_contract.md`.

### 4. Next Task Package

Create
`docs/tasks/M16_relationship_dialogue_consumption/T273_relationship_dialogue_m16_gate_review.md`
for M16 gate review.

### 5. Worker Summary And Handoff

Write `docs/worker_summary/T272_worker_summary.md` and append a T272 worker
record to `docs/07_handoff.md`.

Do not mark T272 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\services\dialogue_draft_stub.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_dialogue_draft_stub.py tests\test_dialogue_context_planner.py -q
```

```powershell
git diff --check
```

## Reviewer Type

Adversarial review recommended.

Reviewer should verify that T272 is review-only deterministic stub work and
does not send messages or call LLMs.
