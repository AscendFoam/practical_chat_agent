# Apply Executor Audit Manifest Contract

Task: T409 Apply Executor Audit Manifest
Status: worker draft for review

## Scope

This contract describes the local-only apply executor audit manifest in:

- `src/practical_chat_agent/services/apply_executor_audit_manifest.py`

The manifest normalizes completed local apply audit records from:

- `PersonaGrowthApplyAudit`
- `MemoryLifecycleApplyAudit`

It preserves rollback references and gate ids for review/export. It does not
read private chat logs, call providers, write memory stores, write persona
version stores, generate replies, send messages, connect to platforms, or
generate voice/avatar/media.

## Implemented Records

### ApplyExecutorAuditManifestEntry

Fields include:

- `entry_id`
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
- `final_confirmation=confirmed`
- local-only and no-provider/no-outbound flags
- `created_at`

Entry apply types:

- `persona_growth`
- `memory_lifecycle`

### ApplyExecutorAuditManifest

Fields include:

- `manifest_id`
- `entries`
- `entry_count`
- local-only and no-provider/no-outbound flags
- `created_at`

Entries are sorted deterministically by `(created_at, apply_id)`.

### ApplyExecutorAuditManifestBuilder

Method:

- `build(audits)`

Behavior:

- accepts persona growth apply audits;
- accepts memory lifecycle apply audits;
- rejects unsupported audit schemas;
- requires `final_confirmation=confirmed`;
- requires local-only, review-required, no automatic apply, no provider calls,
  no message sends, and not runtime-ready;
- requires rollback references for every entry;
- preserves changed persona field paths;
- preserves affected memory ids;
- preserves gate ids and reviewer id.

## Required Invariants

- The manifest is local-only.
- It is an audit/read model only.
- It never writes `PersonaVersionStore`.
- It never writes `MemoryEventStore`.
- It never calls providers.
- It never sends, schedules, delivers, or connects to platforms.
- It never generates replies, audio, images, video, voice, or avatar output.
- It does not serialize raw store paths, private chat text, provider
  credentials, platform recipients, queues, webhooks, tokens, or media
  payloads.

## Tests

Implemented tests:

- `tests/test_apply_executor_audit_manifest.py`

Regression tests also run:

- `tests/test_persona_growth_apply_executor.py`
- `tests/test_memory_lifecycle_apply_executor.py`

Covered behavior:

- persona growth and memory lifecycle audits are normalized into one manifest;
- rollback references are preserved;
- unsupported schemas are rejected;
- missing rollback evidence is rejected;
- forbidden private/provider/outbound/media fields are absent from manifest
  JSON;
- the builder exposes no provider, outbound, scheduler, platform, or media
  methods.

## Verification

Expected minimum verification:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\services\apply_executor_audit_manifest.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_apply_executor_audit_manifest.py tests\test_persona_growth_apply_executor.py tests\test_memory_lifecycle_apply_executor.py -q -o cache_dir=artifacts\t409_pytest_cache --basetemp=artifacts\t409_pytest_basetemp
```

```powershell
git diff --check
```

## Non-Actions

T409 does not implement:

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

- The manifest is local-only and caller-supplied-audit-only.
- No review workspace displays completed apply audit records yet.
- Automatic apply remains unauthorized.
