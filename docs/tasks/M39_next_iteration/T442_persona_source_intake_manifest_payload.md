# T442: Persona Source Intake Manifest Payload

## Task ID

T442

## Goal

Add a deterministic local `persona_source_intake_manifest` payload to the
text-first web demo state and cover it with contract tests.

This task is payload-only. It must not render UI, call model providers, read
private data, add source readers, extract traits, write stores, mutate
personas, send messages, connect platform adapters, or enable media runtime.

## Context

M38 added a preview-only persona version draft ledger. M39 prepares the next
safe step toward user-provided source material by defining a consent-gated
source intake manifest before any real source is read, retained, embedded,
extracted, or sent to a model.

The payload should show how future real-person or chat-record distillation can
begin with explicit consent, source ownership, minimization, redaction, blocked
categories, extraction eligibility, and review gates while remaining local,
deterministic, synthetic-only, review-only, and non-ingesting.

## Allowed Files

Future T442 worker may create or modify only:

- `src/practical_chat_agent/ui/text_first_web_demo_adapter.py`
- `tests/test_persona_source_intake_manifest_payload.py`
- `tests/test_text_first_web_demo_local_server.py`
- `docs/contracts/persona_source_intake_manifest_payload.md`
- `docs/tasks/M39_next_iteration/T443_persona_source_intake_manifest_ui.md`
- `docs/worker_summary/T442_worker_summary.md`
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
`persona_source_intake_manifest`.

The payload must include:

- `schema_version`, for example `m39.persona_source_intake_manifest.v1`;
- `manifest_title`;
- `source_candidates`;
- `source_policy_gates`;
- `blocked_source_categories`;
- `redaction_profiles`;
- `review_required: true`;
- `apply_policy`;
- `non_execution_flags`.

### 2. Source Candidates

Add at least five deterministic synthetic source candidate records:

- detailed description;
- fuzzy seed;
- synthetic dialogue excerpt;
- user-provided archive placeholder;
- third-party private source placeholder.

Each candidate must include:

- stable `source_id`;
- `source_kind`;
- `fixture_label`;
- `declared_owner`;
- `consent_status`;
- `minimization_status`;
- `redaction_profile_id`;
- `safe_summary`;
- `raw_content_retained: false`;
- `extraction_eligible`;
- `blocked_reason_ids`;
- `review_gate_ids`;
- `review_required: true`.

At least two candidates must be ineligible for extraction because of missing
consent, unsafe source ownership, real-person replacement risk, deception risk,
or failed minimization/redaction.

### 3. Policy Gates

Add policy gates for:

- `explicit_consent_required`;
- `private_source_minimization_required`;
- `real_person_replacement_blocked`;
- `deception_blocked`;
- `sensitive_data_redaction_required`;
- `reviewer_approval_required`.

Each gate must include:

- stable `gate_id`;
- `gate_code`;
- `enabled: true`;
- `safe_summary`;
- `blocks_extraction_when_failed: true`.

### 4. Blocked Source Categories

Add blocked source categories for:

- no consent from the represented person;
- third-party private chat material;
- deceptive replacement request;
- sensitive data not yet redacted;
- request to impersonate a real person without clear disclosure.

Each blocked category must include:

- `blocked_reason_id`;
- `blocked_code`;
- severity from `medium` or `high`;
- `safe_summary`;
- `blocks_extraction: true`.

### 5. Redaction Profiles

Add redaction profiles for:

- low-risk user-authored description;
- synthetic dialogue fixture;
- private archive placeholder;
- third-party private source placeholder.

Each profile must include:

- `redaction_profile_id`;
- `profile_label`;
- `redaction_status`;
- `safe_summary`;
- `retains_raw_content: false`;
- `requires_review: true`.

### 6. Apply Policy

`apply_policy` must be preview-only and non-ingesting:

- no source files read;
- no raw content retained;
- no embeddings created;
- no extraction performed;
- no persona mutation;
- no runtime write;
- reviewer approval required before any future extraction task.

### 7. Non-Execution Flags

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

1. Add failing tests in `tests/test_persona_source_intake_manifest_payload.py`.
2. Run focused tests and capture RED output in the worker summary.
3. Implement the payload.
4. Re-run focused tests and capture GREEN output.
5. Run a small integration set that includes
   `tests/test_text_first_web_demo_local_server.py`.

The tests should verify:

- payload key exists in serialized demo state;
- schema version and review/apply policies are correct;
- required source candidates are present;
- every source candidate has explicit consent, ownership, minimization,
  redaction, eligibility, blocked reason, and review gate fields;
- raw content is never retained;
- ineligible source candidates have blocked reason ids;
- required policy gate codes are present and block extraction when failed;
- blocked source categories and redaction profiles are linked by ids;
- non-execution flags are safe;
- recursive payload scan finds no unsafe true states for provider calls,
  private-source reads, raw source retention, embeddings, extraction, store
  writes, automatic apply, outbound messaging, platform adapters, or media
  runtime;
- `/demo-state.json` includes the manifest.

## Expected Outputs

- Payload added to the adapter.
- Contract doc added at
  `docs/contracts/persona_source_intake_manifest_payload.md`.
- T443 task package created for static UI rendering.
- Worker summary created at
  `docs/worker_summary/T442_worker_summary.md`.
- Handoff record appended to `docs/07_handoff.md`.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'; pytest tests\test_persona_source_intake_manifest_payload.py tests\test_text_first_web_demo_local_server.py -q -o cache_dir=artifacts\t442_pytest_cache --basetemp=artifacts\t442_pytest_basetemp
```

```powershell
python -m py_compile src\practical_chat_agent\ui\text_first_web_demo_adapter.py
```

```powershell
git diff --check
```

## Reviewer Type

Payload contract review for source consent, minimization, redaction,
extraction eligibility, blocked categories, review gates, non-execution flags,
and no private or provider surfaces.
