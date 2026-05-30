# AIGC Labeling Contract

Task: T313 AIGC Labeling Plan
Status: worker draft for review

## Scope

This contract defines reusable local labeling metadata for AI-generated and
synthetic companion-agent content. It supports visible labels, metadata labels,
review requirements, and privacy-safe surface mapping.

It does not insert watermarks, write files, publish content, share content,
capture consent, call model providers, call platform services, or claim legal
or platform compliance.

Implemented model:

- `AIGCLabelingRequirement`

Implemented literal sets:

- `AIGCContentModality`
- `AIGCProductSurface`

## AIGCContentModality

Supported modalities:

- `text`
- `image`
- `audio`
- `video`
- `virtual_scene`
- `persona`
- `virtual_history`
- `role_dynamic_post`
- `export`
- `shared_content`

The values are intentionally distinct so later UI/export code can decide
whether a local text disclosure is enough or whether copy/download/export/share
metadata labels are also required.

## AIGCProductSurface

Supported product surfaces:

- `companion_reply`
- `persona_card`
- `virtual_history`
- `role_dynamic_post`
- `export_manifest`
- `shared_content`
- `voice_avatar`
- `web_demo`

The values describe where the content appears, not where it is delivered. They
do not encode external platforms, queues, webhooks, tokens, or delivery targets.

## AIGCLabelingRequirement

| Field | Meaning |
| --- | --- |
| `schema_version` | Always `aigc_labeling_requirement_v1`. |
| `requirement_id` | Generated local labeling requirement id. |
| `user_id` | Owner user id. |
| `content_id` | Local generated/synthetic content id. |
| `content_modality` | One `AIGCContentModality`. |
| `product_surface` | One `AIGCProductSurface`. |
| `visible_label_required` | Always true. |
| `visible_label_text` | Human-visible AI/synthetic disclosure text. |
| `disclosure_labels` | Normalized disclosure label list. |
| `metadata_label_required` | Whether metadata/implicit labels are required before copy/download/export/share. |
| `metadata_labels` | Metadata label list, including `implicit_metadata_label` when required. |
| `copy_download_export_share_requires_metadata` | Whether outbound-capable user actions require metadata labels. |
| `review_required` | Always true in this contract. |
| `source_refs` | Redacted local source references only. |
| `created_at` | Requirement creation timestamp. |

`AIGCLabelingRequirement.from_disclosure_labels(...)` maps existing local label
lists, such as `AIGCDisclosureMetadata`, into the reusable requirement shape.

## Normalized Labels

Every requirement includes:

- `ai_generated`
- `synthetic_content`
- `review_required`

Virtual histories and role dynamic posts also include:

- `imagined_content`
- `not_real_world_activity`

Generated image, audio, video, virtual-scene, export, shared-content,
export-manifest, voice-avatar, and shared-content surfaces also include:

- `implicit_metadata_label`

## Visible Label Text

Default generated/synthetic content label:

```text
AI-generated synthetic content.
```

Virtual history and role dynamic post label:

```text
AI-generated synthetic imagined companion content. Not real-world activity.
```

The visible label must mention AI-generated and synthetic content. Imagined
role-life surfaces also receive explicit imagined/not-real-world wording.

## Invariants

- Visible labels are required for every generated/synthetic content surface.
- Every requirement is review-required.
- `ai_generated`, `synthetic_content`, and `review_required` are never dropped.
- Virtual history and role dynamic post labels preserve imagined/not-real-world
  disclosure.
- Copy/download/export/share-capable generated media or manifests require
  `implicit_metadata_label`.
- Payloads contain no raw private chat text.
- Payloads expose no send, schedule, delivery, platform, webhook, token, or
  queue fields.
- `source_refs` must stay redacted local references, not raw transcripts or
  private messages.

## Mapping From Existing Models

| Existing object | Mapping |
| --- | --- |
| `AIGCDisclosureMetadata` | Use `from_disclosure_labels(...)`; `synthetic_content` is added if absent. |
| `RoleDynamicPost` | `content_modality=role_dynamic_post`, `product_surface=role_dynamic_post`. |
| Persona virtual history | `content_modality=virtual_history`, `product_surface=virtual_history`. |
| `ControlExportManifest` | `content_modality=export`, `product_surface=export_manifest`. |
| Future shared content | `content_modality=shared_content`, `product_surface=shared_content`. |
| Future voice/avatar media | `content_modality=audio` or `video`, `product_surface=voice_avatar`. |

## Non-Actions

T313 does not implement:

- legal advice;
- compliance completion;
- watermarking;
- file metadata insertion;
- export writing;
- copy, download, share, publish, send, or schedule actions;
- UI;
- platform integration;
- model-provider calls;
- private chat-log reads;
- launch or app-store approval.

## Verification

Expected minimum verification:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\core\models.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_aigc_labeling_plan_contract.py tests\test_virtual_life_aigc_labeling.py tests\test_consent_center_data_model.py -q
```

```powershell
git diff --check
```
