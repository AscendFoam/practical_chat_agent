# T363: Synthetic Distillation Input Contract

## Task ID

T363

## Goal

Define synthetic-only input and de-identification contracts for future
chat-record style distillation without reading private chat logs or enabling
real-person recreation.

## Why Now

T360 scoped distillation readiness, T361 defined memory architecture gates, and
T362 defined persona growth patch boundaries. The next risk is source data:
before any real chat-record processing can be considered, the project needs a
synthetic input contract for speaker mapping, redaction, third-party
minimization, style feature extraction, consent refs, clone-risk warnings, and
safe transformation into a new fictional persona.

## Allowed Files

Future T363 worker may create or modify only:

- `docs/product/synthetic_distillation_input_policy.md`
- `docs/data_contracts/synthetic_distillation_input_contract.md`
- `docs/tasks/M25_memory_persona_growth/T364_memory_retrieval_consolidation_refresh.md`
- `docs/worker_summary/T363_worker_summary.md`
- `docs/07_handoff.md`

If T363 needs code changes, tests, Browser runs, model-provider calls,
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
- Do not implement real-person recreation, authorized digital twin support,
  private-chat distillation, embeddings, similarity scoring, extraction, or
  persona synthesis.
- Do not enable proactive candidate generation, automatic outreach, sending,
  scheduling, voice, avatar, Live2D, camera, microphone, ASR, TTS, media
  generation, or media capture.
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
- `docs/data_contracts/persona_card_v1_contract.md`
- `docs/data_contracts/persona_compiler_contract.md`
- `docs/data_contracts/consent_center_contract.md`
- `docs/data_contracts/aigc_labeling_contract.md`
- `docs/data_contracts/crisis_dependency_policy_contract.md`

Recommended:

- `docs/reference/和gpt-pro的对话.md`
- `docs/reference/gpt-pro关于后续从M13开始的计划分析.md`
- existing de-identification, source-reference, privacy, and distillation
  contracts discoverable through `rg`, but do not read private directories.

## Expected Outputs

### 1. Synthetic Distillation Input Policy

Create `docs/product/synthetic_distillation_input_policy.md` with:

- product objective and non-goals;
- safe target: de-identified style inspiration into a new fictional persona;
- blocked targets: real-person clone, public figure, ex-partner, family member,
  deceased person, minor, voice/face likeness, hidden impersonation;
- consent requirements;
- speaker mapping and third-party minimization principles;
- redaction and source-ref principles;
- clone-risk and similarity-risk warning principles;
- user-facing disclosure requirements;
- synthetic fixture strategy.

### 2. Synthetic Distillation Input Contract

Create `docs/data_contracts/synthetic_distillation_input_contract.md` with:

- future candidate model names and fields;
- input manifest shape;
- source segment shape using synthetic snippets only;
- speaker mapping shape;
- consent refs;
- redaction refs;
- extracted de-identified feature shape;
- blocked clone-risk result shape;
- forbidden fields and surfaces;
- acceptance criteria for later implementation tasks.

The contract must clearly state that T363 does not implement extraction,
similarity scoring, private data readers, or persona synthesis.

### 3. Next Task Package

Create
`docs/tasks/M25_memory_persona_growth/T364_memory_retrieval_consolidation_refresh.md`
for memory consolidation, retrieval, and explanation contract refresh.

### 4. Worker Summary And Handoff

Write `docs/worker_summary/T363_worker_summary.md` and append a T363 worker
record to `docs/07_handoff.md`.

Do not mark T363 complete in `docs/04_task_board.md`.

## Verification

Minimum command:

```powershell
git diff --check
```

## Reviewer Type

Adversarial privacy, de-identification, real-person likeness, product-safety,
and memory-architecture review recommended.

Reviewer should block if the task permits private chat ingestion, raw private
text, real-person recreation, voice/avatar likeness, weak consent, hidden
impersonation, provider calls, platform delivery, automatic outreach, or
legal/launch/user-study claims.

