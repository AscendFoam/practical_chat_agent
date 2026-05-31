# Review Workspace Snapshot Store Contract

Task: T384 Review Workspace Snapshot Store
Status: worker draft for review

## Scope

This contract describes the implemented local JSON snapshot store in
`src/practical_chat_agent/services/review_workspace_store.py`.

The store persists safe `ReviewWorkspaceBundle` records for local prototype
review workflows. It does not apply decisions, mutate memory stores, write
persona versions, synthesize personas, call providers, generate replies, send
messages, create UI, connect to platform delivery, enable voice/avatar
runtime, generate media, or recreate real people.

## Implemented Service

### ReviewWorkspaceSnapshotStore

Implementation:

- `practical_chat_agent.services.review_workspace_store.ReviewWorkspaceSnapshotStore`

Constructor:

| Argument | Meaning |
| --- | --- |
| `root` | Caller-owned local directory where JSON snapshots are stored. |

Methods:

| Method | Behavior |
| --- | --- |
| `save_bundle(bundle, file_name=None)` | Writes a bundle JSON file under the store root and creates parent directories as needed. |
| `load_bundle(bundle_id_or_file_name)` | Loads a bundle by bundle id or JSON file name through Pydantic validation. |
| `list_bundles()` | Loads all root-level JSON bundle files and returns them sorted by `created_at` then `bundle_id`. |
| `filter_bundles(...)` | Returns deterministic bundle subsets by candidate kind, owner user id, persona id, priority band, or blocker state. |

Supported filters:

| Filter | Match Rule |
| --- | --- |
| `candidate_kind` | Any candidate binding has the requested kind. |
| `owner_user_id` | Any candidate binding has the requested owner user id. |
| `persona_id` | Any candidate binding has the requested persona id. |
| `priority_band` | Any candidate binding has the requested priority band. |
| `has_blockers` | Bundle has or does not have blocking issue codes. |

## Stored Record

The store writes the JSON representation of
`ReviewWorkspaceBundle.model_dump_json(indent=2)`.

Allowed stored fields are those already defined by the T383 workspace binding
contract:

- bundle ids;
- candidate binding ids;
- artifact binding ids;
- candidate kinds;
- candidate ids;
- queue item ids;
- schema versions;
- owner user ids;
- persona ids;
- safe summaries;
- reason labels;
- redacted source refs;
- priority scores and bands;
- issue codes;
- blocking issue codes;
- review-required flags;
- preview-only flags;
- non-apply flags;
- non-runtime-ready flags;
- timestamps.

## Required Invariants

- Store paths must remain under the caller-supplied root.
- Absolute paths are rejected.
- Path traversal outside the root is rejected.
- Snapshot files must use `.json`.
- Loaded records must pass `ReviewWorkspaceBundle` Pydantic validation.
- Listing order is deterministic by `created_at` and `bundle_id`.
- Filtering never mutates stored records.
- Persisted bundles remain review-required, preview-only, non-applying, and
  non-runtime-ready.

## Forbidden Fields And Surfaces

Serialized snapshot files must not contain:

- raw private chat text;
- raw transcripts;
- private message bodies;
- private chat history paths;
- provider credentials;
- platform recipient ids;
- send queues;
- schedules;
- webhooks;
- tokens;
- delivery state;
- microphone, camera, audio, image, or video payloads;
- generated media paths;
- runtime reply-generation fields;
- decision apply fields;
- persona synthesis fields;
- mutation executor fields.

The store must not expose methods for:

- sending or scheduling;
- delivery;
- provider calls;
- webhooks;
- memory or persona mutation;
- review decision apply;
- PersonaVersionStore writes;
- deletion executors;
- retrieval enablement;
- persona synthesis;
- reply generation;
- voice/avatar/audio/image/video generation.

## Tests

Implemented tests:

- `tests/test_review_workspace_snapshot_store.py`

Covered behavior:

- bundles can be saved and loaded without losing readiness or issue state;
- listing is deterministic;
- filtering by candidate kind, owner user id, persona id, priority band, and
  blocker status works;
- path traversal is rejected;
- serialized files do not contain forbidden private/provider/outbound/media
  fields;
- store instances expose no runtime, delivery, provider, mutation, apply,
  synthesis, voice/avatar, or media methods.

## Verification

Expected minimum verification:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\services\review_workspace_store.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_review_workspace_snapshot_store.py tests\test_review_workspace_bindings.py -q -o cache_dir=artifacts\t384_pytest_cache --basetemp=artifacts\t384_pytest_basetemp
```

```powershell
git diff --check
```

## Non-Actions

T384 does not implement:

- private data ingestion;
- source readers;
- extraction from real logs;
- embeddings;
- vector search;
- semantic ranking;
- similarity scoring;
- model-provider calls;
- de-identification quality validation;
- PersonaCard synthesis;
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

- Snapshot storage is local prototype persistence, not production persistence.
- The store preserves existing bundle fields and does not independently prove
  de-identification quality.
- Review decisions can be recorded elsewhere but are not previewed here.
- T385 still needs deterministic review decision impact previews.
