# T374: Memory Retrieval Explanation Integration

## Task ID

T374

## Goal

Implement local deterministic retrieval, consolidation, and explanation
integration tests for the M25/M26 memory system.

T374 should connect existing `MemoryEvent v2`, `MemoryConsolidationService`,
`MemoryRetrievalBundle`, `MemoryViewerItem`, `TextFirstMemoryExplanation`, and
new M26 governance/growth/distillation candidate records through test-covered
helper logic. It must not add private data, model providers, vector search,
runtime dialogue, outbound messaging, platform delivery, voice/avatar runtime,
media generation, or real-person recreation.

## Why Now

T371 through T373 implemented candidate records for memory governance, persona
growth, and synthetic distillation input. T374 should prove the read/selection
boundary: what enters or stays out of retrieval bundles, explanation traces,
and persona-growth/distillation review evidence.

## Allowed Files

Future T374 worker may create or modify only:

- `src/practical_chat_agent/services/memory_retrieval_explanation.py`
- `tests/test_memory_retrieval_explanation_integration.py`
- `docs/data_contracts/memory_retrieval_explanation_integration_contract.md`
- `docs/tasks/M26_memory_persona_implementation/T375_m26_milestone_review.md`
- `docs/worker_summary/T374_worker_summary.md`
- `docs/07_handoff.md`

If T374 needs other source files, fixtures, task-board edits, private data,
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
- Do not modify existing store mutation semantics.
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
- `docs/research/memory_retrieval_consolidation_refresh.md`
- `docs/data_contracts/memory_retrieval_consolidation_refresh_contract.md`
- `docs/data_contracts/memory_event_v2_contract.md`
- `docs/data_contracts/memory_retrieval_bundle_v2_contract.md`
- `docs/data_contracts/memory_viewer_contract.md`
- `docs/data_contracts/text_first_chat_memory_contract.md`
- `docs/data_contracts/memory_governance_candidate_contract.md`
- `docs/data_contracts/persona_growth_candidate_implementation_contract.md`
- `docs/data_contracts/synthetic_distillation_input_implementation_contract.md`
- `src/practical_chat_agent/core/models.py`
- `src/practical_chat_agent/ui/text_first_chat_memory.py`
- `src/practical_chat_agent/services/memory_consolidation_v2.py`
- `src/practical_chat_agent/services/memory_governance.py`
- `src/practical_chat_agent/services/persona_growth.py`
- `src/practical_chat_agent/services/synthetic_distillation_input.py`
- relevant existing memory tests.

## Expected Outputs

### 1. Retrieval Explanation Helper

Create `src/practical_chat_agent/services/memory_retrieval_explanation.py` with
local deterministic helper logic that can:

- select eligible `MemoryEvent` records for a requested purpose;
- produce `MemoryRetrievalBundle` records with selected and excluded ids;
- produce `MemoryExplanationTrace` records for include/exclude decisions;
- create contradiction/supersession/deletion cascade candidates when supplied
  synthetic triggers require them;
- prepare persona-growth evidence bundles only from eligible memory;
- keep synthetic distillation feature candidates review-only.

### 2. Tests

Create `tests/test_memory_retrieval_explanation_integration.py` with
synthetic-only tests that prove:

- imagined memory cannot enter factual response bundles;
- deleted, frozen, archived, and superseded current-fact memory is excluded;
- review-required memory is excluded outside review surfaces;
- withdrawn-consent memory is excluded or creates a deletion cascade plan;
- contradiction creates a candidate and does not overwrite memory;
- supersession creates a candidate and does not mutate lifecycle directly;
- persona-growth evidence does not mutate PersonaCard;
- synthetic distillation features remain review-only;
- include/exclude reasons are exposed through explanation traces;
- forbidden private/provider/outbound/platform/media fields are absent.

### 3. Data Contract

Create
`docs/data_contracts/memory_retrieval_explanation_integration_contract.md`
describing implemented helper behavior, invariants, tests, forbidden fields,
non-actions, and residual risks.

### 4. Next Task Package

Create `docs/tasks/M26_memory_persona_implementation/T375_m26_milestone_review.md`
for M26 milestone review.

### 5. Worker Summary And Handoff

Write `docs/worker_summary/T374_worker_summary.md` and append a T374 worker
record to `docs/07_handoff.md`.

Do not mark T374 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\services\memory_retrieval_explanation.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_memory_retrieval_explanation_integration.py tests\test_memory_governance_candidates.py tests\test_persona_growth_candidates.py tests\test_synthetic_distillation_input_candidates.py tests\test_memory_retrieval_bundle_schema.py tests\test_text_first_chat_memory_prototype.py -q
```

```powershell
git diff --check
```

Use project-local pytest cache and basetemp paths if the default user temp
directory is not writable.

## Reviewer Type

Adversarial memory-architecture, lifecycle, retrieval-safety, privacy,
persona-safety, distillation-safety, and product-safety review recommended.

Reviewer should block if T374 lets imagined memory enter factual bundles,
retrieves deleted/frozen/archived/review-required memory incorrectly, mutates
stores through explanation helpers, allows persona growth to auto-apply,
enables runtime distillation/synthesis, or introduces provider/platform/outbound
or voice/avatar/media behavior.
