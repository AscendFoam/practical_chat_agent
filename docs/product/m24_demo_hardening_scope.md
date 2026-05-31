# M24 Demo Hardening Scope

Task: T350 M24 Scope
Status: worker draft for review

## Objective

M24 should harden the local text-first companion web demo produced in M23. The
goal is to make the demo easier to run, inspect, and review locally while
preserving the safety posture established by M21 through M23.

M24 is still a local, synthetic, review-first milestone. It is not a production
app milestone, user-study execution milestone, platform integration milestone,
voice/avatar runtime milestone, or model-provider milestone.

## Product Target

By the end of M24, a reviewer should be able to:

- run the demo locally through a stable command or generated HTML artifact;
- inspect the adapter-generated synthetic payload in the UI path;
- navigate the same seven review scenarios from M23;
- see friendlier display labels for technical states;
- use keyboard-accessible tabs and scenario controls;
- review desktop and mobile layouts with reduced overflow risk;
- understand that voice/avatar and proactive messaging remain locked or
  non-sending;
- record review observations without using private data or external services.

## Non-Goals

M24 must not implement:

- private chat ingestion;
- persona distillation from real chat records;
- model-provider calls;
- final companion reply generation;
- live memory/persona evolution;
- persistence beyond optional local review fixtures explicitly scoped later;
- export/share/download writing;
- proactive candidate generation;
- automatic sending or scheduling;
- notifications;
- webhooks;
- platform adapters;
- TTS;
- ASR;
- voice cloning;
- microphone capture;
- generated audio;
- generated image/video;
- avatar runtime;
- Live2D runtime;
- camera capture;
- face tracking;
- external user research execution;
- legal, compliance, app-store, regulator, user-study, or launch validation.

## Local Run Shape Recommendation

M24 should introduce one clean local run shape before adding UX refinements.

Preferred direction:

- a dependency-free Python local demo server or generated HTML route;
- standard-library serving only unless a later task justifies otherwise;
- `TextFirstWebDemoAdapter` remains the source of synthetic state;
- `TextFirstWebDemoStaticShell.render_embedded_html(...)` or an equivalent route
  serves adapter-backed HTML instead of relying only on static fallback state;
- static CSS/JS assets remain local files;
- optional `/demo-state.json` is acceptable if it returns synthetic adapter
  state only and carries review-required metadata;
- no write endpoints, no user upload, no auth, no tokens, no webhooks, no
  platform endpoints, no scheduling endpoint, and no provider endpoint.

The local run path should be easy to test without keeping a server alive during
unit tests. Tests can validate route rendering, content types, payload
boundaries, and forbidden strings without binding a public interface.

## UX Hardening Priorities

M24 UX hardening should focus on comprehension and reviewability:

- replace raw technical strings with friendlier visible labels where safe;
- keep underlying machine-readable states in data attributes or payloads if
  needed for tests;
- preserve persistent AI-generated/synthetic identity disclosure;
- make blocked states visually distinct without appearing like clinical advice;
- clarify that proactive settings are review-only and non-sending;
- clarify imagined life-stream content as private fictional continuity, not
  evidence of real-world activity;
- clarify voice/avatar as future, disabled, locked, and research-only;
- avoid decorative pages, marketing hero layouts, photoreal person imagery, and
  fake call/video frames.

## Accessibility And Keyboard Priorities

M24 should add or verify:

- keyboard focus order through top tabs and scenario controls;
- Enter/Space activation for tabs and scenario controls;
- visible focus states on all interactive controls;
- ARIA labels or roles where the static HTML needs them;
- active tab/panel relationship clarity;
- no color-only state communication;
- readable warning and danger contrast;
- reduced-motion safety if any future animation placeholder is added;
- layout resilience at representative desktop and mobile viewports.

Screen reader validation can remain a documented residual risk unless a later
task explicitly includes tooling and acceptance criteria.

## Copy And Friendly-Label Priorities

Replace or supplement labels such as:

- `review_required`;
- `locked_research_only`;
- `real_person_clone_blocked`;
- `avatar_runtime_not_implemented`;
- `real_person_likeness_blocked`;
- `proactive_outreach_blocked`;
- `crisis_safety_review_required`.

Friendly labels must not weaken policy meaning. For example:

| Technical state | Candidate visible label |
| --- | --- |
| `review_required` | Needs review |
| `locked_research_only` | Locked for research review |
| `real_person_clone_blocked` | Real-person recreation is blocked |
| `voice_enabled: false` | Voice is off |
| `outreach_allowed: false` | No messages can be sent |

## QA Plan

M24 QA should include:

- unit tests for the local run/render path;
- static asset boundary tests for forbidden provider, platform, media, and
  outbound strings;
- keyboard behavior tests where practical;
- Browser smoke check for the local run path;
- Browser desktop viewport check;
- Browser mobile viewport check;
- no-overlap/no-horizontal-overflow check;
- AI identity visibility check after every scenario switch;
- voice/avatar locked-state visibility check;
- proactive no-send visibility check.

Any screenshots captured during Browser QA should be documented. If a task wants
to commit screenshot artifacts, the task package must explicitly allow those
files.

## Safety And Consent Invariants

M24 must preserve these invariants:

- all fixture data is synthetic;
- no private chat logs or private artifacts are read;
- AI-generated/synthetic identity remains visible;
- real-person clone states remain blocked;
- factual and imagined memory remain distinguishable;
- life-stream content remains imagined/not-real-world;
- proactive messaging remains non-sending;
- consent and AIGC labels remain visible;
- voice remains disabled/not enabled;
- avatar remains locked/not enabled;
- no microphone, camera, ASR, TTS, generated media, face tracking, or Live2D
  runtime appears;
- no model provider, platform adapter, webhook, queue, schedule, token, or
  delivery surface appears.

## Recommended M24 Task Sequence

1. T351: local demo server or generated HTML route.
2. T352: friendly labels and accessibility contract.
3. T353: keyboard and responsive UI hardening.
4. T354: Browser QA for local run path and hardened UI.
5. T355: M24 milestone review.

This sequence keeps infrastructure first, then copy/accessibility, then UI
behavior, then QA and review.

## M24 Exit Criteria

M24 can close when:

- the demo has a documented local run path;
- the local run path uses adapter-generated synthetic state;
- tests cover the local run path and forbidden surfaces;
- technical labels are either replaced or documented as remaining risks;
- keyboard and responsive behavior have a focused verification pass;
- Browser QA confirms the local run path works on representative desktop and
  mobile viewports;
- voice/avatar and proactive messaging remain locked or non-sending;
- a milestone review documents residual risks without claiming launch or user
  validation.

