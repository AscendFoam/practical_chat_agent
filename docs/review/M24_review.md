# M24 Review: Demo Hardening And Local Backend

## Status

Gate recommendation: PASS_WITH_WARNINGS for entering M25 memory, persona
growth, and distillation planning.

M24 made the M23 text-first demo easier to run and review locally. It added a
dependency-free local server helper, defined friendly labels and accessibility
requirements, hardened the static UI, and ran Browser QA on the local run path.
It did not implement production serving, private chat ingestion, real-person
distillation, model-provider calls, automatic outreach, platform delivery,
voice/avatar runtime, media generation, external user research, or launch
readiness.

## Task Coverage

| Task | Result | Evidence |
| --- | --- | --- |
| T350 M24 scope | Implemented | `docs/product/m24_demo_hardening_scope.md`. |
| T351 Local demo server | Implemented | `TextFirstWebDemoLocalServer`, local route tests, server contract. |
| T352 Friendly labels and accessibility contract | Implemented | Product label plan and display/accessibility contract. |
| T353 Keyboard responsive UI hardening | Implemented | Static UI updates and accessibility tests. |
| T354 Local run Browser QA | Implemented | `docs/qa/local_run_browser_qa.md`. |

## Implemented Code And Static Assets

- `src/practical_chat_agent/ui/text_first_web_demo_local_server.py`
  - `LocalDemoResponse`
  - `TextFirstWebDemoLocalServer`
  - `build_http_server(...)`
- `src/practical_chat_agent/ui/static/text_first_web_demo.html`
- `src/practical_chat_agent/ui/static/text_first_web_demo.css`
- `src/practical_chat_agent/ui/static/text_first_web_demo.js`

## Tests Added Or Expanded

- `tests/test_text_first_web_demo_local_server.py`
- `tests/test_text_first_web_demo_accessibility.py`

M24 also kept these M23 tests in the verification set:

- `tests/test_text_first_web_demo_static.py`
- `tests/test_text_first_web_demo_state_switching.py`
- `tests/test_text_first_web_demo_adapter.py`

## Product, Data-Contract, QA, And Task Artifacts

Product:

- `docs/product/m24_demo_hardening_scope.md`
- `docs/product/web_demo_friendly_labels_accessibility.md`

Data contracts:

- `docs/data_contracts/local_web_demo_server_contract.md`
- `docs/data_contracts/web_demo_display_accessibility_contract.md`

QA:

- `docs/qa/local_run_browser_qa.md`

Task packages:

- `docs/tasks/M24_demo_hardening_and_local_backend/T351_local_demo_server.md`
- `docs/tasks/M24_demo_hardening_and_local_backend/T352_friendly_labels_accessibility_contract.md`
- `docs/tasks/M24_demo_hardening_and_local_backend/T353_keyboard_responsive_ui_hardening.md`
- `docs/tasks/M24_demo_hardening_and_local_backend/T354_local_run_browser_qa.md`
- `docs/tasks/M24_demo_hardening_and_local_backend/T355_m24_milestone_review.md`

Worker summaries:

- `docs/worker_summary/T350_worker_summary.md`
- `docs/worker_summary/T351_worker_summary.md`
- `docs/worker_summary/T352_worker_summary.md`
- `docs/worker_summary/T353_worker_summary.md`
- `docs/worker_summary/T354_worker_summary.md`

## Verification Evidence

T351 verification:

```text
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\ui\text_first_web_demo_local_server.py
```

Result: passed.

```text
$env:PYTHONPATH='src'
pytest tests\test_text_first_web_demo_local_server.py tests\test_text_first_web_demo_static.py tests\test_text_first_web_demo_adapter.py -q -o cache_dir=artifacts\t351_pytest_cache --basetemp=artifacts\t351_pytest_basetemp
```

Result: passed, `17 passed`.

T353 verification:

```text
$env:PYTHONPATH='src'
pytest tests\test_text_first_web_demo_accessibility.py tests\test_text_first_web_demo_state_switching.py tests\test_text_first_web_demo_static.py tests\test_text_first_web_demo_local_server.py tests\test_text_first_web_demo_adapter.py -q -o cache_dir=artifacts\t353_pytest_cache --basetemp=artifacts\t353_pytest_basetemp
```

Result: passed, `25 passed`.

T350, T352, and T354 verification:

```text
git diff --check
```

Result: passed with Windows line-ending conversion warnings.

## Browser QA Evidence Summary

T354 used the T351 local server helper:

```text
build_http_server(port=8769)
```

Tested URL:

```text
http://127.0.0.1:8769/
```

Browser QA checked:

- desktop `1280x720`;
- mobile `390x844`;
- all seven scenarios;
- selected tab `aria-selected=true`;
- active scenario `aria-pressed=true`;
- expected active panel visibility;
- AI identity visibility;
- friendly labels;
- proactive no-send label;
- voice-off labels;
- avatar-locked label;
- no page-level horizontal overflow in tested viewports;
- no browser console errors or warnings in the tested desktop pass.

Browser QA recorded one important residual risk: automated keypress focus
traversal was inconclusive, so real manual keyboard traversal and screen-reader
behavior remain unverified.

## Safety Boundary Assessment

M24 is safe to treat as local review infrastructure because:

- the local server serves only adapter-backed synthetic state and local static
  assets;
- path traversal and unknown files are rejected;
- responses include no provider credentials, private chat text, generated media
  paths, platform delivery fields, send queues, schedules, webhooks, microphone
  prompts, or camera prompts;
- static UI keeps AI-generated/synthetic identity visible;
- friendly labels preserve safety meaning;
- real-person recreation remains blocked;
- memory distinguishes evidence-backed and imagined states;
- life stream remains imagined/not-real-world;
- proactive state remains non-sending;
- voice remains off;
- avatar remains locked for research review;
- Browser QA did not find horizontal overflow in representative desktop/mobile
  viewports.

## Explicit Non-Actions

M24 did not implement:

- production backend;
- public hosting;
- authentication;
- persistence;
- private chat ingestion;
- real persona distillation;
- model-provider calls;
- final companion reply generation;
- memory/persona mutation;
- proactive candidate generation;
- automatic sending or scheduling;
- notifications;
- webhooks;
- platform integration;
- export/share/download writing;
- TTS;
- ASR;
- voice cloning;
- microphone capture;
- generated audio;
- generated images/video;
- avatar runtime;
- Live2D runtime;
- camera capture;
- face tracking;
- external user research execution;
- legal, compliance, app-store, regulator, user-study, or launch validation.

## Residual Risks

- M24 remains a local synthetic demo, not a production app.
- Real manual keyboard traversal remains unverified.
- Arrow-key roving tab behavior is not implemented.
- Screen-reader, high-contrast, zoom, CJK localization, RTL layout, and
  extreme-payload testing remain unverified.
- Screenshots were captured only as transient Browser artifacts and are not
  committed.
- No real users participated in the walkthrough or QA.
- No persistence, memory mutation, persona growth, or distillation workflow is
  implemented yet.
- Voice/avatar remain locked and are not runtime features.

## M25 Entry Recommendation

Proceed to M25 with memory, persona growth, and distillation planning.

M25 should:

- stay local, synthetic, and review-first at the start;
- design an advanced memory architecture before implementation;
- model memory provenance, confidence, salience, decay, contradiction,
  consolidation, and user control;
- model persona growth as bounded, reviewable state changes rather than
  uncontrolled drift;
- plan distillation from chat records using synthetic fixtures first;
- define consent, redaction, third-party data, and real-person likeness
  boundaries before any private data handling;
- avoid model-provider calls, private chat ingestion, automatic outreach,
  platform delivery, voice/avatar runtime, and launch claims until later
  explicit task packages allow them.

## Reviewer Recommendation

Reviewer should mark M24 as PASS_WITH_WARNINGS if fresh diff check is clean and
no later diff weakens local-only, synthetic, no-send, voice-off, avatar-locked,
AI identity, or real-person recreation boundaries.

Reviewer should BLOCK only if later changes hide Browser QA risks, treat
automated QA as completed accessibility validation, imply launch readiness, or
recommend private data ingestion, real-person recreation, provider calls,
automatic outreach, platform delivery, voice/avatar runtime, or media
generation before a scoped follow-up task.

