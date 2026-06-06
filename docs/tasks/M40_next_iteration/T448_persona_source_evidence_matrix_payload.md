# T448: Persona Source Evidence Matrix Payload

## Task ID

T448

## Goal

Add a deterministic local `persona_source_evidence_matrix` payload to the
text-first web demo state and cover it with contract tests.

This task is payload-only. It must not render UI, call model providers, read
private data, add source readers, create embeddings, extract traits from real
content, write stores, mutate personas, send messages, connect platform
adapters, or enable media runtime.

## Context

M39 introduced `persona_source_intake_manifest`: source candidates, consent,
ownership, minimization, redaction profiles, extraction eligibility, blocked
categories, policy gates, static rendering, Review Workspace linkage, and
responsive hardening.

M40 should connect that intake manifest to a deterministic evidence matrix
without reading any real source. T448 should prove the payload contract before
static matrix UI or Review Workspace evidence cards are added.

The payload should show how future persona distillation can reason about
eligible sources, excluded sources, evidence quality, trait hypotheses, and
review gates while remaining local, deterministic, synthetic-only,
review-only, and non-extracting.

## Allowed Files

Future T448 worker may create or modify only:

- `src/practical_chat_agent/ui/text_first_web_demo_adapter.py`
- `tests/test_persona_source_evidence_matrix_payload.py`
- `tests/test_persona_source_intake_manifest_payload.py`
- `tests/test_text_first_web_demo_local_server.py`
- `docs/contracts/persona_source_evidence_matrix_payload.md`
- `docs/tasks/M40_next_iteration/T449_persona_source_evidence_matrix_ui.md`
- `docs/worker_summary/T448_worker_summary.md`
- `docs/07_handoff.md`

If implementation requires static UI rendering, JavaScript/CSS edits, package
changes, private data, source readers, model providers, runtime stores,
platform adapters, outbound messaging, media runtime, automatic apply, or
task-board edits, Captain must revise this package before assignment.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not ingest, summarize, transform, quote, or commit real private chat
  records.
- Do not call model providers or prompt execution layers.
- Do not add source readers, embeddings, vector search, semantic ranking,
  similarity scoring, fine-tuning, or remote inference.
- Do not modify JavaScript, CSS, HTML, or Browser QA surfaces in this task.
- Do not write PersonaCard, PersonaVersionStore, MemoryEventStore, review
  stores, runtime stores, local databases, queues, schedulers, or files outside
  the allowed docs/test/code files.
- Do not add platform adapters, webhooks, auth, tokens, recipient ids, delivery
  state, automatic outreach, or outbound messaging.
- Do not add microphone, camera, ASR, TTS, voice cloning, Live2D, generated
  audio, generated image, generated video, or media capture.
- Do not add payment processing, production pricing claims, legal advice,
  compliance completion, app-store approval, launch approval, clinical claims,
  regulator acceptance, or user-study validation.
- Do not modify `docs/04_task_board.md`.

## Expected Implementation

### 1. Adapter Payload

Update `TextFirstWebDemoState` so serialized demo state contains
`persona_source_evidence_matrix`.

The payload must include:

- `schema_version`, for example `m40.persona_source_evidence_matrix.v1`;
- `matrix_title`;
- `source_intake_manifest_ref`;
- `eligible_source_ids`;
- `excluded_source_refs`;
- `evidence_rows`;
- `trait_hypotheses`;
- `quality_labels`;
- `review_gate_results`;
- `review_required: true`;
- `apply_policy`;
- `non_execution_flags`.

### 2. Source Intake Linkage

The matrix must reference the synthetic M39 intake manifest:

- `source_intake_manifest_ref.schema_version` should point to
  `m39.persona_source_intake_manifest.v1`;
- `eligible_source_ids` must match M39 candidates with
  `extraction_eligible: true`;
- `excluded_source_refs` must cite ineligible M39 candidates and their blocked
  reason ids;
- evidence row `source_id` values must be eligible source ids only;
- trait hypotheses must cite evidence row ids, not raw source content.

### 3. Evidence Rows

Add deterministic evidence rows for eligible sources:

- detailed description evidence;
- fuzzy seed evidence;
- synthetic dialogue evidence.

Each evidence row must include:

- stable `evidence_row_id`;
- `source_id`;
- `source_kind`;
- `evidence_kind`;
- `safe_summary`;
- `quality_label_id`;
- `supports_trait_paths`;
- `uncertainty_notes`;
- `review_gate_result_ids`;
- `raw_content_retained: false`;
- `review_required: true`.

### 4. Excluded Source Refs

Add exclusion refs for every ineligible source candidate.

Each exclusion ref must include:

- `source_id`;
- `source_kind`;
- `blocked_reason_ids`;
- `safe_summary`;
- `excluded_from_evidence: true`;
- `raw_content_retained: false`;
- `mutation_allowed: false`.

### 5. Trait Hypotheses

Add at least six deterministic trait hypotheses covering:

- `style.tone`;
- `style.pacing`;
- `style.humor`;
- `relationship.boundary_style`;
- `memory.use_preference`;
- `growth.short_term_hint`.

Each trait hypothesis must include:

- stable `trait_hypothesis_id`;
- `trait_path`;
- `hypothesis_summary`;
- `supporting_evidence_row_ids`;
- `conflicting_evidence_row_ids`;
- `confidence_band` from `low`, `medium`, or `high`;
- `uncertainty_summary`;
- `review_gate_result_ids`;
- `apply_status: preview_only`;
- `mutation_allowed: false`.

### 6. Quality Labels

Quality labels must cover:

- `strong_synthetic_description`;
- `fuzzy_seed`;
- `synthetic_dialogue_fixture`;
- `blocked_archive_placeholder`;
- `blocked_third_party_private_source`.

Each label must include:

- `quality_label_id`;
- `quality_code`;
- severity from `low`, `medium`, or `high`;
- `safe_summary`;
- `blocks_unreviewed_extraction`.

### 7. Review Gate Results

Gate results must cover:

- consent;
- minimization;
- redaction;
- uncertainty;
- anti-deception.

Each gate result must include:

- `review_gate_result_id`;
- `gate_code`;
- `status` from `passed`, `needs_review`, or `blocked`;
- `safe_summary`;
- `blocks_extraction_when_failed: true`.

### 8. Non-Execution Flags

Required flags:

- `local_only: true`;
- `synthetic_fixture: true`;
- `uses_model_provider: false`;
- `reads_private_sources: false`;
- `retains_raw_source_content: false`;
- `creates_embeddings: false`;
- `performs_extraction: false`;
- `writes_persona_store: false`;
- `writes_persona_version_store: false`;
- `writes_memory_store: false`;
- `writes_review_store: false`;
- `writes_runtime_store: false`;
- `automatic_apply: false`;
- `sends_messages: false`;
- `uses_platform_adapter: false`;
- `uses_media_runtime: false`.

Tests must fail if a risky execution flag is missing or set to an unsafe state.

## Tests

Use TDD:

1. Add failing tests in `tests/test_persona_source_evidence_matrix_payload.py`.
2. Run focused tests and capture RED output in the worker summary.
3. Implement the payload.
4. Re-run focused tests and capture GREEN output.
5. Run a small integration set that includes
   `tests/test_text_first_web_demo_local_server.py`.

The tests should verify:

- payload key exists in serialized demo state;
- schema version and review/apply policies are correct;
- source linkage to `persona_source_intake_manifest`;
- eligible and excluded source ids match the manifest;
- evidence rows use only eligible source ids;
- excluded source refs cover every ineligible source candidate;
- trait hypotheses cover required paths and cite evidence row ids;
- quality labels and review gate results cover required codes;
- raw content is never retained;
- non-execution flags are safe;
- recursive payload scan finds no unsafe true states for provider calls,
  private-source reads, raw source retention, embeddings, extraction, store
  writes, automatic apply, outbound messaging, platform adapters, or media
  runtime;
- `/demo-state.json` includes the matrix.

## Expected Outputs

- Payload added to the adapter.
- Contract doc added at
  `docs/contracts/persona_source_evidence_matrix_payload.md`.
- T449 task package created for static UI rendering.
- Worker summary created at
  `docs/worker_summary/T448_worker_summary.md`.
- Handoff record appended to `docs/07_handoff.md`.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'; pytest tests\test_persona_source_evidence_matrix_payload.py tests\test_persona_source_intake_manifest_payload.py tests\test_text_first_web_demo_local_server.py -q -o cache_dir=artifacts\t448_pytest_cache --basetemp=artifacts\t448_pytest_basetemp
```

```powershell
python -m py_compile src\practical_chat_agent\ui\text_first_web_demo_adapter.py
```

```powershell
git diff --check
```

## Reviewer Type

Payload contract review for source intake linkage, eligible source handling,
excluded source handling, evidence row consistency, trait hypothesis coverage,
quality/review gate coverage, non-execution flags, and no private or provider
surfaces.
