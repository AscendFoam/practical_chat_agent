# Task T172: CommunicationPolicyBrief Schema

## Task ID

T172

## Goal

Define compact communication and boundary policy briefs derived from approved ContactSkill and approved preference patches.

## Allowed Files

- `src/practical_chat_agent/core/models.py`
- `docs/data_contracts/contactskill_decomposition_contract.md`
- `docs/07_handoff.md`

## Forbidden Scope

- Do not replace existing ReplyPlanner policy engine.
- Do not modify ContactSkill records.
- Do not auto-approve policies.
- Do not add sending or platform integration.

## Expected Output

Schema may include:

- preferred tone
- avoid tone
- question style
- humor allowed
- proactivity level
- repair strategy
- boundary rules
- version / superseded_by
- evidence refs

## Verification

- Compile changed models.
- Validate synthetic safe policy brief.

## Reviewer Type

normal
