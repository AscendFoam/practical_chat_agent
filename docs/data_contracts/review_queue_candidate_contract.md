# Review Queue Candidate Contract

Task: T377 Review Queue Candidate Models
Status: worker draft for review

## Scope

This contract describes the implemented local review queue records in
`src/practical_chat_agent/services/review_queue.py`.

The records wrap existing M26 candidate artifacts into reviewable queue items
and snapshots. They do not apply decisions, mutate memory stores, write persona
versions, call providers, read private data, generate replies, send messages,
create UI, connect to platform delivery, enable voice/avatar runtime, generate
media, or recreate real people.

## Implemented Records

### ReviewQueueItem

Implementation:

- `practical_chat_agent.services.review_queue.ReviewQueueItem`

Fields:

| Field | Meaning |
| --- | --- |
| `schema_version` | Always `review_queue_item_v1`. |
| `item_id` | Generated `rqitem_` id. |
| `candidate_kind` | Candidate family wrapped by the item. |
| `candidate_id` | Source candidate id. |
| `source_schema_version` | Source record schema version when available. |
| `owner_user_id` | Optional owner user id. |
| `persona_id` | Optional persona id. |
| `title` | Safe display title. |
| `safe_summary` | Safe display summary. |
| `reason_labels` | Review reason labels and risk labels. |
| `source_refs` | Redacted source refs and candidate ids. |
| `priority_score` | Deterministic score from 0 to 100. |
| `priority_band` | `critical`, `high`, `normal`, or `low`. |
| `review_required` | Always true. |
| `review_status` | `queued` by default. |
| `blocks_auto_apply` | Always true. |
| `candidate_created_at` | Source candidate timestamp when available. |
| `created_at` | Queue item creation timestamp. |

Required invariants:

- review is always required;
- auto-apply is always blocked;
- reason labels and source refs are deduplicated;
- extra fields are forbidden.

### ReviewQueueSnapshot

Implementation:

- `practical_chat_agent.services.review_queue.ReviewQueueSnapshot`

Fields:

| Field | Meaning |
| --- | --- |
| `schema_version` | Always `review_queue_snapshot_v1`. |
| `snapshot_id` | Generated `rqsnap_` id. |
| `items` | Queue items sorted by priority and timestamp. |
| `counts_by_kind` | Counts by candidate kind. |
| `high_priority_item_ids` | Items with priority score at least 70. |
| `review_required` | Always true. |
| `generated_at` | Snapshot timestamp. |

Helper:

- `from_items(...)`

### ReviewQueueDecisionRecord

Implementation:

- `practical_chat_agent.services.review_queue.ReviewQueueDecisionRecord`

Fields:

| Field | Meaning |
| --- | --- |
| `schema_version` | Always `review_queue_decision_record_v1`. |
| `decision_id` | Generated `rqdec_` id. |
| `item_id` | Reviewed queue item id. |
| `candidate_kind` | Source candidate family. |
| `candidate_id` | Source candidate id. |
| `reviewer_id` | Reviewer id. |
| `decision` | `approve`, `reject`, `freeze`, or `request_changes`. |
| `decision_notes` | Safe reviewer notes. |
| `applies_changes` | Always false. |
| `writes_memory_store` | Always false. |
| `writes_persona_version` | Always false. |
| `decided_at` | Decision timestamp. |

Required invariants:

- decision records cannot apply changes;
- decision records cannot write memory stores;
- decision records cannot write persona versions.

### ReviewQueueService

Implementation:

- `practical_chat_agent.services.review_queue.ReviewQueueService`

Methods:

| Method | Behavior |
| --- | --- |
| `item_from_candidate(candidate)` | Wraps supported M26 candidates as queue items. |
| `build_snapshot(items)` | Sorts items and computes queue counts. |
| `record_decision(item, ...)` | Creates review-only decision records. |

Supported candidate families:

- `MemoryContradictionCandidate`
- `MemorySupersessionCandidate`
- `MemoryDeletionCascadePlan`
- `PersonaGrowthEvidenceBundle`
- `PersonaGrowthPatchCandidate`
- `SyntheticDistillationInputManifest`
- `DeidentifiedStyleFeatureCandidate`
- `MemoryRetrievalExplanationResult`

## Priority Behavior

Priority is deterministic and local:

| Candidate | Priority behavior |
| --- | --- |
| Consent/data-rights deletion cascade | Critical, score 100. |
| Other deletion cascade | Critical, score 90. |
| Memory contradiction | High, score 70 or 80 with warnings. |
| Memory supersession | High, score 75. |
| Persona-growth patch with blocking labels | High, score 85. |
| Persona-growth patch without blocking labels | Normal, score 60. |
| Persona-growth evidence with blocked memory | High, score 70. |
| Synthetic distillation manifest with blocking reasons | Critical, score 90. |
| Synthetic distillation manifest without blocking reasons | Normal, score 55. |
| Blocked de-identified style feature | High, score 80. |
| Routine de-identified style feature | Low, score 45. |
| Retrieval explanation with deletion cascade | High, score 85. |
| Retrieval explanation with safety warnings | High, score 70. |
| Routine retrieval explanation | Low, score 40. |

Snapshots sort by descending priority, then source timestamp, then item id.

## Forbidden Fields And Surfaces

The implemented records must not contain:

- raw private chat text;
- raw transcripts;
- private message bodies;
- provider credentials;
- platform recipient ids;
- send queues;
- schedules;
- webhooks;
- tokens;
- delivery state;
- microphone, camera, audio, image, or video payloads;
- runtime reply-generation methods;
- mutation/apply methods;
- voice/avatar/media generation methods.

## Tests

Implemented tests:

- `tests/test_review_queue_candidates.py`

Covered behavior:

- memory governance candidates can be wrapped with priority and source refs;
- persona-growth patch, synthetic distillation manifest, style feature, and
  retrieval explanation records can be wrapped;
- snapshots put deletion/high-risk items before routine items;
- decision records do not apply changes;
- queue items reject extra private/provider/outbound/media fields;
- service exposes no runtime, delivery, provider, mutation, voice/avatar, or
  media methods.

## Verification

Expected minimum verification:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\services\review_queue.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_review_queue_candidates.py tests\test_memory_governance_candidates.py tests\test_persona_growth_candidates.py tests\test_synthetic_distillation_input_candidates.py -q -o cache_dir=artifacts\t377_pytest_cache --basetemp=artifacts\t377_pytest_basetemp
```

```powershell
git diff --check
```

## Non-Actions

T377 does not implement:

- private data ingestion;
- source readers;
- extraction from real logs;
- embeddings;
- vector search;
- semantic ranking;
- similarity scoring;
- model-provider calls;
- final companion reply generation;
- runtime memory or persona mutation;
- decision apply paths;
- review UI;
- proactive candidates;
- automatic sending or scheduling;
- platform integration;
- voice/avatar/video behavior;
- generated media;
- legal, clinical, launch, app-store, or regulator approval.

## Residual Risks

- Queue items are local records only; no user-facing review UI exists.
- Decision records do not execute approved changes.
- Priority is conservative and rule-based; it is not a learned risk model.
- T378 still needs dry-run planning for memory lifecycle decisions.
