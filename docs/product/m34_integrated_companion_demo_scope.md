# M34 Integrated Companion Demo Scope

Status: opened by T411 after M33 `PASS_WITH_WARNINGS`

## Purpose

M34 should turn the accumulated local prototype surfaces into a more coherent
integrated companion demo. The goal is not platform delivery or production
launch; it is a stronger local product narrative that lets a reviewer inspect
how persona customization, memory, review controls, proactive settings, life
stream, voice/avatar locked states, and commercial positioning fit together.

## Product Intent

The demo should better communicate the target experience:

- a customizable AI companion persona with explicit AI disclosure;
- memory-backed continuity that distinguishes factual, inferred, relational,
  procedural, and imagined memory;
- review-first distillation and apply controls;
- proactive suggestions that remain consented and review-gated;
- synthetic life-stream style content that is clearly labeled as imagined;
- voice/avatar surfaces that remain locked or review-only unless future policy
  explicitly permits them;
- a commercial framing that favors trust, control, and retention through user
  value rather than dependency pressure.

## In Scope

- Improve the local web demo information architecture and scenario flow.
- Add a concise integrated scenario spine across chat, persona, memory, review,
  proactive, life stream, voice/avatar, controls, and commercialization.
- Add server-safe payload fields for reviewer-facing product readiness and
  remaining-risk summaries.
- Add static UI display for commercial positioning and trust controls.
- Add tests that ensure no private/provider/platform/outbound/media expansion.
- Keep Browser QA as a final visual check for meaningful UI changes.

## Integrated Scenario Spine Requirements

The first code-facing M34 task should add an `integrated_scenario` payload to
the local web demo state. The payload should be server-safe and synthetic, with
fields such as:

- `scenario_title`: short reviewer-facing title;
- `persona_promise`: what kind of companion experience the synthetic persona
  is demonstrating;
- `memory_promise`: how continuity is grounded in reviewed memory rather than
  hidden raw logs;
- `review_promise`: how review gates and rollback evidence protect user
  control;
- `proactive_promise`: how proactive suggestions remain consented and
  review-gated;
- `life_stream_promise`: how imagined content is labeled and separated from
  real-world claims;
- `voice_avatar_boundary`: why voice/avatar is currently locked or review-only;
- `commercial_positioning`: trust-first monetization framing;
- `readiness_summary`: local prototype readiness and remaining gaps;
- `scenario_steps`: ordered cards linking to the existing demo sections.

The static UI should add an integrated scenario panel or section that lets a
reviewer scan this spine before diving into individual tabs. The panel should
not become a marketing landing page; it should remain an operational product
review surface.

## Commercial Positioning Requirements

Commercial framing should be explicit but bounded:

- acceptable: subscription tiers for memory depth, persona customization,
  review tooling, privacy controls, and premium synthetic content workflows;
- acceptable: enterprise/internal coaching adaptation as a separate governed
  product surface;
- not acceptable: dependency pressure, guilt-based retention, paywalled
  emotional crisis handling, impersonation claims, real-person replacement
  claims, or hidden monetization of private chat content.

## Browser QA Expectations

For code-facing M34 UI tasks, final verification should include:

- focused pytest coverage;
- local web demo regression tests when static assets change;
- Browser QA of the changed local page through a localhost preview;
- confirmation that text fits, the changed panel is visible, and no new
  private/provider/outbound/media controls appear.

## Out Of Scope

- Reading `private/chat_history/`, `private/distilled/`, or private artifacts.
- Model-provider calls.
- Source readers or extraction from real logs.
- Embeddings, vector search, semantic ranking, fine-tuning, or similarity
  scoring.
- Real platform adapters, webhooks, queues, tokens, recipient ids, delivery
  state, automatic outreach, sending, or scheduling.
- Microphone, camera, ASR, TTS, voice cloning, Live2D, generated audio,
  generated image, generated video, or media capture.
- Legal advice, app-store approval, launch approval, clinical claims,
  compliance completion, or regulator acceptance.

## Expected User Value

M34 should make the demo easier to evaluate as a product:

- reviewers can understand what the app is;
- reviewers can see how persona and memory control support believable
  companionship;
- reviewers can see where safety boundaries block unrealistic or risky
  behavior;
- reviewers can see commercial opportunities without hiding trust constraints.

## Suggested Task Sequence

1. T412: refine the integrated companion demo scope into concrete UI payload
   and panel requirements.
2. T413: add an integrated scenario spine to the demo payload.
3. T414: add a trust/commercial positioning panel.
4. T415: harden responsive review and commercial surfaces.
5. T416: run M34 milestone review and open the next implementation milestone.

## Review Standard

M34 should be judged on coherence, local demo quality, clear safety/trust
boundaries, no private data exposure, no unauthorized outbound behavior, and
no misleading claims that the demo is production-ready.
