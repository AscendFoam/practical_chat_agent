# Task T172: CommunicationPolicyBrief + BoundaryProfileBrief Schemas

## Task ID

T172

## Goal

Define additive `CommunicationPolicyBrief` and `BoundaryProfileBrief` schemas and contract notes derived from approved `ContactSkill`, with optional policy enrichment from approved patch hints only where the T170 design explicitly allows it.

## Why Now

T172 is the second schema slice after T171. It formalizes the policy and boundary parts of the T170 decomposition before any projection or runtime integration is allowed. This task exists to remove semantic ambiguity from T170 reviewer notes before T173-T174 start interpreting the design in code.

## Read First

- `docs/04_task_board.md`
- `docs/03_architecture.md`
- `docs/07_handoff.md`
- `docs/architecture/contactskill_decomposition.md`
- `docs/review/T170_review.md`
- `docs/data_contracts/contactskill_decomposition_contract.md`
- `docs/reference/AI_coding_workflow.md`

## Inputs To Respect

- T170 reviewer note N01 must be resolved here: formalize how `BoundaryProfileBrief.sensitivity_summary` is derived.
- T170 reviewer note N03 must be handled explicitly: either keep `important_event_summaries` under the boundary brief with a documented rationale or revise the contract with a clearly justified ownership decision.
- T170 reviewer note N04 must be documented conservatively: approved patch hints may enrich communication policy, but this task must not broaden patch semantics beyond the existing review-only compact-hint contract from T164.
- T171 reviewer note N05 must be resolved or explicitly deferred here: decide whether these derived briefs need their own `schema_version` field, or document why parent-store versioning remains sufficient.

## Allowed Files

- `src/practical_chat_agent/core/models.py`
- `docs/data_contracts/contactskill_decomposition_contract.md`
- `tests/test_contactskill_policy_briefs.py`
- `docs/07_handoff.md`

## Forbidden Scope

- Do not replace existing ReplyPlanner policy engine.
- Do not modify or remove existing `ContactSkill` / `ContactSkillStoreRecord` fields except for additive helper types strictly needed by the new briefs.
- Do not implement projection service logic, `ChatContext` integration, ReplyPlanner consumption changes, or any CLI entrypoint.
- Do not auto-approve policies.
- Do not reinterpret approved patches as automatic learning or as a new approval boundary.
- Do not add sending or platform integration.

## Expected Output

Produce:

- additive Pydantic models for `CommunicationPolicyBrief` and `BoundaryProfileBrief`
- any tightly scoped helper model(s) needed to keep the schema typed and reviewable
- contract documentation in `docs/data_contracts/contactskill_decomposition_contract.md` for:
  - fields and field meanings
  - evidence/source traceability
  - the exact sensitivity reduction rule
  - the chosen ownership for `important_event_summaries`
  - the derived-brief versioning decision
  - how approved patch hints relate to the policy brief without changing T164 semantics
- committed synthetic validation tests covering:
  - valid construction of both briefs
  - the chosen sensitivity-summary derivation rule
  - required traceability fields
  - safe handling of optional patch-hint enrichment

## Verification

- Run: `python -m py_compile src/practical_chat_agent/core/models.py`
- Run: `pytest tests/test_contactskill_policy_briefs.py -q`
- Verify the models remain additive only and do not require runtime wiring.

## Expected Handoff Update

Append a T172 implementation record to `docs/07_handoff.md` that captures:

- which fields belong to `CommunicationPolicyBrief` vs `BoundaryProfileBrief`
- the finalized sensitivity reduction rule
- the final ownership decision for `important_event_summaries`
- the versioning decision for these derived briefs
- how approved patch hints are handled without broadening patch semantics
- what T173 can now assume for projection logic

## Reviewer Type

normal

## Reviewer Focus

- Are the schemas additive and non-breaking?
- Did the worker resolve the sensitivity-reduction rule explicitly rather than leaving it in prose?
- Is the boundary/event ownership decision explicit and technically coherent?
- Did the task avoid runtime integration, patch-semantic expansion, or ReplyPlanner behavior changes?
