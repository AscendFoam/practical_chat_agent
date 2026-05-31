# T392: M29 Milestone Review

## Task ID

T392

## Goal

Perform an adversarial review of M29 Review Workspace UI.

T392 should review T388 through T391 together: scope, presentation adapter,
static review panel, local server payload, tests, contracts, and handoff. The
review should decide whether M29 can close before any later milestone adds
real apply executors, real import/de-identification, provider-backed
extraction, proactive candidates, voice/avatar runtime, media generation,
platform delivery, monetization, or production persistence.

## Allowed Files

Future T392 reviewer may create or modify only:

- `docs/review/M29_review.md`
- `docs/worker_summary/T392_worker_summary.md`
- `docs/07_handoff.md`

If T392 needs code changes, test changes, task-board edits, private data,
Browser runs beyond local QA, model-provider calls, package changes, platform
adapters, outbound messaging, voice/avatar runtime, media generation, or apply
executors, Captain must revise this package before assignment.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not ingest, summarize, transform, quote, or commit real private chat
  records.
- Do not call model providers.
- Do not implement source readers, extraction from real logs, embeddings,
  vector search, semantic ranking, fine-tuning, similarity scoring, persona
  synthesis, final companion reply generation, runtime persona mutation, or
  runtime memory mutation.
- Do not apply review decisions or dry-run plans.
- Do not mutate memory stores, PersonaCard objects, or PersonaVersionStore.
- Do not add routes, CLIs, schedulers, queues, webhooks, auth, tokens,
  recipient ids, delivery state, or platform persistence behavior.
- Do not implement proactive candidates, automatic outreach, sending,
  scheduling, notifications, platform delivery, microphone, camera, ASR, TTS,
  voice cloning, voice/avatar likeness, Live2D, generated audio, generated
  image, generated video, or media capture.
- Do not modify `docs/04_task_board.md`.
- Do not claim launch approval, legal compliance, app-store acceptance,
  clinical validation, regulator acceptance, user-study validation, or real
  user evidence.

## Inputs To Review

Required:

- `docs/product/m29_review_workspace_ui_scope.md`
- `docs/data_contracts/review_workspace_presentation_contract.md`
- `docs/data_contracts/review_workspace_static_panel_contract.md`
- `docs/data_contracts/review_workspace_local_server_payload_contract.md`
- `src/practical_chat_agent/ui/review_workspace_adapter.py`
- `src/practical_chat_agent/ui/text_first_web_demo_adapter.py`
- `src/practical_chat_agent/ui/text_first_web_demo_local_server.py`
- `src/practical_chat_agent/ui/static/text_first_web_demo.html`
- `src/practical_chat_agent/ui/static/text_first_web_demo.css`
- `src/practical_chat_agent/ui/static/text_first_web_demo.js`
- `tests/test_review_workspace_presentation_adapter.py`
- `tests/test_review_workspace_static_panel.py`
- `tests/test_review_workspace_local_server_payload.py`
- related local demo adapter/server/static tests.

## Expected Outputs

### 1. Milestone Review

Create `docs/review/M29_review.md` with:

- verdict: `PASS`, `PASS_WITH_WARNINGS`, or `BLOCK`;
- reviewed files and tests;
- findings ordered by severity;
- privacy/provider/outbound/media/apply safety assessment;
- static/server contract assessment;
- residual risks;
- recommendation for the next milestone.

### 2. Worker Summary And Handoff

Write `docs/worker_summary/T392_worker_summary.md` and append a T392 review
record to `docs/07_handoff.md`.

Do not mark M29 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\ui\review_workspace_adapter.py src\practical_chat_agent\ui\text_first_web_demo_adapter.py src\practical_chat_agent\ui\text_first_web_demo_local_server.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_review_workspace_presentation_adapter.py tests\test_review_workspace_static_panel.py tests\test_review_workspace_local_server_payload.py tests\test_text_first_web_demo_adapter.py tests\test_text_first_web_demo_local_server.py tests\test_text_first_web_demo_static.py tests\test_text_first_web_demo_accessibility.py -q
```

```powershell
rg -n "private/chat_history|raw_text|raw_transcript|provider_credentials|platform_recipient|send_queue|webhook|microphone|camera|audio_bytes|image_bytes|video_bytes|apply_decision|mutate_store|write_persona_version|generate_audio|generate_image|generate_video" src\practical_chat_agent\ui tests\test_review_workspace_presentation_adapter.py tests\test_review_workspace_static_panel.py tests\test_review_workspace_local_server_payload.py
```

```powershell
git diff --check
```

Use project-local pytest cache and basetemp paths if the default user temp
directory is not writable.

## Reviewer Type

Adversarial milestone review for privacy, non-apply safety, synthetic-only
data, static/server UI fit, product-safety, documentation accuracy, and
residual-risk clarity.
