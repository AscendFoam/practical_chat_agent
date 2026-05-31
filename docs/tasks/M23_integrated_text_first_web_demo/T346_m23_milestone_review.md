# T346: M23 Milestone Review

## Task ID

T346

## Goal

Review M23 end to end and decide whether the integrated text-first web demo is
safe and coherent enough to enter the next milestone.

## Why Now

T340 scoped the web demo, T341 created the state adapter, T342 built the static
shell, T343 added scenario switching, T344 ran visual QA, and T345 added the
walkthrough and supervised-review protocol. M23 now needs a milestone review
that consolidates implementation evidence, boundaries, residual risks, and the
recommended next milestone.

## Allowed Files

Future T346 worker may create or modify only:

- `docs/review/M23_review.md`
- `docs/tasks/M24_demo_hardening_and_local_backend/T350_m24_scope.md`
- `docs/worker_summary/T346_worker_summary.md`
- `docs/07_handoff.md`

If T346 needs code changes, tests, browser reruns, model-provider calls,
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
- Do not modify `docs/04_task_board.md`.
- Do not claim legal advice, compliance completion, app-store approval, launch
  approval, user-study validation, regulator acceptance, or real user evidence.

## Inputs To Read

Required:

- `docs/product/text_first_web_demo_scope.md`
- `docs/data_contracts/text_first_web_demo_state_contract.md`
- `docs/data_contracts/static_web_demo_shell_contract.md`
- `docs/data_contracts/web_demo_state_switching_contract.md`
- `docs/qa/web_demo_visual_qa.md`
- `docs/product/text_first_web_demo_walkthrough.md`
- `docs/research/text_first_web_demo_study_protocol_update.md`
- `docs/worker_summary/T340_worker_summary.md`
- `docs/worker_summary/T341_worker_summary.md`
- `docs/worker_summary/T342_worker_summary.md`
- `docs/worker_summary/T343_worker_summary.md`
- `docs/worker_summary/T344_worker_summary.md`
- `docs/worker_summary/T345_worker_summary.md`

Optional:

- `docs/review/M21_review.md`
- `docs/review/M22_review.md`

## Expected Outputs

### 1. Milestone Review

Create `docs/review/M23_review.md` with:

- gate recommendation;
- task coverage table for T340 through T345;
- implemented code and static assets;
- product, research, QA, and data-contract artifacts;
- browser QA evidence summary;
- safety boundary assessment;
- explicit non-actions;
- residual risks;
- recommendation for M24.

### 2. Next Milestone Scope

Create
`docs/tasks/M24_demo_hardening_and_local_backend/T350_m24_scope.md`
for the next milestone. The proposed M24 scope should stay local and
review-first, focusing on demo hardening, local backend serving, accessibility,
friendly labels, and generated-payload wiring. It must not introduce real
private chat ingestion, platform delivery, model providers, voice/avatar
runtime, or automatic outreach.

### 3. Worker Summary And Handoff

Write `docs/worker_summary/T346_worker_summary.md` and append a T346 worker
record to `docs/07_handoff.md`.

Do not mark T346 complete in `docs/04_task_board.md`.

## Verification

Minimum command:

```powershell
git diff --check
```

## Reviewer Type

Adversarial product/safety UX, frontend, and architecture review recommended.

Reviewer should block if M23 review claims launch readiness, hides residual
risks, ignores missing accessibility/workflow gaps, treats the walkthrough as a
completed user study, or recommends enabling private data, model providers,
automatic outreach, platform delivery, voice runtime, avatar runtime, or media
generation before a scoped follow-up task.

