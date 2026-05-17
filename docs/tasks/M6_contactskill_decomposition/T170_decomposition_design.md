# Task T170: ContactSkill Decomposition Design

## Task ID

T170

## Goal

Write a design document for compatible ContactSkill decomposition.

Do not delete or replace ContactSkill. Define how approved ContactSkill can project into smaller derived briefs: PartnerPersonaBrief, CommunicationPolicyBrief, BoundaryProfileBrief, and later RelationshipState inputs.

## Why Now

The updated design document correctly warns that ContactSkill is becoming overloaded, but direct removal would break the existing evidence-first pipeline. A design task prevents accidental big-bang refactor.

## Allowed Files

- `docs/architecture/contactskill_decomposition.md`
- `docs/07_handoff.md`

## Forbidden Scope

- Do not edit code.
- Do not change existing ContactSkill behavior.
- Do not migrate data.
- Do not claim ContactSkill is deprecated.

## Expected Output

Design must include:

- field ownership table
- fallback strategy from derived briefs to existing ContactSkill brief
- evidence refs preservation rules
- migration/compatibility plan
- forbidden persona clone/impersonation boundaries

## Verification

- Document references current T120-T123/T130-T133 pipeline.
- Document explicitly states old data remains runnable.

## Reviewer Type

normal
