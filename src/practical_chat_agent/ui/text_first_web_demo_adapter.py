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
from practical_chat_agent.services.virtual_life_engine import (
    VirtualLifeEngine,
    VirtualLifeSeedContext,
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
        )

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
