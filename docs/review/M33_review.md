# M33 Controlled Apply Executor Review

Review target: T407 through T410
Reviewer posture: adversarial local mutation review
Verdict: PASS_WITH_WARNINGS

## Scope Reviewed

M33 introduced the first controlled local apply path:

- T407: local persona growth apply executor;
- T408: local memory lifecycle apply executor;
- T409: local apply executor audit manifest;
- T410: review workspace apply audit panel.

The milestone was reviewed as a local-only, explicit-human-confirmed apply
system. It was not reviewed as production automatic apply, platform delivery,
model-provider execution, real private-chat ingestion, or runtime companion
mutation.

## Findings

No blocking defects were found in the reviewed M33 scope.

Warnings:

- The executors are intentionally local and caller-supplied-store-only. This is
  acceptable for M33, but it is not a production authorization model.
- The review workspace cards use synthetic demo audits. This proves projection
  shape and privacy filtering, not production persistence or real user
  evidence.
- M33 does not add policy for automatic apply. Automatic apply remains outside
  scope and should stay blocked until a separate consent, rollback, and abuse
  review milestone exists.
- M33 does not prove concurrent edit handling beyond the source-version check
  in persona growth apply and pre-validation in memory lifecycle apply.

## Local-Only Apply Boundaries

PASS_WITH_WARNINGS.

Evidence:

- `PersonaGrowthApplyRequest` requires `local_only=True`, `review_required=True`,
  `automatic_apply=False`, `calls_provider=False`, `sends_messages=False`, and
  `runtime_ready=False`.
- `MemoryLifecycleApplyRequest` requires the same local/no-provider/no-outbound
  boundary flags.
- `ApplyExecutorAuditManifestBuilder` is a read-model builder only and does not
  write stores.
- Review workspace projection sets display cards to `changes_state=false`.

Residual risk:

- Local flags are model-level guardrails, not a full authorization subsystem.

## Final Confirmation Gates

PASS.

Evidence:

- Persona apply requires `CONFIRM_LOCAL_PERSONA_APPLY`.
- Memory lifecycle apply requires `CONFIRM_LOCAL_MEMORY_APPLY`.
- Audit manifest entries require `final_confirmation=confirmed`.
- Tests cover missing confirmation blocking writes.

## Manual Eligibility Gates

PASS.

Evidence:

- Persona apply requires manual eligibility outcome `eligible` and candidate
  kind/id/decision matching.
- Memory lifecycle apply requires manual eligibility outcome `eligible` and
  candidate kind/id/decision matching.
- Tests cover blocked manual eligibility blocking writes.

## Apply Executor Approval Gates

PASS.

Evidence:

- Persona and memory apply require final approval outcome
  `ready_for_separately_scoped_executor_design`.
- Tests cover blocked approval blocking writes.
- Audit manifest preserves `approval_id`.

## Persona Version Rollback Evidence

PASS_WITH_WARNINGS.

Evidence:

- Persona apply writes one new `PersonaVersionStore` record.
- Persona apply audit records `prior_version_id`, `new_version_id`, and
  `rollback_target_version_id`.
- Audit manifest preserves persona rollback references.

Residual risk:

- Rollback is evidenced, not executed by M33.

## Memory Lifecycle Rollback Evidence

PASS_WITH_WARNINGS.

Evidence:

- Memory lifecycle apply pre-validates all target memory ids before writing.
- It records prior lifecycle states, new lifecycle states, rollback record ids,
  and applied record ids.
- Missing memory id tests prove no partial write for that case.
- Audit manifest preserves memory rollback record ids.

Residual risk:

- Rollback is evidenced, not executed by M33.

## Audit Manifest Completeness

PASS.

Evidence:

- T409 normalizes persona and memory apply audits into one manifest.
- Unsupported schemas are rejected.
- Missing rollback evidence is rejected.
- Entries sort deterministically by created time and apply id.
- Gate ids, reviewer id, source artifact ids, changed field paths, affected
  memory ids, rollback refs, and applied refs are preserved.

## Review Workspace Projection Safety

PASS_WITH_WARNINGS.

Evidence:

- T410 projects apply audit entries as `review_workspace_apply_audit_card_v1`.
- Static UI renders apply type, source artifact, reviewer, gate ids, changed
  fields, affected memories, and rollback refs.
- Browser QA confirmed 2 apply audit cards in the Review scenario, with persona
  audit text, memory audit text, and rollback refs present.

Residual risk:

- Browser QA used synthetic local static data; production persistence is not in
  scope.

## Forbidden Surface Checks

PASS.

Evidence:

- M33 focused tests assert no private/provider/outbound/media fields in audit
  records, manifests, and review payloads.
- Static tests check that UI hooks do not introduce platform delivery or media
  generation actions.
- No private chat history or private distilled artifacts were read.

## Fresh Verification

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\services\persona_growth_apply_executor.py src\practical_chat_agent\services\memory_lifecycle_apply_executor.py src\practical_chat_agent\services\apply_executor_audit_manifest.py src\practical_chat_agent\ui\text_first_web_demo_adapter.py
```

Result: passed.

```powershell
$env:PYTHONPATH='src'
pytest tests\test_persona_growth_apply_executor.py tests\test_memory_lifecycle_apply_executor.py tests\test_apply_executor_audit_manifest.py tests\test_review_workspace_apply_audit_panel.py -q -o cache_dir=artifacts\t411_pytest_cache --basetemp=artifacts\t411_pytest_basetemp
```

Result: passed, `21 passed`.

## Verdict

M33 is fit to close as `PASS_WITH_WARNINGS`.

The warnings are not blockers for the milestone because M33 explicitly scoped
itself to local, explicit, audited apply behavior. They should remain visible
when planning future production authorization, rollback execution, and
automatic apply work.
