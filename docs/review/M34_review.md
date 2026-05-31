# M34 Integrated Companion Demo Review

Review target: T412 through T415
Reviewer posture: adversarial product-demo review
Verdict: PASS_WITH_WARNINGS

## Scope Reviewed

M34 was reviewed as a local integrated companion demo milestone:

- T412: integrated companion demo scope refinement;
- T413: integrated scenario spine payload and static UI;
- T414: trust/commercial positioning payload and static UI;
- T415: responsive hardening for the integrated demo surfaces.

The milestone was not reviewed as a production companion runtime, model-provider
integration, real private-chat distillation pipeline, outbound messaging
system, voice/avatar runtime, media-generation feature, or commercial launch
approval.

## Findings

No blocking defects were found in the reviewed M34 scope.

Warnings:

- The demo is still synthetic and local-only. It explains the target companion
  experience, but it does not prove real-time human-like conversation quality.
- Commercial positioning is trust-first and appropriately bounded, but it has
  not been validated by pricing tests, legal review, app-store review, or user
  research.
- Voice/avatar and life-stream surfaces remain locked, labeled, or imagined.
  This is correct for M34, but it means the user-visible multimodal experience
  remains future work.
- Browser QA was performed on available local/narrow viewports and synthetic
  fixtures, not a full device matrix.

## Integrated Scenario Spine

PASS_WITH_WARNINGS.

Evidence:

- `TextFirstWebDemoState` now includes `integrated_scenario`.
- The payload includes persona, memory, review, proactive, life-stream,
  voice/avatar boundary, commercial positioning, readiness, and ordered
  scenario-step fields.
- Static UI renders an integrated scenario panel before the tabbed review
  surfaces, making the demo easier to scan as a product workflow.
- Tests assert required server-safe payload fields and static hooks.

Residual risk:

- The spine is a reviewer-facing product narrative, not an executable
  companion session loop.

## Trust And Commercial Positioning

PASS_WITH_WARNINGS.

Evidence:

- `TextFirstWebDemoState` now includes `trust_commercial`.
- Pricing hypotheses are framed around reviewed memory depth, persona
  customization, review tooling, exports, and synthetic content workflows.
- Trust controls preserve AI disclosure, rollback evidence, locked voice/avatar
  boundaries, and safety-over-revenue language.
- Unacceptable patterns explicitly include guilt-based retention,
  impersonation claims, crisis paywalls, and hidden private-data use.
- Tests assert the payload and static UI do not add payment processing,
  provider calls, outbound controls, or media generation.

Residual risk:

- Commercial language is still a hypothesis and needs future validation before
  being treated as pricing or launch strategy.

## Responsive And Static UI Hardening

PASS.

Evidence:

- T415 added `min-width: 0` to repeated item cards.
- Mobile CSS constrains integrated scenario, trust/commercial, and review grids
  to a single-column `minmax(0, 1fr)` layout.
- Accessibility/static tests check section labels and forbidden controls.
- Focused responsive tests passed.

## Browser QA Evidence

PASS_WITH_WARNINGS.

Evidence:

- T413 Browser QA confirmed the integrated scenario spine was visible, with 8
  scenario cards, commercial positioning text, and voice/avatar boundary text.
- T414 Browser QA confirmed the trust/commercial panel rendered with 3 pricing
  items, 4 trust controls, 4 unacceptable patterns, and 3 readiness gaps.
- T415 Browser QA confirmed the narrow viewport rendered single-column scenario
  and trust/commercial grids without horizontal overflow and with readable trust
  panel content.

Residual risk:

- Browser QA used local static fixtures and the available viewport only.

## Forbidden Surface Checks

PASS.

Evidence:

- No task read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- No task added model-provider calls, source readers, extraction from real
  logs, embeddings, vector search, platform adapters, webhooks, queues,
  recipient identifiers, delivery state, schedulers, automatic outreach,
  voice/avatar runtime, microphone/camera access, ASR, TTS, voice cloning, or
  generated media.
- Static tests assert no action controls for approval, provider calls, platform
  connection, outbound delivery, or media generation were introduced.
- Served demo payload tests assert no forbidden private/provider/outbound/media
  fields are exposed in the new surfaces.

## Fresh Verification

```powershell
$env:PYTHONPATH='src'
pytest tests\test_integrated_demo_scenario_spine.py tests\test_trust_commercial_positioning_panel.py tests\test_integrated_demo_responsive_hardening.py tests\test_text_first_web_demo_static.py tests\test_text_first_web_demo_local_server.py tests\test_text_first_web_demo_accessibility.py tests\test_text_first_web_demo_state_switching.py tests\test_review_workspace_apply_audit_panel.py -q -o cache_dir=artifacts\t416_pytest_cache --basetemp=artifacts\t416_pytest_basetemp
```

Result: passed, `36 passed`.

## Verdict

M34 is fit to close as `PASS_WITH_WARNINGS`.

The warnings are not blockers because M34 explicitly scoped itself to a local,
synthetic, review-facing product demo. They should remain visible when planning
the next milestone: the product now needs an inspectable local interaction loop
that feels closer to companionship without crossing into private-data ingestion,
model-provider calls, outbound messaging, or voice/avatar/media runtime.
