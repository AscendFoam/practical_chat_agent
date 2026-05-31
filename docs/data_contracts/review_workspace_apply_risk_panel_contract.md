# Review Workspace Apply Risk Panel Contract

Task: T404 Apply Risk Review Panel
Status: worker draft for review

## Scope

This contract describes the read-only apply-executor risk panel additions to
the local review workspace demo:

- `src/practical_chat_agent/ui/text_first_web_demo_adapter.py`
- `src/practical_chat_agent/ui/static/text_first_web_demo.js`
- `src/practical_chat_agent/ui/static/text_first_web_demo.css`

The panel renders synthetic T402 risk assessments and T403 approval decisions
as review cards. It does not add apply buttons, mutation controls, state
writes, provider calls, platform integration, outbound messaging, or media
behavior.

## Implemented Payload

`review_workspace` now includes:

- `apply_risk_reviews`

Each risk card contains:

- `schema_version=review_workspace_apply_risk_card_v1`
- `card_kind=apply_risk_review`
- `title`
- `display_label`
- `safe_summary`
- `status_badges`
- `assessment_id`
- `approval_id`
- `preview_id`
- `decision_id`
- `candidate_kind`
- `candidate_id`
- `risk_recommendation`
- `final_outcome`
- `manual_eligibility_outcome`
- `risk_factors`
- `required_approval_gate_codes`
- `satisfied_approval_gate_codes`
- `missing_approval_gate_codes`
- `stale_reasons`
- `issue_codes`
- `blocking_issue_codes`
- `review_required`
- `preview_only`
- `risk_assessment_only`
- `executor_ready=false`
- `changes_state=false`
- `runtime_ready=false`

The payload is built from synthetic `ApplyExecutorRiskAssessment`,
`ApplyExecutorApprovalDecision`, and `ManualApplyEligibilityDecision` records.
Internal apply/write flags from the source records are intentionally stripped
from the served review workspace card payload.

## Static Rendering

The static review workspace panel now:

- combines `review.cards`, `review.manual_apply_previews`, and
  `review.apply_risk_reviews`;
- renders risk recommendation, approval outcome, manual eligibility, executor
  readiness, approval gates, stale reasons, and risk factors as read-only text;
- renders risk details through DOM/text nodes;
- applies `.apply-risk-card` styling for visual distinction;
- keeps all action controls absent.

## Required Invariants

- Apply risk cards are read-only.
- Approval outcomes are not executable authority.
- `executor_ready` stays false.
- No apply/mutation control is exposed.
- No memory store, PersonaCard, or PersonaVersionStore write is performed.
- No provider, outbound, platform, voice/avatar, or media behavior is added.
- Payload fields are synthetic and safe.

## Tests

Implemented tests:

- `tests/test_review_workspace_apply_risk_panel.py`

Regression tests also run:

- `tests/test_review_workspace_apply_preview_panel.py`
- `tests/test_apply_executor_approval_gate.py`

Covered behavior:

- server payload includes read-only synthetic apply risk cards;
- cards include risk recommendation, final outcome, approvals, blockers, risk
  factors, and non-executing flags;
- payloads contain no forbidden private/provider/outbound/media/mutation or
  internal fields;
- static JS/CSS know how to render apply risk details;
- existing review cards and manual apply preview cards are preserved;
- no action controls or mutation/provider/outbound/media controls are exposed.

## Verification

Expected minimum verification:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\ui\text_first_web_demo_adapter.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_review_workspace_apply_risk_panel.py tests\test_review_workspace_apply_preview_panel.py tests\test_apply_executor_approval_gate.py -q -o cache_dir=artifacts\t404_pytest_cache --basetemp=artifacts\t404_pytest_basetemp
```

```powershell
git diff --check
```

## Non-Actions

T404 does not implement:

- apply executors;
- manual apply execution;
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
- Approval outcomes remain non-executable.
- No future apply executor exists.
- Browser screenshot QA remains environment-blocked.
