# T463: Source Proposal Persona Draft Responsive Hardening

## Task ID

T463

## Goal

Harden the static layout for `source_proposal_persona_draft` and its Review
Workspace draft cards so dense field paths, ids, evidence refs, rollback refs,
and gate refs wrap cleanly in narrow viewports.

This task is CSS/static test hardening only. It must not add adapter payload
changes, source readers, private data access, model providers, embeddings,
real extraction, store writes, persona apply, outbound messaging, platform
adapters, or media runtime.

## Context

T460 introduced the draft payload. T461 rendered the draft section. T462 linked
draft records into Review Workspace. T463 should make the draft section and
draft review cards robust against long ids and mobile widths before M42 review.

## Allowed Files

Future T463 worker may create or modify only:

- `src/practical_chat_agent/ui/static/text_first_web_demo.css`
- `tests/test_source_proposal_persona_draft_responsive_hardening.py`
- `tests/test_static_source_proposal_persona_draft.py`
- `tests/test_source_proposal_persona_draft_review_linkage.py`
- `tests/test_text_first_web_demo_static.py`
- `tests/test_text_first_web_demo_state_switching.py`
- `docs/tasks/M42_next_iteration/T464_m42_milestone_review.md`
- `docs/worker_summary/T463_worker_summary.md`
- `docs/07_handoff.md`

If implementation requires Python adapter payload changes, JavaScript behavior
changes, HTML structure changes, source readers, model providers, private data,
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
- Do not modify Python adapter payload code in this task.
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

- Add or verify wrapping guards for `.source-draft-review-card`.
- Ensure draft card titles, status badges, detail lists, and meta rows cannot
  overflow their parent cards.
- Ensure the draft section, draft layout, draft grid, selected proposal labels,
  field change cards, unchanged cards, conflict cards, rollback cards, gate
  cards, and outcome cards have explicit narrow-viewport behavior.
- Create `docs/tasks/M42_next_iteration/T464_m42_milestone_review.md`.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'; pytest tests\test_source_proposal_persona_draft_responsive_hardening.py tests\test_static_source_proposal_persona_draft.py tests\test_source_proposal_persona_draft_review_linkage.py tests\test_text_first_web_demo_static.py tests\test_text_first_web_demo_state_switching.py -q -o cache_dir=artifacts\t463_pytest_cache --basetemp=artifacts\t463_pytest_basetemp
```

```powershell
git diff --check
```

## Reviewer Type

Static responsive hardening review for source proposal persona draft section
and Review Workspace draft cards.
