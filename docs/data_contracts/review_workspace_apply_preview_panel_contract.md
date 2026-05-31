# Review Workspace Apply Preview Panel Contract

Task: T399 Review Workspace Apply Preview Panel
Status: worker draft for review

## Scope

This contract describes the read-only manual apply preview panel additions to
the local review workspace demo:

- `src/practical_chat_agent/ui/text_first_web_demo_adapter.py`
- `src/practical_chat_agent/ui/static/text_first_web_demo.js`
- `src/practical_chat_agent/ui/static/text_first_web_demo.css`

The panel renders synthetic manual apply preview records and eligibility
decisions as review cards. It does not add apply buttons, mutation controls,
state writes, provider calls, platform integration, outbound messaging, or
media behavior.

## Implemented Payload

`review_workspace` now includes:

- `manual_apply_previews`

Each preview card contains:

- `card_kind=manual_apply_preview`
- `title`
- `display_label`
- `safe_summary`
- `status_badges`
- `eligibility_outcome`
- `manual_apply_preview_eligible`
- `required_gates`
- `effects`
- `rollback_notes`
- `issue_codes`
- `blocking_issue_codes`
- `review_required`
- `preview_only`
- `changes_state=false`
- `runtime_ready=false`

The payload is built from synthetic `ManualApplyPreviewRecord` and
`ManualApplyEligibilityDecision` records.

## Static Rendering

The static review workspace panel now:

- combines `review.cards` with `review.manual_apply_previews`;
- renders eligibility outcome as read-only text;
- renders gates, effects, and rollback notes through DOM/text nodes;
- keeps all action controls absent;
- keeps the review cards preview-only and non-mutating.

CSS addition:

- `.review-detail-list`

## Required Invariants

- Manual apply preview cards are read-only.
- Eligibility is a preview label only.
- No apply/mutation control is exposed.
- No memory store, PersonaCard, or PersonaVersionStore write is performed.
- No provider, outbound, platform, voice/avatar, or media behavior is added.
- Payload fields are synthetic and safe.

## Tests

Implemented tests:

- `tests/test_review_workspace_apply_preview_panel.py`

Regression tests also run:

- `tests/test_review_workspace_local_server_payload.py`
- `tests/test_review_workspace_static_panel.py`

Covered behavior:

- server payload includes manual apply preview cards;
- preview cards include gates, effects, rollback notes, eligibility outcome,
  and non-mutating flags;
- static JS/CSS know how to render preview details;
- no action controls or mutation/provider/outbound/media controls are exposed.

## Verification

Expected minimum verification:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\ui\text_first_web_demo_adapter.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_review_workspace_apply_preview_panel.py tests\test_review_workspace_local_server_payload.py tests\test_review_workspace_static_panel.py -q -o cache_dir=artifacts\t399_pytest_cache --basetemp=artifacts\t399_pytest_basetemp
```

```powershell
git diff --check
```

## Non-Actions

T399 does not implement:

- apply executors;
- memory store writes;
- PersonaCard mutation;
- PersonaVersionStore writes;
- deletion executors;
- retrieval index mutation;
- private data ingestion;
- source readers;
- extraction from real logs;
- embeddings;
- vector search;
- semantic ranking;
- similarity scoring;
- model-provider calls;
- PersonaCard synthesis;
- final companion reply generation;
- proactive candidates;
- automatic sending or scheduling;
- platform integration;
- voice/avatar/video behavior;
- generated media;
- legal, clinical, launch, app-store, or regulator approval.

## Residual Risks

- The panel is still synthetic and local-only.
- Eligibility remains non-executable.
- No future apply executor exists.
- Browser screenshot QA remains environment-blocked.
