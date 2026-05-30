# T330: Voice Technology Survey

## Task ID

T330

## Goal

Survey current voice technology routes for the companion-agent project and
recommend only authorized, non-real-person, clearly labeled options for future
M22 experiments.

## Why Now

M21 established text-first UX state contracts. The user goal includes eventual
voice/video-like companion behavior, but voice introduces biometric, consent,
deception, synthetic-media labeling, dependency, latency, and platform-policy
risk. M22 must start with research and boundaries before any runtime voice
feature.

## Allowed Files

Future T330 worker may create or modify only:

- `docs/research/voice_technology_survey.md`
- `docs/tasks/M22_voice_and_avatar_exploration/T331_voice_consent_data_model.md`
- `docs/worker_summary/T330_worker_summary.md`
- `docs/07_handoff.md`

If T330 needs code, tests, audio capture, TTS/ASR runtime, model-provider calls,
browser automation, private data processing, external account setup, platform
adapters, outbound messaging, or task-board edits, Captain must revise this
package before assignment.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not call model providers, synthesize audio, clone voices, capture
  microphone input, or process voice samples.
- Do not build UI, browser demo, avatar, or Live2D behavior.
- Do not call platform adapters or send messages.
- Do not claim legal advice, compliance completion, biometric compliance,
  synthetic-media compliance, app-store approval, launch approval, or regulator
  acceptance.
- Do not modify `docs/04_task_board.md`, `docs/05_decision_log.md`,
  `docs/06_eval_protocol.md`, or `docs/08_risks_and_open_questions.md`.

## Inputs To Read

Required:

- `docs/review/M21_review.md`
- `docs/compliance/china_compliance_checklist.md`
- `docs/compliance/international_privacy_platform_policy_checklist.md`
- `docs/compliance/aigc_labeling_plan.md`
- `docs/data_contracts/consent_center_contract.md`
- `docs/data_contracts/aigc_labeling_contract.md`
- `docs/data_contracts/crisis_dependency_policy_contract.md`
- `docs/product/text_first_user_study_protocol.md`

Optional:

- `docs/reference/gpt-pro关于后续从M13开始的计划分析.md`

## Expected Outputs

### 1. Voice Technology Survey

Create `docs/research/voice_technology_survey.md` with:

- access date and source confidence notes;
- ASR options;
- TTS options;
- voice-conversion/voice-cloning risks;
- non-real synthetic voice recommendation;
- latency and quality considerations;
- consent and labeling requirements;
- app-store/platform-policy risks;
- child/minor and dependency risks;
- blocked routes;
- recommendation for T331.

Use current official/primary sources where possible. This task may use web
research, but must not call voice providers or process audio.

### 2. Next Task Package

Create
`docs/tasks/M22_voice_and_avatar_exploration/T331_voice_consent_data_model.md`
for voice consent data model work.

### 3. Worker Summary And Handoff

Write `docs/worker_summary/T330_worker_summary.md` and append a T330 worker
record to `docs/07_handoff.md`.

Do not mark T330 complete in `docs/04_task_board.md`.

## Verification

Minimum command:

```powershell
git diff --check
```

## Reviewer Type

Adversarial voice/privacy/product-policy review recommended.

Reviewer should block if the survey recommends unauthorized voice cloning,
deceased-person voice simulation, biometric capture without consent, unlabeled
synthetic audio, or runtime voice implementation before consent and labeling
contracts.
