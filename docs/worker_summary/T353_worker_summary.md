# T353 Worker Summary

## Changed

- Added `tests/test_text_first_web_demo_accessibility.py`.
- Updated `src/practical_chat_agent/ui/static/text_first_web_demo.html`.
- Updated `src/practical_chat_agent/ui/static/text_first_web_demo.css`.
- Updated `src/practical_chat_agent/ui/static/text_first_web_demo.js`.
- Added
  `docs/tasks/M24_demo_hardening_and_local_backend/T354_local_run_browser_qa.md`.
- Appended the T353 handoff record to `docs/07_handoff.md`.
- Wrote this worker summary.

## Implementation Result

T353 hardens the static UI:

- adds top-level `role="tablist"` and tab `role="tab"` semantics;
- adds stable tab ids and `aria-controls`;
- adds panel `role="tabpanel"`, `aria-labelledby`, `hidden`, and
  `aria-hidden` states;
- updates JavaScript to maintain `aria-selected` and panel hidden state;
- adds scenario `aria-pressed` state and updates it during switching;
- adds friendly label mapping for technical state values;
- renders friendlier labels for memory, persona, crisis, dependency, life,
  controls, proactive, voice, and avatar states;
- preserves AI identity, proactive no-send, voice-off, and avatar-locked
  surfaces;
- adds long-label wrapping rules without adding external assets or dependencies.

## TDD Evidence

RED command:

```text
$env:PYTHONPATH='src'
pytest tests\test_text_first_web_demo_accessibility.py -q -o cache_dir=artifacts\t353_pytest_cache_red --basetemp=artifacts\t353_pytest_basetemp_red
```

Result: failed as expected, 4 failures. The existing static assets lacked tab
ARIA relationships, scenario pressed state, friendly label mapping, and
long-label wrapping rules.

GREEN command:

```text
$env:PYTHONPATH='src'
pytest tests\test_text_first_web_demo_accessibility.py tests\test_text_first_web_demo_state_switching.py tests\test_text_first_web_demo_static.py tests\test_text_first_web_demo_local_server.py tests\test_text_first_web_demo_adapter.py -q -o cache_dir=artifacts\t353_pytest_cache_green2 --basetemp=artifacts\t353_pytest_basetemp_green2
```

Result: passed, `25 passed`.

## Browser Verification

Browser smoke verification used the T351 local server path on a temporary local
URL:

```text
http://127.0.0.1:8768/
```

Checks performed:

- desktop viewport `1280x720`;
- mobile viewport `390x844`;
- root page loaded through the local server helper;
- active tab used `aria-selected=true`;
- active panel was visible and not hidden;
- active scenario used `aria-pressed=true`;
- Dependency scenario selected the Proactive panel;
- Proactive summary showed `Consent: Enabled / No messages can be sent`;
- Voice / Avatar scenario selected the Voice / Avatar panel;
- Voice rows showed `Voice is off`;
- Avatar notice showed `Avatar locked for research review`;
- AI identity strip remained visible;
- no page-level horizontal overflow was detected in tested desktop/mobile
  viewports;
- temporary preview server was stopped after verification.

## Explicit Non-Actions

- No Python backend change, package-manager dependency, model-provider call,
  final reply generation, private data processing, voice/avatar runtime, media
  generation, external network asset, platform adapter, outbound messaging,
  screenshot artifact, or task-board edit was added.
- No legal advice, compliance completion, app-store approval, launch approval,
  user-study validation, real user evidence, or regulator acceptance was
  claimed.
- No `private/chat_history/`, `private/distilled/`, or private artifact content
  was read, quoted, summarized, or committed.
- T353 does not mark itself complete in `docs/04_task_board.md`.

## Verification

Commands run:

```text
$env:PYTHONPATH='src'
pytest tests\test_text_first_web_demo_accessibility.py tests\test_text_first_web_demo_state_switching.py tests\test_text_first_web_demo_static.py tests\test_text_first_web_demo_local_server.py tests\test_text_first_web_demo_adapter.py -q -o cache_dir=artifacts\t353_pytest_cache --basetemp=artifacts\t353_pytest_basetemp
```

Result: passed, `25 passed`.

```text
git diff --check
```

Result: passed with Windows line-ending conversion warnings.

## Remaining Risks

- Browser verification was a smoke pass, not the formal T354 QA pass.
- Arrow-key roving tab behavior is not implemented.
- Screen-reader validation, high-contrast validation, zoom validation, CJK
  localization, RTL layout, and extreme-payload testing remain unverified.

## Recommended Reviewer Type

Adversarial frontend, accessibility, and product/safety UX review.
