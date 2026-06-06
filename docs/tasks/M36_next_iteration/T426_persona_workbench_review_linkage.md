# T426: Persona Workbench Review Linkage

## Task ID

T426

## Goal

Link `persona_distillation_workbench` trait candidates and blocked requests to
the existing review workspace surfaces as preview-only local review cards.

T426 should make workbench outputs visible in the Review Workspace without
adding automatic apply, runtime store writes, model providers, private data,
platform adapters, outbound messaging, or media runtime.

## Context

T424 added the deterministic workbench payload. T425 rendered the workbench in
the static demo. The next slice should connect the workbench to the existing
review workspace pattern so reviewers can inspect distillation candidates
alongside session candidates, manual previews, risk reviews, and audit
summaries.

## Allowed Files

Future T426 worker may create or modify only:

- `src/practical_chat_agent/ui/text_first_web_demo_adapter.py`
- `src/practical_chat_agent/ui/static/text_first_web_demo.js`
- `src/practical_chat_agent/ui/static/text_first_web_demo.css`
- `tests/test_persona_workbench_review_linkage.py`
- `tests/test_persona_distillation_workbench_payload.py`
- `tests/test_static_persona_distillation_workbench.py`
- `tests/test_session_review_candidate_linkage.py`
- `tests/test_review_workspace_apply_audit_panel.py`
- `docs/contracts/persona_distillation_workbench_payload.md`
- `docs/tasks/M36_next_iteration/T427_persona_workbench_responsive_hardening.md`
- `docs/worker_summary/T426_worker_summary.md`
- `docs/07_handoff.md`

If implementation requires private data, source readers, model providers,
package changes, runtime stores, platform adapters, outbound messaging, media
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
  the allowed docs/test/code/static files.
- Do not add platform adapters, webhooks, auth, tokens, recipient ids, delivery
  state, automatic outreach, or outbound messaging.
- Do not add microphone, camera, ASR, TTS, voice cloning, Live2D, generated
  audio, generated image, generated video, or media capture.
- Do not add payment processing, production pricing claims, legal advice,
  compliance completion, app-store approval, launch approval, clinical claims,
  regulator acceptance, or user-study validation.
- Do not modify `docs/04_task_board.md`.

## Expected Implementation

### 1. Adapter Review Cards

Update the adapter review workspace payload to include workbench-derived cards:

- one card per `extracted_trait_candidates` entry;
- one card per `blocked_requests` entry;
- filter key `distillation`;
- safe source surface `persona_distillation_workbench`;
- `review_required: true`;
- `preview_only: true`;
- `changes_state: false`;
- `mutation_allowed: false`;
- no automatic apply;
- no outbound messaging.

Trait cards should include category, candidate value, confidence band, evidence
ref ids, and safe summary.

Blocked request cards should show blocked status, request type, risk reason,
and user-facing explanation.

### 2. Static Fallback Review Cards

Update the static fallback `review_workspace` to include deterministic
workbench review cards and a non-zero `distillation` filter tab.

The existing review rendering should display the cards without action controls.
Add small CSS only if card type styling or wrapping requires it.

### 3. Tests

Add focused tests that verify:

- adapter review workspace includes distillation cards;
- trait candidate review cards have valid evidence refs and preview-only status;
- blocked request review cards have blocked status and no mutation;
- static fallback includes distillation review cards and filter count;
- review workspace rendering code displays workbench-specific details;
- recursive scans find no unsafe true states for provider calls, private-source
  reads, runtime writes, automatic apply, outbound messaging, adapter use, or
  media runtime.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'; pytest tests\test_persona_workbench_review_linkage.py tests\test_persona_distillation_workbench_payload.py tests\test_static_persona_distillation_workbench.py tests\test_session_review_candidate_linkage.py tests\test_review_workspace_apply_audit_panel.py -q -o cache_dir=artifacts\t426_pytest_cache --basetemp=artifacts\t426_pytest_basetemp
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

- Review scenario visible;
- distillation filter visible with non-zero count;
- workbench trait and blocked cards visible;
- no forbidden action controls;
- no horizontal overflow at the available narrow viewport.

## Reviewer Type

Code and static UI review for safe review-workspace linkage, preview-only
distillation cards, no mutation pathways, and no forbidden execution surfaces.
