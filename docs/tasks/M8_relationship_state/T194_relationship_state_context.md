# Task T194: RelationshipState Compact Context

## Task ID

T194

## Goal

Inject approved RelationshipState compact summary into `ChatContext`.

## Forbidden Scope

- Do not inject raw signal history.
- Do not auto-update state.
- Do not change sending behavior.

## Allowed Files

- `src/practical_chat_agent/core/models.py`
- `src/practical_chat_agent/services/chat_context.py`
- `docs/07_handoff.md`

## Reviewer Type

normal
