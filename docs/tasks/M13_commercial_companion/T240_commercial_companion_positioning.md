# T240: M13 Commercial Companion Positioning And Safety Boundary Pack

## Task ID

T240

## Goal

Turn the returned GPT-Pro M13+ research into a docs-only product positioning,
safety boundary, architecture, roadmap, and M14 task-package foundation for a
commercial text-first AI persona companion product.

This task must not write implementation code. It should make the product
direction executable for later workers while preserving the current governance
boundaries: review-first, privacy-safe, no deception, no unauthorized clone, no
automatic sending, no live platform integration, and no private-content commits.

## Why Now

M12 closed with `Gate M12 Conditional`. The project now has only a
local/synthetic/dry-run WeCom Customer Service evidence slice and no live
delivery authorization.

The user returned `docs/reference/gpt-pro关于后续从M13开始的计划分析.md`. Captain
accepts its core recommendation: M13 should be research/governance/docs-only
before any Persona Compiler, proactive companion, memory OS, voice/avatar, or
commercial UX implementation work.

## Allowed Files

Worker may create or modify only these paths:

- `docs/product/M13_commercial_companion_positioning.md`
- `docs/product/M13_competitor_matrix.md`
- `docs/safety/M13_clone_and_persona_risk_tiers.md`
- `docs/safety/M13_proactive_companionship_redlines.md`
- `docs/architecture/M13_persona_memory_relationship_architecture.md`
- `docs/roadmap/M13_plus_milestone_plan.md`
- `docs/tasks/M14_persona_compiler_schema/T250_persona_compiler_schema.md`
- `docs/worker_summary/T240_worker_summary.md`
- `docs/07_handoff.md`

The worker may create the parent directories above if they do not exist.

## Forbidden Scope

- Do not modify `src/**`, `tests/**`, package metadata, runtime config, CLI
  commands, connectors, adapters, stores, or schemas.
- Do not modify `docs/04_task_board.md`, `docs/05_decision_log.md`,
  `docs/06_eval_protocol.md`, or `docs/08_risks_and_open_questions.md`; those
  remain Captain-owned after review.
- Do not read, quote, summarize, or commit content from `private/chat_history/`,
  `private/distilled/`, or other private artifacts.
- Do not add live WeChat, WeCom, Feishu, Tencent, app-store, or external
  platform integration.
- Do not call platform APIs, load credentials, register callbacks, poll/sync
  messages, create transports, add schedulers, or send messages.
- Do not create or endorse unauthorized real-person clones, ex-partner clones,
  deceased-person resurrection, public-figure/persona imitation, voice cloning,
  face/avatar deepfakes, or "pretend to be a real person" flows.
- Do not describe future planned capabilities as already implemented.
- Do not present legal/compliance notes as legal advice or production approval.
- Do not use unofficial WeChat SDKs or vendor third-party SDK code.

## Inputs To Read

Required:

- `README.md`
- `AGENTS.md`
- `docs/reference/AI_coding_workflow.md`
- `docs/04_task_board.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`
- `docs/reference/gpt-pro关于后续从M13开始的计划分析.md`
- `docs/review/M12_review.md`
- `docs/worker_summary/T234_worker_summary.md`

Recommended:

- `docs/00_raw_idea.md`
- `docs/01_feasibility_report.md`
- `docs/03_architecture.md`
- `docs/05_decision_log.md`
- `docs/06_eval_protocol.md`
- existing task packages under `docs/tasks/M12_wechat_adapter/`
- official references verified by Captain on 2026-05-31:
  - `https://www.cac.gov.cn/2026-04/10/c_1777558395078289.htm`
  - `https://www.cac.gov.cn/2022-12/11/c_1672221949354811.htm`
  - `https://www.cac.gov.cn/2025-03/14/c_1743654684782215.htm`

If the worker has browsing available, it may verify public facts against
official/legal/primary sources and stable competitor pages. If browsing is not
available, explicitly state that the M13 pack relies on the provided GPT-Pro
report and committed repository context.

## Expected Outputs

### 1. Product Positioning

Create `docs/product/M13_commercial_companion_positioning.md`.

Must include:

- recommended product positioning: transparent, controllable, text-first AI
  persona object, not a real-person replacement
- target users and non-target users
- MVP promise and explicit non-promises
- why the project should not continue with live WeChat/WeCom delivery now
- first commercial validation assumptions
- open questions for user research and pricing/retention validation
- short "do not build yet" list

### 2. Competitor Matrix

Create `docs/product/M13_competitor_matrix.md`.

Must include:

- competitor rows at least for TheOne, Replika, Character.AI, Talkie, MiniMax
  Xingye, AI Love/ailover, and at least two domestic products that need follow
  up such as Glow, 猫箱, 米苏时空, or 轻偶
- columns for positioning, capabilities, business model signal, target users,
  observed risks, and implication for this project
- a separate "commoditized capabilities" section
- a separate "remaining product gaps" section
- clear source-confidence labeling when data comes only from the GPT-Pro report

### 3. Clone And Persona Risk Tiers

Create `docs/safety/M13_clone_and_persona_risk_tiers.md`.

Must define at least these tiers:

- L1: original fictional persona from user description/template/random seed
- L2: de-identified abstract style inspiration that does not preserve a real
  person's name, face, voice, biography, private events, or identifiable speech
  fingerprint
- L3: self-authorized digital self, future-only and consent-heavy
- L4: third-party/deceased/commemorative mode, research-only and not an
  engineering target now
- L5: unauthorized real-person clone, public figure clone, ex-partner/family
  clone, voice/face deepfake, or deceptive impersonation; prohibited

For each tier include allowed status, required consent/evidence, product copy
constraints, storage constraints, and gate status.

### 4. Proactive Companionship Redlines

Create `docs/safety/M13_proactive_companionship_redlines.md`.

Must include:

- consent requirements before any proactive candidate
- frequency caps, quiet hours, no-response backoff, and user-visible controls
- dependency and emotional-manipulation redlines
- crisis/self-harm handling expectations at a product-policy level
- examples of blocked language patterns such as guilt, exclusivity, coercion,
  or paid intimacy escalation
- explicit statement that no external-platform automatic sending is allowed

### 5. Persona / Memory / Relationship Architecture Draft

Create `docs/architecture/M13_persona_memory_relationship_architecture.md`.

Must include:

- seven-engine target architecture:
  `Persona Compiler`, `Memory OS v2`, `Relationship Engine`,
  `Dialogue Engine`, `Proactive Engine`, `Virtual Life Engine`, and
  `Safety & Compliance Engine`
- state separation for factual, inferred, relational, procedural, and imagined
  memory
- data flow from persona creation to chat/retrieval/proactive review, all
  still local/review-first at this stage
- dependency map from M14 through M22
- explicit non-goals: no live platform delivery, no unauthorized clone, no
  deepfake, no raw-private-content commit

### 6. M13+ Roadmap

Create `docs/roadmap/M13_plus_milestone_plan.md`.

Must include:

- M13 through M22 milestone table with goal, scope, non-goals, review gate, and
  candidate task IDs
- M13 gate recommendation:
  - `Gate M13 Allow`: only allows entering M14 Persona Compiler schema/local
    creation work
  - `Gate M13 Conditional`: requires more research or redline tightening
  - `Gate M13 Block`: if the roadmap still attempts platform auto-send,
    unauthorized cloning, or deceptive real-person simulation
- no claim that future milestones are implemented

### 7. M14 First Worker Task Package

Create `docs/tasks/M14_persona_compiler_schema/T250_persona_compiler_schema.md`.

This should be a complete worker task package for the next engineering
milestone if M13 passes review. It should likely focus on `PersonaCard v1`
schema and source/consent policy, not a full compiler yet.

The M14 task package must include:

- task ID, goal, why now, allowed files, forbidden scope, inputs, expected
  outputs, verification, docs to update, and reviewer type
- no runtime behavior, no LLM calls, no private reads, no clone behavior
- tests/schemas only if the future task explicitly allows them

### 8. Worker Summary And Handoff

Create `docs/worker_summary/T240_worker_summary.md` and append/update
`docs/07_handoff.md`.

The summary must state:

- files changed
- research/source basis
- what was intentionally not done
- verification commands and results
- remaining risks
- recommended reviewer type

The handoff update must not mark T240 complete. It should say that T240 awaits
review and Captain judgment.

## Verification

Minimum verification commands:

```powershell
git diff --check
```

```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
Test-Path docs\product\M13_commercial_companion_positioning.md
Test-Path docs\product\M13_competitor_matrix.md
Test-Path docs\safety\M13_clone_and_persona_risk_tiers.md
Test-Path docs\safety\M13_proactive_companionship_redlines.md
Test-Path docs\architecture\M13_persona_memory_relationship_architecture.md
Test-Path docs\roadmap\M13_plus_milestone_plan.md
Test-Path docs\tasks\M14_persona_compiler_schema\T250_persona_compiler_schema.md
Test-Path docs\worker_summary\T240_worker_summary.md
```

```powershell
rg -n "Gate M13|M14|M22|L1|L5|automatic sending|unauthorized clone|imagined memory" docs\product docs\safety docs\architecture docs\roadmap docs\tasks\M14_persona_compiler_schema docs\worker_summary\T240_worker_summary.md
```

If the worker modifies no Python files, no `py_compile` or pytest command is
required. If the worker accidentally touches code/tests, stop and report that
as a scope violation instead of trying to repair it in place.

## Docs To Update After Completion

Worker updates only:

- `docs/07_handoff.md`
- `docs/worker_summary/T240_worker_summary.md`

Captain updates after review:

- `docs/00_raw_idea.md`
- `docs/01_feasibility_report.md`
- `docs/03_architecture.md`
- `docs/04_task_board.md`
- `docs/05_decision_log.md`
- `docs/06_eval_protocol.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

## Reviewer Type

Adversarial review recommended.

Reviewer should verify:

- the docs do not overclaim implementation/compliance/product readiness
- the roadmap preserves one Current Unique Task and review gates
- no real-person clone, automatic sending, or live platform path is authorized
- no private artifacts are read or quoted
- M14's task package is concrete enough for a strong worker but still safely
  scoped
