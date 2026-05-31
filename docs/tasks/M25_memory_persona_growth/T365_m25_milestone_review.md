# T365: M25 Milestone Review

## Task ID

T365

## Goal

Review M25 memory, persona growth, and distillation-readiness planning and
decide whether the project can proceed to an implementation-foundation
milestone.

## Why Now

T360 through T364 should have scoped M25, designed the memory architecture,
defined persona growth patches, defined synthetic distillation input
boundaries, and refreshed memory consolidation/retrieval/explanation contracts.
M25 needs an adversarial gate before any follow-up task introduces code,
fixtures, stores, extraction, retrieval changes, or runtime behavior.

## Allowed Files

Future T365 worker may create or modify only:

- `docs/review/M25_review.md`
- `docs/tasks/M26_memory_persona_implementation/T370_m26_scope.md`
- `docs/worker_summary/T365_worker_summary.md`
- `docs/07_handoff.md`

If T365 needs code changes, tests, Browser runs, model-provider calls,
generated media, private data processing, persistence, task-board edits,
platform adapters, outbound messaging, voice/avatar runtime, or screenshot
artifacts, Captain must revise this package before assignment.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not ingest, summarize, transform, or quote real private chat records.
- Do not call model providers.
- Do not add or modify Python source code or tests.
- Do not create stores, routes, CLIs, schedulers, send paths, queues, webhooks,
  platform adapters, auth, tokens, or persistence behavior.
- Do not implement retrieval ranking, vector search, embeddings, extraction,
  persona growth patch application, distillation, dialogue runtime, proactive
  candidates, or platform delivery.
- Do not enable automatic outreach, sending, scheduling, voice, avatar, Live2D,
  camera, microphone, ASR, TTS, media generation, or media capture.
- Do not implement real-person recreation, authorized digital twin support, or
  private-chat distillation.
- Do not modify `docs/04_task_board.md`.
- Do not claim legal advice, compliance completion, app-store approval, launch
  approval, user-study validation, regulator acceptance, or real user evidence.

## Inputs To Read

Required:

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

## Expected Outputs

### 1. M25 Review

Create `docs/review/M25_review.md` with:

- gate recommendation;
- T360 through T364 coverage summary;
- architecture and contract artifacts;
- verification evidence;
- safety boundary assessment;
- explicit non-actions;
- residual risks;
- M26 entry recommendation.

### 2. M26 Scope Task

Create `docs/tasks/M26_memory_persona_implementation/T370_m26_scope.md` for a
conservative implementation-foundation milestone. M26 should start with
synthetic fixtures, tests, and local models/services only. It should still
forbid private data, provider calls, outbound messaging, voice/avatar runtime,
media generation, and real-person recreation unless explicitly scoped later.

### 3. Worker Summary And Handoff

Write `docs/worker_summary/T365_worker_summary.md` and append a T365 worker
record to `docs/07_handoff.md`.

Do not mark T365 complete in `docs/04_task_board.md`.

## Verification

Minimum command:

```powershell
git diff --check
```

## Reviewer Type

Adversarial memory-architecture, privacy, persona-safety, distillation-safety,
dependency-risk, and product-safety review recommended.

Reviewer should block if M25 review hides residual risks, implies launch or
legal validation, recommends private data ingestion too early, enables
real-person recreation, weakens consent/deletion gates, allows unreviewed
persona growth, introduces provider/platform/outbound/media behavior, or treats
voice/avatar/proactive behavior as implemented.

