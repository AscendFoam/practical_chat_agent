# T424: Persona Distillation Workbench Payload

## Task ID

T424

## Goal

Add a deterministic local `persona_distillation_workbench` payload to the
text-first web demo state and cover it with contract tests.

This task is payload-only. It must not render UI, call model providers, read
private data, write runtime stores, or apply trait candidates.

## Context

T423 refined M36 into a local persona intake and distillation workbench
milestone. The first implementation slice should prove the payload contract
before any static UI or review-linkage surfaces are added.

The payload should let later demo tasks show:

- four synthetic input modes;
- structured trait candidates with safe evidence references;
- blocked clone/deception/private-import requests;
- explicit non-execution flags.

## Allowed Files

Future T424 worker may create or modify only:

- `src/practical_chat_agent/ui/text_first_web_demo_adapter.py`
- `tests/test_persona_distillation_workbench_payload.py`
- `tests/test_text_first_web_demo_local_server.py`
- `docs/contracts/persona_distillation_workbench_payload.md`
- `docs/tasks/M36_next_iteration/T425_persona_distillation_workbench_ui.md`
- `docs/worker_summary/T424_worker_summary.md`
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
`persona_distillation_workbench`.

The payload must include:

- `schema_version`, for example `m36.persona_distillation_workbench.v1`;
- `workbench_title`;
- `review_required: true`;
- `apply_policy` set to preview-only and non-mutating;
- `input_modes`;
- `synthetic_inputs`;
- `evidence_refs`;
- `extracted_trait_candidates`;
- `blocked_requests`;
- `safety_gates`;
- `non_execution_flags`.

### 2. Required Input Modes

`input_modes` must include exactly these mode ids unless the contract doc
explains an intentional addition:

- `detailed_description`;
- `fuzzy_seed`;
- `synthetic_dialogue_excerpt`;
- `random_fictional_seed`.

Each mode must state that private sources are not allowed and review is
required.

### 3. Synthetic Inputs

Add at least one synthetic input for each required mode.

Each input must include:

- `input_id`;
- `mode_id`;
- `fixture_label`;
- `safe_summary`;
- `detail_level`;
- `contains_private_content: false`;
- `real_person_reference: false`;
- `raw_content_retained: false`.

Synthetic dialogue excerpts may be summarized rather than stored as raw turns.
Do not introduce real chat data or private file paths.

### 4. Evidence References

Add safe `evidence_refs` entries that point to synthetic input ids.

Each evidence ref must include:

- `evidence_id`;
- `source_input_id`;
- `source_mode_id`;
- `source_kind: synthetic_fixture`;
- `safe_summary`;
- `raw_private_content_included: false`.

### 5. Trait Candidates

Add at least one `extracted_trait_candidates` entry for each category:

- `tone`;
- `pacing`;
- `attachment_style`;
- `humor_style`;
- `boundary_style`;
- `topic_affinity`;
- `taboo_pattern`;
- `memory_use_preference`;
- `growth_hint`.

Each candidate must include:

- `trait_id`;
- `category`;
- `candidate_value`;
- `confidence_band` from `low`, `medium`, or `high`;
- non-empty `evidence_ref_ids`;
- `safe_summary`;
- `review_status: needs_review`;
- `apply_status: preview_only`;
- `mutation_allowed: false`.

### 6. Blocked Requests

Add blocked request examples for:

- real-person clone or replacement;
- deception or impersonation;
- private chat import without consent and source-handling gates.

Each blocked record must include:

- `blocked_request_id`;
- `request_type`;
- `risk_reason`;
- `safe_summary`;
- `user_facing_explanation`;
- `source_mode_id`;
- `status: blocked`;
- `raw_private_content_included: false`;
- `mutation_allowed: false`.

### 7. Safety Gates And Non-Execution Flags

Add safety gates for:

- `synthetic_only_gate`;
- `clone_deception_blocker`;
- `private_source_blocker`;
- `human_review_gate`;
- `non_mutation_gate`;
- `outbound_blocker`.

`non_execution_flags` must include:

- `local_only: true`;
- `synthetic_fixture: true`;
- `uses_model_provider: false`;
- `reads_private_sources: false`;
- `writes_runtime_store: false`;
- `automatic_apply: false`;
- `sends_messages: false`;
- `uses_platform_adapter: false`;
- `uses_media_runtime: false`.

## Test Requirements

Use TDD:

1. Add failing tests in
   `tests/test_persona_distillation_workbench_payload.py`.
2. Run the focused tests and capture RED output in the worker summary.
3. Implement the payload.
4. Re-run the focused tests and capture GREEN output.
5. Run a small integration set that includes
   `tests/test_text_first_web_demo_local_server.py`.

The tests should verify:

- payload key exists in serialized demo state;
- schema version and review/apply policies are correct;
- all required input modes and trait categories exist;
- every trait candidate has valid evidence refs and preview-only apply status;
- blocked request records are present and blocked;
- non-execution flags are safe;
- recursive payload scan finds no unsafe true states for provider calls,
  private-source reads, runtime writes, automatic apply, outbound messaging,
  platform adapters, or media runtime.

## Expected Outputs

- Payload added to the adapter.
- Contract doc added at
  `docs/contracts/persona_distillation_workbench_payload.md`.
- T425 task package created for static UI rendering.
- Worker summary created at
  `docs/worker_summary/T424_worker_summary.md`.
- Handoff record appended to `docs/07_handoff.md`.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'; pytest tests\test_persona_distillation_workbench_payload.py tests\test_text_first_web_demo_local_server.py -q -o cache_dir=artifacts\t424_pytest_cache --basetemp=artifacts\t424_pytest_basetemp
```

```powershell
python -m py_compile src\practical_chat_agent\ui\text_first_web_demo_adapter.py
```

```powershell
git diff --check
```

## Reviewer Type

Code and contract review for deterministic payload shape, synthetic-only
boundaries, safe evidence references, blocked clone/deception records, and
non-execution guarantees.
