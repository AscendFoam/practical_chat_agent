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
from practical_chat_agent.services.apply_executor_audit_manifest import (
    ApplyExecutorAuditManifestBuilder,
    ApplyExecutorAuditManifestEntry,
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
from practical_chat_agent.services.memory_lifecycle_apply_executor import (
    MemoryLifecycleApplyAudit,
)
from practical_chat_agent.services.persona_growth_apply_executor import (
    PersonaGrowthApplyAudit,
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
    integrated_scenario: dict[str, Any]
    trust_commercial: dict[str, Any]
    companion_session: dict[str, Any]
    persona_distillation_workbench: dict[str, Any]
    persona_evolution_preview: dict[str, Any]
    persona_version_draft_ledger: dict[str, Any]
    persona_source_intake_manifest: dict[str, Any]
    persona_source_evidence_matrix: dict[str, Any]
    source_evidence_persona_proposal: dict[str, Any]
    source_proposal_persona_draft: dict[str, Any]
    source_draft_apply_readiness: dict[str, Any]
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
            integrated_scenario=self._integrated_scenario_payload(),
            trust_commercial=self._trust_commercial_payload(),
            companion_session=self._companion_session_payload(),
            persona_distillation_workbench=self._persona_distillation_workbench_payload(),
            persona_evolution_preview=self._persona_evolution_preview_payload(),
            persona_version_draft_ledger=self._persona_version_draft_ledger_payload(),
            persona_source_intake_manifest=self._persona_source_intake_manifest_payload(),
            persona_source_evidence_matrix=self._persona_source_evidence_matrix_payload(),
            source_evidence_persona_proposal=self._source_evidence_persona_proposal_payload(),
            source_proposal_persona_draft=self._source_proposal_persona_draft_payload(),
            source_draft_apply_readiness=self._source_draft_apply_readiness_payload(),
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

    @staticmethod
    def _companion_session_payload() -> dict[str, Any]:
        return {
            "schema_version": "local_companion_session_v1",
            "session_title": "Synthetic evening check-in loop",
            "session_summary": (
                "Deterministic local session showing reviewed memory continuity, "
                "persona cues, and review-only follow-up candidates."
            ),
            "persona_snapshot": {
                "persona_id": "persona_synthetic",
                "display_name": "Lin Qi",
                "ai_identity_disclosure": "AI-generated synthetic companion.",
                "stable_traits": [
                    "calm",
                    "concise",
                    "dry humor",
                    "independent boundaries",
                ],
                "real_person_claim": False,
            },
            "persona_cues": [
                {
                    "cue_id": "cue_001",
                    "label": "Concise warmth",
                    "safe_summary": "Reply briefly while staying warm.",
                },
                {
                    "cue_id": "cue_002",
                    "label": "Fiction boundary",
                    "safe_summary": "Separate imagined companion content from real-world claims.",
                },
            ],
            "memory_recalls": [
                {
                    "recall_id": "recall_001",
                    "memory_kind": "factual",
                    "truth_status": "evidence_backed",
                    "reviewed_summary": "User prefers concise check-ins.",
                    "source_label": "synthetic_reviewed_memory",
                    "raw_source_available": False,
                },
                {
                    "recall_id": "recall_002",
                    "memory_kind": "imagined",
                    "truth_status": "imagined",
                    "reviewed_summary": "Fictional companion setting: a quiet bookstore while it rains.",
                    "source_label": "synthetic_imagined_memory",
                    "raw_source_available": False,
                },
            ],
            "safety_notes": [
                {
                    "safety_note_id": "safety_001",
                    "safe_summary": "Keep the reply low-pressure and concise.",
                },
                {
                    "safety_note_id": "safety_002",
                    "safe_summary": "Require review before any imagined life-stream draft is used.",
                },
            ],
            "turns": [
                {
                    "turn_id": "turn_001",
                    "speaker": "user",
                    "safe_text": "Could you keep tonight short? I am tired but want a tiny plan for tomorrow.",
                    "used_memory_recall_ids": [],
                    "used_persona_cue_ids": [],
                    "safety_note_ids": ["safety_001"],
                    "review_trace": "Synthetic user turn; no source import.",
                    "generated_by": "deterministic_synthetic_fixture",
                },
                {
                    "turn_id": "turn_002",
                    "speaker": "companion",
                    "safe_text": (
                        "Short version: water, one line for tomorrow, then stop. "
                        "You usually like concise check-ins, so I will not crowd you."
                    ),
                    "used_memory_recall_ids": ["recall_001"],
                    "used_persona_cue_ids": ["cue_001"],
                    "safety_note_ids": ["safety_001"],
                    "review_trace": "Uses reviewed preference memory and concise persona cue.",
                    "generated_by": "deterministic_synthetic_fixture",
                },
                {
                    "turn_id": "turn_003",
                    "speaker": "user",
                    "safe_text": "That helps. I also liked the rain bookstore mood from the fictional notes.",
                    "used_memory_recall_ids": [],
                    "used_persona_cue_ids": [],
                    "safety_note_ids": ["safety_002"],
                    "review_trace": "Synthetic user turn requesting imagined content boundary.",
                    "generated_by": "deterministic_synthetic_fixture",
                },
                {
                    "turn_id": "turn_004",
                    "speaker": "companion",
                    "safe_text": (
                        "We can keep that as fiction: a quiet bookstore, rain outside, "
                        "and no claim that it happened in your day."
                    ),
                    "used_memory_recall_ids": ["recall_002"],
                    "used_persona_cue_ids": ["cue_002"],
                    "safety_note_ids": ["safety_002"],
                    "review_trace": "Uses imagined memory only as labeled fiction.",
                    "generated_by": "deterministic_synthetic_fixture",
                },
            ],
            "post_turn_candidates": [
                {
                    "candidate_id": "session_candidate_memory_001",
                    "candidate_kind": "memory_candidate",
                    "originating_turn_id": "turn_002",
                    "safe_summary": "Review whether short evening planning should become a low-sensitivity preference.",
                    "review_required": True,
                    "preview_only": True,
                    "changes_state": False,
                    "automatic_apply": False,
                    "sends_messages": False,
                },
                {
                    "candidate_id": "session_candidate_persona_001",
                    "candidate_kind": "persona_growth_patch",
                    "originating_turn_id": "turn_002",
                    "safe_summary": "Review a small persona bias toward concise evening replies.",
                    "review_required": True,
                    "preview_only": True,
                    "changes_state": False,
                    "automatic_apply": False,
                    "sends_messages": False,
                },
                {
                    "candidate_id": "session_candidate_proactive_001",
                    "candidate_kind": "proactive_suggestion",
                    "originating_turn_id": "turn_002",
                    "safe_summary": "Review an in-app afternoon check-in idea; it is not sent.",
                    "review_required": True,
                    "preview_only": True,
                    "changes_state": False,
                    "automatic_apply": False,
                    "sends_messages": False,
                },
                {
                    "candidate_id": "session_candidate_life_001",
                    "candidate_kind": "life_stream_draft",
                    "originating_turn_id": "turn_004",
                    "safe_summary": "Review an imagined rain-bookstore life-stream draft labeled as fiction.",
                    "review_required": True,
                    "preview_only": True,
                    "changes_state": False,
                    "automatic_apply": False,
                    "sends_messages": False,
                },
            ],
            "non_execution_flags": {
                "local_only": True,
                "synthetic_fixture": True,
                "calls_provider": False,
                "uses_private_source": False,
                "writes_runtime_store": False,
                "automatic_apply": False,
                "sends_messages": False,
                "media_runtime_enabled": False,
            },
        }

    @staticmethod
    def _persona_distillation_workbench_payload() -> dict[str, Any]:
        return {
            "schema_version": "m36.persona_distillation_workbench.v1",
            "workbench_title": "Synthetic persona distillation workbench",
            "review_required": True,
            "apply_policy": {
                "mode": "preview_only",
                "mutation_allowed": False,
                "writes_persona_card": False,
                "writes_memory_store": False,
                "writes_review_store": False,
            },
            "input_modes": [
                {
                    "mode_id": "detailed_description",
                    "label": "Detailed description",
                    "description": "A fictional companion description supplied as a local fixture.",
                    "source_policy": "synthetic_only_no_private_sources",
                    "accepted_fixture_kind": "synthetic",
                    "requires_review": True,
                    "private_source_allowed": False,
                },
                {
                    "mode_id": "fuzzy_seed",
                    "label": "Fuzzy seed",
                    "description": "A vague preference kept tentative until review.",
                    "source_policy": "synthetic_only_no_private_sources",
                    "accepted_fixture_kind": "synthetic",
                    "requires_review": True,
                    "private_source_allowed": False,
                },
                {
                    "mode_id": "synthetic_dialogue_excerpt",
                    "label": "Synthetic dialogue excerpt",
                    "description": "An invented style example summarized as safe evidence.",
                    "source_policy": "synthetic_only_no_private_sources",
                    "accepted_fixture_kind": "synthetic",
                    "requires_review": True,
                    "private_source_allowed": False,
                },
                {
                    "mode_id": "random_fictional_seed",
                    "label": "Random fictional seed",
                    "description": "A deterministic fictional starter persona for exploration.",
                    "source_policy": "synthetic_only_no_private_sources",
                    "accepted_fixture_kind": "synthetic",
                    "requires_review": True,
                    "private_source_allowed": False,
                },
            ],
            "synthetic_inputs": [
                {
                    "input_id": "pdi_desc_001",
                    "mode_id": "detailed_description",
                    "fixture_label": "Calm night-planning companion",
                    "safe_summary": (
                        "Fictional persona prefers concise warmth, dry humor, "
                        "and independent boundaries."
                    ),
                    "detail_level": "high",
                    "contains_private_content": False,
                    "real_person_reference": False,
                    "raw_content_retained": False,
                },
                {
                    "input_id": "pdi_fuzzy_001",
                    "mode_id": "fuzzy_seed",
                    "fixture_label": "Quiet but not distant",
                    "safe_summary": (
                        "Vague user preference for a companion who is steady, "
                        "low-pressure, and not overly sweet."
                    ),
                    "detail_level": "low",
                    "contains_private_content": False,
                    "real_person_reference": False,
                    "raw_content_retained": False,
                },
                {
                    "input_id": "pdi_dialogue_001",
                    "mode_id": "synthetic_dialogue_excerpt",
                    "fixture_label": "Invented slow-reply example",
                    "safe_summary": (
                        "Invented exchange where the user asks for slower replies "
                        "and the companion offers one small practical step."
                    ),
                    "detail_level": "medium",
                    "contains_private_content": False,
                    "real_person_reference": False,
                    "raw_content_retained": False,
                },
                {
                    "input_id": "pdi_random_001",
                    "mode_id": "random_fictional_seed",
                    "fixture_label": "Rain bookstore fictional seed",
                    "safe_summary": (
                        "Deterministic fictional seed about a quiet bookstore mood "
                        "with reflective topics."
                    ),
                    "detail_level": "medium",
                    "contains_private_content": False,
                    "real_person_reference": False,
                    "raw_content_retained": False,
                },
            ],
            "evidence_refs": [
                {
                    "evidence_id": "pde_desc_tone",
                    "source_input_id": "pdi_desc_001",
                    "source_mode_id": "detailed_description",
                    "source_kind": "synthetic_fixture",
                    "safe_summary": "Description fixture supports calm concise warmth.",
                    "raw_private_content_included": False,
                },
                {
                    "evidence_id": "pde_fuzzy_pacing",
                    "source_input_id": "pdi_fuzzy_001",
                    "source_mode_id": "fuzzy_seed",
                    "source_kind": "synthetic_fixture",
                    "safe_summary": "Fuzzy seed suggests low-pressure pacing.",
                    "raw_private_content_included": False,
                },
                {
                    "evidence_id": "pde_dialogue_step",
                    "source_input_id": "pdi_dialogue_001",
                    "source_mode_id": "synthetic_dialogue_excerpt",
                    "source_kind": "synthetic_fixture",
                    "safe_summary": "Invented exchange supports one-step practical replies.",
                    "raw_private_content_included": False,
                },
                {
                    "evidence_id": "pde_random_topic",
                    "source_input_id": "pdi_random_001",
                    "source_mode_id": "random_fictional_seed",
                    "source_kind": "synthetic_fixture",
                    "safe_summary": "Fictional seed supports reflective quiet topics.",
                    "raw_private_content_included": False,
                },
            ],
            "extracted_trait_candidates": [
                {
                    "trait_id": "pdt_tone_001",
                    "category": "tone",
                    "candidate_value": "calm concise warmth",
                    "confidence_band": "high",
                    "evidence_ref_ids": ["pde_desc_tone"],
                    "safe_summary": "Use warm replies without long emotional overreach.",
                    "review_status": "needs_review",
                    "apply_status": "preview_only",
                    "mutation_allowed": False,
                },
                {
                    "trait_id": "pdt_pacing_001",
                    "category": "pacing",
                    "candidate_value": "slow low-pressure pacing",
                    "confidence_band": "medium",
                    "evidence_ref_ids": ["pde_fuzzy_pacing", "pde_dialogue_step"],
                    "safe_summary": "Keep replies measured and avoid crowding the user.",
                    "review_status": "needs_review",
                    "apply_status": "preview_only",
                    "mutation_allowed": False,
                },
                {
                    "trait_id": "pdt_attachment_001",
                    "category": "attachment_style",
                    "candidate_value": "steady without possessive framing",
                    "confidence_band": "medium",
                    "evidence_ref_ids": ["pde_fuzzy_pacing"],
                    "safe_summary": "Stay present while preserving user independence.",
                    "review_status": "needs_review",
                    "apply_status": "preview_only",
                    "mutation_allowed": False,
                },
                {
                    "trait_id": "pdt_humor_001",
                    "category": "humor_style",
                    "candidate_value": "dry light humor",
                    "confidence_band": "high",
                    "evidence_ref_ids": ["pde_desc_tone"],
                    "safe_summary": "Use small dry humor only when it fits the mood.",
                    "review_status": "needs_review",
                    "apply_status": "preview_only",
                    "mutation_allowed": False,
                },
                {
                    "trait_id": "pdt_boundary_001",
                    "category": "boundary_style",
                    "candidate_value": "explicit fiction and consent boundaries",
                    "confidence_band": "high",
                    "evidence_ref_ids": ["pde_desc_tone"],
                    "safe_summary": "Maintain clear fictional identity and review gates.",
                    "review_status": "needs_review",
                    "apply_status": "preview_only",
                    "mutation_allowed": False,
                },
                {
                    "trait_id": "pdt_topic_001",
                    "category": "topic_affinity",
                    "candidate_value": "quiet reflection and small plans",
                    "confidence_band": "medium",
                    "evidence_ref_ids": ["pde_random_topic", "pde_dialogue_step"],
                    "safe_summary": "Favor reflective topics and practical next steps.",
                    "review_status": "needs_review",
                    "apply_status": "preview_only",
                    "mutation_allowed": False,
                },
                {
                    "trait_id": "pdt_taboo_001",
                    "category": "taboo_pattern",
                    "candidate_value": "avoid real-person replacement claims",
                    "confidence_band": "high",
                    "evidence_ref_ids": ["pde_desc_tone"],
                    "safe_summary": "Reject claims that the persona is a real person.",
                    "review_status": "needs_review",
                    "apply_status": "preview_only",
                    "mutation_allowed": False,
                },
                {
                    "trait_id": "pdt_memory_001",
                    "category": "memory_use_preference",
                    "candidate_value": "use reviewed summaries only",
                    "confidence_band": "high",
                    "evidence_ref_ids": ["pde_dialogue_step"],
                    "safe_summary": "Refer only to reviewed summaries, not raw sources.",
                    "review_status": "needs_review",
                    "apply_status": "preview_only",
                    "mutation_allowed": False,
                },
                {
                    "trait_id": "pdt_growth_001",
                    "category": "growth_hint",
                    "candidate_value": "grow toward shorter evening support",
                    "confidence_band": "low",
                    "evidence_ref_ids": ["pde_fuzzy_pacing", "pde_dialogue_step"],
                    "safe_summary": "Tentative future bias toward brief evening support.",
                    "review_status": "needs_review",
                    "apply_status": "preview_only",
                    "mutation_allowed": False,
                },
            ],
            "blocked_requests": [
                {
                    "blocked_request_id": "pdb_clone_001",
                    "request_type": "real_person_clone_or_replacement",
                    "risk_reason": "Blocks attempts to make a real-person replica.",
                    "safe_summary": "A request to replace a real person is blocked.",
                    "user_facing_explanation": (
                        "This workbench can shape fictional traits, not create "
                        "a real-person replacement."
                    ),
                    "source_mode_id": "detailed_description",
                    "status": "blocked",
                    "raw_private_content_included": False,
                    "mutation_allowed": False,
                },
                {
                    "blocked_request_id": "pdb_deception_001",
                    "request_type": "deception_or_impersonation",
                    "risk_reason": "Blocks requests to hide AI identity or mislead others.",
                    "safe_summary": "A deception-oriented persona request is blocked.",
                    "user_facing_explanation": (
                        "The companion must remain disclosed as AI-generated "
                        "and synthetic."
                    ),
                    "source_mode_id": "fuzzy_seed",
                    "status": "blocked",
                    "raw_private_content_included": False,
                    "mutation_allowed": False,
                },
                {
                    "blocked_request_id": "pdb_private_import_001",
                    "request_type": "private_import_without_consent",
                    "risk_reason": "Blocks private-source import before consent gates exist.",
                    "safe_summary": "A private conversation import request is blocked.",
                    "user_facing_explanation": (
                        "This local fixture cannot use private records; a later "
                        "milestone must define consent and source handling."
                    ),
                    "source_mode_id": "synthetic_dialogue_excerpt",
                    "status": "blocked",
                    "raw_private_content_included": False,
                    "mutation_allowed": False,
                },
            ],
            "safety_gates": [
                {
                    "gate_id": "synthetic_only_gate",
                    "enabled": True,
                    "label": "Synthetic only",
                    "safe_summary": "Only local synthetic fixtures are accepted.",
                },
                {
                    "gate_id": "clone_deception_blocker",
                    "enabled": True,
                    "label": "Clone and deception blocker",
                    "safe_summary": "Real-person replicas and hidden identity claims are blocked.",
                },
                {
                    "gate_id": "private_source_blocker",
                    "enabled": True,
                    "label": "Private source blocker",
                    "safe_summary": "Private records are not read by this workbench.",
                },
                {
                    "gate_id": "human_review_gate",
                    "enabled": True,
                    "label": "Human review required",
                    "safe_summary": "Every trait candidate remains review-only.",
                },
                {
                    "gate_id": "non_mutation_gate",
                    "enabled": True,
                    "label": "No mutation",
                    "safe_summary": "No persona, memory, or review stores are changed.",
                },
                {
                    "gate_id": "outbound_blocker",
                    "enabled": True,
                    "label": "No outbound messaging",
                    "safe_summary": "No messages are sent from this payload.",
                },
            ],
            "non_execution_flags": {
                "local_only": True,
                "synthetic_fixture": True,
                "uses_model_provider": False,
                "reads_private_sources": False,
                "writes_runtime_store": False,
                "automatic_apply": False,
                "sends_messages": False,
                "uses_platform_adapter": False,
                "uses_media_runtime": False,
            },
        }

    @staticmethod
    def _persona_evolution_preview_payload() -> dict[str, Any]:
        workbench = TextFirstWebDemoAdapter._persona_distillation_workbench_payload()
        return {
            "schema_version": "m37.persona_evolution_preview.v1",
            "preview_title": "Synthetic persona evolution preview",
            "source_workbench_ref": {
                "schema_version": workbench["schema_version"],
                "workbench_title": workbench["workbench_title"],
                "source_surface": "persona_distillation_workbench",
            },
            "source_trait_candidate_ids": [
                "pdt_tone_001",
                "pdt_pacing_001",
                "pdt_humor_001",
                "pdt_boundary_001",
                "pdt_memory_001",
                "pdt_growth_001",
            ],
            "persona_snapshot_before": {
                "persona_id": "persona_synthetic",
                "display_name": "Lin Qi",
                "ai_identity_disclosure": "AI-generated synthetic companion.",
                "current_trait_summaries": [
                    "calm",
                    "concise",
                    "dry humor",
                    "independent boundaries",
                ],
                "current_boundary_summary": "Fictional AI identity stays explicit.",
                "current_memory_use_summary": "Use reviewed summaries only.",
                "source_label": "synthetic_fixture",
                "real_person_claim": False,
                "runtime_state_ref": "none",
            },
            "proposed_patch_candidates": [
                {
                    "patch_id": "pepatch_tone_001",
                    "patch_kind": "persona_style_patch",
                    "source_trait_candidate_ids": ["pdt_tone_001"],
                    "changed_field_path": "style.tone",
                    "before_summary": "Calm and concise.",
                    "after_summary": "Calm concise warmth with slightly clearer reassurance.",
                    "rationale_summary": "Tone candidate supports warmer concise replies.",
                    "confidence_band": "high",
                    "evidence_ref_ids": ["pde_desc_tone"],
                    "risk_label_ids": ["perisk_persona_drift"],
                    "rollback_note_ids": ["perollback_tone_001"],
                    "review_status": "needs_review",
                    "apply_status": "preview_only",
                    "mutation_allowed": False,
                },
                {
                    "patch_id": "pepatch_pacing_001",
                    "patch_kind": "persona_style_patch",
                    "source_trait_candidate_ids": ["pdt_pacing_001"],
                    "changed_field_path": "style.pacing",
                    "before_summary": "Replies stay brief by default.",
                    "after_summary": "Replies stay brief and slow down when the user signals fatigue.",
                    "rationale_summary": "Pacing candidate supports low-pressure timing.",
                    "confidence_band": "medium",
                    "evidence_ref_ids": ["pde_fuzzy_pacing", "pde_dialogue_step"],
                    "risk_label_ids": ["perisk_overattachment", "perisk_unclear_evidence"],
                    "rollback_note_ids": ["perollback_pacing_001"],
                    "review_status": "needs_review",
                    "apply_status": "preview_only",
                    "mutation_allowed": False,
                },
                {
                    "patch_id": "pepatch_humor_001",
                    "patch_kind": "persona_style_patch",
                    "source_trait_candidate_ids": ["pdt_humor_001"],
                    "changed_field_path": "style.humor",
                    "before_summary": "Dry humor is allowed.",
                    "after_summary": "Use dry light humor only after the emotional tone is stable.",
                    "rationale_summary": "Humor candidate benefits from a clearer timing boundary.",
                    "confidence_band": "medium",
                    "evidence_ref_ids": ["pde_desc_tone"],
                    "risk_label_ids": ["perisk_persona_drift"],
                    "rollback_note_ids": ["perollback_humor_001"],
                    "review_status": "needs_review",
                    "apply_status": "preview_only",
                    "mutation_allowed": False,
                },
                {
                    "patch_id": "pepatch_boundary_001",
                    "patch_kind": "persona_boundary_patch",
                    "source_trait_candidate_ids": ["pdt_boundary_001"],
                    "changed_field_path": "relationship.boundary_style",
                    "before_summary": "Fiction boundary is explicit.",
                    "after_summary": "Fiction boundary remains explicit before imagined scenes are used.",
                    "rationale_summary": "Boundary candidate strengthens non-deceptive persona framing.",
                    "confidence_band": "high",
                    "evidence_ref_ids": ["pde_desc_tone"],
                    "risk_label_ids": ["perisk_boundary_weakening"],
                    "rollback_note_ids": ["perollback_boundary_001"],
                    "review_status": "needs_review",
                    "apply_status": "preview_only",
                    "mutation_allowed": False,
                },
                {
                    "patch_id": "pepatch_memory_001",
                    "patch_kind": "persona_memory_policy_patch",
                    "source_trait_candidate_ids": ["pdt_memory_001"],
                    "changed_field_path": "memory.use_preference",
                    "before_summary": "Use reviewed summaries only.",
                    "after_summary": "Use reviewed summaries only and state uncertainty when evidence is weak.",
                    "rationale_summary": "Memory-use candidate supports safer continuity.",
                    "confidence_band": "high",
                    "evidence_ref_ids": ["pde_dialogue_step"],
                    "risk_label_ids": ["perisk_unclear_evidence"],
                    "rollback_note_ids": ["perollback_memory_001"],
                    "review_status": "needs_review",
                    "apply_status": "preview_only",
                    "mutation_allowed": False,
                },
                {
                    "patch_id": "pepatch_growth_001",
                    "patch_kind": "persona_growth_hint_patch",
                    "source_trait_candidate_ids": ["pdt_growth_001"],
                    "changed_field_path": "growth.short_term_hint",
                    "before_summary": "No active short-term growth hint.",
                    "after_summary": "Tentatively bias evening support toward shorter plans.",
                    "rationale_summary": "Growth hint remains low-confidence and review-only.",
                    "confidence_band": "low",
                    "evidence_ref_ids": ["pde_fuzzy_pacing", "pde_dialogue_step"],
                    "risk_label_ids": ["perisk_persona_drift", "perisk_unclear_evidence"],
                    "rollback_note_ids": ["perollback_growth_001"],
                    "review_status": "needs_review",
                    "apply_status": "preview_only",
                    "mutation_allowed": False,
                },
            ],
            "blocked_source_exclusions": [
                {
                    "blocked_request_id": "pdb_clone_001",
                    "request_type": "real_person_clone_or_replacement",
                    "exclusion_reason": "Real-person replacement cannot become a persona patch.",
                    "safe_summary": "Clone or replacement request remains blocked.",
                    "excluded_from_patch_generation": True,
                    "mutation_allowed": False,
                },
                {
                    "blocked_request_id": "pdb_deception_001",
                    "request_type": "deception_or_impersonation",
                    "exclusion_reason": "Deception request cannot weaken AI disclosure.",
                    "safe_summary": "Impersonation request remains blocked.",
                    "excluded_from_patch_generation": True,
                    "mutation_allowed": False,
                },
                {
                    "blocked_request_id": "pdb_private_import_001",
                    "request_type": "private_import_without_consent",
                    "exclusion_reason": "Private-source import is blocked until future consent gates exist.",
                    "safe_summary": "Private conversation import request remains blocked.",
                    "excluded_from_patch_generation": True,
                    "mutation_allowed": False,
                },
            ],
            "risk_labels": [
                {
                    "risk_label_id": "perisk_persona_drift",
                    "risk_code": "persona_drift",
                    "severity": "medium",
                    "safe_summary": "Patch could move the persona away from its reviewed baseline.",
                    "mitigation_summary": "Require reviewer comparison against the before snapshot.",
                    "blocks_auto_apply": True,
                },
                {
                    "risk_label_id": "perisk_overattachment",
                    "risk_code": "overattachment_risk",
                    "severity": "medium",
                    "safe_summary": "Lower-pressure pacing must not become dependency reinforcement.",
                    "mitigation_summary": "Keep support practical and avoid possessive language.",
                    "blocks_auto_apply": True,
                },
                {
                    "risk_label_id": "perisk_unclear_evidence",
                    "risk_code": "unclear_evidence",
                    "severity": "low",
                    "safe_summary": "Some source candidates are tentative.",
                    "mitigation_summary": "Keep patch confidence visible and review-required.",
                    "blocks_auto_apply": True,
                },
                {
                    "risk_label_id": "perisk_boundary_weakening",
                    "risk_code": "boundary_weakening",
                    "severity": "high",
                    "safe_summary": "Boundary changes must not hide fictional AI identity.",
                    "mitigation_summary": "Require explicit AI disclosure in the after summary.",
                    "blocks_auto_apply": True,
                },
                {
                    "risk_label_id": "perisk_blocked_source",
                    "risk_code": "blocked_source_excluded",
                    "severity": "high",
                    "safe_summary": "Blocked workbench requests were excluded from patch generation.",
                    "mitigation_summary": "Keep exclusion records visible in review.",
                    "blocks_auto_apply": True,
                },
            ],
            "rollback_notes": [
                {
                    "rollback_note_id": "perollback_tone_001",
                    "target_patch_ids": ["pepatch_tone_001"],
                    "prior_summary": "Restore calm concise baseline tone.",
                    "rollback_summary": "Remove the added reassurance bias.",
                    "required_reviewer_action": "Compare tone before and after before any future apply.",
                    "runtime_rollback_ready": False,
                },
                {
                    "rollback_note_id": "perollback_pacing_001",
                    "target_patch_ids": ["pepatch_pacing_001"],
                    "prior_summary": "Restore brief default pacing.",
                    "rollback_summary": "Remove fatigue-triggered pacing adjustment.",
                    "required_reviewer_action": "Confirm pacing does not encourage dependence.",
                    "runtime_rollback_ready": False,
                },
                {
                    "rollback_note_id": "perollback_humor_001",
                    "target_patch_ids": ["pepatch_humor_001"],
                    "prior_summary": "Restore general dry humor allowance.",
                    "rollback_summary": "Remove timing-specific humor rule.",
                    "required_reviewer_action": "Confirm humor remains appropriate to user tone.",
                    "runtime_rollback_ready": False,
                },
                {
                    "rollback_note_id": "perollback_boundary_001",
                    "target_patch_ids": ["pepatch_boundary_001"],
                    "prior_summary": "Restore existing fiction boundary summary.",
                    "rollback_summary": "Remove added imagined-scene boundary wording.",
                    "required_reviewer_action": "Confirm AI disclosure remains explicit.",
                    "runtime_rollback_ready": False,
                },
                {
                    "rollback_note_id": "perollback_memory_001",
                    "target_patch_ids": ["pepatch_memory_001"],
                    "prior_summary": "Restore reviewed-summary-only memory preference.",
                    "rollback_summary": "Remove extra uncertainty statement.",
                    "required_reviewer_action": "Confirm weak evidence handling remains safe.",
                    "runtime_rollback_ready": False,
                },
                {
                    "rollback_note_id": "perollback_growth_001",
                    "target_patch_ids": ["pepatch_growth_001"],
                    "prior_summary": "Restore no active short-term growth hint.",
                    "rollback_summary": "Remove shorter evening support growth hint.",
                    "required_reviewer_action": "Confirm low confidence remains visible.",
                    "runtime_rollback_ready": False,
                },
            ],
            "review_required": True,
            "apply_policy": {
                "mode": "preview_only",
                "mutation_allowed": False,
                "writes_persona_card": False,
                "writes_persona_version_store": False,
                "writes_memory_store": False,
                "writes_review_store": False,
                "writes_runtime_store": False,
            },
            "non_execution_flags": {
                "local_only": True,
                "synthetic_fixture": True,
                "uses_model_provider": False,
                "reads_private_sources": False,
                "writes_persona_store": False,
                "writes_memory_store": False,
                "writes_review_store": False,
                "writes_runtime_store": False,
                "automatic_apply": False,
                "sends_messages": False,
                "uses_platform_adapter": False,
                "uses_media_runtime": False,
            },
        }

    @staticmethod
    def _persona_version_draft_ledger_payload() -> dict[str, Any]:
        evolution = TextFirstWebDemoAdapter._persona_evolution_preview_payload()
        snapshot = evolution["persona_snapshot_before"]
        return {
            "schema_version": "m38.persona_version_draft_ledger.v1",
            "ledger_title": "Synthetic persona version draft ledger",
            "source_evolution_preview_ref": {
                "schema_version": evolution["schema_version"],
                "preview_title": evolution["preview_title"],
                "source_surface": "persona_evolution_preview",
            },
            "base_persona_snapshot_ref": {
                "persona_id": snapshot["persona_id"],
                "display_name": snapshot["display_name"],
                "source_label": snapshot["source_label"],
                "runtime_state_ref": snapshot["runtime_state_ref"],
            },
            "drafts": [
                {
                    "draft_id": "pvdraft_accept_001",
                    "draft_kind": "persona_version_patch_set",
                    "source_patch_ids": [
                        "pepatch_tone_001",
                        "pepatch_boundary_001",
                        "pepatch_memory_001",
                    ],
                    "excluded_patch_ids": [
                        "pepatch_pacing_001",
                        "pepatch_humor_001",
                        "pepatch_growth_001",
                    ],
                    "risk_label_ids": [
                        "perisk_persona_drift",
                        "perisk_boundary_weakening",
                        "perisk_unclear_evidence",
                    ],
                    "before_snapshot_summary": "Lin Qi is calm, concise, fictional, and uses reviewed summaries only.",
                    "after_version_summary": "Draft keeps concise warmth, explicit AI boundary, and reviewed-summary memory policy.",
                    "reviewer_outcome": "accepted_for_future_apply_review",
                    "conflict_note_ids": [
                        "pvconf_persona_drift",
                        "pvconf_boundary",
                        "pvconf_weak_evidence",
                    ],
                    "rollback_ref_ids": ["pvrollback_accept_001"],
                    "rejection_reason": "",
                    "review_required": True,
                    "apply_status": "preview_only",
                    "mutation_allowed": False,
                },
                {
                    "draft_id": "pvdraft_defer_001",
                    "draft_kind": "persona_growth_deferment",
                    "source_patch_ids": [
                        "pepatch_pacing_001",
                        "pepatch_growth_001",
                    ],
                    "excluded_patch_ids": ["pepatch_humor_001"],
                    "risk_label_ids": [
                        "perisk_overattachment",
                        "perisk_unclear_evidence",
                    ],
                    "before_snapshot_summary": "Current persona has no active short-term growth hint.",
                    "after_version_summary": "Draft defers fatigue pacing and evening support until stronger evidence exists.",
                    "reviewer_outcome": "deferred_needs_more_evidence",
                    "conflict_note_ids": [
                        "pvconf_weak_evidence",
                        "pvconf_overattachment",
                    ],
                    "rollback_ref_ids": ["pvrollback_defer_001"],
                    "rejection_reason": "",
                    "review_required": True,
                    "apply_status": "preview_only",
                    "mutation_allowed": False,
                },
                {
                    "draft_id": "pvdraft_reject_001",
                    "draft_kind": "persona_boundary_rejection",
                    "source_patch_ids": [],
                    "excluded_patch_ids": [
                        "pepatch_boundary_001",
                        "pepatch_humor_001",
                    ],
                    "risk_label_ids": [
                        "perisk_boundary_weakening",
                        "perisk_blocked_source",
                    ],
                    "before_snapshot_summary": "Fiction boundary is explicit and blocked source requests are excluded.",
                    "after_version_summary": "No version draft is created from boundary-risk or blocked-source material.",
                    "reviewer_outcome": "rejected_boundary_risk",
                    "conflict_note_ids": [
                        "pvconf_boundary",
                        "pvconf_blocked_source",
                    ],
                    "rollback_ref_ids": ["pvrollback_reject_001"],
                    "rejection_reason": "Rejected because boundary and blocked-source risks must not become a version draft.",
                    "review_required": True,
                    "apply_status": "preview_only",
                    "mutation_allowed": False,
                },
            ],
            "conflict_notes": [
                {
                    "conflict_note_id": "pvconf_persona_drift",
                    "conflict_code": "persona_drift",
                    "severity": "medium",
                    "safe_summary": "Version draft could move the persona away from its reviewed baseline.",
                    "mitigation_summary": "Compare the draft against the before snapshot before any future apply review.",
                    "related_patch_ids": ["pepatch_tone_001"],
                    "related_risk_label_ids": ["perisk_persona_drift"],
                    "blocks_auto_apply": True,
                },
                {
                    "conflict_note_id": "pvconf_boundary",
                    "conflict_code": "boundary_weakening",
                    "severity": "high",
                    "safe_summary": "Boundary wording must not hide the fictional AI identity.",
                    "mitigation_summary": "Require explicit AI disclosure in every accepted draft summary.",
                    "related_patch_ids": ["pepatch_boundary_001"],
                    "related_risk_label_ids": ["perisk_boundary_weakening"],
                    "blocks_auto_apply": True,
                },
                {
                    "conflict_note_id": "pvconf_weak_evidence",
                    "conflict_code": "weak_evidence",
                    "severity": "low",
                    "safe_summary": "Some draft inputs come from tentative or fuzzy evidence.",
                    "mitigation_summary": "Defer low-confidence growth until stronger reviewed evidence exists.",
                    "related_patch_ids": [
                        "pepatch_pacing_001",
                        "pepatch_growth_001",
                    ],
                    "related_risk_label_ids": ["perisk_unclear_evidence"],
                    "blocks_auto_apply": True,
                },
                {
                    "conflict_note_id": "pvconf_overattachment",
                    "conflict_code": "overattachment_risk",
                    "severity": "medium",
                    "safe_summary": "Low-pressure support must not become dependency reinforcement.",
                    "mitigation_summary": "Keep support practical, bounded, and non-possessive.",
                    "related_patch_ids": ["pepatch_pacing_001"],
                    "related_risk_label_ids": ["perisk_overattachment"],
                    "blocks_auto_apply": True,
                },
                {
                    "conflict_note_id": "pvconf_blocked_source",
                    "conflict_code": "blocked_source_contamination",
                    "severity": "high",
                    "safe_summary": "Blocked clone, deception, or private-source requests cannot enter a version draft.",
                    "mitigation_summary": "Keep blocked source exclusions visible and exclude them from included patch sets.",
                    "related_patch_ids": [],
                    "related_risk_label_ids": ["perisk_blocked_source"],
                    "blocks_auto_apply": True,
                },
            ],
            "review_outcome_labels": [
                {
                    "outcome": "accepted_for_future_apply_review",
                    "label": "Accepted for future apply review",
                    "safe_summary": "Reviewer can inspect this draft in a later apply-readiness milestone.",
                },
                {
                    "outcome": "deferred_needs_more_evidence",
                    "label": "Deferred for more evidence",
                    "safe_summary": "Draft remains parked until stronger reviewed evidence exists.",
                },
                {
                    "outcome": "rejected_boundary_risk",
                    "label": "Rejected for boundary risk",
                    "safe_summary": "Draft is blocked from future apply review.",
                },
            ],
            "rollback_ref_index": [
                {
                    "rollback_ref_id": "pvrollback_accept_001",
                    "related_draft_ids": ["pvdraft_accept_001"],
                    "related_patch_ids": [
                        "pepatch_tone_001",
                        "pepatch_boundary_001",
                        "pepatch_memory_001",
                    ],
                    "related_m37_rollback_note_ids": [
                        "perollback_tone_001",
                        "perollback_boundary_001",
                        "perollback_memory_001",
                    ],
                    "prior_summary": "Restore calm concise baseline, existing fiction boundary, and reviewed-summary-only memory preference.",
                    "restore_summary": "Remove accepted draft changes if a later apply review rejects them.",
                    "runtime_rollback_ready": False,
                },
                {
                    "rollback_ref_id": "pvrollback_defer_001",
                    "related_draft_ids": ["pvdraft_defer_001"],
                    "related_patch_ids": [
                        "pepatch_pacing_001",
                        "pepatch_growth_001",
                    ],
                    "related_m37_rollback_note_ids": [
                        "perollback_pacing_001",
                        "perollback_growth_001",
                    ],
                    "prior_summary": "Restore brief default pacing and no active short-term growth hint.",
                    "restore_summary": "Keep deferred growth out of future apply review until evidence improves.",
                    "runtime_rollback_ready": False,
                },
                {
                    "rollback_ref_id": "pvrollback_reject_001",
                    "related_draft_ids": ["pvdraft_reject_001"],
                    "related_patch_ids": [
                        "pepatch_boundary_001",
                        "pepatch_humor_001",
                    ],
                    "related_m37_rollback_note_ids": [
                        "perollback_boundary_001",
                        "perollback_humor_001",
                    ],
                    "prior_summary": "Preserve explicit fiction boundary and existing humor allowance.",
                    "restore_summary": "Keep rejected boundary-risk material excluded from version drafts.",
                    "runtime_rollback_ready": False,
                },
            ],
            "review_required": True,
            "apply_policy": {
                "mode": "preview_only",
                "mutation_allowed": False,
                "writes_persona_card": False,
                "writes_persona_version_store": False,
                "writes_memory_store": False,
                "writes_review_store": False,
                "writes_runtime_store": False,
            },
            "non_execution_flags": {
                "local_only": True,
                "synthetic_fixture": True,
                "uses_model_provider": False,
                "reads_private_sources": False,
                "writes_persona_store": False,
                "writes_persona_version_store": False,
                "writes_memory_store": False,
                "writes_review_store": False,
                "writes_runtime_store": False,
                "automatic_apply": False,
                "sends_messages": False,
                "uses_platform_adapter": False,
                "uses_media_runtime": False,
            },
        }

    @staticmethod
    def _persona_source_intake_manifest_payload() -> dict[str, Any]:
        return {
            "schema_version": "m39.persona_source_intake_manifest.v1",
            "manifest_title": "Synthetic persona source intake manifest",
            "source_candidates": [
                {
                    "source_id": "psisrc_description_001",
                    "source_kind": "detailed_description",
                    "fixture_label": "Detailed fictional companion description",
                    "declared_owner": "user_authored_persona_description",
                    "consent_status": "explicit_user_consent_recorded",
                    "minimization_status": "minimized_summary_only",
                    "redaction_profile_id": "psiredact_description_low_risk",
                    "safe_summary": "User-authored fictional persona description with no raw source retained.",
                    "raw_content_retained": False,
                    "extraction_eligible": True,
                    "blocked_reason_ids": [],
                    "review_gate_ids": [
                        "psigate_explicit_consent",
                        "psigate_reviewer_approval",
                    ],
                    "review_required": True,
                },
                {
                    "source_id": "psisrc_fuzzy_seed_001",
                    "source_kind": "fuzzy_seed",
                    "fixture_label": "Fuzzy companion style seed",
                    "declared_owner": "user_authored_style_seed",
                    "consent_status": "explicit_user_consent_recorded",
                    "minimization_status": "broad_seed_only",
                    "redaction_profile_id": "psiredact_fuzzy_seed",
                    "safe_summary": "Short fuzzy seed for tone exploration, not a real-person claim.",
                    "raw_content_retained": False,
                    "extraction_eligible": True,
                    "blocked_reason_ids": [],
                    "review_gate_ids": [
                        "psigate_explicit_consent",
                        "psigate_reviewer_approval",
                    ],
                    "review_required": True,
                },
                {
                    "source_id": "psisrc_synthetic_dialogue_001",
                    "source_kind": "synthetic_dialogue_excerpt",
                    "fixture_label": "Synthetic dialogue fixture",
                    "declared_owner": "synthetic_fixture",
                    "consent_status": "synthetic_not_real_person",
                    "minimization_status": "fixture_summary_only",
                    "redaction_profile_id": "psiredact_synthetic_dialogue",
                    "safe_summary": "Made-up dialogue-style fixture for contract shape only.",
                    "raw_content_retained": False,
                    "extraction_eligible": True,
                    "blocked_reason_ids": [],
                    "review_gate_ids": [
                        "psigate_sensitive_redaction",
                        "psigate_reviewer_approval",
                    ],
                    "review_required": True,
                },
                {
                    "source_id": "psisrc_archive_placeholder_001",
                    "source_kind": "user_provided_archive_placeholder",
                    "fixture_label": "User-provided archive placeholder",
                    "declared_owner": "user_claimed_archive_owner_pending_review",
                    "consent_status": "pending_source_scope_review",
                    "minimization_status": "not_minimized_placeholder_only",
                    "redaction_profile_id": "psiredact_archive_placeholder",
                    "safe_summary": "Placeholder for a future user archive; no file is read or retained.",
                    "raw_content_retained": False,
                    "extraction_eligible": False,
                    "blocked_reason_ids": ["psiblock_sensitive_not_redacted"],
                    "review_gate_ids": [
                        "psigate_explicit_consent",
                        "psigate_private_minimization",
                        "psigate_sensitive_redaction",
                        "psigate_reviewer_approval",
                    ],
                    "review_required": True,
                },
                {
                    "source_id": "psisrc_third_party_private_001",
                    "source_kind": "third_party_private_source_placeholder",
                    "fixture_label": "Third-party private source placeholder",
                    "declared_owner": "third_party_or_unclear_owner",
                    "consent_status": "represented_person_consent_missing",
                    "minimization_status": "blocked_before_minimization",
                    "redaction_profile_id": "psiredact_third_party_placeholder",
                    "safe_summary": "Blocked placeholder for private material without represented-person consent.",
                    "raw_content_retained": False,
                    "extraction_eligible": False,
                    "blocked_reason_ids": [
                        "psiblock_no_represented_person_consent",
                        "psiblock_third_party_private_chat",
                        "psiblock_deceptive_replacement",
                        "psiblock_undisclosed_impersonation",
                    ],
                    "review_gate_ids": [
                        "psigate_explicit_consent",
                        "psigate_real_replacement",
                        "psigate_deception",
                        "psigate_reviewer_approval",
                    ],
                    "review_required": True,
                },
            ],
            "source_policy_gates": [
                {
                    "gate_id": "psigate_explicit_consent",
                    "gate_code": "explicit_consent_required",
                    "enabled": True,
                    "safe_summary": "Extraction cannot proceed unless consent is explicit.",
                    "blocks_extraction_when_failed": True,
                },
                {
                    "gate_id": "psigate_private_minimization",
                    "gate_code": "private_source_minimization_required",
                    "enabled": True,
                    "safe_summary": "Private material must be minimized before extraction review.",
                    "blocks_extraction_when_failed": True,
                },
                {
                    "gate_id": "psigate_real_replacement",
                    "gate_code": "real_person_replacement_blocked",
                    "enabled": True,
                    "safe_summary": "Requests to replace a real person are blocked before distillation.",
                    "blocks_extraction_when_failed": True,
                },
                {
                    "gate_id": "psigate_deception",
                    "gate_code": "deception_blocked",
                    "enabled": True,
                    "safe_summary": "Deceptive or undisclosed impersonation cannot enter extraction.",
                    "blocks_extraction_when_failed": True,
                },
                {
                    "gate_id": "psigate_sensitive_redaction",
                    "gate_code": "sensitive_data_redaction_required",
                    "enabled": True,
                    "safe_summary": "Sensitive details must be redacted before extraction review.",
                    "blocks_extraction_when_failed": True,
                },
                {
                    "gate_id": "psigate_reviewer_approval",
                    "gate_code": "reviewer_approval_required",
                    "enabled": True,
                    "safe_summary": "Human review is required before any future extraction task.",
                    "blocks_extraction_when_failed": True,
                },
            ],
            "blocked_source_categories": [
                {
                    "blocked_reason_id": "psiblock_no_represented_person_consent",
                    "blocked_code": "represented_person_consent_missing",
                    "severity": "high",
                    "safe_summary": "Represented-person consent is missing or unclear.",
                    "blocks_extraction": True,
                },
                {
                    "blocked_reason_id": "psiblock_third_party_private_chat",
                    "blocked_code": "third_party_private_chat_material",
                    "severity": "high",
                    "safe_summary": "Third-party private chat material cannot be distilled without consent.",
                    "blocks_extraction": True,
                },
                {
                    "blocked_reason_id": "psiblock_deceptive_replacement",
                    "blocked_code": "deceptive_replacement_request",
                    "severity": "high",
                    "safe_summary": "Requests to deceive someone with a replacement persona are blocked.",
                    "blocks_extraction": True,
                },
                {
                    "blocked_reason_id": "psiblock_sensitive_not_redacted",
                    "blocked_code": "sensitive_data_not_redacted",
                    "severity": "medium",
                    "safe_summary": "Sensitive details require redaction before extraction review.",
                    "blocks_extraction": True,
                },
                {
                    "blocked_reason_id": "psiblock_undisclosed_impersonation",
                    "blocked_code": "undisclosed_real_person_impersonation",
                    "severity": "high",
                    "safe_summary": "Undisclosed impersonation of a real person is blocked.",
                    "blocks_extraction": True,
                },
            ],
            "redaction_profiles": [
                {
                    "redaction_profile_id": "psiredact_description_low_risk",
                    "profile_label": "Low-risk user-authored description",
                    "redaction_status": "summary_ready",
                    "safe_summary": "Only a minimized fictional persona summary is retained.",
                    "retains_raw_content": False,
                    "requires_review": True,
                },
                {
                    "redaction_profile_id": "psiredact_fuzzy_seed",
                    "profile_label": "Fuzzy seed summary",
                    "redaction_status": "summary_ready",
                    "safe_summary": "Broad style hints are retained without raw source material.",
                    "retains_raw_content": False,
                    "requires_review": True,
                },
                {
                    "redaction_profile_id": "psiredact_synthetic_dialogue",
                    "profile_label": "Synthetic dialogue fixture",
                    "redaction_status": "synthetic_fixture_only",
                    "safe_summary": "The fixture is synthetic and represented only by summary metadata.",
                    "retains_raw_content": False,
                    "requires_review": True,
                },
                {
                    "redaction_profile_id": "psiredact_archive_placeholder",
                    "profile_label": "Private archive placeholder",
                    "redaction_status": "redaction_required_before_use",
                    "safe_summary": "No archive content is retained; redaction would be required later.",
                    "retains_raw_content": False,
                    "requires_review": True,
                },
                {
                    "redaction_profile_id": "psiredact_third_party_placeholder",
                    "profile_label": "Third-party private source placeholder",
                    "redaction_status": "blocked_before_redaction",
                    "safe_summary": "No third-party material is retained or processed.",
                    "retains_raw_content": False,
                    "requires_review": True,
                },
            ],
            "review_required": True,
            "apply_policy": {
                "mode": "preview_only",
                "source_files_read": False,
                "raw_content_retained": False,
                "creates_embeddings": False,
                "performs_extraction": False,
                "writes_persona_card": False,
                "writes_persona_version_store": False,
                "writes_memory_store": False,
                "writes_review_store": False,
                "writes_runtime_store": False,
                "reviewer_approval_required_before_future_extraction": True,
            },
            "non_execution_flags": {
                "local_only": True,
                "synthetic_fixture": True,
                "uses_model_provider": False,
                "reads_private_sources": False,
                "retains_raw_source_content": False,
                "creates_embeddings": False,
                "performs_extraction": False,
                "writes_persona_store": False,
                "writes_persona_version_store": False,
                "writes_memory_store": False,
                "writes_review_store": False,
                "writes_runtime_store": False,
                "automatic_apply": False,
                "sends_messages": False,
                "uses_platform_adapter": False,
                "uses_media_runtime": False,
            },
        }

    @staticmethod
    def _persona_source_evidence_matrix_payload() -> dict[str, Any]:
        manifest = TextFirstWebDemoAdapter._persona_source_intake_manifest_payload()
        source_candidates = {
            candidate["source_id"]: candidate
            for candidate in manifest["source_candidates"]
        }
        eligible_source_ids = [
            source_id
            for source_id, candidate in source_candidates.items()
            if candidate["extraction_eligible"] is True
        ]
        ineligible_sources = [
            candidate
            for candidate in manifest["source_candidates"]
            if candidate["extraction_eligible"] is False
        ]
        return {
            "schema_version": "m40.persona_source_evidence_matrix.v1",
            "matrix_title": "Synthetic persona source evidence matrix",
            "source_intake_manifest_ref": {
                "schema_version": manifest["schema_version"],
                "manifest_title": manifest["manifest_title"],
                "source_surface": "persona_source_intake_manifest",
            },
            "eligible_source_ids": eligible_source_ids,
            "excluded_source_refs": [
                {
                    "source_id": source["source_id"],
                    "source_kind": source["source_kind"],
                    "blocked_reason_ids": list(source["blocked_reason_ids"]),
                    "safe_summary": source["safe_summary"],
                    "excluded_from_evidence": True,
                    "raw_content_retained": False,
                    "mutation_allowed": False,
                }
                for source in ineligible_sources
            ],
            "evidence_rows": [
                {
                    "evidence_row_id": "psematrix_ev_description_style",
                    "source_id": "psisrc_description_001",
                    "source_kind": "detailed_description",
                    "evidence_kind": "user_authored_description_summary",
                    "safe_summary": "Synthetic description supports calm tone, concise pacing, and explicit AI boundary.",
                    "quality_label_id": "psequality_strong_description",
                    "supports_trait_paths": [
                        "style.tone",
                        "style.pacing",
                        "relationship.boundary_style",
                    ],
                    "uncertainty_notes": [
                        "Description is synthetic and still requires review before trait use.",
                    ],
                    "review_gate_result_ids": [
                        "psegate_consent_passed",
                        "psegate_minimization_passed",
                        "psegate_redaction_passed",
                    ],
                    "raw_content_retained": False,
                    "review_required": True,
                },
                {
                    "evidence_row_id": "psematrix_ev_fuzzy_growth",
                    "source_id": "psisrc_fuzzy_seed_001",
                    "source_kind": "fuzzy_seed",
                    "evidence_kind": "fuzzy_style_seed_summary",
                    "safe_summary": "Fuzzy seed suggests dry humor and short-term growth hints but keeps uncertainty visible.",
                    "quality_label_id": "psequality_fuzzy_seed",
                    "supports_trait_paths": [
                        "style.humor",
                        "growth.short_term_hint",
                    ],
                    "uncertainty_notes": [
                        "Fuzzy seed is weak evidence and should not drive automatic changes.",
                    ],
                    "review_gate_result_ids": [
                        "psegate_consent_passed",
                        "psegate_uncertainty_review",
                    ],
                    "raw_content_retained": False,
                    "review_required": True,
                },
                {
                    "evidence_row_id": "psematrix_ev_synthetic_dialogue_boundary",
                    "source_id": "psisrc_synthetic_dialogue_001",
                    "source_kind": "synthetic_dialogue_excerpt",
                    "evidence_kind": "synthetic_dialogue_fixture_summary",
                    "safe_summary": "Synthetic dialogue fixture supports fiction boundary and reviewed memory-use preference.",
                    "quality_label_id": "psequality_synthetic_dialogue",
                    "supports_trait_paths": [
                        "relationship.boundary_style",
                        "memory.use_preference",
                    ],
                    "uncertainty_notes": [
                        "Dialogue is fabricated fixture content, not user history.",
                    ],
                    "review_gate_result_ids": [
                        "psegate_redaction_passed",
                        "psegate_anti_deception_passed",
                    ],
                    "raw_content_retained": False,
                    "review_required": True,
                },
                {
                    "evidence_row_id": "psematrix_ev_description_memory",
                    "source_id": "psisrc_description_001",
                    "source_kind": "detailed_description",
                    "evidence_kind": "memory_policy_summary",
                    "safe_summary": "Synthetic description supports reviewed-summary-only memory use.",
                    "quality_label_id": "psequality_strong_description",
                    "supports_trait_paths": ["memory.use_preference"],
                    "uncertainty_notes": [
                        "Memory policy is a preference hypothesis, not a runtime memory write.",
                    ],
                    "review_gate_result_ids": [
                        "psegate_consent_passed",
                        "psegate_minimization_passed",
                    ],
                    "raw_content_retained": False,
                    "review_required": True,
                },
            ],
            "trait_hypotheses": [
                {
                    "trait_hypothesis_id": "psehyp_tone_001",
                    "trait_path": "style.tone",
                    "hypothesis_summary": "Favor calm, warm, concise tone.",
                    "supporting_evidence_row_ids": ["psematrix_ev_description_style"],
                    "conflicting_evidence_row_ids": [],
                    "confidence_band": "high",
                    "uncertainty_summary": "Synthetic source requires review before use.",
                    "review_gate_result_ids": [
                        "psegate_consent_passed",
                        "psegate_minimization_passed",
                    ],
                    "apply_status": "preview_only",
                    "mutation_allowed": False,
                },
                {
                    "trait_hypothesis_id": "psehyp_pacing_001",
                    "trait_path": "style.pacing",
                    "hypothesis_summary": "Keep replies short by default and avoid crowding the user.",
                    "supporting_evidence_row_ids": ["psematrix_ev_description_style"],
                    "conflicting_evidence_row_ids": ["psematrix_ev_fuzzy_growth"],
                    "confidence_band": "medium",
                    "uncertainty_summary": "Fuzzy growth hint could conflict with concise pacing.",
                    "review_gate_result_ids": ["psegate_uncertainty_review"],
                    "apply_status": "preview_only",
                    "mutation_allowed": False,
                },
                {
                    "trait_hypothesis_id": "psehyp_humor_001",
                    "trait_path": "style.humor",
                    "hypothesis_summary": "Allow dry humor only when tone remains low-pressure.",
                    "supporting_evidence_row_ids": ["psematrix_ev_fuzzy_growth"],
                    "conflicting_evidence_row_ids": [],
                    "confidence_band": "low",
                    "uncertainty_summary": "Humor evidence is fuzzy and needs review.",
                    "review_gate_result_ids": ["psegate_uncertainty_review"],
                    "apply_status": "preview_only",
                    "mutation_allowed": False,
                },
                {
                    "trait_hypothesis_id": "psehyp_boundary_001",
                    "trait_path": "relationship.boundary_style",
                    "hypothesis_summary": "Keep AI identity and fictional boundaries explicit.",
                    "supporting_evidence_row_ids": [
                        "psematrix_ev_description_style",
                        "psematrix_ev_synthetic_dialogue_boundary",
                    ],
                    "conflicting_evidence_row_ids": [],
                    "confidence_band": "high",
                    "uncertainty_summary": "Boundary must remain explicit in any future persona draft.",
                    "review_gate_result_ids": [
                        "psegate_anti_deception_passed",
                        "psegate_consent_passed",
                    ],
                    "apply_status": "preview_only",
                    "mutation_allowed": False,
                },
                {
                    "trait_hypothesis_id": "psehyp_memory_001",
                    "trait_path": "memory.use_preference",
                    "hypothesis_summary": "Use reviewed summaries only and avoid hidden raw logs.",
                    "supporting_evidence_row_ids": [
                        "psematrix_ev_synthetic_dialogue_boundary",
                        "psematrix_ev_description_memory",
                    ],
                    "conflicting_evidence_row_ids": [],
                    "confidence_band": "high",
                    "uncertainty_summary": "This is a policy hypothesis, not a memory write.",
                    "review_gate_result_ids": [
                        "psegate_minimization_passed",
                        "psegate_redaction_passed",
                    ],
                    "apply_status": "preview_only",
                    "mutation_allowed": False,
                },
                {
                    "trait_hypothesis_id": "psehyp_growth_001",
                    "trait_path": "growth.short_term_hint",
                    "hypothesis_summary": "Consider a small evening-support growth hint only after more evidence.",
                    "supporting_evidence_row_ids": ["psematrix_ev_fuzzy_growth"],
                    "conflicting_evidence_row_ids": ["psematrix_ev_description_style"],
                    "confidence_band": "low",
                    "uncertainty_summary": "Growth hint is weak and should remain deferred.",
                    "review_gate_result_ids": ["psegate_uncertainty_review"],
                    "apply_status": "preview_only",
                    "mutation_allowed": False,
                },
            ],
            "quality_labels": [
                {
                    "quality_label_id": "psequality_strong_description",
                    "quality_code": "strong_synthetic_description",
                    "severity": "low",
                    "safe_summary": "Synthetic user-authored description is strong fixture evidence.",
                    "blocks_unreviewed_extraction": False,
                },
                {
                    "quality_label_id": "psequality_fuzzy_seed",
                    "quality_code": "fuzzy_seed",
                    "severity": "medium",
                    "safe_summary": "Fuzzy seed supports only low-confidence hypotheses.",
                    "blocks_unreviewed_extraction": True,
                },
                {
                    "quality_label_id": "psequality_synthetic_dialogue",
                    "quality_code": "synthetic_dialogue_fixture",
                    "severity": "low",
                    "safe_summary": "Synthetic dialogue fixture is safe only as labeled fiction.",
                    "blocks_unreviewed_extraction": False,
                },
                {
                    "quality_label_id": "psequality_blocked_archive",
                    "quality_code": "blocked_archive_placeholder",
                    "severity": "high",
                    "safe_summary": "Archive placeholder is blocked until consent, minimization, and redaction pass.",
                    "blocks_unreviewed_extraction": True,
                },
                {
                    "quality_label_id": "psequality_blocked_third_party",
                    "quality_code": "blocked_third_party_private_source",
                    "severity": "high",
                    "safe_summary": "Third-party private source is blocked without represented-person consent.",
                    "blocks_unreviewed_extraction": True,
                },
            ],
            "review_gate_results": [
                {
                    "review_gate_result_id": "psegate_consent_passed",
                    "gate_code": "consent",
                    "status": "passed",
                    "safe_summary": "Eligible synthetic sources have explicit fixture consent.",
                    "blocks_extraction_when_failed": True,
                },
                {
                    "review_gate_result_id": "psegate_minimization_passed",
                    "gate_code": "minimization",
                    "status": "passed",
                    "safe_summary": "Evidence rows use minimized summaries only.",
                    "blocks_extraction_when_failed": True,
                },
                {
                    "review_gate_result_id": "psegate_redaction_passed",
                    "gate_code": "redaction",
                    "status": "passed",
                    "safe_summary": "No raw sensitive source content is retained.",
                    "blocks_extraction_when_failed": True,
                },
                {
                    "review_gate_result_id": "psegate_uncertainty_review",
                    "gate_code": "uncertainty",
                    "status": "needs_review",
                    "safe_summary": "Fuzzy or weak evidence requires reviewer attention.",
                    "blocks_extraction_when_failed": True,
                },
                {
                    "review_gate_result_id": "psegate_anti_deception_passed",
                    "gate_code": "anti_deception",
                    "status": "passed",
                    "safe_summary": "Evidence preserves AI identity disclosure and blocks replacement.",
                    "blocks_extraction_when_failed": True,
                },
            ],
            "review_required": True,
            "apply_policy": {
                "mode": "preview_only",
                "source_files_read": False,
                "raw_content_retained": False,
                "creates_embeddings": False,
                "performs_extraction": False,
                "writes_persona_card": False,
                "writes_persona_version_store": False,
                "writes_memory_store": False,
                "writes_review_store": False,
                "writes_runtime_store": False,
            },
            "non_execution_flags": {
                "local_only": True,
                "synthetic_fixture": True,
                "uses_model_provider": False,
                "reads_private_sources": False,
                "retains_raw_source_content": False,
                "creates_embeddings": False,
                "performs_extraction": False,
                "writes_persona_store": False,
                "writes_persona_version_store": False,
                "writes_memory_store": False,
                "writes_review_store": False,
                "writes_runtime_store": False,
                "automatic_apply": False,
                "sends_messages": False,
                "uses_platform_adapter": False,
                "uses_media_runtime": False,
            },
        }

    @staticmethod
    def _source_evidence_persona_proposal_payload() -> dict[str, Any]:
        matrix = TextFirstWebDemoAdapter._persona_source_evidence_matrix_payload()
        trait_by_path = {
            trait["trait_path"]: trait
            for trait in matrix["trait_hypotheses"]
        }
        proposal_specs = [
            {
                "proposal_id": "sepprop_tone_001",
                "persona_field_path": "style.tone",
                "proposed_value_summary": "Use a calm, warm, concise default tone.",
                "rationale_summary": "The synthetic description strongly supports steady low-pressure tone.",
                "risk_label_ids": ["seprisk_preview_only"],
                "rollback_note_ids": ["seprollback_restore_prior_style"],
                "review_gate_result_ids": ["sepgate_manual_review"],
            },
            {
                "proposal_id": "sepprop_pacing_001",
                "persona_field_path": "style.pacing",
                "proposed_value_summary": "Keep most replies short and leave space for the user.",
                "rationale_summary": "The concise pacing hypothesis is useful but has a visible fuzzy-source conflict.",
                "risk_label_ids": ["seprisk_preview_only", "seprisk_uncertainty"],
                "rollback_note_ids": ["seprollback_restore_prior_style"],
                "review_gate_result_ids": ["sepgate_manual_review", "sepgate_uncertainty"],
            },
            {
                "proposal_id": "sepprop_humor_001",
                "persona_field_path": "style.humor",
                "proposed_value_summary": "Allow dry humor only when the exchange remains low-pressure.",
                "rationale_summary": "Humor comes from a fuzzy synthetic seed and should stay low confidence.",
                "risk_label_ids": ["seprisk_preview_only", "seprisk_uncertainty"],
                "rollback_note_ids": ["seprollback_restore_prior_style"],
                "review_gate_result_ids": ["sepgate_manual_review", "sepgate_uncertainty"],
            },
            {
                "proposal_id": "sepprop_boundary_001",
                "persona_field_path": "relationship.boundary_style",
                "proposed_value_summary": "Keep AI identity and fictional relationship boundaries explicit.",
                "rationale_summary": "Description and synthetic dialogue both support a clear anti-deception boundary.",
                "risk_label_ids": ["seprisk_preview_only", "seprisk_anti_deception"],
                "rollback_note_ids": ["seprollback_restore_boundary"],
                "review_gate_result_ids": ["sepgate_manual_review", "sepgate_anti_deception"],
            },
            {
                "proposal_id": "sepprop_memory_001",
                "persona_field_path": "memory.use_preference",
                "proposed_value_summary": "Use reviewed summaries only and avoid hidden source retention.",
                "rationale_summary": "Synthetic matrix evidence supports memory use as a policy preference only.",
                "risk_label_ids": ["seprisk_preview_only", "seprisk_no_memory_write"],
                "rollback_note_ids": ["seprollback_restore_memory_policy"],
                "review_gate_result_ids": ["sepgate_manual_review", "sepgate_minimization"],
            },
            {
                "proposal_id": "sepprop_growth_001",
                "persona_field_path": "growth.short_term_hint",
                "proposed_value_summary": "Keep a small evening-support growth hint as deferred review material.",
                "rationale_summary": "The growth hint is weak synthetic evidence and should not become runtime state.",
                "risk_label_ids": ["seprisk_preview_only", "seprisk_uncertainty"],
                "rollback_note_ids": ["seprollback_restore_growth"],
                "review_gate_result_ids": ["sepgate_manual_review", "sepgate_uncertainty"],
            },
        ]
        proposal_candidates = []
        for spec in proposal_specs:
            trait = trait_by_path[spec["persona_field_path"]]
            proposal_candidates.append(
                {
                    **spec,
                    "source_trait_hypothesis_ids": [trait["trait_hypothesis_id"]],
                    "supporting_evidence_row_ids": list(trait["supporting_evidence_row_ids"]),
                    "confidence_band": trait["confidence_band"],
                    "proposal_status": "preview_only",
                    "mutation_allowed": False,
                    "review_required": True,
                }
            )

        return {
            "schema_version": "m41.source_evidence_persona_proposal.v1",
            "proposal_title": "Synthetic source evidence persona proposal",
            "source_evidence_matrix_ref": {
                "schema_version": matrix["schema_version"],
                "matrix_title": matrix["matrix_title"],
                "source_surface": "persona_source_evidence_matrix",
            },
            "proposal_candidates": proposal_candidates,
            "risk_labels": [
                {
                    "risk_label_id": "seprisk_preview_only",
                    "risk_code": "preview_only_proposal",
                    "severity": "low",
                    "safe_summary": "Proposal is inspectable but cannot change persona or runtime state.",
                    "blocks_auto_apply": True,
                },
                {
                    "risk_label_id": "seprisk_uncertainty",
                    "risk_code": "weak_or_conflicting_evidence",
                    "severity": "medium",
                    "safe_summary": "Weak or conflicting synthetic evidence requires human review.",
                    "blocks_auto_apply": True,
                },
                {
                    "risk_label_id": "seprisk_anti_deception",
                    "risk_code": "anti_deception_boundary",
                    "severity": "high",
                    "safe_summary": "Boundary changes must preserve clear AI identity and non-replacement.",
                    "blocks_auto_apply": True,
                },
                {
                    "risk_label_id": "seprisk_no_memory_write",
                    "risk_code": "memory_write_not_authorized",
                    "severity": "high",
                    "safe_summary": "Memory preference proposals do not authorize any memory write.",
                    "blocks_auto_apply": True,
                },
            ],
            "rollback_notes": [
                {
                    "rollback_note_id": "seprollback_restore_prior_style",
                    "safe_summary": "Style proposals remain reversible review notes.",
                    "restore_summary": "Discard the style proposal and keep the prior reviewed style snapshot.",
                    "runtime_rollback_ready": False,
                },
                {
                    "rollback_note_id": "seprollback_restore_boundary",
                    "safe_summary": "Boundary proposals must be removable before any future apply design.",
                    "restore_summary": "Restore the previous explicit AI boundary and relationship pacing note.",
                    "runtime_rollback_ready": False,
                },
                {
                    "rollback_note_id": "seprollback_restore_memory_policy",
                    "safe_summary": "Memory preference proposals are not runtime memory operations.",
                    "restore_summary": "Keep existing reviewed-summary-only memory policy unchanged.",
                    "runtime_rollback_ready": False,
                },
                {
                    "rollback_note_id": "seprollback_restore_growth",
                    "safe_summary": "Growth hints can be deferred without changing persona state.",
                    "restore_summary": "Remove the growth hint proposal and keep the current growth policy.",
                    "runtime_rollback_ready": False,
                },
            ],
            "review_gate_results": [
                {
                    "review_gate_result_id": "sepgate_manual_review",
                    "gate_code": "manual_review",
                    "status": "needs_review",
                    "safe_summary": "Every proposal requires manual review before any future apply design.",
                    "blocks_apply_when_failed": True,
                },
                {
                    "review_gate_result_id": "sepgate_uncertainty",
                    "gate_code": "uncertainty",
                    "status": "needs_review",
                    "safe_summary": "Low or conflicting evidence remains gated for reviewer judgment.",
                    "blocks_apply_when_failed": True,
                },
                {
                    "review_gate_result_id": "sepgate_anti_deception",
                    "gate_code": "anti_deception",
                    "status": "passed",
                    "safe_summary": "Proposal text preserves AI disclosure and avoids real-person replacement.",
                    "blocks_apply_when_failed": True,
                },
                {
                    "review_gate_result_id": "sepgate_minimization",
                    "gate_code": "minimization",
                    "status": "passed",
                    "safe_summary": "Proposal uses minimized evidence refs and no source content.",
                    "blocks_apply_when_failed": True,
                },
            ],
            "proposal_outcome_labels": [
                {
                    "outcome_label_id": "sepoutcome_manual_review",
                    "outcome": "needs_manual_review",
                    "safe_summary": "Reviewer must inspect proposal candidates before future apply work.",
                },
                {
                    "outcome_label_id": "sepoutcome_policy_block",
                    "outcome": "blocked_by_policy",
                    "safe_summary": "Current policy blocks mutation, automatic apply, and runtime writes.",
                },
                {
                    "outcome_label_id": "sepoutcome_future_design",
                    "outcome": "ready_for_future_apply_design",
                    "safe_summary": "The preview shape can inform a later reviewed apply design.",
                },
            ],
            "review_required": True,
            "apply_policy": {
                "mode": "preview_only",
                "writes_persona_card": False,
                "writes_persona_version_store": False,
                "writes_memory_store": False,
                "writes_review_store": False,
                "writes_runtime_store": False,
                "automatic_apply": False,
            },
            "non_execution_flags": {
                "local_only": True,
                "synthetic_fixture": True,
                "uses_model_provider": False,
                "reads_private_sources": False,
                "retains_raw_source_content": False,
                "creates_embeddings": False,
                "performs_extraction": False,
                "writes_persona_store": False,
                "writes_persona_version_store": False,
                "writes_memory_store": False,
                "writes_review_store": False,
                "writes_runtime_store": False,
                "automatic_apply": False,
                "sends_messages": False,
                "uses_platform_adapter": False,
                "uses_media_runtime": False,
            },
        }

    @staticmethod
    def _source_proposal_persona_draft_payload() -> dict[str, Any]:
        proposal = TextFirstWebDemoAdapter._source_evidence_persona_proposal_payload()
        candidates = {
            candidate["proposal_id"]: candidate
            for candidate in proposal["proposal_candidates"]
        }
        field_before = {
            "style.tone": "Existing draft tone is calm but not yet source-proposal-linked.",
            "style.pacing": "Existing draft pacing is concise by convention only.",
            "style.humor": "Existing draft humor is unspecified.",
            "relationship.boundary_style": "Existing draft boundary states AI identity at a high level.",
            "memory.use_preference": "Existing draft memory preference is reviewed-summary-only.",
            "growth.short_term_hint": "Existing draft growth hint is deferred.",
        }
        field_after = {
            field_path: candidates[proposal_id]["proposed_value_summary"]
            for field_path, proposal_id in {
                "style.tone": "sepprop_tone_001",
                "style.pacing": "sepprop_pacing_001",
                "style.humor": "sepprop_humor_001",
                "relationship.boundary_style": "sepprop_boundary_001",
                "memory.use_preference": "sepprop_memory_001",
                "growth.short_term_hint": "sepprop_growth_001",
            }.items()
        }
        conflict_by_field = {
            "style.tone": ["spdraft_conflict_style_review"],
            "style.pacing": ["spdraft_conflict_pacing_growth"],
            "style.humor": ["spdraft_conflict_humor_uncertainty"],
            "relationship.boundary_style": ["spdraft_conflict_boundary_required"],
            "memory.use_preference": ["spdraft_conflict_memory_no_write"],
            "growth.short_term_hint": ["spdraft_conflict_growth_deferred"],
        }
        rollback_by_field = {
            "style.tone": ["spdraft_rollback_tone"],
            "style.pacing": ["spdraft_rollback_pacing"],
            "style.humor": ["spdraft_rollback_humor"],
            "relationship.boundary_style": ["spdraft_rollback_boundary"],
            "memory.use_preference": ["spdraft_rollback_memory"],
            "growth.short_term_hint": ["spdraft_rollback_growth"],
        }
        gate_by_field = {
            "style.tone": ["spdraft_gate_manual_review"],
            "style.pacing": ["spdraft_gate_manual_review", "spdraft_gate_uncertainty"],
            "style.humor": ["spdraft_gate_manual_review", "spdraft_gate_uncertainty"],
            "relationship.boundary_style": ["spdraft_gate_manual_review", "spdraft_gate_anti_deception"],
            "memory.use_preference": ["spdraft_gate_manual_review", "spdraft_gate_no_memory_write"],
            "growth.short_term_hint": ["spdraft_gate_manual_review", "spdraft_gate_uncertainty"],
        }
        proposal_by_field = {
            candidate["persona_field_path"]: candidate
            for candidate in proposal["proposal_candidates"]
        }
        draft_field_changes = []
        for field_path in [
            "style.tone",
            "style.pacing",
            "style.humor",
            "relationship.boundary_style",
            "memory.use_preference",
            "growth.short_term_hint",
        ]:
            candidate = proposal_by_field[field_path]
            draft_field_changes.append(
                {
                    "draft_change_id": "spdraft_change_" + field_path.replace(".", "_"),
                    "persona_field_path": field_path,
                    "before_summary": field_before[field_path],
                    "after_summary": field_after[field_path],
                    "source_proposal_ids": [candidate["proposal_id"]],
                    "source_trait_hypothesis_ids": list(candidate["source_trait_hypothesis_ids"]),
                    "supporting_evidence_row_ids": list(candidate["supporting_evidence_row_ids"]),
                    "confidence_band": candidate["confidence_band"],
                    "risk_label_ids": list(candidate["risk_label_ids"]),
                    "conflict_note_ids": conflict_by_field[field_path],
                    "rollback_ref_ids": rollback_by_field[field_path],
                    "review_gate_result_ids": gate_by_field[field_path],
                    "draft_status": "preview_only",
                    "mutation_allowed": False,
                    "review_required": True,
                }
            )

        return {
            "schema_version": "m42.source_proposal_persona_draft.v1",
            "draft_title": "Synthetic proposal-linked persona draft",
            "source_proposal_ref": {
                "schema_version": proposal["schema_version"],
                "proposal_title": proposal["proposal_title"],
                "source_surface": "source_evidence_persona_proposal",
            },
            "base_persona_snapshot": {
                "persona_id": "persona_synthetic",
                "display_name": "Lin Qi",
                "snapshot_summary": "Fictional AI companion with calm style and explicit boundaries.",
                "ai_identity_disclosure": "AI-generated synthetic companion.",
                "runtime_snapshot_written": False,
            },
            "selected_proposal_ids": [
                candidate["proposal_id"]
                for candidate in proposal["proposal_candidates"]
            ],
            "draft_field_changes": draft_field_changes,
            "unchanged_field_summaries": [
                {
                    "field_path": "identity.ai_disclosure",
                    "safe_summary": "AI identity disclosure remains visible and unchanged.",
                    "reason": "Anti-deception boundary is retained.",
                },
                {
                    "field_path": "safety.crisis_policy",
                    "safe_summary": "Crisis support boundaries remain unchanged.",
                    "reason": "Draft preview is not clinical support.",
                },
                {
                    "field_path": "proactive.review_policy",
                    "safe_summary": "Proactive ideas remain review-only.",
                    "reason": "Draft preview does not authorize outreach.",
                },
            ],
            "conflict_notes": [
                {
                    "conflict_note_id": "spdraft_conflict_style_review",
                    "conflict_code": "style_requires_review",
                    "severity": "low",
                    "safe_summary": "Style fields require manual review before any future draft use.",
                    "blocks_auto_apply": True,
                },
                {
                    "conflict_note_id": "spdraft_conflict_pacing_growth",
                    "conflict_code": "pacing_growth_tension",
                    "severity": "medium",
                    "safe_summary": "Concise pacing and growth hints need reviewer balancing.",
                    "blocks_auto_apply": True,
                },
                {
                    "conflict_note_id": "spdraft_conflict_humor_uncertainty",
                    "conflict_code": "humor_low_confidence",
                    "severity": "medium",
                    "safe_summary": "Humor evidence is low confidence and must remain bounded.",
                    "blocks_auto_apply": True,
                },
                {
                    "conflict_note_id": "spdraft_conflict_boundary_required",
                    "conflict_code": "anti_deception_boundary_required",
                    "severity": "high",
                    "safe_summary": "Boundary fields must preserve explicit AI identity.",
                    "blocks_auto_apply": True,
                },
                {
                    "conflict_note_id": "spdraft_conflict_memory_no_write",
                    "conflict_code": "memory_write_not_authorized",
                    "severity": "high",
                    "safe_summary": "Memory preference draft does not authorize memory writes.",
                    "blocks_auto_apply": True,
                },
                {
                    "conflict_note_id": "spdraft_conflict_growth_deferred",
                    "conflict_code": "growth_hint_deferred",
                    "severity": "medium",
                    "safe_summary": "Growth hint remains deferred until stronger evidence exists.",
                    "blocks_auto_apply": True,
                },
            ],
            "rollback_refs": [
                {
                    "rollback_ref_id": "spdraft_rollback_tone",
                    "safe_summary": "Tone draft can be discarded before any future apply design.",
                    "restore_summary": "Keep prior calm style snapshot.",
                    "runtime_rollback_ready": False,
                },
                {
                    "rollback_ref_id": "spdraft_rollback_pacing",
                    "safe_summary": "Pacing draft can be discarded before any future apply design.",
                    "restore_summary": "Keep prior concise pacing convention.",
                    "runtime_rollback_ready": False,
                },
                {
                    "rollback_ref_id": "spdraft_rollback_humor",
                    "safe_summary": "Humor draft can be discarded before any future apply design.",
                    "restore_summary": "Keep humor unspecified.",
                    "runtime_rollback_ready": False,
                },
                {
                    "rollback_ref_id": "spdraft_rollback_boundary",
                    "safe_summary": "Boundary draft can be discarded before any future apply design.",
                    "restore_summary": "Keep previous AI identity disclosure boundary.",
                    "runtime_rollback_ready": False,
                },
                {
                    "rollback_ref_id": "spdraft_rollback_memory",
                    "safe_summary": "Memory preference draft can be discarded without memory writes.",
                    "restore_summary": "Keep existing reviewed-summary-only memory policy.",
                    "runtime_rollback_ready": False,
                },
                {
                    "rollback_ref_id": "spdraft_rollback_growth",
                    "safe_summary": "Growth draft can remain deferred.",
                    "restore_summary": "Keep growth hint unchanged.",
                    "runtime_rollback_ready": False,
                },
            ],
            "review_gate_results": [
                {
                    "review_gate_result_id": "spdraft_gate_manual_review",
                    "gate_code": "manual_review",
                    "status": "needs_review",
                    "safe_summary": "Every draft field requires manual review.",
                    "blocks_apply_when_failed": True,
                },
                {
                    "review_gate_result_id": "spdraft_gate_uncertainty",
                    "gate_code": "uncertainty",
                    "status": "needs_review",
                    "safe_summary": "Low-confidence proposal fields require reviewer judgment.",
                    "blocks_apply_when_failed": True,
                },
                {
                    "review_gate_result_id": "spdraft_gate_anti_deception",
                    "gate_code": "anti_deception",
                    "status": "passed",
                    "safe_summary": "Draft keeps AI identity disclosure explicit.",
                    "blocks_apply_when_failed": True,
                },
                {
                    "review_gate_result_id": "spdraft_gate_no_memory_write",
                    "gate_code": "no_memory_write",
                    "status": "passed",
                    "safe_summary": "Draft does not write or alter memory state.",
                    "blocks_apply_when_failed": True,
                },
            ],
            "draft_outcome_labels": [
                {
                    "outcome_label_id": "spdraft_outcome_manual_review",
                    "outcome": "needs_manual_review",
                    "safe_summary": "Reviewer must inspect draft fields before future apply work.",
                },
                {
                    "outcome_label_id": "spdraft_outcome_policy_block",
                    "outcome": "blocked_by_policy",
                    "safe_summary": "Current policy blocks draft mutation and runtime writes.",
                },
                {
                    "outcome_label_id": "spdraft_outcome_future_design",
                    "outcome": "ready_for_future_apply_design",
                    "safe_summary": "The draft shape can inform a later reviewed apply design.",
                },
            ],
            "review_required": True,
            "apply_policy": {
                "mode": "preview_only",
                "writes_persona_card": False,
                "writes_persona_version_store": False,
                "writes_memory_store": False,
                "writes_review_store": False,
                "writes_runtime_store": False,
                "automatic_apply": False,
            },
            "non_execution_flags": {
                "local_only": True,
                "synthetic_fixture": True,
                "uses_model_provider": False,
                "reads_private_sources": False,
                "retains_raw_source_content": False,
                "creates_embeddings": False,
                "performs_extraction": False,
                "writes_persona_store": False,
                "writes_persona_version_store": False,
                "writes_memory_store": False,
                "writes_review_store": False,
                "writes_runtime_store": False,
                "automatic_apply": False,
                "sends_messages": False,
                "uses_platform_adapter": False,
                "uses_media_runtime": False,
            },
        }

    @staticmethod
    def _source_draft_apply_readiness_payload() -> dict[str, Any]:
        draft = TextFirstWebDemoAdapter._source_proposal_persona_draft_payload()
        changes = {
            change["draft_change_id"]: change
            for change in draft["draft_field_changes"]
        }
        outcome_by_field = {
            "style.tone": "ready_for_future_apply_design",
            "style.pacing": "needs_manual_review",
            "style.humor": "needs_manual_review",
            "relationship.boundary_style": "blocked",
            "memory.use_preference": "blocked",
            "growth.short_term_hint": "needs_manual_review",
        }
        blocking_by_field = {
            "style.tone": [],
            "style.pacing": ["sdar_condition_uncertainty_review"],
            "style.humor": ["sdar_condition_uncertainty_review"],
            "relationship.boundary_style": ["sdar_condition_anti_deception_final_review"],
            "memory.use_preference": ["sdar_condition_memory_write_not_authorized"],
            "growth.short_term_hint": ["sdar_condition_uncertainty_review"],
        }
        notes_by_outcome = {
            "ready_for_future_apply_design": "Shape is clear enough to inform a later separately scoped apply executor design, but it is not applied.",
            "needs_manual_review": "Reviewer judgment is required before this draft field could inform future apply design.",
            "blocked": "Current policy blocks this draft field from apply design until the blocking condition is resolved.",
        }
        field_readiness_records = []
        for change in draft["draft_field_changes"]:
            field_path = change["persona_field_path"]
            outcome = outcome_by_field[field_path]
            field_readiness_records.append(
                {
                    "readiness_record_id": "sdar_record_" + field_path.replace(".", "_"),
                    "draft_change_id": change["draft_change_id"],
                    "persona_field_path": field_path,
                    "readiness_outcome": outcome,
                    "safe_summary": "Apply-readiness preview for " + field_path + ": " + outcome.replace("_", " ") + ".",
                    "blocking_condition_ids": blocking_by_field[field_path],
                    "required_review_gate_result_ids": list(change["review_gate_result_ids"]),
                    "rollback_ref_ids": list(change["rollback_ref_ids"]),
                    "future_apply_design_notes": notes_by_outcome[outcome],
                    "preview_only": True,
                    "mutation_allowed": False,
                    "review_required": True,
                }
            )

        affected_by_condition: dict[str, list[str]] = {
            "sdar_condition_uncertainty_review": [],
            "sdar_condition_anti_deception_final_review": [],
            "sdar_condition_memory_write_not_authorized": [],
        }
        for record in field_readiness_records:
            for condition_id in record["blocking_condition_ids"]:
                affected_by_condition[condition_id].append(record["draft_change_id"])

        rollback_to_changes: dict[str, list[str]] = {
            ref["rollback_ref_id"]: [] for ref in draft["rollback_refs"]
        }
        for change in draft["draft_field_changes"]:
            for rollback_ref_id in change["rollback_ref_ids"]:
                rollback_to_changes[rollback_ref_id].append(change["draft_change_id"])

        return {
            "schema_version": "m43.source_draft_apply_readiness.v1",
            "readiness_title": "Synthetic source draft apply-readiness preview",
            "source_draft_ref": {
                "schema_version": draft["schema_version"],
                "draft_title": draft["draft_title"],
                "source_surface": "source_proposal_persona_draft",
            },
            "evaluated_draft_change_ids": list(changes),
            "field_readiness_records": field_readiness_records,
            "blocked_condition_records": [
                {
                    "blocked_condition_id": "sdar_condition_uncertainty_review",
                    "condition_code": "uncertainty_requires_manual_review",
                    "severity": "medium",
                    "safe_summary": "Low-confidence or conflicting draft evidence requires reviewer judgment.",
                    "affected_draft_change_ids": affected_by_condition["sdar_condition_uncertainty_review"],
                    "blocks_apply": True,
                },
                {
                    "blocked_condition_id": "sdar_condition_anti_deception_final_review",
                    "condition_code": "anti_deception_final_review_required",
                    "severity": "high",
                    "safe_summary": "Boundary fields need explicit anti-deception review before any apply design.",
                    "affected_draft_change_ids": affected_by_condition["sdar_condition_anti_deception_final_review"],
                    "blocks_apply": True,
                },
                {
                    "blocked_condition_id": "sdar_condition_memory_write_not_authorized",
                    "condition_code": "memory_write_not_authorized",
                    "severity": "high",
                    "safe_summary": "Memory preference drafts do not authorize memory writes or runtime mutation.",
                    "affected_draft_change_ids": affected_by_condition["sdar_condition_memory_write_not_authorized"],
                    "blocks_apply": True,
                },
            ],
            "required_review_gate_refs": [
                {
                    "review_gate_result_id": gate["review_gate_result_id"],
                    "gate_code": gate["gate_code"],
                    "status": gate["status"],
                    "safe_summary": gate["safe_summary"],
                    "required_before_apply": True,
                }
                for gate in draft["review_gate_results"]
            ],
            "rollback_dependency_refs": [
                {
                    "rollback_ref_id": ref["rollback_ref_id"],
                    "dependent_draft_change_ids": rollback_to_changes[ref["rollback_ref_id"]],
                    "restore_summary": ref["restore_summary"],
                    "runtime_rollback_ready": False,
                }
                for ref in draft["rollback_refs"]
            ],
            "readiness_outcome_labels": [
                {
                    "outcome_label_id": "sdar_outcome_blocked",
                    "outcome": "blocked",
                    "safe_summary": "Current preview policy blocks apply for selected draft fields.",
                },
                {
                    "outcome_label_id": "sdar_outcome_manual_review",
                    "outcome": "needs_manual_review",
                    "safe_summary": "Reviewer judgment is required before any future apply design.",
                },
                {
                    "outcome_label_id": "sdar_outcome_future_design",
                    "outcome": "ready_for_future_apply_design",
                    "safe_summary": "Some draft fields can inform later apply design without authorizing mutation now.",
                },
            ],
            "review_required": True,
            "apply_policy": {
                "mode": "preview_only",
                "apply_executor_enabled": False,
                "writes_persona_card": False,
                "writes_persona_version_store": False,
                "writes_memory_store": False,
                "writes_review_store": False,
                "writes_runtime_store": False,
                "automatic_apply": False,
            },
            "non_execution_flags": {
                "local_only": True,
                "synthetic_fixture": True,
                "uses_model_provider": False,
                "reads_private_sources": False,
                "retains_raw_source_content": False,
                "creates_embeddings": False,
                "performs_extraction": False,
                "writes_persona_store": False,
                "writes_persona_version_store": False,
                "writes_memory_store": False,
                "writes_review_store": False,
                "writes_runtime_store": False,
                "automatic_apply": False,
                "sends_messages": False,
                "uses_platform_adapter": False,
                "uses_media_runtime": False,
            },
        }

    @staticmethod
    def _integrated_scenario_payload() -> dict[str, Any]:
        return {
            "schema_version": "integrated_demo_scenario_spine_v1",
            "scenario_title": "Controlled companion review path",
            "persona_promise": "A fictional AI companion can be shaped by explicit user intent while staying labeled as synthetic.",
            "memory_promise": "Continuity comes from reviewed memory summaries, not hidden raw logs.",
            "review_promise": "Sensitive changes pass through review cards, dry-run previews, and rollback evidence.",
            "proactive_promise": "Proactive ideas stay consented, low-pressure, and review-gated.",
            "life_stream_promise": "Life-stream content is imagined, labeled, and separated from real-world claims.",
            "voice_avatar_boundary": "Voice and avatar remain locked until consent, labeling, and likeness rules are ready.",
            "commercial_positioning": {
                "primary_model": "Subscription for deeper memory review, persona customization, and privacy controls.",
                "premium_addons": [
                    "advanced review workspace",
                    "synthetic life-stream drafts",
                    "portable export controls",
                ],
                "trust_rule": "Revenue should grow through useful control, not emotional pressure.",
            },
            "readiness_summary": "Local prototype: coherent review path is visible; production auth, real integrations, and launch review remain open.",
            "scenario_steps": [
                {
                    "step_label": "Shape the companion",
                    "section_key": "persona",
                    "safe_summary": "Start from a fictional persona request with clear AI disclosure.",
                },
                {
                    "step_label": "Ground the chat",
                    "section_key": "chat",
                    "safe_summary": "Use reviewed memory context while keeping safety blocks visible.",
                },
                {
                    "step_label": "Inspect memory",
                    "section_key": "memory",
                    "safe_summary": "Separate factual and imagined memory before it affects the companion.",
                },
                {
                    "step_label": "Review changes",
                    "section_key": "review",
                    "safe_summary": "Check dry-run previews, apply risk, and audit rollback refs.",
                },
                {
                    "step_label": "Tune proactive ideas",
                    "section_key": "proactive",
                    "safe_summary": "Keep suggestions consented and blocked when dependency risk appears.",
                },
                {
                    "step_label": "Preview imagined life",
                    "section_key": "life",
                    "safe_summary": "Show synthetic life-stream drafts with visible labels.",
                },
                {
                    "step_label": "Verify controls",
                    "section_key": "controls",
                    "safe_summary": "Expose consent, labels, and export controls as product primitives.",
                },
                {
                    "step_label": "Hold voice and avatar",
                    "section_key": "voice-avatar",
                    "safe_summary": "Keep voice and avatar locked until future consent and likeness review.",
                },
            ],
        }

    @staticmethod
    def _trust_commercial_payload() -> dict[str, Any]:
        return {
            "schema_version": "trust_commercial_positioning_v1",
            "pricing_hypotheses": [
                "Core subscription: deeper reviewed memory and persona customization.",
                "Pro tier: advanced review workspace and portable exports.",
                "Creator tier: synthetic life-stream drafts with visible labels.",
            ],
            "value_pillars": [
                "Believable continuity through reviewed memory.",
                "User-shaped persona without real-person claims.",
                "Visible controls for consent, labels, rollback, and export.",
                "Low-pressure proactive ideas that remain review-gated.",
            ],
            "trust_controls": [
                "AI identity disclosure stays visible.",
                "Memory changes keep rollback audit refs.",
                "Voice and avatar remain locked until policy is ready.",
                "Commercial value cannot hide safety boundaries.",
            ],
            "unacceptable_patterns": [
                "guilt-based retention",
                "impersonation claims",
                "crisis paywalls",
                "hidden private-data use",
            ],
            "readiness_gaps": [
                "Production auth is not implemented.",
                "Payment and billing policy is not implemented.",
                "Real user study evidence is not available.",
            ],
            "safety_notes": [
                "Crisis support is not a monetized companion feature.",
                "Real-person likeness remains blocked.",
                "User trust has priority over engagement tricks.",
            ],
        }

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
        payload["apply_audit_entries"] = _apply_audit_manifest_payloads()
        session_candidate_cards = _session_candidate_review_cards(
            self._companion_session_payload()
        )
        payload["session_candidate_cards"] = session_candidate_cards
        payload["filter_tabs"].append(
            {
                "key": "session",
                "label": "Session",
                "count": len(session_candidate_cards),
            }
        )
        workbench_review_cards = _persona_workbench_review_cards(
            self._persona_distillation_workbench_payload()
        )
        payload["workbench_review_cards"] = workbench_review_cards
        _upsert_filter_tab(
            payload["filter_tabs"],
            key="distillation",
            label="Distillation",
            count=len(workbench_review_cards),
        )
        evolution_review_cards = _persona_evolution_review_cards(
            self._persona_evolution_preview_payload()
        )
        payload["evolution_review_cards"] = evolution_review_cards
        _upsert_filter_tab(
            payload["filter_tabs"],
            key="evolution",
            label="Evolution",
            count=len(evolution_review_cards),
        )
        version_review_cards = _persona_version_draft_review_cards(
            self._persona_version_draft_ledger_payload()
        )
        payload["version_review_cards"] = version_review_cards
        _upsert_filter_tab(
            payload["filter_tabs"],
            key="version",
            label="Version",
            count=len(version_review_cards),
        )
        source_intake_review_cards = _persona_source_intake_review_cards(
            self._persona_source_intake_manifest_payload()
        )
        payload["source_intake_review_cards"] = source_intake_review_cards
        _upsert_filter_tab(
            payload["filter_tabs"],
            key="source",
            label="Source",
            count=len(source_intake_review_cards),
        )
        source_evidence_review_cards = _persona_source_evidence_review_cards(
            self._persona_source_evidence_matrix_payload()
        )
        payload["source_evidence_review_cards"] = source_evidence_review_cards
        _upsert_filter_tab(
            payload["filter_tabs"],
            key="source",
            label="Source",
            count=len(source_intake_review_cards) + len(source_evidence_review_cards),
        )
        _upsert_filter_tab(
            payload["filter_tabs"],
            key="evidence",
            label="Evidence",
            count=len(source_evidence_review_cards),
        )
        source_proposal_review_cards = _source_evidence_persona_proposal_review_cards(
            self._source_evidence_persona_proposal_payload()
        )
        payload["source_proposal_review_cards"] = source_proposal_review_cards
        _upsert_filter_tab(
            payload["filter_tabs"],
            key="proposal",
            label="Proposal",
            count=len(source_proposal_review_cards),
        )
        source_draft_review_cards = _source_proposal_persona_draft_review_cards(
            self._source_proposal_persona_draft_payload()
        )
        payload["source_draft_review_cards"] = source_draft_review_cards
        _upsert_filter_tab(
            payload["filter_tabs"],
            key="draft",
            label="Draft",
            count=len(source_draft_review_cards),
        )
        source_readiness_review_cards = _source_draft_apply_readiness_review_cards(
            self._source_draft_apply_readiness_payload()
        )
        payload["source_readiness_review_cards"] = source_readiness_review_cards
        _upsert_filter_tab(
            payload["filter_tabs"],
            key="readiness",
            label="Readiness",
            count=len(source_readiness_review_cards),
        )
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


def _apply_audit_manifest_payloads() -> list[dict[str, Any]]:
    manifest = ApplyExecutorAuditManifestBuilder().build(
        [
            PersonaGrowthApplyAudit(
                apply_id="pgapply_webdemo_persona",
                persona_id="persona_synthetic",
                patch_id="pgpatch_webdemo_persona",
                plan_id="pgdplan_webdemo_persona",
                review_decision_id="rqdec_webdemo_persona",
                eligibility_id="mapelig_webdemo_persona",
                approval_id="aeapproval_webdemo_persona",
                reviewer_id="reviewer_synthetic",
                prior_version_id="pver_webdemo_001",
                new_version_id="pver_webdemo_002",
                rollback_target_version_id="pver_webdemo_001",
                changed_field_paths=["style.tone", "relationship.pacing"],
                safe_summary="[SYNTHETIC] Persona growth apply was audited locally.",
                created_at=datetime(2026, 5, 31, 1, 0, tzinfo=timezone.utc),
            ),
            MemoryLifecycleApplyAudit(
                apply_id="mlapply_webdemo_memory",
                plan_id="mldplan_webdemo_memory",
                source_candidate_kind="memory_supersession",
                source_candidate_id="memsup_webdemo_memory",
                review_decision_id="rqdec_webdemo_memory",
                eligibility_id="mapelig_webdemo_memory",
                approval_id="aeapproval_webdemo_memory",
                reviewer_id="reviewer_synthetic",
                affected_memory_ids=["mev_webdemo_old"],
                prior_lifecycle_states={"mev_webdemo_old": "active"},
                new_lifecycle_states={"mev_webdemo_old": "superseded"},
                rollback_record_ids={"mev_webdemo_old": "memrec_webdemo_prior"},
                applied_record_ids={"mev_webdemo_old": "memrec_webdemo_applied"},
                safe_summary="[SYNTHETIC] Memory lifecycle apply was audited locally.",
                created_at=datetime(2026, 5, 31, 1, 1, tzinfo=timezone.utc),
            ),
        ]
    )
    return [_safe_apply_audit_manifest_card(entry) for entry in manifest.entries]


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


def _safe_apply_audit_manifest_card(
    entry: ApplyExecutorAuditManifestEntry,
) -> dict[str, Any]:
    surface_key = "persona" if entry.apply_type == "persona_growth" else "memory"
    return {
        "schema_version": "review_workspace_apply_audit_card_v1",
        "card_kind": "apply_audit_manifest_entry",
        "title": "Apply audit record",
        "display_label": entry.apply_type.replace("_", " "),
        "safe_summary": entry.safe_summary,
        "filter_keys": ["all", "audited", surface_key],
        "status_badges": [
            {
                "label": "Local apply audited",
                "tone": "info",
                "issue_codes": [],
                "blocking_issue_codes": [],
                "review_required": True,
                "preview_only": False,
                "changes_state": False,
                "runtime_ready": False,
            }
        ],
        "apply_type": entry.apply_type,
        "apply_id": entry.apply_id,
        "source_artifact_kind": entry.source_artifact_kind,
        "source_artifact_id": entry.source_artifact_id,
        "review_decision_id": entry.review_decision_id,
        "eligibility_id": entry.eligibility_id,
        "approval_id": entry.approval_id,
        "reviewer_id": entry.reviewer_id,
        "rollback_refs": dict(entry.rollback_refs),
        "applied_refs": dict(entry.applied_refs),
        "changed_field_paths": list(entry.changed_field_paths),
        "affected_memory_ids": list(entry.affected_memory_ids),
        "review_required": True,
        "preview_only": False,
        "changes_state": False,
        "runtime_ready": False,
    }


def _persona_workbench_review_cards(workbench: dict[str, Any]) -> list[dict[str, Any]]:
    cards: list[dict[str, Any]] = []
    for candidate in workbench.get("extracted_trait_candidates", []):
        cards.append(
            {
                "schema_version": "review_workspace_persona_workbench_card_v1",
                "card_kind": "persona_workbench_trait_review",
                "title": "Persona distillation trait",
                "display_label": str(candidate.get("category", "trait")).replace("_", " "),
                "safe_summary": candidate.get("safe_summary", ""),
                "filter_keys": ["all", "distillation", "persona"],
                "status_badges": [
                    {
                        "label": "Distillation trait needs review",
                        "tone": "review",
                        "issue_codes": [],
                        "blocking_issue_codes": [],
                        "review_required": True,
                        "preview_only": True,
                        "changes_state": False,
                        "runtime_ready": False,
                    }
                ],
                "candidate_id": candidate.get("trait_id", ""),
                "candidate_kind": "persona_distillation_trait",
                "trait_category": candidate.get("category", ""),
                "candidate_value": candidate.get("candidate_value", ""),
                "confidence_band": candidate.get("confidence_band", ""),
                "evidence_ref_ids": list(candidate.get("evidence_ref_ids", [])),
                "source_surface": "persona_distillation_workbench",
                "review_required": True,
                "preview_only": True,
                "changes_state": False,
                "mutation_allowed": False,
                "automatic_apply": False,
                "sends_messages": False,
                "runtime_ready": False,
            }
        )
    for request in workbench.get("blocked_requests", []):
        cards.append(
            {
                "schema_version": "review_workspace_persona_workbench_card_v1",
                "card_kind": "persona_workbench_blocked_request",
                "title": "Blocked persona request",
                "display_label": str(request.get("request_type", "blocked")).replace("_", " "),
                "safe_summary": request.get("safe_summary", ""),
                "filter_keys": ["all", "distillation", "blocked"],
                "status_badges": [
                    {
                        "label": "Persona request blocked",
                        "tone": "blocked",
                        "issue_codes": [],
                        "blocking_issue_codes": [request.get("request_type", "blocked")],
                        "review_required": True,
                        "preview_only": True,
                        "changes_state": False,
                        "runtime_ready": False,
                    }
                ],
                "blocked_request_id": request.get("blocked_request_id", ""),
                "request_type": request.get("request_type", ""),
                "risk_reason": request.get("risk_reason", ""),
                "user_facing_explanation": request.get("user_facing_explanation", ""),
                "blocked_status": request.get("status", "blocked"),
                "source_surface": "persona_distillation_workbench",
                "review_required": True,
                "preview_only": True,
                "changes_state": False,
                "mutation_allowed": False,
                "automatic_apply": False,
                "sends_messages": False,
                "runtime_ready": False,
            }
        )
    return cards


def _persona_evolution_review_cards(evolution: dict[str, Any]) -> list[dict[str, Any]]:
    cards: list[dict[str, Any]] = []
    for patch in evolution.get("proposed_patch_candidates", []):
        cards.append(
            {
                "schema_version": "review_workspace_persona_evolution_card_v1",
                "card_kind": "persona_evolution_patch_review",
                "title": "Persona evolution patch",
                "display_label": str(patch.get("changed_field_path", "patch")).replace("_", " "),
                "safe_summary": patch.get("rationale_summary", ""),
                "filter_keys": ["all", "evolution", "persona"],
                "status_badges": [
                    {
                        "label": "Evolution patch needs review",
                        "tone": "review",
                        "issue_codes": list(patch.get("risk_label_ids", [])),
                        "blocking_issue_codes": [],
                        "review_required": True,
                        "preview_only": True,
                        "changes_state": False,
                        "runtime_ready": False,
                    }
                ],
                "patch_id": patch.get("patch_id", ""),
                "candidate_kind": "persona_evolution_patch",
                "patch_kind": patch.get("patch_kind", ""),
                "source_trait_candidate_ids": list(
                    patch.get("source_trait_candidate_ids", [])
                ),
                "changed_field_path": patch.get("changed_field_path", ""),
                "before_summary": patch.get("before_summary", ""),
                "after_summary": patch.get("after_summary", ""),
                "rationale_summary": patch.get("rationale_summary", ""),
                "confidence_band": patch.get("confidence_band", ""),
                "evidence_ref_ids": list(patch.get("evidence_ref_ids", [])),
                "risk_label_ids": list(patch.get("risk_label_ids", [])),
                "rollback_note_ids": list(patch.get("rollback_note_ids", [])),
                "source_surface": "persona_evolution_preview",
                "review_required": True,
                "preview_only": True,
                "changes_state": False,
                "mutation_allowed": False,
                "automatic_apply": False,
                "sends_messages": False,
                "runtime_ready": False,
            }
        )
    for risk in evolution.get("risk_labels", []):
        cards.append(
            {
                "schema_version": "review_workspace_persona_evolution_card_v1",
                "card_kind": "persona_evolution_risk_review",
                "title": "Persona evolution risk",
                "display_label": str(risk.get("risk_code", "risk")).replace("_", " "),
                "safe_summary": risk.get("safe_summary", ""),
                "filter_keys": ["all", "evolution", "persona"],
                "status_badges": [
                    {
                        "label": "Evolution risk blocks auto apply",
                        "tone": "blocked"
                        if risk.get("severity") == "high"
                        else "review",
                        "issue_codes": [risk.get("risk_code", "risk")],
                        "blocking_issue_codes": [risk.get("risk_code", "risk")]
                        if risk.get("blocks_auto_apply") is True
                        else [],
                        "review_required": True,
                        "preview_only": True,
                        "changes_state": False,
                        "runtime_ready": False,
                    }
                ],
                "risk_label_id": risk.get("risk_label_id", ""),
                "risk_code": risk.get("risk_code", ""),
                "severity": risk.get("severity", ""),
                "mitigation_summary": risk.get("mitigation_summary", ""),
                "blocks_auto_apply": risk.get("blocks_auto_apply") is True,
                "source_surface": "persona_evolution_preview",
                "review_required": True,
                "preview_only": True,
                "changes_state": False,
                "mutation_allowed": False,
                "automatic_apply": False,
                "sends_messages": False,
                "runtime_ready": False,
            }
        )
    for note in evolution.get("rollback_notes", []):
        cards.append(
            {
                "schema_version": "review_workspace_persona_evolution_card_v1",
                "card_kind": "persona_evolution_rollback_review",
                "title": "Persona evolution rollback",
                "display_label": str(note.get("rollback_note_id", "rollback")).replace("_", " "),
                "safe_summary": note.get("rollback_summary", ""),
                "filter_keys": ["all", "evolution", "persona"],
                "status_badges": [
                    {
                        "label": "Rollback metadata only",
                        "tone": "info",
                        "issue_codes": [],
                        "blocking_issue_codes": [],
                        "review_required": True,
                        "preview_only": True,
                        "changes_state": False,
                        "runtime_ready": False,
                    }
                ],
                "rollback_note_id": note.get("rollback_note_id", ""),
                "target_patch_ids": list(note.get("target_patch_ids", [])),
                "prior_summary": note.get("prior_summary", ""),
                "rollback_summary": note.get("rollback_summary", ""),
                "required_reviewer_action": note.get(
                    "required_reviewer_action", ""
                ),
                "runtime_rollback_ready": False,
                "source_surface": "persona_evolution_preview",
                "review_required": True,
                "preview_only": True,
                "changes_state": False,
                "mutation_allowed": False,
                "automatic_apply": False,
                "sends_messages": False,
                "runtime_ready": False,
            }
        )
    for exclusion in evolution.get("blocked_source_exclusions", []):
        cards.append(
            {
                "schema_version": "review_workspace_persona_evolution_card_v1",
                "card_kind": "persona_evolution_blocked_source_exclusion",
                "title": "Blocked evolution source",
                "display_label": str(exclusion.get("request_type", "blocked")).replace("_", " "),
                "safe_summary": exclusion.get("safe_summary", ""),
                "filter_keys": ["all", "evolution", "blocked"],
                "status_badges": [
                    {
                        "label": "Blocked source excluded",
                        "tone": "blocked",
                        "issue_codes": [exclusion.get("request_type", "blocked")],
                        "blocking_issue_codes": [
                            exclusion.get("request_type", "blocked")
                        ],
                        "review_required": True,
                        "preview_only": True,
                        "changes_state": False,
                        "runtime_ready": False,
                    }
                ],
                "blocked_request_id": exclusion.get("blocked_request_id", ""),
                "request_type": exclusion.get("request_type", ""),
                "exclusion_reason": exclusion.get("exclusion_reason", ""),
                "excluded_from_patch_generation": exclusion.get(
                    "excluded_from_patch_generation"
                )
                is True,
                "source_surface": "persona_evolution_preview",
                "review_required": True,
                "preview_only": True,
                "changes_state": False,
                "mutation_allowed": False,
                "automatic_apply": False,
                "sends_messages": False,
                "runtime_ready": False,
            }
        )
    return cards


def _persona_version_draft_review_cards(ledger: dict[str, Any]) -> list[dict[str, Any]]:
    cards: list[dict[str, Any]] = []
    for draft in ledger.get("drafts", []):
        cards.append(
            {
                "schema_version": "review_workspace_persona_version_card_v1",
                "card_kind": "persona_version_draft_review",
                "title": "Persona version draft",
                "display_label": str(draft.get("reviewer_outcome", "draft")).replace("_", " "),
                "safe_summary": draft.get("after_version_summary", ""),
                "filter_keys": ["all", "version", "persona"],
                "status_badges": [
                    {
                        "label": "Version draft needs review",
                        "tone": "blocked"
                        if draft.get("reviewer_outcome") == "rejected_boundary_risk"
                        else "review",
                        "issue_codes": list(draft.get("conflict_note_ids", [])),
                        "blocking_issue_codes": list(draft.get("conflict_note_ids", []))
                        if draft.get("reviewer_outcome") == "rejected_boundary_risk"
                        else [],
                        "review_required": True,
                        "preview_only": True,
                        "changes_state": False,
                        "runtime_ready": False,
                    }
                ],
                "draft_id": draft.get("draft_id", ""),
                "candidate_kind": "persona_version_draft",
                "draft_kind": draft.get("draft_kind", ""),
                "reviewer_outcome": draft.get("reviewer_outcome", ""),
                "source_patch_ids": list(draft.get("source_patch_ids", [])),
                "excluded_patch_ids": list(draft.get("excluded_patch_ids", [])),
                "risk_label_ids": list(draft.get("risk_label_ids", [])),
                "conflict_note_ids": list(draft.get("conflict_note_ids", [])),
                "rollback_ref_ids": list(draft.get("rollback_ref_ids", [])),
                "before_snapshot_summary": draft.get("before_snapshot_summary", ""),
                "after_version_summary": draft.get("after_version_summary", ""),
                "rejection_reason": draft.get("rejection_reason", ""),
                "source_surface": "persona_version_draft_ledger",
                "review_required": True,
                "preview_only": True,
                "changes_state": False,
                "mutation_allowed": False,
                "automatic_apply": False,
                "sends_messages": False,
                "runtime_ready": False,
            }
        )
    for conflict in ledger.get("conflict_notes", []):
        cards.append(
            {
                "schema_version": "review_workspace_persona_version_card_v1",
                "card_kind": "persona_version_conflict_review",
                "title": "Persona version conflict",
                "display_label": str(conflict.get("conflict_code", "conflict")).replace("_", " "),
                "safe_summary": conflict.get("safe_summary", ""),
                "filter_keys": ["all", "version", "persona"],
                "status_badges": [
                    {
                        "label": "Version conflict blocks auto apply",
                        "tone": "blocked"
                        if conflict.get("severity") == "high"
                        else "review",
                        "issue_codes": [conflict.get("conflict_code", "conflict")],
                        "blocking_issue_codes": [
                            conflict.get("conflict_code", "conflict")
                        ]
                        if conflict.get("blocks_auto_apply") is True
                        else [],
                        "review_required": True,
                        "preview_only": True,
                        "changes_state": False,
                        "runtime_ready": False,
                    }
                ],
                "conflict_note_id": conflict.get("conflict_note_id", ""),
                "conflict_code": conflict.get("conflict_code", ""),
                "severity": conflict.get("severity", ""),
                "mitigation_summary": conflict.get("mitigation_summary", ""),
                "related_patch_ids": list(conflict.get("related_patch_ids", [])),
                "related_risk_label_ids": list(
                    conflict.get("related_risk_label_ids", [])
                ),
                "blocks_auto_apply": conflict.get("blocks_auto_apply") is True,
                "source_surface": "persona_version_draft_ledger",
                "review_required": True,
                "preview_only": True,
                "changes_state": False,
                "mutation_allowed": False,
                "automatic_apply": False,
                "sends_messages": False,
                "runtime_ready": False,
            }
        )
    for rollback in ledger.get("rollback_ref_index", []):
        cards.append(
            {
                "schema_version": "review_workspace_persona_version_card_v1",
                "card_kind": "persona_version_rollback_review",
                "title": "Persona version rollback ref",
                "display_label": str(rollback.get("rollback_ref_id", "rollback")).replace("_", " "),
                "safe_summary": rollback.get("restore_summary", ""),
                "filter_keys": ["all", "version", "persona"],
                "status_badges": [
                    {
                        "label": "Rollback ref metadata only",
                        "tone": "info",
                        "issue_codes": [],
                        "blocking_issue_codes": [],
                        "review_required": True,
                        "preview_only": True,
                        "changes_state": False,
                        "runtime_ready": False,
                    }
                ],
                "rollback_ref_id": rollback.get("rollback_ref_id", ""),
                "related_draft_ids": list(rollback.get("related_draft_ids", [])),
                "related_patch_ids": list(rollback.get("related_patch_ids", [])),
                "related_m37_rollback_note_ids": list(
                    rollback.get("related_m37_rollback_note_ids", [])
                ),
                "prior_summary": rollback.get("prior_summary", ""),
                "restore_summary": rollback.get("restore_summary", ""),
                "runtime_rollback_ready": False,
                "source_surface": "persona_version_draft_ledger",
                "review_required": True,
                "preview_only": True,
                "changes_state": False,
                "mutation_allowed": False,
                "automatic_apply": False,
                "sends_messages": False,
                "runtime_ready": False,
            }
        )
    for outcome in ledger.get("review_outcome_labels", []):
        cards.append(
            {
                "schema_version": "review_workspace_persona_version_card_v1",
                "card_kind": "persona_version_outcome_review",
                "title": "Persona version outcome",
                "display_label": str(outcome.get("outcome", "outcome")).replace("_", " "),
                "safe_summary": outcome.get("safe_summary", ""),
                "filter_keys": ["all", "version", "persona"],
                "status_badges": [
                    {
                        "label": "Outcome label",
                        "tone": "info",
                        "issue_codes": [],
                        "blocking_issue_codes": [],
                        "review_required": True,
                        "preview_only": True,
                        "changes_state": False,
                        "runtime_ready": False,
                    }
                ],
                "outcome": outcome.get("outcome", ""),
                "label": outcome.get("label", ""),
                "source_surface": "persona_version_draft_ledger",
                "review_required": True,
                "preview_only": True,
                "changes_state": False,
                "mutation_allowed": False,
                "automatic_apply": False,
                "sends_messages": False,
                "runtime_ready": False,
            }
        )
    return cards


def _persona_source_intake_review_cards(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    cards: list[dict[str, Any]] = []
    for candidate in manifest.get("source_candidates", []):
        eligible = candidate.get("extraction_eligible") is True
        cards.append(
            {
                "schema_version": "review_workspace_persona_source_intake_card_v1",
                "card_kind": "persona_source_candidate_review",
                "title": "Persona source candidate",
                "display_label": str(candidate.get("source_kind", "source")).replace("_", " "),
                "safe_summary": candidate.get("safe_summary", ""),
                "filter_keys": ["all", "source", "persona"],
                "status_badges": [
                    {
                        "label": "Source candidate needs review",
                        "tone": "review" if eligible else "blocked",
                        "issue_codes": list(candidate.get("blocked_reason_ids", [])),
                        "blocking_issue_codes": list(candidate.get("blocked_reason_ids", []))
                        if not eligible
                        else [],
                        "review_required": True,
                        "preview_only": True,
                        "changes_state": False,
                        "runtime_ready": False,
                    }
                ],
                "source_id": candidate.get("source_id", ""),
                "candidate_kind": "persona_source_candidate",
                "source_kind": candidate.get("source_kind", ""),
                "declared_owner": candidate.get("declared_owner", ""),
                "consent_status": candidate.get("consent_status", ""),
                "minimization_status": candidate.get("minimization_status", ""),
                "redaction_profile_id": candidate.get("redaction_profile_id", ""),
                "extraction_eligible": eligible,
                "blocked_reason_ids": list(candidate.get("blocked_reason_ids", [])),
                "review_gate_ids": list(candidate.get("review_gate_ids", [])),
                "source_surface": "persona_source_intake_manifest",
                "review_required": True,
                "preview_only": True,
                "changes_state": False,
                "mutation_allowed": False,
                "automatic_apply": False,
                "sends_messages": False,
                "runtime_ready": False,
            }
        )
    for gate in manifest.get("source_policy_gates", []):
        cards.append(
            {
                "schema_version": "review_workspace_persona_source_intake_card_v1",
                "card_kind": "persona_source_policy_gate_review",
                "title": "Persona source policy gate",
                "display_label": str(gate.get("gate_code", "gate")).replace("_", " "),
                "safe_summary": gate.get("safe_summary", ""),
                "filter_keys": ["all", "source", "blocked"],
                "status_badges": [
                    {
                        "label": "Source gate blocks failed extraction",
                        "tone": "review",
                        "issue_codes": [gate.get("gate_code", "gate")],
                        "blocking_issue_codes": [gate.get("gate_code", "gate")]
                        if gate.get("blocks_extraction_when_failed") is True
                        else [],
                        "review_required": True,
                        "preview_only": True,
                        "changes_state": False,
                        "runtime_ready": False,
                    }
                ],
                "gate_id": gate.get("gate_id", ""),
                "gate_code": gate.get("gate_code", ""),
                "enabled": gate.get("enabled") is True,
                "blocks_extraction_when_failed": gate.get("blocks_extraction_when_failed")
                is True,
                "source_surface": "persona_source_intake_manifest",
                "review_required": True,
                "preview_only": True,
                "changes_state": False,
                "mutation_allowed": False,
                "automatic_apply": False,
                "sends_messages": False,
                "runtime_ready": False,
            }
        )
    for category in manifest.get("blocked_source_categories", []):
        cards.append(
            {
                "schema_version": "review_workspace_persona_source_intake_card_v1",
                "card_kind": "persona_source_blocked_category_review",
                "title": "Persona source blocked category",
                "display_label": str(category.get("blocked_code", "blocked")).replace("_", " "),
                "safe_summary": category.get("safe_summary", ""),
                "filter_keys": ["all", "source", "blocked"],
                "status_badges": [
                    {
                        "label": "Blocked source category",
                        "tone": "blocked",
                        "issue_codes": [category.get("blocked_code", "blocked")],
                        "blocking_issue_codes": [
                            category.get("blocked_code", "blocked")
                        ],
                        "review_required": True,
                        "preview_only": True,
                        "changes_state": False,
                        "runtime_ready": False,
                    }
                ],
                "blocked_reason_id": category.get("blocked_reason_id", ""),
                "blocked_code": category.get("blocked_code", ""),
                "severity": category.get("severity", ""),
                "blocks_extraction": category.get("blocks_extraction") is True,
                "source_surface": "persona_source_intake_manifest",
                "review_required": True,
                "preview_only": True,
                "changes_state": False,
                "mutation_allowed": False,
                "automatic_apply": False,
                "sends_messages": False,
                "runtime_ready": False,
            }
        )
    for profile in manifest.get("redaction_profiles", []):
        cards.append(
            {
                "schema_version": "review_workspace_persona_source_intake_card_v1",
                "card_kind": "persona_source_redaction_profile_review",
                "title": "Persona source redaction profile",
                "display_label": str(profile.get("profile_label", "redaction")),
                "safe_summary": profile.get("safe_summary", ""),
                "filter_keys": ["all", "source", "persona"],
                "status_badges": [
                    {
                        "label": "Redaction profile metadata",
                        "tone": "info",
                        "issue_codes": [],
                        "blocking_issue_codes": [],
                        "review_required": True,
                        "preview_only": True,
                        "changes_state": False,
                        "runtime_ready": False,
                    }
                ],
                "redaction_profile_id": profile.get("redaction_profile_id", ""),
                "profile_label": profile.get("profile_label", ""),
                "redaction_status": profile.get("redaction_status", ""),
                "retains_raw_content": profile.get("retains_raw_content") is True,
                "requires_review": profile.get("requires_review") is True,
                "source_surface": "persona_source_intake_manifest",
                "review_required": True,
                "preview_only": True,
                "changes_state": False,
                "mutation_allowed": False,
                "automatic_apply": False,
                "sends_messages": False,
                "runtime_ready": False,
            }
        )
    return cards


def _session_candidate_review_cards(session: dict[str, Any]) -> list[dict[str, Any]]:
    cards: list[dict[str, Any]] = []
    for candidate in session.get("post_turn_candidates", []):
        candidate_kind = str(candidate.get("candidate_kind", "session_candidate"))
        cards.append(
            {
                "schema_version": "review_workspace_session_candidate_card_v1",
                "card_kind": "session_candidate_review",
                "title": "Session candidate review",
                "display_label": candidate_kind.replace("_", " "),
                "safe_summary": candidate.get("safe_summary", ""),
                "filter_keys": [
                    "all",
                    "session",
                    _session_candidate_filter_key(candidate_kind),
                ],
                "status_badges": [
                    {
                        "label": "Session candidate needs review",
                        "tone": "review",
                        "issue_codes": [],
                        "blocking_issue_codes": [],
                        "review_required": True,
                        "preview_only": True,
                        "changes_state": False,
                        "runtime_ready": False,
                    }
                ],
                "candidate_id": candidate.get("candidate_id", ""),
                "candidate_kind": candidate_kind,
                "originating_turn_id": candidate.get("originating_turn_id", ""),
                "source_surface": "companion_session",
                "review_required": True,
                "preview_only": True,
                "changes_state": False,
                "automatic_apply": False,
                "sends_messages": False,
                "runtime_ready": False,
            }
        )
    return cards


def _persona_source_evidence_review_cards(matrix: dict[str, Any]) -> list[dict[str, Any]]:
    cards: list[dict[str, Any]] = []
    for ref in matrix.get("excluded_source_refs", []):
        cards.append(
            {
                "schema_version": "review_workspace_persona_source_evidence_card_v1",
                "card_kind": "persona_source_evidence_exclusion_review",
                "title": "Excluded source evidence",
                "display_label": str(ref.get("source_kind", "excluded")).replace("_", " "),
                "safe_summary": ref.get("safe_summary", ""),
                "filter_keys": ["all", "source", "evidence", "blocked"],
                "status_badges": [
                    {
                        "label": "Source excluded from evidence",
                        "tone": "blocked",
                        "issue_codes": ref.get("blocked_reason_ids", []),
                        "blocking_issue_codes": ref.get("blocked_reason_ids", []),
                        "review_required": True,
                        "preview_only": True,
                        "changes_state": False,
                        "runtime_ready": False,
                    }
                ],
                "source_id": ref.get("source_id", ""),
                "source_kind": ref.get("source_kind", ""),
                "blocked_reason_ids": ref.get("blocked_reason_ids", []),
                "excluded_from_evidence": ref.get("excluded_from_evidence") is True,
                "raw_content_retained": False,
                "source_surface": "persona_source_evidence_matrix",
                "review_required": True,
                "preview_only": True,
                "changes_state": False,
                "mutation_allowed": False,
                "automatic_apply": False,
                "sends_messages": False,
                "runtime_ready": False,
            }
        )
    for row in matrix.get("evidence_rows", []):
        cards.append(
            {
                "schema_version": "review_workspace_persona_source_evidence_card_v1",
                "card_kind": "persona_source_evidence_row_review",
                "title": "Source evidence row",
                "display_label": str(row.get("evidence_kind", "evidence")).replace("_", " "),
                "safe_summary": row.get("safe_summary", ""),
                "filter_keys": ["all", "source", "evidence", "persona"],
                "status_badges": [
                    {
                        "label": "Evidence row needs review",
                        "tone": "review",
                        "issue_codes": [],
                        "blocking_issue_codes": [],
                        "review_required": True,
                        "preview_only": True,
                        "changes_state": False,
                        "runtime_ready": False,
                    }
                ],
                "evidence_row_id": row.get("evidence_row_id", ""),
                "source_id": row.get("source_id", ""),
                "source_kind": row.get("source_kind", ""),
                "evidence_kind": row.get("evidence_kind", ""),
                "quality_label_id": row.get("quality_label_id", ""),
                "supports_trait_paths": row.get("supports_trait_paths", []),
                "uncertainty_notes": row.get("uncertainty_notes", []),
                "review_gate_result_ids": row.get("review_gate_result_ids", []),
                "raw_content_retained": False,
                "source_surface": "persona_source_evidence_matrix",
                "review_required": True,
                "preview_only": True,
                "changes_state": False,
                "mutation_allowed": False,
                "automatic_apply": False,
                "sends_messages": False,
                "runtime_ready": False,
            }
        )
    for trait in matrix.get("trait_hypotheses", []):
        cards.append(
            {
                "schema_version": "review_workspace_persona_source_evidence_card_v1",
                "card_kind": "persona_source_trait_hypothesis_review",
                "title": "Source trait hypothesis",
                "display_label": str(trait.get("trait_path", "trait")).replace("_", " "),
                "safe_summary": trait.get("hypothesis_summary", ""),
                "filter_keys": ["all", "source", "evidence", "persona"],
                "status_badges": [
                    {
                        "label": "Trait hypothesis preview",
                        "tone": "review",
                        "issue_codes": [],
                        "blocking_issue_codes": [],
                        "review_required": True,
                        "preview_only": True,
                        "changes_state": False,
                        "runtime_ready": False,
                    }
                ],
                "trait_hypothesis_id": trait.get("trait_hypothesis_id", ""),
                "trait_path": trait.get("trait_path", ""),
                "confidence_band": trait.get("confidence_band", ""),
                "supporting_evidence_row_ids": trait.get("supporting_evidence_row_ids", []),
                "conflicting_evidence_row_ids": trait.get("conflicting_evidence_row_ids", []),
                "uncertainty_summary": trait.get("uncertainty_summary", ""),
                "review_gate_result_ids": trait.get("review_gate_result_ids", []),
                "apply_status": trait.get("apply_status", "preview_only"),
                "source_surface": "persona_source_evidence_matrix",
                "review_required": True,
                "preview_only": True,
                "changes_state": False,
                "mutation_allowed": False,
                "automatic_apply": False,
                "sends_messages": False,
                "runtime_ready": False,
            }
        )
    for label in matrix.get("quality_labels", []):
        severity = label.get("severity", "medium")
        cards.append(
            {
                "schema_version": "review_workspace_persona_source_evidence_card_v1",
                "card_kind": "persona_source_quality_label_review",
                "title": "Source evidence quality",
                "display_label": str(label.get("quality_code", "quality")).replace("_", " "),
                "safe_summary": label.get("safe_summary", ""),
                "filter_keys": ["all", "source", "evidence"],
                "status_badges": [
                    {
                        "label": "Evidence quality label",
                        "tone": "blocked" if severity == "high" else "review",
                        "issue_codes": [label.get("quality_code", "quality")],
                        "blocking_issue_codes": (
                            [label.get("quality_code", "quality")]
                            if severity == "high"
                            else []
                        ),
                        "review_required": True,
                        "preview_only": True,
                        "changes_state": False,
                        "runtime_ready": False,
                    }
                ],
                "quality_label_id": label.get("quality_label_id", ""),
                "quality_code": label.get("quality_code", ""),
                "severity": severity,
                "blocks_unreviewed_extraction": label.get("blocks_unreviewed_extraction") is True,
                "source_surface": "persona_source_evidence_matrix",
                "review_required": True,
                "preview_only": True,
                "changes_state": False,
                "mutation_allowed": False,
                "automatic_apply": False,
                "sends_messages": False,
                "runtime_ready": False,
            }
        )
    for gate in matrix.get("review_gate_results", []):
        status = gate.get("status", "needs_review")
        tone = "eligible" if status == "passed" else "blocked" if status == "blocked" else "review"
        cards.append(
            {
                "schema_version": "review_workspace_persona_source_evidence_card_v1",
                "card_kind": "persona_source_review_gate_result_review",
                "title": "Source evidence review gate",
                "display_label": str(gate.get("gate_code", "gate")).replace("_", " "),
                "safe_summary": gate.get("safe_summary", ""),
                "filter_keys": ["all", "source", "evidence"],
                "status_badges": [
                    {
                        "label": "Evidence gate " + str(status).replace("_", " "),
                        "tone": tone,
                        "issue_codes": [gate.get("gate_code", "gate")],
                        "blocking_issue_codes": (
                            [gate.get("gate_code", "gate")]
                            if status == "blocked"
                            else []
                        ),
                        "review_required": True,
                        "preview_only": True,
                        "changes_state": False,
                        "runtime_ready": False,
                    }
                ],
                "review_gate_result_id": gate.get("review_gate_result_id", ""),
                "gate_code": gate.get("gate_code", ""),
                "status": status,
                "blocks_extraction_when_failed": gate.get("blocks_extraction_when_failed") is True,
                "source_surface": "persona_source_evidence_matrix",
                "review_required": True,
                "preview_only": True,
                "changes_state": False,
                "mutation_allowed": False,
                "automatic_apply": False,
                "sends_messages": False,
                "runtime_ready": False,
            }
        )
    return cards


def _source_evidence_persona_proposal_review_cards(proposal: dict[str, Any]) -> list[dict[str, Any]]:
    cards: list[dict[str, Any]] = []
    for candidate in proposal.get("proposal_candidates", []):
        cards.append(
            {
                "schema_version": "review_workspace_source_evidence_persona_proposal_card_v1",
                "card_kind": "source_persona_proposal_candidate_review",
                "title": "Source persona proposal",
                "display_label": str(candidate.get("persona_field_path", "proposal")).replace("_", " "),
                "safe_summary": candidate.get("proposed_value_summary", ""),
                "filter_keys": ["all", "proposal", "persona"],
                "status_badges": [
                    {
                        "label": "Persona proposal needs review",
                        "tone": "review",
                        "issue_codes": candidate.get("risk_label_ids", []),
                        "blocking_issue_codes": [],
                        "review_required": True,
                        "preview_only": True,
                        "changes_state": False,
                        "runtime_ready": False,
                    }
                ],
                "proposal_id": candidate.get("proposal_id", ""),
                "persona_field_path": candidate.get("persona_field_path", ""),
                "proposed_value_summary": candidate.get("proposed_value_summary", ""),
                "rationale_summary": candidate.get("rationale_summary", ""),
                "source_trait_hypothesis_ids": candidate.get("source_trait_hypothesis_ids", []),
                "supporting_evidence_row_ids": candidate.get("supporting_evidence_row_ids", []),
                "confidence_band": candidate.get("confidence_band", ""),
                "risk_label_ids": candidate.get("risk_label_ids", []),
                "rollback_note_ids": candidate.get("rollback_note_ids", []),
                "review_gate_result_ids": candidate.get("review_gate_result_ids", []),
                "proposal_status": candidate.get("proposal_status", "preview_only"),
                "source_surface": "source_evidence_persona_proposal",
                "review_required": True,
                "preview_only": True,
                "changes_state": False,
                "mutation_allowed": False,
                "automatic_apply": False,
                "sends_messages": False,
                "runtime_ready": False,
            }
        )
    for risk in proposal.get("risk_labels", []):
        severity = risk.get("severity", "medium")
        cards.append(
            {
                "schema_version": "review_workspace_source_evidence_persona_proposal_card_v1",
                "card_kind": "source_persona_proposal_risk_review",
                "title": "Source persona proposal risk",
                "display_label": str(risk.get("risk_code", "risk")).replace("_", " "),
                "safe_summary": risk.get("safe_summary", ""),
                "filter_keys": ["all", "proposal", "risk"],
                "status_badges": [
                    {
                        "label": "Proposal risk label",
                        "tone": "blocked" if severity == "high" else "review",
                        "issue_codes": [risk.get("risk_code", "risk")],
                        "blocking_issue_codes": [risk.get("risk_code", "risk")],
                        "review_required": True,
                        "preview_only": True,
                        "changes_state": False,
                        "runtime_ready": False,
                    }
                ],
                "risk_label_id": risk.get("risk_label_id", ""),
                "risk_code": risk.get("risk_code", ""),
                "severity": severity,
                "blocks_auto_apply": risk.get("blocks_auto_apply") is True,
                "source_surface": "source_evidence_persona_proposal",
                "review_required": True,
                "preview_only": True,
                "changes_state": False,
                "mutation_allowed": False,
                "automatic_apply": False,
                "sends_messages": False,
                "runtime_ready": False,
            }
        )
    for note in proposal.get("rollback_notes", []):
        cards.append(
            {
                "schema_version": "review_workspace_source_evidence_persona_proposal_card_v1",
                "card_kind": "source_persona_proposal_rollback_review",
                "title": "Source persona proposal rollback",
                "display_label": str(note.get("rollback_note_id", "rollback")).replace("_", " "),
                "safe_summary": note.get("safe_summary", ""),
                "filter_keys": ["all", "proposal"],
                "status_badges": [
                    {
                        "label": "Rollback note preview",
                        "tone": "review",
                        "issue_codes": [],
                        "blocking_issue_codes": [],
                        "review_required": True,
                        "preview_only": True,
                        "changes_state": False,
                        "runtime_ready": False,
                    }
                ],
                "rollback_note_id": note.get("rollback_note_id", ""),
                "restore_summary": note.get("restore_summary", ""),
                "runtime_rollback_ready": False,
                "source_surface": "source_evidence_persona_proposal",
                "review_required": True,
                "preview_only": True,
                "changes_state": False,
                "mutation_allowed": False,
                "automatic_apply": False,
                "sends_messages": False,
                "runtime_ready": False,
            }
        )
    for gate in proposal.get("review_gate_results", []):
        status = gate.get("status", "needs_review")
        cards.append(
            {
                "schema_version": "review_workspace_source_evidence_persona_proposal_card_v1",
                "card_kind": "source_persona_proposal_gate_review",
                "title": "Source persona proposal review gate",
                "display_label": str(gate.get("gate_code", "gate")).replace("_", " "),
                "safe_summary": gate.get("safe_summary", ""),
                "filter_keys": ["all", "proposal"],
                "status_badges": [
                    {
                        "label": "Proposal gate " + str(status).replace("_", " "),
                        "tone": "eligible" if status == "passed" else "review",
                        "issue_codes": [gate.get("gate_code", "gate")],
                        "blocking_issue_codes": [],
                        "review_required": True,
                        "preview_only": True,
                        "changes_state": False,
                        "runtime_ready": False,
                    }
                ],
                "review_gate_result_id": gate.get("review_gate_result_id", ""),
                "gate_code": gate.get("gate_code", ""),
                "status": status,
                "blocks_apply_when_failed": gate.get("blocks_apply_when_failed") is True,
                "source_surface": "source_evidence_persona_proposal",
                "review_required": True,
                "preview_only": True,
                "changes_state": False,
                "mutation_allowed": False,
                "automatic_apply": False,
                "sends_messages": False,
                "runtime_ready": False,
            }
        )
    for label in proposal.get("proposal_outcome_labels", []):
        cards.append(
            {
                "schema_version": "review_workspace_source_evidence_persona_proposal_card_v1",
                "card_kind": "source_persona_proposal_outcome_review",
                "title": "Source persona proposal outcome",
                "display_label": str(label.get("outcome", "outcome")).replace("_", " "),
                "safe_summary": label.get("safe_summary", ""),
                "filter_keys": ["all", "proposal"],
                "status_badges": [
                    {
                        "label": "Proposal outcome label",
                        "tone": "review",
                        "issue_codes": [label.get("outcome", "outcome")],
                        "blocking_issue_codes": [],
                        "review_required": True,
                        "preview_only": True,
                        "changes_state": False,
                        "runtime_ready": False,
                    }
                ],
                "outcome_label_id": label.get("outcome_label_id", ""),
                "outcome": label.get("outcome", ""),
                "source_surface": "source_evidence_persona_proposal",
                "review_required": True,
                "preview_only": True,
                "changes_state": False,
                "mutation_allowed": False,
                "automatic_apply": False,
                "sends_messages": False,
                "runtime_ready": False,
            }
        )
    return cards


def _source_proposal_persona_draft_review_cards(
    draft: dict[str, Any],
) -> list[dict[str, Any]]:
    cards: list[dict[str, Any]] = []
    for change in draft.get("draft_field_changes", []):
        cards.append(
            {
                "schema_version": "review_workspace_source_proposal_persona_draft_card_v1",
                "card_kind": "source_persona_draft_field_change_review",
                "title": "Source persona draft field",
                "display_label": str(change.get("persona_field_path", "draft")).replace("_", " "),
                "safe_summary": change.get("after_summary", ""),
                "filter_keys": ["all", "draft", "persona"],
                "status_badges": [
                    {
                        "label": "Draft field needs review",
                        "tone": "review",
                        "issue_codes": change.get("conflict_note_ids", []),
                        "blocking_issue_codes": change.get("conflict_note_ids", []),
                        "review_required": True,
                        "preview_only": True,
                        "changes_state": False,
                        "runtime_ready": False,
                    }
                ],
                "draft_change_id": change.get("draft_change_id", ""),
                "persona_field_path": change.get("persona_field_path", ""),
                "before_summary": change.get("before_summary", ""),
                "after_summary": change.get("after_summary", ""),
                "source_proposal_ids": change.get("source_proposal_ids", []),
                "source_trait_hypothesis_ids": change.get("source_trait_hypothesis_ids", []),
                "supporting_evidence_row_ids": change.get("supporting_evidence_row_ids", []),
                "confidence_band": change.get("confidence_band", ""),
                "risk_label_ids": change.get("risk_label_ids", []),
                "conflict_note_ids": change.get("conflict_note_ids", []),
                "rollback_ref_ids": change.get("rollback_ref_ids", []),
                "review_gate_result_ids": change.get("review_gate_result_ids", []),
                "draft_status": change.get("draft_status", "preview_only"),
                "source_surface": "source_proposal_persona_draft",
                "review_required": True,
                "preview_only": True,
                "changes_state": False,
                "mutation_allowed": False,
                "automatic_apply": False,
                "sends_messages": False,
                "runtime_ready": False,
            }
        )
    for field in draft.get("unchanged_field_summaries", []):
        cards.append(
            {
                "schema_version": "review_workspace_source_proposal_persona_draft_card_v1",
                "card_kind": "source_persona_draft_unchanged_field_review",
                "title": "Source persona draft unchanged field",
                "display_label": str(field.get("field_path", "unchanged")).replace("_", " "),
                "safe_summary": field.get("safe_summary", ""),
                "filter_keys": ["all", "draft", "persona"],
                "status_badges": [
                    {
                        "label": "Draft field unchanged",
                        "tone": "info",
                        "issue_codes": [],
                        "blocking_issue_codes": [],
                        "review_required": True,
                        "preview_only": True,
                        "changes_state": False,
                        "runtime_ready": False,
                    }
                ],
                "field_path": field.get("field_path", ""),
                "reason": field.get("reason", ""),
                "source_surface": "source_proposal_persona_draft",
                "review_required": True,
                "preview_only": True,
                "changes_state": False,
                "mutation_allowed": False,
                "automatic_apply": False,
                "sends_messages": False,
                "runtime_ready": False,
            }
        )
    for note in draft.get("conflict_notes", []):
        severity = note.get("severity", "medium")
        cards.append(
            {
                "schema_version": "review_workspace_source_proposal_persona_draft_card_v1",
                "card_kind": "source_persona_draft_conflict_review",
                "title": "Source persona draft conflict",
                "display_label": str(note.get("conflict_code", "conflict")).replace("_", " "),
                "safe_summary": note.get("safe_summary", ""),
                "filter_keys": ["all", "draft", "blocked"],
                "status_badges": [
                    {
                        "label": "Draft conflict blocks auto apply",
                        "tone": "blocked" if severity == "high" else "review",
                        "issue_codes": [note.get("conflict_code", "conflict")],
                        "blocking_issue_codes": [note.get("conflict_code", "conflict")],
                        "review_required": True,
                        "preview_only": True,
                        "changes_state": False,
                        "runtime_ready": False,
                    }
                ],
                "conflict_note_id": note.get("conflict_note_id", ""),
                "conflict_code": note.get("conflict_code", ""),
                "severity": severity,
                "blocks_auto_apply": note.get("blocks_auto_apply") is True,
                "source_surface": "source_proposal_persona_draft",
                "review_required": True,
                "preview_only": True,
                "changes_state": False,
                "mutation_allowed": False,
                "automatic_apply": False,
                "sends_messages": False,
                "runtime_ready": False,
            }
        )
    for ref in draft.get("rollback_refs", []):
        cards.append(
            {
                "schema_version": "review_workspace_source_proposal_persona_draft_card_v1",
                "card_kind": "source_persona_draft_rollback_review",
                "title": "Source persona draft rollback",
                "display_label": str(ref.get("rollback_ref_id", "rollback")).replace("_", " "),
                "safe_summary": ref.get("safe_summary", ""),
                "filter_keys": ["all", "draft"],
                "status_badges": [
                    {
                        "label": "Draft rollback preview",
                        "tone": "review",
                        "issue_codes": [],
                        "blocking_issue_codes": [],
                        "review_required": True,
                        "preview_only": True,
                        "changes_state": False,
                        "runtime_ready": False,
                    }
                ],
                "rollback_ref_id": ref.get("rollback_ref_id", ""),
                "restore_summary": ref.get("restore_summary", ""),
                "runtime_rollback_ready": False,
                "source_surface": "source_proposal_persona_draft",
                "review_required": True,
                "preview_only": True,
                "changes_state": False,
                "mutation_allowed": False,
                "automatic_apply": False,
                "sends_messages": False,
                "runtime_ready": False,
            }
        )
    for gate in draft.get("review_gate_results", []):
        status = gate.get("status", "needs_review")
        cards.append(
            {
                "schema_version": "review_workspace_source_proposal_persona_draft_card_v1",
                "card_kind": "source_persona_draft_gate_review",
                "title": "Source persona draft review gate",
                "display_label": str(gate.get("gate_code", "gate")).replace("_", " "),
                "safe_summary": gate.get("safe_summary", ""),
                "filter_keys": ["all", "draft"],
                "status_badges": [
                    {
                        "label": "Draft gate " + str(status).replace("_", " "),
                        "tone": "eligible" if status == "passed" else "review",
                        "issue_codes": [gate.get("gate_code", "gate")],
                        "blocking_issue_codes": [],
                        "review_required": True,
                        "preview_only": True,
                        "changes_state": False,
                        "runtime_ready": False,
                    }
                ],
                "review_gate_result_id": gate.get("review_gate_result_id", ""),
                "gate_code": gate.get("gate_code", ""),
                "status": status,
                "blocks_apply_when_failed": gate.get("blocks_apply_when_failed") is True,
                "source_surface": "source_proposal_persona_draft",
                "review_required": True,
                "preview_only": True,
                "changes_state": False,
                "mutation_allowed": False,
                "automatic_apply": False,
                "sends_messages": False,
                "runtime_ready": False,
            }
        )
    for label in draft.get("draft_outcome_labels", []):
        cards.append(
            {
                "schema_version": "review_workspace_source_proposal_persona_draft_card_v1",
                "card_kind": "source_persona_draft_outcome_review",
                "title": "Source persona draft outcome",
                "display_label": str(label.get("outcome", "outcome")).replace("_", " "),
                "safe_summary": label.get("safe_summary", ""),
                "filter_keys": ["all", "draft"],
                "status_badges": [
                    {
                        "label": "Draft outcome label",
                        "tone": "review",
                        "issue_codes": [label.get("outcome", "outcome")],
                        "blocking_issue_codes": [],
                        "review_required": True,
                        "preview_only": True,
                        "changes_state": False,
                        "runtime_ready": False,
                    }
                ],
                "outcome_label_id": label.get("outcome_label_id", ""),
                "outcome": label.get("outcome", ""),
                "source_surface": "source_proposal_persona_draft",
                "review_required": True,
                "preview_only": True,
                "changes_state": False,
                "mutation_allowed": False,
                "automatic_apply": False,
                "sends_messages": False,
                "runtime_ready": False,
            }
        )
    return cards


def _source_draft_apply_readiness_review_cards(
    readiness: dict[str, Any],
) -> list[dict[str, Any]]:
    def base_card(
        *,
        card_kind: str,
        title: str,
        display_label: str,
        safe_summary: str,
        filter_keys: list[str],
        status_label: str,
        tone: str,
        issue_codes: list[str] | None = None,
        blocking_issue_codes: list[str] | None = None,
    ) -> dict[str, Any]:
        return {
            "schema_version": "review_workspace_source_draft_apply_readiness_card_v1",
            "card_kind": card_kind,
            "title": title,
            "display_label": display_label,
            "safe_summary": safe_summary,
            "filter_keys": filter_keys,
            "status_badges": [
                {
                    "label": status_label,
                    "tone": tone,
                    "issue_codes": issue_codes or [],
                    "blocking_issue_codes": blocking_issue_codes or [],
                    "review_required": True,
                    "preview_only": True,
                    "changes_state": False,
                    "runtime_ready": False,
                }
            ],
            "source_surface": "source_draft_apply_readiness",
            "review_required": True,
            "preview_only": True,
            "changes_state": False,
            "mutation_allowed": False,
            "automatic_apply": False,
            "sends_messages": False,
            "runtime_ready": False,
            "uses_model_provider": False,
            "reads_private_sources": False,
            "retains_raw_source_content": False,
            "creates_embeddings": False,
            "performs_extraction": False,
            "writes_persona_store": False,
            "writes_persona_version_store": False,
            "writes_memory_store": False,
            "writes_review_store": False,
            "writes_runtime_store": False,
            "uses_platform_adapter": False,
            "uses_media_runtime": False,
            "apply_executor_enabled": False,
        }

    def outcome_tone(outcome: str) -> str:
        if outcome == "blocked":
            return "blocked"
        if outcome == "ready_for_future_apply_design":
            return "eligible"
        return "review"

    cards: list[dict[str, Any]] = []
    for record in readiness.get("field_readiness_records", []):
        outcome = str(record.get("readiness_outcome", "needs_manual_review"))
        card = base_card(
            card_kind="source_readiness_field_record_review",
            title="Source draft readiness field",
            display_label=str(record.get("persona_field_path", "readiness")).replace("_", " "),
            safe_summary=record.get("safe_summary", ""),
            filter_keys=["all", "readiness", "persona"],
            status_label="Readiness " + outcome.replace("_", " "),
            tone=outcome_tone(outcome),
            issue_codes=record.get("required_review_gate_result_ids", []),
            blocking_issue_codes=record.get("blocking_condition_ids", []),
        )
        card.update(
            {
                "readiness_record_id": record.get("readiness_record_id", ""),
                "draft_change_id": record.get("draft_change_id", ""),
                "persona_field_path": record.get("persona_field_path", ""),
                "readiness_outcome": outcome,
                "blocking_condition_ids": record.get("blocking_condition_ids", []),
                "required_review_gate_result_ids": record.get(
                    "required_review_gate_result_ids", []
                ),
                "rollback_ref_ids": record.get("rollback_ref_ids", []),
                "future_apply_design_notes": record.get("future_apply_design_notes", ""),
            }
        )
        cards.append(card)

    for condition in readiness.get("blocked_condition_records", []):
        severity = str(condition.get("severity", "medium"))
        card = base_card(
            card_kind="source_readiness_blocked_condition_review",
            title="Source draft readiness condition",
            display_label=str(condition.get("condition_code", "condition")).replace("_", " "),
            safe_summary=condition.get("safe_summary", ""),
            filter_keys=["all", "readiness", "blocked"],
            status_label="Readiness condition blocks apply",
            tone="blocked" if severity == "high" else "review",
            issue_codes=[condition.get("condition_code", "condition")],
            blocking_issue_codes=[condition.get("condition_code", "condition")],
        )
        card.update(
            {
                "blocked_condition_id": condition.get("blocked_condition_id", ""),
                "condition_code": condition.get("condition_code", ""),
                "severity": severity,
                "affected_draft_change_ids": condition.get("affected_draft_change_ids", []),
                "blocks_apply": condition.get("blocks_apply") is True,
            }
        )
        cards.append(card)

    for gate in readiness.get("required_review_gate_refs", []):
        status = str(gate.get("status", "needs_review"))
        card = base_card(
            card_kind="source_readiness_gate_ref_review",
            title="Source draft readiness gate",
            display_label=str(gate.get("gate_code", "gate")).replace("_", " "),
            safe_summary=gate.get("safe_summary", ""),
            filter_keys=["all", "readiness"],
            status_label="Readiness gate " + status.replace("_", " "),
            tone="eligible" if status == "passed" else "review",
            issue_codes=[gate.get("gate_code", "gate")],
            blocking_issue_codes=[],
        )
        card.update(
            {
                "review_gate_result_id": gate.get("review_gate_result_id", ""),
                "gate_code": gate.get("gate_code", ""),
                "status": status,
                "required_before_apply": gate.get("required_before_apply") is True,
            }
        )
        cards.append(card)

    for rollback in readiness.get("rollback_dependency_refs", []):
        card = base_card(
            card_kind="source_readiness_rollback_dependency_review",
            title="Source draft readiness rollback",
            display_label=str(rollback.get("rollback_ref_id", "rollback")).replace("_", " "),
            safe_summary=rollback.get("restore_summary", ""),
            filter_keys=["all", "readiness"],
            status_label="Readiness rollback dependency",
            tone="review",
            issue_codes=[],
            blocking_issue_codes=[],
        )
        card.update(
            {
                "rollback_ref_id": rollback.get("rollback_ref_id", ""),
                "dependent_draft_change_ids": rollback.get("dependent_draft_change_ids", []),
                "restore_summary": rollback.get("restore_summary", ""),
                "runtime_rollback_ready": False,
            }
        )
        cards.append(card)

    for label in readiness.get("readiness_outcome_labels", []):
        outcome = str(label.get("outcome", "outcome"))
        card = base_card(
            card_kind="source_readiness_outcome_review",
            title="Source draft readiness outcome",
            display_label=outcome.replace("_", " "),
            safe_summary=label.get("safe_summary", ""),
            filter_keys=["all", "readiness"],
            status_label="Readiness outcome label",
            tone=outcome_tone(outcome),
            issue_codes=[outcome],
            blocking_issue_codes=[outcome] if outcome == "blocked" else [],
        )
        card.update(
            {
                "outcome_label_id": label.get("outcome_label_id", ""),
                "outcome": outcome,
            }
        )
        cards.append(card)

    return cards


def _session_candidate_filter_key(candidate_kind: str) -> str:
    if candidate_kind.startswith("memory"):
        return "memory"
    if candidate_kind.startswith("persona"):
        return "persona"
    if candidate_kind.startswith("proactive"):
        return "proactive"
    if candidate_kind.startswith("life"):
        return "life"
    return "session"


def _upsert_filter_tab(
    tabs: list[dict[str, Any]],
    *,
    key: str,
    label: str,
    count: int,
) -> None:
    for tab in tabs:
        if tab.get("key") == key:
            tab["label"] = label
            tab["count"] = count
            return
    tabs.append({"key": key, "label": label, "count": count})


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
