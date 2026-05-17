# Task T191: RelationshipSignal Extractor

## Task ID

T191

## Goal

Extract conservative relationship signals from feedback and approved metadata.

## Forbidden Scope

- Do not read raw chat history.
- Do not auto-update RelationshipState.
- Do not call an LLM unless Captain explicitly expands scope.

## Allowed Files

- `src/practical_chat_agent/services/feedback.py`
- `src/practical_chat_agent/core/models.py`
- `docs/07_handoff.md`

## Reviewer Type

adversarial
