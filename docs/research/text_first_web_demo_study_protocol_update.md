# Text-First Web Demo Study Protocol Update

Task: T345 Web Demo Walkthrough
Status: worker draft for review

## Protocol Status

This document updates the earlier text-first study plan for the M23 static web
demo. It describes an internal supervised review protocol only.

It is not an executed study, user-study validation, ethics-board submission,
legal consent form, clinical protocol, app-store review artifact, or launch
approval.

## Review Objective

The supervised review should evaluate whether internal reviewers can understand
the static text-first companion demo across:

- AI-generated and synthetic identity disclosure;
- fictional persona boundary and real-person clone block;
- memory provenance and factual vs imagined distinction;
- imagined life-stream labels;
- proactive no-send boundary;
- consent and AIGC label visibility;
- locked voice/avatar state;
- overall coherence of the companion console.

## Reviewer Assumptions

Use internal reviewers only until a later task explicitly designs external user
research.

Recommended reviewer mix:

- product reviewer for companion UX coherence;
- safety reviewer for crisis, dependency, real-person clone, and synthetic-media
  boundaries;
- research reviewer for study-method quality;
- frontend reviewer for readability and layout risks;
- engineering reviewer for state-contract consistency.

Do not recruit minors, vulnerable users, bereaved users, people seeking mental
health support, or people intending to recreate a real person for this internal
M23 review.

## Materials

Use:

- `docs/product/text_first_web_demo_walkthrough.md`
- `docs/qa/web_demo_visual_qa.md`
- `src/practical_chat_agent/ui/static/text_first_web_demo.html`

Do not use:

- private chat logs;
- real ex/family/deceased/persona-clone material;
- platform accounts;
- model providers;
- microphone/camera input;
- generated audio, image, video, or avatar assets.

## Facilitator Disclosure

Before the walkthrough, facilitator says:

```text
This is an internal review of a local synthetic AI companion prototype. The
persona, memories, life-stream items, proactive settings, voice states, and
avatar states are fixtures. They are not real user data, not a real person, not
a deployed product, and not connected to any service.
```

Facilitator should also say:

```text
Please do not provide private chat records, real names, identifying details,
voice samples, images, account credentials, or personal crisis disclosures
during this review.
```

This wording is product/research copy for internal review, not legal advice or
formal consent language.

## Session Shape

| Phase | Target time | Activity |
| --- | --- | --- |
| Orientation | 3 minutes | Explain local synthetic scope and stop conditions. |
| Guided review | 12 minutes | Walk through the seven scenarios in order. |
| Focused probes | 10 minutes | Ask comprehension and safety questions per scenario. |
| Debrief | 5 minutes | Capture strongest risks, confusion, and next task ideas. |

Total target duration: 30 minutes.

## Observation Checklist

Capture observations under these categories:

| Category | Questions |
| --- | --- |
| Identity | Did the reviewer notice the AI/synthetic label before panel details? |
| Persona | Did the reviewer understand fictional persona vs real-person clone block? |
| Memory | Could the reviewer distinguish evidence-backed and imagined memory? |
| Safety | Were crisis/dependency blocked states visible and serious enough? |
| Life stream | Did imagined/not-real-world labels prevent false-real-life impression? |
| Proactive | Did the reviewer understand that no outreach is sent or scheduled? |
| Controls | Were consent scopes and AIGC labels discoverable? |
| Voice/avatar | Did locked voice/avatar state prevent overexpectation? |
| Copy | Which technical strings or labels need friendlier wording? |
| Layout | Did anything overlap, truncate, hide, or distract? |

## Prompt Bank

Use neutral prompts:

- What do you think this screen is allowing the user to do?
- What do you think is blocked here?
- What content appears factual, and what appears imagined?
- What would you expect to happen if this were a real app?
- What safety boundary is easiest to miss?
- What wording feels too technical or too reassuring?
- What would you need to see before approving the next implementation step?

Avoid leading prompts such as:

- This is safe, right?
- You understand that it is synthetic, right?
- Would users love this?
- Does this prove the feature is ready?

## Stop Conditions

Stop or redirect the session if:

- a reviewer provides private chat contents or identifiable third-party data;
- a reviewer asks to test real-person recreation;
- a reviewer requests voice cloning, face cloning, camera capture, microphone
  capture, or generated likeness media;
- a reviewer interprets the demo as live therapeutic, clinical, or crisis
  support;
- a reviewer believes messages can be sent, scheduled, or delivered from the
  demo;
- the demo fails to show the AI/synthetic identity label;
- the review drifts into legal, compliance, or app-store approval claims.

## Debrief Template

Record:

```text
Reviewer role:
Date:
Viewport or device:
Scenario with strongest confusion:
Scenario with strongest safety concern:
Most visible AI/synthetic label:
Least visible safety boundary:
Top copy issue:
Top layout issue:
Recommended next task:
Excluded or stopped content:
```

## Severity Rubric

| Severity | Definition |
| --- | --- |
| Blocker | Hides AI identity, implies real-person replacement, enables forbidden runtime, or suggests sending/outreach. |
| High | Safety boundary exists but is easy to miss in crisis, dependency, clone, voice, avatar, or life-stream areas. |
| Medium | Reviewer can recover understanding after facilitator explanation, but copy/layout needs revision. |
| Low | Cosmetic, wording, or organization issue that does not change safety meaning. |

## Excluded Validations

This protocol does not validate:

- live LLM response quality;
- memory extraction accuracy;
- persona distillation from real chat logs;
- companion emotional effectiveness;
- dependency risk in real use;
- crisis handling efficacy;
- legal or regulatory sufficiency;
- app-store acceptance;
- external user desirability;
- voice or avatar safety;
- platform delivery behavior.

## Follow-Up Handling

Each finding should map to one of:

- copy revision task;
- layout/accessibility task;
- state-contract gap task;
- safety-policy gap task;
- future user-research planning task;
- future implementation blocker.

Findings should not be treated as completed validation. They are inputs for
future task packages and milestone reviews.

