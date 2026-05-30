# Memory Event Store v2 Contract

Task: T261 Memory Store v2
Status: worker draft for review

## Scope

`MemoryEventStore` is a caller-path local JSON store for `MemoryEvent v2`
records. It persists and inspects typed memory events while preserving
factual/inferred/relational/procedural/imagined separation. It does not
implement retrieval ranking, vector search, dialogue runtime consumption,
private readers, proactive behavior, or platform integration.

Implementation entry point:

- `practical_chat_agent.services.memory_event_store.MemoryEventStore`

The store writes only to the path passed by the caller.

## Store File

`MemoryEventStoreFile` fields:

| Field | Meaning |
| --- | --- |
| `schema_version` | Always `memory_event_store_v2`. |
| `records` | Append-only list of store records. |

## Store Record

`MemoryEventStoreRecord` fields:

| Field | Meaning |
| --- | --- |
| `schema_version` | Always `memory_event_store_record_v2`. |
| `record_id` | Generated `memrec_` id. |
| `event` | Stored `MemoryEvent`. |
| `operation` | `append` or `lifecycle_update`. |
| `parent_record_id` | Previous record id for lifecycle updates. |
| `created_at` | Record timestamp. |

## Methods

- `append(event)`: append a `MemoryEvent`.
- `list_records(include_history=False)`: latest record per event by default;
  all records when `include_history=true`.
- `list_events()`: latest `MemoryEvent` objects.
- `list_by_user(user_id)`: latest events for a user.
- `list_by_event_type(event_type)`: latest events by type.
- `list_factual_events(user_id=None)`: factual events only.
- `get(event_id)`: latest event by id.
- `get_record(event_id)`: latest store record by id.
- `update_lifecycle(event_id, lifecycle_state)`: append a lifecycle update.
- `export_safe_json()`: export JSON-compatible records.

## Lifecycle Behavior

Lifecycle updates are append-only. The store appends a new record with a copied
`MemoryEvent` whose lifecycle is updated. Historical records remain available
through `include_history=true`.

Frozen, deleted, and archived events rely on `MemoryEvent.is_retrieval_eligible`
to return false.

## Type Separation

The store never coerces event type or truth status.

`list_factual_events()` returns only events with:

- `event_type="factual"`;
- `truth_status="evidence_backed"`.

Imagined memory is therefore excluded from factual helpers even when it is
present in the same store file.

## Export Safety

The export path serializes store records and current MemoryEvent fields. The
schema contains no raw transcript fields, private chat history, delivery
requests, scheduler data, or platform payloads.

Future changes must be blocked if they add raw private content or outbound
delivery data without a new explicit task and review.

## Non-Actions

T261 does not implement:

- vector search;
- retrieval ranking;
- semantic similarity;
- private chat-log ingestion;
- LLM extraction;
- background consolidation;
- forgetting or decay policy;
- dialogue runtime consumption;
- proactive candidates;
- outbound sending;
- platform integration.

## Verification

Expected minimum verification:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\services\memory_event_store.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_memory_event_store.py tests\test_memory_event_schema.py -q
```

```powershell
git diff --check
```
