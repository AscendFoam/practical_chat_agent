# T435: M38 Next Iteration Scope

## Task ID

T435

## Goal

Refine M38 into the first concrete implementation task for a local
`persona_version_draft_ledger` payload.

T435 is documentation-only. It must not add product code, tests, providers,
private data ingestion, runtime store writes, automatic apply, outbound
messaging, platform adapters, or media runtime.

## Context

M37 closed with `PASS_WITH_WARNINGS`: persona evolution patches are visible,
reviewable, linked to Review Workspace, and responsive, but still cannot become
auditable version drafts or apply-ready records.

M38 should introduce a local, deterministic ledger that groups reviewed
evolution patches into version drafts with explicit outcomes, conflict notes,
and rollback refs. This prepares a later apply milestone without mutating
runtime state.

## Allowed Files

Future T435 worker may create or modify only:

- `docs/product/m38_next_iteration_scope.md`
- `docs/tasks/M38_next_iteration/T436_persona_version_draft_ledger_payload.md`
- `docs/worker_summary/T435_worker_summary.md`
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

1. Refine `docs/product/m38_next_iteration_scope.md` if needed so the milestone
   has a concrete payload-first sequence.
2. Create `docs/tasks/M38_next_iteration/T436_persona_version_draft_ledger_payload.md`.
3. The T436 task package should define:
   - adapter payload fields;
   - contract tests;
   - source linkage to `persona_evolution_preview`;
   - draft outcomes;
   - conflict note requirements;
   - rollback ref requirements;
   - non-execution flags;
   - forbidden scope.
4. Create `docs/worker_summary/T435_worker_summary.md`.
5. Append handoff notes to `docs/07_handoff.md`.

## Verification

Minimum command:

```powershell
git diff --check
```

## Reviewer Type

Documentation/scope review for the next implementation task.
