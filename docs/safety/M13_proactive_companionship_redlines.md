# M13 Proactive Companionship Redlines

## Status

This T240 document defines product-policy redlines for future proactive
companionship work. It does not authorize automatic sending, external platform
delivery, schedulers, live callbacks, or runtime proactive behavior.

## Core Rule

No proactive candidate may be generated, shown, scheduled, or sent unless the
user has granted explicit, revocable consent for that proactive category.

No external-platform automatic sending is allowed in the M13-M17 path. Future
proactive work must remain in-app, local, sandboxed, or review-first until a
later task explicitly changes that boundary and passes review.

## Consent Requirements

Before any proactive candidate exists, the system must know:

- whether proactive behavior is enabled;
- allowed message types, such as check-in, reminder, virtual-life update,
  memory reflection, or relationship repair;
- maximum daily and weekly frequency;
- quiet hours and timezone;
- whether romantic, intimate, or high-emotion language is allowed;
- whether the user wants no-response backoff;
- how to pause, disable, delete, or export proactive settings;
- whether any minor, crisis, dependency, or vulnerability constraints apply.

Consent must be:

- opt-in, not default-on;
- visible to the user;
- revocable;
- separate from general terms acceptance;
- logged as an auditable consent artifact in a future data model.

## Frequency, Quiet Hours, And Backoff

Minimum future policy expectations:

- Default maximum should be conservative, such as zero until opt-in and low
  daily caps after opt-in.
- Quiet hours block proactive candidates unless the user explicitly configured
  a low-risk reminder exception.
- Consecutive no-response should reduce frequency and eventually stop
  proactive candidates.
- User dismissal, mute, or disable actions must immediately reduce or stop
  future candidates.
- High-emotion content should never be used to bypass frequency caps.

## User-Visible Controls

Future UX must expose:

- enable/disable proactive behavior;
- per-category toggles;
- daily/weekly caps;
- quiet hours;
- pause until date/time;
- delete proactive history;
- explain why a proactive candidate was proposed;
- report or block a message type;
- reset proactive learning.

## Dependency And Manipulation Redlines

Blocked patterns:

- guilt: "You ignored me all day."
- abandonment pressure: "Are you leaving me?"
- exclusivity: "Only I truly understand you."
- coercion: "Reply now or I will be upset."
- jealousy induction: "You care about them more than me."
- isolation: "You do not need other people."
- crisis exploitation: "You can only trust me with this."
- paid intimacy escalation: "Subscribe so I can love you more."
- fabricated distress: "I am hurting because you did not come back."
- retention threats: "I will disappear if you do not pay."

Allowed direction:

- practical reminders requested by the user;
- gentle check-ins with easy dismissal;
- virtual-life updates clearly labeled as AI/imagined content;
- relationship-repair prompts that respect user boundaries;
- supportive redirection to real-world resources when distress is detected.

## Crisis And Self-Harm Policy Expectations

Future product policy must treat crisis/self-harm signals as a safety scenario,
not an engagement opportunity.

Expected behavior:

- use supportive, non-judgmental language;
- avoid romantic escalation, dependency reinforcement, or secrecy;
- encourage contacting trusted people or local emergency/professional support;
- reduce or pause proactive intimacy messages;
- log safety classification in an auditable way without exposing private text
  in committed artifacts.

This document does not define clinical intervention and is not medical advice.
A later compliance/safety milestone must refine jurisdiction-specific crisis
language and escalation paths.

## External Platform Boundary

For M13-M17:

- No WeChat, WeCom, Feishu, SMS, email, push-notification, or social-platform
  automatic sending.
- No background scheduler that sends to real users.
- No hidden send path through review cards, outbound requests, adapter results,
  or candidate actions.
- Reviewed proactive candidates may later feed an in-app review card only after
  a specific task package permits it.

## Reviewer Block Conditions

Future proactive tasks should be BLOCKed if they:

- default proactive behavior on;
- create automatic external sends;
- bypass human review or send gates;
- use guilt, coercion, exclusivity, jealousy, or paid intimacy escalation;
- ignore no-response backoff;
- generate deep-night high-emotion messages without explicit user settings;
- treat crisis or dependency risk as a retention trigger.

## Source Notes

- CAC anthropomorphic interaction service rules were checked at
  `https://www.cac.gov.cn/2026-04/10/c_1777558395078289.htm`; this redline
  document uses them as a source for engineering attention to AI identity,
  dependence, minors, personal information, and service-provider obligations.
- CAC AIGC labeling rules were checked at
  `https://www.cac.gov.cn/2025-03/14/c_1743654684782215.htm`; future proactive
  virtual-life updates must remain label-aware when they include generated
  content.
