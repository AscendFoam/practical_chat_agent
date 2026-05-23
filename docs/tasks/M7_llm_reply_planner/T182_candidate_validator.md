# Task T182: Candidate Validator

## Task ID

T182

## Goal

Extract and harden a deterministic validator layer that can be shared by template and LLM-generated reply candidates, then close the specific privacy/refusal/test gaps carried forward from the T181 review.

## Why Now

T181 is accepted with `PASS_WITH_WARNINGS`: the repo now has an opt-in offline LLM generator CLI, but the review identified validator hardening debt that should be resolved before any hybrid planner wiring or default runtime LLM path is considered.

This is the next smallest safe step because:

- it improves the review-only safety boundary without changing generation scope
- it addresses the deferred T181 review items directly
- it reduces risk before T183 hybrid planner work tries to combine deterministic and LLM candidates

## Read First

- `docs/04_task_board.md`
- `docs/03_architecture.md`
- `docs/06_eval_protocol.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`
- `docs/review/T181_review.md`
- `docs/data_contracts/llm_candidate_generator_contract.md`
- `src/practical_chat_agent/services/llm_reply_generator.py`
- `src/practical_chat_agent/services/reply_planner.py`
- `src/practical_chat_agent/core/models.py`

## Allowed Files

- `src/practical_chat_agent/services/llm_reply_generator.py`
- `src/practical_chat_agent/services/reply_planner.py`
- `src/practical_chat_agent/services/reply_candidate_validator.py` (new, preferred if extraction happens)
- `src/practical_chat_agent/core/models.py` (only if a small additive schema/helper adjustment is unavoidable)
- `src/practical_chat_agent/app/main.py` (only if minimal CLI wiring is required by the validator change)
- `tests/test_llm_reply_generator.py`
- `tests/test_reply_planner.py`
- `tests/test_reply_candidate_validator.py` (new)
- `docs/07_handoff.md`

## Forbidden Scope

- Do not add a new candidate generation path.
- Do not redesign the T181 prompt or provider call flow except where required for deterministic validation/preflight enforcement.
- Do not implement hybrid planner wiring.
- Do not make LLM generation the default planner path.
- Do not add send/platform integration.
- Do not mutate approved memory, ContactSkill, or any runtime store.
- Do not consume raw chat transcript, full approved-store JSON, or any new non-compact context input surface.
- Do not claim planner-quality completion or production readiness.

## Expected Output

- A deterministic validator layer that can be reused across candidate sources rather than living only inside T181 service code.
- Explicit validator checks for:
  - non-empty candidate text
  - supporting context refs
  - boundary reminders
  - approved ref types
  - generator/source consistency where applicable
  - privacy leakage rejection
  - anti-impersonation rejection
  - stable rank normalization after filtering
- Explicit handling for the currently deferred `INPUT_TOO_LARGE` path, or an equivalent deterministic preflight refusal before provider call.
- Committed regression tests covering the T181 review gaps:
  - `_build_llm_input` output-shape expectations
  - provider-response parse error paths
  - generator-to-validator end-to-end synthetic flow
  - CLI stdout privacy regression
- A short handoff update that states what was extracted, what was hardened, and what still remains deferred.

## Implementation Notes

- Prefer extraction into a small shared validator module if that simplifies reuse between deterministic and LLM candidate paths.
- Keep the validator deterministic. No embeddings, no semantic search service, no external moderation dependency.
- If privacy-leak detection is improved, keep it conservative and explain the deterministic rule in code/tests.
- If `reply_planner.py` is touched, keep changes limited to validator reuse or equivalent safety-preserving refactor. Do not change planner strategy selection logic.

## Verification

- `python -m py_compile src/practical_chat_agent/services/llm_reply_generator.py src/practical_chat_agent/services/reply_planner.py src/practical_chat_agent/app/main.py`
- `pytest tests/test_llm_reply_generator.py -q`
- `pytest tests/test_reply_planner.py -q`
- `pytest tests/test_reply_candidate_validator.py -q` if the file is added
- `pytest tests/ -q`

Acceptance criteria:

- A good synthetic candidate passes validation.
- A candidate missing refs or boundary reminders fails validation.
- A candidate echoing compact-context text fails validation.
- A candidate that impersonates the contact voice fails validation.
- Oversize input triggers deterministic refusal behavior instead of silently relying on generic provider failure.
- CLI stdout remains safe metadata only.

## Reviewer Type

adversarial
