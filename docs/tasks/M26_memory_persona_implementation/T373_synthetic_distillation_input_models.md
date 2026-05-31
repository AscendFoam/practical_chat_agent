# T373: Synthetic Distillation Input Models

## Task ID

T373

## Goal

Implement local synthetic distillation input candidate records and tests.

T373 should turn the M25 synthetic distillation input contract into executable
local models without enabling private chat ingestion, source readers,
embeddings, similarity scoring, model-provider calls, persona synthesis,
voice/avatar likeness, platform delivery, outbound messaging, generated media,
or real-person recreation.

## Why Now

T371 implemented memory governance candidates and T372 implemented persona
growth candidates. The next implementation layer should make de-identified
style inspiration input auditable and testable before any future task considers
private source material or persona synthesis.

## Allowed Files

Future T373 worker may create or modify only:

- `src/practical_chat_agent/services/synthetic_distillation_input.py`
- `tests/test_synthetic_distillation_input_candidates.py`
- `docs/data_contracts/synthetic_distillation_input_implementation_contract.md`
- `docs/tasks/M26_memory_persona_implementation/T374_memory_retrieval_explanation_integration.md`
- `docs/worker_summary/T373_worker_summary.md`
- `docs/07_handoff.md`

If T373 needs other source files, fixtures, task-board edits, private data,
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
  synthesis, final companion reply generation, or runtime persona mutation.
- Do not store raw source text, full transcripts, real names, real account ids,
  real file names, exact private quotes, voice samples, images, video, or
  generated media paths.
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
- `docs/product/synthetic_distillation_input_policy.md`
- `docs/data_contracts/synthetic_distillation_input_contract.md`
- `docs/data_contracts/memory_governance_candidate_contract.md`
- `docs/data_contracts/persona_growth_candidate_implementation_contract.md`
- `src/practical_chat_agent/core/models.py`
- `src/practical_chat_agent/services/memory_governance.py`
- `src/practical_chat_agent/services/persona_growth.py`
- `tests/test_memory_governance_candidates.py`
- `tests/test_persona_growth_candidates.py`

## Expected Outputs

### 1. Synthetic Distillation Input Models

Create `src/practical_chat_agent/services/synthetic_distillation_input.py` with
local Pydantic models and deterministic validation for:

- `SyntheticDistillationInputManifest`
- `SyntheticDistillationSourceSegment`
- `SyntheticSpeakerAlias`
- `DistillationConsentRef`
- `DistillationRedactionRef`
- `DeidentifiedStyleFeatureCandidate`
- `CloneRiskDecision`
- `FictionalPersonaSynthesisInput`

The records should preserve aliases, synthetic markers, redaction refs, consent
refs, clone-risk flags, abstract style labels, and fictional-persona output
invariants.

### 2. Tests

Create `tests/test_synthetic_distillation_input_candidates.py` with
synthetic-only tests that prove:

- committed source segments are synthetic and do not contain raw private text;
- speaker aliases replace real identities;
- third parties are minimized by default;
- withdrawn consent blocks feature candidates;
- clone-risk flags block unsafe manifests;
- biometric, ex-partner, family-member, deceased-person, public-figure,
  hidden-impersonation, and minor-risk flags block safe transformation;
- feature outputs are abstract labels, not raw quotes;
- fictional persona synthesis inputs are review-required and never
  runtime-ready;
- voice/avatar scopes remain inactive or blocked;
- forbidden private/provider/outbound/platform/media fields are absent.

### 3. Data Contract

Create
`docs/data_contracts/synthetic_distillation_input_implementation_contract.md`
describing the implemented records, invariants, forbidden fields, tests,
non-actions, and residual risks.

### 4. Next Task Package

Create
`docs/tasks/M26_memory_persona_implementation/T374_memory_retrieval_explanation_integration.md`
for retrieval, consolidation, and explanation integration tests.

### 5. Worker Summary And Handoff

Write `docs/worker_summary/T373_worker_summary.md` and append a T373 worker
record to `docs/07_handoff.md`.

Do not mark T373 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\services\synthetic_distillation_input.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_synthetic_distillation_input_candidates.py tests\test_memory_governance_candidates.py tests\test_persona_growth_candidates.py -q
```

```powershell
git diff --check
```

Use project-local pytest cache and basetemp paths if the default user temp
directory is not writable.

## Reviewer Type

Adversarial privacy, de-identification, real-person likeness,
distillation-safety, persona-safety, and product-safety review recommended.

Reviewer should block if T373 reads private data, retains real identifiers,
allows raw quotes, allows clone-risk flags through, enables runtime persona
synthesis, weakens fictional disclosure, introduces provider/platform/outbound
or voice/avatar/media behavior, or implies real-person recreation is supported.
