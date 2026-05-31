# T379: Persona Growth Dry-Run Apply Plans

## Task ID

T379

## Goal

Implement local deterministic dry-run plans for persona growth patch
candidates.

T379 should preview how a `PersonaGrowthPatchCandidate` would affect a
`PersonaCard` if later approved by a separate apply path. It must not mutate
`PersonaCard`, write `PersonaVersionStore`, apply review decisions, call
providers, read private data, send messages, create UI, or connect to
platforms/media.

## Why Now

T378 previews memory lifecycle effects. Persona growth needs the same
preview-only layer before any real version-writing or user-facing edit flow is
implemented.

## Allowed Files

Future T379 worker may create or modify only:

- `src/practical_chat_agent/services/persona_growth_dry_run.py`
- `tests/test_persona_growth_dry_run_apply.py`
- `docs/data_contracts/persona_growth_dry_run_apply_contract.md`
- `docs/tasks/M27_review_queue_dry_run_apply/T380_distillation_review_readiness.md`
- `docs/worker_summary/T379_worker_summary.md`
- `docs/07_handoff.md`

If T379 needs other source files, fixtures, task-board edits, private data,
Browser runs, model-provider calls, package changes, persistence, routes,
stores, CLIs, platform adapters, outbound messaging, voice/avatar runtime, or
media generation, Captain must revise this package before assignment.

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
- Do not mutate `PersonaCard`.
- Do not write `PersonaVersionStore`.
- Do not apply review decisions.
- Do not auto-apply growth patches.
- Do not create UI, routes, CLIs, schedulers, queues, webhooks, auth, tokens,
  recipient ids, delivery state, or persistence behavior.
- Do not implement proactive candidates, automatic outreach, sending,
  scheduling, notifications, platform delivery, microphone, camera, ASR, TTS,
  voice cloning, voice/avatar likeness, Live2D, generated audio, generated
  image, generated video, or media capture.
- Do not implement real-person recreation, authorized digital twin support,
  grief/deceased-person resurrection, ex-partner clone, family-member clone, or
  public-figure imitation.
- Do not modify `docs/04_task_board.md`.
- Do not claim launch approval, legal compliance, app-store acceptance,
  clinical validation, regulator acceptance, user-study validation, or real
  user evidence.

## Inputs To Read

Required:

- `docs/product/m27_review_queue_dry_run_apply_scope.md`
- `docs/data_contracts/review_queue_candidate_contract.md`
- `docs/data_contracts/persona_growth_candidate_implementation_contract.md`
- `src/practical_chat_agent/services/review_queue.py`
- `src/practical_chat_agent/services/persona_growth.py`
- `src/practical_chat_agent/core/models.py`
- relevant persona growth and review queue tests.

## Expected Outputs

### 1. Dry-Run Plan Records And Service

Create `src/practical_chat_agent/services/persona_growth_dry_run.py` with:

- `PersonaGrowthDryRunFieldPreview`
- `PersonaGrowthDryRunPlan`
- `PersonaGrowthDryRunService`

Required behavior:

- create preview records from a `PersonaGrowthPatchCandidate`;
- optionally attach a `ReviewQueueDecisionRecord`;
- preserve source persona id/version and patch id;
- preview field paths, old summaries, proposed summaries, numeric deltas, and
  source refs;
- mark blocked fields and blocking risk labels;
- keep `preview_only=true`, `applies_changes=false`, and
  `writes_persona_version=false`;
- never mutate the input `PersonaCard`.

### 2. Tests

Create `tests/test_persona_growth_dry_run_apply.py` with synthetic-only tests
that prove:

- dry-run plans preserve PersonaCard state;
- safe field previews are listed without writing versions;
- blocked labels prevent apply readiness;
- weekly delta cap status is visible;
- review decisions are referenced but not applied;
- frozen or unknown fields remain blocked by upstream patch validation;
- models reject forbidden private/provider/outbound/media fields;
- service exposes no send/schedule/deliver/provider/mutation/media methods.

### 3. Data Contract

Create `docs/data_contracts/persona_growth_dry_run_apply_contract.md`
describing implemented records, invariants, forbidden fields, tests,
verification, non-actions, and residual risks.

### 4. Next Task Package

Create
`docs/tasks/M27_review_queue_dry_run_apply/T380_distillation_review_readiness.md`
for synthetic distillation review readiness aggregation.

### 5. Worker Summary And Handoff

Write `docs/worker_summary/T379_worker_summary.md` and append a T379 worker
record to `docs/07_handoff.md`.

Do not mark T379 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\services\persona_growth_dry_run.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_persona_growth_dry_run_apply.py tests\test_persona_growth_candidates.py tests\test_review_queue_candidates.py -q
```

```powershell
git diff --check
```

Use project-local pytest cache and basetemp paths if the default user temp
directory is not writable.

## Reviewer Type

Adversarial persona-growth, dry-run safety, privacy, review queue,
product-safety, and documentation-accuracy review.

Reviewer should block if T379 mutates PersonaCard, writes persona versions,
applies decisions, allows private/provider/outbound/media fields, reads private
data, calls providers, exposes send/schedule/deliver/runtime methods, or
implies launch or production readiness.
