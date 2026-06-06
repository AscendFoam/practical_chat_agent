# T460: Source Proposal Persona Draft Payload

## Task ID

T460

## Goal

Add a deterministic local `source_proposal_persona_draft` payload to the
text-first web demo adapter.

This task is payload and contract-test only. It must not render UI, read
private data, add source readers, call model providers, create embeddings,
extract traits from real content, write stores, apply persona changes, send
messages, connect platform adapters, or enable media runtime.

## Context

M41 introduced `source_evidence_persona_proposal`, which exposes proposal
candidates derived from M40 source evidence matrix summaries. T460 should show
the next safe step: grouping already reviewable proposal candidates into an
inspectable PersonaCard draft preview without mutating PersonaCard or runtime
state.

T460 must preserve a strict distinction:

- M41 persona proposal: what persona field might be proposed for review;
- M42 persona draft: what an inspectable draft snapshot could look like;
- future apply executor: actual mutation, still not authorized here.

## Allowed Files

Future T460 worker may create or modify only:

- `src/practical_chat_agent/ui/text_first_web_demo_adapter.py`
- `tests/test_source_proposal_persona_draft_payload.py`
- `tests/test_text_first_web_demo_local_server.py`
- `docs/contracts/source_proposal_persona_draft_payload.md`
- `docs/tasks/M42_next_iteration/T461_source_proposal_persona_draft_ui.md`
- `docs/worker_summary/T460_worker_summary.md`
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

Add `source_proposal_persona_draft` to `TextFirstWebDemoState`.

Required top-level fields:

- `schema_version: m42.source_proposal_persona_draft.v1`;
- `draft_title`;
- `source_proposal_ref`;
- `base_persona_snapshot`;
- `selected_proposal_ids`;
- `draft_field_changes`;
- `unchanged_field_summaries`;
- `conflict_notes`;
- `rollback_refs`;
- `review_gate_results`;
- `draft_outcome_labels`;
- `review_required: true`;
- `apply_policy`;
- `non_execution_flags`.

Required draft field paths:

- `style.tone`;
- `style.pacing`;
- `style.humor`;
- `relationship.boundary_style`;
- `memory.use_preference`;
- `growth.short_term_hint`.

Each draft field change must include:

- `draft_change_id`;
- `persona_field_path`;
- `before_summary`;
- `after_summary`;
- `source_proposal_ids`;
- `source_trait_hypothesis_ids`;
- `supporting_evidence_row_ids`;
- confidence band from `low`, `medium`, or `high`;
- `risk_label_ids`;
- `rollback_ref_ids`;
- `review_gate_result_ids`;
- `draft_status: preview_only`;
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

- served JSON includes the draft payload;
- draft field changes cover the required persona field paths;
- draft changes cite M41 proposal candidates and M40 evidence refs already
  carried by proposals;
- conflict notes, rollback refs, review gates, and outcome labels are
  internally referenced;
- no unsafe execution flag is true;
- no private/provider/outbound/media surfaces appear.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'; pytest tests\test_source_proposal_persona_draft_payload.py tests\test_source_evidence_persona_proposal_payload.py tests\test_text_first_web_demo_local_server.py -q -o cache_dir=artifacts\t460_pytest_cache --basetemp=artifacts\t460_pytest_basetemp
```

```powershell
python -m py_compile src\practical_chat_agent\ui\text_first_web_demo_adapter.py
```

```powershell
git diff --check
```

## Reviewer Type

Payload contract review for proposal-to-persona-draft preview, internal
references, non-extraction guarantees, non-mutation guarantees, and absence of
private/provider/runtime surfaces.
