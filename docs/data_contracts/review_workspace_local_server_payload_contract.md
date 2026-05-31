# Review Workspace Local Server Payload Contract

Task: T391 Review Workspace Local Server Payload
Status: worker draft for review

## Scope

This contract describes the synthetic review workspace payload now included in
the text-first web demo adapter and local server responses:

- `src/practical_chat_agent/ui/text_first_web_demo_adapter.py`
- `src/practical_chat_agent/ui/text_first_web_demo_local_server.py`
- `src/practical_chat_agent/ui/static/text_first_web_demo.js`

The payload is generated from the T389 review workspace presentation adapter,
then projected into a smaller server-safe UI shape for the local web demo. It
does not apply decisions, mutate memory stores, write persona versions, call
providers, generate replies, send messages, connect to platform delivery,
enable voice/avatar runtime, generate media, or recreate real people.

## Implemented Payload

`TextFirstWebDemoState` now includes:

- `review_workspace`

The adapter builds synthetic records for:

- one blocked memory lifecycle review item;
- one eligible persona growth review item;
- decision impact previews for both items;
- one safe export summary card.

The local server exposes the same payload through:

- embedded HTML returned by `/` and `/text_first_web_demo.html`;
- JSON returned by `/demo-state.json`.

The static JavaScript keeps its embedded fallback fixture for cases where
`window.TEXT_FIRST_WEB_DEMO_STATE` is absent.

## Server-Safe Projection

The adapter calls `ReviewWorkspacePresentationAdapter.build_panel(...)`, then
projects the panel into a UI-safe dictionary with:

- `schema_version`
- `filter_tabs`
- `cards`
- `review_required`
- `preview_only`
- `changes_state=false`
- `runtime_ready=false`

Cards contain:

- `schema_version`
- `card_kind`
- `title`
- `display_label`
- `safe_summary`
- `filter_keys`
- `status_badges`
- `candidate_kind`
- `candidate_id`
- `decision_id`
- `preview_outcome`
- `reason_labels`
- `source_refs`
- `issue_codes`
- `blocking_issue_codes`
- `counts`
- `review_required`
- `preview_only`
- `changes_state=false`
- `runtime_ready=false`

Status badges contain labels, tones, issue codes, blocker codes, and the same
review-only/no-state-change flags.

The server-safe projection intentionally omits internal review queue fields and
write/apply executor flags from the public demo payload. It preserves the
review-only state through `review_required`, `preview_only`, `changes_state`,
and `runtime_ready`.

## Data Assumptions

- All records are synthetic fixtures constructed in code.
- Source refs are synthetic ids only.
- Safe summaries are `[SYNTHETIC]` user-facing summaries, not source text.
- The payload is local demo state, not production persistence.
- Decision impact outcomes are preview labels only.

## Required Invariants

- Local server responses remain synthetic and provider-free.
- Review workspace cards are display-only.
- No endpoint applies decisions or mutates memory/persona state.
- No internal queue field is exposed in server payload.
- Review-required, preview-only, no-state-change flags remain visible.
- The static panel can use server-provided `review_workspace` when present.
- The fallback static fixture remains available when server payload is absent.

## Forbidden Fields And Surfaces

Server responses must not contain:

- raw private chat text;
- raw transcripts;
- private message bodies;
- private chat history paths;
- provider credentials or API keys;
- platform recipient ids;
- queue fields;
- schedules;
- webhooks;
- tokens;
- delivery state;
- microphone, camera, audio, image, or video payloads;
- generated media paths;
- decision-apply controls;
- mutation executor controls.

The adapter and local server must not expose methods for provider calls,
outbound delivery, scheduling, publishing, memory/persona mutation, decision
apply, PersonaVersionStore writes, voice/avatar capture, or media generation.

## Tests

Implemented tests:

- `tests/test_review_workspace_local_server_payload.py`

Regression tests also run:

- `tests/test_text_first_web_demo_local_server.py`
- `tests/test_text_first_web_demo_adapter.py`
- `tests/test_review_workspace_static_panel.py`

Covered behavior:

- adapter emits a synthetic `review_workspace` section;
- local server JSON includes review workspace fields;
- embedded HTML includes server-provided review workspace payload;
- static JS keeps the safe fallback fixture;
- forbidden private/provider/outbound/media/internal queue fields are absent;
- adapter and server expose no provider/outbound/mutation/media methods.

## Verification

Expected minimum verification:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\ui\text_first_web_demo_adapter.py src\practical_chat_agent\ui\text_first_web_demo_local_server.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_review_workspace_local_server_payload.py tests\test_text_first_web_demo_local_server.py tests\test_text_first_web_demo_adapter.py tests\test_review_workspace_static_panel.py -q -o cache_dir=artifacts\t391_pytest_cache --basetemp=artifacts\t391_pytest_basetemp
```

```powershell
git diff --check
```

Browser QA note:

- T391 changes server payload behavior but not the static layout.
- The local server route tests verify `/`, `/text_first_web_demo.html`, and
  `/demo-state.json` payload behavior without starting a long-lived process.
- Earlier local browser navigation attempts in T390 were blocked by the
  browser client, so T391 uses route-level verification as the reproducible
  local evidence.

## Non-Actions

T391 does not implement:

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
- new local server routes;
- proactive candidates;
- automatic sending or scheduling;
- platform integration;
- voice/avatar/video behavior;
- generated media;
- legal, clinical, launch, app-store, or regulator approval.

## Residual Risks

- The payload remains synthetic and does not prove real review quality.
- The server-safe projection trusts already-safe M28/T389 records and does not
  independently inspect source artifacts.
- Browser visual QA remains blocked by local navigation policy in this
  environment.
- No apply executor or real-data import/de-identification quality evaluation
  exists.
