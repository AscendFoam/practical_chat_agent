# T438: Persona Version Draft Review Linkage

## Task ID

T438

## Goal

Link the static `persona_version_draft_ledger` section into the Review
Workspace so reviewers can inspect each version draft, conflict note, rollback
ref, and outcome label from the same local review surface.

T438 must remain static and non-executing. It must not apply persona changes,
write stores, call model providers, read private data, send messages, connect
platform adapters, or enable media runtime.

## Context

T436 added the deterministic `persona_version_draft_ledger` adapter payload.
T437 renders that payload in the static text-first demo. The next slice should
make the version draft ledger visible in Review Workspace filters and cards,
matching the pattern used for session candidates, workbench review cards, and
evolution review cards.

## Allowed Files

Future T438 worker may create or modify only:

- `src/practical_chat_agent/ui/text_first_web_demo_adapter.py`
- `src/practical_chat_agent/ui/static/text_first_web_demo.css`
- `src/practical_chat_agent/ui/static/text_first_web_demo.js`
- `tests/test_persona_version_draft_review_linkage.py`
- `tests/test_persona_version_draft_ledger_payload.py`
- `tests/test_static_persona_version_draft_ledger.py`
- `tests/test_text_first_web_demo_local_server.py`
- `tests/test_text_first_web_demo_static.py`
- `tests/test_text_first_web_demo_state_switching.py`
- `docs/contracts/persona_version_draft_ledger_payload.md`
- `docs/tasks/M38_next_iteration/T439_persona_version_draft_responsive_hardening.md`
- `docs/worker_summary/T438_worker_summary.md`
- `docs/07_handoff.md`

If implementation requires new HTML anchors, package changes, private data,
source readers, model providers, runtime stores, platform adapters, outbound
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
`persona_version_draft_ledger`:

- one review card per version draft;
- one review card per conflict note;
- one review card per rollback ref;
- one review card per outcome label.

Cards should be appended to `review_workspace` in the same derived-state style
as existing session, workbench, and evolution review cards. Served JSON and
static fallback state should agree on counts and safety flags.

### 2. Review Filter

Add or update a Review Workspace filter tab:

- key: `version`;
- label: `Version`;
- count: derived version-draft review card count.

The existing `all`, `persona`, `distillation`, and `evolution` filters must
keep working.

### 3. Card Details

Each card should include enough static detail for review:

- source surface: `persona_version_draft_ledger`;
- card kind;
- draft outcome and included/excluded patch ids for draft cards;
- conflict code and mitigation for conflict cards;
- related draft ids, patch ids, and restore summary for rollback cards;
- outcome label and safe summary for outcome cards;
- preview-only and non-mutating status badges.

### 4. No Action Controls

The Review Workspace must not render buttons, forms, links, or commands that
imply apply, commit, mutate, clone, import, upload, record, connect, send,
publish, generate media, enable runtime, or activate an adapter.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'; pytest tests\test_persona_version_draft_review_linkage.py tests\test_static_persona_version_draft_ledger.py tests\test_text_first_web_demo_static.py tests\test_text_first_web_demo_state_switching.py -q -o cache_dir=artifacts\t438_pytest_cache --basetemp=artifacts\t438_pytest_basetemp
```

```powershell
$env:PYTHONPATH='src'; pytest tests\test_persona_version_draft_ledger_payload.py tests\test_text_first_web_demo_local_server.py -q -o cache_dir=artifacts\t438_server_cache --basetemp=artifacts\t438_server_basetemp
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

If a local static target is available, perform Browser QA:

- Review Workspace shows the Version filter with the expected count;
- version draft review cards are visible in Review Workspace;
- draft, conflict, rollback, and outcome details are present;
- no forbidden action controls appear;
- no horizontal overflow at the available narrow viewport.

## Reviewer Type

Static UI review for review-linkage accuracy, card count consistency,
non-execution language, and no forbidden action controls.
