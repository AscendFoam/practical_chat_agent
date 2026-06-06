# T430: Persona Evolution Preview Payload

## Task ID

T430

## Goal

Add a deterministic local `persona_evolution_preview` payload to the text-first
web demo state and cover it with contract tests.

This task is payload-only. It must not render UI, call model providers, read
private data, write stores, apply persona changes, send messages, connect
platform adapters, or enable media runtime.

## Context

M36 introduced the local persona distillation workbench. T429 refined M37 into
a controlled persona evolution preview milestone. The first implementation
slice should prove the payload contract before any static UI or review-linkage
surfaces are added.

The payload should show how reviewed workbench trait candidates become
preview-only persona patch proposals with before/after summaries, risk labels,
and rollback notes.

## Allowed Files

Future T430 worker may create or modify only:

- `src/practical_chat_agent/ui/text_first_web_demo_adapter.py`
- `tests/test_persona_evolution_preview_payload.py`
- `tests/test_persona_distillation_workbench_payload.py`
- `tests/test_text_first_web_demo_local_server.py`
- `docs/contracts/persona_evolution_preview_payload.md`
- `docs/tasks/M37_next_iteration/T431_persona_evolution_preview_ui.md`
- `docs/worker_summary/T430_worker_summary.md`
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
`persona_evolution_preview`.

The payload must include:

- `schema_version`, for example `m37.persona_evolution_preview.v1`;
- `preview_title`;
- `source_workbench_ref`;
- `source_trait_candidate_ids`;
- `persona_snapshot_before`;
- `proposed_patch_candidates`;
- `blocked_source_exclusions`;
- `risk_labels`;
- `rollback_notes`;
- `review_required: true`;
- `apply_policy` set to preview-only and non-mutating;
- `non_execution_flags`.

### 2. Source Workbench Linkage

The payload must reference the synthetic M36 workbench:

- `source_workbench_ref` should point to
  `m36.persona_distillation_workbench.v1`;
- `source_trait_candidate_ids` must match existing M36 trait candidate ids;
- proposed patches must use only source trait candidate ids;
- blocked request ids must appear only in `blocked_source_exclusions`.

### 3. Persona Snapshot Before

`persona_snapshot_before` must include:

- `persona_id`;
- `display_name`;
- `ai_identity_disclosure`;
- `current_trait_summaries`;
- `current_boundary_summary`;
- `current_memory_use_summary`;
- `source_label: synthetic_fixture`;
- `real_person_claim: false`;
- `runtime_state_ref: none`.

### 4. Patch Candidates

Add at least six `proposed_patch_candidates` entries covering:

- `style.tone`;
- `style.pacing`;
- `style.humor`;
- `relationship.boundary_style`;
- `memory.use_preference`;
- `growth.short_term_hint`.

Each patch must include:

- `patch_id`;
- `patch_kind`;
- non-empty `source_trait_candidate_ids`;
- `changed_field_path`;
- `before_summary`;
- `after_summary`;
- `rationale_summary`;
- `confidence_band` from `low`, `medium`, or `high`;
- non-empty `evidence_ref_ids`;
- non-empty `risk_label_ids`;
- non-empty `rollback_note_ids`;
- `review_status: needs_review`;
- `apply_status: preview_only`;
- `mutation_allowed: false`.

### 5. Risk Labels

Add risk labels for:

- `persona_drift`;
- `overattachment_risk`;
- `unclear_evidence`;
- `boundary_weakening`;
- `blocked_source_excluded`.

Each risk label must include:

- `risk_label_id`;
- `risk_code`;
- severity from `low`, `medium`, or `high`;
- `safe_summary`;
- `mitigation_summary`;
- `blocks_auto_apply: true`.

### 6. Rollback Notes

Each rollback note must include:

- `rollback_note_id`;
- non-empty `target_patch_ids`;
- `prior_summary`;
- `rollback_summary`;
- `required_reviewer_action`;
- `runtime_rollback_ready: false`.

### 7. Blocked Source Exclusions

Add blocked source exclusions for every M36 blocked request.

Each exclusion must include:

- `blocked_request_id`;
- `request_type`;
- `exclusion_reason`;
- `safe_summary`;
- `excluded_from_patch_generation: true`;
- `mutation_allowed: false`.

### 8. Non-Execution Flags

`non_execution_flags` must include:

- `local_only: true`;
- `synthetic_fixture: true`;
- `uses_model_provider: false`;
- `reads_private_sources: false`;
- `writes_persona_store: false`;
- `writes_memory_store: false`;
- `writes_review_store: false`;
- `writes_runtime_store: false`;
- `automatic_apply: false`;
- `sends_messages: false`;
- `uses_platform_adapter: false`;
- `uses_media_runtime: false`.

## Test Requirements

Use TDD:

1. Add failing tests in `tests/test_persona_evolution_preview_payload.py`.
2. Run focused tests and capture RED output in the worker summary.
3. Implement the payload.
4. Re-run focused tests and capture GREEN output.
5. Run a small integration set that includes
   `tests/test_text_first_web_demo_local_server.py`.

The tests should verify:

- payload key exists in serialized demo state;
- schema version and review/apply policies are correct;
- patch candidates cover the required field paths;
- every patch references valid M36 trait candidate ids and evidence refs;
- blocked request ids appear only in blocked source exclusions;
- risk labels and rollback notes are linked and safe;
- non-execution flags are safe;
- recursive payload scan finds no unsafe true states for provider calls,
  private-source reads, store writes, automatic apply, outbound messaging,
  platform adapters, or media runtime.

## Expected Outputs

- Payload added to the adapter.
- Contract doc added at
  `docs/contracts/persona_evolution_preview_payload.md`.
- T431 task package created for static UI rendering.
- Worker summary created at
  `docs/worker_summary/T430_worker_summary.md`.
- Handoff record appended to `docs/07_handoff.md`.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'; pytest tests\test_persona_evolution_preview_payload.py tests\test_persona_distillation_workbench_payload.py tests\test_text_first_web_demo_local_server.py -q -o cache_dir=artifacts\t430_pytest_cache --basetemp=artifacts\t430_pytest_basetemp
```

```powershell
python -m py_compile src\practical_chat_agent\ui\text_first_web_demo_adapter.py
```

```powershell
git diff --check
```

## Reviewer Type

Code and contract review for deterministic payload shape, valid source
workbench linkage, preview-only patch semantics, risk/rollback coverage, and
non-execution guarantees.
