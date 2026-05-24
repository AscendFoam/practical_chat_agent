"""Tests for the LocalApprovedStoreRetriever (T201).

Covers:
- MemoryRetriever protocol conformance
- Approved/runtime-ready record retrieval
- Exclusion of candidate/rejected/frozen/archived/not-human-reviewed records
- Contact-id filtering
- Simple query matching
- Limit enforcement
- Source provenance ("approved_store")
- Score derivation from importance
- Memory-type mapping
- Evidence-ref preservation
- Deterministic ordering
- Store-not-found / invalid-store / empty-store edge cases
- Contract boundary assertions (no raw fields in MemoryHit)
"""

from __future__ import annotations

from pathlib import Path

import pytest

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
# Helpers
# ---------------------------------------------------------------------------


def _make_review_metadata(
    *,
    reviewed_by_human: bool = True,
    last_decision: str = "approved",
    evidence_validation_status: str = "passed",
) -> DistilledArtifactReviewMetadata:
    return DistilledArtifactReviewMetadata(
        review_state="reviewed" if reviewed_by_human else "pending_human_review",
        reviewed_by_human=reviewed_by_human,
        last_decision=last_decision,
        evidence_validation_status=evidence_validation_status,
    )


def _make_store_record(
    *,
    memory_id: str = "mem_test",
    subject_id: str = "contact_1",
    claim: str = "test claim",
    memory_type: str = "semantic",
    importance: float = 0.5,
    confidence: float = 0.5,
    status: str = "approved",
    evidence_refs: list[str] | None = None,
    review_metadata: DistilledArtifactReviewMetadata | None = None,
) -> MemoryFactStoreRecord:
    return MemoryFactStoreRecord(
        memory_fact=MemoryFactCandidate(
            memory_id=memory_id,
            subject_id=subject_id,
            claim=claim,
            memory_type=memory_type,
            importance=importance,
            confidence=confidence,
            status=status,
            sensitivity="low",
            evidence_refs=evidence_refs or ["evt_1"],
        ),
        review_metadata=review_metadata or _make_review_metadata(),
    )


def _write_store(tmp_path: Path, records: list[MemoryFactStoreRecord]) -> Path:
    store = MemoryFactStoreFile(records=records)
    store_file = tmp_path / "memory_fact_store.json"
    store_file.write_text(store.model_dump_json(), encoding="utf-8")
    return store_file


# ---------------------------------------------------------------------------
# Protocol conformance
# ---------------------------------------------------------------------------


class TestProtocolConformance:
    def test_isinstance_memory_retriever(self, tmp_path: Path) -> None:
        retriever = LocalApprovedStoreRetriever(tmp_path / "store.json")
        assert isinstance(retriever, MemoryRetriever)

    def test_retrieve_method_signature(self, tmp_path: Path) -> None:
        retriever = LocalApprovedStoreRetriever(tmp_path / "store.json")
        result = retriever.retrieve(contact_id="c1")
        assert isinstance(result, MemoryRetrieverResult)


# ---------------------------------------------------------------------------
# Approved record retrieval
# ---------------------------------------------------------------------------


class TestApprovedRecordRetrieval:
    def test_returns_approved_runtime_ready_records(self, tmp_path: Path) -> None:
        records = [
            _make_store_record(memory_id="m1", claim="likes coffee"),
            _make_store_record(memory_id="m2", claim="works at startup"),
        ]
        store_file = _write_store(tmp_path, records)
        retriever = LocalApprovedStoreRetriever(store_file)
        result = retriever.retrieve(contact_id="contact_1")
        assert result.status == "success"
        assert len(result.hits) == 2
        assert result.candidate_count == 2

    def test_hit_fields_populated_correctly(self, tmp_path: Path) -> None:
        records = [
            _make_store_record(
                memory_id="m1",
                claim="likes matcha",
                memory_type="semantic",
                importance=0.85,
                confidence=0.9,
                evidence_refs=["evt_a", "evt_b"],
            ),
        ]
        store_file = _write_store(tmp_path, records)
        retriever = LocalApprovedStoreRetriever(store_file)
        result = retriever.retrieve(contact_id="contact_1")
        assert len(result.hits) == 1
        hit = result.hits[0]
        assert hit.memory_id == "m1"
        assert hit.fact == "likes matcha"
        assert hit.source == "approved_store"
        assert hit.score == 0.85
        assert hit.evidence_refs == ["evt_a", "evt_b"]

    def test_returns_success_with_empty_hits_when_no_match(self, tmp_path: Path) -> None:
        records = [
            _make_store_record(memory_id="m1", subject_id="other_contact"),
        ]
        store_file = _write_store(tmp_path, records)
        retriever = LocalApprovedStoreRetriever(store_file)
        result = retriever.retrieve(contact_id="contact_1")
        assert result.status == "success"
        assert result.hits == []
        assert result.candidate_count == 0

    def test_contact_id_populated(self, tmp_path: Path) -> None:
        records = [_make_store_record()]
        store_file = _write_store(tmp_path, records)
        retriever = LocalApprovedStoreRetriever(store_file)
        result = retriever.retrieve(contact_id="contact_1")
        assert result.contact_id == "contact_1"


# ---------------------------------------------------------------------------
# Excluded records
# ---------------------------------------------------------------------------


class TestExcludedRecords:
    def test_candidate_status_excluded(self, tmp_path: Path) -> None:
        records = [
            _make_store_record(
                memory_id="m1",
                status="candidate",
                review_metadata=_make_review_metadata(),
            ),
        ]
        store_file = _write_store(tmp_path, records)
        retriever = LocalApprovedStoreRetriever(store_file)
        result = retriever.retrieve(contact_id="contact_1")
        assert result.hits == []

    def test_rejected_status_excluded(self, tmp_path: Path) -> None:
        records = [
            _make_store_record(
                memory_id="m1",
                status="rejected",
                review_metadata=_make_review_metadata(last_decision="rejected"),
            ),
        ]
        store_file = _write_store(tmp_path, records)
        retriever = LocalApprovedStoreRetriever(store_file)
        result = retriever.retrieve(contact_id="contact_1")
        assert result.hits == []

    def test_frozen_status_excluded(self, tmp_path: Path) -> None:
        records = [
            _make_store_record(
                memory_id="m1",
                status="frozen",
                review_metadata=_make_review_metadata(last_decision="frozen"),
            ),
        ]
        store_file = _write_store(tmp_path, records)
        retriever = LocalApprovedStoreRetriever(store_file)
        result = retriever.retrieve(contact_id="contact_1")
        assert result.hits == []

    def test_archived_status_excluded(self, tmp_path: Path) -> None:
        records = [
            _make_store_record(
                memory_id="m1",
                status="archived",
                review_metadata=_make_review_metadata(last_decision="archived"),
            ),
        ]
        store_file = _write_store(tmp_path, records)
        retriever = LocalApprovedStoreRetriever(store_file)
        result = retriever.retrieve(contact_id="contact_1")
        assert result.hits == []

    def test_not_human_reviewed_excluded(self, tmp_path: Path) -> None:
        records = [
            _make_store_record(
                memory_id="m1",
                review_metadata=_make_review_metadata(reviewed_by_human=False),
            ),
        ]
        store_file = _write_store(tmp_path, records)
        retriever = LocalApprovedStoreRetriever(store_file)
        result = retriever.retrieve(contact_id="contact_1")
        assert result.hits == []

    def test_evidence_validation_not_passed_excluded(self, tmp_path: Path) -> None:
        records = [
            _make_store_record(
                memory_id="m1",
                review_metadata=_make_review_metadata(evidence_validation_status="not_run"),
            ),
        ]
        store_file = _write_store(tmp_path, records)
        retriever = LocalApprovedStoreRetriever(store_file)
        result = retriever.retrieve(contact_id="contact_1")
        assert result.hits == []

    def test_evidence_validation_failed_excluded(self, tmp_path: Path) -> None:
        records = [
            _make_store_record(
                memory_id="m1",
                review_metadata=_make_review_metadata(evidence_validation_status="failed"),
            ),
        ]
        store_file = _write_store(tmp_path, records)
        retriever = LocalApprovedStoreRetriever(store_file)
        result = retriever.retrieve(contact_id="contact_1")
        assert result.hits == []

    def test_wrong_contact_excluded(self, tmp_path: Path) -> None:
        records = [
            _make_store_record(memory_id="m1", subject_id="contact_other"),
        ]
        store_file = _write_store(tmp_path, records)
        retriever = LocalApprovedStoreRetriever(store_file)
        result = retriever.retrieve(contact_id="contact_1")
        assert result.hits == []

    def test_mixed_records_only_approved_returned(self, tmp_path: Path) -> None:
        records = [
            _make_store_record(memory_id="m1", claim="approved fact"),
            _make_store_record(
                memory_id="m2",
                claim="candidate fact",
                status="candidate",
                review_metadata=_make_review_metadata(),
            ),
            _make_store_record(
                memory_id="m3",
                claim="rejected fact",
                status="rejected",
                review_metadata=_make_review_metadata(last_decision="rejected"),
            ),
            _make_store_record(
                memory_id="m4",
                claim="frozen fact",
                status="frozen",
                review_metadata=_make_review_metadata(last_decision="frozen"),
            ),
        ]
        store_file = _write_store(tmp_path, records)
        retriever = LocalApprovedStoreRetriever(store_file)
        result = retriever.retrieve(contact_id="contact_1")
        assert len(result.hits) == 1
        assert result.hits[0].fact == "approved fact"

    def test_mixed_contacts_only_matching_returned(self, tmp_path: Path) -> None:
        records = [
            _make_store_record(memory_id="m1", subject_id="contact_1", claim="c1 fact"),
            _make_store_record(memory_id="m2", subject_id="contact_2", claim="c2 fact"),
        ]
        store_file = _write_store(tmp_path, records)
        retriever = LocalApprovedStoreRetriever(store_file)
        result = retriever.retrieve(contact_id="contact_1")
        assert len(result.hits) == 1
        assert result.hits[0].fact == "c1 fact"


# ---------------------------------------------------------------------------
# Query filtering
# ---------------------------------------------------------------------------


class TestQueryFiltering:
    def test_query_matches_claim(self, tmp_path: Path) -> None:
        records = [
            _make_store_record(memory_id="m1", claim="likes coffee"),
            _make_store_record(memory_id="m2", claim="works at startup"),
        ]
        store_file = _write_store(tmp_path, records)
        retriever = LocalApprovedStoreRetriever(store_file)
        result = retriever.retrieve(contact_id="contact_1", query="coffee")
        assert len(result.hits) == 1
        assert result.hits[0].fact == "likes coffee"

    def test_query_case_insensitive(self, tmp_path: Path) -> None:
        records = [
            _make_store_record(memory_id="m1", claim="Likes Coffee"),
        ]
        store_file = _write_store(tmp_path, records)
        retriever = LocalApprovedStoreRetriever(store_file)
        result = retriever.retrieve(contact_id="contact_1", query="coffee")
        assert len(result.hits) == 1

    def test_query_no_match_returns_empty(self, tmp_path: Path) -> None:
        records = [
            _make_store_record(memory_id="m1", claim="likes coffee"),
        ]
        store_file = _write_store(tmp_path, records)
        retriever = LocalApprovedStoreRetriever(store_file)
        result = retriever.retrieve(contact_id="contact_1", query="pizza")
        assert result.hits == []

    def test_query_none_returns_all(self, tmp_path: Path) -> None:
        records = [
            _make_store_record(memory_id="m1", claim="fact a"),
            _make_store_record(memory_id="m2", claim="fact b"),
        ]
        store_file = _write_store(tmp_path, records)
        retriever = LocalApprovedStoreRetriever(store_file)
        result = retriever.retrieve(contact_id="contact_1", query=None)
        assert len(result.hits) == 2

    def test_query_empty_string_returns_all(self, tmp_path: Path) -> None:
        records = [
            _make_store_record(memory_id="m1", claim="fact a"),
            _make_store_record(memory_id="m2", claim="fact b"),
        ]
        store_file = _write_store(tmp_path, records)
        retriever = LocalApprovedStoreRetriever(store_file)
        result = retriever.retrieve(contact_id="contact_1", query="")
        assert len(result.hits) == 2

    def test_query_whitespace_only_returns_all(self, tmp_path: Path) -> None:
        records = [
            _make_store_record(memory_id="m1", claim="fact a"),
        ]
        store_file = _write_store(tmp_path, records)
        retriever = LocalApprovedStoreRetriever(store_file)
        result = retriever.retrieve(contact_id="contact_1", query="   ")
        assert len(result.hits) == 1


# ---------------------------------------------------------------------------
# Limit enforcement
# ---------------------------------------------------------------------------


class TestLimitEnforcement:
    def test_limit_respected(self, tmp_path: Path) -> None:
        records = [
            _make_store_record(memory_id=f"m{i}", claim=f"fact {i}", importance=0.9 - i * 0.05)
            for i in range(10)
        ]
        store_file = _write_store(tmp_path, records)
        retriever = LocalApprovedStoreRetriever(store_file)
        result = retriever.retrieve(contact_id="contact_1", limit=3)
        assert len(result.hits) == 3
        assert result.candidate_count == 10

    def test_limit_zero_returns_no_hits(self, tmp_path: Path) -> None:
        records = [_make_store_record(memory_id="m1", claim="fact")]
        store_file = _write_store(tmp_path, records)
        retriever = LocalApprovedStoreRetriever(store_file)
        result = retriever.retrieve(contact_id="contact_1", limit=0)
        assert len(result.hits) == 0

    def test_limit_larger_than_records(self, tmp_path: Path) -> None:
        records = [
            _make_store_record(memory_id="m1", claim="fact"),
        ]
        store_file = _write_store(tmp_path, records)
        retriever = LocalApprovedStoreRetriever(store_file)
        result = retriever.retrieve(contact_id="contact_1", limit=100)
        assert len(result.hits) == 1

    def test_default_limit_is_8(self, tmp_path: Path) -> None:
        records = [
            _make_store_record(memory_id=f"m{i}", claim=f"fact {i}")
            for i in range(15)
        ]
        store_file = _write_store(tmp_path, records)
        retriever = LocalApprovedStoreRetriever(store_file)
        result = retriever.retrieve(contact_id="contact_1")
        assert len(result.hits) <= 8


# ---------------------------------------------------------------------------
# Source provenance
# ---------------------------------------------------------------------------


class TestSourceProvenance:
    def test_all_hits_have_approved_store_source(self, tmp_path: Path) -> None:
        records = [
            _make_store_record(memory_id=f"m{i}", claim=f"fact {i}")
            for i in range(5)
        ]
        store_file = _write_store(tmp_path, records)
        retriever = LocalApprovedStoreRetriever(store_file)
        result = retriever.retrieve(contact_id="contact_1")
        for hit in result.hits:
            assert hit.source == "approved_store"


# ---------------------------------------------------------------------------
# Score derivation
# ---------------------------------------------------------------------------


class TestScoreDerivation:
    def test_score_from_importance(self, tmp_path: Path) -> None:
        records = [
            _make_store_record(memory_id="m1", claim="high", importance=0.95),
            _make_store_record(memory_id="m2", claim="low", importance=0.1),
        ]
        store_file = _write_store(tmp_path, records)
        retriever = LocalApprovedStoreRetriever(store_file)
        result = retriever.retrieve(contact_id="contact_1")
        hit_by_fact = {h.fact: h for h in result.hits}
        assert hit_by_fact["high"].score == 0.95
        assert hit_by_fact["low"].score == 0.1

    def test_score_in_valid_range(self, tmp_path: Path) -> None:
        records = [
            _make_store_record(memory_id="m1", claim="f", importance=0.0),
            _make_store_record(memory_id="m2", claim="g", importance=1.0),
        ]
        store_file = _write_store(tmp_path, records)
        retriever = LocalApprovedStoreRetriever(store_file)
        result = retriever.retrieve(contact_id="contact_1")
        for hit in result.hits:
            assert 0.0 <= hit.score <= 1.0


# ---------------------------------------------------------------------------
# Memory type mapping
# ---------------------------------------------------------------------------


class TestMemoryTypeMapping:
    @pytest.mark.parametrize(
        ("distillation_type", "expected_runtime"),
        [
            ("semantic", "fact"),
            ("episodic", "fact"),
            ("relationship", "relationship"),
            ("procedural", "preference"),
            ("reflection", "reflection"),
        ],
    )
    def test_type_mapping(
        self, tmp_path: Path, distillation_type: str, expected_runtime: str
    ) -> None:
        records = [
            _make_store_record(
                memory_id="m1",
                claim="typed fact",
                memory_type=distillation_type,
            ),
        ]
        store_file = _write_store(tmp_path, records)
        retriever = LocalApprovedStoreRetriever(store_file)
        result = retriever.retrieve(contact_id="contact_1")
        assert len(result.hits) == 1
        assert result.hits[0].memory_type.value == expected_runtime


# ---------------------------------------------------------------------------
# Evidence ref preservation
# ---------------------------------------------------------------------------


class TestEvidenceRefPreservation:
    def test_evidence_refs_carried_through(self, tmp_path: Path) -> None:
        records = [
            _make_store_record(
                memory_id="m1",
                claim="fact with refs",
                evidence_refs=["evt_1", "evt_2", "evt_3"],
            ),
        ]
        store_file = _write_store(tmp_path, records)
        retriever = LocalApprovedStoreRetriever(store_file)
        result = retriever.retrieve(contact_id="contact_1")
        assert result.hits[0].evidence_refs == ["evt_1", "evt_2", "evt_3"]

    def test_empty_evidence_refs(self, tmp_path: Path) -> None:
        # MemoryFactCandidate requires min_length=1 for evidence_refs,
        # so we always have at least one ref.  But the hit should carry
        # whatever the record has.
        records = [
            _make_store_record(
                memory_id="m1",
                claim="fact with single ref",
                evidence_refs=["evt_single"],
            ),
        ]
        store_file = _write_store(tmp_path, records)
        retriever = LocalApprovedStoreRetriever(store_file)
        result = retriever.retrieve(contact_id="contact_1")
        assert result.hits[0].evidence_refs == ["evt_single"]


# ---------------------------------------------------------------------------
# Deterministic ordering
# ---------------------------------------------------------------------------


class TestDeterministicOrdering:
    def test_sorted_by_importance_desc(self, tmp_path: Path) -> None:
        records = [
            _make_store_record(memory_id="m1", claim="low", importance=0.2),
            _make_store_record(memory_id="m2", claim="high", importance=0.9),
            _make_store_record(memory_id="m3", claim="mid", importance=0.5),
        ]
        store_file = _write_store(tmp_path, records)
        retriever = LocalApprovedStoreRetriever(store_file)
        result = retriever.retrieve(contact_id="contact_1")
        assert [h.fact for h in result.hits] == ["high", "mid", "low"]

    def test_tiebreak_by_confidence_desc(self, tmp_path: Path) -> None:
        records = [
            _make_store_record(memory_id="m1", claim="lower_conf", importance=0.5, confidence=0.3),
            _make_store_record(memory_id="m2", claim="higher_conf", importance=0.5, confidence=0.8),
        ]
        store_file = _write_store(tmp_path, records)
        retriever = LocalApprovedStoreRetriever(store_file)
        result = retriever.retrieve(contact_id="contact_1")
        assert result.hits[0].fact == "higher_conf"
        assert result.hits[1].fact == "lower_conf"

    def test_tiebreak_by_memory_id_asc(self, tmp_path: Path) -> None:
        records = [
            _make_store_record(memory_id="m_b", claim="b", importance=0.5, confidence=0.5),
            _make_store_record(memory_id="m_a", claim="a", importance=0.5, confidence=0.5),
        ]
        store_file = _write_store(tmp_path, records)
        retriever = LocalApprovedStoreRetriever(store_file)
        result = retriever.retrieve(contact_id="contact_1")
        assert result.hits[0].memory_id == "m_a"
        assert result.hits[1].memory_id == "m_b"

    def test_ordering_is_deterministic_across_calls(self, tmp_path: Path) -> None:
        records = [
            _make_store_record(memory_id=f"m{i}", claim=f"fact {i}", importance=i / 10)
            for i in range(10)
        ]
        store_file = _write_store(tmp_path, records)
        retriever = LocalApprovedStoreRetriever(store_file)
        r1 = retriever.retrieve(contact_id="contact_1")
        r2 = retriever.retrieve(contact_id="contact_1")
        assert [h.memory_id for h in r1.hits] == [h.memory_id for h in r2.hits]


# ---------------------------------------------------------------------------
# Store path resolution
# ---------------------------------------------------------------------------


class TestStorePathResolution:
    def test_file_path_directly(self, tmp_path: Path) -> None:
        records = [_make_store_record(memory_id="m1")]
        store_file = _write_store(tmp_path, records)
        retriever = LocalApprovedStoreRetriever(store_file)
        result = retriever.retrieve(contact_id="contact_1")
        assert result.status == "success"
        assert len(result.hits) == 1

    def test_directory_path_resolves_store_file(self, tmp_path: Path) -> None:
        records = [_make_store_record(memory_id="m1")]
        _write_store(tmp_path, records)
        retriever = LocalApprovedStoreRetriever(tmp_path)
        result = retriever.retrieve(contact_id="contact_1")
        assert result.status == "success"
        assert len(result.hits) == 1


# ---------------------------------------------------------------------------
# Store not found / invalid / empty
# ---------------------------------------------------------------------------


class TestStoreEdgeCases:
    def test_nonexistent_path_returns_not_configured(self, tmp_path: Path) -> None:
        retriever = LocalApprovedStoreRetriever(tmp_path / "nonexistent.json")
        result = retriever.retrieve(contact_id="contact_1")
        assert result.status == "not_configured"
        assert result.hits == []
        assert result.contact_id == "contact_1"

    def test_nonexistent_directory_returns_not_configured(self, tmp_path: Path) -> None:
        retriever = LocalApprovedStoreRetriever(tmp_path / "missing_dir")
        result = retriever.retrieve(contact_id="contact_1")
        assert result.status == "not_configured"

    def test_empty_directory_returns_not_configured(self, tmp_path: Path) -> None:
        empty_dir = tmp_path / "empty"
        empty_dir.mkdir()
        retriever = LocalApprovedStoreRetriever(empty_dir)
        result = retriever.retrieve(contact_id="contact_1")
        assert result.status == "not_configured"

    def test_invalid_json_returns_error(self, tmp_path: Path) -> None:
        bad_file = tmp_path / "memory_fact_store.json"
        bad_file.write_text("not json", encoding="utf-8")
        retriever = LocalApprovedStoreRetriever(bad_file)
        result = retriever.retrieve(contact_id="contact_1")
        assert result.status == "error"
        assert result.hits == []

    def test_valid_json_extra_fields_returns_success_empty(self, tmp_path: Path) -> None:
        # Pydantic tolerates extra fields; the store is valid but has no records.
        bad_file = tmp_path / "memory_fact_store.json"
        bad_file.write_text('{"wrong": "shape"}', encoding="utf-8")
        retriever = LocalApprovedStoreRetriever(bad_file)
        result = retriever.retrieve(contact_id="contact_1")
        assert result.status == "success"
        assert result.hits == []

    def test_invalid_record_types_returns_error(self, tmp_path: Path) -> None:
        # A store file where records is not a list of valid records.
        bad_file = tmp_path / "memory_fact_store.json"
        bad_file.write_text('{"records": [{"invalid": true}]}', encoding="utf-8")
        retriever = LocalApprovedStoreRetriever(bad_file)
        result = retriever.retrieve(contact_id="contact_1")
        assert result.status == "error"

    def test_empty_store_returns_success_with_no_hits(self, tmp_path: Path) -> None:
        store_file = _write_store(tmp_path, [])
        retriever = LocalApprovedStoreRetriever(store_file)
        result = retriever.retrieve(contact_id="contact_1")
        assert result.status == "success"
        assert result.hits == []
        assert result.candidate_count == 0

    def test_directory_with_no_store_file(self, tmp_path: Path) -> None:
        data_dir = tmp_path / "data"
        data_dir.mkdir()
        (data_dir / "other.json").write_text("{}", encoding="utf-8")
        retriever = LocalApprovedStoreRetriever(data_dir)
        result = retriever.retrieve(contact_id="contact_1")
        assert result.status == "not_configured"


# ---------------------------------------------------------------------------
# Notes
# ---------------------------------------------------------------------------


class TestNotes:
    def test_notes_contain_load_summary(self, tmp_path: Path) -> None:
        records = [_make_store_record(memory_id="m1")]
        store_file = _write_store(tmp_path, records)
        retriever = LocalApprovedStoreRetriever(store_file)
        result = retriever.retrieve(contact_id="contact_1")
        assert any("loaded" in note for note in result.notes)
        assert any("eligible" in note for note in result.notes)
        assert any("returning" in note for note in result.notes)

    def test_notes_include_query_when_provided(self, tmp_path: Path) -> None:
        records = [_make_store_record(memory_id="m1", claim="coffee")]
        store_file = _write_store(tmp_path, records)
        retriever = LocalApprovedStoreRetriever(store_file)
        result = retriever.retrieve(contact_id="contact_1", query="coffee")
        assert any("query filter" in note for note in result.notes)

    def test_notes_no_query_when_none(self, tmp_path: Path) -> None:
        records = [_make_store_record(memory_id="m1")]
        store_file = _write_store(tmp_path, records)
        retriever = LocalApprovedStoreRetriever(store_file)
        result = retriever.retrieve(contact_id="contact_1", query=None)
        assert not any("query filter" in note for note in result.notes)


# ---------------------------------------------------------------------------
# Contract boundary assertions
# ---------------------------------------------------------------------------


class TestContractBoundaries:
    def test_hit_has_no_raw_transcript_field(self, tmp_path: Path) -> None:
        records = [_make_store_record(memory_id="m1", claim="safe summary")]
        store_file = _write_store(tmp_path, records)
        retriever = LocalApprovedStoreRetriever(store_file)
        result = retriever.retrieve(contact_id="contact_1")
        for hit in result.hits:
            assert not hasattr(hit, "raw_text")
            assert not hasattr(hit, "transcript")
            assert not hasattr(hit, "chat_history")

    def test_hit_has_no_embedding_field(self, tmp_path: Path) -> None:
        records = [_make_store_record(memory_id="m1")]
        store_file = _write_store(tmp_path, records)
        retriever = LocalApprovedStoreRetriever(store_file)
        result = retriever.retrieve(contact_id="contact_1")
        for hit in result.hits:
            assert not hasattr(hit, "embedding")
            assert not hasattr(hit, "vector")

    def test_hit_has_no_write_capability(self, tmp_path: Path) -> None:
        records = [_make_store_record(memory_id="m1")]
        store_file = _write_store(tmp_path, records)
        retriever = LocalApprovedStoreRetriever(store_file)
        result = retriever.retrieve(contact_id="contact_1")
        for hit in result.hits:
            assert not hasattr(hit, "save")
            assert not hasattr(hit, "write")
            assert not hasattr(hit, "update_memory")

    def test_hit_has_no_file_path(self, tmp_path: Path) -> None:
        records = [_make_store_record(memory_id="m1")]
        store_file = _write_store(tmp_path, records)
        retriever = LocalApprovedStoreRetriever(store_file)
        result = retriever.retrieve(contact_id="contact_1")
        for hit in result.hits:
            assert not hasattr(hit, "file_path")
            assert not hasattr(hit, "source_path")

    def test_hit_has_no_review_metadata(self, tmp_path: Path) -> None:
        records = [_make_store_record(memory_id="m1")]
        store_file = _write_store(tmp_path, records)
        retriever = LocalApprovedStoreRetriever(store_file)
        result = retriever.retrieve(contact_id="contact_1")
        for hit in result.hits:
            assert not hasattr(hit, "review_metadata")
            assert not hasattr(hit, "review_history")

    def test_no_mutation_of_store_file(self, tmp_path: Path) -> None:
        records = [_make_store_record(memory_id="m1")]
        store_file = _write_store(tmp_path, records)
        content_before = store_file.read_text(encoding="utf-8")
        retriever = LocalApprovedStoreRetriever(store_file)
        retriever.retrieve(contact_id="contact_1")
        content_after = store_file.read_text(encoding="utf-8")
        assert content_before == content_after


# ---------------------------------------------------------------------------
# JSON round-trip
# ---------------------------------------------------------------------------


class TestJsonRoundTrip:
    def test_hit_json_round_trip(self, tmp_path: Path) -> None:
        records = [
            _make_store_record(
                memory_id="m1",
                claim="likes matcha",
                memory_type="procedural",
                importance=0.88,
                evidence_refs=["evt_x", "evt_y"],
            ),
        ]
        store_file = _write_store(tmp_path, records)
        retriever = LocalApprovedStoreRetriever(store_file)
        result = retriever.retrieve(contact_id="contact_1")
        assert len(result.hits) == 1
        raw = result.hits[0].model_dump_json()
        restored = MemoryHit.model_validate_json(raw)
        assert restored.memory_id == "m1"
        assert restored.fact == "likes matcha"
        assert restored.score == 0.88
        assert restored.source == "approved_store"
        assert restored.evidence_refs == ["evt_x", "evt_y"]

    def test_result_json_round_trip(self, tmp_path: Path) -> None:
        records = [_make_store_record(memory_id="m1", claim="fact")]
        store_file = _write_store(tmp_path, records)
        retriever = LocalApprovedStoreRetriever(store_file)
        result = retriever.retrieve(contact_id="contact_1")
        raw = result.model_dump_json()
        restored = MemoryRetrieverResult.model_validate_json(raw)
        assert restored.status == "success"
        assert restored.contact_id == "contact_1"
        assert len(restored.hits) == 1


# ---------------------------------------------------------------------------
# Candidate count
# ---------------------------------------------------------------------------


class TestCandidateCount:
    def test_candidate_count_equals_eligible(self, tmp_path: Path) -> None:
        records = [
            _make_store_record(memory_id="m1", subject_id="contact_1"),
            _make_store_record(memory_id="m2", subject_id="contact_1"),
            _make_store_record(memory_id="m3", subject_id="contact_other"),
        ]
        store_file = _write_store(tmp_path, records)
        retriever = LocalApprovedStoreRetriever(store_file)
        result = retriever.retrieve(contact_id="contact_1")
        assert result.candidate_count == 2

    def test_candidate_count_after_query_filter(self, tmp_path: Path) -> None:
        records = [
            _make_store_record(memory_id="m1", claim="likes coffee"),
            _make_store_record(memory_id="m2", claim="likes tea"),
        ]
        store_file = _write_store(tmp_path, records)
        retriever = LocalApprovedStoreRetriever(store_file)
        result = retriever.retrieve(contact_id="contact_1", query="coffee")
        assert result.candidate_count == 1
