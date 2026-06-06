# T443: Persona Source Intake Manifest UI

## Task ID

T443

## Goal

Render the local `persona_source_intake_manifest` payload in the static
text-first web demo.

This task is static rendering only. It must not add source readers, read
private data, call model providers, extract traits, write stores, apply persona
changes, send messages, connect platform adapters, or enable media runtime.

## Context

T442 introduced the deterministic source intake manifest payload and contract
tests. T443 should make that manifest visible in the static demo so reviewers
can inspect source candidates, consent state, minimization, redaction profiles,
blocked categories, review gates, and non-execution labels before any future
Review Workspace linkage task.

## Allowed Files

Future T443 worker may create or modify only:

- `src/practical_chat_agent/ui/static/text_first_web_demo.html`
- `src/practical_chat_agent/ui/static/text_first_web_demo.css`
- `src/practical_chat_agent/ui/static/text_first_web_demo.js`
- `tests/test_static_persona_source_intake_manifest.py`
- `tests/test_text_first_web_demo_static.py`
- `tests/test_text_first_web_demo_state_switching.py`
- `docs/contracts/persona_source_intake_manifest_payload.md`
- `docs/tasks/M39_next_iteration/T444_persona_source_intake_review_linkage.md`
- `docs/worker_summary/T443_worker_summary.md`
- `docs/07_handoff.md`

If implementation requires adapter payload changes, source readers, model
providers, private data, runtime stores, platform adapters, outbound messaging,
media runtime, automatic apply, package changes, or task-board edits, Captain
must revise this package before assignment.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not ingest, summarize, transform, quote, or commit real private chat
  records.
- Do not call model providers or prompt execution layers.
- Do not add source readers, embeddings, vector search, semantic ranking,
  similarity scoring, fine-tuning, or remote inference.
- Do not modify Python adapter payload code in this task.
- Do not write PersonaCard, PersonaVersionStore, MemoryEventStore, review
  stores, runtime stores, local databases, queues, schedulers, or files outside
  the allowed static/test/docs files.
- Do not add platform adapters, webhooks, auth, tokens, recipient ids, delivery
  state, automatic outreach, or outbound messaging.
- Do not add microphone, camera, ASR, TTS, voice cloning, Live2D, generated
  audio, generated image, generated video, or media capture.
- Do not add payment processing, production pricing claims, legal advice,
  compliance completion, app-store approval, launch approval, clinical claims,
  regulator acceptance, or user-study validation.
- Do not modify `docs/04_task_board.md`.

## Expected Implementation

### 1. Static Anchors

Add a manifest section to the static demo with anchors for:

- manifest root;
- title;
- schema;
- source candidates;
- policy gates;
- blocked categories;
- redaction profiles;
- non-execution flags.

### 2. JavaScript Rendering

Render from both:

- `window.TEXT_FIRST_WEB_DEMO_STATE.persona_source_intake_manifest`;
- fallback static demo state.

The renderer should display:

- source kind;
- declared owner;
- consent status;
- minimization status;
- redaction profile id;
- extraction eligibility;
- blocked reason ids;
- review gate ids;
- preview-only and non-ingesting labels.

### 3. CSS

Use existing visual patterns and ensure long ids, consent labels, blocked
reason ids, and redaction summaries wrap safely in narrow viewports.

### 4. Safety

The section must not include controls that imply import, upload, read, retain,
extract, embed, apply, commit, mutate, clone, connect, send, publish, media
generation, adapter activation, store-write, or runtime enablement.

## Tests

Use TDD:

1. Add failing static tests for required DOM anchors and renderer/fallback
   state.
2. Run the focused static tests and capture RED output.
3. Implement the static HTML, JS, and CSS.
4. Re-run focused tests and capture GREEN output.
5. Run `node --check` on the JavaScript file.

## Browser QA

After tests pass, run the static demo locally and verify at the available
viewport:

- manifest section is visible;
- all source candidate cards render;
- policy gates, blocked categories, redaction profiles, and non-execution
  labels render;
- no forbidden action controls appear;
- no horizontal overflow.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'; pytest tests\test_static_persona_source_intake_manifest.py tests\test_text_first_web_demo_static.py tests\test_text_first_web_demo_state_switching.py -q -o cache_dir=artifacts\t443_pytest_cache --basetemp=artifacts\t443_pytest_basetemp
```

```powershell
node --check src\practical_chat_agent\ui\static\text_first_web_demo.js
```

```powershell
git diff --check
```

## Reviewer Type

Static UI review for source intake visibility, deterministic fallback behavior,
safe non-execution labeling, responsive wrapping, and absence of action
controls.
