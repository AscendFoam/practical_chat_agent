# Task T170: ContactSkill Decomposition Design

## Task ID

T170

## Goal

Write a compatibility-first design document for ContactSkill decomposition.

Do not delete, replace, or deprecate `ContactSkill`. Define how approved `ContactSkill` records can project into smaller derived briefs such as `PartnerPersonaBrief`, `CommunicationPolicyBrief`, and `BoundaryProfileBrief`, while leaving the current aggregate record runnable as the fallback contract.

## Why Now

M5 is now functionally complete within review-only constraints. The next safe step is design-only M6 work that reduces `ContactSkill` overload without breaking the existing T120-T164 storage, approval, and runtime path. This task exists to prevent accidental big-bang refactor or premature schema churn.

## Read First

- `docs/04_task_board.md`
- `docs/03_architecture.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`
- `docs/reference/AI_coding_workflow.md`

## Inputs To Consider

The design should explicitly account for these already-shipped surfaces:

- T113 original `ContactSkill` builder intent and evidence model
- T120-T123 approved-store and runtime-ready context path
- T130-T133 reply planner and policy layer expectations
- T160-T164 patch pipeline, especially approved compact patch context as an additive communication-hint layer

You do not need to reread private data or produce implementation code. This is an architecture package only.

## Allowed Files

- `docs/architecture/contactskill_decomposition.md`
- `docs/07_handoff.md`

## Forbidden Scope

- Do not edit code.
- Do not change existing ContactSkill behavior.
- Do not migrate data.
- Do not claim ContactSkill is deprecated.
- Do not define a breaking replacement plan that requires immediate schema or runtime changes.
- Do not introduce LLM, platform, send-gate, or realtime integration scope.
- Do not change task board, risks, or other governance files from the worker side.

## Expected Output

Design must include:

- current pain points in the all-in-one `ContactSkill` shape
- proposed derived-brief set with concise responsibilities for each brief
- field ownership table mapping current `ContactSkill` areas to future derived briefs
- fallback strategy showing how runtime can continue to consume the existing aggregate if derived briefs are absent
- evidence-ref preservation rules and approval-boundary rules
- compatibility and migration phases that remain additive, not breaking
- explicit non-goals and forbidden scope boundaries
- persona-clone / impersonation / autonomous-contact boundaries that remain unchanged

The design should be concrete enough that later schema tasks (`T171+`) can be split cleanly without reopening M5 behavior.

## Verification

- Document references the current T120-T123, T130-T133, and T160-T164 pipeline.
- Document explicitly states existing approved `ContactSkill` data remains runnable.
- Document makes clear that decomposition is projection/addition, not replacement.
- Handoff update states what future tasks can now proceed from the design and what is still intentionally deferred.

## Expected Handoff Update

Append a T170 implementation/design record to `docs/07_handoff.md` that captures:

- what decomposition shape was proposed
- what compatibility guarantees were preserved
- what follow-up schema tasks are now unblocked
- what important open questions remain, if any

## Reviewer Type

normal

## Reviewer Focus

- Is the design additive and compatibility-first?
- Does it preserve evidence-first review boundaries and approved-store assumptions?
- Does it avoid smuggling in code changes, migrations, or deprecation claims?
- Does it give later worker tasks a clean, non-overlapping split for schema and projection work?
