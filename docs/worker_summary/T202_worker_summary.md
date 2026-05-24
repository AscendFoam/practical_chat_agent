# T202 Worker Summary

## Task

T202: Retrieval Eval Set — create a committed synthetic retrieval eval set that can evaluate `MemoryRetrieverResult` quality and boundary behavior for local retrievers without using private chat content.

## What Changed

### `tests/test_memory_retriever_eval_set.py` (new)

- `RetrievalEvalCase` dataclass: eval case contract with case_id, description, contact_id, query, limit, expected_status, expected_hit_memory_ids, expected_min/max_hits, forbidden_memory_ids, expected_candidate_count, and tags.
- `build_synthetic_eval_store()`: deterministic synthetic store builder producing 15 records across 2 contacts (synth_alice: 6 approved + 6 excluded; synth_bob: 3 approved).
- `run_eval_case()`: generic eval runner that takes any `MemoryRetriever` and a `RetrievalEvalCase`, runs `retrieve()`, and asserts expectations.
- 19 eval cases (E01–E19) covering:
  - Relevant hits: single-match query, all-approved no-query, second-contact retrieval, multi-match query.
  - Exclusion: candidate, rejected, frozen, archived, not-human-reviewed, failed-evidence-validation (each with explicit forbidden_id), all combined.
  - Query: case-insensitive, substring, miss (0 hits), multi-match, limit-cuts-query.
  - Ordering: deterministic importance-desc ordering verified.
  - Boundary: unknown-contact empty, limit enforcement with candidate_count, query miss.
  - Cross-contact: isolation (bob's facts don't leak to alice), independent second-contact retrieval.
- 8 contract boundary tests: source provenance, score boundedness, evidence refs non-empty, memory type validity, hit JSON round-trip, result JSON round-trip, store immutability.
- 6 coverage audit tests: required tags present, all excluded types covered, multiple contacts, deterministic store build, ordering case requirements, expected record count.
- 1 reuse demonstration: `run_eval_case()` works through the `MemoryRetriever` protocol interface.

### `docs/data_contracts/memory_retriever_eval_set.md` (new)

- Full eval set contract documentation: purpose, scope, synthetic store layout, eval case table, required tag coverage, reuse instructions, contract boundary test descriptions.

### `docs/data_contracts/memory_retriever_contract.md`

- Added T202 eval set reference section before Intentional Gaps.

### `docs/07_handoff.md`

- Added T202 worker completion record at the top.

## Verification

- T202 tests: 33 passed (19 eval cases + 8 boundary + 6 audit + 0 failures).
- T200 + T201 + T202 tests: 136 passed.
- Full suite: 677 passed (33 new + 644 existing), no regressions.

## Remaining Risks

- The eval set tests only `LocalApprovedStoreRetriever`. When T203 adds an external adapter, the adapter may produce different hit ordering or scoring. The `run_eval_case()` runner supports `expected_hit_memory_ids=None` (order not checked) to accommodate adapters that don't guarantee the same ordering semantics.
- Query matching is simple substring; the eval cases reflect this. If a future adapter uses semantic matching, some query-miss cases (E03) might need adjustment.
- The eval set does not test `LocalMemoryRetriever` (the T200 adapter over `MemoryRetrievalService`) because that adapter requires live `AgentProfile`, `InboundEvent`, and `MemoryFact` objects. A future eval set could extend coverage to that adapter.
- The synthetic store has no real-world distribution of importance/confidence values; it is designed for deterministic boundary coverage, not representativeness.
