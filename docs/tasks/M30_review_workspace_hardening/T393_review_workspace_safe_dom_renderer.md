# T393: Review Workspace Safe DOM Renderer

## Task ID

T393

## Goal

Harden the static review workspace panel by rendering review card payload
fields through DOM nodes and `textContent` instead of string-built markup.

T393 should preserve the T390/T391 static panel behavior, fallback fixture,
server-provided payload support, and accessibility surface while reducing the
risk of unsafe markup if later milestones pass user-provided or imported
review data into the panel.

## Allowed Files

Future T393 worker may create or modify only:

- `src/practical_chat_agent/ui/static/text_first_web_demo.js`
- `tests/test_review_workspace_static_panel.py`
- `docs/product/m30_review_workspace_hardening_scope.md`
- `docs/data_contracts/review_workspace_static_panel_contract.md`
- `docs/tasks/M30_review_workspace_hardening/T393_review_workspace_safe_dom_renderer.md`
- `docs/tasks/M30_review_workspace_hardening/T394_review_workspace_projection_boundary_tests.md`
- `docs/worker_summary/T393_worker_summary.md`
- `docs/07_handoff.md`

If T393 needs Python adapter changes, local server route changes, private data,
Browser runs beyond local static QA, model-provider calls, package changes,
platform adapters, outbound messaging, voice/avatar runtime, media generation,
persistence outside local synthetic payloads, or apply executors, Captain must
revise this package before assignment.

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

## Expected Outputs

- `drawReviewWorkspace` no longer routes review card payload fields through the
  generic string/`innerHTML` item renderer.
- Review card title, badges, summary, blockers, reasons, and counts are built
  with DOM nodes and `textContent`.
- Static tests prove review workspace rendering uses the safe DOM path.
- Existing static, accessibility, and local server payload tests remain green.
- M30 scope and T394 next task package exist.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'
pytest tests\test_review_workspace_static_panel.py tests\test_text_first_web_demo_static.py tests\test_text_first_web_demo_accessibility.py tests\test_review_workspace_local_server_payload.py -q
```

```powershell
git diff --check
```

Use project-local pytest cache and basetemp paths if the default user temp
directory is not writable.

## Reviewer Type

Adversarial static UI hardening review for safe rendering, privacy,
non-apply safety, accessibility, and documentation accuracy.
