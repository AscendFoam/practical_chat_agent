# T372: Persona Growth Candidate Models

## Task ID

T372

## Goal

Implement local synthetic persona growth candidate records and tests.

T372 should turn the M25 persona growth patch contract into executable local
models without enabling runtime persona mutation, auto-apply, provider calls,
private data ingestion, proactive messaging, voice/avatar runtime, media
generation, platform delivery, or real-person recreation.

## Why Now

T371 implements memory governance candidate records. Persona growth should use
those tested evidence boundaries before it proposes changes to PersonaCard
fields. T372 should prove that growth remains bounded, review-required,
version-ready, reversible, and blocked against dependency, real-person
similarity, voice/avatar likeness, and other high-risk changes.

## Allowed Files

Future T372 worker may create or modify only:

- `src/practical_chat_agent/services/persona_growth.py`
- `tests/test_persona_growth_candidates.py`
- `docs/data_contracts/persona_growth_candidate_implementation_contract.md`
- `docs/tasks/M26_memory_persona_implementation/T373_synthetic_distillation_input_models.md`
- `docs/worker_summary/T372_worker_summary.md`
- `docs/07_handoff.md`

If T372 needs other source files, fixtures, task-board edits, private data,
Browser runs, model-provider calls, package changes, persistence, routes,
stores, CLIs, platform adapters, outbound messaging, voice/avatar runtime, or
media generation, Captain must revise this package before assignment.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not ingest, summarize, transform, quote, or commit real private chat
  records.
- Do not call model providers.
- Do not implement source readers, extraction, embeddings, vector search,
  semantic ranking, fine-tuning, similarity scoring, persona synthesis, final
  companion reply generation, or runtime persona mutation.
- Do not modify `PersonaCard`, `PersonaVersionStore`, or persona review state
  directly from patch candidates.
- Do not create stores, routes, CLIs, schedulers, queues, webhooks, auth,
  tokens, recipient ids, delivery state, or persistence behavior.
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

- `docs/product/m26_memory_persona_implementation_scope.md`
- `docs/product/persona_growth_policy.md`
- `docs/data_contracts/persona_growth_patch_contract.md`
- `docs/data_contracts/memory_governance_candidate_contract.md`
- `src/practical_chat_agent/core/models.py`
- `src/practical_chat_agent/services/memory_governance.py`
- `src/practical_chat_agent/services/persona_review.py`
- `src/practical_chat_agent/services/persona_version_store.py`
- `tests/test_persona_card_schema.py`
- `tests/test_persona_review.py`
- `tests/test_persona_version_store.py`
- `tests/test_memory_governance_candidates.py`

## Expected Outputs

### 1. Persona Growth Models

Create `src/practical_chat_agent/services/persona_growth.py` with local
Pydantic models and deterministic validation for:

- `PersonaGrowthFieldChange`
- `PersonaGrowthPatchCandidate`
- `PersonaGrowthPatchReview`
- `PersonaGrowthJournalEntry`

The records should preserve source persona id, source version, evidence memory
ids, review refs, field paths, old/new value summaries, numeric deltas, safety
warnings, clone/similarity warnings, review status, and user-facing
explanations.

### 2. Tests

Create `tests/test_persona_growth_candidates.py` with synthetic-only tests that
prove:

- every patch is review-required;
- auto-apply is impossible;
- frozen fields cannot be changed;
- unknown field paths are rejected;
- numeric deltas cannot exceed policy caps;
- weekly trait movement cannot exceed `max_weekly_trait_delta`;
- `core_traits.jealousy` cannot increase by default;
- blocking safety labels block approval;
- imagined memory cannot justify factual identity changes;
- rejected, frozen, archived, or needs-changes patches do not create persona
  versions;
- review records do not write PersonaCard versions directly;
- forbidden private/provider/outbound/platform/media fields are absent.

### 3. Data Contract

Create `docs/data_contracts/persona_growth_candidate_implementation_contract.md`
describing the implemented records, invariants, forbidden fields, tests,
non-actions, and residual risks.

### 4. Next Task Package

Create
`docs/tasks/M26_memory_persona_implementation/T373_synthetic_distillation_input_models.md`
for synthetic distillation input candidate model implementation.

### 5. Worker Summary And Handoff

Write `docs/worker_summary/T372_worker_summary.md` and append a T372 worker
record to `docs/07_handoff.md`.

Do not mark T372 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\services\persona_growth.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_persona_growth_candidates.py tests\test_memory_governance_candidates.py tests\test_persona_card_schema.py tests\test_persona_review.py tests\test_persona_version_store.py -q
```

```powershell
git diff --check
```

Use project-local pytest cache and basetemp paths if the default user temp
directory is not writable.

## Reviewer Type

Adversarial persona-safety, memory-governance, dependency-risk, privacy,
real-person likeness, and product-safety review recommended.

Reviewer should block if T372 allows auto-apply, mutates PersonaCard directly,
weakens stable-core protections, increases jealousy/dependency/isolation, uses
private data, permits real-person likeness drift, introduces provider/platform
outbound/media behavior, or implies runtime persona growth is enabled.
