# T389: Review Workspace Presentation Adapter

## Task ID

T389

## Goal

Implement local, deterministic presentation view models for review workspace
records.

T389 should convert `ReviewWorkspaceBundle`, `ReviewDecisionImpactPreview`,
and `ReviewWorkspaceSafeExportManifest` records into UI-ready safe cards,
filters, counts, and status summaries for a later local static review panel.
It must not create UI assets, apply decisions, mutate memory/persona state,
call providers, send messages, or connect to platforms/media.

## Why Now

M29 starts by building the presentation adapter before static UI work. This
keeps review workspace semantics testable in Python before binding them to the
existing text-first web demo assets.

## Allowed Files

Future T389 worker may create or modify only:

- `src/practical_chat_agent/ui/review_workspace_adapter.py`
- `tests/test_review_workspace_presentation_adapter.py`
- `docs/data_contracts/review_workspace_presentation_contract.md`
- `docs/tasks/M29_review_workspace_ui/T390_review_workspace_static_panel.md`
- `docs/worker_summary/T389_worker_summary.md`
- `docs/07_handoff.md`

If T389 needs other source files, fixtures, task-board edits, private data,
Browser runs, model-provider calls, package changes, routes, CLIs, platform
adapters, outbound messaging, voice/avatar runtime, media generation,
persistence outside local records, UI asset edits, or apply executors, Captain
must revise this package before assignment.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not ingest, summarize, transform, quote, or commit real private chat
  records.
- Do not call model providers.
- Do not implement source readers, extraction from real logs, embeddings,
  vector search, semantic ranking, fine-tuning, similarity scoring, persona
  synthesis, final companion reply generation, runtime persona mutation, or
  runtime memory mutation.
- Do not apply review decisions or dry-run plans.
- Do not mutate memory stores, PersonaCard objects, or PersonaVersionStore.
- Do not create static UI assets, routes, CLIs, schedulers, queues, webhooks,
  auth, tokens, recipient ids, delivery state, or platform persistence
  behavior.
- Do not implement proactive candidates, automatic outreach, sending,
  scheduling, notifications, platform delivery, microphone, camera, ASR, TTS,
  voice cloning, voice/avatar likeness, Live2D, generated audio, generated
  image, generated video, or media capture.
- Do not modify `docs/04_task_board.md`.
- Do not claim launch approval, legal compliance, app-store acceptance,
  clinical validation, regulator acceptance, user-study validation, or real
  user evidence.

## Inputs To Read

Required:

- `docs/product/m29_review_workspace_ui_scope.md`
- `docs/data_contracts/review_workspace_binding_contract.md`
- `docs/data_contracts/review_decision_impact_preview_contract.md`
- `docs/data_contracts/review_workspace_safe_export_contract.md`
- `src/practical_chat_agent/services/review_workspace.py`
- `src/practical_chat_agent/services/review_decision_impact_preview.py`
- `src/practical_chat_agent/services/review_workspace_export.py`
- relevant M28 tests.

## Expected Outputs

### 1. Presentation Records And Adapter

Create `src/practical_chat_agent/ui/review_workspace_adapter.py` with:

- `ReviewWorkspaceStatusBadge`
- `ReviewWorkspacePresentationCard`
- `ReviewWorkspacePresentationPanel`
- `ReviewWorkspacePresentationAdapter`

Required behavior:

- accept safe M28 workspace bundles, impact previews, and export manifests;
- produce UI-ready cards for review items, blocker states, decision outcomes,
  and export summaries;
- include only safe ids, display labels, safe summaries, reason labels, source
  refs, issue codes, blocker codes, counts, and review/preview/non-apply
  flags;
- produce deterministic tabs and filter metadata for `all`, `blocked`,
  `eligible`, `memory`, `persona`, and `distillation`;
- order cards deterministically by urgency, bundle id, queue item id,
  candidate id, decision id, and card id;
- keep all presentation records review-required, preview-only, non-applying,
  non-mutating, and non-runtime-ready.

### 2. Tests

Create `tests/test_review_workspace_presentation_adapter.py` with synthetic-only
tests that prove:

- workspace bundles produce safe presentation cards;
- decision impact previews produce outcome/status badges;
- export manifests produce safe count summaries;
- tabs/filter metadata are deterministic;
- blocked items sort before eligible routine items;
- serialized presentation panels do not contain forbidden
  private/provider/outbound/media fields;
- adapter exposes no send/schedule/deliver/provider/mutation/apply/synthesis
  or media methods.

### 3. Data Contract

Create `docs/data_contracts/review_workspace_presentation_contract.md`
describing implemented records, invariants, forbidden fields, tests,
verification, non-actions, and residual risks.

### 4. Next Task Package

Create
`docs/tasks/M29_review_workspace_ui/T390_review_workspace_static_panel.md`
for adding a local static review panel to the existing text-first web demo.

### 5. Worker Summary And Handoff

Write `docs/worker_summary/T389_worker_summary.md` and append a T389 worker
record to `docs/07_handoff.md`.

Do not mark T389 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\ui\review_workspace_adapter.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_review_workspace_presentation_adapter.py tests\test_review_workspace_safe_export.py tests\test_review_decision_impact_preview.py -q
```

```powershell
git diff --check
```

Use project-local pytest cache and basetemp paths if the default user temp
directory is not writable.

## Reviewer Type

Adversarial presentation-adapter review for privacy, non-apply safety,
UI-readiness, deterministic ordering, product-safety, and documentation
accuracy.
