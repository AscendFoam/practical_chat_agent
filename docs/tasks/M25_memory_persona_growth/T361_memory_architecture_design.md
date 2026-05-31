# T361: Memory Architecture Design

## Task ID

T361

## Goal

Design the M25 memory architecture for long-term companion memory, persona
growth support, and future distillation readiness while staying contract-only,
synthetic, local, and review-first.

## Why Now

T360 scoped M25 around memory, persona growth, and distillation planning. Before
adding code or new runtime behavior, the project needs a clear architecture for
how memory is written, managed, retrieved, explained, forgotten, and separated
from persona growth and imagined virtual-life continuity.

## Allowed Files

Future T361 worker may create or modify only:

- `docs/research/memory_architecture_design.md`
- `docs/data_contracts/memory_architecture_contract.md`
- `docs/tasks/M25_memory_persona_growth/T362_persona_growth_policy.md`
- `docs/worker_summary/T361_worker_summary.md`
- `docs/07_handoff.md`

If T361 needs code changes, tests, Browser runs, model-provider calls,
generated media, private data processing, persistence, task-board edits,
platform adapters, outbound messaging, voice/avatar runtime, or screenshot
artifacts, Captain must revise this package before assignment.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not ingest, summarize, transform, or quote real private chat records.
- Do not call model providers.
- Do not add or modify Python source code or tests.
- Do not add package-manager dependencies.
- Do not create stores, routes, CLIs, services, schedulers, send paths,
  queues, webhooks, platform adapters, auth, tokens, or persistence behavior.
- Do not implement memory extraction, retrieval ranking, vector search,
  embeddings, model prompts, or dialogue runtime use.
- Do not enable automatic outreach, proactive candidate generation, voice,
  avatar, Live2D, camera, microphone, ASR, TTS, media generation, or media
  capture.
- Do not implement real-person recreation, private-chat distillation, or
  authorized digital twin support.
- Do not modify `docs/04_task_board.md`.
- Do not claim legal advice, compliance completion, app-store approval, launch
  approval, user-study validation, regulator acceptance, or real user evidence.

## Inputs To Read

Required:

- `docs/product/m25_memory_persona_growth_scope.md`
- `docs/data_contracts/memory_event_v2_contract.md`
- `docs/data_contracts/memory_event_store_v2_contract.md`
- `docs/data_contracts/memory_lifecycle_v2_contract.md`
- `docs/data_contracts/memory_consolidation_v2_contract.md`
- `docs/data_contracts/memory_retrieval_bundle_v2_contract.md`
- `docs/data_contracts/memory_viewer_contract.md`
- `docs/data_contracts/text_first_chat_memory_contract.md`
- `docs/data_contracts/consent_center_contract.md`
- `docs/data_contracts/aigc_labeling_contract.md`
- `docs/data_contracts/crisis_dependency_policy_contract.md`
- `docs/data_contracts/persona_card_v1_contract.md`
- `docs/data_contracts/relationship_context_bundle_contract.md`

Recommended:

- `docs/reference/和gpt-pro的对话.md`
- `docs/reference/gpt-pro关于后续从M13开始的计划分析.md`
- current memory/persona model declarations discoverable with `rg` in
  `src/practical_chat_agent/core/models.py`, but do not modify source code.

## Expected Outputs

### 1. Memory Architecture Design

Create `docs/research/memory_architecture_design.md` with:

- product objective and architecture assumptions;
- layered memory model covering working, episodic, semantic/profile,
  procedural, relational, persona self-memory, imagined continuity, and audit
  memory;
- write path from synthetic event candidate to reviewed memory event;
- manage path for consolidation, contradiction, decay, compression, freeze,
  archive, deletion, and consent withdrawal;
- read path for retrieval eligibility, bundle packaging, explanation, and
  exclusion;
- provenance, confidence, sensitivity, salience, lifecycle, and retrieval
  permission requirements;
- distinction between factual, inferred, relational, procedural, and imagined
  memory;
- memory poisoning and untrusted-source quarantine boundaries;
- how memory supports persona growth without silently mutating PersonaCard;
- how memory prepares for future de-identified distillation without reading
  private data now;
- residual risks and future task recommendations.

### 2. Memory Architecture Contract

Create `docs/data_contracts/memory_architecture_contract.md` with:

- canonical architecture layer names;
- required record families and their responsibilities;
- lifecycle and consent gates;
- retrieval and explanation invariants;
- forbidden fields and surfaces;
- synthetic fixture requirements;
- acceptance criteria for later implementation tasks.

This contract should reference existing models instead of redefining them when
possible. It may propose future model names, but must mark them as future
contract candidates rather than implemented code.

### 3. Next Task Package

Create
`docs/tasks/M25_memory_persona_growth/T362_persona_growth_policy.md` for the
persona growth policy and patch contract task. T362 should remain docs/contract
focused unless the new task explicitly allows code and tests.

### 4. Worker Summary And Handoff

Write `docs/worker_summary/T361_worker_summary.md` and append a T361 worker
record to `docs/07_handoff.md`.

Do not mark T361 complete in `docs/04_task_board.md`.

## Verification

Minimum command:

```powershell
git diff --check
```

## Reviewer Type

Adversarial memory-architecture, privacy, product-safety, and persona-safety
review recommended.

Reviewer should block if the architecture collapses imagined memory into
factual memory, stores raw private text, permits private data ingestion,
enables real-person recreation, allows unbounded persona drift, enables
automatic outreach, introduces provider calls or platform delivery, weakens
consent withdrawal, or treats documentation as legal/clinical/launch
validation.

