# Task T181: LLM Candidate Offline CLI

## Task ID

T181

## Goal

Implement an offline experimental CLI for LLM-assisted candidates that outputs private `ReplyPlan`-compatible artifacts.

## Forbidden Scope

- Do not make LLM mode default.
- Do not send messages.
- Do not mutate memory/ContactSkill.
- Do not write raw prompts/responses to committed dirs.

## Allowed Files

- `src/practical_chat_agent/services/reply_planner.py`
- `src/practical_chat_agent/app/main.py`
- `docs/07_handoff.md`

## Verification

- Run on synthetic/redacted private context.
- Validate output schema.
- Confirm no raw transcript echo or committed private artifact.

## Reviewer Type

adversarial
