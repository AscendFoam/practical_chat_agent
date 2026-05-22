# Task T173: ContactSkill Projection Service

## Task ID

T173

## Goal

Implement a lazy `ContactSkillProjectionService` that derives `PartnerPersonaBrief`, `CommunicationPolicyBrief`, and `BoundaryProfileBrief` from approved, runtime-ready `ContactSkillStoreRecord` inputs.

## Why Now

T173 begins only after T171-T172 have frozen the brief schemas and contract semantics. This task turns the design into code while keeping storage, approval, and runtime integration boundaries unchanged.

## Read First

- `docs/04_task_board.md`
- `docs/07_handoff.md`
- `docs/architecture/contactskill_decomposition.md`
- `docs/data_contracts/contactskill_decomposition_contract.md`
- `docs/reference/AI_coding_workflow.md`

## Inputs To Respect

- Projection must be lazy and computed from the parent approved record; do not persist derived briefs as a new store format.
- Only approved + runtime-ready parent records may produce briefs.
- T120-T123 evidence and approval rules still belong to the parent record. This task projects them; it does not redefine them.

## Allowed Files

- `src/practical_chat_agent/services/contact_skill.py`
- `src/practical_chat_agent/core/models.py`
- `tests/test_contactskill_projection.py`
- `docs/07_handoff.md`

## Forbidden Scope

- Do not mutate ContactSkill records or write back any derived-brief artifact.
- Do not read raw chat history.
- Do not call an LLM.
- Do not auto-approve derived briefs.
- Do not add CLI commands, new storage, migration, or `ChatContext` integration in this task.
- Do not add platform integration or sending.

## Expected Output

Produce:

- a projection service API that takes a parent approved store record and returns derived brief objects deterministically
- runtime-ready gating that excludes candidate/rejected/frozen/archived parent records
- preservation of evidence refs and `source_skill_record_id`
- committed synthetic tests covering:
  - approved/runtime-ready projection success
  - non-runtime-ready exclusion
  - contact-id / traceability preservation
  - sensitivity and policy-field mapping according to the T171-T172 contract

## Verification

- Run: `python -m py_compile src/practical_chat_agent/core/models.py src/practical_chat_agent/services/contact_skill.py`
- Run: `pytest tests/test_contactskill_projection.py -q`
- Confirm projection remains pure/additive and writes nothing to disk.

## Expected Handoff Update

Append a T173 implementation record to `docs/07_handoff.md` that captures:

- the projection service entrypoint(s)
- runtime-ready gating rules
- how each brief is built from the parent record
- what T174 can now consume safely

## Reviewer Type

adversarial

## Reviewer Focus

- Does projection preserve approval and evidence boundaries instead of inventing a parallel workflow?
- Are non-runtime-ready parent records excluded correctly?
- Is the implementation deterministic and non-mutating?
- Did the task avoid slipping into `ChatContext` integration or new persistence?
