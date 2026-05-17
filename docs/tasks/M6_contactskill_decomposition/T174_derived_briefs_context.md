# Task T174: Derived Briefs Context Integration

## Task ID

T174

## Goal

Add derived briefs to `ChatContext` as compact runtime hints, with fallback to existing ContactSkill brief.

## Allowed Files

- `src/practical_chat_agent/core/models.py`
- `src/practical_chat_agent/services/chat_context.py`
- `docs/07_handoff.md`

## Forbidden Scope

- Do not remove existing approved ContactSkill brief support.
- Do not inject full ContactSkill JSON.
- Do not inject raw transcripts.
- Do not modify ReplyPlanner generation behavior unless Captain expands scope.

## Expected Output

`ChatContext` can carry derived briefs when available and safely fallback when not.

## Verification

- Derived brief context loads from synthetic fixture.
- Missing derived briefs keep existing context behavior.

## Reviewer Type

normal
