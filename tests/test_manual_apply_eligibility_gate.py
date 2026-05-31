"""T398 manual apply eligibility gate tests.

The gate is deterministic and non-mutating. It does not apply decisions,
mutate stores, call providers, generate media, or enable outbound behavior.
"""

from __future__ import annotations

import importlib

from practical_chat_agent.services.manual_apply_preview import (
    ManualApplyPreviewEffect,
    ManualApplyPreviewGate,
    ManualApplyPreviewRecord,
)


def _module():
    return importlib.import_module(
        "practical_chat_agent.services.manual_apply_eligibility_gate"
    )


def _preview(*, eligible: bool = True, blocked: bool = False) -> ManualApplyPreviewRecord:
    gates = [
        ManualApplyPreviewGate(
            gate_code="human_approval",
            label="Human approval",
            safe_summary="[SYNTHETIC] Human approval is present.",
            satisfied=eligible and not blocked,
            blocking_issue_codes=[] if eligible and not blocked else ["manual_apply_gate_unsatisfied"],
        )
    ]
    return ManualApplyPreviewRecord(
        bundle_id="rwbundle_gate",
        decision_id="rqdec_gate",
        candidate_kind="persona_growth_patch",
        candidate_id="pgpatch_gate",
        preview_outcome="future_manual_apply_eligible" if not blocked else "blocked_before_apply",
        safe_summary="[SYNTHETIC] Review manual apply gate.",
        reason_labels=["memory_pattern"],
        source_refs=["synthetic_gate_ref"],
        artifact_ids=["pgdplan_gate"],
        required_gates=gates,
        effects=[
            ManualApplyPreviewEffect(
                effect_kind="persona_version_preview",
                target_ref="persona_synthetic",
                safe_summary="[SYNTHETIC] Persona warmth would be adjusted.",
                artifact_ids=["pgdplan_gate"],
                rollback_notes=["[SYNTHETIC] Keep prior persona version."],
            )
        ],
        rollback_notes=["[SYNTHETIC] Keep prior persona version."],
        blocking_issue_codes=["candidate_id_mismatch"] if blocked else [],
    )


def test_eligible_preview_produces_non_mutating_eligible_decision() -> None:
    decision = _module().ManualApplyEligibilityGate().evaluate(_preview())

    assert decision.eligibility_outcome == "eligible"
    assert decision.safe_summary == "[SYNTHETIC] Manual apply preview is eligible."
    assert decision.blocking_issue_codes == []
    assert decision.stale_reasons == []
    assert decision.effect_count == 1
    assert decision.review_required is True
    assert decision.preview_only is True
    assert decision.applies_changes is False
    assert decision.writes_memory_store is False
    assert decision.writes_persona_version is False
    assert decision.runtime_ready is False


def test_blocked_preview_produces_blocked_decision() -> None:
    decision = _module().ManualApplyEligibilityGate().evaluate(_preview(blocked=True))

    assert decision.eligibility_outcome == "blocked"
    assert "candidate_id_mismatch" in decision.blocking_issue_codes
    assert "manual_apply_gate_unsatisfied" in decision.blocking_issue_codes
    assert decision.applies_changes is False


def test_stale_context_produces_stale_decision() -> None:
    decision = _module().ManualApplyEligibilityGate().evaluate(
        _preview(),
        expected_decision_id="rqdec_other",
        expected_candidate_id="pgpatch_other",
        expected_preview_outcome="blocked_before_apply",
    )

    assert decision.eligibility_outcome == "stale"
    assert decision.blocking_issue_codes == ["manual_apply_preview_stale"]
    assert decision.stale_reasons == [
        "decision_id_mismatch",
        "candidate_id_mismatch",
        "preview_outcome_mismatch",
    ]


def test_gate_mismatch_produces_blocked_decision() -> None:
    decision = _module().ManualApplyEligibilityGate().evaluate(
        _preview(),
        required_gate_codes=["human_approval", "active_consent_scope"],
    )

    assert decision.eligibility_outcome == "blocked"
    assert "missing_required_gate:active_consent_scope" in decision.blocking_issue_codes


def test_serialized_eligibility_decision_contains_no_forbidden_fields() -> None:
    serialized = _module().ManualApplyEligibilityGate().evaluate(_preview()).model_dump_json().lower()

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


def test_eligibility_gate_exposes_no_runtime_or_apply_methods() -> None:
    service = _module().ManualApplyEligibilityGate()

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
        assert not hasattr(service, method_name)
