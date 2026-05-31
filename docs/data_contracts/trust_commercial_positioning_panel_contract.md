# Trust Commercial Positioning Panel Contract

Task: T414 Trust Commercial Positioning Panel
Status: worker draft for review

## Scope

This contract describes the trust/commercial positioning panel in:

- `src/practical_chat_agent/ui/text_first_web_demo_adapter.py`
- `src/practical_chat_agent/ui/static/text_first_web_demo.html`
- `src/practical_chat_agent/ui/static/text_first_web_demo.js`
- `src/practical_chat_agent/ui/static/text_first_web_demo.css`

The panel is a synthetic local product-review surface. It does not implement
payments, billing, external integrations, private data use, provider calls,
outbound behavior, or media generation.

## Payload

`TextFirstWebDemoState` now includes:

- `trust_commercial`

Required payload fields:

- `schema_version=trust_commercial_positioning_v1`
- `pricing_hypotheses`
- `value_pillars`
- `trust_controls`
- `unacceptable_patterns`
- `readiness_gaps`
- `safety_notes`

## Static UI

The static demo includes:

- `#trust-commercial-panel`
- `#trust-pricing-list`
- `#trust-control-list`
- `#unacceptable-pattern-list`
- `#readiness-gap-list`
- `drawTrustCommercial(...)`
- `.trust-commercial-grid`

## Safety Invariants

- The payload is synthetic and local-only.
- It does not include raw private records, provider credentials, recipient ids,
  webhooks, tokens, or media payloads.
- It explicitly names unacceptable monetization patterns:
  - guilt-based retention;
  - impersonation claims;
  - crisis paywalls;
  - hidden private-data use.
- It does not add controls for outreach, billing, external delivery, provider
  calls, or media generation.

## Tests

Implemented tests:

- `tests/test_trust_commercial_positioning_panel.py`

Regression tests also run:

- `tests/test_integrated_demo_scenario_spine.py`
- `tests/test_text_first_web_demo_static.py`
- `tests/test_text_first_web_demo_local_server.py`

Covered behavior:

- payload contains trust and commercial positioning;
- unacceptable monetization patterns are explicit;
- static HTML/JS/CSS include expected panel hooks;
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
pytest tests\test_trust_commercial_positioning_panel.py tests\test_integrated_demo_scenario_spine.py tests\test_text_first_web_demo_static.py tests\test_text_first_web_demo_local_server.py -q -o cache_dir=artifacts\t414_pytest_cache --basetemp=artifacts\t414_pytest_basetemp
```

```powershell
git diff --check
```

## Non-Actions

T414 does not implement:

- payment processing;
- billing;
- production business rules;
- runtime companion behavior;
- new apply execution;
- persona version mutation;
- memory lifecycle mutation;
- private data ingestion;
- source readers;
- model-provider calls;
- final companion reply generation;
- proactive candidates;
- automatic sending or scheduling;
- external-system integration;
- voice/avatar/video behavior;
- generated media;
- legal, clinical, launch, app-store, or regulator approval.

## Residual Risks

- Commercial positioning is a hypothesis review surface.
- No customer validation or pricing validation is claimed.
- The panel does not authorize production monetization.
