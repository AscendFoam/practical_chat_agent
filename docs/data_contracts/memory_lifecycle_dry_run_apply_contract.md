# Memory Lifecycle Dry-Run Apply Contract

Task: T378 Memory Lifecycle Dry-Run Apply Plans
Status: worker draft for review

## Scope

This contract describes the implemented preview-only memory lifecycle dry-run
records in `src/practical_chat_agent/services/memory_lifecycle_dry_run.py`.

The records turn memory governance candidates into proposed effects without
applying them. They do not mutate `MemoryEventStore`, delete records, write
lifecycle updates, enable retrieval, call providers, read private data,
generate replies, send messages, create UI, connect to platform delivery,
enable voice/avatar runtime, generate media, or recreate real people.

## Implemented Records

### MemoryLifecycleDryRunEffect

Implementation:

- `practical_chat_agent.services.memory_lifecycle_dry_run.MemoryLifecycleDryRunEffect`

Fields:

| Field | Meaning |
| --- | --- |
| `schema_version` | Always `memory_lifecycle_dry_run_effect_v1`. |
| `effect_id` | Generated `mldeff_` id. |
| `action` | Preview action such as `suppress_retrieval`, `training_exclusion`, `supersede`, or `request_clarification`. |
| `memory_id` | Target memory id. |
| `replacement_memory_id` | Optional replacement memory id for supersession previews. |
| `safe_summary` | Safe display summary. |
| `source_refs` | Redacted candidate or artifact refs. |
| `preview_only` | Always true. |
| `applies_changes` | Always false. |
| `writes_memory_store` | Always false. |
| `retrieval_enabled_after` | Always false. |
| `created_at` | Effect timestamp. |

Required invariants:

- effects are preview-only;
- effects cannot apply changes;
- effects cannot write memory stores;
- effects cannot enable retrieval.

### MemoryLifecycleDryRunPlan

Implementation:

- `practical_chat_agent.services.memory_lifecycle_dry_run.MemoryLifecycleDryRunPlan`

Fields:

| Field | Meaning |
| --- | --- |
| `schema_version` | Always `memory_lifecycle_dry_run_plan_v1`. |
| `plan_id` | Generated `mldplan_` id. |
| `source_candidate_kind` | `memory_deletion_cascade`, `memory_supersession`, or `memory_contradiction`. |
| `source_candidate_id` | Source governance candidate id. |
| `source_schema_version` | Source schema version. |
| `review_decision_id` | Optional review queue decision ref. |
| `review_decision` | Optional review decision label. |
| `safe_summary` | Safe plan summary. |
| `affected_memory_ids` | Memory ids touched by the preview. |
| `effects` | Preview effects. |
| `blocked_reasons` | Reasons no real apply/retrieval occurs. |
| `preview_only` | Always true. |
| `review_required` | Always true. |
| `applies_changes` | Always false. |
| `writes_memory_store` | Always false. |
| `created_at` | Plan timestamp. |

Helper:

- `effect_by_memory_id(memory_id)`

Required invariants:

- plans are preview-only;
- plans require review;
- plans cannot apply changes;
- plans cannot write memory stores;
- `retrieval_not_enabled_by_dry_run` is always included in blocked reasons.

### MemoryLifecycleDryRunService

Implementation:

- `practical_chat_agent.services.memory_lifecycle_dry_run.MemoryLifecycleDryRunService`

Method:

- `plan_from_candidate(candidate, decision_record=None)`

Supported candidates:

- `MemoryDeletionCascadePlan`
- `MemorySupersessionCandidate`
- `MemoryContradictionCandidate`

## Candidate Behavior

Deletion cascade plans:

- produce one effect per target memory and recommended action;
- preserve target memory ids and affected artifact refs;
- keep suppress/training/delete/freeze/archive actions preview-only.

Supersession plans:

- preview a `supersede` effect for the source memory;
- preserve replacement memory id;
- do not change lifecycle state in the store.

Contradiction plans:

- map `request_clarification` to clarification preview effects;
- map `supersede_old`, `archive_old`, `reject_new`, and `keep_both` to matching
  preview actions;
- do not overwrite memory summaries or lifecycle states.

Review decisions:

- may be referenced by id and decision label;
- do not trigger apply behavior.

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

- `tests/test_memory_lifecycle_dry_run_apply.py`

Covered behavior:

- deletion cascade dry-run plans list suppress/training effects without store
  mutation;
- supersession dry-run plans preview lifecycle transition without changing
  source memory state;
- contradiction dry-run plans preview clarification without overwriting memory;
- review decisions are referenced but not applied;
- review-required memory is not made retrieval-eligible;
- extra private/provider/outbound/media fields are rejected;
- service exposes no runtime, delivery, provider, mutation, voice/avatar, or
  media methods.

## Verification

Expected minimum verification:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\services\memory_lifecycle_dry_run.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_memory_lifecycle_dry_run_apply.py tests\test_review_queue_candidates.py tests\test_memory_governance_candidates.py -q -o cache_dir=artifacts\t378_pytest_cache --basetemp=artifacts\t378_pytest_basetemp
```

```powershell
git diff --check
```

## Non-Actions

T378 does not implement:

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
- deletion executors;
- review UI;
- proactive candidates;
- automatic sending or scheduling;
- platform integration;
- voice/avatar/video behavior;
- generated media;
- legal, clinical, launch, app-store, or regulator approval.

## Residual Risks

- Dry-run plans do not execute approved changes.
- No user-facing review UI or approval workflow exists.
- No cache/index cascade executor exists.
- T379 still needs persona growth dry-run apply plans.
