# International Privacy / Platform Policy Checklist

Task: T311 International Privacy / Platform Policy Checklist
Status: worker draft for review

## Scope And Disclaimer

This checklist is a product and engineering planning artifact for an
AI companion-agent prototype. It is not legal advice, does not prove compliance,
does not complete any filing, app-store review, regulator review, or launch
approval, and does not authorize closed testing or commercial launch.

The checklist should be reviewed by qualified counsel and platform-policy
reviewers before any real user data, public distribution, paid feature,
international distribution, app-store submission, voice/avatar feature,
synthetic-media feature, proactive messaging, or companion/dependency-risk
feature.

Access date for online sources: 2026-05-31 (workspace date).

## Official / Primary Sources Consulted

| Source | URL | Product relevance |
| --- | --- | --- |
| EU GDPR, Regulation (EU) 2016/679, EUR-Lex | https://eur-lex.europa.eu/eli/reg/2016/679/oj | Personal data, lawful basis, transparency, data-subject rights, sensitive data, transfers, processors. |
| EU AI Act, Regulation (EU) 2024/1689, EUR-Lex | https://eur-lex.europa.eu/eli/reg/2024/1689/oj | AI transparency, prohibited practices, risk classification, GPAI/provider/deployer obligations, synthetic content and human-interaction disclosures. |
| EU Digital Services Act, Regulation (EU) 2022/2065, EUR-Lex | https://eur-lex.europa.eu/eli/reg/2022/2065/oj | Online platform/content moderation, notices, transparency, ads/recommender obligations if distribution becomes platform-like. |
| FTC Children's Online Privacy Protection Rule (COPPA) | https://www.ftc.gov/legal-library/browse/rules/childrens-online-privacy-protection-rule-coppa | US child privacy, verifiable parental consent, children under 13, apps/online services. |
| FTC Children's Privacy guidance | https://www.ftc.gov/business-guidance/privacy-security/childrens-privacy | COPPA business guidance and voice-recording child privacy context. |
| FTC AI companion chatbot inquiry, 2025 | https://www.ftc.gov/news-events/news/press-releases/2025/09/ftc-launches-inquiry-ai-chatbots-acting-companions | Directly relevant to AI companion chatbot safety, children/teens, risk disclosure, monitoring, and safeguards. |
| FTC AI deception guidance, 2023 | https://www.ftc.gov/business-guidance/blog/2023/03/chatbots-deepfakes-voice-clones-ai-deception-sale | Deceptive AI tools, chatbots, deepfakes, voice clones, unfair/deceptive practice risk. |
| FTC voice cloning challenge / impersonation context, 2024 | https://www.ftc.gov/policy/advocacy-research/tech-at-ftc/2024/04/approaches-address-ai-enabled-voice-cloning | Voice cloning fraud, biometric misuse, detection and authentication controls. |
| UK ICO AI and data protection guidance | https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/artificial-intelligence/ | UK GDPR and AI system data protection, DPIA/risk-management guidance. |
| California CCPA regulations, California Attorney General | https://oag.ca.gov/privacy/ccpa/regs | California consumer privacy rights, request handling, minors, notice obligations. |
| California CPPA CCPA/CPRA regulations | https://cppa.ca.gov/regulations/consumer_privacy_act.html | CPRA-era regulatory text and enforcement agency context. |
| Illinois Biometric Information Privacy Act, 740 ILCS 14 | https://ilga.gov/documents/legislation/ilcs/documents/074000140K1.htm | Biometric identifiers/information, voice/face/avatar risk review. |
| Apple App Review Guidelines | https://developer.apple.com/app-store/review/guidelines/ | App Store privacy, safety, UGC, payments, impersonation, health/medical and content rules. |
| Google Play AI-Generated Content policy | https://support.google.com/googleplay/android-developer/answer/14094294 | Generative AI app content safety, reporting, restricted content, deceptive behavior. |
| Google Play Developer Program Policy | https://support.google.com/googleplay/android-developer/answer/16543315 | Google Play developer requirements, AI-generated content, restricted content, metadata/policy constraints. |
| Google Play Deceptive Behavior policy | https://support.google.com/googleplay/android-developer/answer/15407219 | App impersonation, misleading claims, metadata/store listing accuracy. |

## Applicability Assumptions

- Local prototype: no public users, no app-store distribution, no platform
  messaging, no paid subscriptions, no voice/avatar biometric processing, and no
  production data-subject request workflow.
- Closed test: invited users, explicit consent, limited data scope, no minors by
  default, AI identity disclosure, AIGC labels, delete/export request workflow,
  incident response, and human review for dependency/crisis risks.
- Commercial launch: public-facing service with AI companion interaction,
  memory, persona customization, generated content, possible proactive
  messaging, and future voice/avatar features. This likely triggers privacy,
  AI transparency, child safety, consumer protection, platform, payment, and
  synthetic-media obligations in multiple jurisdictions.

## Launch Gate Summary

| Gate | Local prototype | Closed test | Commercial launch |
| --- | --- | --- | --- |
| Privacy notice and lawful basis | Draft | Required | Required and counsel-reviewed |
| Consent center | Draft model | Required for test users | Required with withdrawal/deletion/export |
| Data-subject request workflow | Local preview | Required process | Required operational process |
| AI identity / synthetic labels | Required in artifacts | Required in UI/output | Required and jurisdiction/platform reviewed |
| Child/minor policy | Block minors | Strongly recommended to block | Required age/minor handling if minors possible |
| Voice/avatar/biometric processing | Not enabled | Avoid unless separately reviewed | Requires biometric/synthetic-media review |
| Dependency/crisis safeguards | Draft tests | Required | Required and monitored |
| App-store/platform review | Not applicable | Required for any channel test | Required per channel |
| Paid feature/payment policy | Not applicable | Avoid or review | Required subscription/payment review |
| Launch readiness | Not claimed | Not claimed | Requires legal/product/security sign-off |

## Checklist: Privacy, Consent, And Data Rights

- [ ] Map personal data categories for account data, chat content, persona
  prompts, memory records, relationship state, proactive preferences, telemetry,
  payments, support tickets, safety events, exports, and deletion requests.
- [ ] Identify special/sensitive categories by jurisdiction, including mental
  health inferences, emotional state, relationship data, voice, face/avatar,
  biometric identifiers, child data, location, and payment data.
- [ ] Define lawful basis / consent path by jurisdiction and feature.
- [ ] Separate essential service processing from optional memory, persona
  distillation, voice/avatar, proactive messaging, analytics, and model
  improvement.
- [ ] Provide clear AI identity disclosure and privacy notice before collecting
  persona or chat inputs.
- [ ] Provide user controls for access, correction, deletion, portability/export,
  consent withdrawal, memory freeze, persona reset, and account deletion.
- [ ] Avoid dark patterns in consent, cancellation, deletion, export, and paid
  subscription flows.
- [ ] Define retention for raw chat input, summaries, memories, persona cards,
  audit logs, safety logs, and generated media.
- [ ] Review processor/subprocessor contracts before external model, analytics,
  crash reporting, payment, or cloud services.
- [ ] Review cross-border transfer mechanisms before serving EU/UK users or
  storing data outside the user's region.

## Checklist: AI Transparency And Generated Content

- [ ] Disclose that users are interacting with AI, not a human.
- [ ] Label generated companion replies, personas, virtual histories, role
  dynamic posts, images, audio, video, and avatar/Live2D outputs.
- [ ] Preserve labels in copy, download, export, share, and platform publishing
  flows.
- [ ] Add controls to prevent deception, impersonation, fake professional
  authority, fake intimacy, fake legal/medical/financial advice, and fake
  endorsements.
- [ ] Review EU AI Act transparency obligations for human-AI interaction,
  synthetic media/deepfake labeling, emotion inference, and manipulative
  practices before EU distribution.
- [ ] Do not represent model outputs as accurate, clinically safe, legally valid,
  or emotionally therapeutic without evidence and reviewed policy.
- [ ] Keep generated "moments" or social feed content clearly fictional or
  AI-generated, not real-world activity.

## Checklist: Companion, Dependency, And Crisis Risk

- [ ] Treat AI companion behavior as a high-scrutiny product category because
  regulators are examining AI chatbots acting as companions, especially for
  children and teenagers.
- [ ] Block product goals that encourage dependency, isolation, social
  replacement, psychological control, coercion, or concealment of AI identity.
- [ ] Add dependency-risk detection and escalation before affectionate,
  romantic, proactive, voice, avatar, or long-session features.
- [ ] Add safe-exit, pause, break reminders, user autonomy prompts, and
  dependency-language caps.
- [ ] Add crisis/self-harm response tests that route users to emergency or
  professional support resources without making clinical claims.
- [ ] Prohibit minor-facing romantic, sexual, manipulative, or dependency-focused
  companion behavior.
- [ ] Add incident response for self-harm, abuse, exploitation, impersonation,
  and harassment reports.

## Checklist: Children And Minors

- [ ] Default recommendation: block minors from the early companion product.
- [ ] If minors are allowed, implement age assurance, child/minor privacy review,
  parental consent where required, minor mode, content limits, time/session
  limits, complaint channels, and guardian support.
- [ ] Review COPPA for US users under 13 and UK/EU child data obligations before
  any child-directed or teen-popular distribution.
- [ ] Disable personalized ads, manipulative recommendations, proactive
  dependency messaging, romantic behavior, and unsafe UGC for minors.
- [ ] Add special review for voice recordings, photos, avatars, and emotional
  data from minors.

## Checklist: Voice, Avatar, Biometrics, And Synthetic Media

- [ ] Do not enable real-person voice clone, face clone, avatar deepfake, or
  deceased-person simulation without a separate explicit policy and legal
  review.
- [ ] If voice or face inputs are used, determine whether biometric privacy laws
  apply and define consent, retention, deletion, security, and vendor controls.
- [ ] Add explicit visible labels for synthetic voice, avatar, video, image, and
  virtual scenes.
- [ ] Add safeguards against fraud, scams, impersonation, unauthorized likeness,
  intimate image abuse, and misleading endorsements.
- [ ] Do not process voice/face data for model improvement without explicit,
  separate consent and deletion mechanics.

## Checklist: Platform And App-Store Policy

- [ ] Before App Store or Google Play submission, review all app metadata,
  screenshots, claims, age rating, privacy labels/data safety declarations,
  subscriptions, UGC/moderation controls, and reporting flows.
- [ ] Implement in-app reporting/flagging for offensive or unsafe AI-generated
  content before Google Play distribution.
- [ ] Avoid app names, icons, screenshots, or descriptions that imply official
  affiliation or impersonate another service, brand, person, or platform.
- [ ] Avoid claims like "therapy", "legal advice", "doctor", "guaranteed
  emotional support", "human companion", or "real person" unless specifically
  reviewed and substantiated.
- [ ] Use platform payment mechanisms where required and review subscription
  cancellation/refund policies.
- [ ] Do not integrate messaging platforms or push/proactive messaging until
  consent, quiet hours, frequency caps, complaint channels, and platform policy
  review are complete.

## Checklist: Payments, Monetization, And Commercial Claims

- [ ] Avoid paid intimacy escalation, dependency monetization, crisis upsell, or
  manipulative retention mechanics.
- [ ] Clearly disclose subscriptions, renewals, cancellation, refunds, and
  feature limits.
- [ ] Do not sell or share personal information without explicit legal review and
  jurisdiction-specific opt-out handling.
- [ ] Review consumer-protection requirements for AI performance claims,
  therapeutic/mental-health claims, and "humanlike" marketing language.

## Checklist: Data Transfer, Security, And Vendors

- [ ] Maintain a data map for regions, processors, subprocessors, model
  providers, analytics, payment vendors, storage, support, moderation, and crash
  reporting.
- [ ] Review data processing agreements and transfer mechanisms for EU/UK users.
- [ ] Encrypt sensitive data at rest and in transit.
- [ ] Minimize logs and avoid logging raw user chats by default.
- [ ] Add access controls, deletion workflows, retention automation, audit logs,
  and incident response.
- [ ] Review external model providers for retention, training use, deletion,
  abuse monitoring, security, and data location.

## Open Legal / Product Review Questions

- Which jurisdictions are in scope for closed test and public launch?
- Is the product child-directed, teen-popular, or adult-only?
- Does the companion agent fall under high-risk, transparency, or prohibited
  practice categories in any jurisdiction?
- Which data categories are special/sensitive or biometric?
- What consent and withdrawal mechanics are required for memory/persona
  distillation and style extraction?
- Can proactive messaging be offered without creating harassment, spam,
  dependency, or platform-policy risk?
- What platform/app-store age rating and content moderation commitments apply?
- Which model providers and cloud regions are acceptable for real user data?

## Required Before Closed Test

- [ ] Human legal/product-policy review of this checklist.
- [ ] Consent Center data model.
- [ ] Privacy notice and data map.
- [ ] AI identity and generated-content labels in UI.
- [ ] Minor policy decision.
- [ ] Crisis/dependency policy tests.
- [ ] Data-subject request process for access, deletion, export, and withdrawal.
- [ ] Incident/complaint workflow.
- [ ] App-store/platform policy review if any platform channel is used.

## Explicit Non-Actions

T311 does not implement:

- legal advice;
- compliance completion;
- filing, regulator review, or app-store approval;
- launch approval;
- UI;
- code;
- platform integration;
- outbound messaging;
- model-provider integration;
- user-data processing changes.
