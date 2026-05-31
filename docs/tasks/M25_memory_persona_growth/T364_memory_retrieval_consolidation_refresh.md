# T364: Memory Retrieval Consolidation Refresh

## Task ID

T364

## Goal

Refresh the memory consolidation, retrieval, and explanation contracts against
the M25 memory architecture, persona growth policy, and synthetic distillation
input boundaries.

## Why Now

T361 defined the memory architecture. T362 defined persona growth patches. T363
defined synthetic distillation input boundaries. Before M25 review, the project
needs a focused refresh that ties existing memory consolidation and retrieval
contracts to the new architecture, especially contradiction handling,
withdrawal, imagined/factual separation, persona-growth evidence, and
de-identified distillation readiness.

## Allowed Files

Future T364 worker may create or modify only:

- `docs/research/memory_retrieval_consolidation_refresh.md`
- `docs/data_contracts/memory_retrieval_consolidation_refresh_contract.md`
- `docs/tasks/M25_memory_persona_growth/T365_m25_milestone_review.md`
- `docs/worker_summary/T364_worker_summary.md`
- `docs/07_handoff.md`

If T364 needs code changes, tests, Browser runs, model-provider calls,
generated media, private data processing, persistence, task-board edits,
platform adapters, outbound messaging, voice/avatar runtime, or screenshot
artifacts, Captain must revise this package before assignment.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not ingest, summarize, transform, or quote real private chat records.
- Do not call model providers.
- Do not add or modify Python source code or tests unless Captain revises this
  package.
- Do not implement retrieval ranking, vector search, embeddings, extraction,
  persona growth patch application, distillation, or dialogue runtime use.
- Do not create stores, routes, CLIs, schedulers, send paths, queues, webhooks,
  platform adapters, auth, tokens, or persistence behavior.
- Do not enable proactive candidate generation, automatic outreach, sending,
  scheduling, voice, avatar, Live2D, camera, microphone, ASR, TTS, media
  generation, or media capture.
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
- `docs/data_contracts/memory_event_v2_contract.md`
- `docs/data_contracts/memory_lifecycle_v2_contract.md`
- `docs/data_contracts/memory_consolidation_v2_contract.md`
- `docs/data_contracts/memory_retrieval_bundle_v2_contract.md`
- `docs/data_contracts/memory_viewer_contract.md`
- `docs/data_contracts/text_first_chat_memory_contract.md`
- `docs/data_contracts/consent_center_contract.md`
- `docs/data_contracts/crisis_dependency_policy_contract.md`

## Expected Outputs

### 1. Refresh Research Note

Create `docs/research/memory_retrieval_consolidation_refresh.md` with:

- architecture alignment summary;
- consolidation refresh requirements;
- retrieval refresh requirements;
- explanation surface requirements;
- contradiction and supersession handling;
- consent withdrawal and deletion cascade requirements;
- persona-growth evidence boundary;
- distillation-readiness boundary;
- synthetic fixture recommendations;
- residual risks.

### 2. Refresh Contract

Create
`docs/data_contracts/memory_retrieval_consolidation_refresh_contract.md` with:

- future candidate record names where needed;
- requirements for consolidation candidates;
- requirements for retrieval bundles;
- requirements for viewer/chat explanation surfaces;
- forbidden fields and surfaces;
- acceptance criteria for later code/test tasks.

### 3. Next Task Package

Create `docs/tasks/M25_memory_persona_growth/T365_m25_milestone_review.md` for
M25 milestone review.

### 4. Worker Summary And Handoff

Write `docs/worker_summary/T364_worker_summary.md` and append a T364 worker
record to `docs/07_handoff.md`.

Do not mark T364 complete in `docs/04_task_board.md`.

## Verification

Minimum command:

```powershell
git diff --check
```

## Reviewer Type

Adversarial memory-architecture, privacy, persona-safety, distillation-safety,
and product-safety review recommended.

Reviewer should block if the refresh weakens factual/imagined separation,
permits private data ingestion, stores raw private text, enables real-person
recreation, bypasses consent withdrawal, allows persona growth mutation without
review, introduces provider/platform/outbound/media behavior, or claims
legal/clinical/launch validation.

