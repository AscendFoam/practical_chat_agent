"""T203: Optional Mem0 adapter spike tests.

These tests verify the adapter boundary without requiring the ``mem0`` package
or network access.  The "working path" tests inject a mock client via the
``_client`` parameter, which is the documented test-injection point for this
spike.

Covers:

- ``not_configured`` degradation when unconfigured / package absent.
- Protocol conformance (``isinstance`` check).
- Successful retrieval with a mocked client (search and get_all paths).
- Error handling (client raises exceptions).
- Contract boundary preservation (source, score bounds, no raw fields).
- T202 eval case shape reuse demonstration.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from unittest.mock import MagicMock

import pytest

from practical_chat_agent.core.enums import MemoryType
from practical_chat_agent.core.models import MemoryHit, MemoryRetrieverResult
from practical_chat_agent.services.memory_retrieval import MemoryRetriever
from practical_chat_agent.services.optional_mem0_adapter import (
    Mem0AdapterRetriever,
    _infer_memory_type,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_mock_client(
    *,
    search_result: list[dict[str, Any]] | None = None,
    get_all_result: list[dict[str, Any]] | None = None,
) -> MagicMock:
    client = MagicMock()
    client.search.return_value = search_result or []
    client.get_all.return_value = get_all_result or []
    return client


# Minimal inline eval-case type for reuse demonstration.
# Avoids cross-test-module import fragility while reusing the same shape.


@dataclass(frozen=True)
class _SpikeEvalCase:
    case_id: str
    description: str
    contact_id: str
    query: str | None
    limit: int
    expected_status: str
    expected_min_hits: int
    expected_max_hits: int
    forbidden_memory_ids: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)


def _run_spike_eval(
    retriever: MemoryRetriever,
    case: _SpikeEvalCase,
) -> MemoryRetrieverResult:
    """Lightweight eval runner mirroring T202 ``run_eval_case``."""
    result = retriever.retrieve(
        contact_id=case.contact_id,
        query=case.query,
        limit=case.limit,
    )
    assert result.status == case.expected_status, (
        f"[{case.case_id}] status: expected {case.expected_status!r}, "
        f"got {result.status!r}"
    )
    assert case.expected_min_hits <= len(result.hits) <= case.expected_max_hits, (
        f"[{case.case_id}] hit count {len(result.hits)} "
        f"not in [{case.expected_min_hits}, {case.expected_max_hits}]"
    )
    if case.forbidden_memory_ids:
        actual_ids = {h.memory_id for h in result.hits}
        violations = actual_ids & set(case.forbidden_memory_ids)
        assert not violations, (
            f"[{case.case_id}] forbidden ids in hits: {violations}"
        )
    return result


# ---------------------------------------------------------------------------
# 1. not_configured degradation
# ---------------------------------------------------------------------------


class TestMem0AdapterNotConfigured:
    def test_no_api_key_returns_not_configured(self) -> None:
        adapter = Mem0AdapterRetriever()
        result = adapter.retrieve(contact_id="user_1")
        assert result.status == "not_configured"
        assert result.contact_id == "user_1"
        assert result.hits == []

    def test_explicit_none_api_key(self) -> None:
        adapter = Mem0AdapterRetriever(api_key=None)
        result = adapter.retrieve(contact_id="user_1")
        assert result.status == "not_configured"

    def test_empty_api_key(self) -> None:
        adapter = Mem0AdapterRetriever(api_key="")
        result = adapter.retrieve(contact_id="user_1")
        assert result.status == "not_configured"

    def test_whitespace_api_key(self) -> None:
        adapter = Mem0AdapterRetriever(api_key="   ")
        result = adapter.retrieve(contact_id="user_1")
        assert result.status == "not_configured"

    def test_not_configured_carries_reason(self) -> None:
        adapter = Mem0AdapterRetriever()
        result = adapter.retrieve(contact_id="user_1")
        assert len(result.notes) > 0
        assert any("API key" in note for note in result.notes)

    def test_not_configured_multiple_calls(self) -> None:
        adapter = Mem0AdapterRetriever()
        for _ in range(3):
            result = adapter.retrieve(contact_id="user_1")
            assert result.status == "not_configured"


# ---------------------------------------------------------------------------
# 2. Protocol conformance
# ---------------------------------------------------------------------------


class TestMem0AdapterProtocolConformance:
    def test_isinstance_without_client(self) -> None:
        adapter = Mem0AdapterRetriever()
        assert isinstance(adapter, MemoryRetriever)

    def test_isinstance_with_mock_client(self) -> None:
        adapter = Mem0AdapterRetriever(_client=MagicMock())
        assert isinstance(adapter, MemoryRetriever)


# ---------------------------------------------------------------------------
# 3. Successful retrieval with mocked client
# ---------------------------------------------------------------------------


class TestMem0AdapterSearchWithQuery:
    def test_search_returns_hits(self) -> None:
        client = _make_mock_client(
            search_result=[
                {"id": "mem_001", "memory": "Alice likes coffee", "score": 0.95},
                {"id": "mem_002", "memory": "Alice works as a designer", "score": 0.80},
            ],
        )
        adapter = Mem0AdapterRetriever(_client=client)
        result = adapter.retrieve(contact_id="alice", query="coffee", limit=5)
        assert result.status == "success"
        assert len(result.hits) == 2
        assert result.hits[0].memory_id == "mem_001"
        assert result.hits[0].fact == "Alice likes coffee"
        client.search.assert_called_once_with(
            query="coffee", user_id="alice", limit=5,
        )

    def test_search_empty_results(self) -> None:
        client = _make_mock_client(search_result=[])
        adapter = Mem0AdapterRetriever(_client=client)
        result = adapter.retrieve(contact_id="alice", query="nothing")
        assert result.status == "success"
        assert result.hits == []
        assert result.candidate_count == 0


class TestMem0AdapterGetAll:
    def test_get_all_returns_hits(self) -> None:
        client = _make_mock_client(
            get_all_result=[
                {"id": "mem_001", "memory": "Alice likes coffee"},
                {"id": "mem_002", "memory": "Alice works as a designer"},
            ],
        )
        adapter = Mem0AdapterRetriever(_client=client)
        result = adapter.retrieve(contact_id="alice", limit=5)
        assert result.status == "success"
        assert len(result.hits) == 2
        client.get_all.assert_called_once_with(user_id="alice")

    def test_get_all_empty(self) -> None:
        client = _make_mock_client(get_all_result=[])
        adapter = Mem0AdapterRetriever(_client=client)
        result = adapter.retrieve(contact_id="alice")
        assert result.status == "success"
        assert result.hits == []

    def test_get_all_default_score(self) -> None:
        client = _make_mock_client(
            get_all_result=[
                {"id": "mem_001", "memory": "Some fact without score"},
            ],
        )
        adapter = Mem0AdapterRetriever(_client=client)
        result = adapter.retrieve(contact_id="alice")
        assert result.hits[0].score == 0.5

    def test_candidate_count_total_from_get_all(self) -> None:
        client = _make_mock_client(
            get_all_result=[
                {"id": f"mem_{i:03d}", "memory": f"Fact {i}"}
                for i in range(7)
            ],
        )
        adapter = Mem0AdapterRetriever(_client=client)
        result = adapter.retrieve(contact_id="alice", limit=3)
        assert result.candidate_count == 7
        assert len(result.hits) == 3


class TestMem0AdapterLimit:
    def test_limit_enforced_on_search(self) -> None:
        client = _make_mock_client(
            search_result=[
                {"id": f"mem_{i:03d}", "memory": f"Fact {i}", "score": 0.9}
                for i in range(10)
            ],
        )
        adapter = Mem0AdapterRetriever(_client=client)
        result = adapter.retrieve(contact_id="alice", query="fact", limit=3)
        assert len(result.hits) == 3

    def test_limit_enforced_on_get_all(self) -> None:
        client = _make_mock_client(
            get_all_result=[
                {"id": f"mem_{i:03d}", "memory": f"Fact {i}"}
                for i in range(10)
            ],
        )
        adapter = Mem0AdapterRetriever(_client=client)
        result = adapter.retrieve(contact_id="alice", limit=4)
        assert len(result.hits) == 4


class TestMem0AdapterErrorHandling:
    def test_search_exception_returns_error(self) -> None:
        client = MagicMock()
        client.search.side_effect = Exception("Network timeout")
        adapter = Mem0AdapterRetriever(_client=client)
        result = adapter.retrieve(contact_id="alice", query="test")
        assert result.status == "error"
        assert result.contact_id == "alice"
        assert any("Network timeout" in note for note in result.notes)

    def test_get_all_exception_returns_error(self) -> None:
        client = MagicMock()
        client.get_all.side_effect = RuntimeError("Service unavailable")
        adapter = Mem0AdapterRetriever(_client=client)
        result = adapter.retrieve(contact_id="alice")
        assert result.status == "error"
        assert any("Service unavailable" in note for note in result.notes)


class TestMem0AdapterFieldMapping:
    def test_contact_id_propagated(self) -> None:
        client = _make_mock_client(get_all_result=[])
        adapter = Mem0AdapterRetriever(_client=client)
        result = adapter.retrieve(contact_id="bob_123")
        assert result.contact_id == "bob_123"

    def test_score_from_mem0_search(self) -> None:
        client = _make_mock_client(
            search_result=[
                {"id": "mem_001", "memory": "Fact", "score": 0.92},
            ],
        )
        adapter = Mem0AdapterRetriever(_client=client)
        result = adapter.retrieve(contact_id="alice", query="fact")
        assert result.hits[0].score == 0.92

    def test_score_clamped_above_1(self) -> None:
        client = _make_mock_client(
            search_result=[
                {"id": "mem_001", "memory": "Fact", "score": 1.5},
            ],
        )
        adapter = Mem0AdapterRetriever(_client=client)
        result = adapter.retrieve(contact_id="alice", query="fact")
        assert result.hits[0].score == 1.0

    def test_score_clamped_below_0(self) -> None:
        client = _make_mock_client(
            search_result=[
                {"id": "mem_001", "memory": "Fact", "score": -0.3},
            ],
        )
        adapter = Mem0AdapterRetriever(_client=client)
        result = adapter.retrieve(contact_id="alice", query="fact")
        assert result.hits[0].score == 0.0

    def test_score_invalid_falls_back(self) -> None:
        client = _make_mock_client(
            search_result=[
                {"id": "mem_001", "memory": "Fact", "score": "not_a_number"},
            ],
        )
        adapter = Mem0AdapterRetriever(_client=client)
        result = adapter.retrieve(contact_id="alice", query="fact")
        assert result.hits[0].score == 0.5

    def test_evidence_refs_populated(self) -> None:
        client = _make_mock_client(
            search_result=[
                {"id": "mem_abc", "memory": "Some fact"},
            ],
        )
        adapter = Mem0AdapterRetriever(_client=client)
        result = adapter.retrieve(contact_id="alice", query="fact")
        assert result.hits[0].evidence_refs == ["mem0:mem_abc"]

    def test_items_without_id_skipped(self) -> None:
        client = _make_mock_client(
            search_result=[
                {"id": "", "memory": "No ID"},
                {"id": "mem_001", "memory": "Valid fact"},
                {"memory": "Missing ID entirely"},
            ],
        )
        adapter = Mem0AdapterRetriever(_client=client)
        result = adapter.retrieve(contact_id="alice", query="fact")
        assert len(result.hits) == 1
        assert result.hits[0].memory_id == "mem_001"

    def test_items_without_memory_skipped(self) -> None:
        client = _make_mock_client(
            search_result=[
                {"id": "mem_001", "memory": ""},
                {"id": "mem_002", "memory": "Valid fact"},
            ],
        )
        adapter = Mem0AdapterRetriever(_client=client)
        result = adapter.retrieve(contact_id="alice", query="fact")
        assert len(result.hits) == 1
        assert result.hits[0].memory_id == "mem_002"

    def test_non_dict_items_skipped(self) -> None:
        client = _make_mock_client(
            search_result=[
                "not a dict",
                42,
                {"id": "mem_001", "memory": "Valid fact"},
            ],
        )
        adapter = Mem0AdapterRetriever(_client=client)
        result = adapter.retrieve(contact_id="alice", query="fact")
        assert len(result.hits) == 1

    def test_notes_include_query_info(self) -> None:
        client = _make_mock_client(
            search_result=[
                {"id": "mem_001", "memory": "Coffee fact", "score": 0.9},
            ],
        )
        adapter = Mem0AdapterRetriever(_client=client)
        result = adapter.retrieve(contact_id="alice", query="coffee")
        assert any("coffee" in note for note in result.notes)

    def test_notes_include_hit_count(self) -> None:
        client = _make_mock_client(
            get_all_result=[
                {"id": "mem_001", "memory": "Fact 1"},
                {"id": "mem_002", "memory": "Fact 2"},
            ],
        )
        adapter = Mem0AdapterRetriever(_client=client)
        result = adapter.retrieve(contact_id="alice")
        assert any("2 hits" in note for note in result.notes)


# ---------------------------------------------------------------------------
# 4. Memory type inference
# ---------------------------------------------------------------------------


class TestMemoryTypeInference:
    def test_preference_keywords(self) -> None:
        assert _infer_memory_type("Alice likes coffee") == MemoryType.PREFERENCE
        assert _infer_memory_type("Bob loves hiking") == MemoryType.PREFERENCE
        assert _infer_memory_type("prefers tea over coffee") == MemoryType.PREFERENCE

    def test_relationship_keywords(self) -> None:
        assert _infer_memory_type("Alice is a friend from college") == MemoryType.RELATIONSHIP
        assert _infer_memory_type("met at a coding bootcamp") == MemoryType.RELATIONSHIP

    def test_reflection_keywords(self) -> None:
        assert _infer_memory_type("feels stressed about deadlines") == MemoryType.REFLECTION
        assert _infer_memory_type("worries about the future") == MemoryType.REFLECTION

    def test_default_to_fact(self) -> None:
        assert _infer_memory_type("works as a software engineer") == MemoryType.FACT
        assert _infer_memory_type("went to the store") == MemoryType.FACT

    def test_combined_types_in_retrieval(self) -> None:
        client = _make_mock_client(
            get_all_result=[
                {"id": "m1", "memory": "Alice likes dark chocolate"},
                {"id": "m2", "memory": "Alice is a friend from college"},
                {"id": "m3", "memory": "Alice feels stressed about deadlines"},
                {"id": "m4", "memory": "Alice works as a UX designer"},
            ],
        )
        adapter = Mem0AdapterRetriever(_client=client)
        result = adapter.retrieve(contact_id="alice")
        types = {h.memory_type for h in result.hits}
        assert MemoryType.PREFERENCE in types
        assert MemoryType.RELATIONSHIP in types
        assert MemoryType.REFLECTION in types
        assert MemoryType.FACT in types


# ---------------------------------------------------------------------------
# 5. Contract boundary preservation
# ---------------------------------------------------------------------------


class TestMem0AdapterContractBoundaries:
    def test_source_is_external_adapter(self) -> None:
        client = _make_mock_client(
            get_all_result=[{"id": "m1", "memory": "Some fact"}],
        )
        adapter = Mem0AdapterRetriever(_client=client)
        result = adapter.retrieve(contact_id="alice")
        for hit in result.hits:
            assert hit.source == "external_adapter"

    def test_scores_bounded(self) -> None:
        client = _make_mock_client(
            get_all_result=[
                {"id": "m1", "memory": "Fact 1", "score": 0.95},
                {"id": "m2", "memory": "Fact 2"},
            ],
        )
        adapter = Mem0AdapterRetriever(_client=client)
        result = adapter.retrieve(contact_id="alice")
        for hit in result.hits:
            assert 0.0 <= hit.score <= 1.0

    def test_hit_has_no_raw_transcript(self) -> None:
        client = _make_mock_client(
            get_all_result=[{"id": "m1", "memory": "Safe summary"}],
        )
        adapter = Mem0AdapterRetriever(_client=client)
        result = adapter.retrieve(contact_id="alice")
        for hit in result.hits:
            assert not hasattr(hit, "raw_text")
            assert not hasattr(hit, "transcript")
            assert not hasattr(hit, "chat_history")

    def test_hit_has_no_embedding(self) -> None:
        client = _make_mock_client(
            get_all_result=[{"id": "m1", "memory": "Safe summary"}],
        )
        adapter = Mem0AdapterRetriever(_client=client)
        result = adapter.retrieve(contact_id="alice")
        for hit in result.hits:
            assert not hasattr(hit, "embedding")
            assert not hasattr(hit, "vector")

    def test_hit_has_no_write_capability(self) -> None:
        client = _make_mock_client(
            get_all_result=[{"id": "m1", "memory": "Safe summary"}],
        )
        adapter = Mem0AdapterRetriever(_client=client)
        result = adapter.retrieve(contact_id="alice")
        for hit in result.hits:
            assert not hasattr(hit, "save")
            assert not hasattr(hit, "write")
            assert not hasattr(hit, "update_memory")

    def test_json_round_trip_result(self) -> None:
        client = _make_mock_client(
            search_result=[
                {"id": "mem_001", "memory": "Test fact", "score": 0.8},
            ],
        )
        adapter = Mem0AdapterRetriever(_client=client)
        result = adapter.retrieve(contact_id="alice", query="test")
        raw = result.model_dump_json()
        restored = MemoryRetrieverResult.model_validate_json(raw)
        assert restored.status == "success"
        assert len(restored.hits) == 1
        assert restored.hits[0].source == "external_adapter"

    def test_adapter_does_not_mutate_client(self) -> None:
        client = _make_mock_client(
            get_all_result=[{"id": "m1", "memory": "Fact"}],
        )
        adapter = Mem0AdapterRetriever(_client=client)
        adapter.retrieve(contact_id="alice")
        client.add.assert_not_called()
        client.delete.assert_not_called()
        client.update.assert_not_called()


# ---------------------------------------------------------------------------
# 6. T202 eval case shape reuse demonstration
# ---------------------------------------------------------------------------


class TestMem0AdapterEvalReuse:
    """Demonstrates that the adapter works with the T202 eval case runner shape."""

    def test_success_case_via_eval_runner(self) -> None:
        client = _make_mock_client(
            search_result=[
                {
                    "id": "mem_alice_01",
                    "memory": "Alice prefers morning coffee with oat milk",
                    "score": 0.9,
                },
            ],
        )
        adapter = Mem0AdapterRetriever(_client=client)
        case = _SpikeEvalCase(
            case_id="mem0_reuse_success",
            description="Mock-backed adapter passes a success eval case",
            contact_id="synth_alice",
            query="coffee",
            limit=8,
            expected_status="success",
            expected_min_hits=1,
            expected_max_hits=1,
            tags=["relevant_hits"],
        )
        result = _run_spike_eval(adapter, case)
        assert result.status == "success"
        assert result.hits[0].memory_id == "mem_alice_01"

    def test_not_configured_case_via_eval_runner(self) -> None:
        adapter = Mem0AdapterRetriever()
        case = _SpikeEvalCase(
            case_id="mem0_reuse_not_configured",
            description="Unconfigured adapter reports not_configured",
            contact_id="any",
            query=None,
            limit=8,
            expected_status="not_configured",
            expected_min_hits=0,
            expected_max_hits=0,
        )
        result = _run_spike_eval(adapter, case)
        assert result.status == "not_configured"

    def test_forbidden_ids_checked(self) -> None:
        client = _make_mock_client(
            get_all_result=[
                {"id": "mem_good", "memory": "Good fact"},
                {"id": "mem_bad", "memory": "Bad fact"},
            ],
        )
        adapter = Mem0AdapterRetriever(_client=client)
        case = _SpikeEvalCase(
            case_id="mem0_forbidden_ids",
            description="Forbidden ids are detected in hits",
            contact_id="alice",
            query=None,
            limit=8,
            expected_status="success",
            expected_min_hits=0,
            expected_max_hits=10,
            forbidden_memory_ids=["mem_bad"],
        )
        with pytest.raises(AssertionError, match="forbidden"):
            _run_spike_eval(adapter, case)

    def test_empty_query_uses_get_all(self) -> None:
        client = _make_mock_client(
            get_all_result=[
                {"id": "mem_001", "memory": "Fact one"},
                {"id": "mem_002", "memory": "Fact two"},
            ],
        )
        adapter = Mem0AdapterRetriever(_client=client)
        case = _SpikeEvalCase(
            case_id="mem0_get_all_path",
            description="No query uses get_all, not search",
            contact_id="alice",
            query=None,
            limit=8,
            expected_status="success",
            expected_min_hits=2,
            expected_max_hits=2,
        )
        result = _run_spike_eval(adapter, case)
        client.get_all.assert_called_once()
        client.search.assert_not_called()
