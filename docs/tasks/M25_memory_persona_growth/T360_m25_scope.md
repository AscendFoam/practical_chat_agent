# T360: M25 Scope

## Task ID

T360

## Goal

Scope M25 as the memory, persona growth, and distillation-planning milestone for
the text-first companion agent.

## Why Now

M24 hardened the local text-first demo and verified its local run path. The next
product risk is not more UI chrome; it is whether the companion can support
advanced memory, bounded persona growth, and eventual chat-record distillation
without losing provenance, consent, safety, or user control.

## Allowed Files

Future T360 worker may create or modify only:

- `docs/product/m25_memory_persona_growth_scope.md`
- `docs/tasks/M25_memory_persona_growth/T361_memory_architecture_design.md`
- `docs/worker_summary/T360_worker_summary.md`
- `docs/07_handoff.md`

If T360 needs code changes, tests, browser reruns, model-provider calls,
generated media, voice/avatar runtime, private data processing, task-board
edits, platform adapters, outbound messaging, screenshot artifacts, or launch
claims, Captain must revise this package before assignment.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not ingest or summarize real private chat records.
- Do not call model providers.
- Do not synthesize audio, generate images/video, clone voices/faces, capture
  microphone/camera input, or process media samples.
- Do not add external network assets or package-manager dependencies.
- Do not add backend routes, persistence, platform delivery, push notification,
  send, schedule, queue, webhook, token, adapter, or realtime fields.
- Do not enable automatic outreach, voice, avatar, Live2D, camera, microphone,
  ASR, TTS, or media runtime.
- Do not implement real-person recreation support.
- Do not modify `docs/04_task_board.md`.
- Do not claim legal advice, compliance completion, app-store approval, launch
  approval, user-study validation, regulator acceptance, or real user evidence.

## Inputs To Read

Required:

- `docs/review/M24_review.md`
- `docs/review/M23_review.md`
- `docs/product/m24_demo_hardening_scope.md`
- `docs/data_contracts/text_first_web_demo_state_contract.md`
- `docs/data_contracts/local_web_demo_server_contract.md`
- `docs/data_contracts/web_demo_display_accessibility_contract.md`

Recommended:

- `docs/reference/和gpt-pro的对话.md`
- `docs/reference/gpt-pro关于后续从M13开始的计划分析.md`
- existing memory, consent, AIGC labeling, crisis/dependency, persona, and
  relationship-context contracts discoverable through `rg`.

## Expected Outputs

### 1. M25 Product Scope

Create `docs/product/m25_memory_persona_growth_scope.md` with:

- objective and non-goals;
- memory architecture principles;
- persona growth principles;
- distillation-readiness principles;
- consent and user-control requirements;
- synthetic-fixture strategy;
- safety boundaries for real-person likeness, grief, ex-partner, family-member,
  public-figure, dependency, and crisis scenarios;
- recommended M25 task sequence.

### 2. Next Task Package

Create
`docs/tasks/M25_memory_persona_growth/T361_memory_architecture_design.md`
for memory architecture design. T361 should remain docs/contract focused and
must not read private chat logs or call model providers.

### 3. Worker Summary And Handoff

Write `docs/worker_summary/T360_worker_summary.md` and append a T360 worker
record to `docs/07_handoff.md`.

Do not mark T360 complete in `docs/04_task_board.md`.

## Verification

Minimum command:

```powershell
git diff --check
```

## Reviewer Type

Adversarial product/safety UX, privacy, memory-architecture, and persona-safety
review recommended.

Reviewer should block if M25 scope allows private chat ingestion, real-person
recreation, provider calls, unbounded persona drift, automatic outreach,
platform delivery, voice/avatar runtime, media generation, or launch/user-study
claims before explicit follow-up tasks define consent, provenance, redaction,
and review gates.

