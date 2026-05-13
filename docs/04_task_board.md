# Task Board

更新日期：2026-05-13

## Board Rules

- 只有 `Current Unique Task` 可以被 worker 执行。
- 每个任务的具体任务包在 `docs/tasks/<milestone>/` 中。
- Worker 只读本任务包指定输入，只改 `Allowed files`。
- Reviewer 完成后由 Captain 更新本任务板、`07_handoff`、`08_risks_and_open_questions` 和必要的 `05_decision_log`。
- 微信真实发送、主动触发、SDK vendor 都不能提前做。
- T00 review 结论为 `PASS`；Gate 0 仍未通过。

## Milestone 0: WeChatBot/iLink 隔离 POC

目标：在仓库外验证 WeChatBot/iLink 是否值得进入主仓库。

- [x] T00: 建立仓库外 sandbox 并记录 SDK 安装与 QuickStart 结果。任务包：`docs/tasks/M0_wechat_ilink_poc/T00_sandbox_install.md`
- [ ] T01: 验证扫码登录、凭据缓存、重启恢复和会话失效表现。任务包：`docs/tasks/M0_wechat_ilink_poc/T01_login_session.md`
- [ ] T02: 验证增量收消息字段、消息 ID、联系人/会话 ID 与 `context_token`。任务包：`docs/tasks/M0_wechat_ilink_poc/T02_receive_context_token.md`
- [ ] T03: 验证文本 reply/send 与媒体元数据能力。任务包：`docs/tasks/M0_wechat_ilink_poc/T03_reply_media.md`
- [ ] T04: 完成 `wechat_ilink_poc_notes` 与 Gate 0 决策。任务包：`docs/tasks/M0_wechat_ilink_poc/T04_gate0_decision.md`

Gate 0：只有 POC 可登录、收消息、reply、媒体行为清楚且风险可接受，才进入 M1。

## Milestone 1: 微信 iLink 增量消息接入主流程

目标：先 fixture、后真实 SDK，把微信新消息接到现有 runtime，默认 disabled。

- [ ] T10: 新增 iLink raw payload fixture mapper，不依赖真实 SDK。任务包：`docs/tasks/M1_wechat_ilink_ingestion/T10_fixture_mapper.md`
- [ ] T11: 新增微信 iLink 配置项和可见 CLI 壳，默认 disabled。任务包：`docs/tasks/M1_wechat_ilink_ingestion/T11_config_cli_skeleton.md`
- [ ] T12: 新增 platform account/session/context token additive schema 与仓储。任务包：`docs/tasks/M1_wechat_ilink_ingestion/T12_session_token_storage.md`
- [ ] T13: 实现 session/token 服务，支持 token upsert 与失效标记。任务包：`docs/tasks/M1_wechat_ilink_ingestion/T13_session_token_service.md`
- [ ] T14: 实现 `wechat-ilink-listen --limit n`，把真实或 adapter 消息送入 runtime。任务包：`docs/tasks/M1_wechat_ilink_ingestion/T14_limited_listen.md`
- [ ] T15: 完成 Gate 1 fixture/limited-listen 验证与文档更新。任务包：`docs/tasks/M1_wechat_ilink_ingestion/T15_gate1_review.md`

## Milestone 2: 微信 ingestion、去重、媒体与历史补录统一

目标：统一 iLink、桌面扫描、手工导入三类微信来源。

- [ ] T20: 新增 raw payload 与 ingest run 归档模型。任务包：`docs/tasks/M2_wechat_ingestion_unification/T20_raw_ingest_models.md`
- [ ] T21: 实现 dedupe service 和 canonical event 写入策略。任务包：`docs/tasks/M2_wechat_ingestion_unification/T21_dedupe_service.md`
- [ ] T22: 将 `WeChatDesktopConnector` 结果接入统一 ingestion。任务包：`docs/tasks/M2_wechat_ingestion_unification/T22_desktop_ingestion.md`
- [ ] T23: 实现微信手工导入文件最小 parser。任务包：`docs/tasks/M2_wechat_ingestion_unification/T23_import_file.md`
- [ ] T24: 新增 media asset 元数据服务与 CLI。任务包：`docs/tasks/M2_wechat_ingestion_unification/T24_media_assets.md`

## Milestone 3: ContactSkill / RelationshipSkill 蒸馏

目标：生成可审阅、可追溯、可脱敏的联系人 Skill，并注入建议链路。

- [ ] T30: 新增 contacts/contact_skills 模型、Pydantic schema 与仓储。任务包：`docs/tasks/M3_contact_skill/T30_contact_models.md`
- [ ] T31: 实现 contact resolution，统一 platform user/channel 到 contact。任务包：`docs/tasks/M3_contact_skill/T31_contact_resolution.md`
- [ ] T32: 实现 ContactSkill 生成服务，基于摘要和证据，不直接塞全量原文。任务包：`docs/tasks/M3_contact_skill/T32_skill_generation.md`
- [ ] T33: 实现 review/approve/export CLI。任务包：`docs/tasks/M3_contact_skill/T33_skill_review_cli.md`
- [ ] T34: 将 approved ContactSkill 压缩注入 `ChatContext` 和回复建议。任务包：`docs/tasks/M3_contact_skill/T34_skill_context_injection.md`

## Milestone 4: 记忆生命周期与联系人画像强化

目标：补齐记忆纠错、冻结、证据链、冲突和反思。

- [ ] T40: 为记忆增加 status/metadata 过渡能力和 freeze/archive/correct CLI。任务包：`docs/tasks/M4_memory_lifecycle/T40_memory_status_cli.md`
- [ ] T41: 实现 evidence/conflict 可视化和冲突降权。任务包：`docs/tasks/M4_memory_lifecycle/T41_evidence_conflicts.md`
- [ ] T42: 实现 `memory-reflect` 时间窗口反思记忆。任务包：`docs/tasks/M4_memory_lifecycle/T42_memory_reflection.md`
- [ ] T43: 确保 ContactSkill 只优先使用 approved memory/event 证据。任务包：`docs/tasks/M4_memory_lifecycle/T43_skill_approved_sources.md`

## Milestone 5: 半自动微信回复投递闭环

目标：审批后用微信 iLink 完成文本投递，并完整审计。

- [ ] T50: 新增 `WeChatIlinkDeliveryConnector` 文本发送，处理 token 缺失/失效。任务包：`docs/tasks/M5_wechat_delivery/T50_wechat_delivery_connector.md`
- [ ] T51: 扩展微信平台 policy：群聊草稿、安静时段、频率、avoid topics。任务包：`docs/tasks/M5_wechat_delivery/T51_wechat_policy.md`
- [ ] T52: 增强 action CLI 的 platform/status/context/policy 查看能力。任务包：`docs/tasks/M5_wechat_delivery/T52_action_operator_ux.md`
- [ ] T53: 完成安全测试会话 E2E 发送验证与 Gate 3 决策。任务包：`docs/tasks/M5_wechat_delivery/T53_gate3_send_validation.md`

## Milestone 6: 主动触发与长期关系管理

目标：只生成审批草稿的主动关系提醒，不做无人值守自动聊天。

- [ ] T60: 新增 trigger_rules/scheduled_actions 模型与仓储。任务包：`docs/tasks/M6_proactive_relationship/T60_trigger_models.md`
- [ ] T61: 实现 trigger create/list/disable/run-once CLI。任务包：`docs/tasks/M6_proactive_relationship/T61_trigger_cli.md`
- [ ] T62: 实现 scheduled action 生成器，默认 `PENDING_APPROVAL` 或 `DRAFT_ONLY`。任务包：`docs/tasks/M6_proactive_relationship/T62_scheduled_actions.md`
- [ ] T63: 实现退让、限频、禁用与 quiet-hours 规则验证。任务包：`docs/tasks/M6_proactive_relationship/T63_proactive_policy.md`

## Milestone 7: 工程硬化、迁移、测试、观测

目标：把新增能力从实验态推进到可回放、可测试、可排错。

- [ ] T70: 引入 Alembic baseline 或等价 migration 方案。任务包：`docs/tasks/M7_engineering_hardening/T70_migrations.md`
- [ ] T71: 建立 tests 目录并覆盖微信 mapper、dedupe、policy、delivery 失败路径。任务包：`docs/tasks/M7_engineering_hardening/T71_tests.md`
- [ ] T72: 新增 `system-status`、`connector-status`、`wechat-status`、`policy-status`。任务包：`docs/tasks/M7_engineering_hardening/T72_status_cli.md`
- [ ] T73: 完成全链路文档、配置样例和 milestone review。任务包：`docs/tasks/M7_engineering_hardening/T73_final_milestone_review.md`

## Current Unique Task

T01: 验证扫码登录、凭据缓存、重启恢复和会话失效表现。

任务包：`docs/tasks/M0_wechat_ilink_poc/T01_login_session.md`

为什么现在做它：T00 只证明 SDK 可安装并进入二维码阶段。Gate 0 还需要先确认真实扫码、凭据落盘、重启复用、会话失效和自动重登行为；这些结果决定 T02 收消息和 T03 reply/media 是否值得继续。

T01 额外输入：

- T00 reviewer 的 N01 已接受：确认 `Python 3.12.7` sandbox 与项目常用 Python 3.11 环境的兼容边界。
- T00 reviewer 的 N02 已接受：确认官方文档 URL 与本地 `wechatbot-sdk 0.2.1` 行为是否对应。

## Next Captain Output Required

下一次 Captain 分发任务时，必须输出：

1. 当前唯一任务。
2. 为什么现在做它。
3. Worker 任务包。
4. 允许修改的文件范围。
5. 禁止做的事。
6. 验证命令或验收标准。
7. 完成后需要更新的治理文件。
