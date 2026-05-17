# Task T173: ContactSkill Projection Service

## Task ID

T173

## Goal

Implement a projection service that derives compact PartnerPersona/CommunicationPolicy/BoundaryProfile briefs from approved ContactSkill records.

## Allowed Files

- `src/practical_chat_agent/services/contact_skill.py`
- `src/practical_chat_agent/core/models.py`
- `src/practical_chat_agent/app/main.py`
- `docs/07_handoff.md`

## Forbidden Scope

- Do not mutate ContactSkill records.
- Do not read raw chat history.
- Do not call an LLM.
- Do not auto-approve derived briefs.
- Do not add platform integration or sending.

## Expected Output

Projection should preserve record ids/evidence refs and produce compact derived briefs.

## Verification

- Run projection on synthetic approved ContactSkill fixture.
- Confirm candidate/rejected/frozen ContactSkill records are excluded.
- Confirm evidence refs are preserved.

## Reviewer Type

adversarial
