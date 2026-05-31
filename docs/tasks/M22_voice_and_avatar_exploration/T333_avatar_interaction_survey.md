# T333: Avatar Interaction Survey

## Task ID

T333

## Goal

Survey avatar, Live2D-like, and lightweight video-presence interaction routes
for the companion-agent project, then recommend only transparent,
non-real-person, clearly labeled options for future experiments.

## Why Now

T330 surveyed voice technology, T331 added voice consent contracts, and T332
defined a synthetic-only benchmark plan. The user goal includes video-like or
Live2D-style interaction, but avatar features add face/likeness, deception,
dependency, child-safety, platform-policy, and synthetic-media labeling risk.
M22 should research boundaries before any avatar runtime.

## Allowed Files

Future T333 worker may create or modify only:

- `docs/research/avatar_interaction_survey.md`
- `docs/tasks/M22_voice_and_avatar_exploration/T334_m22_milestone_review.md`
- `docs/worker_summary/T333_worker_summary.md`
- `docs/07_handoff.md`

If T333 needs code, tests, generated images/video, face capture, camera input,
avatar runtime, Live2D runtime, browser automation, UI, model-provider calls,
private data processing, task-board edits, platform adapters, or outbound
messaging, Captain must revise this package before assignment.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not call model providers, generate images/video, clone faces, animate
  avatars, capture camera input, or process biometric samples.
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
- `docs/research/asr_tts_latency_benchmark_plan.md`
- `docs/data_contracts/voice_consent_contract.md`
- `docs/data_contracts/aigc_labeling_contract.md`
- `docs/data_contracts/consent_center_contract.md`
- `docs/data_contracts/crisis_dependency_policy_contract.md`
- `docs/compliance/aigc_labeling_plan.md`
- `docs/compliance/international_privacy_platform_policy_checklist.md`
- `docs/compliance/china_compliance_checklist.md`

## Expected Outputs

### 1. Avatar Interaction Survey

Create `docs/research/avatar_interaction_survey.md` with:

- access date and source confidence notes if web research is used;
- avatar route taxonomy;
- Live2D / 2D sprite / 3D avatar / generated video route comparison;
- face cloning and real-person likeness risks;
- labeling and consent requirements;
- dependency and minor risks;
- UI safety posture for a future text-first demo;
- blocked routes;
- recommendation for T334 milestone review.

Use current official/primary sources where possible. This task may use web
research, but must not call avatar providers or generate/process media.

### 2. Next Task Package

Create `docs/tasks/M22_voice_and_avatar_exploration/T334_m22_milestone_review.md`
for M22 milestone review.

### 3. Worker Summary And Handoff

Write `docs/worker_summary/T333_worker_summary.md` and append a T333 worker
record to `docs/07_handoff.md`.

Do not mark T333 complete in `docs/04_task_board.md`.

## Verification

Minimum command:

```powershell
git diff --check
```

## Reviewer Type

Adversarial avatar/privacy/product-policy review recommended.

Reviewer should block if T333 recommends real-person face clones, camera capture
without consent, unlabeled synthetic video/avatar output, avatar runtime before
consent/labeling review, minor-facing intimate avatars, or platform delivery
behavior.
