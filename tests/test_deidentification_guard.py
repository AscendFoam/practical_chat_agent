"""T252 synthetic DeidentificationGuard tests.

All examples are fabricated. These tests define local guard behavior only; they
do not read private chat logs, call models, score real-person similarity, or
enable style extraction from private material.
"""

from __future__ import annotations

from practical_chat_agent.services.deidentification_guard import DeidentificationGuard


def _guard() -> DeidentificationGuard:
    return DeidentificationGuard()


class TestDeidentificationGuardAllowedAbstractStyle:
    def test_allows_generic_abstract_style_signals(self) -> None:
        decision = _guard().assess(
            "concise warm style, delayed response rhythm, dry humor, practical follow-up questions"
        )

        assert decision.allowed is True
        assert decision.risk_flags == []
        assert decision.blocked_reason is None
        assert decision.source_text_retained is False
        assert "concise" in decision.safe_summary
        assert "warm" in decision.safe_summary
        assert "delayed_response" in decision.safe_summary
        assert "dry_humor" in decision.safe_summary

    def test_returns_machine_readable_decision(self) -> None:
        decision = _guard().assess("warm concise style")
        dumped = decision.model_dump()

        assert dumped["schema_version"] == "deidentification_guard_decision_v1"
        assert dumped["allowed"] is True
        assert isinstance(dumped["risk_flags"], list)
        assert isinstance(dumped["safe_summary"], str)


class TestDeidentificationGuardBlocksIdentifiers:
    def test_blocks_direct_identifiers_and_handles(self) -> None:
        decision = _guard().assess(
            "Use Zhang Wei, phone 13800138000, address 12 River Road, "
            "@zhangwei, works at Northstar Robotics."
        )

        assert decision.allowed is False
        assert "direct_identifier" in decision.risk_flags
        assert "contact_identifier" in decision.risk_flags
        assert "location_identifier" in decision.risk_flags
        assert "org_school_identifier" in decision.risk_flags
        assert "handle_identifier" in decision.risk_flags
        assert "13800138000" not in decision.safe_summary
        assert "Zhang Wei" not in decision.safe_summary
        assert decision.blocked_reason is not None

    def test_blocks_voice_face_image_and_real_person_avatar_cues(self) -> None:
        decision = _guard().assess(
            "Keep her exact voice, copy the face photo, use an image likeness, "
            "and make a real-person avatar."
        )

        assert decision.allowed is False
        assert "voice_biometric" in decision.risk_flags
        assert "face_biometric" in decision.risk_flags
        assert "image_biometric" in decision.risk_flags
        assert "real_person_avatar" in decision.risk_flags
        assert "voice" not in decision.safe_summary
        assert "face" not in decision.safe_summary

    def test_blocks_exact_biography_and_private_event_reconstruction(self) -> None:
        decision = _guard().assess(
            "She broke up with me at West Lake on 2024-02-14 after our three-year "
            "relationship; reconstruct that private event and exact biography."
        )

        assert decision.allowed is False
        assert "private_event" in decision.risk_flags
        assert "exact_biography" in decision.risk_flags
        assert "West Lake" not in decision.safe_summary
        assert "2024-02-14" not in decision.safe_summary

    def test_blocks_distinctive_catchphrase_when_clone_intent_is_present(self) -> None:
        decision = _guard().assess(
            "Make it talk exactly like this person and always say 'moon sugar knife' "
            "as their unique catchphrase."
        )

        assert decision.allowed is False
        assert "clone_intent" in decision.risk_flags
        assert "distinctive_catchphrase" in decision.risk_flags
        assert "moon sugar knife" not in decision.safe_summary


class TestDeidentificationGuardSurfaceArea:
    def test_guard_does_not_expose_private_or_runtime_methods(self) -> None:
        guard = _guard()

        for method_name in (
            "read_chat_history",
            "load_private_corpus",
            "score_similarity_against_private_source",
            "compile_persona",
            "send",
            "schedule",
            "deliver",
        ):
            assert not hasattr(guard, method_name)
