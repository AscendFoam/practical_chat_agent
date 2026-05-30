# Memory And Persona Control Requirements

Task: T300 Memory/persona control requirements
Status: worker draft for review

## Scope

This document defines local/prototype requirements for controlling companion
artifacts created in M14-M18. It does not define UI implementation, mutate
records, delete files, export data, call LLMs, or integrate with platforms.

## Artifact Inventory

Control surfaces must account for:

- Persona artifacts:
  - `PersonaCard`;
  - persona review cards;
  - persona version records.
- Memory artifacts:
  - `MemoryEvent`;
  - `MemoryRetrievalBundle`;
  - lifecycle recommendations;
  - consolidation candidates.
- Relationship/dialogue artifacts:
  - `RelationshipState`;
  - `RelationshipContextBundle`;
  - `DialogueContextPlan`;
  - `DialogueDraftStub`.
- Proactive artifacts:
  - `ProactiveConsent`;
  - `ProactivePolicyDecision`;
  - `ProactiveReviewCard`.
- Virtual life artifacts:
  - `RoleDynamicPost`;
  - `VirtualLifeSeedContext`;
  - `VirtualLifeReviewCard`.

## Required View Controls

View controls must support:

- listing artifacts by type, user id, persona id, and status;
- opening one artifact with complete schema fields;
- displaying truth status, AIGC labels, review status, lifecycle state, consent
  status, and safety labels without inference;
- showing provenance refs, memory refs, relationship context refs, and source
  ids;
- distinguishing factual, inferred, relational, procedural, and imagined memory;
- displaying imagined virtual life content as imagined, not as real-world
  activity;
- displaying whether an artifact is runtime-ready, review-required, blocked,
  paused, frozen, deleted, archived, or local-review-only.

## Required Edit Controls

Edit controls must support draft-only local changes for:

- persona display name, traits, speech style, growth policy, proactive
  preferences, and safety policy;
- memory summary, sensitivity, lifecycle state, retrieval permission, review
  notes, and provenance refs;
- proactive consent status, local review surfaces, allowed low-pressure intents,
  quiet hours, frequency caps, pause reasons, and safety notes;
- virtual life post review notes, factual-claim notes, and safety notes.

Edits must:

- create an audit event;
- preserve previous values;
- require confirmation for identity, safety, deletion, freeze, export, and
  retrieval-permission changes;
- never silently promote imagined content to factual memory;
- never enable outbound sending or platform delivery.

## Delete, Freeze, And Export Requirements

Delete/freeze/export controls must:

- support dry-run preview before mutation;
- require explicit confirmation;
- create audit events;
- distinguish soft delete from hard delete;
- block retrieval for deleted, frozen, archived, and superseded memory;
- preserve enough audit metadata to prove the operation happened;
- never delete private source files as a side effect;
- export only selected artifacts and metadata;
- label exports that contain imagined or AIGC content;
- include provenance and review status in exports.

## Audit Event Requirements

Every control operation must record:

- `audit_id`;
- actor id;
- user id;
- artifact type;
- artifact id;
- operation name;
- before/after summaries;
- reason;
- confirmation status;
- timestamp;
- safety flags;
- source task or UI surface.

Audit records must not contain raw private chat contents.

## Review And Confirmation Requirements

The following require confirmation:

- delete;
- freeze/unfreeze;
- export;
- making a persona runtime-ready;
- changing retrieval permission;
- changing memory truth status;
- changing proactive consent from disabled/paused to enabled;
- approving virtual life posts for demo surfaces;
- any edit involving factual claims, real-person similarity, crisis/low-mood
  labels, or imagined/factual contamination risk.

## Privacy And Safety Boundaries

Control surfaces must:

- avoid reading `private/chat_history/` directly;
- avoid quoting private chat contents;
- preserve AI/fictional/AIGC labels;
- preserve review-required status;
- show imagined/factual separation;
- block real-person clone, deceptive impersonation, and deceased-person
  simulation paths unless a future explicit reviewed policy changes this;
- never create outbound requests, scheduled messages, or platform actions.

## Non-Goals

T300 does not define:

- UI layout;
- API endpoints;
- database schema;
- actual mutation services;
- deletion implementation;
- export implementation;
- LLM generation;
- platform integration;
- web demo.

## Open Questions

- Should audit events be stored in the same local store as artifacts or in a
  separate append-only store?
- What export formats are required for the first prototype: JSONL, JSON, CSV,
  or ZIP bundle?
- Which controls need dual confirmation for high-sensitivity records?
- How should local access control be represented before authentication exists?
- Which artifact types should be visible in the first web demo?
