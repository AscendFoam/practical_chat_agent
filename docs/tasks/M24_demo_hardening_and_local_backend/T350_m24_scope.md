# T350: M24 Scope

## Task ID

T350

## Goal

Scope M24 as a local demo hardening and local backend milestone for the
text-first companion web demo.

## Why Now

M23 produced a static text-first web demo and documented its visual QA,
walkthrough, and internal supervised-review protocol. The next useful milestone
is to make the demo easier to run, inspect, and review locally without changing
its safety posture or introducing live product behavior.

## Allowed Files

Future T350 worker may create or modify only:

- `docs/product/m24_demo_hardening_scope.md`
- `docs/tasks/M24_demo_hardening_and_local_backend/T351_local_demo_server.md`
- `docs/worker_summary/T350_worker_summary.md`
- `docs/07_handoff.md`

If T350 needs code changes, tests, browser reruns, model-provider calls,
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
- Do not add production backend routes, persistence, platform delivery, push
  notification, send, schedule, queue, webhook, token, adapter, or realtime
  fields.
- Do not enable voice, avatar, Live2D, camera, microphone, ASR, TTS, or media
  runtime.
- Do not modify `docs/04_task_board.md`.
- Do not claim legal advice, compliance completion, app-store approval, launch
  approval, user-study validation, regulator acceptance, or real user evidence.

## Inputs To Read

Required:

- `docs/review/M23_review.md`
- `docs/product/text_first_web_demo_scope.md`
- `docs/qa/web_demo_visual_qa.md`
- `docs/product/text_first_web_demo_walkthrough.md`
- `docs/research/text_first_web_demo_study_protocol_update.md`
- `docs/data_contracts/text_first_web_demo_state_contract.md`
- `docs/data_contracts/static_web_demo_shell_contract.md`
- `docs/data_contracts/web_demo_state_switching_contract.md`
- `src/practical_chat_agent/ui/text_first_web_demo_adapter.py`
- `src/practical_chat_agent/ui/text_first_web_demo_static.py`
- `src/practical_chat_agent/ui/static/text_first_web_demo.html`
- `src/practical_chat_agent/ui/static/text_first_web_demo.css`
- `src/practical_chat_agent/ui/static/text_first_web_demo.js`

## Expected Outputs

### 1. M24 Product Scope

Create `docs/product/m24_demo_hardening_scope.md` with:

- M24 objective and non-goals;
- local run shape recommendation;
- local backend or generated HTML direction;
- UX hardening priorities;
- accessibility and keyboard priorities;
- copy/friendly-label priorities;
- QA plan for desktop/mobile/accessibility;
- safety and consent invariants;
- recommended task sequence for M24.

The scope must keep M24 local, synthetic, review-first, and non-sending.

### 2. Next Task Package

Create
`docs/tasks/M24_demo_hardening_and_local_backend/T351_local_demo_server.md`
for a local demo server or generated HTML route. The task should require tests
and must keep the implementation local, synthetic, dependency-light, and
non-sending.

### 3. Worker Summary And Handoff

Write `docs/worker_summary/T350_worker_summary.md` and append a T350 worker
record to `docs/07_handoff.md`.

Do not mark T350 complete in `docs/04_task_board.md`.

## Verification

Minimum command:

```powershell
git diff --check
```

## Reviewer Type

Adversarial product/safety UX and architecture review recommended.

Reviewer should block if the M24 scope introduces private chat ingestion,
provider calls, outbound messaging, platform delivery, persistence beyond local
review fixtures, automatic outreach, voice/avatar runtime, media generation, or
launch/user-study/compliance claims.

