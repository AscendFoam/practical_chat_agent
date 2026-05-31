# Memory Lifecycle Apply Executor Contract

Task: T408 Memory Lifecycle Apply Executor
Status: worker draft for review

## Scope

This contract describes the local-only memory lifecycle apply executor in:

- `src/practical_chat_agent/services/memory_lifecycle_apply_executor.py`

The executor applies a reviewed `MemoryLifecycleDryRunPlan` to a
caller-supplied `MemoryEventStore` only after explicit final confirmation,
manual apply eligibility, and apply executor approval. It does not read private
chat logs, call providers, write persona versions, generate replies, send
messages, connect to platforms, or generate voice/avatar/media.

## Implemented Records

### MemoryLifecycleApplyRequest

Fields include:

- `plan`
- `manual_eligibility`
- `approval_decision`
- `memory_store`
- `reviewer_id`
- `final_confirmation`
- local-only and no-provider/no-outbound flags

Required confirmation:

- `CONFIRM_LOCAL_MEMORY_APPLY`

### MemoryLifecycleApplyAudit

Fields include:

- `apply_id`
- `plan_id`
- `source_candidate_kind`
- `source_candidate_id`
- `review_decision_id`
- `eligibility_id`
- `approval_id`
- `reviewer_id`
- `affected_memory_ids`
- `prior_lifecycle_states`
- `new_lifecycle_states`
- `rollback_record_ids`
- `applied_record_ids`
- `safe_summary`
- `final_confirmation=confirmed`
- local-only and no-provider/no-outbound flags

The audit records that local memory lifecycle records were written. It does not
contain store paths, private text, provider credentials, platform recipients,
message queues, webhooks, tokens, or media payloads.

### MemoryLifecycleApplyExecutor

Method:

- `apply(request)`

Behavior:

- requires final confirmation;
- requires the dry-run plan to be approved;
- requires at least one dry-run effect;
- requires manual eligibility outcome `eligible`;
- requires apply executor approval outcome
  `ready_for_separately_scoped_executor_design`;
- requires manual eligibility and approval decisions to match the plan
  decision id, candidate kind, and candidate id;
- pre-validates all target memory ids before writing any lifecycle update;
- applies only actions present in dry-run effects;
- maps lifecycle actions to local states:
  - `delete` -> `deleted`;
  - `archive` and `reject_new` -> `archived`;
  - `freeze`, `suppress_retrieval`, and `training_exclusion` -> `frozen`;
  - `supersede` -> `superseded`;
- collapses multiple effects for one memory id to the strongest local state;
- writes only to the caller-supplied `MemoryEventStore`;
- returns an audit record with rollback record ids.

## Required Invariants

- The executor is local-only.
- It writes only to the caller-supplied `MemoryEventStore`.
- It never writes persona versions.
- It never calls providers.
- It never sends, schedules, delivers, or connects to platforms.
- It never generates replies, audio, images, video, voice, or avatar output.
- It blocks missing final confirmation, unapproved plans, blocked manual
  eligibility, blocked approval, mismatched decisions, missing memory ids,
  unsupported effects, and empty effect lists.

## Tests

Implemented tests:

- `tests/test_memory_lifecycle_apply_executor.py`

Regression tests also run:

- `tests/test_memory_event_store.py`
- `tests/test_memory_lifecycle_dry_run_apply.py`
- `tests/test_apply_executor_approval_gate.py`

Covered behavior:

- safe confirmed memory lifecycle apply updates local lifecycle state;
- prior records remain available as rollback evidence;
- missing confirmation blocks writes;
- blocked manual eligibility blocks writes;
- blocked approval blocks writes;
- missing memory ids block writes;
- audit records contain no forbidden private/provider/outbound/media fields;
- executor exposes no provider, outbound, scheduler, platform, or media
  methods.

## Verification

Expected minimum verification:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\services\memory_lifecycle_apply_executor.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_memory_lifecycle_apply_executor.py tests\test_memory_event_store.py tests\test_memory_lifecycle_dry_run_apply.py tests\test_apply_executor_approval_gate.py -q -o cache_dir=artifacts\t408_pytest_cache --basetemp=artifacts\t408_pytest_basetemp
```

```powershell
git diff --check
```

## Non-Actions

T408 does not implement:

- persona version mutation;
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

- The executor is local-only and caller-supplied-store-only.
- It does not display apply audit records in the review workspace yet.
- It does not authorize automatic apply behavior.
