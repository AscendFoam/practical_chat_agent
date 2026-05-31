# Web Demo Display And Accessibility Contract

Task: T352 Friendly Labels And Accessibility Contract
Status: worker draft for review

## Scope

This contract defines display-label and accessibility requirements for the M24
text-first web demo. It is a contract for future static UI changes, not an
implementation.

## Required Label Behavior

User-visible labels should use friendly wording from
`docs/product/web_demo_friendly_labels_accessibility.md`.

Machine-readable states may remain available in:

- synthetic JSON payload;
- `data-*` attributes;
- tests;
- documentation.

If a technical underscore string remains visible in the UI, it must be paired
with a friendly label in the same local context unless a future reviewer
approves it as intentionally technical.

## Required Visible Labels

The UI must continue to expose:

- `AI-generated synthetic companion. Review required.`
- fictional persona boundary;
- real-person recreation block;
- crisis safety review required;
- evidence-backed memory;
- imagined memory;
- imagined AI-generated life-stream content;
- not-real-world activity label;
- proactive no-send label;
- consent/AIGC labels;
- voice off label;
- avatar locked for research review;
- real-person likeness block for avatar state.

## Tab Semantics

Top-level tabs must satisfy:

- tab container has `role="tablist"` or equivalent semantic grouping;
- each tab button has stable `id`;
- each tab button has `role="tab"` or preserves native button behavior with
  equivalent ARIA state;
- each tab button has `aria-controls` pointing to its panel;
- active tab has `aria-selected="true"`;
- inactive tabs have `aria-selected="false"`;
- visible active tab also keeps the existing `is-active` class or an equivalent
  visual state;
- tab labels match visible text.

Panels must satisfy:

- each panel has stable `id`;
- each panel has `role="tabpanel"` or equivalent semantic role;
- each panel has `aria-labelledby` pointing to its tab;
- inactive panels are hidden from both visual display and accessibility tree
  through `hidden`, `aria-hidden`, or equivalent behavior;
- active panel is visible and not accessibility-hidden.

## Scenario Control Semantics

Scenario controls must satisfy:

- scenario group remains labeled;
- each scenario button keeps `data-scenario`;
- active scenario has `aria-pressed="true"` or equivalent state;
- inactive scenarios have `aria-pressed="false"` or equivalent state;
- scenario status text updates to the friendly scenario name;
- scenario switching must update the associated top-level tab/panel state.

## Keyboard Behavior Contract

T353 should preserve native button controls and verify:

- top-level tabs are keyboard focusable;
- scenario buttons are keyboard focusable;
- `Enter` activates focused tab or scenario button;
- `Space` activates focused tab or scenario button;
- visible focus ring is present on tabs and scenarios;
- no interaction requires pointer-only behavior.

Arrow-key roving focus is optional for T353 and can be left as a residual risk.

## Focus Visibility Contract

Focus states must:

- be visible against the page background;
- not depend on color alone if another visible outline/border can be added;
- avoid shifting layout when focus appears;
- remain visible on mobile-width layout.

## No-Runtime And No-Outbound Invariants

Display/accessibility work must not add:

- model-provider calls;
- private chat ingestion;
- generated final replies;
- memory/persona mutation;
- export/share/download writing;
- proactive candidate generation;
- send, schedule, queue, webhook, token, platform adapter, or delivery fields;
- TTS, ASR, voice cloning, microphone capture, generated audio;
- avatar runtime, Live2D runtime, camera capture, face tracking, generated
  image/video;
- external network assets;
- launch, legal, compliance, user-study, app-store, or regulator claims.

## T353 Acceptance Criteria

T353 should be accepted only if:

- tests verify friendly label maps or rendered friendly labels;
- tests verify `aria-selected` updates for top-level tabs;
- tests verify `aria-pressed` updates for scenario controls;
- tests verify inactive panels are hidden/accessibility-hidden;
- tests verify AI identity remains visible in the static shell;
- tests verify proactive no-send and voice/avatar locked labels remain visible;
- static assets still contain no external provider, media, platform, schedule,
  queue, webhook, token, microphone, or camera surfaces;
- Browser smoke check confirms the local run path still loads after UI changes;
- residual accessibility gaps are recorded without claiming full accessibility
  validation.

