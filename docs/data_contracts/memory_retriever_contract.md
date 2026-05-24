# MemoryRetriever Interface Contract

## Purpose

This contract defines the `MemoryRetriever` protocol, the `MemoryHit` data model, and the `MemoryRetrieverResult` envelope. Together they establish a retriever abstraction that:

- sits above the existing local retrieval logic in `MemoryRetrievalService`,
- is narrow enough for T201 to implement a local approved-store retriever without guessing intent,
- is open enough for later M9 tasks (T202 eval set, T203 optional external adapter spike) to build on, and
- preserves the project's approved-only, review-safe, offline-first constraints.

## Scope

### In scope

- `MemoryRetriever` protocol definition (structural typing via `typing.Protocol`).
- `MemoryHit` data contract: the review-safe retrieval result shape.
- `MemoryRetrieverResult` envelope: status, hits, metadata.
- `LocalMemoryRetriever`: a thin adapter that wraps the existing `MemoryRetrievalService` and converts its output to the new contract.
- `convert_retrieval_result()`: a standalone converter from service-level `MemoryRetrievalResult` to protocol-level `MemoryRetrieverResult`.

### Out of scope

- Vector DB integration.
- Mem0 / Zep / external adapter implementation.
- Auto-write or runtime mutation of memories.
- Raw chat transcript retrieval.
- Reply-planner or policy-engine behavior changes.
- Embedding calls or external provider calls.
- ChatContext field changes or ChatContextAssembler wiring.

## Data Models

### MemoryHit

Location: `src/practical_chat_agent/core/models.py`

```python
class MemoryHit(BaseModel):
    hit_id: str              # auto-generated, unique per retrieval event
    memory_id: str           # required, min_length=1, reference to underlying memory
    fact: str                # required, min_length=1, review-safe text content
    memory_type: MemoryType  # FACT | PREFERENCE | RELATIONSHIP | REFLECTION
    score: float             # 0.0-1.0, retrieval relevance score
    evidence_refs: list[str] # traceability refs to source events/chunks
    source: str              # required, min_length=1, provenance label
```

Required fields: `memory_id`, `fact`, `source`.

Constraints:
- `score` is bounded [0.0, 1.0].
- `hit_id` is auto-generated per retrieval event and is NOT stable across calls.
- `memory_id` references the underlying `MemoryFact.memory_id` or equivalent stable ID.
- `source` indicates where the hit came from. Defined convention values:
  - `"local_memory_retrieval"` — from the existing `MemoryRetrievalService`.
  - `"approved_store"` — for T201 local approved-store retriever.
  - `"external_adapter"` — reserved for future T203 optional spike.
  - Other values are allowed but should be documented.

What `MemoryHit` deliberately does NOT carry:
- Raw transcript content or chat history text.
- Embedding vectors or similarity scores.
- Write, save, or mutation methods.
- Private metadata (e.g., internal file paths, review history).

### MemoryRetrieverResult

Location: `src/practical_chat_agent/core/models.py`

```python
class MemoryRetrieverResult(BaseModel):
    status: Literal["success", "not_configured", "error"]
    contact_id: str | None
    hits: list[MemoryHit]
    candidate_count: int
    notes: list[str]
```

Status values:
- `"success"` — retrieval completed, hits may be empty if nothing matched.
- `"not_configured"` — the retriever lacks required context or configuration.
- `"error"` — retrieval failed due to an error condition.

### Relationship to existing models

| Existing model | New model | Relationship |
|---|---|---|
| `MemoryFact` | `MemoryHit` | `MemoryHit` is a thinner, retrieval-focused projection of `MemoryFact`. Carries `memory_id` as reference back to the source fact. |
| `MemoryRetrievalResult` | `MemoryRetrieverResult` | `MemoryRetrieverResult` is the protocol-level envelope. `convert_retrieval_result()` converts between them. |

## Protocol

### MemoryRetriever

Location: `src/practical_chat_agent/services/memory_retrieval.py`

```python
@runtime_checkable
class MemoryRetriever(Protocol):
    def retrieve(
        self,
        *,
        contact_id: str,
        query: str | None = None,
        limit: int = 8,
    ) -> MemoryRetrieverResult: ...
```

Parameters:
- `contact_id` (required): the contact to retrieve memories for.
- `query` (optional): text query for relevance matching. Implementations may ignore this if they don't support query-based retrieval.
- `limit` (default 8): maximum number of hits to return.

Implementations MUST:
- Return only approved, review-safe content in `MemoryHit` items.
- Never read raw chat transcripts.
- Never auto-write or mutate memory.
- Preserve `evidence_refs` for traceability.

Implementations MAY:
- Return fewer than `limit` hits if fewer memories match.
- Ignore the `query` parameter if the retrieval strategy doesn't use text matching.
- Use internal scoring/ranking strategies as appropriate.

## Adapter

### LocalMemoryRetriever

Location: `src/practical_chat_agent/services/memory_retrieval.py`

Wraps `MemoryRetrievalService` and satisfies the `MemoryRetriever` protocol.

Construction:
```python
adapter = LocalMemoryRetriever(service)
```

Context management:
```python
contextualized = adapter.with_context(agent=agent, event=event, candidates=memories)
```

`with_context()` returns a new `LocalMemoryRetriever` instance with the provided context, leaving the original adapter unchanged.

Retrieval:
- Without context: returns `MemoryRetrieverResult(status="not_configured")`.
- With context: delegates to `MemoryRetrievalService.retrieve()` and converts the result via `convert_retrieval_result()`.

### convert_retrieval_result()

A standalone function that converts `MemoryRetrievalResult` to `MemoryRetrieverResult`:
- Maps `MemoryFact.selected_hits` to `MemoryHit` items with `source="local_memory_retrieval"`.
- Carries `salience` as the `score`.
- Preserves `evidence_refs`, `memory_type`, and `fact` text.
- Applies the `limit` parameter.
- Carries `retrieval_notes` through to `notes`.

## T201 Implementation Guide

T201 will implement a `LocalApprovedStoreRetriever` that:

1. Implements the `MemoryRetriever` protocol.
2. Reads from approved memory-fact store records (already validated by evidence validation and human review).
3. Returns `MemoryHit` items with `source="approved_store"`.
4. Filters to only runtime-ready records (`is_runtime_ready() == True`).
5. May use `query` for simple text matching or return all approved facts up to `limit`.

The constructor should accept the store file path and validation report path, similar to how `ChatContextAssembler` loads approved store context today.

## T201 Implementation Record

### LocalApprovedStoreRetriever

Location: `src/practical_chat_agent/services/memory_retrieval.py`

Construction:
```python
retriever = LocalApprovedStoreRetriever(store_path)
```

Parameters:
- `store_path` (Path): Path to a `memory_fact_store.json` file, or a directory containing one.

The retriever satisfies `isinstance(retriever, MemoryRetriever)` at runtime.

### Retrieval behavior

```python
result = retriever.retrieve(contact_id="user_1", query="coffee", limit=5)
```

- **Store loading**: Reads `MemoryFactStoreFile` from disk on each `retrieve()` call. No caching, no external calls.
- **Eligibility filter**: A record is eligible only when:
  - `record.memory_fact.subject_id == contact_id`
  - `record.is_runtime_ready()` returns `True` (implies `status == "approved"`, `reviewed_by_human == True`, `last_decision == "approved"`)
  - `record.review_metadata.evidence_validation_status == "passed"`
- **Query matching**: If `query` is provided and non-empty, case-insensitive substring match on `memory_fact.claim`. Records not containing the query substring are excluded.
- **Scoring**: `MemoryHit.score` is derived from `MemoryFactCandidate.importance`.
- **Sorting**: Records are sorted by `importance` descending, then `confidence` descending, then `memory_id` ascending for determinism.
- **Limit**: Applied after sorting.
- **Memory type mapping**: Uses `MemoryFactCandidate.to_runtime_memory_type()` to map distillation types to runtime `MemoryType`.
- **Source**: All hits carry `source="approved_store"`.

### Status values

- `"success"`: Store loaded successfully, hits may be empty.
- `"not_configured"`: Store file not found at the given path.
- `"error"`: Store file exists but could not be parsed.

### What is excluded

Candidate, rejected, frozen, archived records, not-human-reviewed records, records with failed/not-run evidence validation, and records with wrong contact_id never appear in hits.

### What MemoryHit does NOT carry

No raw transcript content, no embedding vectors, no file paths, no review metadata, no write/mutation methods.

## Intentional Gaps

These are explicitly deferred to later tasks:

- **No ChatContext wiring**: T200 does not change `ChatContext.memory_hits` or `ChatContextAssembler`. T201 or later wiring tasks will integrate retriever results.
- **No external adapters**: T203 may spike a Mem0/Zep adapter, but T200 only defines the interface.
- **No semantic scoring**: The current `score` field is derived from `salience`. Future tasks may implement embedding-based or LLM-based scoring behind the same `MemoryRetriever` interface.
- **No async support**: The protocol is synchronous. An async variant can be added later if needed without breaking the sync contract.
