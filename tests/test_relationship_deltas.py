"""Tests for relationship delta candidate generation (T192)."""
from __future__ import annotations

from practical_chat_agent.core.models import (
    RelationshipDeltaCandidate,
    RelationshipSignal,
    RelationshipState,
)
from practical_chat_agent.services.feedback import RelationshipDeltaGenerator


def _make_signal(
    *,
    signal_id: str = "sig_test_001",
    contact_id: str = "contact_test",
    dimension_name: str = "boundary_risk",
    direction: str = "increase",
    strength: float = 0.7,
    evidence_refs: list[str] | None = None,
    provenance: str = "feedback_boundary",
) -> RelationshipSignal:
    return RelationshipSignal(
        signal_id=signal_id,
        contact_id=contact_id,
        dimension_name=dimension_name,  # type: ignore[arg-type]
        direction=direction,  # type: ignore[arg-type]
        strength=strength,
        evidence_refs=evidence_refs or ["fb_001"],
        provenance=provenance,
    )


def _make_state(
    *,
    state_id: str = "state_test_001",
    contact_id: str = "contact_test",
    boundary_risk: float = 0.3,
    intimacy_level: float = 0.5,
    initiative_allowance: float = 0.5,
) -> RelationshipState:
    return RelationshipState(
        state_id=state_id,
        contact_id=contact_id,
        familiarity=0.3,
        trust=0.3,
        warmth=0.3,
        reciprocity=0.3,
        conflict_level=0.3,
        boundary_risk=boundary_risk,
        initiative_allowance=initiative_allowance,
        intimacy_level=intimacy_level,
        uncertainty=0.5,
        evidence_refs=["state_evidence_001"],
    )


class TestRelationshipDeltaGenerator:
    def setup_method(self):
        self.generator = RelationshipDeltaGenerator()

    # -- clear signal-to-delta mapping --

    def test_boundary_violation_signal_produces_delta(self):
        signal = _make_signal(
            dimension_name="boundary_risk", direction="increase", strength=0.7,
        )
        state = _make_state(boundary_risk=0.3)
        deltas = self.generator.generate_from_signals(
            signals=[signal], current_state=state,
        )
        assert len(deltas) == 1
        delta = deltas[0]
        assert delta.contact_id == "contact_test"
        assert delta.source_state_id == "state_test_001"
        assert len(delta.dimension_changes) == 1
        dc = delta.dimension_changes[0]
        assert dc.dimension_name == "boundary_risk"
        assert dc.current_value == 0.3
        assert dc.proposed_value > 0.3
        assert dc.direction == "increase"
        assert dc.magnitude > 0.0
        assert abs(dc.magnitude - (dc.proposed_value - dc.current_value)) < 1e-6

    def test_too_intimate_signals_produce_multi_dimension_delta(self):
        sig1 = _make_signal(
            signal_id="sig_br",
            dimension_name="boundary_risk",
            direction="increase",
            strength=0.5,
        )
        sig2 = _make_signal(
            signal_id="sig_il",
            dimension_name="intimacy_level",
            direction="decrease",
            strength=0.4,
        )
        state = _make_state(boundary_risk=0.3, intimacy_level=0.6)
        deltas = self.generator.generate_from_signals(
            signals=[sig1, sig2], current_state=state,
        )
        assert len(deltas) == 1
        dims = {dc.dimension_name for dc in deltas[0].dimension_changes}
        assert "boundary_risk" in dims
        assert "intimacy_level" in dims

    def test_too_eager_signal_produces_initiative_delta(self):
        signal = _make_signal(
            dimension_name="initiative_allowance",
            direction="decrease",
            strength=0.5,
        )
        state = _make_state(initiative_allowance=0.6)
        deltas = self.generator.generate_from_signals(
            signals=[signal], current_state=state,
        )
        assert len(deltas) == 1
        dc = deltas[0].dimension_changes[0]
        assert dc.dimension_name == "initiative_allowance"
        assert dc.direction == "decrease"
        assert dc.proposed_value < 0.6

    # -- no-delta behavior --

    def test_empty_signals_no_delta(self):
        state = _make_state()
        deltas = self.generator.generate_from_signals(
            signals=[], current_state=state,
        )
        assert deltas == []

    def test_wrong_contact_no_delta(self):
        signal = _make_signal(contact_id="contact_other")
        state = _make_state(contact_id="contact_test")
        deltas = self.generator.generate_from_signals(
            signals=[signal], current_state=state,
        )
        assert deltas == []

    def test_unknown_direction_no_delta(self):
        signal = _make_signal(direction="unknown", strength=0.7)
        state = _make_state()
        deltas = self.generator.generate_from_signals(
            signals=[signal], current_state=state,
        )
        assert deltas == []

    def test_weak_signal_no_delta(self):
        signal = _make_signal(strength=0.1)
        state = _make_state()
        deltas = self.generator.generate_from_signals(
            signals=[signal], current_state=state,
        )
        assert deltas == []

    def test_contradictory_directions_no_delta(self):
        sig1 = _make_signal(
            signal_id="sig_up",
            dimension_name="boundary_risk",
            direction="increase",
            strength=0.7,
        )
        sig2 = _make_signal(
            signal_id="sig_down",
            dimension_name="boundary_risk",
            direction="decrease",
            strength=0.6,
        )
        state = _make_state(boundary_risk=0.3)
        deltas = self.generator.generate_from_signals(
            signals=[sig1, sig2], current_state=state,
        )
        assert deltas == []

    def test_stable_direction_no_delta(self):
        signal = _make_signal(direction="stable", strength=0.7)
        state = _make_state()
        deltas = self.generator.generate_from_signals(
            signals=[signal], current_state=state,
        )
        assert deltas == []

    # -- magnitude/direction consistency --

    def test_magnitude_equals_abs_diff(self):
        signal = _make_signal(strength=0.7)
        state = _make_state(boundary_risk=0.3)
        deltas = self.generator.generate_from_signals(
            signals=[signal], current_state=state,
        )
        dc = deltas[0].dimension_changes[0]
        assert abs(dc.magnitude - abs(dc.proposed_value - dc.current_value)) < 1e-6

    def test_decrease_direction_validated(self):
        signal = _make_signal(
            dimension_name="intimacy_level",
            direction="decrease",
            strength=0.5,
        )
        state = _make_state(intimacy_level=0.6)
        deltas = self.generator.generate_from_signals(
            signals=[signal], current_state=state,
        )
        dc = deltas[0].dimension_changes[0]
        assert dc.direction == "decrease"
        assert dc.proposed_value < dc.current_value

    def test_clamped_at_upper_boundary(self):
        signal = _make_signal(strength=0.9)
        state = _make_state(boundary_risk=0.95)
        deltas = self.generator.generate_from_signals(
            signals=[signal], current_state=state,
        )
        dc = deltas[0].dimension_changes[0]
        assert dc.proposed_value <= 1.0
        assert abs(dc.magnitude - abs(dc.proposed_value - dc.current_value)) < 1e-6

    def test_clamped_at_lower_boundary(self):
        signal = _make_signal(
            dimension_name="initiative_allowance",
            direction="decrease",
            strength=0.9,
        )
        state = _make_state(initiative_allowance=0.02)
        deltas = self.generator.generate_from_signals(
            signals=[signal], current_state=state,
        )
        dc = deltas[0].dimension_changes[0]
        assert dc.proposed_value >= 0.0
        assert abs(dc.magnitude - abs(dc.proposed_value - dc.current_value)) < 1e-6

    def test_no_delta_when_already_at_upper_boundary(self):
        signal = _make_signal(strength=0.7)
        state = _make_state(boundary_risk=1.0)
        deltas = self.generator.generate_from_signals(
            signals=[signal], current_state=state,
        )
        assert deltas == []

    def test_no_delta_when_already_at_lower_boundary(self):
        signal = _make_signal(
            dimension_name="initiative_allowance",
            direction="decrease",
            strength=0.7,
        )
        state = _make_state(initiative_allowance=0.0)
        deltas = self.generator.generate_from_signals(
            signals=[signal], current_state=state,
        )
        assert deltas == []

    # -- evidence refs and signal refs --

    def test_evidence_refs_preserved(self):
        signal = _make_signal(evidence_refs=["fb_001", "fb_002"])
        state = _make_state()
        deltas = self.generator.generate_from_signals(
            signals=[signal], current_state=state,
        )
        assert "fb_001" in deltas[0].evidence_refs
        assert "fb_002" in deltas[0].evidence_refs

    def test_signal_refs_preserved(self):
        signal = _make_signal(signal_id="sig_abc")
        state = _make_state()
        deltas = self.generator.generate_from_signals(
            signals=[signal], current_state=state,
        )
        assert "sig_abc" in deltas[0].signal_refs

    def test_evidence_refs_deduplicated(self):
        sig1 = _make_signal(
            signal_id="sig_1",
            evidence_refs=["fb_001", "fb_002"],
        )
        sig2 = _make_signal(
            signal_id="sig_2",
            dimension_name="intimacy_level",
            direction="decrease",
            evidence_refs=["fb_002", "fb_003"],
        )
        state = _make_state()
        deltas = self.generator.generate_from_signals(
            signals=[sig1, sig2], current_state=state,
        )
        refs = deltas[0].evidence_refs
        assert refs.count("fb_002") == 1

    def test_state_evidence_not_in_delta_evidence(self):
        signal = _make_signal(evidence_refs=["fb_signal_001"])
        state = _make_state()
        deltas = self.generator.generate_from_signals(
            signals=[signal], current_state=state,
        )
        assert "state_evidence_001" not in deltas[0].evidence_refs

    # -- no state mutation --

    def test_state_not_mutated(self):
        signal = _make_signal(strength=0.7)
        state = _make_state(boundary_risk=0.3)
        original_risk = state.boundary_risk
        self.generator.generate_from_signals(signals=[signal], current_state=state)
        assert state.boundary_risk == original_risk

    # -- delta candidate properties --

    def test_delta_status_is_candidate(self):
        signal = _make_signal()
        state = _make_state()
        deltas = self.generator.generate_from_signals(
            signals=[signal], current_state=state,
        )
        assert deltas[0].status == "candidate"
        assert not deltas[0].is_runtime_ready()

    def test_delta_rationale_nonempty(self):
        signal = _make_signal()
        state = _make_state()
        deltas = self.generator.generate_from_signals(
            signals=[signal], current_state=state,
        )
        assert len(deltas[0].delta_rationale) > 0

    def test_no_raw_text_in_delta(self):
        signal = _make_signal()
        state = _make_state()
        deltas = self.generator.generate_from_signals(
            signals=[signal], current_state=state,
        )
        delta = deltas[0]
        assert "sensitive" not in delta.delta_rationale.casefold()
        for dc in delta.dimension_changes:
            if dc.rationale:
                assert "sensitive" not in dc.rationale.casefold()

    # -- multi-signal aggregation --

    def test_multiple_signals_same_dimension_uses_max_strength(self):
        sig1 = _make_signal(signal_id="sig_weak", strength=0.4)
        sig2 = _make_signal(signal_id="sig_strong", strength=0.7)
        state = _make_state(boundary_risk=0.3)
        deltas = self.generator.generate_from_signals(
            signals=[sig1, sig2], current_state=state,
        )
        dc = deltas[0].dimension_changes[0]
        expected_magnitude = 0.7 * self.generator._MAGNITUDE_SCALE
        assert abs(dc.magnitude - expected_magnitude) < 1e-4

    def test_all_signal_refs_collected(self):
        sig1 = _make_signal(signal_id="sig_a")
        sig2 = _make_signal(
            signal_id="sig_b",
            dimension_name="intimacy_level",
            direction="decrease",
            strength=0.4,
        )
        state = _make_state()
        deltas = self.generator.generate_from_signals(
            signals=[sig1, sig2], current_state=state,
        )
        refs = deltas[0].signal_refs
        assert "sig_a" in refs
        assert "sig_b" in refs

    def test_signal_and_dimension_counts_in_rationale(self):
        sig1 = _make_signal(signal_id="sig_1")
        sig2 = _make_signal(
            signal_id="sig_2",
            dimension_name="intimacy_level",
            direction="decrease",
            strength=0.4,
        )
        state = _make_state()
        deltas = self.generator.generate_from_signals(
            signals=[sig1, sig2], current_state=state,
        )
        assert "2 signal(s)" in deltas[0].delta_rationale
        assert "2 dimension(s)" in deltas[0].delta_rationale
