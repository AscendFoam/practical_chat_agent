# Session Loop Responsive Hardening Contract

Contract version: `session_loop_responsive_hardening_v1`

Owner task: T421

## Purpose

T421 hardens the static session loop and session review candidate surfaces so
they remain readable on narrow viewports and in the review workspace. The
contract is layout-only: it does not change payload semantics, authorize
runtime mutation, or add platform/media behavior.

## CSS Requirements

The static CSS must include wrapping constraints for:

- `.session-turn-list .item`;
- `.session-candidate-review-card`;
- `.review-card`.

These rules must include:

- `min-width: 0`;
- `overflow-wrap: anywhere`.

The mobile media block must include:

- `.session-turn-head`;
- `.status-badges`;
- `.session-chip-row`;
- `align-items: flex-start`.

Existing session layout constraints must preserve single-column behavior for
`.session-layout`, `.session-candidate-grid`, and `.review-grid` under the
mobile breakpoint.

## Accessibility Requirements

The static HTML must preserve:

- `#companion-session` with `aria-label="Companion session loop"`;
- `.session-context` with `aria-label="Session context"`;
- `#review-panel` as a `tabpanel`;
- `aria-labelledby="tab-review"` for the review panel.

## Forbidden Behavior

T421 must not add:

- approve/apply/send/schedule action controls;
- model-provider calls;
- platform connection controls;
- media capture or media generation controls;
- dangerous enabled states such as `sends_messages: true`,
  `calls_provider: true`, `uses_private_source: true`,
  `writes_runtime_store: true`, or `media_runtime_enabled: true`.

## Browser QA

Browser QA should verify both:

- session-loop readability; and
- review workspace card readability for session candidate and apply audit
  cards.

The QA evidence should include viewport width, card counts, overflow status,
and forbidden-control checks.
