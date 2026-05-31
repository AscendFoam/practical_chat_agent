# T399: Review Workspace Apply Preview Panel

## Task ID

T399

## Goal

Expose manual apply preview records and eligibility decisions in the local
review workspace UI as read-only cards.

T399 should render synthetic manual apply preview records in the existing
review workspace static/server demo flow. It must remain preview-only and must
not add apply buttons or mutation controls.

## Allowed Files

Future T399 worker may create or modify only:

- `src/practical_chat_agent/ui/text_first_web_demo_adapter.py`
- `src/practical_chat_agent/ui/static/text_first_web_demo.js`
- `src/practical_chat_agent/ui/static/text_first_web_demo.css`
- `tests/test_review_workspace_apply_preview_panel.py`
- `tests/test_review_workspace_local_server_payload.py`
- `docs/data_contracts/review_workspace_apply_preview_panel_contract.md`
- `docs/tasks/M31_manual_apply_preview/T400_m31_milestone_review.md`
- `docs/worker_summary/T399_worker_summary.md`
- `docs/07_handoff.md`

If T399 needs private data, model-provider calls, package changes, new routes,
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
- Do not add schedulers, queues, webhooks, auth, tokens, recipient ids,
  delivery state, or platform persistence behavior.
- Do not implement proactive candidates, automatic outreach, sending,
  scheduling, notifications, platform delivery, microphone, camera, ASR, TTS,
  voice cloning, voice/avatar likeness, Live2D, generated audio, generated
  image, generated video, or media capture.
- Do not modify `docs/04_task_board.md`.

## Expected Outputs

- Synthetic local demo payload includes manual apply preview cards.
- Static review workspace panel renders eligibility outcome, gates, blockers,
  effects, and rollback notes through DOM/text rendering.
- Tests prove no apply/mutation/provider/outbound/media controls are exposed.
- T400 milestone review task exists.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'
pytest tests\test_review_workspace_apply_preview_panel.py tests\test_review_workspace_local_server_payload.py tests\test_review_workspace_static_panel.py -q
```

```powershell
git diff --check
```

Use project-local pytest cache and basetemp paths if the default user temp
directory is not writable.

## Reviewer Type

Adversarial read-only UI review for manual apply preview display, privacy,
non-mutation safety, accessibility, and documentation accuracy.
