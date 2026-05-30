# Memory Retrieval Bundle v2 Contract

Task: T263 Memory Retrieval Bundle Contract
Status: worker draft for review

## Scope

`MemoryRetrievalBundle v2` packages already-selected `MemoryEvent` records for
future review or dialogue-facing surfaces. It is schema-only. It does not
implement retrieval ranking, vector search, semantic similarity, private
readers, runtime dialogue, proactive behavior, or platform integration.

Implemented models:

- `MemoryRetrievalPurpose`
- `MemoryRetrievalBundleItem`
- `MemoryRetrievalBundle`

## Bundle Item

`MemoryRetrievalBundleItem` fields:

| Field | Meaning |
| --- | --- |
| `schema_version` | Always `memory_retrieval_bundle_item_v2`. |
| `event_id` | Source MemoryEvent id. |
| `event_type` | Factual/inferred/relational/procedural/imagined. |
| `truth_status` | Source truth status. |
| `summary` | Safe event summary. |
| `provenance_refs` | Evidence/source refs copied from provenance. |
| `retrieval_context` | Context in which the item is packaged. |
| `sensitivity` | Source sensitivity. |
| `lifecycle_state` | Source lifecycle state. |
| `review_required` | Whether source event requires review. |

`MemoryRetrievalBundleItem.from_event(...)` copies fields from a `MemoryEvent`
without ranking or scoring it.

## Bundle

`MemoryRetrievalBundle` fields:

| Field | Meaning |
| --- | --- |
| `schema_version` | Always `memory_retrieval_bundle_v2`. |
| `bundle_id` | Generated `memrb_` id. |
| `purpose` | `factual_response`, `inferred_context`, `relationship_context`, `procedural_context`, `imagined_context`, or `review_surface`. |
| `query_summary` | Safe summary of why the bundle exists. |
| `items` | Already-selected bundle items. |
| `selected_memory_ids` | Populated from item ids. |
| `excluded_memory_ids` | Memory ids omitted by the caller. |
| `exclusion_reasons` | Caller-supplied exclusion reasons. |
| `truth_status_counts` | Populated from item truth statuses. |
| `imagined_memory_count` | Count of imagined items. |
| `safety_warnings` | Caller-supplied warnings. |
| `include_review_required` | Explicit flag allowing review-required items. |
| `generated_at` | Bundle timestamp. |

## Invariants

- `factual_response` bundles cannot include imagined memory as factual evidence.
- Deleted, frozen, or archived memory cannot be included.
- Review-required memory cannot be included unless
  `include_review_required=true`.
- Bundle items preserve event type, truth status, provenance refs, lifecycle
  state, sensitivity, and retrieval context.
- Bundles contain no raw transcript, send, schedule, delivery, or runtime
  fields.

## Non-Actions

T263 does not implement:

- memory selection;
- vector search;
- retrieval ranking;
- semantic similarity;
- query parsing;
- private chat-log reads;
- LLM extraction;
- dialogue runtime consumption;
- proactive candidates;
- outbound sending;
- platform integration.

## Verification

Expected minimum verification:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\core\models.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_memory_retrieval_bundle_schema.py tests\test_memory_event_schema.py -q
```

```powershell
git diff --check
```
