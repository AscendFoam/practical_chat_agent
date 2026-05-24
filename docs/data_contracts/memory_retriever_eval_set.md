# Memory Retrieval Eval Set Contract

## Purpose

This contract defines a committed synthetic retrieval eval set that exercises `MemoryRetriever` implementations through the public `retrieve()` surface. The eval set is designed to be:

- **Synthetic**: contains no private chat content, real names, real platform IDs, or real file paths.
- **Deterministic**: the same store produces the same results on every run.
- **Reusable**: any `MemoryRetriever` implementation (local or external adapter) can be tested against the same eval cases.
- **Committed**: the eval set lives in `tests/test_memory_retriever_eval_set.py` and is runnable in CI.

## Scope

### In scope

- Synthetic store fixture with multiple contacts, memory types, and statuses.
- Eval case contract (`RetrievalEvalCase` dataclass) specifying expected retrieval behavior.
- Generic eval runner (`run_eval_case()`) that asserts expectations against any `MemoryRetriever`.
- Eval cases covering: relevant hits, wrong-contact exclusion, non-runtime-ready exclusion, query miss, deterministic ordering, limit enforcement, case-insensitive query, substring query, cross-contact isolation, unknown-contact boundary, combined exclusions.
- Contract boundary tests for source provenance, score boundedness, evidence ref preservation, memory type validity, JSON round-trip, and store immutability.
- Coverage audit tests ensuring all required eval dimensions are present.
- Reuse demonstration showing how a future retriever implementation would use the same cases.

### Out of scope

- Retrieval algorithm or scoring improvements.
- Vector DB, Mem0, Zep, embedding calls, or external provider calls.
- ChatContextAssembler, ReplyPlanner, policy engine, send gate, or platform adapter integration.
- Raw chat transcript retrieval.
- Runtime mutation of memory stores.

## Synthetic Store

The synthetic store is built by `build_synthetic_eval_store()` in `tests/test_memory_retriever_eval_set.py`.

### Contact: `synth_alice`

**Approved records (6)** — sorted by importance descending:

| memory_id | claim | distillation_type | importance | confidence | runtime_type |
|---|---|---|---|---|---|
| mem_alice_01 | Alice prefers morning coffee with oat milk | procedural | 0.90 | 0.85 | PREFERENCE |
| mem_alice_03 | Alice and the user share a college friendship dating back to 2018 | relationship | 0.85 | 0.80 | RELATIONSHIP |
| mem_alice_05 | Alice enjoys weekend hiking trips in the mountains | episodic | 0.75 | 0.85 | FACT |
| mem_alice_02 | Alice works as a UX designer at a startup | semantic | 0.70 | 0.90 | FACT |
| mem_alice_04 | Alice often feels stressed about project deadlines | reflection | 0.60 | 0.75 | REFLECTION |
| mem_alice_06 | Alice likes dark chocolate more than milk chocolate | procedural | 0.50 | 0.70 | PREFERENCE |

All approved records have: `status="approved"`, `reviewed_by_human=True`, `last_decision="approved"`, `evidence_validation_status="passed"`, and 2 evidence refs each.

**Excluded records (6)** — none should appear in retrieval results:

| memory_id | exclusion reason |
|---|---|
| mem_alice_07 | candidate status |
| mem_alice_08 | rejected status |
| mem_alice_09 | frozen status |
| mem_alice_10 | archived status |
| mem_alice_11 | not human-reviewed |
| mem_alice_12 | failed evidence validation |

### Contact: `synth_bob`

**Approved records (3)**:

| memory_id | claim | distillation_type | importance | confidence | runtime_type |
|---|---|---|---|---|---|
| mem_bob_01 | Bob is a software engineer at a tech company | semantic | 0.80 | 0.90 | FACT |
| mem_bob_02 | Bob prefers afternoon tea over coffee | procedural | 0.70 | 0.80 | PREFERENCE |
| mem_bob_03 | Bob and the user met at a coding bootcamp | relationship | 0.65 | 0.75 | RELATIONSHIP |

## Eval Case Contract

### RetrievalEvalCase

```python
@dataclass(frozen=True)
class RetrievalEvalCase:
    case_id: str                      # unique identifier
    description: str                  # what the case verifies
    contact_id: str                   # contact to query
    query: str | None                 # optional text query
    limit: int                        # max hits
    expected_status: str              # expected result status
    expected_hit_memory_ids: list[str] | None  # ordered ids, or None
    expected_min_hits: int            # lower bound on hit count
    expected_max_hits: int            # upper bound on hit count
    forbidden_memory_ids: list[str]   # ids that must not appear
    expected_candidate_count: int | None  # exact candidate_count, or None
    tags: list[str]                   # dimension labels
```

### Eval Cases

| case_id | contact | query | limit | expected hits | tags |
|---|---|---|---|---|---|
| E01_query_single_hit | synth_alice | "coffee" | 8 | mem_alice_01 | relevant_hits, query |
| E02_all_approved_no_query | synth_alice | None | 8 | all 6 approved (importance-desc) | relevant_hits, ordering |
| E03_query_miss_empty | synth_alice | "quantum physics" | 8 | 0 | query, boundary |
| E04_candidate_excluded | synth_alice | None | 20 | no mem_alice_07 | exclusion |
| E05_rejected_excluded | synth_alice | None | 20 | no mem_alice_08 | exclusion |
| E06_frozen_excluded | synth_alice | None | 20 | no mem_alice_09 | exclusion |
| E07_archived_excluded | synth_alice | None | 20 | no mem_alice_10 | exclusion |
| E08_not_reviewed_excluded | synth_alice | None | 20 | no mem_alice_11 | exclusion |
| E09_failed_validation_excluded | synth_alice | None | 20 | no mem_alice_12 | exclusion |
| E10_cross_contact_isolation | synth_alice | "engineer" | 8 | 0 (engineer is bob's) | exclusion, cross_contact |
| E11_deterministic_ordering | synth_alice | None | 8 | exact 6-id order | ordering |
| E12_limit_enforcement | synth_alice | None | 3 | top 3 | boundary, limit |
| E13_unknown_contact_empty | synth_unknown | None | 8 | 0 | boundary |
| E14_case_insensitive_query | synth_alice | "COFFEE" | 8 | mem_alice_01 | query |
| E15_substring_query | synth_alice | "oat milk" | 8 | mem_alice_01 | query |
| E16_second_contact | synth_bob | None | 8 | all 3 bob records | relevant_hits, cross_contact |
| E17_all_exclusions_combined | synth_alice | None | 20 | exactly 6, no excluded ids | exclusion, boundary |
| E18_query_multi_match | synth_alice | "milk" | 8 | mem_alice_01, mem_alice_06 | relevant_hits, query |
| E19_limit_cuts_query_matches | synth_alice | "milk" | 1 | mem_alice_01 | query, limit |

### Required tag coverage

Every eval set must have cases covering these tags:

- `relevant_hits` — positive retrieval cases
- `exclusion` — non-runtime-ready record exclusion
- `query` — query-based filtering behavior
- `ordering` — deterministic hit ordering
- `boundary` — edge cases (unknown contact, limit, query miss)

### Coverage audit

The test class `TestEvalCoverageAudit` verifies:
- All required tags are present in the eval case table.
- All excluded record types (candidate, rejected, frozen, archived, not-reviewed, failed-validation) have at least one explicit forbidden-id check.
- Multiple contacts are exercised.
- The synthetic store builds deterministically.
- At least one ordering case specifies exact expected ids.

## How to Reuse with a Different Retriever

A future `MemoryRetriever` implementation (e.g., T203 external adapter) can reuse this eval set by:

1. Building or pointing to the same synthetic store data.
2. Instantiating the new retriever.
3. Passing it to `run_eval_case(retriever, case)` for each eval case.

Example:

```python
from tests.test_memory_retriever_eval_set import (
    EVAL_CASES,
    RetrievalEvalCase,
    build_synthetic_eval_store,
    run_eval_case,
)

def test_external_adapter_eval():
    store = build_synthetic_eval_store()
    # ... set up external adapter pointing at the store data ...
    retriever: MemoryRetriever = ExternalAdapterRetriever(...)
    for case in EVAL_CASES:
        run_eval_case(retriever, case)
```

The `run_eval_case` function only uses the `MemoryRetriever.retrieve()` method and inspects the returned `MemoryRetrieverResult`. It does not access implementation-private state.

## Contract Boundary Tests

In addition to the parametrised eval cases, the test module includes boundary tests that verify hit-level properties:

- **Source provenance**: all hits have `source="approved_store"`.
- **Score boundedness**: all `score` values are in `[0.0, 1.0]`.
- **Evidence refs preserved**: all hits have non-empty `evidence_refs`.
- **Memory type validity**: all `memory_type` values are valid `MemoryType` enum members.
- **JSON round-trip**: hits and results survive serialization/deserialization.
- **Store immutability**: calling `retrieve()` does not modify the store file.
