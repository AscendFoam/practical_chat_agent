"""T312 Consent Center data model tests.

All records are synthetic. These tests define local consent/data-rights state
only; they do not capture real consent, mutate data, call an LLM, or enable
external/platform behavior.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone

from practical_chat_agent.core.models import (
    ConsentCenterState,
    ConsentFeatureScope,
    ConsentGrantRecord,
    ConsentWithdrawalRecord,
    DataRightsRequestRecord,
)


def _grant(feature_scope: ConsentFeatureScope, **overrides: object) -> ConsentGrantRecord:
    data: dict[str, object] = {
        "user_id": "user_synthetic",
        "feature_scope": feature_scope,
        "policy_version": "policy_v1",
        "actor_id": "user_synthetic",
        "granted_at": datetime(2026, 1, 1, tzinfo=timezone.utc),
        "evidence_refs": ["synthetic_consent_event_001"],
    }
    data.update(overrides)
    return ConsentGrantRecord(**data)


def test_consent_grant_is_feature_specific_versioned_actor_attributed_and_timestamped() -> None:
    memory = _grant("memory")
    persona = _grant("persona_distillation")

    assert memory.schema_version == "consent_grant_record_v1"
    assert memory.grant_id.startswith("consentgrant_")
    assert memory.user_id == "user_synthetic"
    assert memory.feature_scope == "memory"
    assert memory.policy_version == "policy_v1"
    assert memory.actor_id == "user_synthetic"
    assert memory.granted is True
    assert memory.granted_at == datetime(2026, 1, 1, tzinfo=timezone.utc)
    assert persona.feature_scope == "persona_distillation"
    assert persona.feature_scope != memory.feature_scope


def test_withdrawal_supersedes_prior_grants_for_same_feature_scope() -> None:
    memory = _grant("memory")
    proactive = _grant("proactive_messaging")
    withdrawal = ConsentWithdrawalRecord(
        user_id="user_synthetic",
        feature_scope="proactive_messaging",
        supersedes_grant_ids=[proactive.grant_id],
        actor_id="user_synthetic",
        reason="Synthetic user withdrew proactive permission.",
        withdrawn_at=datetime(2026, 1, 2, tzinfo=timezone.utc),
    )

    state = ConsentCenterState(
        user_id="user_synthetic",
        grants=[memory, proactive],
        withdrawals=[withdrawal],
    )

    assert state.schema_version == "consent_center_state_v1"
    assert state.has_active_consent("memory") is True
    assert state.has_active_consent("proactive_messaging") is False
    assert state.active_feature_scopes == ["memory"]
    assert state.withdrawn_feature_scopes == ["proactive_messaging"]


def test_required_feature_scopes_are_distinct() -> None:
    scopes: list[ConsentFeatureScope] = [
        "memory",
        "persona_distillation",
        "proactive_messaging",
        "aigc_export_share",
        "voice_avatar",
        "analytics",
        "model_improvement",
        "payment_marketing",
    ]
    grants = [_grant(scope) for scope in scopes]
    state = ConsentCenterState(user_id="user_synthetic", grants=grants)

    assert state.active_feature_scopes == scopes
    assert len(set(state.active_feature_scopes)) == len(scopes)


def test_minor_guardian_state_does_not_enable_minor_access_by_default() -> None:
    state = ConsentCenterState(
        user_id="minor_synthetic",
        is_minor=True,
        guardian_actor_id="guardian_synthetic",
    )

    assert state.is_minor is True
    assert state.guardian_actor_id == "guardian_synthetic"
    assert state.guardian_consent_required is True
    assert state.minor_access_allowed is False
    assert state.active_feature_scopes == []


def test_data_rights_requests_cover_access_correction_deletion_export_withdrawal_and_objection() -> None:
    request_types = [
        "access",
        "correction",
        "deletion",
        "export",
        "withdrawal",
        "objection",
    ]

    requests = [
        DataRightsRequestRecord(
            user_id="user_synthetic",
            request_type=request_type,
            status="received",
            actor_id="user_synthetic",
            reason=f"Synthetic {request_type} request.",
            target_scopes=["memory", "persona_distillation"],
        )
        for request_type in request_types
    ]

    assert [request.request_type for request in requests] == request_types
    for request in requests:
        assert request.schema_version == "data_rights_request_record_v1"
        assert request.request_id.startswith("datarights_")
        assert request.review_required is True
        assert request.status == "received"
        assert not hasattr(request, "execute")
        assert not hasattr(request, "apply")


def test_consent_center_payloads_have_no_raw_private_delivery_or_platform_fields() -> None:
    grant = _grant("aigc_export_share")
    withdrawal = ConsentWithdrawalRecord(
        user_id="user_synthetic",
        feature_scope="aigc_export_share",
        supersedes_grant_ids=[grant.grant_id],
        actor_id="user_synthetic",
        reason="Synthetic user withdrew share permission.",
    )
    state = ConsentCenterState(
        user_id="user_synthetic",
        grants=[grant],
        withdrawals=[withdrawal],
    )
    request = DataRightsRequestRecord(
        user_id="user_synthetic",
        request_type="export",
        status="in_review",
        actor_id="user_synthetic",
        reason="Synthetic export request.",
        target_scopes=["aigc_export_share"],
    )

    serialized = json.dumps(
        {
            "state": state.model_dump(mode="json"),
            "request": request.model_dump(mode="json"),
        },
        ensure_ascii=False,
    ).lower()

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
