# Task T201: Local Approved-Store Retriever

## Task ID

T201

## Goal

Implement a local `MemoryRetriever` protocol implementation over approved local memory store records using simple deterministic filters.

## Why Now

T200 has defined the `MemoryRetriever`, `MemoryHit`, and `MemoryRetrieverResult` contract. The next safe M9 step is to prove that contract against the existing approved-store boundary before any retrieval eval set or external adapter spike.

This task must turn the contract into a local, approved-only retriever. It should not broaden retrieval into raw transcript search, vector DB, external memory systems, or planner behavior changes.

## Read First

- `docs/04_task_board.md`
- `docs/06_eval_protocol.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`
- `docs/data_contracts/memory_retriever_contract.md`
- `src/practical_chat_agent/services/memory_retrieval.py`
- `src/practical_chat_agent/services/chat_context.py`
- `src/practical_chat_agent/core/models.py`

## Inputs To Respect

- Use the T200 `MemoryRetriever` protocol and return `MemoryRetrieverResult`.
- Return `MemoryHit` items with `source="approved_store"`.
- Consume only approved/runtime-ready local store records.
- Preserve evidence refs and safe fact text.
- Keep retrieval deterministic and local.
- Prefer simple text matching / deterministic scoring over embedding or provider calls.
- Preserve existing `ChatContextAssembler` behavior unless a minimal helper reuse is necessary.

## Expected Output

- A local approved-store retriever implementation that satisfies `MemoryRetriever`.
- Deterministic filtering to exclude candidate/rejected/frozen/archived/not-human-reviewed records.
- Simple query/limit behavior suitable for later T202 retrieval eval.
- Tests that prove approved-only filtering, evidence preservation, source provenance, and no raw transcript access.
- Handoff notes explaining how T202 can evaluate retrieval quality without changing the approved-store boundary.

## Forbidden Scope

- Do not add vector DB or external memory dependency.
- Do not retrieve candidate/rejected/frozen records.
- Do not read raw chat history.
- Do not auto-write, approve, freeze, reject, archive, or otherwise mutate memory/store records.
- Do not change ReplyPlanner, policy-engine, send-gate, platform adapter, or outbound behavior.
- Do not introduce Mem0, Zep, embedding calls, provider calls, or async adapter machinery.
- Do not treat T195 relationship-context gaps as part of this task.

## Allowed Files

- `src/practical_chat_agent/core/models.py`
- `src/practical_chat_agent/services/memory_retrieval.py`
- `src/practical_chat_agent/services/chat_context.py`
- `tests/test_local_approved_store_retriever.py`
- `docs/data_contracts/memory_retriever_contract.md`
- `docs/07_handoff.md`

## Verification

- `python -m py_compile src/practical_chat_agent/core/models.py src/practical_chat_agent/services/memory_retrieval.py src/practical_chat_agent/services/chat_context.py`
- `pytest tests/test_local_approved_store_retriever.py -q`
- If existing T200 tests are touched or the shared contract is changed: `pytest tests/test_memory_retriever_contract.py tests/test_local_approved_store_retriever.py -q`

## Acceptance Criteria

- The new retriever satisfies `isinstance(retriever, MemoryRetriever)` at runtime.
- Approved/runtime-ready memory records can become `MemoryHit` results with `source="approved_store"`.
- Candidate/rejected/frozen/archived/not-human-reviewed records never appear in hits.
- `limit` is enforced deterministically.
- Query behavior is documented and covered by tests.
- Evidence refs are preserved.
- No private/raw transcript fields, file paths, review history, or raw chat text are introduced into `MemoryHit`.
- The implementation is additive and does not change current planner behavior.

## Review Focus

- Does the retriever actually consume only approved/runtime-ready records?
- Does it preserve the T200 contract without inventing a parallel result shape?
- Are scoring/query semantics simple, deterministic, and documented?
- Are forbidden records and raw/private surfaces excluded by tests?
- Did the task avoid external adapter creep and planner behavior changes?

## Reviewer Type

adversarial
