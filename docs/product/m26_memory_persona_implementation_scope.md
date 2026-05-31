# M26 Memory Persona Implementation Scope

Task: T370 M26 Scope
Status: worker draft for review

## Objective

M26 begins implementation of the M25 memory, persona growth, and synthetic
distillation contracts.

The milestone should make the safety boundary executable before the project
adds more immersive or sensitive behavior. The first implementation layer is:

```text
synthetic fixtures + local candidate models + deterministic local services + tests
```

M26 is not a private-data, provider, outbound, platform, voice/avatar, media,
or real-person recreation milestone. It should prove that memory governance,
persona growth, and distillation-readiness records preserve consent,
truth-status separation, review gates, user-control semantics, and forbidden
field boundaries under deterministic tests.

## Product Rationale

The long-term companion product needs believable continuity and change. That
requires memory and persona systems that can be trusted when the product later
becomes more immersive.

M26 should therefore focus on three product properties:

- continuity without hidden mutation;
- personalization without real-person replacement;
- immersion without pretending generated or imagined material is factual.

These properties are commercially useful because they support paid companion
features such as durable memory, persona versioning, explainable adaptation,
and safe de-identified style inspiration. They are only defensible if users can
inspect, correct, delete, freeze, approve, reject, roll back, and understand
what happened.

## M25 Invariants To Preserve

M26 implementation must preserve:

- factual, inferred, relational, procedural, and imagined memory separation;
- imagined memory isolation from factual retrieval and real-world evidence;
- append-only memory write posture unless a reviewed lifecycle update path is
  explicitly scoped;
- consolidation as recommendation-only by default;
- contradiction and supersession as review candidates, not silent overwrites;
- consent withdrawal as an auditable cascade-planning trigger;
- review-required exclusion outside review surfaces;
- persona growth as patch candidates that cannot auto-apply;
- stable persona core fields as frozen against memory-driven growth;
- trait delta caps and blocking labels for dependency, crisis, jealousy,
  exclusivity, isolation, guilt, paid intimacy escalation, real-person
  similarity, voice likeness, and avatar likeness;
- distillation as de-identified abstract style inspiration into a new
  fictional persona, not a clone;
- synthetic-only fixtures with no committed private chat text, real account
  ids, source file names, voice samples, images, video, provider metadata,
  platform delivery fields, or generated media paths.

## Implementation Sequence

### T371 Memory Governance Candidate Models

Implement local Pydantic records and deterministic helpers for:

- `MemoryContradictionCandidate`;
- `MemorySupersessionCandidate`;
- `MemoryDeletionCascadePlan`;
- `MemoryExplanationTrace`;
- `PersonaGrowthEvidenceBundle`.

The first code task should prove that these records are review-required,
preserve source memory ids and redacted refs, do not mutate
`MemoryEventStore`, and reject forbidden private/provider/outbound/media
fields.

### T372 Persona Growth Candidate Models

Implement local Pydantic records and deterministic validation for:

- `PersonaGrowthFieldChange`;
- `PersonaGrowthPatchCandidate`;
- `PersonaGrowthPatchReview`;
- `PersonaGrowthJournalEntry`.

Tests should prove that frozen fields cannot be patched, review is always
required, auto-apply is impossible, blocking safety labels block approval,
weekly deltas are capped, jealousy cannot increase by default, and approved
manual apply remains a later task.

### T373 Synthetic Distillation Input Candidate Models

Implement local Pydantic records and deterministic validation for:

- synthetic input manifests;
- source segments;
- speaker aliases;
- consent refs;
- redaction refs;
- de-identified style feature candidates;
- clone-risk decisions;
- fictional persona synthesis input candidates.

Tests should prove speaker aliases replace identities, third parties are
minimized by default, withdrawn consent blocks features, clone-risk flags block
unsafe manifests, feature outputs are abstract labels rather than raw quotes,
and generated persona inputs are never runtime-ready.

### T374 Retrieval And Explanation Integration Tests

Add deterministic tests and local helper logic that connect M25 retrieval and
explanation requirements to existing `MemoryEvent v2`,
`MemoryConsolidationService`, `MemoryRetrievalBundle`, `MemoryViewerItem`, and
text-first chat memory surfaces.

Tests should prove:

- imagined memory cannot enter factual response bundles;
- deleted, frozen, archived, and superseded current-fact memory is excluded;
- review-required memory is excluded outside review surfaces;
- withdrawn-consent memory is excluded or creates a deletion cascade plan;
- contradiction and supersession create candidates rather than store mutation;
- persona-growth evidence bundles do not mutate PersonaCard;
- include and exclude reasons are explainable.

### T375 M26 Milestone Review

Review the code, tests, contracts, and residual risks before any later
milestone expands into retrieval ranking, embeddings, private source readers,
provider-backed extraction, user-facing runtime mutation, proactive candidates,
voice/avatar, media generation, or platform integration.

## Local Synthetic Fixture Strategy

Fixtures should be small and deterministic. Inline test helpers are acceptable
when they keep the fixture visible and obviously synthetic.

Recommended fixture families:

- factual memory that conflicts with a later synthetic factual statement;
- procedural preference correction, such as concise replies;
- imagined continuity memory that must remain fictional;
- high-sensitivity memory requiring review;
- deleted/frozen/archived lifecycle memory;
- withdrawn memory consent;
- persona growth evidence using safe summaries;
- blocked clone-risk style input;
- third-party minimized synthetic speaker;
- crisis/dependency warning labels that block growth.

Fixture text shown in docs or test constants should use `[SYNTHETIC]` markers
when practical. Fixtures must not use real names from private records, private
chat snippets, screenshots, voice samples, photos, generated media, platform
recipient ids, provider metadata, or real source paths.

## Proposed Test Acceptance Gates

Each implementation task should run focused tests plus diff checks. Suggested
minimum commands:

```powershell
$env:PYTHONPATH='src'
python -m py_compile <changed-python-files>
```

```powershell
$env:PYTHONPATH='src'
pytest <focused-test-files> -q
```

```powershell
git diff --check
```

Browser QA is not required in M26 unless a later task explicitly changes a web
UI. No model-provider, network, package-manager, platform, microphone, camera,
or media-generation command should be required.

## Explicit Non-Goals

M26 must not implement or claim:

- private chat ingestion;
- raw private transcript reads;
- source readers for `private/chat_history/` or `private/distilled/`;
- model-provider calls;
- LLM extraction;
- embeddings, vector search, semantic ranking, or fine-tuning;
- de-identification quality guarantees;
- real-person recreation or authorized digital twin support;
- public-figure, ex-partner, family-member, deceased-person, coworker,
  classmate, minor, voice, face, or avatar likeness workflows;
- final companion reply generation;
- runtime memory/persona mutation without review;
- proactive candidate generation;
- automatic sending, scheduling, notifications, queues, webhooks, platform
  adapters, auth, recipient ids, tokens, or delivery state;
- voice, ASR, TTS, voice cloning, microphone capture, generated audio, camera
  capture, face tracking, avatar runtime, Live2D runtime, generated images, or
  generated video;
- public hosting, production persistence, payment flows, analytics, launch
  approval, legal compliance completion, app-store acceptance, clinical
  validation, regulator acceptance, user-study validation, or real user
  evidence.

## M26 Exit Criteria

M26 can close when:

- memory governance candidate records exist and are test-covered;
- persona growth patch candidate records exist and are test-covered;
- synthetic distillation input candidate records exist and are test-covered;
- retrieval/consolidation explanation tests prove lifecycle, consent,
  review-required, and imagined/factual exclusion behavior;
- forbidden private/provider/outbound/platform/media fields are rejected or
  absent in candidate records;
- no private data, provider call, automatic sending, platform delivery,
  voice/avatar runtime, generated media, real-person recreation, launch claim,
  legal claim, clinical claim, or real user evidence has been introduced;
- residual risks are documented before the next milestone.

## Residual Risks

- M26 will still not prove live conversation quality.
- Local deterministic tests cannot validate real de-identification quality,
  semantic retrieval quality, or user trust.
- Consent withdrawal cascade planning will not fully erase future caches or
  indexes until those systems exist.
- Similarity-risk and clone-risk logic will remain conservative and synthetic.
- Persona growth will remain review-first and may feel less spontaneous until
  future UX work makes approval flows ergonomic.
- Voice/avatar, proactive messaging, and virtual social feed behavior remain
  locked or documentation-only until later scoped milestones.
