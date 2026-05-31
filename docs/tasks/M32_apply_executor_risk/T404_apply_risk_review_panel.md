# T404: Apply Risk Review Panel

## Task ID

T404

## Goal

Expose T402/T403 apply-executor risk and approval decisions in the local review
workspace as read-only risk cards.

T404 should make risk assessments and approval gate outcomes inspectable in the
text-first web demo review workspace. It must not add any apply controls or
mutation behavior.

## Allowed Files

Future T404 worker may create or modify only:

- `src/practical_chat_agent/ui/text_first_web_demo_adapter.py`
- `src/practical_chat_agent/ui/static/text_first_web_demo.js`
- `src/practical_chat_agent/ui/static/text_first_web_demo.css`
- `tests/test_review_workspace_apply_risk_panel.py`
- `docs/data_contracts/review_workspace_apply_risk_panel_contract.md`
- `docs/tasks/M32_apply_executor_risk/T405_m32_milestone_review.md`
- `docs/worker_summary/T404_worker_summary.md`
- `docs/07_handoff.md`

If T404 needs local server route changes, private data, model-provider calls,
package changes, platform adapters, outbound messaging, voice/avatar runtime,
media generation, persistence outside local demo payloads, or apply executors,
Captain must revise this package before assignment.

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
- Do not apply review decisions, manual apply previews, risk assessments, or
  approval decisions.
- Do not mutate memory stores, PersonaCard objects, or PersonaVersionStore.
- Do not add CLIs, schedulers, queues, webhooks, auth, tokens, recipient ids,
  delivery state, or platform persistence behavior.
- Do not implement proactive candidates, automatic outreach, sending,
  scheduling, notifications, platform delivery, microphone, camera, ASR, TTS,
  voice cloning, voice/avatar likeness, Live2D, generated audio, generated
  image, generated video, or media capture.
- Do not modify `docs/04_task_board.md`.

## Expected Outputs

### 1. Synthetic Review Workspace Payload

Extend the local demo adapter to include synthetic read-only apply risk cards
under the existing review workspace payload.

Risk cards should include safe fields such as:

- risk assessment id;
- approval id;
- preview id;
- decision id;
- candidate kind/id;
- risk recommendation;
- approval final outcome;
- required/satisfied/missing approval gates;
- blocker codes;
- stale reasons;
- non-executing flags.

The payload must not include internal queue ids, executor handles, mutation
methods, provider credentials, recipient ids, private text, media payloads, or
apply controls.

### 2. Static Renderer

Render apply risk cards in the review workspace panel using safe DOM text-node
construction. Do not use string-built HTML for risk-card content.

The rendered card should make the non-executing boundary visible, including
`executor_ready=false` and no apply controls.

### 3. Tests

Create `tests/test_review_workspace_apply_risk_panel.py` proving:

- the adapter payload includes read-only synthetic apply risk cards;
- cards include risk recommendation, final outcome, approvals, blockers, and
  non-executing flags;
- forbidden private/provider/outbound/media/mutation/internal fields are
  absent from served payloads;
- the static renderer has a risk-card rendering branch and no apply/action
  control labels for risk cards;
- existing manual apply preview cards and review workspace cards still render.

### 4. Data Contract

Create `docs/data_contracts/review_workspace_apply_risk_panel_contract.md`.

### 5. Next Task Package

Create `docs/tasks/M32_apply_executor_risk/T405_m32_milestone_review.md`.

### 6. Worker Summary And Handoff

Write `docs/worker_summary/T404_worker_summary.md` and append a T404 worker
record to `docs/07_handoff.md`.

Do not mark T404 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\ui\text_first_web_demo_adapter.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_review_workspace_apply_risk_panel.py tests\test_review_workspace_apply_preview_panel.py tests\test_apply_executor_approval_gate.py -q
```

```powershell
git diff --check
```

Use project-local pytest cache and basetemp paths if the default user temp
directory is not writable.

## Reviewer Type

Adversarial read-only UI review for apply-risk display, non-apply safety,
privacy, DOM rendering safety, and documentation accuracy.
