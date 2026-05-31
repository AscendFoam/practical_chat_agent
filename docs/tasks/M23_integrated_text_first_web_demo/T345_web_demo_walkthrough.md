# T345: Web Demo Walkthrough

## Task ID

T345

## Goal

Create a user-facing walkthrough and lightweight study protocol update for the
static text-first web demo, so reviewers can run a consistent supervised demo
without implying production readiness or user-study validation.

## Why Now

T342 created the static shell, T343 added scenario switching, and T344 verified
desktop/mobile visual layout. The next step is to make the demo understandable
to human reviewers and define what observations should be captured before M23
closes.

## Allowed Files

Future T345 worker may create or modify only:

- `docs/product/text_first_web_demo_walkthrough.md`
- `docs/research/text_first_web_demo_study_protocol_update.md`
- `docs/tasks/M23_integrated_text_first_web_demo/T346_m23_milestone_review.md`
- `docs/worker_summary/T345_worker_summary.md`
- `docs/07_handoff.md`

If T345 needs frontend code changes, tests, model-provider calls, generated
media, voice/avatar runtime, private data processing, task-board edits,
platform adapters, outbound messaging, screenshot artifacts, or launch claims,
Captain must revise this package before assignment.

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
- `docs/data_contracts/static_web_demo_shell_contract.md`
- `docs/data_contracts/web_demo_state_switching_contract.md`
- `docs/qa/web_demo_visual_qa.md`
- `src/practical_chat_agent/ui/static/text_first_web_demo.html`
- `src/practical_chat_agent/ui/static/text_first_web_demo.js`

Optional:

- `docs/review/M22_review.md`
- `docs/review/M21_review.md`

## Expected Outputs

### 1. Product Walkthrough

Create `docs/product/text_first_web_demo_walkthrough.md` with:

- reviewer audience and demo purpose;
- local setup path/URL assumptions;
- a guided route through all seven scenarios;
- what the facilitator should say about AI identity and synthetic content;
- what the facilitator should not claim;
- expected reviewer observations for persona, memory, life stream, proactive,
  controls, and locked voice/avatar states;
- issue logging format.

### 2. Study Protocol Update

Create `docs/research/text_first_web_demo_study_protocol_update.md` with:

- internal supervised-review protocol;
- participant/reviewer assumptions;
- consent/debrief wording as product copy, not legal advice;
- observation checklist;
- stop conditions;
- residual risks and excluded validations;
- how findings should feed future task packages.

### 3. Next Task Package

Create
`docs/tasks/M23_integrated_text_first_web_demo/T346_m23_milestone_review.md`
for M23 milestone review.

### 4. Worker Summary And Handoff

Write `docs/worker_summary/T345_worker_summary.md` and append a T345 worker
record to `docs/07_handoff.md`.

Do not mark T345 complete in `docs/04_task_board.md`.

## Verification

Minimum command:

```powershell
git diff --check
```

Browser verification is not required for T345 unless the task package is revised
to allow UI changes.

## Reviewer Type

Adversarial product/safety UX and research-methods review recommended.

Reviewer should block if the walkthrough hides the AI/synthetic nature of the
demo, presents voice/avatar as enabled, implies automatic outreach, claims
validation or compliance, or asks reviewers to use private personal chat data.

