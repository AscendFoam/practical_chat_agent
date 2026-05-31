"""T380 synthetic distillation review readiness tests.

All examples are synthetic. These tests do not read private chat history, call
LLMs, retain source text, synthesize personas, generate media, send messages,
or connect to external platforms.
"""

from __future__ import annotations

import importlib
from typing import Any

import pytest
from pydantic import ValidationError

from practical_chat_agent.services.review_queue import ReviewQueueService
from practical_chat_agent.services.synthetic_distillation_input import (
    CloneRiskDecision,
    DeidentifiedStyleFeatureCandidate,
    DistillationConsentRef,
    SyntheticDistillationInputManifest,
    SyntheticDistillationSourceSegment,
    SyntheticSpeakerAlias,
)


def _readiness() -> Any:
    try:
        return importlib.import_module("practical_chat_agent.services.distillation_review_readiness")
    except ModuleNotFoundError as exc:
        pytest.fail(f"distillation_review_readiness module is missing: {exc}")


def _service() -> Any:
    return _readiness().DistillationReviewReadinessService()


def _consent(*, granted: bool = True, withdrawn: bool = False) -> DistillationConsentRef:
    return DistillationConsentRef(
        feature_scope="persona_distillation",
        policy_version="synthetic_policy_v1",
        actor_type="user",
        granted=granted,
        withdrawn=withdrawn,
        evidence_ref="synthetic_consent_ref_001",
    )


def _segment() -> SyntheticDistillationSourceSegment:
    return SyntheticDistillationSourceSegment(
        speaker_alias="STYLE_SUBJECT_A",
        segment_kind="message",
        synthetic_text="[SYNTHETIC] concise warm reply with dry humor",
        source_ref="synthetic_segment_001",
        allowed_feature_families=["tone", "length", "humor"],
    )


def _manifest(
    *,
    consent_refs: list[DistillationConsentRef] | None = None,
    risk_flags: list[str] | None = None,
) -> SyntheticDistillationInputManifest:
    return SyntheticDistillationInputManifest(
        manifest_id="manifest_synthetic",
        user_id="user_synthetic",
        input_mode="synthetic_chat_segments",
        consent_refs=[_consent()] if consent_refs is None else consent_refs,
        speaker_map=[
            SyntheticSpeakerAlias(
                speaker_alias="STYLE_SUBJECT_A",
                speaker_role="style_subject",
                is_target_style_subject=True,
            )
        ],
        segments=[_segment()],
        clone_risk_decision=CloneRiskDecision.from_flags(
            manifest_id="manifest_synthetic",
            risk_flags=list(risk_flags or []),
        ),
    )


def _feature(**overrides: object) -> DeidentifiedStyleFeatureCandidate:
    data: dict[str, object] = {
        "manifest_id": "manifest_synthetic",
        "feature_family": "tone",
        "feature_label": "warm",
        "value_summary": "[SYNTHETIC] Warm concise style.",
        "confidence": 0.8,
        "evidence_segment_ids": ["sdseg_001"],
        "source_speaker_aliases": ["STYLE_SUBJECT_A"],
    }
    data.update(overrides)
    return DeidentifiedStyleFeatureCandidate(**data)


class TestDistillationReviewReadiness:
    def test_active_synthetic_manifest_and_safe_feature_are_review_ready(self) -> None:
        manifest = _manifest()
        feature = _feature()
        queue_service = ReviewQueueService()
        review_items = [
            queue_service.item_from_candidate(manifest),
            queue_service.item_from_candidate(feature),
        ]

        summary = _service().build_summary(
            manifest,
            features=[feature],
            review_items=review_items,
        )

        assert summary.manifest_id == manifest.manifest_id
        assert summary.feature_ids == [feature.feature_id]
        assert summary.review_queue_item_ids == [item.item_id for item in review_items]
        assert summary.ready_for_persona_synthesis is True
        assert summary.blocking_issue_codes == []
        assert summary.source_text_retained is False

    def test_withdrawn_consent_blocks_readiness(self) -> None:
        manifest = _manifest(consent_refs=[_consent(granted=False, withdrawn=True)])

        summary = _service().build_summary(manifest, features=[])

        assert summary.ready_for_persona_synthesis is False
        assert "withdrawn_consent" in summary.blocking_issue_codes
        assert "persona_distillation_consent_missing_or_withdrawn" in summary.blocking_issue_codes

    def test_clone_risk_block_prevents_readiness(self) -> None:
        manifest = _manifest(risk_flags=["ex_partner"])

        summary = _service().build_summary(manifest, features=[_feature()])

        assert summary.ready_for_persona_synthesis is False
        assert "clone_risk_blocked" in summary.blocking_issue_codes

    def test_retained_source_text_or_blocked_features_prevent_readiness(self) -> None:
        manifest = _manifest()
        retained_text_feature = DeidentifiedStyleFeatureCandidate.model_construct(
            schema_version="deidentified_style_feature_candidate_v1",
            feature_id="sdfeat_retained",
            manifest_id=manifest.manifest_id,
            feature_family="tone",
            feature_label="warm",
            value_summary="[SYNTHETIC] Warm concise style.",
            confidence=0.7,
            evidence_segment_ids=["sdseg_001"],
            source_speaker_aliases=["STYLE_SUBJECT_A"],
            source_text_retained=True,
            review_required=True,
            blocked_from_persona_synthesis=False,
            blocking_reasons=[],
        )
        blocked_feature = _feature(
            blocked_from_persona_synthesis=True,
            blocking_reasons=["identifier_or_third_party_review_required"],
        )

        summary = _service().build_summary(
            manifest,
            features=[retained_text_feature, blocked_feature],
        )

        assert summary.ready_for_persona_synthesis is False
        assert "source_text_retained" in summary.blocking_issue_codes
        assert "feature_blocked_from_persona_synthesis" in summary.blocking_issue_codes

    def test_missing_active_persona_distillation_consent_prevents_readiness(self) -> None:
        manifest = _manifest(consent_refs=[])

        summary = _service().build_summary(manifest, features=[_feature()])

        assert summary.ready_for_persona_synthesis is False
        assert "persona_distillation_consent_missing_or_withdrawn" in summary.blocking_issue_codes


class TestDistillationReviewReadinessSafetyBoundaries:
    def test_models_forbid_extra_private_provider_outbound_and_media_fields(self) -> None:
        module = _readiness()

        with pytest.raises(ValidationError):
            module.DistillationReadinessIssue(
                issue_code="withdrawn_consent",
                severity="blocker",
                safe_summary="[SYNTHETIC] Consent withdrawn.",
                provider_credentials="secret",
            )

        summary = _service().build_summary(_manifest(), features=[_feature()])
        serialized = summary.model_dump_json().lower()
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
        ):
            assert forbidden not in serialized

    def test_service_does_not_expose_runtime_or_delivery_methods(self) -> None:
        service = _service()

        for method_name in (
            "send",
            "schedule",
            "deliver",
            "call_provider",
            "open_webhook",
            "synthesize_persona",
            "generate_reply",
            "generate_voice",
            "generate_avatar",
            "generate_audio",
            "generate_image",
            "generate_video",
        ):
            assert not hasattr(service, method_name)
