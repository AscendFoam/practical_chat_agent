"""T182: Shared Reply Candidate Validator Tests.

Deterministic tests for the shared validator module that provides
checks reusable across template-based and LLM-generated candidates.
All fixtures are synthetic and contain no private chat content.

Coverage areas:
  1. check_text_non_empty
  2. check_supporting_refs / check_boundary_reminders
  3. check_ref_types (valid + invalid)
  4. has_privacy_leak (Tier 1, Tier 2, safe)
  5. has_impersonation (all patterns)
  6. normalize_ranks
  7. check_ranks_contiguous
  8. check_input_size
"""

from __future__ import annotations

import pytest

from practical_chat_agent.core.models import ReplyPlanContextRef
from practical_chat_agent.services.reply_candidate_validator import (
    MAX_INPUT_CHARS,
    VALID_REF_TYPES,
    check_boundary_reminders,
    check_input_size,
    check_ranks_contiguous,
    check_ref_types,
    check_supporting_refs,
    check_text_non_empty,
    has_impersonation,
    has_privacy_leak,
    normalize_ranks,
)


# =========================================================================
# check_text_non_empty
# =========================================================================


class TestCheckTextNonEmpty:
    def test_non_empty_text_passes(self) -> None:
        assert check_text_non_empty("some draft text") is True

    def test_empty_text_fails(self) -> None:
        assert check_text_non_empty("") is False

    def test_whitespace_only_fails(self) -> None:
        assert check_text_non_empty("   ") is False


# =========================================================================
# check_supporting_refs
# =========================================================================


class TestCheckSupportingRefs:
    def test_non_empty_refs_passes(self) -> None:
        assert check_supporting_refs(["ref1"]) is True

    def test_empty_refs_fails(self) -> None:
        assert check_supporting_refs([]) is False


# =========================================================================
# check_boundary_reminders
# =========================================================================


class TestCheckBoundaryReminders:
    def test_non_empty_reminders_passes(self) -> None:
        assert check_boundary_reminders(["reminder"]) is True

    def test_empty_reminders_fails(self) -> None:
        assert check_boundary_reminders([]) is False


# =========================================================================
# check_ref_types
# =========================================================================


class TestCheckRefTypes:
    def test_all_valid_types_passes(self) -> None:
        refs = [
            ReplyPlanContextRef(ref_type="approved_contact_skill_record", ref_id="id1"),
            ReplyPlanContextRef(ref_type="approved_memory_fact_record", ref_id="id2"),
            ReplyPlanContextRef(ref_type="approved_store_evidence_ref", ref_id="id3"),
            ReplyPlanContextRef(ref_type="recent_event", ref_id="id4"),
            ReplyPlanContextRef(ref_type="memory_hit", ref_id="id5"),
            ReplyPlanContextRef(ref_type="policy_boundary", ref_id="id6"),
        ]
        assert check_ref_types(refs) is True

    def test_invalid_type_fails(self) -> None:
        refs = [
            ReplyPlanContextRef.model_construct(ref_type="candidate_record", ref_id="id1"),
        ]
        assert check_ref_types(refs) is False

    def test_mixed_valid_and_invalid_fails(self) -> None:
        refs = [
            ReplyPlanContextRef(ref_type="approved_contact_skill_record", ref_id="id1"),
            ReplyPlanContextRef.model_construct(ref_type="candidate_record", ref_id="id2"),
        ]
        assert check_ref_types(refs) is False

    def test_empty_refs_list_passes(self) -> None:
        """Empty list trivially passes — no refs to have invalid types."""
        assert check_ref_types([]) is True

    def test_valid_ref_types_constant_is_frozenset(self) -> None:
        assert isinstance(VALID_REF_TYPES, frozenset)
        assert len(VALID_REF_TYPES) == 6


# =========================================================================
# has_privacy_leak
# =========================================================================


class TestHasPrivacyLeak:
    """Two-tier privacy leak detection."""

    # Tier 1: full normalized substring match

    def test_exact_context_quote_detected(self) -> None:
        """Full context text appearing verbatim in draft is detected."""
        assert has_privacy_leak(
            draft_text="I see your point about unique private detail abc123.",
            context_texts=["unique private detail abc123"],
        ) is True

    def test_short_context_ignored(self) -> None:
        """Context text shorter than 8 chars is not checked."""
        assert has_privacy_leak(
            draft_text="hi there",
            context_texts=["short"],
        ) is False

    def test_no_match_passes(self) -> None:
        """Safe draft with no context text matched passes."""
        assert has_privacy_leak(
            draft_text="收到，我先跟上你这个点。",
            context_texts=["unique private detail abc123"],
        ) is False

    def test_empty_context_list_passes(self) -> None:
        """Empty context list always passes."""
        assert has_privacy_leak(
            draft_text="some text",
            context_texts=[],
        ) is False

    def test_normalized_whitespace_match(self) -> None:
        """Whitespace normalization applied before matching."""
        assert has_privacy_leak(
            draft_text="hello   world  foo",
            context_texts=["hello world foo"],
        ) is True

    def test_case_insensitive_match(self) -> None:
        """Matching is case-insensitive."""
        assert has_privacy_leak(
            draft_text="PRIVATE DETAIL LEAKED",
            context_texts=["private detail leaked"],
        ) is True

    # Tier 2: 4+ consecutive word sequence match

    def test_four_word_sequence_detected(self) -> None:
        """4+ consecutive words from context appearing in draft is detected."""
        assert has_privacy_leak(
            draft_text="The meeting about budget planning for q3 went well.",
            context_texts=["budget planning for q3"],
        ) is True

    def test_three_word_sequence_not_detected(self) -> None:
        """Only 3 consecutive words from a longer context — Tier 2 needs 4+."""
        assert has_privacy_leak(
            draft_text="the budget planning meeting went well",
            context_texts=["quarterly budget planning review is scheduled"],
        ) is False

    def test_fewer_than_four_context_words_only_tier1(self) -> None:
        """Context with <4 words skips Tier 2; only Tier 1 (full substring) may catch it."""
        # 3-word context that appears as full substring is caught by Tier 1 only
        assert has_privacy_leak(
            draft_text="The unique private data is here.",
            context_texts=["unique private data"],
        ) is True  # Tier 1 catches the full 3-word substring

    def test_multiple_context_texts_tier2(self) -> None:
        """Tier 2 check scans all context texts."""
        assert has_privacy_leak(
            draft_text="I remember you mentioned your cat likes to sleep on the sofa.",
            context_texts=[
                "some unrelated text",
                "my cat likes to sleep on warm surfaces",
                "other random stuff",
            ],
        ) is True


# =========================================================================
# has_impersonation
# =========================================================================


class TestHasImpersonation:
    def test_first_person_would_detected(self) -> None:
        assert has_impersonation("I would say that sounds reasonable.") is True

    def test_first_person_think_detected(self) -> None:
        assert has_impersonation("I think we should do this.") is True

    def test_first_person_want_detected(self) -> None:
        assert has_impersonation("I want to tell you something.") is True

    def test_he_would_say_detected(self) -> None:
        assert has_impersonation("He would say it's fine.") is True

    def test_she_would_say_detected(self) -> None:
        assert has_impersonation("She would say let's wait.") is True

    def test_chinese_impersonation_detected(self) -> None:
        assert has_impersonation("对方会觉得这样不太好。") is True

    def test_role_play_detected(self) -> None:
        assert has_impersonation("作为朋友的身份来说，我觉得...") is True

    def test_safe_text_passes(self) -> None:
        assert has_impersonation("收到，我先跟上你这个点。") is False

    def test_safe_english_passes(self) -> None:
        assert has_impersonation("Let me know what you think.") is False


# =========================================================================
# normalize_ranks
# =========================================================================


class _MockCandidate:
    """Minimal candidate stub for rank testing."""
    def __init__(self, rank: int) -> None:
        self.priority_rank = rank


class TestNormalizeRanks:
    def test_renumbers_from_one(self) -> None:
        candidates = [_MockCandidate(5), _MockCandidate(10), _MockCandidate(3)]
        normalize_ranks(candidates)
        assert [c.priority_rank for c in candidates] == [1, 2, 3]

    def test_empty_list(self) -> None:
        result = normalize_ranks([])
        assert result == []

    def test_single_candidate(self) -> None:
        candidates = [_MockCandidate(99)]
        normalize_ranks(candidates)
        assert candidates[0].priority_rank == 1

    def test_already_contiguous(self) -> None:
        candidates = [_MockCandidate(1), _MockCandidate(2), _MockCandidate(3)]
        normalize_ranks(candidates)
        assert [c.priority_rank for c in candidates] == [1, 2, 3]

    def test_returns_list(self) -> None:
        candidates = [_MockCandidate(1)]
        result = normalize_ranks(candidates)
        assert result is candidates


# =========================================================================
# check_ranks_contiguous
# =========================================================================


class TestCheckRanksContiguous:
    def test_contiguous_ranks_pass(self) -> None:
        candidates = [_MockCandidate(1), _MockCandidate(2), _MockCandidate(3)]
        assert check_ranks_contiguous(candidates) is True

    def test_non_contiguous_ranks_fail(self) -> None:
        candidates = [_MockCandidate(1), _MockCandidate(3)]
        assert check_ranks_contiguous(candidates) is False

    def test_duplicate_ranks_fail(self) -> None:
        candidates = [_MockCandidate(1), _MockCandidate(1), _MockCandidate(2)]
        assert check_ranks_contiguous(candidates) is False

    def test_gap_in_ranks_fail(self) -> None:
        candidates = [_MockCandidate(1), _MockCandidate(2), _MockCandidate(4)]
        assert check_ranks_contiguous(candidates) is False

    def test_empty_list_passes(self) -> None:
        assert check_ranks_contiguous([]) is True

    def test_single_candidate_passes(self) -> None:
        assert check_ranks_contiguous([_MockCandidate(1)]) is True


# =========================================================================
# check_input_size
# =========================================================================


class TestCheckInputSize:
    def test_within_limit_passes(self) -> None:
        data = "x" * 1000
        assert check_input_size(data, max_chars=2000) is True

    def test_exceeds_limit_fails(self) -> None:
        data = "x" * 3000
        assert check_input_size(data, max_chars=2000) is False

    def test_exactly_at_limit_passes(self) -> None:
        data = "x" * 20000
        assert check_input_size(data, max_chars=20000) is True

    def test_default_max_chars(self) -> None:
        data = "x" * MAX_INPUT_CHARS
        assert check_input_size(data) is True
        assert check_input_size(data + "x") is False
