"""T372 persona growth candidate tests.

All examples are synthetic and fictional. These tests do not read private chat
history, call LLMs, mutate PersonaCard versions, generate dialogue, schedule
messages, or connect to external platforms.
"""

from __future__ import annotations

import importlib
from typing import Any

import pytest
from pydantic import ValidationError

from practical_chat_agent.core.models import (
    MemoryEvent,
    MemoryProvenance,
    PersonaCard,
    PersonaEmotionModel,
    PersonaGrowthPolicy,
    PersonaIdentity,
    PersonaProactivePreferences,
    PersonaRelationshipModel,
    PersonaSafetyPolicy,
    PersonaSourcePolicy,
    PersonaSpeechStyle,
    PersonaTraitProfile,
    PersonaVirtualHistory,
)
from practical_chat_agent.services.memory_governance import PersonaGrowthEvidenceBundle


def _growth() -> Any:
    try:
        return importlib.import_module("practical_chat_agent.services.persona_growth")
    except ModuleNotFoundError as exc:
        pytest.fail(f"persona_growth module is missing: {exc}")


def _card(**overrides: object) -> PersonaCard:
    data: dict[str, object] = {
        "user_id": "user_synthetic",
        "display_name": "Lin Qi",
        "creation_mode": "detailed_prompt",
        "source_policy": PersonaSourcePolicy(source_type="original", risk_tier="L1"),
        "identity": PersonaIdentity(
            display_name="Lin Qi",
            fictional=True,
            age_range="mid_20s",
            world_setting="contemporary_realistic",
        ),
        "core_traits": PersonaTraitProfile(
            warmth=0.62,
            directness=0.78,
            humor=0.36,
            independence=0.81,
            jealousy=0.18,
            emotional_stability=0.69,
        ),
        "speech_style": PersonaSpeechStyle(
            sentence_length="short_to_medium",
            emoji_frequency="low",
            punctuation_style="minimal",
            taboo_phrases=["Only I understand you."],
        ),
        "emotion_model": PersonaEmotionModel(
            baseline_mood="calm",
            comforting_style="practical_plus_subtle_affection",
        ),
        "relationship_model": PersonaRelationshipModel(
            attachment_style="slow_warming",
            trust_growth_rate=0.35,
            intimacy_growth_rate=0.25,
            boundary_sensitivity=0.8,
        ),
        "virtual_history": PersonaVirtualHistory(
            background="Fictional background in a synthetic city.",
            daily_routine=["evening reading"],
            current_goals=["learn photography"],
        ),
        "growth_policy": PersonaGrowthPolicy(
            frozen_fields=["identity.age_range"],
            mutable_fields=["core_traits.warmth", "speech_style.sentence_length"],
            max_weekly_trait_delta=0.05,
        ),
        "proactive_preferences": PersonaProactivePreferences(default_enabled=False),
        "safety_policy": PersonaSafetyPolicy(),
    }
    data.update(overrides)
    return PersonaCard(**data)


def _factual_memory() -> MemoryEvent:
    return MemoryEvent(
        user_id="user_synthetic",
        event_type="factual",
        truth_status="evidence_backed",
        summary="[SYNTHETIC] User asked for slightly warmer replies.",
        provenance=MemoryProvenance(
            source_type="synthetic_test",
            evidence_refs=["synthetic_event_growth_001"],
        ),
        sensitivity="low",
    )


def _imagined_memory() -> MemoryEvent:
    return MemoryEvent(
        user_id="user_synthetic",
        event_type="imagined",
        truth_status="imagined",
        summary="[SYNTHETIC] Fictional persona dreamed of using a new nickname.",
        provenance=MemoryProvenance(source_type="imagined_generation"),
        sensitivity="low",
        imagined_context_label="dream_log",
    )


def _safe_change(**overrides: object) -> Any:
    module = _growth()
    data: dict[str, object] = {
        "field_path": "core_traits.warmth",
        "old_value_summary": "0.62",
        "proposed_value_summary": "0.66",
        "numeric_delta": 0.04,
        "change_reason": "[SYNTHETIC] User repeatedly asked for slightly warmer replies.",
        "source_memory_ids": ["mev_synthetic"],
    }
    data.update(overrides)
    return module.PersonaGrowthFieldChange(**data)


class TestPersonaGrowthFieldChange:
    def test_mutable_trait_change_is_reviewable_and_not_auto_approvable(self) -> None:
        change = _safe_change()

        assert change.schema_version == "persona_growth_field_change_v1"
        assert change.field_path == "core_traits.warmth"
        assert change.requires_user_review is True
        assert change.blocks_approval is False
        assert change.numeric_delta == 0.04

    @pytest.mark.parametrize("field_path", ["identity.age_range", "safety_policy.no_deception"])
    def test_frozen_fields_are_rejected(self, field_path: str) -> None:
        module = _growth()

        with pytest.raises(ValidationError):
            module.PersonaGrowthFieldChange(
                field_path=field_path,
                old_value_summary="old",
                proposed_value_summary="new",
                change_reason="[SYNTHETIC] Unsafe frozen field change.",
            )

    def test_unknown_field_path_is_rejected(self) -> None:
        module = _growth()

        with pytest.raises(ValidationError):
            module.PersonaGrowthFieldChange(
                field_path="unknown.surface",
                old_value_summary="old",
                proposed_value_summary="new",
                change_reason="[SYNTHETIC] Unknown field.",
            )

    def test_single_numeric_delta_cannot_exceed_global_cap(self) -> None:
        module = _growth()

        with pytest.raises(ValidationError):
            module.PersonaGrowthFieldChange(
                field_path="core_traits.warmth",
                old_value_summary="0.62",
                proposed_value_summary="0.95",
                numeric_delta=0.21,
                change_reason="[SYNTHETIC] Too much movement.",
            )

    def test_jealousy_cannot_increase_by_default(self) -> None:
        module = _growth()

        with pytest.raises(ValidationError):
            module.PersonaGrowthFieldChange(
                field_path="core_traits.jealousy",
                old_value_summary="0.18",
                proposed_value_summary="0.19",
                numeric_delta=0.01,
                change_reason="[SYNTHETIC] Jealousy should not increase.",
            )

        decrease = module.PersonaGrowthFieldChange(
            field_path="core_traits.jealousy",
            old_value_summary="0.18",
            proposed_value_summary="0.15",
            numeric_delta=-0.03,
            change_reason="[SYNTHETIC] De-escalate jealousy.",
        )
        assert decrease.blocks_approval is False


class TestPersonaGrowthPatchCandidate:
    def test_patch_candidate_preserves_persona_version_and_never_auto_applies(self) -> None:
        module = _growth()
        persona = _card()
        memory = _factual_memory()
        evidence = PersonaGrowthEvidenceBundle.from_events(
            persona_id=persona.persona_id,
            events=[memory],
        )

        patch = module.PersonaGrowthPatchCandidate.from_persona_card(
            persona,
            trigger_type="memory_pattern",
            trigger_summary="[SYNTHETIC] User prefers warmer wording.",
            changes=[_safe_change(source_memory_ids=[memory.event_id])],
            evidence_bundle=evidence,
            user_facing_explanation=(
                "[SYNTHETIC] Propose slightly warmer replies based on repeated feedback."
            ),
        )

        assert patch.schema_version == "persona_growth_patch_candidate_v1"
        assert patch.patch_id.startswith("pgpatch_")
        assert patch.user_id == persona.user_id
        assert patch.persona_id == persona.persona_id
        assert patch.source_persona_version == persona.version
        assert patch.evidence_memory_ids == [memory.event_id]
        assert patch.review_required is True
        assert patch.auto_apply_allowed is False
        assert patch.writes_persona_version is False
        assert patch.patch_status == "candidate"

    def test_weekly_trait_movement_cannot_exceed_persona_policy_cap(self) -> None:
        module = _growth()
        persona = _card()

        with pytest.raises(ValidationError):
            module.PersonaGrowthPatchCandidate.from_persona_card(
                persona,
                trigger_type="memory_pattern",
                trigger_summary="[SYNTHETIC] Warmth already moved this week.",
                changes=[_safe_change(numeric_delta=0.03, proposed_value_summary="0.65")],
                user_facing_explanation="[SYNTHETIC] Too much weekly warmth movement.",
                weekly_trait_delta_by_field={"core_traits.warmth": 0.03},
            )

    def test_blocking_safety_labels_block_approval(self) -> None:
        module = _growth()
        persona = _card()
        risky_change = _safe_change(
            risk_labels=["dependency_language", "real_person_similarity"],
            change_reason="[SYNTHETIC] Unsafe dependency-like growth.",
        )
        patch = module.PersonaGrowthPatchCandidate.from_persona_card(
            persona,
            trigger_type="memory_pattern",
            trigger_summary="[SYNTHETIC] Unsafe growth.",
            changes=[risky_change],
            user_facing_explanation="[SYNTHETIC] Unsafe growth should not approve.",
        )

        assert patch.blocking_risk_labels == ["dependency_language", "real_person_similarity"]
        with pytest.raises(ValidationError):
            module.PersonaGrowthPatchReview.from_patch(
                patch,
                reviewer_id="reviewer_synthetic",
                decision="approve_for_manual_apply",
            )

        rejected = module.PersonaGrowthPatchReview.from_patch(
            patch,
            reviewer_id="reviewer_synthetic",
            decision="reject",
        )
        assert rejected.writes_persona_version is False

    def test_blocked_or_non_approved_patch_states_do_not_write_versions(self) -> None:
        module = _growth()
        persona = _card()

        for patch_status in ("rejected", "frozen", "needs_changes", "archived"):
            patch = module.PersonaGrowthPatchCandidate.from_persona_card(
                persona,
                trigger_type="reviewer_note",
                trigger_summary="[SYNTHETIC] Non-approved patch state.",
                changes=[_safe_change()],
                user_facing_explanation="[SYNTHETIC] Non-approved patches do not apply.",
                patch_status=patch_status,
            )
            assert patch.auto_apply_allowed is False
            assert patch.writes_persona_version is False

    def test_imagined_memory_cannot_justify_factual_identity_changes(self) -> None:
        module = _growth()
        persona = _card()
        imagined = _imagined_memory()
        evidence = PersonaGrowthEvidenceBundle.from_events(
            persona_id=persona.persona_id,
            events=[imagined],
            evidence_purpose="factual_persona_growth",
        )

        assert evidence.blocked_memory_ids == [imagined.event_id]
        with pytest.raises(ValidationError):
            module.PersonaGrowthFieldChange(
                field_path="identity.display_name",
                old_value_summary="Lin Qi",
                proposed_value_summary="Dream Nickname",
                change_reason="[SYNTHETIC] Imagined memory cannot change factual identity.",
                source_memory_ids=evidence.blocked_memory_ids,
            )


class TestPersonaGrowthReviewAndJournal:
    def test_review_records_do_not_write_persona_versions_directly(self) -> None:
        module = _growth()
        persona = _card()
        patch = module.PersonaGrowthPatchCandidate.from_persona_card(
            persona,
            trigger_type="user_preference",
            trigger_summary="[SYNTHETIC] User asks for warmer replies.",
            changes=[_safe_change()],
            user_facing_explanation="[SYNTHETIC] Slight warmth adjustment.",
        )

        review = module.PersonaGrowthPatchReview.from_patch(
            patch,
            reviewer_id="reviewer_synthetic",
            decision="approve_for_manual_apply",
            decision_notes=["[SYNTHETIC] Approved for later manual apply."],
        )

        assert review.auto_apply_allowed is False
        assert review.writes_persona_version is False
        assert review.approved_field_paths == ["core_traits.warmth"]

    def test_journal_entry_records_manual_apply_reference_without_writing_versions(self) -> None:
        module = _growth()

        journal = module.PersonaGrowthJournalEntry(
            persona_id="persona_synthetic",
            source_patch_id="pgpatch_synthetic",
            source_version_id="persona_synthetic_v2",
            summary="[SYNTHETIC] Warmer replies were approved and manually applied.",
            changed_field_paths=["core_traits.warmth"],
            safety_warnings=[],
        )

        assert journal.schema_version == "persona_growth_journal_entry_v1"
        assert journal.journal_id.startswith("pgjournal_")
        assert journal.writes_persona_version is False


class TestPersonaGrowthForbiddenSurface:
    def test_models_forbid_extra_private_provider_outbound_and_media_fields(self) -> None:
        module = _growth()

        with pytest.raises(ValidationError):
            module.PersonaGrowthPatchCandidate(
                user_id="user_synthetic",
                persona_id="persona_synthetic",
                source_persona_version=1,
                trigger_type="memory_pattern",
                trigger_summary="[SYNTHETIC] Extra field should fail.",
                changes=[_safe_change()],
                user_facing_explanation="[SYNTHETIC] Extra field should fail.",
                provider_credentials="secret",
            )

        forbidden_field_names = {
            "raw_private_text",
            "full_transcript",
            "provider_credentials",
            "platform_recipient_id",
            "send_queue",
            "schedule",
            "webhook",
            "token",
            "microphone_prompt",
            "camera_prompt",
            "audio_bytes",
            "image_bytes",
            "video_bytes",
        }
        for model in (
            module.PersonaGrowthFieldChange,
            module.PersonaGrowthPatchCandidate,
            module.PersonaGrowthPatchReview,
            module.PersonaGrowthJournalEntry,
        ):
            assert forbidden_field_names.isdisjoint(model.model_fields)

    def test_candidate_objects_do_not_expose_runtime_or_delivery_methods(self) -> None:
        module = _growth()
        change = _safe_change()

        for method_name in (
            "send",
            "schedule",
            "deliver",
            "call_provider",
            "open_webhook",
            "mutate_persona",
            "apply_to_persona_card",
            "write_version",
            "run_runtime",
            "capture_microphone",
            "capture_camera",
            "generate_audio",
            "generate_image",
            "generate_video",
        ):
            assert not hasattr(change, method_name)
