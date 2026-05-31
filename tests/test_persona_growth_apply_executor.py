"""T407 persona growth apply executor tests.

All examples are synthetic. The executor writes only to caller-supplied local
PersonaVersionStore paths. These tests do not read private chat history, call
providers, mutate memory stores, generate replies, send messages, or connect to
external platforms/media.
"""

from __future__ import annotations

import importlib
from pathlib import Path
from typing import Any

import pytest

from practical_chat_agent.services.apply_executor_approval_gate import (
    ApplyExecutorApprovalDecision,
)
from practical_chat_agent.services.manual_apply_eligibility_gate import (
    ManualApplyEligibilityDecision,
)
from practical_chat_agent.services.persona_compiler import PersonaCompilerService
from practical_chat_agent.services.persona_growth import (
    PersonaGrowthFieldChange,
    PersonaGrowthPatchCandidate,
)
from practical_chat_agent.services.persona_growth_dry_run import (
    PersonaGrowthDryRunPlan,
    PersonaGrowthDryRunService,
)
from practical_chat_agent.services.persona_version_store import PersonaVersionStore
from practical_chat_agent.services.review_queue import ReviewQueueService


def _module():
    return importlib.import_module(
        "practical_chat_agent.services.persona_growth_apply_executor"
    )


def _store(tmp_path: Path) -> PersonaVersionStore:
    return PersonaVersionStore(tmp_path / "persona_versions.json")


def _persona():
    return PersonaCompilerService().compile(
        {
            "user_id": "user_synthetic",
            "display_name": "Lin Qi",
            "creation_mode": "detailed_prompt",
            "description": "fictional calm concise companion with dry humor",
        }
    )


def _plan(store: PersonaVersionStore) -> tuple[Any, PersonaGrowthDryRunPlan]:
    saved = store.save(_persona())
    change = PersonaGrowthFieldChange(
        field_path="core_traits.warmth",
        old_value_summary=str(saved.card.core_traits.warmth),
        proposed_value_summary=str(saved.card.core_traits.warmth + 0.04),
        numeric_delta=0.04,
        change_reason="[SYNTHETIC] User asked for warmer replies.",
        source_memory_ids=["mev_synthetic_apply"],
    )
    patch = PersonaGrowthPatchCandidate.from_persona_card(
        saved.card,
        trigger_type="memory_pattern",
        trigger_summary="[SYNTHETIC] Warmer reply preference.",
        changes=[change],
        user_facing_explanation="[SYNTHETIC] Propose slightly warmer replies.",
        weekly_trait_delta_by_field={"core_traits.warmth": 0.0},
    )
    item = ReviewQueueService().item_from_candidate(patch)
    decision = ReviewQueueService().record_decision(
        item,
        reviewer_id="reviewer_synthetic",
        decision="approve",
        decision_notes=["[SYNTHETIC] Approved for local apply."],
    )
    plan = PersonaGrowthDryRunService().plan_from_patch(
        patch,
        source_persona=saved.card,
        decision_record=decision,
    )
    return saved, plan


def _manual_decision(
    plan: PersonaGrowthDryRunPlan,
    *,
    outcome: str = "eligible",
) -> ManualApplyEligibilityDecision:
    return ManualApplyEligibilityDecision(
        preview_id="mapprev_persona_apply",
        bundle_id="rwbundle_persona_apply",
        decision_id=plan.review_decision_id or "rqdec_persona_apply",
        candidate_kind="persona_growth_patch",
        candidate_id=plan.patch_id,
        preview_outcome="future_manual_apply_eligible",
        eligibility_outcome=outcome,
        safe_summary=f"[SYNTHETIC] Manual apply is {outcome}.",
        required_gate_codes=["human_approval"],
        satisfied_gate_codes=["human_approval"] if outcome == "eligible" else [],
        missing_gate_codes=[] if outcome == "eligible" else ["human_approval"],
        issue_codes=[] if outcome == "eligible" else ["manual_apply_blocked"],
        blocking_issue_codes=[] if outcome == "eligible" else ["manual_apply_blocked"],
        effect_count=1,
    )


def _approval_decision(
    plan: PersonaGrowthDryRunPlan,
    manual: ManualApplyEligibilityDecision,
    *,
    final_outcome: str = "ready_for_separately_scoped_executor_design",
) -> ApplyExecutorApprovalDecision:
    risk_recommendation = (
        "needs_review" if final_outcome == "needs_review" else final_outcome
    )
    return ApplyExecutorApprovalDecision(
        assessment_id="aeassess_persona_apply",
        preview_id=manual.preview_id,
        decision_id=plan.review_decision_id or "rqdec_persona_apply",
        candidate_kind="persona_growth_patch",
        candidate_id=plan.patch_id,
        risk_recommendation=risk_recommendation,
        manual_eligibility_outcome=manual.eligibility_outcome,
        safe_summary=f"[SYNTHETIC] Approval outcome is {final_outcome}.",
        required_approval_gate_codes=["final_human_confirmation"],
        satisfied_approval_gate_codes=(
            ["final_human_confirmation"]
            if final_outcome == "ready_for_separately_scoped_executor_design"
            else []
        ),
        blocking_issue_codes=[] if final_outcome == "ready_for_separately_scoped_executor_design" else ["approval_blocked"],
        final_outcome=final_outcome,
    )


def _request(
    *,
    store: PersonaVersionStore,
    plan: PersonaGrowthDryRunPlan,
    manual: ManualApplyEligibilityDecision,
    approval: ApplyExecutorApprovalDecision,
    final_confirmation: str = "CONFIRM_LOCAL_PERSONA_APPLY",
):
    module = _module()
    return module.PersonaGrowthApplyRequest(
        plan=plan,
        manual_eligibility=manual,
        approval_decision=approval,
        persona_store=store,
        reviewer_id="reviewer_synthetic",
        final_confirmation=final_confirmation,
    )


def test_confirmed_safe_persona_growth_writes_new_version_with_rollback(
    tmp_path: Path,
) -> None:
    module = _module()
    store = _store(tmp_path)
    saved, plan = _plan(store)
    manual = _manual_decision(plan)
    approval = _approval_decision(plan, manual)

    audit = module.PersonaGrowthApplyExecutor().apply(
        _request(store=store, plan=plan, manual=manual, approval=approval)
    )

    versions = store.list_versions(saved.persona_id)
    latest = store.latest_record(saved.persona_id)
    assert len(versions) == 2
    assert audit.schema_version == "persona_growth_apply_audit_v1"
    assert audit.persona_id == saved.persona_id
    assert audit.patch_id == plan.patch_id
    assert audit.prior_version_id == saved.version_id
    assert audit.new_version_id == latest.version_id
    assert audit.rollback_target_version_id == saved.version_id
    assert audit.changed_field_paths == ["core_traits.warmth"]
    assert audit.final_confirmation == "confirmed"
    assert audit.local_only is True
    assert audit.writes_persona_version is True
    assert audit.writes_memory_store is False
    assert latest.parent_version_id == saved.version_id
    assert latest.card.core_traits.warmth == pytest.approx(
        saved.card.core_traits.warmth + 0.04
    )


def test_missing_confirmation_blocks_without_writing(tmp_path: Path) -> None:
    module = _module()
    store = _store(tmp_path)
    saved, plan = _plan(store)
    manual = _manual_decision(plan)
    approval = _approval_decision(plan, manual)

    with pytest.raises(module.PersonaGrowthApplyError):
        module.PersonaGrowthApplyExecutor().apply(
            _request(
                store=store,
                plan=plan,
                manual=manual,
                approval=approval,
                final_confirmation="",
            )
        )

    assert len(store.list_versions(saved.persona_id)) == 1


def test_blocked_manual_or_approval_decisions_block_without_writing(
    tmp_path: Path,
) -> None:
    module = _module()
    store = _store(tmp_path)
    saved, plan = _plan(store)
    blocked_manual = _manual_decision(plan, outcome="blocked")
    ready_approval = _approval_decision(plan, blocked_manual)
    eligible_manual = _manual_decision(plan)
    blocked_approval = _approval_decision(
        plan,
        eligible_manual,
        final_outcome="blocked",
    )

    with pytest.raises(module.PersonaGrowthApplyError):
        module.PersonaGrowthApplyExecutor().apply(
            _request(
                store=store,
                plan=plan,
                manual=blocked_manual,
                approval=ready_approval,
            )
        )
    with pytest.raises(module.PersonaGrowthApplyError):
        module.PersonaGrowthApplyExecutor().apply(
            _request(
                store=store,
                plan=plan,
                manual=eligible_manual,
                approval=blocked_approval,
            )
        )

    assert len(store.list_versions(saved.persona_id)) == 1


def test_stale_source_version_blocks_without_writing(tmp_path: Path) -> None:
    module = _module()
    store = _store(tmp_path)
    saved, plan = _plan(store)
    store.save(saved.card.model_copy(deep=True))
    manual = _manual_decision(plan)
    approval = _approval_decision(plan, manual)

    with pytest.raises(module.PersonaGrowthApplyError):
        module.PersonaGrowthApplyExecutor().apply(
            _request(store=store, plan=plan, manual=manual, approval=approval)
        )

    assert len(store.list_versions(saved.persona_id)) == 2


def test_apply_audit_contains_no_private_provider_outbound_or_media_fields(
    tmp_path: Path,
) -> None:
    module = _module()
    store = _store(tmp_path)
    _, plan = _plan(store)
    manual = _manual_decision(plan)
    approval = _approval_decision(plan, manual)

    audit = module.PersonaGrowthApplyExecutor().apply(
        _request(store=store, plan=plan, manual=manual, approval=approval)
    )
    serialized = audit.model_dump_json().lower()

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
        "generated_audio",
        "generated_image",
        "generated_video",
    ):
        assert forbidden not in serialized


def test_executor_exposes_no_provider_outbound_scheduler_or_media_methods() -> None:
    service = _module().PersonaGrowthApplyExecutor()

    for method_name in (
        "send",
        "schedule",
        "deliver",
        "call_provider",
        "open_webhook",
        "mutate_memory_store",
        "generate_reply",
        "generate_voice",
        "generate_avatar",
        "generate_audio",
        "generate_image",
        "generate_video",
        "connect_platform",
    ):
        assert not hasattr(service, method_name)
