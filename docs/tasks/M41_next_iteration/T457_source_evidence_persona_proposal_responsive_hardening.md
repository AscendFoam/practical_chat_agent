# T457: Source Evidence Persona Proposal Responsive Hardening

## Task ID

T457

## Goal

Harden responsive layout and text wrapping for the source evidence persona
proposal section and Review Workspace proposal cards.

This task is CSS/static-test and milestone-packaging only. It must not change
adapter payload semantics, add source readers, read private data, call model
providers, create embeddings, extract traits, write stores, apply persona
changes, send messages, connect platform adapters, or enable media runtime.

## Context

T454 introduced the deterministic proposal payload. T455 rendered it in the
static demo. T456 linked proposal records into Review Workspace. T457 should
make dense proposal ids, field paths, evidence refs, risk refs, rollback refs,
and gate refs wrap safely on narrow viewports, then prepare the M41 milestone
review task.

## Allowed Files

Future T457 worker may create or modify only:

- `src/practical_chat_agent/ui/static/text_first_web_demo.css`
- `tests/test_source_evidence_persona_proposal_responsive_hardening.py`
- `docs/tasks/M41_next_iteration/T458_m41_milestone_review.md`
- `docs/worker_summary/T457_worker_summary.md`
- `docs/07_handoff.md`

If implementation requires adapter payload changes, JavaScript behavior
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
- Do not modify static HTML or JavaScript in this task unless the task package
  is revised.
- Do not write PersonaCard, PersonaVersionStore, MemoryEventStore, review
  stores, runtime stores, local databases, queues, schedulers, or files outside
  the allowed files.
- Do not add platform adapters, webhooks, auth, tokens, recipient ids, delivery
  state, automatic outreach, or outbound messaging.
- Do not add microphone, camera, ASR, TTS, voice cloning, Live2D, generated
  audio, generated image, generated video, or media capture.
- Do not add payment processing, production pricing claims, legal advice,
  compliance completion, app-store approval, launch approval, clinical claims,
  regulator acceptance, or user-study validation.
- Do not modify `docs/04_task_board.md`.

## Expected Implementation

- Add responsive wrapping tests for:
  - `.source-evidence-persona-proposal`;
  - `.source-proposal-card`;
  - `.source-proposal-risk-card`;
  - `.source-proposal-rollback-card`;
  - `.source-proposal-gate-card`;
  - `.source-proposal-outcome-card`;
  - `.source-proposal-review-card`.
- Ensure proposal lists, non-execution labels, matrix summary, item titles,
  item metadata, status badges, and Review Workspace detail rows have
  `min-width: 0` and wrapping guards.
- Ensure mobile media rules include source proposal section, proposal grids,
  proposal section heads, proposal labels, and proposal review-card detail
  rows.
- Create `docs/tasks/M41_next_iteration/T458_m41_milestone_review.md`.

## Browser QA

After tests pass, verify proposal section and Review Workspace proposal cards
at desktop and narrow viewport if a browser automation target is available:

- proposal section renders without horizontal overflow;
- proposal candidate, risk, rollback, gate, and outcome cards wrap cleanly;
- Review Workspace proposal cards render without clipped ids;
- no forbidden action controls appear.

If no callable browser automation tool is available, do not claim browser QA.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'; pytest tests\test_source_evidence_persona_proposal_responsive_hardening.py tests\test_static_source_evidence_persona_proposal.py tests\test_source_evidence_persona_proposal_review_linkage.py tests\test_text_first_web_demo_static.py tests\test_text_first_web_demo_state_switching.py -q -o cache_dir=artifacts\t457_pytest_cache --basetemp=artifacts\t457_pytest_basetemp
```

```powershell
git diff --check
```

## Reviewer Type

Responsive CSS/static hardening review for proposal section, Review Workspace
proposal cards, mobile wrapping, and absence of new action controls.
