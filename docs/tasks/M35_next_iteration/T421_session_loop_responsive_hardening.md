# T421: Session Loop Responsive Hardening

## Task ID

T421

## Goal

Harden the M35 session loop and session candidate review linkage for responsive
layout, scanability, and Browser QA.

T421 should verify and improve the static demo after T418-T420 added the local
session payload, session loop UI, and review workspace linkage. The task should
focus on text fit, narrow viewport layout, candidate card density, review
workspace scanability, and preserved local-only boundaries.

## Allowed Files

Future T421 worker may create or modify only:

- `src/practical_chat_agent/ui/static/text_first_web_demo.html`
- `src/practical_chat_agent/ui/static/text_first_web_demo.js`
- `src/practical_chat_agent/ui/static/text_first_web_demo.css`
- `tests/test_session_loop_responsive_hardening.py`
- `tests/test_static_companion_session_loop.py`
- `tests/test_session_review_candidate_linkage.py`
- `tests/test_text_first_web_demo_accessibility.py`
- `docs/data_contracts/session_loop_responsive_hardening_contract.md`
- `docs/tasks/M35_next_iteration/T422_m35_milestone_review.md`
- `docs/worker_summary/T421_worker_summary.md`
- `docs/07_handoff.md`

If T421 needs adapter payload changes, private data, source readers,
model-provider calls, package changes, platform adapters, outbound messaging,
voice/avatar runtime, media generation, automatic apply triggers,
PersonaVersionStore writes, MemoryEventStore writes, runtime store writes, or
task-board edits, Captain must revise this package before assignment.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not ingest, summarize, transform, quote, or commit real private chat
  records.
- Do not call model providers or remote inference.
- Do not implement prompt execution, embeddings, vector search, semantic
  ranking, similarity scoring, fine-tuning, source readers, or real chat
  distillation.
- Do not write PersonaVersionStore, MemoryEventStore, review stores, runtime
  stores, files under `private/`, or persistent user data.
- Do not add schedulers, queues, webhooks, auth, tokens, recipient ids,
  delivery state, platform adapters, automatic outreach, outbound messaging,
  or delivery simulation.
- Do not add microphone, camera, ASR, TTS, voice cloning, Live2D, generated
  audio, generated image, generated video, or media capture.
- Do not add payment processing, production pricing claims, legal advice,
  compliance completion, app-store approval, launch approval, clinical claims,
  or regulator acceptance.
- Do not modify `docs/04_task_board.md`.

## Expected Outputs

### 1. Responsive Hardening

Improve static HTML/CSS/JS as needed so:

- session turns wrap cleanly on narrow viewports;
- memory/persona/safety chips do not overflow;
- session candidate cards remain scannable;
- review workspace cards, including session candidate and apply audit cards,
  remain readable;
- no layout shift or text overlap occurs around the session loop.

### 2. Tests

Create `tests/test_session_loop_responsive_hardening.py` proving:

- CSS contains responsive constraints for the session loop and session review
  cards;
- HTML keeps accessible labels for session and review sections;
- JS does not introduce forbidden action controls;
- served payload/static assets remain free of dangerous provider/outbound or
  media enabled states.

### 3. Data Contract

Create `docs/data_contracts/session_loop_responsive_hardening_contract.md`.

### 4. Next Task Package

Create `docs/tasks/M35_next_iteration/T422_m35_milestone_review.md`.

T422 should be scoped to adversarial M35 milestone review.

### 5. Worker Summary And Handoff

Write `docs/worker_summary/T421_worker_summary.md` and append a T421 worker
record to `docs/07_handoff.md`.

Do not mark T421 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'
pytest tests\test_session_loop_responsive_hardening.py tests\test_static_companion_session_loop.py tests\test_session_review_candidate_linkage.py tests\test_text_first_web_demo_accessibility.py -q
```

```powershell
git diff --check
```

Use project-local pytest cache and basetemp paths if the default user temp
directory is not writable.

## Browser QA

After tests pass, use the in-app Browser through a localhost preview to verify
desktop and narrow/mobile-width rendering for:

- the companion session loop;
- session candidate review cards;
- existing apply audit cards.

## Reviewer Type

Adversarial responsive UI review for session-loop text fit, review card
scanability, accessible static structure, and no provider/outbound/media
surface expansion.
