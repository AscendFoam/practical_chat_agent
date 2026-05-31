"""T373 synthetic distillation input candidate tests.

All examples are synthetic. These tests do not read private chat history, call
LLMs, extract from real logs, synthesize personas, generate voice/avatar media,
schedule messages, or connect to external platforms.
"""

from __future__ import annotations

import importlib
from typing import Any

import pytest
from pydantic import ValidationError


def _distill() -> Any:
    try:
        return importlib.import_module("practical_chat_agent.services.synthetic_distillation_input")
    except ModuleNotFoundError as exc:
        pytest.fail(f"synthetic_distillation_input module is missing: {exc}")


def _subject_alias() -> Any:
    module = _distill()
    return module.SyntheticSpeakerAlias(
        speaker_alias="STYLE_SUBJECT_A",
        speaker_role="style_subject",
        is_target_style_subject=True,
    )


def _third_party_alias() -> Any:
    module = _distill()
    return module.SyntheticSpeakerAlias(
        speaker_alias="THIRD_PARTY_B",
        speaker_role="third_party",
        is_target_style_subject=False,
    )


def _segment(**overrides: object) -> Any:
    module = _distill()
    data: dict[str, object] = {
        "speaker_alias": "STYLE_SUBJECT_A",
        "segment_kind": "message",
        "synthetic_text": "[SYNTHETIC] concise warm reply with dry humor",
        "source_ref": "synthetic_segment_001",
        "allowed_feature_families": ["tone", "length", "humor"],
    }
    data.update(overrides)
    return module.SyntheticDistillationSourceSegment(**data)


def _active_distillation_consent() -> Any:
    module = _distill()
    return module.DistillationConsentRef(
        feature_scope="persona_distillation",
        policy_version="synthetic_policy_v1",
        actor_type="user",
        granted=True,
        withdrawn=False,
        evidence_ref="synthetic_consent_ref_001",
    )


def _safe_clone_decision() -> Any:
    module = _distill()
    return module.CloneRiskDecision.from_flags(
        manifest_id="manifest_synthetic",
        risk_flags=[],
    )


class TestSyntheticSourceSegments:
    def test_source_segment_requires_synthetic_marker_and_no_raw_private_text(self) -> None:
        segment = _segment()

        assert segment.schema_version == "synthetic_distillation_source_segment_v1"
        assert segment.segment_id.startswith("sdseg_")
        assert segment.synthetic_text.startswith("[SYNTHETIC]")
        assert segment.contains_raw_private_text is False
        assert segment.modality == "text"

        module = _distill()
        with pytest.raises(ValidationError):
            module.SyntheticDistillationSourceSegment(
                speaker_alias="STYLE_SUBJECT_A",
                segment_kind="message",
                synthetic_text="missing marker",
                source_ref="synthetic_segment_002",
            )

        with pytest.raises(ValidationError):
            module.SyntheticDistillationSourceSegment(
                speaker_alias="STYLE_SUBJECT_A",
                segment_kind="message",
                synthetic_text="[SYNTHETIC] unsafe raw marker",
                source_ref="synthetic_segment_003",
                contains_raw_private_text=True,
            )

    def test_source_segment_rejects_private_paths_and_media_references(self) -> None:
        module = _distill()

        with pytest.raises(ValidationError):
            module.SyntheticDistillationSourceSegment(
                speaker_alias="STYLE_SUBJECT_A",
                segment_kind="message",
                synthetic_text="[SYNTHETIC] copied from private/chat_history/a.txt",
                source_ref="synthetic_segment_004",
            )

        with pytest.raises(ValidationError):
            module.SyntheticDistillationSourceSegment(
                speaker_alias="STYLE_SUBJECT_A",
                segment_kind="message",
                synthetic_text="[SYNTHETIC] voice sample attached",
                source_ref="synthetic_segment_005",
            )


class TestSpeakerAliasesAndConsent:
    def test_speaker_aliases_replace_real_identity_and_minimize_third_parties(self) -> None:
        module = _distill()
        subject = _subject_alias()
        third_party = _third_party_alias()

        assert subject.real_identity_retained is False
        assert subject.third_party_minimized is False
        assert third_party.third_party_minimized is True

        with pytest.raises(ValidationError):
            module.SyntheticSpeakerAlias(
                speaker_alias="REAL_PERSON_ALICE",
                speaker_role="style_subject",
                is_target_style_subject=True,
                real_identity_retained=True,
            )

    def test_voice_avatar_consent_cannot_be_granted_in_text_distillation_scope(self) -> None:
        module = _distill()

        with pytest.raises(ValidationError):
            module.DistillationConsentRef(
                feature_scope="voice_avatar",
                policy_version="synthetic_policy_v1",
                actor_type="user",
                granted=True,
                withdrawn=False,
                evidence_ref="synthetic_voice_consent",
            )

    def test_withdrawn_consent_blocks_manifest_feature_extraction(self) -> None:
        module = _distill()
        withdrawn = module.DistillationConsentRef(
            feature_scope="persona_distillation",
            policy_version="synthetic_policy_v1",
            actor_type="user",
            granted=False,
            withdrawn=True,
            evidence_ref="synthetic_withdrawal_ref",
        )
        manifest = module.SyntheticDistillationInputManifest(
            user_id="user_synthetic",
            input_mode="synthetic_chat_segments",
            consent_refs=[withdrawn],
            speaker_map=[_subject_alias(), _third_party_alias()],
            segments=[_segment()],
            redaction_refs=[],
            clone_risk_decision=_safe_clone_decision(),
        )

        assert manifest.review_required is True
        assert not manifest.is_feature_extraction_allowed()
        assert "withdrawn_consent" in manifest.blocking_reasons


class TestCloneRiskDecision:
    @pytest.mark.parametrize(
        "risk_flag",
        [
            "voice_biometric",
            "face_biometric",
            "ex_partner",
            "family_member",
            "deceased_person",
            "public_figure",
            "hidden_impersonation",
            "minor_risk",
        ],
    )
    def test_high_risk_flags_block_safe_transformation(self, risk_flag: str) -> None:
        module = _distill()

        decision = module.CloneRiskDecision.from_flags(
            manifest_id="manifest_synthetic",
            risk_flags=[risk_flag],
        )

        assert decision.schema_version == "clone_risk_decision_v1"
        assert decision.risk_level == "blocked"
        assert decision.decision == "block"
        assert decision.safe_transformation_allowed is False
        assert risk_flag in decision.risk_flags


class TestStyleFeatureCandidates:
    def test_style_feature_candidate_uses_abstract_label_not_raw_quote(self) -> None:
        module = _distill()

        feature = module.DeidentifiedStyleFeatureCandidate(
            manifest_id="manifest_synthetic",
            feature_family="tone",
            feature_label="warm",
            value_summary="[SYNTHETIC] Warm and concise style.",
            confidence=0.82,
            evidence_segment_ids=["sdseg_synthetic"],
            source_speaker_aliases=["STYLE_SUBJECT_A"],
        )

        assert feature.schema_version == "deidentified_style_feature_candidate_v1"
        assert feature.feature_id.startswith("sdfeat_")
        assert feature.source_text_retained is False
        assert feature.review_required is True

        with pytest.raises(ValidationError):
            module.DeidentifiedStyleFeatureCandidate(
                manifest_id="manifest_synthetic",
                feature_family="identity",
                feature_label="real name",
                value_summary="[SYNTHETIC] Should not extract identity.",
                evidence_segment_ids=["sdseg_synthetic"],
                source_speaker_aliases=["STYLE_SUBJECT_A"],
            )

        with pytest.raises(ValidationError):
            module.DeidentifiedStyleFeatureCandidate(
                manifest_id="manifest_synthetic",
                feature_family="tone",
                feature_label='"exact private phrase"',
                value_summary="[SYNTHETIC] Should not retain quotes.",
                evidence_segment_ids=["sdseg_synthetic"],
                source_speaker_aliases=["STYLE_SUBJECT_A"],
            )

        with pytest.raises(ValidationError):
            module.DeidentifiedStyleFeatureCandidate(
                manifest_id="manifest_synthetic",
                feature_family="tone",
                feature_label="warm",
                value_summary="[SYNTHETIC] Should not retain source text.",
                evidence_segment_ids=["sdseg_synthetic"],
                source_speaker_aliases=["STYLE_SUBJECT_A"],
                source_text_retained=True,
            )


class TestFictionalPersonaSynthesisInput:
    def test_fictional_persona_input_is_review_required_and_never_runtime_ready(self) -> None:
        module = _distill()

        synthesis_input = module.FictionalPersonaSynthesisInput(
            manifest_id="manifest_synthetic",
            style_feature_ids=["sdfeat_001"],
        )

        assert synthesis_input.schema_version == "fictional_persona_synthesis_input_v1"
        assert synthesis_input.input_id.startswith("sdpinput_")
        assert synthesis_input.review_required is True
        assert synthesis_input.runtime_ready is False
        assert "ai_generated" in synthesis_input.required_disclosures
        assert "fictional" in synthesis_input.required_disclosures
        assert "deidentified" in synthesis_input.required_disclosures
        assert "names" in synthesis_input.must_not_include
        assert "voices" in synthesis_input.must_not_include


class TestSyntheticDistillationManifest:
    def test_safe_manifest_allows_l2_review_only(self) -> None:
        module = _distill()
        decision = module.CloneRiskDecision.from_flags(
            manifest_id="manifest_synthetic",
            risk_flags=[],
        )

        manifest = module.SyntheticDistillationInputManifest(
            manifest_id="manifest_synthetic",
            user_id="user_synthetic",
            input_mode="synthetic_chat_segments",
            consent_refs=[_active_distillation_consent()],
            speaker_map=[_subject_alias(), _third_party_alias()],
            segments=[_segment()],
            redaction_refs=[],
            clone_risk_decision=decision,
        )

        assert manifest.target_mode == "deidentified_style_inspiration"
        assert manifest.output_intent == "new_fictional_persona"
        assert manifest.review_required is True
        assert manifest.is_feature_extraction_allowed()

    def test_user_supplied_future_source_category_is_not_runtime_allowed(self) -> None:
        module = _distill()

        with pytest.raises(ValidationError):
            module.SyntheticDistillationInputManifest(
                user_id="user_synthetic",
                input_mode="synthetic_chat_segments",
                source_category="user_supplied_future",
                consent_refs=[_active_distillation_consent()],
                speaker_map=[_subject_alias()],
                segments=[_segment()],
                redaction_refs=[],
                clone_risk_decision=_safe_clone_decision(),
            )


class TestSyntheticDistillationForbiddenSurface:
    def test_models_forbid_extra_private_provider_outbound_and_media_fields(self) -> None:
        module = _distill()

        with pytest.raises(ValidationError):
            module.SyntheticDistillationInputManifest(
                user_id="user_synthetic",
                input_mode="synthetic_chat_segments",
                consent_refs=[_active_distillation_consent()],
                speaker_map=[_subject_alias()],
                segments=[_segment()],
                redaction_refs=[],
                clone_risk_decision=_safe_clone_decision(),
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
            module.SyntheticDistillationInputManifest,
            module.SyntheticDistillationSourceSegment,
            module.SyntheticSpeakerAlias,
            module.DistillationConsentRef,
            module.DistillationRedactionRef,
            module.DeidentifiedStyleFeatureCandidate,
            module.CloneRiskDecision,
            module.FictionalPersonaSynthesisInput,
        ):
            assert forbidden_field_names.isdisjoint(model.model_fields)

    def test_candidate_objects_do_not_expose_runtime_or_delivery_methods(self) -> None:
        module = _distill()
        manifest = module.SyntheticDistillationInputManifest(
            user_id="user_synthetic",
            input_mode="synthetic_chat_segments",
            consent_refs=[_active_distillation_consent()],
            speaker_map=[_subject_alias()],
            segments=[_segment()],
            redaction_refs=[],
            clone_risk_decision=_safe_clone_decision(),
        )

        for method_name in (
            "send",
            "schedule",
            "deliver",
            "call_provider",
            "open_webhook",
            "synthesize_persona",
            "read_private_chat",
            "generate_voice",
            "generate_avatar",
            "generate_audio",
            "generate_image",
            "generate_video",
        ):
            assert not hasattr(manifest, method_name)
