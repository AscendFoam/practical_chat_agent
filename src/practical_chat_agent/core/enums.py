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


class ActionKind(StrEnum):
    REPLY_DRAFT = "reply_draft"
    NO_OP = "no_op"

