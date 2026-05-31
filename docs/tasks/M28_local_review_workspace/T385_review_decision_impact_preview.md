# T385: Review Decision Impact Preview

## Task ID

T385

## Goal

Implement deterministic, non-applying impact previews for review queue
decisions attached to review workspace bundles and dry-run/readiness artifacts.

T385 should combine a `ReviewQueueDecisionRecord` with its matching
`ReviewWorkspaceBundle` and artifact bindings so a later local review surface
can show what an approve, reject, freeze, or request-changes decision would
mean. It must not apply review decisions, mutate memory/persona state, call
providers, create UI, send messages, or connect to platforms/media.

## Why Now

T383 added explicit candidate/artifact bindings and T384 added safe local
snapshot storage. M28 next needs review decision impact previews before any
future apply executor exists, so reviewers can inspect effects and blockers
without trusting mismatched refs or changing state.

## Allowed Files

Future T385 worker may create or modify only:

- `src/practical_chat_agent/services/review_decision_impact_preview.py`
- `tests/test_review_decision_impact_preview.py`
- `docs/data_contracts/review_decision_impact_preview_contract.md`
- `docs/tasks/M28_local_review_workspace/T386_review_workspace_safe_export.md`
- `docs/worker_summary/T385_worker_summary.md`
- `docs/07_handoff.md`

If T385 needs other source files, fixtures, task-board edits, private data,
Browser runs, model-provider calls, package changes, routes, CLIs, platform
adapters, outbound messaging, voice/avatar runtime, media generation,
persistence outside safe local records, or apply executors, Captain must
revise this package before assignment.

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
- Do not apply review decisions or dry-run plans.
- Do not mutate memory stores, PersonaCard objects, or PersonaVersionStore.
- Do not create UI, routes, CLIs, schedulers, queues, webhooks, auth, tokens,
  recipient ids, delivery state, or platform persistence behavior.
- Do not implement proactive candidates, automatic outreach, sending,
  scheduling, notifications, platform delivery, microphone, camera, ASR, TTS,
  voice cloning, voice/avatar likeness, Live2D, generated audio, generated
  image, generated video, or media capture.
- Do not modify `docs/04_task_board.md`.
- Do not claim launch approval, legal compliance, app-store acceptance,
  clinical validation, regulator acceptance, user-study validation, or real
  user evidence.

## Inputs To Read

Required:

- `docs/product/m28_local_review_workspace_scope.md`
- `docs/data_contracts/review_queue_candidate_contract.md`
- `docs/data_contracts/review_workspace_binding_contract.md`
- `docs/data_contracts/review_workspace_snapshot_store_contract.md`
- `docs/data_contracts/memory_lifecycle_dry_run_apply_contract.md`
- `docs/data_contracts/persona_growth_dry_run_apply_contract.md`
- `docs/data_contracts/distillation_review_readiness_contract.md`
- `src/practical_chat_agent/services/review_queue.py`
- `src/practical_chat_agent/services/review_workspace.py`
- `src/practical_chat_agent/services/review_workspace_store.py`
- `src/practical_chat_agent/services/memory_lifecycle_dry_run.py`
- `src/practical_chat_agent/services/persona_growth_dry_run.py`
- `src/practical_chat_agent/services/distillation_review_readiness.py`
- relevant M28 tests.

## Expected Outputs

### 1. Impact Preview Records And Service

Create `src/practical_chat_agent/services/review_decision_impact_preview.py`
with:

- `ReviewDecisionImpactIssue`
- `ReviewDecisionArtifactImpact`
- `ReviewDecisionImpactPreview`
- `ReviewDecisionImpactPreviewService`

Required behavior:

- accept a `ReviewWorkspaceBundle` and a `ReviewQueueDecisionRecord`;
- find the matching candidate binding by queue item id, candidate kind, and
  candidate id;
- report blocker issues when the decision does not match any candidate binding;
- report blocker issues when the matching candidate binding or artifact
  binding has blockers;
- include only safe ids, decision label, reviewer id, safe summaries, reason
  labels, source refs, issue codes, and preview flags;
- summarize artifact impact for memory lifecycle dry-run plans, persona
  growth dry-run plans, and distillation readiness summaries;
- map decision labels to non-applying preview outcomes:
  - `approve`: eligible for a future manual apply only when no blockers exist;
  - `reject`: rejected for future apply;
  - `freeze`: frozen for later reconsideration;
  - `request_changes`: needs reviewer-requested changes before later apply;
- keep all preview records review-required, preview-only, non-applying,
  non-mutating, and non-runtime-ready.

### 2. Tests

Create `tests/test_review_decision_impact_preview.py` with synthetic-only
tests that prove:

- approve decisions on ready bundles produce preview-only manual-apply
  eligibility but do not apply changes;
- reject, freeze, and request-changes decisions produce the expected
  non-applying preview outcomes;
- mismatched decision item ids, candidate kinds, or candidate ids produce
  blocker issues;
- existing workspace binding blockers are carried into the impact preview;
- artifact impacts preserve safe artifact refs without applying dry-run plans;
- serialized previews do not contain forbidden private/provider/outbound/media
  fields;
- service exposes no send/schedule/deliver/provider/mutation/apply/synthesis
  or media methods.

### 3. Data Contract

Create `docs/data_contracts/review_decision_impact_preview_contract.md`
describing implemented records, invariants, forbidden fields, tests,
verification, non-actions, and residual risks.

### 4. Next Task Package

Create
`docs/tasks/M28_local_review_workspace/T386_review_workspace_safe_export.md`
for safe local export manifests over review workspace snapshots and impact
previews.

### 5. Worker Summary And Handoff

Write `docs/worker_summary/T385_worker_summary.md` and append a T385 worker
record to `docs/07_handoff.md`.

Do not mark T385 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\services\review_decision_impact_preview.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_review_decision_impact_preview.py tests\test_review_workspace_snapshot_store.py tests\test_review_workspace_bindings.py -q
```

```powershell
git diff --check
```

Use project-local pytest cache and basetemp paths if the default user temp
directory is not writable.

## Reviewer Type

Adversarial review decision impact, non-apply safety, binding correctness,
privacy, dry-run safety, product-safety, and documentation-accuracy review.

Reviewer should block if T385 applies decisions, mutates memory/persona state,
writes PersonaVersionStore, trusts mismatched refs, reads private data, calls
providers, exposes send/schedule/deliver/runtime methods, allows
private/provider/outbound/media fields, or implies launch or production
readiness.
