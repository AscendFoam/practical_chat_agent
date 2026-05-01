from __future__ import annotations

from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from practical_chat_agent.core.enums import ActionStatus, ChannelType, SafetyMode
from practical_chat_agent.core.models import ActionExecutionRecord, AgentProfile, InboundEvent, PolicyDecision
from practical_chat_agent.storage.repositories.base import ActionRepository


class PolicyEngine:
    """Small conservative policy layer for outbound actions."""

    def __init__(
        self,
        *,
        action_repository: ActionRepository,
        quiet_hours_start: str | None = "23:00",
        quiet_hours_end: str | None = "08:00",
        timezone_name: str = "Asia/Shanghai",
        frequency_limit_count: int = 3,
        frequency_limit_window_seconds: int = 600,
        group_chat_draft_only: bool = True,
    ) -> None:
        self.action_repository = action_repository
        self.quiet_hours_start = self._parse_hhmm(quiet_hours_start)
        self.quiet_hours_end = self._parse_hhmm(quiet_hours_end)
        self.timezone_name = timezone_name
        self.frequency_limit_count = frequency_limit_count
        self.frequency_limit_window_seconds = frequency_limit_window_seconds
        self.group_chat_draft_only = group_chat_draft_only

    def review_outbound_action(
        self,
        *,
        action: ActionExecutionRecord,
        agent: AgentProfile,
        event: InboundEvent | None = None,
        now: datetime | None = None,
    ) -> PolicyDecision:
        risk_flags: list[str] = []
        metadata: dict[str, object] = {}
        allowed = True
        requires_approval = action.requires_approval
        draft_only = False

        if agent.safety_mode == SafetyMode.DRAFT_ONLY:
            draft_only = True
            requires_approval = True
            risk_flags.append("agent_safety_mode_draft_only")
        elif agent.safety_mode == SafetyMode.HUMAN_IN_THE_LOOP:
            requires_approval = True
            risk_flags.append("agent_safety_mode_requires_approval")
        else:
            requires_approval = True
            risk_flags.append("default_human_approval_required")

        if action.channel_type == ChannelType.GROUP:
            requires_approval = True
            risk_flags.append("group_chat_requires_approval")
            if self.group_chat_draft_only:
                draft_only = True
                risk_flags.append("group_chat_downgraded_to_draft_only")

        local_now = self._local_now(now)
        metadata["policy_time"] = local_now.isoformat()
        if self._is_quiet_hours(local_now):
            requires_approval = True
            risk_flags.append("quiet_hours")
            metadata["quiet_hours"] = {
                "timezone": self.timezone_name,
                "start": self._format_time(self.quiet_hours_start),
                "end": self._format_time(self.quiet_hours_end),
            }

        recent_sent_count = self._recent_sent_count(
            agent_id=action.agent_id,
            channel_id=action.channel_id,
            now=now,
        )
        metadata["recent_sent_count"] = recent_sent_count
        metadata["frequency_limit_count"] = self.frequency_limit_count
        metadata["frequency_limit_window_seconds"] = self.frequency_limit_window_seconds
        if self.frequency_limit_count > 0 and recent_sent_count >= self.frequency_limit_count:
            allowed = False
            requires_approval = True
            risk_flags.append("frequency_limit_exceeded")

        if not (action.message_text or "").strip():
            allowed = False
            risk_flags.append("empty_message")

        reason = self._build_reason(
            allowed=allowed,
            requires_approval=requires_approval,
            draft_only=draft_only,
            risk_flags=risk_flags,
        )
        return PolicyDecision(
            allowed=allowed,
            requires_approval=requires_approval,
            draft_only=draft_only,
            risk_flags=risk_flags,
            reason=reason,
            metadata=metadata,
        )

    def initial_status(self, decision: PolicyDecision) -> ActionStatus:
        if not decision.allowed:
            return ActionStatus.POLICY_BLOCKED
        if decision.draft_only:
            return ActionStatus.DRAFT_ONLY
        if decision.requires_approval:
            return ActionStatus.PENDING_APPROVAL
        return ActionStatus.APPROVED

    @staticmethod
    def _parse_hhmm(value: str | None) -> time | None:
        if value is None or not value.strip():
            return None
        hour_text, minute_text = value.strip().split(":", maxsplit=1)
        return time(hour=int(hour_text), minute=int(minute_text))

    @staticmethod
    def _format_time(value: time | None) -> str | None:
        if value is None:
            return None
        return value.strftime("%H:%M")

    def _local_now(self, now: datetime | None) -> datetime:
        current = now or datetime.now(tz=ZoneInfo("UTC"))
        if current.tzinfo is None:
            current = current.replace(tzinfo=ZoneInfo("UTC"))
        try:
            zone = ZoneInfo(self.timezone_name)
        except ZoneInfoNotFoundError:
            zone = ZoneInfo("UTC")
        return current.astimezone(zone)

    def _is_quiet_hours(self, local_now: datetime) -> bool:
        if self.quiet_hours_start is None or self.quiet_hours_end is None:
            return False
        current_time = local_now.time()
        if self.quiet_hours_start < self.quiet_hours_end:
            return self.quiet_hours_start <= current_time < self.quiet_hours_end
        return current_time >= self.quiet_hours_start or current_time < self.quiet_hours_end

    def _recent_sent_count(self, *, agent_id: str, channel_id: str, now: datetime | None) -> int:
        if self.frequency_limit_window_seconds <= 0:
            return 0
        current = now or datetime.now(tz=ZoneInfo("UTC"))
        if current.tzinfo is None:
            current = current.replace(tzinfo=ZoneInfo("UTC"))
        cutoff = current - timedelta(seconds=self.frequency_limit_window_seconds)
        recent_actions = self.action_repository.list_recent(
            agent_id=agent_id,
            status=ActionStatus.SENT.value,
            channel_id=channel_id,
            limit=max(self.frequency_limit_count + 10, 20),
        )
        return sum(
            1
            for action in recent_actions
            if action.sent_at is not None and self._as_aware_utc(action.sent_at) >= cutoff
        )

    @staticmethod
    def _build_reason(
        *,
        allowed: bool,
        requires_approval: bool,
        draft_only: bool,
        risk_flags: list[str],
    ) -> str:
        if not allowed:
            return "Policy blocked the action: " + ", ".join(risk_flags)
        if draft_only:
            return "Action is retained as a local draft only: " + ", ".join(risk_flags)
        if requires_approval:
            return "Human approval is required before sending: " + ", ".join(risk_flags)
        return "Action is allowed for sending."

    @staticmethod
    def _as_aware_utc(value: datetime) -> datetime:
        if value.tzinfo is None:
            return value.replace(tzinfo=ZoneInfo("UTC"))
        return value.astimezone(ZoneInfo("UTC"))
