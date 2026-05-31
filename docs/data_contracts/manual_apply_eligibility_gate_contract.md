# Manual Apply Eligibility Gate Contract

Task: T398 Manual Apply Eligibility Gate
Status: worker draft for review

## Scope

This contract describes the deterministic non-mutating eligibility gate in:

- `src/practical_chat_agent/services/manual_apply_eligibility_gate.py`

The gate evaluates a `ManualApplyPreviewRecord` and optional expected context,
then returns an eligibility decision. It does not apply decisions, mutate
memory stores, mutate PersonaCard, write PersonaVersionStore, delete records,
alter retrieval indexes, call providers, generate replies, send messages,
connect to platform APIs, or generate voice/avatar/media.

## Implemented Records

### ManualApplyEligibilityDecision

Fields include:

- `preview_id`
- `bundle_id`
- `decision_id`
- `candidate_kind`
- `candidate_id`
- `preview_outcome`
- `eligibility_outcome`
- `safe_summary`
- `required_gate_codes`
- `satisfied_gate_codes`
- `missing_gate_codes`
- `stale_reasons`
- `issue_codes`
- `blocking_issue_codes`
- `effect_count`
- non-mutating flags

Eligibility outcomes:

- `eligible`
- `blocked`
- `stale`

### ManualApplyEligibilityGate

Method:

- `evaluate(preview, expected_decision_id=None, expected_candidate_id=None,
  expected_preview_outcome=None, required_gate_codes=None)`

Behavior:

- returns `stale` when expected context no longer matches the preview;
- returns `blocked` when blockers exist, required gates are missing, or the
  preview record is not eligible;
- returns `eligible` only when the preview record is eligible, all required
  gates are satisfied, and no stale context is detected.

## Required Invariants

All decisions must preserve:

- `review_required=true`
- `preview_only=true`
- `applies_changes=false`
- `writes_memory_store=false`
- `writes_persona_version=false`
- `runtime_ready=false`

Eligibility is a preview label only and is not executable authority.

## Forbidden Fields And Surfaces

Eligibility decisions must not contain:

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

- `tests/test_manual_apply_eligibility_gate.py`

Regression tests also run:

- `tests/test_manual_apply_preview_records.py`

Covered behavior:

- eligible previews produce eligible decisions;
- blocked previews produce blocked decisions;
- stale expected context produces stale decisions;
- required gate mismatches produce blocked decisions;
- serialized decisions contain no forbidden fields;
- gate exposes no runtime/apply/mutation/provider/outbound/media methods.

## Verification

Expected minimum verification:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\services\manual_apply_eligibility_gate.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_manual_apply_eligibility_gate.py tests\test_manual_apply_preview_records.py -q -o cache_dir=artifacts\t398_pytest_cache --basetemp=artifacts\t398_pytest_basetemp
```

```powershell
git diff --check
```

## Non-Actions

T398 does not implement:

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

- Eligibility is not executable authority.
- No UI displays manual apply preview decisions yet.
- No future apply executor exists.
