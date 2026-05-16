from __future__ import annotations

from collections.abc import Iterable

from practical_chat_agent.core.models import (
    ChatContext,
    ReplyPlan,
    ReplyPlanCandidate,
    ReplyPlanContextRef,
    ReplyPlanSourceContext,
)
from practical_chat_agent.services.policy import (
    ReplyPlanPolicyEngine,
    ReplyPlanPolicyProfile,
)

_BOUNDARY_REVIEW_ONLY = "Drafts are for human review only."
_BOUNDARY_NO_IMPERSONATION = "Do not imitate the contact or write as if they are speaking."
_BOUNDARY_NO_UNVERIFIED_CLAIMS = "Do not assume unverified feelings, motives, or commitments."
_BOUNDARY_LOW_PRESSURE = "Keep follow-up wording optional and low-pressure."
_BOUNDARY_COMPACT_CONTEXT_ONLY = "Use compact approved-store hints and safe runtime ids only."
_BOUNDARY_THIN_CONTEXT = "When approved context is thin, prefer neutral wording over closeness."
_BOUNDARY_PACED_TONE = "Keep pacing calm and avoid sounding urgent or overly intimate."


class ReplyPlannerError(ValueError):
    """Raised when safe reply planning cannot proceed."""


class ReplyPlanner:
    """Build a review-only ReplyPlan from compact runtime context."""

    def __init__(self, *, policy_engine: ReplyPlanPolicyEngine | None = None) -> None:
        self.policy_engine = policy_engine or ReplyPlanPolicyEngine()

    def generate(self, *, context: ChatContext) -> ReplyPlan:
        contact_id = context.user_id.strip()
        if not contact_id:
            raise ReplyPlannerError("ChatContext.user_id must be a non-empty contact id.")
        self._validate_contact_alignment(context=context, contact_id=contact_id)

        policy_profile = self.policy_engine.build_profile(context=context)
        source_context = self._build_source_context(context=context)
        policy_boundary_summary = self._build_policy_boundary_summary(
            context=context,
            policy_profile=policy_profile,
        )
        candidates = self._build_candidates(
            context=context,
            source_context=source_context,
            policy_profile=policy_profile,
        )
        notes_on_candidate_differences = self._build_candidate_difference_notes(
            context=context,
            policy_profile=policy_profile,
        )

        plan = ReplyPlan(
            contact_id=contact_id,
            source_context=source_context,
            policy_boundary_summary=policy_boundary_summary,
            notes_on_candidate_differences=notes_on_candidate_differences,
            candidates=candidates,
        )
        self._validate_plan(plan=plan, contact_id=contact_id)
        return plan

    def _validate_contact_alignment(self, *, context: ChatContext, contact_id: str) -> None:
        approved_store_context = context.approved_store_context
        if approved_store_context.contact_id and approved_store_context.contact_id != contact_id:
            raise ReplyPlannerError(
                "ApprovedStoreContext.contact_id does not match ChatContext.user_id.",
            )
        contact_skill = approved_store_context.contact_skill
        if contact_skill is not None and contact_skill.contact_id != contact_id:
            raise ReplyPlannerError(
                "Approved contact-skill brief contact_id does not match ChatContext.user_id.",
            )

    def _build_source_context(self, *, context: ChatContext) -> ReplyPlanSourceContext:
        approved_store_context = context.approved_store_context
        contact_skill = approved_store_context.contact_skill
        evidence_refs = self._dedupe(
            approved_store_context.evidence_refs
            + (contact_skill.evidence_refs if contact_skill is not None else [])
            + [
                evidence_ref
                for memory_fact in approved_store_context.memory_facts
                for evidence_ref in memory_fact.evidence_refs
            ],
        )
        return ReplyPlanSourceContext(
            approved_store_status=approved_store_context.status,
            chat_context_summary=self._build_safe_context_summary(context=context),
            recent_event_ids=self._dedupe(event.event_id for event in context.recent_events[:4]),
            memory_hit_ids=self._dedupe(memory.memory_id for memory in context.memory_hits[:4]),
            approved_contact_skill_record_id=contact_skill.record_id if contact_skill is not None else None,
            approved_memory_record_ids=self._dedupe(
                memory_fact.record_id for memory_fact in approved_store_context.memory_facts[:4]
            ),
            approved_store_evidence_refs=evidence_refs[:6],
        )

    def _build_safe_context_summary(self, *, context: ChatContext) -> str:
        approved_store_context = context.approved_store_context
        approved_contact_skill = "yes" if approved_store_context.contact_skill is not None else "no"
        return (
            "Safe runtime context: "
            f"platform={context.platform.value}, "
            f"channel_type={context.channel_type.value}, "
            f"relationship_mode={context.relationship_mode}, "
            f"recent_event_count={len(context.recent_events)}, "
            f"memory_hit_count={len(context.memory_hits)}, "
            f"approved_store_status={approved_store_context.status}, "
            f"approved_contact_skill={approved_contact_skill}, "
            f"approved_memory_count={len(approved_store_context.memory_facts)}."
        )

    def _build_policy_boundary_summary(
        self,
        *,
        context: ChatContext,
        policy_profile: ReplyPlanPolicyProfile,
    ) -> list[str]:
        boundaries = [
            _BOUNDARY_REVIEW_ONLY,
            _BOUNDARY_NO_IMPERSONATION,
            _BOUNDARY_NO_UNVERIFIED_CLAIMS,
            _BOUNDARY_LOW_PRESSURE,
            _BOUNDARY_COMPACT_CONTEXT_ONLY,
        ]
        if policy_profile.thin_context:
            boundaries.append(_BOUNDARY_THIN_CONTEXT)
        boundaries.extend(policy_profile.policy_boundary_summary)
        return self._dedupe(boundaries)

    def _build_candidates(
        self,
        *,
        context: ChatContext,
        source_context: ReplyPlanSourceContext,
        policy_profile: ReplyPlanPolicyProfile,
    ) -> list[ReplyPlanCandidate]:
        approved_store_context = context.approved_store_context
        contact_skill = approved_store_context.contact_skill
        relationship_type = contact_skill.relationship_type if contact_skill is not None else "unknown"

        drafts = self._draft_templates(
            relationship_type=relationship_type,
            policy_profile=policy_profile,
        )
        shared_boundary_reminders = self._shared_boundary_reminders(
            context=context,
            policy_profile=policy_profile,
        )
        approved_contact_skill_ref = self._optional_ref(
            ref_type="approved_contact_skill_record",
            ref_id=source_context.approved_contact_skill_record_id,
            note="approved relationship brief",
        )
        approved_memory_ref = self._optional_ref(
            ref_type="approved_memory_fact_record",
            ref_id=source_context.approved_memory_record_ids[0] if source_context.approved_memory_record_ids else None,
            note="approved memory brief",
        )
        approved_evidence_ref = self._optional_ref(
            ref_type="approved_store_evidence_ref",
            ref_id=source_context.approved_store_evidence_refs[0] if source_context.approved_store_evidence_refs else None,
            note="approved store evidence",
        )
        recent_event_ref = self._optional_ref(
            ref_type="recent_event",
            ref_id=source_context.recent_event_ids[0] if source_context.recent_event_ids else None,
            note="recent runtime event",
        )
        memory_hit_ref = self._optional_ref(
            ref_type="memory_hit",
            ref_id=source_context.memory_hit_ids[0] if source_context.memory_hit_ids else None,
            note="runtime memory hit",
        )
        review_only_ref = ReplyPlanContextRef(
            ref_type="policy_boundary",
            ref_id="boundary_review_only",
            note=_BOUNDARY_REVIEW_ONLY,
        )
        low_pressure_ref = ReplyPlanContextRef(
            ref_type="policy_boundary",
            ref_id="boundary_low_pressure",
            note=_BOUNDARY_LOW_PRESSURE,
        )
        paced_tone_ref = ReplyPlanContextRef(
            ref_type="policy_boundary",
            ref_id="boundary_paced_tone",
            note=_BOUNDARY_PACED_TONE,
        )
        relationship_brief_note = (
            "approved relationship brief"
            if approved_contact_skill_ref is not None
            else "runtime-only context"
        )
        context_caution_note = (
            " The context looks sensitive or thin, so the wording stays deliberately contained."
            if policy_profile.conservative_mode
            else ""
        )

        candidates = [
            self._build_candidate(
                policy_profile=policy_profile,
                approach_label="conservative_acknowledgment",
                priority_rank=1,
                draft_text=drafts[0],
                rationale=(
                    "Keeps the reply low-pressure and reviewable while staying anchored to "
                    f"{relationship_brief_note}.{context_caution_note}"
                ),
                supporting_context_refs=self._refs_for_candidate(
                    approved_contact_skill_ref,
                    recent_event_ref,
                    review_only_ref,
                ),
                base_risk_flags=[],
                boundary_reminders=self._candidate_boundaries(shared_boundary_reminders, _BOUNDARY_REVIEW_ONLY),
                base_confidence=0.78 if approved_contact_skill_ref is not None else 0.68,
            ),
            self._build_candidate(
                policy_profile=policy_profile,
                approach_label="optional_follow_up",
                priority_rank=2,
                draft_text=drafts[1],
                rationale=(
                    "Keeps a low-pressure reopening option available without assuming the contact "
                    "owes more detail, using only compact approved-store hints and safe runtime references."
                ),
                supporting_context_refs=self._refs_for_candidate(
                    approved_memory_ref,
                    recent_event_ref,
                    low_pressure_ref,
                ),
                base_risk_flags=["invites_more_disclosure"],
                boundary_reminders=self._candidate_boundaries(shared_boundary_reminders, _BOUNDARY_LOW_PRESSURE),
                base_confidence=0.71 if approved_memory_ref is not None else 0.63,
            ),
            self._build_candidate(
                policy_profile=policy_profile,
                approach_label="paced_next_step",
                priority_rank=3,
                draft_text=drafts[2],
                rationale=(
                    "Offers a paced next-step frame so the user can stay responsive without "
                    "sounding urgent, overly intimate, or falsely certain."
                ),
                supporting_context_refs=self._refs_for_candidate(
                    approved_evidence_ref,
                    memory_hit_ref,
                    paced_tone_ref,
                ),
                base_risk_flags=["tone_requires_review"],
                boundary_reminders=self._candidate_boundaries(shared_boundary_reminders, _BOUNDARY_PACED_TONE),
                base_confidence=0.66 if approved_evidence_ref is not None else 0.58,
            ),
        ]
        return candidates

    def _build_candidate_difference_notes(
        self,
        *,
        context: ChatContext,
        policy_profile: ReplyPlanPolicyProfile,
    ) -> list[str]:
        notes = [
            "Candidate 1 acknowledges the message without extending the thread.",
            "Candidate 2 adds an optional follow-up that invites clarification.",
            "Candidate 3 suggests a paced next step and needs closer tone review.",
        ]
        if policy_profile.conservative_mode:
            notes[1] = "Candidate 2 keeps a no-pressure reopening option instead of a direct push for more detail."
            notes[2] = "Candidate 3 preserves pacing while explicitly avoiding action-pushing or intimacy escalation."
        if context.approved_store_context.status != "loaded":
            notes.append("Approved store context is thin, so all options stay on the conservative side.")
        if policy_profile.boundary_sensitive:
            notes.append("Sensitive or boundary-heavy context shifted the wording toward acknowledgment and slower pacing.")
        return notes

    def _shared_boundary_reminders(
        self,
        *,
        context: ChatContext,
        policy_profile: ReplyPlanPolicyProfile,
    ) -> list[str]:
        reminders = []
        contact_skill = context.approved_store_context.contact_skill
        if contact_skill is not None:
            reminders.extend(contact_skill.boundary_reminders[:2])
            reminders.extend(contact_skill.strategy_hints[:1])
        reminders.extend(
            [
                _BOUNDARY_NO_IMPERSONATION,
                _BOUNDARY_NO_UNVERIFIED_CLAIMS,
            ],
        )
        reminders.extend(policy_profile.shared_boundary_reminders)
        if policy_profile.thin_context:
            reminders.append(_BOUNDARY_THIN_CONTEXT)
        return self._dedupe(reminders)

    @staticmethod
    def _candidate_boundaries(shared_boundaries: list[str], *candidate_boundaries: str) -> list[str]:
        return ReplyPlanner._dedupe([*shared_boundaries, *candidate_boundaries])

    def _build_candidate(
        self,
        *,
        policy_profile: ReplyPlanPolicyProfile,
        approach_label: str,
        priority_rank: int,
        draft_text: str,
        rationale: str,
        supporting_context_refs: list[ReplyPlanContextRef],
        base_risk_flags: list[str],
        boundary_reminders: list[str],
        base_confidence: float,
    ) -> ReplyPlanCandidate:
        assessment = self.policy_engine.assess_candidate(
            policy_profile=policy_profile,
            candidate_text=draft_text,
            approach_label=approach_label,
        )
        return ReplyPlanCandidate(
            approach_label=approach_label,
            priority_rank=priority_rank,
            draft_text=draft_text,
            rationale=rationale,
            supporting_context_refs=supporting_context_refs,
            risk_flags=self._dedupe([*base_risk_flags, *assessment.risk_flags]),
            boundary_reminders=self._candidate_boundaries(
                boundary_reminders,
                *assessment.boundary_reminders,
            ),
            confidence=self._clamp_confidence(base_confidence - assessment.confidence_penalty),
        )

    @staticmethod
    def _refs_for_candidate(*refs: ReplyPlanContextRef | None) -> list[ReplyPlanContextRef]:
        result = [ref for ref in refs if ref is not None]
        if not result:
            raise ReplyPlannerError("Each candidate must retain at least one safe supporting context ref.")
        return result

    @staticmethod
    def _optional_ref(
        *,
        ref_type: str,
        ref_id: str | None,
        note: str | None = None,
    ) -> ReplyPlanContextRef | None:
        if ref_id is None or not ref_id.strip():
            return None
        return ReplyPlanContextRef(ref_type=ref_type, ref_id=ref_id, note=note)

    @staticmethod
    def _draft_templates(
        *,
        relationship_type: str,
        policy_profile: ReplyPlanPolicyProfile,
    ) -> tuple[str, str, str]:
        if policy_profile.conservative_mode:
            if relationship_type == "colleague" or policy_profile.practical_tone:
                return (
                    "收到，这个点我先记下。",
                    "这个点先放在这里；如果你之后愿意，再补一句重点也可以。",
                    "先不往前推，等你方便的时候再决定要不要继续展开。",
                )
            return (
                "收到，我先接住这个点，你不用现在展开。",
                "这个点我先记下；如果你之后愿意，再补一句也可以。",
                "先不把话题往前推，等你想说的时候再继续也可以。",
            )
        if relationship_type in {"friend", "classmate", "family"}:
            return (
                "收到，我先接住你这条消息。",
                "我先接住这个点，如果你愿意，也可以继续说说你现在最在意的是哪一部分。",
                "我先把这个点记下，等你方便的时候我们再慢慢展开，不急着一下说完。",
            )
        if relationship_type == "colleague":
            return (
                "收到，我先记下这个点。",
                "收到。如果你愿意，可以补一句你现在最想先处理哪一部分。",
                "这个点我先接住；等你方便的时候，我们再把下一步顺一顺。",
            )
        return (
            "收到，我先接住这条消息。",
            "我先接住这个点，如果你愿意，也可以再补充一点你现在最在意的部分。",
            "我先把这个点记下，后面按你的节奏慢慢展开也可以。",
        )

    @staticmethod
    def _validate_plan(*, plan: ReplyPlan, contact_id: str) -> None:
        if plan.contact_id != contact_id:
            raise ReplyPlannerError("ReplyPlan.contact_id must match the routed contact id.")
        priority_ranks = [candidate.priority_rank for candidate in plan.candidates]
        if len(priority_ranks) != len(set(priority_ranks)):
            raise ReplyPlannerError("ReplyPlan candidate priority_rank values must be unique.")
        if sorted(priority_ranks) != list(range(1, len(priority_ranks) + 1)):
            raise ReplyPlannerError("ReplyPlan candidate priority_rank values must form a stable 1..N sequence.")

    @staticmethod
    def _clamp_confidence(value: float) -> float:
        return max(0.0, min(1.0, round(value, 2)))

    @staticmethod
    def _dedupe(values: Iterable[object]) -> list[str]:
        seen: set[str] = set()
        result: list[str] = []
        for value in values:
            if value is None:
                continue
            text = str(value).strip()
            if not text or text in seen:
                continue
            seen.add(text)
            result.append(text)
        return result
