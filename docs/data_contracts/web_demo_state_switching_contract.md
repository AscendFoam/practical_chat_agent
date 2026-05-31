# Web Demo State Switching Contract

Task: T343 Web Demo State Switching
Status: worker draft for review

## Scope

Web demo state switching adds local scenario controls to the static text-first
demo shell. It is browser-local UI behavior over synthetic payloads. It does
not mutate source data, call services, generate media, enable voice/avatar
runtime, send messages, or integrate with platforms.

Implemented surfaces:

- `#scenario-controls`
- `#scenario-status`
- scenario buttons in `text_first_web_demo.html`
- local switching logic in `text_first_web_demo.js`

## Scenario Vocabulary

Supported scenario ids:

- `safe-review`
- `blocked-persona`
- `crisis-chat`
- `dependency-proactive`
- `life-review`
- `controls-review`
- `voice-avatar-locked`

Each scenario maps to an existing static panel:

| Scenario | Panel |
| --- | --- |
| `safe-review` | Chat |
| `blocked-persona` | Persona |
| `crisis-chat` | Chat |
| `dependency-proactive` | Proactive |
| `life-review` | Life |
| `controls-review` | Controls |
| `voice-avatar-locked` | Voice / Avatar |

## Local Interaction Model

`text_first_web_demo.js` keeps a `baseState`, clones it with `cloneState(...)`,
and calls `setScenario(...)` for UI transitions. The source payload is not
mutated by scenario switching.

Scenario buttons update:

- active scenario button;
- scenario status text;
- active top-level panel;
- rendered panel content.

## Safety Invariants

- AI-generated synthetic identity remains visible.
- Persona clone blocked state remains visible.
- Crisis/dependency blocked states remain visible.
- Life-stream imagined/not-real-world content remains labeled.
- Voice remains `voice_enabled=false`.
- Avatar remains `avatar_enabled=false`.
- Scenario switching does not add external assets or service calls.
- Payloads and static assets contain no raw private text, transcripts, generated
  media paths, provider credentials, send queues, schedules, webhooks, platform
  delivery, or media-capture prompts.

## Non-Actions

T343 does not implement:

- production frontend app;
- model-provider calls;
- final reply generation;
- private chat-log reads;
- persistence;
- export/share/download writing;
- proactive candidate generation;
- automatic sending or scheduling;
- platform integration;
- TTS/ASR;
- voice/avatar/video runtime;
- Live2D behavior;
- legal, clinical, app-store, user-study, or launch approval.

## Verification

Expected minimum verification:

```powershell
$env:PYTHONPATH='src'
pytest tests\test_text_first_web_demo_state_switching.py tests\test_text_first_web_demo_static.py tests\test_text_first_web_demo_adapter.py -q
```

```powershell
git diff --check
```

Browser verification should confirm:

- the static page loads locally;
- scenario buttons are visible;
- Dependency scenario selects the Proactive panel;
- Voice / Avatar scenario selects the Voice / Avatar panel;
- AI identity remains visible after switching;
- voice/avatar remain not enabled;
- no layout overlap is visible at the tested viewport.
