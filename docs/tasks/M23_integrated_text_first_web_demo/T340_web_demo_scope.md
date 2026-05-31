# T340: Text-First Web Demo Scope

## Task ID

T340

## Goal

Define the scope, routes, fixtures, safety gates, and implementation sequence
for an integrated text-first web demo that stitches the existing local
companion contracts into one usable prototype.

## Why Now

M21 produced text-first UX state contracts and M22 bounded voice/avatar risk.
The project now needs a usable local demo so the companion experience can be
evaluated as a product, while voice/avatar runtime, outbound sending, provider
calls, and private data processing remain blocked.

## Allowed Files

Future T340 worker may create or modify only:

- `docs/product/text_first_web_demo_scope.md`
- `docs/tasks/M23_integrated_text_first_web_demo/T341_web_demo_state_adapter.md`
- `docs/worker_summary/T340_worker_summary.md`
- `docs/07_handoff.md`

If T340 needs code, tests, frontend implementation, browser automation,
model-provider calls, voice/avatar runtime, media generation, private data
processing, task-board edits, platform adapters, or outbound messaging, Captain
must revise this package before assignment.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not call model providers.
- Do not synthesize audio, generate images/video, clone voices/faces, capture
  microphone/camera input, or process media samples.
- Do not implement UI or start a dev server in T340.
- Do not add platform delivery, push notification, send, schedule, queue,
  webhook, token, adapter, or realtime fields.
- Do not modify `docs/04_task_board.md`.
- Do not claim legal advice, compliance completion, app-store approval, launch
  approval, user-study validation, or regulator acceptance.

## Inputs To Read

Required:

- `docs/review/M21_review.md`
- `docs/review/M22_review.md`
- `docs/product/text_first_ux_information_architecture.md`
- `docs/product/text_first_user_study_protocol.md`
- `docs/data_contracts/text_first_onboarding_contract.md`
- `docs/data_contracts/text_first_chat_memory_contract.md`
- `docs/data_contracts/text_first_life_stream_contract.md`
- `docs/data_contracts/text_first_proactive_settings_contract.md`
- `docs/data_contracts/consent_center_contract.md`
- `docs/data_contracts/aigc_labeling_contract.md`
- `docs/data_contracts/crisis_dependency_policy_contract.md`
- `docs/data_contracts/voice_consent_contract.md`

## Expected Outputs

### 1. Web Demo Scope

Create `docs/product/text_first_web_demo_scope.md` with:

- target user experience;
- surfaces and routes;
- synthetic fixture strategy;
- state-contract integration map;
- explicit blocked features;
- accessibility and responsive-layout expectations;
- design-system and visual posture;
- safety and consent gates;
- local-only run assumption;
- implementation sequence for T341 and later tasks.

T340 should select a conservative implementation direction. Current repository
state favors a dependency-light local static web demo or small Python-served
prototype over adding a large frontend framework before the UX contract is
validated.

### 2. Next Task Package

Create
`docs/tasks/M23_integrated_text_first_web_demo/T341_web_demo_state_adapter.md`
for a local state adapter that prepares synthetic demo payloads from existing
Python state contracts. T341 may include code and tests if scoped explicitly.

### 3. Worker Summary And Handoff

Write `docs/worker_summary/T340_worker_summary.md` and append a T340 worker
record to `docs/07_handoff.md`.

Do not mark T340 complete in `docs/04_task_board.md`.

## Verification

Minimum command:

```powershell
git diff --check
```

## Reviewer Type

Adversarial product/safety UX review recommended.

Reviewer should block if T340 scopes voice/avatar runtime, provider calls,
private data processing, outbound sending, unlabeled generated content,
real-person clone support, or launch-readiness claims into the web demo.
