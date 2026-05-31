# M29 Review Workspace Presentation Scope

Task: T388 M29 Scope
Status: worker draft for review

## Objective

M29 turns the M28 local review workspace records into a local, inspectable
presentation layer for the text-first companion demo.

The milestone should make pending review items, blockers, decision impact
previews, and safe export summaries understandable in UI-ready view models
before any real mutation, private-data import, provider-backed extraction,
proactive outreach, voice/avatar behavior, platform delivery, public UI, or
commercial launch work.

M29 remains local, deterministic, synthetic-fixture-driven, and review-only.

## Why This Milestone Is Next

M28 closed with `PASS_WITH_WARNINGS` and three relevant warnings:

- review workspace records remain local prototype records only;
- safe exports summarize already-created safe records but do not prove source
  safety;
- future manual apply eligibility is a preview label, not executable
  authority.

The safest next step is a presentation adapter and local static panel, not an
apply executor. Reviewers should be able to see why a memory/persona/style
artifact is pending or blocked before any later task mutates state.

## Product Rationale

The companion product needs a user-control surface where users can inspect:

- what the companion wants to remember or change;
- why a persona-growth patch is blocked or eligible for later manual apply;
- what a style-distillation readiness summary means;
- which changes are review-only and non-executing;
- which records can be exported safely for audit/debugging.

This matters for trust because the companion should not silently change memory
or persona behavior. The review workspace presentation layer is the bridge
between backend review records and a later usable local web demo.

## M28 Invariants To Preserve

M29 implementation must preserve:

- workspace records are review-required and non-applying;
- review decisions are preview labels only until a separately scoped apply
  executor exists;
- safe exports contain ids, safe summaries, labels, refs, issue codes, counts,
  and flags only;
- no raw private transcript, provider credential, platform recipient, send
  queue, schedule, webhook, token, voice/avatar, audio/image/video payload, or
  generated media path appears in presentation records;
- no UI action mutates memory/persona state or writes PersonaVersionStore;
- no UI action sends, schedules, notifies, calls providers, or connects to
  platform/media runtimes.

## Implementation Sequence

### T389 Review Workspace Presentation Adapter

Implement local Pydantic view models and deterministic helpers for:

- review workspace summary cards;
- blocker summaries;
- decision impact summaries;
- safe export summary cards;
- tab/filter metadata for a future local UI.

Tests should prove that view models contain only safe fields, preserve
non-apply flags, order items deterministically, and expose no runtime,
provider, mutation, outbound, voice/avatar, or media behavior.

### T390 Review Workspace Static Panel

Add a local static review panel to the existing text-first web demo assets.

The panel should consume a synthetic payload from T389 and display review
items, blocker states, decision outcomes, and safe export counts. It must be
local-only, static, synthetic, non-sending, non-mutating, and accessible.

### T391 Review Workspace Local Server Payload

Expose the review workspace panel payload through the existing local demo
server shape if needed.

The route or payload helper must serve synthetic-only data, must not read
private files, and must not add provider/platform/media/runtime integration.

### T392 M29 Milestone Review

Review code, tests, contracts, local UI assets, and residual risks before any
later milestone adds real apply executors, real import/de-identification,
provider-backed extraction, proactive candidates, voice/avatar runtime, media
generation, platform delivery, monetization, or production persistence.

## Local Synthetic Fixture Strategy

Fixtures should reuse M28 synthetic records:

- review workspace candidate bindings;
- artifact bindings;
- snapshot bundles;
- decision impact previews;
- safe export manifests.

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

Browser QA is required only for tasks that modify static UI assets or local
server behavior. No network, package-manager, provider, platform, microphone,
camera, or media command should be required.

## Explicit Non-Goals

M29 must not implement or claim:

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

## M29 Exit Criteria

M29 can close when:

- review workspace presentation view models exist and are test-covered;
- local static UI can render a synthetic review workspace panel;
- local server/static payload behavior is verified if touched;
- review-only/non-apply flags remain visible;
- blocker and decision impact states are understandable;
- forbidden private/provider/outbound/platform/media fields are rejected or
  absent;
- no private data, provider calls, automatic sending, platform delivery,
  voice/avatar runtime, generated media, real-person recreation, launch claim,
  legal claim, clinical claim, or real user evidence has been introduced;
- residual risks are documented before M30.

## Residual Risks

- M29 will still not prove live companion quality or user trust.
- M29 will still not implement real memory lifecycle or persona-growth
  mutation.
- Review UI will use synthetic local fixtures, not real user data.
- No real import/de-identification quality, semantic retrieval quality, or
  similarity-risk quality evaluation exists.
- Voice/avatar, proactive messaging, platform delivery, commercial packaging,
  and virtual social feed behavior remain locked for later scoped milestones.
