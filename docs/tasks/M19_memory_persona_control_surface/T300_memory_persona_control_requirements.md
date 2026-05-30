# T300: Memory/Persona Control Requirements

## Task ID

T300

## Goal

Define local/prototype control-surface requirements for viewing, editing,
deleting, freezing, exporting, and auditing persona, memory, and related review
artifacts. T300 is requirements-only and should prepare M19 for data-contract
work.

T300 must not build UI, modify runtime data, delete files, call LLMs, or
integrate with platforms.

## Why Now

M14-M18 introduced persona, memory, proactive, and virtual life artifacts. A
humanlike companion product needs user control and auditability before any
prototype UI or demo exposes those artifacts. M19 starts by defining what local
controls must exist and which operations require review/audit records.

## Allowed Files

Future T300 worker may create or modify only:

- `docs/requirements/memory_persona_control_requirements.md`
- `docs/tasks/M19_memory_persona_control_surface/T301_memory_viewer_data_contract.md`
- `docs/worker_summary/T300_worker_summary.md`
- `docs/07_handoff.md`

If T300 needs code changes, tests, UI, filesystem deletion, platform adapters,
or task-board edits, Captain must revise this package before assignment.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not call LLMs, model providers, external APIs, browser automation, or
  network services.
- Do not build UI.
- Do not modify, delete, freeze, export, or migrate actual records.
- Do not publish, send, deliver, enqueue, webhook, notify, or call platform
  adapters.
- Do not implement real social-feed integration, voice/avatar/video behavior,
  Live2D, web demo, or product UI.
- Do not implement real-person clone behavior, deceased-person simulation, or
  deceptive impersonation paths.
- Do not modify `docs/04_task_board.md`, `docs/05_decision_log.md`,
  `docs/06_eval_protocol.md`, or `docs/08_risks_and_open_questions.md`.

## Inputs To Read

Required:

- `docs/review/M14_review.md`
- `docs/review/M15_review.md`
- `docs/review/M16_review.md`
- `docs/review/M17_review.md`
- `docs/review/M18_review.md`
- `docs/data_contracts/persona_card_v1.md` if present, otherwise M14 persona
  data contracts under `docs/data_contracts/`
- `docs/data_contracts/memory_event_v2_contract.md`
- `docs/data_contracts/proactive_consent_contract.md`
- `docs/data_contracts/role_dynamic_post_contract.md`

## Expected Outputs

### 1. Requirements Document

Create `docs/requirements/memory_persona_control_requirements.md` with:

- artifact inventory;
- required view controls;
- required edit controls;
- delete/freeze/export requirements;
- audit event requirements;
- review and confirmation requirements;
- privacy and safety boundaries;
- non-goals;
- open questions.

### 2. Next Task Package

Create
`docs/tasks/M19_memory_persona_control_surface/T301_memory_viewer_data_contract.md`
for the Memory Viewer data contract. T301 should define local read-only viewer
data objects first and should not build UI.

### 3. Worker Summary And Handoff

Write `docs/worker_summary/T300_worker_summary.md` and append a T300 worker
record to `docs/07_handoff.md`.

Do not mark T300 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

```powershell
git diff --check
```

No code tests are required unless T300 changes code or tests, which it should
not do.

## Reviewer Type

Adversarial review recommended.

Reviewer should verify that T300 is requirements-only and does not implement UI,
record mutation, deletion, export, sending, platform integration, or LLM calls.
