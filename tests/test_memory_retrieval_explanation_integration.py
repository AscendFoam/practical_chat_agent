"""T374 memory retrieval and explanation integration tests.

All records are synthetic. These tests do not read private chat history, call
LLMs, rank vector search, mutate stores, generate replies, schedule messages,
or connect to external platforms.
"""

from __future__ import annotations

import importlib
from typing import Any

import pytest

from practical_chat_agent.core.models import MemoryEvent, MemoryProvenance
from practical_chat_agent.services.memory_event_store import MemoryEventStore
from practical_chat_agent.services.persona_compiler import PersonaCompilerService
from practical_chat_agent.services.synthetic_distillation_input import DeidentifiedStyleFeatureCandidate


def _integration() -> Any:
    try:
        return importlib.import_module("practical_chat_agent.services.memory_retrieval_explanation")
    except ModuleNotFoundError as exc:
        pytest.fail(f"memory_retrieval_explanation module is missing: {exc}")


def _service() -> Any:
    return _integration().MemoryRetrievalExplanationService()


def _provenance(**overrides: object) -> MemoryProvenance:
    data: dict[str, object] = {
        "source_type": "synthetic_test",
        "evidence_refs": ["synthetic_event_001"],
    }
    data.update(overrides)
    return MemoryProvenance(**data)


def _factual(**overrides: object) -> MemoryEvent:
    data: dict[str, object] = {
        "user_id": "user_synthetic",
        "event_type": "factual",
        "truth_status": "evidence_backed",
        "summary": "[SYNTHETIC] User prefers concise check-ins.",
        "provenance": _provenance(),
        "sensitivity": "low",
    }
    data.update(overrides)
    return MemoryEvent(**data)


def _imagined() -> MemoryEvent:
    return MemoryEvent(
        user_id="user_synthetic",
        event_type="imagined",
        truth_status="imagined",
        summary="[SYNTHETIC] Fictional persona imagined a quiet bookstore.",
        provenance=MemoryProvenance(source_type="imagined_generation"),
        sensitivity="low",
        imagined_context_label="virtual_life",
    )


def _persona():
    return PersonaCompilerService().compile(
        {
            "user_id": "user_synthetic",
            "display_name": "Lin Qi",
            "creation_mode": "detailed_prompt",
            "description": "fictional calm concise companion with dry humor",
        }
    )


class TestRetrievalEligibilityAndExplanation:
    def test_imagined_memory_is_excluded_from_factual_response_bundle(self) -> None:
        factual = _factual()
        imagined = _imagined()

        result = _service().build_bundle(
            [factual, imagined],
            purpose="factual_response",
            query_summary="answer with factual memory only",
        )

        assert result.bundle.selected_memory_ids == [factual.event_id]
        assert result.bundle.excluded_memory_ids == [imagined.event_id]
        assert result.bundle.exclusion_reasons[imagined.event_id] == (
            "imagined_memory_excluded_from_factual_response"
        )
        excluded_trace = result.trace_by_memory_id(imagined.event_id)
        assert excluded_trace.included is False
        assert excluded_trace.reason == "imagined_memory_excluded_from_factual_response"

    @pytest.mark.parametrize("lifecycle_state", ["deleted", "frozen", "archived", "superseded"])
    def test_inactive_or_superseded_memory_is_excluded(self, lifecycle_state: str) -> None:
        event = _factual(lifecycle_state=lifecycle_state)

        result = _service().build_bundle(
            [event],
            purpose="factual_response",
            query_summary="answer with active memory only",
        )

        assert result.bundle.selected_memory_ids == []
        assert result.bundle.excluded_memory_ids == [event.event_id]
        assert result.bundle.exclusion_reasons[event.event_id] == f"{lifecycle_state}_memory_excluded"

    def test_review_required_memory_is_excluded_outside_review_surface(self) -> None:
        event = _factual(sensitivity="high")

        result = _service().build_bundle(
            [event],
            purpose="factual_response",
            query_summary="answer without sensitive review memory",
        )

        assert result.bundle.selected_memory_ids == []
        assert result.bundle.exclusion_reasons[event.event_id] == "review_required_memory_excluded"
        assert "review_required" in result.trace_by_memory_id(event.event_id).safety_warnings

    def test_review_required_memory_cannot_be_forced_into_factual_response(self) -> None:
        event = _factual(sensitivity="high")

        result = _service().build_bundle(
            [event],
            purpose="factual_response",
            query_summary="answer without sensitive review memory",
            include_review_required=True,
        )

        assert result.bundle.selected_memory_ids == []
        assert result.bundle.exclusion_reasons[event.event_id] == "review_required_memory_excluded"

    def test_withdrawn_consent_excludes_memory_and_creates_deletion_cascade_plan(self) -> None:
        event = _factual()

        result = _service().build_bundle(
            [event],
            purpose="factual_response",
            query_summary="answer after consent withdrawal",
            withdrawn_memory_ids={event.event_id},
        )

        assert result.bundle.selected_memory_ids == []
        assert result.bundle.exclusion_reasons[event.event_id] == "withdrawn_consent"
        assert result.deletion_cascade_plan is not None
        assert result.deletion_cascade_plan.trigger_type == "consent_withdrawal"
        assert result.deletion_cascade_plan.target_memory_ids == [event.event_id]


class TestGovernanceCandidateIntegration:
    def test_contradiction_candidate_does_not_overwrite_memory(self, tmp_path: Any) -> None:
        old_event = _factual(summary="[SYNTHETIC] User prefers short replies.")
        new_event = _factual(summary="[SYNTHETIC] User now prefers detailed replies.")
        store = MemoryEventStore(tmp_path / "memory_events.json")
        store.append(old_event)
        store.append(new_event)

        candidate = _service().create_contradiction_candidate(
            [old_event, new_event],
            safe_summary="[SYNTHETIC] Reply length preference changed.",
        )

        assert candidate.review_required is True
        assert candidate.memory_ids == [old_event.event_id, new_event.event_id]
        assert store.get(old_event.event_id).summary == old_event.summary

    def test_supersession_candidate_does_not_mutate_lifecycle(self, tmp_path: Any) -> None:
        source = _factual(summary="[SYNTHETIC] User prefers short replies.")
        replacement = _factual(summary="[SYNTHETIC] User now prefers detailed replies.")
        store = MemoryEventStore(tmp_path / "memory_events.json")
        store.append(source)
        store.append(replacement)

        candidate = _service().create_supersession_candidate(
            source_memory_id=source.event_id,
            replacement_memory_id=replacement.event_id,
            reason="[SYNTHETIC] Newer preference should be reviewed.",
        )

        assert candidate.applies_lifecycle_update is False
        assert store.get(source.event_id).lifecycle_state == "active"


class TestPersonaAndDistillationIntegration:
    def test_persona_growth_evidence_uses_only_eligible_memory_and_does_not_mutate_persona(self) -> None:
        persona = _persona()
        before = persona.model_dump(mode="json")
        factual = _factual()
        imagined = _imagined()

        evidence = _service().prepare_persona_growth_evidence(
            persona_id=persona.persona_id,
            events=[factual, imagined],
        )

        assert evidence.memory_ids == [factual.event_id]
        assert evidence.blocked_memory_ids == [imagined.event_id]
        assert persona.model_dump(mode="json") == before

    def test_synthetic_distillation_features_remain_review_only(self) -> None:
        feature = DeidentifiedStyleFeatureCandidate(
            manifest_id="manifest_synthetic",
            feature_family="tone",
            feature_label="warm",
            value_summary="[SYNTHETIC] Warm concise style.",
            evidence_segment_ids=["sdseg_001"],
            source_speaker_aliases=["STYLE_SUBJECT_A"],
        )

        assert _service().is_distillation_feature_review_only(feature)
        assert feature.review_required is True
        assert feature.source_text_retained is False


class TestExplanationSurfaceAndForbiddenFields:
    def test_included_memory_trace_preserves_reason_and_provenance_refs(self) -> None:
        event = _factual()

        result = _service().build_bundle(
            [event],
            purpose="factual_response",
            query_summary="answer with factual memory",
        )
        trace = result.trace_by_memory_id(event.event_id)

        assert trace.included is True
        assert trace.reason == "included_for_factual_response"
        assert trace.provenance_refs == ["synthetic_event_001"]

    def test_helper_result_has_no_private_provider_outbound_or_media_fields(self) -> None:
        result = _service().build_bundle(
            [_factual(), _imagined()],
            purpose="factual_response",
            query_summary="inspect forbidden fields",
        )
        serialized = result.model_dump_json().lower()

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
            "generate_reply",
            "mutate_store",
            "apply_persona_growth",
            "synthesize_persona",
            "generate_voice",
            "generate_avatar",
            "generate_audio",
            "generate_image",
            "generate_video",
        ):
            assert not hasattr(service, method_name)
