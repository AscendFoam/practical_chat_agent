# T459: M42 Next Iteration Scope

## Task ID

T459

## Goal

Refine M42 as a local proposal-to-persona-draft preview milestone and create
the first implementation task package.

This task is docs-only. It must not modify product code, tests, static assets,
source readers, model providers, stores, platform adapters, outbound
messaging, or media runtime.

## Context

M41 closed with a local source-evidence-to-persona-proposal preview layer. The
next step is to show how reviewed proposal candidates could be assembled into
a PersonaCard draft preview while preserving review and non-mutation
boundaries.

## Allowed Files

Future T459 worker may create or modify only:

- `docs/product/m42_next_iteration_scope.md`
- `docs/tasks/M42_next_iteration/T460_source_proposal_persona_draft_payload.md`
- `docs/worker_summary/T459_worker_summary.md`
- `docs/07_handoff.md`

If implementation requires product code, tests, static assets, source readers,
model providers, private data, runtime stores, platform adapters, outbound
messaging, media runtime, automatic apply, package changes, or task-board
edits, Captain must revise this package before assignment.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not ingest, summarize, transform, quote, or commit real private chat
  records.
- Do not modify product code, tests, static assets, or package files.
- Do not call model providers or prompt execution layers.
- Do not add source readers, embeddings, vector search, semantic ranking,
  similarity scoring, fine-tuning, or remote inference.
- Do not write PersonaCard, PersonaVersionStore, MemoryEventStore, review
  stores, runtime stores, local databases, queues, schedulers, or files outside
  the allowed docs files.
- Do not add platform adapters, webhooks, auth, tokens, recipient ids, delivery
  state, automatic outreach, or outbound messaging.
- Do not add microphone, camera, ASR, TTS, voice cloning, Live2D, generated
  audio, generated image, generated video, or media capture.
- Do not add payment processing, production pricing claims, legal advice,
  compliance completion, app-store approval, launch approval, clinical claims,
  regulator acceptance, or user-study validation.
- Do not modify `docs/04_task_board.md`.

## Expected Output

Update the M42 scope with a concrete T460 implementation slice.

Create `docs/tasks/M42_next_iteration/T460_source_proposal_persona_draft_payload.md`
with:

- allowed files;
- forbidden scope;
- expected payload shape for `source_proposal_persona_draft`;
- required preview-only apply policy;
- required non-execution flags;
- focused verification commands.

## Verification

Minimum command:

```powershell
git diff --check
```

## Reviewer Type

Docs-only scope review for M42 proposal-to-persona-draft preview, task
boundaries, non-mutation guarantees, and next task readiness.
