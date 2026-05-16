from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from practical_chat_agent.core.enums import ActionStatus, ChannelType, ChatIntent, SafetyMode
from practical_chat_agent.core.models import (
    ActionExecutionRecord,
    AgentProfile,
    ChatContext,
    InboundEvent,
    PolicyDecision,
)
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


@dataclass
class ReplyPlanPolicyProfile:
    context_risk_flags: list[str] = field(default_factory=list)
    policy_boundary_summary: list[str] = field(default_factory=list)
    shared_boundary_reminders: list[str] = field(default_factory=list)
    conservative_mode: bool = False
    avoid_follow_up: bool = False
    practical_tone: bool = False
    thin_context: bool = False
    boundary_sensitive: bool = False


@dataclass
class ReplyCandidatePolicyAssessment:
    risk_flags: list[str] = field(default_factory=list)
    boundary_reminders: list[str] = field(default_factory=list)
    confidence_penalty: float = 0.0


class ReplyPlanPolicyEngine:
    """Policy helpers for review-only reply planning."""

    _SENSITIVE_TOPIC_KEYWORDS = (
        "家庭",
        "父母",
        "家里",
        "感情",
        "关系",
        "分手",
        "前任",
        "结婚",
        "离婚",
        "生病",
        "医院",
        "抑郁",
        "焦虑",
        "创伤",
        "心理",
        "秘密",
        "隐私",
        "借钱",
        "债",
        "therapy",
        "family",
        "relationship",
        "breakup",
        "marriage",
        "illness",
        "health",
        "private",
        "secret",
        "money",
        "debt",
        "grief",
        "loss",
    )
    _BOUNDARY_CUE_KEYWORDS = (
        "边界",
        "保持距离",
        "给空间",
        "不要追问",
        "不追问",
        "别追问",
        "不要逼",
        "不逼",
        "不要催",
        "别催",
        "谨慎",
        "保守",
        "低压",
        "慢一点",
        "先别",
        "暂时别",
        "boundary",
        "space",
        "do not push",
        "don't push",
        "not ready",
        "low pressure",
        "sensitive",
        "cautious",
        "keep distance",
    )
    _AVOID_FOLLOW_UP_KEYWORDS = (
        "不要追问",
        "不追问",
        "别追问",
        "给空间",
        "先别",
        "暂时别",
        "不要催",
        "do not push",
        "don't push",
        "not ready",
        "space",
        "optional",
        "low pressure",
    )
    _PRACTICAL_TONE_KEYWORDS = (
        "简短",
        "直接",
        "务实",
        "只回重点",
        "别太长",
        "brief",
        "direct",
        "practical",
        "concise",
    )
    _OVER_PROACTIVE_DRAFT_CUES = (
        "继续说说",
        "哪一部分",
        "再补一句",
        "下一步",
        "顺一顺",
        "展开",
        "聊聊",
        "见面",
        "打电话",
        "马上",
        "现在就",
        "next step",
        "tell me more",
        "follow up",
    )
    _ACTION_PUSH_CUES = (
        "见面",
        "打电话",
        "约",
        "马上",
        "现在就",
        "安排",
        "call",
        "meet",
        "schedule",
        "right away",
    )
    _NO_PRESSURE_CUES = (
        "不用现在",
        "先不",
        "不往前推",
        "等你方便",
        "等你想说",
        "之后愿意",
        "later if you want",
        "no rush",
    )
    _IMPERSONATION_CUES = (
        "对方会",
        "他会",
        "她会",
        "ta会",
        "替你回",
        "我替你说",
        "像对方一样",
        "对方会怎么说",
        "they would say",
        "he would say",
        "she would say",
    )

    def build_profile(self, *, context: ChatContext) -> ReplyPlanPolicyProfile:
        contact_skill = context.approved_store_context.contact_skill
        thin_context = (
            context.approved_store_context.status != "loaded"
            or contact_skill is None
        )
        skill_texts = []
        boundary_texts = []
        if contact_skill is not None:
            skill_texts.extend([contact_skill.relationship_summary, *contact_skill.strategy_hints])
            boundary_texts.extend(contact_skill.boundary_reminders)

        runtime_texts = [
            context.latest_message_text,
            *(event.text for event in context.recent_events[:3]),
            *(memory.fact for memory in context.memory_hits[:2]),
            *(memory.claim for memory in context.approved_store_context.memory_facts[:2]),
            *context.memory_retrieval_notes[:3],
        ]
        combined_boundary_texts = boundary_texts + skill_texts
        sensitive_topic = self._contains_any(runtime_texts + skill_texts, self._SENSITIVE_TOPIC_KEYWORDS)
        explicit_boundary = self._contains_any(combined_boundary_texts, self._BOUNDARY_CUE_KEYWORDS)
        emotion_intent = context.intent in {ChatIntent.EMOTION, ChatIntent.RELATIONSHIP}
        boundary_sensitive = explicit_boundary or (emotion_intent and sensitive_topic)
        avoid_follow_up = self._contains_any(combined_boundary_texts, self._AVOID_FOLLOW_UP_KEYWORDS) or (
            boundary_sensitive and sensitive_topic
        )
        practical_tone = (
            (contact_skill is not None and contact_skill.relationship_type == "colleague")
            or self._contains_any(skill_texts, self._PRACTICAL_TONE_KEYWORDS)
        )
        conservative_mode = thin_context or boundary_sensitive or avoid_follow_up

        context_risk_flags: list[str] = []
        policy_boundary_summary: list[str] = []
        shared_boundary_reminders: list[str] = []

        if thin_context:
            context_risk_flags.append("thin_context")
            policy_boundary_summary.append(
                "Approved context is thin; avoid relationship-specific assumptions or intimate wording.",
            )
            shared_boundary_reminders.append(
                "Approved context is thin; keep the reply generic and do not over-claim familiarity.",
            )

        if boundary_sensitive:
            context_risk_flags.append("boundary_sensitive")
            policy_boundary_summary.append(
                "This context looks sensitive or boundary-heavy; prefer contained, non-invasive wording.",
            )
            shared_boundary_reminders.append(
                "Sensitive context: do not push for disclosure, reassurance, or emotional escalation.",
            )

        if avoid_follow_up:
            policy_boundary_summary.append(
                "Avoid follow-up that pressures the contact to explain more or move faster.",
            )
            shared_boundary_reminders.append(
                "Keep any follow-up optional; do not chase for more detail or immediate action.",
            )

        if practical_tone:
            policy_boundary_summary.append("Keep the wording brief, practical, and low-drama.")
            shared_boundary_reminders.append(
                "Prefer concise, practical wording over emotionally expansive phrasing.",
            )

        return ReplyPlanPolicyProfile(
            context_risk_flags=self._dedupe(context_risk_flags),
            policy_boundary_summary=self._dedupe(policy_boundary_summary),
            shared_boundary_reminders=self._dedupe(shared_boundary_reminders),
            conservative_mode=conservative_mode,
            avoid_follow_up=avoid_follow_up,
            practical_tone=practical_tone,
            thin_context=thin_context,
            boundary_sensitive=boundary_sensitive,
        )

    def assess_candidate(
        self,
        *,
        policy_profile: ReplyPlanPolicyProfile,
        candidate_text: str,
        approach_label: str,
    ) -> ReplyCandidatePolicyAssessment:
        risk_flags = list(policy_profile.context_risk_flags)
        boundary_reminders = list(policy_profile.shared_boundary_reminders)
        confidence_penalty = 0.0

        if policy_profile.thin_context:
            confidence_penalty += 0.10
        if policy_profile.boundary_sensitive:
            confidence_penalty += 0.06

        if self._candidate_is_over_proactive(
            candidate_text=candidate_text,
            approach_label=approach_label,
            policy_profile=policy_profile,
        ):
            risk_flags.append("over_proactive")
            boundary_reminders.append(
                "Avoid pushing action, intimacy, or more disclosure beyond the current context.",
            )
            confidence_penalty += 0.08

        if self._contains_any([candidate_text], self._IMPERSONATION_CUES):
            risk_flags.append("impersonation_risk")
            boundary_reminders.append(
                "Keep the draft in the user's voice; do not predict the contact's words or inner state.",
            )
            confidence_penalty += 0.15

        return ReplyCandidatePolicyAssessment(
            risk_flags=self._dedupe(risk_flags),
            boundary_reminders=self._dedupe(boundary_reminders),
            confidence_penalty=confidence_penalty,
        )

    def _candidate_is_over_proactive(
        self,
        *,
        candidate_text: str,
        approach_label: str,
        policy_profile: ReplyPlanPolicyProfile,
    ) -> bool:
        if self._contains_any([candidate_text], self._ACTION_PUSH_CUES):
            return True
        if not (policy_profile.conservative_mode or policy_profile.avoid_follow_up):
            return False
        if approach_label == "optional_follow_up":
            return True
        if self._contains_any([candidate_text], self._NO_PRESSURE_CUES):
            return False
        if approach_label == "paced_next_step":
            return self._contains_any([candidate_text], self._OVER_PROACTIVE_DRAFT_CUES)
        return self._contains_any([candidate_text], self._OVER_PROACTIVE_DRAFT_CUES)

    @staticmethod
    def _contains_any(values: list[str | None], keywords: tuple[str, ...]) -> bool:
        lowered_keywords = tuple(keyword.casefold() for keyword in keywords)
        for value in values:
            if value is None:
                continue
            text = value.casefold()
            if any(keyword in text for keyword in lowered_keywords):
                return True
        return False

    @staticmethod
    def _dedupe(values: list[str]) -> list[str]:
        seen: set[str] = set()
        result: list[str] = []
        for value in values:
            text = value.strip()
            if not text or text in seen:
                continue
            seen.add(text)
            result.append(text)
        return result
