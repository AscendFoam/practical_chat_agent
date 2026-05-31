"""T402 apply executor risk record tests.

All records are risk-assessment-only and non-executing. These tests do not
apply decisions, mutate stores, call providers, generate media, or enable
outbound behavior.
"""

from __future__ import annotations

import importlib

import pytest


def _module():
    return importlib.import_module("practical_chat_agent.services.apply_executor_risk")


def _ready_assessment():
    module = _module()
    return module.ApplyExecutorRiskAssessment(
        preview_id="mapprev_ready",
        decision_id="rqdec_ready",
        candidate_kind="persona_growth_patch",
        candidate_id="pgpatch_ready",
        safe_summary="[SYNTHETIC] Assess future executor readiness.",
        risk_factors=[
            module.ApplyExecutorRiskFactor(
                risk_code="persona_drift",
                severity="medium",
                safe_summary="[SYNTHETIC] Persona drift risk is bounded.",
            )
        ],
        approval_gates=[
            module.ApplyExecutorApprovalGate(
                gate_code="final_human_confirmation",
                label="Final human confirmation",
                safe_summary="[SYNTHETIC] Final confirmation is present.",
                satisfied=True,
            )
        ],
        rollback_requirements=[
            module.ApplyExecutorRollbackRequirement(
                requirement_code="previous_persona_version_available",
                safe_summary="[SYNTHETIC] Previous persona version is available.",
                covered=True,
            )
        ],
        audit_requirements=[
            module.ApplyExecutorAuditRequirement(
                event_code="manual_apply_audit_record",
                safe_summary="[SYNTHETIC] Audit record fields are ready.",
                covered=True,
            )
        ],
    )


def test_ready_risk_assessment_is_non_executing_and_serializable() -> None:
    assessment = _ready_assessment()
    payload = assessment.model_dump(mode="json")

    assert payload["schema_version"] == "apply_executor_risk_assessment_v1"
    assert payload["final_recommendation"] == "ready_for_separately_scoped_executor_design"
    assert payload["blocking_issue_codes"] == []
    assert payload["risk_assessment_only"] is True
    assert payload["executor_ready"] is False
    assert payload["review_required"] is True
    assert payload["applies_changes"] is False
    assert payload["writes_memory_store"] is False
    assert payload["writes_persona_version"] is False
    assert payload["runtime_ready"] is False


def test_critical_risk_blocks_executor_readiness() -> None:
    module = _module()
    assessment = module.ApplyExecutorRiskAssessment(
        preview_id="mapprev_blocked",
        decision_id="rqdec_blocked",
        candidate_kind="memory_deletion_cascade",
        candidate_id="memdel_blocked",
        safe_summary="[SYNTHETIC] Assess deletion risk.",
        risk_factors=[
            module.ApplyExecutorRiskFactor(
                risk_code="irreversible_deletion",
                severity="critical",
                safe_summary="[SYNTHETIC] Deletion rollback is not proven.",
            )
        ],
        approval_gates=[],
        rollback_requirements=[],
        audit_requirements=[],
    )

    assert assessment.final_recommendation == "blocked"
    assert "critical_risk:irreversible_deletion" in assessment.blocking_issue_codes
    assert assessment.executor_ready is False


def test_missing_approval_or_rollback_blocks_assessment() -> None:
    module = _module()
    assessment = module.ApplyExecutorRiskAssessment(
        preview_id="mapprev_missing_gate",
        decision_id="rqdec_missing_gate",
        candidate_kind="persona_growth_patch",
        candidate_id="pgpatch_missing_gate",
        safe_summary="[SYNTHETIC] Assess missing approval.",
        risk_factors=[],
        approval_gates=[
            module.ApplyExecutorApprovalGate(
                gate_code="final_human_confirmation",
                label="Final human confirmation",
                safe_summary="[SYNTHETIC] Final confirmation is missing.",
                satisfied=False,
            )
        ],
        rollback_requirements=[
            module.ApplyExecutorRollbackRequirement(
                requirement_code="previous_persona_version_available",
                safe_summary="[SYNTHETIC] Previous version is not available.",
                covered=False,
            )
        ],
        audit_requirements=[],
    )

    assert assessment.final_recommendation == "blocked"
    assert "approval_gate_unsatisfied:final_human_confirmation" in assessment.blocking_issue_codes
    assert "rollback_requirement_uncovered:previous_persona_version_available" in assessment.blocking_issue_codes


def test_high_risk_with_all_controls_needs_review() -> None:
    module = _module()
    assessment = module.ApplyExecutorRiskAssessment(
        preview_id="mapprev_review",
        decision_id="rqdec_review",
        candidate_kind="persona_growth_patch",
        candidate_id="pgpatch_review",
        safe_summary="[SYNTHETIC] Assess high risk.",
        risk_factors=[
            module.ApplyExecutorRiskFactor(
                risk_code="relationship_expectation_shift",
                severity="high",
                safe_summary="[SYNTHETIC] User expectation risk needs review.",
            )
        ],
        approval_gates=[
            module.ApplyExecutorApprovalGate(
                gate_code="final_human_confirmation",
                label="Final human confirmation",
                safe_summary="[SYNTHETIC] Final confirmation is present.",
                satisfied=True,
            )
        ],
        rollback_requirements=[],
        audit_requirements=[],
    )

    assert assessment.final_recommendation == "needs_review"
    assert assessment.blocking_issue_codes == []


def test_serialized_risk_assessment_contains_no_forbidden_fields() -> None:
    serialized = _ready_assessment().model_dump_json().lower()

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


def test_risk_records_expose_no_runtime_or_apply_methods() -> None:
    module = _module()

    for target in (
        module.ApplyExecutorRiskFactor,
        module.ApplyExecutorApprovalGate,
        module.ApplyExecutorRollbackRequirement,
        module.ApplyExecutorAuditRequirement,
        module.ApplyExecutorRiskAssessment,
    ):
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


def test_risk_assessment_rejects_executing_flags() -> None:
    module = _module()

    with pytest.raises(ValueError):
        module.ApplyExecutorRiskAssessment(
            preview_id="mapprev_mutating",
            decision_id="rqdec_mutating",
            candidate_kind="persona_growth_patch",
            candidate_id="pgpatch_mutating",
            safe_summary="[SYNTHETIC] Mutating flags are rejected.",
            risk_factors=[],
            approval_gates=[],
            rollback_requirements=[],
            audit_requirements=[],
            applies_changes=True,
        )
