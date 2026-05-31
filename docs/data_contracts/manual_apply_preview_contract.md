# Manual Apply Preview Contract

Task: T397 Manual Apply Preview Records
Status: worker draft for review

## Scope

This contract describes non-mutating manual apply preview records implemented
in:

- `src/practical_chat_agent/services/manual_apply_preview.py`

The records summarize what a future manual apply action would need to inspect.
They do not apply review decisions, mutate memory stores, mutate PersonaCard,
write PersonaVersionStore, delete records, alter retrieval indexes, call
providers, generate replies, send messages, connect to platform APIs, or
generate voice/avatar/media.

## Implemented Records

### ManualApplyPreviewGate

Fields include:

- `gate_code`
- `label`
- `safe_summary`
- `satisfied`
- `blocking_issue_codes`
- `source_refs`
- `blocks_preview`
- non-mutating flags

Unsatisfied gates automatically block the preview and include
`manual_apply_gate_unsatisfied`.

### ManualApplyPreviewEffect

Fields include:

- `effect_kind`
- `target_ref`
- `safe_summary`
- `artifact_ids`
- `source_refs`
- `rollback_notes`
- non-mutating flags

Supported effect kinds:

- `memory_store_preview`
- `persona_version_preview`
- `deletion_preview`
- `cache_invalidation_preview`

### ManualApplyPreviewRecord

Fields include:

- `bundle_id`
- `decision_id`
- `candidate_kind`
- `candidate_id`
- `preview_outcome`
- `safe_summary`
- `reason_labels`
- `source_refs`
- `artifact_ids`
- `required_gates`
- `effects`
- `rollback_notes`
- `issue_codes`
- `blocking_issue_codes`
- `manual_apply_preview_eligible`
- `effect_count`
- non-mutating flags

`ManualApplyPreviewRecord.from_impact_preview(...)` projects a
`ReviewDecisionImpactPreview` into a manual apply preview record without
carrying internal queue ids.

## Required Invariants

All records must preserve:

- `review_required=true`
- `preview_only=true`
- `applies_changes=false`
- `writes_memory_store=false`
- `writes_persona_version=false`
- `runtime_ready=false`

`manual_apply_preview_eligible` is true only when:

- the decision impact outcome is `future_manual_apply_eligible`;
- there are no blocking issue codes;
- all required gates are satisfied.

Eligibility is a preview label only and is not executable authority.

## Forbidden Fields And Surfaces

Records must not contain:

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

Records must not expose methods for apply, mutation, provider calls, outbound
delivery, scheduling, publishing, PersonaVersionStore writes, deletion
execution, retrieval mutation, voice/avatar generation, or media generation.

## Tests

Implemented tests:

- `tests/test_manual_apply_preview_records.py`

Covered behavior:

- records are serializable and non-mutating;
- satisfied gates and effects can make an eligible preview;
- unsatisfied gates block preview eligibility;
- blocked decision impact previews remain ineligible;
- serialized records contain no forbidden private/provider/outbound/media or
  internal queue fields;
- records expose no runtime/apply/mutation/provider/outbound/media methods;
- mutating flags are rejected.

## Verification

Expected minimum verification:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\services\manual_apply_preview.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_manual_apply_preview_records.py -q -o cache_dir=artifacts\t397_pytest_cache --basetemp=artifacts\t397_pytest_basetemp
```

```powershell
git diff --check
```

## Non-Actions

T397 does not implement:

- apply executors;
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

- Preview eligibility is not executable authority.
- T398 still needs an eligibility gate over preview records.
- No UI displays these records yet.
- No future apply executor exists.
