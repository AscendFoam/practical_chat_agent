# M31 Manual Apply Preview Scope

Task: T396 Manual Apply Preview Scope
Status: worker draft for review

## Objective

M31 designs and implements non-mutating manual apply preview records for the
review workspace.

The milestone should let a reviewer inspect what would happen if an approved
review decision were later applied, while still preventing actual memory store
writes, PersonaCard mutation, PersonaVersionStore writes, deletion execution,
runtime reply changes, provider calls, outbound messaging, or platform/media
behavior.

## Why This Milestone Is Next

M29 made review workspace records visible in local UI. M30 hardened rendering,
server-safe projection, and local QA fallback. The next safe step is not an
executor; it is a stronger preview layer that makes future apply consequences
explicit and auditable before any state-changing milestone exists.

## Product Rationale

Human-like companion behavior needs memory/persona evolution, but silent
mutation would undermine trust. Manual apply previews create a middle layer:

- reviewers can inspect target records, proposed effects, blockers, and
  rollback notes;
- users can see why a memory/persona change is being considered;
- future executors must prove they satisfy explicit gates before mutating
  state.

## Non-Mutating Boundary

M31 records must preserve:

- `review_required=true`
- `preview_only=true`
- `applies_changes=false`
- `writes_memory_store=false`
- `writes_persona_version=false`
- `runtime_ready=false`

No M31 task may apply a review decision, mutate a memory store, mutate
PersonaCard, write PersonaVersionStore, delete records, alter retrieval
indexes, call model providers, send messages, schedule actions, connect to
platform APIs, or generate voice/avatar/media.

## Gates Required Before Any Future Apply Executor

Any later apply executor must be separately scoped and must require all of:

- source candidate is synthetic or approved de-identified input;
- review workspace bundle has no blocking issue codes;
- decision record is an explicit human approval;
- candidate id and candidate kind match the bound workspace record;
- dry-run artifact exists for every target effect;
- manual apply preview exists and is current;
- user consent scope is active for the affected feature;
- safe export manifest can describe the action without raw private content;
- rollback/invalidation plan exists for affected cache/index/view artifacts;
- reviewer confirms the final no-blocker state immediately before execution.

These gates are documentation requirements in M31, not executable authority.

## Implementation Sequence

### T397 Manual Apply Preview Records

Create Pydantic records for non-mutating manual apply previews. Records should
summarize target candidate, decision, dry-run artifacts, effect summaries,
blockers, required gates, and rollback notes. Tests must prove the records are
preview-only and cannot write memory/persona state.

### T398 Manual Apply Eligibility Gate

Create a deterministic gate that reads review workspace bundles, decision
impact previews, and manual apply preview records, then returns eligible,
blocked, or stale. The gate must not apply anything.

### T399 Review Workspace Apply Preview Panel

Expose manual apply preview records in the local review workspace UI as
read-only preview cards. The panel must show blockers, gates, rollback notes,
and explicit non-apply labels.

### T400 M31 Milestone Review

Perform adversarial review before any mutation executor milestone.

## M31 Exit Criteria

M31 can close when:

- non-mutating manual apply preview records exist and are test-covered;
- eligibility gate exists and is non-applying;
- local UI can inspect apply previews as read-only cards;
- forbidden private/provider/outbound/media/apply executor fields are absent;
- residual risks are documented before any future apply executor milestone.

## Residual Risks

- M31 still does not mutate memory/persona state.
- M31 still does not prove real-data import/de-identification quality.
- M31 still does not prove live companion quality or user trust.
- Future apply executor design remains high-risk and must be separately
  reviewed.
