# T353: Keyboard Responsive UI Hardening

## Task ID

T353

## Goal

Update the static web demo UI to use friendly labels and stronger
keyboard/accessibility semantics while preserving local-only, synthetic,
non-sending behavior.

## Why Now

T352 defined the display-label and accessibility contract. T353 should implement
the first static UI hardening pass before formal M24 Browser QA.

## Allowed Files

Future T353 worker may create or modify only:

- `src/practical_chat_agent/ui/static/text_first_web_demo.html`
- `src/practical_chat_agent/ui/static/text_first_web_demo.css`
- `src/practical_chat_agent/ui/static/text_first_web_demo.js`
- `tests/test_text_first_web_demo_accessibility.py`
- `tests/test_text_first_web_demo_static.py`
- `tests/test_text_first_web_demo_state_switching.py`
- `docs/data_contracts/web_demo_display_accessibility_contract.md`
- `docs/tasks/M24_demo_hardening_and_local_backend/T354_local_run_browser_qa.md`
- `docs/worker_summary/T353_worker_summary.md`
- `docs/07_handoff.md`

If T353 needs Python backend changes, package-manager dependencies, model
provider calls, generated media, voice/avatar runtime, private data processing,
task-board edits, platform adapters, outbound messaging, screenshot artifacts,
or launch claims, Captain must revise this package before assignment.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not call model providers.
- Do not synthesize audio, generate images/video, clone voices/faces, capture
  microphone/camera input, or process media samples.
- Do not add external network assets or package-manager dependencies.
- Do not add backend routes, persistence, platform delivery, push notification,
  send, schedule, queue, webhook, token, adapter, or realtime fields.
- Do not enable voice, avatar, Live2D, camera, microphone, ASR, TTS, or media
  runtime.
- Do not modify `docs/04_task_board.md`.
- Do not claim legal advice, compliance completion, app-store approval, launch
  approval, user-study validation, regulator acceptance, or real user evidence.

## Inputs To Read

Required:

- `docs/product/web_demo_friendly_labels_accessibility.md`
- `docs/data_contracts/web_demo_display_accessibility_contract.md`
- `docs/data_contracts/local_web_demo_server_contract.md`
- `docs/qa/web_demo_visual_qa.md`
- `src/practical_chat_agent/ui/static/text_first_web_demo.html`
- `src/practical_chat_agent/ui/static/text_first_web_demo.css`
- `src/practical_chat_agent/ui/static/text_first_web_demo.js`
- `tests/test_text_first_web_demo_static.py`
- `tests/test_text_first_web_demo_state_switching.py`

## Expected Outputs

### 1. Static UI Hardening

Update the static HTML/CSS/JS to:

- use friendly labels for technical states where visible;
- preserve machine-readable state in payloads, `data-*` attributes, or tests;
- add top-level tab accessibility semantics;
- add panel accessibility semantics;
- add scenario active-state semantics;
- preserve visible focus states;
- ensure long labels wrap without horizontal page overflow;
- keep AI identity visible;
- keep proactive no-send visible;
- keep voice/avatar locked/off visible.

### 2. Tests

Add or update tests to cover:

- friendly label mapping or rendered labels;
- tab `aria-selected`/`aria-controls`/panel relationships;
- scenario `aria-pressed` semantics;
- hidden inactive panels;
- no forbidden external/provider/media/platform/outbound strings;
- voice/avatar not enabled;
- proactive no-send label remains present.

Follow TDD: write failing tests before changing static assets.

### 3. Next Task Package

Create
`docs/tasks/M24_demo_hardening_and_local_backend/T354_local_run_browser_qa.md`
for formal Browser QA of the local run path and hardened UI.

### 4. Worker Summary And Handoff

Write `docs/worker_summary/T353_worker_summary.md` and append a T353 worker
record to `docs/07_handoff.md`.

Do not mark T353 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'
pytest tests\test_text_first_web_demo_accessibility.py tests\test_text_first_web_demo_state_switching.py tests\test_text_first_web_demo_static.py tests\test_text_first_web_demo_local_server.py tests\test_text_first_web_demo_adapter.py -q -o cache_dir=artifacts\t353_pytest_cache --basetemp=artifacts\t353_pytest_basetemp
```

```powershell
git diff --check
```

Browser smoke verification is required after static UI changes. Use the T351
local run path or an equivalent temporary localhost route, and stop any server
after verification.

## Reviewer Type

Adversarial frontend, accessibility, and product/safety UX review recommended.

Reviewer should block if friendly labels weaken safety meaning, keyboard
semantics are absent, AI identity is hidden, proactive behavior appears
send-capable, voice/avatar appears enabled, external assets are added, or
Browser smoke verification is skipped.

