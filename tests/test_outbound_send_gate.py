"""T221 outbound send-gate tests.

All fixtures are synthetic and review-safe. These tests cover deterministic
gate decisions only; they do not exercise adapters, scheduling, runtime loops,
or private transcript access.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

from practical_chat_agent.core.models import (
    OutboundMessagePayload,
    OutboundMessageRequest,
    OutboundRequestHumanApproval,
    OutboundRequestSendGate,
)
from practical_chat_agent.services.outbound_send_gate import (
    OutboundSendGate,
    OutboundSendGateConfig,
    OutboundSendGateContext,
)


def _approved_human_approval() -> OutboundRequestHumanApproval:
    return OutboundRequestHumanApproval(
        review_state="approved",
        approved_by_human=True,
        reviewer_id="reviewer_synthetic",
        reviewed_at=datetime(2026, 5, 28, 9, 0, tzinfo=timezone.utc),
        review_notes=["synthetic outbound approval"],
    )


def _request(**overrides: object) -> OutboundMessageRequest:
    data: dict[str, object] = {
        "contact_id": "contact_synthetic",
        "user_id": "user_synthetic",
        "source_type": "human_authored",
        "payload": OutboundMessagePayload(
            draft_text="Synthetic outbound draft for review.",
            safe_summary="Synthetic outbound draft summary.",
        ),
        "human_approval": _approved_human_approval(),
        "channel_preference": "feishu",
    }
    data.update(overrides)
    return OutboundMessageRequest(**data)


def _allowed_history_request(
    *,
    draft_text: str,
    evaluated_at: datetime,
    channel_preference: str = "feishu",
    contact_id: str = "contact_synthetic",
    user_id: str = "user_synthetic",
) -> OutboundMessageRequest:
    return _request(
        contact_id=contact_id,
        user_id=user_id,
        channel_preference=channel_preference,
        payload=OutboundMessagePayload(draft_text=draft_text),
        send_gate=OutboundRequestSendGate(
            gate_state="allowed",
            evaluator_id="send_gate_history",
            evaluated_at=evaluated_at,
            gate_notes=["historical gate allow"],
        ),
    )


def _config(**overrides: object) -> OutboundSendGateConfig:
    data: dict[str, object] = {
        "evaluator_id": "send_gate_t221",
        "manual_only_mode": True,
        "kill_switch_enabled": False,
        "quiet_hours_start": None,
        "quiet_hours_end": None,
        "timezone_name": "Asia/Shanghai",
        "frequency_limit_count": 0,
        "frequency_limit_window_seconds": 0,
        "duplicate_window_seconds": 0,
    }
    data.update(overrides)
    return OutboundSendGateConfig(**data)


class TestOutboundSendGateEvaluate:
    def test_allows_approved_request_and_returns_new_request_without_mutation(self) -> None:
        request = _request()
        gate = OutboundSendGate(config=_config())

        now = datetime(2026, 5, 28, 14, 30, tzinfo=ZoneInfo("Asia/Shanghai"))
        decision = gate.evaluate(request, now=now)

        assert decision.allowed is True
        assert decision.evaluated_request.is_sendable() is True
        assert decision.evaluated_request.send_gate.gate_state == "allowed"
        assert decision.evaluated_request.send_gate.evaluator_id == "send_gate_t221"
        assert decision.evaluated_request.send_gate.evaluated_at == now
        assert "gate_allowed" in decision.gate_notes
        assert request.send_gate.gate_state == "not_evaluated"
        assert decision.evaluated_request.contact_id == request.contact_id
        assert decision.evaluated_request.user_id == request.user_id
        assert decision.evaluated_request.channel_preference == "feishu"
        assert decision.evaluated_request.created_at == request.created_at

    def test_accepts_stable_mapping_input(self) -> None:
        request = _request()
        gate = OutboundSendGate(config=_config())

        decision = gate.evaluate(request.model_dump())

        assert decision.allowed is True
        assert decision.evaluated_request.is_sendable() is True

    def test_pending_human_approval_blocks_gate(self) -> None:
        request = _request(
            human_approval=OutboundRequestHumanApproval(),
        )
        gate = OutboundSendGate(config=_config())

        decision = gate.evaluate(request)

        assert decision.allowed is False
        assert decision.evaluated_request.is_sendable() is False
        assert decision.evaluated_request.send_gate.gate_state == "blocked"
        assert "human_approval_pending" in decision.blocked_reasons

    def test_rejected_human_approval_blocks_gate(self) -> None:
        request = _request(
            human_approval=OutboundRequestHumanApproval(
                review_state="rejected",
                approved_by_human=False,
                reviewer_id="reviewer_synthetic",
                reviewed_at=datetime(2026, 5, 28, 9, 0, tzinfo=timezone.utc),
                review_notes=["rejected for review"],
            ),
        )
        gate = OutboundSendGate(config=_config())

        decision = gate.evaluate(request)

        assert decision.allowed is False
        assert "human_approval_rejected" in decision.blocked_reasons

    def test_kill_switch_blocks_all_requests(self) -> None:
        gate = OutboundSendGate(config=_config(kill_switch_enabled=True))

        decision = gate.evaluate(_request())

        assert decision.allowed is False
        assert "kill_switch_enabled" in decision.blocked_reasons

    def test_whitespace_payload_is_blocked_defensively(self) -> None:
        gate = OutboundSendGate(config=_config())
        request = _request(payload=OutboundMessagePayload(draft_text="   "))

        decision = gate.evaluate(request)

        assert decision.allowed is False
        assert "empty_draft_text" in decision.blocked_reasons

    def test_quiet_hours_blocks_during_daytime_window(self) -> None:
        gate = OutboundSendGate(
            config=_config(
                quiet_hours_start="09:00",
                quiet_hours_end="18:00",
            ),
        )
        now = datetime(2026, 5, 28, 10, 30, tzinfo=ZoneInfo("Asia/Shanghai"))

        decision = gate.evaluate(_request(), now=now)

        assert decision.allowed is False
        assert "quiet_hours_blocked" in decision.blocked_reasons

    def test_quiet_hours_blocks_in_overnight_window(self) -> None:
        gate = OutboundSendGate(
            config=_config(
                quiet_hours_start="23:00",
                quiet_hours_end="08:00",
            ),
        )
        now = datetime(2026, 5, 28, 23, 30, tzinfo=ZoneInfo("Asia/Shanghai"))

        decision = gate.evaluate(_request(), now=now)

        assert decision.allowed is False
        assert "quiet_hours_blocked" in decision.blocked_reasons

    def test_quiet_hours_clear_note_is_recorded_outside_quiet_window(self) -> None:
        gate = OutboundSendGate(
            config=_config(
                quiet_hours_start="23:00",
                quiet_hours_end="08:00",
            ),
        )
        now = datetime(2026, 5, 28, 14, 30, tzinfo=timezone.utc)

        decision = gate.evaluate(_request(), now=now)

        assert decision.allowed is True
        assert "quiet_hours_clear" in decision.passed_checks

    def test_frequency_limit_blocks_excess_allowed_history(self) -> None:
        now = datetime(2026, 5, 28, 14, 30, tzinfo=timezone.utc)
        history = [
            _allowed_history_request(
                draft_text="older draft one",
                evaluated_at=now - timedelta(seconds=120),
            ),
            _allowed_history_request(
                draft_text="older draft two",
                evaluated_at=now - timedelta(seconds=60),
            ),
        ]
        gate = OutboundSendGate(
            config=_config(
                frequency_limit_count=2,
                frequency_limit_window_seconds=600,
            ),
        )

        decision = gate.evaluate(_request(), now=now, recent_requests=history)

        assert decision.allowed is False
        assert "frequency_limit_exceeded" in decision.blocked_reasons

    def test_frequency_limit_clear_note_is_recorded_below_threshold(self) -> None:
        now = datetime(2026, 5, 28, 14, 30, tzinfo=timezone.utc)
        history = [
            _allowed_history_request(
                draft_text="older draft one",
                evaluated_at=now - timedelta(seconds=120),
            ),
        ]
        gate = OutboundSendGate(
            config=_config(
                frequency_limit_count=2,
                frequency_limit_window_seconds=600,
            ),
        )

        decision = gate.evaluate(_request(), now=now, recent_requests=history)

        assert decision.allowed is True
        assert "frequency_limit_clear" in decision.passed_checks

    def test_duplicate_suppression_blocks_same_normalized_draft_text(self) -> None:
        now = datetime(2026, 5, 28, 14, 30, tzinfo=timezone.utc)
        history = [
            _allowed_history_request(
                draft_text=" Synthetic   outbound   draft for review. ",
                evaluated_at=now - timedelta(seconds=120),
            ),
        ]
        gate = OutboundSendGate(
            config=_config(
                duplicate_window_seconds=600,
            ),
        )

        decision = gate.evaluate(_request(), now=now, recent_requests=history)

        assert decision.allowed is False
        assert "duplicate_suppressed" in decision.blocked_reasons

    def test_duplicate_clear_note_is_recorded_for_distinct_draft_text(self) -> None:
        now = datetime(2026, 5, 28, 14, 30, tzinfo=timezone.utc)
        history = [
            _allowed_history_request(
                draft_text="A distinct synthetic history draft.",
                evaluated_at=now - timedelta(seconds=120),
            ),
        ]
        gate = OutboundSendGate(
            config=_config(
                duplicate_window_seconds=600,
            ),
        )

        decision = gate.evaluate(_request(), now=now, recent_requests=history)

        assert decision.allowed is True
        assert "duplicate_check_clear" in decision.passed_checks

    def test_self_echo_prevention_blocks_latest_inbound_text(self) -> None:
        gate = OutboundSendGate(config=_config())
        context = OutboundSendGateContext(
            latest_inbound_text="Synthetic outbound draft for review.",
        )

        decision = gate.evaluate(_request(), context=context)

        assert decision.allowed is False
        assert "self_echo_prevention" in decision.blocked_reasons

    def test_self_echo_clear_note_is_recorded_for_non_matching_context(self) -> None:
        gate = OutboundSendGate(config=_config())
        context = OutboundSendGateContext(
            latest_inbound_text="A different synthetic inbound message.",
            self_echo_reference_texts=["Another distinct synthetic note."],
        )

        decision = gate.evaluate(_request(), context=context)

        assert decision.allowed is True
        assert "self_echo_clear" in decision.passed_checks

    def test_self_echo_prevention_blocks_explicit_reference_text(self) -> None:
        gate = OutboundSendGate(config=_config())
        context = OutboundSendGateContext(
            self_echo_reference_texts=["  synthetic OUTBOUND draft for review.  "],
        )

        decision = gate.evaluate(_request(), context=context)

        assert decision.allowed is False
        assert "self_echo_prevention" in decision.blocked_reasons

    def test_multiple_block_reasons_are_preserved(self) -> None:
        gate = OutboundSendGate(config=_config(kill_switch_enabled=True))
        request = _request(
            human_approval=OutboundRequestHumanApproval(),
        )

        decision = gate.evaluate(request)

        assert decision.allowed is False
        assert "human_approval_pending" in decision.blocked_reasons
        assert "kill_switch_enabled" in decision.blocked_reasons
