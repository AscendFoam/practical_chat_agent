# T334: M22 Milestone Review

## Task ID

T334

## Goal

Review M22 voice and avatar exploration outputs and decide whether the project
can proceed to a text-first web demo milestone while keeping voice/avatar
runtime blocked.

## Why Now

M22 has produced voice route research, a voice consent data model, a synthetic
benchmark plan, and avatar interaction research. Before moving to a usable
prototype milestone, the project needs an adversarial milestone review that
checks whether M22 preserved consent, labeling, anti-impersonation, privacy,
minor, crisis/dependency, and no-runtime boundaries.

## Allowed Files

Future T334 worker may create or modify only:

- `docs/review/M22_review.md`
- `docs/tasks/M23_integrated_text_first_web_demo/T340_web_demo_scope.md`
- `docs/worker_summary/T334_worker_summary.md`
- `docs/07_handoff.md`

If T334 needs code, tests, UI, browser automation, model-provider calls,
voice/avatar runtime, media generation, private data processing, task-board
edits, platform adapters, or outbound messaging, Captain must revise this
package before assignment.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not call model providers, synthesize audio, generate images/video, clone
  voices/faces, capture microphone/camera input, or process media samples.
- Do not build UI, browser demo, avatar runtime, Live2D behavior, playback, or
  recording controls.
- Do not add platform delivery, push notification, send, schedule, queue,
  webhook, token, adapter, or realtime fields.
- Do not modify `docs/04_task_board.md`.
- Do not claim legal advice, biometric compliance, synthetic-media compliance,
  app-store approval, launch approval, or regulator acceptance.

## Inputs To Read

Required:

- `docs/research/voice_technology_survey.md`
- `docs/data_contracts/voice_consent_contract.md`
- `docs/research/asr_tts_latency_benchmark_plan.md`
- `docs/research/avatar_interaction_survey.md`
- `docs/data_contracts/aigc_labeling_contract.md`
- `docs/data_contracts/consent_center_contract.md`
- `docs/data_contracts/crisis_dependency_policy_contract.md`
- `docs/review/M21_review.md`

## Expected Outputs

### 1. M22 Review

Create `docs/review/M22_review.md` with:

- task coverage table;
- implemented code and docs summary;
- verification evidence;
- safety boundary assessment;
- explicit non-actions;
- residual risks;
- gate recommendation: `PASS`, `PASS_WITH_WARNINGS`, or `BLOCK`;
- recommendation for M23.

The review should be adversarial. It should block if M22 added runtime voice,
runtime avatar, provider calls, media generation, private data processing,
unlabeled synthetic media, real-person clone routes, camera/microphone capture,
or platform delivery.

### 2. Next Task Package

Create
`docs/tasks/M23_integrated_text_first_web_demo/T340_web_demo_scope.md` for a
text-first web demo milestone. T340 should scope the next milestone around
integrating existing local contracts into a transparent UI, not voice/avatar
runtime.

### 3. Worker Summary And Handoff

Write `docs/worker_summary/T334_worker_summary.md` and append a T334 worker
record to `docs/07_handoff.md`.

Do not mark T334 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'
pytest tests\test_voice_consent_data_model.py tests\test_consent_center_data_model.py tests\test_aigc_labeling_plan_contract.py tests\test_crisis_dependency_policy.py -q -o cache_dir=artifacts\t334_pytest_cache --basetemp=artifacts\t334_pytest_basetemp
```

```powershell
git diff --check
```

## Reviewer Type

Adversarial milestone review recommended.

Reviewer should mark `BLOCK` if the M22 record implies launch readiness,
voice/avatar runtime readiness, legal sufficiency, app-store approval,
real-person clone support, camera/microphone capture, or unlabeled synthetic
media support.
