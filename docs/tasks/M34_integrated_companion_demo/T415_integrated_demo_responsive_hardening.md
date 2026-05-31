# T415: Integrated Demo Responsive Hardening

## Task ID

T415

## Goal

Harden the integrated local web demo for responsive layout and text fit.

T415 should verify and improve the static demo after T413-T414 added integrated
scenario and trust/commercial panels. The work should focus on layout density,
mobile wrapping, first-viewport scanability, and preserving local-only safety
boundaries.

## Allowed Files

Future T415 worker may create or modify only:

- `src/practical_chat_agent/ui/static/text_first_web_demo.html`
- `src/practical_chat_agent/ui/static/text_first_web_demo.js`
- `src/practical_chat_agent/ui/static/text_first_web_demo.css`
- `tests/test_integrated_demo_responsive_hardening.py`
- `docs/data_contracts/integrated_demo_responsive_hardening_contract.md`
- `docs/tasks/M34_integrated_companion_demo/T416_m34_milestone_review.md`
- `docs/worker_summary/T415_worker_summary.md`
- `docs/07_handoff.md`

If T415 needs private data, source readers, model-provider calls, package
changes, external system adapters, outbound messaging, voice/avatar runtime,
media generation, automatic apply triggers, PersonaVersionStore writes, or
MemoryEventStore writes, Captain must revise this package before assignment.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not ingest, summarize, transform, quote, or commit real private chat
  records.
- Do not call model providers.
- Do not modify runtime services or stores.
- Do not add schedulers, queues, webhooks, auth, tokens, recipient ids,
  delivery state, or external-system persistence behavior.
- Do not implement automatic outreach, sending, scheduling, notifications,
  external delivery, microphone, camera, ASR, TTS, voice cloning,
  voice/avatar likeness, Live2D, generated audio, generated image, generated
  video, or media capture.
- Do not modify `docs/04_task_board.md`.

## Expected Outputs

### 1. Responsive Hardening

Improve static CSS/HTML/JS as needed so:

- integrated scenario and trust/commercial sections scan cleanly;
- long labels and commercial text wrap without overflow;
- mobile layout remains usable;
- review workspace and voice/avatar locked states still render.

### 2. Tests

Create `tests/test_integrated_demo_responsive_hardening.py` proving:

- static CSS includes responsive constraints for new panels;
- HTML keeps accessible labels for the new sections;
- JS does not introduce forbidden action controls;
- served payload/static assets remain free of forbidden private/provider/outbound
  or media fields.

### 3. Data Contract

Create `docs/data_contracts/integrated_demo_responsive_hardening_contract.md`.

### 4. Next Task Package

Create `docs/tasks/M34_integrated_companion_demo/T416_m34_milestone_review.md`.

### 5. Worker Summary And Handoff

Write `docs/worker_summary/T415_worker_summary.md` and append a T415 worker
record to `docs/07_handoff.md`.

Do not mark T415 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'
pytest tests\test_integrated_demo_responsive_hardening.py tests\test_text_first_web_demo_static.py tests\test_text_first_web_demo_accessibility.py tests\test_text_first_web_demo_state_switching.py -q
```

```powershell
git diff --check
```

Use project-local pytest cache and basetemp paths if the default user temp
directory is not writable.

## Browser QA

After tests pass, use the in-app Browser through a localhost preview to verify
desktop and narrow/mobile-width rendering for the integrated scenario and
trust/commercial panels.

## Reviewer Type

Adversarial responsive UI review for text fit, scanability, accessible static
structure, and no provider/outbound/media surface expansion.
