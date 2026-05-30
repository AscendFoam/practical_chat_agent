# T271: Dialogue Context Planner

## Task ID

T271

## Goal

Implement a deterministic local planner that converts a
`RelationshipContextBundle` into a dialogue-context plan with tone, pacing,
memory-use constraints, and safety reminders, without generating replies,
calling LLMs, sending messages, or integrating with external platforms.

## Why Now

T270 defines the relationship context bundle. The next safe step is a planning
layer that makes the bundle useful to later dialogue generation while remaining
review-first and non-generative.

## Allowed Files

Future T271 worker may create or modify only:

- `src/practical_chat_agent/services/dialogue_context_planner.py`
- `tests/test_dialogue_context_planner.py`
- `docs/data_contracts/dialogue_context_plan_contract.md`
- `docs/tasks/M16_relationship_dialogue_consumption/T272_dialogue_draft_stub.md`
- `docs/worker_summary/T271_worker_summary.md`
- `docs/07_handoff.md`

If the task needs LLM calls, UI, runtime dialogue, proactive behavior, outbound
requests, platform integration, or private readers, Captain must revise this
package before assignment.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not call LLMs, model providers, external APIs, browser automation, or
  network services.
- Do not generate final user-visible replies.
- Do not implement proactive candidates, schedulers, outbound requests,
  automatic sending, or platform integration.
- Do not implement real-person style extraction, clone behavior, voice/face
  work, Live2D/video simulation, or web demo.
- Do not modify `docs/04_task_board.md`, `docs/05_decision_log.md`,
  `docs/06_eval_protocol.md`, or `docs/08_risks_and_open_questions.md`.

## Inputs To Read

Required:

- `src/practical_chat_agent/core/models.py`
- `tests/test_relationship_context_bundle_schema.py`
- `docs/data_contracts/relationship_context_bundle_contract.md`
- `docs/review/M15_review.md`

## Expected Outputs

### 1. Planner Service

Return a local plan with:

- tone guidance;
- response length guidance;
- boundary reminders;
- memory-use notes;
- relationship pacing notes;
- safety warnings.

### 2. Tests

Add focused tests proving:

- high boundary risk increases caution;
- high trust/warmth allows warmer tone but not dependency language;
- factual context can be used only as factual notes;
- imagined context is labeled and not used as factual evidence;
- planner returns plan metadata only and no draft reply text;
- service exposes no send/schedule/runtime methods.

### 3. Contract Doc

Create `docs/data_contracts/dialogue_context_plan_contract.md`.

### 4. Next Task Package

Create `docs/tasks/M16_relationship_dialogue_consumption/T272_dialogue_draft_stub.md`
for a deterministic draft stub. T272 still must not call LLMs or send messages.

### 5. Worker Summary And Handoff

Write `docs/worker_summary/T271_worker_summary.md` and append a T271 worker
record to `docs/07_handoff.md`.

Do not mark T271 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\services\dialogue_context_planner.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_dialogue_context_planner.py tests\test_relationship_context_bundle_schema.py -q
```

```powershell
git diff --check
```

## Reviewer Type

Adversarial review recommended.

Reviewer should verify that T271 is planning metadata only and does not
generate replies, send messages, or connect to external platforms.
