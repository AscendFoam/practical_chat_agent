# Task T183: Hybrid ReplyPlanner

## Task ID

T183

## Goal

Integrate template and optional LLM candidate generation into one opt-in, review-only `ReplyPlanner` surface while preserving backward-compatible template mode, shared deterministic validation, policy/boundary gating, and compact-context boundaries.

## Why Now

T182 is accepted with `PASS_WITH_WARNINGS`: the repo now has a shared validator layer and stronger regression coverage, so the next safe step is planner integration rather than more standalone generator/validator work.

This is the next smallest safe step because:

- it uses the now-committed generator + validator layers without making them default runtime behavior
- it keeps quality judgment deferred to T184
- it lets us evaluate integration discipline separately from quality claims

## Read First

- `docs/04_task_board.md`
- `docs/03_architecture.md`
- `docs/06_eval_protocol.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`
- `docs/review/T181_review.md`
- `docs/review/T182_review.md`
- `docs/data_contracts/llm_candidate_generator_contract.md`
- `src/practical_chat_agent/services/reply_planner.py`
- `src/practical_chat_agent/services/llm_reply_generator.py`
- `src/practical_chat_agent/services/reply_candidate_validator.py`
- `src/practical_chat_agent/core/models.py`

## Allowed Files

- `src/practical_chat_agent/services/reply_planner.py`
- `src/practical_chat_agent/services/llm_reply_generator.py`
- `src/practical_chat_agent/services/reply_candidate_validator.py`
- `src/practical_chat_agent/app/main.py`
- `src/practical_chat_agent/core/models.py` (only if a small additive planner-mode or metadata adjustment is unavoidable)
- `tests/test_reply_planner.py`
- `tests/test_llm_reply_generator.py`
- `tests/test_reply_candidate_validator.py`
- `tests/test_hybrid_reply_planner.py` (new)
- `docs/07_handoff.md`

## Forbidden Scope

- Do not make LLM mode default.
- Do not bypass candidate validator or policy engine.
- Do not mutate memory/ContactSkill.
- Do not add send/platform integration.
- Do not consume raw chat transcript, full approved-store JSON, or any non-compact context input path.
- Do not treat LLM refusal as a hard failure for template mode; degraded review-only output is acceptable if documented.
- Do not claim planner quality is proven; holdout judgment remains T184.

## Expected Output

- An explicit opt-in hybrid planner path that can:
  - keep existing template-only behavior intact by default
  - optionally request LLM candidates
  - validate LLM candidates deterministically
  - merge or choose candidates into one review-only `ReplyPlan`
  - still run policy/boundary review before final output
- Clear behavior for provider-unavailable or refusal cases:
  - template mode continues to work
  - hybrid mode degrades predictably and safely
- No mutation of approved stores, ContactSkill, memory, or outbound behavior.
- Tests that prove:
  - template mode remains backward-compatible
  - hybrid mode is opt-in, not default
  - invalid LLM candidates do not bypass validator/policy gates
  - provider refusal/unavailability does not crash planner flow
  - final `ReplyPlan` remains review-only and policy-constrained

## Implementation Notes

- Keep the integration surface narrow. Prefer an explicit mode/flag rather than implicit auto-selection.
- Template candidates remain the baseline safety fallback.
- If LLM candidates are merged with template candidates, make the ranking/selection rule deterministic and documented.
- If T182's `INPUT_TOO_LARGE` bug is trivial to fix inside allowed files, it is acceptable to fix it as part of T183, but do not expand scope beyond that narrow carry-forward repair.

## Verification

- `python -m py_compile src/practical_chat_agent/services/reply_planner.py src/practical_chat_agent/services/llm_reply_generator.py src/practical_chat_agent/services/reply_candidate_validator.py src/practical_chat_agent/app/main.py`
- `pytest tests/test_reply_planner.py -q`
- `pytest tests/test_llm_reply_generator.py -q`
- `pytest tests/test_reply_candidate_validator.py -q`
- `pytest tests/test_hybrid_reply_planner.py -q` if the file is added
- `pytest tests/ -q`

Acceptance criteria:

- Template mode remains backward-compatible.
- Hybrid mode is explicitly opt-in and not the default.
- LLM candidate generation/refusal cannot bypass validator or policy review.
- Provider unavailability/refusal degrades safely without crashing the planner.
- Final output remains a review-only `ReplyPlan`.

## Reviewer Type

adversarial
