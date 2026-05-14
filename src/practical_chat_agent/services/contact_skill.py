from __future__ import annotations

import json
import re
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
    ContactSkillTopicPreference,
    ContactSkillUserSidePreferences,
    MemoryFactCandidate,
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
