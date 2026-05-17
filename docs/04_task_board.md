# Task Board

更新日期：2026-05-16

## Captain Current State Override

- T133 review decision: `PASS_WITH_WARNINGS`.
- Gate M3: `Conditional`.
- T133 is complete as a docs/private-artifact milestone eval.
- Current Unique Task: T140 Feedback Schema CLI.
- Current task package: `docs/tasks/M4_feedback_loop/T140_feedback_schema_cli.md`.
- M4/T140 may proceed only under review-only constraints: no auto-send, no realtime platform integration, no automatic ContactSkill/Memory mutation, no LLM drafting expansion, and no relationship-aware maturity claim before broader recalibration.
- T150 must add committed regression tests covering ReplyPlanner structure, boundary sensitivity, thin context, false positives, subtle false negatives, privacy leakage, contact alignment, and candidate ranking.

## Current Unique Task

T140: Feedback Schema CLI.

Task package: `docs/tasks/M4_feedback_loop/T140_feedback_schema_cli.md`

Why now: T133 passed with warnings and Gate M3 is `Conditional`. M4 may start with private, review-only feedback capture, but T140 must not send messages, mutate ContactSkill/Memory automatically, integrate realtime platforms, or claim relationship-aware maturity.

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
- [x] T112: 实现 chunk summary 与 fact extraction 的 LLM/JSON 校验管线。review `PASS`。任务包：`docs/tasks/M1_offline_distillation_mvp/T112_summary_fact_extraction.md`
- [x] T113: 实现 ContactSkill builder 与 Markdown review exporter。review `PASS_WITH_WARNINGS`。任务包：`docs/tasks/M1_offline_distillation_mvp/T113_contact_skill_builder.md`
- [x] T114: 在一个选定联系人样本上运行 distillation MVP 并人工抽查 evidence。Gate M1 `Conditional`。review `PASS_WITH_WARNINGS`。任务包：`docs/tasks/M1_offline_distillation_mvp/T114_run_mvp_sample.md`

## Milestone 2: Memory / Skill Store 与证据校验

目标：把离线产物纳入项目模型、仓储和审阅流。

状态：Gate M1 = `Conditional`，允许进入 M2，但必须保留 candidate-only / human-review-first，且继续跟踪 T113/T114 的启发式泛化、confidence 数值和 paraphrase compression 风险。

- [x] T120: 新增离线 memory/skill Pydantic 模型和文件 store。review `PASS_WITH_WARNINGS`。任务包：`docs/tasks/M2_memory_skill_store/T120_file_store_models.md`
- [x] T121: 实现 evidence validator 与 rejected/frozen 状态规则。review `PASS_WITH_WARNINGS`。任务包：`docs/tasks/M2_memory_skill_store/T121_evidence_validator.md`
- [x] T122: 实现 contact-skill review/approve/export CLI。review `PASS_WITH_WARNINGS`。任务包：`docs/tasks/M2_memory_skill_store/T122_skill_review_cli.md`
- [x] T123: 将 approved memory/skill 接入现有 `ChatContext`。review `PASS_WITH_WARNINGS`。任务包：`docs/tasks/M2_memory_skill_store/T123_context_integration.md`

## Milestone 3: 联系人感知 Reply Planner

目标：基于 approved ContactSkill 和 memory 生成可解释、多候选、安全的回复草稿。

- [x] T130: 定义 ReplyPlan schema 和 prompt contract。review `PASS_WITH_WARNINGS`。任务包：`docs/tasks/M3_relationship_reply_planner/T130_reply_plan_schema.md`
- [x] T131: 实现 relationship-aware ReplyPlanner。review `PASS_WITH_WARNINGS`。任务包：`docs/tasks/M3_relationship_reply_planner/T131_reply_planner.md`
- [x] T132: 增加边界/禁忌/policy 校验，防止冒充和过度主动。review `PASS_WITH_WARNINGS`。任务包：`docs/tasks/M3_relationship_reply_planner/T132_reply_policy.md`
- [x] T133: 用历史 holdout 场景评估回复自然度和边界遵守。review `PASS_WITH_WARNINGS` / Gate M3 `Conditional`。任务包：`docs/tasks/M3_relationship_reply_planner/T133_holdout_eval.md`

## Milestone 4: Feedback Capture

目标：只记录、校验、汇总用户对 ReplyPlan candidates 的 accept/edit/reject/boundary feedback，不应用反馈、不更新记忆、不接平台。

- [ ] T140: 定义 feedback log schema 与 CLI。任务包：`docs/tasks/M4_feedback_loop/T140_feedback_schema_cli.md`
- [ ] T141: 实现 feedback log validator。任务包：`docs/tasks/M4_feedback_loop/T141_feedback_log_validator.md`
- [ ] T142: 实现 feedback summary exporter。任务包：`docs/tasks/M4_feedback_loop/T142_feedback_summary_exporter.md`

## Milestone 4.5: Regression Hardening

目标：把 M3 Conditional 与 M4 feedback capture 变成 clean-env 可复现的 committed tests，先补安全网再进入反馈应用或 LLM drafting。

- [ ] T150: ReplyPlanner regression tests。任务包：`docs/tasks/M4_5_regression_hardening/T150_replyplanner_regression_tests.md`
- [ ] T151: Policy fixture suite。任务包：`docs/tasks/M4_5_regression_hardening/T151_policy_fixture_suite.md`
- [ ] T152: Feedback CLI regression tests。任务包：`docs/tasks/M4_5_regression_hardening/T152_feedback_cli_regression_tests.md`

## Milestone 5: Feedback To Patch

目标：把多条相似 feedback 转成可审阅 PreferencePatch candidates；仍不自动 approve、不自动改 ContactSkill/Memory。

- [ ] T160: PreferencePatch schema。任务包：`docs/tasks/M5_feedback_to_patch/T160_preference_patch_schema.md`
- [ ] T161: feedback clusterer。任务包：`docs/tasks/M5_feedback_to_patch/T161_feedback_clusterer.md`
- [ ] T162: patch proposal CLI。任务包：`docs/tasks/M5_feedback_to_patch/T162_patch_proposal_cli.md`
- [ ] T163: patch review CLI。任务包：`docs/tasks/M5_feedback_to_patch/T163_patch_review_cli.md`
- [ ] T164: approved patch compact context。任务包：`docs/tasks/M5_feedback_to_patch/T164_approved_patch_context.md`

## Milestone 6: ContactSkill Compatible Decomposition

目标：不废除 ContactSkill；在 approved ContactSkill 上兼容式派生 PartnerPersona / CommunicationPolicy / BoundaryProfile briefs。

- [ ] T170: ContactSkill decomposition design。任务包：`docs/tasks/M6_contactskill_decomposition/T170_decomposition_design.md`
- [ ] T171: PartnerPersonaBrief schema。任务包：`docs/tasks/M6_contactskill_decomposition/T171_partner_persona_brief_schema.md`
- [ ] T172: CommunicationPolicyBrief schema。任务包：`docs/tasks/M6_contactskill_decomposition/T172_communication_policy_brief_schema.md`
- [ ] T173: ContactSkill projection service。任务包：`docs/tasks/M6_contactskill_decomposition/T173_projection_service.md`
- [ ] T174: derived briefs context integration。任务包：`docs/tasks/M6_contactskill_decomposition/T174_derived_briefs_context.md`

## Milestone 7: LLM-Assisted ReplyPlanner

目标：在 regression safety net 之后引入可选 LLM candidate generator，仍输出 `ReplyPlan`，默认 review-only。

- [ ] T180: LLM candidate generator contract。任务包：`docs/tasks/M7_llm_reply_planner/T180_llm_candidate_contract.md`
- [ ] T181: LLM candidate offline CLI。任务包：`docs/tasks/M7_llm_reply_planner/T181_llm_candidate_offline_cli.md`
- [ ] T182: candidate validator。任务包：`docs/tasks/M7_llm_reply_planner/T182_candidate_validator.md`
- [ ] T183: hybrid ReplyPlanner。任务包：`docs/tasks/M7_llm_reply_planner/T183_hybrid_reply_planner.md`
- [ ] T184: LLM planner holdout eval。任务包：`docs/tasks/M7_llm_reply_planner/T184_llm_planner_holdout_eval.md`

## Milestone 8: RelationshipState

目标：建立多维关系状态与人工审阅 delta，不使用单一好感度，不自动覆盖长期状态。

- [ ] T190: RelationshipState schema。任务包：`docs/tasks/M8_relationship_state/T190_relationship_state_schema.md`
- [ ] T191: RelationshipSignal extractor。任务包：`docs/tasks/M8_relationship_state/T191_relationship_signal_extractor.md`
- [ ] T192: RelationshipDeltaCandidate。任务包：`docs/tasks/M8_relationship_state/T192_relationship_delta_candidate.md`
- [ ] T193: relationship review CLI。任务包：`docs/tasks/M8_relationship_state/T193_relationship_review_cli.md`
- [ ] T194: RelationshipState compact context。任务包：`docs/tasks/M8_relationship_state/T194_relationship_state_context.md`
- [ ] T195: relationship-aware reply eval。任务包：`docs/tasks/M8_relationship_state/T195_relationship_aware_eval.md`

## Milestone 9: Memory Retrieval Layer

目标：先定义 `MemoryRetriever` 抽象和 local approved-store retriever，再评估 Mem0 等外部 memory adapter。

- [ ] T200: MemoryRetriever interface。任务包：`docs/tasks/M9_memory_retrieval_layer/T200_memory_retriever_interface.md`
- [ ] T201: local approved-store retriever。任务包：`docs/tasks/M9_memory_retrieval_layer/T201_local_approved_store_retriever.md`
- [ ] T202: retrieval eval set。任务包：`docs/tasks/M9_memory_retrieval_layer/T202_retrieval_eval_set.md`
- [ ] T203: optional Mem0 adapter spike。任务包：`docs/tasks/M9_memory_retrieval_layer/T203_optional_mem0_adapter_spike.md`

## Milestone 10: BehaviorPlanner

目标：生成主动行为草稿 CandidateAction，不自动发送，不做全天候自我模拟。

- [ ] T210: behavior schema。任务包：`docs/tasks/M10_behavior_planner/T210_behavior_schema.md`
- [ ] T211: action planner rule engine。任务包：`docs/tasks/M10_behavior_planner/T211_action_planner_rule_engine.md`
- [ ] T212: proactive draft generator。任务包：`docs/tasks/M10_behavior_planner/T212_proactive_draft_generator.md`
- [ ] T213: CandidateAction review CLI。任务包：`docs/tasks/M10_behavior_planner/T213_candidate_action_review_cli.md`
- [ ] T214: behavior safety eval。任务包：`docs/tasks/M10_behavior_planner/T214_behavior_safety_eval.md`

## Milestone 11: OutboundSendGate + Feishu Sandbox

目标：先建立所有平台发送前的安全阀，再接 fake adapter 和飞书沙箱；平台不得进入核心逻辑。

- [ ] T220: OutboundMessageRequest schema。任务包：`docs/tasks/M11_outbound_sendgate_feishu/T220_outbound_message_request_schema.md`
- [ ] T221: OutboundSendGate。任务包：`docs/tasks/M11_outbound_sendgate_feishu/T221_outbound_send_gate.md`
- [ ] T222: local fake adapter。任务包：`docs/tasks/M11_outbound_sendgate_feishu/T222_local_fake_adapter.md`
- [ ] T223: Feishu adapter。任务包：`docs/tasks/M11_outbound_sendgate_feishu/T223_feishu_adapter.md`
- [ ] T224: Feishu review card。任务包：`docs/tasks/M11_outbound_sendgate_feishu/T224_feishu_review_card.md`

## Milestone 12: WeChat Adapter

目标：微信只作为最后的薄 adapter，可替换，不绕过 send gate，不写 memory，不驱动核心架构。

- [ ] T230: WeChat adapter research spike。任务包：`docs/tasks/M12_wechat_adapter/T230_wechat_adapter_research_spike.md`
- [ ] T231: WeChat inbound adapter。任务包：`docs/tasks/M12_wechat_adapter/T231_wechat_inbound_adapter.md`
- [ ] T232: WeChat outbound adapter。任务包：`docs/tasks/M12_wechat_adapter/T232_wechat_outbound_adapter.md`
- [ ] T233: WeChat safety mode。任务包：`docs/tasks/M12_wechat_adapter/T233_wechat_safety_mode.md`

## Historical Current Unique Task (Superseded)

T133: 用历史 holdout 场景评估回复自然度和边界遵守。

任务包：`docs/tasks/M3_relationship_reply_planner/T133_holdout_eval.md`

为什么现在做它：T132 已完成并被 review `PASS_WITH_WARNINGS` 接受，policy/boundary 风险层已接入 ReplyPlanner。M3 仍未完成；下一步需要 T133 做匿名 holdout eval，验证 T130-T132 的 ReplyPlanner 是否在自然度、边界遵守、证据使用和隐私安全上足以给出 Gate M3 判断。本任务不修改 planner 代码，不提交私密原文，不进入 M4。

## Next Captain Output Required

下一轮 Captain 分发任务时必须输出：

1. 当前唯一任务。
2. 为什么现在做它。
3. Worker 任务包。
4. 允许修改的文件范围。
5. 禁止做的事。
6. 验证命令或验收标准。
7. 完成后需要更新的治理文件。
