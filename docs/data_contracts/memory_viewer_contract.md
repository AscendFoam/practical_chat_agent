# Memory Viewer Contract

Task: T301 Memory Viewer Data Contract
Status: worker draft for review

## Scope

Memory Viewer models provide read-only local data objects for inspecting
`MemoryEvent` records. They do not build UI, mutate records, delete records,
export records, call LLMs, or integrate with external platforms.

Implemented models:

- `MemoryViewerItem`
- `MemoryViewerFilter`
- `MemoryViewerPage`

## MemoryViewerItem

Fields:

- `memory_id`
- `user_id`
- `event_type`
- `truth_status`
- `sensitivity`
- `lifecycle_state`
- `review_required`
- `summary`
- `provenance_refs`
- `is_retrieval_eligible`
- `is_factual_evidence`
- `can_edit`
- `can_delete`
- `can_freeze`
- `can_export`
- `safety_notes`
- `created_at`
- `updated_at`

Permission fields are metadata only. They do not perform mutations.

## MemoryViewerFilter

Fields:

- `event_types`
- `truth_statuses`
- `lifecycle_states`
- `sensitivities`
- `include_deleted`

## MemoryViewerPage

Fields:

- `items`
- `filters`
- `total_count`
- `page`
- `page_size`
- `generated_at`

## Invariants

- Viewer items preserve core MemoryEvent fields.
- Deleted/frozen/archived memory is visible but not retrieval-eligible.
- Imagined memory is labeled with `imagined_memory`.
- Imagined memory is not factual evidence.
- Factual evidence requires factual event type and factual retrieval eligibility.
- Viewer payloads contain no raw private text, send, schedule, delivery,
  platform, webhook, token, or queue fields.

## Non-Actions

T301 does not implement:

- UI;
- mutation services;
- delete/freeze/export execution;
- persistence changes;
- LLM calls;
- platform integration;
- sending or scheduling.

## Verification

Expected minimum verification:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\core\models.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_memory_viewer_contract.py tests\test_memory_event_schema.py tests\test_memory_retrieval_bundle_schema.py -q
```

```powershell
git diff --check
```
