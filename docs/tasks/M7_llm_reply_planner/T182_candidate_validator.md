# Task T182: Candidate Validator

## Task ID

T182

## Goal

Validate template and LLM-generated reply candidates for schema, refs, boundary reminders, privacy, and anti-impersonation constraints.

## Allowed Files

- `src/practical_chat_agent/services/reply_planner.py`
- `src/practical_chat_agent/services/policy.py`
- `src/practical_chat_agent/app/main.py`
- `docs/07_handoff.md`

## Forbidden Scope

- Do not generate candidates.
- Do not send messages.
- Do not mutate memory/ContactSkill.

## Verification

- Good synthetic candidate passes.
- Candidate missing refs fails.
- Candidate echoing raw text or impersonating contact fails.

## Reviewer Type

adversarial
