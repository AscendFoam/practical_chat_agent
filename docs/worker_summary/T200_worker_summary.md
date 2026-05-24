# T200 Worker Summary

## Task

T200: MemoryRetriever Interface — define a `MemoryRetriever` protocol and `MemoryHit` contract that sits above existing local retrieval logic without introducing external memory systems.

## What Changed

### `src/practical_chat_agent/core/models.py`
- Added `MemoryRetrieverStatus` Literal type ("success", "not_configured", "error").
- Added `MemoryHit` model: thin, review-safe retrieval result with `hit_id`, `memory_id`, `fact`, `memory_type`, `score`, `evidence_refs`, `source`.
- Added `MemoryRetrieverResult` model: protocol-level envelope with `status`, `contact_id`, `hits`, `candidate_count`, `notes`.

### `src/practical_chat_agent/services/memory_retrieval.py`
- Added `MemoryRetriever` protocol (typing.Protocol, runtime_checkable) with `retrieve(*, contact_id, query, limit) -> MemoryRetrieverResult`.
- Added `convert_retrieval_result()`: standalone converter from service-level `MemoryRetrievalResult` to `MemoryRetrieverResult`.
- Added `LocalMemoryRetriever`: adapter wrapping `MemoryRetrievalService`, satisfying the `MemoryRetriever` protocol via `with_context()` + `retrieve()`.

### `tests/test_memory_retriever_contract.py` (new)
- 40 tests covering MemoryHit validation, MemoryRetrieverResult validation, protocol conformance (isinstance check), LocalMemoryRetriever with/without context, conversion fidelity, limit enforcement, source provenance, score derivation from salience, evidence ref preservation, note carry-through, context isolation, JSON round-trip, and contract boundary assertions.

### `docs/data_contracts/memory_retriever_contract.md` (new)
- Contract document explaining models, protocol, adapter, T201 implementation guide, and intentional gaps.

### `docs/07_handoff.md`
- Added T200 worker completion record.

## Verification

- Compile: passed for models.py, memory_retrieval.py, chat_context.py.
- T200 tests: 40 passed.
- Full suite: 560 passed (40 new + 520 existing), no regressions.

## Remaining Risks

- `LocalMemoryRetriever` requires agent/event context before retrieval — it does not support standalone query-only retrieval. T201's approved-store retriever will have a simpler standalone path.
- The protocol does not yet support async retrieval. If async is needed later, a separate `AsyncMemoryRetriever` protocol can be added without breaking the sync contract.
- No ChatContext wiring is done yet. T201 or a later wiring task will integrate retriever results into the context assembly pipeline.
- `MemoryHit.source` is a free-form string with documented convention values but no Literal enforcement. This is intentional to keep the contract open for future adapter sources without model changes.
