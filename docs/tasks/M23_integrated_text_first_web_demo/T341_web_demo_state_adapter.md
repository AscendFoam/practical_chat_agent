# T341: Web Demo State Adapter

## Task ID

T341

## Goal

Create a local Python state adapter that assembles synthetic demo payloads from
the existing text-first companion contracts for a future static web demo.

## Why Now

T340 scoped M23 around a dependency-light text-first web demo. Before building
frontend UI, the project needs a single serializable demo state that stitches
onboarding, persona, chat/memory, life stream, proactive settings, consent,
AIGC labels, safety decisions, and voice/avatar locked states together without
model calls or private data.

## Allowed Files

Future T341 worker may create or modify only:

- `src/practical_chat_agent/ui/text_first_web_demo_adapter.py`
- `tests/test_text_first_web_demo_adapter.py`
- `docs/data_contracts/text_first_web_demo_state_contract.md`
- `docs/tasks/M23_integrated_text_first_web_demo/T342_static_web_demo_shell.md`
- `docs/worker_summary/T341_worker_summary.md`
- `docs/07_handoff.md`

If T341 needs frontend implementation, browser automation, model-provider
calls, voice/avatar runtime, media generation, private data processing,
task-board edits, platform adapters, or outbound messaging, Captain must revise
this package before assignment.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not call model providers.
- Do not synthesize audio, generate images/video, clone voices/faces, capture
  microphone/camera input, or process media samples.
- Do not build frontend UI or start a dev server in T341.
- Do not add platform delivery, push notification, send, schedule, queue,
  webhook, token, adapter, or realtime fields.
- Do not modify `docs/04_task_board.md`.
- Do not claim legal advice, compliance completion, app-store approval, launch
  approval, user-study validation, or regulator acceptance.

## Inputs To Read

Required:

- `docs/product/text_first_web_demo_scope.md`
- `src/practical_chat_agent/ui/text_first_onboarding.py`
- `src/practical_chat_agent/ui/text_first_chat_memory.py`
- `src/practical_chat_agent/ui/text_first_life_stream.py`
- `src/practical_chat_agent/ui/text_first_proactive_settings.py`
- `src/practical_chat_agent/core/models.py`
- `src/practical_chat_agent/services/companion_safety_policy.py`
- `docs/data_contracts/voice_consent_contract.md`

## Expected Outputs

### 1. Tests First

Create `tests/test_text_first_web_demo_adapter.py` before implementation.

Minimum test coverage:

- adapter returns one serializable state for the demo;
- state includes onboarding, persona, chat_memory, life_stream, proactive,
  controls, voice, and avatar sections;
- all sections include AI/synthetic or review-required labels where expected;
- blocked real-person clone scenario is represented;
- crisis/dependency blocked scenario is represented;
- voice is disabled or review-required, never runtime-enabled;
- avatar is locked/research-only, never runtime-enabled;
- payload contains no raw private text, audio bytes, transcripts, generated
  media paths, provider tokens, send/schedule/delivery/platform/webhook/queue
  fields, or runtime methods.

### 2. Adapter Code

Create `src/practical_chat_agent/ui/text_first_web_demo_adapter.py`.

Recommended objects:

- `TextFirstWebDemoState`
- `TextFirstWebDemoAdapter`

The adapter should use existing model/prototype classes where practical rather
than duplicating their logic. It should emit JSON-serializable Pydantic models
or dictionaries suitable for a static web shell.

### 3. Contract

Create `docs/data_contracts/text_first_web_demo_state_contract.md` explaining:

- demo state schema;
- section mapping;
- fixture assumptions;
- safety gates;
- blocked fields and non-actions;
- verification commands.

### 4. Next Task Package

Create
`docs/tasks/M23_integrated_text_first_web_demo/T342_static_web_demo_shell.md`
for building the static web UI shell that consumes the adapter payload.

### 5. Worker Summary And Handoff

Write `docs/worker_summary/T341_worker_summary.md` and append a T341 worker
record to `docs/07_handoff.md`.

Do not mark T341 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\ui\text_first_web_demo_adapter.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_text_first_web_demo_adapter.py tests\test_text_first_onboarding_prototype.py tests\test_text_first_chat_memory_prototype.py tests\test_text_first_life_stream_prototype.py tests\test_text_first_proactive_settings_prototype.py tests\test_voice_consent_data_model.py -q -o cache_dir=artifacts\t341_pytest_cache --basetemp=artifacts\t341_pytest_basetemp
```

```powershell
git diff --check
```

## Reviewer Type

Adversarial product/safety UX review recommended.

Reviewer should block if T341 duplicates contracts incorrectly, hides labels,
adds model/provider calls, reads private data, enables voice/avatar runtime,
introduces outbound fields, or makes launch-readiness claims.
