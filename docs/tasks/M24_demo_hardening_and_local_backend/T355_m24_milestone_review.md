# T355: M24 Milestone Review

## Task ID

T355

## Goal

Review M24 end to end and decide whether the local text-first demo is ready to
enter the next milestone for memory/persona growth and distillation planning.

## Why Now

T350 scoped M24, T351 added the local server helper, T352 defined friendly
labels and accessibility requirements, T353 hardened the static UI, and T354
ran Browser QA for the local run path. M24 now needs a milestone review and a
safe next-scope package.

## Allowed Files

Future T355 worker may create or modify only:

- `docs/review/M24_review.md`
- `docs/tasks/M25_memory_persona_growth/T360_m25_scope.md`
- `docs/worker_summary/T355_worker_summary.md`
- `docs/07_handoff.md`

If T355 needs code changes, tests, browser reruns, model-provider calls,
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

- `docs/product/m24_demo_hardening_scope.md`
- `docs/data_contracts/local_web_demo_server_contract.md`
- `docs/product/web_demo_friendly_labels_accessibility.md`
- `docs/data_contracts/web_demo_display_accessibility_contract.md`
- `docs/qa/local_run_browser_qa.md`
- `docs/worker_summary/T350_worker_summary.md`
- `docs/worker_summary/T351_worker_summary.md`
- `docs/worker_summary/T352_worker_summary.md`
- `docs/worker_summary/T353_worker_summary.md`
- `docs/worker_summary/T354_worker_summary.md`

Optional:

- `docs/review/M23_review.md`
- `docs/review/M22_review.md`
- `docs/review/M21_review.md`

## Expected Outputs

### 1. Milestone Review

Create `docs/review/M24_review.md` with:

- gate recommendation;
- task coverage table for T350 through T354;
- implemented code and tests;
- product, data-contract, QA, and worker-summary artifacts;
- Browser QA evidence summary;
- safety boundary assessment;
- explicit non-actions;
- residual risks;
- recommendation for M25.

### 2. Next Milestone Scope

Create `docs/tasks/M25_memory_persona_growth/T360_m25_scope.md` for memory,
persona growth, and distillation planning. The scope should stay local,
synthetic, and review-first unless later task packages explicitly allow private
data handling. It should not introduce provider calls, private chat ingestion,
automatic outreach, platform delivery, voice/avatar runtime, or real-person
recreation support.

### 3. Worker Summary And Handoff

Write `docs/worker_summary/T355_worker_summary.md` and append a T355 worker
record to `docs/07_handoff.md`.

Do not mark T355 complete in `docs/04_task_board.md`.

## Verification

Minimum command:

```powershell
git diff --check
```

## Reviewer Type

Adversarial product/safety UX, accessibility, frontend, and architecture review
recommended.

Reviewer should block if M24 review hides Browser QA risks, treats automated
QA as completed accessibility validation, claims launch readiness, or recommends
private data ingestion, real-person recreation, model-provider calls,
automatic outreach, platform delivery, voice/avatar runtime, or media
generation before a scoped follow-up task.

