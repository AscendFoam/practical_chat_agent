# T455: Source Evidence Persona Proposal UI

## Task ID

T455

## Goal

Render the local `source_evidence_persona_proposal` payload in the static
text-first web demo.

This task is static rendering only. It must not add adapter payload changes,
source readers, private data access, model providers, embeddings, real
extraction, store writes, persona apply, outbound messaging, platform adapters,
or media runtime.

## Context

T454 introduced the deterministic proposal payload and contract tests. T455
should make the proposal visible in the demo so reviewers can inspect proposed
persona fields, source trait refs, evidence refs, confidence bands, risk
labels, rollback notes, review gates, outcomes, and non-execution labels.

T455 must preserve the distinction between:

- M40 source evidence matrix;
- M41 persona proposal preview;
- future reviewed apply executor.

## Allowed Files

Future T455 worker may create or modify only:

- `src/practical_chat_agent/ui/static/text_first_web_demo.html`
- `src/practical_chat_agent/ui/static/text_first_web_demo.css`
- `src/practical_chat_agent/ui/static/text_first_web_demo.js`
- `tests/test_static_source_evidence_persona_proposal.py`
- `tests/test_text_first_web_demo_static.py`
- `tests/test_text_first_web_demo_state_switching.py`
- `docs/contracts/source_evidence_persona_proposal_payload.md`
- `docs/tasks/M41_next_iteration/T456_source_evidence_persona_proposal_review_linkage.md`
- `docs/worker_summary/T455_worker_summary.md`
- `docs/07_handoff.md`

If implementation requires Python adapter payload changes, source readers,
model providers, private data, runtime stores, platform adapters, outbound
messaging, media runtime, automatic apply, package changes, or task-board
edits, Captain must revise this package before assignment.

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

- Add static anchors for the persona proposal section.
- Render from both embedded state and JavaScript fallback state.
- Show source evidence matrix linkage, proposal candidates, risk labels,
  rollback notes, review gate results, proposal outcome labels, apply policy,
  and non-execution flags.
- Candidate cards should show persona field path, proposed value summary,
  confidence band, rationale summary, source trait refs, evidence refs, risk
  refs, rollback refs, review gate refs, `preview_only`, and
  `mutation_allowed: false`.
- Do not include controls that imply import, upload, read, retain, extract,
  embed, apply, commit, mutate, clone, connect, send, publish, media
  generation, adapter activation, store-write, or runtime enablement.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'; pytest tests\test_static_source_evidence_persona_proposal.py tests\test_text_first_web_demo_static.py tests\test_text_first_web_demo_state_switching.py -q -o cache_dir=artifacts\t455_pytest_cache --basetemp=artifacts\t455_pytest_basetemp
```

```powershell
node --check src\practical_chat_agent\ui\static\text_first_web_demo.js
```

```powershell
git diff --check
```

## Reviewer Type

Static UI review for persona proposal visibility, deterministic fallback
behavior, safe non-execution labeling, responsive wrapping, and absence of
action controls.
