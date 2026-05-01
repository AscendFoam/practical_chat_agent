from __future__ import annotations

from enum import StrEnum


class SourceType(StrEnum):
    CHAT_MESSAGE = "chat_message"
    MEETING_SEGMENT = "meeting_segment"
    SYSTEM_EVENT = "system_event"


class Platform(StrEnum):
    WECHAT = "wechat"
    FEISHU = "feishu"
    TELEGRAM = "telegram"
    TENCENT_MEETING = "tencent_meeting"
    MANUAL_IMPORT = "manual_import"


class MeetingAudioSource(StrEnum):
    LOOPBACK = "loopback"
    MICROPHONE = "microphone"


class MeetingExportTemplate(StrEnum):
    BRIEF = "brief"
    STANDARD = "standard"
    FULL = "full"


class ChannelType(StrEnum):
    DM = "dm"
    GROUP = "group"
    MEETING = "meeting"


class Direction(StrEnum):
    INBOUND = "inbound"
    OUTBOUND = "outbound"


class ContentType(StrEnum):
    TEXT = "text"
    IMAGE = "image"
    AUDIO = "audio"
    FILE = "file"
    SYSTEM = "system"


class PersonaType(StrEnum):
    FRIEND = "friend"
    MENTOR = "mentor"
    COMPANION = "companion"
    ROMANTIC = "romantic"


class SafetyMode(StrEnum):
    DISCLOSED_AI = "disclosed_ai"
    HUMAN_IN_THE_LOOP = "human_in_the_loop"
    DRAFT_ONLY = "draft_only"


class MemoryType(StrEnum):
    PREFERENCE = "preference"
    FACT = "fact"
    RELATIONSHIP = "relationship"
    REFLECTION = "reflection"


class MemoryScope(StrEnum):
    WORKING = "working"
    LONG_TERM = "long_term"


class ChatIntent(StrEnum):
    GENERAL = "general"
    GREETING = "greeting"
    PLAN = "plan"
    EMOTION = "emotion"
    RELATIONSHIP = "relationship"
    PREFERENCE = "preference"
    WORK = "work"


class ActionKind(StrEnum):
    REPLY_DRAFT = "reply_draft"
    NO_OP = "no_op"


class ActionStatus(StrEnum):
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    SENT = "sent"
    FAILED = "failed"
    POLICY_BLOCKED = "policy_blocked"
    DRAFT_ONLY = "draft_only"
    CANCELLED = "cancelled"
