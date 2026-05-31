# T344: Web Demo Visual QA

## Task ID

T344

## Goal

Run and document browser visual QA for the static text-first web demo across
desktop and mobile-sized viewports, focusing on layout, labels, scenario
switching, and locked voice/avatar states.

## Why Now

T342 created the static shell and T343 added scenario switching. Before adding
more features, the project needs a focused QA pass that checks whether the
local UI is readable, responsive, and safe to continue building on.

## Allowed Files

Future T344 worker may create or modify only:

- `docs/qa/web_demo_visual_qa.md`
- `docs/tasks/M23_integrated_text_first_web_demo/T345_web_demo_walkthrough.md`
- `docs/worker_summary/T344_worker_summary.md`
- `docs/07_handoff.md`

If T344 needs frontend code changes, tests, model-provider calls, generated
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

- `docs/data_contracts/static_web_demo_shell_contract.md`
- `docs/data_contracts/web_demo_state_switching_contract.md`
- `src/practical_chat_agent/ui/static/text_first_web_demo.html`
- `src/practical_chat_agent/ui/static/text_first_web_demo.css`
- `src/practical_chat_agent/ui/static/text_first_web_demo.js`
- `tests/test_text_first_web_demo_static.py`
- `tests/test_text_first_web_demo_state_switching.py`

## Expected Outputs

### 1. Visual QA Report

Create `docs/qa/web_demo_visual_qa.md` with:

- tested local URL or local file path;
- viewport assumptions;
- screenshots or screenshot references if captured;
- pass/fail notes for desktop and mobile;
- tab and scenario switching notes;
- AI identity label visibility;
- voice/avatar locked-state visibility;
- text overlap/truncation findings;
- residual UI risks.

### 2. Next Task Package

Create
`docs/tasks/M23_integrated_text_first_web_demo/T345_web_demo_walkthrough.md`
for a user-facing walkthrough and study protocol update.

### 3. Worker Summary And Handoff

Write `docs/worker_summary/T344_worker_summary.md` and append a T344 worker
record to `docs/07_handoff.md`.

Do not mark T344 complete in `docs/04_task_board.md`.

## Verification

Minimum command:

```powershell
git diff --check
```

Browser verification with the Browser plugin is required.

## Reviewer Type

Adversarial product/safety UX and frontend review recommended.

Reviewer should block if visual QA is not actually run, AI labels are hidden,
scenario controls obscure content, mobile text overlaps, voice/avatar appears
enabled, or launch-readiness claims are made.
