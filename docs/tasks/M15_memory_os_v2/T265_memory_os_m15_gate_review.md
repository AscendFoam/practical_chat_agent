# T265: Memory OS M15 Gate Review

## Task ID

T265

## Goal

Perform a documentation gate review for M15 Memory OS v2 by summarizing T260
through T264, recording verification evidence, known gaps, and the allowed next
milestone entry point.

## Why Now

T260-T264 have implemented MemoryEvent schema, local MemoryEvent store,
lifecycle policy recommendations, retrieval bundle schemas, and consolidation
candidate stubs. Before moving into M16 relationship/dialogue consumption, the
project needs a clear gate record that distinguishes implemented Memory OS v2
foundations from retrieval ranking, runtime dialogue, proactive behavior, and
product UX that remain future work.

## Allowed Files

Future T265 worker may create or modify only:

- `docs/review/M15_review.md`
- `docs/tasks/M16_relationship_dialogue_consumption/T270_relationship_context_bundle.md`
- `docs/worker_summary/T265_worker_summary.md`
- `docs/07_handoff.md`

If T265 needs code changes, tests, task-board edits, or implementation work,
Captain must revise this package before assignment.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not call LLMs, model providers, external APIs, browser automation, or
  network services.
- Do not implement code.
- Do not implement retrieval ranking, vector search, runtime dialogue,
  proactive candidates, schedulers, outbound requests, or platform integration.
- Do not implement real-person style extraction, clone behavior, voice/face
  work, Live2D/video simulation, or web demo.
- Do not modify `docs/04_task_board.md`, `docs/05_decision_log.md`,
  `docs/06_eval_protocol.md`, or `docs/08_risks_and_open_questions.md`.

## Inputs To Read

Required:

- `docs/data_contracts/memory_event_v2_contract.md`
- `docs/data_contracts/memory_event_store_v2_contract.md`
- `docs/data_contracts/memory_lifecycle_v2_contract.md`
- `docs/data_contracts/memory_retrieval_bundle_v2_contract.md`
- `docs/data_contracts/memory_consolidation_v2_contract.md`
- `docs/worker_summary/T260_worker_summary.md`
- `docs/worker_summary/T261_worker_summary.md`
- `docs/worker_summary/T262_worker_summary.md`
- `docs/worker_summary/T263_worker_summary.md`
- `docs/worker_summary/T264_worker_summary.md`
- `tests/test_memory_event_schema.py`
- `tests/test_memory_event_store.py`
- `tests/test_memory_lifecycle_v2.py`
- `tests/test_memory_retrieval_bundle_schema.py`
- `tests/test_memory_consolidation_v2.py`

## Expected Outputs

### 1. M15 Review

Create `docs/review/M15_review.md` with:

- task coverage summary;
- implemented code and contract list;
- verification commands and results;
- explicit non-actions;
- memory truth/isolation assessment;
- residual risks;
- gate recommendation.

### 2. M16 Entry Task Package

Create
`docs/tasks/M16_relationship_dialogue_consumption/T270_relationship_context_bundle.md`
for relationship/dialogue context bundle work. T270 should remain schema/local
and should not call LLMs or send messages.

### 3. Worker Summary And Handoff

Write `docs/worker_summary/T265_worker_summary.md` and append a T265 worker
record to `docs/07_handoff.md`.

Do not mark T265 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'
pytest tests\test_memory_event_schema.py tests\test_memory_event_store.py tests\test_memory_lifecycle_v2.py tests\test_memory_retrieval_bundle_schema.py tests\test_memory_consolidation_v2.py -q
```

```powershell
git diff --check
```

## Reviewer Type

Adversarial review recommended.

Reviewer should verify that M15 can be considered a local Memory OS v2
foundation only, not a retrieval-ranking layer, runtime dialogue engine,
proactive system, or web demo.
