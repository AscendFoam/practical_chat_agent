# M28 Local Review Workspace Scope

Task: T382 M28 Scope
Status: worker draft for review

## Objective

M28 turns the M27 review queue, dry-run apply plans, and distillation readiness
summaries into a local review workspace foundation.

The milestone should make candidate bindings, review artifact grouping,
review decision impact previews, and safe export manifests explicit before
any real mutation, private-data import, provider-backed extraction,
proactive outreach, voice/avatar behavior, platform delivery, public UI, or
commercial launch work.

M28 remains local, deterministic, synthetic-fixture-driven, and review-only.

## Why This Milestone Is Next

M27 closed with `PASS_WITH_WARNINGS` and three relevant warnings:

- review queue and dry-run artifacts are local records only;
- distillation readiness preserves supplied review queue refs without matching
  them to source candidate ids;
- dry-run plans preview effects but do not validate external cascade coverage.

The safest next step is not an apply executor. The next layer should first
prove that reviewed artifacts can be grouped, bound, inspected, and exported
without mutating memory/persona state or trusting mismatched refs.

## Product Rationale

The companion product needs users to understand why memory, persona growth, or
style-inspiration artifacts are waiting for review before the agent changes.
A local review workspace is the backend shape for later controls such as:

- memory/persona review inbox;
- before/after preview;
- consent and clone-risk blocking explanation;
- deletion/freeze/supersession preview;
- persona-growth preview;
- distillation readiness explanation;
- safe export for audit or debugging.

This matters for commercial trust because users should be able to inspect and
reject changes before the companion appears to remember, grow, or imitate a
style.

## M27 Invariants To Preserve

M28 implementation must preserve:

- review queue items are review-first and non-applying;
- review decisions are records only until a separately scoped apply executor
  exists;
- dry-run apply plans never mutate stores, write persona versions, or enable
  retrieval;
- distillation readiness never reads private data, retains source text, or
  synthesizes personas;
- candidate-kind and candidate-id binding must be explicit before a queue item
  can be associated with dry-run/readiness artifacts;
- workspace snapshots contain ids, safe summaries, reason labels, state flags,
  and issue codes only;
- no raw private transcript, provider credential, platform recipient, send
  queue, schedule, webhook, token, voice/avatar, audio/image/video payload, or
  generated media path appears in workspace records.

## Implementation Sequence

### T383 Review Workspace Binding Records

Implement local Pydantic records and deterministic helpers for:

- `ReviewWorkspaceCandidateBinding`;
- `ReviewWorkspaceArtifactBinding`;
- `ReviewWorkspaceBundle`;
- `ReviewWorkspaceService`.

Tests should prove that queue items bind only to matching source candidates,
dry-run/readiness artifacts keep matching refs, mismatches produce blocker
issues, and forbidden runtime/private/provider/media fields remain absent.

### T384 Review Workspace Snapshot Store

Implement a local JSON snapshot store for review workspace bundles.

Tests should prove snapshots can be saved, loaded, sorted, and filtered by
candidate kind, owner user, persona id, priority, and blocker status without
mutating source stores or storing raw private content.

### T385 Review Decision Impact Preview

Implement deterministic impact previews that combine review decisions with
their matching dry-run/readiness artifacts.

Tests should prove approve/reject/freeze/request-changes decisions are
referenced but not applied, and that the preview clearly reports what would
remain blocked before any future executor exists.

### T386 Review Workspace Safe Export Manifest

Implement a local export manifest for a selected review workspace snapshot.

Tests should prove exports contain only safe summaries, ids, reason labels,
issue codes, and synthetic refs; they must not include raw private text,
provider metadata, platform delivery state, media payloads, or generated media
paths.

### T387 M28 Milestone Review

Review code, tests, contracts, and residual risks before any later milestone
adds a user-facing review UI, real apply executor, real import/de-identification,
provider-backed extraction, proactive candidates, voice/avatar runtime, media
generation, platform delivery, or monetization.

## Local Synthetic Fixture Strategy

Fixtures should reuse M27 synthetic candidates:

- memory deletion cascade;
- memory supersession;
- memory contradiction;
- persona-growth patch;
- synthetic distillation manifest;
- de-identified style feature;
- distillation readiness summary;
- review queue items and decision records.

Fixture strings should use `[SYNTHETIC]` markers when they contain
user-facing summaries. Fixtures must not use real private names, raw chat
snippets, private file paths, screenshots, voice samples, photos, generated
media, provider metadata, platform recipient ids, or real source paths.

## Proposed Acceptance Gates

Each implementation task should run:

```powershell
$env:PYTHONPATH='src'
python -m py_compile <changed-python-files>
```

```powershell
$env:PYTHONPATH='src'
pytest <focused-test-files> -q -o cache_dir=artifacts\<task>_pytest_cache --basetemp=artifacts\<task>_pytest_basetemp
```

```powershell
git diff --check
```

No Browser QA is required unless a later task explicitly creates UI. No
network, package-manager, provider, platform, microphone, camera, or media
command should be required.

## Explicit Non-Goals

M28 must not implement or claim:

- private chat ingestion;
- raw private transcript reads;
- source readers for `private/chat_history/` or `private/distilled/`;
- model-provider calls;
- LLM extraction;
- embeddings, vector search, semantic ranking, similarity scoring, or
  fine-tuning;
- de-identification quality guarantees;
- real-person recreation or authorized digital twin support;
- persona synthesis from distillation inputs;
- final companion reply generation;
- runtime memory or persona mutation;
- decision apply paths;
- deletion executors or cache/index cascade executors;
- automatic persona-growth apply;
- proactive candidate generation;
- automatic sending, scheduling, notifications, queues, webhooks, tokens, or
  platform delivery;
- voice, ASR, TTS, voice cloning, microphone capture, generated audio, camera
  capture, avatar runtime, Live2D runtime, face tracking, generated images, or
  generated video;
- public hosting, production persistence, payment flows, analytics, launch
  approval, legal compliance completion, app-store acceptance, clinical
  validation, regulator acceptance, user-study validation, or real user
  evidence.

## M28 Exit Criteria

M28 can close when:

- review workspace bindings exist and are test-covered;
- mismatched queue item and source candidate ids are blocked;
- workspace snapshots can be locally stored and read without raw private data;
- review decision impact previews exist and are non-applying;
- safe export manifests exist and are test-covered;
- forbidden private/provider/outbound/platform/media fields are rejected or
  absent;
- no private data, provider calls, automatic sending, platform delivery,
  voice/avatar runtime, generated media, real-person recreation, launch claim,
  legal claim, clinical claim, or real user evidence has been introduced;
- residual risks are documented before M29.

## Residual Risks

- M28 will still not prove live companion quality or user trust.
- Workspace snapshots are local prototype records, not production persistence.
- No user-facing UI exists unless separately scoped later.
- No actual memory lifecycle or persona-growth mutation executor exists.
- No real import/de-identification quality, semantic retrieval quality, or
  similarity-risk quality evaluation exists.
- Voice/avatar, proactive messaging, platform delivery, commercial packaging,
  and virtual social feed behavior remain locked for later scoped milestones.
