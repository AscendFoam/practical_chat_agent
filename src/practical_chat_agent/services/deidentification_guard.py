"""Synthetic deidentification guard for future L2 style inspiration work.

T252 keeps this guard deterministic and local. It classifies fabricated text
into allowed abstract style signals or blocked identifying/biometric/private
details. It does not read files, call models, or compare against private
corpora.
"""

from __future__ import annotations

import re
from typing import Literal

from pydantic import BaseModel, Field


DeidentificationRiskFlag = Literal[
    "direct_identifier",
    "contact_identifier",
    "location_identifier",
    "org_school_identifier",
    "handle_identifier",
    "voice_biometric",
    "face_biometric",
    "image_biometric",
    "real_person_avatar",
    "private_event",
    "exact_biography",
    "clone_intent",
    "distinctive_catchphrase",
]


class DeidentificationGuardDecision(BaseModel):
    schema_version: str = "deidentification_guard_decision_v1"
    allowed: bool
    risk_flags: list[DeidentificationRiskFlag] = Field(default_factory=list)
    safe_summary: str
    blocked_reason: str | None = None
    source_text_retained: bool = False


class DeidentificationGuard:
    """Assess whether synthetic style material is abstract enough for L2 work."""

    def assess(self, text: str) -> DeidentificationGuardDecision:
        normalized = text.casefold()
        risk_flags = self._risk_flags(text=text, normalized=normalized)
        allowed_terms = self._abstract_style_terms(normalized)

        if risk_flags:
            return DeidentificationGuardDecision(
                allowed=False,
                risk_flags=risk_flags,
                safe_summary=self._blocked_summary(allowed_terms),
                blocked_reason="identifying, biometric, private-event, or clone-intent signal detected",
                source_text_retained=False,
            )

        return DeidentificationGuardDecision(
            allowed=True,
            risk_flags=[],
            safe_summary=", ".join(allowed_terms) if allowed_terms else "generic_abstract_style",
            blocked_reason=None,
            source_text_retained=False,
        )

    def _risk_flags(
        self,
        *,
        text: str,
        normalized: str,
    ) -> list[DeidentificationRiskFlag]:
        flags: list[DeidentificationRiskFlag] = []

        if self._has_direct_identifier(text):
            flags.append("direct_identifier")
        if re.search(r"\b\d{7,}\b", text) or re.search(r"\b[\w.+-]+@[\w.-]+\.\w+\b", text):
            flags.append("contact_identifier")
        if self._has_any(normalized, ("address", " road", " street", " avenue", " lane", "west lake")):
            flags.append("location_identifier")
        if self._has_any(
            normalized,
            ("works at", "employer", "company", "school", "university", "robotics"),
        ):
            flags.append("org_school_identifier")
        if re.search(r"@\w+", text):
            flags.append("handle_identifier")
        if self._has_any(normalized, ("voice", "same voice", "voice clone")):
            flags.append("voice_biometric")
        if self._has_any(normalized, ("face", "facial", "likeness")):
            flags.append("face_biometric")
        if self._has_any(normalized, ("photo", "image", "picture")):
            flags.append("image_biometric")
        if "real-person avatar" in normalized or "real person avatar" in normalized:
            flags.append("real_person_avatar")
        if self._has_any(
            normalized,
            ("private event", "broke up", "breakup", "our relationship", "three-year relationship"),
        ):
            flags.append("private_event")
        if self._has_any(normalized, ("exact biography", "born in", "grew up", "after our")):
            flags.append("exact_biography")
        if self._has_any(normalized, ("talk exactly like", "copy this person", "clone", "same as this person")):
            flags.append("clone_intent")
        if self._has_distinctive_catchphrase(text=text, normalized=normalized):
            flags.append("distinctive_catchphrase")

        return self._dedupe(flags)

    def _abstract_style_terms(self, normalized: str) -> list[str]:
        terms: list[str] = []
        if "concise" in normalized or "short" in normalized:
            terms.append("concise")
        if "warm" in normalized or "kind" in normalized:
            terms.append("warm")
        if "delayed response" in normalized or "slow reply" in normalized:
            terms.append("delayed_response")
        if "dry humor" in normalized:
            terms.append("dry_humor")
        if "practical" in normalized:
            terms.append("practical")
        if "gentle" in normalized:
            terms.append("gentle")
        return self._dedupe_strings(terms)

    @staticmethod
    def _blocked_summary(allowed_terms: list[str]) -> str:
        if allowed_terms:
            return "blocked_identifying_input; retained abstract signals: " + ", ".join(allowed_terms)
        return "blocked_identifying_input; no safe abstract style summary available"

    @staticmethod
    def _has_direct_identifier(text: str) -> bool:
        return bool(re.search(r"\b[A-Z][a-z]+ [A-Z][a-z]+\b", text))

    @staticmethod
    def _has_distinctive_catchphrase(*, text: str, normalized: str) -> bool:
        has_quoted_phrase = bool(re.search(r"['\"][^'\"]{6,}['\"]", text))
        return has_quoted_phrase and ("catchphrase" in normalized or "talk exactly like" in normalized)

    @staticmethod
    def _has_any(text: str, terms: tuple[str, ...]) -> bool:
        return any(term in text for term in terms)

    @staticmethod
    def _dedupe(flags: list[DeidentificationRiskFlag]) -> list[DeidentificationRiskFlag]:
        seen: set[str] = set()
        result: list[DeidentificationRiskFlag] = []
        for flag in flags:
            if flag not in seen:
                seen.add(flag)
                result.append(flag)
        return result

    @staticmethod
    def _dedupe_strings(values: list[str]) -> list[str]:
        seen: set[str] = set()
        result: list[str] = []
        for value in values:
            if value not in seen:
                seen.add(value)
                result.append(value)
        return result
