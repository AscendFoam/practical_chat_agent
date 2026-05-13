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
| R011 | 当前脱敏 fixture 尚未覆盖 `type=80`/`chatRecords` 转发结构 | T102 adapter 可能缺少复杂消息样例，T150 测试覆盖不足 | deferred 到 T102/T150，后续补充合成 fixture，不使用真实原文 |
| R012 | `event_id` 当前采用 SHA-1 规则可能被误解为安全哈希 | 长期可追溯 ID 规则可能需要更强或更明确的稳定性/隐私说明 | deferred 到 T102，决定保留 SHA-1、升级 SHA-256 或补充命名空间规则 |

## Open Questions

| ID | 问题 | 需要谁回答 | 最晚解决点 |
| --- | --- | --- | --- |
| Q101 | 在存在额外 `member` 行时，如何把私聊导出的 `sender_role` 判定做得足够稳健？ | T102 worker / reviewer | T102 |
| Q102 | normalized event 输出时区应默认 `Asia/Shanghai`，还是同时保留 UTC 与本地时间？ | Captain / T102 worker | T102 |
| Q103 | `type=7` 与稀有 `type=4/23/24/99` 应如何进一步细分？ | T102 worker | T102 |
| Q105 | 第一轮 distillation MVP 选哪个联系人或样本？ | 用户/Captain | T114 前 |
| Q106 | LLM 抽取使用哪个模型、预算和脱敏策略？ | 用户/Captain | T112 前 |
| Q107 | ContactSkill review 先用 Markdown 文件还是 CLI？ | Captain | T113 前 |
| Q108 | `event_id` 是否应从 SHA-1 升级为 SHA-256，或保留 SHA-1 但加入更明确的 namespaced input 规则？ | Captain / T102 worker | T102 |

## Closed Questions

| ID | 结论 | 关闭依据 |
| --- | --- | --- |
| Q001 | SDK 包名为 `wechatbot-sdk`，验证版本 `0.2.1`，导入路径为 `from wechatbot import WeChatBot`。 | T00 notes + T00 review |
| Q002 | 是否继续修微信扫码登录？不继续。 | 用户本轮明确跳过微信聊天记录扫描/SDK路线 |
| Q100 | WeFlow 顶层行类型稳定分为 `header`、`member`、`message`；normalized event 只需要消费 `_type=message`。 | T100 worker draft + `docs/review/T100_review.md` PASS |
| Q104 | 可以生成安全脱敏 fixture，且最小样例不包含真实内容。 | T100 worker draft + `docs/review/T100_review.md` PASS |

## Deferred Items

- iLink 登录、收消息、reply、媒体和 `context_token` 验证。
- 微信桌面扫描记录读取。
- 实时平台接入。
- 自动发送。
- 向量数据库和 pgvector。
- DPO/微调/LoRA。
- 前端 review UI。
