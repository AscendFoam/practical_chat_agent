# T342: Static Web Demo Shell

## Task ID

T342

## Goal

Build a dependency-light local static web shell that consumes the synthetic
`TextFirstWebDemoState` payload and presents the text-first companion prototype
as one usable demo.

## Why Now

T341 creates a serializable local demo state. The next step is a real browser
surface that lets reviewers inspect onboarding, persona, chat/memory, life
stream, proactive settings, controls, voice locked state, and avatar locked
state without provider calls, private data, or runtime media.

## Allowed Files

Future T342 worker may create or modify only:

- `src/practical_chat_agent/ui/text_first_web_demo_static.py`
- `src/practical_chat_agent/ui/static/text_first_web_demo.html`
- `src/practical_chat_agent/ui/static/text_first_web_demo.css`
- `src/practical_chat_agent/ui/static/text_first_web_demo.js`
- `tests/test_text_first_web_demo_static.py`
- `docs/data_contracts/static_web_demo_shell_contract.md`
- `docs/tasks/M23_integrated_text_first_web_demo/T343_web_demo_state_switching.md`
- `docs/worker_summary/T342_worker_summary.md`
- `docs/07_handoff.md`

If T342 needs external frontend packages, generated media, model-provider
calls, voice/avatar runtime, private data processing, task-board edits,
platform adapters, or outbound messaging, Captain must revise this package
before assignment.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not call model providers.
- Do not synthesize audio, generate images/video, clone voices/faces, capture
  microphone/camera input, or process media samples.
- Do not add platform delivery, push notification, send, schedule, queue,
  webhook, token, adapter, or realtime fields.
- Do not modify `docs/04_task_board.md`.
- Do not claim legal advice, compliance completion, app-store approval, launch
  approval, user-study validation, or regulator acceptance.

## Inputs To Read

Required:

- `docs/product/text_first_web_demo_scope.md`
- `docs/data_contracts/text_first_web_demo_state_contract.md`
- `src/practical_chat_agent/ui/text_first_web_demo_adapter.py`
- `tests/test_text_first_web_demo_adapter.py`

## Expected Outputs

### 1. Tests First

Create `tests/test_text_first_web_demo_static.py` before implementation.

Minimum test coverage:

- static shell file paths are exposed by Python helper;
- generated payload can be embedded or loaded without private data;
- HTML includes app container, persistent AI identity area, tabs, and locked
  voice/avatar surfaces;
- HTML/JS/CSS contain no provider URLs, send/schedule/platform/webhook/queue
  fields, microphone/camera prompts, or generated media paths;
- helper exposes no server, provider, outbound, microphone, camera, audio, or
  video methods.

### 2. Static Shell

Create a local static shell using plain HTML/CSS/JavaScript:

- no package manager;
- no external network assets;
- no server requirement if possible;
- responsive layout;
- tabs for Chat, Persona, Memory, Life Stream, Controls, Voice/Avatar;
- persistent AI/synthetic label;
- synthetic demo state rendered from adapter payload;
- voice/avatar displayed as locked, not interactive runtime.

### 3. Contract

Create `docs/data_contracts/static_web_demo_shell_contract.md` explaining:

- files;
- payload flow;
- UI surfaces;
- no-runtime boundaries;
- manual local open/run instructions;
- verification commands.

### 4. Next Task Package

Create
`docs/tasks/M23_integrated_text_first_web_demo/T343_web_demo_state_switching.md`
for adding local scenario switching across safe, blocked, crisis, and
review-required states.

### 5. Worker Summary And Handoff

Write `docs/worker_summary/T342_worker_summary.md` and append a T342 worker
record to `docs/07_handoff.md`.

Do not mark T342 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\ui\text_first_web_demo_static.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_text_first_web_demo_static.py tests\test_text_first_web_demo_adapter.py -q -o cache_dir=artifacts\t342_pytest_cache --basetemp=artifacts\t342_pytest_basetemp
```

```powershell
git diff --check
```

If T342 starts any local server, it must also verify the browser surface with
the Browser plugin and report the local URL. Prefer static file open if the
implementation works without a server.

## Reviewer Type

Adversarial product/safety UX and frontend review recommended.

Reviewer should block if T342 hides AI labels, introduces external network
assets, provider calls, private data, voice/avatar runtime, microphone/camera
prompts, outbound fields, unreadable mobile layout, overlapping text, or
launch-readiness claims.
