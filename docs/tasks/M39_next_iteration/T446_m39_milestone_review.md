# T446: M39 Milestone Review

## Task ID

T446

## Goal

Review M39 as a completed milestone slice and decide whether the consent-gated
source intake manifest loop is ready to close with warnings or needs another
pre-review fix.

This task is review/documentation only. It must not add product code,
providers, private data ingestion, source readers, runtime store writes,
automatic apply, outbound messaging, platform adapters, or media runtime.

## Context

M39 added a controlled persona source intake path:

- T441 refined the M39 scope.
- T442 added the deterministic adapter payload and contract.
- T443 rendered the static source intake manifest section.
- T444 linked source intake items into Review Workspace.
- T445 hardened dense source intake and Review Workspace source layouts for
  narrow viewports.

The milestone review should inspect whether the local prototype now exposes a
safe, reviewable source-intake loop: synthetic source candidates, explicit
consent and ownership, minimization, redaction profiles, extraction
eligibility, blocked categories, policy gates, Review Workspace source cards,
and responsive safety.

## Allowed Files

Future T446 reviewer may create or modify only:

- `docs/review/M39_review.md`
- `docs/product/m40_next_iteration_scope.md`
- `docs/tasks/M40_next_iteration/T447_next_iteration_scope.md`
- `docs/worker_summary/T446_worker_summary.md`
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

Read the M39 task outputs and verify:

- payload contract coverage for `persona_source_intake_manifest`;
- static UI anchors and fallback rendering;
- Review Workspace linkage count and card-kind consistency;
- responsive hardening for manifest and source review cards;
- non-execution flags remain safe;
- no private data or provider paths were introduced;
- Browser QA evidence exists for T443, T444, and T445.

## Expected Outputs

1. `docs/review/M39_review.md`
   - verdict: `PASS`, `PASS_WITH_WARNINGS`, or `BLOCK`;
   - reviewed files/tasks;
   - findings with severity;
   - verification evidence;
   - residual risks.

2. `docs/product/m40_next_iteration_scope.md`
   - next milestone scope based on M39 review.

3. `docs/tasks/M40_next_iteration/T447_next_iteration_scope.md`
   - next task package.

4. `docs/worker_summary/T446_worker_summary.md`
   - reviewer summary and non-actions.

5. Append handoff notes to `docs/07_handoff.md`.

## Verification

Minimum command:

```powershell
git diff --check
```

If the reviewer chooses to rerun code checks, prefer the latest M39 focused
tests:

```powershell
$env:PYTHONPATH='src'; pytest tests\test_persona_source_intake_manifest_payload.py tests\test_static_persona_source_intake_manifest.py tests\test_persona_source_intake_review_linkage.py tests\test_persona_source_intake_responsive_hardening.py tests\test_text_first_web_demo_local_server.py tests\test_text_first_web_demo_static.py tests\test_text_first_web_demo_state_switching.py -q -o cache_dir=artifacts\t446_pytest_cache --basetemp=artifacts\t446_pytest_basetemp
```

## Reviewer Type

Milestone review for M39 consent-gated source intake readiness.
