# T409: Apply Executor Audit Manifest

## Task ID

T409

## Goal

Implement a local-only apply executor audit manifest.

T409 should combine completed local apply audit records from T407 persona
growth apply and T408 memory lifecycle apply into a reviewable manifest. The
manifest should preserve rollback references and gate ids while keeping private
content, provider/platform details, outbound delivery state, and media payloads
out of the serialized surface.

## Allowed Files

Future T409 worker may create or modify only:

- `src/practical_chat_agent/services/apply_executor_audit_manifest.py`
- `tests/test_apply_executor_audit_manifest.py`
- `docs/data_contracts/apply_executor_audit_manifest_contract.md`
- `docs/tasks/M33_controlled_apply_executor/T410_review_workspace_apply_audit_panel.md`
- `docs/worker_summary/T409_worker_summary.md`
- `docs/07_handoff.md`

If T409 needs private data, source readers, model-provider calls, local server
routes, package changes, platform adapters, outbound messaging, voice/avatar
runtime, media generation, automatic apply triggers, PersonaVersionStore
writes, or MemoryEventStore writes, Captain must revise this package before
assignment.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not ingest, summarize, transform, quote, or commit real private chat
  records.
- Do not call model providers.
- Do not implement source readers, extraction from real logs, embeddings,
  vector search, semantic ranking, fine-tuning, similarity scoring, persona
  synthesis, final companion reply generation, or runtime mutation.
- Do not write PersonaVersionStore or MemoryEventStore.
- Do not add routes, CLIs, schedulers, queues, webhooks, auth, tokens,
  recipient ids, delivery state, or platform persistence behavior.
- Do not implement proactive candidates, automatic outreach, sending,
  scheduling, notifications, platform delivery, microphone, camera, ASR, TTS,
  voice cloning, voice/avatar likeness, Live2D, generated audio, generated
  image, generated video, or media capture.
- Do not modify `docs/04_task_board.md`.

## Expected Outputs

### 1. Manifest Records

Create `apply_executor_audit_manifest.py` with records such as:

- `ApplyExecutorAuditManifestEntry`
- `ApplyExecutorAuditManifest`
- `ApplyExecutorAuditManifestBuilder`

Entries should normalize:

- apply type;
- apply id;
- source artifact id;
- review decision id;
- eligibility id;
- approval id;
- reviewer id;
- rollback references;
- changed field paths or affected memory ids;
- safe summary;
- local-only flags.

### 2. Manifest Behavior

The builder should:

- accept persona growth apply audits and memory lifecycle apply audits;
- reject unsupported audit schemas;
- require `final_confirmation=confirmed`;
- require local-only/no-provider/no-outbound flags;
- require rollback references for every entry;
- avoid storing raw store paths, private text, provider credentials, platform
  recipients, queues, webhooks, tokens, or media payloads;
- sort entries deterministically by created time and apply id;
- produce a serializable manifest for review/export.

### 3. Tests

Create `tests/test_apply_executor_audit_manifest.py` proving:

- persona growth and memory lifecycle audits are normalized into one manifest;
- rollback references are preserved;
- unsupported schemas are rejected;
- missing rollback evidence is rejected;
- forbidden private/provider/outbound/media fields are absent from manifest
  JSON;
- the builder exposes no provider, outbound, voice/avatar, media, scheduler, or
  platform methods.

### 4. Data Contract

Create `docs/data_contracts/apply_executor_audit_manifest_contract.md`.

### 5. Next Task Package

Create
`docs/tasks/M33_controlled_apply_executor/T410_review_workspace_apply_audit_panel.md`.

### 6. Worker Summary And Handoff

Write `docs/worker_summary/T409_worker_summary.md` and append a T409 worker
record to `docs/07_handoff.md`.

Do not mark T409 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\services\apply_executor_audit_manifest.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_apply_executor_audit_manifest.py tests\test_persona_growth_apply_executor.py tests\test_memory_lifecycle_apply_executor.py -q
```

```powershell
git diff --check
```

Use project-local pytest cache and basetemp paths if the default user temp
directory is not writable.

## Reviewer Type

Adversarial auditability review for rollback evidence, privacy, local-only
boundaries, deterministic serialization, and no platform/provider surface
expansion.
