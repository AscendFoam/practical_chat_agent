from __future__ import annotations

import json
import re
import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from practical_chat_agent.core.models import (
    ChunkSummary,
    ContactSkillCandidate,
    ContactSkillCommunicationStyle,
    ContactSkillImportantEvent,
    ContactSkillPattern,
    ContactSkillRelationshipState,
    ContactSkillReplyStrategy,
    ContactSkillStoreFile,
    ContactSkillStoreRecord,
    ContactSkillTopicPreference,
    ContactSkillUserSidePreferences,
    DistilledArtifactReviewMetadata,
    DistilledArtifactReviewDecision,
    DistilledArtifactSourceMetadata,
    DistillationStatus,
    MemoryFactStoreFile,
    MemoryFactStoreRecord,
    MemoryFactCandidate,
    utc_now,
)

_CONCERN_TOKENS = (
    "worry",
    "concern",
    "fear",
    "pressure",
    "behind",
    "unreachable",
    "not passing",
    "national line",
)

_PRACTICAL_SUPPORT_TOKENS = (
    "tutoring",
    "support",
    "help",
    "review the materials first",
    "review materials first",
    "foundation",
    "progress",
)


class ContactSkillBuilderError(ValueError):
    """Raised when contact skill builder inputs or outputs are invalid."""


@dataclass(frozen=True)
class ContactSkillBuildResult:
    output_dir: Path | None
    candidate: ContactSkillCandidate
    review_markdown: str
    report: dict[str, Any]


@dataclass(frozen=True)
class FileStoreSaveResult:
    output_path: Path
    record_count: int
    statuses: list[DistillationStatus]


@dataclass(frozen=True)
class StoreRecordSummary:
    record_id: str
    artifact_type: str
    artifact_id: str
    status: DistillationStatus
    review_state: str
    reviewed_by_human: bool
    last_decision: DistillationStatus | None
    evidence_validation_status: str
    approval_ready_after_validation: bool | None
    runtime_ready_after_validation: bool | None
    missing_ref_count: int | None
    safe_path: str
    review_artifact_path: str | None
    approval_block_reasons: list[str]
    runtime_block_reasons: list[str]


@dataclass(frozen=True)
class StoreReviewListResult:
    input_path: Path
    run_dir: Path
    validation_report_path: Path | None
    validation_report_found: bool
    records: list[StoreRecordSummary]


@dataclass(frozen=True)
class StoreReviewDecisionResult:
    decision: DistillationStatus
    input_path: Path
    run_dir: Path
    validation_report_path: Path | None
    saved_output_path: Path
    record: StoreRecordSummary


@dataclass(frozen=True)
class StoreReviewExportResult:
    input_path: Path
    run_dir: Path
    validation_report_path: Path | None
    output_path: Path
    record_count: int
    record_ids: list[str]


@dataclass
class _StoreWorkspace:
    input_path: Path
    run_dir: Path
    memory_store: MemoryFactStoreFile | None = None
    memory_input_path: Path | None = None
    memory_output_path: Path | None = None
    contact_skill_store: ContactSkillStoreFile | None = None
    contact_skill_input_path: Path | None = None
    contact_skill_output_path: Path | None = None


@dataclass(frozen=True)
class _StoreRecordHandle:
    store_kind: str
    index: int
    input_path: Path
    output_path: Path
    record: MemoryFactStoreRecord | ContactSkillStoreRecord


@dataclass(frozen=True)
class _ValidationReportContext:
    report: dict[str, Any] | None
    report_path: Path | None
    summary_status: str
    records_by_id: dict[str, dict[str, Any]]


class ContactSkillBuilderService:
    """Build a conservative ContactSkill candidate from validated distillation outputs."""

    def __init__(self) -> None:
        self._repo_root = Path.cwd().resolve()
        self._private_distilled_root = (self._repo_root / "private" / "distilled").resolve()

    def build_contact_skill(
        self,
        *,
        input_path: Path,
        output_dir: Path | None,
        contact_id: str | None = None,
        dry_run: bool = False,
    ) -> ContactSkillBuildResult:
        summaries_path, facts_path = self._resolve_input_files(input_path)
        summaries = self._load_chunk_summaries(summaries_path=summaries_path)
        facts = self._load_memory_facts(facts_path=facts_path)
        filtered_summaries, filtered_facts, resolved_contact_id = self._filter_contact_scope(
            chunk_summaries=summaries,
            memory_facts=facts,
            contact_id=contact_id,
        )
        if not filtered_summaries:
            raise ContactSkillBuilderError("No chunk summaries available for the requested contact.")

        candidate = self._build_candidate(
            contact_id=resolved_contact_id,
            chunk_summaries=filtered_summaries,
            memory_facts=filtered_facts,
        )

        from practical_chat_agent.exporters.contact_skill_markdown import (  # noqa: PLC0415
            render_contact_skill_review_markdown,
        )

        review_markdown = render_contact_skill_review_markdown(
            candidate=candidate,
            chunk_summaries=filtered_summaries,
            memory_facts=filtered_facts,
        )

        resolved_output_dir: Path | None = None
        if not dry_run:
            resolved_output_dir = self._resolve_output_dir(output_dir or summaries_path.parent)
            resolved_output_dir.mkdir(parents=True, exist_ok=True)
            self._write_candidate(
                output_path=resolved_output_dir / "contact_skill.candidate.json",
                candidate=candidate,
            )
            self._write_review_markdown(
                output_path=resolved_output_dir / "contact_skill.review.md",
                markdown=review_markdown,
            )
            self._write_run_report(
                output_dir=resolved_output_dir,
                skill_report=self._build_report(
                    candidate=candidate,
                    chunk_summaries=filtered_summaries,
                    memory_facts=filtered_facts,
                    input_dir=summaries_path.parent,
                    output_dir=resolved_output_dir,
                    dry_run=dry_run,
                ),
            )

        report = self._build_report(
            candidate=candidate,
            chunk_summaries=filtered_summaries,
            memory_facts=filtered_facts,
            input_dir=summaries_path.parent,
            output_dir=resolved_output_dir,
            dry_run=dry_run,
        )
        return ContactSkillBuildResult(
            output_dir=resolved_output_dir,
            candidate=candidate,
            review_markdown=review_markdown,
            report=report,
        )

    def _build_candidate(
        self,
        *,
        contact_id: str,
        chunk_summaries: list[ChunkSummary],
        memory_facts: list[MemoryFactCandidate],
    ) -> ContactSkillCandidate:
        contact_facts = [fact for fact in memory_facts if fact.subject_id == contact_id]
        chunk_confidence = self._average(summary.confidence for summary in chunk_summaries)
        fact_confidence = self._average(fact.confidence for fact in contact_facts)
        if contact_facts:
            candidate_confidence = self._clamp((chunk_confidence + fact_confidence) / 2.0)
        else:
            candidate_confidence = chunk_confidence

        candidate = ContactSkillCandidate(
            contact_id=contact_id,
            relationship_type=self._infer_relationship_type(
                chunk_summaries=chunk_summaries,
                memory_facts=contact_facts,
            ),
            status="candidate",
            confidence=candidate_confidence,
            sensitivity=self._max_sensitivity(
                [summary.sensitivity for summary in chunk_summaries]
                + [fact.sensitivity for fact in memory_facts],
                default="medium",
            ),
            evidence_refs=collect_source_refs(
                chunk_summaries=chunk_summaries,
                memory_facts=memory_facts,
            ),
            source_chunk_ids=self._unique(summary.chunk_id for summary in chunk_summaries),
            source_memory_ids=self._unique(fact.memory_id for fact in memory_facts),
            relationship_state=self._build_relationship_state(
                contact_id=contact_id,
                chunk_summaries=chunk_summaries,
                memory_facts=memory_facts,
            ),
            communication_style=self._build_communication_style(
                contact_id=contact_id,
                chunk_summaries=chunk_summaries,
                memory_facts=memory_facts,
            ),
            preferred_topics=self._build_preferred_topics(contact_id=contact_id, memory_facts=memory_facts),
            avoid_topics=self._build_avoid_topics(contact_id=contact_id, memory_facts=memory_facts),
            important_events=self._build_important_events(contact_id=contact_id, memory_facts=memory_facts),
            stable_preferences=self._build_stable_preferences(
                contact_id=contact_id,
                chunk_summaries=chunk_summaries,
                memory_facts=memory_facts,
            ),
            emotional_patterns=self._build_emotional_patterns(contact_id=contact_id, memory_facts=memory_facts),
            user_side_preferences=self._build_user_side_preferences(memory_facts=memory_facts),
            reply_strategy=self._build_reply_strategy(
                contact_id=contact_id,
                memory_facts=memory_facts,
            ),
            review_notes=self._build_review_notes(
                contact_id=contact_id,
                chunk_summaries=chunk_summaries,
                memory_facts=memory_facts,
            ),
        )
        self._assert_candidate(candidate=candidate)
        return candidate

    def _build_relationship_state(
        self,
        *,
        contact_id: str,
        chunk_summaries: list[ChunkSummary],
        memory_facts: list[MemoryFactCandidate],
    ) -> ContactSkillRelationshipState:
        contact_facts = [fact for fact in memory_facts if fact.subject_id == contact_id]
        user_facts = [fact for fact in memory_facts if fact.subject_id == "user"]
        closeness = self._clamp(0.22 + min(len(contact_facts), 6) * 0.08)
        trust_level = self._clamp(0.28 + len(chunk_summaries) * 0.08 + len(contact_facts) * 0.05)

        initiative_balance = "unknown"
        if user_facts and contact_facts:
            if len(user_facts) > len(contact_facts):
                initiative_balance = "user_leads_more"
            elif len(contact_facts) > len(user_facts):
                initiative_balance = "contact_leads_more"
            else:
                initiative_balance = "balanced"
        elif user_facts:
            initiative_balance = "user_leads_more"
        elif contact_facts:
            initiative_balance = "contact_leads_more"

        evidence_refs = self._best_refs_for_kind(
            memory_facts=contact_facts,
            kinds=("relationship", "reflection", "semantic", "episodic"),
            fallback_refs=self._summary_evidence_refs(chunk_summaries),
            max_refs=6,
        )
        confidence_inputs = [fact.confidence for fact in contact_facts] or [summary.confidence for summary in chunk_summaries]
        sensitivity_inputs = [fact.sensitivity for fact in contact_facts] or [summary.sensitivity for summary in chunk_summaries]
        return ContactSkillRelationshipState(
            current_status=self._infer_current_status(
                chunk_summaries=chunk_summaries,
                memory_facts=contact_facts,
            ),
            closeness=closeness,
            trust_level=trust_level,
            interaction_frequency=self._infer_interaction_frequency(chunk_summaries=chunk_summaries),
            initiative_balance=initiative_balance,
            confidence=self._average(confidence_inputs),
            evidence_refs=evidence_refs,
            sensitivity=self._max_sensitivity(sensitivity_inputs, default="medium"),
            status="candidate",
        )

    def _build_communication_style(
        self,
        *,
        contact_id: str,
        chunk_summaries: list[ChunkSummary],
        memory_facts: list[MemoryFactCandidate],
    ) -> ContactSkillCommunicationStyle:
        contact_facts = [fact for fact in memory_facts if fact.subject_id == contact_id]
        joined = self._joined_text(chunk_summaries=chunk_summaries, memory_facts=contact_facts)

        tone = "casual"
        if self._contains_any(joined, _CONCERN_TOKENS):
            tone = "reserved"
        elif self._contains_any(joined, ("thanks", "support", "help")):
            tone = "warm"

        message_length = "medium"
        max_message_count = max((summary.message_count for summary in chunk_summaries), default=0)
        if max_message_count <= 6:
            message_length = "short"
        elif max_message_count >= 18:
            message_length = "long"

        directness = "medium"
        if self._contains_any(
            joined,
            ("introduces self", "target school", "estimated score", "exam", "score"),
        ):
            directness = "high"
        elif not joined:
            directness = "unknown"

        response_latency = "unknown"
        interaction_flags = {flag for summary in chunk_summaries for flag in summary.interaction_flags}
        if "reply" in interaction_flags and len(chunk_summaries) > 1:
            response_latency = "mixed_or_unknown"

        evidence_refs = self._best_refs_for_kind(
            memory_facts=contact_facts,
            kinds=("semantic", "episodic", "reflection"),
            fallback_refs=self._summary_evidence_refs(chunk_summaries),
            max_refs=6,
        )
        confidence_inputs = [summary.confidence for summary in chunk_summaries] + [fact.confidence for fact in contact_facts]
        return ContactSkillCommunicationStyle(
            message_length=message_length,
            tone=tone,
            response_latency=response_latency,
            directness=directness,
            confidence=self._average(confidence_inputs),
            evidence_refs=evidence_refs,
            sensitivity=self._max_sensitivity(
                [summary.sensitivity for summary in chunk_summaries] + [fact.sensitivity for fact in contact_facts],
                default="medium",
            ),
            status="candidate",
        )

    def _build_preferred_topics(
        self,
        *,
        contact_id: str,
        memory_facts: list[MemoryFactCandidate],
    ) -> list[ContactSkillTopicPreference]:
        items: list[ContactSkillTopicPreference] = []
        for fact in memory_facts:
            if fact.subject_id != contact_id:
                continue
            if self._contains_any(fact.claim, _CONCERN_TOKENS):
                continue
            topic = self._extract_topic(fact.claim)
            if topic is None or topic in {"score expectations", "score pressure", "performance pressure"}:
                continue
            items.append(
                ContactSkillTopicPreference(
                    topic=topic,
                    reason="Derived from explicit factual or reflective sharing in the current sample.",
                    claim=f"Contact appears open to discussion about {topic} when it stays grounded in current context.",
                    evidence_refs=fact.evidence_refs,
                    confidence=self._clamp((fact.confidence + fact.importance) / 2.0),
                    sensitivity=fact.sensitivity,
                    status="candidate",
                ),
            )
        return self._dedupe_topic_preferences(items)[:4]

    def _build_avoid_topics(
        self,
        *,
        contact_id: str,
        memory_facts: list[MemoryFactCandidate],
    ) -> list[ContactSkillTopicPreference]:
        items: list[ContactSkillTopicPreference] = []
        for fact in memory_facts:
            if fact.subject_id != contact_id:
                continue
            if not self._contains_any(fact.claim, _CONCERN_TOKENS):
                continue
            topic = self._extract_topic(fact.claim) or "current pressure points"
            items.append(
                ContactSkillTopicPreference(
                    topic=topic,
                    reason="The current sample contains stress or worry signals around this topic.",
                    claim=f"Handle {topic} gently and avoid pushing for certainty or guarantees.",
                    evidence_refs=fact.evidence_refs,
                    confidence=self._clamp(fact.confidence + 0.08),
                    sensitivity=self._max_sensitivity([fact.sensitivity, "medium"], default="medium"),
                    status="candidate",
                ),
            )
        return self._dedupe_topic_preferences(items)[:4]

    def _build_important_events(
        self,
        *,
        contact_id: str,
        memory_facts: list[MemoryFactCandidate],
    ) -> list[ContactSkillImportantEvent]:
        items: list[ContactSkillImportantEvent] = []
        for fact in sorted(memory_facts, key=lambda item: item.importance, reverse=True):
            if fact.subject_id != contact_id:
                continue
            if self._contains_any(fact.claim, ("introduces self", "introduces themselves", "name is")):
                continue
            topic = self._extract_topic(fact.claim)
            if topic is None and fact.importance < 0.75:
                continue
            items.append(
                ContactSkillImportantEvent(
                    event=fact.claim,
                    claim="This item may matter for future relationship-aware follow-up context.",
                    evidence_refs=fact.evidence_refs,
                    confidence=fact.confidence,
                    sensitivity=fact.sensitivity,
                    status="candidate",
                    importance=fact.importance,
                ),
            )
            if len(items) >= 4:
                break
        return items

    def _build_stable_preferences(
        self,
        *,
        contact_id: str,
        chunk_summaries: list[ChunkSummary],
        memory_facts: list[MemoryFactCandidate],
    ) -> list[ContactSkillPattern]:
        items: list[ContactSkillPattern] = []
        contact_facts = [fact for fact in memory_facts if fact.subject_id == contact_id]
        user_facts = [fact for fact in memory_facts if fact.subject_id == "user"]
        study_fact = next(
            (
                fact
                for fact in contact_facts
                if self._extract_topic(fact.claim) in {"study progress", "exam preparation"}
            ),
            None,
        )
        school_fact = next((fact for fact in contact_facts if self._extract_topic(fact.claim) == "school plans"), None)
        user_support_fact = next(
            (
                fact
                for fact in user_facts
                if self._contains_any(fact.claim, _PRACTICAL_SUPPORT_TOKENS)
            ),
            None,
        )
        if study_fact is not None and (school_fact is not None or user_support_fact is not None):
            evidence_refs = self._unique(
                list(study_fact.evidence_refs)
                + list(school_fact.evidence_refs if school_fact is not None else [])
                + list(user_support_fact.evidence_refs if user_support_fact is not None else [])
                + self._summary_evidence_refs(chunk_summaries)[:2]
            )
            items.append(
                ContactSkillPattern(
                    pattern="Keep the exchange concrete, practical, and anchored in the contact's current situation.",
                    claim="Current sample suggests practical, study-specific context is a stronger footing than abstract reassurance alone.",
                    evidence_refs=evidence_refs[:6],
                    confidence=self._average(
                        [
                            study_fact.confidence,
                            school_fact.confidence if school_fact is not None else study_fact.confidence,
                            user_support_fact.confidence if user_support_fact is not None else study_fact.confidence,
                        ],
                    ),
                    sensitivity=self._max_sensitivity(
                        [
                            study_fact.sensitivity,
                            school_fact.sensitivity if school_fact is not None else study_fact.sensitivity,
                        ],
                        default="medium",
                    ),
                    status="candidate",
                ),
            )
        return items

    def _build_emotional_patterns(
        self,
        *,
        contact_id: str,
        memory_facts: list[MemoryFactCandidate],
    ) -> list[ContactSkillPattern]:
        items: list[ContactSkillPattern] = []
        contact_facts = [fact for fact in memory_facts if fact.subject_id == contact_id]
        concern_fact = next((fact for fact in contact_facts if self._contains_any(fact.claim, _CONCERN_TOKENS)), None)
        if concern_fact is not None:
            items.append(
                ContactSkillPattern(
                    pattern="Performance pressure can surface quickly; acknowledge pressure before offering advice.",
                    claim="The current sample contains explicit worry or fear signals around outcomes.",
                    evidence_refs=concern_fact.evidence_refs,
                    confidence=concern_fact.confidence,
                    sensitivity=self._max_sensitivity([concern_fact.sensitivity, "medium"], default="medium"),
                    status="candidate",
                ),
            )

        self_critical_fact = next(
            (
                fact
                for fact in contact_facts
                if self._contains_any(fact.claim, ("behind", "rushed", "feels behind"))
            ),
            None,
        )
        if self_critical_fact is not None:
            items.append(
                ContactSkillPattern(
                    pattern="When discussing progress, lead with validation before switching into suggestions or problem solving.",
                    claim="The contact describes study progress in a self-critical way in the current sample.",
                    evidence_refs=self_critical_fact.evidence_refs,
                    confidence=self_critical_fact.confidence,
                    sensitivity=self._max_sensitivity([self_critical_fact.sensitivity, "medium"], default="medium"),
                    status="candidate",
                ),
            )
        return items[:2]

    def _build_user_side_preferences(
        self,
        *,
        memory_facts: list[MemoryFactCandidate],
    ) -> ContactSkillUserSidePreferences:
        user_facts = [fact for fact in memory_facts if fact.subject_id == "user"]
        user_goal = "Keep the conversation practical, supportive, and non-pressuring."
        if any(self._contains_any(fact.claim, ("review the materials first", "review materials first")) for fact in user_facts):
            user_goal = "Understand the contact's current situation first, then offer measured support."
        elif any(self._contains_any(fact.claim, ("tutoring", "support", "help")) for fact in user_facts):
            user_goal = "Be useful without becoming pushy or overconfident."
        return ContactSkillUserSidePreferences(
            user_goal=user_goal,
            boundaries=[
                "Do not pressure the contact for vulnerable details or performance guarantees.",
                "Do not imitate the contact or speculate about what they would say next.",
                "Keep any suggested reply human-reviewed before it is sent.",
            ],
            preferred_reply_style="Sincere, practical, and low-pressure.",
        )

    def _build_reply_strategy(
        self,
        *,
        contact_id: str,
        memory_facts: list[MemoryFactCandidate],
    ) -> ContactSkillReplyStrategy:
        sensitive = any(
            fact.subject_id == contact_id and self._contains_any(fact.claim, _CONCERN_TOKENS)
            for fact in memory_facts
        )
        default = "Acknowledge the contact's current situation, then add one practical and low-pressure follow-up."
        if any(
            fact.subject_id == "user" and self._contains_any(fact.claim, ("review the materials first", "review materials first"))
            for fact in memory_facts
        ):
            default = "Reflect the current situation first, then offer one measured next step only after the context is understood."
        return ContactSkillReplyStrategy(
            default=default,
            when_contact_is_cold="Reduce question density and leave room for the contact to disengage naturally.",
            when_contact_opens_topic="Stay with the topic the contact already opened instead of switching into relationship talk.",
            for_sensitive_topics=(
                "Acknowledge pressure first, avoid certainty theater, and ask permission before going deeper."
                if sensitive
                else "Keep sensitive topics brief, non-invasive, and optional."
            ),
        )

    def _build_review_notes(
        self,
        *,
        contact_id: str,
        chunk_summaries: list[ChunkSummary],
        memory_facts: list[MemoryFactCandidate],
    ) -> list[str]:
        notes = [
            "Candidate only; requires human review before any downstream planner use.",
            "Do not use this artifact for persona clone, impersonation, or autonomous contact simulation.",
        ]
        if any(summary.risk_flags for summary in chunk_summaries):
            notes.append(
                "Some supporting chunks carry mixed-message or forwarded-content risk flags; confirm those claims before approval.",
            )
        if not any(fact.subject_id == contact_id for fact in memory_facts):
            notes.append("Contact-specific memory facts were sparse, so this candidate leans more heavily on chunk-level summaries.")
        if any(fact.subject_id == "user" for fact in memory_facts):
            notes.append("User-side facts were used only to shape reply strategy and boundaries, not to define the contact.")
        if any(self._contains_any(fact.claim, _CONCERN_TOKENS) for fact in memory_facts if fact.subject_id == contact_id):
            notes.append("Review whether score or pressure-related claims should be narrowed further before approval.")
        return notes

    def _assert_candidate(self, *, candidate: ContactSkillCandidate) -> None:
        if candidate.status != "candidate":
            raise ContactSkillBuilderError("ContactSkill candidate must stay in candidate status.")
        if not candidate.evidence_refs:
            raise ContactSkillBuilderError("ContactSkill candidate must include evidence_refs.")

    def _load_chunk_summaries(self, *, summaries_path: Path) -> list[ChunkSummary]:
        summaries: list[ChunkSummary] = []
        with summaries_path.open("r", encoding="utf-8") as handle:
            for line_no, raw_line in enumerate(handle, start=1):
                line = raw_line.strip()
                if not line:
                    continue
                try:
                    payload = json.loads(line)
                except json.JSONDecodeError as exc:
                    raise ContactSkillBuilderError(
                        f"chunk_summaries.jsonl line {line_no} is invalid JSON.",
                    ) from exc
                summaries.append(ChunkSummary.model_validate(payload))
        return summaries

    def _load_memory_facts(self, *, facts_path: Path) -> list[MemoryFactCandidate]:
        facts: list[MemoryFactCandidate] = []
        with facts_path.open("r", encoding="utf-8") as handle:
            for line_no, raw_line in enumerate(handle, start=1):
                line = raw_line.strip()
                if not line:
                    continue
                try:
                    payload = json.loads(line)
                except json.JSONDecodeError as exc:
                    raise ContactSkillBuilderError(
                        f"memory_facts.jsonl line {line_no} is invalid JSON.",
                    ) from exc
                facts.append(MemoryFactCandidate.model_validate(payload))
        return facts

    def _filter_contact_scope(
        self,
        *,
        chunk_summaries: list[ChunkSummary],
        memory_facts: list[MemoryFactCandidate],
        contact_id: str | None,
    ) -> tuple[list[ChunkSummary], list[MemoryFactCandidate], str]:
        available_contact_ids = self._unique(summary.contact_id for summary in chunk_summaries)
        if not available_contact_ids:
            raise ContactSkillBuilderError("No contact_id found in chunk summaries.")
        resolved_contact_id = contact_id or available_contact_ids[0]
        if resolved_contact_id not in available_contact_ids:
            raise ContactSkillBuilderError(
                f"Requested contact_id {resolved_contact_id} is not present in chunk summaries.",
            )
        filtered_summaries = [summary for summary in chunk_summaries if summary.contact_id == resolved_contact_id]
        filtered_chunk_ids = {summary.chunk_id for summary in filtered_summaries}
        filtered_facts = [
            fact
            for fact in memory_facts
            if (
                fact.subject_id == resolved_contact_id
                or fact.subject_id == "user"
                or any(chunk_id in filtered_chunk_ids for chunk_id in fact.source_chunk_ids)
            )
        ]
        return filtered_summaries, filtered_facts, resolved_contact_id

    def _resolve_input_files(self, input_path: Path) -> tuple[Path, Path]:
        resolved_input = self._resolve_existing_path(input_path)
        self._ensure_within_root(
            candidate=resolved_input,
            root=self._private_distilled_root,
            error_message="Input must stay within private/distilled.",
        )
        if resolved_input.is_dir():
            summaries_path = resolved_input / "chunk_summaries.jsonl"
            facts_path = resolved_input / "memory_facts.jsonl"
            if summaries_path.is_file() and facts_path.is_file():
                return summaries_path, facts_path
            raise ContactSkillBuilderError(
                "Input directory must contain chunk_summaries.jsonl and memory_facts.jsonl.",
            )
        if resolved_input.name != "chunk_summaries.jsonl":
            raise ContactSkillBuilderError("Input file must be chunk_summaries.jsonl.")
        facts_path = resolved_input.parent / "memory_facts.jsonl"
        if not facts_path.is_file():
            raise ContactSkillBuilderError("chunk_summaries.jsonl must live beside memory_facts.jsonl.")
        return resolved_input, facts_path

    def _resolve_existing_path(self, path: Path) -> Path:
        resolved = (self._repo_root / path).resolve() if not path.is_absolute() else path.resolve()
        if not resolved.exists():
            raise ContactSkillBuilderError(f"Input path does not exist: {path}")
        return resolved

    def _resolve_output_dir(self, output_dir: Path) -> Path:
        resolved = (self._repo_root / output_dir).resolve() if not output_dir.is_absolute() else output_dir.resolve()
        self._ensure_within_root(
            candidate=resolved,
            root=self._private_distilled_root,
            error_message="Output must stay within private/distilled.",
        )
        return resolved

    @staticmethod
    def _ensure_within_root(*, candidate: Path, root: Path, error_message: str) -> None:
        try:
            candidate.relative_to(root)
        except ValueError as exc:
            raise ContactSkillBuilderError(error_message) from exc

    def _safe_relative_path(self, path: Path | None) -> str | None:
        if path is None:
            return None
        try:
            return str(path.relative_to(self._repo_root)).replace("\\", "/")
        except ValueError:
            return str(path).replace("\\", "/")

    def _write_candidate(self, *, output_path: Path, candidate: ContactSkillCandidate) -> None:
        output_path.write_text(
            json.dumps(candidate.model_dump(mode="json"), ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    def _write_review_markdown(self, *, output_path: Path, markdown: str) -> None:
        output_path.write_text(markdown.rstrip() + "\n", encoding="utf-8")

    def _write_run_report(self, *, output_dir: Path, skill_report: dict[str, Any]) -> None:
        report_path = output_dir / "run_report.json"
        merged_report: dict[str, Any] = {}
        warnings = list(skill_report.get("warnings", []))
        if report_path.exists():
            try:
                existing_report = json.loads(report_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                warnings.append("existing_run_report_invalid_json")
            else:
                if isinstance(existing_report, dict):
                    merged_report = existing_report
                else:
                    warnings.append("existing_run_report_not_object")
        if warnings:
            skill_report["warnings"] = sorted(set(warnings))
        merged_report["contact_skill"] = skill_report
        existing_output_files = merged_report.get("output_files")
        output_files = list(existing_output_files) if isinstance(existing_output_files, list) else []
        for filename in ("contact_skill.candidate.json", "contact_skill.review.md", "run_report.json"):
            if filename not in output_files:
                output_files.append(filename)
        merged_report["output_files"] = output_files
        report_path.write_text(
            json.dumps(merged_report, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    def _build_report(
        self,
        *,
        candidate: ContactSkillCandidate,
        chunk_summaries: list[ChunkSummary],
        memory_facts: list[MemoryFactCandidate],
        input_dir: Path,
        output_dir: Path | None,
        dry_run: bool,
    ) -> dict[str, Any]:
        contact_facts = [fact for fact in memory_facts if fact.subject_id == candidate.contact_id]
        warnings = self._collect_report_warnings(
            contact_id=candidate.contact_id,
            chunk_summaries=chunk_summaries,
            memory_facts=memory_facts,
        )
        return {
            "tool": "chatlog-build-contact-skill",
            "contact_id": candidate.contact_id,
            "candidate_status": candidate.status,
            "relationship_type": candidate.relationship_type,
            "confidence": candidate.confidence,
            "sensitivity": candidate.sensitivity,
            "source_counts": {
                "chunk_summaries": len(chunk_summaries),
                "memory_facts": len(memory_facts),
                "contact_memory_facts": len(contact_facts),
                "source_chunk_ids": len(candidate.source_chunk_ids),
                "source_memory_ids": len(candidate.source_memory_ids),
                "evidence_refs": len(candidate.evidence_refs),
            },
            "skill_sections": {
                "preferred_topics": len(candidate.preferred_topics),
                "avoid_topics": len(candidate.avoid_topics),
                "important_events": len(candidate.important_events),
                "stable_preferences": len(candidate.stable_preferences),
                "emotional_patterns": len(candidate.emotional_patterns),
                "review_notes": len(candidate.review_notes),
            },
            "warnings": warnings,
            "dry_run": dry_run,
            "input_dir": self._safe_relative_path(input_dir),
            "output_dir": self._safe_relative_path(output_dir),
            "output_files": (
                ["contact_skill.candidate.json", "contact_skill.review.md", "run_report.json"]
                if output_dir is not None
                else []
            ),
        }

    def _collect_report_warnings(
        self,
        *,
        contact_id: str,
        chunk_summaries: list[ChunkSummary],
        memory_facts: list[MemoryFactCandidate],
    ) -> list[str]:
        warnings: list[str] = []
        if any(summary.risk_flags for summary in chunk_summaries):
            warnings.append("source_chunks_have_risk_flags")
        if any("forwarded_records" in summary.interaction_flags for summary in chunk_summaries):
            warnings.append("source_chunks_include_forwarded_records")
        if not any(fact.subject_id == contact_id for fact in memory_facts):
            warnings.append("contact_facts_sparse")
        if any(self._contains_any(fact.claim, _CONCERN_TOKENS) for fact in memory_facts if fact.subject_id == contact_id):
            warnings.append("contains_sensitive_pressure_signals")
        return warnings

    @staticmethod
    def _infer_relationship_type(
        *,
        chunk_summaries: list[ChunkSummary],
        memory_facts: list[MemoryFactCandidate],
    ) -> str:
        joined = " ".join(
            [summary.summary for summary in chunk_summaries] + [fact.claim for fact in memory_facts],
        ).casefold()
        if any(token in joined for token in ("classmate", "schoolmate", "classmate")):
            return "classmate"
        if any(token in joined for token in ("colleague", "coworker", "work", "mentor")):
            return "colleague"
        if any(token in joined for token in ("family", "father", "mother", "brother", "sister")):
            return "family"
        if chunk_summaries or memory_facts:
            return "friend"
        return "unknown"

    def _infer_current_status(
        self,
        *,
        chunk_summaries: list[ChunkSummary],
        memory_facts: list[MemoryFactCandidate],
    ) -> str:
        joined = self._joined_text(chunk_summaries=chunk_summaries, memory_facts=memory_facts)
        if self._contains_any(joined, _CONCERN_TOKENS):
            return "supportive_problem_solving_phase"
        if self._contains_any(joined, _PRACTICAL_SUPPORT_TOKENS):
            return "practical_support_exchange"
        if chunk_summaries or memory_facts:
            return "low_frequency_but_continuing"
        return "unknown"

    @staticmethod
    def _infer_interaction_frequency(*, chunk_summaries: list[ChunkSummary]) -> str:
        total_messages = sum(summary.message_count for summary in chunk_summaries)
        if total_messages >= 30:
            return "high"
        if total_messages >= 10:
            return "medium"
        if total_messages > 0:
            return "low"
        return "unknown"

    @staticmethod
    def _extract_topic(claim: str) -> str | None:
        lowered = claim.casefold()
        mapping = (
            ("target school", "school plans"),
            ("school", "school plans"),
            ("exam prep", "exam preparation"),
            ("exam", "exam preparation"),
            ("study", "study progress"),
            ("preparation", "study progress"),
            ("materials", "study progress"),
            ("score", "score expectations"),
            ("national line", "score pressure"),
            ("tutoring", "practical support"),
            ("support", "practical support"),
        )
        for needle, topic in mapping:
            if needle in lowered:
                return topic
        return None

    @staticmethod
    def _best_refs_for_kind(
        *,
        memory_facts: list[MemoryFactCandidate],
        kinds: tuple[str, ...],
        fallback_refs: list[str],
        max_refs: int,
    ) -> list[str]:
        refs: list[str] = []
        seen: set[str] = set()
        for fact in memory_facts:
            if fact.memory_type not in kinds:
                continue
            for ref in fact.evidence_refs:
                if ref in seen:
                    continue
                seen.add(ref)
                refs.append(ref)
                if len(refs) >= max_refs:
                    return refs
        for ref in fallback_refs:
            if ref in seen:
                continue
            seen.add(ref)
            refs.append(ref)
            if len(refs) >= max_refs:
                break
        return refs

    @staticmethod
    def _average(values: Iterable[float]) -> float:
        value_list = [float(value) for value in values]
        if not value_list:
            return 0.0
        return sum(value_list) / len(value_list)

    @staticmethod
    def _clamp(value: float) -> float:
        return max(0.0, min(float(value), 1.0))

    @staticmethod
    def _max_sensitivity(values: list[str], *, default: str) -> str:
        rank = {"low": 0, "medium": 1, "high": 2}
        filtered = [value for value in values if value in rank]
        if not filtered:
            return default
        return max(filtered, key=lambda value: rank[value])

    @staticmethod
    def _unique(values: Iterable[str]) -> list[str]:
        seen: set[str] = set()
        ordered: list[str] = []
        for value in values:
            if not isinstance(value, str) or not value:
                continue
            if value in seen:
                continue
            seen.add(value)
            ordered.append(value)
        return ordered

    @staticmethod
    def _summary_evidence_refs(chunk_summaries: list[ChunkSummary]) -> list[str]:
        refs: list[str] = []
        for summary in chunk_summaries:
            refs.extend(summary.evidence_refs)
        return ContactSkillBuilderService._unique(refs)

    @staticmethod
    def _joined_text(
        *,
        chunk_summaries: list[ChunkSummary],
        memory_facts: list[MemoryFactCandidate],
    ) -> str:
        values = [summary.summary for summary in chunk_summaries] + [fact.claim for fact in memory_facts]
        return " ".join(values).casefold()

    @staticmethod
    def _contains_any(text: str, tokens: Iterable[str]) -> bool:
        lowered = text.casefold()
        return any(token.casefold() in lowered for token in tokens)

    @staticmethod
    def _dedupe_topic_preferences(
        values: list[ContactSkillTopicPreference],
    ) -> list[ContactSkillTopicPreference]:
        kept: dict[str, ContactSkillTopicPreference] = {}
        for item in values:
            key = item.topic.casefold()
            existing = kept.get(key)
            if existing is None or item.confidence > existing.confidence:
                kept[key] = item
        ordered = list(kept.values())
        ordered.sort(key=lambda item: item.confidence, reverse=True)
        return ordered


class ContactSkillFileStoreService:
    """Load and save offline memory/contact-skill stores under private/distilled."""

    MEMORY_STORE_FILENAME = "memory_fact_store.json"
    CONTACT_SKILL_STORE_FILENAME = "contact_skill_store.json"
    MEMORY_FACTS_FILENAME = "memory_facts.jsonl"
    CONTACT_SKILL_CANDIDATE_FILENAME = "contact_skill.candidate.json"
    CONTACT_SKILL_REVIEW_FILENAME = "contact_skill.review.md"

    def __init__(self) -> None:
        self._repo_root = Path.cwd().resolve()
        self._private_distilled_root = (self._repo_root / "private" / "distilled").resolve()

    def load_memory_store(self, *, input_path: Path) -> MemoryFactStoreFile:
        resolved_input = self._resolve_existing_path(input_path)
        self._ensure_within_root(
            candidate=resolved_input,
            root=self._private_distilled_root,
            error_message="Input must stay within private/distilled.",
        )
        if resolved_input.is_dir():
            store_path = resolved_input / self.MEMORY_STORE_FILENAME
            if store_path.is_file():
                return self._load_memory_store_file(store_path=store_path)
            facts_path = resolved_input / self.MEMORY_FACTS_FILENAME
            if facts_path.is_file():
                return self._wrap_memory_facts_jsonl(facts_path=facts_path)
            raise ContactSkillBuilderError(
                "Input directory must contain memory_fact_store.json or memory_facts.jsonl.",
            )
        if resolved_input.name == self.MEMORY_FACTS_FILENAME:
            return self._wrap_memory_facts_jsonl(facts_path=resolved_input)
        return self._load_memory_store_file(store_path=resolved_input)

    def save_memory_store(
        self,
        *,
        output_path: Path,
        store: MemoryFactStoreFile,
    ) -> FileStoreSaveResult:
        resolved_output = self._resolve_store_output_path(
            output_path=output_path,
            default_filename=self.MEMORY_STORE_FILENAME,
        )
        normalized_store = MemoryFactStoreFile(
            generated_at=store.generated_at,
            records=[
                record.model_copy(update={"updated_at": record.updated_at})
                for record in store.records
            ],
        )
        resolved_output.parent.mkdir(parents=True, exist_ok=True)
        self._write_json(output_path=resolved_output, payload=normalized_store.model_dump(mode="json"))
        return FileStoreSaveResult(
            output_path=resolved_output,
            record_count=len(normalized_store.records),
            statuses=[record.memory_fact.status for record in normalized_store.records],
        )

    def load_contact_skill_store(self, *, input_path: Path) -> ContactSkillStoreFile:
        resolved_input = self._resolve_existing_path(input_path)
        self._ensure_within_root(
            candidate=resolved_input,
            root=self._private_distilled_root,
            error_message="Input must stay within private/distilled.",
        )
        if resolved_input.is_dir():
            store_path = resolved_input / self.CONTACT_SKILL_STORE_FILENAME
            if store_path.is_file():
                return self._load_contact_skill_store_file(store_path=store_path)
            candidate_path = resolved_input / self.CONTACT_SKILL_CANDIDATE_FILENAME
            if candidate_path.is_file():
                return self._wrap_contact_skill_candidate(
                    candidate_path=candidate_path,
                    review_artifact_path=resolved_input / self.CONTACT_SKILL_REVIEW_FILENAME,
                )
            raise ContactSkillBuilderError(
                "Input directory must contain contact_skill_store.json or contact_skill.candidate.json.",
            )
        if resolved_input.name == self.CONTACT_SKILL_CANDIDATE_FILENAME:
            return self._wrap_contact_skill_candidate(
                candidate_path=resolved_input,
                review_artifact_path=resolved_input.parent / self.CONTACT_SKILL_REVIEW_FILENAME,
            )
        return self._load_contact_skill_store_file(store_path=resolved_input)

    def save_contact_skill_store(
        self,
        *,
        output_path: Path,
        store: ContactSkillStoreFile,
    ) -> FileStoreSaveResult:
        resolved_output = self._resolve_store_output_path(
            output_path=output_path,
            default_filename=self.CONTACT_SKILL_STORE_FILENAME,
        )
        normalized_store = ContactSkillStoreFile(
            generated_at=store.generated_at,
            records=[
                record.model_copy(update={"updated_at": record.updated_at})
                for record in store.records
            ],
        )
        resolved_output.parent.mkdir(parents=True, exist_ok=True)
        self._write_json(output_path=resolved_output, payload=normalized_store.model_dump(mode="json"))
        return FileStoreSaveResult(
            output_path=resolved_output,
            record_count=len(normalized_store.records),
            statuses=[record.contact_skill.status for record in normalized_store.records],
        )

    def _load_memory_store_file(self, *, store_path: Path) -> MemoryFactStoreFile:
        payload = self._read_json_object(store_path)
        if "records" in payload:
            return MemoryFactStoreFile.model_validate(payload)
        if "memory_fact" in payload:
            return MemoryFactStoreFile(records=[MemoryFactStoreRecord.model_validate(payload)])
        raise ContactSkillBuilderError("Unsupported memory store file shape.")

    def _load_contact_skill_store_file(self, *, store_path: Path) -> ContactSkillStoreFile:
        payload = self._read_json_object(store_path)
        if "records" in payload:
            return ContactSkillStoreFile.model_validate(payload)
        if "contact_skill" in payload:
            return ContactSkillStoreFile(records=[ContactSkillStoreRecord.model_validate(payload)])
        raise ContactSkillBuilderError("Unsupported contact skill store file shape.")

    def _wrap_memory_facts_jsonl(self, *, facts_path: Path) -> MemoryFactStoreFile:
        source_run_id = self._infer_run_id(path=facts_path)
        records: list[MemoryFactStoreRecord] = []
        for fact in self._load_memory_facts_jsonl(facts_path=facts_path):
            records.append(
                MemoryFactStoreRecord(
                    record_id=self._stable_store_record_id(
                        prefix="memstore",
                        seed=f"memory_fact:{source_run_id or 'unknown'}:{fact.memory_id}",
                    ),
                    memory_fact=fact,
                    source_metadata=DistilledArtifactSourceMetadata(
                        source_run_id=source_run_id,
                        source_artifact_path=self._safe_relative_path(facts_path),
                        source_chunk_ids=list(fact.source_chunk_ids),
                        source_event_ids=self._extract_event_ids(fact.evidence_refs),
                    ),
                    review_metadata=self._default_review_metadata(status=fact.status),
                ),
            )
        return MemoryFactStoreFile(records=records)

    def _wrap_contact_skill_candidate(
        self,
        *,
        candidate_path: Path,
        review_artifact_path: Path | None,
    ) -> ContactSkillStoreFile:
        candidate = self._load_contact_skill_candidate(candidate_path=candidate_path)
        source_run_id = self._infer_run_id(path=candidate_path)
        review_path = review_artifact_path if review_artifact_path and review_artifact_path.is_file() else None
        record = ContactSkillStoreRecord(
            record_id=self._stable_store_record_id(
                prefix="skillstore",
                seed=f"contact_skill:{source_run_id or 'unknown'}:{candidate.contact_id}",
            ),
            contact_skill=candidate,
            source_metadata=DistilledArtifactSourceMetadata(
                source_run_id=source_run_id,
                source_artifact_path=self._safe_relative_path(candidate_path),
                review_artifact_path=self._safe_relative_path(review_path),
                source_chunk_ids=list(candidate.source_chunk_ids),
                source_memory_ids=list(candidate.source_memory_ids),
                source_event_ids=self._extract_event_ids(candidate.evidence_refs),
            ),
            review_metadata=self._default_review_metadata(status=candidate.status),
        )
        return ContactSkillStoreFile(records=[record])

    def _load_memory_facts_jsonl(self, *, facts_path: Path) -> list[MemoryFactCandidate]:
        facts: list[MemoryFactCandidate] = []
        with facts_path.open("r", encoding="utf-8") as handle:
            for line_no, raw_line in enumerate(handle, start=1):
                line = raw_line.strip()
                if not line:
                    continue
                try:
                    payload = json.loads(line)
                except json.JSONDecodeError as exc:
                    raise ContactSkillBuilderError(
                        f"memory_facts.jsonl line {line_no} is invalid JSON.",
                    ) from exc
                facts.append(MemoryFactCandidate.model_validate(payload))
        return facts

    def _load_contact_skill_candidate(self, *, candidate_path: Path) -> ContactSkillCandidate:
        payload = self._read_json_object(candidate_path)
        return ContactSkillCandidate.model_validate(payload)

    def _read_json_object(self, path: Path) -> dict[str, Any]:
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ContactSkillBuilderError(f"{path.name} is invalid JSON.") from exc
        if not isinstance(payload, dict):
            raise ContactSkillBuilderError(f"{path.name} must contain a JSON object.")
        return payload

    def _write_json(self, *, output_path: Path, payload: dict[str, Any]) -> None:
        output_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    def _resolve_existing_path(self, path: Path) -> Path:
        resolved = (self._repo_root / path).resolve() if not path.is_absolute() else path.resolve()
        if not resolved.exists():
            raise ContactSkillBuilderError(f"Input path does not exist: {path}")
        return resolved

    def _resolve_store_output_path(self, *, output_path: Path, default_filename: str) -> Path:
        resolved = (self._repo_root / output_path).resolve() if not output_path.is_absolute() else output_path.resolve()
        if resolved.suffix.casefold() != ".json":
            resolved = resolved / default_filename
        self._ensure_within_root(
            candidate=resolved,
            root=self._private_distilled_root,
            error_message="Output must stay within private/distilled.",
        )
        return resolved

    @staticmethod
    def _ensure_within_root(*, candidate: Path, root: Path, error_message: str) -> None:
        try:
            candidate.relative_to(root)
        except ValueError as exc:
            raise ContactSkillBuilderError(error_message) from exc

    def _safe_relative_path(self, path: Path | None) -> str | None:
        if path is None:
            return None
        try:
            return str(path.relative_to(self._repo_root)).replace("\\", "/")
        except ValueError:
            return str(path).replace("\\", "/")

    def _infer_run_id(self, *, path: Path) -> str | None:
        relative = self._safe_relative_path(path)
        if relative is None:
            return None
        parts = relative.split("/")
        if len(parts) >= 3 and parts[0] == "private" and parts[1] == "distilled":
            return parts[2]
        return None

    @staticmethod
    def _extract_event_ids(refs: Iterable[str]) -> list[str]:
        event_ids: list[str] = []
        seen: set[str] = set()
        for ref in refs:
            if not isinstance(ref, str) or not ref.startswith("evt_"):
                continue
            if ref in seen:
                continue
            seen.add(ref)
            event_ids.append(ref)
        return event_ids

    @staticmethod
    def _stable_store_record_id(*, prefix: str, seed: str) -> str:
        digest = hashlib.sha1(seed.encode("utf-8")).hexdigest()[:16]
        return f"{prefix}_{digest}"

    @staticmethod
    def _default_review_metadata(*, status: DistillationStatus) -> DistilledArtifactReviewMetadata:
        if status == "candidate":
            return DistilledArtifactReviewMetadata()
        return DistilledArtifactReviewMetadata(
            review_state="unknown",
            decision_notes=[
                "Loaded legacy artifact without explicit review metadata; human approval must be re-established.",
            ],
        )


class ContactSkillStoreReviewError(ValueError):
    """Raised when a store review request cannot be completed safely."""


class ContactSkillStoreReviewService:
    """List, review, and export private distilled store records."""

    VALIDATION_REPORT_FILENAME = "evidence_validation_report.json"
    DEFAULT_EXPORT_FILENAME = "store_review_export.md"
    REVIEW_ACTIONS = {
        "approve": "approved",
        "reject": "rejected",
        "freeze": "frozen",
        "archive": "archived",
    }

    def __init__(self) -> None:
        self._store_service = ContactSkillFileStoreService()
        self._repo_root = self._store_service._repo_root
        self._private_distilled_root = self._store_service._private_distilled_root

    def list_store_records(
        self,
        *,
        input_path: Path,
        validation_report_path: Path | None = None,
    ) -> StoreReviewListResult:
        workspace = self._load_workspace(input_path=input_path)
        validation_context = self._load_validation_report(
            workspace=workspace,
            validation_report_path=validation_report_path,
            required=False,
        )
        records = [self._build_record_summary(handle=handle, validation_context=validation_context) for handle in self._iter_record_handles(workspace)]
        return StoreReviewListResult(
            input_path=workspace.input_path,
            run_dir=workspace.run_dir,
            validation_report_path=validation_context.report_path,
            validation_report_found=validation_context.report is not None,
            records=records,
        )

    def apply_record_decision(
        self,
        *,
        input_path: Path,
        record_id: str,
        decision: str,
        reviewer_id: str | None,
        reviewer_name: str | None,
        notes: list[str] | None,
        validation_report_path: Path | None = None,
        output_path: Path | None = None,
    ) -> StoreReviewDecisionResult:
        if not reviewer_id and not reviewer_name:
            raise ContactSkillStoreReviewError("A human reviewer id or name is required for review decisions.")
        normalized_decision = self._normalize_decision(decision)
        workspace = self._load_workspace(input_path=input_path)
        validation_context = self._load_validation_report(
            workspace=workspace,
            validation_report_path=validation_report_path,
            required=normalized_decision == "approved",
        )
        record_handle = self._find_record_handle(workspace=workspace, record_id=record_id)
        validation_record = validation_context.records_by_id.get(record_id)
        if normalized_decision == "approved":
            self._assert_approval_allowed(
                record_handle=record_handle,
                validation_context=validation_context,
                validation_record=validation_record,
            )

        cleaned_notes = self._clean_notes(notes)
        evidence_validation_status = self._resolve_evidence_validation_status(
            current_status=self._record_status(record_handle.record),
            review_metadata_status=self._record_review_metadata(record_handle.record).evidence_validation_status,
            validation_context=validation_context,
            validation_record=validation_record,
        )
        reviewed_at = utc_now()
        updated_record = self._apply_decision_to_record(
            record=record_handle.record,
            decision=normalized_decision,
            reviewer_id=reviewer_id,
            reviewer_name=reviewer_name,
            reviewed_at=reviewed_at,
            notes=cleaned_notes,
            evidence_validation_status=evidence_validation_status,
        )
        self._write_back_record(
            workspace=workspace,
            record_handle=record_handle,
            updated_record=updated_record,
        )
        saved_output_path = self._save_workspace_record(
            workspace=workspace,
            record_handle=record_handle,
            output_path=output_path,
        )
        updated_handle = self._find_record_handle(workspace=workspace, record_id=record_id)
        summary = self._build_record_summary(handle=updated_handle, validation_context=validation_context)
        return StoreReviewDecisionResult(
            decision=normalized_decision,
            input_path=workspace.input_path,
            run_dir=workspace.run_dir,
            validation_report_path=validation_context.report_path,
            saved_output_path=saved_output_path,
            record=summary,
        )

    def export_review_artifact(
        self,
        *,
        input_path: Path,
        output_path: Path | None = None,
        record_id: str | None = None,
        validation_report_path: Path | None = None,
    ) -> StoreReviewExportResult:
        list_result = self.list_store_records(
            input_path=input_path,
            validation_report_path=validation_report_path,
        )
        selected_records = list_result.records
        if record_id is not None:
            selected_records = [record for record in selected_records if record.record_id == record_id]
            if not selected_records:
                raise ContactSkillStoreReviewError(f"Record not found: {record_id}")
        resolved_output = self._resolve_markdown_output_path(
            output_path=output_path,
            run_dir=list_result.run_dir,
            record_id=record_id,
        )
        from practical_chat_agent.exporters.contact_skill_markdown import (  # noqa: PLC0415
            render_store_review_markdown,
        )

        markdown = render_store_review_markdown(
            input_path=self._store_service._safe_relative_path(list_result.input_path) or str(list_result.input_path),
            run_dir=self._store_service._safe_relative_path(list_result.run_dir) or str(list_result.run_dir),
            validation_report_path=self._store_service._safe_relative_path(list_result.validation_report_path),
            validation_report_found=list_result.validation_report_found,
            records=[self._record_summary_to_dict(record) for record in selected_records],
        )
        resolved_output.parent.mkdir(parents=True, exist_ok=True)
        resolved_output.write_text(markdown, encoding="utf-8")
        return StoreReviewExportResult(
            input_path=list_result.input_path,
            run_dir=list_result.run_dir,
            validation_report_path=list_result.validation_report_path,
            output_path=resolved_output,
            record_count=len(selected_records),
            record_ids=[record.record_id for record in selected_records],
        )

    def _load_workspace(self, *, input_path: Path) -> _StoreWorkspace:
        resolved_input = self._store_service._resolve_existing_path(input_path)
        self._store_service._ensure_within_root(
            candidate=resolved_input,
            root=self._private_distilled_root,
            error_message="Input must stay within private/distilled.",
        )
        workspace = _StoreWorkspace(
            input_path=resolved_input,
            run_dir=self._resolve_run_dir(path=resolved_input),
        )
        if resolved_input.is_dir():
            memory_input_path = self._detect_memory_input_path(resolved_input)
            contact_skill_input_path = self._detect_contact_skill_input_path(resolved_input)
            if memory_input_path is not None:
                workspace.memory_input_path = memory_input_path
                workspace.memory_output_path = resolved_input / self._store_service.MEMORY_STORE_FILENAME
                workspace.memory_store = self._store_service.load_memory_store(input_path=memory_input_path)
            if contact_skill_input_path is not None:
                workspace.contact_skill_input_path = contact_skill_input_path
                workspace.contact_skill_output_path = resolved_input / self._store_service.CONTACT_SKILL_STORE_FILENAME
                workspace.contact_skill_store = self._store_service.load_contact_skill_store(
                    input_path=contact_skill_input_path,
                )
        elif resolved_input.name in {
            self._store_service.MEMORY_STORE_FILENAME,
            self._store_service.MEMORY_FACTS_FILENAME,
        }:
            workspace.memory_input_path = resolved_input
            workspace.memory_output_path = (
                resolved_input
                if resolved_input.name == self._store_service.MEMORY_STORE_FILENAME
                else resolved_input.parent / self._store_service.MEMORY_STORE_FILENAME
            )
            workspace.memory_store = self._store_service.load_memory_store(input_path=resolved_input)
        elif resolved_input.name in {
            self._store_service.CONTACT_SKILL_STORE_FILENAME,
            self._store_service.CONTACT_SKILL_CANDIDATE_FILENAME,
        }:
            workspace.contact_skill_input_path = resolved_input
            workspace.contact_skill_output_path = (
                resolved_input
                if resolved_input.name == self._store_service.CONTACT_SKILL_STORE_FILENAME
                else resolved_input.parent / self._store_service.CONTACT_SKILL_STORE_FILENAME
            )
            workspace.contact_skill_store = self._store_service.load_contact_skill_store(input_path=resolved_input)
        else:
            raise ContactSkillStoreReviewError(
                "Input must be a private/distilled run directory or a memory/contact-skill store artifact path.",
            )

        if workspace.memory_store is None and workspace.contact_skill_store is None:
            raise ContactSkillStoreReviewError(
                "No memory or contact-skill store artifacts were found under the requested path.",
            )
        return workspace

    def _load_validation_report(
        self,
        *,
        workspace: _StoreWorkspace,
        validation_report_path: Path | None,
        required: bool,
    ) -> _ValidationReportContext:
        resolved_report_path: Path | None = None
        if validation_report_path is not None:
            resolved_report_path = self._store_service._resolve_existing_path(validation_report_path)
            self._store_service._ensure_within_root(
                candidate=resolved_report_path,
                root=self._private_distilled_root,
                error_message="Validation report must stay within private/distilled.",
            )
        else:
            candidate = workspace.run_dir / self.VALIDATION_REPORT_FILENAME
            if candidate.is_file():
                resolved_report_path = candidate

        if resolved_report_path is None:
            if required:
                raise ContactSkillStoreReviewError(
                    "Approve requires an evidence_validation_report.json under the same private/distilled run directory "
                    "or an explicit --validation-report path.",
                )
            return _ValidationReportContext(
                report=None,
                report_path=None,
                summary_status="not_run",
                records_by_id={},
            )

        report = self._store_service._read_json_object(resolved_report_path)
        expected_run_dir = self._store_service._safe_relative_path(workspace.run_dir)
        report_run_dir = report.get("run_dir")
        if expected_run_dir is not None and report_run_dir not in {None, expected_run_dir}:
            raise ContactSkillStoreReviewError(
                "Validation report does not match the requested private/distilled run directory.",
            )
        summary = report.get("summary")
        records = report.get("records")
        if not isinstance(summary, dict) or not isinstance(records, list):
            raise ContactSkillStoreReviewError("Validation report is missing summary or records.")
        records_by_id = {
            item["record_id"]: item
            for item in records
            if isinstance(item, dict) and isinstance(item.get("record_id"), str)
        }
        summary_status = summary.get("evidence_validation_status", "not_run")
        if not isinstance(summary_status, str):
            summary_status = "not_run"
        return _ValidationReportContext(
            report=report,
            report_path=resolved_report_path,
            summary_status=summary_status,
            records_by_id=records_by_id,
        )

    def _iter_record_handles(self, workspace: _StoreWorkspace) -> Iterable[_StoreRecordHandle]:
        if workspace.memory_store is not None and workspace.memory_input_path is not None and workspace.memory_output_path is not None:
            for index, record in enumerate(workspace.memory_store.records):
                yield _StoreRecordHandle(
                    store_kind="memory",
                    index=index,
                    input_path=workspace.memory_input_path,
                    output_path=workspace.memory_output_path,
                    record=record,
                )
        if (
            workspace.contact_skill_store is not None
            and workspace.contact_skill_input_path is not None
            and workspace.contact_skill_output_path is not None
        ):
            for index, record in enumerate(workspace.contact_skill_store.records):
                yield _StoreRecordHandle(
                    store_kind="contact_skill",
                    index=index,
                    input_path=workspace.contact_skill_input_path,
                    output_path=workspace.contact_skill_output_path,
                    record=record,
                )

    def _find_record_handle(self, *, workspace: _StoreWorkspace, record_id: str) -> _StoreRecordHandle:
        for handle in self._iter_record_handles(workspace):
            if handle.record.record_id == record_id:
                return handle
        raise ContactSkillStoreReviewError(f"Record not found: {record_id}")

    def _build_record_summary(
        self,
        *,
        handle: _StoreRecordHandle,
        validation_context: _ValidationReportContext,
    ) -> StoreRecordSummary:
        validation_record = validation_context.records_by_id.get(handle.record.record_id)
        gate_summary = self._build_gate_summary(
            record=handle.record,
            validation_context=validation_context,
            validation_record=validation_record,
        )
        review_metadata = self._record_review_metadata(handle.record)
        return StoreRecordSummary(
            record_id=handle.record.record_id,
            artifact_type=self._record_artifact_type(handle.record),
            artifact_id=self._record_artifact_id(handle.record),
            status=self._record_status(handle.record),
            review_state=review_metadata.review_state,
            reviewed_by_human=review_metadata.reviewed_by_human,
            last_decision=review_metadata.last_decision,
            evidence_validation_status=self._resolve_evidence_validation_status(
                current_status=self._record_status(handle.record),
                review_metadata_status=review_metadata.evidence_validation_status,
                validation_context=validation_context,
                validation_record=validation_record,
            ),
            approval_ready_after_validation=gate_summary["approval_ready_after_validation"],
            runtime_ready_after_validation=gate_summary["runtime_ready_after_validation"],
            missing_ref_count=gate_summary["missing_ref_count"],
            safe_path=self._store_service._safe_relative_path(handle.input_path) or str(handle.input_path),
            review_artifact_path=handle.record.source_metadata.review_artifact_path,
            approval_block_reasons=gate_summary["approval_block_reasons"],
            runtime_block_reasons=gate_summary["runtime_block_reasons"],
        )

    def _build_gate_summary(
        self,
        *,
        record: MemoryFactStoreRecord | ContactSkillStoreRecord,
        validation_context: _ValidationReportContext,
        validation_record: dict[str, Any] | None,
    ) -> dict[str, Any]:
        if validation_context.report is None:
            return {
                "approval_ready_after_validation": None,
                "runtime_ready_after_validation": None,
                "missing_ref_count": None,
                "approval_block_reasons": [],
                "runtime_block_reasons": [],
            }
        if validation_record is None:
            return {
                "approval_ready_after_validation": None,
                "runtime_ready_after_validation": None,
                "missing_ref_count": None,
                "approval_block_reasons": ["record_not_present_in_validation_report"],
                "runtime_block_reasons": ["record_not_present_in_validation_report"],
            }

        status = self._record_status(record)
        store_runtime_ready = record.is_runtime_ready()
        checked_ref_count = int(validation_record.get("checked_ref_count", 0))
        missing_refs = validation_record.get("missing_refs", [])
        missing_ref_count = int(validation_record.get("missing_ref_count", len(missing_refs)))

        approval_block_reasons: list[str] = []
        runtime_block_reasons: list[str] = []
        if validation_context.summary_status != "passed":
            approval_block_reasons.append("validation_report_not_passed")
            runtime_block_reasons.append("validation_report_not_passed")
        if checked_ref_count == 0:
            approval_block_reasons.append("no_evidence_refs_found")
            runtime_block_reasons.append("no_evidence_refs_found")
        if missing_ref_count > 0:
            approval_block_reasons.append("missing_evidence_refs")
            runtime_block_reasons.append("missing_evidence_refs")
        if status == "candidate":
            approval_block_reasons.append("candidate_not_approval_ready_by_default")
            runtime_block_reasons.append("candidate_not_runtime_ready")
        elif status in {"rejected", "frozen", "archived"}:
            approval_block_reasons.append(f"status_{status}_not_approval_ready")
            runtime_block_reasons.append(f"status_{status}_never_runtime_ready")
        elif status == "approved" and not store_runtime_ready:
            runtime_block_reasons.append("human_review_runtime_gate_not_satisfied")

        approval_block_reasons = self._unique_strings(approval_block_reasons)
        runtime_block_reasons = self._unique_strings(runtime_block_reasons)
        approval_ready = status == "approved" and not approval_block_reasons
        runtime_ready = status == "approved" and not runtime_block_reasons
        return {
            "approval_ready_after_validation": approval_ready,
            "runtime_ready_after_validation": runtime_ready,
            "missing_ref_count": missing_ref_count,
            "approval_block_reasons": approval_block_reasons,
            "runtime_block_reasons": runtime_block_reasons,
        }

    def _assert_approval_allowed(
        self,
        *,
        record_handle: _StoreRecordHandle,
        validation_context: _ValidationReportContext,
        validation_record: dict[str, Any] | None,
    ) -> None:
        current_status = self._record_status(record_handle.record)
        if current_status in {"rejected", "frozen", "archived"}:
            raise ContactSkillStoreReviewError(
                f"Approve is blocked for records with status={current_status}. Reopen is not implemented in T122.",
            )
        if validation_context.report is None or validation_context.report_path is None:
            raise ContactSkillStoreReviewError("Approve requires a validation report.")
        if validation_record is None:
            raise ContactSkillStoreReviewError(
                "Approve requires the target record to appear in the validation report for the same run directory.",
            )
        missing_ref_count = int(validation_record.get("missing_ref_count", 0))
        if missing_ref_count > 0:
            raise ContactSkillStoreReviewError(
                "Approve is blocked because the target record still has missing evidence refs in the validation report.",
            )
        checked_ref_count = int(validation_record.get("checked_ref_count", 0))
        if checked_ref_count == 0:
            raise ContactSkillStoreReviewError(
                "Approve is blocked because the target record has no validated evidence refs.",
            )
        if validation_context.summary_status != "passed":
            raise ContactSkillStoreReviewError(
                f"Approve requires a passed validation report, got status={validation_context.summary_status}.",
            )

    def _apply_decision_to_record(
        self,
        *,
        record: MemoryFactStoreRecord | ContactSkillStoreRecord,
        decision: DistillationStatus,
        reviewer_id: str | None,
        reviewer_name: str | None,
        reviewed_at: Any,
        notes: list[str],
        evidence_validation_status: str,
    ) -> MemoryFactStoreRecord | ContactSkillStoreRecord:
        updated_metadata = self._update_review_metadata(
            review_metadata=record.review_metadata,
            decision=decision,
            reviewer_id=reviewer_id,
            reviewer_name=reviewer_name,
            reviewed_at=reviewed_at,
            notes=notes,
            evidence_validation_status=evidence_validation_status,
        )
        if isinstance(record, MemoryFactStoreRecord):
            updated_payload = self._update_candidate_status(record.memory_fact.model_dump(mode="json"), status=decision)
            return record.model_copy(
                update={
                    "memory_fact": MemoryFactCandidate.model_validate(updated_payload),
                    "review_metadata": updated_metadata,
                    "updated_at": reviewed_at,
                },
            )
        updated_payload = self._update_candidate_status(record.contact_skill.model_dump(mode="json"), status=decision)
        return record.model_copy(
            update={
                "contact_skill": ContactSkillCandidate.model_validate(updated_payload),
                "review_metadata": updated_metadata,
                "updated_at": reviewed_at,
            },
        )

    def _update_review_metadata(
        self,
        *,
        review_metadata: DistilledArtifactReviewMetadata,
        decision: DistillationStatus,
        reviewer_id: str | None,
        reviewer_name: str | None,
        reviewed_at: Any,
        notes: list[str],
        evidence_validation_status: str,
    ) -> DistilledArtifactReviewMetadata:
        cleaned_notes = notes or [f"Human decision recorded: {decision}."]
        decision_record = DistilledArtifactReviewDecision(
            status=decision,
            reviewer_id=reviewer_id,
            reviewer_name=reviewer_name,
            reviewed_at=reviewed_at,
            notes=cleaned_notes,
            evidence_validation_status=evidence_validation_status,
        )
        return review_metadata.model_copy(
            update={
                "review_state": "reviewed",
                "reviewed_by_human": True,
                "last_decision": decision,
                "last_reviewed_at": reviewed_at,
                "last_reviewer_id": reviewer_id,
                "last_reviewer_name": reviewer_name,
                "evidence_validation_status": evidence_validation_status,
                "decision_notes": list(review_metadata.decision_notes) + cleaned_notes,
                "history": list(review_metadata.history) + [decision_record],
            },
        )

    def _write_back_record(
        self,
        *,
        workspace: _StoreWorkspace,
        record_handle: _StoreRecordHandle,
        updated_record: MemoryFactStoreRecord | ContactSkillStoreRecord,
    ) -> None:
        if record_handle.store_kind == "memory":
            if workspace.memory_store is None:
                raise ContactSkillStoreReviewError("Memory store is not loaded.")
            records = list(workspace.memory_store.records)
            records[record_handle.index] = updated_record
            workspace.memory_store = workspace.memory_store.model_copy(update={"records": records})
            return
        if workspace.contact_skill_store is None:
            raise ContactSkillStoreReviewError("Contact-skill store is not loaded.")
        records = list(workspace.contact_skill_store.records)
        records[record_handle.index] = updated_record
        workspace.contact_skill_store = workspace.contact_skill_store.model_copy(update={"records": records})

    def _save_workspace_record(
        self,
        *,
        workspace: _StoreWorkspace,
        record_handle: _StoreRecordHandle,
        output_path: Path | None,
    ) -> Path:
        if record_handle.store_kind == "memory":
            if workspace.memory_store is None or workspace.memory_output_path is None:
                raise ContactSkillStoreReviewError("Memory store is not available for saving.")
            target_path = output_path or workspace.memory_output_path
            return self._store_service.save_memory_store(
                output_path=target_path,
                store=workspace.memory_store,
            ).output_path
        if workspace.contact_skill_store is None or workspace.contact_skill_output_path is None:
            raise ContactSkillStoreReviewError("Contact-skill store is not available for saving.")
        target_path = output_path or workspace.contact_skill_output_path
        return self._store_service.save_contact_skill_store(
            output_path=target_path,
            store=workspace.contact_skill_store,
        ).output_path

    def _resolve_markdown_output_path(
        self,
        *,
        output_path: Path | None,
        run_dir: Path,
        record_id: str | None,
    ) -> Path:
        default_filename = (
            f"store_review_{record_id}.md"
            if record_id is not None
            else self.DEFAULT_EXPORT_FILENAME
        )
        base_path = output_path or (run_dir / default_filename)
        resolved = (self._repo_root / base_path).resolve() if not base_path.is_absolute() else base_path.resolve()
        if resolved.suffix.casefold() != ".md":
            resolved = resolved / default_filename
        self._store_service._ensure_within_root(
            candidate=resolved,
            root=self._private_distilled_root,
            error_message="Export output must stay within private/distilled.",
        )
        return resolved

    def _resolve_run_dir(self, *, path: Path) -> Path:
        try:
            relative = path.relative_to(self._private_distilled_root)
        except ValueError as exc:
            raise ContactSkillStoreReviewError("Input must stay within private/distilled.") from exc
        if not relative.parts:
            return self._private_distilled_root
        return self._private_distilled_root / relative.parts[0]

    def _detect_memory_input_path(self, directory: Path) -> Path | None:
        store_path = directory / self._store_service.MEMORY_STORE_FILENAME
        if store_path.is_file():
            return store_path
        legacy_path = directory / self._store_service.MEMORY_FACTS_FILENAME
        if legacy_path.is_file():
            return legacy_path
        return None

    def _detect_contact_skill_input_path(self, directory: Path) -> Path | None:
        store_path = directory / self._store_service.CONTACT_SKILL_STORE_FILENAME
        if store_path.is_file():
            return store_path
        legacy_path = directory / self._store_service.CONTACT_SKILL_CANDIDATE_FILENAME
        if legacy_path.is_file():
            return legacy_path
        return None

    def _normalize_decision(self, decision: str) -> DistillationStatus:
        normalized = decision.strip().lower()
        resolved = self.REVIEW_ACTIONS.get(normalized)
        if resolved is None:
            raise ContactSkillStoreReviewError(
                "Decision must be one of approve, reject, freeze, or archive.",
            )
        return resolved

    @staticmethod
    def _clean_notes(notes: list[str] | None) -> list[str]:
        if not notes:
            return []
        cleaned: list[str] = []
        for note in notes:
            stripped = " ".join(note.split()).strip()
            if stripped:
                cleaned.append(stripped)
        return cleaned

    @staticmethod
    def _record_artifact_type(record: MemoryFactStoreRecord | ContactSkillStoreRecord) -> str:
        return record.artifact_type

    @staticmethod
    def _record_artifact_id(record: MemoryFactStoreRecord | ContactSkillStoreRecord) -> str:
        if isinstance(record, MemoryFactStoreRecord):
            return record.memory_fact.memory_id
        return record.contact_skill.contact_id

    @staticmethod
    def _record_status(record: MemoryFactStoreRecord | ContactSkillStoreRecord) -> DistillationStatus:
        if isinstance(record, MemoryFactStoreRecord):
            return record.memory_fact.status
        return record.contact_skill.status

    @staticmethod
    def _record_review_metadata(record: MemoryFactStoreRecord | ContactSkillStoreRecord) -> DistilledArtifactReviewMetadata:
        return record.review_metadata

    @staticmethod
    def _resolve_evidence_validation_status(
        *,
        current_status: DistillationStatus,
        review_metadata_status: str,
        validation_context: _ValidationReportContext,
        validation_record: dict[str, Any] | None,
    ) -> str:
        del current_status
        if validation_context.report is None:
            return review_metadata_status or "not_run"
        if validation_record is None:
            return "partial"
        missing_ref_count = int(validation_record.get("missing_ref_count", 0))
        checked_ref_count = int(validation_record.get("checked_ref_count", 0))
        if checked_ref_count == 0 or missing_ref_count > 0:
            return "failed"
        if validation_context.summary_status == "passed":
            return "passed"
        if validation_context.summary_status == "failed":
            return "partial"
        return validation_context.summary_status or "not_run"

    @classmethod
    def _update_candidate_status(cls, value: Any, *, status: DistillationStatus) -> Any:
        if isinstance(value, dict):
            updated: dict[str, Any] = {}
            for key, item in value.items():
                if key == "status" and isinstance(item, str) and item in {
                    "candidate",
                    "approved",
                    "rejected",
                    "frozen",
                    "archived",
                }:
                    updated[key] = status
                else:
                    updated[key] = cls._update_candidate_status(item, status=status)
            return updated
        if isinstance(value, list):
            return [cls._update_candidate_status(item, status=status) for item in value]
        return value

    @staticmethod
    def _unique_strings(values: Iterable[str]) -> list[str]:
        seen: set[str] = set()
        ordered: list[str] = []
        for value in values:
            if not isinstance(value, str) or not value:
                continue
            if value in seen:
                continue
            seen.add(value)
            ordered.append(value)
        return ordered

    @staticmethod
    def _record_summary_to_dict(record: StoreRecordSummary) -> dict[str, Any]:
        return {
            "record_id": record.record_id,
            "artifact_type": record.artifact_type,
            "artifact_id": record.artifact_id,
            "status": record.status,
            "review_state": record.review_state,
            "reviewed_by_human": record.reviewed_by_human,
            "last_decision": record.last_decision,
            "evidence_validation_status": record.evidence_validation_status,
            "approval_ready_after_validation": record.approval_ready_after_validation,
            "runtime_ready_after_validation": record.runtime_ready_after_validation,
            "missing_ref_count": record.missing_ref_count,
            "safe_path": record.safe_path,
            "review_artifact_path": record.review_artifact_path,
            "approval_block_reasons": record.approval_block_reasons,
            "runtime_block_reasons": record.runtime_block_reasons,
        }

def summarize_distillation_inputs(
    *,
    chunk_summary_count: int,
    memory_fact_count: int,
) -> str:
    """Return a tiny status string for downstream ContactSkill work."""

    return (
        f"distillation_inputs_ready:"
        f" chunk_summaries={chunk_summary_count}"
        f" memory_facts={memory_fact_count}"
    )


def collect_source_refs(
    *,
    chunk_summaries: list[ChunkSummary],
    memory_facts: list[MemoryFactCandidate],
) -> list[str]:
    """Collect unique refs for future ContactSkill review assembly."""

    refs: list[str] = []
    seen: set[str] = set()
    for summary in chunk_summaries:
        for ref in summary.evidence_refs:
            if ref in seen:
                continue
            seen.add(ref)
            refs.append(ref)
    for fact in memory_facts:
        for ref in fact.evidence_refs:
            if ref in seen:
                continue
            seen.add(ref)
            refs.append(ref)
    return refs


def collect_reference_fact_ids(
    *,
    memory_facts: list[MemoryFactCandidate],
    max_items: int = 12,
) -> list[str]:
    """Collect memory ids in stable order for candidate provenance."""

    return ContactSkillBuilderService._unique(
        fact.memory_id for fact in memory_facts[:max_items]
    )


def redact_review_text(text: str, *, max_length: int = 120) -> str:
    """Redact obvious sensitive tokens before rendering markdown review text."""

    cleaned = " ".join(text.split()).strip()
    if not cleaned:
        return ""
    patterns = [
        (re.compile(r"\b[A-Z0-9._%+\-]+@[A-Z0-9.\-]+\.[A-Z]{2,}\b", re.IGNORECASE), "[EMAIL]"),
        (re.compile(r"(?<!\w)(?:\+?\d[\d\-\s]{6,}\d)(?!\w)"), "[PHONE]"),
        (re.compile(r"\b(?:https?://|www\.)\S+\b", re.IGNORECASE), "[URL]"),
        (re.compile(r"\b\d{6,}\b"), "[NUMBER]"),
        (
            re.compile(
                r"(introduces (?:self|themselves) as:?\s*)(?:['\"]?)([^,.;'\"\n]+)(?:['\"]?)",
                re.IGNORECASE,
            ),
            r"\1[NAME]",
        ),
        (re.compile(r"(name is\s+)([^,.;]+)", re.IGNORECASE), r"\1[NAME]"),
    ]
    redacted = cleaned
    for pattern, replacement in patterns:
        redacted = pattern.sub(replacement, redacted)
    if len(redacted) <= max_length:
        return redacted
    return f"{redacted[: max_length - 3].rstrip()}..."
