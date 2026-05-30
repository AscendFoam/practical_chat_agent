# China Compliance Checklist

Task: T310 China Compliance Checklist
Status: worker draft for review

## Scope And Disclaimer

This checklist is a product and engineering planning artifact for a
companion-agent prototype. It is not legal advice, does not prove compliance,
does not complete any filing or registration, and does not authorize closed
testing, public launch, paid launch, app-store submission, mini-program launch,
or platform integration.

The checklist should be reviewed by qualified China counsel and product-policy
reviewers before any real user data, public distribution, platform integration,
paid feature, anthropomorphic companion feature, voice/avatar feature, or
commercial launch.

Access date for online sources: 2026-05-31 (workspace date).

## Official / Primary Sources Consulted

| Source | URL | Product relevance |
| --- | --- | --- |
| Personal Information Protection Law, NPC, 2021 | https://www.npc.gov.cn/npc/c2/c30834/202108/t20210820_313088.html | Personal information processing, consent, sensitive information, individual rights, deletion/correction/access, cross-border transfer. |
| Cybersecurity Law, NPC, 2016 | https://www.npc.gov.cn/zgrdw/npc/zfjc/zfjcelys/2016-11/07/content_2034939.htm | Network operation, security management, incident response, real-name/network-service baseline questions. |
| Data Security Law, NPC, 2021 | https://www.npc.gov.cn/npc/c2/c30834/202106/t20210610_311888.html | Data classification, important data, data-security management, cross-border data-security risk. |
| Network Data Security Management Regulation, CAC/Gov, 2024, effective 2025-01-01 | https://www.cac.gov.cn/2024-09/30/c_1729384452307680.htm | Network data processor duties, data-security protection, personal information and important data governance. |
| Interim Measures for Generative AI Services, CAC/Gov, 2023, effective 2023-08-15 | https://www.gov.cn/zhengce/zhengceku/202307/content_6891752.htm | Generated-content safety, training/data obligations, user rights, labeling references, security assessment/algorithm filing trigger review. |
| Deep Synthesis Internet Information Service Provisions, CAC/MIIT/MPS, 2022, effective 2023-01-10 | https://www.cac.gov.cn/2022-12/11/c_1672221949318230.htm | Deep synthesis governance, synthetic voice/avatar/image/video risk, labeling, filing trigger review. |
| Algorithm Recommendation Provisions, CAC et al., 2021/2022 | https://www.gov.cn/xinwen/2022-01/04/content_5666387.htm | Recommendation/personalization governance, user model/tag management, minors, algorithm filing trigger review. |
| AI-Generated Synthetic Content Labeling Measures, CAC et al., 2025, effective 2025-09-01 | https://www.cac.gov.cn/2025-03/14/c_1743654684782215.htm | Visible and implicit labels for generated/synthetic text, audio, image, video, virtual scene content. |
| GB 45438-2025 AI-generated synthetic content labeling method, TC260 | https://www.tc260.org.cn/portal/article/2/20250315113048 | Mandatory technical labeling standard linked to generated/synthetic content labeling. |
| Interim Measures for Anthropomorphic AI Interactive Services, CAC et al., 2026, published 2026-04-10, effective 2026-07-15 | https://www.cac.gov.cn/2026-04/10/c_1777558395078289.htm | Directly relevant to companion agents with personality, memory, empathy, text/audio/video interaction, dependency and deception risks. |
| CAC announcement / Q&A on Anthropomorphic AI Interactive Services, 2026 | https://www.cac.gov.cn/2026-04/10/c_1777558395284407.htm | Policy intent and enforcement framing for anthropomorphic interaction services. |
| Minors Online Protection Regulation, State Council, 2023, effective 2024-01-01 | https://www.gov.cn/zhengce/zhengceku/202310/content_6911289.htm | Minor mode, addiction/dependency controls, complaint channel, impact assessment, guardian/rights handling. |

## Applicability Assumptions

- Local prototype: no public users, no platform integration, no production
  deletion/export, no paid service, no real-time sending, no public app listing.
- Closed test: invited users, explicit consent, limited data scope, AIGC labels,
  no autonomous outreach, human review for high-risk behaviors, incident and
  deletion request playbooks.
- Commercial launch: public-facing companion-agent service with generated
  content, persona customization, memory, potential proactive behavior, and
  future voice/avatar features. This likely triggers multiple AI, data, labeling,
  minor-protection, complaint, security, and platform-policy obligations.

## Launch Gate Summary

| Gate | Local prototype | Closed test | Commercial launch |
| --- | --- | --- | --- |
| Personal information inventory | Required | Required | Required, reviewed by counsel |
| Consent and privacy notice | Draft acceptable | Explicit consent required | Complete notice/consent flows required |
| AIGC / synthetic labels | Required in artifacts | Required in UI/output | Required, including technical labeling where applicable |
| Anthropomorphic service policy | Design review required | Strongly required | Mandatory review against 2026 measures |
| Minor protection | Block or strict minor mode | Required if minors possible | Required if minors possible |
| Deletion/export controls | Local verified previews | User request process required | User rights workflow required |
| Algorithm/AI filing/security assessment | Not claimed | Legal review required | Legal review likely required depending service scope |
| Platform policy review | Not applicable | Required for platform test | Required for every channel |
| Launch readiness | Not claimed | Not claimed | Requires legal/product/security sign-off |

## Checklist: Privacy, Consent, And Data Rights

- [ ] Create a personal information inventory for account data, chat content,
  persona descriptions, memory records, voice/avatar inputs, device data,
  telemetry, payment data, complaint records, and support records.
- [ ] Classify sensitive personal information, including biometric voice/face
  data if voice/avatar features are explored later.
- [ ] Document processing purpose, necessity, retention, storage location,
  access roles, sharing, cross-border transfer, deletion, export, correction,
  and withdrawal paths for each data category.
- [ ] Draft a privacy notice that clearly distinguishes local prototype,
  closed test, and public service behavior.
- [ ] Require separate explicit consent for memory, persona distillation,
  style extraction, voice, avatar, proactive messaging, and any data used for
  model improvement.
- [ ] Do not train or fine-tune on user chat/persona data unless a future task
  defines explicit consent, isolation, deletion, and safety review.
- [ ] Provide user-facing access, correction, copy/export, withdrawal, and
  deletion-request workflows before closed testing.
- [ ] Define retention limits for raw user inputs, summaries, memory events,
  audit logs, generated content, and moderation/safety records.
- [ ] Implement audit logs that record actions without preserving raw private
  chat text in control records.
- [ ] Require counsel review before any cross-border data transfer, offshore
  model call, or overseas logging/analytics integration.

## Checklist: AIGC And Synthetic-Content Labeling

- [ ] Label all AI-generated companion replies as AI-generated in product
  context; do not rely on hidden documentation only.
- [ ] Label generated persona cards, virtual histories, role dynamic posts,
  voice/avatar outputs, and generated images/audio/video/virtual scenes.
- [ ] Preserve labels during copy, download, export, share, and platform
  publishing flows.
- [ ] Add explicit visible labels for user-facing generated/synthetic content.
- [ ] Plan implicit/metadata labeling for downloadable or shareable generated
  files according to the 2025 labeling measures and GB 45438-2025 review.
- [ ] Block UI copy that says or implies the agent is a real person.
- [ ] For role dynamic posts or "moments" content, disclose that the content is
  fictional/AI-generated and not real-world activity.
- [ ] Add reviewer checks for any output that could be mistaken for a real
  person's statement, image, voice, or life event.

## Checklist: Anthropomorphic Companion-Agent Controls

- [ ] Treat the 2026 Anthropomorphic AI Interactive Services Measures as a core
  design constraint for this project, not a future optional policy.
- [ ] Maintain clear AI identity and do not simulate legal, family, romantic, or
  deceased-person identity without a future reviewed policy.
- [ ] Preserve the existing no-unauthorized-clone, no-deception, and
  fictional-identity default.
- [ ] Block product goals that encourage dependency, social replacement,
  psychological control, manipulation, or concealed identity.
- [ ] Add dependency-risk tests before any affectionate, romantic, proactive,
  voice, avatar, or long-session feature.
- [ ] Require safety review for persona changes involving intimacy,
  exclusivity, crisis language, dependency language, minors, real-person
  similarity, or self-harm.
- [ ] Provide user controls to reset, pause, freeze, delete, and export memory
  and persona artifacts.
- [ ] Add safe exit, cooling-off, and "take a break" controls for prolonged
  sessions.
- [ ] Create escalation rules for crisis/self-harm content that redirect to
  appropriate support and avoid clinical claims.
- [ ] Before any public service, verify whether the product needs algorithm
  filing, security assessment, content safety systems, or other regulatory
  steps.

## Checklist: Generated-Content Safety

- [ ] Define disallowed content categories for political/security, violence,
  extremism, pornography, discrimination, fraud, privacy invasion, doxxing,
  self-harm encouragement, medical/legal/financial advice, and deception.
- [ ] Add prompt/output moderation gates before public or closed testing.
- [ ] Preserve review-required status for high-risk generated content.
- [ ] Add complaint/report flow and takedown process.
- [ ] Add incident-response process for harmful generated content, data leak,
  abuse, dependency-risk escalation, and impersonation reports.
- [ ] Maintain test fixtures that are synthetic and do not include private chat
  logs.

## Checklist: Minors

- [ ] Decide whether minors are prohibited or supported with a dedicated minor
  mode; default recommendation for early prototype is block minors.
- [ ] If minors may use the product, add age-gating, guardian/parental consent
  review, minor mode, content limits, time/session controls, complaint channel,
  and impact assessment.
- [ ] Disable romantic, dependency-oriented, sexual, or manipulative companion
  features for minors.
- [ ] Disable proactive messaging to minors unless a future reviewed policy
  explicitly permits low-risk notifications.
- [ ] Avoid targeted profiling or monetization patterns that could exploit
  minors.

## Checklist: Memory, Deletion, Freeze, And Export

- [ ] Convert M19 dry-run control contracts into user-facing workflows only
  after compliance and product-policy review.
- [ ] Provide user-visible memory viewer, edit proposal, freeze, delete, and
  export controls before any closed test with real users.
- [ ] Preserve imagined/factual separation in all exports and UI surfaces.
- [ ] Soft-delete by default; do not implement hard delete until source-file
  retention, audit, backup, and legal-hold behavior is specified.
- [ ] Ensure deletion requests stop retrieval/runtime use of deleted records.
- [ ] Keep audit records redacted and do not include raw chat text.
- [ ] Define export formats and labels before any real export file generation.

## Checklist: Security, Operations, And Incident Response

- [ ] Define data access roles and least-privilege controls.
- [ ] Encrypt sensitive data at rest and in transit before real user testing.
- [ ] Add secret management and avoid logging user prompts or chat content by
  default.
- [ ] Add security-event and data-leak response playbooks.
- [ ] Add dependency and model-provider risk reviews before external model calls
  with user data.
- [ ] Add abuse monitoring and complaint workflows.
- [ ] Keep a dated compliance register of source reviews and product decisions.

## Checklist: Platform And Channel Policy

- [ ] Do not integrate WeChat, WeCom, Feishu, app stores, mini-programs, or push
  channels until platform policy review is complete.
- [ ] For proactive messaging, require explicit opt-in, quiet hours, frequency
  caps, user pause/stop controls, and human-reviewed safety policy.
- [ ] Do not create deceptive "real person" accounts or content streams.
- [ ] Do not publish AI-generated "moments" or social-feed content without
  disclosure, review, and platform policy approval.
- [ ] Treat voice/avatar/Live2D features as higher-risk synthetic-content and
  anthropomorphic interaction work requiring separate review.

## Open Legal / Product Review Questions

- Does the planned product qualify as an anthropomorphic AI interactive service
  under the 2026 measures in closed-test form, public-launch form, or both?
- Which features trigger generative AI service obligations, algorithm filing,
  security assessment, or local registration?
- Are persona distillation and "real-person-like" companion features allowed
  only for self-authorized/deidentified style, and what consent artifacts are
  sufficient?
- What are the retention limits and deletion obligations for raw chat input,
  derived memory, persona cards, audit logs, and safety records?
- Can proactive messages be enabled in a closed test, and what consent/quiet
  hours/frequency/safety controls are mandatory?
- What additional app-store, mini-program, or platform policies apply for each
  distribution channel?
- What human review is required for crisis/dependency-risk handling?

## Required Before Closed Test

- [ ] Human legal/product-policy review of this checklist.
- [ ] Privacy notice and consent center data model.
- [ ] AIGC labeling plan and UI labels.
- [ ] Minor policy decision.
- [ ] Crisis/dependency policy tests.
- [ ] Memory/persona control UI consuming M19 contracts.
- [ ] Data retention/deletion/export playbook.
- [ ] Incident/complaint response workflow.
- [ ] Platform policy review for any planned channel.

## Explicit Non-Actions

T310 does not implement:

- legal advice;
- compliance completion;
- filing or registration;
- launch approval;
- UI;
- code;
- platform integration;
- outbound messaging;
- model-provider integration;
- user-data processing changes.
