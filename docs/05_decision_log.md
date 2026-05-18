# Decision Log

## D030: T151 PASS_WITH_WARNINGS, accept task, advance to T152

- Date: 2026-05-18
- Status: Accepted
- Context: `docs/review/T151_review.md` gives `PASS_WITH_WARNINGS` for the committed policy fixture suite. No blocking issues were found.
- Decision: T151 is complete. The project may continue to T152 Feedback CLI Regression Tests.
- Warning handling:
  - Accepted:
    - N01 the final conservative fallback branch in `_candidate_is_over_proactive` is not independently covered, but the branch is behaviorally redundant with already-tested proactive detection logic.
    - N02 confidence-penalty coverage is not exhaustive across every additive combination, but the component penalties and a representative combined case are already deterministic and sufficient for this task scope.
    - N03 the baseline fixture contamination found by T151 is a positive correction, not a remaining defect; direct policy-engine tests successfully exposed and fixed the issue.
  - Deferred: none.
  - Rejected: none.
- Conditions carried forward:
  - T152 remains required before M5 because the feedback CLI loop is still not regression-hardened from committed repo contents alone.
  - T152 should emphasize privacy-safe stdout, corrupted-log surfacing, compact validation behavior, non-mutation guarantees, and aggregate summary behavior.
- Impact: `docs/04_task_board.md` moves the Current Unique Task from T151 to T152.

## D029: T150 PASS_WITH_WARNINGS, accept task, advance to T151

- Date: 2026-05-18
- Status: Accepted
- Context: `docs/review/T150_review.md` gives `PASS_WITH_WARNINGS` for the committed ReplyPlanner regression test task. No blocking issues were found.
- Decision: T150 is complete. The project may continue to T151 Policy Fixture Suite.
- Warning handling:
  - Accepted:
    - N01 `TestNotConfiguredPath` overlaps with the `thin_context` fixture but still asserts a distinct invariant.
    - N02 policy-layer behavior is still exercised indirectly through `ReplyPlanner`; direct `ReplyPlanPolicyEngine` unit coverage is better treated as T151 scope.
    - N03 `practical` summary wording assertion is intentionally fragile as a regression guard.
    - N04 false-negative probes intentionally assert current missed-detection behavior as a documented limitation.
    - N05 helper constructors are simple enough that missing isolated unit tests is low risk.
    - N06 `notes_on_candidate_differences` is not yet asserted, but this is informational rather than safety-critical.
  - Deferred: none.
  - Rejected: none.
- Conditions carried forward:
  - T151 should add more explicit policy-fixture coverage, including direct `ReplyPlanPolicyEngine` expectations where helpful.
  - T151 should consider separating missing-store-path coverage more clearly from thin-context coverage.
  - T151 should consider adding assertions for `notes_on_candidate_differences`.
  - T152 remains required before M5 because the feedback CLI loop is not yet regression-hardened.
- Impact: `docs/04_task_board.md` moves the Current Unique Task from T150 to T151.

## D028: Gate M4 Conditional, enter T150 instead of M5

- Date: 2026-05-17
- Status: Accepted
- Context: `docs/review/M4_review.md` judges M4 feedback capture as functionally complete but not yet clean-environment reproducible.
- Decision: Gate M4 is `Conditional`. The project may proceed only to M4.5 regression hardening, beginning with T150 ReplyPlanner Regression Tests.
- Reasoning:
  - T140/T141/T142 provide the intended M4 read-only flow: record, validate, and summarize feedback.
  - No blocking pseudo-completion was found.
  - Clean-environment proof is still missing because committed tests and committed synthetic fixtures do not yet cover M3/M4 behavior.
  - M5 feedback-to-patch remains unauthorized until T150-T152 reduce this reproducibility gap.
- Impact: `docs/04_task_board.md` moves the Current Unique Task from T142 to T150.

## D027: T142 PASS_WITH_WARNINGS, accept task, complete M4 functional scope

- Date: 2026-05-17
- Status: Accepted
- Context: `docs/review/T142_review.md` gives `PASS_WITH_WARNINGS` for the feedback summary exporter task. No blocking issues were found.
- Decision: T142 is complete. M4 functional scope is now present: feedback can be recorded, validated, and summarized in a review-only, privacy-safe flow.
- Warning handling:
  - Accepted:
    - N01 duplicated `_resolve_plan_path` / `_load_plan_safe` helpers. Low-risk refactor debt only.
    - N02 raw `input_path` appears in stdout. Style inconsistency only.
    - N03 aggregate presence counts may reveal low-risk existence patterns. Acceptable for the current offline single-user tool.
    - N04 unreadable input can still produce an output artifact describing the failure. Acceptable current behavior.
    - N05 summary returns an untyped `dict`. Consistent with current M4 style.
    - N06 no `reason_tag` / `policy_risk_flag` aggregation because those fields do not exist in the current record schema.
  - Deferred: none.
  - Rejected: none.
- Conditions carried forward:
  - M4 remains review-only and non-mutating.
  - M4 is complete for scope, not yet sufficient for M5.
  - T150-T152 remain responsible for committed reproducibility coverage.
- Impact: T142 closes the implementation side of M4 and hands off to Captain milestone review.

## D025: T140 PASS_WITH_WARNINGS, accept task, advance to T141

- Date: 2026-05-17
- Status: Accepted
- Context: `docs/review/T140_review.md` gives `PASS_WITH_WARNINGS` for the feedback schema + CLI task. No blocking issues were found.
- Decision: T140 is complete. The project may continue to T141 Feedback Log Validator.
- Warning handling:
  - Accepted:
    - N03 `_count_records` re-reads the whole log after append. Low-impact inefficiency only.
    - N04 `reply_plan_id` currently proxies `approved_contact_skill_record_id`. Acceptable because `ReplyPlan` has no dedicated stable `plan_id` yet.
    - N06 `ReplyFeedbackAction` uses `Literal[...]` rather than an enum. Consistent with current project patterns.
  - Deferred:
    - N01 corrupted log file can be silently replaced, causing possible data loss. Carry into T141/R042.
    - N02 `source_plan_path` may be absolute or relative and can become stale after moves. Carry into T141-or-later/R043.
    - N05 CLI/service do not enforce private path confinement on `--output`. Carry into T141/T152/R043.
  - Rejected: none.
- Conditions carried forward:
  - M4 stays capture/validate/summary only.
  - T141 must remain read-only and must not mutate feedback logs, ContactSkill, MemoryFact, approved stores, planner templates, or outbound behavior.
  - T150/T152 remain responsible for committed regression coverage.
- Impact: `docs/04_task_board.md` moves the Current Unique Task from T140 to T141.

## D026: T141 PASS_WITH_WARNINGS, accept task, advance to T142

- Date: 2026-05-17
- Status: Accepted
- Context: `docs/review/T141_review.md` gives `PASS_WITH_WARNINGS` for the feedback log validator task. No blocking issues were found.
- Decision: T141 is complete. The project may continue to T142 Feedback Summary Exporter.
- Warning handling:
  - Accepted:
    - N01 raw `input_path` appears in CLI output. Low-risk style inconsistency only.
    - N03 `_is_private_path` uses a coarse directory-name heuristic. Acceptable for MVP.
    - N04 `_resolve_plan_path` depends on CWD for relative paths. Acceptable with the current private/offline workflow.
    - N05 `strict_mode` is stored in the report but not read by the service. Minor dead data only.
  - Deferred:
    - N02 `reply_plan_id` coherence is not cross-checked against the loaded plan context. Carry into T142 if the summary needs to surface it.
    - N06 `record_results` may grow large on bigger logs. Carry into T142 as a compact-output concern.
  - Rejected: none.
- Conditions carried forward:
  - M4 stays capture/validation/summary only.
  - T142 must remain aggregate-only and privacy-safe.
  - T150/T152 remain responsible for committed regression coverage.
- Impact: `docs/04_task_board.md` moves the Current Unique Task from T141 to T142.

## D023: T133 PASS_WITH_WARNINGS, Gate M3 Conditional, enter T140

- Date: 2026-05-16
- Status: Accepted
- Context: `docs/review/T133_review.md` gives `PASS_WITH_WARNINGS` for the T133 holdout eval. `docs/review/M3_review.md` confirms Gate M3 = `Conditional`.
- Decision: T133 is complete. M3 may proceed to M4/T140 only under review-only constraints.
- Warning handling: T133 N01/N02/N03/N04/N05 are all accepted. No T133 warnings are deferred or rejected.
- Conditions:
  - ReplyPlanner remains review-only. No auto-send, realtime platform integration, or LLM drafting expansion.
  - T150 must add committed regression tests for structure, boundary sensitivity, thin context, false positives, subtle false negatives, privacy leakage, contact alignment, and ranking.
  - Do not claim relationship-aware maturity until broader sample recalibration.
- Impact: Current Unique Task becomes T140 Feedback Schema CLI. T140 records human feedback only; it must not automatically update ContactSkill/Memory or send messages.

## D024: Adopt updated GPT roadmap as staged backlog, revise M4+

- Date: 2026-05-16
- Status: Accepted
- Context: `docs/reference/gpt的后续设计思路(更新版).md` was reviewed against current project state: M3 is `Conditional`, T140 is current, and the project remains offline-first/review-only.
- Decision: Adopt the roadmap's strategic direction but revise milestone/task ordering to preserve the current safety architecture.
- Adopted changes:
  - M4 is narrowed to feedback capture, validation, and safe summary only.
  - M4.5 is added for committed ReplyPlanner/policy/feedback regression tests.
  - Feedback-to-patch moves after regression hardening.
  - ContactSkill decomposition becomes compatible projection, not replacement.
  - LLM-assisted ReplyPlanner, RelationshipState, MemoryRetriever, BehaviorPlanner, Feishu, and WeChat are delayed behind tests and review gates.
- Rejected for immediate execution:
  - Direct Mem0 integration.
  - Direct Feishu/WebSocket/platform integration.
  - Direct ContactSkill deletion/replacement.
  - Automatic learning, automatic sending, or proactive behavior.
- Impact: `docs/04_task_board.md` and task packages under `docs/tasks/` were updated to reflect the staged roadmap. Current Unique Task remains T140.

更新日期：2026-05-15

## D001: 下一阶段以微信主线为优先

- 日期：2026-05-13
- 状态：Superseded
- 背景：上一版计划认为应优先验证 WeChatBot/iLink，再接入微信主流程。
- 原决策：按 `Sprint 0 -> Sprint 7` 推进微信 iLink/扫描/投递路线。
- 被取代原因：T01 登录/session 验证被 BLOCK，且用户已通过 WeFlow 成功导出聊天记录，不再需要扫描或实时接入作为当前主线。

## D002: WeChatBot/iLink SDK 先做仓库外隔离 POC

- 日期：2026-05-13
- 状态：Paused
- 背景：非官方或半官方 SDK 可能有稳定性、账号和接口风险。
- 原决策：Sprint 0 不修改主仓库业务代码，先仓库外验证登录、收消息、reply、媒体和 `context_token`。
- 当前结果：T00 安装和二维码阶段 review `PASS`；T01 登录/session review `BLOCK`。
- 新决策：不修 T01，不继续 iLink 登录验证。相关记录保留为历史，不作为当前开发阻塞项。

## D003: 出站消息默认 human-in-the-loop

- 日期：2026-05-13
- 状态：Accepted
- 背景：聊天 agent 涉及真实社交关系，误发送和越界回复风险高。
- 决策：当前阶段只生成草稿和 review artifact，不自动发送。未来若恢复投递功能，必须经过 `PolicyEngine` 和人工审批。
- 影响：新路线的 ReplyPlanner 只输出候选草稿、rationale 和 risk flags。

## D004: 治理文档采用 AI coding workflow

- 日期：2026-05-13
- 状态：Accepted
- 背景：用户要求像新项目一样建立 00-08 文档，并给出可指导 worker 的 `04_task_board.md`。
- 决策：所有开发以 `Current Unique Task` 和 `docs/tasks/` 任务包为准。
- 影响：路线切换后，旧任务保留为 paused legacy，新任务从 T100 开始。

## D005: T00 review 通过，曾推进到 T01

- 日期：2026-05-13
- 状态：Historical
- 背景：`docs/review/T00_review.md` 给出 `PASS`，确认 SDK 安装、导入、构造和二维码阶段探测真实有效。
- 决策：T00 标记完成。
- 当前影响：仅作为旧 iLink 路线历史证据，不再驱动主线。

## D006: 路线切换到 WeFlow 离线蒸馏 MVP

- 日期：2026-05-13
- 状态：Accepted
- 背景：用户已通过 WeFlow 工具提取聊天记录并存放在 `private/chat_history/`。`docs/review/T01_review.md` 的 BLOCK 主要来自未完成扫码登录，但用户明确希望跳过整个微信聊天记录扫描/SDK路线。
- 决策：暂停 iLink/扫描主线，直接进入基于 WeFlow JSONL 的长期关系感知 chat agent 设计与实验。
- 当前唯一任务：T100 WeFlow JSONL schema profiling 与 normalized event 合约。
- 影响：`02_experiment_plan.md`、`04_task_board.md` 和 00-08 治理文档已按新路线更新。

## D007: 当前阶段不做微调、实时接入、自动发送

- 日期：2026-05-13
- 状态：Accepted
- 背景：两份新设计文档都强调 Memory + ContactSkill + RAG/Skill 的解耦架构，而不是把隐私事实写进模型权重。
- 决策：M0-M1 只做离线解析、切块、摘要、事实抽取、ContactSkill candidate 和人工 review。
- 影响：不引入 LoRA/DPO/微调，不恢复微信 SDK，不建立自动投递功能。

## D008: T100 review PASS，进入 T101 隐私与 source_ref 规则

- 日期：2026-05-14
- 状态：Accepted
- 背景：`docs/review/T100_review.md` 给出 `PASS`，确认 T100 已完成 WeFlow schema profile、normalized event contract 和安全脱敏 fixture，且未越界实现 chunker、LLM、数据库或实时微信接入。
- 决策：T100 标记完成；当前唯一任务切换为 T101。
- Warning 处理：N01 accepted，Q100/Q104 关闭依据更新为 “T100 worker draft + review PASS”；N02 deferred 到 T102/T150 处理 type=80/chatRecords fixture 覆盖；N03 deferred 到 T102 决定 `event_id` 是否从 SHA-1 升级或补充 SHA-256。
- 影响：下一步先固定隐私脱敏规则和 source_ref/raw_ref 规则，再允许实现最小 normalize CLI。

## D009: T101 review PASS，进入 T102 最小 normalize CLI

- 日期：2026-05-14
- 状态：Accepted
- 背景：`docs/review/T101_review.md` 给出 `PASS`，确认隐私脱敏规则、source_ref/raw_ref 规则和补充 source_ref 预览形态的合成 fixture 均满足任务要求，且未修改 `src/**`、未复制真实原文、未实现脱敏器或 LLM 流程。
- 决策：T101 标记完成；当前唯一任务切换为 T102。
- Warning 处理：N01 deferred，继续由 T102/T150 补充 `type=80` 和 `chatRecords` 合成 fixture；N02 accepted，preview hex 值作为 fixture 注释可接受，不要求返修；N03 deferred，T102 实现时校验结构化替换 token 与实际脱敏需求是否对齐。
- 影响：T102 worker 必须遵守 `privacy_redaction_rules.md` 的 Field Handling Matrix 和 `source_ref_rules.md` 的 Allowed Public Shape，且所有 normalize 输出只能落入 `private/distilled/`。

## D010: T102 review PASS，进入 T103 M0 review

- 日期：2026-05-14
- 状态：Accepted
- 背景：`docs/review/T102_review.md` 给出 `PASS`，确认 `chatlog-normalize` CLI 可运行，输入限制在 `private/chat_history/`，输出限制在 `private/distilled/`，stdout/report 不泄露真实原文、真实文件名、真实联系人或真实平台 ID。
- 决策：T102 标记完成；当前唯一任务切换为 T103 M0 review。
- Warning 处理：N01 deferred 到 T103/T150 评估 timezone fallback warning；N02/N03 deferred 到 T110/T150 考虑流式处理与内存写入；N04 accepted，系统消息关键词作为 MVP 兜底可接受；N05 deferred 到 T112+ 蒸馏阶段处理 PII token 替换；N06 deferred 到 T114/T150 验证单文件 sender_role 稳健性。
- 影响：下一步不直接进入 M1 worker 实现，而是先做 T103 gate review，决定 M0 是否 `Allow`、`Conditional` 或 `Block`。

## D011: T103 Gate M0 Conditional，进入 T110

- 日期：2026-05-14
- 状态：Accepted
- 背景：`docs/review/T103_milestone_review.md` 已汇总 T100-T102 的产物与 review 结论；`docs/review/T103_review.md` 接受 worker 草案，确认 Gate M0 = `Conditional`。T100/T101/T102 均已 reviewer `PASS`，M0 硬性条件已满足，但仍有若干明确记录的非阻塞问题需要带入 M1。
- 决策：Gate M0 = `Conditional`；允许进入 M1，当前唯一任务切换为 T110 conversation chunker v0。
- 条件：
  - T110/T150 继续覆盖 `type=80` / `chatRecords` 的保守处理与测试。
  - T110/T114/T150 保留并验证 `sender_role`、timezone fallback、性能/内存相关不确定性。
  - T112+ 任意 LLM-facing 蒸馏步骤继续遵守 T101 的隐私边界，不把私有 normalize 文本直接扩散到可提交产物。
- 影响：T110 worker 可以启动，但必须承接 M0 条件，尤其是保留不确定性信号、避免私密内容进入可提交目录，并为 T112+/T114/T150 留出验证路径。

## D012: T110 review PASS，进入 T111 蒸馏 schema

- 日期：2026-05-14
- 状态：Accepted
- 背景：`docs/review/T110_review.md` 给出 `PASS`，确认 `ConversationChunkingService` 和 `chatlog-chunk` CLI 已完成 conversation chunker v0，输出限制在 `private/distilled/`，未引入 LLM、embedding、ContactSkill、数据库或实时平台接入。
- 决策：T110 标记完成；当前唯一任务切换为 T111 Distillation Schemas。
- Reviewer non-blocking issues 处理：因 verdict 为 `PASS`，不要求 worker 返修；N01/N02/N03 作为 accepted observations 进入后续实现注意事项；N04 deferred 到 T150 自动化测试；N05 accepted，`topic_hint` 保持 optional，不阻塞 T111。
- 影响：T111 必须在 T112 引入 LLM-facing 抽取前定义 ChunkSummary、MemoryFactCandidate、ContactSkillCandidate 的强 schema、JSON contract、evidence_refs 和反 impersonation/数字克隆边界。

## D013: T111 review PASS，进入 T112 摘要与事实抽取

- 日期：2026-05-14
- 状态：Accepted
- 背景：`docs/review/T111_review.md` 给出 `PASS`，确认 `ChunkSummary`、`MemoryFactCandidate`、`ContactSkillCandidate` 及辅助 schema 已在 `core.models` 中定义，`docs/data_contracts/distillation_output_contract.md` 已固定 JSON contract、状态/敏感度约定和 anti-impersonation 边界。
- 决策：T111 标记完成；当前唯一任务切换为 T112 Summary And Fact Extraction。
- Reviewer non-blocking issues 处理：N01 accepted，关系/沟通风格字段保留自由字符串以适配 MVP LLM 输出；N02 accepted/deferred，`redaction_policy` 字典形态当前可接受，后续可在 T120/T150 收紧；N03 deferred 到 T120 处理 `DistillationMemoryType` 与现有 `MemoryType` 映射；N04 deferred 到 T120 store 补充 `created_at` / `updated_at`；N05 deferred 到 T150 增加 Pydantic 约束测试。
- 影响：T112 可以启动，但必须把 LLM 输出校验为 T111 schema，缺失 `evidence_refs`、`confidence`、`sensitivity` 或 `status` 的输出一律视为无效；不得把私密原文或 LLM 原始输入输出写入可提交目录。

## D014: T112 review PASS，进入 T113 ContactSkill builder

- 日期：2026-05-14
- 状态：Accepted
- 背景：`docs/review/T112_review.md` 给出 `PASS`，确认 `ChatlogDistillationService` 和 `chatlog-distill` CLI 已能在小样本上消费 T110 chunks/T102 normalized events，调用 OpenAI-compatible LLM，并在写入前完成 provider 输出归一化、T111 schema 校验和 evidence refs 范围校验。
- 决策：T112 标记完成；当前唯一任务切换为 T113 ContactSkill builder 与 Markdown review exporter。
- Reviewer non-blocking issues 处理：N01 deferred 到 T114 关注 evidence refs 粒度；N02 deferred 到 T114/T150 关注 provider shape drift；N03 accepted/deferred，MVP sensitivity 关键词兜底可接受，后续 T150 可补测试；N04 accepted/deferred，memory_type fallback 可接受，T114/T150 观察误分类；N05 accepted，`contact_skill.py` 轻量辅助不越界；N06 deferred 到 T150 自动化测试；N07 accepted/deferred，T112 已在 prompt 层部分实现 PII token 替换，后续隐私测试继续覆盖。
- 影响：T113 可以消费 `chunk_summaries.jsonl` 和 `memory_facts.jsonl` 生成 `contact_skill.candidate.json` 与 `contact_skill.review.md`；仍不得自动 approve、不得保存大段原文、不得生成“模拟联系人说话”的内容。

## D015: T113 review PASS_WITH_WARNINGS，进入 T114 MVP sample run

- 日期：2026-05-14
- 状态：Accepted
- 背景：`docs/review/T113_review.md` 给出 `PASS_WITH_WARNINGS`，确认 `ContactSkillBuilderService` 和 Markdown exporter 已能消费 T112 outputs，生成 `contact_skill.candidate.json` 与 `contact_skill.review.md`，candidate 保持 `status="candidate"`，保留 evidence refs，且没有自动 approve、冒充联系人、数据库 migration、实时平台接入或自动发送。
- 决策：T113 标记完成；当前唯一任务切换为 T114 Run MVP Sample。
- Warning 处理：N01 accepted，重复 `_build_report()` 仅为低影响重复工作；N02 deferred 到 T114/T120+，小样本启发式 token/topic/relationship 推断需要在不同或更大样本上验证；N03 deferred 到 T114/T120+，formulaic confidence/relationship 数值需要人工检查是否显得过度精确；N04 accepted，缺少 `exporters/__init__.py` 不影响当前运行；N05 accepted，未使用 helper 无当前风险。
- 影响：T114 必须抽查至少 5 条 memory facts 的 evidence 支持度，并额外关注 T113 启发式泛化、confidence 数值可信度、topic 提取覆盖率和 review artifact 是否仍适合人工审阅。

## D016: Gate M1 Conditional，进入 M2/T120

- 日期：2026-05-14
- 状态：Accepted
- 背景：`docs/review/T114_review.md` 给出 `PASS_WITH_WARNINGS`，确认 worker 的 Gate M1 verdict = `Conditional`；`docs/review/M1_review.md` 作为 Captain 综合审查，同样确认 M1 可条件进入 M2。
- 决策：T114 标记完成；Gate M1 = `Conditional`；当前唯一任务切换为 T120 File Store Models。
- Warning 处理：T114 N01/N02 accepted，candidate-only fact 的轻微语义上提由 human review 兜底；T114 N03 accepted，样本过小是结构限制并由 `Conditional` verdict 表达；T114 N04 accepted，不要求补查 report 字段。新增 R030 继续跟踪 paraphrase compression。
- 条件：
  - M2 必须保持 candidate-only / human-review-first，不得把 candidate 或 rejected/frozen 内容直接注入 runtime prompt。
  - T120 必须保留 status 与 evidence refs，并不得引入数据库 migration 或向量库。
  - R028/R029/R030 必须继续活跃到更广样本或后续 store/review 机制能缓解为止。
- 影响：允许进入 M2，但不得把 M1 写成无条件成功；T120 是文件 store 与模型稳定化任务，不是 runtime integration。

## D017: T120 review PASS_WITH_WARNINGS，进入 T121

- 日期：2026-05-14
- 状态：Accepted
- 背景：`docs/review/T120_review.md` 给出 `PASS_WITH_WARNINGS`，确认 T120 已完成离线 memory/skill 文件 store、review metadata、source metadata、legacy artifact wrapping 和 human-review-first `is_runtime_ready()` gate；未引入 CLI、数据库 migration、向量库、runtime prompt 注入或自动 approve。
- 决策：T120 标记完成；当前唯一任务切换为 T121 Evidence Validator。
- Warning 处理：N01 accepted，`updated_at` no-op normalization 不影响正确性，T122 更新 review 状态时再明确 timestamp 语义；N02 accepted，两个 service 间 path/helper duplication 对 MVP 可接受，暂不抽基类；N03 accepted，single-record store shape 兼容入口由 Pydantic 校验兜底；N04 accepted，`DistillationMemoryType` 到 runtime `MemoryType` 的粗粒度映射符合 MVP；N05 deferred 到 T150，需补 store model validation、legacy wrapping、load/save round-trip、runtime-ready gate 和 path confinement 自动化测试。
- 影响：T121 必须只做 evidence validator 与 rejected/frozen 状态规则，不做 approve CLI、runtime integration、数据库或向量库；missing refs 必须阻止 approval。

## D018: T121 review PASS_WITH_WARNINGS，进入 T122

- 日期：2026-05-15
- 状态：Accepted
- 背景：`docs/review/T121_review.md` 给出 `PASS_WITH_WARNINGS`，确认 T121 已完成 read-only evidence validator、`chatlog-validate-evidence` CLI、same-run evidence index、nested `evidence_refs` collection、status gate 和 missing-ref approval/runtime blocking；未自动 approve、未做 review/approve CLI、未接数据库、向量库或 runtime prompt。
- 决策：T121 标记完成；当前唯一任务切换为 T122 Skill Review CLI。
- Warning 处理：N01 accepted，当前 schema 没有 stable contact skill artifact id，fallback 到 `contact_id` 不影响正确性；N02 accepted/deferred，JSON/JSONL helper 第三次重复对 MVP 可接受，若 T150 或后续重构统一文件 IO 可一并处理；N03 accepted，递归扫描全 payload 的性能对当前数据量无风险；N04 accepted，validator read-only 不写回 store 是正确设计，T122 决定是否写入 `review_metadata.evidence_validation_status`；N05 deferred 到 T150，需补 evidence index、nested refs、status rules、missing refs blocking、human review gate interaction 和 path confinement 自动化测试。
- 影响：T122 必须把 T121 validation report 作为 approve gate；不得在 missing refs、candidate-only 或未人工审阅情况下绕过 approval/runtime 安全边界。

## D019: T122 review PASS_WITH_WARNINGS，进入 T123

- 日期：2026-05-15
- 状态：Accepted
- 背景：`docs/review/T122_review.md` 给出 `PASS_WITH_WARNINGS`，确认 T122 已完成 `chatlog-review-store` CLI、`ContactSkillStoreReviewService`、approval gate、review metadata history、safe export 和 stable record_id；approve 需要 T121 report passed、目标 record present、0 missing refs、checked refs > 0，且拒绝 rejected/frozen/archived re-approval；未做 runtime integration、数据库、向量库、LLM 或自动发送。
- 决策：T122 标记完成；当前唯一任务切换为 T123 Context Integration。
- Warning 处理：N01 accepted，`del current_status` 是低影响接口/风格问题；N02 accepted，递归更新所有合法 `status` 字段符合当前 schema，未来 schema 若出现不同语义再重审；N03 accepted，`store_runtime_ready` 提前计算只是轻微 style note；N04 accepted/deferred，review service 访问 file store private helpers 对 MVP 可接受，未来可抽公共 file IO/path utility；N05 accepted，mutable `_StoreWorkspace` 当前局部可控；N06 deferred 到 T150，需补 approval gate、reject/freeze/archive flow、review metadata history、recursive status update、export path confinement、stable record_id 和 no-auto-approve 测试。
- 影响：T123 必须只读取 approved + runtime-ready store records，生成 compact `ChatContext` brief；不得注入 candidate/rejected/frozen/archived，不得把大段原文放入 prompt，不得实现 ReplyPlanner 或自动发送。

## D020: T130 review PASS_WITH_WARNINGS，进入 T131

- 日期：2026-05-15
- 状态：Accepted
- 背景：`docs/review/T130_review.md` 给出 `PASS_WITH_WARNINGS`，确认 T130 已完成 ReplyPlan schema 与 prompt contract：支持 3+ candidates、per-candidate rationale / refs / risk flags / boundary reminders，兼容 T123 compact approved-store context，且没有引入 LLM 调用、发送逻辑、数据库、向量库或私密原文泄露。
- 决策：T130 标记完成；当前唯一任务切换为 T131 Relationship-Aware Reply Planner。
- Warning 处理：N01 accepted，单值 `ReplyPlanMode` 当前符合 review-only scope；N02 deferred 到 R034，T131 必须保证候选 `priority_rank` 稳定且不冲突；N03 accepted，`approach_label` 自由字符串对 MVP 可接受；N04 deferred 到 R034，T131 必须校验 `ReplyPlan.contact_id` 与 source context / T123 approved-store context 对齐。
- 影响：T131 可以实现 planner service/CLI，但必须继续保持 review-only、人类确认优先、只消费 approved + runtime-ready compact context，不得自动发送或绕过 T123/T130 的安全边界。

## D021: T131 review PASS_WITH_WARNINGS，进入 T132

- 日期：2026-05-16
- 状态：Accepted
- 背景：`docs/review/T131_review.md` 给出 `PASS_WITH_WARNINGS`，确认 T131 已完成 review-only `ReplyPlanner` service 与 `chat-reply-plan` CLI：只消费 T123 compact approved-store context，输出 T130 `ReplyPlan`，包含 3 个结构可区分候选，并校验 `priority_rank` 唯一性与 `contact_id` 对齐；未引入自动发送、数据库、向量库、实时平台接入或私密原文读取。
- 决策：T131 标记完成；当前唯一任务切换为 T132 Reply Policy。M3 尚未完成，不能进入 M4。
- Warning 处理：N01 accepted/deferred，硬编码模板和浅层 relationship-awareness 进入 R035，由 T132/T133 继续约束和评估；N02 accepted，硬编码 confidence 在 contract-wiring MVP 可接受；N03 accepted/deferred，`strategy_hints` / `relationship_summary` 未参与草稿生成进入 R035；N04 deferred 到 R036，committed tests/fixtures 留给 T150，并由 T133 提供匿名化评估记录；N05 accepted，`_dedupe(values)` 类型注解缺失为低风险风格问题；N06 accepted，当前 enum fallback 足够支撑 MVP。
- 影响：T132 worker 只应补 policy/boundary 风险层，不重写 T131 planner 主流程，不进入 M4/T140，不实现自动发送或平台集成。

## D022: T132 review PASS_WITH_WARNINGS，进入 T133

- 日期：2026-05-16
- 状态：Accepted
- 背景：`docs/review/T132_review.md` 给出 `PASS_WITH_WARNINGS`，确认 T132 已在 `ReplyPlanner` 前后加入 policy/boundary 风险层：覆盖 `boundary_sensitive`、`over_proactive`、`impersonation_risk`、`thin_context`，保留 T131 的 review-only `ReplyPlan` contract、`priority_rank` 校验和 `contact_id` 对齐；未引入自动发送、数据库、向量库、实时平台接入或私密原文输出。
- 决策：T132 标记完成；当前唯一任务切换为 T133 Holdout Eval。M3 尚未完成，不能进入 M4。
- Warning 处理：N01 accepted，runtime text 仅用于 detection 且不 echo；N02 accepted，宽泛关键词已有 compound trigger 缓解；N03 accepted/deferred，substring matching false-positive 风险进入 R037，由 T133/T150 继续观察和测试；N04 accepted，`_dedupe` 重复是低风险重复；N05 deferred，T132 无 committed tests/fixtures 并入 R036；N06 accepted，重复分支无 correctness 影响；N07 accepted，approved memory claim 仅限量用于 detection，不进入输出 surface。
- 影响：T133 只做匿名 holdout eval 和 Gate M3 判断，不修改 planner 代码，不提交 holdout 原文，不进入 M4/T140。
