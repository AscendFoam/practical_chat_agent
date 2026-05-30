# M13 Commercial Companion Positioning

## Status

This document is a T240 planning artifact. It describes a product direction for
future work; it does not claim that the product, compliance program, platform
delivery, proactive sending, voice, avatar, or commercial launch has been
implemented.

Source basis:

- Repository governance state through M12, especially `Gate M12 Conditional`.
- GPT-Pro M13+ report in
  `docs/reference/gpt-pro关于后续从M13开始的计划分析.md`.
- Current public/source checks recorded in T240 docs, including CAC
  anthropomorphic-interaction, deep-synthesis, and AIGC-labeling pages.
  Legal notes are engineering redlines, not legal advice.

## Recommended Positioning

Build a transparent, controllable, text-first AI persona companion product.

The product should help a user create and co-shape an AI persona object with
stable identity, long-term relationship memory, explainable growth, a virtual
life stream, and user-controlled memory/persona state. It must not position
itself as a real-person replacement, hidden clone, deceased-person
resurrection, public-figure imitation, or platform auto-send agent.

Recommended product promise:

```text
Create an AI persona that is clearly AI, deeply customizable, relationship-aware,
and able to grow with you. You can inspect, edit, freeze, delete, and export what
it remembers and how it changes.
```

## Why Not More Live WeChat / WeCom Delivery Now

M12 proved only a local, synthetic, dry-run WeCom Customer Service chain:
official-surface research, synthetic inbound normalization, local provider
eligibility, and review-safe dry-run payload preparation.

Continuing directly into live WeChat/WeCom delivery would spend engineering
effort on a risky adapter path while the product's commercial wedge is still
undefined. It would also blur states that the repo has carefully separated:
candidate action, outbound request, send gate, provider eligibility, dry-run
payload, API acceptance, acknowledgement, retry, failure event, and delivery.

Near-term product value is more likely to come from:

- persona compilation from detailed, fuzzy, template, random, and de-identified
  style-inspiration inputs;
- memory that separates factual, inferred, relational, procedural, and imagined
  records;
- relationship-aware dialogue and review-first proactive behavior;
- virtual life streams that are labeled as AI/imagined content;
- user controls for memory, persona versions, consent, deletion, and export.

## Target Users

- Users who want a long-running AI companion but want identity transparency and
  control rather than deception.
- Users who enjoy creating rich fictional personas and gradually shaping them
  through conversation.
- Users who want a companion that remembers shared history, boundaries,
  preferences, and relationship state in an explainable way.
- Users who want to import writing/chat style signals only as de-identified
  inspiration for a new AI persona, not to clone a real person.
- Power users, creators, or researchers who need auditable persona and memory
  schemas before any broader UX or marketplace work.

## Non-Target Users

- Users who want to impersonate an ex-partner, family member, deceased person,
  public figure, coworker, or other third party without consent.
- Users who want a hidden auto-reply agent for live social platforms.
- Users who want unlabelled AI-generated photos, voice, videos, or social posts
  that can be mistaken for a real person.
- Users seeking crisis counseling, diagnosis, emergency intervention, or
  professional mental-health replacement.
- Users seeking manipulative retention patterns such as guilt messages,
  jealousy loops, paid intimacy escalation, or "only I understand you" framing.

## MVP Promise

The first commercial MVP should promise:

- transparent fictional AI persona creation;
- detailed-prompt, fuzzy-preference, template, and random-seed creation modes;
- de-identified style inspiration as a later gated mode;
- versioned persona cards with source and consent metadata;
- stable core traits plus bounded growth policy;
- evidence-backed factual and relationship memory;
- isolated imagined memory for virtual life and dream-like content;
- review-first proactive candidates inside the app or sandbox;
- user-visible memory/persona controls.

## Explicit Non-Promises

The MVP must not promise:

- "clone anyone from chat logs";
- "bring back a deceased person";
- "make an AI indistinguishable from a real person";
- automatic external-platform sending;
- live WeChat/WeCom/Feishu delivery;
- voice cloning or face/avatar deepfakes;
- legal compliance certification;
- production security assessment completion;
- app-store approval;
- creator marketplace;
- paid intimacy escalation.

## First Commercial Validation Assumptions

The product direction should be validated before heavy implementation:

1. Users prefer transparent high-fidelity AI personas over deceptive real-person
   clones when controls and memory quality are strong.
2. Persona creation completion rate is higher when detailed, fuzzy, template,
   and random-seed modes all exist.
3. Users value memory explanations if they are compact and not immersion
   breaking.
4. Users trust the product more when they can edit, freeze, delete, and export
   memory and persona records.
5. Text-first companionship can reach meaningful retention before voice/avatar
   work.
6. De-identified style inspiration is commercially useful even when
   unauthorized real-person replicas are prohibited.
7. Proactive messages improve companionship only when they are consented,
   rate-limited, easy to disable, and non-coercive.

## Open User Research Questions

- Which persona creation mode has the highest completion and activation rate?
- Do users understand the distinction between de-identified style inspiration
  and a real-person clone?
- How much memory explanation is useful before it harms immersion?
- Which memory controls are essential on day one: delete, freeze, edit, export,
  or version rollback?
- Are users willing to pay for text-only long-term memory before voice/avatar?
- What proactive message frequency feels caring rather than intrusive?
- What user segments are unsafe or unsuitable for the product without
  additional protections?

## Pricing And Retention Questions

Initial hypotheses only:

- Free tier: limited text chat, basic template/random persona, short memory.
- Subscription tier: long-term memory, deep persona editing, version history,
  proactive candidates, virtual life stream, export.
- Premium tier: higher model budget, more personas, advanced memory controls,
  authorized non-real voice/avatar sandbox when later allowed.
- Professional/authorized tier: future-only consent-heavy digital-self or
  family/enterprise scenarios, after legal and safety review.

Do not validate retention through dependency pressure, guilt messages,
exclusive attachment, or paid intimacy unlocks.

## Do Not Build Yet

- Live WeChat/WeCom/Feishu production delivery.
- Personal-WeChat automation, desktop automation, scan-login resurrection, or
  unofficial SDK paths.
- External-platform automatic sending.
- Unauthorized real-person replicas, ex-partner/family clones, deceased-person
  resurrection, or public-figure clones.
- Voice cloning, face deepfakes, real-person video calls, or real-person avatar
  generation.
- Creator marketplace or public role distribution.
- App-store submission, paid launch, or legal compliance claims.

## Recommended Next Product Step

If T240 passes review, enter M14 with a narrow Persona Compiler schema task:
define `PersonaCard v1`, source/consent policy, risk-tier mapping, versioning
metadata, and synthetic tests. Do not implement a full compiler, LLM calls,
private chat-log reads, runtime dialogue changes, or proactive behavior in the
first M14 task.

## Source Notes

- TheOne public page checked during T240:
  `https://one.dxcat.cn/`.
- Replika public page checked during T240:
  `https://replika.com/`.
- Character.AI Character Calls and Voice FAQ / blog checked during T240:
  `https://support.character.ai/hc/en-us/articles/23957274129691-Character-Calls-Voice-FAQ`
  and `https://blog.character.ai/introducing-character-calls/`.
- Talkie public page checked during T240:
  `https://www.talkie-ai.com/`.
- MiniMax Xingye public page checked during T240:
  `https://www.xingyeai.com/`.
- CAC anthropomorphic interaction service rules checked during T240:
  `https://www.cac.gov.cn/2026-04/10/c_1777558395078289.htm`.
- CAC deep synthesis rules checked during T240:
  `https://www.cac.gov.cn/2022-12/11/c_1672221949354811.htm`.
- CAC AIGC labeling rules checked during T240:
  `https://www.cac.gov.cn/2025-03/14/c_1743654684782215.htm`.
