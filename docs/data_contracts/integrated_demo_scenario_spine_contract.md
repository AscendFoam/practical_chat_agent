# Integrated Demo Scenario Spine Contract

Task: T413 Integrated Demo Scenario Spine
Status: worker draft for review

## Scope

This contract describes the local integrated scenario spine in:

- `src/practical_chat_agent/ui/text_first_web_demo_adapter.py`
- `src/practical_chat_agent/ui/static/text_first_web_demo.html`
- `src/practical_chat_agent/ui/static/text_first_web_demo.js`
- `src/practical_chat_agent/ui/static/text_first_web_demo.css`

The spine is a synthetic product-review surface. It does not execute companion
runtime behavior, read private chat logs, call providers, write stores, send
messages, connect to external systems, or generate voice/avatar/media.

## Payload

`TextFirstWebDemoState` now includes:

- `integrated_scenario`

Required payload fields:

- `schema_version=integrated_demo_scenario_spine_v1`
- `scenario_title`
- `persona_promise`
- `memory_promise`
- `review_promise`
- `proactive_promise`
- `life_stream_promise`
- `voice_avatar_boundary`
- `commercial_positioning`
- `readiness_summary`
- `scenario_steps`

Each scenario step includes:

- `step_label`
- `section_key`
- `safe_summary`

Expected section keys include:

- `persona`
- `chat`
- `memory`
- `review`
- `proactive`
- `life`
- `controls`
- `voice-avatar`

## Static UI

The static demo includes:

- `#integrated-scenario`
- `#scenario-spine-list`
- `#scenario-readiness`
- `#scenario-commercial`
- `drawIntegratedScenario(...)`
- `.scenario-spine-grid`

The integrated scenario is visible near the top of the local demo. It is an
operational review surface rather than a marketing landing page.

## Safety Invariants

- The payload is synthetic and local-only.
- It contains safe summaries rather than raw private records.
- Commercial positioning excludes dependency pressure, impersonation,
  replacement claims, crisis paywalls, and monetization of private chat
  content.
- Static assets do not add controls for sending, scheduling, external-system
  delivery, provider calls, webhooks, tokens, or media generation.
- Voice/avatar remains a boundary state, not an enabled runtime.

## Tests

Implemented tests:

- `tests/test_integrated_demo_scenario_spine.py`

Regression tests also run:

- `tests/test_text_first_web_demo_static.py`
- `tests/test_text_first_web_demo_local_server.py`

Covered behavior:

- adapter state includes `integrated_scenario`;
- scenario steps have safe labels, section keys, and summaries;
- commercial positioning excludes dependency and impersonation claims;
- static HTML/JS/CSS include expected hooks;
- served payload/static assets contain no forbidden private/provider/outbound
  or media fields.

## Verification

Expected minimum verification:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\ui\text_first_web_demo_adapter.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_integrated_demo_scenario_spine.py tests\test_text_first_web_demo_static.py tests\test_text_first_web_demo_local_server.py -q -o cache_dir=artifacts\t413_pytest_cache --basetemp=artifacts\t413_pytest_basetemp
```

```powershell
git diff --check
```

## Non-Actions

T413 does not implement:

- runtime companion behavior;
- new apply execution;
- persona version mutation;
- memory lifecycle mutation;
- private data ingestion;
- source readers;
- extraction from real logs;
- embeddings;
- vector search;
- semantic ranking;
- similarity scoring;
- model-provider calls;
- final companion reply generation;
- proactive candidates;
- automatic sending or scheduling;
- external-system integration;
- voice/avatar/video behavior;
- generated media;
- legal, clinical, launch, app-store, or regulator approval.

## Residual Risks

- The scenario spine is synthetic and local-only.
- It improves reviewer comprehension but does not prove user value.
- Commercial framing is a prototype review surface, not a validated business
  model.
