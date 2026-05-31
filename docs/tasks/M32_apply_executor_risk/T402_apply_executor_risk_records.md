# T402: Apply Executor Risk Records

## Task ID

T402

## Goal

Create non-executing apply executor risk assessment records.

T402 should define local Pydantic records for risk factors, approval gates,
rollback requirements, audit requirements, and final risk recommendation. The
records must not execute anything or mutate state.

## Allowed Files

Future T402 worker may create or modify only:

- `src/practical_chat_agent/services/apply_executor_risk.py`
- `tests/test_apply_executor_risk_records.py`
- `docs/data_contracts/apply_executor_risk_contract.md`
- `docs/tasks/M32_apply_executor_risk/T403_apply_executor_approval_gate.md`
- `docs/worker_summary/T402_worker_summary.md`
- `docs/07_handoff.md`

If T402 needs UI changes, local server routes, private data, model-provider
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
- Do not apply review decisions, manual apply previews, or dry-run plans.
- Do not mutate memory stores, PersonaCard objects, or PersonaVersionStore.
- Do not add routes, CLIs, schedulers, queues, webhooks, auth, tokens,
  recipient ids, delivery state, or platform persistence behavior.
- Do not implement proactive candidates, automatic outreach, sending,
  scheduling, notifications, platform delivery, microphone, camera, ASR, TTS,
  voice cloning, voice/avatar likeness, Live2D, generated audio, generated
  image, generated video, or media capture.
- Do not modify `docs/04_task_board.md`.

## Expected Outputs

### 1. Risk Records

Create `apply_executor_risk.py` with records such as:

- `ApplyExecutorRiskFactor`
- `ApplyExecutorApprovalGate`
- `ApplyExecutorRollbackRequirement`
- `ApplyExecutorAuditRequirement`
- `ApplyExecutorRiskAssessment`

Records should include safe ids, candidate kind/id, decision id, risk severity,
required approvals, rollback requirements, audit requirements, blockers, and
non-executing flags.

### 2. Tests

Create `tests/test_apply_executor_risk_records.py` proving:

- records are serializable and deterministic;
- critical risk or missing approval blocks executor readiness;
- rollback and audit requirements are preserved;
- records always remain risk-assessment-only and non-executing;
- forbidden private/provider/outbound/media/mutation fields are absent;
- no apply, mutation, provider, outbound, voice/avatar, or media methods exist.

### 3. Data Contract

Create `docs/data_contracts/apply_executor_risk_contract.md`.

### 4. Next Task Package

Create
`docs/tasks/M32_apply_executor_risk/T403_apply_executor_approval_gate.md`.

### 5. Worker Summary And Handoff

Write `docs/worker_summary/T402_worker_summary.md` and append a T402 worker
record to `docs/07_handoff.md`.

Do not mark T402 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\services\apply_executor_risk.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_apply_executor_risk_records.py -q
```

```powershell
git diff --check
```

Use project-local pytest cache and basetemp paths if the default user temp
directory is not writable.

## Reviewer Type

Adversarial non-executing risk-record review for mutation safety, approval
coverage, rollback clarity, auditability, privacy, and documentation accuracy.
