# Task T181: LLM Candidate Offline CLI

## Task ID

T181

## Goal

Implement an opt-in offline CLI that generates private `LLMReplyPlan` artifacts or structured refusals from safe synthetic/redacted `ChatContext` JSON, while preserving the existing deterministic planner path unchanged.

This task may call an LLM provider, but it must remain offline, additive, and review-only.

## Why Now

T180 has already fixed the contract boundary for optional LLM-generated candidates. The next smallest safe step is to implement a separate offline generator CLI before extracting a standalone validator (T182), before any hybrid planner work (T183), and before any quality claim from holdout evaluation (T184).

## Read First

- `docs/04_task_board.md`
- `docs/03_architecture.md`
- `docs/06_eval_protocol.md`
- `docs/07_handoff.md`
- `docs/data_contracts/llm_candidate_generator_contract.md`
- `docs/review/T180_review.md`
- `docs/reference/AI_coding_workflow.md`
- `src/practical_chat_agent/core/models.py`
- `src/practical_chat_agent/services/reply_planner.py`
- `src/practical_chat_agent/services/chatlog_distillation.py`
- `src/practical_chat_agent/app/main.py`

## Inputs To Respect

- T181 is offline and opt-in only. It may generate a private artifact from a safe `ChatContext` JSON file, but it must not become part of the default runtime planner path.
- T181 must preserve the existing deterministic `ReplyPlanner` and `chat-reply-plan` behavior exactly. No hybrid planning is authorized in this task.
- Input must stay within the existing compact-context boundary already encoded in `ChatContext` and documented by T123/T164/T174. No raw `private/chat_history/` reads, no full store JSON dumps, and no new `ChatContextAssembler` path are authorized.
- The generator may return candidates or a structured refusal, but deterministic post-generation validation is required before any output file is written.
- If live provider access or credentials are unavailable, document that limitation honestly. Do not fake a successful provider run.

## Allowed Files

- `src/practical_chat_agent/core/models.py`
- `src/practical_chat_agent/services/llm_reply_generator.py`
- `src/practical_chat_agent/services/reply_planner.py`
- `src/practical_chat_agent/app/main.py`
- `tests/test_llm_reply_generator.py`
- `docs/07_handoff.md`

## Forbidden Scope

- Do not make LLM mode default.
- Do not modify current `chat-reply-plan` behavior.
- Do not implement hybrid planner logic, deterministic/LLM ranking merge logic, or any T183 work.
- Do not mutate memory, `ContactSkill`, approved stores, runtime context, feedback logs, or policy state.
- Do not add sending, platform integration, DB, vector DB, UI, or background automation.
- Do not write raw prompts, raw provider responses, or raw transcript text to committed directories.
- Do not loosen policy/boundary review, approved-store semantics, or no-impersonation rules.

## Expected Output

- A separate offline CLI entrypoint, for example `chat-reply-generate-llm`, that:
  - reads safe synthetic/redacted `ChatContext` JSON
  - calls an LLM provider through an OpenAI-compatible request path or equivalent existing repo pattern
  - emits a private `LLMReplyPlan` JSON artifact or structured refusal
  - performs deterministic post-generation validation before writing output
  - prints only safe metadata to stdout
- Additive models/helpers required to represent `LLMReplyPlan`, generation metadata, and structured refusal shape in repo code.
- A separate generator service or helper layer that keeps LLM-specific logic out of the existing deterministic planner flow.
- Focused automated coverage for:
  - valid plan generation/normalization from provider-shaped output
  - structured refusal behavior
  - rejection of invalid refs, missing boundary reminders, rank problems, privacy-unsafe output, or impersonating output
  - CLI private-output behavior and safe stdout summary

## Verification

- `python -m py_compile src/practical_chat_agent/core/models.py src/practical_chat_agent/services/llm_reply_generator.py src/practical_chat_agent/services/reply_planner.py src/practical_chat_agent/app/main.py`
- `pytest tests/test_llm_reply_generator.py -q`
- If live provider access is available: one smoke run on safe synthetic/redacted private context that writes only to a private output path and records whether the result was a validated plan or structured refusal.
- If live provider access is not available: explicitly record that the smoke run was not executed, and rely only on deterministic automated coverage for this task.

## Expected Handoff Update

Append a T181 implementation record to `docs/07_handoff.md` that captures:

- CLI name and file/output contract
- where LLM-specific logic lives
- how deterministic post-generation validation works
- what provider/runtime assumptions were verified versus not verified
- what T182 may extract or harden next

## Reviewer Type

adversarial

## Reviewer Focus

- Does T181 stay separate from the existing deterministic `ReplyPlanner`, or does it quietly start hybrid/runtime integration early?
- Does the CLI consume only safe `ChatContext` JSON and avoid inventing a new raw-transcript or full-store input path?
- Are output writing rules private-path-only and safe on stdout?
- Is deterministic post-generation validation real and enforced before output is accepted?
- Does the implementation avoid prompt/response leakage, impersonation, and unauthorized fact insertion?

## Notes For Worker

- Reuse existing provider-call patterns where practical, but do not broaden this task into a shared provider refactor unless required for correctness.
- Keep the validation surface only as wide as T181 needs for safe offline generation; T182 remains the task for validator hardening/extraction.
