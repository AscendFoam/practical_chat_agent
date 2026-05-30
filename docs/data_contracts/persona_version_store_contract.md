# Persona Version Store Contract

Task: T254 Persona Version Store
Status: worker draft for review

## Scope

The T254 version store is a local JSON, append-only history for `PersonaCard v1`
records. It gives M14 a safe persistence boundary for candidate cards, reviewed
copies, rollback, freeze, delete/tombstone, and export without wiring personas
into runtime dialogue, memory retrieval, proactive behavior, or platform
delivery.

Implementation entry point:

- `practical_chat_agent.services.persona_version_store.PersonaVersionStore`

The store writes only to the path passed by the caller.

## Store File

`PersonaVersionStoreFile` fields:

| Field | Meaning |
| --- | --- |
| `schema_version` | Always `persona_version_store_v1`. |
| `records` | Append-only list of `PersonaVersionRecord`. |

## Version Record

`PersonaVersionRecord` fields:

| Field | Meaning |
| --- | --- |
| `schema_version` | Always `persona_version_record_v1`. |
| `version_id` | Deterministic id: `{persona_id}_v{version_number}`. |
| `persona_id` | Persona id shared by all versions. |
| `version_number` | Monotonic per persona. |
| `operation` | `save`, `rollback`, `freeze`, or `delete`. |
| `card` | Stored PersonaCard copy. |
| `parent_version_id` | Previous latest version when applicable. |
| `deleted` | Tombstone marker for delete operations. |
| `created_at` | Store record timestamp. |

## Service Methods

- `save(card)`: appends a new saved version.
- `list_versions(persona_id)`: returns all records for a persona.
- `latest_record(persona_id, include_deleted=False)`: returns latest version,
  excluding tombstones by default.
- `latest_card(persona_id)`: returns the latest non-deleted card.
- `rollback(persona_id, version_id)`: appends a rollback version copied from a
  prior version without mutating history.
- `freeze(persona_id, reviewer_id)`: appends a frozen review copy.
- `delete(persona_id, reason)`: appends an archived tombstone copy.
- `export_persona(persona_id)`: returns safe JSON-compatible data for all
  versions.

## Control Semantics

- Save is append-only.
- Rollback creates a new record and keeps later records in history.
- Freeze stores a `status="frozen"` card; it is not runtime-ready.
- Delete stores a `status="archived"` card with `deleted=true`; it is not
  runtime-ready.
- Runtime readiness remains delegated to `PersonaCard.is_runtime_ready()`.

## Export Safety

The export method serializes stored PersonaCards and version metadata. The
current PersonaCard schema contains no raw transcripts, private chat history,
send requests, schedule state, delivery connectors, or platform payloads.

Future reviewers should block any store change that adds raw private content or
delivery data to the export path without a new explicit task.

## Non-Actions

T254 does not implement:

- database migrations;
- global store discovery;
- CLI or UI;
- LLM calls;
- private chat-log reads;
- runtime dialogue;
- memory retrieval;
- proactive candidates;
- schedulers;
- outbound requests;
- platform integration;
- voice/avatar/deepfake behavior.

## Verification

Expected minimum verification:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\services\persona_version_store.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_persona_version_store.py tests\test_persona_review.py tests\test_persona_compiler.py -q
```

```powershell
git diff --check
```
