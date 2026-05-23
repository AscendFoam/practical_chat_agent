from __future__ import annotations

import json
from pathlib import Path

from practical_chat_agent.core.models import (
    ApprovedContactSkillBrief,
    ApprovedMemoryFactBrief,
    ApprovedPatchBrief,
    ApprovedPatchContext,
    ApprovedStoreContext,
    AgentProfile,
    ChatContext,
    ChatContextEvent,
    ContactSkillStoreFile,
    ContactSkillStoreRecord,
    DerivedBriefContext,
    InboundEvent,
    MemoryFact,
    MemoryFactStoreFile,
    MemoryFactStoreRecord,
    MemoryProfileSnapshot,
)
from practical_chat_agent.services.contact_skill import ContactSkillProjectionService
from practical_chat_agent.services.feedback import ApprovedPatchContextService


class ChatContextAssembler:
    """Build a compact chat context from recent events and long-term memory hits."""

    def __init__(
        self,
        *,
        recent_events_limit: int = 8,
        memory_hits_limit: int = 8,
        approved_store_path: Path | None = None,
        approved_memory_limit: int = 4,
        approved_patch_path: Path | None = None,
    ) -> None:
        self.recent_events_limit = max(int(recent_events_limit), 1)
        self.memory_hits_limit = max(int(memory_hits_limit), 1)
        self.approved_store_path = approved_store_path
        self.approved_memory_limit = max(int(approved_memory_limit), 1)
        self.approved_patch_path = approved_patch_path
        self._repo_root = Path.cwd().resolve()
        self._private_distilled_root = (self._repo_root / "private" / "distilled").resolve()

    def assemble(
        self,
        *,
        agent: AgentProfile,
        event: InboundEvent,
        recent_events: list[InboundEvent],
        memory_hits: list[MemoryFact],
        intent,
        memory_candidate_count: int = 0,
        memory_profile: MemoryProfileSnapshot | None = None,
        memory_retrieval_notes: list[str] | None = None,
    ) -> ChatContext:
        rendered_events = [
            ChatContextEvent(
                event_id=item.event_id,
                actor_id=item.actor_id,
                actor_name=item.actor_name,
                direction=item.direction,
                content_type=item.content_type,
                source_type=item.source_type,
                occurred_at=item.occurred_at,
                text=item.text,
            )
            for item in recent_events[-self.recent_events_limit :]
        ]
        selected_memory_hits = memory_hits[: self.memory_hits_limit]
        approved_store_context, eligible_skill_record = self._load_approved_store_context(
            contact_id=event.actor_id,
        )
        approved_patch_context = self._load_approved_patch_context(
            contact_id=event.actor_id,
        )
        approved_patch_briefs = (
            approved_patch_context.patches
            if approved_patch_context.status == "loaded"
            else None
        )
        derived_brief_context = self._load_derived_brief_context(
            contact_id=event.actor_id,
            skill_record=eligible_skill_record,
            approved_patch_briefs=approved_patch_briefs,
        )
        combined_retrieval_notes = list(memory_retrieval_notes or [])
        combined_retrieval_notes.extend(self._build_approved_store_notes(approved_store_context))
        combined_retrieval_notes.extend(self._build_approved_patch_notes(approved_patch_context))
        combined_retrieval_notes.extend(self._build_derived_brief_notes(derived_brief_context))
        summary = self._build_summary(
            agent=agent,
            event=event,
            recent_events=rendered_events,
            memory_hits=selected_memory_hits,
            memory_profile=memory_profile or MemoryProfileSnapshot(),
            approved_store_context=approved_store_context,
            approved_patch_context=approved_patch_context,
            derived_brief_context=derived_brief_context,
        )
        return ChatContext(
            agent_id=agent.agent_id,
            agent_display_name=agent.display_name,
            persona_type=agent.persona_type,
            relationship_mode=agent.relationship_mode,
            speech_style=agent.speech_style,
            channel_id=event.channel_id,
            channel_type=event.channel_type,
            platform=event.platform,
            user_id=event.actor_id,
            user_name=event.actor_name,
            intent=intent,
            latest_message_text=(event.text or "").strip() or None,
            recent_events=rendered_events,
            memory_hits=selected_memory_hits,
            memory_candidate_count=max(int(memory_candidate_count), len(selected_memory_hits)),
            memory_profile=memory_profile or MemoryProfileSnapshot(),
            memory_retrieval_notes=combined_retrieval_notes,
            approved_store_context=approved_store_context,
            approved_patch_context=approved_patch_context,
            derived_brief_context=derived_brief_context,
            summary=summary,
        )

    @staticmethod
    def _build_summary(
        *,
        agent: AgentProfile,
        event: InboundEvent,
        recent_events: list[ChatContextEvent],
        memory_hits: list[MemoryFact],
        memory_profile: MemoryProfileSnapshot,
        approved_store_context: ApprovedStoreContext,
        approved_patch_context: ApprovedPatchContext,
        derived_brief_context: DerivedBriefContext,
    ) -> str:
        user_name = event.actor_name or event.actor_id
        latest_text = (event.text or "").strip()
        if len(latest_text) > 96:
            latest_text = f"{latest_text[:93].rstrip()}..."
        memory_preview = ", ".join(memory.fact for memory in memory_hits[:2] if memory.fact.strip())
        if len(memory_preview) > 120:
            memory_preview = f"{memory_preview[:117].rstrip()}..."
        pieces = [
            f"{agent.display_name} is handling a {event.channel_type.value} chat on {event.platform.value}.",
            f"Latest inbound message from {user_name}: {latest_text or '<empty>'}.",
            f"Recent window contains {len(recent_events)} events.",
        ]
        if memory_hits:
            pieces.append(f"Known memory hints: {memory_preview}.")
        if memory_profile is not None and memory_profile.summary:
            pieces.append(f"User profile snapshot: {memory_profile.summary}.")
        if approved_store_context.contact_skill is not None:
            pieces.append(
                f"Approved contact skill brief: {approved_store_context.contact_skill.relationship_summary}.",
            )
        if approved_store_context.status == "loaded" and approved_store_context.memory_facts:
            memory_brief = "; ".join(item.claim for item in approved_store_context.memory_facts[:2])
            if len(memory_brief) > 140:
                memory_brief = f"{memory_brief[:137].rstrip()}..."
            pieces.append(
                f"Approved store memory briefs: {memory_brief}.",
            )
        if approved_patch_context.status == "loaded" and approved_patch_context.patches:
            patch_hints = "; ".join(
                f"[{p.patch_type}] {p.compact_instruction}" for p in approved_patch_context.patches[:3]
            )
            if len(patch_hints) > 200:
                patch_hints = f"{patch_hints[:197].rstrip()}..."
            pieces.append(
                f"Approved preference patch hints: {patch_hints}.",
            )
        if derived_brief_context.status == "loaded":
            if derived_brief_context.persona is not None:
                pieces.append(
                    f"Derived persona brief: {derived_brief_context.persona.relationship_state_summary}.",
                )
            if derived_brief_context.boundary is not None:
                pieces.append(
                    f"Derived boundary sensitivity: {derived_brief_context.boundary.sensitivity_summary}.",
                )
        return " ".join(piece for piece in pieces if piece)

    def _load_approved_store_context(self, *, contact_id: str) -> tuple[ApprovedStoreContext, ContactSkillStoreRecord | None]:
        if self.approved_store_path is None:
            return ApprovedStoreContext(status="not_configured"), None
        resolved_input = self._resolve_configured_store_path(self.approved_store_path)
        if resolved_input is None:
            return ApprovedStoreContext(
                status="store_path_missing",
                source_path=self._safe_relative_path(self.approved_store_path),
                notes=["Configured approved store path does not exist."],
            ), None

        memory_store_path, skill_store_path = self._resolve_store_files(resolved_input)
        source_path = self._safe_relative_path(resolved_input)
        validation_report_path = self._resolve_validation_report_path(resolved_input)
        validation_report_relative = self._safe_relative_path(validation_report_path)
        if validation_report_path is None:
            return ApprovedStoreContext(
                status="validation_report_missing",
                source_path=source_path,
                contact_id=contact_id,
                notes=["No evidence validation report found for approved store context."],
            ), None
        validation_report = self._load_validation_report(validation_report_path)
        if validation_report_path is not None and validation_report is None:
            return ApprovedStoreContext(
                status="validation_report_missing",
                source_path=source_path,
                validation_report_path=validation_report_relative,
                notes=["Configured validation report could not be read as a JSON object."],
            ), None

        validation_records = self._validation_records_by_id(validation_report)
        approved_memory = self._load_runtime_ready_memory_briefs(
            memory_store_path=memory_store_path,
            contact_id=contact_id,
            validation_records=validation_records,
        )
        approved_skill, eligible_record = self._load_runtime_ready_contact_skill_brief(
            skill_store_path=skill_store_path,
            contact_id=contact_id,
            validation_records=validation_records,
        )

        if approved_skill is None and not approved_memory:
            notes: list[str] = []
            if validation_report_path is None:
                notes.append("No validation report found for approved store context.")
            return ApprovedStoreContext(
                status="no_runtime_ready_records",
                source_path=source_path,
                validation_report_path=validation_report_relative,
                contact_id=contact_id,
                notes=notes or ["No approved runtime-ready store records matched this contact."],
            ), None

        source_record_ids = []
        evidence_refs = []
        if approved_skill is not None:
            source_record_ids.append(approved_skill.record_id)
            evidence_refs.extend(approved_skill.evidence_refs)
        for item in approved_memory:
            source_record_ids.append(item.record_id)
            evidence_refs.extend(item.evidence_refs)
        return ApprovedStoreContext(
            status="loaded",
            source_path=source_path,
            validation_report_path=validation_report_relative,
            contact_id=contact_id,
            contact_skill=approved_skill,
            memory_facts=approved_memory,
            source_record_ids=self._unique_strings(source_record_ids),
            evidence_refs=self._unique_strings(evidence_refs),
        ), eligible_record

    def _build_approved_store_notes(self, context: ApprovedStoreContext) -> list[str]:
        if context.status != "loaded":
            return list(context.notes)
        notes = [
            f"approved_store_context source={context.source_path or 'private/distilled'}",
            f"approved_store_record_ids={', '.join(context.source_record_ids[:4])}",
        ]
        if context.contact_skill is not None:
            notes.append(
                f"approved_contact_skill={context.contact_skill.relationship_summary}",
            )
            if context.contact_skill.strategy_hints:
                notes.append(
                    f"approved_strategy_hints={'; '.join(context.contact_skill.strategy_hints[:2])}",
                )
            if context.contact_skill.boundary_reminders:
                notes.append(
                    f"approved_boundaries={'; '.join(context.contact_skill.boundary_reminders[:2])}",
                )
        if context.memory_facts:
            notes.append(
                f"approved_memory_facts={'; '.join(item.claim for item in context.memory_facts[:2])}",
            )
        return notes

    def _load_derived_brief_context(
        self,
        *,
        contact_id: str,
        skill_record: ContactSkillStoreRecord | None,
        approved_patch_briefs: list[ApprovedPatchBrief] | None,
    ) -> DerivedBriefContext:
        if skill_record is None:
            return DerivedBriefContext()
        projection_service = ContactSkillProjectionService()
        result = projection_service.project_all(
            record=skill_record,
            approved_patch_hints=approved_patch_briefs,
        )
        if not result.runtime_ready:
            return DerivedBriefContext(
                status="no_runtime_ready_records",
                notes=["Eligible record is not runtime-ready for derived brief projection."],
            )
        return DerivedBriefContext(
            status="loaded",
            persona=result.persona,
            policy=result.policy,
            boundary=result.boundary,
            source_skill_record_id=result.record_id,
        )

    @staticmethod
    def _build_derived_brief_notes(context: DerivedBriefContext) -> list[str]:
        if context.status != "loaded":
            return list(context.notes)
        notes = [
            f"derived_brief_context source_skill_record_id={context.source_skill_record_id}",
        ]
        if context.persona is not None:
            notes.append(
                f"derived_persona_summary={context.persona.relationship_state_summary}",
            )
        if context.policy is not None and context.policy.stable_preference_hints:
            notes.append(
                f"derived_stable_prefs={'; '.join(context.policy.stable_preference_hints[:2])}",
            )
        if context.boundary is not None:
            notes.append(
                f"derived_boundary_sensitivity={context.boundary.sensitivity_summary}",
            )
        return notes

    def _load_approved_patch_context(self, *, contact_id: str) -> ApprovedPatchContext:
        if self.approved_patch_path is None:
            return ApprovedPatchContext(status="not_configured")
        resolved = self._resolve_configured_store_path(self.approved_patch_path)
        if resolved is None:
            return ApprovedPatchContext(
                status="store_path_missing",
                source_path=self._safe_relative_path(self.approved_patch_path),
                contact_id=contact_id,
                notes=["Configured approved patch path does not exist."],
            )
        service = ApprovedPatchContextService()
        return service.load_approved_patches(
            report_path=resolved,
            contact_id=contact_id,
        )

    @staticmethod
    def _build_approved_patch_notes(context: ApprovedPatchContext) -> list[str]:
        if context.status != "loaded":
            return list(context.notes)
        notes = [
            f"approved_patch_context source={context.source_path or 'private/distilled'}",
            f"approved_patch_count={len(context.patches)}",
        ]
        for patch in context.patches[:4]:
            notes.append(
                f"approved_patch {patch.patch_id}: "
                f"[{patch.patch_type}] {patch.compact_instruction} "
                f"(sensitivity={patch.sensitivity}, "
                f"feedback_count={patch.supporting_feedback_count})"
            )
        return notes

    def _load_runtime_ready_memory_briefs(
        self,
        *,
        memory_store_path: Path | None,
        contact_id: str,
        validation_records: dict[str, dict],
    ) -> list[ApprovedMemoryFactBrief]:
        if memory_store_path is None or not memory_store_path.is_file():
            return []
        store = self._read_json_model(memory_store_path, MemoryFactStoreFile)
        if store is None:
            return []
        approved_items: list[ApprovedMemoryFactBrief] = []
        for record in store.records:
            if not self._memory_record_eligible(
                record=record,
                contact_id=contact_id,
                validation_records=validation_records,
            ):
                continue
            approved_items.append(
                ApprovedMemoryFactBrief(
                    record_id=record.record_id,
                    memory_id=record.memory_fact.memory_id,
                    memory_type=record.memory_fact.memory_type,
                    claim=self._compact_text(record.memory_fact.claim, max_length=140),
                    evidence_refs=self._limit_refs(record.memory_fact.evidence_refs),
                ),
            )
            if len(approved_items) >= self.approved_memory_limit:
                break
        return approved_items

    def _load_runtime_ready_contact_skill_brief(
        self,
        *,
        skill_store_path: Path | None,
        contact_id: str,
        validation_records: dict[str, dict],
    ) -> tuple[ApprovedContactSkillBrief | None, ContactSkillStoreRecord | None]:
        if skill_store_path is None or not skill_store_path.is_file():
            return None, None
        store = self._read_json_model(skill_store_path, ContactSkillStoreFile)
        if store is None:
            return None, None
        for record in store.records:
            if not self._contact_skill_record_eligible(
                record=record,
                contact_id=contact_id,
                validation_records=validation_records,
            ):
                continue
            strategy_hints = self._collect_strategy_hints(record)
            boundary_reminders = [
                self._compact_text(note, max_length=120)
                for note in record.contact_skill.usage_boundary.notes[:2]
            ]
            boundary_reminders.extend(
                self._compact_text(item, max_length=100)
                for item in record.contact_skill.user_side_preferences.boundaries[:2]
            )
            return ApprovedContactSkillBrief(
                record_id=record.record_id,
                contact_id=record.contact_skill.contact_id,
                relationship_type=record.contact_skill.relationship_type,
                relationship_summary=self._build_relationship_summary(record),
                strategy_hints=self._unique_strings([hint for hint in strategy_hints if hint]),
                boundary_reminders=self._unique_strings([item for item in boundary_reminders if item]),
                evidence_refs=self._limit_refs(record.contact_skill.evidence_refs),
            ), record
        return None, None

    def _memory_record_eligible(
        self,
        *,
        record: MemoryFactStoreRecord,
        contact_id: str,
        validation_records: dict[str, dict],
    ) -> bool:
        if record.memory_fact.subject_id != contact_id:
            return False
        if record.memory_fact.status != "approved":
            return False
        if not record.is_runtime_ready():
            return False
        if record.review_metadata.evidence_validation_status != "passed":
            return False
        if not self._validation_record_is_evidence_ready(
            validation_record=validation_records.get(record.record_id),
        ):
            return False
        return True

    def _contact_skill_record_eligible(
        self,
        *,
        record: ContactSkillStoreRecord,
        contact_id: str,
        validation_records: dict[str, dict],
    ) -> bool:
        if record.contact_skill.contact_id != contact_id:
            return False
        if record.contact_skill.status != "approved":
            return False
        if not record.is_runtime_ready():
            return False
        if record.review_metadata.evidence_validation_status != "passed":
            return False
        if not self._validation_record_is_evidence_ready(
            validation_record=validation_records.get(record.record_id),
        ):
            return False
        return True

    def _resolve_configured_store_path(self, path: Path) -> Path | None:
        resolved = (self._repo_root / path).resolve() if not path.is_absolute() else path.resolve()
        if not resolved.exists():
            return None
        self._ensure_within_private_distilled(resolved)
        return resolved

    def _resolve_store_files(self, path: Path) -> tuple[Path | None, Path | None]:
        if path.is_file():
            name = path.name
            if name == "memory_fact_store.json":
                return path, None
            if name == "contact_skill_store.json":
                return None, path
            return None, None
        memory_store = path / "memory_fact_store.json"
        contact_skill_store = path / "contact_skill_store.json"
        return (
            memory_store if memory_store.is_file() else None,
            contact_skill_store if contact_skill_store.is_file() else None,
        )

    def _resolve_validation_report_path(self, path: Path) -> Path | None:
        run_dir = path if path.is_dir() else path.parent
        candidate = run_dir / "evidence_validation_report.json"
        return candidate if candidate.is_file() else None

    def _load_validation_report(self, path: Path | None) -> dict | None:
        if path is None:
            return None
        try:
            payload = json.loads(path.read_text(encoding="utf-8-sig"))
        except (OSError, json.JSONDecodeError):
            return None
        return payload if isinstance(payload, dict) else None

    @staticmethod
    def _validation_records_by_id(validation_report: dict | None) -> dict[str, dict]:
        if validation_report is None:
            return {}
        records = validation_report.get("records")
        if not isinstance(records, list):
            return {}
        mapped: dict[str, dict] = {}
        for item in records:
            if not isinstance(item, dict):
                continue
            record_id = item.get("record_id")
            if isinstance(record_id, str) and record_id:
                mapped[record_id] = item
        return mapped

    @staticmethod
    def _validation_record_is_evidence_ready(*, validation_record: dict | None) -> bool:
        if validation_record is None:
            return False
        missing_ref_count = int(validation_record.get("missing_ref_count", 0))
        checked_ref_count = int(validation_record.get("checked_ref_count", 0))
        return missing_ref_count == 0 and checked_ref_count > 0

    @staticmethod
    def _read_json_model(path: Path, model_type):
        try:
            payload = json.loads(path.read_text(encoding="utf-8-sig"))
        except (OSError, json.JSONDecodeError):
            return None
        if not isinstance(payload, dict):
            return None
        try:
            return model_type.model_validate(payload)
        except Exception:
            return None

    def _build_relationship_summary(self, record: ContactSkillStoreRecord) -> str:
        skill = record.contact_skill
        state = skill.relationship_state
        pieces = [
            f"{skill.relationship_type} relationship",
            f"current_status={state.current_status}",
            f"tone={skill.communication_style.tone}",
            f"directness={skill.communication_style.directness}",
        ]
        return self._compact_text("; ".join(pieces), max_length=160)

    def _collect_strategy_hints(self, record: ContactSkillStoreRecord) -> list[str]:
        strategy = record.contact_skill.reply_strategy
        hints = [
            strategy.default,
            strategy.when_contact_is_cold,
            strategy.when_contact_opens_topic,
            strategy.for_sensitive_topics,
        ]
        return [
            self._compact_text(item, max_length=120)
            for item in hints
            if isinstance(item, str) and item.strip()
        ][:4]

    def _safe_relative_path(self, path: Path | None) -> str | None:
        if path is None:
            return None
        try:
            return str(path.relative_to(self._repo_root)).replace("\\", "/")
        except ValueError:
            return str(path).replace("\\", "/")

    def _ensure_within_private_distilled(self, path: Path) -> None:
        try:
            path.relative_to(self._private_distilled_root)
        except ValueError as exc:
            raise ValueError("Approved store path must stay within private/distilled.") from exc

    @staticmethod
    def _compact_text(text: str, *, max_length: int) -> str:
        cleaned = " ".join((text or "").split()).strip()
        if not cleaned:
            return ""
        if len(cleaned) <= max_length:
            return cleaned
        return f"{cleaned[: max_length - 3].rstrip()}..."

    @staticmethod
    def _limit_refs(refs: list[str], *, limit: int = 6) -> list[str]:
        return [ref for ref in refs[:limit] if isinstance(ref, str) and ref]

    @staticmethod
    def _unique_strings(values: list[str]) -> list[str]:
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
