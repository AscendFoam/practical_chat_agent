# T371: Memory Governance Candidate Models

## Task ID

T371

## Goal

Implement local synthetic memory-governance candidate records and tests for the
M25/M26 memory architecture.

T371 should make contradiction, supersession, deletion cascade, explanation
trace, and persona-growth evidence boundaries executable without adding
private-data ingestion, provider calls, retrieval ranking, runtime dialogue,
automatic sending, platform delivery, voice/avatar runtime, media generation,
or real-person recreation.

## Why Now

M25 defined these records as contract candidates. M26 should implement the
lowest-risk memory-governance layer first so later persona growth and
distillation tasks can reference tested, review-first evidence records.

## Allowed Files

Future T371 worker may create or modify only:

- `src/practical_chat_agent/services/memory_governance.py`
- `tests/test_memory_governance_candidates.py`
- `docs/data_contracts/memory_governance_candidate_contract.md`
- `docs/tasks/M26_memory_persona_implementation/T372_persona_growth_candidate_models.md`
- `docs/worker_summary/T371_worker_summary.md`
- `docs/07_handoff.md`

If T371 needs other source files, fixtures, task-board edits, private data,
Browser runs, model-provider calls, package changes, persistence, routes,
stores, CLIs, platform adapters, outbound messaging, voice/avatar runtime, or
media generation, Captain must revise this package before assignment.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not ingest, summarize, transform, quote, or commit real private chat
  records.
- Do not call model providers.
- Do not add source readers, embeddings, vector search, semantic ranking,
  fine-tuning, LLM extraction, private transcript parsing, or persona synthesis.
- Do not modify `MemoryEventStore` or mutate lifecycle state from governance
  candidates.
- Do not create stores, routes, CLIs, schedulers, queues, webhooks, auth,
  tokens, recipient ids, delivery state, or persistence behavior.
- Do not implement final companion reply generation, proactive candidates,
  automatic outreach, sending, scheduling, notifications, platform delivery,
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

- `docs/product/m26_memory_persona_implementation_scope.md`
- `docs/review/M25_review.md`
- `docs/research/memory_architecture_design.md`
- `docs/data_contracts/memory_architecture_contract.md`
- `docs/research/memory_retrieval_consolidation_refresh.md`
- `docs/data_contracts/memory_retrieval_consolidation_refresh_contract.md`
- `docs/data_contracts/memory_event_v2_contract.md`
- `docs/data_contracts/memory_event_store_v2_contract.md`
- `docs/data_contracts/memory_consolidation_v2_contract.md`
- `src/practical_chat_agent/core/models.py`
- `src/practical_chat_agent/services/memory_event_store.py`
- `src/practical_chat_agent/services/memory_consolidation_v2.py`
- `tests/test_memory_event_schema.py`
- `tests/test_memory_consolidation_v2.py`

## Expected Outputs

### 1. Memory Governance Models

Create `src/practical_chat_agent/services/memory_governance.py` with local
Pydantic models and deterministic helper methods for:

- `MemoryContradictionCandidate`
- `MemorySupersessionCandidate`
- `MemoryDeletionCascadePlan`
- `MemoryExplanationTrace`
- `PersonaGrowthEvidenceBundle`

The models should use safe summaries, ids, redacted refs, review flags, safety
warnings, and candidate lifecycle fields. They must not include raw private
text, transcripts, media paths, provider metadata, platform delivery fields, or
runtime send/schedule fields.

Recommended helper behavior:

- create contradiction candidates from two or more `MemoryEvent` ids;
- create supersession candidates without applying lifecycle updates;
- create deletion cascade plans for deletion or consent withdrawal triggers;
- create explanation traces with include/exclude reasons;
- create persona-growth evidence bundles that preserve truth status and block
  unsafe memory ids.

### 2. Tests

Create `tests/test_memory_governance_candidates.py` with synthetic-only tests
that prove:

- contradiction candidates are review-required and preserve memory ids;
- supersession candidates do not update `MemoryEventStore`;
- deletion cascade plans are review-required and keep `completed=false`;
- withdrawn-consent plans recommend suppression or deletion actions;
- explanation traces expose include/exclude reasons and redacted refs;
- persona-growth evidence bundles use safe summaries only;
- imagined memory cannot be used for factual persona-growth evidence;
- crisis, dependency, clone-risk, or high-sensitivity warnings keep evidence
  blocked or review-only;
- forbidden private/provider/outbound/platform/media field names are absent;
- no model exposes send, schedule, deliver, provider, webhook, token,
  microphone, camera, audio, image, video, or runtime mutation methods.

### 3. Data Contract

Create `docs/data_contracts/memory_governance_candidate_contract.md` describing
the implemented records, invariants, forbidden fields, tests, non-actions, and
residual risks.

### 4. Next Task Package

Create
`docs/tasks/M26_memory_persona_implementation/T372_persona_growth_candidate_models.md`
for persona growth candidate model implementation.

### 5. Worker Summary And Handoff

Write `docs/worker_summary/T371_worker_summary.md` and append a T371 worker
record to `docs/07_handoff.md`.

Do not mark T371 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\services\memory_governance.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_memory_governance_candidates.py tests\test_memory_event_schema.py tests\test_memory_consolidation_v2.py -q
```

```powershell
git diff --check
```

## Reviewer Type

Adversarial memory-architecture, privacy, lifecycle, persona-safety,
dependency-risk, and product-safety review recommended.

Reviewer should block if T371 mutates memory state directly, reads private
data, includes raw transcript fields, weakens imagined/factual separation,
allows persona growth to auto-apply, introduces provider/platform/outbound/media
behavior, or implies that governance candidates are runtime dialogue behavior.
