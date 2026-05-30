# 商业化陪伴式 Chat Agent 后续路线深度调研 Prompt

你是接手 `practical_chat_agent` 项目的 GPT-Pro 深度调研 AI。请联网调研并输出一份中文报告，目标是帮助项目从当前的“离线关系记忆 + 回复草稿 + 人工审核 + 平台安全边界”原型，规划成一个可商业化、可合规运营、可长期迭代的陪伴式 AI 人格对象产品。

你的任务不是写代码，而是做外部调研、产品判断、技术路线设计、法规风险梳理和后续 milestone/task 建议。报告必须能直接指导后续 Captain 把路线拆成工程任务包。

## 1. 当前项目背景

仓库：`D:\Codes\Social\practical_chat_agent`

当前主线已经完成到 M12：

- 基于 WeFlow 导出的私密聊天记录做本地离线蒸馏。
- 已有 evidence-backed memory、ContactSkill/derived briefs、RelationshipState、MemoryRetriever、LLM-assisted ReplyPlanner、BehaviorPlanner、OutboundSendGate、Feishu sandbox/review card。
- M12 探索了 WeChat-family adapter，但结论是 `Gate M12 Conditional`：
  - 只接受本地、合成、dry-run 的 WeCom Customer Service slice。
  - 不授权 live WeChat/WeCom delivery、credentials、callbacks、polling、transport、retry、acknowledgement、failure-event mutation、production recipient mapping 或 automatic sending。
  - personal WeChat automation、scan-login resurrection、desktop automation、unofficial SDK vendoring 仍然 blocked。

请把 M12 之后的方向视为一次产品战略再定位，而不是继续堆平台适配。

## 2. 新产品设想

用户希望把项目推进成更完整的商业化陪伴式 chat agent，核心不是“冒充真人”，而是：

- 用户可以深度自定义一个 AI 聊天对象。
- 用户可以用详细描述、模糊设定、模板、随机种子或聊天记录风格启发来生成角色。
- 角色能有长期记忆、关系历史、人格演化、可解释的成长。
- 角色能在用户授权下主动发消息，但必须克制、可控、不制造依赖和愧疚。
- 角色可以有“虚拟生活流”：动态、日记、私密世界线、虚拟朋友圈、语音留言、虚拟照片等。
- 长期可探索授权语音、虚拟形象、非真人风格 avatar、合规真人风格数字分身。
- 真人聊天记录蒸馏必须优先做 L1/L2：抽象风格启发、去身份化新角色；谨慎做本人授权数字分身；极谨慎做逝者纪念；不做非授权克隆前任、家人、公众人物。

请重点评价：这个方向是否适合商业化，如何阶段化落地，哪些能力应该先做，哪些必须推迟或禁止。

## 3. 必须联网调研的主题

### 3.1 竞品和市场

请调研国内外陪伴式 AI / AI 角色 / AI 恋爱 / AI 朋友 / AI 生活流产品，至少包括：

- TheOne / 响梦环
- 爱语 AI 键盘或类似恋爱回复辅助产品
- Replika
- Character.AI
- Talkie / MiniMax 星野 / Glow / 猫箱 / 米苏时空 / 轻偶 / AI Love 等同类产品中公开可查部分
- 具备主动消息、长期记忆、角色动态、语音、avatar、朋友圈/生活流的产品

请输出：

- 核心卖点矩阵
- 定价/商业模式
- 目标用户
- 差异化点
- 已有能力是否已经同质化
- 用户痛点和差评中反复出现的问题
- 哪些方向仍有产品空白

### 3.2 长期记忆和人格系统研究

请调研并比较：

- Generative Agents
- MemoryBank
- MemGPT / Letta
- LangMem
- Mem0
- Graphiti / Zep
- MemoryOS
- A-MEM
- RMM / reflective memory management
- LoCoMo、LongMemEval、BEAM、LongMemEval-V2 等长期对话记忆评测
- memory poisoning / RAG poisoning / AgentPoison / MINJA 等长期记忆安全风险
- sleep-time compute、offline memory consolidation、dreamer / imagined memory 方向

请回答：

- 哪些概念适合工程落地到本项目？
- 如何区分 episodic / semantic / relational / procedural / imagined memory？
- 如何实现“难忘”“自然遗忘”“压缩遗忘”“强制遗忘”？
- 如何避免把 imagined/dream memory 当作 factual memory？
- 如何支持用户查看、编辑、删除、冻结、导出记忆？
- 如何评估记忆质量和关系连续性？

### 3.3 人格编译与人格演化

请设计一个商业产品可用的 `Persona Compiler`：

- 输入：用户描述、模糊偏好、问卷、模板、随机种子、聊天记录风格启发。
- 输出：角色身份、人格核心、说话风格、情绪模型、关系模式、虚拟经历、边界禁忌、成长策略、主动行为偏好。
- 需要支持“稳定核心 + 可解释变化”，而不是每轮漂移。
- 需要支持用户手动编辑和版本回滚。

请给出建议 schema、生成流程、人工审核/自动校验流程、相似度限制、去身份化转换层。

### 3.4 主动陪伴和安全策略

请调研主动消息在陪伴产品中的作用与风险，设计一套安全 `Proactive Engine`：

- 用户授权开关
- 每日/每周频次限制
- 安静时段
- 允许的消息类型
- 高亲密表达阈值
- 连续追问限制
- 危机/低落场景处理
- 未成年人保护
- 依赖/沉迷提醒
- 反操控规则

请明确禁止：

- 制造抛弃感、愧疚感、唯一依赖感
- 情绪勒索式留存
- 深夜高频刺激
- 引导脱离现实关系
- 诱导付费解锁亲密或安慰

### 3.5 虚拟生活流和多模态路线

请调研“AI 朋友圈 / 角色动态 / 私密世界线 / 虚拟日记 / 虚拟照片 / 语音留言 / Live2D / 3D avatar / 视频通话”的产品和技术路线。

请区分：

- 文本动态
- 虚拟照片/图片生成
- 平台授权音色
- 用户本人授权音色
- 第三方本人授权数字分身
- 非真人 avatar
- 真人风格 deepfake / talking head

请给出阶段化路线：

1. 文本 + 角色动态
2. 授权平台音色 + 语音通话
3. 非真人虚拟形象 + 短视频动态
4. 低延迟 avatar 视频通话
5. 经严格授权的真人风格数字分身

请说明每阶段的技术复杂度、合规风险、成本、验证方式和不应触碰的边界。

### 3.6 法规、合规、伦理和平台政策

请面向中国市场和国际市场分别调研：

- 中国《人工智能拟人化互动服务管理暂行办法》及其生效时间、适用范围、关键义务。
- 中国《互联网信息服务深度合成管理规定》。
- 中国《人工智能生成合成内容标识办法》。
- 中国《个人信息保护法》。
- 民法典关于肖像、声音、名誉、隐私、死者人格利益的相关规则。
- 未成年人保护、沉迷/依赖、心理危机干预、算法备案、安全评估触发条件。
- App Store / Google Play / 微信生态 / 国内应用商店对 AI 陪伴、深度合成、成人内容、情感依赖、虚假身份的政策。
- 国际上 GDPR、CCPA、AI companion safety、deepfake/voice clone consent 的关键约束。

请输出：

- 必须从第一版就做的合规底座
- 哪些功能需要用户单独同意
- 哪些功能需要第三方本人授权
- 哪些功能需要近亲属/权利人授权
- 哪些营销表述禁止使用
- 哪些能力不建议开源
- 数据留存、删除、导出、训练使用、内容标识、水印、审计日志建议

### 3.7 商业模式和开源策略

请判断：

- 项目应完整开源、部分开源，还是商业闭源为主？
- 哪些基础组件适合开源？
- 哪些高风险能力不应开源？
- 免费层、订阅层、高级层、专业/授权层、创作者市场如何设计？
- 如何避免“孤独榨取”式商业模式？
- 怎样验证用户愿意长期使用并付费？

## 4. 请给出后续 milestone 建议

请在调研后给出一个可执行的 M13+ 路线图。每个 milestone 必须包含：

- Goal
- Why now
- Scope
- Explicit non-goals
- Key data models / services
- Verification / eval
- Review gate
- Risks
- Candidate task list

请至少覆盖这些方向，但可以调整顺序：

- M13: Commercial companion product research and positioning
- M14: Persona Compiler schema and local creation flow
- M15: Memory OS v2 with episodic/semantic/relational/imagined separation
- M16: Relationship Engine semantic consumption by ReplyPlanner/BehaviorPlanner
- M17: Proactive Engine hardening and consent UX
- M18: Virtual Life Stream / role dynamics MVP
- M19: Memory/persona user control surface: view/edit/delete/export/freeze
- M20: Compliance and safety governance baseline
- M21: Product UX prototype for text-first companion
- M22: Voice / avatar exploratory track under authorization constraints

请大胆但要有边界：worker 能力很强，但项目必须继续遵守 review-first、human-approved、privacy-safe、no deception、no unauthorized clone 的原则。

## 5. 输出格式

请输出一份结构清晰的中文调研报告，建议结构：

1. Executive Summary：是否值得商业化、最推荐方向、最大风险。
2. 项目现状校正：当前 repo 到 M12 已经证明/未证明什么。
3. 竞品与市场矩阵。
4. 产品定位建议。
5. 技术架构建议：Persona Compiler / Memory OS / Relationship Engine / Dialogue Engine / Proactive Engine / Virtual Life Engine / Safety & Compliance Engine。
6. 合规与伦理红线。
7. 多模态路线与授权边界。
8. 开源与商业化策略。
9. M13+ milestone/task roadmap。
10. 还需要继续调研的问题。
11. 推荐第一步。

最后单独给出：

```text
推荐第一步：
目标：
为什么：
需要阅读/调研：
建议产物：
后续可拆成的 worker task：
不建议现在做：
```

报告必须包含可执行判断，不要只做资料罗列。若引用网页、法规、论文或 GitHub 项目，请给出链接和日期。若信息可能随时间变化，请明确“截至调研日期”。
