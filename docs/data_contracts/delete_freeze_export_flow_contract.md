# Delete / Freeze / Export Flow Contract

Task: T303 Delete / Freeze / Export Local Flow Contract
Status: worker draft for review

## Scope

The delete/freeze/export flow contract defines local dry-run preview,
confirmation, audit, and export-manifest data objects for high-impact control
operations. It does not mutate records, delete files, write export files, call
an LLM, read private chat logs, schedule work, or integrate with platforms.

Implementation objects:

- `ControlOperationTarget`
- `ControlOperationPreview`
- `ControlOperationConfirmation`
- `ControlAuditEvent`
- `ControlExportManifest`

## ControlOperationTarget

| Field | Meaning |
| --- | --- |
| `schema_version` | Always `control_operation_target_v1`. |
| `artifact_type` | Target artifact category. |
| `artifact_id` | Target artifact id. |
| `user_id` | Owner user id. |
| `persona_id` | Optional persona id. |
| `current_state` | Current lifecycle/status summary. |
| `review_required` | Whether the target requires review. |
| `retrieval_eligible` | Current retrieval eligibility. |
| `runtime_eligible` | Current runtime eligibility. |
| `provenance_refs` | Provenance references. |
| `safety_labels` | Safety and disclosure labels. |

Supported `artifact_type` values:

- `memory_event`
- `persona_card`
- `persona_version_record`
- `role_dynamic_post`
- `proactive_consent`
- `proactive_review_card`

## ControlOperationPreview

| Field | Meaning |
| --- | --- |
| `schema_version` | Always `control_operation_preview_v1`. |
| `preview_id` | Generated dry-run preview id. |
| `operation` | `soft_delete`, `hard_delete`, `freeze`, `unfreeze`, or `export`. |
| `target` | `ControlOperationTarget`. |
| `reason` | Human-readable reason. |
| `dry_run` | Always true. |
| `requires_confirmation` | Always true. |
| `hard_delete` | True only for `hard_delete`. |
| `would_change_state_to` | State that would result if a future operation executed. |
| `retrieval_eligible_after` | Previewed retrieval eligibility. |
| `runtime_eligible_after` | Previewed runtime eligibility. |
| `source_files_untouched` | Always true. |
| `writes_records` | Always false. |
| `writes_export_files` | Always false. |
| `safety_flags` | Review and safety flags. |
| `created_at` | Preview timestamp. |

Delete and freeze previews mark retrieval/runtime eligibility false. Export
previews keep current eligibility and are manifest-only.

## ControlOperationConfirmation

| Field | Meaning |
| --- | --- |
| `schema_version` | Always `control_operation_confirmation_v1`. |
| `confirmation_id` | Generated confirmation id. |
| `preview_id` | Required dry-run preview id. |
| `operation` | Operation copied from preview. |
| `target` | Target copied from preview. |
| `actor_id` | Human actor id. |
| `confirmed` | Whether the preview was explicitly confirmed. |
| `confirmation_phrase` | Required when `confirmed=true`. |
| `confirmation_status` | `confirmed` or `rejected`; `dry_run_only` is reserved for audit without confirmation. |
| `reason` | Confirmation reason. |
| `executes_operation` | Always false. |
| `writes_records` | Always false. |
| `writes_export_files` | Always false. |
| `created_at` | Confirmation timestamp. |

Confirmations are records of human intent only. They do not execute the
operation.

## ControlAuditEvent

| Field | Meaning |
| --- | --- |
| `schema_version` | Always `control_audit_event_v1`. |
| `audit_id` | Generated audit id. |
| `actor_id` | Human actor id. |
| `user_id` | Target owner. |
| `target` | Control target. |
| `operation` | Control operation. |
| `before_summary` | Redacted before-state summary. |
| `after_summary` | Redacted after-state summary. |
| `reason` | Preview reason. |
| `confirmation_status` | `dry_run_only`, `confirmed`, or `rejected`. |
| `safety_flags` | Safety flags. |
| `source_surface` | Local surface id. |
| `redacted_content_only` | Always true. |
| `writes_records` | Always false. |
| `writes_export_files` | Always false. |
| `created_at` | Audit timestamp. |

## ControlExportManifest

| Field | Meaning |
| --- | --- |
| `schema_version` | Always `control_export_manifest_v1`. |
| `export_id` | Generated manifest id. |
| `user_id` | Export owner. |
| `format` | Always `manifest_json`. |
| `reason` | Manifest reason. |
| `targets` | Selected targets. |
| `target_count` | Derived target count. |
| `include_provenance` | Whether provenance refs are included. |
| `provenance_refs` | Aggregated provenance refs. |
| `contains_imagined_content` | Derived from target labels. |
| `contains_aigc_content` | Derived from target labels. |
| `contains_review_required_items` | Derived from target review flags and labels. |
| `imagined_target_ids` | Targets labeled as imagined. |
| `aigc_target_ids` | Targets labeled as AIGC. |
| `review_required_target_ids` | Targets requiring review. |
| `redacted_content_only` | Always true. |
| `source_files_untouched` | Always true. |
| `writes_export_files` | Always false. |
| `generated_at` | Manifest timestamp. |

## Invariants

- Every high-impact operation starts as a dry-run preview.
- Confirmations reference a preview and do not execute the operation.
- Delete distinguishes `soft_delete` from `hard_delete`.
- Delete and freeze previews make affected artifacts non-retrieval/runtime
  eligible in the preview.
- Audit events preserve actor, user, target, operation, summaries, reason,
  confirmation status, timestamp, and safety flags.
- Export manifests label imagined content, AIGC content, review-required
  targets, and provenance refs.
- Payloads are redacted summaries only.
- Payloads expose no send, schedule, delivery, platform, webhook, token, or
  queue fields.

## Non-Actions

T303 does not implement:

- UI;
- APIs;
- persistence;
- actual deletion;
- actual freeze/unfreeze;
- real export writing;
- source-file removal;
- version-store writes;
- LLM calls;
- private chat-log reads;
- memory retrieval changes;
- proactive candidates;
- schedulers;
- outbound requests;
- platform integration;
- voice/avatar/deepfake behavior;
- web demo behavior.

## Verification

Expected minimum verification:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\core\models.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_delete_freeze_export_flow_contract.py tests\test_memory_viewer_contract.py tests\test_persona_version_editor_contract.py -q
```

```powershell
git diff --check
```
