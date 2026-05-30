# T301: Memory Viewer Data Contract

## Task ID

T301

## Goal

Define local read-only Memory Viewer data objects for inspecting `MemoryEvent`
records and related retrieval/lifecycle metadata. T301 should prepare data
contracts and tests only; it must not build UI or mutate records.

## Why Now

T300 defined control-surface requirements. The first concrete control artifact
should be a read-only memory viewer contract so users can inspect what the
companion remembers before edit/delete/freeze/export flows exist.

## Allowed Files

Future T301 worker may create or modify only:

- `src/practical_chat_agent/core/models.py`
- `tests/test_memory_viewer_contract.py`
- `docs/data_contracts/memory_viewer_contract.md`
- `docs/tasks/M19_memory_persona_control_surface/T302_persona_version_editor_contract.md`
- `docs/worker_summary/T301_worker_summary.md`
- `docs/07_handoff.md`

If T301 needs UI, mutation services, deletion/export code, platform adapters,
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
- Do not modify `docs/04_task_board.md`, `docs/05_decision_log.md`,
  `docs/06_eval_protocol.md`, or `docs/08_risks_and_open_questions.md`.

## Inputs To Read

Required:

- `docs/requirements/memory_persona_control_requirements.md`
- `docs/data_contracts/memory_event_v2_contract.md`
- `docs/data_contracts/memory_retrieval_bundle_v2_contract.md`
- `docs/data_contracts/memory_lifecycle_v2_contract.md`
- `src/practical_chat_agent/core/models.py` memory sections
- `tests/test_memory_event_schema.py`
- `tests/test_memory_retrieval_bundle_schema.py`

## Expected Outputs

### 1. Viewer Models And Tests

Add read-only viewer models to `src/practical_chat_agent/core/models.py`.

Minimum expected objects:

- `MemoryViewerItem`;
- `MemoryViewerFilter`;
- `MemoryViewerPage`.

Minimum expected behavior:

- preserves memory id, event type, truth status, sensitivity, lifecycle state,
  review-required status, summary, provenance refs, created/updated timestamps,
  and safety notes;
- exposes `can_edit`, `can_delete`, `can_freeze`, and `can_export` booleans as
  permissions metadata only;
- deleted/frozen/archived memory is visible as non-retrieval-eligible;
- imagined memory is labeled and cannot be shown as factual evidence;
- viewer payload contains no raw private text, send, schedule, delivery,
  platform, webhook, token, or queue fields.

### 2. Data Contract

Create `docs/data_contracts/memory_viewer_contract.md` describing viewer fields,
filters, invariants, non-actions, and verification.

### 3. Next Task Package

Create
`docs/tasks/M19_memory_persona_control_surface/T302_persona_version_editor_contract.md`.
T302 should define a local persona version editor contract without building UI.

### 4. Worker Summary And Handoff

Write `docs/worker_summary/T301_worker_summary.md` and append a T301 worker
record to `docs/07_handoff.md`.

Do not mark T301 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\core\models.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_memory_viewer_contract.py tests\test_memory_event_schema.py tests\test_memory_retrieval_bundle_schema.py -q
```

```powershell
git diff --check
```

## Reviewer Type

Adversarial review recommended.

Reviewer should verify that T301 is read-only data-contract work and cannot
mutate, delete, export, send, schedule, or integrate with platforms.
