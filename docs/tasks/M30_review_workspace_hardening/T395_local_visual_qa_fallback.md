# T395: Local Visual QA Fallback

## Task ID

T395

## Goal

Create a reproducible local visual QA fallback for the review workspace demo
when browser navigation is blocked by the environment.

T395 should verify that the local static review workspace panel can be
inspected without relying on the in-app browser path that blocked T390/T391.
The fallback may use static HTML capture, DOM snapshot checks, or another
deterministic local artifact that does not require network access, package
installs, model providers, platform integration, media generation, or outbound
behavior.

## Allowed Files

Future T395 worker may create or modify only:

- `src/practical_chat_agent/ui/text_first_web_demo_static.py`
- `tests/test_review_workspace_visual_qa_fallback.py`
- `docs/data_contracts/review_workspace_visual_qa_fallback_contract.md`
- `docs/tasks/M30_review_workspace_hardening/T396_manual_apply_preview_scope.md`
- `docs/worker_summary/T395_worker_summary.md`
- `docs/07_handoff.md`

If T395 needs static layout changes, browser automation, package installs,
private data, model-provider calls, platform adapters, outbound messaging,
voice/avatar runtime, media generation, persistence outside local artifacts,
or apply executors, Captain must revise this package before assignment.

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

## Expected Outputs

- A deterministic local visual/DOM QA fallback for the review workspace panel.
- Tests prove the fallback includes the Review tab, review cards, safe summary,
  status badges, blocker text, safe export summary, and no action controls.
- Contract documents why this fallback is not browser screenshot evidence.
- T396 next task package exists for manual apply preview scoping.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'
pytest tests\test_review_workspace_visual_qa_fallback.py tests\test_review_workspace_static_panel.py -q
```

```powershell
git diff --check
```

Use project-local pytest cache and basetemp paths if the default user temp
directory is not writable.

## Reviewer Type

Adversarial local visual QA fallback review for static inspectability,
privacy, non-apply safety, and documentation accuracy.
