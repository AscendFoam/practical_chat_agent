# Apply Executor Approval Gate Contract

Task: T403 Apply Executor Approval Gate
Status: worker draft for review

## Scope

This contract describes the deterministic non-executing approval gate in:

- `src/practical_chat_agent/services/apply_executor_approval_gate.py`

The gate evaluates a T402 `ApplyExecutorRiskAssessment` and optional T398
`ManualApplyEligibilityDecision`, then returns a review-only approval decision.
It does not apply decisions, mutate memory stores, mutate PersonaCard, write
PersonaVersionStore, delete records, alter retrieval indexes, call providers,
generate replies, send messages, connect to platform APIs, or generate
voice/avatar/media.

## Implemented Records

### ApplyExecutorApprovalDecision

Fields include:

- `approval_id`
- `assessment_id`
- `preview_id`
- `decision_id`
- `candidate_kind`
- `candidate_id`
- `risk_recommendation`
- `manual_eligibility_outcome`
- `safe_summary`
- `required_approval_gate_codes`
- `satisfied_approval_gate_codes`
- `missing_approval_gate_codes`
- `stale_reasons`
- `issue_codes`
- `risk_blocking_issue_codes`
- `manual_blocking_issue_codes`
- `blocking_issue_codes`
- `final_outcome`
- non-executing flags

Final outcomes:

- `blocked`
- `needs_review`
- `ready_for_separately_scoped_executor_design`

Manual eligibility states:

- `eligible`
- `blocked`
- `stale`
- `not_supplied`

### ApplyExecutorApprovalGate

Method:

- `evaluate(risk_assessment, manual_eligibility=None,
  required_approval_gate_codes=None)`

Behavior:

- returns `blocked` when the risk assessment has blockers;
- returns `blocked` when required approval gates are missing or unsatisfied;
- returns `blocked` when supplied manual eligibility is blocked or stale;
- returns `blocked` when supplied manual eligibility does not match the risk
  assessment preview id, decision id, candidate kind, or candidate id;
- returns `needs_review` when the risk assessment recommendation is
  `needs_review` and no blocker is present;
- returns `ready_for_separately_scoped_executor_design` only when no blocker is
  present, required approvals are satisfied, and supplied manual eligibility is
  eligible and context-matched;
- preserves `executor_ready=false` for every outcome.

## Required Invariants

All decisions must preserve:

- `review_required=true`
- `risk_assessment_only=true`
- `executor_ready=false`
- `applies_changes=false`
- `writes_memory_store=false`
- `writes_persona_version=false`
- `runtime_ready=false`

Approval decisions are review evidence only. They are not executable
authorization.

## Forbidden Fields And Surfaces

Approval decisions must not contain:

- raw private chat text;
- raw transcripts;
- private message bodies;
- private chat history paths;
- provider credentials;
- platform recipient ids;
- send queues;
- schedules;
- webhooks;
- tokens;
- microphone, camera, audio, image, or video payloads;
- generated media paths;
- internal queue item ids;
- decision apply executor fields;
- mutation executor fields.

The gate must not expose methods for apply, mutation, provider calls, outbound
delivery, scheduling, publishing, PersonaVersionStore writes, deletion
execution, retrieval mutation, voice/avatar generation, or media generation.

## Tests

Implemented tests:

- `tests/test_apply_executor_approval_gate.py`

Regression tests also run:

- `tests/test_apply_executor_risk_records.py`
- `tests/test_manual_apply_eligibility_gate.py`

Covered behavior:

- ready low/medium-risk assessments can produce
  `ready_for_separately_scoped_executor_design`;
- blocked risk assessments remain blocked;
- high-risk assessments remain `needs_review`;
- unsatisfied required gates block;
- stale or mismatched manual eligibility blocks;
- serialized decisions contain no forbidden fields;
- gate and decision records expose no runtime/apply/mutation/provider/outbound
  or media methods;
- executing flags are rejected.

## Verification

Expected minimum verification:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\services\apply_executor_approval_gate.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_apply_executor_approval_gate.py tests\test_apply_executor_risk_records.py tests\test_manual_apply_eligibility_gate.py -q -o cache_dir=artifacts\t403_pytest_cache --basetemp=artifacts\t403_pytest_basetemp
```

```powershell
git diff --check
```

## Non-Actions

T403 does not implement:

- apply executors;
- manual apply execution;
- memory store writes;
- PersonaCard mutation;
- PersonaVersionStore writes;
- deletion executors;
- retrieval index mutation;
- UI changes;
- local server routes;
- private data ingestion;
- source readers;
- extraction from real logs;
- embeddings;
- vector search;
- semantic ranking;
- similarity scoring;
- model-provider calls;
- PersonaCard synthesis;
- final companion reply generation;
- proactive candidates;
- automatic sending or scheduling;
- platform integration;
- voice/avatar/video behavior;
- generated media;
- legal, clinical, launch, app-store, or regulator approval.

## Residual Risks

- Approval outcomes are not executable authority.
- No UI displays risk approval decisions yet.
- No future apply executor exists.
