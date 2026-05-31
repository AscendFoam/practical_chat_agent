# M27 Milestone Review

Task: T381 M27 Milestone Review
Verdict: PASS_WITH_WARNINGS

## Findings

No blocking or high-severity issues were found.

## Warnings

### W1: Review queue and dry-run artifacts remain local records only

Severity: warning

Evidence:

- `docs/product/m27_review_queue_dry_run_apply_scope.md:185`
- `docs/data_contracts/review_queue_candidate_contract.md`
- `docs/data_contracts/memory_lifecycle_dry_run_apply_contract.md`
- `docs/data_contracts/persona_growth_dry_run_apply_contract.md`
- `docs/data_contracts/distillation_review_readiness_contract.md`

M27 intentionally stops before UI, persistence, apply executors, real import,
provider-backed extraction, semantic retrieval ranking, proactive messaging,
voice/avatar runtime, media generation, platform delivery, and monetization.
This is acceptable for M27, but M28 must keep those gates explicit before
turning any review or dry-run record into user-facing or mutating behavior.

### W2: Distillation readiness preserves supplied review queue refs without matching them

Severity: warning

Evidence:

- `src/practical_chat_agent/services/distillation_review_readiness.py:92`
- `src/practical_chat_agent/services/distillation_review_readiness.py:200`
- `tests/test_distillation_review_readiness.py:99`

The readiness service preserves `ReviewQueueItem` ids as refs and does not
validate that each queue item corresponds to the supplied manifest or features.
This is acceptable because T380 is review-only and does not apply decisions,
but a future review UI or apply path should enforce candidate-kind and
candidate-id matching.

### W3: Dry-run plans preview effects but do not validate external cascade coverage

Severity: warning

Evidence:

- `src/practical_chat_agent/services/memory_lifecycle_dry_run.py:57`
- `src/practical_chat_agent/services/memory_lifecycle_dry_run.py:89`
- `tests/test_memory_lifecycle_dry_run_apply.py:59`

Memory lifecycle dry-run effects correctly refuse to mutate stores or enable
retrieval, but M27 does not validate cache/index/vector-store cascade coverage
because those executors are intentionally out of scope. Future mutation work
must add separate coverage before any deletion, freeze, archive, or
supersession operation becomes real.

## Reviewed Files

Scope and task packages:

- `docs/product/m27_review_queue_dry_run_apply_scope.md`
- `docs/tasks/M27_review_queue_dry_run_apply/T376_m27_scope.md`
- `docs/tasks/M27_review_queue_dry_run_apply/T377_review_queue_candidate_models.md`
- `docs/tasks/M27_review_queue_dry_run_apply/T378_memory_lifecycle_dry_run_apply.md`
- `docs/tasks/M27_review_queue_dry_run_apply/T379_persona_growth_dry_run_apply.md`
- `docs/tasks/M27_review_queue_dry_run_apply/T380_distillation_review_readiness.md`
- `docs/tasks/M27_review_queue_dry_run_apply/T381_m27_milestone_review.md`

Implementation:

- `src/practical_chat_agent/services/review_queue.py`
- `src/practical_chat_agent/services/memory_lifecycle_dry_run.py`
- `src/practical_chat_agent/services/persona_growth_dry_run.py`
- `src/practical_chat_agent/services/distillation_review_readiness.py`

Tests:

- `tests/test_review_queue_candidates.py`
- `tests/test_memory_lifecycle_dry_run_apply.py`
- `tests/test_persona_growth_dry_run_apply.py`
- `tests/test_distillation_review_readiness.py`

Contracts and summaries:

- `docs/data_contracts/review_queue_candidate_contract.md`
- `docs/data_contracts/memory_lifecycle_dry_run_apply_contract.md`
- `docs/data_contracts/persona_growth_dry_run_apply_contract.md`
- `docs/data_contracts/distillation_review_readiness_contract.md`
- `docs/worker_summary/T376_worker_summary.md`
- `docs/worker_summary/T377_worker_summary.md`
- `docs/worker_summary/T378_worker_summary.md`
- `docs/worker_summary/T379_worker_summary.md`
- `docs/worker_summary/T380_worker_summary.md`
- `docs/07_handoff.md`

## Boundary Evidence

- Review queue items and snapshots require review and block auto-apply:
  `src/practical_chat_agent/services/review_queue.py:67`,
  `src/practical_chat_agent/services/review_queue.py:75`,
  `src/practical_chat_agent/services/review_queue.py:91`, and
  `src/practical_chat_agent/services/review_queue.py:108`.
- Review queue decision records cannot apply changes or write memory/persona
  state:
  `src/practical_chat_agent/services/review_queue.py:130`,
  `src/practical_chat_agent/services/review_queue.py:155`,
  `src/practical_chat_agent/services/review_queue.py:157`, and
  `src/practical_chat_agent/services/review_queue.py:159`.
- Memory lifecycle dry-run effects/plans remain preview-only and cannot enable
  retrieval:
  `src/practical_chat_agent/services/memory_lifecycle_dry_run.py:57`,
  `src/practical_chat_agent/services/memory_lifecycle_dry_run.py:60`,
  `src/practical_chat_agent/services/memory_lifecycle_dry_run.py:71`,
  `src/practical_chat_agent/services/memory_lifecycle_dry_run.py:89`, and
  `src/practical_chat_agent/services/memory_lifecycle_dry_run.py:103`.
- Persona growth dry-run previews/plans remain preview-only and cannot write
  persona versions:
  `src/practical_chat_agent/services/persona_growth_dry_run.py:41`,
  `src/practical_chat_agent/services/persona_growth_dry_run.py:43`,
  `src/practical_chat_agent/services/persona_growth_dry_run.py:94`, and
  `src/practical_chat_agent/services/persona_growth_dry_run.py:108`.
- Distillation readiness summaries require review, are not runtime-ready, and
  block readiness when blocker issues or source text retention exist:
  `src/practical_chat_agent/services/distillation_review_readiness.py:61`,
  `src/practical_chat_agent/services/distillation_review_readiness.py:62`,
  `src/practical_chat_agent/services/distillation_review_readiness.py:64`,
  `src/practical_chat_agent/services/distillation_review_readiness.py:84`, and
  `src/practical_chat_agent/services/distillation_review_readiness.py:172`.

## Verification

```powershell
$env:PYTHONPATH='src'
pytest tests\test_review_queue_candidates.py tests\test_memory_lifecycle_dry_run_apply.py tests\test_persona_growth_dry_run_apply.py tests\test_distillation_review_readiness.py -q -o cache_dir=artifacts\t381_pytest_cache --basetemp=artifacts\t381_pytest_basetemp
```

Result: passed, `24 passed`.

```powershell
git diff --check
```

Result: passed with Windows line-ending conversion warning for
`docs/07_handoff.md`.

Additional read-only scans:

```powershell
rg -n "private/chat_history|private\\chat_history|private/distilled|provider_credentials|platform_recipient|send_queue|webhook|token|microphone|camera|audio_bytes|image_bytes|video_bytes" <M27 source and test files>
```

Result: only safety-boundary tests mention these forbidden fields.

```powershell
rg -n "def (send|schedule|deliver|call_provider|open_webhook|mutate_store|mutate_persona|apply_decision|apply_persona_growth|write_persona_version|delete_memory|update_lifecycle|synthesize_persona|generate_reply|generate_voice|generate_avatar|generate_audio|generate_image|generate_video)\b" <M27 source files>
```

Result: no matches.

```powershell
rg -n "requests\.|httpx|openai|anthropic|websocket|socket|subprocess|Start-Process|Invoke-WebRequest" <M27 source and test files>
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

- Keep M28 scoped to a local review surface or persistence schema before any
  mutation executor.
- Require candidate-kind and candidate-id binding checks before review queue
  decisions can influence readiness or apply previews.
- Require a dedicated dry-run-to-apply task with explicit store/cache/index
  cascade tests before any memory lifecycle mutation.
- Require a separate persona version write review before any PersonaCard or
  PersonaVersionStore mutation.
- Keep real private import/de-identification, provider-backed extraction,
  voice/avatar behavior, proactive messaging, platform delivery, and
  monetization behind separate task packages and reviews.
