# M27 Review Queue And Dry-Run Apply Scope

Task: T376 M27 Scope
Status: worker draft for review

## Objective

M27 turns the M26 candidate records into a local review queue and dry-run apply
foundation.

The milestone should make review operations executable before any real
mutation, private-data import, provider-backed extraction, proactive outreach,
voice/avatar behavior, platform delivery, or commercial launch work. The
implementation layer is:

```text
synthetic fixtures + review queue records + deterministic dry-run apply plans + tests
```

M27 is not a runtime companion, platform, media, or real-person recreation
milestone.

## Product Rationale

The companion product needs users to understand and control how memory,
persona, and de-identified style inputs affect the agent. M26 created
candidate records; M27 should make those candidates reviewable in one local
queue and prove that future apply paths can be simulated safely before any
state changes happen.

This matters for paid companion features because durable memory and adaptive
persona behavior will only be credible if users can inspect, approve, reject,
freeze, and preview consequences.

## M26 Invariants To Preserve

M27 implementation must preserve:

- candidate records are review-first;
- review queue entries do not mutate source stores;
- dry-run apply plans do not write memory or persona versions;
- review-required memory cannot enter non-review retrieval surfaces;
- deletion cascades are plans, not executions;
- supersession and contradiction remain review decisions before lifecycle
  changes;
- persona growth cannot auto-apply and cannot patch frozen fields;
- synthetic distillation remains de-identified, text-only, review-required,
  and not runtime-ready;
- no raw private transcript, provider credential, platform recipient, send
  queue, schedule, webhook, token, voice/avatar, audio/image/video payload, or
  generated media path appears in queue or dry-run records.

## Implementation Sequence

### T377 Review Queue Candidate Models

Implement local Pydantic records and deterministic helpers for:

- `ReviewQueueItem`;
- `ReviewQueueSnapshot`;
- `ReviewQueueDecisionRecord`;
- `ReviewQueueService`.

Tests should prove that M26 candidate records can be wrapped into a stable
review queue with priority, reason labels, source refs, due-state hints, and
safe display summaries, while forbidden fields and runtime methods remain
absent.

### T378 Memory Lifecycle Dry-Run Apply Plans

Implement local dry-run planners for memory governance decisions:

- deletion cascade dry-run plans;
- supersession dry-run plans;
- contradiction-resolution dry-run plans.

Tests should prove the planners only describe proposed lifecycle effects and
affected refs, never mutate `MemoryEventStore`, never delete records, and never
enable retrieval for review-required or withdrawn memories.

### T379 Persona Growth Dry-Run Apply Plans

Implement local dry-run planners for persona growth patch candidates.

Tests should prove planners can preview allowed field changes, blocked fields,
weekly delta usage, and rollback refs without mutating `PersonaCard` or
writing `PersonaVersionStore` versions.

### T380 Distillation Review Readiness Aggregator

Implement a local aggregator that turns synthetic distillation manifests and
style feature candidates into review queue items and readiness summaries.

Tests should prove withdrawn consent, clone risk, retained source text, missing
persona-distillation consent, and blocked features prevent readiness.

### T381 M27 Milestone Review

Review code, tests, contracts, and residual risks before any later milestone
expands into user-facing review UI, real import/de-identification, semantic
retrieval ranking, provider-backed extraction, proactive candidates,
voice/avatar runtime, media generation, platform delivery, or monetization.

## Local Synthetic Fixture Strategy

Fixtures should remain small and visible:

- a memory deletion cascade candidate;
- a memory supersession candidate;
- a memory contradiction candidate;
- a persona-growth patch candidate with one safe field and one blocked field;
- a synthetic distillation manifest with active consent;
- a synthetic distillation manifest with withdrawn consent or clone-risk block;
- review queue snapshots with mixed priorities.

Fixture strings should use `[SYNTHETIC]` markers when they contain user-facing
summaries. Fixtures must not use real private names, raw chat snippets,
private file paths, screenshots, voice samples, photos, generated media,
provider metadata, platform recipient ids, or real source paths.

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

M27 must not implement or claim:

- private chat ingestion;
- raw private transcript reads;
- source readers for `private/chat_history/` or `private/distilled/`;
- model-provider calls;
- LLM extraction;
- embeddings, vector search, semantic ranking, or fine-tuning;
- de-identification quality guarantees;
- real-person recreation or authorized digital twin support;
- final companion reply generation;
- runtime memory or persona mutation;
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

## M27 Exit Criteria

M27 can close when:

- review queue records exist and are test-covered;
- memory lifecycle dry-run apply plans exist and are test-covered;
- persona growth dry-run apply plans exist and are test-covered;
- synthetic distillation review readiness aggregation exists and is
  test-covered;
- forbidden private/provider/outbound/platform/media fields are rejected or
  absent;
- no private data, provider calls, automatic sending, platform delivery,
  voice/avatar runtime, generated media, real-person recreation, launch claim,
  legal claim, clinical claim, or real user evidence has been introduced;
- residual risks are documented before M28.

## Residual Risks

- M27 will still not prove live conversation quality or user trust.
- Dry-run apply plans are not production mutation executors.
- No user-facing UI exists yet; queue records are local data structures only.
- No semantic retrieval quality, de-identification quality, or similarity-risk
  quality evaluation exists.
- Voice/avatar, proactive messaging, platform delivery, commercial packaging,
  and virtual social feed behavior remain locked for later scoped milestones.
