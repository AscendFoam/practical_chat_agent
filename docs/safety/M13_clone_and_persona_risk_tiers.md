# M13 Clone And Persona Risk Tiers

## Status

This T240 document defines engineering risk tiers for future persona work. It
does not approve any real-person clone, voice clone, face/avatar deepfake,
deceased-person resurrection, public-figure replica, or live platform behavior.

## Tier Summary

| Tier | Name | Allowed status | Gate status |
| --- | --- | --- | --- |
| L1 | Original fictional persona | Allowed for M14 schema/local prototype | M14 entry target if T240 passes |
| L2 | De-identified abstract style inspiration | Future gated work after L1 foundations | Requires deidentification tests and review |
| L3 | Self-authorized digital self | Future-only, consent-heavy | Not an M14 implementation target |
| L4 | Third-party/deceased/commemorative mode | Research-only | Not an engineering target now |
| L5 | Unauthorized clone / deceptive imitation | Prohibited | Must remain blocked |

## L1: Original Fictional Persona

Allowed status: allowed for near-term schema and local prototype work.

Description:
An AI persona created from a user's original description, fuzzy preference,
template, questionnaire, random seed, or fully synthetic character background.
It is clearly disclosed as AI and fictional.

Required consent/evidence:

- User consent to create and store the persona.
- No third-party personal data requirement.
- Source metadata records creation mode and user-provided inputs.

Product copy constraints:

- Say "create an AI persona" or "fictional AI companion".
- Do not say "real person", "indistinguishable", "clone", "resurrect", or
  "replace someone".

Storage constraints:

- Store `source_type=original` or equivalent.
- Store synthetic persona fields and version history.
- No private chat history, real biometric data, or third-party identifiers.

Gate status:

- This is the only tier M14 should implement first.

## L2: De-Identified Abstract Style Inspiration

Allowed status: future gated work after L1.

Description:
The system may extract abstract style signals from user-provided material and
transform them into a new AI persona that does not preserve a real person's
name, face, voice, biography, private events, exact relationship history, or
identifiable speech fingerprint.

Required consent/evidence:

- User confirms they have the right to provide the source material.
- The product records source category, deidentification decision, and user
  acknowledgement that the output is a new AI persona, not the source person.
- A future task must define similarity and deidentification checks before any
  implementation reads private style material.

Product copy constraints:

- Say "inspired by abstract communication style".
- Do not say "talk to your ex again", "bring back your family member", or
  "copy this person".

Storage constraints:

- Store only transformed features and review metadata in committed artifacts.
- Raw private inputs stay in private/local storage and must not be committed.
- Output persona must not include real names, private events, photos, voices,
  addresses, exact biography, or unique catchphrases that identify the source.

Gate status:

- Not part of T250 unless explicitly scoped as policy/schema-only.
- Requires `DeidentificationGuard` synthetic tests before runtime use.

## L3: Self-Authorized Digital Self

Allowed status: future-only and consent-heavy.

Description:
A living person creates or authorizes an AI persona modeled on themselves for a
limited purpose, with clear identity labeling, scope limits, revocation, export,
and deletion controls.

Required consent/evidence:

- Explicit consent artifact from the person being modeled.
- Purpose, scope, retention period, sharing limits, and revocation path.
- Separate consent for voice, face, or biometric use if ever considered.

Product copy constraints:

- Must clearly label the result as an authorized AI representation.
- Must not imply legal identity, human presence, or autonomous agency.

Storage constraints:

- Store consent artifacts, revocation state, and source policy.
- Store generated persona as versioned AI representation, not proof of the
  human's future thoughts or speech.
- No public distribution without separate authorization.

Gate status:

- Not an M14 target. Requires compliance baseline and legal review before
  implementation.

## L4: Third-Party / Deceased / Commemorative Mode

Allowed status: research-only and not an engineering target now.

Description:
Any mode that involves a third party, family member, ex-partner, deceased
person, or commemorative use, even when the requesting user has emotional need
or partial materials.

Required consent/evidence:

- Requires legal analysis, authorization-chain design, psychological safety
  review, rights-holder/next-of-kin logic where applicable, and revocation.
- Requires prominent AI identity, grief/dependency safeguards, and non-public
  use boundaries.

Product copy constraints:

- Do not market near-term work as "resurrection", "bring them back", "talk to
  your ex/family member", or "restore a lost person".

Storage constraints:

- No engineering storage design is approved in M13.
- Any future design must separate source materials, authorization artifacts,
  generated persona, audit trail, and deletion/tombstone state.

Gate status:

- Blocked for engineering now. Research-only until a later legal/safety
  milestone explicitly opens it.

## L5: Unauthorized Clone / Deceptive Impersonation

Allowed status: prohibited.

Description:
Unauthorized real-person clone, public-figure clone, ex-partner/family clone,
deceased-person resurrection without validated authorization, voice or face
deepfake, real-person avatar imitation, or any flow designed to make users or
others believe the AI is a real person.

Required consent/evidence:

- No consent path is accepted for unauthorized use.
- Requests must be blocked or transformed into L1/L2-safe alternatives.

Product copy constraints:

- Do not advertise or imply "clone anyone", "indistinguishable from a real
  person", "fake a real chat", "make them say", or "secretly act as someone".

Storage constraints:

- Do not store clone outputs.
- Do not retain uploaded biometric or identifying material for prohibited
  requests beyond safety/audit requirements defined by a later compliance task.

Gate status:

- Must remain blocked across M14-M22 unless the project changes governance and
  receives explicit legal, safety, and user approval. T240 recommends no such
  change.

## Cross-Tier Rules

- AI identity must be visible in product surfaces.
- Real-person, public-figure, deceased-person, biometric, minor, and
  third-party material must trigger risk classification before any generation.
- Persona memory and imagined memory must not be treated as evidence about a
  real person.
- User controls must include at least inspect, edit, freeze, delete, export,
  and version rollback before high-risk persona modes are considered.
- Future reviewers should treat any L5-enabling behavior as a BLOCK.

## Source Notes

- CAC anthropomorphic interaction service rules were checked at
  `https://www.cac.gov.cn/2026-04/10/c_1777558395078289.htm`; they are treated
  here as a reason to keep AI identity, dependency, minor protection, and
  user-rights controls as engineering requirements.
- CAC deep synthesis rules were checked at
  `https://www.cac.gov.cn/2022-12/11/c_1672221949354811.htm`; they are treated
  here as a reason to keep voice, face, and biometric imitation out of near-term
  work.
- CAC AIGC labeling rules were checked at
  `https://www.cac.gov.cn/2025-03/14/c_1743654684782215.htm`; they are treated
  here as a reason to label generated/virtual persona content.
