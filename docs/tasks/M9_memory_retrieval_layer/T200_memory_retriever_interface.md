# Task T200: MemoryRetriever Interface

## Task ID

T200

## Goal

Define a `MemoryRetriever` interface and `MemoryHit` contract that can sit above existing local retrieval logic without introducing external memory systems.

## Why Now

T195 has closed M8 with `PASS_WITH_WARNINGS`. The project now knows two things clearly:

- the current repo can expose and evaluate review-safe relationship-state context
- the current planner still does not semantically consume that context

The next safe step is therefore not more ad hoc planner wiring. It is contract-first M9 work: define the retrieval abstraction before any new retriever implementation or external adapter spike.

## Read First

- `docs/04_task_board.md`
- `docs/06_eval_protocol.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`
- `src/practical_chat_agent/services/memory_retrieval.py`
- `src/practical_chat_agent/services/chat_context.py`
- `src/practical_chat_agent/core/models.py`

## Inputs To Respect

- Keep the mainline approved-only, review-safe, and offline-first.
- Treat this as contract work, not retrieval-quality work.
- Preserve compatibility with the current local retrieval flow instead of inventing a second parallel shape.
- Do not use T200 to solve deferred T195 planner-behavior gaps.

## Forbidden Scope

- Do not add vector DB.
- Do not add Mem0/Zep adapter.
- Do not auto-write memories.
- Do not read raw chat history.
- Do not change reply-planner behavior.
- Do not add provider calls, embedding calls, or external services.

## Allowed Files

- `src/practical_chat_agent/core/models.py`
- `src/practical_chat_agent/services/memory_retrieval.py`
- `src/practical_chat_agent/services/chat_context.py`
- `tests/test_memory_retriever_contract.py`
- `docs/data_contracts/memory_retriever_contract.md`
- `docs/07_handoff.md`

## Expected Output

Produce a narrow, reusable contract layer that makes later M9 tasks easier to implement and review:

- a `MemoryRetriever` interface or protocol
- a `MemoryHit` data contract for selected retrieval results
- any minimal adapter or wrapper needed so existing local retrieval code can satisfy the new contract
- a short contract document that explains boundaries, required fields, and what is intentionally out of scope

## Implementation Notes

- Prefer additive work over broad refactors.
- Reuse existing retrieval/result model shapes where that keeps the boundary smaller and clearer.
- If a naming choice must be made, prefer names that can accommodate local retrievers first and external adapters later.
- Keep the contract explicit about approved-only and review-safe retrieval inputs.
- If `ChatContextAssembler` needs only minimal touch points to reference the abstraction, keep them narrow.

## Verification

- `python -m py_compile src/practical_chat_agent/core/models.py src/practical_chat_agent/services/memory_retrieval.py src/practical_chat_agent/services/chat_context.py`
- `pytest tests/test_memory_retriever_contract.py -q`

If a dedicated test file is unnecessary, explain why in `docs/07_handoff.md` and still run compile verification.

## Acceptance Criteria

- The repo has a clear retriever interface boundary that later tasks can implement against.
- No external memory dependency is introduced.
- No raw transcript retrieval path is introduced.
- Existing local retrieval behavior is not broadened into auto-write or runtime mutation.
- The contract document is specific enough that T201 can implement a local approved-store retriever without guessing intent.

## Review Focus

- Is the abstraction actually contract-first, or did it smuggle in implementation scope?
- Does it preserve approved-only and review-safe boundaries?
- Is it compatible with current local retrieval surfaces?
- Does it avoid external dependency creep?

## Reviewer Type

normal
