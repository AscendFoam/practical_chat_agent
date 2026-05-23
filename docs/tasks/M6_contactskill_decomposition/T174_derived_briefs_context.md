# Task T174: Derived Briefs Context Integration

## Task ID

T174

## Goal

Add derived briefs to `ChatContext` / approved-store context as compact runtime hints, while preserving the existing `ApprovedContactSkillBrief` fallback path exactly.

## Why Now

T174 is the final M6 step. It consumes the T173 projection layer and exposes richer context structure without breaking the current T123/T164 compact-context behavior. This task finishes the compatibility-first integration promised by T170 without broadening scope into planner-generation changes or new storage.

## Read First

- `docs/04_task_board.md`
- `docs/07_handoff.md`
- `docs/architecture/contactskill_decomposition.md`
- `docs/data_contracts/contactskill_decomposition_contract.md`
- `docs/reference/AI_coding_workflow.md`

## Inputs To Respect

- `ApprovedContactSkillBrief` remains the minimum guaranteed fallback output.
- Derived briefs are optional overlays; missing or partial derived brief availability must not break current context assembly.
- Approved patch context from T164 remains a separate compact context path and must not be conflated with derived-brief presence.
- T173 follow-ups must be respected here:
  - treat `relationship_state_summary` and `important_event_summaries` as projection-owned outputs; do not silently reformat them in context assembly
  - preserve thin `CommunicationPolicyBrief.evidence_refs` exactly as projected; do not backfill evidence in the assembler
  - preserve explicit projected `sensitivity_summary` values and do not fall back to schema defaults silently

## Allowed Files

- `src/practical_chat_agent/core/models.py`
- `src/practical_chat_agent/services/chat_context.py`
- `tests/test_chat_context_decomposition.py`
- `docs/07_handoff.md`

## Forbidden Scope

- Do not remove existing approved ContactSkill brief support.
- Do not inject full ContactSkill JSON.
- Do not inject raw transcripts.
- Do not modify ReplyPlanner candidate-generation behavior, policy-engine behavior, or add any outbound/send integration.
- Do not add new persistence, migration, or CLI behavior.

## Expected Output

Produce:

- additive `ChatContext` / approved-store context fields for the derived briefs
- assembler logic that uses derived briefs when available
- explicit fallback behavior to the existing `ApprovedContactSkillBrief` when derived briefs are absent or partial
- committed synthetic tests covering:
  - derived-brief context load success
  - fallback behavior when projection is unavailable
  - partial-derived-brief behavior
  - coexistence with the existing approved-patch compact context path
  - preservation of projected summary/event formatting and sensitivity values without assembler rewriting

## Verification

- Run: `python -m py_compile src/practical_chat_agent/core/models.py src/practical_chat_agent/services/chat_context.py`
- Run: `pytest tests/test_chat_context_decomposition.py -q`
- Confirm missing derived briefs keep existing context behavior unchanged.

## Expected Handoff Update

Append a T174 implementation record to `docs/07_handoff.md` that captures:

- which `ChatContext` fields were added
- how fallback to `ApprovedContactSkillBrief` is enforced
- what remains unchanged in the existing T123/T164 context path
- how derived briefs and approved-patch compact context coexist without replacing each other
- whether any later planner task is actually needed to consume the richer structure

## Reviewer Type

normal

## Reviewer Focus

- Does the integration preserve existing fallback behavior exactly?
- Can partial or missing derived briefs coexist safely with the old aggregate path?
- Did the task avoid changing planner behavior or introducing new persistence?
