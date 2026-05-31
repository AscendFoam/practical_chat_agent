# Memory Retrieval Consolidation Refresh Contract

Task: T364 Memory Retrieval Consolidation Refresh
Status: worker draft for review

## Scope

This contract refreshes memory consolidation, retrieval, and explanation
requirements for M25. It is documentation-only. It does not implement new
models, tests, services, stores, ranking, vector search, embeddings, dialogue
runtime, private data ingestion, persona mutation, or platform behavior.

Existing authoritative contracts:

- `MemoryEvent v2`
- `MemoryLifecyclePolicyService`
- `MemoryConsolidationService`
- `MemoryRetrievalBundle`
- `MemoryViewerItem`
- `TextFirstChatMemoryPrototype`
- `ConsentCenterState`
- `PersonaGrowthPatchContract`
- `SyntheticDistillationInputContract`
- `CompanionSafetyPolicy`

Future model names in this document are contract candidates only.

## Future Candidate Records

### MemoryContradictionCandidate

Candidate fields:

| Field | Meaning |
| --- | --- |
| `schema_version` | Future value: `memory_contradiction_candidate_v1`. |
| `candidate_id` | Generated local id. |
| `user_id` | Owner user id. |
| `memory_ids` | Existing memory ids in conflict. |
| `new_evidence_refs` | Redacted refs for new evidence. |
| `conflict_type` | `fact_conflict`, `preference_change`, `relationship_change`, `source_dispute`, or `imagined_fact_boundary`. |
| `safe_summary` | Safe summary of the conflict. |
| `proposed_resolution` | `keep_both`, `supersede_old`, `archive_old`, `request_clarification`, or `reject_new`. |
| `review_required` | Always true. |
| `safety_warnings` | Warning labels. |

### MemorySupersessionCandidate

Candidate fields:

| Field | Meaning |
| --- | --- |
| `schema_version` | Future value: `memory_supersession_candidate_v1`. |
| `candidate_id` | Generated local id. |
| `source_memory_id` | Memory proposed to become superseded. |
| `replacement_memory_id` | Proposed replacement memory. |
| `reason` | Safe reason summary. |
| `review_required` | Always true. |
| `applies_lifecycle_update` | Always false until a future reviewed apply path. |

### MemoryDeletionCascadePlan

Candidate fields:

| Field | Meaning |
| --- | --- |
| `schema_version` | Future value: `memory_deletion_cascade_plan_v1`. |
| `plan_id` | Generated local id. |
| `user_id` | Owner user id. |
| `trigger_type` | `user_delete`, `consent_withdrawal`, `data_rights_request`, or `safety_block`. |
| `target_memory_ids` | Source memory ids affected. |
| `affected_artifact_refs` | Retrieval, viewer, persona patch, distillation, export, cache, or index refs. |
| `recommended_actions` | `delete`, `freeze`, `archive`, `suppress_retrieval`, or `training_exclusion`. |
| `review_required` | Always true. |
| `completed` | Always false in candidate contract. |

### MemoryExplanationTrace

Candidate fields:

| Field | Meaning |
| --- | --- |
| `schema_version` | Future value: `memory_explanation_trace_v1`. |
| `trace_id` | Generated local id. |
| `memory_id` | Source memory id. |
| `surface` | `viewer`, `chat_review`, `retrieval_bundle`, `persona_growth_patch`, or `distillation_review`. |
| `included` | Whether memory was included. |
| `reason` | Safe include/exclude reason. |
| `provenance_refs` | Redacted source refs. |
| `truth_status` | Source truth status. |
| `safety_warnings` | Warning labels. |

### PersonaGrowthEvidenceBundle

Candidate fields:

| Field | Meaning |
| --- | --- |
| `schema_version` | Future value: `persona_growth_evidence_bundle_v1`. |
| `bundle_id` | Generated local id. |
| `persona_id` | Target persona id. |
| `memory_ids` | Memory ids supporting a future growth patch. |
| `safe_summaries` | Safe summaries only. |
| `blocked_memory_ids` | Memory ids excluded from growth evidence. |
| `exclusion_reasons` | Exclusion reasons. |
| `review_required` | Always true. |

## Consolidation Requirements

Consolidation candidates must:

- preserve event type;
- preserve truth status;
- preserve source memory ids;
- preserve provenance refs;
- keep imagined memory separate;
- emit review candidates for sensitive or review-required memory;
- emit decay/compress recommendations without mutation;
- emit contradiction candidates instead of overwriting;
- emit supersession candidates instead of direct lifecycle updates;
- emit deletion cascade plans when triggered by deletion or consent withdrawal.

Consolidation candidates must not:

- merge imagined memory into factual memory;
- merge private source text into summaries;
- apply lifecycle updates;
- write stores;
- mutate PersonaCard;
- create proactive candidates;
- call providers;
- send or schedule messages.

## Retrieval Bundle Requirements

Retrieval bundles must:

- declare purpose;
- include only lifecycle-eligible memory unless review purpose explicitly
  allows otherwise;
- exclude review-required memory outside review surfaces;
- exclude imagined memory from factual response purposes;
- preserve event type, truth status, sensitivity, lifecycle, and provenance;
- record selected memory ids;
- record excluded memory ids when known;
- record exclusion reasons when known;
- carry safety warnings;
- carry consent-withdrawal warnings when applicable.

Retrieval bundles must not contain:

- raw private text;
- full transcripts;
- media paths;
- provider metadata;
- platform delivery fields;
- send/schedule/queue/webhook/token fields;
- persona mutation payloads.

## Explanation Surface Requirements

Viewer, chat review, retrieval, persona growth, and distillation review
surfaces should expose:

- memory id;
- event type;
- truth status;
- summary;
- provenance refs;
- lifecycle state;
- retrieval eligibility;
- review-required state;
- sensitivity;
- factual-evidence flag;
- imagined-memory flag;
- include/exclude reason;
- safety notes;
- available user controls.

User controls may be represented as metadata until implementation exists:

- edit;
- correct;
- freeze;
- delete;
- archive;
- export;
- withdraw consent.

## Consent Withdrawal Requirements

Any future retrieval or consolidation path must treat withdrawn consent as:

- not retrieval-eligible;
- review-required;
- excluded from persona-growth evidence;
- excluded from distillation feature generation;
- requiring deletion cascade planning before further use.

Consent withdrawal must not be reduced to "do not mention it in the prompt."

## Persona Growth Evidence Requirements

Memory used for persona growth must:

- be active or explicitly review-included;
- have valid provenance;
- be represented by safe summaries;
- preserve truth status;
- not be imagined unless the patch only affects fictional virtual continuity;
- not include crisis/dependency/real-person-likeness warnings unless the patch
  is blocked or review-only.

Persona growth evidence bundles must not mutate PersonaCard.

## Distillation Readiness Requirements

Synthetic de-identified style features may appear as review-only evidence only
when:

- source manifest is synthetic;
- clone-risk decision allows L2 review;
- consent refs are present and active in the fixture;
- features are abstract labels, not raw quotes;
- output intent remains a new fictional persona.

Any blocked clone-risk flag excludes the feature from retrieval or growth use.

## Forbidden Fields And Surfaces

Refresh records must not contain:

- raw private chat text;
- full transcripts;
- private screenshots;
- real source file names;
- real message ids;
- real account ids;
- voice samples;
- audio bytes;
- images;
- videos;
- generated media paths;
- provider credentials;
- platform recipient ids;
- send queues;
- schedules;
- webhooks;
- tokens;
- delivery state;
- microphone or camera prompts;
- clinical scripts;
- real-person clone payloads.

## Acceptance Criteria For Later Code/Test Tasks

Later implementation should be accepted only if tests prove:

- imagined memory cannot enter factual response bundles;
- deleted/frozen/archived memory is excluded;
- review-required memory is excluded outside review purposes;
- withdrawn-consent memory is excluded or produces a cascade plan;
- contradiction creates a candidate and does not overwrite;
- supersession creates a candidate and does not mutate lifecycle directly;
- persona growth evidence does not mutate PersonaCard;
- synthetic distillation features remain review-only;
- forbidden private/provider/outbound/media/platform fields are absent;
- explanation surfaces expose include/exclude reasons.

## Non-Actions

T364 does not implement:

- Python models;
- services;
- tests;
- stores;
- retrieval ranking;
- vector search;
- embeddings;
- LLM calls;
- private chat-log reads;
- dialogue runtime;
- persona mutation;
- proactive candidates;
- sending or scheduling;
- platform integration;
- voice/avatar/video behavior;
- legal, clinical, launch, app-store, or regulator approval.

