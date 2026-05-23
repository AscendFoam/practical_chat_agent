from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from urllib.request import Request, urlopen

from practical_chat_agent.core.models import (
    ChatContext,
    LLMGenerationMetadata,
    LLMReplyPlan,
    LLMReplyPlanCandidate,
    LLMReplyPlanRefusal,
    ReplyPlanContextRef,
)
from practical_chat_agent.services.reply_candidate_validator import (
    check_boundary_reminders,
    check_input_size,
    check_ref_types,
    check_supporting_refs,
    check_text_non_empty,
    has_impersonation,
    has_privacy_leak,
    normalize_ranks,
)


class LLMReplyGeneratorError(ValueError):
    """Raised when LLM generator encounters a non-recoverable error."""


class LLMReplyPlanValidator:
    """Deterministic post-generation validator for LLM-generated reply plans.

    Implements the validation checks defined in Section 7 of the
    LLM Candidate Generator Contract.  Validation is stateless and
    per-candidate: invalid candidates are excluded silently, and only
    the validated subset is returned.

    Core validation logic is delegated to
    ``practical_chat_agent.services.reply_candidate_validator`` for
    reuse across template and LLM-generated candidate paths.
    """

    @classmethod
    def validate(
        cls,
        *,
        plan: LLMReplyPlan,
        context_texts: list[str] | None = None,
    ) -> LLMReplyPlan:
        """Validate and return a cleaned plan containing only valid candidates.

        Invalid candidates are excluded silently.  Ranks are re-assigned to
        a contiguous 1..N sequence after filtering.
        """
        valid_candidates: list[LLMReplyPlanCandidate] = []
        for candidate in plan.candidates:
            if cls._candidate_is_valid(
                candidate=candidate,
                context_texts=context_texts,
            ):
                valid_candidates.append(candidate)

        validated = plan.model_copy(deep=True)
        validated.candidates = valid_candidates
        normalize_ranks(validated.candidates)
        return validated

    @classmethod
    def _candidate_is_valid(
        cls,
        *,
        candidate: LLMReplyPlanCandidate,
        context_texts: list[str] | None,
    ) -> bool:
        if not check_text_non_empty(candidate.draft_text):
            return False
        if not check_supporting_refs(candidate.supporting_context_refs):
            return False
        if not check_boundary_reminders(candidate.boundary_reminders):
            return False
        if not check_ref_types(candidate.supporting_context_refs):
            return False
        if candidate.generator_type != "llm_generated":
            return False
        if context_texts and has_privacy_leak(
            draft_text=candidate.draft_text,
            context_texts=context_texts,
        ):
            return False
        if has_impersonation(candidate.draft_text):
            return False
        return True


class LLMReplyGeneratorService:
    """Offline LLM candidate generator that consumes safe ChatContext.

    This service is opt-in and additive.  It does not modify any
    runtime state, does not write to approved stores, and does not
    alter the existing deterministic ReplyPlanner path.
    """

    backend_name = "llm_reply_generator"

    def __init__(
        self,
        *,
        api_key: str | None,
        base_url: str | None,
        model: str | None,
        timeout_seconds: float = 45.0,
        enabled: bool = True,
        default_model: str = "deepseek-chat",
        max_input_chars: int = 20_000,
    ) -> None:
        self.api_key = (api_key or "").strip() or None
        self.base_url = (base_url or "").strip() or None
        self.model = (model or "").strip() or None
        self.timeout_seconds = max(float(timeout_seconds), 3.0)
        self.enabled = enabled
        self.default_model = default_model
        self.max_input_chars = max_input_chars
        self._prompt_template_hash = self._compute_prompt_hash()

    @property
    def resolved_model(self) -> str:
        return self.model or self.default_model

    def availability_reason(self) -> str | None:
        if not self.enabled:
            return "LLM reply generator is disabled"
        if not self.api_key:
            return "OPENAI_API_KEY is not configured"
        if not self.base_url:
            return "OPENAI_BASE_URL is not configured"
        return None

    def generate(
        self,
        *,
        context: ChatContext,
    ) -> LLMReplyPlan:
        """Generate an LLMReplyPlan from a safe ChatContext.

        Returns either a plan with validated candidates or a structured
        refusal.  Never raises for provider errors — those are captured
        as refusals instead.
        """
        contact_id = context.user_id.strip() or None

        # --- availability check ---
        reason = self.availability_reason()
        if reason is not None:
            return self._refusal(
                contact_id=contact_id,
                code="PROVIDER_ERROR",
                reason=reason,
                retryable=False,
            )

        # --- build safe input ---
        llm_input = self._build_llm_input(context=context)
        if llm_input is None:
            return self._refusal(
                contact_id=contact_id,
                code="MISSING_REQUIRED_CONTEXT",
                reason="ChatContext is empty or missing required contact id.",
                retryable=False,
            )

        context_texts = self._collect_context_texts(context=context)

        # --- input size preflight ---
        system_prompt = self._build_system_prompt()
        input_json = json.dumps(llm_input, ensure_ascii=False)
        estimated_size = len(system_prompt) + len(input_json)
        if not check_input_size(estimated_size, max_chars=self.max_input_chars):
            return self._refusal(
                contact_id=contact_id,
                code="INPUT_TOO_LARGE",
                reason=(
                    f"Estimated input size ({estimated_size} chars) exceeds "
                    f"limit ({self.max_input_chars})."
                ),
                retryable=False,
            )

        # --- call provider ---
        start = datetime.now(timezone.utc)
        try:
            response = self._call_provider(llm_input_data=llm_input)
        except LLMReplyGeneratorError as exc:
            return self._refusal(
                contact_id=contact_id,
                code="PROVIDER_ERROR",
                reason=str(exc),
                retryable=True,
            )
        latency_ms = int((datetime.now(timezone.utc) - start).total_seconds() * 1000)

        # --- parse + normalize ---
        try:
            raw_candidates = self._parse_provider_response(response=response)
        except LLMReplyGeneratorError as exc:
            return self._refusal(
                contact_id=contact_id,
                code="INVALID_OUTPUT_SCHEMA",
                reason=str(exc),
                retryable=True,
            )

        # --- build candidates ---
        candidates = self._build_candidates(raw_candidates=raw_candidates)

        # --- deterministic validation ---
        source_snapshot = self._build_source_snapshot(context=context)
        metadata = self._build_metadata(
            latency_ms=latency_ms,
        )
        plan = LLMReplyPlan(
            contact_id=contact_id,
            source_context_snapshot=source_snapshot,
            generation_metadata=metadata,
            candidates=candidates,
        )
        validated = LLMReplyPlanValidator.validate(
            plan=plan,
            context_texts=context_texts,
        )

        return validated

    def _build_llm_input(self, *, context: ChatContext) -> dict[str, Any] | None:
        contact_id = context.user_id.strip() if context.user_id else ""
        if not contact_id:
            return None

        approved = context.approved_store_context
        skill_brief = approved.contact_skill
        derived = context.derived_brief_context
        patches = context.approved_patch_context

        compact: dict[str, Any] = {
            "contact_id": contact_id,
            "contact_name": context.user_name or contact_id,
            "relationship_mode": context.relationship_mode,
            "latest_message_text": context.latest_message_text or "",
        }

        if skill_brief is not None:
            compact["relationship_summary"] = skill_brief.relationship_summary
            if skill_brief.strategy_hints:
                compact["strategy_hints"] = skill_brief.strategy_hints[:3]
            if skill_brief.boundary_reminders:
                compact["boundary_reminders"] = skill_brief.boundary_reminders[:3]

        if approved.memory_facts:
            compact["approved_memory_claims"] = [
                m.claim for m in approved.memory_facts[:4]
            ]

        if derived.status == "loaded":
            if derived.persona is not None:
                compact["persona_summary"] = derived.persona.relationship_state_summary
            if derived.boundary is not None:
                compact["boundary_sensitivity"] = derived.boundary.sensitivity_summary

        if patches.status == "loaded" and patches.patches:
            compact["approved_patch_hints"] = [
                f"[{p.patch_type}] {p.compact_instruction}"
                for p in patches.patches[:3]
            ]

        compact["recent_event_count"] = len(context.recent_events)
        compact["memory_hit_count"] = len(context.memory_hits)

        return compact

    @staticmethod
    def _collect_context_texts(*, context: ChatContext) -> list[str]:
        texts: list[str] = []
        if context.latest_message_text:
            texts.append(context.latest_message_text)
        for event in context.recent_events[:8]:
            if event.text:
                texts.append(event.text)
        for memory in context.memory_hits[:8]:
            if memory.fact:
                texts.append(memory.fact)
        if context.summary:
            texts.append(context.summary)
        for mf in context.approved_store_context.memory_facts[:4]:
            texts.append(mf.claim)
        return texts

    def _call_provider(self, *, llm_input_data: dict[str, Any]) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "model": self.resolved_model,
            "temperature": 0.7,
            "messages": [
                {"role": "system", "content": self._build_system_prompt()},
                {"role": "user", "content": json.dumps(llm_input_data, ensure_ascii=False)},
            ],
        }

        url = self._chat_completions_url()
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        return self._post_json(url=url, payload=payload, headers=headers)

    @staticmethod
    def _build_system_prompt() -> str:
        return (
            "You are a reply draft generator for a social chat agent.\n"
            "You will receive compact chat context as a JSON object.\n"
            "Generate 2-3 candidate reply drafts based on the provided context.\n"
            "Rules:\n"
            "1. Do NOT impersonate the contact. All drafts are from the user's perspective.\n"
            "2. Use only the provided context — do not invent relationship details.\n"
            "3. Keep wording natural, low-pressure, and review-friendly.\n"
            "4. When context is thin or sensitive, prefer conservative drafts.\n"
            "5. No markdown formatting in draft_text. Plain text only.\n"
            "Return a JSON object with a 'candidates' array. "
            "Each candidate has: approach_label, draft_text, rationale, "
            "boundary_reminders (array of strings), risk_flags (array of strings), "
            "confidence (0.0-1.0). "
            "Return valid JSON only."
        )

    @staticmethod
    def _parse_provider_response(*, response: dict[str, Any]) -> list[dict[str, Any]]:
        choices = response.get("choices")
        if not isinstance(choices, list) or not choices:
            raise LLMReplyGeneratorError("Provider response has no choices.")
        first = choices[0]
        if not isinstance(first, dict):
            raise LLMReplyGeneratorError("Provider choice is not a dict.")
        message = first.get("message")
        if not isinstance(message, dict):
            raise LLMReplyGeneratorError("Provider message is missing.")
        content = message.get("content")
        if not isinstance(content, str) or not content.strip():
            raise LLMReplyGeneratorError("Provider message content is empty.")

        cleaned = content.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.strip("`")
            if cleaned.startswith("json"):
                cleaned = cleaned[4:].strip()

        try:
            parsed = json.loads(cleaned)
        except json.JSONDecodeError as exc:
            raise LLMReplyGeneratorError(
                f"Provider response is not valid JSON: {exc}",
            ) from exc

        if not isinstance(parsed, dict):
            raise LLMReplyGeneratorError("Provider response is not a JSON object.")

        raw_candidates = parsed.get("candidates")
        if isinstance(raw_candidates, list):
            return raw_candidates

        return []

    def _build_candidates(
        self,
        *,
        raw_candidates: list[dict[str, Any]],
    ) -> list[LLMReplyPlanCandidate]:
        candidates: list[LLMReplyPlanCandidate] = []
        for idx, raw in enumerate(raw_candidates, start=1):
            if not isinstance(raw, dict):
                continue
            draft_text = (raw.get("draft_text") or "").strip()
            if not draft_text:
                continue
            rationale = (raw.get("rationale") or "").strip()
            approach_label = (raw.get("approach_label") or "").strip() or "llm_generated"

            supporting_refs = self._build_default_refs()
            boundary_reminders = raw.get("boundary_reminders")
            if not isinstance(boundary_reminders, list) or not boundary_reminders:
                boundary_reminders = ["Drafts are for human review only."]
            else:
                boundary_reminders = [str(r) for r in boundary_reminders if r]

            risk_flags_raw = raw.get("risk_flags")
            risk_flags: list[str] = (
                [str(r) for r in risk_flags_raw if r]
                if isinstance(risk_flags_raw, list)
                else []
            )

            confidence: float | None = None
            raw_conf = raw.get("confidence")
            if isinstance(raw_conf, (int, float)) and 0.0 <= raw_conf <= 1.0:
                confidence = float(raw_conf)

            try:
                candidate = LLMReplyPlanCandidate(
                    approach_label=approach_label,
                    priority_rank=idx,
                    draft_text=draft_text,
                    rationale=rationale,
                    supporting_context_refs=supporting_refs,
                    risk_flags=risk_flags,
                    boundary_reminders=boundary_reminders,
                    confidence=confidence,
                )
            except Exception:
                continue
            candidates.append(candidate)
        return candidates

    @staticmethod
    def _build_default_refs() -> list[ReplyPlanContextRef]:
        return [
            ReplyPlanContextRef(
                ref_type="policy_boundary",
                ref_id="boundary_review_only",
                note="Drafts are for human review only.",
            ),
        ]

    def _build_source_snapshot(self, *, context: ChatContext) -> dict[str, Any]:
        approved = context.approved_store_context
        skill = approved.contact_skill
        return {
            "approved_store_status": approved.status,
            "approved_contact_skill_record_id": skill.record_id if skill is not None else None,
            "approved_memory_record_ids": [m.record_id for m in approved.memory_facts[:4]],
            "recent_event_count": len(context.recent_events),
        }

    def _build_metadata(self, *, latency_ms: int) -> LLMGenerationMetadata:
        return LLMGenerationMetadata(
            provider=str(self.base_url or "unknown"),
            model=self.resolved_model,
            temperature=0.7,
            prompt_template_hash=self._prompt_template_hash,
            generated_at=datetime.now(timezone.utc),
            latency_ms=latency_ms,
        )

    def _refusal(
        self,
        *,
        contact_id: str | None,
        code: str,
        reason: str,
        retryable: bool,
    ) -> LLMReplyPlan:
        metadata = LLMGenerationMetadata(
            provider=str(self.base_url or "unknown") if self.base_url else "unknown",
            model=self.resolved_model,
            temperature=0.7,
            prompt_template_hash=self._prompt_template_hash,
            generated_at=datetime.now(timezone.utc),
            latency_ms=None,
        )
        return LLMReplyPlan(
            contact_id=contact_id,
            source_context_snapshot={},
            generation_metadata=metadata,
            candidates=[],
            refusal=LLMReplyPlanRefusal(
                refusal_code=code,  # type: ignore[arg-type]
                refusal_reason=reason,
                is_retryable=retryable,
            ),
        )

    def _chat_completions_url(self) -> str:
        base = (self.base_url or "").rstrip("/") + "/"
        return urljoin(base, "chat/completions")

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
            raise LLMReplyGeneratorError(
                f"Provider returned HTTP {exc.code}: {exc.reason}",
            ) from exc
        except URLError as exc:
            raise LLMReplyGeneratorError(
                f"Provider request failed: {exc.reason}",
            ) from exc
        except OSError as exc:
            raise LLMReplyGeneratorError(
                f"Provider communication error: {exc}",
            ) from exc

    @staticmethod
    def _compute_prompt_hash() -> str:
        text = LLMReplyGeneratorService._build_system_prompt()
        return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]
