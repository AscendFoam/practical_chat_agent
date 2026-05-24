"""Tests for the MemoryRetriever interface and MemoryHit contract (T200).

Covers:
- MemoryHit model validation
- MemoryRetrieverResult model validation
- MemoryRetriever protocol conformance
- LocalMemoryRetriever adapter behaviour
- convert_retrieval_result conversion fidelity
"""

from __future__ import annotations

from datetime import datetime, timezone

import pytest

from practical_chat_agent.core.enums import ChatIntent, MemoryType, MemoryScope
from practical_chat_agent.core.models import (
    AgentProfile,
    InboundEvent,
    MemoryFact,
    MemoryHit,
    MemoryRetrievalResult,
    MemoryRetrieverResult,
)
from practical_chat_agent.core.enums import ChannelType, Direction, ContentType, SourceType, Platform, PersonaType
from practical_chat_agent.services.memory_retrieval import (
    LocalMemoryRetriever,
    MemoryRetriever,
    MemoryRetrievalService,
    convert_retrieval_result,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _make_memory(
    *,
    memory_id: str = "mem_test",
    fact: str = "test fact",
    memory_type: MemoryType = MemoryType.FACT,
    salience: float = 0.5,
    confidence: float = 0.5,
    evidence_refs: list[str] | None = None,
) -> MemoryFact:
    return MemoryFact(
        memory_id=memory_id,
        agent_id="agent_1",
        user_id="user_1",
        memory_type=memory_type,
        scope=MemoryScope.LONG_TERM,
        salience=salience,
        confidence=confidence,
        fact=fact,
        evidence_refs=evidence_refs or [],
    )


def _make_event(*, text: str = "hello") -> InboundEvent:
    return InboundEvent(
        source_type=SourceType.CHAT_MESSAGE,
        platform=Platform.TELEGRAM,
        channel_id="ch_1",
        channel_type=ChannelType.DM,
        account_id="acc_1",
        actor_id="user_1",
        actor_name="TestUser",
        direction=Direction.INBOUND,
        content_type=ContentType.TEXT,
        text=text,
    )


def _make_agent() -> AgentProfile:
    return AgentProfile(
        agent_id="agent_1",
        display_name="TestAgent",
    )


# ---------------------------------------------------------------------------
# MemoryHit tests
# ---------------------------------------------------------------------------


class TestMemoryHit:
    def test_valid_minimal(self) -> None:
        hit = MemoryHit(memory_id="mem_1", fact="likes coffee", source="local")
        assert hit.memory_id == "mem_1"
        assert hit.fact == "likes coffee"
        assert hit.source == "local"
        assert hit.hit_id.startswith("mhit_")
        assert hit.memory_type == MemoryType.FACT
        assert hit.score == 0.0
        assert hit.evidence_refs == []

    def test_hit_id_auto_generated(self) -> None:
        hit = MemoryHit(memory_id="mem_1", fact="f", source="s")
        assert hit.hit_id
        assert isinstance(hit.hit_id, str)

    def test_hit_id_explicit(self) -> None:
        hit = MemoryHit(hit_id="custom_id", memory_id="mem_1", fact="f", source="s")
        assert hit.hit_id == "custom_id"

    def test_score_bounds_valid(self) -> None:
        MemoryHit(memory_id="m", fact="f", source="s", score=0.0)
        MemoryHit(memory_id="m", fact="f", source="s", score=1.0)
        MemoryHit(memory_id="m", fact="f", source="s", score=0.5)

    def test_score_bounds_invalid(self) -> None:
        with pytest.raises(Exception):
            MemoryHit(memory_id="m", fact="f", source="s", score=-0.1)
        with pytest.raises(Exception):
            MemoryHit(memory_id="m", fact="f", source="s", score=1.1)

    def test_memory_id_required(self) -> None:
        with pytest.raises(Exception):
            MemoryHit(fact="f", source="s")  # type: ignore[call-arg]

    def test_fact_required(self) -> None:
        with pytest.raises(Exception):
            MemoryHit(memory_id="m", source="s")  # type: ignore[call-arg]

    def test_source_required(self) -> None:
        with pytest.raises(Exception):
            MemoryHit(memory_id="m", fact="f")  # type: ignore[call-arg]

    def test_empty_memory_id_rejected(self) -> None:
        with pytest.raises(Exception):
            MemoryHit(memory_id="", fact="f", source="s")

    def test_empty_fact_rejected(self) -> None:
        with pytest.raises(Exception):
            MemoryHit(memory_id="m", fact="", source="s")

    def test_empty_source_rejected(self) -> None:
        with pytest.raises(Exception):
            MemoryHit(memory_id="m", fact="f", source="")

    def test_evidence_refs_preserved(self) -> None:
        hit = MemoryHit(
            memory_id="m", fact="f", source="s",
            evidence_refs=["evt_1", "evt_2"],
        )
        assert hit.evidence_refs == ["evt_1", "evt_2"]

    def test_memory_type_set(self) -> None:
        hit = MemoryHit(
            memory_id="m", fact="f", source="s",
            memory_type=MemoryType.RELATIONSHIP,
        )
        assert hit.memory_type == MemoryType.RELATIONSHIP

    def test_json_round_trip(self) -> None:
        hit = MemoryHit(
            memory_id="mem_1",
            fact="likes matcha",
            memory_type=MemoryType.PREFERENCE,
            score=0.85,
            evidence_refs=["evt_a"],
            source="approved_store",
        )
        raw = hit.model_dump_json()
        restored = MemoryHit.model_validate_json(raw)
        assert restored.memory_id == hit.memory_id
        assert restored.fact == hit.fact
        assert restored.score == hit.score
        assert restored.source == hit.source


# ---------------------------------------------------------------------------
# MemoryRetrieverResult tests
# ---------------------------------------------------------------------------


class TestMemoryRetrieverResult:
    def test_success_default(self) -> None:
        result = MemoryRetrieverResult()
        assert result.status == "success"
        assert result.contact_id is None
        assert result.hits == []
        assert result.candidate_count == 0
        assert result.notes == []

    def test_success_with_hits(self) -> None:
        hits = [
            MemoryHit(memory_id="m1", fact="f1", source="s1"),
            MemoryHit(memory_id="m2", fact="f2", source="s2"),
        ]
        result = MemoryRetrieverResult(
            status="success",
            contact_id="contact_1",
            hits=hits,
            candidate_count=10,
            notes=["note1"],
        )
        assert result.status == "success"
        assert result.contact_id == "contact_1"
        assert len(result.hits) == 2
        assert result.candidate_count == 10

    def test_not_configured(self) -> None:
        result = MemoryRetrieverResult(
            status="not_configured",
            contact_id="c1",
            notes=["No context set."],
        )
        assert result.status == "not_configured"
        assert result.hits == []

    def test_error(self) -> None:
        result = MemoryRetrieverResult(
            status="error",
            contact_id="c1",
            notes=["Provider timeout."],
        )
        assert result.status == "error"

    def test_invalid_status_rejected(self) -> None:
        with pytest.raises(Exception):
            MemoryRetrieverResult(status="unknown_status")

    def test_json_round_trip(self) -> None:
        result = MemoryRetrieverResult(
            status="success",
            contact_id="contact_x",
            hits=[MemoryHit(memory_id="m1", fact="f1", source="s1")],
            candidate_count=5,
            notes=["ok"],
        )
        raw = result.model_dump_json()
        restored = MemoryRetrieverResult.model_validate_json(raw)
        assert restored.status == result.status
        assert restored.contact_id == result.contact_id
        assert len(restored.hits) == 1


# ---------------------------------------------------------------------------
# Protocol conformance tests
# ---------------------------------------------------------------------------


class TestMemoryRetrieverProtocol:
    def test_local_retriever_isinstance(self) -> None:
        service = MemoryRetrievalService()
        adapter = LocalMemoryRetriever(service)
        assert isinstance(adapter, MemoryRetriever)

    def test_protocol_is_runtime_checkable(self) -> None:
        assert isinstance(MemoryRetriever, type)


# ---------------------------------------------------------------------------
# LocalMemoryRetriever tests
# ---------------------------------------------------------------------------


class TestLocalMemoryRetriever:
    def test_retrieve_without_context_returns_not_configured(self) -> None:
        service = MemoryRetrievalService()
        adapter = LocalMemoryRetriever(service)
        result = adapter.retrieve(contact_id="user_1")
        assert result.status == "not_configured"
        assert result.contact_id == "user_1"
        assert result.hits == []
        assert len(result.notes) > 0

    def test_retrieve_with_context_returns_success(self) -> None:
        service = MemoryRetrievalService()
        agent = _make_agent()
        event = _make_event()
        memories = [
            _make_memory(memory_id="m1", fact="likes coffee", salience=0.9),
            _make_memory(memory_id="m2", fact="likes tea", salience=0.3),
        ]
        adapter = LocalMemoryRetriever(service).with_context(
            agent=agent,
            event=event,
            candidates=memories,
        )
        result = adapter.retrieve(contact_id="user_1")
        assert result.status == "success"
        assert result.contact_id == "user_1"
        assert len(result.hits) > 0

    def test_retrieve_hits_have_correct_source(self) -> None:
        service = MemoryRetrievalService()
        agent = _make_agent()
        event = _make_event()
        memories = [_make_memory(memory_id="m1", fact="likes coffee")]
        adapter = LocalMemoryRetriever(service).with_context(
            agent=agent,
            event=event,
            candidates=memories,
        )
        result = adapter.retrieve(contact_id="user_1")
        for hit in result.hits:
            assert hit.source == "local_memory_retrieval"

    def test_retrieve_respects_limit(self) -> None:
        service = MemoryRetrievalService()
        agent = _make_agent()
        event = _make_event()
        memories = [_make_memory(memory_id=f"m{i}", fact=f"fact {i}") for i in range(20)]
        adapter = LocalMemoryRetriever(service).with_context(
            agent=agent,
            event=event,
            candidates=memories,
        )
        result = adapter.retrieve(contact_id="user_1", limit=3)
        assert len(result.hits) <= 3

    def test_retrieve_preserves_evidence_refs(self) -> None:
        service = MemoryRetrievalService()
        agent = _make_agent()
        event = _make_event()
        memories = [
            _make_memory(
                memory_id="m1",
                fact="fact with evidence",
                evidence_refs=["evt_1", "evt_2"],
            ),
        ]
        adapter = LocalMemoryRetriever(service).with_context(
            agent=agent,
            event=event,
            candidates=memories,
        )
        result = adapter.retrieve(contact_id="user_1")
        if result.hits:
            assert result.hits[0].evidence_refs == ["evt_1", "evt_2"]

    def test_retrieve_score_derived_from_salience(self) -> None:
        service = MemoryRetrievalService()
        agent = _make_agent()
        event = _make_event()
        memories = [
            _make_memory(memory_id="m1", fact="high salience fact", salience=0.95),
        ]
        adapter = LocalMemoryRetriever(service).with_context(
            agent=agent,
            event=event,
            candidates=memories,
        )
        result = adapter.retrieve(contact_id="user_1")
        if result.hits:
            assert result.hits[0].score == 0.95

    def test_with_context_returns_new_instance(self) -> None:
        service = MemoryRetrievalService()
        adapter1 = LocalMemoryRetriever(service)
        agent = _make_agent()
        event = _make_event()
        adapter2 = adapter1.with_context(agent=agent, event=event, candidates=[])
        assert adapter1 is not adapter2
        # adapter1 still has no context
        r1 = adapter1.retrieve(contact_id="c1")
        assert r1.status == "not_configured"

    def test_candidate_count_preserved(self) -> None:
        service = MemoryRetrievalService()
        agent = _make_agent()
        event = _make_event()
        memories = [_make_memory(memory_id=f"m{i}", fact=f"f{i}") for i in range(5)]
        adapter = LocalMemoryRetriever(service).with_context(
            agent=agent,
            event=event,
            candidates=memories,
        )
        result = adapter.retrieve(contact_id="user_1")
        assert result.candidate_count > 0

    def test_notes_carry_through(self) -> None:
        service = MemoryRetrievalService()
        agent = _make_agent()
        event = _make_event()
        memories = [_make_memory(memory_id="m1", fact="f")]
        adapter = LocalMemoryRetriever(service).with_context(
            agent=agent,
            event=event,
            candidates=memories,
        )
        result = adapter.retrieve(contact_id="user_1")
        assert len(result.notes) > 0


# ---------------------------------------------------------------------------
# convert_retrieval_result tests
# ---------------------------------------------------------------------------


class TestConvertRetrievalResult:
    def test_converts_empty_result(self) -> None:
        service_result = MemoryRetrievalResult(
            user_id="user_1",
            intent=ChatIntent.GENERAL,
            candidate_count=0,
            selected_hits=[],
            retrieval_notes=["no candidates"],
        )
        result = convert_retrieval_result(service_result, contact_id="contact_1")
        assert result.status == "success"
        assert result.contact_id == "contact_1"
        assert result.hits == []
        assert result.candidate_count == 0
        assert "no candidates" in result.notes

    def test_converts_selected_hits_to_memory_hits(self) -> None:
        memories = [
            _make_memory(
                memory_id="m1",
                fact="likes matcha",
                memory_type=MemoryType.PREFERENCE,
                salience=0.8,
                evidence_refs=["evt_1"],
            ),
            _make_memory(
                memory_id="m2",
                fact="works at startup",
                memory_type=MemoryType.FACT,
                salience=0.5,
            ),
        ]
        service_result = MemoryRetrievalResult(
            user_id="user_1",
            selected_hits=memories,
            candidate_count=10,
        )
        result = convert_retrieval_result(service_result, contact_id="c1")
        assert len(result.hits) == 2
        assert result.hits[0].memory_id == "m1"
        assert result.hits[0].fact == "likes matcha"
        assert result.hits[0].memory_type == MemoryType.PREFERENCE
        assert result.hits[0].score == 0.8
        assert result.hits[0].source == "local_memory_retrieval"
        assert result.hits[0].evidence_refs == ["evt_1"]
        assert result.hits[1].memory_id == "m2"
        assert result.candidate_count == 10

    def test_limit_applied(self) -> None:
        memories = [_make_memory(memory_id=f"m{i}", fact=f"f{i}") for i in range(10)]
        service_result = MemoryRetrievalResult(
            user_id="user_1",
            selected_hits=memories,
            candidate_count=10,
        )
        result = convert_retrieval_result(service_result, contact_id="c1", limit=3)
        assert len(result.hits) == 3

    def test_notes_preserved(self) -> None:
        service_result = MemoryRetrievalResult(
            user_id="u1",
            retrieval_notes=["detected intent: greeting", "scanned 5 candidates"],
        )
        result = convert_retrieval_result(service_result, contact_id="c1")
        assert "detected intent: greeting" in result.notes
        assert "scanned 5 candidates" in result.notes

    def test_hit_ids_are_unique(self) -> None:
        memories = [_make_memory(memory_id=f"m{i}", fact=f"f{i}") for i in range(5)]
        service_result = MemoryRetrievalResult(
            user_id="u1",
            selected_hits=memories,
        )
        result = convert_retrieval_result(service_result, contact_id="c1")
        hit_ids = [h.hit_id for h in result.hits]
        assert len(hit_ids) == len(set(hit_ids))


# ---------------------------------------------------------------------------
# Contract boundary tests
# ---------------------------------------------------------------------------


class TestContractBoundaries:
    def test_memory_hit_has_no_raw_transcript_field(self) -> None:
        """MemoryHit must not carry raw transcript content."""
        hit = MemoryHit(memory_id="m", fact="safe summary", source="s")
        assert not hasattr(hit, "raw_text")
        assert not hasattr(hit, "transcript")
        assert not hasattr(hit, "chat_history")

    def test_memory_hit_has_no_embedding_field(self) -> None:
        """MemoryHit must not carry embedding vectors."""
        hit = MemoryHit(memory_id="m", fact="f", source="s")
        assert not hasattr(hit, "embedding")
        assert not hasattr(hit, "vector")

    def test_memory_hit_has_no_write_capability(self) -> None:
        """MemoryHit is a read-only data contract, no mutation methods."""
        hit = MemoryHit(memory_id="m", fact="f", source="s")
        assert not hasattr(hit, "save")
        assert not hasattr(hit, "write")
        assert not hasattr(hit, "update_memory")

    def test_retriever_result_status_values(self) -> None:
        """Only the three defined statuses are valid."""
        for status in ("success", "not_configured", "error"):
            result = MemoryRetrieverResult(status=status)
            assert result.status == status
