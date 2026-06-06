# T434: M37 Milestone Review

## Task ID

T434

## Goal

Review M37 as a completed milestone slice and decide whether the persona
evolution preview loop is ready to close with warnings or needs another
pre-review fix.

This task is review/documentation only. It must not add product code,
providers, private data ingestion, runtime store writes, automatic apply,
outbound messaging, platform adapters, or media runtime.

## Context

M37 added a controlled persona evolution preview path:

- T430 added the deterministic adapter payload and contract.
- T431 rendered the static persona evolution preview section.
- T432 linked evolution preview items into Review Workspace.
- T433 hardened dense evolution layouts for narrow viewports.

The milestone review should inspect whether the local prototype now exposes a
safe, reviewable persona evolution loop: source workbench linkage, before
snapshot, patch proposals, risks, rollbacks, blocked source exclusions, Review
Workspace cards, and responsive safety.

## Allowed Files

Future T434 reviewer may create or modify only:

- `docs/review/M37_review.md`
- `docs/product/m38_next_iteration_scope.md`
- `docs/tasks/M38_next_iteration/T435_next_iteration_scope.md`
- `docs/worker_summary/T434_worker_summary.md`
- `docs/07_handoff.md`

If review requires code, tests, package changes, private data, source readers,
model providers, runtime stores, platform adapters, outbound messaging, media
runtime, automatic apply, or task-board edits, Captain must create a separate
task package before implementation.

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

## Expected Review

Read the M37 task outputs and verify:

- payload contract coverage for `persona_evolution_preview`;
- static UI anchors and fallback rendering;
- Review Workspace linkage count and card-kind consistency;
- responsive hardening for evolution section and review cards;
- non-execution flags remain safe;
- no private data or provider paths were introduced;
- Browser QA evidence exists for T431, T432, and T433.

## Expected Outputs

1. `docs/review/M37_review.md`
   - verdict: `PASS`, `PASS_WITH_WARNINGS`, or `BLOCK`;
   - reviewed files/tasks;
   - findings with severity;
   - verification evidence;
   - residual risks.

2. `docs/product/m38_next_iteration_scope.md`
   - next milestone scope based on M37 review.

3. `docs/tasks/M38_next_iteration/T435_next_iteration_scope.md`
   - next task package.

4. `docs/worker_summary/T434_worker_summary.md`
   - reviewer summary and non-actions.

5. Append handoff notes to `docs/07_handoff.md`.

## Verification

Minimum command:

```powershell
git diff --check
```

If the reviewer chooses to rerun code checks, prefer the latest M37 focused
tests:

```powershell
$env:PYTHONPATH='src'; pytest tests\test_persona_evolution_preview_payload.py tests\test_persona_evolution_review_linkage.py tests\test_persona_evolution_responsive_hardening.py tests\test_static_persona_evolution_preview.py tests\test_text_first_web_demo_local_server.py tests\test_text_first_web_demo_static.py tests\test_text_first_web_demo_state_switching.py -q -o cache_dir=artifacts\t434_pytest_cache --basetemp=artifacts\t434_pytest_basetemp
```

## Reviewer Type

Milestone review for M37 persona evolution preview readiness.
