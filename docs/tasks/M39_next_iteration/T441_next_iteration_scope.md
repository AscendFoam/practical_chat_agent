# T441: M39 Next Iteration Scope

## Task ID

T441

## Goal

Refine M39 into the first concrete implementation task for a local
`persona_source_intake_manifest` payload.

T441 is documentation-only. It must not add product code, tests, providers,
private data ingestion, source readers, runtime store writes, automatic apply,
outbound messaging, platform adapters, or media runtime.

## Context

M38 closed with `PASS_WITH_WARNINGS`: persona version drafts are visible,
reviewable, linked to Review Workspace, and responsive, but the product still
lacks an explicit consent-gated intake contract for future user-provided source
material.

M39 should introduce a local deterministic source intake manifest before any
real extraction work. The manifest should model source kind, declared owner,
consent state, minimization status, redaction profile, extraction eligibility,
blocked reasons, and review gates.

## Allowed Files

Future T441 worker may create or modify only:

- `docs/product/m39_next_iteration_scope.md`
- `docs/tasks/M39_next_iteration/T442_persona_source_intake_manifest_payload.md`
- `docs/worker_summary/T441_worker_summary.md`
- `docs/07_handoff.md`

If implementation requires code, tests, package changes, private data, source
readers, model providers, runtime stores, platform adapters, outbound
messaging, media runtime, automatic apply, or task-board edits, Captain must
create a separate task package.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not ingest, summarize, transform, quote, or commit real private chat
  records.
- Do not call model providers or prompt execution layers.
- Do not add source readers, embeddings, vector search, semantic ranking,
  similarity scoring, fine-tuning, or remote inference.
- Do not write PersonaCard, PersonaVersionStore, MemoryEventStore, review
  stores, runtime stores, local databases, queues, schedulers, or code files.
- Do not add platform adapters, webhooks, auth, tokens, recipient ids, delivery
  state, automatic outreach, or outbound messaging.
- Do not add microphone, camera, ASR, TTS, voice cloning, Live2D, generated
  audio, generated image, generated video, or media capture.
- Do not add payment processing, production pricing claims, legal advice,
  compliance completion, app-store approval, launch approval, clinical claims,
  regulator acceptance, or user-study validation.
- Do not modify `docs/04_task_board.md`.

## Expected Work

1. Refine `docs/product/m39_next_iteration_scope.md` if needed so the milestone
   has a concrete payload-first sequence.
2. Create
   `docs/tasks/M39_next_iteration/T442_persona_source_intake_manifest_payload.md`.
3. The T442 task package should define:
   - adapter payload fields;
   - contract tests;
   - deterministic synthetic source candidates;
   - source policy gate requirements;
   - blocked source category requirements;
   - redaction profile requirements;
   - extraction eligibility rules;
   - non-execution flags;
   - forbidden scope.
4. Create `docs/worker_summary/T441_worker_summary.md`.
5. Append handoff notes to `docs/07_handoff.md`.

## Verification

Minimum command:

```powershell
git diff --check
```

## Reviewer Type

Documentation/scope review for the next implementation task.
