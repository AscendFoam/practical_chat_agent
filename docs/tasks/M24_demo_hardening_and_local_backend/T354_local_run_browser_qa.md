# T354: Local Run Browser QA

## Task ID

T354

## Goal

Run and document formal Browser QA for the M24 local run path and hardened
static UI.

## Why Now

T351 added the local server helper and T353 hardened the static UI with friendly
labels and accessibility semantics. T354 should verify the integrated local run
path in a browser before M24 closes.

## Allowed Files

Future T354 worker may create or modify only:

- `docs/qa/local_run_browser_qa.md`
- `docs/tasks/M24_demo_hardening_and_local_backend/T355_m24_milestone_review.md`
- `docs/worker_summary/T354_worker_summary.md`
- `docs/07_handoff.md`

If T354 needs code changes, tests, static asset edits, model-provider calls,
generated media, voice/avatar runtime, private data processing, task-board
edits, platform adapters, outbound messaging, screenshot artifacts, or launch
claims, Captain must revise this package before assignment.

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

- `docs/data_contracts/local_web_demo_server_contract.md`
- `docs/data_contracts/web_demo_display_accessibility_contract.md`
- `docs/product/web_demo_friendly_labels_accessibility.md`
- `docs/worker_summary/T351_worker_summary.md`
- `docs/worker_summary/T353_worker_summary.md`
- `src/practical_chat_agent/ui/text_first_web_demo_local_server.py`
- `src/practical_chat_agent/ui/static/text_first_web_demo.html`
- `src/practical_chat_agent/ui/static/text_first_web_demo.css`
- `src/practical_chat_agent/ui/static/text_first_web_demo.js`
- `tests/test_text_first_web_demo_accessibility.py`
- `tests/test_text_first_web_demo_local_server.py`

## Expected Outputs

### 1. Browser QA Report

Create `docs/qa/local_run_browser_qa.md` with:

- tested local run command or helper;
- tested local URL;
- viewport assumptions;
- screenshot notes if screenshots are captured;
- desktop pass/fail notes;
- mobile pass/fail notes;
- scenario switching notes;
- tab/panel ARIA notes;
- scenario `aria-pressed` notes;
- friendly label visibility notes;
- AI identity visibility notes;
- proactive no-send visibility notes;
- voice/avatar locked visibility notes;
- text overlap/truncation notes;
- residual accessibility and QA risks.

### 2. Next Task Package

Create
`docs/tasks/M24_demo_hardening_and_local_backend/T355_m24_milestone_review.md`
for M24 milestone review.

### 3. Worker Summary And Handoff

Write `docs/worker_summary/T354_worker_summary.md` and append a T354 worker
record to `docs/07_handoff.md`.

Do not mark T354 complete in `docs/04_task_board.md`.

## Verification

Minimum command:

```powershell
git diff --check
```

Browser verification with the Browser plugin is required.

## Reviewer Type

Adversarial frontend, accessibility, and product/safety UX review recommended.

Reviewer should block if Browser QA is not actually run, local run path is not
used, AI identity is hidden, friendly labels are absent, active ARIA states do
not update, proactive appears send-capable, voice/avatar appears enabled, or
launch/user-study/compliance claims are made.

