# Memory Retrieval Consolidation Refresh

Task: T364 Memory Retrieval Consolidation Refresh
Status: worker draft for review

## Objective

This note refreshes memory consolidation, retrieval, and explanation
requirements against the M25 architecture.

The goal is to make later implementation testable before any runtime memory
quality work expands. The refresh keeps the system local, synthetic,
review-first, typed by truth status, and closed to private data.

## Architecture Alignment Summary

Existing contracts already provide safe building blocks:

- `MemoryEvent v2` separates factual, inferred, relational, procedural, and
  imagined memory.
- `MemoryLifecyclePolicyService` returns recommendations without mutation.
- `MemoryConsolidationService` produces candidates and keeps imagined memory
  separate.
- `MemoryRetrievalBundle` packages already-selected memory and rejects
  imagined memory in factual response bundles.
- `MemoryViewerItem` explains memory state, retrieval eligibility, and user
  controls.
- `TextFirstMemoryExplanation` preserves truth status, provenance refs, and
  imagined/factual separation in the chat review surface.

M25 adds requirements around contradiction, consent withdrawal, persona growth
evidence, and de-identified distillation readiness.

## Consolidation Refresh Requirements

Consolidation should remain recommendation-only.

Required behavior:

- group memory only within compatible event types and truth statuses;
- keep imagined memory isolated through `separate_imagined`;
- never merge imagined memory into factual, inferred, relational, or procedural
  records;
- emit review candidates for medium/high sensitivity and review-required
  memory;
- emit contradiction candidates rather than overwriting old records;
- support supersession only through review;
- preserve source memory ids and provenance refs;
- produce decay/compress recommendations for low-salience old memory;
- emit deletion/withdrawal cascade plans rather than silently removing derived
  records;
- exclude quarantined or untrusted input from active consolidation.

Recommended future candidate records:

- `MemoryContradictionCandidate`
- `MemorySupersessionCandidate`
- `MemoryDeletionCascadePlan`
- `MemoryConsentWithdrawalImpact`

These are not implemented in T364.

## Retrieval Refresh Requirements

Retrieval should remain eligibility-first. Ranking can come later.

Required retrieval gates:

1. Requested purpose is declared.
2. Consent scope is active.
3. Lifecycle state is eligible.
4. Retrieval permission allows the requested context.
5. Review-required records are excluded unless purpose is review.
6. Imagined memory is excluded from factual response purposes.
7. Crisis, dependency, clone-risk, withdrawn-consent, and high-sensitivity
   warnings are preserved.
8. Selected and excluded ids are recorded.
9. Exclusion reasons are explainable.

`MemoryRetrievalBundle` should remain the packaging boundary. Later
implementation may add selection/ranking before bundle creation, but the
bundle must remain free of raw transcripts, delivery state, provider metadata,
or media payloads.

## Explanation Surface Requirements

Every review or user-facing memory surface should answer:

- what was remembered;
- whether it is factual, inferred, relational, procedural, or imagined;
- where it came from through redacted refs;
- why it is visible;
- whether it is retrieval-eligible;
- why it was excluded when applicable;
- whether review, sensitivity, crisis, dependency, clone-risk, or consent
  warnings apply;
- what the user can do next: edit, correct, delete, freeze, archive, export,
  or withdraw consent.

`MemoryViewerItem` and `TextFirstMemoryExplanation` already support much of
this. Later implementation should add explicit exclusion/explanation traces
before any runtime dialogue uses selected memory.

## Contradiction And Supersession Handling

Contradictions are normal in long-running companion memory. They must not be
treated as corruption, and they must not be silently overwritten.

Required future flow:

1. New evidence conflicts with existing memory.
2. A contradiction candidate records source memory ids, new evidence refs,
   conflict type, and safe summaries.
3. Reviewer or user chooses keep both, supersede old, archive old, request
   clarification, or reject new evidence.
4. Supersession creates a new record or lifecycle update while preserving
   audit history.
5. Retrieval excludes superseded current-fact candidates unless purpose is
   review or audit.

Imagined and factual memory cannot resolve into one factual record.

## Consent Withdrawal And Deletion Cascade

Consent withdrawal should not merely hide memory in prompts. It should produce
an auditable impact plan.

Future deletion cascade plans should consider:

- source memory events;
- retrieval bundles;
- viewer pages;
- chat explanation surfaces;
- consolidation candidates;
- contradiction candidates;
- persona growth patches;
- synthetic distillation feature candidates;
- exports;
- caches and indexes if later introduced;
- training/model-improvement exclusion records if later introduced.

Until this is implemented, withdrawn-consent memory must be treated as not
retrieval-eligible and review-required.

## Persona-Growth Evidence Boundary

Memory can support persona growth only as evidence.

Allowed:

- a growth patch references memory ids;
- a growth patch quotes safe summaries, not raw source text;
- relationship memory informs pacing or boundary warnings;
- procedural memory informs speech-style preference patches.

Forbidden:

- memory consolidation mutates PersonaCard directly;
- retrieval bundle applies growth patches;
- imagined memory justifies factual identity changes;
- dependency or crisis memory increases intimacy, exclusivity, jealousy, or
  proactive behavior;
- real-person likeness memory creates clone drift.

## Distillation-Readiness Boundary

Memory refresh must support future de-identified style work without allowing
private data now.

Allowed:

- synthetic style feature ids can be referenced as future evidence;
- clone-risk warnings can be carried into retrieval/explanation surfaces;
- de-identified style features can remain review-required.

Forbidden:

- raw private chat text;
- real source file paths;
- speaker names or account ids;
- direct use of private-chat segments as memory;
- generation of a real-person persona;
- voice/avatar likeness.

## Synthetic Fixture Recommendations

Later code/test tasks should include fixtures for:

- factual event included in factual bundle;
- imagined event excluded from factual bundle;
- inferred memory with confidence and rationale;
- procedural preference correction;
- relational boundary repair;
- medium/high sensitivity review exclusion;
- frozen/deleted/archived lifecycle exclusion;
- contradiction candidate creation;
- supersession review candidate;
- consent withdrawal impact;
- persona growth evidence bundle;
- synthetic de-identified style feature as review-only evidence;
- crisis/dependency safety warning preservation.

## Residual Risks

- T364 does not implement code or tests.
- Existing MemoryRetriever legacy contracts still use older `MemoryFact`
  shapes; later work should bridge legacy approved-store retrieval to
  `MemoryEvent v2` carefully.
- No ranking, vector search, semantic similarity, or long-context evaluation is
  implemented here.
- Consent withdrawal cascade is a requirement, not runtime behavior.
- Contradiction/supersession candidates are not implemented.
- No live companion quality, user research, legal validation, or launch
  readiness is claimed.

