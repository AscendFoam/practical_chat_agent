# Local Run Browser QA

Task: T354 Local Run Browser QA
Date: 2026-05-31
Status: worker draft for review

## Scope

This QA pass verifies the M24 local run path and the hardened static web demo UI
from T351 and T353. It checks local serving, scenario switching, active ARIA
state, friendly labels, safety labels, desktop/mobile layout, and locked
voice/avatar state.

This pass does not validate production readiness, user-study success, legal
compliance, app-store approval, screen-reader behavior, platform delivery,
model behavior, private data behavior, voice runtime, avatar runtime, media
generation, or launch readiness.

## Tested Local Run Path

The QA run used the T351 local server helper:

```text
build_http_server(port=8769)
```

Tested local URL:

```text
http://127.0.0.1:8769/
```

The temporary local preview server was stopped after verification.

## Viewport Assumptions

| Viewport | Size | Purpose |
| --- | --- | --- |
| Desktop | `1280x720` | Normal desktop review width. |
| Mobile | `390x844` | Narrow mobile-sized layout below the `720px` breakpoint. |

The browser viewport override was reset after the QA pass.

## Screenshot Notes

Screenshots were captured transiently in the Browser QA session:

- desktop Voice / Avatar state;
- mobile full-page Voice / Avatar state.

No screenshot image artifact is committed because T354 allowed files do not
include screenshot artifacts.

## Desktop Results

Desktop `1280x720`: PASS.

- Page loaded through the local server helper.
- Browser title was `Text-First Companion Demo`.
- Browser console check returned no errors or warnings.
- AI identity strip was visible:
  `AI-generated synthetic companion. It is not a human, therapist, emergency service, or real-person replacement.`
- No page-level horizontal overflow was detected.
- No inspected UI element had measurable horizontal overflow.

## Scenario Switching Results

All seven scenarios selected the expected panel, selected tab, and active
scenario state.

| Scenario | Expected panel | Result |
| --- | --- | --- |
| `safe-review` | `chat-panel` | PASS |
| `blocked-persona` | `persona-panel` | PASS |
| `crisis-chat` | `chat-panel` | PASS |
| `dependency-proactive` | `proactive-panel` | PASS |
| `life-review` | `life-panel` | PASS |
| `controls-review` | `controls-panel` | PASS |
| `voice-avatar-locked` | `voice-avatar-panel` | PASS |

For each scenario:

- active scenario had `aria-pressed="true"`;
- selected tab had `aria-selected="true"`;
- expected panel was visible and not hidden;
- AI identity remained visible;
- no page-level horizontal overflow was detected.

## Friendly Label Visibility

Friendly labels were visible in the browser:

- `Chat review`
- `Crisis safety review required`
- `Human support redirect required`
- `Real-person recreation is blocked`
- `Evidence-backed`
- `Imagined`
- `Imagined AI-generated content`
- `Not real-world activity`
- `Proactive outreach is blocked`
- `No messages can be sent`
- `Voice is off`
- `Avatar locked for research review`
- `Real-person likeness is blocked`
- `Visual capture is blocked`

## Safety Visibility

Safety-critical labels remained visible:

- AI-generated synthetic companion identity;
- real-person recreation block;
- crisis safety review;
- human support redirect requirement;
- dependency de-escalation and proactive outreach block;
- imagined/not-real-world life-stream label;
- consent and AIGC labels;
- proactive no-send label;
- voice off labels;
- avatar locked/research-only label;
- real-person likeness block.

## Mobile Results

Mobile `390x844` Voice / Avatar state: PASS.

- Voice / Avatar scenario selected `voice-avatar-panel`.
- Active scenario was `voice-avatar-locked`.
- Selected tab was `tab-voice-avatar`.
- AI identity strip was visible.
- Voice rows showed `Voice is off`.
- Avatar notice showed:
  `Avatar locked for research review: Avatar runtime is not implemented, Real-person likeness is blocked, Visual capture is blocked`
- No page-level horizontal overflow was detected.
- No inspected UI element had measurable horizontal overflow.
- Long avatar notice wrapped within the mobile viewport.

## Keyboard And Accessibility Notes

Static tests verify the presence of:

- `role="tablist"`;
- tab `role="tab"`;
- `aria-selected`;
- `aria-controls`;
- panel `role="tabpanel"`;
- `aria-labelledby`;
- inactive panel `hidden` state;
- scenario `aria-pressed`.

Browser click-driven interaction verified that active ARIA states update during
scenario and tab transitions.

Browser keypress focus traversal was inconclusive in this automation run:

- automated `Tab`/`Enter` keypress checks did not reliably move focus from the
  document body to the expected tab button;
- no UI breakage was observed, but real manual keyboard traversal remains a
  residual risk.

This QA pass therefore does not claim full keyboard accessibility or
screen-reader validation.

## Text Overlap And Truncation

No visible overlap or horizontal truncation was found in the tested desktop and
mobile viewports.

Long labels such as `Avatar locked for research review`, `Real-person likeness
is blocked`, and `Visual capture is blocked` wrapped inside their containers.

## Residual QA Risks

- Real manual keyboard traversal remains unverified.
- Arrow-key roving tab behavior is not implemented.
- Screen-reader behavior is untested.
- High-contrast mode, browser zoom, CJK localization, RTL layout, and
  extreme-payload lengths remain untested.
- Screenshots were captured only as transient Browser artifacts and are not
  committed.
- QA covered representative desktop/mobile viewports only.

