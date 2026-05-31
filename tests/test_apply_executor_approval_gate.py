"""T403 apply executor approval gate tests.

The gate is deterministic and non-executing. It does not apply decisions,
mutate stores, call providers, generate media, or enable outbound behavior.
"""

from __future__ import annotations

import importlib

import pytest

from practical_chat_agent.services.apply_executor_risk import (
    ApplyExecutorApprovalGate as RiskApprovalGate,
)
from practical_chat_agent.services.apply_executor_risk import (
    ApplyExecutorRiskAssessment,
    ApplyExecutorRiskFactor,
    ApplyExecutorRollbackRequirement,
)
from practical_chat_agent.services.manual_apply_eligibility_gate import (
    ManualApplyEligibilityDecision,
)


def _module():
    return importlib.import_module(
        "practical_chat_agent.services.apply_executor_approval_gate"
    )


def _risk_assessment(
    *,
    severity: str = "medium",
    gate_satisfied: bool = True,
    rollback_covered: bool = True,
) -> ApplyExecutorRiskAssessment:
    return ApplyExecutorRiskAssessment(
        preview_id="mapprev_approval",
        decision_id="rqdec_approval",
        candidate_kind="persona_growth_patch",
        candidate_id="pgpatch_approval",
        safe_summary="[SYNTHETIC] Assess future executor approval.",
        risk_factors=[
            ApplyExecutorRiskFactor(
                risk_code="persona_drift",
                severity=severity,
                safe_summary="[SYNTHETIC] Persona drift risk is bounded.",
            )
        ],
        approval_gates=[
            RiskApprovalGate(
                gate_code="final_human_confirmation",
                label="Final human confirmation",
                safe_summary="[SYNTHETIC] Human confirmation is present.",
                satisfied=gate_satisfied,
            )
        ],
        rollback_requirements=[
            ApplyExecutorRollbackRequirement(
                requirement_code="previous_persona_version_available",
                safe_summary="[SYNTHETIC] Previous persona version is available.",
                covered=rollback_covered,
            )
        ],
        audit_requirements=[],
    )


def _manual_eligibility(
    *,
    eligibility_outcome: str = "eligible",
    preview_id: str = "mapprev_approval",
    decision_id: str = "rqdec_approval",
    candidate_kind: str = "persona_growth_patch",
    candidate_id: str = "pgpatch_approval",
) -> ManualApplyEligibilityDecision:
    return ManualApplyEligibilityDecision(
        preview_id=preview_id,
        bundle_id="rwbundle_approval",
        decision_id=decision_id,
        candidate_kind=candidate_kind,
        candidate_id=candidate_id,
        preview_outcome="future_manual_apply_eligible",
        eligibility_outcome=eligibility_outcome,
        safe_summary="[SYNTHETIC] Manual eligibility is available.",
        required_gate_codes=["human_approval"],
        satisfied_gate_codes=["human_approval"] if eligibility_outcome == "eligible" else [],
        missing_gate_codes=[] if eligibility_outcome == "eligible" else ["human_approval"],
        stale_reasons=["manual_preview_stale"] if eligibility_outcome == "stale" else [],
        issue_codes=[] if eligibility_outcome == "eligible" else ["manual_apply_issue"],
        blocking_issue_codes=[] if eligibility_outcome == "eligible" else ["manual_apply_blocked"],
        effect_count=1,
    )


def test_ready_assessment_with_required_controls_produces_review_only_ready_decision() -> None:
    decision = _module().ApplyExecutorApprovalGate().evaluate(
        _risk_assessment(),
        manual_eligibility=_manual_eligibility(),
        required_approval_gate_codes=["final_human_confirmation"],
    )

    assert decision.schema_version == "apply_executor_approval_decision_v1"
    assert decision.final_outcome == "ready_for_separately_scoped_executor_design"
    assert decision.risk_recommendation == "ready_for_separately_scoped_executor_design"
    assert decision.manual_eligibility_outcome == "eligible"
    assert decision.required_approval_gate_codes == ["final_human_confirmation"]
    assert decision.satisfied_approval_gate_codes == ["final_human_confirmation"]
    assert decision.missing_approval_gate_codes == []
    assert decision.blocking_issue_codes == []
    assert decision.review_required is True
    assert decision.risk_assessment_only is True
    assert decision.executor_ready is False
    assert decision.applies_changes is False
    assert decision.writes_memory_store is False
    assert decision.writes_persona_version is False
    assert decision.runtime_ready is False


def test_blocked_risk_assessment_remains_blocked() -> None:
    decision = _module().ApplyExecutorApprovalGate().evaluate(
        _risk_assessment(severity="critical"),
        manual_eligibility=_manual_eligibility(),
        required_approval_gate_codes=["final_human_confirmation"],
    )

    assert decision.final_outcome == "blocked"
    assert "critical_risk:persona_drift" in decision.blocking_issue_codes
    assert decision.executor_ready is False


def test_high_risk_with_controls_still_needs_review() -> None:
    decision = _module().ApplyExecutorApprovalGate().evaluate(
        _risk_assessment(severity="high"),
        manual_eligibility=_manual_eligibility(),
        required_approval_gate_codes=["final_human_confirmation"],
    )

    assert decision.final_outcome == "needs_review"
    assert decision.blocking_issue_codes == []
    assert decision.executor_ready is False


def test_unsatisfied_required_gate_blocks_decision() -> None:
    decision = _module().ApplyExecutorApprovalGate().evaluate(
        _risk_assessment(gate_satisfied=False),
        manual_eligibility=_manual_eligibility(),
        required_approval_gate_codes=["final_human_confirmation", "second_reviewer"],
    )

    assert decision.final_outcome == "blocked"
    assert "approval_gate_unsatisfied:final_human_confirmation" in decision.blocking_issue_codes
    assert "missing_approval_gate:second_reviewer" in decision.blocking_issue_codes


def test_stale_or_mismatched_manual_eligibility_blocks_decision() -> None:
    gate = _module().ApplyExecutorApprovalGate()

    stale = gate.evaluate(
        _risk_assessment(),
        manual_eligibility=_manual_eligibility(eligibility_outcome="stale"),
        required_approval_gate_codes=["final_human_confirmation"],
    )
    mismatch = gate.evaluate(
        _risk_assessment(),
        manual_eligibility=_manual_eligibility(candidate_id="pgpatch_other"),
        required_approval_gate_codes=["final_human_confirmation"],
    )

    assert stale.final_outcome == "blocked"
    assert "manual_apply_eligibility_stale" in stale.blocking_issue_codes
    assert "manual_preview_stale" in stale.stale_reasons
    assert mismatch.final_outcome == "blocked"
    assert "manual_candidate_id_mismatch" in mismatch.stale_reasons
    assert "manual_apply_eligibility_context_mismatch" in mismatch.blocking_issue_codes


def test_serialized_approval_decision_contains_no_forbidden_fields() -> None:
    serialized = (
        _module()
        .ApplyExecutorApprovalGate()
        .evaluate(
            _risk_assessment(),
            manual_eligibility=_manual_eligibility(),
            required_approval_gate_codes=["final_human_confirmation"],
        )
        .model_dump_json()
        .lower()
    )

    for forbidden in (
        "raw_text",
        "raw_transcript",
        "chat_history",
        "private_messages",
        "provider_credentials",
        "platform_recipient",
        "send_queue",
        "schedule",
        "webhook",
        "token",
        "microphone",
        "camera",
        "audio_bytes",
        "image_bytes",
        "video_bytes",
        "queue_item_id",
        "apply_decision",
        "mutate_store",
        "write_persona_version",
        "generate_audio",
        "generate_image",
        "generate_video",
    ):
        assert forbidden not in serialized


def test_approval_gate_exposes_no_runtime_or_apply_methods() -> None:
    module = _module()

    for target in (module.ApplyExecutorApprovalDecision, module.ApplyExecutorApprovalGate()):
        for method_name in (
            "apply",
            "apply_decision",
            "mutate_store",
            "mutate_persona",
            "write_persona_version",
            "delete_memory",
            "call_provider",
            "generate_reply",
            "send",
            "schedule",
            "deliver",
            "generate_audio",
            "generate_image",
            "generate_video",
        ):
            assert not hasattr(target, method_name)


def test_approval_decision_rejects_executing_flags() -> None:
    module = _module()

    with pytest.raises(ValueError):
        module.ApplyExecutorApprovalDecision(
            assessment_id="aeassess_mutating",
            preview_id="mapprev_mutating",
            decision_id="rqdec_mutating",
            candidate_kind="persona_growth_patch",
            candidate_id="pgpatch_mutating",
            risk_recommendation="ready_for_separately_scoped_executor_design",
            manual_eligibility_outcome="not_supplied",
            safe_summary="[SYNTHETIC] Mutating flags are rejected.",
            final_outcome="blocked",
            applies_changes=True,
        )
