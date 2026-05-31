# M30 Review Workspace Hardening Scope

Task: T393 M30 Scope And First Hardening Task
Status: worker draft for review

## Objective

M30 hardens the M29 review workspace UI before any later milestone introduces
real imported data, real review decisions, manual apply preview flows, or
state mutation.

M29 closed with `PASS_WITH_WARNINGS`. M30 addresses those warnings in order:

- browser visual QA was unavailable;
- internal presentation models still carry review queue identifiers;
- static review card rendering used string-built markup.

M30 remains local, synthetic, non-applying, provider-free, and platform-free.

## Why This Milestone Is Next

The review workspace is becoming the control surface for memory/persona change
review. Before it consumes anything beyond synthetic demo payloads, it needs a
stronger rendering and projection boundary. This avoids carrying private text,
internal identifiers, or unsafe markup into a future user-facing review panel.

## Implementation Sequence

### T393 Review Workspace Safe DOM Renderer

Replace review workspace card string rendering with DOM nodes and
`textContent`, while preserving the existing static shell, fallback fixture,
server payload consumption, and accessibility tests.

### T394 Review Workspace Projection Boundary Tests

Add focused tests around the T391 server-safe projection to prove internal
review queue identifiers and executor/write fields cannot appear in the served
demo payload, even though they exist in internal presentation records.

### T395 Local Visual QA Fallback

Create a reproducible local visual QA fallback that does not depend on the
blocked in-app browser path. This can be a static DOM snapshot check, a local
HTML capture artifact, or another deterministic local verification method that
does not require network, providers, package installs, or live platform access.

### T396 Manual Apply Preview Scope

Only after T393-T395, design a separate manual-apply preview milestone. That
scope should define review-only previews and explicit non-actions before any
real state mutation executor exists.

## Required Invariants

- No private chat ingestion or private artifact reads.
- No model-provider calls.
- No automatic sending, scheduling, notification, platform delivery, webhook,
  queue persistence, token, or recipient mapping.
- No voice/avatar runtime, microphone/camera capture, generated audio,
  generated image, or generated video.
- No review decision apply path, memory store write, PersonaCard mutation,
  PersonaVersionStore write, or deletion executor.
- Static UI must treat review payload fields as text, not trusted markup.
- Server payloads must stay synthetic and omit internal-only identifiers.

## Exit Criteria

M30 can close when:

- review workspace cards render payload fields via DOM/text nodes;
- server-safe projection boundary is tested against internal identifier leaks;
- local visual QA has a reproducible fallback or a documented environment
  blocker;
- manual-apply preview has a separate scoped plan;
- all residual risks are documented before any apply/mutation milestone.

## Residual Risks

- M30 still will not prove real user trust or real-data review quality.
- M30 still will not implement real memory/persona mutation.
- Browser-based screenshot QA may remain unavailable in this environment.
- Real import/de-identification quality, semantic retrieval quality, and
  similarity-risk evaluation remain separate future work.
