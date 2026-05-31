# Review Workspace Static Panel Contract

Task: T390 Review Workspace Static Panel
Status: worker draft for review

## Scope

This contract describes the local static review workspace panel added to the
text-first web demo assets:

- `src/practical_chat_agent/ui/static/text_first_web_demo.html`
- `src/practical_chat_agent/ui/static/text_first_web_demo.css`
- `src/practical_chat_agent/ui/static/text_first_web_demo.js`

The panel renders a synthetic review workspace fixture with review items,
blocker states, decision outcomes, and safe export counts. It does not apply
decisions, mutate memory stores, write persona versions, call providers,
generate replies, send messages, add routes, connect to platform delivery,
enable voice/avatar runtime, generate media, or recreate real people.

## Implemented Static Surface

HTML additions:

- `#tab-review`
- `#review-panel`
- `#review-filters`
- `#review-workspace-list`
- `#review-export-summary`

Scenario addition:

- `data-scenario="review-workspace"`

JavaScript additions:

- `fallbackState.review_workspace`
- `reviewToneClasses`
- `drawReviewWorkspace(review)`
- `appendReviewWorkspaceCard(card)`
- `appendReviewMeta(parent, value, extraClass)`
- `reviewCountsPlain(counts)`

CSS additions:

- `.filter-row`
- `.filter-chip`
- `.review-grid`
- `.review-card`
- `.status-badges`
- `.status-badge`
- `.status-badge.tone-blocked`
- `.status-badge.tone-eligible`
- `.status-badge.tone-review`
- `.status-badge.tone-info`
- `.review-counts`
- `.review-summary`

M30/T393 hardening:

- review workspace card payload fields are rendered through DOM nodes and
  `textContent`;
- `drawReviewWorkspace` no longer sends review card payload fields through the
  generic string/`innerHTML` item renderer;
- the generic item renderer remains used by older synthetic-only demo panels,
  but not by review workspace cards.

## Data Assumptions

The static fixture mirrors the T389 presentation shape without requiring a
local server payload:

- `filter_tabs`
- `cards`
- `status_badges`
- `issue_codes`
- `blocking_issue_codes`
- `reason_labels`
- `source_refs`
- `counts`
- `review_required`
- `preview_only`
- `changes_state=false`

The fixture is synthetic and safe. It contains no raw private text, provider
credentials, platform recipient ids, outbound queues, schedule/webhook fields,
tokens, voice/avatar capture data, audio/image/video payloads, or generated
media paths.

## Required Invariants

- The review workspace panel is local static UI only.
- Review cards do not expose action controls.
- Review cards show blocker and eligible states as status badges.
- Export counts are display-only.
- The panel preserves preview-only/no-state-change copy.
- The panel is reachable through an accessible tab relationship.
- The panel uses stable wrapping styles and responsive grid behavior.
- Review card payload fields are treated as text, not trusted markup.

## Forbidden Fields And Controls

The static assets must not contain:

- raw private chat text;
- raw transcripts;
- private message bodies;
- provider credentials;
- platform recipient ids;
- send queues;
- schedules;
- webhooks;
- tokens;
- microphone, camera, audio, image, or video payloads;
- generated media paths;
- decision-apply controls;
- mutation controls;
- provider call controls;
- delivery or publish controls.

The panel must not expose controls such as:

- approve/reject action buttons;
- delivery or publish controls;
- provider/webhook controls;
- mutation controls;
- media generation controls.

## Tests

Implemented tests:

- `tests/test_review_workspace_static_panel.py`

Covered behavior:

- static assets include the review workspace panel target;
- JS fixture data contains review workspace cards and filter tabs;
- blocked and eligible states are renderable;
- forbidden private/provider/outbound/media fields are absent;
- the panel exposes no action controls;
- review workspace cards use a DOM/text-node rendering path for payload
  fields.

Regression tests also run:

- `tests/test_text_first_web_demo_static.py`
- `tests/test_text_first_web_demo_accessibility.py`

## Verification

Expected minimum verification:

```powershell
$env:PYTHONPATH='src'
pytest tests\test_review_workspace_static_panel.py tests\test_text_first_web_demo_static.py tests\test_text_first_web_demo_accessibility.py -q -o cache_dir=artifacts\t390_pytest_cache --basetemp=artifacts\t390_pytest_basetemp
```

```powershell
git diff --check
```

Browser QA note:

- Browser QA was attempted against a local static server.
- Direct `file://` access was blocked by the in-app browser URL policy.
- Local `http://127.0.0.1:8771/...` and `http://localhost:8771/...` access
  were blocked by the browser client with `ERR_BLOCKED_BY_CLIENT`.
- Static and accessibility tests are the verification evidence for this task.

## Non-Actions

T390 does not implement:

- private data ingestion;
- source readers;
- extraction from real logs;
- embeddings;
- vector search;
- semantic ranking;
- similarity scoring;
- model-provider calls;
- de-identification quality validation;
- PersonaCard synthesis;
- final companion reply generation;
- runtime memory or persona mutation;
- decision apply paths;
- deletion executors;
- local server routes;
- proactive candidates;
- automatic sending or scheduling;
- platform integration;
- voice/avatar/video behavior;
- generated media;
- legal, clinical, launch, app-store, or regulator approval.

## Residual Risks

- The static panel uses an embedded synthetic fixture, not a live local server
  payload.
- Browser visual QA could not be completed because the browser client blocked
  local navigation.
- No apply executor or real-data import/de-identification quality evaluation
  exists.
- T391 still needs local server payload integration if the demo should serve
  the T389 adapter output dynamically.
- Other static demo sections still use the older synthetic-only string item
  renderer; T393 hardens only review workspace cards.
