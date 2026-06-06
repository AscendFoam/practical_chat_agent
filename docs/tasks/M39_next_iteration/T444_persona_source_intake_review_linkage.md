# T444: Persona Source Intake Review Linkage

## Task ID

T444

## Goal

Expose deterministic source intake manifest cards in Review Workspace.

This task links already-rendered manifest data into review cards only. It must
not read private data, add source readers, call model providers, extract
traits, retain raw content, write stores, apply persona changes, send messages,
connect platform adapters, or enable media runtime.

## Context

T442 introduced `persona_source_intake_manifest` as a deterministic local
payload. T443 rendered it in the static text-first web demo. T444 should make
source candidates, policy gates, blocked categories, and redaction profiles
reviewable from Review Workspace while preserving preview-only,
non-ingesting semantics.

## Allowed Files

Future T444 worker may create or modify only:

- `src/practical_chat_agent/ui/text_first_web_demo_adapter.py`
- `src/practical_chat_agent/ui/static/text_first_web_demo.js`
- `tests/test_persona_source_intake_review_linkage.py`
- `tests/test_text_first_web_demo_local_server.py`
- `tests/test_text_first_web_demo_static.py`
- `tests/test_text_first_web_demo_state_switching.py`
- `docs/contracts/persona_source_intake_manifest_payload.md`
- `docs/tasks/M39_next_iteration/T445_persona_source_intake_responsive_hardening.md`
- `docs/worker_summary/T444_worker_summary.md`
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
- Do not add new static source-intake action controls.
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

Add `review_workspace.source_intake_review_cards`.

The count must equal:

- number of `source_candidates`;
- plus number of `source_policy_gates`;
- plus number of `blocked_source_categories`;
- plus number of `redaction_profiles`.

Required card contract:

- `schema_version: review_workspace_persona_source_intake_card_v1`;
- `source_surface: persona_source_intake_manifest`;
- `filter_keys` includes `source`;
- `review_required: true`;
- `preview_only: true`;
- `changes_state: false`;
- `mutation_allowed: false`;
- `automatic_apply: false`;
- `sends_messages: false`;
- `runtime_ready: false`.

Required card kinds:

- `persona_source_candidate_review`;
- `persona_source_policy_gate_review`;
- `persona_source_blocked_category_review`;
- `persona_source_redaction_profile_review`.

Review Workspace filter tabs must include
`{ key: source, label: Source, count: len(source_intake_review_cards) }`.

### 2. Static Fallback Linkage

Update the JavaScript fallback state so Review Workspace still exposes source
cards when static HTML is opened directly.

### 3. Rendered Detail Rows

Review cards should show relevant detail rows for:

- source kind;
- consent status;
- declared owner;
- minimization status;
- extraction eligibility;
- blocked reason ids;
- review gate ids;
- policy gate code;
- blocked code;
- redaction status;
- preview-only and non-ingesting state.

## Tests

Use TDD:

1. Add failing review-linkage tests.
2. Run focused tests and capture RED output.
3. Implement adapter and static fallback linkage.
4. Re-run focused tests and capture GREEN output.
5. Run `python -m py_compile` and `node --check`.

## Browser QA

After tests pass, verify the Review Workspace source filter at the available
viewport:

- `Source` filter tab is visible with the expected count;
- source intake review cards render;
- card detail rows are visible;
- no forbidden action controls appear;
- no horizontal overflow.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'; pytest tests\test_persona_source_intake_review_linkage.py tests\test_persona_source_intake_manifest_payload.py tests\test_text_first_web_demo_local_server.py tests\test_text_first_web_demo_static.py tests\test_text_first_web_demo_state_switching.py -q -o cache_dir=artifacts\t444_pytest_cache --basetemp=artifacts\t444_pytest_basetemp
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

Review Workspace linkage review for source-card counts, filter behavior,
detail rows, preview-only semantics, non-ingesting guarantees, and absence of
private/provider/runtime surfaces.
