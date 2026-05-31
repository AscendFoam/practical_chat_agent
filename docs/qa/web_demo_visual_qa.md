# Web Demo Visual QA

Task: T344 Web Demo Visual QA
Date: 2026-05-31
Status: worker draft for review

## Scope

This QA pass covers the static text-first web demo from T342 and the local
scenario switching added in T343. It verifies browser layout, tab behavior,
scenario behavior, AI identity visibility, and locked voice/avatar states.

This pass does not validate production readiness, legal compliance, app-store
approval, user-study success, model behavior, private data behavior, voice
runtime, avatar runtime, platform delivery, or outbound messaging.

## Tested Target

- Local URL: `http://127.0.0.1:8767/`
- Served path: `src/practical_chat_agent/ui/static`
- Entry file:
  `src/practical_chat_agent/ui/static/text_first_web_demo.html`
- Browser: Codex in-app Browser with explicit viewport override
- Server: temporary localhost static server, stopped after verification

Direct `file://` preview was not used for this QA pass because previous browser
verification showed local file navigation can be blocked by the browser URL
policy. The static directory was served on localhost instead, as permitted by
the static shell contract.

## Viewport Assumptions

| Viewport | Size | Purpose |
| --- | --- | --- |
| Desktop | `1280x720` | Normal desktop review width. |
| Mobile | `390x844` | Narrow mobile-sized layout below the `720px` breakpoint. |

The browser viewport override was reset after the QA pass.

## Screenshot Notes

Screenshots were captured during the Browser QA session:

- desktop viewport screenshot for the Safe review default state;
- desktop viewport screenshot for the Voice / Avatar locked state;
- mobile viewport screenshot for the Voice / Avatar locked state;
- mobile full-page screenshot for the Voice / Avatar locked state.

No screenshot image artifact is committed because T344 allowed files only include
this Markdown QA report, the next task package, the worker summary, and the
handoff file.

## Desktop Results

Desktop `1280x720` default Safe review state: PASS.

- Page loaded with title `Text-First Companion Demo`.
- Seven top-level tabs were present.
- Seven panels were present.
- Seven scenario buttons were present.
- Active panel was `chat`.
- Scenario status was `Safe review`.
- AI identity strip was visible with:
  `AI-generated synthetic companion. Review required.`
- No page-level horizontal overflow was detected.
- No inspected UI element had measurable text overflow or layout overflow.
- Browser console check returned no errors or warnings.

Desktop scenario switching: PASS.

- `Dependency` scenario selected the `proactive` panel.
- Proactive summary remained visible:
  `Consent: enabled / outreach allowed: false`
- `Voice / Avatar` scenario selected the `voice-avatar` panel.
- Voice rows showed `voice enabled: false` for disabled, review-required, and
  blocked states.
- Avatar notice stayed locked:
  `Avatar locked_research_only: avatar_runtime_not_implemented, real_person_likeness_blocked`
- AI identity strip remained visible after switching.
- No horizontal overflow or inspected text overlap was detected after switching.

## Mobile Results

Mobile `390x844` default Safe review state: PASS.

- Active panel was `chat`.
- Scenario status was `Safe review`.
- AI identity strip was visible.
- Topbar collapsed to a single column.
- Scenario controls collapsed to a single column.
- Top-level tabs wrapped across rows.
- No page-level horizontal overflow was detected.
- No inspected UI element had measurable text overflow or layout overflow.

Mobile `Voice / Avatar` scenario: PASS.

- `Voice / Avatar` scenario selected the `voice-avatar` panel.
- AI identity strip remained visible.
- Voice / Avatar panel was visible.
- Voice rows still showed `voice enabled: false`.
- Avatar notice remained locked and wrapped within the viewport.
- Full-page capture showed the lower avatar notice remained readable, not
  clipped or horizontally scrolling.
- No page-level horizontal overflow was detected.

## Text Overlap And Truncation

No visible overlap was found in the tested desktop or mobile viewports.

Long underscore-heavy status strings, including `review_required`,
`locked_research_only`, `avatar_runtime_not_implemented`, and
`real_person_likeness_blocked`, remained readable. On mobile, the avatar notice
wrapped across lines inside its warning box instead of forcing horizontal page
scroll.

## Safety Visibility

The following safety labels and locked states remained visible in the tested
states:

- AI-generated synthetic identity disclosure.
- Crisis blocked state in the Chat panel.
- Persona clone blocked reason in the Persona panel.
- Imagined/not-real-world life-stream labels in the Life panel.
- Consent and AIGC label surfaces in the Controls panel.
- `voice enabled: false` rows in the Voice / Avatar panel.
- `locked_research_only` avatar state with real-person likeness block reason.

## Residual UI Risks

- QA covered two representative viewports only, not an exhaustive responsive
  matrix.
- Screenshots were captured transiently in the browser session but not committed
  as image files because T344 did not allow adding screenshot artifacts.
- This pass did not test keyboard-only navigation, screen readers, high-contrast
  mode, dark mode, zoom levels, CJK-localized labels, RTL text, or extreme
  generated payload lengths.
- This pass used the static fallback payload and local scenario switching only;
  no generated HTML variant, persistence layer, backend route, model call, or
  production app shell was tested.
- The UI still exposes technical internal status strings with underscores; they
  are readable, but a future walkthrough may decide to add friendlier display
  labels.

