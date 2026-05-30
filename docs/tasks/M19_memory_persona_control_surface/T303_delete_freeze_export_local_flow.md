# T303: Delete / Freeze / Export Local Flow Contract

## Task ID

T303

## Goal

Define local control-flow data contracts for delete, freeze, unfreeze, and
export operations across memory/persona control surfaces. T303 should model
dry-run previews, explicit confirmations, audit events, and export manifests
without mutating records or writing export files.

## Why Now

T301 added read-only memory inspection and T302 added draft-only persona edit
proposals. M19 still needs typed contracts for high-impact control operations
before any UI/demo can safely expose delete, freeze, or export actions.

## Allowed Files

Future T303 worker may create or modify only:

- `src/practical_chat_agent/core/models.py`
- `tests/test_delete_freeze_export_flow_contract.py`
- `docs/data_contracts/delete_freeze_export_flow_contract.md`
- `docs/tasks/M19_memory_persona_control_surface/T304_m19_gate_review.md`
- `docs/worker_summary/T303_worker_summary.md`
- `docs/07_handoff.md`

If T303 needs UI, mutation services, file deletion, real export writing,
platform adapters, or task-board edits, Captain must revise this package before
assignment.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not call LLMs, model providers, external APIs, browser automation, or
  network services.
- Do not build UI.
- Do not actually delete, freeze, unfreeze, export, migrate, or write records.
- Do not remove private source files or generated artifacts.
- Do not write ZIP/JSON/CSV exports.
- Do not publish, send, deliver, enqueue, webhook, notify, or call platform
  adapters.
- Do not modify `docs/04_task_board.md`, `docs/05_decision_log.md`,
  `docs/06_eval_protocol.md`, or `docs/08_risks_and_open_questions.md`.

## Inputs To Read

Required:

- `docs/requirements/memory_persona_control_requirements.md`
- `docs/data_contracts/memory_viewer_contract.md`
- `docs/data_contracts/persona_version_editor_contract.md`
- `docs/data_contracts/persona_version_store_contract.md`
- `src/practical_chat_agent/core/models.py`
- `tests/test_memory_viewer_contract.py`
- `tests/test_persona_version_editor_contract.py`
- `tests/test_persona_version_store.py`

## Expected Outputs

### 1. Flow Models And Tests

Add contract models to `src/practical_chat_agent/core/models.py`.

Minimum expected objects:

- `ControlOperationTarget`;
- `ControlOperationPreview`;
- `ControlOperationConfirmation`;
- `ControlAuditEvent`;
- `ControlExportManifest`.

Minimum expected behavior:

- delete/freeze/unfreeze/export operations require dry-run preview before
  confirmation;
- delete distinguishes soft delete from hard delete;
- freeze/delete previews mark affected retrieval/runtime eligibility;
- export manifests label imagined, AIGC, review-required, and provenance
  metadata;
- audit events preserve actor, user, target, operation, before/after summaries,
  reason, confirmation status, timestamp, and safety flags;
- audit/export payloads contain no raw private chat text and no send, schedule,
  delivery, platform, webhook, token, or queue fields;
- models are contract-only and expose no method that mutates source artifacts.

### 2. Data Contract

Create `docs/data_contracts/delete_freeze_export_flow_contract.md` describing
fields, invariants, non-actions, and verification.

### 3. Next Task Package

Create `docs/tasks/M19_memory_persona_control_surface/T304_m19_gate_review.md`
for M19 adversarial gate review.

### 4. Worker Summary And Handoff

Write `docs/worker_summary/T303_worker_summary.md` and append a T303 worker
record to `docs/07_handoff.md`.

Do not mark T303 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\core\models.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_delete_freeze_export_flow_contract.py tests\test_memory_viewer_contract.py tests\test_persona_version_editor_contract.py -q
```

```powershell
git diff --check
```

## Reviewer Type

Adversarial review recommended.

Reviewer should verify that T303 creates preview/audit/export contracts only
and cannot delete files, mutate records, write exports, send messages, schedule
work, or integrate platforms.
