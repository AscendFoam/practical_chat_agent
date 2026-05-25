from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from collections.abc import Iterable, Mapping

from practical_chat_agent.core.models import (
    AgentSelfState,
    DistilledArtifactReviewDecision,
    BehaviorPolicy,
    BehaviorActionType,
    CandidateAction,
    CandidateActionPayload,
    ReplyPlanContextRef,
)


_BOUNDARY_RULE_FLAGS = frozenset(
    {
        "boundary_sensitive",
        "boundary_risk",
        "high_sensitivity",
        "sensitive_context",
    },
)
_MEMORY_REVIEW_LABELS = frozenset(
    {
        "memory_review",
        "relationship_review",
        "relationship_signal",
    },
)
_PROACTIVE_BLOCKING_FLAGS = frozenset(
    {
        "thin_context",
        "boundary_sensitive",
        "boundary_risk",
        "high_sensitivity",
        "privacy_risk",
        "blocked_proactive",
    },
)


class BehaviorRulePlanner:
    """Deterministic, local rule planner for review-only CandidateActions."""

    def plan(
        self,
        *,
        self_state: AgentSelfState,
        policy: BehaviorPolicy | None = None,
        safe_context_labels: Iterable[str] | None = None,
    ) -> list[CandidateAction]:
        active_policy = policy or BehaviorPolicy()
        labels = self._normalize_values(safe_context_labels or [])
        risk_flags = self._normalize_values(self_state.risk_flags)

        candidates: list[CandidateAction] = []
        if self._is_boundary_sensitive(
            risk_flags=risk_flags,
            labels=labels,
        ) and self._is_allowed("boundary_review_note", policy=active_policy):
            candidates.append(
                self._build_boundary_review_note(
                    self_state=self_state,
                    policy=active_policy,
                    risk_flags=risk_flags,
                ),
            )

        if (
            self_state.recent_signal_refs or _MEMORY_REVIEW_LABELS.intersection(labels)
        ) and self._is_allowed("memory_review_prompt", policy=active_policy):
            candidates.append(
                self._build_memory_review_prompt(
                    self_state=self_state,
                    policy=active_policy,
                    risk_flags=risk_flags,
                ),
            )

        if (
            self_state.approved_context_refs
            and not _PROACTIVE_BLOCKING_FLAGS.intersection(risk_flags)
            and self._is_allowed("relationship_check_in_draft", policy=active_policy)
        ):
            candidates.append(
                self._build_relationship_check_in(
                    self_state=self_state,
                    policy=active_policy,
                    risk_flags=risk_flags,
                ),
            )

        if not candidates and self._is_allowed("do_nothing", policy=active_policy):
            candidates.append(
                self._build_do_nothing(
                    self_state=self_state,
                    policy=active_policy,
                    risk_flags=risk_flags,
                ),
            )

        return candidates[: active_policy.max_candidates]

    def _build_boundary_review_note(
        self,
        *,
        self_state: AgentSelfState,
        policy: BehaviorPolicy,
        risk_flags: list[str],
    ) -> CandidateAction:
        refs = [
            self._policy_ref(
                ref_id="behavior_boundary_sensitive",
                note="Boundary-sensitive behavior context.",
            ),
        ]
        refs.extend(self._approved_refs(self_state.approved_context_refs[:1]))
        return self._candidate(
            self_state=self_state,
            policy=policy,
            action_type="boundary_review_note",
            title="Review boundary-sensitive context before proposing behavior",
            rationale=(
                "boundary-sensitive context was detected, so the conservative action is "
                "a review note rather than proactive wording."
            ),
            safe_summary="Review boundary-sensitive context before any proactive wording.",
            supporting_context_refs=refs,
            risk_flags=risk_flags,
        )

    def _build_memory_review_prompt(
        self,
        *,
        self_state: AgentSelfState,
        policy: BehaviorPolicy,
        risk_flags: list[str],
    ) -> CandidateAction:
        signal_refs = self._signal_refs(self_state.recent_signal_refs)
        refs = signal_refs or [
            self._policy_ref(
                ref_id="behavior_memory_review_label",
                note="Safe context label requested memory review.",
            ),
        ]
        return self._candidate(
            self_state=self_state,
            policy=policy,
            action_type="memory_review_prompt",
            title="Review recent memory or relationship signals",
            rationale=(
                "Recent review-safe signal refs indicate memory or relationship context "
                "should be checked before proposing a reply behavior."
            ),
            safe_summary="Review recent safe memory or relationship signal refs before replying.",
            supporting_context_refs=refs,
            risk_flags=risk_flags,
        )

    def _build_relationship_check_in(
        self,
        *,
        self_state: AgentSelfState,
        policy: BehaviorPolicy,
        risk_flags: list[str],
    ) -> CandidateAction:
        return self._candidate(
            self_state=self_state,
            policy=policy,
            action_type="relationship_check_in_draft",
            title="Consider a low-pressure relationship check-in",
            rationale=(
                "At least one approved context ref is available and no hard proactive "
                "risk flag blocks a review-only check-in candidate."
            ),
            safe_summary="Consider a low-pressure check-in candidate for human review.",
            supporting_context_refs=self._approved_refs(self_state.approved_context_refs[:1]),
            risk_flags=risk_flags,
        )

    def _build_do_nothing(
        self,
        *,
        self_state: AgentSelfState,
        policy: BehaviorPolicy,
        risk_flags: list[str],
    ) -> CandidateAction:
        return self._candidate(
            self_state=self_state,
            policy=policy,
            action_type="do_nothing",
            title="Do not propose a proactive action",
            rationale=(
                "No conservative behavior rule fired, context is too thin, or allowed "
                "rules were blocked by policy."
            ),
            safe_summary="No proactive candidate: context is too thin.",
            supporting_context_refs=[
                self._policy_ref(
                    ref_id="behavior_rule_no_action",
                    note="No safe proactive behavior rule fired.",
                ),
            ],
            risk_flags=risk_flags,
        )

    def _candidate(
        self,
        *,
        self_state: AgentSelfState,
        policy: BehaviorPolicy,
        action_type: BehaviorActionType,
        title: str,
        rationale: str,
        safe_summary: str,
        supporting_context_refs: list[ReplyPlanContextRef],
        risk_flags: list[str],
    ) -> CandidateAction:
        return CandidateAction(
            action_id=self._stable_action_id(
                self_state=self_state,
                action_type=action_type,
                refs=supporting_context_refs,
            ),
            contact_id=self_state.contact_id or self_state.user_id,
            user_id=self_state.user_id,
            action_type=action_type,
            title=title,
            rationale=rationale,
            supporting_context_refs=supporting_context_refs,
            risk_flags=risk_flags,
            payload=CandidateActionPayload(
                safe_summary=safe_summary,
                metadata={"rule_id": action_type},
            ),
            policy=policy,
        )

    @staticmethod
    def _is_allowed(
        action_type: BehaviorActionType,
        *,
        policy: BehaviorPolicy,
    ) -> bool:
        return action_type in policy.allowed_action_types

    @staticmethod
    def _is_boundary_sensitive(*, risk_flags: list[str], labels: list[str]) -> bool:
        return bool(_BOUNDARY_RULE_FLAGS.intersection(risk_flags) or _BOUNDARY_RULE_FLAGS.intersection(labels))

    @staticmethod
    def _approved_refs(ref_ids: Iterable[str]) -> list[ReplyPlanContextRef]:
        return [
            ReplyPlanContextRef(
                ref_type="approved_contact_skill_record",
                ref_id=ref_id,
                note="approved behavior context ref",
            )
            for ref_id in ref_ids
            if ref_id.strip()
        ]

    @staticmethod
    def _signal_refs(ref_ids: Iterable[str]) -> list[ReplyPlanContextRef]:
        return [
            ReplyPlanContextRef(
                ref_type="approved_store_evidence_ref",
                ref_id=ref_id,
                note="review-safe recent signal ref",
            )
            for ref_id in ref_ids
            if ref_id.strip()
        ]

    @staticmethod
    def _policy_ref(*, ref_id: str, note: str) -> ReplyPlanContextRef:
        return ReplyPlanContextRef(ref_type="policy_boundary", ref_id=ref_id, note=note)

    @staticmethod
    def _normalize_values(values: Iterable[str]) -> list[str]:
        result: list[str] = []
        seen: set[str] = set()
        for value in values:
            normalized = value.strip().casefold()
            if not normalized or normalized in seen:
                continue
            seen.add(normalized)
            result.append(normalized)
        return result

    @staticmethod
    def _stable_action_id(
        *,
        self_state: AgentSelfState,
        action_type: str,
        refs: list[ReplyPlanContextRef],
    ) -> str:
        pieces = [
            self_state.agent_id,
            self_state.user_id,
            self_state.contact_id or "",
            action_type,
            *[ref.ref_id for ref in refs],
        ]
        digest = hashlib.sha1("|".join(pieces).encode("utf-8")).hexdigest()[:16]
        return f"candact_{digest}"


_PROACTIVE_DRAFT_TEXTS: dict[BehaviorActionType, str] = {
    "relationship_check_in_draft": (
        "Review-only draft: consider a brief, low-pressure check-in; keep it "
        "optional and non-committal."
    ),
    "reply_follow_up_draft": (
        "Review-only draft: consider a concise, gentle follow-up that stays optional."
    ),
    "topic_suggestion": (
        "Review only: suggest a simple topic the user could raise if it feels natural."
    ),
    "boundary_review_note": (
        "Review only: check boundary-sensitive context before drafting any proactive wording."
    ),
    "memory_review_prompt": (
        "Review only: verify recent memory or relationship signals before deciding whether to reply."
    ),
    "do_nothing": "Review only: no proactive action is recommended for now.",
}


class ProactiveDraftGenerator:
    """Deterministically enrich review-only CandidateAction artifacts with draft text."""

    def enrich(
        self,
        candidate: CandidateAction | Mapping[str, object],
    ) -> CandidateAction:
        action = candidate if isinstance(candidate, CandidateAction) else CandidateAction.model_validate(candidate)
        draft_text = self._draft_text_for(action.action_type)
        payload = action.payload.model_copy(update={"draft_text": draft_text})
        return action.model_copy(update={"payload": payload})

    @staticmethod
    def _draft_text_for(action_type: BehaviorActionType) -> str:
        try:
            return _PROACTIVE_DRAFT_TEXTS[action_type]
        except KeyError:  # pragma: no cover - guarded by schema validation
            return "Review only: no proactive draft text is available."


class CandidateActionReviewError(ValueError):
    """Raised when a CandidateAction review decision cannot be applied."""


class CandidateActionReviewService:
    """Manual review service for draft-only CandidateAction records."""

    VALID_DECISIONS = frozenset({"approve", "reject", "freeze", "archive"})
    _DECISION_TO_STATUS: dict[str, str] = {
        "approve": "approved",
        "reject": "rejected",
        "freeze": "frozen",
        "archive": "archived",
    }

    def review_candidate(
        self,
        *,
        candidate: CandidateAction | Mapping[str, object],
        decision: str,
        reviewer_id: str,
        note: str | None = None,
    ) -> CandidateAction:
        action = candidate if isinstance(candidate, CandidateAction) else CandidateAction.model_validate(candidate)
        normalized_decision = self._normalize_decision(decision)
        normalized_reviewer_id = reviewer_id.strip()
        if not normalized_reviewer_id:
            raise CandidateActionReviewError("reviewer_id is required.")

        reviewed = action.model_copy(deep=True)
        self._apply_decision(
            reviewed=reviewed,
            decision=normalized_decision,
            reviewer_id=normalized_reviewer_id,
            note=note,
        )
        return reviewed

    def _normalize_decision(self, decision: str) -> str:
        normalized = decision.strip().lower()
        if normalized not in self.VALID_DECISIONS:
            raise CandidateActionReviewError(
                f"Invalid decision '{decision}'. Must be one of: {', '.join(sorted(self.VALID_DECISIONS))}."
            )
        return normalized

    def _apply_decision(
        self,
        *,
        reviewed: CandidateAction,
        decision: str,
        reviewer_id: str,
        note: str | None,
    ) -> None:
        now = datetime.now(timezone.utc)
        status = self._DECISION_TO_STATUS[decision]
        cleaned_note = note.strip() if note is not None else None
        review_decision = DistilledArtifactReviewDecision(
            status=status,  # type: ignore[arg-type]
            reviewer_id=reviewer_id,
            reviewer_name=None,
            reviewed_at=now,
            notes=[cleaned_note] if cleaned_note else [],
        )

        reviewed.review_metadata.history = [
            *reviewed.review_metadata.history,
            review_decision,
        ]
        reviewed.review_metadata.review_state = "reviewed"
        reviewed.review_metadata.reviewed_by_human = True
        reviewed.review_metadata.last_decision = status  # type: ignore[assignment]
        reviewed.review_metadata.last_reviewed_at = now
        reviewed.review_metadata.last_reviewer_id = reviewer_id
        if cleaned_note:
            reviewed.review_metadata.decision_notes = [
                *reviewed.review_metadata.decision_notes,
                cleaned_note,
            ]

        reviewed.status = status  # type: ignore[assignment]
        reviewed.updated_at = now
