# T449: Persona Source Evidence Matrix UI

## Task ID

T449

## Goal

Render the local `persona_source_evidence_matrix` payload in the static
text-first web demo.

This task is static rendering only. It must not add source readers, read
private data, call model providers, create embeddings, extract traits, write
stores, apply persona changes, send messages, connect platform adapters, or
enable media runtime.

## Context

T448 introduced the deterministic source evidence matrix payload and contract
tests. T449 should make that matrix visible in the static demo so reviewers can
inspect eligible sources, excluded sources, evidence rows, trait hypotheses,
quality labels, review gates, and non-execution labels before any future Review
Workspace linkage task.

## Allowed Files

Future T449 worker may create or modify only:

- `src/practical_chat_agent/ui/static/text_first_web_demo.html`
- `src/practical_chat_agent/ui/static/text_first_web_demo.css`
- `src/practical_chat_agent/ui/static/text_first_web_demo.js`
- `tests/test_static_persona_source_evidence_matrix.py`
- `tests/test_text_first_web_demo_static.py`
- `tests/test_text_first_web_demo_state_switching.py`
- `docs/contracts/persona_source_evidence_matrix_payload.md`
- `docs/tasks/M40_next_iteration/T450_persona_source_evidence_review_linkage.md`
- `docs/worker_summary/T449_worker_summary.md`
- `docs/07_handoff.md`

If implementation requires adapter payload changes, source readers, model
providers, private data, runtime stores, platform adapters, outbound messaging,
media runtime, automatic apply, package changes, or task-board edits, Captain
must revise this package before assignment.

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

- Add static anchors for the evidence matrix section.
- Render from both embedded state and JavaScript fallback state.
- Show source manifest linkage, eligible source ids, excluded source refs,
  evidence rows, trait hypotheses, quality labels, review gate results, and
  non-execution flags.
- Do not include controls that imply import, upload, read, retain, extract,
  embed, apply, commit, mutate, clone, connect, send, publish, media generation,
  adapter activation, store-write, or runtime enablement.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'; pytest tests\test_static_persona_source_evidence_matrix.py tests\test_text_first_web_demo_static.py tests\test_text_first_web_demo_state_switching.py -q -o cache_dir=artifacts\t449_pytest_cache --basetemp=artifacts\t449_pytest_basetemp
```

```powershell
node --check src\practical_chat_agent\ui\static\text_first_web_demo.js
```

```powershell
git diff --check
```

## Reviewer Type

Static UI review for evidence matrix visibility, deterministic fallback
behavior, safe non-execution labeling, responsive wrapping, and absence of
action controls.
