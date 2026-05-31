# T420: Session Review Candidate Linkage

## Task ID

T420

## Goal

Link T418/T419 post-session candidates into the local review workspace surface.

T420 should make memory, persona, proactive, and optional life-stream
post-session candidates inspectable from the existing review workspace without
automatic apply, sending, runtime store writes, or platform behavior. The goal
is to connect the session loop to the review-first governance model.

## Allowed Files

Future T420 worker may create or modify only:

- `src/practical_chat_agent/ui/text_first_web_demo_adapter.py`
- `src/practical_chat_agent/ui/static/text_first_web_demo.html`
- `src/practical_chat_agent/ui/static/text_first_web_demo.js`
- `src/practical_chat_agent/ui/static/text_first_web_demo.css`
- `tests/test_session_review_candidate_linkage.py`
- `tests/test_review_workspace_apply_audit_panel.py`
- `tests/test_text_first_web_demo_local_server.py`
- `tests/test_static_companion_session_loop.py`
- `docs/data_contracts/session_review_candidate_linkage_contract.md`
- `docs/tasks/M35_next_iteration/T421_session_loop_responsive_hardening.md`
- `docs/worker_summary/T420_worker_summary.md`
- `docs/07_handoff.md`

If T420 needs private data, source readers, model-provider calls, package
changes, platform adapters, outbound messaging, voice/avatar runtime, media
generation, automatic apply triggers, PersonaVersionStore writes,
MemoryEventStore writes, runtime store writes, or task-board edits, Captain
must revise this package before assignment.

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

### 1. Review Candidate Projection

Expose post-session candidates as review workspace entries or a clearly linked
review candidate panel.

Each linked candidate should preserve:

- candidate id;
- candidate kind;
- originating turn id;
- safe summary;
- review-required status;
- preview-only status;
- non-execution flags;
- session source reference.

### 2. Static Review Linkage

The static demo should let a reviewer move from the session loop to candidate
review context without adding approve/reject/apply/send controls.

Acceptable options:

- add session candidate cards to the existing review workspace list; or
- add a compact linked-review subsection inside the session loop that mirrors
  review workspace card semantics.

### 3. Tests

Create `tests/test_session_review_candidate_linkage.py` proving:

- session post-turn candidates are represented in a review-facing surface;
- memory, persona, and proactive candidates are all present;
- each linked candidate stays review-required, preview-only, non-sending, and
  non-mutating;
- local server payload/static assets contain no dangerous provider/outbound or
  media enabled states;
- existing review workspace apply audit cards still render.

### 4. Data Contract

Create `docs/data_contracts/session_review_candidate_linkage_contract.md`.

### 5. Next Task Package

Create `docs/tasks/M35_next_iteration/T421_session_loop_responsive_hardening.md`.

T421 should be scoped to responsive/browser hardening for the session loop and
review linkage surfaces.

### 6. Worker Summary And Handoff

Write `docs/worker_summary/T420_worker_summary.md` and append a T420 worker
record to `docs/07_handoff.md`.

Do not mark T420 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'
pytest tests\test_session_review_candidate_linkage.py tests\test_static_companion_session_loop.py tests\test_local_companion_session_simulator.py tests\test_review_workspace_apply_audit_panel.py tests\test_text_first_web_demo_local_server.py -q
```

```powershell
git diff --check
```

Use project-local pytest cache and basetemp paths if the default user temp
directory is not writable.

## Browser QA

After tests pass, use the in-app Browser through a localhost preview to verify:

- session candidates are visible in or linked to the review surface;
- no approve/apply/send/provider/platform/media controls appear;
- existing apply audit cards remain visible in the Review scenario.

## Reviewer Type

Adversarial review-linkage review for session candidate traceability,
review-first controls, non-execution boundaries, and no provider/outbound/media
surface expansion.
