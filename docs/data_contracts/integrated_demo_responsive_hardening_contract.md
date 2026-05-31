# Integrated Demo Responsive Hardening Contract

Task: T415 Integrated Demo Responsive Hardening
Status: worker draft for review

## Scope

This contract describes responsive hardening for the local static web demo in:

- `src/practical_chat_agent/ui/static/text_first_web_demo.css`

T415 does not change payload schemas or runtime behavior. It adds CSS
constraints and tests for the integrated scenario and trust/commercial panels.

## Implemented CSS Constraints

Added or verified:

- `.item { min-width: 0; }`
- mobile padding rules for:
  - `.scenario-spine`
  - `.trust-commercial`
- mobile single-column grid rules for:
  - `.scenario-promise-grid`
  - `.scenario-spine-grid`
  - `.trust-commercial-grid`
  - `.review-grid`
- existing text wrapping rules:
  - `overflow-wrap: anywhere;`
  - `word-break: normal;`

## Required Invariants

- Integrated scenario and trust/commercial panels must wrap on narrow viewports.
- Long labels must not widen cards beyond their container.
- Static assets must not add action controls for approval, rejection,
  delivery, external calls, provider calls, or media generation.
- Served payload/static assets must remain free of forbidden private/provider
  outbound or media fields.

## Tests

Implemented tests:

- `tests/test_integrated_demo_responsive_hardening.py`

Regression tests also run:

- `tests/test_text_first_web_demo_static.py`
- `tests/test_text_first_web_demo_accessibility.py`
- `tests/test_text_first_web_demo_state_switching.py`

Covered behavior:

- CSS includes mobile constraints for the integrated and commercial sections;
- HTML keeps accessible labels for new sections;
- JS has no forbidden action controls;
- served demo remains free of forbidden private/provider/outbound/media fields.

## Verification

Expected minimum verification:

```powershell
$env:PYTHONPATH='src'
pytest tests\test_integrated_demo_responsive_hardening.py tests\test_text_first_web_demo_static.py tests\test_text_first_web_demo_accessibility.py tests\test_text_first_web_demo_state_switching.py -q -o cache_dir=artifacts\t415_pytest_cache --basetemp=artifacts\t415_pytest_basetemp
```

```powershell
git diff --check
```

## Non-Actions

T415 does not implement:

- payload or runtime schema changes;
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

- Browser QA is limited to the viewport available in this environment.
- T416 still needs M34 milestone review.
