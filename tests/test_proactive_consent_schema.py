"""T280 Proactive consent schema tests.

All inputs are synthetic. These tests define consent boundaries only; they do
not create proactive candidates, schedule messages, send messages, or connect
to external platforms.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from practical_chat_agent.core.models import ProactiveConsent


class TestProactiveConsent:
    def test_enabled_consent_records_review_only_local_boundaries(self) -> None:
        consent = ProactiveConsent(
            user_id="user_synthetic",
            status="enabled",
            allowed_surfaces=["in_app_review_card"],
            allowed_intents=["gentle_check_in", "shared_interest"],
            quiet_hours={"timezone": "Asia/Shanghai", "start": "22:00", "end": "08:00"},
            max_suggestions_per_day=2,
            min_interval_hours=6,
        )

        assert consent.schema_version == "proactive_consent_v1"
        assert consent.consent_id.startswith("proconsent_")
        assert consent.requires_human_review is True
        assert consent.allowed_surfaces == ["in_app_review_card"]
        assert consent.allowed_intents == ["gentle_check_in", "shared_interest"]
        assert consent.quiet_hours.timezone == "Asia/Shanghai"

    def test_rejects_outbound_or_platform_surfaces(self) -> None:
        for surface in (
            "wechat",
            "feishu",
            "push_notification",
            "sms",
            "email",
            "webhook",
        ):
            with pytest.raises(ValidationError):
                ProactiveConsent(
                    user_id="user_synthetic",
                    status="enabled",
                    allowed_surfaces=[surface],
                    allowed_intents=["gentle_check_in"],
                )

    def test_rejects_disabling_human_review(self) -> None:
        with pytest.raises(ValidationError):
            ProactiveConsent(
                user_id="user_synthetic",
                status="enabled",
                allowed_surfaces=["in_app_review_card"],
                allowed_intents=["gentle_check_in"],
                requires_human_review=False,
            )

    def test_rejects_negative_frequency_or_interval(self) -> None:
        with pytest.raises(ValidationError):
            ProactiveConsent(
                user_id="user_synthetic",
                status="enabled",
                allowed_surfaces=["in_app_review_card"],
                allowed_intents=["gentle_check_in"],
                max_suggestions_per_day=-1,
            )

        with pytest.raises(ValidationError):
            ProactiveConsent(
                user_id="user_synthetic",
                status="enabled",
                allowed_surfaces=["in_app_review_card"],
                allowed_intents=["gentle_check_in"],
                min_interval_hours=-1,
            )

    def test_enabled_consent_requires_low_pressure_intent(self) -> None:
        with pytest.raises(ValidationError):
            ProactiveConsent(
                user_id="user_synthetic",
                status="enabled",
                allowed_surfaces=["in_app_review_card"],
                allowed_intents=[],
            )

        with pytest.raises(ValidationError):
            ProactiveConsent(
                user_id="user_synthetic",
                status="enabled",
                allowed_surfaces=["in_app_review_card"],
                allowed_intents=["retention_nudge"],
            )

    def test_paused_and_revoked_consent_are_representable_without_runtime_enablement(self) -> None:
        paused = ProactiveConsent(
            user_id="user_synthetic",
            status="paused",
            allowed_surfaces=[],
            allowed_intents=[],
            pause_reasons=["user_requested_pause"],
        )
        revoked = ProactiveConsent(
            user_id="user_synthetic",
            status="revoked",
            allowed_surfaces=[],
            allowed_intents=[],
            revoked_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
        )

        assert paused.status == "paused"
        assert paused.pause_reasons == ["user_requested_pause"]
        assert revoked.status == "revoked"
        assert revoked.revoked_at is not None
        assert paused.requires_human_review is True
        assert revoked.requires_human_review is True

    def test_serialized_consent_has_no_delivery_or_platform_fields(self) -> None:
        consent = ProactiveConsent(
            user_id="user_synthetic",
            status="enabled",
            allowed_surfaces=["in_app_review_card"],
            allowed_intents=["gentle_check_in"],
        )
        serialized = json.dumps(consent.model_dump(mode="json"), ensure_ascii=False).lower()

        for forbidden in (
            "send",
            "schedule",
            "delivery",
            "platform",
            "webhook",
            "token",
            "queue",
        ):
            assert forbidden not in serialized
