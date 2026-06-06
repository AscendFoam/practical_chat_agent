# T432: Persona Evolution Review Linkage

## Task ID

T432

## Goal

Link the static `persona_evolution_preview` section into the Review Workspace
so reviewers can inspect each preview-only persona patch, risk label, rollback
note, and blocked source exclusion from the same local review surface.

T432 must remain static and non-executing. It must not apply persona changes,
write stores, call model providers, read private data, send messages, connect
platform adapters, or enable media runtime.

## Context

T430 added the deterministic `persona_evolution_preview` adapter payload. T431
renders that payload in the static text-first demo. The next slice should make
the evolution preview visible in Review Workspace filters and cards, matching
the pattern used for M35 session candidates and M36 workbench review cards.

## Allowed Files

Future T432 worker may create or modify only:

- `src/practical_chat_agent/ui/text_first_web_demo_adapter.py`
- `src/practical_chat_agent/ui/static/text_first_web_demo.css`
- `src/practical_chat_agent/ui/static/text_first_web_demo.js`
- `tests/test_persona_evolution_review_linkage.py`
- `tests/test_persona_evolution_preview_payload.py`
- `tests/test_text_first_web_demo_local_server.py`
- `tests/test_static_persona_evolution_preview.py`
- `tests/test_text_first_web_demo_static.py`
- `tests/test_text_first_web_demo_state_switching.py`
- `docs/contracts/persona_evolution_preview_payload.md`
- `docs/tasks/M37_next_iteration/T433_persona_evolution_responsive_hardening.md`
- `docs/worker_summary/T432_worker_summary.md`
- `docs/07_handoff.md`

If implementation requires HTML anchors, package changes, private data, source
readers, model providers, runtime stores, platform adapters, outbound
messaging, media runtime, automatic apply, or task-board edits, Captain must
revise this package before assignment.

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

### 1. Derived Review Cards

Add adapter and static JavaScript helpers that derive review cards from
`persona_evolution_preview`:

- one review card per proposed patch candidate;
- one review card per risk label;
- one review card per rollback note;
- one review card per blocked source exclusion.

Cards should be appended to `review_workspace` in the same derived-state style
as existing session candidate and persona workbench review cards. Served JSON
and static fallback state should agree on counts and safety flags.

### 2. Review Filter

Add or update a Review Workspace filter tab:

- key: `evolution`;
- label: `Evolution`;
- count: derived evolution review card count.

The existing `all`, `persona`, and `distillation` filters must keep working.

### 3. Card Details

Each card should include enough static detail for review:

- source surface: `persona_evolution_preview`;
- card kind;
- changed field path for patch cards;
- before and after summaries for patch cards;
- risk code and mitigation for risk cards;
- target patch ids and rollback summary for rollback cards;
- blocked request id and exclusion reason for exclusion cards;
- preview-only and non-mutating status badges.

### 4. No Action Controls

The Review Workspace must not render buttons, forms, links, or commands that
imply apply, commit, mutate, clone, import, upload, record, connect, send,
publish, generate media, enable runtime, or activate an adapter.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'; pytest tests\test_persona_evolution_review_linkage.py tests\test_static_persona_evolution_preview.py tests\test_text_first_web_demo_static.py tests\test_text_first_web_demo_state_switching.py -q -o cache_dir=artifacts\t432_pytest_cache --basetemp=artifacts\t432_pytest_basetemp
```

```powershell
$env:PYTHONPATH='src'; pytest tests\test_persona_evolution_preview_payload.py tests\test_text_first_web_demo_local_server.py -q -o cache_dir=artifacts\t432_server_cache --basetemp=artifacts\t432_server_basetemp
```

```powershell
node --check src\practical_chat_agent\ui\static\text_first_web_demo.js
```

```powershell
git diff --check
```

If a local static target is available, perform Browser QA:

- Review Workspace shows the Evolution filter with the expected count;
- evolution review cards are visible in Review Workspace;
- patch, risk, rollback, and exclusion details are present;
- no forbidden action controls appear;
- no horizontal overflow at the available narrow viewport.

## Reviewer Type

Static UI review for review-linkage accuracy, card count consistency,
non-execution language, and no forbidden action controls.
