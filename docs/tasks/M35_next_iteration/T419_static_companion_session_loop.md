# T419: Static Companion Session Loop

## Task ID

T419

## Goal

Render the T418 `companion_session` payload in the static local web demo.

T419 should add a compact operational session-loop panel that shows synthetic
user/companion turns, memory recalls, persona cues, safety notes, and
post-turn review candidates. The UI should make the demo feel closer to a
companion experience without adding model calls, private-data ingestion,
runtime mutation, outbound messaging, or media behavior.

## Allowed Files

Future T419 worker may create or modify only:

- `src/practical_chat_agent/ui/static/text_first_web_demo.html`
- `src/practical_chat_agent/ui/static/text_first_web_demo.js`
- `src/practical_chat_agent/ui/static/text_first_web_demo.css`
- `tests/test_static_companion_session_loop.py`
- `tests/test_text_first_web_demo_static.py`
- `tests/test_text_first_web_demo_state_switching.py`
- `docs/data_contracts/static_companion_session_loop_contract.md`
- `docs/tasks/M35_next_iteration/T420_session_review_candidate_linkage.md`
- `docs/worker_summary/T419_worker_summary.md`
- `docs/07_handoff.md`

If T419 needs adapter payload changes, private data, source readers,
model-provider calls, package changes, platform adapters, outbound messaging,
voice/avatar runtime, media generation, automatic apply triggers,
PersonaVersionStore writes, MemoryEventStore writes, or task-board edits,
Captain must revise this package before assignment.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not ingest, summarize, transform, quote, or commit real private chat
  records.
- Do not call model providers or remote inference.
- Do not implement prompt execution, embeddings, vector search, semantic
  ranking, similarity scoring, fine-tuning, source readers, or real chat
  distillation.
- Do not write PersonaVersionStore, MemoryEventStore, review stores, runtime
  stores, files under `private/`, or persistent user data.
- Do not add schedulers, queues, webhooks, auth, tokens, recipient ids,
  delivery state, platform adapters, automatic outreach, outbound messaging,
  or delivery simulation.
- Do not add microphone, camera, ASR, TTS, voice cloning, Live2D, generated
  audio, generated image, generated video, or media capture.
- Do not add payment processing, production pricing claims, legal advice,
  compliance completion, app-store approval, launch approval, clinical claims,
  or regulator acceptance.
- Do not modify `docs/04_task_board.md`.

## Expected Outputs

### 1. Static UI

Add a session-loop section or panel to the static demo that renders:

- session title and summary;
- ordered user/companion turns;
- memory recall chips or references for companion turns;
- persona cue chips or references for companion turns;
- safety note references;
- post-turn candidate summaries;
- visible non-execution status.

The panel should remain work-focused and compact. It should not become a
landing page or marketing hero.

### 2. Static JavaScript

Update static JS to:

- include safe fallback/default `companion_session` data for static file
  preview;
- render the adapter-backed `companion_session` when supplied by the local
  server;
- avoid action controls for sending, scheduling, provider calls, platform
  connection, media generation, or automatic apply;
- avoid dynamic network calls.

If existing static forbidden-field tests use broad substring scans that conflict
with false non-execution flags such as `sends_messages: false`, narrow those
tests to forbid dangerous enabled states and real action surfaces.

### 3. Responsive CSS

Add CSS so:

- turns and candidate summaries wrap cleanly;
- the session loop remains readable on narrow viewports;
- repeated chips/cards use stable dimensions and `min-width: 0` where needed;
- no text overlaps neighboring sections.

### 4. Tests

Create `tests/test_static_companion_session_loop.py` proving:

- HTML contains session-loop hooks;
- JS contains a renderer for `companion_session`;
- CSS contains responsive/session-loop layout rules;
- static assets expose no provider/outbound/platform/media action controls;
- local server responses render the session payload without dangerous enabled
  states.

Update existing static tests only as needed to avoid false positives around
explicit `false` non-execution flags.

### 5. Data Contract

Create `docs/data_contracts/static_companion_session_loop_contract.md`.

### 6. Next Task Package

Create `docs/tasks/M35_next_iteration/T420_session_review_candidate_linkage.md`.

T420 should be scoped to linking post-session candidates into existing review
workspace surfaces without automatic apply or sending.

### 7. Worker Summary And Handoff

Write `docs/worker_summary/T419_worker_summary.md` and append a T419 worker
record to `docs/07_handoff.md`.

Do not mark T419 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'
pytest tests\test_static_companion_session_loop.py tests\test_local_companion_session_simulator.py tests\test_text_first_web_demo_static.py tests\test_text_first_web_demo_local_server.py tests\test_text_first_web_demo_accessibility.py tests\test_text_first_web_demo_state_switching.py -q
```

```powershell
git diff --check
```

Use project-local pytest cache and basetemp paths if the default user temp
directory is not writable.

## Browser QA

After tests pass, use the in-app Browser through a localhost preview to verify:

- the session-loop section is visible;
- turns, recall/cue chips, and candidates are readable;
- text fits on the tested viewport without horizontal overflow;
- no send/schedule/provider/platform/media controls appear.

## Reviewer Type

Adversarial static UI review for companion-session readability, non-execution
boundaries, responsive layout, and no provider/outbound/media surface
expansion.
