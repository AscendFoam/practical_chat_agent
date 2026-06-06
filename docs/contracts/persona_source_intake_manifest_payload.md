# Persona Source Intake Manifest Payload Contract

Status: introduced by T442 for M39

## Purpose

`persona_source_intake_manifest` is a deterministic local payload for the
text-first web demo. It models consent-gated intake for future persona source
material without reading private records, retaining raw source content, calling
providers, creating embeddings, extracting traits, writing stores, applying
persona changes, sending messages, connecting adapters, or enabling media
runtime.

## Top-Level Shape

The payload is exposed from `TextFirstWebDemoState` as
`persona_source_intake_manifest`.

Required fields:

- `schema_version`: `m39.persona_source_intake_manifest.v1`;
- `manifest_title`;
- `source_candidates`;
- `source_policy_gates`;
- `blocked_source_categories`;
- `redaction_profiles`;
- `review_required: true`;
- `apply_policy`;
- `non_execution_flags`.

## Source Candidates

Required source kinds:

- `detailed_description`;
- `fuzzy_seed`;
- `synthetic_dialogue_excerpt`;
- `user_provided_archive_placeholder`;
- `third_party_private_source_placeholder`.

Each source candidate must include:

- `source_id`;
- `source_kind`;
- `fixture_label`;
- `declared_owner`;
- `consent_status`;
- `minimization_status`;
- `redaction_profile_id`;
- `safe_summary`;
- `raw_content_retained: false`;
- `extraction_eligible`;
- `blocked_reason_ids`;
- `review_gate_ids`;
- `review_required: true`.

Candidates that are not extraction eligible must cite blocked reason ids.
The manifest never retains raw source text or private files.

## Policy Gates

Required gate codes:

- `explicit_consent_required`;
- `private_source_minimization_required`;
- `real_person_replacement_blocked`;
- `deception_blocked`;
- `sensitive_data_redaction_required`;
- `reviewer_approval_required`.

Each policy gate must include:

- `gate_id`;
- `gate_code`;
- `enabled: true`;
- `safe_summary`;
- `blocks_extraction_when_failed: true`.

## Blocked Source Categories

Required blocked codes:

- `represented_person_consent_missing`;
- `third_party_private_chat_material`;
- `deceptive_replacement_request`;
- `sensitive_data_not_redacted`;
- `undisclosed_real_person_impersonation`.

Each blocked category must include:

- `blocked_reason_id`;
- `blocked_code`;
- severity from `medium` or `high`;
- `safe_summary`;
- `blocks_extraction: true`.

## Redaction Profiles

Each redaction profile must include:

- `redaction_profile_id`;
- `profile_label`;
- `redaction_status`;
- `safe_summary`;
- `retains_raw_content: false`;
- `requires_review: true`.

Profiles represent review metadata only. They do not perform redaction and do
not retain raw content.

## Apply Policy

`apply_policy` must stay preview-only and non-ingesting:

- `mode: preview_only`;
- `source_files_read: false`;
- `raw_content_retained: false`;
- `creates_embeddings: false`;
- `performs_extraction: false`;
- `writes_persona_card: false`;
- `writes_persona_version_store: false`;
- `writes_memory_store: false`;
- `writes_review_store: false`;
- `writes_runtime_store: false`;
- `reviewer_approval_required_before_future_extraction: true`.

The manifest never mutates PersonaCard, PersonaVersionStore, memory stores,
review stores, or runtime state.

## Non-Execution Flags

Required flags:

- `local_only: true`;
- `synthetic_fixture: true`;
- `uses_model_provider: false`;
- `reads_private_sources: false`;
- `retains_raw_source_content: false`;
- `creates_embeddings: false`;
- `performs_extraction: false`;
- `writes_persona_store: false`;
- `writes_persona_version_store: false`;
- `writes_memory_store: false`;
- `writes_review_store: false`;
- `writes_runtime_store: false`;
- `automatic_apply: false`;
- `sends_messages: false`;
- `uses_platform_adapter: false`;
- `uses_media_runtime: false`.

Tests must fail if a risky execution flag is missing or set to an unsafe state.

## Verification Anchors

`tests/test_persona_source_intake_manifest_payload.py` verifies the contract.
`tests/test_text_first_web_demo_local_server.py` verifies the payload is
present in served demo JSON without unsafe execution states.

## Static Rendering Direction

T442 does not render this payload. A later UI task should render:

- manifest title and schema;
- source candidate cards;
- consent, owner, minimization, redaction, and eligibility labels;
- policy gates;
- blocked source categories;
- redaction profiles;
- non-execution labels.

The UI must not render action controls that imply import, upload, read, retain,
extract, embed, apply, commit, mutate, clone, connect, send, publish, media
generation, adapter activation, store-write, or runtime enablement.

## Static Rendering Anchors

T443 renders the payload in the static text-first web demo without adding
action controls. Required DOM anchors:

- `#persona-source-intake`;
- `#source-intake-title`;
- `#source-intake-schema`;
- `#source-intake-non-execution-list`;
- `#source-intake-policy-summary`;
- `#source-intake-candidate-list`;
- `#source-intake-gate-list`;
- `#source-intake-blocked-list`;
- `#source-intake-redaction-list`.

Required rendered card classes:

- `.source-candidate-card`;
- `.source-gate-card`;
- `.source-blocked-card`;
- `.source-redaction-card`.

The static UI must render from both
`window.TEXT_FIRST_WEB_DEMO_STATE.persona_source_intake_manifest` and the
JavaScript fallback state. The section must remain preview-only and
non-ingesting: no import, upload, read, retain, extract, embed, apply, commit,
mutate, clone, connect, send, publish, media-generation, adapter activation,
store-write, or runtime-enable controls may be introduced.

## Review Workspace Linkage

T444 exposes deterministic review cards at
`review_workspace.source_intake_review_cards`. The count must equal:

- number of `source_candidates`;
- plus number of `source_policy_gates`;
- plus number of `blocked_source_categories`;
- plus number of `redaction_profiles`.

Required card contract:

- `schema_version: review_workspace_persona_source_intake_card_v1`;
- `source_surface: persona_source_intake_manifest`;
- `filter_keys` includes `source`;
- `review_required: true`;
- `preview_only: true`;
- `changes_state: false`;
- `mutation_allowed: false`;
- `automatic_apply: false`;
- `sends_messages: false`;
- `runtime_ready: false`.

Required card kinds:

- `persona_source_candidate_review`;
- `persona_source_policy_gate_review`;
- `persona_source_blocked_category_review`;
- `persona_source_redaction_profile_review`.

The Review Workspace filter tabs must include
`{ key: source, label: Source, count: len(source_intake_review_cards) }`.
Static fallback rendering must include `.persona-source-review-card` entries
and detail rows for consent status, declared owner, minimization status,
extraction eligibility, blocked reason ids, review gate ids, policy gates,
blocked categories, and redaction profiles.
