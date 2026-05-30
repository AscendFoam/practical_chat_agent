# T302: Persona Version Editor Contract

## Task ID

T302

## Goal

Define local persona version editor data objects for proposing reviewable
changes to `PersonaCard` fields. T302 should be contract/test work only and
must not build UI or mutate stored persona records.

## Why Now

T301 defines read-only memory inspection. The next control-surface contract
should describe how persona edits are represented as draft proposals before any
reviewed version-store operation is implemented.

## Allowed Files

Future T302 worker may create or modify only:

- `src/practical_chat_agent/core/models.py`
- `tests/test_persona_version_editor_contract.py`
- `docs/data_contracts/persona_version_editor_contract.md`
- `docs/tasks/M19_memory_persona_control_surface/T303_delete_freeze_export_local_flow.md`
- `docs/worker_summary/T302_worker_summary.md`
- `docs/07_handoff.md`

If T302 needs UI, mutation services, actual version-store writes, platform
adapters, or task-board edits, Captain must revise this package before
assignment.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not call LLMs, model providers, external APIs, browser automation, or
  network services.
- Do not build UI.
- Do not modify, delete, freeze, export, or migrate actual records.
- Do not write persona versions to storage.
- Do not publish, send, deliver, enqueue, webhook, notify, or call platform
  adapters.
- Do not modify `docs/04_task_board.md`, `docs/05_decision_log.md`,
  `docs/06_eval_protocol.md`, or `docs/08_risks_and_open_questions.md`.

## Inputs To Read

Required:

- `docs/requirements/memory_persona_control_requirements.md`
- `docs/data_contracts/persona_card_v1_contract.md`
- `docs/data_contracts/persona_version_store_contract.md`
- `src/practical_chat_agent/core/models.py` PersonaCard section
- `tests/test_persona_card_schema.py`
- `tests/test_persona_version_store.py`

## Expected Outputs

### 1. Editor Models And Tests

Add contract models to `src/practical_chat_agent/core/models.py`.

Minimum expected objects:

- `PersonaEditFieldChange`;
- `PersonaVersionEditProposal`;
- `PersonaVersionEditReview`.

Minimum expected behavior:

- proposal references source persona id and version;
- field changes preserve field path, old value summary, proposed value summary,
  reason, and risk labels;
- identity/source-policy/safety fields require review;
- proposal is draft/review-only and does not mutate PersonaCard;
- unsafe or real-person-similarity labels block auto-approval;
- payload contains no send, schedule, delivery, platform, webhook, token, or
  queue fields.

### 2. Data Contract

Create `docs/data_contracts/persona_version_editor_contract.md` describing
fields, invariants, non-actions, and verification.

### 3. Next Task Package

Create
`docs/tasks/M19_memory_persona_control_surface/T303_delete_freeze_export_local_flow.md`
for local delete/freeze/export flow contracts.

### 4. Worker Summary And Handoff

Write `docs/worker_summary/T302_worker_summary.md` and append a T302 worker
record to `docs/07_handoff.md`.

Do not mark T302 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\core\models.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_persona_version_editor_contract.py tests\test_persona_card_schema.py tests\test_persona_version_store.py -q
```

```powershell
git diff --check
```

## Reviewer Type

Adversarial review recommended.

Reviewer should verify that T302 represents draft proposals only and cannot
mutate persona records, send messages, schedule work, or integrate platforms.
