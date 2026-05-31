# Memory Architecture Contract

Task: T361 Memory Architecture Design
Status: worker draft for review

## Scope

This contract defines the canonical M25 memory architecture for the companion
agent. It is a documentation contract only. It does not implement new models,
stores, routes, retrieval ranking, extraction, vector search, dialogue runtime,
private data ingestion, or platform behavior.

Existing implemented contracts remain authoritative for their models:

- `MemoryEvent`
- `MemoryEventStore`
- `MemoryLifecyclePolicyService`
- `MemoryConsolidationService`
- `MemoryRetrievalBundle`
- `MemoryViewerItem`
- `TextFirstChatMemoryPrototype`
- `ConsentCenterState`
- `AIGCLabelingRequirement`
- `CompanionSafetyPolicy`
- `PersonaCard`
- `RelationshipContextBundle`

Any future model names in this document are contract candidates, not current
implementation facts.

## Canonical Layer Names

| Layer name | Status | Responsibility |
| --- | --- | --- |
| `working_context` | Future candidate | Current turn/session context; not durable M25 memory. |
| `episodic_event_memory` | Existing via `MemoryEvent` | Evidence-backed interaction events and corrections. |
| `semantic_profile_memory` | Existing via `MemoryEvent` plus future consolidation | Stable facts, preferences, and repeated themes. |
| `procedural_preference_memory` | Existing via `MemoryEvent` | Interaction habits and user-approved behavior rules. |
| `relational_memory` | Existing via `MemoryEvent` and relationship contracts | Trust, warmth, boundary, repair, conflict, pacing, and shared-history guidance. |
| `persona_self_memory` | Existing via PersonaCard plus future growth patches | Fictional AI persona self-continuity and approved growth notes. |
| `imagined_continuity_memory` | Existing via `MemoryEvent` and AIGC labels | Dreams, role dynamics, virtual-life events, and fictional continuity. |
| `audit_memory` | Future candidate | Consent, review, correction, deletion, freeze, export, and rollback audit references. |
| `quarantine_memory` | Future candidate | Untrusted source material awaiting consent, redaction, poisoning checks, and review. |

## Required Record Families

### Existing Records

`MemoryEvent` remains the base durable memory event record. It must preserve:

- event type;
- truth status;
- summary;
- provenance;
- sensitivity;
- salience;
- lifecycle state;
- retrieval permission;
- review requirements;
- timestamps.

`MemoryEventStore` remains append-only and caller-path local. It must not become
a hidden global store or retrieval ranking engine without a new task.

`MemoryConsolidationCandidate` remains recommendation-only. It must not mutate
stores.

`MemoryRetrievalBundle` remains packaging-only for already-selected memory. It
must not implement ranking or vector search.

`MemoryViewerItem` remains read-only inspection metadata.

### Future Contract Candidates

Later tasks may define:

- `MemoryCandidate`: pre-review observation before a `MemoryEvent` exists;
- `MemoryContradictionCandidate`: reviewable conflict between memory records;
- `MemoryDeletionCascadePlan`: deletion/withdrawal propagation plan;
- `MemoryQuarantineRecord`: untrusted source record awaiting review;
- `MemoryAuditEvent`: audit record for consent, review, correction, deletion,
  freeze, export, rollback, and training exclusion.

These names are not implemented in T361.

## Type And Truth Invariants

- Factual memory must be `event_type="factual"` and
  `truth_status="evidence_backed"`.
- Inferred memory must include confidence and inference rationale.
- Relational memory must include relationship dimensions or reference an
  approved relationship context.
- Procedural memory must include preference labels and must not become factual
  biography.
- Imagined memory must include an imagined context label.
- Imagined memory must not enable factual retrieval.
- Factual retrieval bundles must not include imagined memory.
- Deleted, frozen, or archived memory must not be retrieval-eligible.
- Superseded memory must not be used as current fact without explicit review
  purpose and explanation.

## Consent Gates

Memory operations must respect active consent by feature scope:

- `memory` for storing and retrieving companion memory;
- `persona_distillation` for future style extraction or persona synthesis from
  source records;
- `proactive_messaging` for future non-sending proactive candidate review;
- `aigc_export_share` for future copy/download/export/share surfaces;
- `voice_avatar` for future voice/avatar data and output;
- `model_improvement` for any future training or evaluation use.

If consent is withdrawn for a scope, later implementation must mark affected
records unavailable or produce a deletion cascade plan before retrieval,
export, persona growth, distillation, or training-use paths can continue.

T361 does not implement consent mutation or deletion cascades.

## Lifecycle Gates

Durable memory lifecycle states are:

- `active`
- `frozen`
- `deleted`
- `superseded`
- `archived`

Retrieval gates:

- `active` can be eligible only when permission allows the requested context.
- `frozen`, `deleted`, and `archived` are not retrieval-eligible.
- `superseded` is not eligible as current fact unless a future review-purpose
  path explicitly includes superseded records with explanation.
- medium/high sensitivity and `review_required=true` records are not eligible
  outside review surfaces.

## Write Path Contract

Any future write path must:

1. classify the candidate as factual, inferred, relational, procedural, or
   imagined;
2. check consent before durable storage;
3. attach redacted provenance refs;
4. assign sensitivity, salience, confidence where applicable, lifecycle, and
   retrieval permission;
5. route crisis, dependency, relationship replacement, and real-person
   likeness risk through safety review;
6. require review for sensitive, uncertain, contradicted, or high-risk memory;
7. append new records rather than overwriting existing records;
8. avoid storing raw transcript/private chat text.

## Manage Path Contract

Any future manage path must:

- return recommendations or candidates before mutation;
- keep factual, inferred, relational, procedural, and imagined memory separate;
- never merge imagined memory into factual memory;
- keep high-sensitivity memory review-required by default;
- preserve source refs when compressing memory unless deletion/withdrawal
  requires removal or unavailability;
- represent contradictions as candidates rather than silent overwrites;
- keep deletion, freeze, archive, and consent withdrawal auditable.

## Read Path Contract

Any future read path must:

- declare retrieval purpose;
- filter by lifecycle state;
- filter by retrieval permission;
- exclude review-required memory unless the purpose is review;
- exclude imagined memory from factual response purposes;
- preserve event type, truth status, provenance refs, lifecycle, sensitivity,
  and review-required flags in retrieval bundles;
- expose exclusion reasons where practical;
- add safety warnings for crisis, dependency, real-person likeness,
  sensitivity, contradiction, or withdrawal restrictions;
- generate explanation metadata before any future dialogue runtime consumes
  retrieved memory.

## Explanation Invariants

User or reviewer-facing surfaces must be able to explain:

- what type of memory was used;
- whether it is factual, inferred, relational, procedural, or imagined;
- where it came from through redacted source refs;
- whether it was user-edited, system-generated, imagined, or synthetic;
- whether it is sensitive or review-required;
- why it was included or excluded;
- how the user can correct, freeze, delete, or withdraw consent for it.

## Persona Growth Boundary

Memory may support persona growth only by producing reviewable evidence for a
future growth patch. It must not directly mutate:

- `PersonaCard.identity`;
- `PersonaCard.source_policy`;
- `PersonaCard.safety_policy`;
- `PersonaGrowthPolicy`;
- persona version store records;
- proactive preferences;
- voice/avatar state.

Any future persona growth patch must reference memory ids and remain bounded by
PersonaCard review/version contracts.

## Distillation Boundary

Memory architecture may prepare for de-identified distillation, but it must not
ingest private chat records in M25.

Future distillation-ready records must:

- use synthetic fixtures first;
- require `persona_distillation` consent;
- avoid raw source text in committed files;
- minimize third-party data;
- separate feature extraction from persona synthesis;
- produce clone/similarity risk warnings;
- create a new fictional PersonaCard by default;
- keep outputs review-required and non-runtime-ready until approved.

## Forbidden Fields And Surfaces

Memory architecture records must not contain:

- raw private chat text;
- full transcripts;
- private screenshots;
- voice samples;
- audio bytes;
- images or video;
- generated media paths;
- provider credentials;
- platform recipient ids;
- send queues;
- schedules;
- delivery state;
- webhooks;
- tokens;
- microphone or camera prompts;
- clinical advice scripts;
- launch, legal, regulator, app-store, or user-study approval claims.

## Synthetic Fixture Requirements

Later implementation tasks should include fixtures for:

- safe factual memory;
- inferred memory with confidence;
- relational boundary repair;
- procedural preference correction;
- imagined continuity memory;
- contradiction candidate;
- high-sensitivity review-required memory;
- consent withdrawal;
- blocked real-person clone request;
- de-identified style inspiration;
- crisis/dependency safety routing.

Fixtures must be deterministic, local, and visibly synthetic.

## Acceptance Criteria For Later Implementation

Later memory implementation tasks should be accepted only if:

- tests prove factual and imagined memory cannot collapse;
- tests prove deleted/frozen/archived memory is not retrieval-eligible;
- tests prove review-required memory is excluded outside review surfaces;
- tests prove consent withdrawal disables affected retrieval paths or produces
  a deletion cascade plan;
- tests prove contradiction handling creates candidates rather than overwrites;
- tests prove persona growth cannot silently mutate PersonaCard;
- tests prove forbidden private/raw/outbound/provider/media/platform fields are
  absent;
- docs record residual risks without claiming launch or legal validation.

## Non-Actions

T361 does not implement:

- new Python models or services;
- stores;
- APIs;
- CLIs;
- persistence;
- extraction;
- ranking;
- embeddings;
- vector search;
- LLM calls;
- private chat-log reads;
- dialogue runtime;
- persona mutation;
- proactive candidates;
- sending or scheduling;
- platform integration;
- voice/avatar/video behavior.

