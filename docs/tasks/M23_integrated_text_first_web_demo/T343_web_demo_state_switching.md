# T343: Web Demo State Switching

## Task ID

T343

## Goal

Add local scenario switching to the static web demo so reviewers can move
between safe, blocked, crisis/dependency, and review-required states without
changing code or using external services.

## Why Now

T342 renders the integrated static shell. The next usability gap is that the
demo needs explicit scenario controls so reviewers can inspect all critical
safety states, not only the default Chat and Voice / Avatar panels.

## Allowed Files

Future T343 worker may create or modify only:

- `src/practical_chat_agent/ui/text_first_web_demo_adapter.py`
- `src/practical_chat_agent/ui/static/text_first_web_demo.html`
- `src/practical_chat_agent/ui/static/text_first_web_demo.css`
- `src/practical_chat_agent/ui/static/text_first_web_demo.js`
- `tests/test_text_first_web_demo_state_switching.py`
- `docs/data_contracts/web_demo_state_switching_contract.md`
- `docs/tasks/M23_integrated_text_first_web_demo/T344_web_demo_visual_qa.md`
- `docs/worker_summary/T343_worker_summary.md`
- `docs/07_handoff.md`

If T343 needs external frontend packages, model-provider calls, generated
media, voice/avatar runtime, private data processing, task-board edits,
platform adapters, or outbound messaging, Captain must revise this package
before assignment.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not call model providers.
- Do not synthesize audio, generate images/video, clone voices/faces, capture
  microphone/camera input, or process media samples.
- Do not add external network assets or package-manager dependencies.
- Do not add platform delivery, push notification, send, schedule, queue,
  webhook, token, adapter, or realtime fields.
- Do not modify `docs/04_task_board.md`.
- Do not claim legal advice, compliance completion, app-store approval, launch
  approval, user-study validation, or regulator acceptance.

## Inputs To Read

Required:

- `docs/product/text_first_web_demo_scope.md`
- `docs/data_contracts/text_first_web_demo_state_contract.md`
- `docs/data_contracts/static_web_demo_shell_contract.md`
- `src/practical_chat_agent/ui/text_first_web_demo_adapter.py`
- `src/practical_chat_agent/ui/static/text_first_web_demo.html`
- `src/practical_chat_agent/ui/static/text_first_web_demo.css`
- `src/practical_chat_agent/ui/static/text_first_web_demo.js`
- `tests/test_text_first_web_demo_static.py`

## Expected Outputs

### 1. Tests First

Create `tests/test_text_first_web_demo_state_switching.py` before
implementation.

Minimum test coverage:

- scenario controls exist for safe review, blocked persona, crisis chat,
  dependency proactive, life-stream review, controls, and voice/avatar locked;
- switching is local only and does not mutate source payload;
- HTML/JS/CSS contain no external network assets, provider calls, private data,
  generated media paths, microphone/camera prompts, or outbound fields;
- state switching preserves visible AI/synthetic labels;
- helper and UI expose no server, model, media, or outbound methods.

### 2. Static Shell Update

Update the static shell to include scenario controls:

- compact segmented controls or tabs for scenarios;
- no hidden labels;
- no layout shift that obscures content;
- keyboard-accessible buttons;
- responsive behavior.

### 3. Contract

Create `docs/data_contracts/web_demo_state_switching_contract.md` explaining:

- scenario vocabulary;
- local-only interaction model;
- payload immutability expectation;
- blocked features and non-actions;
- verification commands.

### 4. Next Task Package

Create
`docs/tasks/M23_integrated_text_first_web_demo/T344_web_demo_visual_qa.md` for
browser visual QA across desktop and mobile viewports.

### 5. Worker Summary And Handoff

Write `docs/worker_summary/T343_worker_summary.md` and append a T343 worker
record to `docs/07_handoff.md`.

Do not mark T343 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'
pytest tests\test_text_first_web_demo_state_switching.py tests\test_text_first_web_demo_static.py tests\test_text_first_web_demo_adapter.py -q -o cache_dir=artifacts\t343_pytest_cache --basetemp=artifacts\t343_pytest_basetemp
```

```powershell
git diff --check
```

Browser verification with the Browser plugin is required because T343 changes
interactive frontend behavior.

## Reviewer Type

Adversarial product/safety UX and frontend review recommended.

Reviewer should block if scenario switching hides AI labels, creates confusing
states, adds network assets, provider calls, private data, runtime voice/avatar,
media prompts, outbound fields, overlapping text, or launch-readiness claims.
