# Task T171: PartnerPersonaBrief Schema

## Task ID

T171

## Goal

Define an additive `PartnerPersonaBrief` schema and contract derived from approved `ContactSkill`, focused only on reply-relevant stable persona and relationship context.

## Why Now

T170 is now accepted with `PASS`, so M6 may move from architecture-only design into the first schema slice. `PartnerPersonaBrief` is the smallest safe implementation step because it formalizes one derived brief without changing runtime behavior, approved-store behavior, or the current `ApprovedContactSkillBrief` fallback path.

## Read First

- `docs/04_task_board.md`
- `docs/03_architecture.md`
- `docs/07_handoff.md`
- `docs/architecture/contactskill_decomposition.md`
- `docs/review/T170_review.md`
- `docs/reference/AI_coding_workflow.md`

## Inputs To Respect

- `ContactSkill` remains the source of truth. This task adds a new model; it does not replace or mutate the existing aggregate contract.
- The schema must stay compatible with the T120-T123 approved-store path and the T130-T164 runtime/review-only boundaries.
- T170 reviewer note N02 must be resolved here: decide whether `communication_style_snapshot` stays `dict[str, str]` or becomes a structured sub-model, and document the reason in the contract doc / handoff.

## Allowed Files

- `src/practical_chat_agent/core/models.py`
- `docs/data_contracts/contactskill_decomposition_contract.md`
- `tests/test_contactskill_persona_brief.py`
- `docs/07_handoff.md`

## Forbidden Scope

- Do not create persona clone or simulate what the contact would say.
- Do not modify or remove existing `ContactSkill` / `ContactSkillStoreRecord` fields except for additive helper types strictly needed by the new brief.
- Do not implement projection service logic, `ChatContext` integration, ReplyPlanner integration, or any CLI entrypoint.
- Do not inject full `ContactSkill` JSON or raw transcripts into runtime context.
- Do not add storage, migration, approval, or runtime-ready status changes.

## Expected Output

Produce:

- an additive Pydantic model for `PartnerPersonaBrief`
- any tightly scoped helper model(s) needed to keep the schema typed and readable
- contract documentation in `docs/data_contracts/contactskill_decomposition_contract.md` for:
  - fields
  - field meanings
  - evidence/source traceability
  - fallback relationship to `ApprovedContactSkillBrief`
  - the decision taken for `communication_style_snapshot`
- committed synthetic validation tests covering:
  - valid brief construction
  - required traceability fields
  - safe defaults / optional fields
  - the chosen typing shape for communication-style snapshot

## Verification

- Run: `python -m py_compile src/practical_chat_agent/core/models.py`
- Run: `pytest tests/test_contactskill_persona_brief.py -q`
- Verify the new schema is additive only and does not require runtime wiring.

## Expected Handoff Update

Append a T171 implementation record to `docs/07_handoff.md` that captures:

- which fields are included in `PartnerPersonaBrief`
- how `communication_style_snapshot` was typed and why
- what evidence / `source_skill_record_id` traceability is preserved
- what T172 still needs to define next

## Reviewer Type

normal

## Reviewer Focus

- Is the schema additive and non-breaking?
- Did the worker resolve the communication-style typing question explicitly rather than leaving it ambiguous?
- Are evidence and source-traceability fields explicit enough for T173 projection work?
- Did the task avoid slipping into runtime integration or ContactSkill mutation?
