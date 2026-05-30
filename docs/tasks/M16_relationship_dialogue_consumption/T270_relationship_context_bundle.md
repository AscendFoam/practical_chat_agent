# T270: Relationship Context Bundle

## Task ID

T270

## Goal

Define local schema models that package PersonaCard, RelationshipState, and
MemoryEvent context into a reviewable relationship/dialogue context bundle
without calling LLMs, generating replies, sending messages, or integrating with
external platforms.

## Why Now

M14 created PersonaCard foundations and M15 created Memory OS v2 foundations.
The next layer should define a safe context contract before any dialogue engine
consumes persona, relationship, and memory state.

## Allowed Files

Future T270 worker may create or modify only:

- `src/practical_chat_agent/core/models.py`
- `tests/test_relationship_context_bundle_schema.py`
- `docs/data_contracts/relationship_context_bundle_contract.md`
- `docs/tasks/M16_relationship_dialogue_consumption/T271_dialogue_context_planner.md`
- `docs/worker_summary/T270_worker_summary.md`
- `docs/07_handoff.md`

If the task needs LLM calls, retrieval ranking, UI, runtime dialogue,
proactive behavior, outbound requests, platform integration, or private
readers, Captain must revise this package before assignment.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not call LLMs, model providers, external APIs, browser automation, or
  network services.
- Do not generate dialogue replies.
- Do not implement proactive candidates, schedulers, outbound requests,
  automatic sending, or platform integration.
- Do not implement real-person style extraction, clone behavior, voice/face
  work, Live2D/video simulation, or web demo.
- Do not modify `docs/04_task_board.md`, `docs/05_decision_log.md`,
  `docs/06_eval_protocol.md`, or `docs/08_risks_and_open_questions.md`.

## Inputs To Read

Required:

- `docs/review/M14_review.md`
- `docs/review/M15_review.md`
- `src/practical_chat_agent/core/models.py`
- `tests/test_persona_card_schema.py`
- `tests/test_relationship_context.py`
- `tests/test_memory_event_schema.py`
- `tests/test_memory_retrieval_bundle_schema.py`
- `docs/data_contracts/persona_card_v1_contract.md`
- `docs/data_contracts/memory_retrieval_bundle_v2_contract.md`

## Expected Outputs

### 1. Context Bundle Schemas

Add schema models for:

- `RelationshipContextBundle`
- `RelationshipContextPersonaSnapshot`
- `RelationshipContextMemorySnapshot`

The bundle should record:

- user id;
- persona id and disclosure;
- relationship state dimensions;
- memory bundle id;
- safety warnings;
- source ids;
- generated timestamp.

### 2. Invariants

Tests must prove:

- bundle cannot include non-runtime-ready PersonaCard;
- bundle cannot include imagined memory as factual context;
- bundle preserves relationship dimensions without turning them into retention
  or manipulation scores;
- bundle has no draft reply, send, schedule, delivery, or platform fields;
- bundle is local/schema-only.

### 3. Contract Doc

Create `docs/data_contracts/relationship_context_bundle_contract.md`.

### 4. Next Task Package

Create
`docs/tasks/M16_relationship_dialogue_consumption/T271_dialogue_context_planner.md`
for deterministic local dialogue-context planning. T271 should still not call
LLMs or send messages.

### 5. Worker Summary And Handoff

Write `docs/worker_summary/T270_worker_summary.md` and append a T270 worker
record to `docs/07_handoff.md`.

Do not mark T270 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\core\models.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_relationship_context_bundle_schema.py tests\test_persona_card_schema.py tests\test_memory_retrieval_bundle_schema.py -q
```

```powershell
git diff --check
```

## Reviewer Type

Adversarial review recommended.

Reviewer should verify that T270 is schema-only and does not implement reply
generation, proactive behavior, outbound sending, or platform integration.
