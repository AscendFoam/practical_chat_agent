# Risks And Open Questions

更新日期：2026-05-14

## Active Risks

| ID | 风险 | 影响 | 当前缓解 |
| --- | --- | --- | --- |
| R001 | WeFlow JSONL 字段结构与预期不一致 | parser 和 normalized event 合约不稳定 | T100 先做 schema profiling，不直接实现蒸馏 |
| R002 | 私密聊天内容泄露到可提交目录 | 严重隐私风险 | `private/` 受 `.gitignore` 保护；T100 禁止输出原文和真实标识 |
| R003 | sender_role/direction 判断错误 | 事实归因错位，ContactSkill 失真 | T100 明确方向规则；M1 人工抽查 evidence |
| R004 | LLM 编造关系判断 | 产生错误记忆和越界回复 | 所有 claim 必须有 evidence refs，validator 拦截无证据输出 |
| R005 | 单次情绪/聊天被误判为长期模式 | 关系状态过拟合 | M1 区分单次现象与稳定模式，M2 引入 status/review |
| R006 | 过早引入向量库、UI、实时接入或微调 | 拖慢核心验证 | M0-M1 只做离线 MVP |
| R007 | ContactSkill 被误用为联系人模拟器 | 冒充/数字克隆风险 | 文档和 planner 明确只辅助用户回复，不模拟联系人 |
| R008 | 用户手动迁移 docs 后 git 状态复杂 | 误删或覆盖用户文件 | 不 revert 未确认变更，只基于现有路径更新 |
| R009 | T01 review BLOCK 未修复 | 旧 iLink 路线 Gate 0 不通过 | 用户已决定暂停旧路线，不作为当前阻塞项 |
| R010 | `meta.type=private` 的导出里仍可能出现大量 `member` 行 | 若简单按成员数判断方向，会导致 `sender_role` 判错 | T100 contract 已要求用跨文件复用身份和 message 高频对来判定 user/contact |
| R011 | 当前脱敏 fixture 仍未覆盖 `type=80`/`chatRecords` 的合成输入样例 | T150 前的测试覆盖仍可能不足 | T103 worker draft 认为这不阻塞 M1；T110/T150 必须延续保守处理并补 fixture / 测试 |
| R012 | `event_id` 当前最小实现继续采用 SHA-1 命名空间输入 | 长期可追溯 ID 规则可能需要更强或更明确的稳定性/隐私说明 | T103 worker draft 认为 M1 可先继续使用该规则；若 reviewer 或 T150 测试要求更强摘要，再统一升级 |
| R013 | T101 的结构化替换 token 未在 normalize 阶段实现 | 若后续 LLM 蒸馏直接使用原文，可能出现 PII 泄露风险 | T102 review 认为 normalize 私有输出保留原文合理；PII token 替换 deferred 到 T112+ 蒸馏阶段 |
| R014 | T102 normalize 当前双次读取文件并全量缓存 normalized lines | 大规模聊天记录可能出现性能或内存瓶颈 | T103 worker draft 认为对当前 38k 行样本可接受；T110/T150 继续评估是否需要流式化 |
| R015 | 单文件数据场景下 `sender_role` 推断可能退化 | 其他用户或单联系人样本可能出现 user/contact 归因不稳 | T103 worker draft 认为这不阻塞进入 T110；T114/T150 需用实际样本验证并保留 `risk_flags` 兜底 |
| R016 | T110 chunker 可能抹平 T102 的不确定性信号 | 后续摘要/事实抽取可能忽略 `risk_flags`、`interaction_flags` 或原始 message type 的不确定性 | T110 必须保留或传递 `source_message_type_code`、`risk_flags`、`interaction_flags` |

## Open Questions

| ID | 问题 | 需要谁回答 | 最晚解决点 |
| --- | --- | --- | --- |
| Q105 | 第一轮 distillation MVP 选哪个联系人或样本？ | 用户/Captain | T114 前 |
| Q106 | LLM 抽取使用哪个模型、预算和脱敏策略？ | 用户/Captain | T112 前 |
| Q107 | ContactSkill review 先用 Markdown 文件还是 CLI？ | Captain | T113 前 |

## Closed Questions

| ID | 结论 | 关闭依据 |
| --- | --- | --- |
| Q001 | SDK 包名为 `wechatbot-sdk`，验证版本 `0.2.1`，导入路径为 `from wechatbot import WeChatBot`。 | T00 notes + T00 review |
| Q002 | 是否继续修微信扫码登录？不继续。 | 用户本轮明确跳过微信聊天记录扫描/SDK路线 |
| Q100 | WeFlow 顶层行类型稳定分为 `header`、`member`、`message`；normalized event 只需要消费 `_type=message`。 | T100 worker draft + `docs/review/T100_review.md` PASS |
| Q104 | 可以生成安全脱敏 fixture，且最小样例不包含真实内容。 | T100 worker draft + `docs/review/T100_review.md` PASS |
| Q101 | T102 使用跨文件 member 对复用、message 高频对、type=80 系统检测、unknown 兜底和 risk_flags 来判定 `sender_role`。 | `docs/review/T102_review.md` PASS |
| Q102 | T102 最小实现默认使用 `Asia/Shanghai` 渲染 normalized timestamp，并保留 `timestamp_epoch_s`。 | `docs/review/T102_review.md` PASS |
| Q103 | T102 最小实现将 `type=7` 保守映射为 `mixed`，将 `type=4/23/24/99` 保守映射为 `unknown`。 | `docs/review/T102_review.md` PASS |
| Q108 | `event_id` 在 T102 保留 SHA-1，但加入 `weflow` 命名空间输入；MVP 可接受，未来可升级。 | `docs/review/T102_review.md` PASS |
| Q109 | T101 的 `[PHONE]`、`[EMAIL]` 等结构化替换 token 不在 normalize 阶段实现，推迟到 T112+ 蒸馏阶段。 | `docs/review/T102_review.md` PASS |
| Q110 | 是否已有隐私脱敏规则和 source_ref/raw_ref 公开形态？已有，T101 已定义 PII 分类、数据区域边界、字段处理矩阵和 allowed public shape。 | `docs/review/T101_review.md` PASS |
| Q111 | T101 fixture preview hex 是否需要返修为真实哈希形态？不需要；作为合成 fixture 注释占位可接受。 | `docs/review/T101_review.md` PASS，N02 accepted |
| Q112 | Gate M0 verdict 为 `Conditional`；允许进入 M1，但 T110/T112+/T114/T150 必须承接条件。 | `docs/review/T103_review.md` accepted worker draft |

## Deferred Items

- iLink 登录、收消息、reply、媒体和 `context_token` 验证。
- 微信桌面扫描记录读取。
- 实时平台接入。
- 自动发送。
- 向量数据库和 pgvector。
- DPO/微调/LoRA。
- 前端 review UI。
