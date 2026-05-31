# T370: M26 Memory Persona Implementation Scope

## Task ID

T370

## Goal

Define the M26 implementation-foundation milestone for memory governance,
persona growth, and synthetic distillation readiness.

M26 should turn selected M25 contracts into local synthetic candidate models,
fixtures, services, and tests. It should not introduce private data, model
providers, platform delivery, proactive sending, voice/avatar runtime,
generated media, or real-person recreation.

## Why Now

M25 created the planning and contract layer for:

- advanced typed memory;
- contradiction and supersession handling;
- consent withdrawal and deletion cascade planning;
- explainable retrieval/consolidation surfaces;
- bounded persona growth patches;
- synthetic de-identified distillation inputs.

The next milestone should prove these boundaries in code before the project
considers any private-data, retrieval-ranking, provider-backed, or user-facing
runtime expansion.

## Allowed Files

Future T370 worker may create or modify only:

- `docs/product/m26_memory_persona_implementation_scope.md`
- `docs/tasks/M26_memory_persona_implementation/T371_memory_governance_candidate_models.md`
- `docs/worker_summary/T370_worker_summary.md`
- `docs/07_handoff.md`

If T370 needs Python source, tests, fixtures, private data, Browser runs,
model-provider calls, package changes, persistence, routes, stores, task-board
edits, platform adapters, outbound messaging, voice/avatar runtime, or media
generation, Captain must revise this package before assignment.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not ingest, summarize, transform, quote, or commit real private chat
  records.
- Do not call model providers.
- Do not add or modify Python source code or tests in T370.
- Do not create stores, routes, CLIs, schedulers, queues, webhooks, auth,
  tokens, recipient ids, delivery state, or persistence behavior.
- Do not implement extraction, embeddings, vector search, ranking, fine-tuning,
  de-identification scoring, persona synthesis, final companion reply
  generation, proactive candidates, or platform delivery.
- Do not enable automatic outreach, sending, scheduling, notifications,
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

- `docs/review/M25_review.md`
- `docs/product/m25_memory_persona_growth_scope.md`
- `docs/research/memory_architecture_design.md`
- `docs/data_contracts/memory_architecture_contract.md`
- `docs/product/persona_growth_policy.md`
- `docs/data_contracts/persona_growth_patch_contract.md`
- `docs/product/synthetic_distillation_input_policy.md`
- `docs/data_contracts/synthetic_distillation_input_contract.md`
- `docs/research/memory_retrieval_consolidation_refresh.md`
- `docs/data_contracts/memory_retrieval_consolidation_refresh_contract.md`
- `docs/worker_summary/T360_worker_summary.md`
- `docs/worker_summary/T361_worker_summary.md`
- `docs/worker_summary/T362_worker_summary.md`
- `docs/worker_summary/T363_worker_summary.md`
- `docs/worker_summary/T364_worker_summary.md`
- `docs/worker_summary/T365_worker_summary.md`

## Expected Outputs

### 1. M26 Scope

Create `docs/product/m26_memory_persona_implementation_scope.md` with:

- milestone objective;
- M25 invariants to preserve;
- local synthetic fixture strategy;
- implementation sequence;
- proposed test acceptance gates;
- explicit non-goals;
- residual risks.

The recommended M26 task sequence is:

1. T371: memory governance candidate models and synthetic tests for
   contradiction, supersession, deletion cascade, and explanation trace.
2. T372: persona growth patch candidate models and tests for frozen fields,
   review states, safety labels, trait deltas, rollback readiness, and
   auto-apply blocking.
3. T373: synthetic distillation input candidate models and tests for speaker
   aliases, redaction refs, consent refs, clone-risk blocking, third-party
   minimization, and fictional persona input invariants.
4. T374: retrieval/consolidation explanation service tests for lifecycle,
   review-required, consent-withdrawal, imagined/factual separation, and
   include/exclude reasons.
5. T375: M26 milestone review.

### 2. T371 Task Package

Create
`docs/tasks/M26_memory_persona_implementation/T371_memory_governance_candidate_models.md`
for the first implementation task.

T371 should be allowed to touch only narrowly scoped source/test/fixture/docs
files that implement local synthetic candidate records and tests. It should
continue to forbid private data, provider calls, outbound messaging, voice,
avatar, media generation, and real-person recreation.

### 3. Worker Summary And Handoff

Write `docs/worker_summary/T370_worker_summary.md` and append a T370 worker
record to `docs/07_handoff.md`.

Do not mark T370 complete in `docs/04_task_board.md`.

## Verification

Minimum command:

```powershell
git diff --check
```

## Reviewer Type

Adversarial implementation-scope, privacy, memory-safety, persona-safety,
distillation-safety, and product-safety review recommended.

Reviewer should block if T370 recommends private-data ingestion, provider
calls, automatic outreach, platform delivery, voice/avatar runtime, generated
media, real-person recreation, unreviewed persona growth, or direct runtime
mutation before local synthetic models and tests prove the M25 gates.
