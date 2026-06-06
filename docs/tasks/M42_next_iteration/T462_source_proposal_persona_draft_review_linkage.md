# T462: Source Proposal Persona Draft Review Linkage

## Task ID

T462

## Goal

Expose deterministic `source_proposal_persona_draft` records in the local
Review Workspace so reviewers can inspect draft field changes, unchanged
fields, conflict notes, rollback refs, gates, and outcomes next to the rest of
the companion review queue.

This task is Review Workspace linkage only. It must not add source readers,
private data access, model providers, embeddings, real extraction, store
writes, persona apply, outbound messaging, platform adapters, or media runtime.

## Context

T460 introduced the deterministic persona draft payload. T461 rendered the
payload in the static text-first demo. T462 should make the same draft records
reviewable through Review Workspace cards and a `Draft` filter without changing
runtime persona state.

T462 must preserve the distinction between:

- M41 persona proposal preview;
- M42 persona draft preview;
- future reviewed apply executor.

## Allowed Files

Future T462 worker may create or modify only:

- `src/practical_chat_agent/ui/text_first_web_demo_adapter.py`
- `src/practical_chat_agent/ui/static/text_first_web_demo.js`
- `tests/test_source_proposal_persona_draft_review_linkage.py`
- `tests/test_source_proposal_persona_draft_payload.py`
- `tests/test_text_first_web_demo_local_server.py`
- `tests/test_text_first_web_demo_static.py`
- `tests/test_text_first_web_demo_state_switching.py`
- `docs/contracts/source_proposal_persona_draft_payload.md`
- `docs/tasks/M42_next_iteration/T463_source_proposal_persona_draft_responsive_hardening.md`
- `docs/worker_summary/T462_worker_summary.md`
- `docs/07_handoff.md`

If implementation requires source readers, model providers, private data,
runtime stores, platform adapters, outbound messaging, media runtime,
automatic apply, package changes, or task-board edits, Captain must revise this
package before assignment.

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
- Do not add platform adapters, webhooks, auth, tokens, recipient ids, delivery
  state, automatic outreach, or outbound messaging.
- Do not add microphone, camera, ASR, TTS, voice cloning, Live2D, generated
  audio, generated image, generated video, or media capture.
- Do not add payment processing, production pricing claims, legal advice,
  compliance completion, app-store approval, launch approval, clinical claims,
  regulator acceptance, or user-study validation.
- Do not modify `docs/04_task_board.md`.

## Expected Implementation

- Add `review_workspace.source_draft_review_cards` to served demo state.
- Add deterministic cards for:
  - draft field changes;
  - unchanged field summaries;
  - conflict notes;
  - rollback refs;
  - review gate results;
  - draft outcome labels.
- Add a `Draft` filter tab.
- Update static fallback linkage so direct static HTML exposes draft review
  cards.
- Render draft review card detail rows in the existing Review Workspace card
  component.
- Keep all cards `review_required`, `preview_only`, `changes_state: false`,
  `mutation_allowed: false`, `automatic_apply: false`, `sends_messages: false`,
  and `runtime_ready: false`.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'; pytest tests\test_source_proposal_persona_draft_review_linkage.py tests\test_source_proposal_persona_draft_payload.py tests\test_text_first_web_demo_local_server.py tests\test_text_first_web_demo_static.py tests\test_text_first_web_demo_state_switching.py -q -o cache_dir=artifacts\t462_pytest_cache --basetemp=artifacts\t462_pytest_basetemp
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

## Reviewer Type

Review Workspace linkage review for persona draft visibility, deterministic
fallback behavior, safe detail rows, filter counts, and absence of execution
or action controls.
