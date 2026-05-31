# T362: Persona Growth Policy

## Task ID

T362

## Goal

Define the M25 persona growth policy and patch contract so companion personas
can change over time in a bounded, explainable, reviewable, and reversible way.

## Why Now

T361 defines how memory can supply evidence for growth without silently mutating
PersonaCard. The next task should specify what a persona growth patch is, which
fields may change, which fields are frozen, how review works, and how safety
rules prevent dependency, clone drift, or manipulative optimization.

## Allowed Files

Future T362 worker may create or modify only:

- `docs/product/persona_growth_policy.md`
- `docs/data_contracts/persona_growth_patch_contract.md`
- `docs/tasks/M25_memory_persona_growth/T363_synthetic_distillation_input_contract.md`
- `docs/worker_summary/T362_worker_summary.md`
- `docs/07_handoff.md`

If T362 needs code changes, tests, Browser runs, model-provider calls,
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
- Do not implement runtime persona mutation or final companion reply
  generation.
- Do not enable proactive candidate generation, automatic outreach, sending,
  scheduling, voice, avatar, Live2D, camera, microphone, ASR, TTS, media
  generation, or media capture.
- Do not implement real-person recreation, private-chat distillation, voice
  clone, face clone, public-figure clone, ex-partner clone, family-member
  clone, deceased-person resurrection, or authorized digital twin support.
- Do not modify `docs/04_task_board.md`.
- Do not claim legal advice, compliance completion, app-store approval, launch
  approval, user-study validation, regulator acceptance, or real user evidence.

## Inputs To Read

Required:

- `docs/product/m25_memory_persona_growth_scope.md`
- `docs/research/memory_architecture_design.md`
- `docs/data_contracts/memory_architecture_contract.md`
- `docs/data_contracts/persona_card_v1_contract.md`
- `docs/data_contracts/persona_compiler_contract.md`
- `docs/data_contracts/persona_review_card_contract.md`
- `docs/data_contracts/persona_version_store_contract.md`
- `docs/data_contracts/persona_version_editor_contract.md`
- `docs/data_contracts/relationship_state_contract.md`
- `docs/data_contracts/relationship_context_bundle_contract.md`
- `docs/data_contracts/consent_center_contract.md`
- `docs/data_contracts/crisis_dependency_policy_contract.md`
- `docs/data_contracts/aigc_labeling_contract.md`

Recommended:

- `docs/reference/和gpt-pro的对话.md`
- `docs/reference/gpt-pro关于后续从M13开始的计划分析.md`
- current PersonaCard and PersonaGrowthPolicy declarations discoverable with
  `rg` in `src/practical_chat_agent/core/models.py`, but do not modify source
  code.

## Expected Outputs

### 1. Persona Growth Policy

Create `docs/product/persona_growth_policy.md` with:

- product objective and non-goals;
- stable core persona fields that cannot drift;
- mutable persona fields that can change under review;
- short-term mood versus long-term trait distinction;
- relationship-state versus persona-state distinction;
- growth triggers from memory, user correction, explicit preference, and
  review notes;
- max-delta and rate-limit policy;
- user-facing explanation requirements;
- rollback/freeze/delete behavior;
- safety boundaries for dependency, crisis, jealousy, exclusivity, isolation,
  paid intimacy escalation, real-person similarity, grief, ex-partner,
  family-member, public figure, minors, and voice/avatar likeness;
- synthetic fixture strategy.

### 2. Persona Growth Patch Contract

Create `docs/data_contracts/persona_growth_patch_contract.md` with:

- future candidate model names and fields;
- patch lifecycle states;
- allowed and frozen field sets;
- evidence and memory-reference requirements;
- safety warning fields;
- review decision requirements;
- version-store interaction requirements;
- forbidden fields and surfaces;
- acceptance criteria for later implementation tasks.

The contract should reference existing PersonaCard, PersonaGrowthPolicy,
PersonaReviewService, and PersonaVersionStore behavior instead of claiming new
code exists.

### 3. Next Task Package

Create
`docs/tasks/M25_memory_persona_growth/T363_synthetic_distillation_input_contract.md`
for synthetic distillation input and de-identification planning. T363 should
remain synthetic and docs/contract focused.

### 4. Worker Summary And Handoff

Write `docs/worker_summary/T362_worker_summary.md` and append a T362 worker
record to `docs/07_handoff.md`.

Do not mark T362 complete in `docs/04_task_board.md`.

## Verification

Minimum command:

```powershell
git diff --check
```

## Reviewer Type

Adversarial persona-safety, memory-architecture, privacy, product-safety, and
dependency-risk review recommended.

Reviewer should block if persona growth can mutate frozen identity/source/safety
fields, bypass review, optimize for engagement or dependency, drift toward a
real person, enable proactive sending, enable voice/avatar likeness, read
private data, call providers, or claim legal/clinical/launch validation.

