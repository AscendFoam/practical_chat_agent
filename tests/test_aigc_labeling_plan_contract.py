"""T313 AIGC labeling plan contract tests.

All records are synthetic. These tests define reusable labeling metadata only;
they do not publish, share, write export files, call LLMs, or connect to
external/platform services.
"""

from __future__ import annotations

import json

from practical_chat_agent.core.models import (
    AIGCContentModality,
    AIGCLabelingRequirement,
    AIGCProductSurface,
)


def _requirement(
    content_modality: AIGCContentModality,
    product_surface: AIGCProductSurface,
    **overrides: object,
) -> AIGCLabelingRequirement:
    data: dict[str, object] = {
        "user_id": "user_synthetic",
        "content_id": "content_synthetic_001",
        "content_modality": content_modality,
        "product_surface": product_surface,
        "source_refs": ["synthetic_source_001"],
    }
    data.update(overrides)
    return AIGCLabelingRequirement(**data)


def test_generated_modalities_have_distinct_label_requirements() -> None:
    modalities: list[AIGCContentModality] = [
        "text",
        "image",
        "audio",
        "video",
        "virtual_scene",
        "persona",
        "virtual_history",
        "role_dynamic_post",
        "export",
        "shared_content",
    ]

    requirements = [
        _requirement(modality, "web_demo" if modality == "text" else "shared_content")
        for modality in modalities
    ]

    assert [requirement.content_modality for requirement in requirements] == modalities
    assert len({requirement.content_modality for requirement in requirements}) == len(modalities)
    for requirement in requirements:
        assert requirement.schema_version == "aigc_labeling_requirement_v1"
        assert requirement.visible_label_required is True
        assert "ai_generated" in requirement.disclosure_labels
        assert "synthetic_content" in requirement.disclosure_labels
        assert "review_required" in requirement.disclosure_labels


def test_virtual_history_and_role_dynamic_posts_keep_imagined_not_real_world_labels() -> None:
    virtual_history = _requirement("virtual_history", "virtual_history")
    role_post = _requirement("role_dynamic_post", "role_dynamic_post")

    for requirement in (virtual_history, role_post):
        assert "imagined_content" in requirement.disclosure_labels
        assert "not_real_world_activity" in requirement.disclosure_labels
        assert requirement.review_required is True
        assert "AI-generated" in requirement.visible_label_text
        assert "imagined" in requirement.visible_label_text.lower()
        assert "not real-world" in requirement.visible_label_text.lower()
        assert "synthetic" in requirement.visible_label_text.lower()


def test_export_share_download_and_media_surfaces_require_metadata_labels() -> None:
    export = _requirement("export", "export_manifest")
    shared = _requirement("shared_content", "shared_content")
    voice_avatar = _requirement("audio", "voice_avatar")
    video = _requirement("video", "shared_content")

    for requirement in (export, shared, voice_avatar, video):
        assert requirement.metadata_label_required is True
        assert "implicit_metadata_label" in requirement.metadata_labels
        assert requirement.copy_download_export_share_requires_metadata is True


def test_labels_preserve_existing_role_dynamic_post_labels() -> None:
    requirement = AIGCLabelingRequirement.from_disclosure_labels(
        user_id="user_synthetic",
        content_id="rolepost_synthetic_001",
        content_modality="role_dynamic_post",
        product_surface="role_dynamic_post",
        disclosure_labels=[
            "ai_generated",
            "imagined_content",
            "review_required",
            "not_real_world_activity",
        ],
        source_refs=["rolepost_synthetic_001"],
    )

    assert requirement.disclosure_labels == [
        "ai_generated",
        "synthetic_content",
        "imagined_content",
        "review_required",
        "not_real_world_activity",
    ]
    assert requirement.source_refs == ["rolepost_synthetic_001"]


def test_aigc_labeling_payload_has_no_raw_private_delivery_or_platform_fields() -> None:
    requirement = _requirement("shared_content", "shared_content")

    serialized = json.dumps(requirement.model_dump(mode="json"), ensure_ascii=False).lower()

    for forbidden in (
        "raw_text",
        "raw_transcript",
        "chat_history",
        "private_messages",
        "send",
        "schedule",
        "delivery",
        "platform",
        "webhook",
        "token",
        "queue",
    ):
        assert forbidden not in serialized
