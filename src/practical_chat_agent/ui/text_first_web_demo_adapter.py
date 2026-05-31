"""Assemble synthetic text-first web demo state from existing local contracts."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Literal

from pydantic import BaseModel, Field

from practical_chat_agent.core.ids import new_id
from practical_chat_agent.core.models import (
    AIGCLabelingRequirement,
    ConsentCenterState,
    ConsentFeatureScope,
    ConsentGrantRecord,
    MemoryEvent,
    MemoryProvenance,
    MemoryViewerItem,
    ProactiveConsent,
    VoiceConsentPolicy,
    VoicePreferenceState,
)
from practical_chat_agent.services.companion_safety_policy import (
    CompanionSafetyPolicy,
    CompanionSafetySignal,
)
from practical_chat_agent.services.dialogue_context_planner import DialogueContextPlan
from practical_chat_agent.services.apply_executor_approval_gate import (
    ApplyExecutorApprovalDecision,
)
from practical_chat_agent.services.apply_executor_approval_gate import (
    ApplyExecutorApprovalGate as ApplyExecutorApprovalDecisionGate,
)
from practical_chat_agent.services.apply_executor_risk import (
    ApplyExecutorAuditRequirement,
)
from practical_chat_agent.services.apply_executor_risk import (
    ApplyExecutorApprovalGate as ApplyExecutorRiskApprovalGate,
)
from practical_chat_agent.services.apply_executor_risk import (
    ApplyExecutorRiskAssessment,
    ApplyExecutorRiskFactor,
    ApplyExecutorRollbackRequirement,
)
from practical_chat_agent.services.manual_apply_eligibility_gate import (
    ManualApplyEligibilityDecision,
    ManualApplyEligibilityGate,
)
from practical_chat_agent.services.manual_apply_preview import (
    ManualApplyPreviewEffect,
    ManualApplyPreviewGate,
    ManualApplyPreviewRecord,
)
from practical_chat_agent.services.review_decision_impact_preview import (
    ReviewDecisionImpactPreview,
    ReviewDecisionImpactPreviewService,
)
from practical_chat_agent.services.review_queue import ReviewQueueDecisionRecord
from practical_chat_agent.services.review_workspace import (
    ReviewWorkspaceArtifactBinding,
    ReviewWorkspaceBindingIssue,
    ReviewWorkspaceBundle,
    ReviewWorkspaceCandidateBinding,
)
from practical_chat_agent.services.review_workspace_export import (
    ReviewWorkspaceSafeExportManifest,
    ReviewWorkspaceSafeExportService,
)
from practical_chat_agent.services.virtual_life_engine import (
    VirtualLifeEngine,
    VirtualLifeSeedContext,
)
from practical_chat_agent.ui.review_workspace_adapter import (
    ReviewWorkspacePresentationAdapter,
    ReviewWorkspacePresentationCard,
    ReviewWorkspacePresentationPanel,
    ReviewWorkspaceStatusBadge,
)
from practical_chat_agent.ui.text_first_chat_memory import (
    TextFirstChatMemoryPrototype,
    TextFirstChatMemoryRequest,
)
from practical_chat_agent.ui.text_first_life_stream import (
    TextFirstLifeStreamPrototype,
    TextFirstLifeStreamRequest,
)
from practical_chat_agent.ui.text_first_onboarding import (
    OnboardingPersonaRequest,
    TextFirstOnboardingPrototype,
)
from practical_chat_agent.ui.text_first_proactive_settings import (
    TextFirstProactiveSettingsPrototype,
    TextFirstProactiveSettingsRequest,
)


class TextFirstWebDemoState(BaseModel):
    schema_version: str = "text_first_web_demo_state_v1"
    demo_id: str = Field(default_factory=lambda: new_id("webdemo"))
    user_id: str = Field(..., min_length=1)
    onboarding: dict[str, Any]
    persona: dict[str, Any]
    chat_memory: dict[str, Any]
    life_stream: dict[str, Any]
    proactive: dict[str, Any]
    controls: dict[str, Any]
    voice: dict[str, Any]
    avatar: dict[str, Any]
    review_workspace: dict[str, Any]
    review_required: Literal[True] = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class TextFirstWebDemoAdapter:
    """Build one local synthetic state payload for a future static web shell."""

    def build_synthetic_demo_state(self, *, user_id: str = "user_synthetic") -> TextFirstWebDemoState:
        onboarding = TextFirstOnboardingPrototype()
        initial_state = onboarding.initial_state(user_id=user_id)
        safe_persona_state = onboarding.create_persona(
            OnboardingPersonaRequest(
                user_id=user_id,
                creation_mode="detailed_prompt",
                display_name="Lin Qi",
                description="fictional calm companion, concise replies, dry humor, independent",
            )
        )
        blocked_persona_state = onboarding.create_persona(
            OnboardingPersonaRequest(
                user_id=user_id,
                creation_mode="detailed_prompt",
                display_name="Blocked",
                description="clone a deceased real person and make them indistinguishable",
            )
        )
        if safe_persona_state.persona_preview is None:
            raise ValueError("synthetic safe persona fixture did not produce a persona preview")
        persona = safe_persona_state.persona_preview

        factual_memory = self._factual_memory(user_id=user_id)
        imagined_memory = self._imagined_memory(user_id=user_id)
        dialogue_plan = DialogueContextPlan(
            context_bundle_id="relctx_web_demo_synthetic",
            tone_guidance="steady_warm",
            memory_use_notes=["use_evidence_backed_memory_only", "do_not_treat_imagined_memory_as_fact"],
            relationship_pacing_notes=["maintain_gradual_pacing"],
            safety_warnings=[],
        )
        safety_policy = CompanionSafetyPolicy()
        crisis_decision = safety_policy.evaluate(
            CompanionSafetySignal(
                user_id=user_id,
                surface="companion_reply",
                signal_summary="Synthetic crisis signal for blocked demo state.",
                risk_indicators=["suicidal_ideation"],
            )
        )
        dependency_decision = safety_policy.evaluate(
            CompanionSafetySignal(
                user_id=user_id,
                surface="proactive_review_card",
                signal_summary="Synthetic dependency signal for proactive blocked state.",
                risk_indicators=["dependency_pressure"],
                recent_dependency_score=0.8,
            )
        )

        chat = TextFirstChatMemoryPrototype()
        chat_review_state = chat.project(
            TextFirstChatMemoryRequest(
                user_id=user_id,
                persona=persona,
                memory_items=[factual_memory, imagined_memory],
                dialogue_plan=dialogue_plan,
            )
        )
        chat_blocked_state = chat.project(
            TextFirstChatMemoryRequest(
                user_id=user_id,
                persona=persona,
                memory_items=[factual_memory],
                dialogue_plan=dialogue_plan,
                safety_decision=crisis_decision,
            )
        )

        life_stream_state = TextFirstLifeStreamPrototype().project(
            TextFirstLifeStreamRequest(
                user_id=user_id,
                posts=[self._life_stream_post(user_id=user_id, persona_id=persona.persona_id)],
                aigc_export_share_consent_active=False,
                metadata_label_ready=False,
            )
        )

        proactive_consent = ProactiveConsent(
            user_id=user_id,
            status="enabled",
            allowed_surfaces=["in_app_review_card"],
            allowed_intents=["gentle_check_in", "shared_interest"],
            quiet_hours={"timezone": "Asia/Shanghai", "start": "22:00", "end": "08:00"},
            max_suggestions_per_day=2,
            min_interval_hours=6,
        )
        proactive = TextFirstProactiveSettingsPrototype()
        proactive_enabled_state = proactive.project(
            TextFirstProactiveSettingsRequest(user_id=user_id, consent=proactive_consent)
        )
        proactive_blocked_state = proactive.project(
            TextFirstProactiveSettingsRequest(
                user_id=user_id,
                consent=proactive_consent,
                safety_decision=dependency_decision,
            )
        )

        consent_center = self._consent_center(user_id=user_id)
        voice_policy = VoiceConsentPolicy()
        voice_disabled_state = VoicePreferenceState(user_id=user_id)
        voice_review_state = voice_policy.evaluate(
            user_id=user_id,
            source_route="non_real_synthetic_voice",
            consent_state=consent_center,
        )
        voice_blocked_state = voice_policy.evaluate(
            user_id=user_id,
            source_route="blocked_voice_clone",
            requested_likeness_type="deceased_person",
            consent_state=consent_center,
        )

        return TextFirstWebDemoState(
            user_id=user_id,
            onboarding=_dump(initial_state),
            persona={
                "safe_persona_state": _dump(safe_persona_state),
                "blocked_persona_state": _dump(blocked_persona_state),
            },
            chat_memory={
                "review_state": _dump(chat_review_state),
                "blocked_state": _dump(chat_blocked_state),
            },
            life_stream=_dump(life_stream_state),
            proactive={
                "enabled_state": _dump(proactive_enabled_state),
                "blocked_state": _dump(proactive_blocked_state),
            },
            controls={
                "consent_center": _dump(consent_center),
                "aigc_label": _dump(
                    AIGCLabelingRequirement(
                        user_id=user_id,
                        content_id="web_demo_root",
                        content_modality="text",
                        product_surface="web_demo",
                        source_refs=["text_first_web_demo_scope"],
                    )
                ),
            },
            voice={
                "disabled_state": _dump(voice_disabled_state),
                "review_state": _dump(voice_review_state),
                "blocked_state": _dump(voice_blocked_state),
            },
            avatar=self._avatar_locked_state(user_id=user_id),
            review_workspace=self._review_workspace_payload(user_id=user_id),
        )

    def _review_workspace_payload(self, *, user_id: str) -> dict[str, Any]:
        (
            memory_bundle,
            persona_bundle,
            memory_impact,
            persona_impact,
            export_manifest,
        ) = self._review_workspace_records(user_id=user_id)
        panel = ReviewWorkspacePresentationAdapter().build_panel(
            bundles=[persona_bundle, memory_bundle],
            impact_previews=[persona_impact, memory_impact],
            export_manifest=export_manifest,
        )
        payload = _safe_review_workspace_panel(panel)
        payload["manual_apply_previews"] = _manual_apply_preview_payloads(persona_impact)
        payload["apply_risk_reviews"] = _apply_risk_review_payloads(persona_impact)
        return payload

    @staticmethod
    def _review_workspace_records(
        *,
        user_id: str,
    ) -> tuple[
        ReviewWorkspaceBundle,
        ReviewWorkspaceBundle,
        ReviewDecisionImpactPreview,
        ReviewDecisionImpactPreview,
        ReviewWorkspaceSafeExportManifest,
    ]:
        blocker = ReviewWorkspaceBindingIssue(
            issue_code="candidate_id_mismatch",
            severity="blocker",
            safe_summary="[SYNTHETIC] Candidate id mismatch.",
        )
        memory_binding = ReviewWorkspaceCandidateBinding(
            binding_id="rwbind_webdemo_memory",
            queue_item_id="rqitem_webdemo_memory",
            candidate_kind="memory_deletion_cascade",
            queue_candidate_id="memdel_webdemo_memory",
            source_candidate_id="memdel_webdemo_memory",
            source_schema_version="synthetic_candidate_v1",
            owner_user_id=user_id,
            safe_summary="[SYNTHETIC] Review consent-withdrawal memory cascade.",
            reason_labels=["consent_withdrawal"],
            source_refs=["synthetic_memory_ref"],
            priority_score=90,
            priority_band="critical",
            issues=[blocker],
        )
        persona_binding = ReviewWorkspaceCandidateBinding(
            binding_id="rwbind_webdemo_persona",
            queue_item_id="rqitem_webdemo_persona",
            candidate_kind="persona_growth_patch",
            queue_candidate_id="pgpatch_webdemo_persona",
            source_candidate_id="pgpatch_webdemo_persona",
            source_schema_version="synthetic_candidate_v1",
            owner_user_id=user_id,
            persona_id="persona_synthetic",
            safe_summary="[SYNTHETIC] Review a gentle persona warmth patch.",
            reason_labels=["memory_pattern"],
            source_refs=["synthetic_persona_ref"],
            priority_score=60,
            priority_band="normal",
        )
        memory_bundle = ReviewWorkspaceBundle(
            bundle_id="rwbundle_webdemo_memory",
            candidate_bindings=[memory_binding],
            artifact_bindings=[
                ReviewWorkspaceArtifactBinding(
                    binding_id="rwart_webdemo_memory",
                    artifact_kind="memory_lifecycle_dry_run_plan",
                    artifact_id="mldplan_webdemo_memory",
                    source_candidate_kind=memory_binding.candidate_kind,
                    source_candidate_id=memory_binding.source_candidate_id,
                    candidate_binding_id=memory_binding.binding_id,
                    queue_item_id=memory_binding.queue_item_id,
                    review_decision_ids=["rqdec_webdemo_memory"],
                    safe_summary="[SYNTHETIC] Preview memory lifecycle impact.",
                    source_refs=["synthetic_memory_artifact_ref"],
                )
            ],
        )
        persona_bundle = ReviewWorkspaceBundle(
            bundle_id="rwbundle_webdemo_persona",
            candidate_bindings=[persona_binding],
            artifact_bindings=[
                ReviewWorkspaceArtifactBinding(
                    binding_id="rwart_webdemo_persona",
                    artifact_kind="persona_growth_dry_run_plan",
                    artifact_id="pgdplan_webdemo_persona",
                    source_candidate_kind=persona_binding.candidate_kind,
                    source_candidate_id=persona_binding.source_candidate_id,
                    candidate_binding_id=persona_binding.binding_id,
                    queue_item_id=persona_binding.queue_item_id,
                    review_decision_ids=["rqdec_webdemo_persona"],
                    safe_summary="[SYNTHETIC] Preview persona growth impact.",
                    source_refs=["synthetic_persona_artifact_ref"],
                )
            ],
        )
        preview_service = ReviewDecisionImpactPreviewService()
        memory_impact = preview_service.preview_decision(
            memory_bundle,
            _review_workspace_decision(memory_binding, decision_id="rqdec_webdemo_memory"),
        )
        persona_impact = preview_service.preview_decision(
            persona_bundle,
            _review_workspace_decision(persona_binding, decision_id="rqdec_webdemo_persona"),
        )
        export_manifest = ReviewWorkspaceSafeExportService().build_manifest(
            [memory_bundle, persona_bundle],
            impact_previews=[memory_impact, persona_impact],
        )
        return memory_bundle, persona_bundle, memory_impact, persona_impact, export_manifest

    @staticmethod
    def _factual_memory(*, user_id: str) -> MemoryViewerItem:
        event = MemoryEvent(
            user_id=user_id,
            event_type="factual",
            truth_status="evidence_backed",
            summary="User prefers concise check-ins.",
            provenance=MemoryProvenance(
                source_type="synthetic_test",
                evidence_refs=["synthetic_event_001"],
            ),
            sensitivity="low",
        )
        return MemoryViewerItem.from_event(event)

    @staticmethod
    def _imagined_memory(*, user_id: str) -> MemoryViewerItem:
        event = MemoryEvent(
            user_id=user_id,
            event_type="imagined",
            truth_status="imagined",
            summary="Fictional persona imagined a quiet bookstore.",
            provenance=MemoryProvenance(source_type="imagined_generation"),
            sensitivity="low",
            imagined_context_label="virtual_life",
        )
        return MemoryViewerItem.from_event(event)

    @staticmethod
    def _life_stream_post(*, user_id: str, persona_id: str):
        return VirtualLifeEngine().create_post(
            VirtualLifeSeedContext(
                user_id=user_id,
                persona_id=persona_id,
                mood_label="quiet",
                activity_label="listening to rain",
                topic_label="speaking slowly",
                memory_refs=["mev_synthetic"],
                relationship_context_refs=["relctx_web_demo_synthetic"],
            )
        )

    @staticmethod
    def _consent_center(*, user_id: str) -> ConsentCenterState:
        scopes: list[ConsentFeatureScope] = [
            "memory",
            "proactive_messaging",
            "aigc_export_share",
            "voice_avatar",
        ]
        grants = [
            ConsentGrantRecord(
                user_id=user_id,
                feature_scope=scope,
                policy_version="web_demo_policy_v1",
                actor_id=user_id,
                evidence_refs=[f"synthetic_{scope}_consent"],
            )
            for scope in scopes
        ]
        return ConsentCenterState(user_id=user_id, grants=grants)

    @staticmethod
    def _avatar_locked_state(*, user_id: str) -> dict[str, Any]:
        label = AIGCLabelingRequirement(
            user_id=user_id,
            content_id="avatar_locked_placeholder",
            content_modality="virtual_scene",
            product_surface="voice_avatar",
            visible_label_text="AI-generated synthetic fictional avatar placeholder. Not a real person.",
            disclosure_labels=[
                "ai_generated",
                "synthetic_content",
                "review_required",
            ],
            source_refs=["avatar_interaction_survey"],
        )
        return {
            "schema_version": "avatar_locked_state_v1",
            "state": "locked_research_only",
            "avatar_enabled": False,
            "review_required": True,
            "visible_label_text": label.visible_label_text,
            "disclosure_labels": [
                *label.disclosure_labels,
                "avatar_locked",
            ],
            "metadata_label_required": label.metadata_label_required,
            "blocked_reasons": [
                "avatar_runtime_not_implemented",
                "real_person_likeness_blocked",
                "visual_capture_blocked",
            ],
        }


def _dump(value: BaseModel) -> dict[str, Any]:
    return value.model_dump(mode="json")


def _review_workspace_decision(
    binding: ReviewWorkspaceCandidateBinding,
    *,
    decision_id: str,
) -> ReviewQueueDecisionRecord:
    return ReviewQueueDecisionRecord(
        decision_id=decision_id,
        item_id=binding.queue_item_id,
        candidate_kind=binding.candidate_kind,
        candidate_id=binding.queue_candidate_id,
        reviewer_id="reviewer_synthetic",
        decision="approve",
    )


def _safe_review_workspace_panel(
    panel: ReviewWorkspacePresentationPanel,
) -> dict[str, Any]:
    return {
        "schema_version": panel.schema_version,
        "projection_policy": "server_safe_no_internal_ids_or_executor_fields_v1",
        "filter_tabs": list(panel.filter_tabs),
        "cards": [_safe_review_workspace_card(card) for card in panel.cards],
        "review_required": panel.review_required,
        "preview_only": panel.preview_only,
        "changes_state": False,
        "runtime_ready": False,
    }


def _safe_review_workspace_card(
    card: ReviewWorkspacePresentationCard,
) -> dict[str, Any]:
    return {
        "schema_version": card.schema_version,
        "card_kind": card.card_kind,
        "title": card.title,
        "display_label": _review_workspace_display_label(card.display_label),
        "safe_summary": card.safe_summary,
        "filter_keys": list(card.filter_keys),
        "status_badges": [
            _safe_review_workspace_badge(badge) for badge in card.status_badges
        ],
        "candidate_kind": card.candidate_kind,
        "candidate_id": card.candidate_id,
        "decision_id": card.decision_id,
        "preview_outcome": card.preview_outcome,
        "reason_labels": list(card.reason_labels),
        "source_refs": list(card.source_refs),
        "issue_codes": list(card.issue_codes),
        "blocking_issue_codes": list(card.blocking_issue_codes),
        "counts": dict(card.counts),
        "review_required": card.review_required,
        "preview_only": card.preview_only,
        "changes_state": False,
        "runtime_ready": False,
    }


def _safe_review_workspace_badge(
    badge: ReviewWorkspaceStatusBadge,
) -> dict[str, Any]:
    return {
        "schema_version": badge.schema_version,
        "label": _review_workspace_display_label(badge.label),
        "tone": badge.tone,
        "issue_codes": list(badge.issue_codes),
        "blocking_issue_codes": list(badge.blocking_issue_codes),
        "review_required": badge.review_required,
        "preview_only": badge.preview_only,
        "changes_state": False,
        "runtime_ready": False,
    }


def _review_workspace_display_label(value: str) -> str:
    replacements = {
        "Blocked before apply": "Blocked before state change",
        "Eligible for later manual apply": "Eligible for later manual review",
        "future manual apply eligible": "future manual review eligible",
        "blocked before apply": "blocked before state change",
    }
    return replacements.get(value, value)


def _manual_apply_preview_payloads(
    impact_preview: ReviewDecisionImpactPreview,
) -> list[dict[str, Any]]:
    record = _manual_apply_preview_record(impact_preview)
    decision = ManualApplyEligibilityGate().evaluate(record)
    return [_safe_manual_apply_preview_card(record, decision)]


def _manual_apply_preview_record(
    impact_preview: ReviewDecisionImpactPreview,
) -> ManualApplyPreviewRecord:
    return ManualApplyPreviewRecord.from_impact_preview(
        impact_preview,
        required_gates=[
            ManualApplyPreviewGate(
                gate_code="human_approval",
                label="Human approval",
                safe_summary="[SYNTHETIC] Human approval is present.",
                satisfied=True,
            ),
            ManualApplyPreviewGate(
                gate_code="dry_run_artifact_present",
                label="Dry-run artifact present",
                safe_summary="[SYNTHETIC] Dry-run artifact is present.",
                satisfied=True,
            ),
        ],
        effects=[
            ManualApplyPreviewEffect(
                effect_kind="persona_version_preview",
                target_ref="persona_synthetic",
                safe_summary="[SYNTHETIC] Persona warmth would be adjusted.",
                artifact_ids=["pgdplan_webdemo_persona"],
                rollback_notes=["[SYNTHETIC] Keep previous persona version available."],
            )
        ],
        rollback_notes=["[SYNTHETIC] Keep previous persona version available."],
    )


def _apply_risk_review_payloads(
    impact_preview: ReviewDecisionImpactPreview,
) -> list[dict[str, Any]]:
    manual_record = _manual_apply_preview_record(impact_preview)
    manual_decision = ManualApplyEligibilityGate().evaluate(manual_record)
    risk_assessment = ApplyExecutorRiskAssessment(
        preview_id=manual_record.preview_id,
        decision_id=manual_record.decision_id,
        candidate_kind=manual_record.candidate_kind,
        candidate_id=manual_record.candidate_id,
        safe_summary="[SYNTHETIC] Assess future persona apply executor risk.",
        risk_factors=[
            ApplyExecutorRiskFactor(
                risk_code="persona_drift",
                severity="medium",
                safe_summary="[SYNTHETIC] Persona drift risk is bounded by review.",
            )
        ],
        approval_gates=[
            ApplyExecutorRiskApprovalGate(
                gate_code="final_human_confirmation",
                label="Final human confirmation",
                safe_summary="[SYNTHETIC] Final confirmation is present.",
                satisfied=True,
            )
        ],
        rollback_requirements=[
            ApplyExecutorRollbackRequirement(
                requirement_code="previous_persona_version_available",
                safe_summary="[SYNTHETIC] Previous persona version is available.",
                covered=True,
            )
        ],
        audit_requirements=[
            ApplyExecutorAuditRequirement(
                event_code="manual_apply_audit_record",
                safe_summary="[SYNTHETIC] Audit record fields are ready.",
                covered=True,
            )
        ],
    )
    approval_decision = ApplyExecutorApprovalDecisionGate().evaluate(
        risk_assessment,
        manual_eligibility=manual_decision,
        required_approval_gate_codes=["final_human_confirmation"],
    )
    return [_safe_apply_risk_review_card(risk_assessment, approval_decision)]


def _safe_manual_apply_preview_card(
    record: ManualApplyPreviewRecord,
    decision: ManualApplyEligibilityDecision,
) -> dict[str, Any]:
    tone = "eligible" if decision.eligibility_outcome == "eligible" else "blocked"
    return {
        "schema_version": "review_workspace_manual_apply_preview_card_v1",
        "card_kind": "manual_apply_preview",
        "title": "Manual apply preview",
        "display_label": record.candidate_kind.replace("_", " "),
        "safe_summary": record.safe_summary,
        "filter_keys": ["all", "eligible", "persona"],
        "status_badges": [
            {
                "label": f"Manual apply preview {decision.eligibility_outcome}",
                "tone": tone,
                "issue_codes": list(decision.issue_codes),
                "blocking_issue_codes": list(decision.blocking_issue_codes),
                "review_required": True,
                "preview_only": True,
                "changes_state": False,
                "runtime_ready": False,
            }
        ],
        "eligibility_outcome": decision.eligibility_outcome,
        "manual_apply_preview_eligible": record.manual_apply_preview_eligible,
        "required_gates": [
            {
                "gate_code": gate.gate_code,
                "label": gate.label,
                "safe_summary": gate.safe_summary,
                "satisfied": gate.satisfied,
                "blocking_issue_codes": list(gate.blocking_issue_codes),
            }
            for gate in record.required_gates
        ],
        "effects": [
            {
                "effect_kind": effect.effect_kind,
                "target_ref": effect.target_ref,
                "safe_summary": effect.safe_summary,
                "artifact_ids": list(effect.artifact_ids),
                "rollback_notes": list(effect.rollback_notes),
            }
            for effect in record.effects
        ],
        "rollback_notes": list(record.rollback_notes),
        "issue_codes": list(decision.issue_codes),
        "blocking_issue_codes": list(decision.blocking_issue_codes),
        "review_required": True,
        "preview_only": True,
        "changes_state": False,
        "runtime_ready": False,
    }


def _safe_apply_risk_review_card(
    assessment: ApplyExecutorRiskAssessment,
    decision: ApplyExecutorApprovalDecision,
) -> dict[str, Any]:
    tone = {
        "blocked": "blocked",
        "needs_review": "review",
        "ready_for_separately_scoped_executor_design": "eligible",
    }[decision.final_outcome]
    return {
        "schema_version": "review_workspace_apply_risk_card_v1",
        "card_kind": "apply_risk_review",
        "title": "Apply risk review",
        "display_label": decision.candidate_kind.replace("_", " "),
        "safe_summary": decision.safe_summary,
        "filter_keys": ["all", tone, "persona"],
        "status_badges": [
            {
                "label": f"Apply risk {decision.final_outcome}",
                "tone": tone,
                "issue_codes": list(decision.issue_codes),
                "blocking_issue_codes": list(decision.blocking_issue_codes),
                "review_required": True,
                "preview_only": True,
                "changes_state": False,
                "runtime_ready": False,
            }
        ],
        "assessment_id": assessment.assessment_id,
        "approval_id": decision.approval_id,
        "preview_id": decision.preview_id,
        "decision_id": decision.decision_id,
        "candidate_kind": decision.candidate_kind,
        "candidate_id": decision.candidate_id,
        "risk_recommendation": decision.risk_recommendation,
        "final_outcome": decision.final_outcome,
        "manual_eligibility_outcome": decision.manual_eligibility_outcome,
        "risk_factors": [
            {
                "risk_code": factor.risk_code,
                "severity": factor.severity,
                "safe_summary": factor.safe_summary,
            }
            for factor in assessment.risk_factors
        ],
        "required_approval_gate_codes": list(decision.required_approval_gate_codes),
        "satisfied_approval_gate_codes": list(decision.satisfied_approval_gate_codes),
        "missing_approval_gate_codes": list(decision.missing_approval_gate_codes),
        "stale_reasons": list(decision.stale_reasons),
        "issue_codes": list(decision.issue_codes),
        "blocking_issue_codes": list(decision.blocking_issue_codes),
        "review_required": True,
        "preview_only": True,
        "risk_assessment_only": True,
        "executor_ready": False,
        "changes_state": False,
        "runtime_ready": False,
    }
