# T454: Source Evidence Persona Proposal Payload

## Task ID

T454

## Goal

Add a deterministic local `source_evidence_persona_proposal` payload to the
text-first web demo adapter.

This task is payload and contract-test only. It must not render UI, read
private data, add source readers, call model providers, create embeddings,
extract traits from real content, write stores, apply persona changes, send
messages, connect platform adapters, or enable media runtime.

## Context

M40 introduced `persona_source_evidence_matrix`, which exposes eligible source
ids, excluded refs, evidence rows, trait hypotheses, quality labels, and
review gate results. T454 should show the next safe step: grouping the already
reviewed synthetic trait hypotheses into persona proposal candidates that can
later be rendered and reviewed.

T454 must preserve a strict distinction:

- M40 evidence matrix: what synthetic evidence appears to support;
- M41 persona proposal: what persona field might be proposed for review;
- future apply executor: actual mutation, still not authorized here.

## Allowed Files

Future T454 worker may create or modify only:

- `src/practical_chat_agent/ui/text_first_web_demo_adapter.py`
- `tests/test_source_evidence_persona_proposal_payload.py`
- `tests/test_text_first_web_demo_local_server.py`
- `docs/contracts/source_evidence_persona_proposal_payload.md`
- `docs/tasks/M41_next_iteration/T455_source_evidence_persona_proposal_ui.md`
- `docs/worker_summary/T454_worker_summary.md`
- `docs/07_handoff.md`

If implementation requires static UI rendering, JavaScript/CSS changes, source
readers, model providers, private data, runtime stores, platform adapters,
outbound messaging, media runtime, automatic apply, package changes, or
task-board edits, Captain must revise this package before assignment.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not ingest, summarize, transform, quote, or commit real private chat
  records.
- Do not call model providers or prompt execution layers.
- Do not add source readers, embeddings, vector search, semantic ranking,
  similarity scoring, fine-tuning, or remote inference.
- Do not modify static HTML/CSS/JS in this task.
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

## Expected Payload

Add `source_evidence_persona_proposal` to `TextFirstWebDemoState`.

Required top-level fields:

- `schema_version: m41.source_evidence_persona_proposal.v1`;
- `proposal_title`;
- `source_evidence_matrix_ref`;
- `proposal_candidates`;
- `risk_labels`;
- `rollback_notes`;
- `review_gate_results`;
- `proposal_outcome_labels`;
- `review_required: true`;
- `apply_policy`;
- `non_execution_flags`.

Required proposal candidate paths:

- `style.tone`;
- `style.pacing`;
- `style.humor`;
- `relationship.boundary_style`;
- `memory.use_preference`;
- `growth.short_term_hint`.

Each proposal candidate must include:

- `proposal_id`;
- `persona_field_path`;
- `proposed_value_summary`;
- `rationale_summary`;
- `source_trait_hypothesis_ids`;
- `supporting_evidence_row_ids`;
- `confidence_band` from `low`, `medium`, or `high`;
- `risk_label_ids`;
- `rollback_note_ids`;
- `review_gate_result_ids`;
- `proposal_status: preview_only`;
- `mutation_allowed: false`;
- `review_required: true`.

`apply_policy` must state:

- `mode: preview_only`;
- `writes_persona_card: false`;
- `writes_persona_version_store: false`;
- `writes_memory_store: false`;
- `writes_review_store: false`;
- `writes_runtime_store: false`;
- `automatic_apply: false`.

Required `non_execution_flags`:

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

## Tests

Use TDD:

1. Add failing payload contract tests.
2. Run focused tests and capture RED output.
3. Implement the adapter payload.
4. Re-run focused tests and capture GREEN output.
5. Run `python -m py_compile`.

Tests must verify:

- served JSON includes the proposal payload;
- proposal candidates cover the required persona field paths;
- proposal candidates cite M40 trait hypotheses and evidence rows;
- risk labels, rollback notes, review gate results, and outcome labels are
  internally referenced;
- no unsafe execution flag is true;
- no private/provider/outbound/media surfaces appear.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'; pytest tests\test_source_evidence_persona_proposal_payload.py tests\test_persona_source_evidence_matrix_payload.py tests\test_text_first_web_demo_local_server.py -q -o cache_dir=artifacts\t454_pytest_cache --basetemp=artifacts\t454_pytest_basetemp
```

```powershell
python -m py_compile src\practical_chat_agent\ui\text_first_web_demo_adapter.py
```

```powershell
git diff --check
```

## Reviewer Type

Payload contract review for source-evidence-to-persona-proposal preview,
internal references, non-extraction guarantees, non-mutation guarantees, and
absence of private/provider/runtime surfaces.
