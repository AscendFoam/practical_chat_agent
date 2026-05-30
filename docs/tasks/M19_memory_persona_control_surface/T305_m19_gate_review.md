# T305: M19 Milestone Review

## Task ID

T305

## Goal

Perform an adversarial M19 milestone review for the Memory And Persona Control
Surface work. The review should verify that M19 provides local read/edit/delete
/freeze/export/audit contracts and deletion verification without claiming UI,
production deletion, platform integration, or privacy compliance completion.

## Why Now

T300-T304 define requirements, viewer contracts, persona edit proposals,
delete/freeze/export flow contracts, and deletion verification tests. M19 needs
a gate review before moving into M20 compliance and safety baseline work.

## Allowed Files

Future T305 worker may create or modify only:

- `docs/review/M19_review.md`
- `docs/tasks/M20_compliance_and_safety_baseline/T310_china_compliance_checklist.md`
- `docs/worker_summary/T305_worker_summary.md`
- `docs/07_handoff.md`

If T305 needs code, tests, UI, runtime behavior, platform adapters, or
task-board edits, Captain must revise this package before assignment.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not call LLMs, model providers, external APIs, browser automation, or
  network services.
- Do not build UI.
- Do not mutate memory/persona records.
- Do not delete files or write exports.
- Do not publish, send, deliver, enqueue, webhook, notify, or call platform
  adapters.
- Do not modify `docs/04_task_board.md`, `docs/05_decision_log.md`,
  `docs/06_eval_protocol.md`, or `docs/08_risks_and_open_questions.md`.

## Inputs To Read

Required:

- `docs/requirements/memory_persona_control_requirements.md`
- `docs/data_contracts/memory_viewer_contract.md`
- `docs/data_contracts/persona_version_editor_contract.md`
- `docs/data_contracts/delete_freeze_export_flow_contract.md`
- `docs/worker_summary/T300_worker_summary.md`
- `docs/worker_summary/T301_worker_summary.md`
- `docs/worker_summary/T302_worker_summary.md`
- `docs/worker_summary/T303_worker_summary.md`
- `docs/worker_summary/T304_worker_summary.md`
- `tests/test_memory_viewer_contract.py`
- `tests/test_persona_version_editor_contract.py`
- `tests/test_delete_freeze_export_flow_contract.py`
- `tests/test_deletion_verification.py`

## Expected Outputs

### 1. M19 Review

Create `docs/review/M19_review.md` with:

- gate recommendation: `PASS`, `PASS_WITH_WARNINGS`, or `BLOCK`;
- task coverage table for T300-T304;
- implemented code and data contracts;
- verification evidence;
- control-surface safety boundary assessment;
- explicit non-actions;
- residual risks;
- M20 entry recommendation.

### 2. M20 Entry Task Package

Create
`docs/tasks/M20_compliance_and_safety_baseline/T310_china_compliance_checklist.md`
for the China compliance checklist task.

### 3. Worker Summary And Handoff

Write `docs/worker_summary/T305_worker_summary.md` and append a T305 worker
record to `docs/07_handoff.md`.

Do not mark T305 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'
pytest tests\test_memory_viewer_contract.py tests\test_persona_version_editor_contract.py tests\test_delete_freeze_export_flow_contract.py tests\test_deletion_verification.py -q
```

```powershell
git diff --check
```

## Reviewer Type

Adversarial review required.

Reviewer should mark M19 as `PASS_WITH_WARNINGS` only if controls remain local,
review-first, and test-covered. Reviewer should `BLOCK` if the diff claims
production deletion/privacy compliance, exposes raw private content, adds UI
without review, or introduces sending, scheduling, platform integration, or
source-file deletion.
