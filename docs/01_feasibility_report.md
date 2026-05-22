# Feasibility Report

## Captain Update 2026-05-22 (T170 Review)

T170 confirms that a compatibility-first `ContactSkill` decomposition path is feasible in the current repository shape.

The feasibility gap has changed again:

- no longer blocked on whether M6 needs a breaking replacement design
- now focused on whether additive brief schemas can be formalized cleanly, with explicit evidence ownership and no runtime behavior change

So the project is ready to commit the T170 slice and advance to T171, while keeping M6 schema work additive, reviewable, and non-breaking.

## Captain Update 2026-05-22 (T164 Review)

T164 confirms that approved-only patch context integration is feasible in the current repository shape.

The feasibility gap has changed again:

- no longer blocked on exposing approved, runtime-ready patch hints through `ChatContext`
- now focused on whether ContactSkill can be decomposed into narrower derived briefs without breaking the current evidence-first, compatibility-first pipeline

So the project is ready to commit the T164 slice and advance to T170, while keeping M6 design work non-breaking and documentation-first.

## Captain Update 2026-05-22 (T163 Review)

T163 confirms that explicit human review over patch proposals is feasible in the current repository shape.

The feasibility gap has changed again:

- no longer blocked on recording manual approve/reject/freeze/archive decisions while preserving evidence and review history
- now focused on whether only approved, runtime-ready patches can be integrated into `ChatContext` as compact guidance without leaking proposal internals or skipping existing approval boundaries

So the project is ready to commit the T163 slice and advance to T164, but still only within approved-only, compact-context, non-mutating M5 constraints.

## Captain Update 2026-05-18 (T162 Review)

T162 confirms that deterministic, candidate-only patch proposal generation is feasible in the current repository shape.

The feasibility gap has changed again:

- no longer blocked on converting deterministic feedback clusters into conservative `PreferencePatchCandidate` proposals
- now focused on whether human review decisions can be recorded safely without auto-approval, runtime injection, or evidence drift

So the project is ready to commit the T162 slice and advance to T163, but still only within manual-review, non-mutating M5 constraints.

## Captain Update 2026-05-18 (T161 Review)

T161 confirms that deterministic, privacy-safe feedback clustering is feasible in the current repository shape.

The feasibility gap has changed again:

- no longer blocked on turning validated feedback into stable aggregate clusters
- now focused on whether those clusters can be converted into conservative `PreferencePatchCandidate` records without leaking raw text, over-interpreting ambiguous labels, or bypassing review

So the project is ready to commit the T161 slice and advance to T162, but still only within deterministic, candidate-only, review-first M5 constraints.

## Captain Update 2026-05-18 (T160 Review)

T160 confirms that M5 can stay within the current safety envelope while introducing patch-shaped artifacts.

The feasibility gap has changed again:

- no longer blocked on defining a review-only patch contract
- now focused on whether repeated feedback can be clustered deterministically and privately before any patch proposal is generated

So the project is ready to commit the T160 slice and advance to T161, but still only within review-only, candidate-only M5 constraints.

## Captain Update 2026-05-18 (M4.5 Review)

M4.5 confirms that clean-environment reproducibility is now feasible in the current repository shape for the entire reviewed M3/M4 surface.

The feasibility gap has changed:

- no longer blocked on proving planner/policy/feedback behavior from committed contents
- now focused on whether M5 can stay candidate-only and review-first while introducing patch-shaped artifacts

So the project is now ready to commit T152 and advance to T160, but only within schema-only, non-mutating M5 constraints.

## Captain Update 2026-05-18 (T151 Review)

T151 confirms that committed deterministic policy-engine regression testing is feasible in the current repository shape. The repo can now prove both the ReplyPlanner surface and the direct policy layer from committed synthetic fixtures alone.

The remaining feasibility gap is now narrower:

- T152 must prove that the T140-T142 feedback CLI flow is equally reproducible from committed contents
- until that happens, M5 remains premature even though T151 itself is accepted

So the project is ready to commit T151 and advance the worker to T152, but not yet ready to claim full M4.5 completion.

## Captain Update 2026-05-18

T150 confirms that committed deterministic ReplyPlanner regression testing is feasible in the current repository shape. The repo can now prove a meaningful subset of M3 behavior from committed contents alone, without private fixtures or manual-only verification.

The remaining feasibility gap is narrower and more specific:

- T151 must make policy-layer fixture coverage and direct policy expectations more explicit
- T152 must do the same for the feedback CLI capture/validate/summary loop

So the project is still not ready for M5, but it is ready to commit T150 and advance the next worker to T151.

## Captain Update 2026-05-17

T142 confirms that privacy-safe aggregate feedback summary export is feasible in the current architecture. The project can now record, validate, and summarize feedback without mutating ContactSkill, MemoryFact, approved stores, or outbound behavior.

The remaining feasibility gap is reproducibility, not feature reach. M4 is therefore judged `Conditional`: a clean environment still cannot prove the M3/M4 behavior from committed repo contents alone, because committed regression tests and committed synthetic fixtures are still missing. T150-T152 remain the required bridge before M5.

## Captain Update 2026-05-17

T140 confirms that private human feedback capture is feasible in the current architecture: a `ReplyPlan` can be loaded, a chosen candidate can be referenced safely, and accept/edit/reject/boundary feedback can be written without touching memory, ContactSkill, sending, or platform adapters.

The remaining feasibility gap inside M4 is log trustworthiness rather than feature reach. Before any summary or patch-proposal work, T141 must prove that feedback logs can be validated read-only, that broken references fail safely, and that corrupted or non-private path behavior is surfaced instead of silently passing through.

## Captain Update 2026-05-16

Gate M3 is `Conditional` after T133 review. The M3 structure is feasible: `ReplyPlan`, `ReplyPlanner`, policy/boundary checks, and anonymized holdout evaluation all exist and run in the current environment.

The remaining feasibility gap is reproducibility and quality maturity. A clean environment run is not fully proven because committed regression fixtures/tests are still missing, and T133 rates naturalness/evidence usage at 3/5. Proceeding to T140 is feasible only because T140 records human feedback privately and does not apply it automatically.

T150 remains mandatory for committed regression tests before any stronger quality or maturity claim.

## Captain Update 2026-05-16: Roadmap Feasibility

The updated GPT roadmap is feasible if treated as a staged backlog rather than immediate implementation.

Feasible now:

- T140 feedback capture.
- T141 feedback validation.
- T142 safe feedback summary.
- T150-T152 committed regression tests and fixtures.

Feasible later, after tests:

- PreferencePatch candidates and review flow.
- Compatible ContactSkill decomposition.
- Optional LLM-assisted ReplyPlanner.

Not feasible/safe now:

- Direct Mem0/Zep integration.
- Feishu or WeChat adapter work.
- BehaviorPlanner/proactive behavior.
- Automatic memory or ContactSkill mutation from feedback.

更新日期：2026-05-15

## 1. 问题定义

目标是基于 WeFlow 已导出的私密聊天记录，构建长期关系感知 chat agent 的离线蒸馏与运行时基础。

核心挑战：

- 原始 JSONL 字段和消息类型是否可稳定解析。
- 如何避免把一次性聊天误判为长期关系规律。
- 如何让每条记忆和 ContactSkill 结论都有证据链。
- 如何保护 `private/chat_history` 中的敏感内容。
- 如何在回复生成时利用关系记忆而不冒充联系人。

## 2. 技术路线对比

| 方案 | 优点 | 问题 | 当前判断 |
| --- | --- | --- | --- |
| 继续 iLink/扫码/实时接入 | 可实时收发 | T01 BLOCK，平台风险高，用户已不需要 | 暂停 |
| 微信桌面扫描/OCR | 已有部分代码 | 读取记录稳定性差，用户已有 WeFlow 导出 | 暂停 |
| 微调/LoRA | 可学语气 | 难审计、难删除、易泄露隐私 | 不做 |
| RAG 直接检索原文 | 证据强 | 容易把大量原文塞入上下文，缺关系抽象 | 后续作为组件 |
| Memory + ContactSkill | 可解释、可审计、可回滚 | 需要设计抽取和 review 流程 | 当前主线 |
| 离线蒸馏 MVP | 风险低、最快验证核心假设 | 初期不是实时 agent | 当前第一阶段 |

## 3. 可差异化点

- 本地优先处理 WeFlow 导出，不依赖社交平台实时接口。
- 用 evidence refs 约束所有事实和关系判断。
- ContactSkill 用于辅助用户沟通，不用于复刻或冒充联系人。
- 先做审阅版 JSON/Markdown，再接数据库和运行时。
- 用户反馈进入记忆生命周期，而不是训练模型权重。

## 4. MVP 实验

输入：

- `private/chat_history/` 中的 WeFlow JSONL。

输出：

- `docs/data_contracts/weflow_schema_profile.md`
- `docs/data_contracts/normalized_event_contract.md`
- `private/distilled/<run_id>/normalized_events.jsonl`
- `private/distilled/<run_id>/chunks.jsonl`
- `private/distilled/<run_id>/memory_facts.jsonl`
- `private/distilled/<run_id>/contact_skill.candidate.json`
- `private/distilled/<run_id>/contact_skill.review.md`

## 5. 风险

- 原始导出格式不稳定或字段含义不明。
- sender_role/direction 判断错误导致事实归因错位。
- LLM 对关系状态过度推断。
- 私密内容泄露到 docs/examples/tests。
- 初期过早引入向量库、UI 或复杂 agent 框架，拖慢验证。

## 6. Go / No-Go 判断

当前判断：`Go with offline-first constraints`。

约束：

- T100 已通过 review `PASS`，确认 WeFlow schema profile、normalized event contract 和脱敏 fixture 可以作为 M0 后续输入。
- T101 已通过 review `PASS`，确认隐私脱敏规则、source_ref/raw_ref 规则和红线样例可以约束 T102。
- T102 已通过 review `PASS`，确认最小 normalize CLI 可运行，输出限定在 `private/distilled/`，且未做 chunking、LLM、ContactSkill 或数据库接入。
- T103 milestone review 已接受 Gate M0 = `Conditional`，允许进入 M1，但 T110/T150/T112+/T114 必须承接 M0 条件。
- T110 已通过 reviewer `PASS`，conversation chunker v0 可生成 `chunks.jsonl` 并保留 T102 的不确定性信号。
- T111 已通过 reviewer `PASS`，ChunkSummary、MemoryFactCandidate、ContactSkillCandidate schema 和 JSON contract 已可作为 T112 校验边界。
- T112 已通过 reviewer `PASS`，小样本可生成 `chunk_summaries.jsonl` 和 `memory_facts.jsonl`，并在写入前执行 schema/evidence refs 校验。
- T113 已通过 reviewer `PASS_WITH_WARNINGS`，可生成 candidate 状态的 `contact_skill.candidate.json` 和人工审阅用 `contact_skill.review.md`。
- T114 已确认 Gate M1 = `Conditional`，M1 artifact chain 能在一个真实小样本上端到端运行，但启发式泛化、confidence 数字和 paraphrase compression 风险必须带入 M2。
- T120 已通过 reviewer `PASS_WITH_WARNINGS`，离线 memory/skill 文件 store、review metadata、source metadata 和 human-review-first gate 已落地；未接数据库、未引入向量库、未做 runtime prompt 注入。
- T121 已通过 reviewer `PASS_WITH_WARNINGS`，evidence validator、missing-ref approval block、candidate/rejected/frozen/archived 状态规则和 validator report 已落地；未自动 approve、未做 runtime integration。
- T122 已通过 reviewer `PASS_WITH_WARNINGS`，人工 review/approve/reject/freeze/archive/export CLI 已落地，approve 必须受 T121 validation report 约束；仍未做 runtime integration、数据库或自动发送。
- 当前唯一任务切换为 T123，将 approved + runtime-ready memory/skill 以 compact brief 接入 `ChatContext`，不得注入 candidate/rejected/frozen/archived 或大段原文。
- M1 只选 1 个联系人或小样本做 distillation MVP。
- M1 不微调、不自动发送、不接实时平台。
- 所有可提交 fixture 必须脱敏。

补充判断：T130 已完成并通过 `PASS_WITH_WARNINGS`，ReplyPlan schema 与 prompt contract 已经可行；后续风险主要转移到 T131 的组装质量与候选差异化，而不是结构本身。

补充判断：T131 已完成并通过 `PASS_WITH_WARNINGS`，证明从 T123 compact approved-store context 到 T130 `ReplyPlan` 的 review-only wiring 可行；但 clean-env/committed fixture 尚未覆盖，且候选文本仍偏硬编码。当前可进入 T132 policy/boundary validation，但不能进入 M4。

补充判断：T132 已完成并通过 `PASS_WITH_WARNINGS`，证明 ReplyPlanner 可以在不扩大 scope 的情况下加入 policy/boundary 风险层；但匹配逻辑仍是关键词/substring heuristic，且缺少 committed tests。当前可进入 T133 匿名 holdout eval，但仍不能进入 M4。
