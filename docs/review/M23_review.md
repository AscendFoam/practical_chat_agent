# M23 Review: Integrated Text-First Web Demo

## Status

Gate recommendation: PASS_WITH_WARNINGS for entering M24 demo hardening and
local backend work.

M23 produced a coherent local text-first companion demo path: scope, synthetic
state adapter, static web shell, local scenario switching, Browser visual QA,
and supervised-review walkthrough/protocol. It did not implement production
frontend infrastructure, persistence, model-provider calls, private chat
distillation, automatic outreach, platform delivery, voice runtime, avatar
runtime, media generation, or launch readiness.

## Task Coverage

| Task | Result | Evidence |
| --- | --- | --- |
| T340 Text-first web demo scope | Implemented | `docs/product/text_first_web_demo_scope.md`. |
| T341 Web demo state adapter | Implemented | `TextFirstWebDemoAdapter`, adapter tests, and state contract. |
| T342 Static web demo shell | Implemented | Static HTML/CSS/JS shell, helper, tests, and Browser smoke check. |
| T343 Web demo state switching | Implemented | Local scenario controls, switching tests, and Browser verification. |
| T344 Web demo visual QA | Implemented | `docs/qa/web_demo_visual_qa.md` with desktop/mobile Browser evidence. |
| T345 Web demo walkthrough | Implemented | Product walkthrough and internal supervised-review protocol update. |

## Implemented Code And Static Assets

- `src/practical_chat_agent/ui/text_first_web_demo_adapter.py`
  - `TextFirstWebDemoState`
  - `TextFirstWebDemoAdapter`
- `src/practical_chat_agent/ui/text_first_web_demo_static.py`
  - `TextFirstWebDemoStaticShell`
- `src/practical_chat_agent/ui/static/text_first_web_demo.html`
- `src/practical_chat_agent/ui/static/text_first_web_demo.css`
- `src/practical_chat_agent/ui/static/text_first_web_demo.js`

## Tests Added

- `tests/test_text_first_web_demo_adapter.py`
- `tests/test_text_first_web_demo_static.py`
- `tests/test_text_first_web_demo_state_switching.py`

## Product, Research, QA, And Contract Artifacts

Product and research:

- `docs/product/text_first_web_demo_scope.md`
- `docs/product/text_first_web_demo_walkthrough.md`
- `docs/research/text_first_web_demo_study_protocol_update.md`

QA:

- `docs/qa/web_demo_visual_qa.md`

Data contracts:

- `docs/data_contracts/text_first_web_demo_state_contract.md`
- `docs/data_contracts/static_web_demo_shell_contract.md`
- `docs/data_contracts/web_demo_state_switching_contract.md`

## Verification Evidence

T341 verification:

```text
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\ui\text_first_web_demo_adapter.py
```

Result: passed.

```text
$env:PYTHONPATH='src'
pytest tests\test_text_first_web_demo_adapter.py tests\test_text_first_onboarding_prototype.py tests\test_text_first_chat_memory_prototype.py tests\test_text_first_life_stream_prototype.py tests\test_text_first_proactive_settings_prototype.py tests\test_voice_consent_data_model.py -q -o cache_dir=artifacts\t341_pytest_cache --basetemp=artifacts\t341_pytest_basetemp
```

Result: passed, `43 passed`.

T342 verification:

```text
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\ui\text_first_web_demo_static.py
```

Result: passed.

```text
$env:PYTHONPATH='src'
pytest tests\test_text_first_web_demo_static.py tests\test_text_first_web_demo_adapter.py -q -o cache_dir=artifacts\t342_pytest_cache --basetemp=artifacts\t342_pytest_basetemp
```

Result: passed, `11 passed`.

T343 verification:

```text
$env:PYTHONPATH='src'
pytest tests\test_text_first_web_demo_state_switching.py tests\test_text_first_web_demo_static.py tests\test_text_first_web_demo_adapter.py -q -o cache_dir=artifacts\t343_pytest_cache --basetemp=artifacts\t343_pytest_basetemp
```

Result: passed, `15 passed`.

T344 and T345 verification:

```text
git diff --check
```

Result: passed with Windows line-ending conversion warnings.

Additional worker-level evidence is recorded in:

- `docs/worker_summary/T340_worker_summary.md`
- `docs/worker_summary/T341_worker_summary.md`
- `docs/worker_summary/T342_worker_summary.md`
- `docs/worker_summary/T343_worker_summary.md`
- `docs/worker_summary/T344_worker_summary.md`
- `docs/worker_summary/T345_worker_summary.md`

## Browser QA Evidence Summary

T342 and T343 used temporary localhost static serving because direct `file://`
navigation was blocked by the in-app browser URL policy.

T344 performed a focused Browser visual QA pass:

- local URL: `http://127.0.0.1:8767/`;
- served path: `src/practical_chat_agent/ui/static`;
- desktop viewport: `1280x720`;
- mobile viewport: `390x844`;
- seven tabs, seven panels, and seven scenario buttons verified;
- Safe review default state verified;
- Dependency scenario verified to select Proactive panel;
- Voice / Avatar scenario verified to select Voice / Avatar panel;
- AI-generated synthetic identity strip remained visible;
- voice rows remained `voice enabled: false`;
- avatar remained `locked_research_only`;
- no page-level horizontal overflow or inspected text-overflow issues were
  found in tested viewports;
- browser console check returned no errors or warnings in the desktop default
  state;
- temporary server was stopped and viewport override was reset.

## Safety Boundary Assessment

M23 is safe to treat as a local review milestone because:

- AI-generated/synthetic identity is surfaced persistently;
- demo payloads are synthetic fixtures, not private chat history;
- the adapter reuses existing text-first, consent, AIGC, crisis/dependency, and
  voice-consent contracts;
- safe fictional persona and blocked real-person clone states are both visible;
- chat memory distinguishes evidence-backed and imagined memory;
- crisis and dependency states remain blocked/review-oriented;
- imagined life-stream content is labeled as not real-world activity;
- proactive state includes `outreach_allowed=false`;
- controls expose consent scopes and AIGC labels;
- voice disabled, review-required, and blocked states all keep
  `voice_enabled=false`;
- avatar remains locked/research-only with real-person likeness blocked;
- static assets contain no external network assets, provider credentials, raw
  private text, transcripts, generated media paths, platform delivery fields,
  microphone/camera prompts, send queues, schedules, or webhooks;
- walkthrough and protocol explicitly prohibit private chat data, real-person
  recreation, model calls, platform connection, media generation, and launch
  claims.

## Explicit Non-Actions

M23 did not implement:

- production frontend app;
- packaged frontend build system;
- production backend route;
- persistence;
- model-provider calls;
- final companion reply generation;
- private chat-log reads;
- real persona distillation;
- memory/persona mutation;
- export/share/download writing;
- proactive candidate generation;
- automatic sending or scheduling;
- notifications;
- webhooks;
- platform integration;
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
- real user research execution;
- legal, clinical, app-store, regulator, user-study, or launch validation.

## Residual Risks

- M23 remains a static local demo, not a production application.
- Static preview uses a fallback payload; generated adapter payload wiring needs
  a cleaner local route or generated HTML artifact.
- Technical strings with underscores are readable but not user-friendly.
- No keyboard-only pass, screen-reader pass, high-contrast pass, zoom pass, dark
  mode pass, CJK localization pass, RTL pass, or extreme-payload pass has been
  completed.
- Screenshots were captured transiently in Browser QA but not committed as
  image artifacts.
- No real users participated in the walkthrough or protocol.
- No persistence, settings mutation, local issue logging, or route-level
  navigation exists.
- No live model quality, memory quality, persona quality, companionship quality,
  dependency risk, or crisis-handling efficacy has been validated.
- Voice/avatar remain research and locked-state surfaces only.

## M24 Entry Recommendation

Proceed to M24 with a local demo hardening and local backend milestone.

M24 should:

- keep all data synthetic;
- add a local backend or generated HTML path that serves adapter payloads
  cleanly;
- keep static assets dependency-light unless a scoped task justifies otherwise;
- replace technical strings with friendlier labels while preserving underlying
  safety meaning;
- improve keyboard and accessibility behavior;
- harden desktop/mobile layout against longer labels and localized copy;
- add local-only reviewer notes or issue-capture conventions if scoped;
- keep voice/avatar locked;
- keep proactive behavior non-sending and review-only;
- avoid private chat ingestion, model-provider calls, platform delivery, media
  generation, automatic outreach, and launch claims.

## Reviewer Recommendation

Reviewer should mark M23 as PASS_WITH_WARNINGS if fresh diff check is clean and
no later diff weakens identity, consent, labeling, crisis/dependency,
real-person clone, proactive no-send, voice lock, or avatar lock boundaries.

Reviewer should BLOCK only if later changes hide residual risks, treat the
walkthrough as completed user validation, imply launch readiness, or recommend
private data ingestion, model providers, automatic outreach, platform delivery,
voice runtime, avatar runtime, or generated media before a scoped follow-up
task.

