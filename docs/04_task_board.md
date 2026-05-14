# Task Board

更新日期：2026-05-14

## Board Rules

- 当前主线已切换为 WeFlow 导出记录驱动的离线蒸馏与长期关系感知 chat agent。
- 只有 `Current Unique Task` 可以交给 worker 执行。
- Worker 只改任务包 `Allowed files`。
- `private/` 中的聊天记录和蒸馏产物不得提交。
- 可提交文档、fixture、测试必须脱敏。
- 不继续修 T01，不继续微信扫码/扫描/实时 SDK 接入。
- 不微调、不自动发送、不做数字克隆。

## Paused Legacy Track: WeChat SDK / Scan

- [x] T00: SDK 安装和二维码阶段探测，review `PASS`。
- [ ] T01: 登录/session 验证，review `BLOCK`。用户决定不修，路线暂停。

结论：旧 iLink/扫描路线不再驱动下一阶段开发。

## Milestone 0: WeFlow 数据合约与隐私护栏

目标：确认 WeFlow JSONL 可解析，并建立 normalized event 合约和脱敏样例。

- [x] T100: WeFlow JSONL schema profiling 与 normalized event 合约。review `PASS`。任务包：`docs/tasks/M0_weflow_data_contract/T100_schema_profile.md`
- [x] T101: 设计脱敏规则、source_ref 规则和最小红线测试样例。review `PASS`。任务包：`docs/tasks/M0_weflow_data_contract/T101_privacy_source_refs.md`
- [x] T102: 实现 WeFlow adapter 的最小 normalize CLI。review `PASS`。任务包：`docs/tasks/M0_weflow_data_contract/T102_minimal_normalize_cli.md`
- [x] T103: M0 review，Gate M0 `Conditional`，允许进入 M1。review `PASS_WITH_WARNINGS` / `Conditional accepted`。任务包：`docs/tasks/M0_weflow_data_contract/T103_m0_review.md`

## Milestone 1: 离线蒸馏 MVP

目标：从一个联系人或小样本生成 chunks、memory facts、ContactSkill candidate 和 review artifact。

- [x] T110: 实现 conversation chunker v0。review `PASS`。任务包：`docs/tasks/M1_offline_distillation_mvp/T110_chunker_v0.md`
- [x] T111: 定义 ChunkSummary、MemoryFactCandidate、ContactSkillCandidate schema。review `PASS`。任务包：`docs/tasks/M1_offline_distillation_mvp/T111_distillation_schemas.md`
- [ ] T112: 实现 chunk summary 与 fact extraction 的 LLM/JSON 校验管线。任务包：`docs/tasks/M1_offline_distillation_mvp/T112_summary_fact_extraction.md`
- [ ] T113: 实现 ContactSkill builder 与 Markdown review exporter。任务包：`docs/tasks/M1_offline_distillation_mvp/T113_contact_skill_builder.md`
- [ ] T114: 在一个选定联系人样本上运行 distillation MVP 并人工抽查 evidence。任务包：`docs/tasks/M1_offline_distillation_mvp/T114_run_mvp_sample.md`

## Milestone 2: Memory / Skill Store 与证据校验

目标：把离线产物纳入项目模型、仓储和审阅流。

- [ ] T120: 新增离线 memory/skill Pydantic 模型和文件 store。任务包：`docs/tasks/M2_memory_skill_store/T120_file_store_models.md`
- [ ] T121: 实现 evidence validator 与 rejected/frozen 状态规则。任务包：`docs/tasks/M2_memory_skill_store/T121_evidence_validator.md`
- [ ] T122: 实现 contact-skill review/approve/export CLI。任务包：`docs/tasks/M2_memory_skill_store/T122_skill_review_cli.md`
- [ ] T123: 将 approved memory/skill 接入现有 `ChatContext`。任务包：`docs/tasks/M2_memory_skill_store/T123_context_integration.md`

## Milestone 3: 联系人感知 Reply Planner

目标：基于 approved ContactSkill 和 memory 生成可解释、多候选、安全的回复草稿。

- [ ] T130: 定义 ReplyPlan schema 和 prompt contract。任务包：`docs/tasks/M3_relationship_reply_planner/T130_reply_plan_schema.md`
- [ ] T131: 实现 relationship-aware ReplyPlanner。任务包：`docs/tasks/M3_relationship_reply_planner/T131_reply_planner.md`
- [ ] T132: 增加边界/禁忌/policy 校验，防止冒充和过度主动。任务包：`docs/tasks/M3_relationship_reply_planner/T132_reply_policy.md`
- [ ] T133: 用历史 holdout 场景评估回复自然度和边界遵守。任务包：`docs/tasks/M3_relationship_reply_planner/T133_holdout_eval.md`

## Milestone 4: 反馈闭环与记忆修正

目标：让用户对草稿的 accept/edit/reject/boundary feedback 变成可审阅的 memory/skill 更新提案。

- [ ] T140: 定义 feedback log schema 与 CLI。任务包：`docs/tasks/M4_feedback_loop/T140_feedback_schema_cli.md`
- [ ] T141: 实现 edit diff -> preference/boundary proposal。任务包：`docs/tasks/M4_feedback_loop/T141_feedback_to_proposal.md`
- [ ] T142: 实现 skill/memory version diff、rollback、freeze。任务包：`docs/tasks/M4_feedback_loop/T142_versioning_rollback.md`

## Milestone 5: 评估与工程硬化

目标：建立自动化测试、隐私检查和最终工程收口。

- [ ] T150: 建立脱敏 fixture 测试与 parser/chunker/evidence 单测。任务包：`docs/tasks/M5_eval_hardening/T150_tests.md`
- [ ] T151: 建立 privacy leakage smoke test。任务包：`docs/tasks/M5_eval_hardening/T151_privacy_leakage_tests.md`
- [ ] T152: 完成 distillation MVP milestone review 和最终 handoff。任务包：`docs/tasks/M5_eval_hardening/T152_final_review.md`

## Current Unique Task

T112: 实现 chunk summary 与 fact extraction 的 LLM/JSON 校验管线。

任务包：`docs/tasks/M1_offline_distillation_mvp/T112_summary_fact_extraction.md`

为什么现在做它：T111 已通过 reviewer `PASS`，蒸馏输出 schema 和 JSON contract 已经固定。现在可以在小样本上实现 T112，用 LLM 生成 chunk summaries 和 memory fact candidates，但必须先通过 schema/evidence 校验，拒绝无 `evidence_refs` 的输出，并且不得把私密原文或 LLM 原始输入输出写入可提交目录。

## Next Captain Output Required

下一轮 Captain 分发任务时必须输出：

1. 当前唯一任务。
2. 为什么现在做它。
3. Worker 任务包。
4. 允许修改的文件范围。
5. 禁止做的事。
6. 验证命令或验收标准。
7. 完成后需要更新的治理文件。
