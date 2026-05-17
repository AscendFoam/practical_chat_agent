# Task T164: Approved Patch Compact Context

## Task ID

T164

## Goal

Inject approved, runtime-ready preference patches into `ChatContext` as compact review-only communication hints.

## Why Now

Once preference patches are manually approved, ReplyPlanner can use them as compact communication guidance without reading full feedback logs or private notes.

## Allowed Files

- `src/practical_chat_agent/core/models.py`
- `src/practical_chat_agent/services/chat_context.py`
- `src/practical_chat_agent/services/feedback.py`
- `docs/07_handoff.md`

## Forbidden Scope

- Do not inject candidate/rejected/frozen/archived patches.
- Do not inject full feedback notes, edited text, or raw draft text.
- Do not mutate ContactSkill/MemoryFact/store records.
- Do not call an LLM.
- Do not send messages or integrate platforms.

## Expected Output

`ChatContext` should include compact approved patch briefs such as short behavior instructions, patch ids, and supporting feedback refs.

## Verification

- Approved patch enters context as compact brief.
- Candidate/rejected/frozen/archived patch is excluded.
- Full feedback text does not enter context.

## Reviewer Type

adversarial
