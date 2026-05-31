# Apply Executor Risk Contract

Task: T402 Apply Executor Risk Records
Status: worker draft for review

## Scope

This contract describes non-executing risk assessment records in:

- `src/practical_chat_agent/services/apply_executor_risk.py`

The records represent future apply-executor risk, approval prerequisites,
rollback requirements, audit requirements, blockers, and final recommendation.
They do not apply decisions, mutate memory stores, mutate PersonaCard, write
PersonaVersionStore, delete records, alter retrieval indexes, call providers,
generate replies, send messages, connect to platform APIs, or generate
voice/avatar/media.

## Implemented Records

### ApplyExecutorRiskFactor

Fields include:

- `risk_id`
- `risk_code`
- `severity`
- `safe_summary`
- `source_refs`
- non-executing flags

Severity values:

- `low`
- `medium`
- `high`
- `critical`

### ApplyExecutorApprovalGate

Fields include:

- `gate_id`
- `gate_code`
- `label`
- `safe_summary`
- `satisfied`
- `source_refs`
- non-executing flags

Unsatisfied gates produce blocker codes in the assessment.

### ApplyExecutorRollbackRequirement

Fields include:

- `requirement_id`
- `requirement_code`
- `safe_summary`
- `covered`
- `source_refs`
- non-executing flags

Uncovered rollback requirements produce blocker codes in the assessment.

### ApplyExecutorAuditRequirement

Fields include:

- `requirement_id`
- `event_code`
- `safe_summary`
- `covered`
- `source_refs`
- non-executing flags

Uncovered audit requirements produce blocker codes in the assessment.

### ApplyExecutorRiskAssessment

Fields include:

- `assessment_id`
- `preview_id`
- `decision_id`
- `candidate_kind`
- `candidate_id`
- `safe_summary`
- `risk_factors`
- `approval_gates`
- `rollback_requirements`
- `audit_requirements`
- `blocking_issue_codes`
- `final_recommendation`
- non-executing flags

Final recommendations:

- `blocked`
- `needs_review`
- `ready_for_separately_scoped_executor_design`

Behavior:

- `critical` risks add `critical_risk:<risk_code>` blockers.
- Unsatisfied approval gates add
  `approval_gate_unsatisfied:<gate_code>` blockers.
- Uncovered rollback requirements add
  `rollback_requirement_uncovered:<requirement_code>` blockers.
- Uncovered audit requirements add
  `audit_requirement_uncovered:<event_code>` blockers.
- Any blocker produces `blocked`.
- High risk with no blockers produces `needs_review`.
- Lower risk with all controls covered produces
  `ready_for_separately_scoped_executor_design`.
- `executor_ready` remains false even when the recommendation says the design
  can be separately scoped.

## Required Invariants

All records must preserve:

- `risk_assessment_only=true`
- `executor_ready=false`
- `review_required=true`
- `applies_changes=false`
- `writes_memory_store=false`
- `writes_persona_version=false`
- `runtime_ready=false`

These records are evidence for review only. They are not executable authority.

## Forbidden Fields And Surfaces

Risk records must not contain:

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

The module must not expose methods for apply, mutation, provider calls,
outbound delivery, scheduling, publishing, PersonaVersionStore writes, deletion
execution, retrieval mutation, voice/avatar generation, or media generation.

## Tests

Implemented tests:

- `tests/test_apply_executor_risk_records.py`

Covered behavior:

- ready assessments are serializable and non-executing;
- critical risk blocks future executor readiness;
- missing approval or rollback controls block assessments;
- high risk with covered controls requires review;
- serialized records contain no forbidden private/provider/outbound/media or
  mutation fields;
- records expose no runtime, apply, provider, outbound, voice/avatar, or media
  methods;
- executing flags are rejected.

## Verification

Expected minimum verification:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\services\apply_executor_risk.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_apply_executor_risk_records.py -q -o cache_dir=artifacts\t402_pytest_cache --basetemp=artifacts\t402_pytest_basetemp
```

```powershell
git diff --check
```

## Non-Actions

T402 does not implement:

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

- Risk recommendations are review records, not executable authority.
- No approval gate combines these records with manual apply eligibility yet.
- No UI displays risk records yet.
- No future apply executor exists.
