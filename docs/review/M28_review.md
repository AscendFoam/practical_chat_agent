# M28 Milestone Review

Task: T387 M28 Milestone Review
Verdict: PASS_WITH_WARNINGS

## Findings

No blocking or high-severity issues were found.

## Warnings

### W1: Review workspace records remain local prototype records only

Severity: warning

Evidence:

- `docs/product/m28_local_review_workspace_scope.md`
- `docs/data_contracts/review_workspace_binding_contract.md`
- `docs/data_contracts/review_workspace_snapshot_store_contract.md`
- `docs/data_contracts/review_decision_impact_preview_contract.md`
- `docs/data_contracts/review_workspace_safe_export_contract.md`

M28 intentionally stops before a user-facing review UI, real apply executor,
real private import/de-identification, provider-backed extraction, semantic
retrieval ranking, proactive messaging, voice/avatar runtime, media
generation, platform delivery, monetization, and production persistence. This
is acceptable for M28, but later milestones must keep these gates explicit.

### W2: Safe exports summarize safe records but do not prove source safety

Severity: warning

Evidence:

- `src/practical_chat_agent/services/review_workspace_export.py:190`
- `src/practical_chat_agent/services/review_workspace_export.py:231`
- `src/practical_chat_agent/services/review_workspace_export.py:242`
- `tests/test_review_workspace_safe_export.py:254`

Safe export manifests include only safe summaries, ids, labels, refs, issue
codes, counts, and preview flags. They do not independently validate that the
source candidates were de-identified correctly or that upstream source refs are
safe in every future importer. A later real import path still needs separate
de-identification and source-safety evaluation.

### W3: Manual-apply eligibility is a preview label, not executable authority

Severity: warning

Evidence:

- `src/practical_chat_agent/services/review_decision_impact_preview.py:140`
- `src/practical_chat_agent/services/review_decision_impact_preview.py:180`
- `src/practical_chat_agent/services/review_decision_impact_preview.py:184`
- `tests/test_review_decision_impact_preview.py:115`

T385 correctly marks unblocked approve decisions as
`future_manual_apply_eligible`, but this is only a local preview outcome. M28
does not implement store/cache/index cascade coverage, PersonaVersionStore
writes, deletion executors, or production authorization.

## Reviewed Files

Scope and task packages:

- `docs/product/m28_local_review_workspace_scope.md`
- `docs/tasks/M28_local_review_workspace/T382_m28_scope.md`
- `docs/tasks/M28_local_review_workspace/T383_review_workspace_bindings.md`
- `docs/tasks/M28_local_review_workspace/T384_review_workspace_snapshot_store.md`
- `docs/tasks/M28_local_review_workspace/T385_review_decision_impact_preview.md`
- `docs/tasks/M28_local_review_workspace/T386_review_workspace_safe_export.md`
- `docs/tasks/M28_local_review_workspace/T387_m28_milestone_review.md`

Implementation:

- `src/practical_chat_agent/services/review_workspace.py`
- `src/practical_chat_agent/services/review_workspace_store.py`
- `src/practical_chat_agent/services/review_decision_impact_preview.py`
- `src/practical_chat_agent/services/review_workspace_export.py`

Tests:

- `tests/test_review_workspace_bindings.py`
- `tests/test_review_workspace_snapshot_store.py`
- `tests/test_review_decision_impact_preview.py`
- `tests/test_review_workspace_safe_export.py`

Contracts and summaries:

- `docs/data_contracts/review_workspace_binding_contract.md`
- `docs/data_contracts/review_workspace_snapshot_store_contract.md`
- `docs/data_contracts/review_decision_impact_preview_contract.md`
- `docs/data_contracts/review_workspace_safe_export_contract.md`
- `docs/worker_summary/T382_worker_summary.md`
- `docs/worker_summary/T383_worker_summary.md`
- `docs/worker_summary/T384_worker_summary.md`
- `docs/worker_summary/T385_worker_summary.md`
- `docs/worker_summary/T386_worker_summary.md`
- `docs/07_handoff.md`

## Boundary Evidence

- Workspace candidate bindings require review and are never runtime-ready:
  `src/practical_chat_agent/services/review_workspace.py:91`,
  `src/practical_chat_agent/services/review_workspace.py:92`,
  `src/practical_chat_agent/services/review_workspace.py:97`, and
  `src/practical_chat_agent/services/review_workspace.py:99`.
- Workspace artifact bindings and bundles remain preview-only and cannot
  apply changes or write memory/persona state:
  `src/practical_chat_agent/services/review_workspace.py:126`,
  `src/practical_chat_agent/services/review_workspace.py:128`,
  `src/practical_chat_agent/services/review_workspace.py:129`,
  `src/practical_chat_agent/services/review_workspace.py:130`,
  `src/practical_chat_agent/services/review_workspace.py:166`,
  `src/practical_chat_agent/services/review_workspace.py:167`,
  `src/practical_chat_agent/services/review_workspace.py:168`, and
  `src/practical_chat_agent/services/review_workspace.py:169`.
- Candidate/artifact mismatch blockers are explicit:
  `src/practical_chat_agent/services/review_workspace.py:218`,
  `src/practical_chat_agent/services/review_workspace.py:225`,
  `src/practical_chat_agent/services/review_workspace.py:255`,
  `src/practical_chat_agent/services/review_workspace.py:262`, and
  `src/practical_chat_agent/services/review_workspace.py:272`.
- Snapshot storage uses Pydantic validation and rejects paths outside the store
  root:
  `src/practical_chat_agent/services/review_workspace_store.py:35`,
  `src/practical_chat_agent/services/review_workspace_store.py:36`,
  `src/practical_chat_agent/services/review_workspace_store.py:66`, and
  `src/practical_chat_agent/services/review_workspace_store.py:70`.
- Impact previews force blockers to `blocked_before_apply` and keep manual
  apply eligibility as a non-executing flag:
  `src/practical_chat_agent/services/review_decision_impact_preview.py:180`,
  `src/practical_chat_agent/services/review_decision_impact_preview.py:181`,
  `src/practical_chat_agent/services/review_decision_impact_preview.py:183`,
  and `src/practical_chat_agent/services/review_decision_impact_preview.py:184`.
- Safe export manifests remain non-applying, compute deterministic counts, and
  reject paths outside the export root:
  `src/practical_chat_agent/services/review_workspace_export.py:196`,
  `src/practical_chat_agent/services/review_workspace_export.py:197`,
  `src/practical_chat_agent/services/review_workspace_export.py:198`,
  `src/practical_chat_agent/services/review_workspace_export.py:231`,
  `src/practical_chat_agent/services/review_workspace_export.py:242`, and
  `src/practical_chat_agent/services/review_workspace_export.py:310`.

## Verification

```powershell
$env:PYTHONPATH='src'
pytest tests\test_review_workspace_bindings.py tests\test_review_workspace_snapshot_store.py tests\test_review_decision_impact_preview.py tests\test_review_workspace_safe_export.py -q -o cache_dir=artifacts\t387_pytest_cache --basetemp=artifacts\t387_pytest_basetemp
```

Result: passed, `29 passed`.

```powershell
git diff --check
```

Result: passed with Windows line-ending conversion warning for
`docs/07_handoff.md`.

Additional read-only scans:

```powershell
rg -n "private/chat_history|private\\chat_history|private/distilled|provider_credentials|platform_recipient|send_queue|webhook|token|microphone|camera|audio_bytes|image_bytes|video_bytes" <M28 source and test files>
```

Result: only safety-boundary tests mention these forbidden fields.

```powershell
rg -n "def (send|schedule|deliver|call_provider|open_webhook|mutate_store|mutate_persona|apply_decision|apply_persona_growth|write_persona_version|delete_memory|update_lifecycle|synthesize_persona|generate_reply|generate_voice|generate_avatar|generate_audio|generate_image|generate_video)\b" <M28 source files>
```

Result: no matches.

```powershell
rg -n "requests\.|httpx|openai|anthropic|websocket|socket|subprocess|Start-Process|Invoke-WebRequest" <M28 source and test files>
```

Result: no matches.

## Explicit Non-Actions Confirmed

- No private chat history, private distilled artifact, or private source file
  was read, quoted, summarized, transformed, or committed.
- No model provider, network, embedding, vector search, semantic ranking,
  fine-tuning, or similarity scoring behavior was added.
- No review decision apply path was added.
- No memory store mutation, deletion executor, retrieval enablement,
  PersonaCard mutation, or PersonaVersionStore write was added.
- No final companion reply generation, proactive candidate, automatic sending,
  scheduling, notification, queue delivery, webhook, token, platform adapter,
  voice/avatar runtime, audio/image/video generation, microphone, camera,
  ASR, TTS, or Live2D behavior was added.
- No production, launch, legal, app-store, clinical, regulator, user-study, or
  real-user evidence claim was made.

## Recommended Next Gates

- Keep M29 focused on a local review UI or review workspace presentation
  adapter before any mutation executor.
- Require a separate dry-run-to-apply milestone with explicit store/cache/index
  cascade coverage before any memory lifecycle mutation.
- Require separate PersonaVersionStore write review before any persona growth
  patch can mutate a PersonaCard or version store.
- Require real private import/de-identification quality evaluation before any
  chat-history distillation pipeline can process private data.
- Keep provider-backed extraction, proactive messaging, platform delivery,
  voice/avatar behavior, media generation, and monetization behind separate
  task packages and reviews.
