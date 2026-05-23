# Task T185: Hybrid Planner Language and Safety Alignment

## Task ID

T185

## Goal

Make the existing opt-in hybrid planner safer and more consistent by aligning LLM output language with template language, tightening thin-context / boundary-sensitive behavior, normalizing LLM approach labels, and adding committed regression coverage for the valid-candidate merge path.

## Why Now

T184 completed holdout evaluation and returned `PASS_WITH_WARNINGS`, but Gate M7 remains `Conditional`. The holdout evidence is useful and real, yet it exposed narrow alignment gaps that must be fixed before M7 can be considered closed.

This is the next smallest safe step because:

- it is narrow and repair-oriented
- it does not expand planner scope
- it addresses the exact conditions carried forward by the holdout review

## Read First

- `docs/04_task_board.md`
- `docs/06_eval_protocol.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`
- `docs/review/T184_review.md`
- `docs/review/T184_milestone_review.md`
- `docs/review/T183_review.md`
- `docs/tasks/M7_llm_reply_planner/T183_hybrid_reply_planner.md`

## Allowed Files

- `src/practical_chat_agent/services/llm_reply_generator.py`
- `src/practical_chat_agent/services/reply_planner.py`
- `src/practical_chat_agent/app/main.py`
- `tests/test_hybrid_reply_planner.py`
- `tests/test_llm_reply_generator.py`
- `tests/test_reply_candidate_validator.py`
- `docs/07_handoff.md`

## Forbidden Scope

- Do not add new provider integrations.
- Do not make LLM mode default.
- Do not expand planner scope beyond the narrow alignment fixes.
- Do not add send/platform integration.
- Do not mutate memory/ContactSkill.
- Do not add a new holdout campaign.
- Do not change template-only behavior.
- Do not claim M7 is complete until the gate is revisited.

## Expected Output

- LLM candidate language should match the template language used by the planner.
- Thin-context / boundary-sensitive cases should produce LLM draft text that respects the conservative intent of the policy flags.
- LLM `approach_label` values should follow the same naming convention as template labels.
- Committed regression coverage should exist for the valid-candidate merge success path.
- The hybrid planner should remain opt-in and review-only.

## Implementation Notes

- Keep the changes narrow and deterministic.
- Prefer prompt/label/validation adjustments over larger refactors.
- If a minimal test helper is needed, keep it inside the existing hybrid test surface.
- Do not introduce new quality metrics or eval campaigns; T184 already covers the evaluation side.

## Verification

- `python -m py_compile src/practical_chat_agent/services/llm_reply_generator.py src/practical_chat_agent/services/reply_planner.py src/practical_chat_agent/app/main.py`
- `pytest tests/test_hybrid_reply_planner.py -q`
- `pytest tests/test_llm_reply_generator.py -q`
- `pytest tests/test_reply_candidate_validator.py -q`
- `pytest tests/ -q`

Acceptance criteria:

- Hybrid output language matches template language or the trade-off is explicitly documented in code/docs.
- Thin-context / boundary-sensitive drafts are conservative and do not contradict policy intent.
- Hybrid approach labels are normalized.
- A committed synthetic valid-candidate merge test exists.
- Template-only behavior remains unchanged.

## Reviewer Type

adversarial
