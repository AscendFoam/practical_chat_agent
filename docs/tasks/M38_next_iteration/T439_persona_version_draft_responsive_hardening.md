# T439: Persona Version Draft Responsive Hardening

## Task ID

T439

## Goal

Harden the persona version draft ledger and Review Workspace version cards for
narrow viewports, long patch ids, conflict text, rollback refs, and dense
outcome metadata.

T439 is a static UI hardening task. It must not alter version ledger
semantics, apply persona changes, write stores, call model providers, read
private data, send messages, connect platform adapters, or enable media
runtime.

## Context

T437 rendered the static `persona_version_draft_ledger` section. T438 linked
version draft items into Review Workspace. The next slice should focus on
layout resilience before milestone review: no horizontal overflow, no cramped
badge rows, readable draft/conflict/rollback/outcome cards, and stable behavior
at the available narrow browser viewport.

## Allowed Files

Future T439 worker may create or modify only:

- `src/practical_chat_agent/ui/static/text_first_web_demo.css`
- `tests/test_persona_version_draft_responsive_hardening.py`
- `tests/test_persona_version_draft_review_linkage.py`
- `tests/test_static_persona_version_draft_ledger.py`
- `tests/test_text_first_web_demo_static.py`
- `tests/test_text_first_web_demo_state_switching.py`
- `docs/tasks/M38_next_iteration/T440_m38_milestone_review.md`
- `docs/worker_summary/T439_worker_summary.md`
- `docs/07_handoff.md`

If implementation requires JavaScript behavior changes, adapter payload
changes, HTML anchors, package changes, private data, source readers, model
providers, runtime stores, platform adapters, outbound messaging, media
runtime, automatic apply, or task-board edits, Captain must revise this package
before assignment.

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
  the allowed docs/test/static files.
- Do not add platform adapters, webhooks, auth, tokens, recipient ids, delivery
  state, automatic outreach, or outbound messaging.
- Do not add microphone, camera, ASR, TTS, voice cloning, Live2D, generated
  audio, generated image, generated video, or media capture.
- Do not add payment processing, production pricing claims, legal advice,
  compliance completion, app-store approval, launch approval, clinical claims,
  regulator acceptance, or user-study validation.
- Do not modify `docs/04_task_board.md`.

## Expected Implementation

### 1. Responsive CSS Coverage

Add static CSS tests and CSS rules covering:

- `.persona-version-ledger`;
- `.version-ledger-layout`;
- `.version-draft-grid`;
- `.version-conflict-grid`;
- `.version-rollback-grid`;
- `.version-draft-card`;
- `.version-conflict-card`;
- `.version-rollback-card`;
- `.version-outcome-card`;
- `.persona-version-review-card`;
- `.persona-version-review-card .review-detail-list`;
- version non-execution labels and badge rows.

### 2. Narrow Viewport Stability

At `max-width: 720px`, version ledger and review cards should collapse to a
single column, align labels and badges to the start, and wrap long patch ids,
draft ids, conflict codes, mitigation summaries, rollback refs, and outcome
labels.

### 3. No Behavioral Changes

Do not change card counts, payload fields, filter tabs, review semantics, or
fallback data. This task should be CSS-only plus tests/docs.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'; pytest tests\test_persona_version_draft_responsive_hardening.py tests\test_persona_version_draft_review_linkage.py tests\test_static_persona_version_draft_ledger.py tests\test_text_first_web_demo_static.py tests\test_text_first_web_demo_state_switching.py -q -o cache_dir=artifacts\t439_pytest_cache --basetemp=artifacts\t439_pytest_basetemp
```

```powershell
node --check src\practical_chat_agent\ui\static\text_first_web_demo.js
```

```powershell
git diff --check
```

If a local static target is available, perform Browser QA:

- version ledger section has no horizontal overflow;
- Review Workspace version cards have no horizontal overflow;
- badges and detail lists wrap cleanly;
- no forbidden action controls appear;
- no layout overlap at the available narrow viewport.

## Reviewer Type

Static responsive UI review for version draft ledger and Review Workspace
version cards.
