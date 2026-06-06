# T458: M41 Milestone Review

## Task ID

T458

## Goal

Review M41 as the local source-evidence-to-persona-proposal preview milestone.

This task is review/docs-only. It must not modify product code, tests,
payloads, static assets, source readers, model providers, stores, platform
adapters, outbound messaging, or media runtime.

## Context

M41 currently consists of:

- T453: M41 scope refinement and T454 package.
- T454: `source_evidence_persona_proposal` payload and contract tests.
- T455: static source proposal UI rendering.
- T456: Review Workspace proposal linkage.
- T457: responsive hardening for proposal UI and proposal review cards.

The milestone should evaluate whether M41 safely bridges M40 source evidence
matrix records into preview-only persona proposal candidates while preserving
the distinction between evidence preview, persona proposal review, and actual
persona apply.

## Allowed Files

Future T458 worker may create or modify only:

- `docs/review/M41_review.md`
- `docs/product/m42_next_iteration_scope.md`
- `docs/tasks/M42_next_iteration/T459_next_iteration_scope.md`
- `docs/worker_summary/T458_worker_summary.md`
- `docs/07_handoff.md`

If review requires code, static asset, test, adapter, source reader, model
provider, private data, store, platform adapter, outbound messaging, media
runtime, automatic apply, package, or task-board changes, Captain must revise
this package before assignment.

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

## Review Checklist

Review M41 evidence:

- T454 payload shape and contract tests;
- T455 static UI rendering and fallback state;
- T456 Review Workspace linkage;
- T457 responsive hardening;
- non-execution flags and apply policy;
- absence of private/source-reader/provider/extraction/embedding/store/write/
  outbound/platform/media runtime behavior;
- remaining Browser QA gaps if browser automation was unavailable.

The review verdict should be one of:

- `PASS`;
- `PASS_WITH_WARNINGS`;
- `BLOCK`.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'; pytest tests\test_source_evidence_persona_proposal_payload.py tests\test_static_source_evidence_persona_proposal.py tests\test_source_evidence_persona_proposal_review_linkage.py tests\test_source_evidence_persona_proposal_responsive_hardening.py tests\test_text_first_web_demo_local_server.py tests\test_text_first_web_demo_static.py tests\test_text_first_web_demo_state_switching.py -q -o cache_dir=artifacts\t458_pytest_cache --basetemp=artifacts\t458_pytest_basetemp
```

```powershell
python -m py_compile src\practical_chat_agent\ui\text_first_web_demo_adapter.py
```

```powershell
node --check src\practical_chat_agent\ui\static\text_first_web_demo.js
```

```powershell
git diff --check
```

## Expected Outputs

- `docs/review/M41_review.md`
- `docs/product/m42_next_iteration_scope.md`
- `docs/tasks/M42_next_iteration/T459_next_iteration_scope.md`
- `docs/worker_summary/T458_worker_summary.md`
- updated `docs/07_handoff.md`

## Reviewer Type

Milestone review for M41 source-evidence-to-persona-proposal preview,
non-extraction, non-mutation, UI/review visibility, responsive hardening,
remaining risks, and next-iteration scope.
