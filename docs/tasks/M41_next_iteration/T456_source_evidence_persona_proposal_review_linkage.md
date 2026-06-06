# T456: Source Evidence Persona Proposal Review Linkage

## Task ID

T456

## Goal

Expose deterministic `source_evidence_persona_proposal` records in Review
Workspace.

This task links the already-rendered M41 proposal payload into review cards
only. It must not read private data, add source readers, call model providers,
create embeddings, extract traits from real content, write stores, apply
persona changes, send messages, connect platform adapters, or enable media
runtime.

## Context

T454 introduced the source-evidence-to-persona-proposal payload. T455 rendered
the payload in the static text-first demo. T456 should make proposal
candidates, risk labels, rollback notes, review gate results, and outcome
labels inspectable from Review Workspace while preserving preview-only,
non-extracting, non-mutating semantics.

## Allowed Files

Future T456 worker may create or modify only:

- `src/practical_chat_agent/ui/text_first_web_demo_adapter.py`
- `src/practical_chat_agent/ui/static/text_first_web_demo.js`
- `tests/test_source_evidence_persona_proposal_review_linkage.py`
- `tests/test_source_evidence_persona_proposal_payload.py`
- `tests/test_text_first_web_demo_local_server.py`
- `tests/test_text_first_web_demo_static.py`
- `tests/test_text_first_web_demo_state_switching.py`
- `docs/contracts/source_evidence_persona_proposal_payload.md`
- `docs/tasks/M41_next_iteration/T457_source_evidence_persona_proposal_responsive_hardening.md`
- `docs/worker_summary/T456_worker_summary.md`
- `docs/07_handoff.md`

If implementation requires source readers, model providers, private data,
runtime stores, platform adapters, outbound messaging, media runtime,
automatic apply, package changes, or task-board edits, Captain must revise this
package before assignment.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not ingest, summarize, transform, quote, or commit real private chat
  records.
- Do not call model providers or prompt execution layers.
- Do not add source readers, embeddings, vector search, semantic ranking,
  similarity scoring, fine-tuning, or remote inference.
- Do not add real extraction, source import, upload, raw retention, or
  automatic persona mutation.
- Do not write PersonaCard, PersonaVersionStore, MemoryEventStore, review
  stores, runtime stores, local databases, queues, schedulers, or files outside
  the allowed files.
- Do not add platform adapters, webhooks, auth, tokens, recipient ids, delivery
  state, automatic outreach, or outbound messaging.
- Do not add microphone, camera, ASR, TTS, voice cloning, Live2D, generated
  audio, generated image, generated video, or media capture.
- Do not add payment processing, production pricing claims, legal advice,
  compliance completion, app-store approval, launch approval, clinical claims,
  regulator acceptance, or user-study validation.
- Do not modify `docs/04_task_board.md`.

## Expected Implementation

### 1. Adapter Review Cards

Add `review_workspace.source_proposal_review_cards`.

The count must equal:

- number of `proposal_candidates`;
- plus number of `risk_labels`;
- plus number of `rollback_notes`;
- plus number of `review_gate_results`;
- plus number of `proposal_outcome_labels`.

Required card contract:

- `schema_version: review_workspace_source_evidence_persona_proposal_card_v1`;
- `source_surface: source_evidence_persona_proposal`;
- `filter_keys` includes `proposal`;
- `review_required: true`;
- `preview_only: true`;
- `changes_state: false`;
- `mutation_allowed: false`;
- `automatic_apply: false`;
- `sends_messages: false`;
- `runtime_ready: false`.

Required card kinds:

- `source_persona_proposal_candidate_review`;
- `source_persona_proposal_risk_review`;
- `source_persona_proposal_rollback_review`;
- `source_persona_proposal_gate_review`;
- `source_persona_proposal_outcome_review`.

Review Workspace filter tabs must include:

- `{ key: proposal, label: Proposal, count: len(source_proposal_review_cards) }`;
- update `{ key: persona }` count if proposal cards also carry persona filters.

### 2. Static Fallback Linkage

Update the JavaScript fallback state so Review Workspace exposes proposal cards
when static HTML is opened directly.

### 3. Rendered Detail Rows

Review cards should show relevant detail rows for:

- proposal candidate field path, confidence, trait ids, evidence ids, risk
  ids, rollback ids, review gate ids, mutation state, and review state;
- risk code, severity, summary, and auto-apply blocking state;
- rollback id, restore summary, and runtime rollback readiness;
- gate code, status, summary, and apply blocking state;
- outcome label and summary.

## Tests

Use TDD:

1. Add failing review-linkage tests.
2. Run focused tests and capture RED output.
3. Implement adapter and static fallback linkage.
4. Re-run focused tests and capture GREEN output.
5. Run `python -m py_compile` and `node --check`.

## Browser QA

After tests pass, verify Review Workspace proposal filters at the available
viewport if a browser automation target is available:

- `Proposal` filter tab is visible with expected count;
- source proposal review cards render;
- proposal-card detail rows are visible;
- no forbidden action controls appear;
- no horizontal overflow.

If no callable browser automation tool is available, do not claim browser QA.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'; pytest tests\test_source_evidence_persona_proposal_review_linkage.py tests\test_source_evidence_persona_proposal_payload.py tests\test_text_first_web_demo_local_server.py tests\test_text_first_web_demo_static.py tests\test_text_first_web_demo_state_switching.py -q -o cache_dir=artifacts\t456_pytest_cache --basetemp=artifacts\t456_pytest_basetemp
```

```powershell
python -m py_compile src\practical_chat_agent\ui\text_first_web_demo_adapter.py
```

```powershell
node --check src\practical_chat_agent\ui\static\text_first_web_demo.js
```

```powershell
git diff --check
```

## Reviewer Type

Review Workspace linkage review for proposal-card counts, filter behavior,
detail rows, preview-only semantics, non-extracting guarantees, non-mutating
guarantees, and absence of private/provider/runtime surfaces.
