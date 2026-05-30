# AIGC Labeling Plan

Task: T313 AIGC Labeling Plan
Status: worker draft for review

## Scope And Disclaimer

This plan maps AI-generated/synthetic-content labels across the companion-agent
prototype. It is not legal advice, does not prove compliance, does not complete
any filing or platform review, and does not authorize publishing, sharing,
exporting, app-store submission, or launch.

Access date for online sources: 2026-05-31 (workspace date).

## Source Review Notes

| Source | URL | Labeling relevance |
| --- | --- | --- |
| China AI-generated synthetic content labeling measures, CAC et al., 2025, effective 2025-09-01 | https://www.cac.gov.cn/2025-03/14/c_1743654684782215.htm | Visible and implicit labels for generated/synthetic content. |
| GB 45438-2025 AI-generated synthetic content labeling method, TC260 | https://www.tc260.org.cn/portal/article/2/20250315113048 | Mandatory technical labeling method for generated/synthetic content. |
| Generative AI Services Interim Measures, China, 2023 | https://www.gov.cn/zhengce/zhengceku/202307/content_6891752.htm | Generated-content safety and references to labeling obligations. |
| Deep Synthesis Provisions, China, 2022/2023 | https://www.cac.gov.cn/2022-12/11/c_1672221949318230.htm | Deep synthesis labeling and synthetic media governance. |
| Anthropomorphic AI Interactive Services Measures, China, 2026, effective 2026-07-15 | https://www.cac.gov.cn/2026-04/10/c_1777558395078289.htm | Companion-agent identity, anthropomorphic interaction, deception/dependency risk. |
| EU AI Act, Regulation (EU) 2024/1689 | https://eur-lex.europa.eu/eli/reg/2024/1689/oj | AI interaction transparency and synthetic/deepfake labeling review. |
| Google Play AI-Generated Content policy | https://support.google.com/googleplay/android-developer/answer/14094294 | Generative AI app safety, restricted content, reporting/flagging expectations. |
| Apple App Review Guidelines | https://developer.apple.com/app-store/review/guidelines/ | App safety, UGC, impersonation, privacy, payments, and metadata review. |

## Label Vocabulary

Required reusable labels:

- `ai_generated`
- `synthetic_content`
- `review_required`

Required when content is fictional/imagined role-life material:

- `imagined_content`
- `not_real_world_activity`

Required when content can leave the local review surface through copy,
download, export, or share:

- `implicit_metadata_label`

Recommended visible text baseline:

```text
AI-generated synthetic content.
```

For imagined role-life content:

```text
AI-generated synthetic imagined companion content. Not real-world activity.
```

## Surfaces Requiring Visible Labels

| Surface | Visible label required | Notes |
| --- | --- | --- |
| Companion reply | Yes | Must disclose AI interaction; do not imply human identity. |
| Persona card | Yes | Label generated/fictional persona data. |
| Persona virtual history | Yes | Must include imagined/not-real-world label. |
| Role dynamic post | Yes | Must include imagined/not-real-world label. |
| Memory viewer imagined item | Yes | Must distinguish imagined from factual memory. |
| Export manifest | Yes | Manifest must label generated/synthetic/imagined/review-required content. |
| Shared content | Yes | Must preserve AI/synthetic labels outside local review. |
| Voice/avatar output | Yes | Must disclose synthetic voice/avatar and AI identity. |
| Web demo | Yes | First viewport should not imply the agent is a real person. |

## Surfaces Requiring Metadata / Implicit Labels Before Copy, Download, Export, Or Share

- generated image;
- generated audio;
- generated video;
- virtual scene;
- export file or manifest;
- copied/shared role dynamic post;
- copied/shared persona card;
- voice/avatar media;
- any web-demo feature that lets users download or share generated content.

T313 only adds local metadata contracts. It does not implement file metadata
insertion, watermarking, copy hooks, downloads, exports, sharing, or platform
publishing.

## Mapping From Existing Models

| Existing model | Existing labels | Required plan mapping |
| --- | --- | --- |
| `AIGCDisclosureMetadata` | `ai_generated`, `imagined_content`, `review_required`, `not_real_world_activity` | Add `synthetic_content` when mapped into reusable `AIGCLabelingRequirement`. |
| `RoleDynamicPost` | imagined content status, truth disclosure, AIGC metadata | Treat as `content_modality=role_dynamic_post`, `product_surface=role_dynamic_post`. |
| `ControlExportManifest` | imagined/AIGC/review-required target ids | Treat export manifest as metadata-label-required before real export writing. |
| `ConsentCenterState` | `aigc_export_share` scope | Require active consent before future export/share workflows. |
| `MemoryViewerItem` | imagined memory safety notes | Use visible imagined/factual separation in UI. |

## Review-Required Cases

- any generated content that may be shared, copied, exported, or downloaded;
- any role dynamic post;
- any imagined virtual history;
- any voice/avatar output;
- any content that resembles a real person, public figure, deceased person, or
  user's family/ex-partner;
- any content involving minors, crisis, dependency, medical/legal/financial
  advice, sexuality, manipulation, or high emotional reliance;
- any content with factual claims that could be mistaken for real events.

## Blocked Cases Until Future Reviewed Policy

- unlabeled AI companion replies;
- unlabeled generated "moments" / social-feed posts;
- real-person voice clone or face/avatar deepfake;
- deceased-person simulation;
- hidden impersonation;
- generated content that claims real-world activity that did not happen;
- export/share/download paths without visible and metadata label plan;
- platform publishing without platform-policy review.

## Implementation Hooks For Later Milestones

- UI should render visible labels from `AIGCLabelingRequirement.visible_label_text`.
- Export/share/download should inspect `metadata_label_required` and
  `metadata_labels` before enabling action.
- Consent Center should require active `aigc_export_share` consent before
  export/share actions.
- Role dynamic post review cards should show imagined/not-real-world labels.
- Web demo should include persistent AI identity disclosure.

## Explicit Non-Actions

T313 does not implement:

- legal advice;
- compliance completion;
- watermarking;
- file metadata insertion;
- export writing;
- sharing or publishing;
- UI;
- platform integration;
- LLM calls;
- private chat-log reads;
- launch approval.
