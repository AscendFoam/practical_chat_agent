# Task T202: Retrieval Eval Set

## Task ID

T202

## Goal

Create a committed synthetic retrieval eval set that can evaluate `MemoryRetrieverResult` quality and boundary behavior for local retrievers without using private chat content.

## Why Now

T200 defined the `MemoryRetriever` contract, and T201 implemented `LocalApprovedStoreRetriever` over approved local store records. The next M9 step is not an external adapter. It is a deterministic eval set that can compare retrievers through the same `MemoryRetrieverResult` shape and catch retrieval regressions before any optional Mem0/Zep spike.

## Read First

- `docs/04_task_board.md`
- `docs/06_eval_protocol.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`
- `docs/data_contracts/memory_retriever_contract.md`
- `src/practical_chat_agent/services/memory_retrieval.py`
- `tests/test_memory_retriever_contract.py`
- `tests/test_local_approved_store_retriever.py`

## Inputs To Respect

- Use synthetic/redacted data only.
- Evaluate through `MemoryRetriever.retrieve()` and `MemoryRetrieverResult`, not implementation-private helpers.
- Include both positive relevance cases and exclusion/boundary cases.
- Keep eval deterministic and runnable in CI/local tests without provider calls.
- Treat T202 as evaluation scaffolding, not retrieval algorithm improvement.

## Expected Output

- Synthetic approved-store fixture(s) or inline builders covering multiple contacts, memory types, query terms, and non-runtime-ready records.
- A small eval-case contract that states expected contact, query, expected hit ids or memory ids, and expected exclusions.
- Tests that run the eval cases against `LocalApprovedStoreRetriever`.
- Documentation or comments explaining how later retrievers, including `LocalMemoryRetriever` or optional external adapters, can reuse the same eval cases.
- Handoff notes summarizing coverage and remaining retrieval-quality limitations.

## Forbidden Scope

- Do not use private chat content.
- Do not add external services.
- Do not add vector DB, Mem0, Zep, embedding calls, provider calls, or network access.
- Do not change retriever scoring or filtering behavior except if needed for a proven bug, and then keep it within T201 allowed boundaries.
- Do not integrate retriever output into `ChatContextAssembler`, `ReplyPlanner`, policy engine, send gate, or platform adapters.
- Do not write private artifacts or eval outputs under `private/` as committed evidence.

## Allowed Files

- `tests/test_memory_retriever_eval_set.py`
- `tests/fixtures/**`
- `examples/payloads/**`
- `docs/data_contracts/memory_retriever_contract.md`
- `docs/data_contracts/memory_retriever_eval_set.md`
- `docs/07_handoff.md`

## Verification

- `pytest tests/test_memory_retriever_eval_set.py -q`
- `pytest tests/test_memory_retriever_contract.py tests/test_local_approved_store_retriever.py tests/test_memory_retriever_eval_set.py -q`

If the worker changes shared retriever code despite the eval-only intent, also run:

- `python -m py_compile src/practical_chat_agent/services/memory_retrieval.py src/practical_chat_agent/core/models.py`
- `pytest tests/ -q`

## Acceptance Criteria

- Eval cases are synthetic and contain no private chat text, real names, real platform ids, or real file paths.
- Eval cases verify relevant hits, wrong-contact exclusion, non-runtime-ready exclusion, query miss behavior, and deterministic ordering or expected ids.
- Tests consume retrievers through the public `MemoryRetriever` protocol / `retrieve()` surface.
- Eval outputs use `MemoryRetrieverResult` / `MemoryHit` fields and do not inspect private implementation state unless explicitly justified.
- The eval set can be reused by a future retriever implementation without rewriting the cases.
- No new runtime behavior, external dependency, or planner/context integration is introduced.

## Review Focus

- Is this genuinely an eval set, or did it drift into implementation changes?
- Are fixtures fully synthetic and safe to commit?
- Do tests assert meaningful retrieval quality/boundary behavior rather than only schema round trips?
- Can later retrievers reuse the cases through the common protocol?
- Are T200/T201 approved-only and no-raw-transcript boundaries preserved?

## Reviewer Type

normal
