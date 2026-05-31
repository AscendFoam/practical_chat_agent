# T342 Worker Summary

## Changed

- Added `tests/test_text_first_web_demo_static.py`.
- Added `src/practical_chat_agent/ui/text_first_web_demo_static.py`.
- Added static assets:
  - `src/practical_chat_agent/ui/static/text_first_web_demo.html`
  - `src/practical_chat_agent/ui/static/text_first_web_demo.css`
  - `src/practical_chat_agent/ui/static/text_first_web_demo.js`
- Added `docs/data_contracts/static_web_demo_shell_contract.md`.
- Added
  `docs/tasks/M23_integrated_text_first_web_demo/T343_web_demo_state_switching.md`.
- Appended the T342 handoff record to `docs/07_handoff.md`.
- Wrote this worker summary.

## Implementation Result

T342 adds a dependency-light local static web shell:

- no package manager;
- no external network assets;
- HTML/CSS/JS static files;
- Python helper exposes asset paths and adapter-generated embedded HTML;
- tabs for Chat, Persona, Memory, Life, Proactive, Controls, Voice / Avatar;
- persistent AI-generated synthetic identity strip;
- voice and avatar rendered as not enabled;
- static fallback payload for direct local preview.

## TDD Evidence

RED command:

```text
$env:PYTHONPATH='src'
pytest tests\test_text_first_web_demo_static.py -q -o cache_dir=artifacts\t342_pytest_cache_red --basetemp=artifacts\t342_pytest_basetemp_red
```

Result: failed as expected because
`practical_chat_agent.ui.text_first_web_demo_static` did not exist.

GREEN command:

```text
$env:PYTHONPATH='src'
pytest tests\test_text_first_web_demo_static.py -q -o cache_dir=artifacts\t342_pytest_cache_green --basetemp=artifacts\t342_pytest_basetemp_green
```

Result: passed, `5 passed`.

## Browser Verification

- Direct `file://` navigation was blocked by the in-app browser URL policy.
- Used a temporary localhost static server for
  `src/practical_chat_agent/ui/static`.
- Verified `http://127.0.0.1:8767/` loaded with 7 tabs and 7 panels.
- Verified the Chat panel rendered AI identity, memory explanations, and
  crisis blocked state.
- Verified the Voice / Avatar tab was selectable and showed voice enabled false
  and avatar locked state.
- Adjusted tabs from horizontal scrolling to wrapping after screenshot review.
- Stopped the temporary localhost server after verification.

## Explicit Non-Actions

- No model-provider call, final reply generation, private data processing,
  voice/avatar runtime, media generation, external network asset, package
  manager, platform adapter, outbound messaging, or task-board edit was added.
- No legal advice, compliance completion, app-store approval, launch approval,
  user-study validation, or regulator acceptance was claimed.
- No `private/chat_history/`, `private/distilled/`, or private artifact content
  was read, quoted, summarized, or committed.
- T342 does not mark itself complete in `docs/04_task_board.md`.

## Verification

Commands run:

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

```text
git diff --check
```

Result: passed.

## Remaining Risks

- T342 is still a static shell; scenario switching and deeper visual QA remain
  for follow-up tasks.
- Browser verification used a temporary local static server because direct file
  navigation was blocked by browser policy.

## Recommended Reviewer Type

Adversarial product/safety UX and frontend review.
