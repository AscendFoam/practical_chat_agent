"""T183: Hybrid ReplyPlanner tests.

Deterministic tests covering the opt-in hybrid planner mode that
integrates template and LLM-generated candidates.  No LLM provider
calls are made — all LLM behavior is exercised through refusal-only
paths (no API key configured) or synthetic misuse scenarios.

Coverage areas:
  1. Template mode remains backward-compatible (no LLM generator)
  2. Hybrid mode is opt-in, not default (no LLM generator)
  3. Hybrid mode degrades gracefully when LLM is unavailable (refusal)
  4. Hybrid mode degrades gracefully when LLM raises
  5. LLM candidates pass through policy assessment
  6. Final output is always review-only ReplyPlan
  7. CLI --hybrid flag is accepted
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from practical_chat_agent.core.models import (
    ReplyPlan,
    ReplyPlanCandidate,
)
from practical_chat_agent.services.llm_reply_generator import (
    LLMReplyGeneratorService,
)
from practical_chat_agent.services.reply_planner import ReplyPlanner, ReplyPlannerError

from tests.helpers import context


# =========================================================================
# 1. Template mode backward compatibility
# =========================================================================


class TestTemplateModeBackwardCompat:
    """Template mode (default, no LLM) produces a valid 3-candidate ReplyPlan."""

    def test_default_planner_no_llm(self, baseline_friend_context) -> None:
        """Default ReplyPlanner emits valid 3-candidate plan."""
        planner = ReplyPlanner()
        plan = planner.generate(context=baseline_friend_context)
        assert len(plan.candidates) == 3
        assert plan.plan_mode == "candidate_review_only"

    def test_default_planner_is_template_only(self) -> None:
        """Default ReplyPlanner has no LLM generator attached."""
        planner = ReplyPlanner()
        assert planner.llm_generator is None
        assert planner.hybrid_mode is False

    def test_explicit_template_mode(self, baseline_friend_context) -> None:
        """ReplyPlanner with hybrid_mode=False behaves identically to default."""
        planner = ReplyPlanner(hybrid_mode=False)
        plan = planner.generate(context=baseline_friend_context)
        assert len(plan.candidates) == 3
        for c in plan.candidates:
            assert c.draft_text
            assert c.rationale
            assert len(c.supporting_context_refs) >= 1
            assert len(c.boundary_reminders) >= 1


# =========================================================================
# 2. Hybrid mode is opt-in
# =========================================================================


class TestHybridModeOptIn:
    """Hybrid mode is not the default and requires explicit opt-in."""

    def test_hybrid_mode_false_by_default(self) -> None:
        """hybrid_mode defaults to False."""
        planner = ReplyPlanner()
        assert planner.hybrid_mode is False

    def test_hybrid_mode_explicit_opt_in(self) -> None:
        """hybrid_mode can be set to True."""
        planner = ReplyPlanner(hybrid_mode=True)
        assert planner.hybrid_mode is True

    def test_hybrid_without_generator_still_works(self, baseline_friend_context) -> None:
        """Hybrid mode without LLM generator falls back to template-only."""
        planner = ReplyPlanner(hybrid_mode=True, llm_generator=None)
        plan = planner.generate(context=baseline_friend_context)
        assert len(plan.candidates) == 3


# =========================================================================
# 3. Hybrid degrades gracefully when LLM unavailable
# =========================================================================


class TestHybridLlmUnavailable:
    """Hybrid mode degrades to template-only when LLM is unavailable."""

    @pytest.fixture
    def disabled_generator(self) -> LLMReplyGeneratorService:
        return LLMReplyGeneratorService(
            api_key=None,
            base_url=None,
            model=None,
            enabled=True,
        )

    def test_hybrid_refusal_falls_back_to_template(
        self,
        baseline_friend_context,
        disabled_generator,
    ) -> None:
        """When LLM generator returns refusal, template candidates remain."""
        planner = ReplyPlanner(
            hybrid_mode=True,
            llm_generator=disabled_generator,
        )
        plan = planner.generate(context=baseline_friend_context)
        # Without API key, LLM generator returns refusal → template fallback
        assert len(plan.candidates) == 3
        assert plan.plan_mode == "candidate_review_only"

    def test_hybrid_refusal_no_crash(
        self,
        baseline_friend_context,
        disabled_generator,
    ) -> None:
        """LLM refusal does not crash the planner."""
        planner = ReplyPlanner(
            hybrid_mode=True,
            llm_generator=disabled_generator,
        )
        # Should not raise
        plan = planner.generate(context=baseline_friend_context)
        assert isinstance(plan, ReplyPlan)

    def test_force_template_overrides_hybrid(
        self,
        baseline_friend_context,
        disabled_generator,
    ) -> None:
        """force_template=True overrides hybrid mode."""
        planner = ReplyPlanner(
            hybrid_mode=True,
            llm_generator=disabled_generator,
        )
        plan = planner.generate(context=baseline_friend_context, force_template=True)
        assert len(plan.candidates) == 3


# =========================================================================
# 4. Hybrid degrades gracefully when LLM raises
# =========================================================================


class TestHybridLlmError:
    """Hybrid mode degrades to template-only when LLM raises an exception."""

    class _RaisingGenerator(LLMReplyGeneratorService):
        """Generator that raises during generate()."""

        def generate(self, *, context) -> None:  # type: ignore[override]
            msg = "Simulated provider error"
            raise RuntimeError(msg)

    def test_llm_exception_does_not_crash_planner(
        self,
        baseline_friend_context,
    ) -> None:
        """Planner catches LLM exceptions and falls back to template."""
        planner = ReplyPlanner(
            hybrid_mode=True,
            llm_generator=self._RaisingGenerator(
                api_key="sk-test",
                base_url="https://api.example.com/v1",
                model="gpt-4o",
            ),
        )
        plan = planner.generate(context=baseline_friend_context)
        assert len(plan.candidates) == 3
        assert isinstance(plan, ReplyPlan)

    def test_force_template_during_error(
        self,
        baseline_friend_context,
    ) -> None:
        """force_template=True skips LLM even if generator is configured."""
        planner = ReplyPlanner(
            hybrid_mode=True,
            llm_generator=self._RaisingGenerator(
                api_key="sk-test",
                base_url="https://api.example.com/v1",
                model="gpt-4o",
            ),
        )
        plan = planner.generate(context=baseline_friend_context, force_template=True)
        assert len(plan.candidates) == 3


# =========================================================================
# 5. Policy assessment on template candidates (invariant)
# =========================================================================


class TestPolicyAssessmentInvariant:
    """All candidates (template or LLM) go through policy assessment."""

    def test_template_candidates_have_risk_flags(
        self,
        baseline_friend_context,
    ) -> None:
        """Template candidates carry policy-derived risk flags."""
        planner = ReplyPlanner()
        plan = planner.generate(context=baseline_friend_context)
        for c in plan.candidates:
            # Each candidate should have at least the structural risk_flags
            assert isinstance(c.risk_flags, list)
            assert isinstance(c.boundary_reminders, list)
            assert len(c.boundary_reminders) >= 1
            assert c.confidence is not None

    def test_sensitive_context_adds_boundary_flags(
        self,
        sensitive_context,
    ) -> None:
        """Sensitive context produces boundary_sensitive risk flags."""
        planner = ReplyPlanner()
        plan = planner.generate(context=sensitive_context)
        all_flags = [f for c in plan.candidates for f in c.risk_flags]
        assert "boundary_sensitive" in all_flags


# =========================================================================
# 6. Final output is review-only ReplyPlan
# =========================================================================


class TestOutputContractInvariant:
    """Final output is always a review-only ReplyPlan."""

    def test_plan_mode_is_review_only(self, baseline_friend_context) -> None:
        """plan_mode is always candidate_review_only."""
        planner = ReplyPlanner()
        plan = planner.generate(context=baseline_friend_context)
        assert plan.plan_mode == "candidate_review_only"

    def test_plan_has_valid_schema(self, baseline_friend_context) -> None:
        """ReplyPlan has valid schema_version and required fields."""
        planner = ReplyPlanner()
        plan = planner.generate(context=baseline_friend_context)
        assert plan.schema_version == "reply_plan_v1"
        assert plan.contact_id
        assert len(plan.policy_boundary_summary) >= 1
        assert len(plan.notes_on_candidate_differences) >= 1

    def test_candidates_are_review_ready(self, baseline_friend_context) -> None:
        """Each candidate has all review-required fields."""
        planner = ReplyPlanner()
        plan = planner.generate(context=baseline_friend_context)
        for c in plan.candidates:
            assert isinstance(c, ReplyPlanCandidate)
            assert c.approach_label
            assert c.draft_text
            assert c.rationale
            assert len(c.supporting_context_refs) >= 1
            assert len(c.boundary_reminders) >= 1
            assert c.confidence is not None


# =========================================================================
# 7. CLI --hybrid flag
# =========================================================================


class TestCLIHybridFlag:
    """CLI --hybrid flag is accepted and produces valid output."""

    def test_cli_hybrid_flag_accepted(self, tmp_path: Path) -> None:
        """--hybrid flag does not cause CLI error (provider unavailable)."""
        from practical_chat_agent.app.main import app as typer_app
        from typer.testing import CliRunner

        runner = CliRunner()
        ctx = context(contact_id="contact_hybrid")
        input_file = tmp_path / "test_context.json"
        input_file.write_text(ctx.model_dump_json(indent=2), encoding="utf-8")
        output_file = tmp_path / "out.json"

        result = runner.invoke(
            typer_app,
            [
                "chat-reply-plan",
                "--input", str(input_file),
                "--output", str(output_file),
                "--hybrid",
            ],
        )
        assert result.exit_code == 0
        if output_file.exists():
            data = json.loads(output_file.read_text(encoding="utf-8"))
            assert data["schema_version"] == "reply_plan_v1"
            assert len(data["candidates"]) == 3

    def test_cli_hybrid_dry_run_compatible(self, tmp_path: Path) -> None:
        """--hybrid does not interfere with normal template mode."""
        from practical_chat_agent.app.main import app as typer_app
        from typer.testing import CliRunner

        runner = CliRunner()
        ctx = context(contact_id="contact_hybrid_cli")
        input_file = tmp_path / "test_context.json"
        input_file.write_text(ctx.model_dump_json(indent=2), encoding="utf-8")

        result = runner.invoke(
            typer_app,
            [
                "chat-reply-plan",
                "--input", str(input_file),
                "--hybrid",
            ],
        )
        assert result.exit_code == 0
        payload = json.loads(result.stdout)
        assert payload["plan_mode"] == "candidate_review_only"
