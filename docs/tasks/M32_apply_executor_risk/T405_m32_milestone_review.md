# T405: M32 Milestone Review

## Task ID

T405

## Goal

Perform an adversarial review of M32 Apply Executor Risk.

T405 should review T401 through T404 together: scope, risk records, approval
gate, read-only UI panel, tests, contracts, and handoff. The review should
decide whether M32 can close before any future milestone considers a real apply
executor.

## Allowed Files

Future T405 reviewer may create or modify only:

- `docs/review/M32_review.md`
- `docs/worker_summary/T405_worker_summary.md`
- `docs/07_handoff.md`

If T405 needs code changes, test changes, task-board edits, private data,
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
- Do not apply review decisions, manual apply previews, risk assessments,
  approval decisions, or dry-run plans.
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

- `docs/product/m32_apply_executor_risk_scope.md`
- `docs/data_contracts/apply_executor_risk_contract.md`
- `docs/data_contracts/apply_executor_approval_gate_contract.md`
- `docs/data_contracts/review_workspace_apply_risk_panel_contract.md`
- `src/practical_chat_agent/services/apply_executor_risk.py`
- `src/practical_chat_agent/services/apply_executor_approval_gate.py`
- `src/practical_chat_agent/ui/text_first_web_demo_adapter.py`
- `src/practical_chat_agent/ui/static/text_first_web_demo.js`
- `src/practical_chat_agent/ui/static/text_first_web_demo.css`
- `tests/test_apply_executor_risk_records.py`
- `tests/test_apply_executor_approval_gate.py`
- `tests/test_review_workspace_apply_risk_panel.py`
- related review workspace static/local server/apply preview tests.

## Expected Outputs

### 1. Milestone Review

Create `docs/review/M32_review.md` with:

- verdict: `PASS`, `PASS_WITH_WARNINGS`, or `BLOCK`;
- reviewed files and tests;
- findings ordered by severity;
- privacy/provider/outbound/media/apply safety assessment;
- risk-record and approval-gate assessment;
- read-only UI assessment;
- residual risks;
- recommendation for the next milestone.

### 2. Worker Summary And Handoff

Write `docs/worker_summary/T405_worker_summary.md` and append a T405 review
record to `docs/07_handoff.md`.

Do not mark M32 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\services\apply_executor_risk.py src\practical_chat_agent\services\apply_executor_approval_gate.py src\practical_chat_agent\ui\text_first_web_demo_adapter.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_apply_executor_risk_records.py tests\test_apply_executor_approval_gate.py tests\test_review_workspace_apply_risk_panel.py tests\test_review_workspace_apply_preview_panel.py tests\test_review_workspace_local_server_payload.py tests\test_review_workspace_static_panel.py -q
```

```powershell
git diff --check
```

Use project-local pytest cache and basetemp paths if the default user temp
directory is not writable.

## Reviewer Type

Adversarial milestone review for non-execution safety, privacy, executor-risk
clarity, approval-gate correctness, UI read-only guarantees, and residual-risk
clarity.
