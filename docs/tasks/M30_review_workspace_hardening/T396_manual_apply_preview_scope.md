# T396: Manual Apply Preview Scope

## Task ID

T396

## Goal

Design the next milestone for manual apply preview without implementing any
state mutation.

T396 should convert M30 hardening results into a scoped plan for review-only
manual apply previews. The plan must define what a reviewer can inspect before
apply, what remains non-executing, and which gates must exist before any real
memory/persona mutation executor can be implemented.

## Allowed Files

Future T396 worker may create or modify only:

- `docs/product/m31_manual_apply_preview_scope.md`
- `docs/tasks/M31_manual_apply_preview/T397_manual_apply_preview_records.md`
- `docs/worker_summary/T396_worker_summary.md`
- `docs/07_handoff.md`

If T396 needs code changes, tests, private data, Browser runs, model-provider
calls, package changes, routes, CLIs, platform adapters, outbound messaging,
voice/avatar runtime, media generation, persistence outside local docs, or
apply executors, Captain must revise this package before assignment.

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

- M31 scope document for manual apply preview.
- First M31 task package for non-mutating manual apply preview records.
- Worker summary and handoff.
- Explicit list of gates required before any future apply executor.

## Verification

Minimum command:

```powershell
git diff --check
```

## Reviewer Type

Adversarial product/safety scope review for manual apply preview boundaries,
non-mutation guarantees, privacy, and documentation accuracy.
