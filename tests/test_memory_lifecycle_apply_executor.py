"""T408 memory lifecycle apply executor tests.

All examples are synthetic. The executor writes only to caller-supplied local
MemoryEventStore paths. These tests do not read private chat history, call
providers, write persona versions, generate replies, send messages, or connect
to external platforms/media.
"""

from __future__ import annotations

import importlib
from pathlib import Path

import pytest

from practical_chat_agent.core.models import MemoryEvent, MemoryProvenance
from practical_chat_agent.services.apply_executor_approval_gate import (
    ApplyExecutorApprovalDecision,
)
from practical_chat_agent.services.manual_apply_eligibility_gate import (
    ManualApplyEligibilityDecision,
)
from practical_chat_agent.services.memory_event_store import MemoryEventStore
from practical_chat_agent.services.memory_governance import MemorySupersessionCandidate
from practical_chat_agent.services.memory_lifecycle_dry_run import (
    MemoryLifecycleDryRunPlan,
    MemoryLifecycleDryRunService,
)
from practical_chat_agent.services.review_queue import ReviewQueueService


def _module():
    return importlib.import_module(
        "practical_chat_agent.services.memory_lifecycle_apply_executor"
    )


def _store(tmp_path: Path) -> MemoryEventStore:
    return MemoryEventStore(tmp_path / "memory_events.json")


def _memory(summary: str) -> MemoryEvent:
    return MemoryEvent(
        user_id="user_synthetic",
        event_type="factual",
        truth_status="evidence_backed",
        summary=summary,
        provenance=MemoryProvenance(
            source_type="synthetic_test",
            evidence_refs=["synthetic_memory_apply"],
        ),
        sensitivity="low",
    )


def _plan(store: MemoryEventStore) -> tuple[str, str, MemoryLifecycleDryRunPlan]:
    source = store.append(_memory("[SYNTHETIC] User prefers short replies.")).event
    replacement = store.append(
        _memory("[SYNTHETIC] User now prefers detailed replies.")
    ).event
    candidate = MemorySupersessionCandidate.from_memory_ids(
        source_memory_id=source.event_id,
        replacement_memory_id=replacement.event_id,
        reason="[SYNTHETIC] Newer preference should supersede old preference.",
    )
    item = ReviewQueueService().item_from_candidate(candidate)
    decision = ReviewQueueService().record_decision(
        item,
        reviewer_id="reviewer_synthetic",
        decision="approve",
        decision_notes=["[SYNTHETIC] Approved for local apply."],
    )
    plan = MemoryLifecycleDryRunService().plan_from_candidate(
        candidate,
        decision_record=decision,
    )
    return source.event_id, replacement.event_id, plan


def _manual_decision(
    plan: MemoryLifecycleDryRunPlan,
    *,
    outcome: str = "eligible",
) -> ManualApplyEligibilityDecision:
    return ManualApplyEligibilityDecision(
        preview_id="mapprev_memory_apply",
        bundle_id="rwbundle_memory_apply",
        decision_id=plan.review_decision_id or "rqdec_memory_apply",
        candidate_kind=plan.source_candidate_kind,
        candidate_id=plan.source_candidate_id,
        preview_outcome="future_manual_apply_eligible",
        eligibility_outcome=outcome,
        safe_summary=f"[SYNTHETIC] Manual memory apply is {outcome}.",
        required_gate_codes=["human_approval"],
        satisfied_gate_codes=["human_approval"] if outcome == "eligible" else [],
        missing_gate_codes=[] if outcome == "eligible" else ["human_approval"],
        issue_codes=[] if outcome == "eligible" else ["manual_apply_blocked"],
        blocking_issue_codes=[] if outcome == "eligible" else ["manual_apply_blocked"],
        effect_count=len(plan.effects),
    )


def _approval_decision(
    plan: MemoryLifecycleDryRunPlan,
    manual: ManualApplyEligibilityDecision,
    *,
    final_outcome: str = "ready_for_separately_scoped_executor_design",
) -> ApplyExecutorApprovalDecision:
    risk_recommendation = (
        "needs_review" if final_outcome == "needs_review" else final_outcome
    )
    return ApplyExecutorApprovalDecision(
        assessment_id="aeassess_memory_apply",
        preview_id=manual.preview_id,
        decision_id=plan.review_decision_id or "rqdec_memory_apply",
        candidate_kind=plan.source_candidate_kind,
        candidate_id=plan.source_candidate_id,
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
    store: MemoryEventStore,
    plan: MemoryLifecycleDryRunPlan,
    manual: ManualApplyEligibilityDecision,
    approval: ApplyExecutorApprovalDecision,
    final_confirmation: str = "CONFIRM_LOCAL_MEMORY_APPLY",
):
    module = _module()
    return module.MemoryLifecycleApplyRequest(
        plan=plan,
        manual_eligibility=manual,
        approval_decision=approval,
        memory_store=store,
        reviewer_id="reviewer_synthetic",
        final_confirmation=final_confirmation,
    )


def test_confirmed_memory_lifecycle_apply_updates_state_with_rollback(
    tmp_path: Path,
) -> None:
    module = _module()
    store = _store(tmp_path)
    source_id, replacement_id, plan = _plan(store)
    manual = _manual_decision(plan)
    approval = _approval_decision(plan, manual)
    prior_record = store.get_record(source_id)

    audit = module.MemoryLifecycleApplyExecutor().apply(
        _request(store=store, plan=plan, manual=manual, approval=approval)
    )

    assert store.get(source_id).lifecycle_state == "superseded"
    assert store.get(replacement_id).lifecycle_state == "active"
    assert len(store.list_records(include_history=True)) == 3
    assert audit.schema_version == "memory_lifecycle_apply_audit_v1"
    assert audit.plan_id == plan.plan_id
    assert audit.affected_memory_ids == [source_id]
    assert audit.prior_lifecycle_states[source_id] == "active"
    assert audit.new_lifecycle_states[source_id] == "superseded"
    assert audit.rollback_record_ids[source_id] == prior_record.record_id
    assert audit.final_confirmation == "confirmed"
    assert audit.local_only is True
    assert audit.writes_memory_store is True
    assert audit.writes_persona_version is False


def test_missing_confirmation_blocks_without_writing(tmp_path: Path) -> None:
    module = _module()
    store = _store(tmp_path)
    _, _, plan = _plan(store)
    manual = _manual_decision(plan)
    approval = _approval_decision(plan, manual)

    with pytest.raises(module.MemoryLifecycleApplyError):
        module.MemoryLifecycleApplyExecutor().apply(
            _request(
                store=store,
                plan=plan,
                manual=manual,
                approval=approval,
                final_confirmation="",
            )
        )

    assert len(store.list_records(include_history=True)) == 2


def test_blocked_manual_or_approval_decisions_block_without_writing(
    tmp_path: Path,
) -> None:
    module = _module()
    store = _store(tmp_path)
    _, _, plan = _plan(store)
    blocked_manual = _manual_decision(plan, outcome="blocked")
    ready_approval = _approval_decision(plan, blocked_manual)
    eligible_manual = _manual_decision(plan)
    blocked_approval = _approval_decision(
        plan,
        eligible_manual,
        final_outcome="blocked",
    )

    with pytest.raises(module.MemoryLifecycleApplyError):
        module.MemoryLifecycleApplyExecutor().apply(
            _request(
                store=store,
                plan=plan,
                manual=blocked_manual,
                approval=ready_approval,
            )
        )
    with pytest.raises(module.MemoryLifecycleApplyError):
        module.MemoryLifecycleApplyExecutor().apply(
            _request(
                store=store,
                plan=plan,
                manual=eligible_manual,
                approval=blocked_approval,
            )
        )

    assert len(store.list_records(include_history=True)) == 2


def test_missing_memory_id_blocks_without_writing(tmp_path: Path) -> None:
    module = _module()
    store = _store(tmp_path)
    _, _, plan = _plan(store)
    missing_effect = plan.effects[0].model_copy(update={"memory_id": "mev_missing"})
    stale_plan = plan.model_copy(deep=True, update={"effects": [missing_effect]})
    manual = _manual_decision(stale_plan)
    approval = _approval_decision(stale_plan, manual)

    with pytest.raises(module.MemoryLifecycleApplyError):
        module.MemoryLifecycleApplyExecutor().apply(
            _request(store=store, plan=stale_plan, manual=manual, approval=approval)
        )

    assert len(store.list_records(include_history=True)) == 2


def test_apply_audit_contains_no_private_provider_outbound_or_media_fields(
    tmp_path: Path,
) -> None:
    module = _module()
    store = _store(tmp_path)
    _, _, plan = _plan(store)
    manual = _manual_decision(plan)
    approval = _approval_decision(plan, manual)

    audit = module.MemoryLifecycleApplyExecutor().apply(
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
    service = _module().MemoryLifecycleApplyExecutor()

    for method_name in (
        "send",
        "schedule",
        "deliver",
        "call_provider",
        "open_webhook",
        "write_persona_version",
        "generate_reply",
        "generate_voice",
        "generate_avatar",
        "generate_audio",
        "generate_image",
        "generate_video",
        "connect_platform",
    ):
        assert not hasattr(service, method_name)
