# T375: M26 Milestone Review

## Task ID

T375

## Goal

Perform an adversarial milestone review of M26 Memory + Persona Implementation
Foundation.

T375 should inspect T370 through T374 outputs and determine whether M26
successfully established local implementation foundations for memory
governance candidates, persona-growth candidates, synthetic distillation input
candidates, and retrieval/explanation integration.

## Why Now

T371 through T374 added the first M26 implementation-layer modules and tests.
Before opening M27, the project needs a review record that distinguishes
implemented behavior from remaining product/runtime work.

## Allowed Files

Future T375 reviewer may create or modify only:

- `docs/review/M26_review.md`
- `docs/worker_summary/T375_worker_summary.md`
- `docs/07_handoff.md`

If T375 needs code edits, test edits, task-board edits, source ingestion,
private data access, provider calls, Browser runs, package changes, routes,
stores, CLIs, persistence behavior, outbound messaging, platform adapters,
voice/avatar runtime, or media generation, Captain must revise this package
before assignment.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not ingest, summarize, transform, quote, or commit real private chat
  records.
- Do not call model providers.
- Do not implement code changes.
- Do not modify tests.
- Do not run or create source readers, embeddings, vector search, semantic
  ranking, fine-tuning, similarity scoring, persona synthesis, final companion
  reply generation, runtime persona mutation, runtime memory mutation,
  schedulers, queues, webhooks, auth, tokens, recipient ids, delivery state,
  microphone, camera, ASR, TTS, voice cloning, voice/avatar likeness, Live2D,
  generated audio, generated image, generated video, or media capture.
- Do not implement real-person recreation, authorized digital twin support,
  grief/deceased-person resurrection, ex-partner clone, family-member clone, or
  public-figure imitation.
- Do not modify `docs/04_task_board.md`.
- Do not claim launch approval, legal compliance, app-store acceptance,
  clinical validation, regulator acceptance, user-study validation, or real
  user evidence.

## Inputs To Read

Required:

- `docs/product/m26_memory_persona_implementation_scope.md`
- `docs/research/memory_retrieval_consolidation_refresh.md`
- `docs/data_contracts/memory_retrieval_consolidation_refresh_contract.md`
- `docs/data_contracts/memory_governance_candidate_contract.md`
- `docs/data_contracts/persona_growth_candidate_implementation_contract.md`
- `docs/data_contracts/synthetic_distillation_input_implementation_contract.md`
- `docs/data_contracts/memory_retrieval_explanation_integration_contract.md`
- `docs/worker_summary/T371_worker_summary.md`
- `docs/worker_summary/T372_worker_summary.md`
- `docs/worker_summary/T373_worker_summary.md`
- `docs/worker_summary/T374_worker_summary.md`
- `tests/test_memory_governance_candidates.py`
- `tests/test_persona_growth_candidates.py`
- `tests/test_synthetic_distillation_input_candidates.py`
- `tests/test_memory_retrieval_explanation_integration.py`

Optional:

- `src/practical_chat_agent/services/memory_governance.py`
- `src/practical_chat_agent/services/persona_growth.py`
- `src/practical_chat_agent/services/synthetic_distillation_input.py`
- `src/practical_chat_agent/services/memory_retrieval_explanation.py`
- `src/practical_chat_agent/core/models.py`

## Expected Outputs

### 1. Review Record

Create `docs/review/M26_review.md` with:

- review verdict: `PASS`, `PASS_WITH_WARNINGS`, or `BLOCK`;
- coverage table for T371 through T374;
- implemented behavior summary;
- safety/privacy boundary assessment;
- test and verification evidence;
- gap list for M27+;
- explicit distinction between candidate/review-only foundations and runtime
  product features.

Recommended verdict is `PASS_WITH_WARNINGS` if implementation tests pass and
boundaries hold, because M26 still does not include retrieval ranking,
user-facing review UI, real import/de-identification, proactive behavior,
voice/avatar, media, platform delivery, or commercial product workflows.

### 2. Worker Summary And Handoff

Write `docs/worker_summary/T375_worker_summary.md` and append a T375 reviewer
record to `docs/07_handoff.md`.

Do not mark T375 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'
pytest tests\test_memory_governance_candidates.py tests\test_persona_growth_candidates.py tests\test_synthetic_distillation_input_candidates.py tests\test_memory_retrieval_explanation_integration.py -q
```

```powershell
git diff --check
```

Use project-local pytest cache and basetemp paths if the default user temp
directory is not writable.

## Reviewer Type

Adversarial milestone, product-safety, privacy, memory lifecycle,
persona-safety, distillation-safety, and documentation-accuracy review.

Reviewer should block if M26 docs claim runtime behavior that does not exist,
if candidate records can directly mutate stores/personas, if forbidden private
data or delivery/media/provider surfaces were introduced, or if tests are
missing the core review-only and exclusion invariants.
