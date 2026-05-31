# T397: Manual Apply Preview Records

## Task ID

T397

## Goal

Create non-mutating manual apply preview records.

T397 should define local Pydantic records that describe what a future manual
apply action would affect, which gates are required, which blockers remain,
and what rollback/invalidation notes a reviewer must inspect. The records must
not apply anything.

## Allowed Files

Future T397 worker may create or modify only:

- `src/practical_chat_agent/services/manual_apply_preview.py`
- `tests/test_manual_apply_preview_records.py`
- `docs/data_contracts/manual_apply_preview_contract.md`
- `docs/tasks/M31_manual_apply_preview/T398_manual_apply_eligibility_gate.md`
- `docs/worker_summary/T397_worker_summary.md`
- `docs/07_handoff.md`

If T397 needs UI changes, local server routes, private data, model-provider
calls, package changes, platform adapters, outbound messaging, voice/avatar
runtime, media generation, persistence outside local records, or apply
executors, Captain must revise this package before assignment.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not ingest, summarize, transform, quote, or commit real private chat
  records.
- Do not call model providers.
- Do not implement source readers, extraction from real logs, embeddings,
  vector search, semantic ranking, fine-tuning, similarity scoring, persona
  synthesis, final companion reply generation, runtime persona mutation, or
  runtime memory mutation.
- Do not apply review decisions or dry-run plans.
- Do not mutate memory stores, PersonaCard objects, or PersonaVersionStore.
- Do not add routes, CLIs, schedulers, queues, webhooks, auth, tokens,
  recipient ids, delivery state, or platform persistence behavior.
- Do not implement proactive candidates, automatic outreach, sending,
  scheduling, notifications, platform delivery, microphone, camera, ASR, TTS,
  voice cloning, voice/avatar likeness, Live2D, generated audio, generated
  image, generated video, or media capture.
- Do not modify `docs/04_task_board.md`.

## Inputs To Read

Required:

- `docs/product/m31_manual_apply_preview_scope.md`
- `src/practical_chat_agent/services/review_decision_impact_preview.py`
- `src/practical_chat_agent/services/review_workspace.py`
- `src/practical_chat_agent/services/review_queue.py`
- `src/practical_chat_agent/services/review_workspace_export.py`
- existing M28-M30 review workspace tests.

## Expected Outputs

### 1. Preview Records

Create `manual_apply_preview.py` with records such as:

- `ManualApplyPreviewGate`
- `ManualApplyPreviewEffect`
- `ManualApplyPreviewRecord`

Records should include safe ids, candidate kind, decision id, preview outcome,
effect summaries, required gates, blocker codes, rollback notes, source refs,
and non-mutating flags.

### 2. Tests

Create `tests/test_manual_apply_preview_records.py` proving:

- records are serializable and deterministic;
- gates and effects preserve safe summaries only;
- blockers make previews ineligible;
- records always remain preview-only and non-applying;
- forbidden private/provider/outbound/media fields are absent;
- no apply, mutation, provider, outbound, voice/avatar, or media methods exist.

### 3. Data Contract

Create `docs/data_contracts/manual_apply_preview_contract.md`.

### 4. Next Task Package

Create `docs/tasks/M31_manual_apply_preview/T398_manual_apply_eligibility_gate.md`.

### 5. Worker Summary And Handoff

Write `docs/worker_summary/T397_worker_summary.md` and append a T397 worker
record to `docs/07_handoff.md`.

Do not mark T397 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\services\manual_apply_preview.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_manual_apply_preview_records.py -q
```

```powershell
git diff --check
```

Use project-local pytest cache and basetemp paths if the default user temp
directory is not writable.

## Reviewer Type

Adversarial non-mutating record review for privacy, apply-safety, gate
coverage, rollback clarity, and documentation accuracy.
