# T414: Trust Commercial Positioning Panel

## Task ID

T414

## Goal

Add a dedicated trust and commercial positioning panel to the local web demo.

T414 should turn the commercial positioning from T413 into a clearer review
surface: pricing hypotheses, trust controls, unacceptable monetization patterns,
and product readiness gaps. The panel must stay synthetic, local, and
review-oriented.

## Allowed Files

Future T414 worker may create or modify only:

- `src/practical_chat_agent/ui/text_first_web_demo_adapter.py`
- `src/practical_chat_agent/ui/static/text_first_web_demo.html`
- `src/practical_chat_agent/ui/static/text_first_web_demo.js`
- `src/practical_chat_agent/ui/static/text_first_web_demo.css`
- `tests/test_trust_commercial_positioning_panel.py`
- `docs/data_contracts/trust_commercial_positioning_panel_contract.md`
- `docs/tasks/M34_integrated_companion_demo/T415_integrated_demo_responsive_hardening.md`
- `docs/worker_summary/T414_worker_summary.md`
- `docs/07_handoff.md`

If T414 needs private data, source readers, model-provider calls, package
changes, external system adapters, outbound messaging, voice/avatar runtime,
media generation, automatic apply triggers, PersonaVersionStore writes, or
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
  delivery state, or external-system persistence behavior.
- Do not implement automatic outreach, sending, scheduling, notifications,
  external delivery, microphone, camera, ASR, TTS, voice cloning,
  voice/avatar likeness, Live2D, generated audio, generated image, generated
  video, or media capture.
- Do not modify `docs/04_task_board.md`.

## Expected Outputs

### 1. Payload

Add a server-safe trust/commercial payload with:

- pricing hypotheses;
- value pillars;
- trust controls;
- unacceptable monetization patterns;
- readiness gaps;
- safety notes.

### 2. Static UI

Add a panel or section that renders the trust/commercial payload. It should
remain compact and operational, not a landing page.

### 3. Tests

Create `tests/test_trust_commercial_positioning_panel.py` proving:

- payload contains trust and commercial positioning;
- unacceptable monetization patterns are explicit;
- panel hooks are present in HTML/JS/CSS;
- static and served payloads contain no forbidden private/provider/outbound or
  media fields.

### 4. Data Contract

Create `docs/data_contracts/trust_commercial_positioning_panel_contract.md`.

### 5. Next Task Package

Create
`docs/tasks/M34_integrated_companion_demo/T415_integrated_demo_responsive_hardening.md`.

### 6. Worker Summary And Handoff

Write `docs/worker_summary/T414_worker_summary.md` and append a T414 worker
record to `docs/07_handoff.md`.

Do not mark T414 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\ui\text_first_web_demo_adapter.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_trust_commercial_positioning_panel.py tests\test_integrated_demo_scenario_spine.py tests\test_text_first_web_demo_static.py tests\test_text_first_web_demo_local_server.py -q
```

```powershell
git diff --check
```

Use project-local pytest cache and basetemp paths if the default user temp
directory is not writable.

## Browser QA

After tests pass, use the in-app Browser through a localhost preview to verify
that the trust/commercial panel is visible, readable, and does not expose
forbidden action controls.

## Reviewer Type

Adversarial product-commercial review for trust framing, monetization safety,
local-only boundaries, and no provider/outbound/media surface expansion.
