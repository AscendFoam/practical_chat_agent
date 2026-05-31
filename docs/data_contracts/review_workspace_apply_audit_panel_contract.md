# Review Workspace Apply Audit Panel Contract

Task: T410 Review Workspace Apply Audit Panel
Status: worker draft for review

## Scope

This contract describes the review workspace projection for completed local
apply audit manifest entries in:

- `src/practical_chat_agent/ui/text_first_web_demo_adapter.py`
- `src/practical_chat_agent/ui/static/text_first_web_demo.js`
- `src/practical_chat_agent/ui/static/text_first_web_demo.css`

The panel displays already-normalized audit manifest entries from T409. It
does not execute apply operations, read private chat logs, call providers,
write stores, send messages, connect to platforms, or generate
voice/avatar/media.

## Payload Key

The review workspace payload includes:

- `apply_audit_entries`

Each card uses:

- `schema_version=review_workspace_apply_audit_card_v1`
- `card_kind=apply_audit_manifest_entry`

## Card Fields

Fields include:

- `apply_type`
- `apply_id`
- `source_artifact_kind`
- `source_artifact_id`
- `review_decision_id`
- `eligibility_id`
- `approval_id`
- `reviewer_id`
- `rollback_refs`
- `applied_refs`
- `changed_field_paths`
- `affected_memory_ids`
- `safe_summary`
- `status_badges`
- `filter_keys`
- `review_required`
- `preview_only`
- `changes_state`
- `runtime_ready`

The server-side projection keeps `changes_state=false`; the panel is a display
surface only.

## Static UI Behavior

The static web demo:

- concatenates `apply_audit_entries` into the review workspace card list;
- marks cards with `.apply-audit-card`;
- renders apply type, source artifact id, reviewer id, gate ids, changed field
  paths, affected memory ids, and rollback references;
- keeps the panel local and synthetic.

## Required Invariants

- The payload is synthetic and local-only.
- It does not include raw store paths, private chat text, provider
  credentials, platform recipients, queues, webhooks, tokens, or media
  payloads.
- It does not expose actions to execute, send, schedule, deliver, publish,
  call providers, connect platforms, or generate media.
- It does not write `PersonaVersionStore` or `MemoryEventStore`.

## Tests

Implemented tests:

- `tests/test_review_workspace_apply_audit_panel.py`

Regression tests also run:

- `tests/test_apply_executor_audit_manifest.py`

Covered behavior:

- review workspace payload includes apply audit cards;
- persona growth and memory lifecycle cards render separately;
- rollback references and gate ids are present;
- forbidden private/provider/outbound/media fields are absent from payload
  JSON;
- static JS/CSS includes the expected hooks and no platform delivery or media
  actions.

## Verification

Expected minimum verification:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\ui\text_first_web_demo_adapter.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_review_workspace_apply_audit_panel.py tests\test_apply_executor_audit_manifest.py -q -o cache_dir=artifacts\t410_pytest_cache --basetemp=artifacts\t410_pytest_basetemp
```

```powershell
git diff --check
```

## Non-Actions

T410 does not implement:

- new apply execution;
- persona version mutation;
- memory lifecycle mutation;
- private data ingestion;
- source readers;
- extraction from real logs;
- embeddings;
- vector search;
- semantic ranking;
- similarity scoring;
- model-provider calls;
- PersonaCard synthesis;
- final companion reply generation;
- proactive candidates;
- automatic sending or scheduling;
- platform integration;
- voice/avatar/video behavior;
- generated media;
- legal, clinical, launch, app-store, or regulator approval.

## Residual Risks

- The panel displays synthetic local audit records only.
- M33 still needs adversarial review before being treated as closed.
- Automatic apply remains unauthorized.
