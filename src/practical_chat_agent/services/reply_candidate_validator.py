"""Shared deterministic validation for reply candidates.

Provides stateless checks reusable across template-based (ReplyPlanner)
and LLM-generated reply candidates (LLMReplyGeneratorService).

All checks are deterministic: no embeddings, no semantic search, no
external moderation dependency.  Privacy-leak and impersonation checks
are conservative exact-match rules, not semantic classifiers.
"""

from __future__ import annotations

import re
from collections.abc import Sequence

from practical_chat_agent.core.models import ReplyPlanContextRef

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

VALID_REF_TYPES: frozenset[str] = frozenset({
    "approved_contact_skill_record",
    "approved_memory_fact_record",
    "approved_store_evidence_ref",
    "recent_event",
    "memory_hit",
    "policy_boundary",
})

_IMPERSONATION_PATTERNS: list[re.Pattern] = [
    re.compile(r"\bI\s+\(?\s*(?:would|think|feel|believe|know|want)", re.IGNORECASE),
    re.compile(r"\b(?:he|she)\s+would\s+say\b", re.IGNORECASE),
    re.compile(r"(^|[^A-Za-z])对方会"),
    re.compile(r"\b(?:作为|以).*(?:身份|角色).*(?:说|回复|回答)", re.IGNORECASE),
]

MAX_INPUT_CHARS = 20_000

# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------


class ReplyCandidateValidationError(ValueError):
    """Raised when deterministic candidate validation fails."""


# ---------------------------------------------------------------------------
# Per-candidate structural checks
# ---------------------------------------------------------------------------


def check_text_non_empty(draft_text: str) -> bool:
    """Candidate draft text must be non-empty after stripping."""
    return bool(draft_text.strip())


def check_supporting_refs(refs: Sequence[object]) -> bool:
    """Candidate must have at least one supporting context ref."""
    return len(refs) >= 1


def check_boundary_reminders(reminders: Sequence[object]) -> bool:
    """Candidate must have at least one boundary reminder."""
    return len(reminders) >= 1


def check_ref_types(refs: Sequence[ReplyPlanContextRef]) -> bool:
    """All ref types must be in the approved set."""
    return all(r.ref_type in VALID_REF_TYPES for r in refs)


# ---------------------------------------------------------------------------
# Privacy and impersonation checks
# ---------------------------------------------------------------------------


def has_privacy_leak(draft_text: str, context_texts: list[str]) -> bool:
    """Check if *draft_text* contains verbatim fragments from *context_texts*.

    Two-tier deterministic check:

    1. **Full normalized substring match** (min 8 chars) — catches
       verbatim quoting of a complete context string.
    2. **4-consecutive-word sequence match** — catches partial fragments
       where the draft reuses a multi-word phrase from context without
       reproducing the entire string.

    Both tiers use exact (normalized whitespace, lowercased) text
    matching.  Paraphrased or semantically equivalent leaks are **not**
    detected — this is a conservative baseline, not a semantic filter.
    """
    clean_draft = " ".join(draft_text.split()).strip().lower()
    for ctx in context_texts:
        clean_ctx = " ".join(ctx.split()).strip().lower()
        if not clean_ctx or len(clean_ctx) < 8:
            continue

        # Tier 1: full context text appears verbatim in draft
        if clean_ctx in clean_draft:
            return True

        # Tier 2: 4+ consecutive words from context appear in draft
        ctx_words = clean_ctx.split()
        if len(ctx_words) >= 4:
            for i in range(len(ctx_words) - 3):
                fragment = " ".join(ctx_words[i:i + 4])
                if len(fragment) >= 12 and fragment in clean_draft:
                    return True

    return False


def has_impersonation(draft_text: str) -> bool:
    """Check if *draft_text* impersonates the contact's voice.

    Patterns cover English first-person claims, third-person predictions,
    Chinese impersonation markers (``对方会``), and role-play framing
    (``作为/以...身份/角色...说/回复/回答``).

    This is a deterministic regex check — it will produce false negatives
    for novel impersonation patterns and false positives for innocent
    matches (e.g. "I think" in a self-referential thought).
    """
    return any(p.search(draft_text) for p in _IMPERSONATION_PATTERNS)


# ---------------------------------------------------------------------------
# Rank helpers
# ---------------------------------------------------------------------------


def normalize_ranks(candidates: list) -> list:
    """Re-assign ``priority_rank`` to a stable 1..N sequence.

    Mutates candidates in place and returns the list for convenience.
    """
    for idx, candidate in enumerate(candidates, start=1):
        candidate.priority_rank = idx
    return candidates


def check_ranks_contiguous(candidates: list) -> bool:
    """Check that ``priority_rank`` values form a contiguous 1..N sequence.

    An empty candidate list is considered valid.
    """
    if not candidates:
        return True
    ranks = sorted(c.priority_rank for c in candidates)
    return ranks == list(range(1, len(ranks) + 1))


# ---------------------------------------------------------------------------
# Input-size check
# ---------------------------------------------------------------------------


def check_input_size(size: int, max_chars: int = MAX_INPUT_CHARS) -> bool:
    """Check if a payload size fits within the character budget.

    This is a character-count proxy for token estimation.  Callers
    should pass the total estimated size (in characters) of the data
    that would be sent to the provider.
    """
    return size <= max_chars
