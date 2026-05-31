# M25 Memory Persona Growth Scope

Task: T360 M25 Scope
Status: worker draft for review

## Objective

M25 defines the next product layer for a transparent, text-first companion
agent: advanced long-term memory, bounded persona growth, and
distillation-ready planning.

The product direction is a humanlike but clearly AI companion object that can
be deeply customized, remember and explain important relationship context,
change in a controlled way over time, and eventually support de-identified
style inspiration from chat records under explicit consent and review gates.

M25 is not a launch, provider, private-data, platform, voice, avatar, or
automatic outreach milestone. It should produce the architecture, contracts,
synthetic fixtures, and safety gates needed before later implementation can
touch sensitive real-world data.

## Product Rationale

The commercial opportunity is not another generic role-chat shell. Competitive
products already advertise long memory, proactive messages, voice, avatar, and
virtual social feeds. The durable differentiation for this project should be:

- explainable persona compilation from detailed, fuzzy, template, or random
  user intent;
- de-identified style inspiration that creates a new AI persona rather than a
  hidden real-person clone;
- relationship memory that tracks boundaries, repair, pacing, shared history,
  and user corrections;
- persona growth that is visible, versioned, reviewable, and reversible;
- user control over memory, persona versions, consent, deletion, freezing,
  export, and training-use separation;
- transparent virtual life-stream content that enriches immersion without
  pretending to be real-world evidence.

This supports a future paid product because users can trust the companion's
continuity and control surfaces. It also keeps the product away from the
higher-risk pitch of replacing, resurrecting, or impersonating a real person.

## Non-Goals

M25 must not implement or claim:

- private chat ingestion;
- real-person recreation or clone support;
- model-provider calls;
- LLM extraction from private logs;
- fine-tuning;
- production persistence beyond explicitly scoped local synthetic fixtures;
- final companion reply generation;
- runtime memory/persona mutation without review gates;
- proactive candidate generation;
- automatic sending, scheduling, notifications, webhooks, queues, tokens, or
  platform delivery;
- voice, ASR, TTS, voice cloning, microphone capture, generated audio, camera
  capture, face tracking, avatar runtime, Live2D runtime, generated images, or
  video;
- public hosting, authentication, app-store readiness, regulator acceptance,
  legal advice, clinical validation, external user-study validation, or launch
  approval.

## Memory Architecture Principles

M25 should treat memory as a governed write-manage-read system rather than an
unbounded vector database.

Required principles:

- Preserve the current `MemoryEvent v2` separation of factual, inferred,
  relational, procedural, and imagined memory.
- Keep factual memory evidence-backed. Factual records need provenance refs and
  must not store raw transcripts.
- Keep imagined and virtual-life memory isolated from factual retrieval.
- Track provenance, confidence, sensitivity, salience, lifecycle state,
  retrieval permission, created time, and source summary on every memory layer.
- Support multiple time horizons: working context, episodic/event memory,
  stable semantic/profile memory, procedural preference memory, relationship
  memory, persona self-memory, and imagined continuity memory.
- Represent contradiction as candidate evidence, not silent overwrite.
- Use consolidation candidates for compression, deduplication, conflict review,
  and decay. Consolidation should recommend changes before any store mutation.
- Support natural forgetting, compression forgetting, expiry, freeze, archive,
  and hard deletion semantics.
- Treat sensitive memory as review-required by default.
- Keep memory retrieval explainable through source refs and memory-use notes.
- Keep external or untrusted inputs in quarantine until a later reviewed
  extraction path defines sanitization, poisoning checks, and consent mapping.

Existing contracts to reuse:

- `docs/data_contracts/memory_event_v2_contract.md`
- `docs/data_contracts/memory_event_store_v2_contract.md`
- `docs/data_contracts/memory_lifecycle_v2_contract.md`
- `docs/data_contracts/memory_consolidation_v2_contract.md`
- `docs/data_contracts/memory_retrieval_bundle_v2_contract.md`
- `docs/data_contracts/memory_viewer_contract.md`
- `docs/data_contracts/text_first_chat_memory_contract.md`

## Persona Growth Principles

Persona growth should simulate continuity and change without uncontrolled drift
or manipulative optimization.

Required principles:

- Preserve a stable core persona: identity disclosure, fictional status,
  source policy, clone block, safety policy, and hard boundaries do not drift.
- Keep mutable persona dimensions explicit: warmth, directness, humor,
  independence, emotional stability, sentence length, topic preferences,
  initiative style, relationship pacing, virtual routine, and current mood.
- Keep short-term mood/state separate from long-term persona traits.
- Keep relationship-state changes separate from persona trait changes.
- Use candidate growth patches with evidence refs, rationale, expected user
  impact, safety warnings, and user/reviewer decision state.
- Cap weekly trait movement. The existing `PersonaGrowthPolicy` cap of `0.2`
  remains the upper bound unless a later task tightens it.
- Require review for romantic intensity, dependency language, real-person
  similarity, jealousy, exclusivity, isolation language, crisis posture,
  boundary risk, proactive behavior, and any change that makes the persona more
  human-deceptive.
- Keep persona versions append-only and rollback-capable.
- Explain changes in user-facing language before applying them in any future
  runtime.
- Never use engagement, retention, paid intimacy escalation, or emotional
  pressure as a growth objective.

Existing contracts to reuse:

- `docs/data_contracts/persona_card_v1_contract.md`
- `docs/data_contracts/persona_compiler_contract.md`
- `docs/data_contracts/persona_review_card_contract.md`
- `docs/data_contracts/persona_version_store_contract.md`
- `docs/data_contracts/persona_version_editor_contract.md`
- `docs/data_contracts/relationship_state_contract.md`
- `docs/data_contracts/relationship_context_bundle_contract.md`

## Distillation-Readiness Principles

M25 should prepare for eventual chat-record distillation without performing it.
The near-term product stance is de-identified style inspiration and relationship
pattern modeling, not real-person replacement.

Required principles:

- Use synthetic fixtures first. No private chat logs, private distilled
  artifacts, or real private transcripts may be read in M25.
- Separate source ingestion, redaction, feature extraction, style abstraction,
  persona synthesis, similarity risk scoring, and review decisions.
- Store redacted evidence references and source summaries, not raw source text.
- Support speaker mapping and third-party minimization in the future contract.
- Require explicit consent for `persona_distillation` and separate consent for
  any later voice/avatar modality.
- Treat ex-partner, family-member, deceased-person, public-figure, coworker,
  classmate, minor, and other identifiable real-person requests as high-risk or
  blocked unless a future task creates a stricter authorized path.
- Produce a new fictional persona by default. The generated persona must not
  keep the real person's name, face, voice, exact biographical history, unique
  private phrases, or hidden source identity.
- Include clone-risk and similarity-risk warnings before any approval path.
- Keep distillation outputs review-required and non-runtime-ready until human
  review approves a safe L1 or L2 result.

## Consent And User-Control Requirements

M25 design must preserve the Consent Center separation of scopes:

- `memory`
- `persona_distillation`
- `proactive_messaging`
- `aigc_export_share`
- `voice_avatar`
- `analytics`
- `model_improvement`
- `payment_marketing`

Required user controls:

- inspect memory by type, truth status, source refs, sensitivity, lifecycle,
  and retrieval permission;
- edit, correct, pin, suppress, freeze, archive, delete, and export memory;
- inspect and roll back persona versions;
- approve, reject, freeze, or request changes to persona growth patches;
- withdraw consent per feature scope;
- request access, correction, deletion, export, withdrawal, or objection
  records through `DataRightsRequestRecord`;
- see AIGC labels for generated persona, companion reply, virtual history,
  role dynamic post, export, shared content, and web demo surfaces;
- understand when content is factual evidence, inference, procedure, relation,
  or imagined AI-generated continuity.

Consent withdrawal must supersede previous grants for the same feature scope.
Later implementation must define how withdrawal cascades through derived
memory, persona patches, embeddings, caches, summaries, exports, and training
exclusion records before private data is processed.

## Synthetic Fixture Strategy

M25 fixtures should be small, local, deterministic, and obviously synthetic.

Recommended fixture families:

- safe fictional persona with stable core and mutable style preferences;
- fuzzy user preference that gradually converges through reviewed patches;
- contradiction fixture where a new statement conflicts with old memory;
- user correction fixture that updates a procedural preference;
- imagined virtual-life memory that must never become factual evidence;
- sensitive memory fixture that defaults to review-required;
- consent withdrawal fixture for memory and persona distillation scopes;
- blocked real-person recreation request;
- de-identified style inspiration fixture with no names, voices, faces, or raw
  private messages;
- grief, ex-partner, family-member, public-figure, dependency, and crisis risk
  fixtures using generic synthetic labels only.

Fixtures must not use committed private chat text, real names from private
records, voice samples, photos, screenshots, or generated media.

## Safety Boundaries

### Real-Person Likeness

M25 keeps real-person recreation blocked. Any request to recreate a specific
person by name, face, voice, biography, chat history, or private speech pattern
must become a blocked or transformed review record. The safe transformation is
an original fictional persona inspired only by broad, de-identified traits.

### Grief And Deceased People

Deceased-person resurrection remains out of scope. M25 may plan memorial-safe
future boundaries only as documentation. It must not create a persona that
claims to be, speaks as, or appears as a deceased person.

### Ex-Partner And Family Member

Ex-partner and family-member clone requests remain blocked because they combine
third-party privacy, dependency, grief, coercion, and relationship replacement
risk. Later work may support de-identified style abstraction only if consent,
redaction, similarity risk, and user-facing warnings are in place.

### Public Figure

Public-figure clone requests remain blocked. M25 should avoid persona outputs
that combine recognizable names, careers, events, voices, faces, or highly
specific biographies into a public-person likeness.

### Dependency

Memory and persona growth must not optimize for exclusivity, jealousy,
isolation, guilt, paid intimacy escalation, or "only I understand you" language.
Dependency signals should de-escalate or block review flows, and proactive
outreach remains non-sending.

### Crisis

Crisis and self-harm signals must route to the existing review-first
`CompanionSafetyPolicy` posture. M25 must not generate clinical scripts,
emergency dispatch, location-specific crisis routing, or normal romantic
escalation under crisis risk.

### Minors

Minor access remains not enabled by default. Minor or guardian consent states
may be represented only as synthetic contract fixtures until later policy work
defines product eligibility.

## Recommended M25 Task Sequence

1. T361: Memory architecture design.
2. T362: Persona growth policy and patch contract.
3. T363: Synthetic distillation input and de-identification planning.
4. T364: Memory consolidation, retrieval, and explanation contract refresh.
5. T365: M25 milestone review.

This sequence designs the memory substrate first, then controlled persona
change, then distillation readiness, then retrieval/consolidation details, and
finally a review gate before implementation expands to sensitive workflows.

## M25 Exit Criteria

M25 can close when:

- memory architecture layers, lifecycle, retrieval, provenance, sensitivity,
  salience, decay, contradiction, and user-control requirements are documented;
- persona growth has a bounded patch/review/versioning policy;
- distillation readiness has synthetic input, consent, redaction, third-party,
  and clone-risk boundaries;
- synthetic fixtures cover safe, contradictory, sensitive, imagined,
  withdrawal, and blocked-real-person scenarios;
- next implementation tasks do not require private data or provider calls;
- residual risks are documented without claiming legal, clinical, launch, or
  user-study validation.

