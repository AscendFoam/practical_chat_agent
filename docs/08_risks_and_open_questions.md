# Risks And Open Questions

## Captain Update 2026-05-16

Authoritative current risk state after T133/M3 review:

- R035 remains active but is narrowed: T133 holdout partially verifies structure and safety behavior, not relationship-aware maturity. Naturalness is 3/5 and evidence usage is 3/5, so maturity claims remain prohibited.
- R036 remains active: T131-T133 still lack committed regression tests/fixtures. T150 must cover ReplyPlanner contract, policy detection, privacy leakage, contact alignment, ranking, boundary sensitivity, thin context, false positives, and subtle false negatives.
- R037 remains active: T133 observed both false-positive and subtle false-negative probes, so keyword/substr policy risk must be carried into T150 or later refactor.
- R038 is active: M4 feedback logs may be mistaken for automatic learning. T140 must record feedback only and must not mutate ContactSkill/Memory, planner templates, or outbound behavior.

Closed question Q123: Gate M3 is `Conditional`; T140 may proceed only under review-only constraints and with T150 regression tests carried forward.

## Captain Update 2026-05-16: Roadmap Risks

- R039 is active: adopting the updated GPT roadmap too aggressively could reintroduce platform/external-memory scope creep. Mitigation: task board now delays Mem0, Feishu, WeChat, BehaviorPlanner, and LLM drafting behind explicit gates.
- R040 is active: ContactSkill decomposition could accidentally become a breaking replacement. Mitigation: M6 is defined as compatible projection with fallback, not deletion.
- R041 is active: feedback-to-patch could be mistaken for automatic learning. Mitigation: M5 patches remain candidate/review-only and require supporting feedback ids.

Closed question Q124: the updated GPT roadmap is directionally aligned, but M4/M5+ tasks needed revision to preserve feedback-first and regression-first sequencing.

更新日期：2026-05-16

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
| R016 | T112+ 若不消费 T110 保留的不确定性信号，仍可能在摘要/事实抽取中抹平风险 | 后续摘要/事实抽取可能忽略 `risk_flags`、`interaction_flags` 或原始 message type 的不确定性 | T110 review 已确认 chunker 保留/汇总传递相关信号；T112 schema 与抽取逻辑必须显式承接这些字段 |
| R017 | T110 chunker 尚缺自动化测试覆盖 | 边界切分、异常 timestamp、report 形态或隐私泄漏可能在后续改动中回归 | T110 reviewer 判定不阻塞；T150 必须补 chunker fixture/unit tests 与 privacy leakage smoke test |
| R018 | `chunking_reason` 对 conversation/contact 结构边界表达偏粗 | 后续模块若只看 reason 而忽略 `boundary_flags`，可能误解 chunk 边界含义 | T110 reviewer 判定不阻塞；T112/T113/T150 使用 chunk 时应优先读取 `boundary_flags` 和统计字段 |
| R019 | T111 schema 的部分 ContactSkill 风格字段仍是自由字符串 | 后续 LLM 输出可能出现枚举漂移，影响 review 和统计一致性 | T111 reviewer 判定 MVP 可接受；T112/T113 记录实际输出形态，T150 或后续 schema 收紧为 `Literal` |
| R020 | `redaction_policy` 当前为 `dict[str, Any]` | 缺少字段级校验，后续 store/review 可能出现策略键不一致 | T111 reviewer 判定不阻塞；T120/T150 可改为结构化 Pydantic model |
| R021 | `DistillationMemoryType` 与现有运行时 `MemoryType` 未统一 | approved memory candidate 入库时可能需要映射，若未处理会造成类型不一致 | T120 负责定义 `MemoryFactCandidate` -> `MemoryFact` 映射 |
| R022 | T111 candidate schema 暂无 `created_at` / `updated_at` | 文件 store、审阅和版本追踪可能缺少生成/更新时间 | T120 store 或产物写入层补充时间戳 |
| R023 | T111 Pydantic 约束尚缺自动化测试 | `evidence_refs` 非空、`confidence` 范围等约束未来可能回归 | T150 补合法/非法 JSON 的 Pydantic 校验测试 |
| R024 | T112 实测发现 provider 返回 JSON 形状会漂移，可能使用 `predicate/object/high` 一类字段，而不是直接命中 T111 schema | 若没有兼容归一化层，真实小样本会在 schema 校验前失败，导致 distillation 无法写出 | T112 已加入 provider 输出归一化层并在 `private/distilled/t102_smoke` 小样本验证通过；T150 仍应补充 provider shape drift 回归测试 |
| R025 | T112 evidence refs fallback 允许使用 `chunk_id` 作为粗粒度证据 | claim 可能缺少 event_id 级证据，后续人工审阅时证据精度不足 | T112 reviewer 判定不阻塞；T114 统计仅 chunk_id 级 evidence 的比例并人工抽查 |
| R026 | T112 sensitivity 与 memory_type fallback 使用关键词兜底 | 可能出现敏感度低估或 memory type 误分类 | MVP 可接受；T114/T150 观察误分类并补充测试或收紧规则 |
| R027 | T112 LLM 管线缺少自动化测试 | schema 校验、evidence refs 范围、PII 脱敏、provider 归一化未来可能回归 | T150 必须补充自动化测试 |
| R028 | T113 ContactSkill builder 的启发式 tokens/topic/relationship 推断偏当前小样本 | 换联系人或更大样本时，preferred topics、avoid topics、relationship_type 等可能为空或误导 | T113 reviewer 判定不阻塞；T114 必须用样本 run 观察泛化，T120+ 可考虑 LLM-assisted inference |
| R029 | T113 confidence/closeness/trust 数值由公式生成，未按 evidence quality 加权 | 人工 reviewer 可能误读为精确关系量化，导致过度信任 candidate | T113 reviewer 判定 candidate-only 可接受；T114 检查数字是否显得过度精确，T120+ 重设评分策略 |
| R030 | T114 样例虽然 evidence chain 完整，但 reflection / reply-strategy 类 claim 已出现“短证据 -> 平滑 paraphrase”压缩 | 若后续样例更复杂，reviewer 可能高估 claim 的稳健度，进而放大 ContactSkill 中的策略推断 | T114 记录为 `Conditional`；M2 前保持 candidate-only / human-review-first，并在更广样例上继续抽查 |
| R031 | T120 file store 缺少已提交自动化测试 | store model validation、legacy wrapping、load/save round-trip、runtime-ready gate 或 path confinement 未来可能回归 | T120 reviewer 判定不阻塞；T150 必须补对应单测和 path confinement 测试 |
| R032 | T121 evidence validator 缺少已提交自动化测试 | evidence index、nested `evidence_refs` collection、status gate 或 path confinement 未来可能回归 | T121 reviewer 判定不阻塞；T150 必须补 validator 单测与 good/bad fixture 覆盖 |
| R033 | T122 review CLI 缺少已提交自动化测试 | approval gate、reject/freeze/archive、review history、stable record_id 或 export confinement 未来可能回归 | T122 reviewer 判定不阻塞；T150 必须补 full approval lifecycle 与 no-auto-approve 测试 |
| R034 | T130 ReplyPlan 可能出现重复 `priority_rank`，且 `ReplyPlanSourceContext` 可能与 `ReplyPlan.contact_id` 在组装时错位 | 候选排序会歧义，或出现跨联系人上下文串线 | T131 已实现唯一排序与 contact 对齐校验；T150 仍需补回归测试，确认后可关闭 |
| R035 | T131/T132 候选草稿仍主要由 deterministic templates 驱动，relationship-aware 质量尚未通过 holdout 验证 | “relationship-aware” 质量可能被高估，候选可能显得泛化或不够贴合真实关系边界 | T132 已把 boundary / avoid topics / over-proactivity 转成风险控制；T133 必须用匿名 holdout 评估自然度、边界遵守和证据使用 |
| R036 | T131/T132 只有 inline synthetic verification，尚无 committed test/fixture | 干净环境和后续重构存在回归风险 | T150 必须补 ReplyPlanner contract、policy detection、privacy leakage、contact alignment 和 ranking tests；T133 可先记录匿名化人工评估结果 |
| R037 | T132 policy layer 使用 substring keyword matching，可能出现 false positives | 某些普通文本可能被误判为敏感、过度主动或边界场景，导致候选过度保守 | T133 holdout eval 记录 false-positive / false-negative 样例；T150 或后续 refactor 可引入更精确的匹配规则 |
| R038 | M4 feedback log 可能被误解为自动学习或自动记忆更新 | 用户反馈若被直接应用，可能绕过 human-review-first 和 evidence/versioning 约束 | T140 只允许记录 private feedback，不得自动修改 ContactSkill/Memory、planner templates 或 outbound behavior；T141/T142 才能在 reviewable proposal/versioning 范围内继续 |
| R039 | 更新版路线图若被过度提前执行，可能重新引入平台接入、外部 memory 或 LLM scope creep | 破坏当前 offline-first / review-only / evidence-first 安全骨架 | Task board 已把 Mem0、Feishu、WeChat、BehaviorPlanner、LLM drafting 延后到 M7-M12，并要求先通过 M4/M4.5/M5/M6 gates |
| R040 | ContactSkill decomposition 可能被误执行成 breaking replacement | 现有 T113/T120-T123/T130-T133 evidence pipeline 和 runtime context 可能失效 | M6 明确定义为 compatible projection；保留 ContactSkill 作为 legacy aggregate / evidence bundle，并要求 fallback |
| R041 | Feedback-to-Patch 可能被误解为自动学习 | 单条反馈可能被过度泛化并污染长期回复策略 | M5 patches 必须保持 candidate/review-only，包含 supporting_feedback_ids，不自动 approve、不自动 runtime injection |

## Open Questions

| ID | 问题 | 需要谁回答 | 最晚解决点 |
| --- | --- | --- | --- |
| _None_ | _None_ | _None_ | _None_ |

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
| Q113 | T110 conversation chunker v0 是否足以作为 M1 后续输入？足以作为 MVP 输入。 | `docs/review/T110_review.md` PASS |
| Q114 | T111 distillation schemas 是否足以作为 T112 JSON 校验边界？足以作为 MVP schema。 | `docs/review/T111_review.md` PASS |
| Q115 | T112 summary/fact extraction 是否足以支撑 ContactSkill builder？足以作为 T113 的 MVP 输入。 | `docs/review/T112_review.md` PASS |
| Q116 | T113 ContactSkill builder 是否足以支撑 M1 sample review？足以作为 T114 MVP 输入，但带启发式和 confidence warning。 | `docs/review/T113_review.md` PASS_WITH_WARNINGS |
| Q105 | 第一轮 distillation MVP 选哪个联系人或样本？已使用 `private/distilled/t102_smoke` 作为 T114 milestone sample。 | `docs/review/T114_milestone_review.md` worker draft |
| Q106 | LLM 抽取模型、预算和脱敏策略如何处理？T112 已使用配置化 OpenAI-compatible provider/model 路径，并在 prompt 层执行最小 PII token 替换；更完整的 privacy leakage 测试留给 T150。 | `docs/review/T112_review.md` PASS |
| Q107 | ContactSkill review 采用什么形态？M1 采用 Markdown review artifact，CLI review/approve/export 延后到 T122。 | `docs/review/T113_review.md` PASS_WITH_WARNINGS |
| Q117 | Gate M1 是否允许进入下一里程碑？允许以 `Conditional` 进入 M2；必须保持 candidate-only / human-review-first，保留 evidence refs/status，并继续跟踪 R028/R029/R030。 | `docs/review/T114_review.md` + `docs/review/M1_review.md` |
| Q118 | T120 file store 是否足以作为 T121/T122 的基础？足以作为 MVP 基础，但带自动化测试 deferred warning。 | `docs/review/T120_review.md` PASS_WITH_WARNINGS |
| Q119 | T121 evidence validator 是否足以作为 T122 approval gate 的基础？足以作为 MVP 基础；T122 必须读取 validation report 并禁止 missing refs approval。 | `docs/review/T121_review.md` PASS_WITH_WARNINGS |
| Q120 | T122 review CLI 是否足以作为 T123 context integration 的准入基础？足以作为 MVP 基础；T123 必须只读取 approved + runtime-ready records。 | `docs/review/T122_review.md` PASS_WITH_WARNINGS |
| Q121 | T131 是否足以作为 T132 的输入基础？足以作为安全 wiring baseline，但不是质量完成版；T132 必须补 policy/boundary 风险层，M3 仍未完成。 | `docs/review/T131_review.md` PASS_WITH_WARNINGS |
| Q122 | T132 是否足以作为 T133 的输入基础？足以作为 policy/boundary baseline，但不是最终质量证明；T133 必须做匿名 holdout eval 和 Gate M3 判断。 | `docs/review/T132_review.md` PASS_WITH_WARNINGS |
| Q123 | Gate M3 是否允许进入下一里程碑？允许以 `Conditional` 进入 M4/T140，但仅限 review-only feedback capture，并必须把 T150 regression tests 条件带入后续。 | `docs/review/T133_review.md` PASS_WITH_WARNINGS + `docs/review/M3_review.md` |
| Q124 | `gpt的后续设计思路(更新版).md` 是否符合当前项目？方向符合，但必须收敛执行顺序；已将 M4 改为 feedback capture/validate/summary，新增 M4.5 regression hardening，并把 feedback-to-patch、ContactSkill decomposition、LLM planner、RelationshipState、MemoryRetriever、BehaviorPlanner、Feishu、WeChat 延后到 gated milestones。 | Captain roadmap alignment decision + `docs/04_task_board.md` update |

## Deferred Items

- iLink 登录、收消息、reply、媒体和 `context_token` 验证。
- 微信桌面扫描记录读取。
- 实时平台接入。
- 自动发送。
- 向量数据库和 pgvector。
- DPO/微调/LoRA。
- 前端 review UI。
