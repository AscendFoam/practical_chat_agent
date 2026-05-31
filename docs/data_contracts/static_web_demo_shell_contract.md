# Static Web Demo Shell Contract

Task: T342 Static Web Demo Shell
Status: worker draft for review

## Scope

The static web demo shell renders the synthetic `TextFirstWebDemoState` payload
from T341 in a local browser. It is a dependency-light UI shell for review. It
does not call model providers, read private data, generate media, enable
voice/avatar runtime, capture inputs, send messages, or integrate with
platforms.

Implemented files:

- `src/practical_chat_agent/ui/text_first_web_demo_static.py`
- `src/practical_chat_agent/ui/static/text_first_web_demo.html`
- `src/practical_chat_agent/ui/static/text_first_web_demo.css`
- `src/practical_chat_agent/ui/static/text_first_web_demo.js`

Implemented helper:

- `TextFirstWebDemoStaticShell`

## Asset Files

| File | Purpose |
| --- | --- |
| `text_first_web_demo.html` | Static document shell with app container, identity strip, tabs, and panels. |
| `text_first_web_demo.css` | Responsive, dependency-free visual styling. |
| `text_first_web_demo.js` | Local rendering logic and tab switching for synthetic state. |
| `text_first_web_demo_static.py` | Exposes asset paths and can embed adapter payload JSON into HTML. |

The static files use no external network assets.

## Payload Flow

`TextFirstWebDemoStaticShell.build_demo_payload_json(...)` calls
`TextFirstWebDemoAdapter.build_synthetic_demo_state(...)` and returns
JSON-serialized payload text.

`TextFirstWebDemoStaticShell.render_embedded_html(...)` reads the static HTML
file and replaces:

```text
window.TEXT_FIRST_WEB_DEMO_STATE = null;
```

with an adapter-generated payload assignment.

The committed HTML/JS also contains a synthetic fallback payload so the HTML
file can be opened locally for a basic static preview.

## UI Surfaces

The shell includes tabs and panels for:

- Chat;
- Persona;
- Memory;
- Life;
- Proactive;
- Controls;
- Voice / Avatar.

The visible shell includes:

- persistent AI-generated synthetic identity strip;
- chat memory explanations;
- blocked crisis state;
- persona labels and blocked clone state;
- imagined life-stream content;
- proactive review and blocked state;
- consent/AIGC labels;
- voice disabled/review/blocked states;
- avatar locked/research-only state.

## No-Runtime Boundaries

The shell must not contain:

- provider URLs;
- provider credentials;
- raw private text;
- transcripts;
- audio bytes;
- generated media paths;
- microphone or camera prompts;
- send/schedule/delivery/platform/webhook/queue fields;
- runtime voice or avatar controls.

Voice is displayed with `voice_enabled=false`. Avatar is displayed with
`avatar_enabled=false`.

## Local Preview

Preferred local preview:

- open `src/practical_chat_agent/ui/static/text_first_web_demo.html` directly,
  using the built-in synthetic fallback state.

If a browser blocks local file loading, serve only the static directory on
localhost with a temporary local static server and stop it after verification.

## Non-Actions

T342 does not implement:

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
python -m py_compile src\practical_chat_agent\ui\text_first_web_demo_static.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_text_first_web_demo_static.py tests\test_text_first_web_demo_adapter.py -q
```

```powershell
git diff --check
```

Browser verification should confirm:

- static page loads locally;
- seven tabs and seven panels exist;
- AI identity strip is visible;
- Voice / Avatar tab can be selected;
- voice and avatar remain not enabled;
- no layout overlap is visible at the tested viewport.
