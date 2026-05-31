# T332: ASR/TTS Latency Benchmark Plan

## Task ID

T332

## Goal

Design a synthetic-fixture-only ASR/TTS latency benchmark plan that future voice
experiments can use after consent and labeling contracts are reviewed.

## Why Now

T330 surveyed voice technology routes and T331 adds local voice consent data
models. Before any provider call, microphone capture, or generated audio,
M22 needs a benchmark plan that defines what latency and quality would mean
without creating runtime voice behavior.

## Allowed Files

Future T332 worker may create or modify only:

- `docs/research/asr_tts_latency_benchmark_plan.md`
- `docs/tasks/M22_voice_and_avatar_exploration/T333_avatar_interaction_survey.md`
- `docs/worker_summary/T332_worker_summary.md`
- `docs/07_handoff.md`

If T332 needs code, tests, provider calls, generated audio, audio fixtures,
microphone input, ASR/TTS runtime, browser automation, UI, avatar/Live2D code,
private data processing, task-board edits, platform adapters, or outbound
messaging, Captain must revise this package before assignment.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not call model providers, synthesize audio, clone voices, convert voices,
  capture microphone input, upload audio, or process voice samples.
- Do not create audio fixtures or generated audio files.
- Do not implement benchmark code.
- Do not build UI, browser demo, avatar, Live2D behavior, playback controls, or
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
- `docs/data_contracts/aigc_labeling_contract.md`
- `docs/data_contracts/consent_center_contract.md`
- `docs/data_contracts/crisis_dependency_policy_contract.md`

## Expected Outputs

### 1. Benchmark Plan

Create `docs/research/asr_tts_latency_benchmark_plan.md` with:

- benchmark scope and non-actions;
- synthetic text fixture categories only;
- ASR metric definitions for a later approved task;
- TTS metric definitions for a later approved task;
- conversational latency target bands;
- quality and safety evaluation notes;
- consent, logging, retention, and labeling prerequisites;
- provider comparison dimensions without selecting a provider;
- clear block on provider calls and audio processing in T332.

### 2. Next Task Package

Create
`docs/tasks/M22_voice_and_avatar_exploration/T333_avatar_interaction_survey.md`
for avatar/Live2D interaction research. T333 should remain docs-only unless
Captain explicitly allows implementation.

### 3. Worker Summary And Handoff

Write `docs/worker_summary/T332_worker_summary.md` and append a T332 worker
record to `docs/07_handoff.md`.

Do not mark T332 complete in `docs/04_task_board.md`.

## Verification

Minimum command:

```powershell
git diff --check
```

## Reviewer Type

Adversarial voice/privacy/product-policy review recommended.

Reviewer should block if T332 adds provider calls, audio files, benchmark code,
microphone capture, voice cloning, unlabeled generated audio, private data
processing, runtime voice, or platform delivery behavior.
