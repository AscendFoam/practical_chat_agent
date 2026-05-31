# T413: Integrated Demo Scenario Spine

## Task ID

T413

## Goal

Add an integrated scenario spine to the local text-first web demo.

T413 should add a server-safe `integrated_scenario` payload and a static UI
surface that lets reviewers understand how persona customization, memory,
review controls, proactive settings, life stream, voice/avatar locked states,
and commercial positioning fit together.

## Allowed Files

Future T413 worker may create or modify only:

- `src/practical_chat_agent/ui/text_first_web_demo_adapter.py`
- `src/practical_chat_agent/ui/static/text_first_web_demo.html`
- `src/practical_chat_agent/ui/static/text_first_web_demo.js`
- `src/practical_chat_agent/ui/static/text_first_web_demo.css`
- `tests/test_integrated_demo_scenario_spine.py`
- `docs/data_contracts/integrated_demo_scenario_spine_contract.md`
- `docs/tasks/M34_integrated_companion_demo/T414_trust_commercial_positioning_panel.md`
- `docs/worker_summary/T413_worker_summary.md`
- `docs/07_handoff.md`

If T413 needs private data, source readers, model-provider calls, package
changes, platform adapters, outbound messaging, voice/avatar runtime, media
generation, automatic apply triggers, PersonaVersionStore writes, or
MemoryEventStore writes, Captain must revise this package before assignment.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not ingest, summarize, transform, quote, or commit real private chat
  records.
- Do not call model providers.
- Do not implement source readers, extraction from real logs, embeddings,
  vector search, semantic ranking, fine-tuning, similarity scoring, persona
  synthesis, final companion reply generation, or runtime mutation.
- Do not write PersonaVersionStore or MemoryEventStore.
- Do not add schedulers, queues, webhooks, auth, tokens, recipient ids,
  delivery state, or platform persistence behavior.
- Do not implement automatic outreach, sending, scheduling, notifications,
  platform delivery, microphone, camera, ASR, TTS, voice cloning,
  voice/avatar likeness, Live2D, generated audio, generated image, generated
  video, or media capture.
- Do not modify `docs/04_task_board.md`.

## Expected Outputs

### 1. Payload

Add `integrated_scenario` to `TextFirstWebDemoState` and synthetic demo output.

The payload should include:

- scenario title;
- persona promise;
- memory promise;
- review promise;
- proactive promise;
- life stream promise;
- voice/avatar boundary;
- commercial positioning;
- readiness summary;
- ordered scenario steps.

### 2. Static UI

Update the static demo to display the integrated scenario spine. The UI should:

- be visible from the first screen or scenario controls;
- remain work-focused and not a marketing landing page;
- link each scenario step to existing surfaces by label or section key;
- keep text compact enough for desktop and mobile;
- avoid adding action controls for sending, scheduling, platform delivery, or
  media generation.

### 3. Tests

Create `tests/test_integrated_demo_scenario_spine.py` proving:

- adapter state includes `integrated_scenario`;
- all scenario steps have safe labels, section keys, and summaries;
- commercial positioning excludes dependency-pressure and impersonation claims;
- static HTML/JS/CSS contain the expected rendering hooks;
- served payload/static assets contain no private/provider/outbound/media
  fields.

### 4. Data Contract

Create `docs/data_contracts/integrated_demo_scenario_spine_contract.md`.

### 5. Next Task Package

Create
`docs/tasks/M34_integrated_companion_demo/T414_trust_commercial_positioning_panel.md`.

### 6. Worker Summary And Handoff

Write `docs/worker_summary/T413_worker_summary.md` and append a T413 worker
record to `docs/07_handoff.md`.

Do not mark T413 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\ui\text_first_web_demo_adapter.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_integrated_demo_scenario_spine.py tests\test_text_first_web_demo_static.py tests\test_text_first_web_demo_local_server.py -q
```

```powershell
git diff --check
```

Use project-local pytest cache and basetemp paths if the default user temp
directory is not writable.

## Browser QA

After tests pass, use the in-app Browser through a localhost preview to verify:

- the integrated scenario spine is visible;
- scenario text fits without overlap on the tested viewport;
- the page still renders the existing review workspace and voice/avatar locked
  states;
- no send/schedule/provider/platform/media controls appear.

## Reviewer Type

Adversarial product-demo review for coherence, safe commercialization framing,
local-only boundaries, responsive static UI, and no platform/provider/media
surface expansion.
