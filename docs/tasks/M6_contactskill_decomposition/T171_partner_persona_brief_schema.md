# Task T171: PartnerPersonaBrief Schema

## Task ID

T171

## Goal

Define a compact `PartnerPersonaBrief` schema derived from approved ContactSkill, focused only on reply-relevant stable context.

## Allowed Files

- `src/practical_chat_agent/core/models.py`
- `docs/data_contracts/contactskill_decomposition_contract.md`
- `docs/07_handoff.md`

## Forbidden Scope

- Do not create persona clone or simulate what the contact would say.
- Do not modify ContactSkill records.
- Do not inject full ContactSkill JSON or raw transcripts into runtime context.

## Expected Output

Schema may include:

- stable traits relevant to communication
- topic preferences
- stress patterns
- known constraints
- confidence
- evidence refs

## Verification

- Compile changed models.
- Validate synthetic safe brief.

## Reviewer Type

normal
