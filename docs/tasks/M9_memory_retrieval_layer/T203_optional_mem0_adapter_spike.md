# Task T203: Optional Mem0 Adapter Spike

## Task ID

T203

## Goal

Run a contained spike to evaluate whether an optional Mem0-backed retriever adapter can fit behind the existing `MemoryRetriever` contract without weakening review-first memory semantics.

This is a feasibility spike, not a production integration task.

## Why Now

T200 defined the `MemoryRetriever` / `MemoryRetrieverResult` contract, T201 implemented local approved-store retrieval, and T202 added a reusable synthetic eval set. The next smallest safe step is to check whether an optional external-memory adapter boundary can reuse that contract and eval shape without becoming a required dependency or bypassing approved-memory safeguards.

## Inputs To Read

- `AGENTS.md`
- `docs/02_experiment_plan.md`
- `docs/04_task_board.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`
- `docs/data_contracts/memory_retriever_contract.md`
- `docs/data_contracts/memory_retriever_eval_set.md`
- `src/practical_chat_agent/services/memory_retrieval.py`
- `tests/test_memory_retriever_contract.py`
- `tests/test_local_approved_store_retriever.py`
- `tests/test_memory_retriever_eval_set.py`

## Allowed Files

- `src/practical_chat_agent/services/memory_retrieval.py`
- `tests/test_optional_mem0_adapter_spike.py`
- `tests/test_memory_retriever_eval_set.py`
- `docs/data_contracts/memory_retriever_contract.md`
- `docs/spikes/T203_mem0_adapter_spike.md`
- `docs/worker_summary/T203_worker_summary.md`
- `docs/07_handoff.md`

If the spike needs a dedicated adapter module, the worker may add exactly one new file under `src/practical_chat_agent/services/` with a narrowly named optional-adapter purpose, and must document why it was necessary in the worker summary.

## Forbidden Scope

- Do not make `mem0`, `mem0ai`, or any external memory package a required dependency.
- Do not add a dependency install step, vendored SDK code, or committed generated third-party code.
- Do not call Mem0, OpenAI, embedding providers, network services, or external APIs in committed tests.
- Do not read, index, summarize, or copy private raw chat history.
- Do not introduce automatic memory extraction, write-back, sync, mutation, or approval bypass.
- Do not mutate approved local stores.
- Do not remove or weaken `LocalApprovedStoreRetriever`.
- Do not change `ChatContext`, `ChatContextAssembler`, `ReplyPlanner`, policy engine, outbound send behavior, or platform adapters.
- Do not claim Mem0 is adopted or production-ready.

## Expected Output

One of the following narrow outcomes is acceptable:

- A minimal optional Mem0 adapter boundary behind `MemoryRetriever.retrieve()` that degrades safely to `status="not_configured"` when the optional dependency/configuration is absent, plus committed tests that do not require Mem0 or network access.
- Or, if a safe implementation cannot be done without relying on unavailable/unstable external APIs, a documented spike note in `docs/spikes/T203_mem0_adapter_spike.md` explaining the blocker and preserving the existing local retriever as the only implemented retriever.

In either case, the output must:

- preserve `MemoryRetrieverResult` as the public result shape
- avoid raw transcript fields, embedding vectors, and write capabilities in returned data
- reuse the T202 synthetic eval case shape where feasible
- explicitly document unavailable-dependency behavior
- update `docs/07_handoff.md` with implementation/spike result, verification, and residual risks
- write the worker summary to `docs/worker_summary/T203_worker_summary.md`

## Verification

Run the narrow verification relevant to the selected outcome:

```powershell
python -m py_compile src/practical_chat_agent/services/memory_retrieval.py
pytest tests/test_memory_retriever_contract.py tests/test_local_approved_store_retriever.py tests/test_memory_retriever_eval_set.py -q
```

If adapter code is added, also run:

```powershell
pytest tests/test_optional_mem0_adapter_spike.py -q
```

If the Windows default temp directory is inaccessible in this sandbox, set `TEMP` and `TMP` to a workspace-local temp directory before running pytest and record that fact in `docs/07_handoff.md`.

## Docs To Update

- `docs/07_handoff.md`
- `docs/worker_summary/T203_worker_summary.md`
- `docs/spikes/T203_mem0_adapter_spike.md` if a spike note is needed
- `docs/data_contracts/memory_retriever_contract.md` only if the optional-adapter convention needs clarification

Do not update `docs/04_task_board.md`; Captain will mark task completion after review.

## Reviewer Type

adversarial
