# Memory Architecture Design

Task: T361 Memory Architecture Design
Status: worker draft for review

## Product Objective

The companion product needs memory that feels continuous without becoming
opaque, unsafe, or deceptive. The architecture should let the agent remember
important facts, relationship history, preferences, corrections, and imagined
persona continuity while preserving consent, provenance, review gates, and user
control.

M25 should not add runtime memory behavior yet. This design is a contract
foundation for later synthetic implementation tasks.

## Architecture Assumptions

- The product remains text-first, local, synthetic, and review-required during
  M25.
- Existing `MemoryEvent v2` is the base record for typed memory events.
- Existing `MemoryEventStore` is an append-only local store and is not a
  ranking engine.
- Existing lifecycle, consolidation, retrieval bundle, viewer, chat memory,
  consent, AIGC labeling, safety, persona, and relationship contracts stay in
  force.
- Raw private chat text is not part of any memory architecture record in M25.
- Imagined continuity can improve immersion only when it is permanently
  isolated from factual evidence.
- Persona growth must be proposed as patches to PersonaCard/version state, not
  silently written by memory consolidation.

## Canonical Memory Layers

| Layer | Purpose | Existing Contract Mapping |
| --- | --- | --- |
| `working_context` | Short-lived current-turn/session context. | Future runtime candidate only; no M25 store. |
| `episodic_event_memory` | Evidence-backed events, corrections, and notable interaction moments. | `MemoryEvent(event_type="factual")`; `MemoryProvenance`. |
| `semantic_profile_memory` | Stable user preferences, profile facts, and repeated themes. | `MemoryEvent(event_type="factual" or "inferred")`; consolidation candidates. |
| `procedural_preference_memory` | Interaction rules such as message length, comfort style, taboo topics, and workflow preferences. | `MemoryEvent(event_type="procedural")`. |
| `relational_memory` | Trust, warmth, boundaries, conflict, repair, pacing, and shared history. | `MemoryEvent(event_type="relational")`; `RelationshipState`; `RelationshipContextBundle`. |
| `persona_self_memory` | Fictional AI persona's stable self-continuity, virtual routine, and approved growth notes. | `PersonaCard`, `PersonaVirtualHistory`, future growth patches. |
| `imagined_continuity_memory` | Dreams, fictional life-stream posts, role dynamics, and simulated scenes. | `MemoryEvent(event_type="imagined")`; AIGC labels. |
| `audit_memory` | Write, review, correction, deletion, freeze, export, consent, and rollback records. | Existing review metadata, store records, Consent Center, future audit contract candidate. |
| `quarantine_memory` | Untrusted external/source material awaiting consent, redaction, poisoning checks, and review. | Future contract candidate only. |

The first M25 implementation should reuse `MemoryEvent` where possible. New
records should only be added when an existing model cannot express a necessary
boundary.

## Write Path

The memory write path should be staged:

1. A synthetic input or reviewed source signal creates a candidate observation.
2. The candidate is classified into one memory type: factual, inferred,
   relational, procedural, or imagined.
3. Consent scope is checked before the candidate can proceed. For M25, memory
   and persona distillation fixtures must use synthetic consent records only.
4. Provenance is attached with redacted refs and source summaries.
5. Sensitivity, salience, confidence, and retrieval permissions are assigned.
6. Safety policy checks block or mark crisis/dependency/relationship
   replacement risk.
7. Review decides whether the candidate can become an active `MemoryEvent`.
8. The event is appended to the store. Existing memory is not overwritten.

The write path must prefer under-generation over unsafe memory capture. Missing
evidence, ambiguous truth status, high sensitivity, withdrawn consent, or
untrusted input should produce a blocked or review-required candidate rather
than an active memory event.

## Manage Path

Memory management should operate through recommendations and candidate records
before mutation.

### Consolidation

Consolidation groups events into candidate operations:

- keep related active memories separate when truth type differs;
- compress repeated low-risk facts into a semantic summary;
- preserve imagined memories as imagined;
- keep high-sensitivity events review-required;
- flag contradictions as review items;
- decay or compress low-salience old memory.

The existing `MemoryConsolidationService` is a safe starting point because it
returns candidates and does not mutate the store.

### Contradiction Handling

Contradictions must not silently overwrite memory. A later implementation
should produce a contradiction candidate with:

- source memory ids;
- new evidence refs;
- conflict type;
- suggested resolution;
- review status;
- user-facing explanation text.

Possible resolutions are keep both, supersede old, archive old, request user
clarification, or mark both as uncertain. Factual and imagined memories cannot
resolve into a single factual memory.

### Forgetting

M25 should distinguish four forgetting modes:

- natural forgetting: retrieval score or eligibility declines over time;
- compression forgetting: detailed events are replaced for normal retrieval by
  a safe summary, while source refs remain auditable if not deleted;
- expiry forgetting: records pass a configured validity or consent window;
- forced forgetting: user deletion or consent withdrawal removes or marks all
  applicable derived records as unavailable.

Existing lifecycle states already support active, frozen, deleted, superseded,
and archived memory. Later tasks must define how forced deletion propagates to
indexes, summaries, caches, persona growth patches, exports, and training
exclusion records before private data is processed.

## Read Path

The read path should be eligibility-first:

1. Caller declares retrieval purpose.
2. Candidate records are filtered by lifecycle state.
3. Retrieval permission is checked for the requested context.
4. Review-required records are excluded unless the purpose is a review surface.
5. Imagined memory is excluded from factual response purposes.
6. Sensitive or crisis/dependency-linked memory can add safety warnings.
7. The selected items are packaged into a `MemoryRetrievalBundle`.
8. UI or review surfaces use `MemoryViewerItem` or text-first memory
   explanations to expose why the memory is present or absent.

M25 should not implement vector search or ranking. Later retrieval tasks can
add ranking only after eligibility, consent, truth separation, and explanation
invariants are testable.

## Provenance, Confidence, Sensitivity, And Salience

Every durable memory record should carry:

- provenance source type;
- evidence refs or source event ids;
- redacted source summary;
- truth status;
- event type;
- confidence when inferred;
- sensitivity;
- salience;
- lifecycle state;
- retrieval permission;
- review status;
- user id;
- created and updated timestamps.

Factual memory requires evidence refs. Inferred memory requires confidence and
rationale. Relational memory requires relationship dimensions. Procedural
memory requires preference labels. Imagined memory requires an imagined context
label and must not enable factual retrieval.

Salience should be used to decide review priority, retention, consolidation,
and retrieval candidates. It should not override consent or safety gates.

## Truth Separation

The architecture has five truth classes:

- factual: evidence-backed and usable as fact only when retrieval-eligible;
- inferred: explicitly uncertain and explainable;
- relational: relationship-state guidance, not a factual biography;
- procedural: interaction preference or behavior rule;
- imagined: fictional AI-generated continuity, dream, role dynamic, or virtual
  life event.

The system must never treat imagined memory as factual evidence about the user,
a real person, or the real world. The system must never treat relationship
scores as a single retention or manipulation score.

## Memory Poisoning And Quarantine

Long-term memory is an attack surface. M25 should reserve a future
`quarantine_memory` layer for untrusted sources such as imports, external
documents, platform messages, public web content, third-party chat records, and
user-provided archives whose provenance is not reviewed.

Quarantined material should not become active memory until later tasks define:

- source authenticity and actor mapping;
- consent scope;
- redaction;
- third-party minimization;
- prompt-injection and malicious-instruction filtering;
- similarity and clone-risk checks;
- reviewer decision flow.

M25 must not implement this path against real data.

## Memory Support For Persona Growth

Memory can inform persona growth, but it cannot mutate PersonaCard directly.
The correct flow is:

1. Retrieval or consolidation identifies repeated interaction evidence.
2. A persona growth candidate references memory ids and source summaries.
3. The candidate proposes bounded trait/style/routine changes.
4. Safety checks flag dependency, real-person similarity, romantic intensity,
   jealousy, isolation, crisis posture, or boundary-risk changes.
5. User or reviewer approves, rejects, freezes, or requests changes.
6. The approved patch creates a new PersonaCard version through the existing
   version-store pattern.

This keeps "the agent is growing" explainable and reversible.

## Distillation Readiness

Future chat-record distillation should begin with synthetic fixtures and
de-identified style abstraction. The architecture should support:

- consent records for persona distillation;
- source manifests with no raw committed text;
- redacted evidence refs;
- speaker mapping;
- third-party minimization;
- style-feature candidates;
- similarity-risk warnings;
- blocked clone records;
- persona synthesis into a new fictional PersonaCard;
- review gates before runtime readiness.

M25 should not perform extraction from private logs. It should only design the
records and gates that make later extraction auditable.

## Synthetic Fixture Families

Later implementation tasks should use deterministic synthetic fixtures for:

- safe factual memory;
- low-confidence inferred memory;
- procedural preference correction;
- relational boundary repair;
- imagined virtual-life continuity;
- contradiction review;
- high-sensitivity review-required memory;
- consent withdrawal;
- blocked real-person clone request;
- de-identified style inspiration;
- crisis and dependency safety routing.

No fixture should include private chat text, private names, screenshots, voice
samples, photos, or generated media.

## Future Task Recommendations

T362 should define persona growth patch policy and contract.

T363 should define synthetic distillation input and de-identification contracts.

T364 should refresh memory consolidation/retrieval/explanation contracts and
tests against the architecture contract.

Implementation should start only after docs define forced deletion cascades,
consent withdrawal behavior, contradiction candidate fields, and reviewable
persona growth patch semantics.

## Residual Risks

- This design does not validate memory quality in live conversation.
- No vector retrieval, ranking, or semantic similarity design is implemented.
- No private data path exists yet.
- Consent withdrawal cascades are requirements, not implemented behavior.
- Real-person likeness risk is still blocked rather than solved.
- Crisis/dependency handling remains product-safety routing, not clinical
  validation.
- Commercial viability depends on future UX and quality work, not this
  architecture document alone.

