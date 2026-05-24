"""T202: Retrieval eval set — synthetic, committed eval cases for MemoryRetriever.

This module defines a reusable retrieval eval set that:

- Uses only synthetic data (no private chat content).
- Exercises retrievers through the public ``MemoryRetriever.retrieve()`` surface.
- Covers relevant hits, exclusion, query behaviour, deterministic ordering, and boundary cases.
- Can be reused by any ``MemoryRetriever`` implementation (local or external adapter).

Structure
---------

1. **Eval case contract** — ``RetrievalEvalCase`` dataclass describing expected retrieval behaviour.
2. **Synthetic store builder** — ``build_synthetic_eval_store()`` producing a deterministic fixture.
3. **Generic eval runner** — ``run_eval_case()`` that asserts expectations on any ``MemoryRetriever``.
4. **Eval case table** — ``EVAL_CASES`` list covering required eval dimensions.
5. **Parametrised tests** — each case is one pytest sub-test.
6. **Contract boundary tests** — source provenance, score boundedness, evidence refs, memory-type mapping.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import pytest

from practical_chat_agent.core.enums import MemoryType
from practical_chat_agent.core.models import (
    DistilledArtifactReviewMetadata,
    MemoryFactCandidate,
    MemoryFactStoreFile,
    MemoryFactStoreRecord,
    MemoryHit,
    MemoryRetrieverResult,
)
from practical_chat_agent.services.memory_retrieval import (
    LocalApprovedStoreRetriever,
    MemoryRetriever,
)


# ---------------------------------------------------------------------------
# 1. Eval case contract
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class RetrievalEvalCase:
    """One retrieval evaluation scenario.

    Fields
    ------
    case_id
        Unique identifier (used as pytest test id).
    description
        Human-readable summary of what the case verifies.
    contact_id
        The contact to pass to ``retrieve()``.
    query
        Optional text query.
    limit
        Maximum number of hits.
    expected_status
        Expected ``MemoryRetrieverResult.status`` value.
    expected_hit_memory_ids
        If not ``None``, the *exact ordered* list of expected ``memory_id`` values.
        If ``None``, order is not checked (use ``expected_min/max_hits`` instead).
    expected_min_hits
        Lower bound on hit count (inclusive).
    expected_max_hits
        Upper bound on hit count (inclusive).
    forbidden_memory_ids
        ``memory_id`` values that must **not** appear in any hit.
    expected_candidate_count
        If not ``None``, the exact expected ``candidate_count``.
    tags
        Dimension labels for coverage auditing (e.g. ``"relevant_hits"``,
        ``"exclusion"``, ``"query"``, ``"ordering"``, ``"boundary"``).
    """

    case_id: str
    description: str
    contact_id: str
    query: str | None
    limit: int
    expected_status: str
    expected_hit_memory_ids: list[str] | None
    expected_min_hits: int
    expected_max_hits: int
    forbidden_memory_ids: list[str] = field(default_factory=list)
    expected_candidate_count: int | None = None
    tags: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# 2. Synthetic store builder
# ---------------------------------------------------------------------------


def _approved_review(
    *,
    evidence_validation_status: str = "passed",
) -> DistilledArtifactReviewMetadata:
    return DistilledArtifactReviewMetadata(
        review_state="reviewed",
        reviewed_by_human=True,
        last_decision="approved",
        evidence_validation_status=evidence_validation_status,
    )


def _excluded_review(
    *,
    status: str,
    last_decision: str | None = None,
    reviewed_by_human: bool = True,
    evidence_validation_status: str = "passed",
) -> DistilledArtifactReviewMetadata:
    return DistilledArtifactReviewMetadata(
        review_state="reviewed" if reviewed_by_human else "pending_human_review",
        reviewed_by_human=reviewed_by_human,
        last_decision=last_decision if last_decision else status,
        evidence_validation_status=evidence_validation_status,
    )


def build_synthetic_eval_store() -> MemoryFactStoreFile:
    """Return a deterministic synthetic store with two contacts and mixed statuses.

    Approved records for ``synth_alice`` (6 total):
      - mem_alice_01: importance=0.90, confidence=0.85, type=procedural
      - mem_alice_03: importance=0.85, confidence=0.80, type=relationship
      - mem_alice_05: importance=0.75, confidence=0.85, type=episodic
      - mem_alice_02: importance=0.70, confidence=0.90, type=semantic
      - mem_alice_04: importance=0.60, confidence=0.75, type=reflection
      - mem_alice_06: importance=0.50, confidence=0.70, type=procedural

    Excluded records for ``synth_alice`` (6 total):
      - mem_alice_07: candidate status
      - mem_alice_08: rejected status
      - mem_alice_09: frozen status
      - mem_alice_10: archived status
      - mem_alice_11: not human-reviewed
      - mem_alice_12: failed evidence validation

    Approved records for ``synth_bob`` (3 total):
      - mem_bob_01: importance=0.80, confidence=0.90, type=semantic
      - mem_bob_02: importance=0.70, confidence=0.80, type=procedural
      - mem_bob_03: importance=0.65, confidence=0.75, type=relationship
    """
    records: list[MemoryFactStoreRecord] = []

    # --- synth_alice: approved records ---
    alice_approved = [
        ("mem_alice_01", "Alice prefers morning coffee with oat milk", "procedural", 0.90, 0.85),
        ("mem_alice_02", "Alice works as a UX designer at a startup", "semantic", 0.70, 0.90),
        ("mem_alice_03", "Alice and the user share a college friendship dating back to 2018", "relationship", 0.85, 0.80),
        ("mem_alice_04", "Alice often feels stressed about project deadlines", "reflection", 0.60, 0.75),
        ("mem_alice_05", "Alice enjoys weekend hiking trips in the mountains", "episodic", 0.75, 0.85),
        ("mem_alice_06", "Alice likes dark chocolate more than milk chocolate", "procedural", 0.50, 0.70),
    ]
    for mid, claim, mtype, imp, conf in alice_approved:
        records.append(
            MemoryFactStoreRecord(
                memory_fact=MemoryFactCandidate(
                    memory_id=mid,
                    subject_id="synth_alice",
                    claim=claim,
                    memory_type=mtype,
                    importance=imp,
                    confidence=conf,
                    status="approved",
                    sensitivity="low",
                    evidence_refs=[f"evt_{mid}_a", f"evt_{mid}_b"],
                ),
                review_metadata=_approved_review(),
            )
        )

    # --- synth_alice: excluded records ---
    excluded_defs: list[tuple[str, str, str, str | None, bool, str]] = [
        ("mem_alice_07", "Alice candidate fact about travel", "candidate", "candidate", True, "passed"),
        ("mem_alice_08", "Alice rejected fact about cooking", "rejected", "rejected", True, "passed"),
        ("mem_alice_09", "Alice frozen fact about hobbies", "frozen", "frozen", True, "passed"),
        ("mem_alice_10", "Alice archived fact about music", "archived", "archived", True, "passed"),
        ("mem_alice_11", "Alice not reviewed fact about sports", "approved", None, False, "passed"),
        ("mem_alice_12", "Alice failed validation fact about books", "approved", "approved", True, "failed"),
    ]
    for mid, claim, status, last_dec, human_reviewed, ev_status in excluded_defs:
        records.append(
            MemoryFactStoreRecord(
                memory_fact=MemoryFactCandidate(
                    memory_id=mid,
                    subject_id="synth_alice",
                    claim=claim,
                    memory_type="semantic",
                    importance=0.50,
                    confidence=0.50,
                    status=status,
                    sensitivity="low",
                    evidence_refs=[f"evt_{mid}"],
                ),
                review_metadata=_excluded_review(
                    status=status,
                    last_decision=last_dec,
                    reviewed_by_human=human_reviewed,
                    evidence_validation_status=ev_status,
                ),
            )
        )

    # --- synth_bob: approved records ---
    bob_approved = [
        ("mem_bob_01", "Bob is a software engineer at a tech company", "semantic", 0.80, 0.90),
        ("mem_bob_02", "Bob prefers afternoon tea over coffee", "procedural", 0.70, 0.80),
        ("mem_bob_03", "Bob and the user met at a coding bootcamp", "relationship", 0.65, 0.75),
    ]
    for mid, claim, mtype, imp, conf in bob_approved:
        records.append(
            MemoryFactStoreRecord(
                memory_fact=MemoryFactCandidate(
                    memory_id=mid,
                    subject_id="synth_bob",
                    claim=claim,
                    memory_type=mtype,
                    importance=imp,
                    confidence=conf,
                    status="approved",
                    sensitivity="low",
                    evidence_refs=[f"evt_{mid}_a", f"evt_{mid}_b"],
                ),
                review_metadata=_approved_review(),
            )
        )

    return MemoryFactStoreFile(records=records)


# ---------------------------------------------------------------------------
# 3. Generic eval runner
# ---------------------------------------------------------------------------


def run_eval_case(
    retriever: MemoryRetriever,
    case: RetrievalEvalCase,
) -> MemoryRetrieverResult:
    """Run one ``RetrievalEvalCase`` against any ``MemoryRetriever``.

    Returns the result for further inspection.  Raises ``AssertionError``
    on any expectation violation so that pytest reports failures clearly.
    """
    result = retriever.retrieve(
        contact_id=case.contact_id,
        query=case.query,
        limit=case.limit,
    )

    # Status
    assert result.status == case.expected_status, (
        f"[{case.case_id}] expected status={case.expected_status!r}, "
        f"got {result.status!r}"
    )

    # Contact id propagated
    assert result.contact_id == case.contact_id, (
        f"[{case.case_id}] contact_id mismatch: "
        f"expected {case.contact_id!r}, got {result.contact_id!r}"
    )

    # Hit count range
    assert case.expected_min_hits <= len(result.hits) <= case.expected_max_hits, (
        f"[{case.case_id}] hit count {len(result.hits)} "
        f"not in [{case.expected_min_hits}, {case.expected_max_hits}]"
    )

    # Ordered memory ids
    if case.expected_hit_memory_ids is not None:
        actual_ids = [h.memory_id for h in result.hits]
        assert actual_ids == case.expected_hit_memory_ids, (
            f"[{case.case_id}] ordered memory_ids mismatch: "
            f"expected {case.expected_hit_memory_ids}, got {actual_ids}"
        )

    # Forbidden ids
    if case.forbidden_memory_ids:
        actual_ids = {h.memory_id for h in result.hits}
        violations = actual_ids & set(case.forbidden_memory_ids)
        assert not violations, (
            f"[{case.case_id}] forbidden ids found in hits: {violations}"
        )

    # Candidate count
    if case.expected_candidate_count is not None:
        assert result.candidate_count == case.expected_candidate_count, (
            f"[{case.case_id}] candidate_count "
            f"expected {case.expected_candidate_count}, "
            f"got {result.candidate_count}"
        )

    return result


# ---------------------------------------------------------------------------
# 4. Eval case table
# ---------------------------------------------------------------------------


EVAL_CASES: list[RetrievalEvalCase] = [
    # -- relevant hits -------------------------------------------------------
    RetrievalEvalCase(
        case_id="E01_query_single_hit",
        description="Query 'coffee' matches exactly one approved record for synth_alice",
        contact_id="synth_alice",
        query="coffee",
        limit=8,
        expected_status="success",
        expected_hit_memory_ids=["mem_alice_01"],
        expected_min_hits=1,
        expected_max_hits=1,
        tags=["relevant_hits", "query"],
    ),
    RetrievalEvalCase(
        case_id="E02_all_approved_no_query",
        description="No query returns all 6 approved records for synth_alice in importance-desc order",
        contact_id="synth_alice",
        query=None,
        limit=8,
        expected_status="success",
        expected_hit_memory_ids=[
            "mem_alice_01",
            "mem_alice_03",
            "mem_alice_05",
            "mem_alice_02",
            "mem_alice_04",
            "mem_alice_06",
        ],
        expected_min_hits=6,
        expected_max_hits=6,
        expected_candidate_count=6,
        tags=["relevant_hits", "ordering"],
    ),
    # -- query miss ----------------------------------------------------------
    RetrievalEvalCase(
        case_id="E03_query_miss_empty",
        description="Query 'quantum physics' matches nothing for synth_alice",
        contact_id="synth_alice",
        query="quantum physics",
        limit=8,
        expected_status="success",
        expected_hit_memory_ids=[],
        expected_min_hits=0,
        expected_max_hits=0,
        expected_candidate_count=0,
        tags=["query", "boundary"],
    ),
    # -- exclusion: candidate ------------------------------------------------
    RetrievalEvalCase(
        case_id="E04_candidate_excluded",
        description="Candidate-status record is never returned",
        contact_id="synth_alice",
        query=None,
        limit=20,
        expected_status="success",
        expected_hit_memory_ids=None,
        expected_min_hits=0,
        expected_max_hits=20,
        forbidden_memory_ids=["mem_alice_07"],
        tags=["exclusion"],
    ),
    # -- exclusion: rejected -------------------------------------------------
    RetrievalEvalCase(
        case_id="E05_rejected_excluded",
        description="Rejected record is never returned",
        contact_id="synth_alice",
        query=None,
        limit=20,
        expected_status="success",
        expected_hit_memory_ids=None,
        expected_min_hits=0,
        expected_max_hits=20,
        forbidden_memory_ids=["mem_alice_08"],
        tags=["exclusion"],
    ),
    # -- exclusion: frozen ---------------------------------------------------
    RetrievalEvalCase(
        case_id="E06_frozen_excluded",
        description="Frozen record is never returned",
        contact_id="synth_alice",
        query=None,
        limit=20,
        expected_status="success",
        expected_hit_memory_ids=None,
        expected_min_hits=0,
        expected_max_hits=20,
        forbidden_memory_ids=["mem_alice_09"],
        tags=["exclusion"],
    ),
    # -- exclusion: archived -------------------------------------------------
    RetrievalEvalCase(
        case_id="E07_archived_excluded",
        description="Archived record is never returned",
        contact_id="synth_alice",
        query=None,
        limit=20,
        expected_status="success",
        expected_hit_memory_ids=None,
        expected_min_hits=0,
        expected_max_hits=20,
        forbidden_memory_ids=["mem_alice_10"],
        tags=["exclusion"],
    ),
    # -- exclusion: not human-reviewed ---------------------------------------
    RetrievalEvalCase(
        case_id="E08_not_reviewed_excluded",
        description="Not-human-reviewed record is never returned",
        contact_id="synth_alice",
        query=None,
        limit=20,
        expected_status="success",
        expected_hit_memory_ids=None,
        expected_min_hits=0,
        expected_max_hits=20,
        forbidden_memory_ids=["mem_alice_11"],
        tags=["exclusion"],
    ),
    # -- exclusion: failed evidence validation -------------------------------
    RetrievalEvalCase(
        case_id="E09_failed_validation_excluded",
        description="Record with failed evidence validation is never returned",
        contact_id="synth_alice",
        query=None,
        limit=20,
        expected_status="success",
        expected_hit_memory_ids=None,
        expected_min_hits=0,
        expected_max_hits=20,
        forbidden_memory_ids=["mem_alice_12"],
        tags=["exclusion"],
    ),
    # -- cross-contact isolation ---------------------------------------------
    RetrievalEvalCase(
        case_id="E10_cross_contact_isolation",
        description="Query 'engineer' returns no hits for synth_alice because that fact belongs to synth_bob",
        contact_id="synth_alice",
        query="engineer",
        limit=8,
        expected_status="success",
        expected_hit_memory_ids=[],
        expected_min_hits=0,
        expected_max_hits=0,
        forbidden_memory_ids=["mem_bob_01"],
        tags=["exclusion", "cross_contact"],
    ),
    # -- deterministic ordering ----------------------------------------------
    RetrievalEvalCase(
        case_id="E11_deterministic_ordering",
        description="All 6 approved synth_alice records in importance-desc order",
        contact_id="synth_alice",
        query=None,
        limit=8,
        expected_status="success",
        expected_hit_memory_ids=[
            "mem_alice_01",
            "mem_alice_03",
            "mem_alice_05",
            "mem_alice_02",
            "mem_alice_04",
            "mem_alice_06",
        ],
        expected_min_hits=6,
        expected_max_hits=6,
        tags=["ordering"],
    ),
    # -- limit enforcement ---------------------------------------------------
    RetrievalEvalCase(
        case_id="E12_limit_enforcement",
        description="Limit=3 returns top-3 hits; candidate_count still 6",
        contact_id="synth_alice",
        query=None,
        limit=3,
        expected_status="success",
        expected_hit_memory_ids=["mem_alice_01", "mem_alice_03", "mem_alice_05"],
        expected_min_hits=3,
        expected_max_hits=3,
        expected_candidate_count=6,
        tags=["boundary", "limit"],
    ),
    # -- unknown contact -----------------------------------------------------
    RetrievalEvalCase(
        case_id="E13_unknown_contact_empty",
        description="Querying a contact with no records returns success with 0 hits",
        contact_id="synth_unknown",
        query=None,
        limit=8,
        expected_status="success",
        expected_hit_memory_ids=[],
        expected_min_hits=0,
        expected_max_hits=0,
        tags=["boundary"],
    ),
    # -- case-insensitive query ----------------------------------------------
    RetrievalEvalCase(
        case_id="E14_case_insensitive_query",
        description="Query 'COFFEE' matches the same record as 'coffee'",
        contact_id="synth_alice",
        query="COFFEE",
        limit=8,
        expected_status="success",
        expected_hit_memory_ids=["mem_alice_01"],
        expected_min_hits=1,
        expected_max_hits=1,
        tags=["query"],
    ),
    # -- substring query -----------------------------------------------------
    RetrievalEvalCase(
        case_id="E15_substring_query",
        description="Query 'oat milk' matches the coffee preference record",
        contact_id="synth_alice",
        query="oat milk",
        limit=8,
        expected_status="success",
        expected_hit_memory_ids=["mem_alice_01"],
        expected_min_hits=1,
        expected_max_hits=1,
        tags=["query"],
    ),
    # -- second contact ------------------------------------------------------
    RetrievalEvalCase(
        case_id="E16_second_contact",
        description="synth_bob has 3 approved records retrievable independently",
        contact_id="synth_bob",
        query=None,
        limit=8,
        expected_status="success",
        expected_hit_memory_ids=["mem_bob_01", "mem_bob_02", "mem_bob_03"],
        expected_min_hits=3,
        expected_max_hits=3,
        expected_candidate_count=3,
        tags=["relevant_hits", "cross_contact"],
    ),
    # -- all exclusions combined ---------------------------------------------
    RetrievalEvalCase(
        case_id="E17_all_exclusions_combined",
        description="Exactly 6 hits for synth_alice; all 6 excluded records absent",
        contact_id="synth_alice",
        query=None,
        limit=20,
        expected_status="success",
        expected_hit_memory_ids=None,
        expected_min_hits=6,
        expected_max_hits=6,
        forbidden_memory_ids=[
            "mem_alice_07",
            "mem_alice_08",
            "mem_alice_09",
            "mem_alice_10",
            "mem_alice_11",
            "mem_alice_12",
        ],
        tags=["exclusion", "boundary"],
    ),
    # -- query with multiple potential matches -------------------------------
    RetrievalEvalCase(
        case_id="E18_query_multi_match",
        description="Query 'milk' matches two records (oat milk, milk chocolate); returned in importance-desc order",
        contact_id="synth_alice",
        query="milk",
        limit=8,
        expected_status="success",
        expected_hit_memory_ids=["mem_alice_01", "mem_alice_06"],
        expected_min_hits=2,
        expected_max_hits=2,
        tags=["relevant_hits", "query"],
    ),
    # -- limit smaller than query matches ------------------------------------
    RetrievalEvalCase(
        case_id="E19_limit_cuts_query_matches",
        description="Query 'milk' with limit=1 returns only the highest-importance match",
        contact_id="synth_alice",
        query="milk",
        limit=1,
        expected_status="success",
        expected_hit_memory_ids=["mem_alice_01"],
        expected_min_hits=1,
        expected_max_hits=1,
        tags=["query", "limit"],
    ),
]


# ---------------------------------------------------------------------------
# 5. Reusable fixture
# ---------------------------------------------------------------------------


@pytest.fixture()
def eval_store_dir(tmp_path: Path) -> Path:
    """Write the synthetic eval store to a temp dir and return the dir path."""
    store = build_synthetic_eval_store()
    store_file = tmp_path / "memory_fact_store.json"
    store_file.write_text(store.model_dump_json(), encoding="utf-8")
    return tmp_path


@pytest.fixture()
def eval_retriever(eval_store_dir: Path) -> LocalApprovedStoreRetriever:
    """A ``LocalApprovedStoreRetriever`` backed by the synthetic eval store."""
    return LocalApprovedStoreRetriever(eval_store_dir)


# ---------------------------------------------------------------------------
# 6. Parametrised eval-case tests
# ---------------------------------------------------------------------------


class TestRetrievalEvalSet:
    """Run all eval cases against ``LocalApprovedStoreRetriever``."""

    @pytest.mark.parametrize(
        "case",
        EVAL_CASES,
        ids=lambda c: c.case_id,
    )
    def test_eval_case(
        self,
        eval_retriever: LocalApprovedStoreRetriever,
        case: RetrievalEvalCase,
    ) -> None:
        run_eval_case(eval_retriever, case)


# ---------------------------------------------------------------------------
# 7. Contract boundary tests (hit-level properties)
# ---------------------------------------------------------------------------


class TestEvalContractBoundaries:
    """Verify hit-level contract properties using the eval store."""

    def test_source_provenance(self, eval_retriever: LocalApprovedStoreRetriever) -> None:
        result = eval_retriever.retrieve(contact_id="synth_alice")
        for hit in result.hits:
            assert hit.source == "approved_store", (
                f"Expected source='approved_store', got {hit.source!r}"
            )

    def test_scores_bounded(self, eval_retriever: LocalApprovedStoreRetriever) -> None:
        result = eval_retriever.retrieve(contact_id="synth_alice")
        for hit in result.hits:
            assert 0.0 <= hit.score <= 1.0, (
                f"Score {hit.score} out of [0.0, 1.0] for {hit.memory_id}"
            )

    def test_evidence_refs_non_empty(self, eval_retriever: LocalApprovedStoreRetriever) -> None:
        result = eval_retriever.retrieve(contact_id="synth_alice")
        for hit in result.hits:
            assert hit.evidence_refs, (
                f"Empty evidence_refs for {hit.memory_id}"
            )

    def test_memory_types_valid(self, eval_retriever: LocalApprovedStoreRetriever) -> None:
        valid = {mt.value for mt in MemoryType}
        result = eval_retriever.retrieve(contact_id="synth_alice")
        for hit in result.hits:
            assert hit.memory_type.value in valid, (
                f"Invalid memory_type {hit.memory_type!r} for {hit.memory_id}"
            )

    def test_hit_json_round_trip(self, eval_retriever: LocalApprovedStoreRetriever) -> None:
        result = eval_retriever.retrieve(contact_id="synth_alice")
        assert result.hits
        for hit in result.hits:
            raw = hit.model_dump_json()
            restored = MemoryHit.model_validate_json(raw)
            assert restored.memory_id == hit.memory_id
            assert restored.fact == hit.fact
            assert restored.score == hit.score
            assert restored.source == hit.source

    def test_result_json_round_trip(self, eval_retriever: LocalApprovedStoreRetriever) -> None:
        result = eval_retriever.retrieve(contact_id="synth_alice")
        raw = result.model_dump_json()
        restored = MemoryRetrieverResult.model_validate_json(raw)
        assert restored.status == "success"
        assert len(restored.hits) == len(result.hits)

    def test_no_mutation_of_store(self, eval_store_dir: Path) -> None:
        store_file = eval_store_dir / "memory_fact_store.json"
        before = store_file.read_text(encoding="utf-8")
        retriever = LocalApprovedStoreRetriever(eval_store_dir)
        retriever.retrieve(contact_id="synth_alice")
        after = store_file.read_text(encoding="utf-8")
        assert before == after


# ---------------------------------------------------------------------------
# 8. Coverage audit — verify all required eval dimensions are present
# ---------------------------------------------------------------------------


class TestEvalCoverageAudit:
    """Meta-tests ensuring the eval set covers required dimensions."""

    REQUIRED_TAGS = {"relevant_hits", "exclusion", "query", "ordering", "boundary"}

    def test_all_required_tags_present(self) -> None:
        all_tags: set[str] = set()
        for case in EVAL_CASES:
            all_tags.update(case.tags)
        missing = self.REQUIRED_TAGS - all_tags
        assert not missing, f"Eval set missing required tag coverage: {missing}"

    def test_exclusion_covers_all_non_runtime_states(self) -> None:
        exclusion_cases = [c for c in EVAL_CASES if "exclusion" in c.tags]
        all_forbidden: set[str] = set()
        for case in exclusion_cases:
            all_forbidden.update(case.forbidden_memory_ids)
        expected_excluded = {
            "mem_alice_07",
            "mem_alice_08",
            "mem_alice_09",
            "mem_alice_10",
            "mem_alice_11",
            "mem_alice_12",
        }
        missing = expected_excluded - all_forbidden
        assert not missing, (
            f"Exclusion cases do not cover all non-runtime-ready records: {missing}"
        )

    def test_cross_contact_coverage(self) -> None:
        contacts_in_cases = {c.contact_id for c in EVAL_CASES}
        assert "synth_alice" in contacts_in_cases
        assert "synth_bob" in contacts_in_cases
        assert "synth_unknown" in contacts_in_cases

    def test_eval_cases_deterministic(self) -> None:
        """Verify that building the store twice produces identical records."""
        s1 = build_synthetic_eval_store()
        s2 = build_synthetic_eval_store()
        assert len(s1.records) == len(s2.records)
        for r1, r2 in zip(s1.records, s2.records):
            assert r1.memory_fact.memory_id == r2.memory_fact.memory_id
            assert r1.memory_fact.claim == r2.memory_fact.claim
            assert r1.memory_fact.importance == r2.memory_fact.importance

    def test_at_least_one_ordering_case(self) -> None:
        ordering_cases = [c for c in EVAL_CASES if "ordering" in c.tags]
        assert len(ordering_cases) >= 1
        for case in ordering_cases:
            assert case.expected_hit_memory_ids is not None, (
                f"Ordering case {case.case_id} must specify expected_hit_memory_ids"
            )

    def test_store_contains_expected_record_count(self) -> None:
        store = build_synthetic_eval_store()
        assert len(store.records) == 15  # 6 approved + 6 excluded + 3 bob


# ---------------------------------------------------------------------------
# 9. Reuse demonstration — how a future retriever would use the same cases
# ---------------------------------------------------------------------------


class TestEvalReuseDemonstration:
    """Demonstrates that the eval runner works with any MemoryRetriever.

    This test shows the pattern that a future retriever implementation
    (e.g., T203 external adapter) would follow to reuse the same eval cases.
    The wrapper here is trivial (delegates to LocalApprovedStoreRetriever),
    but the key point is that ``run_eval_case`` only uses the
    ``MemoryRetriever`` protocol surface.
    """

    def test_eval_runner_uses_only_protocol(self, eval_store_dir: Path) -> None:
        """run_eval_case works when the retriever is typed as MemoryRetriever."""
        concrete = LocalApprovedStoreRetriever(eval_store_dir)
        # Verify protocol conformance
        assert isinstance(concrete, MemoryRetriever)
        # Pass as protocol type
        retriever: MemoryRetriever = concrete
        case = RetrievalEvalCase(
            case_id="reuse_demo",
            description="Demonstrates that run_eval_case works through the protocol interface",
            contact_id="synth_alice",
            query="coffee",
            limit=8,
            expected_status="success",
            expected_hit_memory_ids=["mem_alice_01"],
            expected_min_hits=1,
            expected_max_hits=1,
            tags=["relevant_hits"],
        )
        result = run_eval_case(retriever, case)
        assert result.status == "success"
        assert len(result.hits) == 1
        assert result.hits[0].memory_id == "mem_alice_01"
