# T400: M31 Milestone Review

## Task ID

T400

## Goal

Perform an adversarial review of M31 Manual Apply Preview.

T400 should review T396 through T399 together: scope, preview records,
eligibility gate, read-only UI panel, tests, contracts, and handoff. The review
should decide whether M31 can close before any future milestone considers a
real apply executor.

## Allowed Files

Future T400 reviewer may create or modify only:

- `docs/review/M31_review.md`
- `docs/worker_summary/T400_worker_summary.md`
- `docs/07_handoff.md`

If T400 needs code changes, test changes, task-board edits, private data,
Browser runs, model-provider calls, package changes, platform adapters,
outbound messaging, voice/avatar runtime, media generation, or apply
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

## Inputs To Review

Required:

- `docs/product/m31_manual_apply_preview_scope.md`
- `docs/data_contracts/manual_apply_preview_contract.md`
- `docs/data_contracts/manual_apply_eligibility_gate_contract.md`
- `docs/data_contracts/review_workspace_apply_preview_panel_contract.md`
- `src/practical_chat_agent/services/manual_apply_preview.py`
- `src/practical_chat_agent/services/manual_apply_eligibility_gate.py`
- `src/practical_chat_agent/ui/text_first_web_demo_adapter.py`
- `src/practical_chat_agent/ui/static/text_first_web_demo.js`
- `src/practical_chat_agent/ui/static/text_first_web_demo.css`
- `tests/test_manual_apply_preview_records.py`
- `tests/test_manual_apply_eligibility_gate.py`
- `tests/test_review_workspace_apply_preview_panel.py`
- related review workspace static/local server tests.

## Expected Outputs

### 1. Milestone Review

Create `docs/review/M31_review.md` with:

- verdict: `PASS`, `PASS_WITH_WARNINGS`, or `BLOCK`;
- reviewed files and tests;
- findings ordered by severity;
- privacy/provider/outbound/media/apply safety assessment;
- manual apply preview and eligibility assessment;
- read-only UI assessment;
- residual risks;
- recommendation for the next milestone.

### 2. Worker Summary And Handoff

Write `docs/worker_summary/T400_worker_summary.md` and append a T400 review
record to `docs/07_handoff.md`.

Do not mark M31 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\services\manual_apply_preview.py src\practical_chat_agent\services\manual_apply_eligibility_gate.py src\practical_chat_agent\ui\text_first_web_demo_adapter.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_manual_apply_preview_records.py tests\test_manual_apply_eligibility_gate.py tests\test_review_workspace_apply_preview_panel.py tests\test_review_workspace_local_server_payload.py tests\test_review_workspace_static_panel.py -q
```

```powershell
git diff --check
```

Use project-local pytest cache and basetemp paths if the default user temp
directory is not writable.

## Reviewer Type

Adversarial milestone review for non-mutation safety, privacy, apply preview
clarity, UI read-only guarantees, and residual-risk clarity.
