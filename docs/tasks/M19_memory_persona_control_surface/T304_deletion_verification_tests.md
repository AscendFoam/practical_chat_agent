# T304: Deletion Verification Tests

## Task ID

T304

## Goal

Add focused verification tests for deletion-related safety boundaries across
the local control contracts and existing persona version store. T304 should
prove that deletion paths remain preview/review/audit-oriented, preserve
history, avoid source-file removal, and do not expose raw private content.

## Why Now

T303 defined dry-run delete/freeze/export flow contracts. Before M19 gate
review, the project needs explicit deletion verification coverage so reviewers
can distinguish tested local tombstone/preview behavior from unimplemented
production deletion.

## Allowed Files

Future T304 worker may create or modify only:

- `tests/test_deletion_verification.py`
- `src/practical_chat_agent/core/models.py`
- `src/practical_chat_agent/services/persona_version_store.py`
- `docs/data_contracts/delete_freeze_export_flow_contract.md`
- `docs/tasks/M19_memory_persona_control_surface/T305_m19_gate_review.md`
- `docs/worker_summary/T304_worker_summary.md`
- `docs/07_handoff.md`

If T304 needs UI, real filesystem deletion, platform adapters, export file
writing, private artifact reads, or task-board edits, Captain must revise this
package before assignment.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not call LLMs, model providers, external APIs, browser automation, or
  network services.
- Do not build UI.
- Do not actually remove source files or generated artifacts.
- Do not write real export ZIP/JSON/CSV bundles.
- Do not publish, send, deliver, enqueue, webhook, notify, or call platform
  adapters.
- Do not modify `docs/04_task_board.md`, `docs/05_decision_log.md`,
  `docs/06_eval_protocol.md`, or `docs/08_risks_and_open_questions.md`.

## Inputs To Read

Required:

- `docs/requirements/memory_persona_control_requirements.md`
- `docs/data_contracts/delete_freeze_export_flow_contract.md`
- `docs/data_contracts/persona_version_store_contract.md`
- `src/practical_chat_agent/core/models.py`
- `src/practical_chat_agent/services/persona_version_store.py`
- `tests/test_delete_freeze_export_flow_contract.py`
- `tests/test_persona_version_store.py`

## Expected Outputs

### 1. Deletion Verification Tests

Create `tests/test_deletion_verification.py`.

Minimum expected coverage:

- persona version-store delete appends a tombstone and preserves prior
  versions;
- latest non-deleted lookup continues to exclude deleted tombstones by default;
- delete/export payloads contain no raw private chat text and no send,
  schedule, delivery, platform, webhook, token, or queue fields;
- dry-run delete previews mark retrieval/runtime eligibility false before any
  confirmation;
- confirmations and audit events do not execute the delete;
- hard delete is represented as a high-impact preview only unless a future
  explicit task implements verified deletion.

If a test reveals a contract gap, fix only the minimal local contract/store code
needed to pass.

### 2. Data Contract Notes

Update `docs/data_contracts/delete_freeze_export_flow_contract.md` only if the
tests reveal a missing invariant or clarification.

### 3. Next Task Package

Create `docs/tasks/M19_memory_persona_control_surface/T305_m19_gate_review.md`
for M19 adversarial milestone review.

### 4. Worker Summary And Handoff

Write `docs/worker_summary/T304_worker_summary.md` and append a T304 worker
record to `docs/07_handoff.md`.

Do not mark T304 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'
pytest tests\test_deletion_verification.py tests\test_delete_freeze_export_flow_contract.py tests\test_persona_version_store.py -q
```

```powershell
git diff --check
```

## Reviewer Type

Adversarial review recommended.

Reviewer should verify that T304 proves local tombstone/preview behavior only
and does not claim production deletion, source-file deletion, platform
integration, export generation, or privacy compliance completion.
