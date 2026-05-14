from __future__ import annotations

import json
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from urllib.request import Request, urlopen

from pydantic import BaseModel, Field, ValidationError

from practical_chat_agent.core.models import (
    ChunkSummary,
    ChunkSummaryObservation,
    DistillationClaim,
    MemoryFactCandidate,
)


class ChatlogDistillationError(ValueError):
    """Raised when distillation input, model output, or file handling is invalid."""

    def __init__(self, message: str, *, code: str | None = None) -> None:
        super().__init__(message)
        self.code = code or message


@dataclass(frozen=True)
class ChatlogDistillationResult:
    output_dir: Path | None
    report: dict[str, Any]


class _ChunkSummaryDraft(BaseModel):
    summary: str
    topics: list[str] = Field(default_factory=list, max_length=8)
    evidence_refs: list[str] = Field(..., min_length=1)
    confidence: float = Field(..., ge=0.0, le=1.0)
    sensitivity: Literal["low", "medium", "high"]
    status: Literal["candidate", "approved", "rejected", "frozen", "archived"]
    important_facts: list[DistillationClaim] = Field(default_factory=list, max_length=6)
    communication_observations: list[ChunkSummaryObservation] = Field(
        default_factory=list,
        max_length=6,
    )
    risk_notes: list[str] = Field(default_factory=list, max_length=6)


class _ChunkDistillationEnvelope(BaseModel):
    chunk_summary: _ChunkSummaryDraft
    memory_facts: list[MemoryFactCandidate] = Field(default_factory=list, max_length=8)


class ChatlogDistillationService:
    """Distill chunk summaries and evidence-backed memory facts from private chat chunks."""

    backend_name = "chatlog_distill"

    _PHONE_PATTERN = re.compile(r"(?<!\w)(?:\+?\d[\d\-\s]{6,}\d)(?!\w)")
    _EMAIL_PATTERN = re.compile(r"\b[A-Z0-9._%+\-]+@[A-Z0-9.\-]+\.[A-Z]{2,}\b", re.IGNORECASE)
    _URL_PATTERN = re.compile(r"\b(?:https?://|www\.)\S+\b", re.IGNORECASE)
    _ACCOUNT_PATTERN = re.compile(r"\b(?:wxid_[A-Za-z0-9_\-]+|[A-Za-z][A-Za-z0-9_\-]{7,})\b")
    _PATH_PATTERN = re.compile(r"(?:[A-Za-z]:\\[^\s]+|/[^\s]+)")
    _DIGIT_RUN_PATTERN = re.compile(r"\b\d{6,}\b")

    def __init__(
        self,
        *,
        api_key: str | None,
        base_url: str | None,
        model: str | None,
        timeout_seconds: float = 45.0,
        enabled: bool = True,
        default_model: str = "deepseek-chat",
    ) -> None:
        self.api_key = (api_key or "").strip() or None
        self.base_url = (base_url or "").strip() or None
        self.model = (model or "").strip() or None
        self.timeout_seconds = max(float(timeout_seconds), 3.0)
        self.enabled = enabled
        self.default_model = default_model
        self._repo_root = Path.cwd().resolve()
        self._private_distilled_root = (self._repo_root / "private" / "distilled").resolve()

    @property
    def resolved_model(self) -> str:
        return self.model or self.default_model

    def availability_reason(self) -> str | None:
        if not self.enabled:
            return "chatlog distillation is disabled"
        if not self.api_key:
            return "OPENAI_API_KEY is not configured"
        if not self.base_url:
            return "OPENAI_BASE_URL is not configured"
        return None

    def distill_chunks(
        self,
        *,
        input_path: Path,
        output_dir: Path | None,
        limit: int | None = None,
        sample: int | None = None,
        dry_run: bool = False,
    ) -> ChatlogDistillationResult:
        chunks_path, normalized_events_path = self._resolve_input_files(input_path)

        selected_chunks, selection_report = self._load_selected_chunks(
            chunks_path=chunks_path,
            limit=limit,
            sample=sample,
        )
        needed_event_ids = {
            event_id
            for chunk in selected_chunks
            for event_id in chunk["event_ids"]
            if isinstance(event_id, str)
        }
        events_by_id, event_scan_report = self._load_events_by_id(
            normalized_events_path=normalized_events_path,
            needed_event_ids=needed_event_ids,
        )

        resolved_output_dir: Path | None = None
        if not dry_run:
            resolved_output_dir = self._resolve_output_dir(output_dir or chunks_path.parent)
            resolved_output_dir.mkdir(parents=True, exist_ok=True)

        summary_records: list[ChunkSummary] = []
        fact_records: list[MemoryFactCandidate] = []
        failure_reasons: Counter[str] = Counter()
        chunk_outcomes: list[dict[str, Any]] = []
        warnings: set[str] = set()

        for chunk in selected_chunks:
            chunk_id = chunk["chunk_id"]
            chunk_event_ids = [event_id for event_id in chunk["event_ids"] if isinstance(event_id, str)]
            chunk_events = [events_by_id[event_id] for event_id in chunk_event_ids if event_id in events_by_id]
            missing_event_ids = [event_id for event_id in chunk_event_ids if event_id not in events_by_id]
            if missing_event_ids:
                failure_reasons["missing_chunk_events"] += 1
                chunk_outcomes.append(
                    {
                        "chunk_id": chunk_id,
                        "status": "skipped",
                        "reason": "missing_chunk_events",
                        "missing_event_count": len(missing_event_ids),
                    },
                )
                warnings.add("missing_selected_events")
                continue

            try:
                envelope = self._distill_remote(chunk=chunk, events=chunk_events)
                chunk_summary = self._build_chunk_summary(chunk=chunk, draft=envelope.chunk_summary)
                memory_facts = self._build_memory_facts(
                    chunk=chunk,
                    facts=envelope.memory_facts,
                )
                validation_errors = self._validate_chunk_evidence(
                    chunk_id=chunk_id,
                    chunk_summary=chunk_summary,
                    memory_facts=memory_facts,
                    allowed_refs=set(chunk_event_ids) | {chunk_id},
                )
                if validation_errors:
                    failure_reasons["invalid_evidence_refs"] += 1
                    chunk_outcomes.append(
                        {
                            "chunk_id": chunk_id,
                            "status": "rejected",
                            "reason": "invalid_evidence_refs",
                            "issues": validation_errors,
                        },
                    )
                    continue

                summary_records.append(chunk_summary)
                fact_records.extend(memory_facts)
                chunk_outcomes.append(
                    {
                        "chunk_id": chunk_id,
                        "status": "ok",
                        "reason": "validated",
                        "fact_count": len(memory_facts),
                    },
                )
            except ChatlogDistillationError as exc:
                failure_reasons[exc.code] += 1
                chunk_outcomes.append(
                    {
                        "chunk_id": chunk_id,
                        "status": "failed",
                        "reason": exc.code,
                    },
                )
            except Exception:
                failure_reasons["unexpected_error"] += 1
                chunk_outcomes.append(
                    {
                        "chunk_id": chunk_id,
                        "status": "failed",
                        "reason": "unexpected_error",
                    },
                )

        report = {
            "tool": "chatlog-distill",
            "backend": self.backend_name,
            "model": self.resolved_model,
            "availability": {
                "configured": self.availability_reason() is None,
                "reason": self.availability_reason(),
            },
            "selection": selection_report,
            "event_scan": event_scan_report,
            "distillation_stats": {
                "selected_chunks": len(selected_chunks),
                "successful_chunks": sum(1 for item in chunk_outcomes if item["status"] == "ok"),
                "failed_chunks": sum(1 for item in chunk_outcomes if item["status"] == "failed"),
                "rejected_chunks": sum(1 for item in chunk_outcomes if item["status"] == "rejected"),
                "skipped_chunks": sum(1 for item in chunk_outcomes if item["status"] == "skipped"),
                "chunk_summaries_written": len(summary_records),
                "memory_facts_written": len(fact_records),
            },
            "failure_reasons": {key: failure_reasons[key] for key in sorted(failure_reasons)},
            "chunk_outcomes": chunk_outcomes[:50],
            "warnings": sorted(warnings),
            "dry_run": dry_run,
            "input_files": {
                "chunks": self._safe_relative_path(chunks_path),
                "normalized_events": self._safe_relative_path(normalized_events_path),
            },
        }

        if resolved_output_dir is not None:
            self._write_jsonl(
                output_path=resolved_output_dir / "chunk_summaries.jsonl",
                records=summary_records,
            )
            self._write_jsonl(
                output_path=resolved_output_dir / "memory_facts.jsonl",
                records=fact_records,
            )
            report["output_dir"] = self._safe_relative_path(resolved_output_dir)
            report["output_files"] = [
                "chunk_summaries.jsonl",
                "memory_facts.jsonl",
                "run_report.json",
            ]
            self._write_run_report(output_dir=resolved_output_dir, distillation_report=report)
        else:
            report["output_dir"] = None
            report["output_files"] = []

        return ChatlogDistillationResult(output_dir=resolved_output_dir, report=report)

    def _distill_remote(
        self,
        *,
        chunk: dict[str, Any],
        events: list[dict[str, Any]],
    ) -> _ChunkDistillationEnvelope:
        remote_reason = self.availability_reason()
        if remote_reason is not None:
            raise ChatlogDistillationError(remote_reason, code="provider_unavailable")

        payload: dict[str, Any] = {
            "model": self.resolved_model,
            "temperature": 0.2,
            "messages": [
                {
                    "role": "system",
                    "content": self._build_system_prompt(),
                },
                {
                    "role": "user",
                    "content": self._build_user_prompt(chunk=chunk, events=events),
                },
            ],
        }
        response_format = self._build_response_format()
        if response_format is not None:
            payload["response_format"] = response_format

        response = self._post_json(
            url=self._chat_completions_url(),
            payload=payload,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
        )
        content = self._extract_message_content(response=response)
        parsed = self._parse_json_content(content=content)
        normalized = self._normalize_provider_output(parsed=parsed, chunk=chunk)
        try:
            return _ChunkDistillationEnvelope.model_validate(normalized)
        except ValidationError as exc:
            raise ChatlogDistillationError(
                "Model output did not match the distillation schema.",
                code="output_invalid_schema",
            ) from exc

    @staticmethod
    def _build_system_prompt() -> str:
        return (
            "You distill one private chat chunk into auditable structured JSON.\n"
            "Return JSON only.\n"
            "Do not include markdown.\n"
            "Do not invent facts beyond the provided events.\n"
            "Every summary claim and every memory fact must include evidence_refs.\n"
            "Evidence refs may only use the provided chunk_id or the provided event_ids.\n"
            "Prefer paraphrases over direct quotes.\n"
            "Keep all statuses as candidate because no human review has happened yet.\n"
            "Keep the output conservative when the signals are weak or mixed.\n"
            "Do not infer a stable relationship pattern from a single ambiguous message.\n"
            "At most 1 chunk_summary object and at most 8 memory_facts."
        )

    def _build_user_prompt(self, *, chunk: dict[str, Any], events: list[dict[str, Any]]) -> str:
        allowed_refs = [chunk["chunk_id"], *chunk["event_ids"]]
        rendered_events = "\n".join(
            f"- {self._render_event_line(event)}"
            for event in events
        )
        return (
            f"Chunk metadata:\n"
            f"- chunk_id: {chunk['chunk_id']}\n"
            f"- contact_id: {chunk['contact_id']}\n"
            f"- conversation_id: {chunk['conversation_id']}\n"
            f"- time_range: {chunk.get('time_range')}\n"
            f"- message_count: {chunk.get('message_count')}\n"
            f"- chunking_reason: {chunk.get('chunking_reason')}\n"
            f"- source_message_type_codes: {chunk.get('source_message_type_codes', [])}\n"
            f"- interaction_flags: {chunk.get('interaction_flags', [])}\n"
            f"- risk_flags: {chunk.get('risk_flags', [])}\n"
            f"- allowed_evidence_refs: {allowed_refs}\n"
            "Tasks:\n"
            "1. Produce one chunk summary.\n"
            "2. Extract only durable or review-worthy memory fact candidates.\n"
            "3. Keep claims concise, paraphrased, and evidence-backed.\n"
            "4. Use subject_id values such as the provided contact_id, user, or a relationship_* id when justified.\n"
            "5. If the evidence is weak, reduce confidence instead of inventing certainty.\n"
            "6. Do not emit any item without evidence_refs.\n"
            "Event window:\n"
            f"{rendered_events}\n"
            "Return an object with exactly these top-level keys: chunk_summary, memory_facts."
        )

    def _build_response_format(self) -> dict[str, Any] | None:
        if "deepseek" in self.resolved_model.casefold():
            return {"type": "json_object"}
        return {
            "type": "json_schema",
            "json_schema": {
                "name": "chunk_distillation_envelope",
                "strict": True,
                "schema": _ChunkDistillationEnvelope.model_json_schema(),
            },
        }

    def _normalize_provider_output(
        self,
        *,
        parsed: dict[str, Any],
        chunk: dict[str, Any],
    ) -> dict[str, Any]:
        envelope = parsed
        for key in ("result", "data", "output"):
            nested = envelope.get(key)
            if isinstance(nested, dict):
                envelope = nested
                break

        raw_chunk_summary = envelope.get("chunk_summary")
        if not isinstance(raw_chunk_summary, dict):
            raw_chunk_summary = {
                "summary": envelope.get("summary"),
                "topics": envelope.get("topics"),
                "evidence_refs": envelope.get("evidence_refs"),
                "confidence": envelope.get("confidence"),
                "sensitivity": envelope.get("sensitivity"),
                "status": envelope.get("status"),
                "important_facts": envelope.get("important_facts"),
                "communication_observations": envelope.get("communication_observations"),
                "risk_notes": envelope.get("risk_notes"),
            }

        raw_memory_facts = envelope.get("memory_facts")
        if not isinstance(raw_memory_facts, list):
            raw_memory_facts = envelope.get("facts")
        if not isinstance(raw_memory_facts, list):
            raw_memory_facts = envelope.get("memories")
        if not isinstance(raw_memory_facts, list):
            raw_memory_facts = []

        return {
            "chunk_summary": self._normalize_chunk_summary(raw=raw_chunk_summary, chunk=chunk),
            "memory_facts": [
                self._normalize_memory_fact(raw=item, chunk=chunk)
                for item in raw_memory_facts
                if isinstance(item, dict)
            ],
        }

    def _normalize_chunk_summary(
        self,
        *,
        raw: dict[str, Any],
        chunk: dict[str, Any],
    ) -> dict[str, Any]:
        summary = self._clean_string(
            raw.get("summary")
            or raw.get("chunk_summary")
            or raw.get("overview")
            or raw.get("description"),
        )
        evidence_refs = self._normalize_evidence_refs(
            raw.get("evidence_refs"),
            default=[chunk["chunk_id"]],
        )
        return {
            "summary": summary,
            "topics": self._clean_string_list(raw.get("topics"), max_items=8),
            "evidence_refs": evidence_refs,
            "confidence": self._coerce_score(raw.get("confidence"), default=0.72),
            "sensitivity": self._normalize_sensitivity(
                raw.get("sensitivity"),
                default=self._default_sensitivity_from_chunk(chunk=chunk),
            ),
            "status": "candidate",
            "important_facts": self._normalize_claim_list(raw.get("important_facts")),
            "communication_observations": self._normalize_observation_list(
                raw.get("communication_observations"),
            ),
            "risk_notes": self._clean_string_list(raw.get("risk_notes"), max_items=6),
        }

    def _normalize_memory_fact(self, *, raw: dict[str, Any], chunk: dict[str, Any]) -> dict[str, Any]:
        subject_id = self._clean_string(raw.get("subject_id")) or str(chunk["contact_id"])
        claim = self._clean_string(raw.get("claim"))
        if not claim:
            claim = self._predicate_object_to_claim(
                subject_id=subject_id,
                predicate=self._clean_string(raw.get("predicate")),
                object_value=self._clean_string(raw.get("object")),
            )
        evidence_refs = self._normalize_evidence_refs(
            raw.get("evidence_refs"),
            default=[chunk["chunk_id"]],
        )
        predicate_hint = self._clean_string(raw.get("predicate"))
        object_hint = self._clean_string(raw.get("object"))
        memory_type = self._normalize_memory_type(
            raw.get("memory_type"),
            predicate_hint=predicate_hint,
            claim=claim,
        )
        confidence = self._coerce_score(raw.get("confidence"), default=0.72)
        return {
            "memory_type": memory_type,
            "subject_id": subject_id,
            "claim": claim,
            "evidence_refs": evidence_refs,
            "confidence": confidence,
            "importance": self._coerce_score(
                raw.get("importance"),
                default=self._default_importance(
                    memory_type=memory_type,
                    confidence=confidence,
                ),
            ),
            "sensitivity": self._normalize_sensitivity(
                raw.get("sensitivity"),
                default=self._default_sensitivity_for_fact(
                    predicate_hint=predicate_hint,
                    object_hint=object_hint,
                    claim=claim,
                    chunk=chunk,
                ),
            ),
            "status": "candidate",
            "rationale": self._clean_string(
                raw.get("rationale")
                or raw.get("reasoning")
                or raw.get("why"),
            ),
            "conflicts_with": self._clean_string_list(raw.get("conflicts_with"), max_items=8),
            "source_chunk_ids": [str(chunk["chunk_id"])],
        }

    def _build_chunk_summary(
        self,
        *,
        chunk: dict[str, Any],
        draft: _ChunkSummaryDraft,
    ) -> ChunkSummary:
        summary_text = self._clean_string(draft.summary)
        if not summary_text:
            raise ChatlogDistillationError(
                "Chunk summary text was empty.",
                code="empty_chunk_summary",
            )
        try:
            return ChunkSummary(
                chunk_id=chunk["chunk_id"],
                contact_id=chunk["contact_id"],
                conversation_id=chunk["conversation_id"],
                time_range=list(chunk.get("time_range", [])),
                event_ids=list(chunk.get("event_ids", [])),
                message_count=int(chunk.get("message_count", 0)),
                chunking_reason=str(chunk.get("chunking_reason", "manual")),
                summary=summary_text,
                topics=self._clean_string_list(draft.topics, max_items=8),
                evidence_refs=list(draft.evidence_refs),
                confidence=float(draft.confidence),
                sensitivity=draft.sensitivity,
                status="candidate",
                important_facts=[self._force_claim_candidate(item) for item in draft.important_facts],
                communication_observations=[
                    self._force_observation_candidate(item)
                    for item in draft.communication_observations
                ],
                risk_notes=self._clean_string_list(draft.risk_notes, max_items=6),
                source_message_type_codes=[
                    int(code)
                    for code in chunk.get("source_message_type_codes", [])
                    if isinstance(code, int)
                ],
                interaction_flags=self._clean_string_list(
                    chunk.get("interaction_flags", []),
                    max_items=12,
                ),
                risk_flags=self._clean_string_list(
                    chunk.get("risk_flags", []),
                    max_items=12,
                ),
            )
        except ValidationError as exc:
            raise ChatlogDistillationError(
                "Chunk summary could not be validated.",
                code="output_invalid_schema",
            ) from exc

    def _build_memory_facts(
        self,
        *,
        chunk: dict[str, Any],
        facts: list[MemoryFactCandidate],
    ) -> list[MemoryFactCandidate]:
        chunk_id = str(chunk["chunk_id"])
        validated: list[MemoryFactCandidate] = []
        for fact in facts:
            claim_text = self._clean_string(fact.claim)
            subject_id = self._clean_string(fact.subject_id)
            if not claim_text or not subject_id:
                raise ChatlogDistillationError(
                    "Memory fact was missing claim or subject_id.",
                    code="empty_memory_fact",
                )
            source_chunk_ids = list(fact.source_chunk_ids) if fact.source_chunk_ids else [chunk_id]
            if any(source_chunk_id != chunk_id for source_chunk_id in source_chunk_ids):
                raise ChatlogDistillationError(
                    "Memory fact referenced a foreign source chunk.",
                    code="invalid_source_chunk_ids",
                )
            try:
                validated.append(
                    MemoryFactCandidate.model_validate(
                        {
                            **fact.model_dump(mode="json"),
                            "subject_id": subject_id,
                            "claim": claim_text,
                            "status": "candidate",
                            "source_chunk_ids": [chunk_id],
                        },
                    ),
                )
            except ValidationError as exc:
                raise ChatlogDistillationError(
                    "Memory fact could not be validated.",
                    code="output_invalid_schema",
                ) from exc
        return validated

    def _validate_chunk_evidence(
        self,
        *,
        chunk_id: str,
        chunk_summary: ChunkSummary,
        memory_facts: list[MemoryFactCandidate],
        allowed_refs: set[str],
    ) -> list[dict[str, Any]]:
        issues: list[dict[str, Any]] = []
        issues.extend(
            self._validate_refs(
                label="chunk_summary",
                refs=chunk_summary.evidence_refs,
                allowed_refs=allowed_refs,
            ),
        )
        for index, claim in enumerate(chunk_summary.important_facts):
            issues.extend(
                self._validate_refs(
                    label=f"important_facts[{index}]",
                    refs=claim.evidence_refs,
                    allowed_refs=allowed_refs,
                ),
            )
        for index, observation in enumerate(chunk_summary.communication_observations):
            issues.extend(
                self._validate_refs(
                    label=f"communication_observations[{index}]",
                    refs=observation.evidence_refs,
                    allowed_refs=allowed_refs,
                ),
            )
        for index, fact in enumerate(memory_facts):
            issues.extend(
                self._validate_refs(
                    label=f"memory_facts[{index}]",
                    refs=fact.evidence_refs,
                    allowed_refs=allowed_refs,
                ),
            )
            if chunk_id not in fact.source_chunk_ids:
                issues.append(
                    {
                        "field": f"memory_facts[{index}].source_chunk_ids",
                        "reason": "missing_selected_chunk_id",
                    },
                )
        return issues

    @staticmethod
    def _validate_refs(
        *,
        label: str,
        refs: list[str],
        allowed_refs: set[str],
    ) -> list[dict[str, Any]]:
        issues: list[dict[str, Any]] = []
        if not refs:
            issues.append({"field": label, "reason": "empty_evidence_refs"})
            return issues
        invalid_refs = [ref for ref in refs if ref not in allowed_refs]
        if invalid_refs:
            issues.append(
                {
                    "field": label,
                    "reason": "out_of_scope_evidence_refs",
                    "invalid_refs": invalid_refs,
                },
            )
        return issues

    def _normalize_claim_list(self, value: Any) -> list[dict[str, Any]]:
        if not isinstance(value, list):
            return []
        normalized: list[dict[str, Any]] = []
        for item in value[:6]:
            if not isinstance(item, dict):
                continue
            claim = self._clean_string(
                item.get("claim")
                or item.get("fact")
                or item.get("summary"),
            )
            if not claim:
                continue
            normalized.append(
                {
                    "claim": claim,
                    "evidence_refs": self._normalize_evidence_refs(item.get("evidence_refs"), default=[]),
                    "confidence": self._coerce_score(item.get("confidence"), default=0.65),
                    "sensitivity": self._normalize_sensitivity(item.get("sensitivity"), default="low"),
                    "status": "candidate",
                    "rationale": self._clean_string(item.get("rationale")),
                },
            )
        return normalized

    def _normalize_observation_list(self, value: Any) -> list[dict[str, Any]]:
        if not isinstance(value, list):
            return []
        normalized: list[dict[str, Any]] = []
        for item in value[:6]:
            if not isinstance(item, dict):
                continue
            claim = self._clean_string(
                item.get("claim")
                or item.get("observation")
                or item.get("summary"),
            )
            if not claim:
                continue
            normalized.append(
                {
                    "observation_type": self._clean_string(item.get("observation_type")) or "general",
                    "claim": claim,
                    "evidence_refs": self._normalize_evidence_refs(item.get("evidence_refs"), default=[]),
                    "confidence": self._coerce_score(item.get("confidence"), default=0.6),
                    "sensitivity": self._normalize_sensitivity(item.get("sensitivity"), default="low"),
                    "status": "candidate",
                    "rationale": self._clean_string(item.get("rationale")),
                },
            )
        return normalized

    @classmethod
    def _normalize_evidence_refs(cls, value: Any, *, default: list[str]) -> list[str]:
        if isinstance(value, list):
            refs = [cleaned for item in value if (cleaned := cls._clean_string(item))]
            if refs:
                return refs
        if isinstance(value, str):
            cleaned = cls._clean_string(value)
            if cleaned:
                return [cleaned]
        return list(default)

    @staticmethod
    def _normalize_sensitivity(value: Any, *, default: Literal["low", "medium", "high"]) -> Literal["low", "medium", "high"]:
        if isinstance(value, str):
            normalized = value.strip().casefold()
            if normalized in {"low", "medium", "high"}:
                return normalized  # type: ignore[return-value]
        return default

    @staticmethod
    def _normalize_memory_type(
        value: Any,
        *,
        predicate_hint: str | None,
        claim: str | None,
    ) -> Literal["semantic", "episodic", "relationship", "procedural", "reflection"]:
        if isinstance(value, str):
            normalized = value.strip().casefold()
            if normalized in {"semantic", "episodic", "relationship", "procedural", "reflection"}:
                return normalized  # type: ignore[return-value]

        hint = " ".join(
            part for part in (predicate_hint or "", claim or "")
            if part
        ).casefold()
        if any(token in hint for token in ("concern", "worried", "anxious", "stress", "emotion", "feels", "doubt")):
            return "reflection"
        if any(token in hint for token in ("boyfriend", "girlfriend", "family", "friend", "relationship", "trust")):
            return "relationship"
        if any(token in hint for token in ("offered", "plan", "strategy", "how_to", "procedure")):
            return "procedural"
        if any(token in hint for token in ("said", "acknowledged", "meeting", "introduced", "shared")):
            return "episodic"
        return "semantic"

    @staticmethod
    def _coerce_score(value: Any, *, default: float) -> float:
        if isinstance(value, str):
            normalized = value.strip().casefold()
            mapping = {
                "very_high": 0.92,
                "high": 0.82,
                "medium": 0.66,
                "low": 0.45,
                "very_low": 0.25,
            }
            if normalized in mapping:
                return mapping[normalized]
        try:
            return max(0.0, min(float(value), 1.0))
        except (TypeError, ValueError):
            return default

    @staticmethod
    def _default_importance(
        *,
        memory_type: Literal["semantic", "episodic", "relationship", "procedural", "reflection"],
        confidence: float,
    ) -> float:
        base = {
            "semantic": 0.72,
            "episodic": 0.62,
            "relationship": 0.76,
            "procedural": 0.64,
            "reflection": 0.74,
        }[memory_type]
        return max(0.0, min((base + confidence) / 2.0, 1.0))

    @staticmethod
    def _default_sensitivity_from_chunk(
        *,
        chunk: dict[str, Any],
    ) -> Literal["low", "medium", "high"]:
        if chunk.get("risk_flags"):
            return "medium"
        return "low"

    @staticmethod
    def _default_sensitivity_for_fact(
        *,
        predicate_hint: str | None,
        object_hint: str | None,
        claim: str | None,
        chunk: dict[str, Any],
    ) -> Literal["low", "medium", "high"]:
        joined = " ".join(
            part for part in (predicate_hint or "", object_hint or "", claim or "")
            if part
        ).casefold()
        if any(token in joined for token in ("phone", "email", "address", "id card", "身份证")):
            return "high"
        if any(token in joined for token in ("concern", "worried", "doubt", "score", "emotion", "stress")):
            return "medium"
        if chunk.get("risk_flags"):
            return "medium"
        return "low"

    @classmethod
    def _predicate_object_to_claim(
        cls,
        *,
        subject_id: str,
        predicate: str | None,
        object_value: str | None,
    ) -> str | None:
        if not predicate and not object_value:
            return None
        subject_label = "User" if subject_id == "user" else "Contact"
        normalized_predicate = (predicate or "").strip().casefold()
        object_text = object_value or ""
        templates = {
            "introduced_self_as": f"{subject_label} introduced themselves as {object_text}.",
            "shared_preparation_background": f"{subject_label} shared their preparation background and current progress.",
            "target_school": f"{subject_label}'s target school is {object_text}.",
            "exam_type": f"{subject_label} said the exam type is {object_text}.",
            "estimated_score_range": f"{subject_label} estimated their score range as {object_text}.",
            "expressed_concern_about_score": f"{subject_label} expressed concern about {object_text}.",
            "offered_tutoring": f"{subject_label} offered tutoring support.",
            "acknowledged_review": f"{subject_label} said they would review the materials first.",
        }
        if normalized_predicate in templates:
            return templates[normalized_predicate]
        if predicate and object_value:
            predicate_text = predicate.replace("_", " ").strip()
            return f"{subject_label} {predicate_text}: {object_text}"
        if object_value:
            return object_text
        return predicate

    def _load_selected_chunks(
        self,
        *,
        chunks_path: Path,
        limit: int | None,
        sample: int | None,
    ) -> tuple[list[dict[str, Any]], dict[str, Any]]:
        total_lines = 0
        parsed_lines = 0
        failed_lines = 0
        chunks: list[dict[str, Any]] = []
        with chunks_path.open("r", encoding="utf-8") as handle:
            for line_no, raw_line in enumerate(handle, start=1):
                total_lines += 1
                line = raw_line.strip()
                if not line:
                    continue
                try:
                    payload = json.loads(line)
                except json.JSONDecodeError:
                    failed_lines += 1
                    continue
                parsed_lines += 1
                chunks.append(self._coerce_chunk(payload=payload, line_no=line_no))

        selected_chunks = self._apply_sample(chunks=chunks, sample=sample)
        if limit is not None:
            selected_chunks = selected_chunks[:limit]

        selection_report = {
            "total_chunk_lines": total_lines,
            "parsed_chunk_lines": parsed_lines,
            "failed_chunk_lines": failed_lines,
            "available_chunks": len(chunks),
            "selected_chunks": len(selected_chunks),
            "limit": limit,
            "sample": sample,
            "selected_chunk_ids": [chunk["chunk_id"] for chunk in selected_chunks[:20]],
        }
        return selected_chunks, selection_report

    @staticmethod
    def _apply_sample(*, chunks: list[dict[str, Any]], sample: int | None) -> list[dict[str, Any]]:
        if sample is None or sample <= 0 or sample >= len(chunks):
            return list(chunks)
        if sample == 1:
            return [chunks[0]]
        max_index = len(chunks) - 1
        selected_indices = sorted(
            {
                round(index * max_index / (sample - 1))
                for index in range(sample)
            },
        )
        return [chunks[index] for index in selected_indices]

    def _load_events_by_id(
        self,
        *,
        normalized_events_path: Path,
        needed_event_ids: set[str],
    ) -> tuple[dict[str, dict[str, Any]], dict[str, Any]]:
        total_lines = 0
        parsed_lines = 0
        failed_lines = 0
        matched_events = 0
        events_by_id: dict[str, dict[str, Any]] = {}
        with normalized_events_path.open("r", encoding="utf-8") as handle:
            for line_no, raw_line in enumerate(handle, start=1):
                total_lines += 1
                line = raw_line.strip()
                if not line:
                    continue
                try:
                    payload = json.loads(line)
                except json.JSONDecodeError:
                    failed_lines += 1
                    continue
                parsed_lines += 1
                event_id = payload.get("event_id")
                if not isinstance(event_id, str) or event_id not in needed_event_ids:
                    continue
                events_by_id[event_id] = self._coerce_event(payload=payload, line_no=line_no)
                matched_events += 1

        event_scan_report = {
            "total_event_lines": total_lines,
            "parsed_event_lines": parsed_lines,
            "failed_event_lines": failed_lines,
            "needed_event_ids": len(needed_event_ids),
            "matched_events": matched_events,
            "missing_events": max(len(needed_event_ids) - matched_events, 0),
        }
        return events_by_id, event_scan_report

    def _resolve_input_files(self, input_path: Path) -> tuple[Path, Path]:
        resolved_input = self._resolve_existing_path(input_path)
        self._ensure_within_root(
            candidate=resolved_input,
            root=self._private_distilled_root,
            error_message="Input must stay within private/distilled.",
        )

        if resolved_input.is_dir():
            chunks_path = resolved_input / "chunks.jsonl"
            normalized_events_path = resolved_input / "normalized_events.jsonl"
            if chunks_path.is_file() and normalized_events_path.is_file():
                return chunks_path, normalized_events_path

            nested_candidates = sorted(
                path.parent.resolve()
                for path in resolved_input.rglob("chunks.jsonl")
                if path.is_file() and (path.parent / "normalized_events.jsonl").is_file()
            )
            unique_candidates = list(dict.fromkeys(nested_candidates))
            if len(unique_candidates) == 1:
                run_dir = unique_candidates[0]
                return run_dir / "chunks.jsonl", run_dir / "normalized_events.jsonl"
            if not unique_candidates:
                raise ChatlogDistillationError(
                    "Input directory must contain chunks.jsonl and normalized_events.jsonl.",
                    code="input_missing_files",
                )
            raise ChatlogDistillationError(
                "Input directory contains multiple run candidates; pass a specific run directory or chunks.jsonl file.",
                code="input_ambiguous",
            )

        if resolved_input.name != "chunks.jsonl":
            raise ChatlogDistillationError(
                "Input file must be chunks.jsonl.",
                code="input_not_chunks_jsonl",
            )
        normalized_events_path = resolved_input.parent / "normalized_events.jsonl"
        if not normalized_events_path.is_file():
            raise ChatlogDistillationError(
                "chunks.jsonl must live beside normalized_events.jsonl.",
                code="input_missing_files",
            )
        return resolved_input, normalized_events_path

    def _resolve_existing_path(self, path: Path) -> Path:
        resolved = (self._repo_root / path).resolve() if not path.is_absolute() else path.resolve()
        if not resolved.exists():
            raise ChatlogDistillationError(
                f"Input path does not exist: {path}",
                code="input_missing",
            )
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
            raise ChatlogDistillationError(error_message, code="path_outside_private_distilled") from exc

    def _safe_relative_path(self, path: Path) -> str:
        try:
            return str(path.relative_to(self._repo_root)).replace("\\", "/")
        except ValueError:
            return str(path).replace("\\", "/")

    def _write_jsonl(self, *, output_path: Path, records: list[BaseModel]) -> None:
        with output_path.open("w", encoding="utf-8", newline="\n") as handle:
            for record in records:
                handle.write(json.dumps(record.model_dump(mode="json"), ensure_ascii=False))
                handle.write("\n")

    def _write_run_report(self, *, output_dir: Path, distillation_report: dict[str, Any]) -> None:
        report_path = output_dir / "run_report.json"
        merged_report: dict[str, Any] = {}

        if report_path.exists():
            try:
                existing_report = json.loads(report_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                distillation_report["warnings"] = sorted(
                    set(distillation_report["warnings"]) | {"existing_run_report_invalid_json"},
                )
            else:
                if isinstance(existing_report, dict):
                    merged_report = existing_report
                else:
                    distillation_report["warnings"] = sorted(
                        set(distillation_report["warnings"]) | {"existing_run_report_not_object"},
                    )

        merged_report["distillation"] = distillation_report
        existing_output_files = merged_report.get("output_files")
        output_files = list(existing_output_files) if isinstance(existing_output_files, list) else []
        for filename in ("chunk_summaries.jsonl", "memory_facts.jsonl", "run_report.json"):
            if filename not in output_files:
                output_files.append(filename)
        merged_report["output_files"] = output_files

        report_path.write_text(
            json.dumps(merged_report, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    @staticmethod
    def _force_claim_candidate(claim: DistillationClaim) -> DistillationClaim:
        payload = claim.model_dump(mode="json")
        payload["status"] = "candidate"
        return DistillationClaim.model_validate(payload)

    @staticmethod
    def _force_observation_candidate(observation: ChunkSummaryObservation) -> ChunkSummaryObservation:
        payload = observation.model_dump(mode="json")
        payload["status"] = "candidate"
        return ChunkSummaryObservation.model_validate(payload)

    def _render_event_line(self, event: dict[str, Any]) -> str:
        flags = sorted(
            {
                *[flag for flag in event.get("interaction_flags", []) if isinstance(flag, str)],
                *[flag for flag in event.get("risk_flags", []) if isinstance(flag, str)],
            },
        )
        flag_text = f" flags={flags}" if flags else ""
        reply_to_event_id = event.get("reply_to_event_id")
        reply_text = f" reply_to={reply_to_event_id}" if isinstance(reply_to_event_id, str) else ""
        text = self._redact_private_text(event.get("text") if isinstance(event.get("text"), str) else "")
        return (
            f"[{event['event_id']}]"
            f"[{event.get('timestamp') or '-'}]"
            f"[{event.get('sender_role') or 'unknown'}]"
            f"[{event.get('message_type') or 'unknown'}]"
            f"{flag_text}{reply_text} {text}"
        ).strip()

    def _redact_private_text(self, text: str, *, max_length: int = 240) -> str:
        cleaned = " ".join(text.split()).strip()
        if not cleaned:
            return "<empty>"
        redacted = self._EMAIL_PATTERN.sub("[EMAIL]", cleaned)
        redacted = self._PHONE_PATTERN.sub("[PHONE]", redacted)
        redacted = self._URL_PATTERN.sub("[URL]", redacted)
        redacted = self._PATH_PATTERN.sub("[PATH]", redacted)
        redacted = self._DIGIT_RUN_PATTERN.sub("[NUMBER]", redacted)
        redacted = self._ACCOUNT_PATTERN.sub("[ACCOUNT]", redacted)
        if len(redacted) <= max_length:
            return redacted
        return f"{redacted[: max_length - 3].rstrip()}..."

    def _chat_completions_url(self) -> str:
        assert self.base_url is not None
        normalized = self.base_url.rstrip("/")
        if normalized.endswith("/chat/completions"):
            return normalized
        return urljoin(f"{normalized}/", "chat/completions")

    def _post_json(
        self,
        *,
        url: str,
        payload: dict[str, Any],
        headers: dict[str, str],
    ) -> dict[str, Any]:
        request = Request(
            url=url,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST",
        )
        try:
            with urlopen(request, timeout=self.timeout_seconds) as response:
                return json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            raise ChatlogDistillationError(
                f"Remote provider returned HTTP {exc.code}.",
                code=f"remote_http_{exc.code}",
            ) from exc
        except URLError as exc:
            raise ChatlogDistillationError(
                f"Remote provider request failed: {exc.reason}.",
                code="remote_request_failed",
            ) from exc

    @staticmethod
    def _extract_message_content(*, response: dict[str, Any]) -> str:
        choices = response.get("choices")
        if isinstance(choices, list) and choices:
            first = choices[0]
            if isinstance(first, dict):
                message = first.get("message")
                if isinstance(message, dict):
                    content = message.get("content")
                    if isinstance(content, str):
                        return content.strip()
                    if isinstance(content, list):
                        text_parts: list[str] = []
                        for item in content:
                            if isinstance(item, str):
                                text_parts.append(item)
                                continue
                            if isinstance(item, dict):
                                text = item.get("text")
                                if isinstance(text, str):
                                    text_parts.append(text)
                        joined = "\n".join(part for part in text_parts if part.strip()).strip()
                        if joined:
                            return joined
        raise ChatlogDistillationError(
            "Remote response did not contain chat message content.",
            code="response_missing_content",
        )

    @staticmethod
    def _parse_json_content(*, content: str) -> dict[str, Any]:
        cleaned = content.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.strip("`")
            if cleaned.startswith("json"):
                cleaned = cleaned[4:].strip()
        try:
            parsed = json.loads(cleaned)
            if isinstance(parsed, dict):
                return parsed
        except json.JSONDecodeError:
            pass

        start = cleaned.find("{")
        end = cleaned.rfind("}")
        if start >= 0 and end > start:
            try:
                parsed = json.loads(cleaned[start : end + 1])
            except json.JSONDecodeError as exc:
                raise ChatlogDistillationError(
                    "Remote response was not valid JSON.",
                    code="response_invalid_json",
                ) from exc
            if isinstance(parsed, dict):
                return parsed
        raise ChatlogDistillationError(
            "Remote response was not valid JSON.",
            code="response_invalid_json",
        )

    @staticmethod
    def _clean_string(value: Any) -> str | None:
        if not isinstance(value, str):
            return None
        cleaned = " ".join(value.split()).strip()
        return cleaned or None

    @classmethod
    def _clean_string_list(cls, values: Any, *, max_items: int) -> list[str]:
        if not isinstance(values, list):
            return []
        kept: list[str] = []
        seen: set[str] = set()
        for value in values:
            cleaned = cls._clean_string(value)
            if not cleaned:
                continue
            normalized = cleaned.casefold()
            if normalized in seen:
                continue
            seen.add(normalized)
            kept.append(cleaned)
            if len(kept) >= max_items:
                break
        return kept

    def _coerce_chunk(self, *, payload: dict[str, Any], line_no: int) -> dict[str, Any]:
        required_string_fields = ("chunk_id", "contact_id", "conversation_id", "chunking_reason")
        for field_name in required_string_fields:
            value = payload.get(field_name)
            if not isinstance(value, str) or not value:
                raise ChatlogDistillationError(
                    f"Chunk line {line_no} is missing {field_name}.",
                    code="invalid_chunk_shape",
                )
        event_ids = payload.get("event_ids")
        if not isinstance(event_ids, list) or not event_ids:
            raise ChatlogDistillationError(
                f"Chunk line {line_no} is missing event_ids.",
                code="invalid_chunk_shape",
            )
        return {
            "chunk_id": payload["chunk_id"],
            "contact_id": payload["contact_id"],
            "conversation_id": payload["conversation_id"],
            "event_ids": [event_id for event_id in event_ids if isinstance(event_id, str)],
            "time_range": list(payload.get("time_range", [])) if isinstance(payload.get("time_range"), list) else [],
            "message_count": int(payload.get("message_count", 0)) if isinstance(payload.get("message_count"), int) else 0,
            "chunking_reason": payload["chunking_reason"],
            "source_message_type_codes": [
                code for code in payload.get("source_message_type_codes", []) if isinstance(code, int)
            ],
            "interaction_flags": [
                flag for flag in payload.get("interaction_flags", []) if isinstance(flag, str)
            ],
            "risk_flags": [
                flag for flag in payload.get("risk_flags", []) if isinstance(flag, str)
            ],
        }

    def _coerce_event(self, *, payload: dict[str, Any], line_no: int) -> dict[str, Any]:
        event_id = payload.get("event_id")
        if not isinstance(event_id, str) or not event_id:
            raise ChatlogDistillationError(
                f"Normalized event line {line_no} is missing event_id.",
                code="invalid_event_shape",
            )
        return {
            "event_id": event_id,
            "timestamp": payload.get("timestamp") if isinstance(payload.get("timestamp"), str) else None,
            "sender_role": payload.get("sender_role") if isinstance(payload.get("sender_role"), str) else "unknown",
            "message_type": payload.get("message_type") if isinstance(payload.get("message_type"), str) else "unknown",
            "text": payload.get("text") if isinstance(payload.get("text"), str) else "",
            "interaction_flags": [
                flag for flag in payload.get("interaction_flags", []) if isinstance(flag, str)
            ],
            "risk_flags": [flag for flag in payload.get("risk_flags", []) if isinstance(flag, str)],
            "reply_to_event_id": (
                payload.get("reply_to_event_id")
                if isinstance(payload.get("reply_to_event_id"), str)
                else None
            ),
        }
