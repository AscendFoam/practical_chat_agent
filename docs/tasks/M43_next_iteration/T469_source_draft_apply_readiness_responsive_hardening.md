# T469: Source Draft Apply Readiness Responsive Hardening

## Task ID

T469

## Goal

Harden the static text-first demo layout for `source_draft_apply_readiness`
and its Review Workspace cards so long readiness ids, outcomes, blocked
condition labels, gate refs, rollback refs, and detail rows wrap cleanly on
desktop and narrow screens.

This task is responsive/static hardening only. It must not add source readers,
private data access, model providers, embeddings, real extraction, store
writes, persona apply, outbound messaging, platform adapters, or media
runtime.

## Context

T466 added the deterministic apply-readiness payload. T467 rendered the
readiness section in the static demo. T468 linked readiness records into the
Review Workspace through `source_readiness_review_cards` and the `Readiness`
filter. T469 should make the readiness section and review cards robust for
long synthetic ids and mobile layouts before M43 review.

## Allowed Files

Future T469 worker may create or modify only:

- `src/practical_chat_agent/ui/static/text_first_web_demo.css`
- `tests/test_source_draft_apply_readiness_responsive_hardening.py`
- `tests/test_static_source_draft_apply_readiness.py`
- `tests/test_source_draft_apply_readiness_review_linkage.py`
- `tests/test_text_first_web_demo_static.py`
- `tests/test_text_first_web_demo_state_switching.py`
- `docs/tasks/M43_next_iteration/T470_m43_milestone_review.md`
- `docs/worker_summary/T469_worker_summary.md`
- `docs/07_handoff.md`

If implementation requires adapter payload changes, JavaScript changes,
source readers, model providers, private data, runtime stores, platform
adapters, outbound messaging, media runtime, automatic apply, package changes,
or task-board edits, Captain must revise this package before assignment.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not ingest, summarize, transform, quote, or commit real private chat
  records.
- Do not call model providers or prompt execution layers.
- Do not add source readers, embeddings, vector search, semantic ranking,
  similarity scoring, fine-tuning, or remote inference.
- Do not write PersonaCard, PersonaVersionStore, MemoryEventStore, review
  stores, runtime stores, local databases, queues, schedulers, or files outside
  the allowed static/test/docs files.
- Do not add platform adapters, webhooks, auth, tokens, recipient ids,
  delivery state, automatic outreach, or outbound messaging.
- Do not add microphone, camera, ASR, TTS, voice cloning, Live2D, generated
  audio, generated image, generated video, or media capture.
- Do not add payment processing, production pricing claims, legal advice,
  compliance completion, app-store approval, launch approval, clinical claims,
  regulator acceptance, or user-study validation.
- Do not modify `docs/04_task_board.md`.

## Expected Implementation

- Add focused CSS coverage for `.source-draft-apply-readiness` child layouts,
  readiness cards, condition/gate/rollback/outcome cards, and
  `.source-readiness-review-card`.
- Ensure long ids and summaries wrap via `min-width: 0`, `overflow-wrap:
  anywhere`, and stable grid/mobile rules.
- Ensure mobile rules explicitly cover readiness section grids, labels,
  card titles, item meta rows, status badges, and review detail rows.
- Create the T470 milestone review task package.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'; pytest tests\test_source_draft_apply_readiness_responsive_hardening.py tests\test_static_source_draft_apply_readiness.py tests\test_source_draft_apply_readiness_review_linkage.py tests\test_text_first_web_demo_static.py tests\test_text_first_web_demo_state_switching.py -q -o cache_dir=artifacts\t469_pytest_cache --basetemp=artifacts\t469_pytest_basetemp
```

```powershell
git diff --check
```

## Reviewer Type

Responsive static UI review for readiness section and readiness review cards,
with emphasis on wrapping, mobile layout, and absence of action controls.
