# T431: Persona Evolution Preview UI

## Task ID

T431

## Goal

Render the deterministic `persona_evolution_preview` payload in the static
text-first web demo.

T431 should make controlled persona evolution visible to reviewers without
adding model providers, private data ingestion, runtime store writes,
automatic apply, outbound messaging, platform adapters, or media runtime.

## Context

T430 added the adapter payload and contract tests. The next slice should show
the preview in the local static demo so reviewers can inspect:

- source workbench linkage;
- persona snapshot before;
- preview-only patch candidates;
- risk labels and mitigations;
- rollback notes;
- blocked source exclusions;
- non-execution badges.

## Allowed Files

Future T431 worker may create or modify only:

- `src/practical_chat_agent/ui/static/text_first_web_demo.html`
- `src/practical_chat_agent/ui/static/text_first_web_demo.css`
- `src/practical_chat_agent/ui/static/text_first_web_demo.js`
- `tests/test_persona_evolution_preview_payload.py`
- `tests/test_static_persona_evolution_preview.py`
- `tests/test_text_first_web_demo_static.py`
- `tests/test_text_first_web_demo_state_switching.py`
- `docs/contracts/persona_evolution_preview_payload.md`
- `docs/tasks/M37_next_iteration/T432_persona_evolution_review_linkage.md`
- `docs/worker_summary/T431_worker_summary.md`
- `docs/07_handoff.md`

If implementation requires adapter payload changes, package changes, private
data, source readers, model providers, runtime stores, platform adapters,
outbound messaging, media runtime, automatic apply, or task-board edits,
Captain must revise this package before assignment.

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
  the allowed docs/test/static files.
- Do not add platform adapters, webhooks, auth, tokens, recipient ids, delivery
  state, automatic outreach, or outbound messaging.
- Do not add microphone, camera, ASR, TTS, voice cloning, Live2D, generated
  audio, generated image, generated video, or media capture.
- Do not add payment processing, production pricing claims, legal advice,
  compliance completion, app-store approval, launch approval, clinical claims,
  regulator acceptance, or user-study validation.
- Do not modify `docs/04_task_board.md`.

## Expected Implementation

### 1. Static Section

Add an evolution preview section to the static demo. It should render from
`window.TEXT_FIRST_WEB_DEMO_STATE.persona_evolution_preview` and from the
static fallback state when served without embedded JSON.

The section should expose:

- preview title and schema/version label;
- source workbench ref;
- persona snapshot before;
- patch candidate cards with before/after summaries;
- changed field paths;
- risk labels and mitigation summaries;
- rollback notes;
- blocked source exclusions;
- non-execution badges.

### 2. No Action Controls

The UI must not render buttons, forms, or commands that imply:

- apply;
- commit;
- mutate;
- clone;
- import;
- upload;
- record;
- connect;
- send;
- publish;
- generate media;
- enable runtime.

Static labels are acceptable when they explain a blocked or preview-only state.

### 3. Fallback State

Update the static JavaScript fallback state with the same deterministic
evolution preview shape used by the adapter. Do not introduce private data or
provider output.

### 4. Tests

Add static tests for:

- evolution preview section exists;
- required changed field paths are present;
- risk labels render;
- rollback notes render;
- blocked source exclusions render;
- non-execution labels render;
- forbidden action controls do not appear.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'; pytest tests\test_static_persona_evolution_preview.py tests\test_text_first_web_demo_static.py tests\test_text_first_web_demo_state_switching.py -q -o cache_dir=artifacts\t431_pytest_cache --basetemp=artifacts\t431_pytest_basetemp
```

```powershell
node --check src\practical_chat_agent\ui\static\text_first_web_demo.js
```

```powershell
git diff --check
```

If a local static target is available, perform Browser QA:

- evolution preview section visible;
- patch candidate cards visible;
- risk labels and rollback notes visible;
- blocked source exclusions visible;
- no forbidden action controls;
- no horizontal overflow at the available narrow viewport.

## Reviewer Type

Static UI review for accurate rendering, safe non-execution language, no
forbidden action controls, and readiness for evolution-to-review linkage.
