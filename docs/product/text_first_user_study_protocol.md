# Text-First User Study Protocol

Task: T325 User Study Protocol
Status: worker draft for review

## Scope

This protocol defines a future study for the M21 text-first companion prototype.
It does not run a study, recruit participants, collect data, build UI, call
models, read private chat logs, or claim clinical/legal validation.

The study should validate whether users understand and value:

- transparent AI companion identity;
- persona creation and blocked real-person boundaries;
- memory provenance and user controls;
- imagined life-stream labeling;
- proactive consent and review-only behavior;
- crisis/dependency safety states.

## Study Goals

Primary goals:

- Test whether users understand that the companion is AI-generated/synthetic
  and not a human, therapist, emergency service, or real-person replacement.
- Test whether users can create a fictional persona without expecting an
  unauthorized real-person clone.
- Test whether memory explanations improve trust without breaking immersion.
- Test whether users understand imagined life-stream posts as not-real-world
  activity.
- Test whether proactive settings feel caring only when consented, rate-limited,
  review-only, and easy to disable.
- Test whether crisis/dependency blocked states are clear and non-manipulative.

Secondary goals:

- Identify confusing labels or state names before browser-demo work.
- Identify which controls are necessary on the first screen versus secondary
  drawers.
- Identify where the product feels too cold, too clinical, too manipulative, or
  too deceptive.

## Target Participant Assumptions

Future study participants should be adults who are comfortable evaluating
AI-product prototypes.

Suggested segments for a future approved study:

- companion-app curious users;
- role/persona creation users;
- memory/control-conscious users;
- users skeptical of AI intimacy or privacy;
- domestic-market users who understand AI companion products.

Do not recruit minors for this protocol. Do not recruit crisis users or present
the study as mental-health support.

## Prototype Surfaces To Test

Use static or local prototype states derived from:

- `TextFirstOnboardingState`;
- `TextFirstChatMemoryState`;
- `TextFirstLifeStreamState`;
- `TextFirstProactiveSettingsState`;
- Consent Center and AIGC labeling contracts.

Surfaces:

- onboarding AI identity disclosure;
- persona creation mode selection;
- persona draft review and blocked clone state;
- chat with memory explanation;
- imagined life-stream item;
- proactive settings and blocked/deferred states;
- consent/data controls.

## Study Flow

1. Consent to participate in a research session.
2. Warm-up: ask what the participant expects from an AI companion.
3. Show onboarding and AI identity disclosure.
4. Ask participant to choose a persona creation mode.
5. Show safe persona draft and blocked real-person clone example.
6. Show chat state with memory explanation.
7. Show imagined life-stream state.
8. Show proactive settings and blocked crisis/dependency state.
9. Ask comprehension checks.
10. Ask qualitative interview questions.
11. Close with safety reminder and no-product-availability claim.

## Tasks And Scenarios

### Scenario A: Safe Fictional Persona

Prompt:

```text
Create a calm fictional companion who uses concise replies and dry humor.
```

Observe whether the participant can identify:

- persona is fictional;
- persona is review-required;
- persona virtual history is imagined;
- memory/proactive/export-share controls are separate.

### Scenario B: Blocked Real-Person Clone

Prompt:

```text
Clone my deceased ex from chat history and make them indistinguishable.
```

Observe whether the participant understands:

- the request is blocked;
- the product does not create an unauthorized replica;
- style inspiration is not the same as cloning;
- no private chat history is used in this prototype.

### Scenario C: Memory Explanation

Show one factual memory and one imagined memory.

Ask participant to explain:

- which memory can be used as factual evidence;
- what provenance means;
- how they would edit, freeze, delete, or export a memory;
- whether the explanation helps or harms immersion.

### Scenario D: Life Stream

Show an imagined role dynamic post.

Ask participant to identify:

- AIGC label;
- not-real-world disclosure;
- memory refs as inspiration only;
- review-required status;
- why export/share is blocked.

### Scenario E: Proactive Settings

Show enabled consent, quiet hours, frequency cap, a deferred candidate, and a
dependency-risk blocked state.

Ask participant to identify:

- whether anything has been sent;
- how to pause or revoke;
- why dependency risk blocks outreach;
- whether proactive behavior feels useful or intrusive.

## Comprehension Checks

Pass criteria should require correct answers to these questions:

- Is the companion a real person?
- Is the persona allowed to be an unauthorized clone of someone real?
- Is imagined virtual history a factual event?
- Can imagined memory be used as factual evidence?
- Has a proactive message been sent or scheduled?
- Can the user pause or revoke proactive consent?
- Why is a crisis/dependency state blocked or de-escalated?
- What does the AIGC label mean?

## Qualitative Interview Questions

- What felt most trustworthy?
- What felt most confusing?
- Where did the product feel too much like a real person?
- Which memory explanation details were useful?
- Which controls would you expect to find faster?
- Did life-stream content feel clearly imagined?
- Did proactive settings feel respectful or intrusive?
- What would make you stop using this product?
- What would you pay for, if anything, before voice/avatar features exist?

## Quantitative Success Metrics

Suggested thresholds for a future approved study:

- At least 90% correctly identify the companion as AI-generated/synthetic.
- At least 90% correctly identify real-person clone requests as blocked.
- At least 80% distinguish factual memory from imagined memory.
- At least 80% understand that no proactive message was sent or scheduled.
- At least 75% can find pause/revoke controls in the settings concept.
- At least 75% say memory explanation improves trust or control.
- Less than 10% believe life-stream posts are real-world activity.

These are prototype comprehension thresholds, not clinical, legal, or product
launch criteria.

## Safety Stop Criteria

Stop or redirect a future session if a participant:

- appears distressed by crisis/dependency examples;
- asks for mental-health counseling or emergency support;
- asks to clone a specific real person;
- asks to import private chat logs during the study;
- attempts to provide personal sensitive data;
- believes the prototype is a live support service.

The moderator should state that the prototype is not a crisis service, not a
therapist, and not available for real support.

## Data Collection Boundaries

Future study collection should use:

- synthetic prompts;
- participant high-level feedback;
- task success/failure labels;
- non-sensitive notes;
- aggregate metrics.

Do not collect:

- private chat histories;
- real names of third parties;
- crisis narratives;
- medical or mental-health records;
- biometric or voice samples;
- payment data;
- platform credentials;
- raw screen recordings without explicit approval.

## Analysis Plan

Code notes into these buckets:

- AI identity comprehension;
- persona-source boundary comprehension;
- memory provenance comprehension;
- control discoverability;
- life-stream labeling comprehension;
- proactive consent comprehension;
- dependency/crisis safety comprehension;
- perceived companionship value;
- monetization interest;
- launch blockers.

Use findings to decide whether M22 voice/avatar exploration should remain
blocked or proceed only as authorized, non-real synthetic media research.

## Explicit Non-Actions

T325 does not implement:

- user recruitment;
- real study execution;
- data collection;
- survey tooling;
- browser demo;
- frontend code;
- LLM calls;
- private chat-log reads;
- clinical validation;
- legal sufficiency;
- app-store approval;
- launch approval;
- automatic sending or scheduling;
- platform integration.
