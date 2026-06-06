# T466: Source Draft Apply Readiness Payload

## Task ID

T466

## Goal

Add a deterministic local `source_draft_apply_readiness` payload to the
text-first web demo state.

This task is payload and contract tests only. It must not add static UI
rendering, JavaScript/CSS edits, source readers, private data access, model
providers, embeddings, real extraction, store writes, persona apply, outbound
messaging, platform adapters, or media runtime.

## Context

M42 introduced a proposal-linked persona draft. M43 should evaluate that draft
for future apply-readiness while preserving the preview-only boundary.

T466 should not implement an apply executor. It should only expose reviewable
records explaining why draft fields are blocked, need manual review, or can
inform a later separately scoped apply design.

## Allowed Files

Future T466 worker may create or modify only:

- `src/practical_chat_agent/ui/text_first_web_demo_adapter.py`
- `tests/test_source_draft_apply_readiness_payload.py`
- `tests/test_source_proposal_persona_draft_payload.py`
- `tests/test_text_first_web_demo_local_server.py`
- `docs/contracts/source_draft_apply_readiness_payload.md`
- `docs/tasks/M43_next_iteration/T467_source_draft_apply_readiness_ui.md`
- `docs/worker_summary/T466_worker_summary.md`
- `docs/07_handoff.md`

If implementation requires static UI rendering, JavaScript/CSS edits, source
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
- Do not write PersonaCard, PersonaVersionStore, MemoryEventStore, review
  stores, runtime stores, local databases, queues, schedulers, or files outside
  the allowed adapter/test/docs files.
- Do not add platform adapters, webhooks, auth, tokens, recipient ids, delivery
  state, automatic outreach, or outbound messaging.
- Do not add microphone, camera, ASR, TTS, voice cloning, Live2D, generated
  audio, generated image, generated video, or media capture.
- Do not add payment processing, production pricing claims, legal advice,
  compliance completion, app-store approval, launch approval, clinical claims,
  regulator acceptance, or user-study validation.
- Do not modify `docs/04_task_board.md`.

## Expected Payload

Add `source_draft_apply_readiness` to `TextFirstWebDemoState` and
`/demo-state.json`.

Required top-level fields:

- `schema_version: m43.source_draft_apply_readiness.v1`;
- `readiness_title`;
- `source_draft_ref`;
- `evaluated_draft_change_ids`;
- `field_readiness_records`;
- `blocked_condition_records`;
- `required_review_gate_refs`;
- `rollback_dependency_refs`;
- `readiness_outcome_labels`;
- `review_required: true`;
- `apply_policy`;
- `non_execution_flags`.

`source_draft_ref.schema_version` must point to
`m42.source_proposal_persona_draft.v1`.

Required field paths:

- `style.tone`;
- `style.pacing`;
- `style.humor`;
- `relationship.boundary_style`;
- `memory.use_preference`;
- `growth.short_term_hint`.

Each field readiness record should include:

- `readiness_record_id`;
- `draft_change_id`;
- `persona_field_path`;
- `readiness_outcome` from `blocked`, `needs_manual_review`, or
  `ready_for_future_apply_design`;
- `safe_summary`;
- `blocking_condition_ids`;
- `required_review_gate_result_ids`;
- `rollback_ref_ids`;
- `future_apply_design_notes`;
- `preview_only: true`;
- `mutation_allowed: false`;
- `review_required: true`.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'; pytest tests\test_source_draft_apply_readiness_payload.py tests\test_source_proposal_persona_draft_payload.py tests\test_text_first_web_demo_local_server.py -q -o cache_dir=artifacts\t466_pytest_cache --basetemp=artifacts\t466_pytest_basetemp
```

```powershell
python -m py_compile src\practical_chat_agent\ui\text_first_web_demo_adapter.py
```

```powershell
git diff --check
```

## Reviewer Type

Payload contract review for deterministic apply-readiness preview, M42 draft
linkage, safe outcomes, non-execution flags, and absence of mutation or
outbound behavior.
