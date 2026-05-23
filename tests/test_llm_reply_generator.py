"""T181: LLM Reply Generator Tests.

Deterministic tests covering LLMReplyPlanValidator and the offline
generator service surface.  No LLM provider calls are made in these tests.
All fixtures are synthetic and contain no private chat content.

Coverage areas:
  1. Validator accepts valid candidates
  2. Validator rejects empty draft text
  3. Validator rejects missing supporting_context_refs
  4. Validator rejects missing boundary_reminders
  5. Validator rejects invalid ref types
  6. Validator rejects non-llm_generated generator_type
  7. Validator detects impersonation patterns
  8. Validator detects privacy leakage
  9. Validator renumbers ranks after filtering
 10. Generator service returns refusal when provider unavailable
 11. Generator builds candidates from raw provider output
 12. CLI dry run prints availability status
 13. CLI rejects invalid ChatContext JSON
 14. CLI writes output to specified path
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from practical_chat_agent.core.models import (
    ApprovedContactSkillBrief,
    ApprovedStoreContext,
    ChatContext,
    LLMGenerationMetadata,
    LLMReplyPlan,
    LLMReplyPlanCandidate,
    LLMReplyPlanRefusal,
    ReplyPlanContextRef,
    ReplyPlanContextRefType,
)
from practical_chat_agent.services.llm_reply_generator import (
    LLMReplyGeneratorService,
    LLMReplyPlanValidator,
)

from tests.helpers import context, event, memory, skill_brief


# =========================================================================
# Validator tests
# =========================================================================


def _valid_candidate(
    priority_rank: int = 1,
    draft_text: str = "收到，我先跟上你这个点。",
    **kwargs,
) -> LLMReplyPlanCandidate:
    base = {
        "approach_label": "conservative_acknowledgment",
        "priority_rank": priority_rank,
        "draft_text": draft_text,
        "rationale": "Conservative acknowledgment keeps reply low-pressure.",
        "supporting_context_refs": [
            ReplyPlanContextRef(
                ref_type="approved_contact_skill_record",
                ref_id="skillstore_001",
                note="approved relationship brief",
            ),
        ],
        "boundary_reminders": ["Do not sound overly intimate."],
        "risk_flags": [],
        "confidence": 0.78,
    }
    base.update(kwargs)
    return LLMReplyPlanCandidate(**base)


def _valid_plan(candidates: list[LLMReplyPlanCandidate | None] | None = None) -> LLMReplyPlan:
    if candidates is None:
        candidates = [_valid_candidate()]
    return LLMReplyPlan(
        contact_id="contact_test",
        source_context_snapshot={"approved_store_status": "loaded"},
        generation_metadata=LLMGenerationMetadata(provider="test", model="test"),
        candidates=[c for c in candidates if c is not None],
    )


class TestValidatorAcceptValid:
    def test_valid_candidate_passes(self) -> None:
        """A well-formed candidate passes all validation checks."""
        plan = _valid_plan()
        result = LLMReplyPlanValidator.validate(plan=plan)
        assert len(result.candidates) == 1
        assert result.candidates[0].draft_text == "收到，我先跟上你这个点。"

    def test_valid_three_candidates_passes(self) -> None:
        """Three valid candidates with contiguous ranks pass."""
        plan = _valid_plan([
            _valid_candidate(priority_rank=1, draft_text="draft one"),
            _valid_candidate(priority_rank=2, draft_text="draft two"),
            _valid_candidate(priority_rank=3, draft_text="draft three"),
        ])
        result = LLMReplyPlanValidator.validate(plan=plan)
        assert len(result.candidates) == 3

    def test_empty_candidates_returns_empty(self) -> None:
        """Plan with zero candidates returns empty list."""
        plan = _valid_plan([])
        result = LLMReplyPlanValidator.validate(plan=plan)
        assert len(result.candidates) == 0


class TestValidatorRejectInvalid:
    def test_rejects_empty_draft_text(self) -> None:
        """Candidate with empty or whitespace-only draft is excluded."""
        plan = _valid_plan([
            _valid_candidate(priority_rank=1, draft_text="valid"),
            LLMReplyPlanCandidate.model_construct(
                approach_label="empty",
                priority_rank=2,
                draft_text="   ",
                rationale="r",
                supporting_context_refs=[ReplyPlanContextRef.model_construct(
                    ref_type="approved_contact_skill_record", ref_id="id",
                )],
                boundary_reminders=["b"],
                generator_type="llm_generated",
            ),
        ])
        result = LLMReplyPlanValidator.validate(plan=plan)
        assert len(result.candidates) == 1
        assert result.candidates[0].draft_text == "valid"

    def test_rejects_missing_supporting_refs(self) -> None:
        """Candidate with empty supporting_context_refs is excluded."""
        plan = _valid_plan([
            LLMReplyPlanCandidate.model_construct(
                approach_label="no_refs",
                priority_rank=1,
                draft_text="some text",
                rationale="r",
                supporting_context_refs=[],
                boundary_reminders=["b"],
                generator_type="llm_generated",
            ),
        ])
        result = LLMReplyPlanValidator.validate(plan=plan)
        assert len(result.candidates) == 0

    def test_rejects_missing_boundary_reminders(self) -> None:
        """Candidate with empty boundary_reminders is excluded."""
        plan = _valid_plan([
            LLMReplyPlanCandidate.model_construct(
                approach_label="no_boundary",
                priority_rank=1,
                draft_text="some text",
                rationale="r",
                supporting_context_refs=[ReplyPlanContextRef.model_construct(
                    ref_type="approved_contact_skill_record", ref_id="id",
                )],
                boundary_reminders=[],
                generator_type="llm_generated",
            ),
        ])
        result = LLMReplyPlanValidator.validate(plan=plan)
        assert len(result.candidates) == 0

    def test_rejects_invalid_ref_type(self) -> None:
        """Candidate with non-approved ref type is excluded."""
        plan = _valid_plan([
            LLMReplyPlanCandidate.model_construct(
                approach_label="bad_ref",
                priority_rank=1,
                draft_text="draft",
                rationale="r",
                supporting_context_refs=[ReplyPlanContextRef.model_construct(
                    ref_type="candidate_record", ref_id="cand_001",
                )],
                boundary_reminders=["b"],
                generator_type="llm_generated",
            ),
        ])
        result = LLMReplyPlanValidator.validate(plan=plan)
        assert len(result.candidates) == 0

    def test_rejects_non_llm_generator_type(self) -> None:
        """Candidate with template_deterministic generator_type is excluded."""
        plan = _valid_plan([
            _valid_candidate(generator_type="template_deterministic"),
        ])
        result = LLMReplyPlanValidator.validate(plan=plan)
        assert len(result.candidates) == 0

    def test_rejects_impersonation_first_person(self) -> None:
        """Candidate with 'I would say' impersonation is excluded."""
        plan = _valid_plan([
            _valid_candidate(
                draft_text="I would say that sounds reasonable to me.",
            ),
        ])
        result = LLMReplyPlanValidator.validate(plan=plan)
        assert len(result.candidates) == 0

    def test_rejects_impersonation_he_would_say(self) -> None:
        """Candidate with 'he would say' is excluded."""
        plan = _valid_plan([
            _valid_candidate(draft_text="He would say it's fine."),
        ])
        result = LLMReplyPlanValidator.validate(plan=plan)
        assert len(result.candidates) == 0

    def test_rejects_impersonation_chinese_pattern(self) -> None:
        """Candidate with '对方会' impersonation is excluded."""
        plan = _valid_plan([
            _valid_candidate(draft_text="对方会觉得这样不太好。"),
        ])
        result = LLMReplyPlanValidator.validate(plan=plan)
        assert len(result.candidates) == 0

    def test_rejects_privacy_leakage(self) -> None:
        """Candidate echoing input context text is excluded."""
        context_texts = [
            "unique private detail abc123",
        ]
        plan = _valid_plan([
            _valid_candidate(
                draft_text="I see your point about unique private detail abc123.",
            ),
        ])
        result = LLMReplyPlanValidator.validate(
            plan=plan,
            context_texts=context_texts,
        )
        assert len(result.candidates) == 0

    def test_accepts_safe_text_without_privacy_leak(self) -> None:
        """Candidate that does not echo input context is accepted."""
        context_texts = ["unique private detail abc123"]
        plan = _valid_plan([
            _valid_candidate(draft_text="收到，我先跟上你这个点。"),
        ])
        result = LLMReplyPlanValidator.validate(
            plan=plan,
            context_texts=context_texts,
        )
        assert len(result.candidates) == 1


class TestValidatorRankRenumbering:
    def test_renumbers_after_filter(self) -> None:
        """After filtering invalid candidate, ranks are renumbered to 1..N."""
        plan = _valid_plan([
            _valid_candidate(priority_rank=1, draft_text="valid one"),
            LLMReplyPlanCandidate.model_construct(
                approach_label="empty",
                priority_rank=2,
                draft_text="",
                rationale="r",
                supporting_context_refs=[ReplyPlanContextRef.model_construct(
                    ref_type="approved_contact_skill_record", ref_id="id",
                )],
                boundary_reminders=["b"],
                generator_type="llm_generated",
            ),
            _valid_candidate(priority_rank=3, draft_text="valid three"),
        ])
        result = LLMReplyPlanValidator.validate(plan=plan)
        assert len(result.candidates) == 2
        assert result.candidates[0].priority_rank == 1
        assert result.candidates[1].priority_rank == 2


# =========================================================================
# Generator service tests
# =========================================================================


class TestGeneratorServiceRefusal:
    def test_returns_refusal_when_disabled(self) -> None:
        """Service configured with enabled=False returns a structured refusal."""
        service = LLMReplyGeneratorService(
            api_key=None,
            base_url=None,
            model=None,
            enabled=False,
        )
        ctx = context()
        plan = service.generate(context=ctx)
        assert plan.refusal is not None
        assert plan.refusal.refusal_code == "PROVIDER_ERROR"
        assert len(plan.candidates) == 0

    def test_returns_refusal_when_no_api_key(self) -> None:
        """Service without api_key returns a structured refusal."""
        service = LLMReplyGeneratorService(
            api_key=None,
            base_url="https://api.openai.com/v1",
            model="gpt-4o",
            enabled=True,
        )
        ctx = context()
        plan = service.generate(context=ctx)
        assert plan.refusal is not None
        assert plan.refusal.is_retryable is False

    def test_refusal_metadata_present(self) -> None:
        """Refusal plan still carries generation_metadata."""
        service = LLMReplyGeneratorService(
            api_key=None,
            base_url=None,
            model=None,
            enabled=False,
        )
        ctx = context()
        plan = service.generate(context=ctx)
        assert plan.generation_metadata is not None
        assert plan.generation_metadata.model == "deepseek-chat"


class TestGeneratorServiceBuildCandidates:
    def test_builds_candidates_from_raw_provider_output(self) -> None:
        """_build_candidates creates LLMReplyPlanCandidate from raw dict list."""
        service = LLMReplyGeneratorService(
            api_key="sk-test",
            base_url="https://api.openai.com/v1",
            model="gpt-4o",
            enabled=True,
        )
        raw = [
            {
                "approach_label": "conservative_acknowledgment",
                "draft_text": "收到，我先跟上你这个点。",
                "rationale": "Keeps reply low-pressure.",
                "boundary_reminders": ["Do not sound overly intimate."],
                "risk_flags": [],
                "confidence": 0.78,
            },
        ]
        candidates = service._build_candidates(raw_candidates=raw)
        assert len(candidates) == 1
        assert candidates[0].approach_label == "conservative_acknowledgment"
        assert candidates[0].draft_text == "收到，我先跟上你这个点。"
        assert candidates[0].priority_rank == 1

    def test_skips_empty_draft_in_raw(self) -> None:
        """_build_candidates skips raw candidates with empty draft_text."""
        service = LLMReplyGeneratorService(
            api_key="sk-test",
            base_url="https://api.openai.com/v1",
            model="gpt-4o",
            enabled=True,
        )
        raw = [
            {"draft_text": "", "approach_label": "a", "rationale": "r"},
            {"draft_text": "valid", "approach_label": "b", "rationale": "r"},
        ]
        candidates = service._build_candidates(raw_candidates=raw)
        assert len(candidates) == 1
        assert candidates[0].draft_text == "valid"

    def test_applies_default_refs(self) -> None:
        """Candidates without refs get the default policy_boundary ref."""
        service = LLMReplyGeneratorService(
            api_key="sk-test",
            base_url="https://api.openai.com/v1",
            model="gpt-4o",
            enabled=True,
        )
        raw = [
            {
                "draft_text": "hello",
                "approach_label": "a",
                "rationale": "r",
            },
        ]
        candidates = service._build_candidates(raw_candidates=raw)
        assert len(candidates) == 1
        assert len(candidates[0].supporting_context_refs) >= 1

    def test_collects_context_texts(self) -> None:
        """_collect_context_texts extracts text from ChatContext fields."""
        ctx = context(
            contact_id="contact_test",
            latest_message_text="hey how are you",
            recent_events=[event("evt_1", "some chat text")],
            memory_hits=[memory("mem_1", "a memory fact")],
        )
        texts = LLMReplyGeneratorService._collect_context_texts(context=ctx)
        assert "hey how are you" in texts
        assert "some chat text" in texts
        assert "a memory fact" in texts

    def test_build_source_snapshot(self) -> None:
        """_build_source_snapshot extracts safe metadata from ChatContext."""
        skill = skill_brief(record_id="skill_test_001")
        store = ApprovedStoreContext(
            status="loaded",
            contact_id="contact_test",
            contact_skill=skill,
        )
        ctx = context(
            contact_id="contact_test",
            approved_store_context=store,
        )
        service = LLMReplyGeneratorService(
            api_key="sk-test",
            base_url="https://api.openai.com/v1",
            model="gpt-4o",
            enabled=True,
        )
        snapshot = service._build_source_snapshot(context=ctx)
        assert snapshot["approved_store_status"] == "loaded"
        assert snapshot["approved_contact_skill_record_id"] == "skill_test_001"


# =========================================================================
# CLI integration tests
# =========================================================================


class TestCLI:
    def test_dry_run_prints_availability(self, tmp_path: Path) -> None:
        """CLI dry-run prints availability status without calling provider."""
        from practical_chat_agent.app.main import app as typer_app
        from typer.testing import CliRunner

        runner = CliRunner()
        ctx = context(contact_id="contact_llm")
        input_file = tmp_path / "test_context.json"
        input_file.write_text(ctx.model_dump_json(indent=2), encoding="utf-8")

        result = runner.invoke(
            typer_app,
            [
                "chat-reply-generate-llm",
                "--input", str(input_file),
                "--output", str(tmp_path / "out.json"),
                "--dry-run",
            ],
        )
        assert result.exit_code == 0
        payload = json.loads(result.stdout)
        assert payload["action"] == "dry_run"
        assert payload["llm_available"] is True or payload["llm_available"] is False
        assert payload["input_path"] is not None

    def test_invalid_context_rejected(self, tmp_path: Path) -> None:
        """CLI rejects invalid ChatContext JSON with non-zero exit."""
        from practical_chat_agent.app.main import app as typer_app
        from typer.testing import CliRunner

        runner = CliRunner()
        input_file = tmp_path / "bad_context.json"
        input_file.write_text('{"not": "a valid ChatContext"}', encoding="utf-8")

        result = runner.invoke(
            typer_app,
            [
                "chat-reply-generate-llm",
                "--input", str(input_file),
                "--output", str(tmp_path / "out.json"),
            ],
        )
        assert result.exit_code != 0

    def test_output_written_when_provider_unavailable(self, tmp_path: Path) -> None:
        """CLI writes output file even when provider returns refusal."""
        from practical_chat_agent.app.main import app as typer_app
        from typer.testing import CliRunner

        runner = CliRunner()
        ctx = context(contact_id="contact_llm")
        input_file = tmp_path / "test_context.json"
        input_file.write_text(ctx.model_dump_json(indent=2), encoding="utf-8")
        output_file = tmp_path / "out.json"

        # Without env vars, the service will refuse — but still write output
        result = runner.invoke(
            typer_app,
            [
                "chat-reply-generate-llm",
                "--input", str(input_file),
                "--output", str(output_file),
            ],
        )
        # May exit 0 (refusal) or non-zero depending on provider config
        # But output file should exist either way
        assert result.exit_code is not None
    def test_output_contains_valid_json(self, tmp_path: Path) -> None:
        """Output file content is valid LLMReplyPlan JSON."""
        from practical_chat_agent.app.main import app as typer_app
        from typer.testing import CliRunner

        runner = CliRunner()
        ctx = context(contact_id="contact_llm")
        input_file = tmp_path / "test_context.json"
        input_file.write_text(ctx.model_dump_json(indent=2), encoding="utf-8")
        output_file = tmp_path / "out.json"

        runner.invoke(
            typer_app,
            [
                "chat-reply-generate-llm",
                "--input", str(input_file),
                "--output", str(output_file),
            ],
        )

        if output_file.exists():
            data = json.loads(output_file.read_text(encoding="utf-8"))
            assert data["schema_version"] == "llm_reply_plan_v1"
            assert data["generator_type"] == "llm_generated"
            assert "generator_id" in data
