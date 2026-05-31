# T425: Persona Distillation Workbench UI

## Task ID

T425

## Goal

Render the deterministic `persona_distillation_workbench` payload in the
static text-first web demo.

T425 should make the M36 workbench visible to reviewers without adding model
providers, private data ingestion, runtime store writes, automatic apply,
outbound messaging, platform adapters, or media runtime.

## Context

T424 added the adapter payload and contract tests. The next slice should show
the workbench in the local static demo so reviewers can inspect:

- four synthetic input modes;
- safe synthetic input summaries;
- evidence-linked trait candidates;
- blocked clone/deception/private-import requests;
- safety gates and non-execution badges.

## Allowed Files

Future T425 worker may create or modify only:

- `src/practical_chat_agent/ui/static/text_first_web_demo.html`
- `src/practical_chat_agent/ui/static/text_first_web_demo.css`
- `src/practical_chat_agent/ui/static/text_first_web_demo.js`
- `tests/test_persona_distillation_workbench_payload.py`
- `tests/test_static_persona_distillation_workbench.py`
- `tests/test_text_first_web_demo_static.py`
- `tests/test_text_first_web_demo_state_switching.py`
- `docs/contracts/persona_distillation_workbench_payload.md`
- `docs/tasks/M36_next_iteration/T426_persona_workbench_review_linkage.md`
- `docs/worker_summary/T425_worker_summary.md`
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

Add a workbench section to the static demo. It should render from
`window.TEXT_FIRST_WEB_DEMO_STATE.persona_distillation_workbench` and from the
static fallback state when served without embedded JSON.

The section should expose:

- workbench title and schema/version label;
- review-required and preview-only status;
- four input modes;
- synthetic input summaries;
- trait candidate cards grouped or labeled by category;
- evidence ref ids and safe summaries;
- blocked request cards with user-facing explanations;
- safety gate badges;
- non-execution badges.

### 2. No Action Controls

The UI must not render buttons, forms, or commands that imply:

- apply;
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
workbench shape used by the adapter. Do not introduce private data or provider
output.

### 4. Tests

Add static tests for:

- workbench section exists;
- all four mode ids are present in fallback rendering code;
- required trait categories are displayed;
- blocked request records are displayed;
- non-execution labels are displayed;
- forbidden action controls do not appear.

Update existing static/state-switching tests only as needed for the new
section.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'; pytest tests\test_static_persona_distillation_workbench.py tests\test_text_first_web_demo_static.py tests\test_text_first_web_demo_state_switching.py -q -o cache_dir=artifacts\t425_pytest_cache --basetemp=artifacts\t425_pytest_basetemp
```

```powershell
git diff --check
```

If a local static target is available, perform Browser QA:

- workbench section visible;
- four modes visible;
- trait and blocked request cards visible;
- no forbidden action controls;
- no horizontal overflow at the available narrow viewport.

## Reviewer Type

Static UI review for accurate rendering, safe non-execution language, no
forbidden action controls, and readiness for workbench-to-review linkage.
