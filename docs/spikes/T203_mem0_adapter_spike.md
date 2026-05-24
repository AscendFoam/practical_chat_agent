# T203: Mem0 Adapter Spike — Findings

## Status

Spike complete. A minimal optional adapter boundary was implemented and committed. The adapter is behind `MemoryRetriever.retrieve()` / `MemoryRetrieverResult` and degrades safely to `not_configured` when the optional dependency or configuration is absent.

## What Was Evaluated

Whether an optional Mem0-backed retriever adapter can fit behind the existing `MemoryRetriever` contract without weakening review-first memory semantics.

## Implementation

### `Mem0AdapterRetriever`

Location: `src/practical_chat_agent/services/optional_mem0_adapter.py`

- Implements `MemoryRetriever` protocol (runtime `isinstance` check passes).
- Accepts a `mem0` cloud API key. If absent or empty, every `retrieve()` returns `status="not_configured"`.
- If `mem0` package is not installed, returns `not_configured` (lazy import, no hard dependency).
- Uses `mem0.Memory.search(query, user_id, limit)` when a query is provided.
- Uses `mem0.Memory.get_all(user_id)` when no query is provided.
- Converts Mem0 results to `MemoryHit` with `source="external_adapter"`.
- Does not call `add()`, `delete()`, `update()`, or any write method on the Mem0 client.
- Does not read raw chat transcripts.

### Test Coverage

Location: `tests/test_optional_mem0_adapter_spike.py`

44 tests covering:
- Not-configured degradation (6 tests): no key, empty key, whitespace key, reason text, multiple calls.
- Protocol conformance (2 tests): isinstance checks with and without client.
- Search with query (2 tests): hit extraction, empty results.
- Get-all without query (4 tests): hit extraction, empty, default score, candidate count.
- Limit enforcement (2 tests): search and get-all paths.
- Error handling (2 tests): client exceptions → error status.
- Field mapping (12 tests): contact_id, score, score clamping, invalid score, evidence refs, missing-id skip, missing-memory skip, non-dict skip, notes content, hit count.
- Memory type inference (5 tests): preference, relationship, reflection, fact defaults, combined types.
- Contract boundaries (7 tests): source provenance, score bounds, no raw transcript, no embedding, no write, JSON round-trip, no client mutation.
- T202 eval shape reuse (4 tests): success case, not-configured case, forbidden-id check, get-all path selection.

All tests use `unittest.mock.MagicMock` to inject a mock Mem0 client. No Mem0 package or network access is required.

## Findings

### What works

1. **Protocol fit**: The `MemoryRetriever` protocol is flexible enough for external adapters. The adapter satisfies `isinstance(retriever, MemoryRetriever)` at runtime.
2. **Graceful degradation**: The lazy-import + no-key pattern produces `not_configured` cleanly when the package is absent.
3. **Result shape preservation**: `MemoryRetrieverResult` with `MemoryHit` items works for external results. JSON round-trip is preserved.
4. **No write surface**: The adapter calls only `search()` and `get_all()`, never `add()`, `delete()`, or `update()`.
5. **Eval reuse**: The T202 eval case runner shape can test the adapter through the protocol interface.

### Limitations and gaps

1. **No review/approval enforcement**: Mem0 manages its own memory lifecycle. The adapter cannot enforce that returned facts have been human-reviewed or evidence-validated the way `LocalApprovedStoreRetriever` does. The adapter trusts Mem0's results as-is.
2. **Heuristic memory type inference**: Mem0 does not categorise memories by type. The adapter uses keyword heuristics (`_infer_memory_type`) that map to `MemoryType` values. This is approximate and may misclassify edge cases.
3. **Synthetic evidence refs**: The adapter fabricates `evidence_refs` as `["mem0:<id>"]` because Mem0 results do not carry structured evidence references traceable to source events. This is weaker than the approved-store path's real event/chunk refs.
4. **Ordering depends on Mem0**: The adapter does not sort results itself; it relies on Mem0's internal scoring and ordering. Deterministic ordering is not guaranteed.
5. **SDK version sensitivity**: The Mem0 Python SDK has undergone API changes across versions. The adapter targets the cloud API pattern (`Memory(api_key=...)`, `search()`, `get_all()`). SDK version pinning would be needed for production use.
6. **Error recovery**: The adapter catches all exceptions and returns `status="error"`, but does not implement retry, rate-limit, or exponential backoff.

### Recommendation

The spike demonstrates that an optional Mem0 adapter boundary **is technically feasible** behind the `MemoryRetriever` contract. However, for production adoption, the following would need to be addressed:

- A review/approval integration layer between Mem0 and the project's human-review workflow.
- Structured evidence ref mapping from Mem0 memories back to source events.
- SDK version pinning and stability testing.
- Error recovery, retry, and rate-limit strategies.
- Security review of API key handling and data transmission.

Until these are addressed, the local approved-store retriever (`LocalApprovedStoreRetriever`) should remain the primary retrieval path, and the Mem0 adapter should remain an optional, off-by-default experiment.

## No Mem0 dependency introduced

- The `mem0` / `mem0ai` package is NOT added to any requirements file.
- The import is lazy (inside `__init__` / `_try_init_client`).
- If the package is absent, the adapter returns `not_configured`.
- Committed tests do not require Mem0 or network access.
