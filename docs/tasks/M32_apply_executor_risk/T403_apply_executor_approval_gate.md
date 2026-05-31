# T403: Apply Executor Approval Gate

## Task ID

T403

## Goal

Create a deterministic, non-executing approval gate for future apply-executor
design.

T403 should evaluate T402 risk assessments and optional T398 manual apply
eligibility decisions, then return a review-only decision: blocked,
needs_review, or ready_for_separately_scoped_executor_design. It must not
execute anything or mutate state.

## Allowed Files

Future T403 worker may create or modify only:

- `src/practical_chat_agent/services/apply_executor_approval_gate.py`
- `tests/test_apply_executor_approval_gate.py`
- `docs/data_contracts/apply_executor_approval_gate_contract.md`
- `docs/tasks/M32_apply_executor_risk/T404_apply_risk_review_panel.md`
- `docs/worker_summary/T403_worker_summary.md`
- `docs/07_handoff.md`

If T403 needs UI changes, local server routes, private data, model-provider
calls, package changes, platform adapters, outbound messaging, voice/avatar
runtime, media generation, persistence outside local decision records, or apply
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
- Do not apply review decisions, manual apply previews, risk assessments, or
  dry-run plans.
- Do not mutate memory stores, PersonaCard objects, or PersonaVersionStore.
- Do not add routes, CLIs, schedulers, queues, webhooks, auth, tokens,
  recipient ids, delivery state, or platform persistence behavior.
- Do not implement proactive candidates, automatic outreach, sending,
  scheduling, notifications, platform delivery, microphone, camera, ASR, TTS,
  voice cloning, voice/avatar likeness, Live2D, generated audio, generated
  image, generated video, or media capture.
- Do not modify `docs/04_task_board.md`.

## Expected Outputs

### 1. Approval Gate Records

Create `apply_executor_approval_gate.py` with records such as:

- `ApplyExecutorApprovalDecision`
- `ApplyExecutorApprovalGate`

The gate should accept an `ApplyExecutorRiskAssessment` and optional
`ManualApplyEligibilityDecision`.

Decision fields should include safe ids, preview id, decision id, candidate
kind/id, risk recommendation, manual eligibility outcome, stale reasons,
required approval gate codes, satisfied/missing approval gate codes, blockers,
final outcome, safe summary, and non-executing flags.

### 2. Gate Behavior

The gate should:

- return `blocked` when the risk assessment has blockers;
- return `blocked` when required approval gates are missing or unsatisfied;
- return `blocked` when supplied manual apply eligibility is blocked or stale;
- return `blocked` when supplied manual apply eligibility does not match the
  risk assessment preview, decision, candidate kind, or candidate id;
- return `needs_review` for high-risk assessments even when controls are
  covered;
- return `ready_for_separately_scoped_executor_design` only when risk records
  have no blockers, required approvals are satisfied, optional manual
  eligibility is eligible and context-matched, and no stale context is present;
- preserve `executor_ready=false` for every outcome.

### 3. Tests

Create `tests/test_apply_executor_approval_gate.py` proving:

- eligible low/medium-risk assessments with required controls can produce
  `ready_for_separately_scoped_executor_design`;
- blocked risk assessments remain blocked;
- high-risk assessments remain `needs_review`;
- unsatisfied required gates block;
- stale or mismatched manual eligibility blocks;
- decisions always remain review-only and non-executing;
- forbidden private/provider/outbound/media/mutation fields are absent;
- no apply, mutation, provider, outbound, voice/avatar, or media methods exist.

### 4. Data Contract

Create `docs/data_contracts/apply_executor_approval_gate_contract.md`.

### 5. Next Task Package

Create `docs/tasks/M32_apply_executor_risk/T404_apply_risk_review_panel.md`.

### 6. Worker Summary And Handoff

Write `docs/worker_summary/T403_worker_summary.md` and append a T403 worker
record to `docs/07_handoff.md`.

Do not mark T403 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\services\apply_executor_approval_gate.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_apply_executor_approval_gate.py tests\test_apply_executor_risk_records.py tests\test_manual_apply_eligibility_gate.py -q
```

```powershell
git diff --check
```

Use project-local pytest cache and basetemp paths if the default user temp
directory is not writable.

## Reviewer Type

Adversarial non-executing approval-gate review for stale-context detection,
non-apply safety, manual-eligibility integration, privacy, and documentation
accuracy.
