# Memory Lifecycle v2 Contract

Task: T262 Memory Lifecycle Policy
Status: worker draft for review

## Scope

`MemoryLifecyclePolicyService` returns deterministic recommendations for
individual `MemoryEvent` records. It does not mutate stores, rank retrieval
results, read private chat logs, generate dialogue, schedule proactive
messages, or connect to external platforms.

Implementation entry point:

- `practical_chat_agent.services.memory_lifecycle_v2.MemoryLifecyclePolicyService`
- `MemoryLifecyclePolicyService.recommend(event, age_days=0, user_delete_requested=False)`

## Recommendation Model

`MemoryLifecycleRecommendation` fields:

| Field | Meaning |
| --- | --- |
| `schema_version` | Always `memory_lifecycle_recommendation_v2`. |
| `event_id` | Source MemoryEvent id. |
| `action` | `keep`, `review_required`, `freeze`, `delete`, `archive`, `decay`, or `compress`. |
| `retrieval_allowed` | Whether the event is eligible in the recommended context. |
| `retrieval_context` | Factual/inferred/relational/procedural/imagined context when applicable. |
| `allowed_contexts` | Allowed retrieval contexts from the event permission model. |
| `suggested_lifecycle_state` | Suggested lifecycle transition for delete/freeze/archive. |
| `reason_flags` | Machine-readable policy reasons. |
| `notes` | Optional future reviewer notes. |

## Policy Rules

Priority order:

1. Explicit user delete request -> `delete`.
2. Inactive lifecycle state:
   - `deleted` -> `delete`;
   - `frozen` -> `freeze`;
   - `archived` -> `archive`.
3. Medium/high sensitivity or `review_required=true` -> `review_required`.
4. Imagined memory -> `keep` only in imagined retrieval context.
5. Low-salience memory older than 180 days -> `compress`.
6. Low-salience memory older than 30 days -> `decay`.
7. Otherwise -> `keep`.

## Imagined Memory Rule

Imagined memory can only be recommended for imagined retrieval context. The
policy must not add factual context to imagined events and must preserve
`MemoryEvent` schema invariants.

## Store Mutation Boundary

The policy returns recommendations only. Callers may choose whether to apply a
recommendation through `MemoryEventStore.update_lifecycle(...)` or another
future reviewed path.

T262 does not mutate `MemoryEventStore` directly.

## Non-Actions

T262 does not implement:

- private chat-log reads;
- memory extraction;
- store mutation;
- vector search;
- retrieval ranking;
- semantic similarity;
- background consolidation;
- dialogue runtime consumption;
- proactive candidates;
- outbound sending;
- platform integration.

## Verification

Expected minimum verification:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\services\memory_lifecycle_v2.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_memory_lifecycle_v2.py tests\test_memory_event_store.py tests\test_memory_event_schema.py -q
```

```powershell
git diff --check
```
