# T352: Friendly Labels And Accessibility Contract

## Task ID

T352

## Goal

Define friendly display labels and accessibility requirements for the M24 local
web demo before changing static UI behavior.

## Why Now

T351 adds a local server helper for adapter-backed demo state. Before editing
the static UI, the project needs a contract that maps technical states to
reviewer-friendly labels and states the keyboard/accessibility requirements that
T353 should implement.

## Allowed Files

Future T352 worker may create or modify only:

- `docs/product/web_demo_friendly_labels_accessibility.md`
- `docs/data_contracts/web_demo_display_accessibility_contract.md`
- `docs/tasks/M24_demo_hardening_and_local_backend/T353_keyboard_responsive_ui_hardening.md`
- `docs/worker_summary/T352_worker_summary.md`
- `docs/07_handoff.md`

If T352 needs code changes, tests, browser reruns, model-provider calls,
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
- Do not add frontend code, backend routes, persistence, platform delivery,
  push notification, send, schedule, queue, webhook, token, adapter, or realtime
  fields.
- Do not enable voice, avatar, Live2D, camera, microphone, ASR, TTS, or media
  runtime.
- Do not modify `docs/04_task_board.md`.
- Do not claim legal advice, compliance completion, app-store approval, launch
  approval, user-study validation, regulator acceptance, or real user evidence.

## Inputs To Read

Required:

- `docs/product/m24_demo_hardening_scope.md`
- `docs/data_contracts/local_web_demo_server_contract.md`
- `docs/qa/web_demo_visual_qa.md`
- `docs/product/text_first_web_demo_walkthrough.md`
- `docs/research/text_first_web_demo_study_protocol_update.md`
- `src/practical_chat_agent/ui/static/text_first_web_demo.html`
- `src/practical_chat_agent/ui/static/text_first_web_demo.css`
- `src/practical_chat_agent/ui/static/text_first_web_demo.js`

## Expected Outputs

### 1. Product Label And Accessibility Plan

Create `docs/product/web_demo_friendly_labels_accessibility.md` with:

- target audiences;
- label tone principles;
- technical-to-friendly label mapping;
- scenario-specific copy improvements;
- accessibility priorities;
- keyboard interaction expectations;
- responsive layout expectations;
- explicit non-goals.

### 2. Display And Accessibility Contract

Create `docs/data_contracts/web_demo_display_accessibility_contract.md` with:

- required display labels;
- required data attributes or machine-readable states, if any;
- active tab/panel semantics;
- keyboard behavior contract;
- focus visibility contract;
- no-runtime and no-outbound invariants;
- acceptance criteria for T353.

### 3. Next Task Package

Create
`docs/tasks/M24_demo_hardening_and_local_backend/T353_keyboard_responsive_ui_hardening.md`
for static UI hardening.

### 4. Worker Summary And Handoff

Write `docs/worker_summary/T352_worker_summary.md` and append a T352 worker
record to `docs/07_handoff.md`.

Do not mark T352 complete in `docs/04_task_board.md`.

## Verification

Minimum command:

```powershell
git diff --check
```

## Reviewer Type

Adversarial product/safety UX, accessibility, and frontend review recommended.

Reviewer should block if friendly labels weaken safety meaning, hide AI
identity, make proactive behavior appear send-capable, present voice/avatar as
enabled, or treat accessibility planning as completed accessibility validation.

