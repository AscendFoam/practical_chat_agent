# T450: Persona Source Evidence Review Linkage

## Task ID

T450

## Goal

Expose deterministic `persona_source_evidence_matrix` rows in Review
Workspace.

This task links the already-rendered M40 evidence matrix into review cards
only. It must not read private data, add source readers, call model providers,
create embeddings, extract traits from real content, write stores, apply
persona changes, send messages, connect platform adapters, or enable media
runtime.

## Context

T448 introduced the source evidence matrix payload. T449 rendered the matrix in
the static text-first demo. T450 should make excluded source refs, evidence
rows, trait hypotheses, quality labels, and review gate results reviewable from
Review Workspace while preserving preview-only, non-extracting semantics.

## Allowed Files

Future T450 worker may create or modify only:

- `src/practical_chat_agent/ui/text_first_web_demo_adapter.py`
- `src/practical_chat_agent/ui/static/text_first_web_demo.js`
- `tests/test_persona_source_evidence_review_linkage.py`
- `tests/test_persona_source_evidence_matrix_payload.py`
- `tests/test_text_first_web_demo_local_server.py`
- `tests/test_text_first_web_demo_static.py`
- `tests/test_text_first_web_demo_state_switching.py`
- `docs/contracts/persona_source_evidence_matrix_payload.md`
- `docs/tasks/M40_next_iteration/T451_persona_source_evidence_responsive_hardening.md`
- `docs/worker_summary/T450_worker_summary.md`
- `docs/07_handoff.md`

If implementation requires source readers, model providers, private data,
runtime stores, platform adapters, outbound messaging, media runtime,
automatic apply, package changes, or task-board edits, Captain must revise this
package before assignment.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not ingest, summarize, transform, quote, or commit real private chat
  records.
- Do not call model providers or prompt execution layers.
- Do not add source readers, embeddings, vector search, semantic ranking,
  similarity scoring, fine-tuning, or remote inference.
- Do not add real extraction, source import, upload, raw retention, or
  automatic persona mutation.
- Do not write PersonaCard, PersonaVersionStore, MemoryEventStore, review
  stores, runtime stores, local databases, queues, schedulers, or files outside
  the allowed files.
- Do not add platform adapters, webhooks, auth, tokens, recipient ids, delivery
  state, automatic outreach, or outbound messaging.
- Do not add microphone, camera, ASR, TTS, voice cloning, Live2D, generated
  audio, generated image, generated video, or media capture.
- Do not add payment processing, production pricing claims, legal advice,
  compliance completion, app-store approval, launch approval, clinical claims,
  regulator acceptance, or user-study validation.
- Do not modify `docs/04_task_board.md`.

## Expected Implementation

### 1. Adapter Review Cards

Add `review_workspace.source_evidence_review_cards`.

The count must equal:

- number of `excluded_source_refs`;
- plus number of `evidence_rows`;
- plus number of `trait_hypotheses`;
- plus number of `quality_labels`;
- plus number of `review_gate_results`.

Required card contract:

- `schema_version: review_workspace_persona_source_evidence_card_v1`;
- `source_surface: persona_source_evidence_matrix`;
- `filter_keys` includes `source` and `evidence`;
- `review_required: true`;
- `preview_only: true`;
- `changes_state: false`;
- `mutation_allowed: false`;
- `automatic_apply: false`;
- `sends_messages: false`;
- `runtime_ready: false`.

Required card kinds:

- `persona_source_evidence_exclusion_review`;
- `persona_source_evidence_row_review`;
- `persona_source_trait_hypothesis_review`;
- `persona_source_quality_label_review`;
- `persona_source_review_gate_result_review`.

Review Workspace filter tabs must include or update:

- `{ key: source, label: Source, count: existing source-card count plus evidence-card count }`;
- `{ key: evidence, label: Evidence, count: len(source_evidence_review_cards) }`.

### 2. Static Fallback Linkage

Update the JavaScript fallback state so Review Workspace exposes evidence
cards when static HTML is opened directly.

### 3. Rendered Detail Rows

Review cards should show relevant detail rows for:

- excluded source id, source kind, blocked reason ids, raw retention, and
  mutation state;
- evidence source id, evidence kind, quality label id, supported trait paths,
  uncertainty notes, and gate ids;
- trait path, confidence band, support/conflict evidence ids, apply status,
  uncertainty, and mutation state;
- quality code, severity, and unreviewed-extraction blocking state;
- gate code, status, summary, and extraction blocking state.

## Tests

Use TDD:

1. Add failing review-linkage tests.
2. Run focused tests and capture RED output.
3. Implement adapter and static fallback linkage.
4. Re-run focused tests and capture GREEN output.
5. Run `python -m py_compile` and `node --check`.

## Browser QA

After tests pass, verify the Review Workspace source/evidence filters at the
available viewport:

- `Source` and `Evidence` filter tabs are visible with expected counts;
- source evidence review cards render;
- evidence-card detail rows are visible;
- no forbidden action controls appear;
- no horizontal overflow.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'; pytest tests\test_persona_source_evidence_review_linkage.py tests\test_persona_source_evidence_matrix_payload.py tests\test_text_first_web_demo_local_server.py tests\test_text_first_web_demo_static.py tests\test_text_first_web_demo_state_switching.py -q -o cache_dir=artifacts\t450_pytest_cache --basetemp=artifacts\t450_pytest_basetemp
```

```powershell
python -m py_compile src\practical_chat_agent\ui\text_first_web_demo_adapter.py
```

```powershell
node --check src\practical_chat_agent\ui\static\text_first_web_demo.js
```

```powershell
git diff --check
```

## Reviewer Type

Review Workspace linkage review for evidence-card counts, filter behavior,
detail rows, preview-only semantics, non-extracting guarantees, and absence of
private/provider/runtime surfaces.
