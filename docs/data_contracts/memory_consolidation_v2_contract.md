# Memory Consolidation v2 Contract

Task: T264 Memory Consolidation Stub
Status: worker draft for review

## Scope

`MemoryConsolidationService` groups synthetic `MemoryEvent` records into
deterministic consolidation candidates. It is recommendation-only. It does not
call LLMs, mutate stores, rank retrieval, read private chat logs, generate
dialogue, create proactive candidates, or connect to external platforms.

Implementation entry point:

- `practical_chat_agent.services.memory_consolidation_v2.MemoryConsolidationService`
- `MemoryConsolidationService.propose(events, age_days_by_event_id=None)`

## Candidate Model

`MemoryConsolidationCandidate` fields:

| Field | Meaning |
| --- | --- |
| `schema_version` | Always `memory_consolidation_candidate_v2`. |
| `group_id` | Generated `memcon_` id. |
| `event_ids` | Source MemoryEvent ids. |
| `event_type` | Shared event type for the group. |
| `proposed_operation` | `keep`, `review`, `decay`, `compress`, or `separate_imagined`. |
| `rationale` | Deterministic rationale string. |
| `safety_warnings` | Machine-readable warnings from lifecycle policy. |

## Grouping Rules

- Active keep candidates group by event type.
- Factual events group only with factual events.
- Procedural, relational, inferred, and imagined events are not merged into
  factual groups.
- Imagined events are emitted as `separate_imagined`.
- Review-required/high-sensitivity events are emitted as `review`.
- Low-salience old events can be emitted as `decay` or `compress`.

## Lifecycle Policy

The service delegates per-event policy classification to
`MemoryLifecyclePolicyService`. It maps:

- `review_required` -> `review`;
- `decay` -> `decay`;
- `compress` -> `compress`;
- imagined event type -> `separate_imagined`;
- otherwise -> `keep`.

## Mutation Boundary

The service returns candidate records only. It does not call
`MemoryEventStore.update_lifecycle(...)` or any other mutation method.

## Non-Actions

T264 does not implement:

- LLM summarization;
- private chat-log reads;
- vector search;
- retrieval ranking;
- semantic similarity;
- store mutation;
- dialogue runtime consumption;
- proactive candidates;
- outbound sending;
- platform integration.

## Verification

Expected minimum verification:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\services\memory_consolidation_v2.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_memory_consolidation_v2.py tests\test_memory_retrieval_bundle_schema.py tests\test_memory_lifecycle_v2.py tests\test_memory_event_schema.py -q
```

```powershell
git diff --check
```
