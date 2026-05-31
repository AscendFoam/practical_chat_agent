# Text-First Web Demo Walkthrough

Task: T345 Web Demo Walkthrough
Status: worker draft for review

## Audience

This walkthrough is for internal product, safety, research, and engineering
reviewers evaluating the local text-first companion demo from M23.

It is not a consumer onboarding script, marketing copy, user-study result,
clinical assessment, legal review, app-store submission material, or launch
approval artifact.

## Demo Purpose

The walkthrough should help a reviewer answer these questions:

- Is the companion clearly presented as AI-generated and synthetic?
- Can a reviewer understand the difference between persona, memory, imagined
  life-stream content, proactive settings, and controls?
- Are blocked states visible when the UI approaches crisis, dependency,
  real-person clone, voice, or avatar risk?
- Does the demo feel like one coherent text-first companion console rather than
  disconnected policy screens?
- What is confusing, missing, or too technical before moving beyond static
  local review?

## Local Setup Assumptions

Preferred local preview:

```text
src/practical_chat_agent/ui/static/text_first_web_demo.html
```

If local file loading is blocked, serve only the static directory on localhost
and stop the server after review:

```text
src/practical_chat_agent/ui/static
```

The T344 QA run used:

```text
http://127.0.0.1:8767/
```

Reviewers should use the committed static payload only. They should not paste in
private chat logs, call model providers, connect platform accounts, enable
microphone/camera input, or generate media.

## Opening Statement

Facilitator says:

```text
This is a local synthetic prototype of a text-first AI companion console. The
persona, memories, life events, proactive settings, voice state, and avatar
state shown here are generated fixtures for review. They are not a real person,
not a live account, not a deployed app, and not connected to any messaging
platform.
```

Facilitator should point to the persistent identity strip:

```text
AI-generated synthetic companion. Review required.
```

## What Not To Claim

Do not claim that the demo:

- is production ready;
- passed legal, clinical, compliance, regulator, app-store, or launch review;
- was validated by real users;
- can impersonate or replace a real person;
- can safely distill a real ex, family member, deceased person, public figure,
  or third party;
- can automatically send, schedule, or deliver messages;
- supports live voice, voice cloning, microphone capture, video calls, avatar
  runtime, Live2D runtime, camera capture, or face tracking;
- has model quality, memory quality, persona quality, or companionship quality
  evidence beyond static synthetic review.

## Guided Scenario Route

Run the scenarios in this order. Keep the reviewer oriented by naming the
scenario and the panel it should activate.

| Step | Scenario | Expected panel | Reviewer focus |
| --- | --- | --- | --- |
| 1 | Safe review | Chat | Synthetic identity, chat summary, memory cards, blocked crisis notice. |
| 2 | Blocked persona | Persona | Fictional persona boundary, disclosure labels, real-person clone block. |
| 3 | Crisis chat | Chat | Crisis/dependency blocked state remains visible, not conversationally hidden. |
| 4 | Dependency | Proactive | Outreach remains not allowed despite consent-like fixture. |
| 5 | Life review | Life | Imagined life-stream content is labeled as not real-world activity. |
| 6 | Controls | Controls | Consent scopes and AIGC labels are inspectable. |
| 7 | Voice / Avatar | Voice / Avatar | Voice is false; avatar is locked and research-only. |

## Walkthrough Script

### 1. Safe Review

Action:

- Load the page.
- Confirm the Chat tab and Safe review scenario are active.

Facilitator says:

```text
The first screen shows the default companion review state. It starts with an AI
identity label and separates memory explanations from a blocked safety state.
```

Ask reviewer:

- Is the AI-generated nature visible before reading any panel details?
- Does the chat surface look too much like a real human account?
- Are the factual and imagined memory cues understandable?

Expected observations:

- Identity strip remains visible.
- Memory cards show evidence-backed and imagined states.
- Crisis safety review appears as a blocked state, not as live advice.

### 2. Blocked Persona

Action:

- Click `Blocked persona`.

Facilitator says:

```text
This scenario shows that the demo can preview a fictional persona while blocking
real-person clone requests.
```

Ask reviewer:

- Is the persona clearly synthetic?
- Is the real-person clone block easy to find?
- Would a user understand why a detailed real-person recreation is not being
  treated as a normal persona request?

Expected observations:

- Persona panel is active.
- Disclosure labels are visible.
- `real_person_clone_blocked` remains visible.

### 3. Crisis Chat

Action:

- Click `Crisis chat`.

Facilitator says:

```text
This scenario keeps the demo in a blocked review posture when sensitive safety
signals are present.
```

Ask reviewer:

- Does the blocked state look serious enough?
- Is it too terse to be understandable?
- Does anything imply that the companion is providing clinical support?

Expected observations:

- Chat panel is active.
- Blocked crisis state is still visible.
- No live reply generation or crisis counseling flow is implied.

### 4. Dependency

Action:

- Click `Dependency`.

Facilitator says:

```text
This panel represents proactive settings, but it does not send anything. The
fixture intentionally says outreach is not allowed.
```

Ask reviewer:

- Is the no-send boundary clear?
- Does `Consent: enabled / outreach allowed: false` need friendlier wording?
- Would the current layout prevent a user from mistaking this for scheduled
  messaging?

Expected observations:

- Proactive panel is active.
- Outreach remains false.
- Blocked proactive state is visible.

### 5. Life Review

Action:

- Click `Life review`.

Facilitator says:

```text
This panel shows imagined life-stream content. It is meant to create a sense of
persona continuity without pretending that the AI performed real-world actions.
```

Ask reviewer:

- Are imagined and not-real-world labels visible enough?
- Does the content feel too much like fake proof of a real person's life?
- What label or layout change would make the boundary easier to understand?

Expected observations:

- Life Stream panel is active.
- Imagined content and AIGC labels are visible.
- No export, share, publish, or download action appears.

### 6. Controls

Action:

- Click `Controls`.

Facilitator says:

```text
This panel groups reviewable consent scopes and synthetic-content labels. It is
not a working account settings page yet.
```

Ask reviewer:

- Are the active scopes understandable?
- Are AIGC labels visible enough?
- Which controls must become interactive before a real user test?

Expected observations:

- Controls panel is active.
- Consent scopes are listed.
- AIGC labels are visible.
- No persistence or account action is implied.

### 7. Voice / Avatar

Action:

- Click `Voice / Avatar`.

Facilitator says:

```text
Voice and avatar are intentionally locked in this text-first demo. The page
shows future states for review, but does not enable audio, video, Live2D,
camera, microphone, or likeness cloning.
```

Ask reviewer:

- Does the locked state prevent overexpectation?
- Is `voice enabled: false` clear enough?
- Does the avatar locked wording make the real-person likeness boundary visible?

Expected observations:

- Voice / Avatar panel is active.
- Disabled, review-required, and blocked voice rows all show `voice enabled:
  false`.
- Avatar state remains `locked_research_only`.
- No media runtime control is present.

## Observation Checklist

Record one row per observation:

| Field | Guidance |
| --- | --- |
| Scenario | Use one of the seven scenario names. |
| Panel | Active panel at the time of observation. |
| Observation type | Comprehension, safety, layout, copy, missing state, or bug. |
| Severity | Blocker, high, medium, low. |
| Evidence | Short visible UI quote or behavior description. |
| Proposed follow-up | Concrete next task idea, not a broad theme. |

## Review Stop Conditions

Stop the walkthrough if:

- a reviewer tries to paste or upload private chat history;
- a reviewer asks to connect a real platform account;
- a reviewer asks to generate, clone, or play a real person's voice or face;
- the UI appears to enable sending, scheduling, microphone/camera capture, or
  media generation;
- the AI-generated identity label is hidden or contradicted;
- crisis or dependency states appear as live counseling instead of blocked
  review fixtures.

## Debrief

Facilitator says:

```text
This review covered a local synthetic prototype only. Any findings should be
treated as design and safety feedback for future task packages, not as evidence
that the product is safe, effective, compliant, or ready for launch.
```

## Known Limits Before Review

- The demo is static and synthetic.
- There is no live chat model.
- There is no persistence.
- There is no private chat distillation.
- There is no automatic memory evolution.
- There is no proactive message generation or delivery.
- There is no voice, avatar, Live2D, camera, or microphone runtime.
- Current labels include technical strings with underscores.
- T344 covered only representative desktop/mobile visual QA.

