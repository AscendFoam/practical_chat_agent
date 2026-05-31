# Persona Growth Apply Executor Contract

Task: T407 Persona Growth Apply Executor
Status: worker draft for review

## Scope

This contract describes the local-only persona growth apply executor in:

- `src/practical_chat_agent/services/persona_growth_apply_executor.py`

The executor applies a reviewed `PersonaGrowthDryRunPlan` to a caller-supplied
`PersonaVersionStore` only after explicit final confirmation, manual apply
eligibility, and apply executor approval. It does not read private chat logs,
call providers, mutate memory stores, generate replies, send messages, connect
to platforms, or generate voice/avatar/media.

## Implemented Records

### PersonaGrowthApplyRequest

Fields include:

- `plan`
- `manual_eligibility`
- `approval_decision`
- `persona_store`
- `reviewer_id`
- `final_confirmation`
- local-only and no-provider/no-outbound flags

Required confirmation:

- `CONFIRM_LOCAL_PERSONA_APPLY`

### PersonaGrowthApplyAudit

Fields include:

- `apply_id`
- `persona_id`
- `patch_id`
- `plan_id`
- `review_decision_id`
- `eligibility_id`
- `approval_id`
- `reviewer_id`
- `prior_version_id`
- `new_version_id`
- `rollback_target_version_id`
- `changed_field_paths`
- `safe_summary`
- `final_confirmation=confirmed`
- local-only and no-provider/no-outbound flags

The audit records that a local persona version was written. It does not contain
store paths, private text, provider credentials, platform recipients, message
queues, webhooks, tokens, or media payloads.

### PersonaGrowthApplyExecutor

Method:

- `apply(request)`

Behavior:

- requires final confirmation;
- requires the dry-run plan to be ready for later manual apply;
- requires at least one dry-run field preview;
- requires manual eligibility outcome `eligible`;
- requires apply executor approval outcome
  `ready_for_separately_scoped_executor_design`;
- requires manual eligibility and approval decisions to match the plan
  decision id, candidate kind, and candidate id;
- requires the latest store version to match the dry-run source persona
  version;
- applies reviewed field previews to a copied `PersonaCard`;
- writes exactly one new `PersonaVersionStore` record;
- returns an audit record with rollback target version id.

## Required Invariants

- The executor is local-only.
- It writes only to the caller-supplied `PersonaVersionStore`.
- It never writes memory stores.
- It never calls providers.
- It never sends, schedules, delivers, or connects to platforms.
- It never generates replies, audio, images, video, voice, or avatar output.
- It blocks missing final confirmation, stale source versions, blocked plans,
  blocked manual eligibility, blocked approval, mismatched decisions, and empty
  field previews.

## Tests

Implemented tests:

- `tests/test_persona_growth_apply_executor.py`

Regression tests also run:

- `tests/test_persona_version_store.py`
- `tests/test_persona_growth_dry_run_apply.py`
- `tests/test_apply_executor_approval_gate.py`

Covered behavior:

- safe confirmed persona growth writes one new persona version;
- original version remains available as rollback target;
- missing confirmation blocks writes;
- blocked manual eligibility blocks writes;
- blocked approval blocks writes;
- stale source versions block writes;
- audit records contain no forbidden private/provider/outbound/media fields;
- executor exposes no provider, outbound, scheduler, platform, or media
  methods.

## Verification

Expected minimum verification:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\services\persona_growth_apply_executor.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_persona_growth_apply_executor.py tests\test_persona_version_store.py tests\test_persona_growth_dry_run_apply.py tests\test_apply_executor_approval_gate.py -q -o cache_dir=artifacts\t407_pytest_cache --basetemp=artifacts\t407_pytest_basetemp
```

```powershell
git diff --check
```

## Non-Actions

T407 does not implement:

- memory lifecycle mutation;
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

- The executor is local-only and synthetic/caller-supplied-store-only.
- It does not solve memory lifecycle apply.
- It does not prove production conflict handling or user trust.
- It does not authorize automatic apply behavior.
