# Task T183: Hybrid ReplyPlanner

## Task ID

T183

## Goal

Support template and optional LLM planner modes while preserving review-only `ReplyPlan` output.

## Forbidden Scope

- Do not make LLM mode default.
- Do not send messages.
- Do not bypass candidate validator or policy engine.
- Do not mutate memory/ContactSkill.

## Allowed Files

- `src/practical_chat_agent/services/reply_planner.py`
- `src/practical_chat_agent/app/main.py`
- `docs/07_handoff.md`

## Verification

- Template mode remains backward-compatible.
- LLM mode produces validated `ReplyPlan` on synthetic input.
- Policy validation still runs after generation.

## Reviewer Type

adversarial
