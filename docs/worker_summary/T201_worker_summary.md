# T201 Worker Summary

## Task

T201: Local Approved-Store Retriever — implement a `LocalApprovedStoreRetriever` that satisfies the T200 `MemoryRetriever` protocol over approved local memory store records using simple deterministic filters.

## What Changed

### `src/practical_chat_agent/services/memory_retrieval.py`
- Added `from pathlib import Path` import.
- Added `MemoryFactStoreFile`, `MemoryFactStoreRecord` to model imports.
- Added `LocalApprovedStoreRetriever` class:
  - Constructor takes `store_path: Path` (file or directory containing `memory_fact_store.json`).
  - `retrieve()` loads store from disk, filters to eligible records, applies optional query, sorts deterministically, and enforces limit.
  - Eligibility: `subject_id == contact_id`, `is_runtime_ready() == True`, `evidence_validation_status == "passed"`.
  - Query: case-insensitive substring match on claim text (skipped if query is None or whitespace).
  - Sorting: importance desc, confidence desc, memory_id asc.
  - Score derived from `MemoryFactCandidate.importance`.
  - Memory type mapped via `to_runtime_memory_type()`.
  - All hits carry `source="approved_store"`.
  - Status `"not_configured"` when store file not found, `"error"` when unparseable.

### `tests/test_local_approved_store_retriever.py` (new)
- 63 tests covering: protocol conformance, approved record retrieval, excluded records (candidate/rejected/frozen/archived/not-reviewed/failed-validation/wrong-contact), query filtering (match, case-insensitive, no-match, None, empty, whitespace), limit enforcement, source provenance, score derivation, memory-type mapping (all 5 distillation types), evidence-ref preservation, deterministic ordering (importance/confidence/memory_id), store path resolution (file vs directory), edge cases (nonexistent path, invalid JSON, wrong schema, empty store, directory without store), notes content, contract boundary assertions (no raw/embedding/write/file/review fields), JSON round-trip, and candidate count.

### `docs/data_contracts/memory_retriever_contract.md`
- Replaced T201 implementation guide with T201 implementation record documenting the `LocalApprovedStoreRetriever` design, retrieval behavior, eligibility filters, scoring, sorting, status values, and exclusion rules.

### `docs/07_handoff.md`
- Added T201 worker completion record at the top.

## Verification

- Compile: passed for models.py, memory_retrieval.py, chat_context.py.
- T201 tests: 63 passed.
- T200 + T201 tests: 103 passed.
- Full suite: 644 passed (63 new + 581 existing), no regressions.

## Remaining Risks

- `LocalApprovedStoreRetriever` reads the store file from disk on every `retrieve()` call. For high-frequency use, a caching layer could be added later, but the current offline-first workflow does not require it.
- The retriever does not yet integrate with `ChatContextAssembler`. A later wiring task will connect retriever results into the context assembly pipeline.
- Query matching is simple substring; T202 retrieval eval may reveal whether more sophisticated matching is needed.
- `MemoryFactCandidate.evidence_refs` requires `min_length=1`, so hits always have at least one evidence ref. This is a schema-level constraint from T120, not a T201 limitation.
- The protocol does not yet support async retrieval. If async is needed later, a separate `AsyncMemoryRetriever` protocol can be added without breaking the sync contract.
