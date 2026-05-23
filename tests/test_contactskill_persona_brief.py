"""Committed synthetic validation tests for PartnerPersonaBrief (T171).

All fixtures are synthetic. No private data, no real contact names,
no real platform IDs, and no raw transcript text.
"""

import pytest
from pydantic import ValidationError

from practical_chat_agent.core.models import (
    CommunicationStyleSnapshot,
    ContactRelationshipType,
    PartnerPersonaBrief,
)


def _make_brief(
    *,
    contact_id: str = "contact_synthetic",
    relationship_type: ContactRelationshipType = "friend",
    relationship_state_summary: str = "Active friendship with moderate closeness.",
    communication_style_snapshot: CommunicationStyleSnapshot | None = None,
    preferred_topics: list[str] | None = None,
    emotional_pattern_labels: list[str] | None = None,
    evidence_refs: list[str] | None = None,
    source_skill_record_id: str = "skillstore_synthetic_001",
) -> PartnerPersonaBrief:
    return PartnerPersonaBrief(
        contact_id=contact_id,
        relationship_type=relationship_type,
        relationship_state_summary=relationship_state_summary,
        communication_style_snapshot=communication_style_snapshot
        or CommunicationStyleSnapshot(),
        preferred_topics=preferred_topics or [],
        emotional_pattern_labels=emotional_pattern_labels or [],
        evidence_refs=evidence_refs or [],
        source_skill_record_id=source_skill_record_id,
    )


class TestValidBriefConstruction:
    def test_minimal_valid_brief(self):
        brief = _make_brief()
        assert brief.contact_id == "contact_synthetic"
        assert brief.relationship_type == "friend"
        assert brief.relationship_state_summary == "Active friendship with moderate closeness."
        assert isinstance(brief.communication_style_snapshot, CommunicationStyleSnapshot)
        assert brief.preferred_topics == []
        assert brief.emotional_pattern_labels == []
        assert brief.evidence_refs == []
        assert brief.source_skill_record_id == "skillstore_synthetic_001"

    def test_full_brief(self):
        brief = PartnerPersonaBrief(
            contact_id="contact_lin",
            relationship_type="colleague",
            relationship_state_summary="Professional but warm; moderate trust.",
            communication_style_snapshot=CommunicationStyleSnapshot(
                message_length="short",
                tone="polite",
                response_latency="fast",
                directness="medium",
            ),
            preferred_topics=["project updates", "weekend plans"],
            emotional_pattern_labels=["generally positive", "occasionally reserved"],
            evidence_refs=["evt_a1", "evt_a2", "chk_b1"],
            source_skill_record_id="skillstore_abc123",
        )
        assert brief.contact_id == "contact_lin"
        assert brief.relationship_type == "colleague"
        assert brief.communication_style_snapshot.message_length == "short"
        assert brief.communication_style_snapshot.tone == "polite"
        assert len(brief.preferred_topics) == 2
        assert len(brief.evidence_refs) == 3

    def test_all_relationship_types(self):
        for rel_type in ("friend", "classmate", "colleague", "family", "unknown"):
            brief = _make_brief(relationship_type=rel_type)
            assert brief.relationship_type == rel_type


class TestRequiredTraceabilityFields:
    def test_contact_id_required(self):
        with pytest.raises(ValidationError):
            PartnerPersonaBrief(
                relationship_type="friend",
                relationship_state_summary="Summary.",
                source_skill_record_id="skillstore_001",
            )

    def test_contact_id_nonempty(self):
        with pytest.raises(ValidationError):
            _make_brief(contact_id="")

    def test_relationship_state_summary_required(self):
        with pytest.raises(ValidationError):
            PartnerPersonaBrief(
                contact_id="contact_001",
                relationship_type="friend",
                source_skill_record_id="skillstore_001",
            )

    def test_relationship_state_summary_nonempty(self):
        with pytest.raises(ValidationError):
            _make_brief(relationship_state_summary="")

    def test_source_skill_record_id_required(self):
        with pytest.raises(ValidationError):
            PartnerPersonaBrief(
                contact_id="contact_001",
                relationship_type="friend",
                relationship_state_summary="Summary.",
            )

    def test_source_skill_record_id_nonempty(self):
        with pytest.raises(ValidationError):
            _make_brief(source_skill_record_id="")

    def test_relationship_type_required(self):
        with pytest.raises(ValidationError):
            PartnerPersonaBrief(
                contact_id="contact_001",
                relationship_state_summary="Summary.",
                source_skill_record_id="skillstore_001",
            )


class TestSafeDefaultsAndOptionalFields:
    def test_communication_style_defaults_to_empty(self):
        brief = _make_brief()
        snap = brief.communication_style_snapshot
        assert snap.message_length is None
        assert snap.tone is None
        assert snap.response_latency is None
        assert snap.directness is None

    def test_preferred_topics_default_empty(self):
        assert _make_brief().preferred_topics == []

    def test_emotional_pattern_labels_default_empty(self):
        assert _make_brief().emotional_pattern_labels == []

    def test_evidence_refs_default_empty(self):
        assert _make_brief().evidence_refs == []

    def test_communication_style_partial(self):
        brief = _make_brief(
            communication_style_snapshot=CommunicationStyleSnapshot(
                tone="casual",
            ),
        )
        assert brief.communication_style_snapshot.tone == "casual"
        assert brief.communication_style_snapshot.message_length is None
        assert brief.communication_style_snapshot.directness is None


class TestCommunicationStyleSnapshotTyping:
    def test_structured_model_not_dict(self):
        brief = _make_brief()
        assert isinstance(brief.communication_style_snapshot, CommunicationStyleSnapshot)
        assert not isinstance(brief.communication_style_snapshot, dict)

    def test_snapshot_field_access(self):
        snap = CommunicationStyleSnapshot(
            message_length="long",
            tone="warm",
            response_latency="slow",
            directness="high",
        )
        assert snap.message_length == "long"
        assert snap.tone == "warm"
        assert snap.response_latency == "slow"
        assert snap.directness == "high"

    def test_snapshot_serialization_round_trip(self):
        snap = CommunicationStyleSnapshot(
            message_length="medium",
            tone="reserved",
        )
        data = snap.model_dump()
        restored = CommunicationStyleSnapshot.model_validate(data)
        assert restored.message_length == "medium"
        assert restored.tone == "reserved"
        assert restored.response_latency is None

    def test_snapshot_none_fields_excluded_in_serialization(self):
        snap = CommunicationStyleSnapshot()
        data = snap.model_dump(exclude_none=True)
        assert data == {}

    def test_brief_serialization_round_trip(self):
        brief = _make_brief(
            communication_style_snapshot=CommunicationStyleSnapshot(
                message_length="short",
                tone="casual",
            ),
            preferred_topics=["sports", "food"],
            evidence_refs=["evt_001"],
        )
        data = brief.model_dump()
        restored = PartnerPersonaBrief.model_validate(data)
        assert restored.contact_id == brief.contact_id
        assert restored.communication_style_snapshot.message_length == "short"
        assert restored.preferred_topics == ["sports", "food"]
        assert restored.evidence_refs == ["evt_001"]


class TestInvalidRelationshipType:
    def test_invalid_relationship_type_rejected(self):
        with pytest.raises(ValidationError):
            _make_brief(relationship_type="invalid_type")
