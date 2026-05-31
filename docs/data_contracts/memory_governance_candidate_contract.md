# Memory Governance Candidate Contract

Task: T371 Memory Governance Candidate Models
Status: worker draft for review

## Scope

This contract describes the implemented local memory-governance candidate
records in `src/practical_chat_agent/services/memory_governance.py`.

The records are review-first, synthetic-friendly, and deterministic. They do
not implement memory store mutation, retrieval ranking, vector search,
embeddings, source ingestion, private chat parsing, model-provider calls,
dialogue generation, persona mutation, proactive messaging, platform delivery,
voice/avatar runtime, media generation, or real-person recreation.

## Implemented Records

### MemoryContradictionCandidate

Implementation:

- `practical_chat_agent.services.memory_governance.MemoryContradictionCandidate`

Fields:

| Field | Meaning |
| --- | --- |
| `schema_version` | Always `memory_contradiction_candidate_v1`. |
| `candidate_id` | Generated `memctr_` id. |
| `user_id` | Owner user id. |
| `memory_ids` | Two or more memory ids in conflict. |
| `new_evidence_refs` | Redacted refs for new evidence. |
| `conflict_type` | `fact_conflict`, `preference_change`, `relationship_change`, `source_dispute`, or `imagined_fact_boundary`. |
| `safe_summary` | Safe summary of the conflict. |
| `proposed_resolution` | `keep_both`, `supersede_old`, `archive_old`, `request_clarification`, or `reject_new`. |
| `review_required` | Always true. |
| `safety_warnings` | Machine-readable warnings. |
| `created_at` | Creation timestamp. |

Helper:

- `from_events(...)`

Required invariant:

- the candidate requires at least two source memory ids;
- the candidate cannot set `review_required=false`.

### MemorySupersessionCandidate

Implementation:

- `practical_chat_agent.services.memory_governance.MemorySupersessionCandidate`

Fields:

| Field | Meaning |
| --- | --- |
| `schema_version` | Always `memory_supersession_candidate_v1`. |
| `candidate_id` | Generated `memsup_` id. |
| `source_memory_id` | Existing memory proposed to become superseded. |
| `replacement_memory_id` | Proposed replacement memory id. |
| `reason` | Safe reason summary. |
| `review_required` | Always true. |
| `applies_lifecycle_update` | Always false. |
| `created_at` | Creation timestamp. |

Helper:

- `from_memory_ids(...)`

Required invariant:

- the candidate must not apply lifecycle updates directly;
- `MemoryEventStore` remains unchanged by creating the candidate.

### MemoryDeletionCascadePlan

Implementation:

- `practical_chat_agent.services.memory_governance.MemoryDeletionCascadePlan`

Fields:

| Field | Meaning |
| --- | --- |
| `schema_version` | Always `memory_deletion_cascade_plan_v1`. |
| `plan_id` | Generated `memdel_` id. |
| `user_id` | Owner user id. |
| `trigger_type` | `user_delete`, `consent_withdrawal`, `data_rights_request`, or `safety_block`. |
| `target_memory_ids` | Source memory ids affected. |
| `affected_artifact_refs` | Retrieval, viewer, persona patch, distillation, export, cache, index, or audit refs. |
| `recommended_actions` | `delete`, `freeze`, `archive`, `suppress_retrieval`, or `training_exclusion`. |
| `review_required` | Always true. |
| `completed` | Always false. |
| `created_at` | Creation timestamp. |

Helper:

- `for_consent_withdrawal(...)`

Required invariant:

- consent withdrawal plans recommend `suppress_retrieval` and
  `training_exclusion`;
- plans are candidates and cannot be completed by this model.

### MemoryExplanationTrace

Implementation:

- `practical_chat_agent.services.memory_governance.MemoryExplanationTrace`

Fields:

| Field | Meaning |
| --- | --- |
| `schema_version` | Always `memory_explanation_trace_v1`. |
| `trace_id` | Generated `memxpl_` id. |
| `memory_id` | Source memory id. |
| `surface` | `viewer`, `chat_review`, `retrieval_bundle`, `persona_growth_patch`, or `distillation_review`. |
| `included` | Whether the memory was included. |
| `reason` | Safe include or exclude reason. |
| `provenance_refs` | Redacted source refs. |
| `truth_status` | Source memory truth status. |
| `safety_warnings` | Warning labels. |
| `created_at` | Creation timestamp. |

Helpers:

- `included_from_event(...)`
- `excluded_from_event(...)`

Required invariant:

- traces expose include/exclude reasons and redacted refs without raw source
  text.

### PersonaGrowthEvidenceBundle

Implementation:

- `practical_chat_agent.services.memory_governance.PersonaGrowthEvidenceBundle`

Fields:

| Field | Meaning |
| --- | --- |
| `schema_version` | Always `persona_growth_evidence_bundle_v1`. |
| `bundle_id` | Generated `pgeb_` id. |
| `persona_id` | Target persona id. |
| `evidence_purpose` | `factual_persona_growth`, `virtual_continuity_growth`, or `review_only`. |
| `memory_ids` | Included memory ids. |
| `safe_summaries` | Safe summary by memory id. |
| `blocked_memory_ids` | Excluded memory ids. |
| `exclusion_reasons` | Exclusion reason by memory id. |
| `review_required` | Always true. |
| `safety_warnings` | Deduplicated warning labels. |
| `created_at` | Creation timestamp. |

Helper:

- `from_events(...)`

Required invariants:

- imagined memory is blocked for `factual_persona_growth`;
- inactive memory is blocked;
- review-required memory is blocked;
- dependency, crisis, real-person similarity, voice/avatar likeness, and other
  blocking labels exclude the memory from normal growth evidence;
- the bundle does not mutate `PersonaCard` or any persona version store.

## Shared Invariants

All implemented records:

- use `extra="forbid"`;
- use local generated ids;
- preserve redacted refs and safe summaries only;
- are review-first candidates;
- do not write stores;
- do not call providers;
- do not contain outbound delivery state;
- do not contain media payloads;
- do not expose runtime delivery methods such as send, schedule, deliver,
  webhook, or provider calls.

## Forbidden Fields And Surfaces

The implemented models must not contain:

- raw private chat text;
- full transcripts;
- private screenshots;
- real source file names;
- real message ids;
- real account ids;
- voice samples;
- audio bytes;
- image bytes;
- video bytes;
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

## Tests

Implemented tests:

- `tests/test_memory_governance_candidates.py`

Covered behavior:

- contradiction candidates are review-required and preserve source memory ids;
- single-memory contradiction candidates are rejected;
- supersession candidates do not update `MemoryEventStore`;
- consent withdrawal plans are review-required and not completed;
- explanation traces expose include/exclude reasons and provenance refs;
- persona-growth evidence bundles block imagined factual evidence;
- dependency and real-person similarity warnings block growth evidence;
- models reject extra private/provider/outbound/media fields;
- candidates do not expose runtime or delivery methods.

## Verification

Expected minimum verification:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\services\memory_governance.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_memory_governance_candidates.py tests\test_memory_event_schema.py tests\test_memory_consolidation_v2.py -q -o cache_dir=artifacts\t371_pytest_cache --basetemp=artifacts\t371_pytest_basetemp
```

```powershell
git diff --check
```

## Non-Actions

T371 does not implement:

- private data ingestion;
- source readers;
- extraction;
- embeddings;
- vector search;
- retrieval ranking;
- similarity scoring;
- model-provider calls;
- storage mutation;
- final companion reply generation;
- persona mutation;
- proactive candidates;
- automatic sending or scheduling;
- platform integration;
- voice/avatar/video behavior;
- generated media;
- legal, clinical, launch, app-store, or regulator approval.

## Residual Risks

- The models are candidate records only; they do not execute deletion,
  supersession, correction, or consent cascade actions.
- No live retrieval quality, semantic similarity, de-identification quality, or
  long-context memory evaluation is implemented.
- Persona growth evidence remains review-only until T372 defines growth patch
  records.
- Synthetic tests do not validate real-world private-data handling.
