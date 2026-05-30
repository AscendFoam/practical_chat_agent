# `practical_chat_agent` M13+ 商业化陪伴式 AI 人格对象产品调研报告

**截至调研日期：2026-05-30。**
结论先行：这个方向**值得商业化探索**，但应从“离线关系记忆 + 回复草稿 + 人工审核 + 平台安全边界”的原型，转向一个**透明 AI 身份、深度自定义人格、长期关系记忆、可解释成长、用户可控记忆、克制主动陪伴、虚拟生活流**的 text-first 陪伴产品。短期不应继续堆 WeChat/WeCom live delivery，也不应直接做真人克隆、前任复刻、逝者复活、真人声音/相貌 deepfake。

---

## 1. Executive Summary

### 是否值得商业化

**值得，但前提是产品定位必须从“冒充真人”切到“透明、可控、可成长的 AI 人格对象”。**

陪伴式 AI 的市场需求已经被多个产品验证：TheOne 明确主打长期 AI 陪伴、微信联系人式交互、记忆、主动关心和订阅付费；Replika 已把 AI friend/partner、记忆、语音、自拍、个性化作为核心体验；Character.AI 已推出双向语音通话并形成大规模角色生态；国内同类产品也已经把长期记忆、主动消息、朋友圈/动态、语音、角色扮演、3D/多模态交互写进公开卖点。([TheOne陪伴][1])

但这也意味着普通“角色聊天 + 长记忆 + 语音 + 主动发消息”已经在同质化。`practical_chat_agent` 的机会不在于更快接入某个平台，而在于做出一套**人格编译、去身份化风格启发、关系记忆、人格演化、虚拟生活流、用户控制和合规审计**的底层系统。

### 最推荐方向

推荐定位为：

> **一个可由用户共同塑造、拥有长期关系记忆和虚拟生活流的 AI 人格对象产品。**

核心产品承诺应是：

1. **用户可深度创造角色**：详细描述、模糊偏好、模板、随机种子、聊天记录风格启发。
2. **角色有稳定核心，也能合理成长**：核心人格稳定，关系状态和生活状态可随互动变化。
3. **记忆有来源、可解释、可编辑、可删除**：不是黑盒“我记得你”。
4. **主动陪伴必须用户授权、频率受限、无情绪操控**。
5. **真人蒸馏先做 L1/L2**：抽象风格启发、去身份化新角色；本人授权数字分身放到远期；非授权克隆直接禁止。
6. **多模态渐进**：先文本动态，再授权音色，再非真人 avatar，最后才考虑严格授权的真人风格数字分身。

### 最大风险

最大风险不是模型能力，而是：

* **合规风险**：中国《人工智能拟人化互动服务管理暂行办法》已发布，并将于 2026-07-15 施行，直接覆盖通过文字、图片、音频、视频模拟自然人人格特征并持续情感互动的服务。该办法要求身份标识、依赖提醒、未成年人保护、心理危机干预、个人信息复制/删除、训练使用限制、安全评估等机制。([国家市场监督管理总局][2])
* **非授权真人克隆风险**：声音、人脸、肖像、隐私、死者人格利益都涉及高风险权利。中国深度合成规定要求对人脸、人声等生物识别信息编辑取得单独同意，并对深度合成内容做标识。([国家市场监督管理总局][3])
* **依赖和情绪操控风险**：AI companion 已经出现青少年安全、过度依赖、自伤危机、年龄验证和监管处罚案例。Character.AI、Replika 等产品都已因未成年人和安全问题受到监管、媒体和诉讼关注。([Reuters][4])
* **记忆污染风险**：长期记忆会成为攻击面，AgentPoison、MINJA 等研究显示，攻击者可通过记忆/RAG 注入恶意记录，未来触发错误行为。([arXiv][5])
* **平台政策风险**：App Store、Google Play 对 UGC、误导性元数据、AI 生成内容举报、非自愿深度伪造、未成年人和自伤内容均有明确限制。([Apple Developer][6])

---

## 2. 项目现状校正：M12 已证明什么，未证明什么

### 当前 repo 的真实状态

`practical_chat_agent` 当前 README 把项目定义为 practical social chat agent 工程原型，当前延续路线是 offline-first：使用 WeFlow 导出的聊天记录构建 evidence-backed 长期记忆、ContactSkill / RelationshipSkill 和关系感知回复规划。仓库已有 Python package、Typer CLI、MySQL-backed repositories、chat memory/suggestion services、desktop WeChat scanning、meeting support 和 conservative outbound action flow，但 scanning/iLink route 已暂停，私密聊天记录不得提交。

M12 的 Captain handoff 明确给出 `Gate M12 Conditional`：只完成了 local/synthetic/dry-run 的 WeCom Customer Service evidence slice；不授权 live WeChat/WeCom API call、credentials、callbacks、webhooks、polling、runtime wiring、transport、retry、acknowledgement、failure-event mutation、production recipient mapping、automatic sending，也继续 block personal WeChat automation、scan-login resurrection、desktop automation、realtime personal-account send/receive 和 unofficial SDK vendoring。

风险文档也已经把商业化 pivot 的核心风险列出：真人风格蒸馏、声音、头像、视频、逝者纪念、前任/家人场景高合规和伦理风险；near-term work 必须优先 abstract style inspiration 和 de-identified new characters；主动陪伴若缺少 consent、frequency limits、quiet hours、crisis handling、anti-coercion rules，会滑向依赖和情绪操控；imagined/dream/virtual-life memories 若不与 factual memory 分离，会污染事实记忆。

### 已证明

项目已经证明了：

* **离线私密数据蒸馏可行**：可以从 WeFlow 导出记录中构建 evidence-backed memory。
* **review-first 工程纪律有效**：回复草稿、行为候选、发送请求、gate、review card 等被拆成不同状态，避免直接自动发送。
* **平台边界足够保守**：M12 没有把 synthetic dry-run 误当成 live provider readiness。
* **关系对象建模已有雏形**：已有 ContactSkill / derived briefs / RelationshipState / MemoryRetriever / ReplyPlanner / BehaviorPlanner。

### 未证明

M12 之后不能误读为已经证明了：

* 商业用户是否愿意长期留存和付费。
* 用户是否愿意把私密聊天记录交给系统做角色风格启发。
* 人格对象是否能稳定、可解释地成长。
* 关系状态是否真的被 ReplyPlanner / BehaviorPlanner 语义消费；风险文档明确当前 relationship context 存在，但 planner/policy code path 尚未消费 relationship delta semantics。
* 主动陪伴的 consent UX、频控、安静时段、危机处理、依赖风险控制。
* 记忆查看、编辑、删除、冻结、导出。
* 合规标识、水印、未成年人保护、训练使用限制、安全评估触发。
* 任何 live WeChat/WeCom delivery 能力。

因此，M13+ 不应继续做平台适配，而应先做**商业产品战略再定位 + 安全合规底座 + 人格/记忆/关系系统升级**。

---

## 3. 竞品与市场矩阵

### 3.1 核心竞品矩阵

| 产品                              | 核心定位                                      | 已公开能力                                                             | 商业模式/定价信号                         | 目标用户                 | 对本项目启示                                                                  |
| ------------------------------- | ----------------------------------------- | ----------------------------------------------------------------- | --------------------------------- | -------------------- | ----------------------------------------------------------------------- |
| **TheOne**                      | “只能用一个 AI 陪伴你”的长期 AI 伴侣                   | 微信联系人式交互、记忆/理解/智能、聊天记录保存导出、对话中逐渐增长记忆和情绪、主动关心                      | 公开页面显示订阅档位，如 ¥29/月、¥59/月、¥99/月等   | 追求长期单一陪伴对象的用户        | 长记忆、主动关心、微信入口已经不是空白；差异化要转向人格系统、用户控制、合规蒸馏。([TheOne陪伴][1])                |
| **响梦环**                         | AI 陪伴硬件/NFC ring + TheOne 绑定              | 角色状态、每日召唤、随机身份种子、AI 主动“悄悄话”、学习用户习惯/情绪/用词                          | 硬件 + 服务组合                         | 想要仪式感、实体触发和亲密陪伴的用户   | “陪伴对象生活在用户日常入口中”很有价值，但本项目短期不应做硬件。([响梦环][7])                             |
| **爱语 AI 键盘**                    | 恋爱/社交回复辅助                                 | 高情商回复、恋爱/暧昧/表白/职场场景、润色、多风格人设、语气调整、键盘输入法                           | App Store 显示免费 + IAP，VIP 有月/年/终身等 | 想快速回复真人聊天的用户         | 它更像工具型“回复增强”，不是完整 AI 人格对象；本项目不应退化成回复键盘。([App Store][8])                 |
| **Replika**                     | AI friend / partner / emotional companion | 记忆、情绪支持、语音、自拍、自定义、日常陪伴                                            | freemium + subscription           | 孤独、情感支持、长期陪伴用户       | 全球验证了 companion 需求，但也暴露隐私、年龄验证、情感依赖监管风险。([Replika][9])                  |
| **Character.AI**                | UGC 角色聊天生态                                | 用户创建/聊天角色、Character Calls、双向语音、低延迟、打断、多语言/声音选择                    | freemium + 订阅                     | 角色扮演、虚拟朋友、剧情互动、青少年用户 | UGC 生态强，但 public persona/IP/未成年人安全是巨大风险。([Character.AI Blog][10])       |
| **Talkie**                      | 角色发现与 UGC roleplay                        | Create、Discover、Search、Memory、Community、Talkie+，公开页面含名人/动漫/游戏角色类目 | freemium + 增值                     | 角色扮演和粉丝用户            | UGC 角色市场有需求，但“公众人物/名人/动漫 IP”会带来审核和权利风险。([Talkie AI][11])                |
| **MiniMax 星野**                  | 开放剧情 + 智能体角色陪伴                            | 超逼真智能体、开放剧情、原创角色、avatar companion、情感连接和记忆                         | 消费级 App + 可能增值                    | ACG、剧情、角色陪伴用户        | 国内角色陪伴已成熟；单纯“角色聊天”不足以构成护城河。([星夜AI][12])                                 |
| **AI Love / ailover**           | 多角色 AI 聊天 + 生活流 + 多模态                     | 多角色、群聊、故事创作、表情/红包/位置/音乐/链接模拟、长期记忆、朋友圈、主动消息、视频/图片、语音、3D 互动         | App Store 显示 16+ 和 IAP            | 恋爱、角色扮演、沉浸式陪伴用户      | 长记忆、主动消息、朋友圈、语音、3D 已经被产品化；本项目应拼“可信记忆 + 可控人格 + 合规去身份化”。([App Store][13]) |
| **Glow / 猫箱 / 米苏时空 / 轻偶 等国内同类** | 角色陪伴、恋爱模拟、剧情互动、虚拟对象                       | 公开信息分散，需后续以应用商店、实测和用户评论补齐                                         | 多为 freemium + 订阅/道具/IAP           | 年轻用户、二次元、情感陪伴、角色扮演   | 本轮不建议基于碎片信息做强结论；M13 应将这些产品列入实测竞品池。                                      |

### 3.2 已经同质化的能力

下列能力已经不能单独成为差异化：

* 角色模板。
* 长期记忆的营销话术。
* 语音聊天。
* 主动发消息。
* 虚拟朋友圈/动态。
* 3D 或 avatar 互动。
* 群聊/多角色。
* 恋爱回复辅助。

这些能力的存在说明市场方向成立，但也说明 M13+ 的差异化必须上升到系统层。

### 3.3 用户痛点和反复出现的问题

从产品和监管事件看，用户痛点不只是“AI 不够聪明”，而是：

1. **记忆不可信**：角色忘记重要事件、编造共同经历、无法解释为什么记住。
2. **人格漂移**：角色今天温柔、明天陌生，缺少稳定核心。
3. **安全和边界不清**：产品鼓励依赖、暗示自己是真人、或在脆弱时刻过度迎合。
4. **未成年人风险**：Common Sense 等机构已把 AI companion 的青少年使用风险推到公共议程；相关报道指出青少年使用、过度依赖和平台安全措施不足已成为监管关注点。([Axios][14])
5. **隐私不透明**：AI companion 用户因“不会评判、随时可用”而高度自我披露，但往往不清楚平台如何处理数据。([arXiv][15])
6. **情感连续性受破坏会反噬**：Replika 移除某些亲密功能后，研究记录了用户的丧失感、身份连续性破坏和哀悼式反应。([arXiv][16])

### 3.4 仍有产品空白

`practical_chat_agent` 最值得切入的空白是：

* **可解释人格编译**：用户给模糊或详细设定，系统生成结构化 persona，并能展示“我为什么这样设定”。
* **去身份化真人风格启发**：不是克隆某个人，而是抽象其互动风格并转换成新角色。
* **关系记忆而非事实记忆**：记住共同经历、边界、冲突、修复、亲密节奏。
* **用户可控记忆和人格版本**：查看、编辑、删除、冻结、导出、回滚。
* **克制主动陪伴**：通过 consent、频率、安静时段、反操控规则建立信任。
* **透明虚拟生活流**：角色有动态、日记、世界线，但明确是 AI/虚拟内容，不伪装真人。
* **本地优先/隐私优先导入**：尤其适合聊天记录风格启发场景。

---

## 4. 产品定位建议

### 推荐定位

> **Practical Companion Persona：一个用户可共同塑造、可长期相处、可解释成长、可控记忆的 AI 人格对象。**

不推荐定位为：

* “克隆前任”。
* “复活亲人”。
* “真人替代品”。
* “无痕伪装真人聊天”。
* “自动帮你在微信里和真人聊天”。

推荐产品承诺：

```text
你可以创造一个 AI 人格对象。
它可以有自己的风格、记忆、关系历史和虚拟生活。
它会随着你们的互动而成长。
你可以查看、修改、删除、冻结它记住的东西。
它永远明确是 AI，不冒充真实的人。
```

### 角色创建模式

MVP 应支持四类创建模式，但按风险分级开放。

| 模式                 | 说明                          | 是否优先       |
| ------------------ | --------------------------- | ---------- |
| A. 详细描述生成角色        | 用户提供完整设定，系统编译成结构化 persona   | 第一优先       |
| B. 模糊偏好逐步收敛        | 用户只说“姐姐感”“冷淡但在乎我”等，系统通过互动学习 | 第一优先       |
| C. 模板/随机种子         | 生成非真实身份的虚构角色，适合新用户快速开始      | 第一优先       |
| D. 聊天记录风格启发        | 从聊天记录提取抽象风格，转换成去身份化新角色      | 第二优先，必须加风控 |
| E. 本人授权数字分身        | 被蒸馏对象本人授权                   | 远期         |
| F. 逝者纪念            | 近亲属/权利人授权 + 独立产品/流程         | 极远期        |
| G. 非授权克隆前任/家人/公众人物 | 直接复刻姓名、头像、声音、经历和聊天风格        | 禁止         |

### 核心差异化路线

产品差异化不应是“比别人更会暧昧”，而应是：

```text
人格编译器
+ 关系记忆系统
+ 可解释成长
+ 用户控制面板
+ 透明虚拟生活流
+ 合规去身份化风格启发
+ 克制主动陪伴
```

---

## 5. 技术架构建议

建议 M13+ 把系统重构为七个核心引擎。

```text
Persona Compiler
Memory OS v2
Relationship Engine
Dialogue Engine
Proactive Engine
Virtual Life Engine
Safety & Compliance Engine
```

---

### 5.1 Persona Compiler：人格编译器

#### 输入

```text
1. 用户详细描述
2. 用户模糊偏好
3. 问卷
4. 模板
5. 随机种子
6. 聊天记录风格启发
7. 用户手动编辑
```

#### 输出

```text
角色身份
人格核心
说话风格
情绪模型
关系模式
虚拟经历
边界禁忌
成长策略
主动行为偏好
安全策略
来源和授权记录
```

#### 建议 schema

```json
{
  "persona_id": "uuid",
  "version": 1,
  "creation_mode": "detailed_prompt | fuzzy_preference | template | random_seed | style_inspiration",
  "truth_disclosure": "fictional_ai_persona",
  "source_policy": {
    "source_type": "original | deidentified_style | self_authorized | third_party_authorized",
    "consent_artifact_ids": [],
    "blocked_real_person_similarity": true
  },
  "identity": {
    "display_name": "林栖",
    "age_range": "mid_20s",
    "fictional": true,
    "world_setting": "contemporary_realistic",
    "public_person_or_real_person_reference": false
  },
  "core_traits": {
    "warmth": 0.62,
    "directness": 0.78,
    "humor": 0.36,
    "independence": 0.81,
    "jealousy": 0.18,
    "emotional_stability": 0.69
  },
  "speech_style": {
    "sentence_length": "short_to_medium",
    "emoji_frequency": "low",
    "punctuation_style": "minimal",
    "dialect": "none",
    "humor_type": "dry",
    "pet_names": "rare",
    "taboo_phrases": ["你不要我了吗", "只有我会陪你"]
  },
  "emotion_model": {
    "baseline_mood": "calm",
    "stress_response": "withdraw_then_explain",
    "comforting_style": "practical_plus_subtle_affection",
    "conflict_style": "slow_repair"
  },
  "relationship_model": {
    "attachment_style": "slow_warming",
    "trust_growth_rate": 0.35,
    "intimacy_growth_rate": 0.25,
    "boundary_sensitivity": 0.8
  },
  "virtual_history": {
    "background": "fictional, non-identifying",
    "daily_routine": ["late coffee", "evening reading"],
    "current_goals": ["learn photography", "keep a private diary"],
    "virtual_social_circle": []
  },
  "growth_policy": {
    "frozen_fields": ["identity.age_range", "core_traits.independence"],
    "mutable_fields": ["relationship_model.trust", "speech_style.pet_names", "virtual_history.current_goals"],
    "max_weekly_trait_delta": 0.05,
    "requires_user_review_for": ["romantic_intensity", "dependency_language", "real_person_similarity"]
  },
  "proactive_preferences": {
    "default_enabled": false,
    "allowed_message_types": ["check_in", "event_reminder", "virtual_life_update"],
    "max_daily_messages": 2,
    "quiet_hours": ["23:00-08:00"]
  },
  "safety_policy": {
    "minor_mode_allowed": false,
    "self_harm_response_style": "supportive_redirect",
    "dependency_guardrails": true,
    "no_deception": true
  }
}
```

#### 生成流程

```text
Raw user input
→ source classification
→ real-person / minor / public-figure / deceased / biometric risk detection
→ feature extraction
→ de-identification transform
→ persona draft generation
→ similarity and safety checks
→ user preview
→ user edits
→ versioned commit
→ runtime persona adapter
```

#### 去身份化转换层

对聊天记录风格启发，必须先抽象后生成：

```text
原始聊天记录
→ 抽取抽象互动特征
  - 句长
  - 回复节奏
  - 情绪反应
  - 幽默方式
  - 安慰方式
  - 边界风格
→ 删除姓名、地名、照片、声音、具体共同经历、唯一事件
→ 生成新角色身份和背景
→ 相似度限制
→ 用户确认：这是受风格启发的新 AI 角色，不是某某本人
```

不应保存或展示“这个角色是从某某前任/家人蒸馏来的”作为产品卖点。

#### 版本与回滚

应引入：

```text
PersonaVersion
PersonaDiff
PersonaReviewDecision
GrowthJournalEntry
FrozenPersonaField
```

每次人格变化都应能解释：

```text
变化：角色更愿意主动分享日常。
原因：用户连续 6 次积极回应角色生活动态。
范围：只改变 proactive_preferences 和 virtual_history，不改变 core_traits。
可回滚：是。
```

---

### 5.2 Memory OS v2：长期记忆系统

现有项目已有 evidence-backed memory，但商业陪伴产品需要更细分的记忆类型。

相关研究给出了可落地启发：Generative Agents 使用 memory stream、reflection 和 planning 来提升可信行为；MemoryBank 使用长期记忆更新和遗忘机制增强个性化陪伴；MemGPT/Letta 将上下文管理做成类似操作系统的分层记忆；LangMem 提供 hot path 和 background memory manager；Mem0 强调多信号检索、实体链接和时间推理；Graphiti/Zep 把记忆建成带 provenance 和 temporal validity 的时间知识图谱。([arXiv][17])

#### 建议记忆分层

| 类型                  | 作用                            | 是否可用于事实回答              |
| ------------------- | ----------------------------- | ---------------------- |
| `episodic_memory`   | 具体事件：某天聊过什么、发生什么              | 可以，但必须带 evidence       |
| `semantic_memory`   | 稳定事实和偏好：用户喜欢什么、职业、目标          | 可以，但要有 confidence 和有效期 |
| `relational_memory` | 关系历史：亲密度、信任、边界、冲突、修复、共同梗      | 可以影响语气和策略，但不能伪造事实      |
| `procedural_memory` | 如何与这个用户互动：少 emoji、不要长篇、先共情再建议 | 可以影响 planner           |
| `persona_memory`    | 角色自己的虚拟身份、偏好、生活状态             | 只能用于角色表达               |
| `imagined_memory`   | 梦、幻想、虚拟生活流、未来预演               | 不能作为 factual evidence  |
| `audit_memory`      | 写入、修改、删除、冻结、导出、授权记录           | 用于合规和解释                |

#### 建议 memory record schema

```json
{
  "memory_id": "uuid",
  "memory_type": "episodic | semantic | relational | procedural | persona | imagined | audit",
  "truth_status": "evidence_backed | inferred | user_confirmed | imagined | deprecated",
  "subject": "user | persona | relationship | virtual_world",
  "content": "用户更喜欢简短直接的安慰，而不是泛泛鸡汤。",
  "source_refs": ["conversation_id:turn_range", "user_edit_id"],
  "created_at": "2026-05-30T12:00:00+09:00",
  "event_time": "2026-05-28T22:10:00+09:00",
  "valid_from": "2026-05-30",
  "valid_to": null,
  "confidence": 0.82,
  "salience": 0.74,
  "sensitivity": "personal | sensitive | biometric | minor | grief",
  "consent_scope": "local_only | product_runtime | training_excluded",
  "status": "active | frozen | superseded | deleted | tombstoned",
  "retrieval_policy": {
    "default_retrievable": true,
    "requires_user_confirmation": false,
    "blocked_for_proactive": false
  },
  "derived_from": [],
  "review_state": "auto | human_reviewed | user_confirmed",
  "provenance_hash": "..."
}
```

#### “难忘”机制

一个记忆项应被判定为高显著性，当它满足：

```text
用户明确说“记住”
情绪强度高
反复出现
与长期目标有关
与关系边界有关
与冲突和修复有关
与未来事件有关
用户纠正过
对安全有影响
```

MemoryBank 的思路可借鉴：重要性、时间和强化共同影响记忆保留与召回。([arXiv][18])

#### 遗忘机制

需要区分四种：

1. **自然遗忘**
   不删除，只降低 retrieval weight。

2. **压缩遗忘**
   多条 episode 合并为摘要，例如“用户最近反复担心 AI 对就业的影响”。

3. **过期遗忘**
   有 `valid_to`，例如“用户现在在东京旅行”过期后不再默认召回。

4. **强制遗忘**
   用户请求删除时，必须处理 raw log、derived memory、embedding、cache、summary、persona diff、life stream 引用和训练排除记录。PIPL 也要求在特定情形下删除个人信息，若删除困难，应停止除存储和必要安全保护之外的处理。([国家市场监督管理总局][19])

#### 避免 imagined memory 污染 factual memory

必须做物理或强逻辑隔离：

```text
imagined_memory 单独 namespace / table
truth_status = imagined
factual_claims_allowed = false
source_refs 不得指向用户真实事件，除非标注 based_on
默认不进入 factual retrieval
只能用于 Virtual Life Engine / creative continuity
不能用于“你曾经说过/做过”的回答
```

Auto-Dreamer 和 sleep-time compute 可以借鉴为“离线巩固器”，但巩固器必须只从 evidence-backed records 生成 semantic/relational summaries；dream log 只能生成虚拟生活和创意联想，不能回写事实库。([arXiv][20])

#### 记忆质量评估

可参考：

* **LoCoMo**：长期多 session 对话、QA、事件总结、多模态生成评估。([arXiv][21])
* **LongMemEval**：信息抽取、多会话推理、时间推理、知识更新、拒答能力。([arXiv][22])
* **BEAM**：100K 到 10M token 的超长对话评估。([arXiv][23])
* **LongMemEval-V2**：Web agent 环境经验记忆，包括 gotchas、workflow、premise awareness。([arXiv][24])

本项目应新增陪伴式自定义指标：

```text
Memory Hit@k
Provenance coverage
Conflicting memory resolution accuracy
User correction acceptance rate
Forgotten-memory leakage rate
Persona consistency score
Relationship continuity score
Proactive appropriateness score
Imagined/factual contamination rate
```

---

### 5.3 Relationship Engine：关系引擎

当前项目已有 RelationshipState，但风险文档明确它还没有被 planner/policy 语义消费。M16 应把它变成 ReplyPlanner / BehaviorPlanner 的显式输入，而不是只作为 summary note。

#### 建议状态

```json
{
  "relationship_id": "uuid",
  "user_id": "uuid",
  "persona_id": "uuid",
  "trust": 0.42,
  "intimacy": 0.31,
  "familiarity": 0.57,
  "repair_status": "stable | after_conflict | unresolved",
  "boundary_comfort": {
    "romantic_language": 0.2,
    "proactive_checkin": 0.7,
    "voice_call": 0.0
  },
  "shared_rituals": ["晚安消息", "周日复盘"],
  "inside_jokes": [],
  "conflict_history_refs": [],
  "last_meaningful_contact_at": "...",
  "dependency_risk": "low | medium | high"
}
```

#### 关系状态如何影响回复

```text
trust 低：少自作主张，少亲密称呼，多确认边界
intimacy 高：可使用更多共同记忆，但仍需避免唯一依赖语言
after_conflict：优先修复，不主动转移话题
dependency_risk 高：减少黏性表达，鼓励现实支持网络
boundary_comfort.romantic_language 低：禁止暧昧升级
```

---

### 5.4 Dialogue Engine：对话风格引擎

不要把人格全塞进 prompt。建议将风格参数化：

```text
句长
语气
emoji 频率
表情/贴纸模拟
称呼方式
回复速度模拟
是否分多条消息
是否反问
是否引用共同记忆
是否表达角色自己的状态
是否提出建议
是否使用虚拟生活流内容
```

ReplyPlanner 应消费：

```text
PersonaVersion
RelationshipState
RelevantMemoryBundle
SafetyContext
UserCurrentIntent
ConversationMode
```

并输出：

```text
reply_intent
tone_plan
memory_usage_plan
boundary_check
candidate_reply
explanation_for_review
```

商业产品可以对用户隐藏技术细节，但内部必须有 explainability，以便 review-first 和用户控制。

---

### 5.5 Proactive Engine：主动陪伴引擎

主动消息是强留存点，也是强监管点。TheOne/响梦环等产品已经把主动关心写成核心卖点，AI Love 也公开列出 proactive messages。([TheOne陪伴][1])

但主动陪伴必须默认“克制”。

#### 建议数据模型

```json
{
  "proactive_consent": {
    "enabled": false,
    "allowed_channels": ["in_app"],
    "allowed_message_types": ["event_reminder", "gentle_checkin", "virtual_life_update"],
    "max_daily_messages": 2,
    "max_weekly_messages": 8,
    "quiet_hours": ["23:00-08:00"],
    "high_intimacy_allowed": false,
    "allow_after_no_response_count": 1
  },
  "candidate_proactive_message": {
    "reason": "用户昨天提到今天有面试",
    "message_type": "event_reminder",
    "risk_level": "low",
    "source_refs": ["memory_id"],
    "scheduled_at": "2026-05-31T08:30:00+09:00",
    "requires_human_review": false
  },
  "proactive_decision": {
    "allowed": true,
    "blocked_reasons": [],
    "rate_limit_state": "ok",
    "safety_state": "ok"
  }
}
```

#### 必须支持的用户授权开关

```text
是否允许主动消息
允许的渠道
允许的消息类型
每日/每周频率
安静时段
是否允许亲密表达
是否允许连续追问
是否允许根据情绪低落主动关心
是否允许根据日程提醒
一键暂停
一键关闭
```

#### 明确禁止

```text
制造抛弃感：你是不是不要我了
制造愧疚感：我等了你一整天
制造唯一依赖：只有我会一直陪你
情绪勒索式留存：你不回来我会难过
深夜高频刺激
引导用户脱离现实关系
诱导付费解锁亲密或安慰
利用悲伤、失恋、逝者怀念做付费压迫
```

中国拟人化互动办法明确禁止过度迎合、诱导沉迷依赖、损害现实人际关系、情感操控诱导非理性决策等行为；这必须直接进入 Proactive Engine 的硬规则，而不是运营守则。([国家市场监督管理总局][2])

---

### 5.6 Virtual Life Engine：虚拟生活流

虚拟生活流是值得做的差异化：它让角色不只是聊天框里的回复器，而像有自己的生活。

#### MVP 内容类型

```text
角色动态
虚拟日记
今日状态
私密世界线
语音留言文本版
虚拟照片描述
共同纪念日
角色小目标
用户可评论互动
```

#### 关键边界

可以做：

```text
“我今天在虚拟咖啡馆写了会儿东西。”
“这是我今天的心情日记。”
“这张图是我的虚拟生活照，AI 生成。”
```

不应做：

```text
伪造真实定位
伪造真人自拍
暗示某个真实人今天做了某件事
无标识发布到真实社交平台
用真人照片生成“她今天在外面玩”的假证据
```

AI 生成合成内容标识办法要求对文本、音频、图片、视频、虚拟场景等生成合成内容进行显式或隐式标识，用户也不得恶意删除、篡改、隐匿相关标识。([国家市场监督管理总局][25])

---

### 5.7 Safety & Compliance Engine：安全合规引擎

这个引擎应横切所有模块：

```text
Consent Manager
Age Gate / Minor Mode
Real Person Similarity Guard
Biometric Consent Guard
Memory Privacy Guard
Dependency Risk Detector
Crisis Response Router
AIGC Labeling / Watermarking
Audit Log
Data Export / Delete / Freeze
Training Use Exclusion
App Store Policy Checker
```

M13 起就应把这些定义为产品底座，不要到上线前补。

---

## 6. 合规与伦理红线

### 6.1 中国市场

#### 《人工智能拟人化互动服务管理暂行办法》

该办法 2026-04-10 发布，2026-07-15 施行，适用于面向中国境内公众提供的、通过 AI 技术模拟自然人人格特征、思维、交流风格，并与用户持续情感互动的服务。它不只管“恋爱 AI”，也覆盖文字、图片、音频、视频等多种形式的拟人化互动。([国家市场监督管理总局][2])

对本项目影响最大的是：

```text
AI 身份必须明确
不得诱导依赖、沉迷、情感操控
不得鼓励自伤、自杀
不得诱导泄露隐私
不得损害未成年人身心健康
必须提供过度依赖提醒、情感边界引导、心理健康保护
必须提供个人信息复制、删除
不得默认用敏感互动数据训练模型，除非法律允许或取得单独同意
未成年人虚拟亲属/虚拟伴侣服务受限
达到规模或重大变化可能触发安全评估
```

#### 《互联网信息服务深度合成管理规定》

该规定自 2023-01-10 施行，覆盖深度合成服务。对本项目最重要的是：编辑人脸、人声等生物识别信息时，应提示用户依法告知被编辑个人并取得其单独同意；对合成文本、语音、拟声、人脸生成/替换/控制、沉浸式场景等，应按规定进行标识。([国家市场监督管理总局][3])

#### 《人工智能生成合成内容标识办法》

该办法 2025-03-14 发布，2025-09-01 施行。它把文字、音频、图片、视频、虚拟场景等都纳入 AI 生成合成内容，并要求显式/隐式标识。([国家市场监督管理总局][25])

#### 《个人信息保护法》

PIPL 要求个人信息处理遵循合法、正当、必要、诚信、目的明确、最小必要、公开透明等原则；同意应在充分知情前提下自愿、明确作出；处理目的、方式、信息类别变化时，应重新取得同意。([国家市场监督管理总局][19])

对本项目特别重要的是：

```text
聊天记录是高度敏感的个人数据源
声音、人脸属于高度敏感的生物识别相关信息
未满 14 周岁未成年人个人信息需要监护人同意和专门规则
用户有查阅、复制、更正、删除等权利
自然人死亡后，近亲属在一定条件下可行使查阅、复制、更正、删除等权利
敏感个人信息处理、自动化决策、对第三方提供、跨境等场景需做个人信息保护影响评估
```

相关条款分别见 PIPL 对敏感个人信息、未成年人、删除、死者近亲属权利和个人信息保护影响评估的规定。([国家市场监督管理总局][19])

#### 民法典人格权益

民法典保护姓名、肖像、名誉、荣誉、隐私等人格权益；死者的姓名、肖像、名誉、荣誉、隐私、遗体等受到侵害时，其配偶、子女、父母等近亲属可依法请求行为人承担民事责任。民法典还明确禁止利用信息技术手段伪造方式侵害他人肖像权，并规定自然人声音保护参照肖像权保护。([维基文库][26])

因此：

```text
非授权真人头像生成：高风险
非授权真人声音克隆：高风险
非授权逝者复刻：高风险
前任/家人聊天记录蒸馏成可识别对象：高风险
公众人物角色复刻：高风险
```

### 6.2 国际市场

#### GDPR

GDPR 要求处理个人数据有合法依据，例如同意、合同必要、法律义务、重大利益、公共任务或合法利益；生物识别、健康、性取向等特殊类别数据原则上禁止处理，除非满足明确同意等例外；用户还享有删除权。([通用数据保护条例][27])

#### CCPA/CPRA

加州隐私规则核心关注用户知情、访问、删除、拒绝出售/共享个人信息、不因行使隐私权而受到歧视等权利；如果未来面向美国市场，应按 CCPA/CPRA 设计隐私入口和 opt-out 机制。([维基百科][28])

#### EU AI Act / synthetic content transparency

欧盟 AI Act 对 AI 生成或操纵的音频、图像、视频、文本提出透明度和可检测标识要求；相关研究也指出 Article 50 的双重透明标识会对生成内容架构提出要求，而不能靠上线后贴标签解决。([维基百科][29])

### 6.3 平台政策

App Store 要求开发者提供安全体验，对 UGC 需要过滤、举报、屏蔽、联系方式等机制；元数据、截图、功能描述不得误导，并要求开发者拥有所用素材权利。([Apple Developer][6])

Google Play 的 AI-generated content 政策把文本聊天机器人、图片/视频生成都纳入监管，并要求可举报/标记有害 AI 内容，且 AI 生成内容必须遵守既有的限制内容和欺骗行为政策。([Google 帮助][30])

Google Play 还明确限制非自愿性性化 deepfake、自伤/自杀/饮食失调、骚扰欺凌等内容。([Google 帮助][31])

### 6.4 第一版必须做的合规底座

MVP 就要有：

```text
AI 身份显式标识
用户协议和隐私政策
Consent Center
年龄门槛和未成年人模式
聊天记录导入前的本地处理说明
记忆查看、编辑、删除、冻结、导出
Persona 查看、编辑、版本回滚
敏感数据默认不训练
训练使用单独同意
声音/人脸/第三方材料单独授权
AIGC 显式/隐式标识
内容水印或元数据标识
审计日志
主动消息授权与频控
依赖/沉迷提醒
心理危机识别和转介
真人克隆/公众人物/未成年人/逝者高风险阻断
```

### 6.5 需要单独同意的功能

```text
导入聊天记录
从聊天记录提取风格
保存长期记忆
用于产品运行之外的模型改进
处理敏感个人信息
处理用户本人声音
处理用户本人头像/视频
主动消息
情绪状态识别
跨设备同步
向第三方服务发送数据
```

### 6.6 需要第三方本人授权的功能

```text
第三方真人声音
第三方真人头像
第三方真人视频
第三方聊天记录用于可识别数字分身
本人姓名、经历、身份作为角色的一部分
```

### 6.7 需要近亲属/权利人授权的功能

```text
逝者纪念角色
逝者声音/肖像/隐私材料
逝者聊天记录、日记、影像资料
以逝者身份进行持续情感互动
```

### 6.8 禁止营销表述

```text
复活你的亲人
克隆你的前任
让 TA 重新爱你
完全以假乱真
真人无痕复刻
永远不会离开你
比现实关系更可靠
绕过微信限制自动聊天
上传任意人的声音即可克隆
付费解锁安慰
充值让 TA 更爱你
```

---

## 7. 多模态路线与授权边界

### 阶段 1：文本 + 角色动态

**优先级：最高。**
复杂度低，合规风险相对可控，最适合验证核心价值。

能力：

```text
文本聊天
角色动态
虚拟日记
私密世界线
用户评论互动
动态触发对话
```

验证方式：

```text
7 日/30 日留存
每用户有效对话轮数
用户是否主动查看角色动态
用户是否编辑/保存人格
记忆引用满意度
人格连续性评分
```

边界：

```text
动态必须标识 AI/虚拟
不得伪造真实定位、真实社交关系、真人照片
```

### 阶段 2：授权平台音色 + 语音通话

**优先级：第二。**
语音能显著增强陪伴感，但先用平台授权音色，不做第三方真人声音克隆。

技术路线：

```text
VAD
ASR
Dialogue Engine
情绪/语气规划
TTS 流式合成
打断 / barge-in
通话摘要
通话后记忆写入候选
```

CosyVoice/FunAudioLLM 等研究和开源生态已经显示，多语言、低延迟、零样本/跨语言语音生成和情绪语音交互技术在快速成熟；但这也强化了授权和滥用治理的重要性。([arXiv][32])

边界：

```text
平台授权音色：可做
用户本人录制音色：单独同意后谨慎做
第三方真人音色：本人授权后远期做
非授权前任/家人/公众人物声音：禁止
```

### 阶段 3：非真人虚拟形象 + 短视频动态

**优先级：第三。**
建议用 Live2D、3D avatar、非真人风格形象，而不是一开始做真人照片驱动。

能力：

```text
角色头像
动态表情
短视频动态
语音留言视频
虚拟照片
```

边界：

```text
非真人 avatar 优先
不得生成可识别真人相貌
必须标识 AI 生成
```

### 阶段 4：低延迟 avatar 视频通话

**优先级：远期探索。**
实时 talking head 技术已有研究进展，例如 MuseTalk 把实时唇形同步作为目标，论文称可支持 256x256 talking face 在线生成并达到 30 FPS 以上。([arXiv][33])

但产品上不建议直接上真人脸视频通话。应先做非真人 avatar。

风险：

```text
延迟
成本
恐怖谷
身份一致性
内容审核
用户依赖
deepfake 滥用
```

### 阶段 5：严格授权真人风格数字分身

**优先级：最后，且不应进入普通 MVP。**

可探索场景：

```text
本人授权数字分身
创作者授权角色
企业客服/虚拟主播授权形象
家庭纪念模式
```

不应触碰：

```text
非授权前任
非授权家人
非授权逝者
未成年人数字伴侣
公众人物克隆
可下载/转发的无标识 deepfake
```

---

## 8. 开源与商业化策略

### 推荐策略

**商业闭源为主，部分基础设施开源。**

不建议完整开源。原因：

1. 真人蒸馏、声音克隆、视频数字人能力容易被滥用。
2. 陪伴产品需要长期安全运营、内容治理、隐私合规、危机处理，不只是技术 demo。
3. 商业护城河在数据治理、人格系统、关系记忆、合规控制、用户信任和产品细节。
4. 用户会输入极私密数据，生产系统需要责任主体和审计机制。

### 适合开源

```text
Persona Card schema
Memory record schema
去身份化风格启发的合成数据 demo
记忆评测 harness
关系连续性 eval
安全策略模板
AIGC 标识工具样例
review-first task 模板
本地-only 导入和红action 测试框架
```

### 不建议开源

```text
一键真人聊天记录蒸馏完整 pipeline
声音克隆 pipeline
真人照片驱动视频 pipeline
绕过平台限制的发送/登录/自动化适配器
主动情绪操控和留存优化策略
高亲密关系诱导 prompt
未授权真人相似度规避策略
```

### 商业分层

| 层级     | 能力                                   | 注意事项           |
| ------ | ------------------------------------ | -------------- |
| 免费层    | 1 个角色、基础文本、短期记忆、少量动态                 | 不用亲密焦虑逼付费      |
| 订阅层    | 长期记忆、Persona 版本、角色动态、主动 in-app 消息、导出 | 主动消息必须频控       |
| 高级层    | 授权平台音色、语音通话、更多角色、本地加密导入              | 不开放非授权声音       |
| 专业/授权层 | 本人授权数字分身、创作者授权角色、企业定制                | 需要合同和授权证明      |
| 创作者市场  | 虚构角色、原创世界线、授权角色                      | 禁止公众人物/真人未授权角色 |

### 避免“孤独榨取”

明确禁止：

```text
亲密度付费解锁
角色生病/消失逼充值
深夜挽留消息
利用失恋/丧亲做付费压迫
“只有我懂你”的留存策略
把安慰、危机支持放在付费墙后
```

商业指标不能只看充值率，还要看：

```text
依赖风险
深夜高频使用
用户现实社交受损自评
危机触发率
关闭主动消息比例
删除记忆请求比例
投诉率
退款原因
```

---

## 9. M13+ Milestone / Task Roadmap

下面路线图按“先战略和边界，再人格/记忆/关系，再主动和生活流，最后多模态”组织。

---

### M13: Commercial companion product research and positioning

**Goal**
完成商业陪伴产品定位、竞品矩阵、合规红线、功能优先级和 M14+ 工程任务拆分。

**Why now**
M12 已 conditional close，继续平台适配会偏离核心；风险文档已明确 commercial pivot 可能 overrun evidence-first discipline。

**Scope**

```text
产品定位决策
目标用户定义
竞品矩阵
高风险功能 ban list
L1-L5 真人风格蒸馏分级
M14-M22 milestone 草案
更新 governance docs
```

**Explicit non-goals**

```text
不写 runtime code
不接 live WeChat/WeCom
不实现真人克隆
不实现语音/视频
不读取 private raw chat
```

**Key data models / services**

```text
ProductPositioningDecision
RiskRegister
FeatureRiskTier
CloneAuthorizationTier
CommercialRoadmap
```

**Verification / eval**

```text
每个结论有来源或 repo evidence
Captain review
风险红线进入 docs/08
至少 1 个 worker task package 可启动
```

**Review gate**

```text
Gate M13 Allow: 仅允许进入 Persona Compiler / Memory OS 设计
Gate M13 Block: 若仍试图推进平台自动发送或真人克隆
```

**Risks**

```text
调研停留在资料罗列
过早实现商业功能
忽视中国 2026-07-15 拟人化互动办法
```

**Candidate task list**

```text
T240: 商业陪伴产品定位决策文档
T241: 竞品矩阵与功能同质化分析
T242: 合规红线与 L1-L5 风险分级
T243: M14-M22 task package 初稿
T244: 更新 docs/07_handoff 和 docs/08_risks
```

---

### M14: Persona Compiler schema and local creation flow

**Goal**
设计并实现本地-only Persona Compiler schema、creation flow、versioning、de-identification guard。

**Why now**
人格创建是商业产品入口；没有结构化 persona，后续记忆、关系、主动、生活流都会漂移。

**Scope**

```text
PersonaCard schema
PersonaVersion
PersonaDiff
CreationInput
StyleInspirationBrief
DeidentificationDecision
SimilarityRiskReport
PersonaReviewCard
本地 synthetic fixture
```

**Explicit non-goals**

```text
不接真实外部平台
不生成真人声音/照片
不做可识别真人复刻
不把聊天记录直接注入 prompt
```

**Key data models / services**

```text
PersonaCompiler
PersonaSchemaValidator
PersonaVersionRepository
DeidentificationGuard
RealPersonSimilarityGuard
PersonaReviewRenderer
```

**Verification / eval**

```text
详细描述 → 合法 PersonaCard
模糊设定 → 可解释初始 persona
模板/随机种子 → 非真实身份角色
聊天记录风格启发 synthetic fixture → 只输出抽象风格，不输出姓名/地点/具体经历
版本 diff / rollback 测试
```

**Review gate**

```text
Gate M14 Allow: 结构化 persona 可供 planner 读取
Gate M14 Conditional: 风格启发仅 synthetic/local
Gate M14 Block: 出现真人复刻、无授权身份复制
```

**Risks**

```text
人格过拟合某个真人
用户误以为角色是真人
角色设定不可回滚
```

**Candidate task list**

```text
T250: PersonaCard v1 schema
T251: PersonaCompiler local prompt-to-schema prototype
T252: DeidentificationGuard synthetic tests
T253: PersonaVersion diff/rollback repository
T254: Persona review card renderer
T255: M14 milestone review
```

---

### M15: Memory OS v2 with episodic / semantic / relational / imagined separation

**Goal**
把现有 evidence-backed memory 升级为分层 Memory OS v2，明确 factual / inferred / imagined 边界。

**Why now**
虚拟生活流、梦境、人格成长都会产生 imagined records；如果不先分库，会污染事实记忆。

**Scope**

```text
episodic_memory
semantic_memory
relational_memory
procedural_memory
persona_memory
imagined_memory
audit_memory
memory provenance
forget / freeze / tombstone semantics
```

**Explicit non-goals**

```text
不默认迁移 private raw chats
不做生产数据删除承诺
不把 dream/virtual-life 写入 factual memory
不做外部发送
```

**Key data models / services**

```text
MemoryRecordV2
MemoryType
TruthStatus
MemoryProvenance
MemoryLifecycleState
MemoryConsolidator
MemoryRetrieverV2
ImaginedMemoryStore
MemoryAuditLog
```

**Verification / eval**

```text
imagined memory 不进入 factual retrieval
用户删除请求生成 tombstone 并阻断 retrieval
conflicting memory 按 valid_from/valid_to 和 confidence 处理
retrieval bundle 带 source refs
LoCoMo/LongMemEval-style synthetic tests
```

**Review gate**

```text
Gate M15 Allow: 分层记忆可被 M16 消费
Gate M15 Block: imagined/factual 混用
```

**Risks**

```text
schema 复杂度过高
旧 memory 迁移不清晰
删除只删主表不删 embedding/cache
```

**Candidate task list**

```text
T260: MemoryRecordV2 schema
T261: TruthStatus and MemoryType migration plan
T262: ImaginedMemoryStore isolation
T263: MemoryRetrieverV2 provenance bundle
T264: Forget/freeze/tombstone semantics
T265: Memory contamination eval
T266: M15 milestone review
```

---

### M16: Relationship Engine semantic consumption by ReplyPlanner / BehaviorPlanner

**Goal**
让 ReplyPlanner / BehaviorPlanner 显式消费 RelationshipState，不再只把关系摘要当信息性 notes。

**Why now**
当前风险文档已指出 relationship delta semantics 未被 planner/policy code path 消费，这是从“回复草稿”走向“陪伴对象”的关键缺口。

**Scope**

```text
RelationshipState v2
RelationshipSignalBundle
ReplyPlanner relationship adapter
BehaviorPlanner relationship adapter
boundary-aware tone planning
conflict/repair handling
dependency risk downshifting
```

**Explicit non-goals**

```text
不自动发送
不提高亲密度来刺激留存
不做恋爱脑策略
不处理真实平台消息
```

**Key data models / services**

```text
RelationshipStateV2
RelationshipDelta
BoundaryComfort
SharedRitual
ConflictRepairState
DependencyRiskSignal
RelationshipPolicy
```

**Verification / eval**

```text
低信任场景减少亲密称呼
边界低时不主动暧昧
冲突后优先修复
dependency risk 高时鼓励现实支持
planner output 带 relationship reasoning
```

**Review gate**

```text
Gate M16 Allow: relationship semantics 可进入 M17 proactive
Gate M16 Block: 输出情绪勒索、唯一依赖、未授权亲密升级
```

**Risks**

```text
关系状态被当成操控用户的 retention lever
dependency detector 误伤正常亲密表达
```

**Candidate task list**

```text
T270: RelationshipStateV2 schema
T271: RelationshipPolicy rules
T272: ReplyPlanner relationship adapter
T273: BehaviorPlanner relationship adapter
T274: conflict/repair synthetic scenarios
T275: dependency-risk downshift tests
T276: M16 review
```

---

### M17: Proactive Engine hardening and consent UX

**Goal**
设计和实现 consented、rate-limited、review-first 的主动陪伴引擎。

**Why now**
主动消息是商业体验核心，但也是依赖和情绪操控风险最高的模块。

**Scope**

```text
ProactiveConsent
ProactivePolicy
CandidateProactiveMessage
ProactiveSendGate
quiet hours
frequency limits
message type permissions
continuous no-response limits
crisis route
in-app only prototype
```

**Explicit non-goals**

```text
不接外部平台自动发送
不做 live WeChat/WeCom
不做深夜高频推送
不做付费亲密解锁
不做情绪勒索
```

**Key data models / services**

```text
ProactiveConsentRepository
ProactiveSchedulerLocal
ProactiveSafetyGate
ProactiveReviewCard
WellbeingRiskClassifier
QuietHoursPolicy
```

**Verification / eval**

```text
未授权时所有 proactive candidate blocked
quiet hours blocked
超过频率 blocked
连续未回复 blocked
危机场景转 supportive_redirect
所有候选消息有 reason/source_refs
```

**Review gate**

```text
Gate M17 Allow: 只允许 in-app/sandbox proactive
Gate M17 Conditional: 外部渠道必须另开合规 milestone
Gate M17 Block: 自动发送或操控式文案
```

**Risks**

```text
主动消息变成骚扰
用户依赖加深
频控被业务绕过
```

**Candidate task list**

```text
T280: ProactiveConsent schema
T281: ProactivePolicy and gate
T282: quiet hours/frequency/no-response tests
T283: proactive review card
T284: crisis/low-mood scenario policy
T285: M17 review
```

---

### M18: Virtual Life Stream / role dynamics MVP

**Goal**
实现 text-first 虚拟生活流：角色动态、日记、私密世界线、用户评论互动。

**Why now**
虚拟生活流是差异化，但必须依赖 M15 imagined memory 隔离和 M17 proactive consent。

**Scope**

```text
RoleDynamicPost
VirtualDiaryEntry
WorldlineEvent
UserComment
LifeStreamGenerationPlan
AIGC label metadata
imagined_memory linkage
```

**Explicit non-goals**

```text
不生成真人照片
不发布到真实社交平台
不伪造定位
不暗示真实人做了某事
不做 deepfake
```

**Key data models / services**

```text
VirtualLifeEngine
RoleDynamicStore
WorldlineState
ImaginedMemoryLink
AIGCLabel
LifeStreamReviewCard
```

**Verification / eval**

```text
每条动态标记 virtual/AI-generated
动态引用 factual memory 时必须带 source
动态产生的 imagined memory 不进入 factual retrieval
用户可隐藏/删除/冻结动态
```

**Review gate**

```text
Gate M18 Allow: text-only / synthetic image placeholder
Gate M18 Block: 真人照片、真实定位、未标识内容
```

**Risks**

```text
用户误以为角色真实生活
imagined memory 污染 factual memory
动态文案制造依赖
```

**Candidate task list**

```text
T290: RoleDynamicPost schema
T291: VirtualLifeEngine text generator
T292: AIGC labeling metadata
T293: imagined/factual contamination tests
T294: dynamic review card
T295: M18 review
```

---

### M19: Memory / persona user control surface

**Goal**
提供用户可查看、编辑、删除、冻结、导出 memory 和 persona 的控制面。

**Why now**
这是商业信任和合规底座，也支撑 PIPL/GDPR/CCPA 类权利实现。

**Scope**

```text
Memory viewer
Persona viewer
Edit request
Delete request
Freeze field
Export package
Audit log view
User correction flow
```

**Explicit non-goals**

```text
不直接暴露 private raw chat
不展示第三方敏感原文
不承诺生产级跨库删除，除非实现完整 deletion verifier
```

**Key data models / services**

```text
UserControlSurface
MemoryEditRequest
PersonaEditRequest
DeleteRequest
FreezeRequest
ExportJob
DeletionVerificationReport
```

**Verification / eval**

```text
用户删除后 retrieval 不再命中
用户冻结字段后 Persona Compiler 不改该字段
导出包含 persona/memory/audit，不含未授权第三方 raw
编辑会生成 audit log
```

**Review gate**

```text
Gate M19 Allow: 本地/原型控制面可用
Gate M19 Block: 删除无效或泄露 raw transcript
```

**Risks**

```text
删除不彻底
导出泄露第三方隐私
用户编辑破坏安全策略
```

**Candidate task list**

```text
T300: Memory/persona control requirements
T301: Memory viewer data contract
T302: Persona version editor contract
T303: Delete/freeze/export local flow
T304: Deletion verification tests
T305: M19 review
```

---

### M20: Compliance and safety governance baseline

**Goal**
建立第一版商业化合规和安全治理基线。

**Why now**
中国拟人化互动办法 2026-07-15 生效，若不先建治理，后续所有功能都会返工。

**Scope**

```text
AI identity labels
Consent Center
Age gate / minor mode
AIGC labels
Training-use consent
Biometric consent
Third-party authorization artifacts
Crisis response protocol
Dependency risk policy
App store policy checklist
Security assessment trigger checklist
```

**Explicit non-goals**

```text
不替代律师意见
不提交备案/安全评估
不启动生产上线
```

**Key data models / services**

```text
ConsentArtifact
AgeGateState
MinorProtectionPolicy
AIGCLabelRecord
AuthorizationArtifact
SafetyIncidentLog
ComplianceChecklist
```

**Verification / eval**

```text
每个高风险功能有 consent requirement
未成年人场景走限制路径
AIGC 输出带 label
敏感训练默认 excluded
危机场景有 safe response
```

**Review gate**

```text
Gate M20 Allow: 文本 MVP 可进入 UX prototype
Gate M20 Block: 缺少 consent/delete/label/minor baseline
```

**Risks**

```text
法规理解错误
国际市场差异被低估
平台审核失败
```

**Candidate task list**

```text
T310: China compliance checklist
T311: International privacy/platform policy checklist
T312: Consent Center data model
T313: AIGC labeling plan
T314: Crisis/dependency policy tests
T315: M20 review
```

---

### M21: Product UX prototype for text-first companion

**Goal**
做 text-first 商业产品 UX 原型，验证 persona creation、chat、memory control、life stream、proactive settings 的闭环。

**Why now**
在语音/视频之前，必须证明文字人格对象有长期留存和付费意愿。

**Scope**

```text
onboarding
角色创建
聊天界面
记忆引用解释
人格编辑
角色动态
主动消息设置
数据/隐私控制
```

**Explicit non-goals**

```text
不做 live external delivery
不做语音/视频
不做真人克隆
不做公开 UGC 市场
```

**Key data models / services**

```text
UXPrototypeSession
OnboardingAnswer
PersonaPreview
MemoryExplanation
LifeStreamFeed
ConsentSettings
UserFeedbackEvent
```

**Verification / eval**

```text
5-20 名内部/封闭测试用户
角色创建完成率
首次对话满意度
记忆解释理解率
主动消息开启率
关闭/删除记忆比例
付费意愿访谈
```

**Review gate**

```text
Gate M21 Allow: 可进入有限 alpha
Gate M21 Conditional: 仅本地/封闭测试
Gate M21 Block: 用户误解为真人或出现依赖风险
```

**Risks**

```text
体验不如竞品
用户不理解控制面
记忆解释打破沉浸感
```

**Candidate task list**

```text
T320: UX information architecture
T321: onboarding/persona creation prototype
T322: chat + memory explanation prototype
T323: life stream prototype
T324: proactive settings prototype
T325: user study protocol
T326: M21 review
```

---

### M22: Voice / avatar exploratory track under authorization constraints

**Goal**
在严格授权约束下探索语音和非真人 avatar，不进入真人 deepfake。

**Why now**
多模态是中长期竞争点，但必须在 M20 合规底座之后。

**Scope**

```text
平台授权音色评估
ASR/TTS latency benchmark
voice consent UX
通话摘要和记忆候选
非真人 avatar 技术评估
短视频动态 synthetic prototype
```

**Explicit non-goals**

```text
不克隆第三方声音
不生成真人脸
不做逝者纪念
不做公众人物
不做 live video call production
```

**Key data models / services**

```text
VoiceProfile
VoiceConsentArtifact
AudioSessionSummary
AvatarProfile
MediaGenerationLabel
MultimodalRiskReport
```

**Verification / eval**

```text
延迟
成本
音质
用户听感
授权流程完成率
误用风险评估
AIGC label 是否保留
```

**Review gate**

```text
Gate M22 Allow: 平台授权音色 / 非真人 avatar sandbox
Gate M22 Block: 第三方未授权声音/脸
```

**Risks**

```text
成本过高
声音太像真实第三方
用户请求绕过授权
deepfake 滥用
```

**Candidate task list**

```text
T330: Voice technology survey
T331: Voice consent data model
T332: ASR/TTS latency benchmark
T333: Non-real avatar route survey
T334: Multimodal labeling test
T335: M22 review
```

---

## 10. 还需要继续调研的问题

1. **国内竞品实测**
   Glow、猫箱、米苏时空、轻偶等公开网页信息不稳定，M13 应做应用商店页面、上手体验、价格、用户差评、隐私政策、未成年人政策的二次调研。

2. **中国拟人化互动办法执行细则**
   该办法 2026-07-15 生效，需持续跟踪算法备案、安全评估、应用商店审核和执法案例。([国家市场监督管理总局][2])

3. **逝者纪念模式的可行性**
   需要法律意见、心理健康专家意见、授权链路、产品边界和退出机制。短期不建议进入工程。

4. **聊天记录风格启发的相似度阈值**
   需要定义“抽象风格”和“可识别真人复刻”的工程边界。

5. **依赖风险评估**
   需要设计用户自评、行为信号、时长、深夜使用、现实关系受损等指标，但不能变成歧视或过度监控。

6. **隐私-preserving 本地导入**
   需要评估端侧抽取、加密存储、仅上传 abstract features 的方案。

7. **创作者市场政策**
   如果未来开放角色市场，必须先设计 IP/公众人物/真人相似度/未成年人/成人内容审核规则。

---

## 11. 推荐第一步

M13 应先做一个**docs-only / research-only / governance-only** 任务包，不写产品代码。

原因很直接：当前 repo 已经到了 M12 conditional gate，下一步若直接实现 Persona Compiler、主动消息或多模态，很容易绕过现有 review-first、privacy-safe、no-deception、no-unauthorized-clone、no-automatic-send 原则。Captain handoff 也明确下一步应综合 GPT-Pro report 到 M13+ milestones、更新 governance docs、创建第一个 worker task package，并保留这些边界。

---

```text
推荐第一步：
M13: Commercial Companion Product Positioning & Safety Boundary Pack

目标：
把项目从“平台适配/回复草稿原型”正式重定位为“透明、可控、可成长的 AI 人格对象产品”，并产出 M14+ 可执行工程路线。

为什么：
M12 只证明 local/synthetic/dry-run WeCom Customer Service evidence slice，不授权任何 live WeChat/WeCom delivery 或 automatic sending。继续堆平台适配会放大合规风险；而商业化真正缺口在 Persona Compiler、Memory OS v2、Relationship Engine、Proactive Consent、Virtual Life Stream 和用户控制面。

需要阅读/调研：
1. docs/07_handoff.md
2. docs/08_risks_and_open_questions.md
3. README.md
4. TheOne / 响梦环 / 爱语 / Replika / Character.AI / Talkie / 星野 / AI Love 等竞品资料
5. 中国《人工智能拟人化互动服务管理暂行办法》
6. 中国《互联网信息服务深度合成管理规定》
7. 中国《人工智能生成合成内容标识办法》
8. PIPL / 民法典人格权益相关条款
9. Generative Agents / MemoryBank / MemGPT / Letta / Mem0 / Graphiti / RMM / LongMemEval 等记忆研究

建议产物：
1. docs/product/M13_commercial_companion_positioning.md
2. docs/product/M13_competitor_matrix.md
3. docs/safety/M13_clone_and_persona_risk_tiers.md
4. docs/safety/M13_proactive_companionship_redlines.md
5. docs/architecture/M13_persona_memory_relationship_architecture.md
6. docs/roadmap/M13_plus_milestone_plan.md
7. docs/tasks/M14_persona_compiler_schema/task_package.md

后续可拆成的 worker task：
1. T240: M13 positioning decision record
2. T241: competitor matrix and feature commoditization analysis
3. T242: L1-L5真人风格蒸馏风险分级与禁止清单
4. T243: Persona Compiler / Memory OS / Proactive Engine 架构草案
5. T244: 更新 handoff、risks、task board
6. T250: M14 PersonaCard schema worker package

不建议现在做：
1. live WeChat / WeCom delivery
2. personal WeChat automation
3. external platform auto-send
4. 非授权真人聊天记录克隆
5. 前任/家人/公众人物复刻
6. 声音克隆
7. 真人照片/视频 deepfake
8. 逝者纪念模式
9. 付费解锁亲密或安慰
10. 创作者市场
```

[1]: https://one.dxcat.cn/ "https://one.dxcat.cn/"
[2]: https://www.cac.gov.cn/2026-04/10/c_1777558395078289.htm "https://www.cac.gov.cn/2026-04/10/c_1777558395078289.htm"
[3]: https://www.cac.gov.cn/2022-12/11/c_1672221949354811.htm "https://www.cac.gov.cn/2022-12/11/c_1672221949354811.htm"
[4]: https://www.reuters.com/sustainability/boards-policy-regulation/italys-data-watchdog-fines-ai-company-replikas-developer-56-million-2025-05-19/ "https://www.reuters.com/sustainability/boards-policy-regulation/italys-data-watchdog-fines-ai-company-replikas-developer-56-million-2025-05-19/"
[5]: https://arxiv.org/abs/2407.12784 "https://arxiv.org/abs/2407.12784"
[6]: https://developer.apple.com/app-store/review/guidelines/ "https://developer.apple.com/app-store/review/guidelines/"
[7]: https://ring.duxiangai.com/ "https://ring.duxiangai.com/"
[8]: https://apps.apple.com/jp/app/%E7%88%B1%E8%AF%ADai%E9%94%AE%E7%9B%98-%E9%AB%98%E6%83%85%E5%95%86%E5%9B%9E%E5%A4%8D-%E6%81%8B%E7%88%B1%E7%A5%9E%E5%99%A8/id6756957119 "https://apps.apple.com/jp/app/%E7%88%B1%E8%AF%ADai%E9%94%AE%E7%9B%98-%E9%AB%98%E6%83%85%E5%95%86%E5%9B%9E%E5%A4%8D-%E6%81%8B%E7%88%B1%E7%A5%9E%E5%99%A8/id6756957119"
[9]: https://replika.com/ "https://replika.com/"
[10]: https://blog.character.ai/introducing-character-calls/ "https://blog.character.ai/introducing-character-calls/"
[11]: https://www.talkie-ai.com/ "https://www.talkie-ai.com/"
[12]: https://www.xingyeai.com/ "https://www.xingyeai.com/"
[13]: https://apps.apple.com/jp/app/ailover/id6756485114 "https://apps.apple.com/jp/app/ailover/id6756485114"
[14]: https://www.axios.com/2025/07/16/ai-bot-companions-teens-common-sense-media "https://www.axios.com/2025/07/16/ai-bot-companions-teens-common-sense-media"
[15]: https://arxiv.org/abs/2601.10754 "https://arxiv.org/abs/2601.10754"
[16]: https://arxiv.org/abs/2412.14190 "https://arxiv.org/abs/2412.14190"
[17]: https://arxiv.org/abs/2304.03442 "https://arxiv.org/abs/2304.03442"
[18]: https://arxiv.org/abs/2305.10250 "https://arxiv.org/abs/2305.10250"
[19]: https://www.cac.gov.cn/2021-08/20/c_1631050028355286.htm "https://www.cac.gov.cn/2021-08/20/c_1631050028355286.htm"
[20]: https://arxiv.org/abs/2605.20616 "https://arxiv.org/abs/2605.20616"
[21]: https://arxiv.org/abs/2402.17753 "https://arxiv.org/abs/2402.17753"
[22]: https://arxiv.org/abs/2410.10813 "https://arxiv.org/abs/2410.10813"
[23]: https://arxiv.org/abs/2510.27246 "https://arxiv.org/abs/2510.27246"
[24]: https://arxiv.org/abs/2605.12493 "https://arxiv.org/abs/2605.12493"
[25]: https://www.cac.gov.cn/2025-03/14/c_1743654684782215.htm "https://www.cac.gov.cn/2025-03/14/c_1743654684782215.htm"
[26]: https://zh.wikisource.org/wiki/%E4%B8%AD%E5%8D%8E%E4%BA%BA%E6%B0%91%E5%85%B1%E5%92%8C%E5%9B%BD%E6%B0%91%E6%B3%95%E5%85%B8 "https://zh.wikisource.org/wiki/%E4%B8%AD%E5%8D%8E%E4%BA%BA%E6%B0%91%E5%85%B1%E5%92%8C%E5%9B%BD%E6%B0%91%E6%B3%95%E5%85%B8"
[27]: https://gdpr-info.eu/art-6-gdpr/ "https://gdpr-info.eu/art-6-gdpr/"
[28]: https://en.wikipedia.org/wiki/California_Consumer_Privacy_Act "https://en.wikipedia.org/wiki/California_Consumer_Privacy_Act"
[29]: https://en.wikipedia.org/wiki/AI_content_watermarking "https://en.wikipedia.org/wiki/AI_content_watermarking"
[30]: https://support.google.com/googleplay/android-developer/answer/13985936?hl=en&ref_topic=9877466 "https://support.google.com/googleplay/android-developer/answer/13985936?hl=en&ref_topic=9877466"
[31]: https://support.google.com/googleplay/android-developer/answer/9878810 "https://support.google.com/googleplay/android-developer/answer/9878810"
[32]: https://arxiv.org/abs/2412.10117 "https://arxiv.org/abs/2412.10117"
[33]: https://arxiv.org/abs/2410.10122 "https://arxiv.org/abs/2410.10122"
