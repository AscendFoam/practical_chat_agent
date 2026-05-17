我仔细读完报告后，整体判断是：

**报告的战略方向大体正确，但执行顺序需要明显收敛。**
它提出的 ContactSkill 解耦、RelationshipState、多级记忆、BehaviorPlanner、飞书优先、Mem0 可选复用等方向都很有价值；但如果现在直接“废除 ContactSkill、接 Mem0、接飞书 WebSocket、上 SQLite/Web UI”，会和你当前项目的阶段约束冲突，也会破坏你已经做好的 evidence-first / human-review-first 管线。

当前更科学的路线应该是：

> **先把现有 review-only 回复规划闭环打硬，再做兼容式解耦；先沉淀反馈数据，再升级生成质量；先做本地/离线行为草稿，再接平台。**

你的仓库当前 M3 已明确是 `Conditional`：ReplyPlan / ReplyPlanner / policy layer 的结构已经完成，但 naturalness 和 evidence usage 都只有 3/5，且还没有 committed regression tests，因此不能把它当成成熟的关系感知回复系统。
T140 的任务也已经规定得很清楚：只记录反馈，不调用 LLM、不自动发送、不接实时平台、不自动修改 ContactSkill/Memory/approved store/planner templates。
报告中关于“避免大型 agent framework、保留人类审查、谨慎引入 Mem0/Letta/微信 Hook”的结论我基本同意。

下面是我建议你接下来真正采用的开发计划。

---

# Practical Chat Agent 后续开发计划 v2

## 0. 总体原则

后续开发不要从“功能完整体”出发，而要从“可验证闭环”出发。

你的项目核心不是：

```text
能接微信 / 能接飞书 / 能主动聊天 / 能像真人
```

而是：

```text
长期关系信息
→ 可审查记忆
→ 安全候选回复
→ 人类反馈
→ 可审查策略修正
→ 更自然、更懂边界的陪伴式回复
```

因此后续所有功能都应该服从四条原则：

1. **Review-only 继续作为默认模式**
   自动发送、主动联系、记忆自动修改都必须晚于反馈闭环、测试集和 send gate。

2. **不要破坏现有 ContactSkill**
   报告建议“废除 ContactSkill”过于激进。正确做法是：保留 ContactSkill 作为当前兼容层，在其上逐步派生 PartnerPersona、CommunicationPolicy、RelationshipState。

3. **先自研抽象，再可选接 Mem0 / Zep / 外部 memory**
   现在不应该直接引入 Mem0。先定义 `MemoryRetriever` 接口和本地实现，等有评估集后再判断是否接第三方。

4. **平台接入晚于 OutboundSendGate**
   飞书确实比微信更适合沙箱测试，但也不应该现在接。至少要先有 feedback log、regression tests、send gate。

---

# 1. 推荐的新里程碑顺序

我建议从现在开始按以下里程碑推进：

```text
M4  Feedback Capture：只记录反馈，不应用反馈
M4.5 Regression Hardening：补 committed tests，固定安全边界
M5  Feedback-to-Patch：把反馈变成可审查策略补丁
M6  ContactSkill Compatible Decomposition：兼容式拆分 ContactSkill
M7  LLM-assisted ReplyPlanner：提升自然度，但仍 review-only
M8  RelationshipState：多维关系状态，先离线候选更新
M9  Memory Retrieval Layer：抽象检索层，可选接 Mem0
M10 BehaviorPlanner：主动行为草稿，不自动发送
M11 OutboundSendGate + Feishu Sandbox：受控平台接入
M12 WeChat Adapter：仅作为可选薄适配层
```

这个顺序比报告里“先重构 ContactSkill + 先接飞书 + 先上三级记忆”的路线更稳，因为它不会中断你当前的 T140/T150 任务链。

---

# 2. M4：Feedback Capture

## 目标

完成当前 T140，但要为后续 patch / relationship / quality eval 留足字段。

T140 不应该只是“记录 accept/edit/reject/boundary”，还应该在 schema 上预留后续分析空间。

## 建议任务

### T140：Feedback Schema CLI

保持当前任务范围不变。

新增模型建议：

```python
ReplyFeedbackAction = Literal[
    "accept",
    "edit",
    "reject",
    "boundary",
    "skip",
    "prefer_other"
]
```

`ReplyFeedbackRecord` 建议字段：

```text
feedback_id
created_at
contact_id
reply_plan_id
source_plan_path
candidate_id
priority_rank
candidate_type
action
user_note
edited_text
edit_summary
boundary_label
boundary_note
reason_tags
source_context_refs
policy_risk_flags_snapshot
created_by
```

其中 `edited_text` 和 `user_note` 只能写入 `private/`，stdout 不输出全文。

### T141：Feedback Log Validator

新增只读校验器：

```bash
chat-feedback-validate --input private/feedback/xxx.jsonl
```

校验：

```text
candidate 是否存在
action 是否合法
edit 是否有 edited_text 或 diff ref
boundary 是否有 boundary_label / note
source plan path 是否仍可读
是否存在泄露到 docs/examples/tests 的风险
```

### T142：Feedback Summary Exporter

输出安全摘要，供 review：

```text
过去 N 条反馈：
- 多少 accept
- 多少 edit
- 多少 reject
- 多少 boundary
- 常见 reason_tags
- 哪些 candidate_type 经常被选中
- 哪些 risk_flags 经常导致拒绝
```

不输出原始回复和编辑全文。

## 验收标准

M4 完成时，你应该能回答：

```text
用户更常选择哪类候选？
哪些候选经常被编辑？
哪些边界风险经常出现？
reject 是因为太冷、太热、太长，还是不像自己？
```

## 明确不做

M4 不做：

```text
自动更新 ContactSkill
自动更新 memory
LLM 分析反馈
平台发送
UI
数据库
向量库
```

这与当前 T140 约束一致。

---

# 3. M4.5：Regression Hardening

报告里提到 AgentEval、LLM-as-judge 等方向有价值，但你现在最缺的是**可提交的 deterministic regression tests**，不是复杂评估器。

M3 review 已明确：当前没有 committed regression tests，T150 必须覆盖结构、boundary sensitivity、thin context、false positives、subtle false negatives、privacy leakage、contact alignment、ranking。

## 建议任务

### T150：Committed ReplyPlanner Regression Tests

先做 pytest，不引入 LLM-as-judge。

测试集至少包含：

```text
1. baseline friend
2. colleague / practical relation
3. thin context
4. sensitive boundary
5. false positive probe
6. subtle false negative probe
7. privacy leakage probe
8. contact_id mismatch
9. approved-store missing
10. ranking uniqueness
11. raw text echo prevention
12. non-approved record leakage prevention
```

### T151：Policy Regression Fixtures

把 T132 里的 inline synthetic verification 转成 committed safe fixtures。

### T152：Feedback CLI Regression Tests

覆盖：

```text
accept
edit
reject
boundary
invalid rank
invalid plan path
stdout safe summary
private output confinement
```

## 为什么这一步必须在 LLM drafting 前

一旦你开始让 LLM 生成更自然的候选，没有 regression suite，就很难知道它是否偷偷：

```text
泄露原文
过度亲密
伪装真人
无证据引用
越过边界
污染 ContactSkill
```

所以 M4.5 是后面所有智能化升级的保险丝。

---

# 4. M5：Feedback-to-Patch

这是报告里最值得采纳的部分之一：**不要训练模型，不要 RLHF，先做自然语言 PreferencePatch。**

## 目标

把用户反馈变成“可审查的策略修正候选”，而不是直接改 memory 或 ContactSkill。

## 新增核心概念

### PreferencePatchCandidate

```text
patch_id
contact_id
patch_type
claim
behavior_instruction
negative_examples
positive_examples
supporting_feedback_ids
affected_candidate_types
confidence
status = candidate
sensitivity
created_at
```

patch_type 可以是：

```text
tone_preference
length_preference
boundary_preference
topic_preference
question_style
humor_style
repair_style
proactivity_preference
```

## 建议任务

### T160：PreferencePatch Schema

只定义 schema，不调用 LLM。

### T161：Feedback Clusterer

先用规则聚类：

```text
too_long
too_cold
too_eager
too_formal
too_intimate
boundary_violation
not_like_me
good_tone
```

### T162：Patch Proposal CLI

可以开始调用 LLM，但仍离线、review-only：

```bash
chat-feedback-propose-patch \
  --feedback-log private/... \
  --output private/patches/...
```

输出 candidate patch，不应用。

### T163：Patch Review CLI

类似 ContactSkill review：

```text
approve
reject
freeze
archive
```

只有 approved patch 能进入 runtime context。

### T164：Approved Patch Compact Context

在 ChatContext 中加入 compact patch brief：

```text
approved_preference_patches:
- 和此联系人聊天时，优先短句、低压、少解释。
- 对方表达压力时，先共情，不急于建议。
```

## 关键设计

一次反馈不能直接更新长期策略。

建议规则：

```text
1 次 edit/reject → feedback record
2–3 次相似反馈 → patch candidate
人工 approve → approved communication patch
多次 patch 冲突 → patch consolidation task
```

---

# 5. M6：ContactSkill 兼容式解耦

报告建议废除 ContactSkill，我不同意现在这样做。

你当前 pipeline 已经围绕 ContactSkill 做了：

```text
candidate builder
review exporter
file store
evidence validator
approved context
ReplyPlanner source refs
```

直接废除会导致大量重构和验证失效。

## 正确做法

把 ContactSkill 保留为 legacy aggregate，同时新增派生视图：

```text
ContactSkillStoreRecord
    ↓ derive / migrate
PartnerPersonaBrief
CommunicationPolicyBrief
RelationshipProfileSeed
BoundaryProfileBrief
```

也就是说：

```text
不要删除 ContactSkill
不要重写上游蒸馏
先新增 compatible projection
```

## 建议任务

### T170：ContactSkill Decomposition Design Doc

文档先行，明确字段归属。

| 字段类型   | 放哪里                              |
| ------ | -------------------------------- |
| 对方稳定事实 | PartnerPersona                   |
| 对方兴趣偏好 | PartnerPersona / TopicPreference |
| 两人相处方式 | CommunicationPolicy              |
| 边界/禁忌  | BoundaryProfile                  |
| 当前关系温度 | RelationshipState                |
| 回复策略   | CommunicationPolicy              |
| 证据链    | 保留在原 store / derived refs        |

### T171：PartnerPersonaBrief Schema

不要做完整 persona clone，只做“与回复相关的稳定画像”。

例如：

```text
stable_traits
topic_preferences
stress_patterns
known_constraints
confidence
evidence_refs
```

### T172：CommunicationPolicyBrief Schema

用于指导回复：

```text
preferred_tone
avoid_tone
question_style
humor_allowed
proactivity_level
repair_strategy
boundary_rules
version
superseded_by
evidence_refs
```

### T173：ContactSkill Projection Service

从 approved ContactSkill 生成 compact derived briefs。

### T174：ChatContext 支持 Derived Briefs

ReplyPlanner 优先读：

```text
CommunicationPolicyBrief
BoundaryProfileBrief
PartnerPersonaBrief
```

没有则 fallback 到原 ContactSkill brief。

## 验收标准

旧数据仍能运行。
新 schema 能进入 ChatContext。
ReplyPlanner 不需要一次性大改。
ContactSkill 继续作为证据聚合层存在。

---

# 6. M7：LLM-assisted ReplyPlanner

等 M4.5 测试和 M5 feedback patch 有了之后，再提升回复自然度。

## 目标

从 deterministic templates 过渡到 LLM-assisted candidates，但仍输出 `ReplyPlan`，仍 review-only。

## 建议架构

```text
ChatContext
+ Approved ContactSkill / Derived Briefs
+ Approved PreferencePatch
+ PolicyProfile
→ LLM Candidate Generator
→ Schema Validator
→ Policy Engine
→ Evidence Ref Checker
→ Candidate Ranker
→ ReplyPlan
```

## Candidate Types

建议固定候选类型：

```text
warm_supportive      温和接住
light_daily          轻松日常
low_pressure         低压不推进
playful              轻微幽默
repair               修复关系
concise              简短回应
boundary_respecting  明确尊重边界
```

每次根据上下文选择 3–5 个。

## 建议任务

### T180：LLM Candidate Generator Contract

先定义输入输出，不接入主 planner。

### T181：LLM Candidate Generator Offline CLI

```bash
chat-reply-generate-llm --context private/... --output private/...
```

### T182：Candidate Validator

检查：

```text
JSON schema
candidate count
candidate type
supporting refs
boundary reminders
no raw transcript echo
no impersonation
no unauthorized facts
```

### T183：Hybrid ReplyPlanner

支持两种模式：

```text
--mode template
--mode llm
```

默认仍 template，LLM 作为实验模式。

### T184：LLM Planner Holdout Eval

复用 T133 场景，对比：

```text
naturalness
evidence usage
boundary adherence
privacy safety
candidate diversity
```

## 不建议立刻做

暂不做：

```text
reranker 模型
DPO / RLHF
fine-tuning
agent self-reflection loop
```

---

# 7. M8：RelationshipState

这是项目真正成为“长期关系感知”的核心，但不能太早介入实时热路径。

## 设计原则

RelationshipState 不是“好感度”。
它是“回复约束和关系节奏控制器”。

建议字段：

```text
familiarity                  熟悉度
trust                        信任
warmth                       温度
reciprocity                  双向性
conflict_level               冲突残留
boundary_risk                边界风险
initiative_allowance         主动联系许可
intimacy_level               亲密层级
uncertainty                  不确定性
recent_interaction_temperature 近期互动热度
last_meaningful_interaction_at
last_conflict_at
last_repair_attempt_at
```

## 关键规则

RelationshipState 不应该每轮自动覆盖。

正确流程：

```text
conversation / feedback
→ RelationshipSignal
→ RelationshipDeltaCandidate
→ human review
→ approved RelationshipState update
→ compact context
```

## 建议任务

### T190：RelationshipState Schema

只做 schema 和文档。

### T191：RelationshipSignal Extractor

从 feedback / reply outcomes / conversation metadata 提取信号：

```text
user selected repair candidate
user rejected intimate candidate
boundary feedback occurred
long silence
positive edit
```

### T192：RelationshipDeltaCandidate

```text
delta_id
contact_id
dimension
old_value
proposed_value
reason
evidence_refs
feedback_refs
confidence
status
```

### T193：Relationship Review CLI

approve/reject/freeze/archive。

### T194：RelationshipState Compact Context

注入 ReplyPlanner：

```text
当前关系：熟悉但近期互动偏冷；避免突然热情或主动推进。
```

### T195：Relationship-aware Reply Eval

同一句消息在不同状态下应有不同回复：

```text
刚认识
熟悉朋友
冷淡期
冲突后
边界敏感
长期未联系
```

---

# 8. M9：Memory Retrieval Layer

报告建议 Mem0 作为底层检索，我认为“方向对，但时间点靠后”。

## 先做抽象

### T200：MemoryRetriever Interface

```python
class MemoryRetriever:
    def retrieve(
        self,
        contact_id: str,
        query: str,
        memory_types: list[str],
        limit: int,
        time_window: TimeWindow | None,
    ) -> list[MemoryHit]:
        ...
```

`MemoryHit` 必须包含：

```text
memory_id
text
memory_type
confidence
sensitivity
evidence_refs
source
valid_from
valid_to
superseded_by
retrieval_score
```

### T201：Local ApprovedStore Retriever

先用本地 approved store 实现。

可以是简单 keyword + recency + type filter，不要急着 vector DB。

### T202：Retrieval Eval Set

构造 30–50 个 synthetic retrieval cases：

```text
事实召回
过期事实
冲突事实
边界事实
偏好事实
关系状态事实
```

### T203：Optional Mem0 Adapter Spike

只做 spike，不合并主线。

评估：

```text
召回率是否提升
是否能隔离自动写入
是否能保留 evidence_refs
是否增加部署复杂度
是否会污染 review-first 语义
```

## 是否引入 Mem0 的判断标准

只有当它满足以下条件，才建议引入：

```text
1. 可以关闭自动提取/自动写入
2. 可以只索引 approved records
3. 可以保留 practical_chat_agent 的 record_id/evidence_refs
4. 可以本地运行或隐私可控
5. 在 retrieval eval 上明显优于本地实现
```

否则继续自研轻量检索。

---

# 9. M10：BehaviorPlanner

主动行为是后期功能，不是当前功能。

报告对 Generative Agents 的批判是对的：不要做全天候自我模拟。你需要的是**事件驱动的候选行为生成器**。

## 目标

生成主动行为草稿，不发送。

## 核心模型

### AgentSelfState

```text
agent_id
timezone
current_mood
energy_level
busyness
available_window
recent_virtual_events
shareable_topics
quiet_hours
```

### BehaviorPolicy

```text
max_daily_proactive_actions
min_interval_hours
allowed_action_kinds
requires_review
relationship_thresholds
boundary_rules
quiet_hours
```

### CandidateAction

```text
action_id
contact_id
action_kind
reason
draft_text
scheduled_after
risk_flags
supporting_context_refs
requires_review = true
status = candidate
```

action_kind：

```text
reply_later
share_daily_life
low_pressure_checkin
topic_reopen
repair_attempt
moment_draft
do_nothing
```

## 建议任务

### T210：Behavior Schema

只定义 schema。

### T211：ActionPlanner Rule Engine

不调用 LLM，先规则判断是否应该生成动作。

### T212：Proactive Draft Generator

可以调用 LLM，但输出 CandidateAction，不能发。

### T213：CandidateAction Review CLI

approve/reject/edit/archive。

### T214：Behavior Safety Eval

重点测试：

```text
长期未联系后不要突然亲密
冲突后不要过度主动
边界反馈后降低主动频率
不要一天多次打扰
不要伪装现实行动
```

## 什么时候才允许半自动

至少满足：

```text
ReplyPlanner regression tests 稳定
Feedback patch 已运行
RelationshipState 已可注入
OutboundSendGate 已完成
主动行为 eval 通过
用户显式 opt-in
```

在此之前全部 draft-only。

---

# 10. M11：OutboundSendGate + Feishu Sandbox

平台接入不应该从“收消息”开始，而应该从“出站安全阀”开始。

## T220：OutboundMessageRequest Schema

```text
request_id
platform
contact_id
channel_id
text
source_kind
source_id
created_at
approved_by_human
risk_flags
send_after
status
```

## T221：OutboundSendGate

必须支持：

```text
manual_only mode
rate limit
duplicate suppression
kill switch
quiet hours
self-echo prevention
audit log
```

## T222：Local Fake Adapter

先做 fake adapter，测试 send gate。

## T223：Feishu Adapter

飞书适合作为第一个真实平台，因为：

```text
官方 API
权限清晰
风控低
适合沙箱
支持卡片交互
```

但注意：飞书不应该进入核心逻辑，只做 adapter。

```text
FeishuEvent → InboundEvent
OutboundMessageRequest → Feishu send
```

## T224：Feishu Review Card

后期可以把候选回复以飞书卡片展示：

```text
候选 A / B / C
Accept
Edit
Reject
Boundary
```

这会极大提升反馈采集效率。

---

# 11. M12：WeChat Adapter

微信要做，但要晚做、薄做、可替换。

## 原则

```text
core 不依赖微信
微信不写 memory
微信不控制 relationship
微信不绕过 send gate
微信 adapter 可以随时替换
```

## 建议任务

### T230：WeChat Adapter Research Spike

比较：

```text
wechatbot
wechaty
WeChatFerry
chatgpt-on-wechat/CowAgent 可剥离部分
```

评估：

```text
维护状态
登录方式
掉线风险
封号风险
Python 兼容
消息 ID 可追踪性
附件支持
是否能只做 adapter
```

### T231：WeChat Inbound Adapter

只做收消息到 InboundEvent。

### T232：WeChat Outbound Adapter

只允许通过 OutboundSendGate。

### T233：WeChat Safety Mode

默认：

```text
manual_send_only = true
proactive_send_disabled = true
rate_limit_strict = true
```

## 不建议

不建议为了微信提前牺牲架构。

如果微信不稳定，飞书 / 本地 Web UI 仍然能验证核心算法。

---

# 12. 关于报告中几个建议的修正

## 12.1 “废除 ContactSkill”应改为“兼容式分解”

报告认为 ContactSkill 概念过载，这个判断对。
但建议废除不合适。

更好做法：

```text
ContactSkill = legacy aggregate / evidence bundle
PartnerPersona = derived stable profile
CommunicationPolicy = derived response rules
BoundaryProfile = derived safety constraints
RelationshipState = independent dynamic state
```

这样不会浪费现有代码。

## 12.2 “先接飞书”应改为“先 OutboundSendGate，再飞书”

飞书确实比微信适合测试。
但当前 T140/T150 前不宜接实时平台。

正确顺序：

```text
Feedback CLI
→ Regression tests
→ SendGate
→ Fake adapter
→ Feishu adapter
→ WeChat adapter
```

## 12.3 “集成 Mem0”应改为“先抽象 MemoryRetriever”

Mem0 有价值，但不能直接进入核心。

正确顺序：

```text
MemoryRetriever interface
→ local approved-store retriever
→ retrieval eval
→ Mem0 adapter spike
→ 决定是否合并
```

## 12.4 “三级记忆”可以采纳，但不要太早放开 auto-approved

报告建议：

```text
Ephemeral Buffer
Auto-approved Fact Store
Safety-Critical Store
```

方向对，但你当前的审查哲学更保守。建议分阶段：

第一阶段：

```text
Ephemeral Buffer：自动
Approved Store：人工
Safety-Critical：人工
```

第二阶段再考虑：

```text
Low-risk auto-approved
```

而且 low-risk auto-approved 不能进入策略层，只能进入临时上下文或低权重 memory。

---

# 13. 最建议立即创建的 Issues

下面是我建议你直接放入 task board 的版本。

## Issue 1: [M4/T140] FeedbackEvent schema and CLI

**Goal**
记录 ReplyPlan candidate 的 accept/edit/reject/boundary 反馈。

**Scope**
新增 `ReplyFeedbackRecord`、`ReplyFeedbackLog`、`FeedbackService`、`chat-reply-feedback` CLI。

**Acceptance Criteria**

```text
accept/edit/reject/boundary 均可追加 JSONL
invalid candidate rank 被拒绝
stdout 不输出 draft/edit/note 全文
不修改 memory/ContactSkill/store/planner
输出限制在 private/
```

**Out of Scope**
LLM、自动应用反馈、平台发送、DB、UI。

---

## Issue 2: [M4/T141] Feedback log validator

**Goal**
验证 feedback log 的结构、安全和引用完整性。

**Acceptance Criteria**

```text
能检查 candidate 引用是否存在
能检查 private path confinement
能检查 action-specific required fields
能输出 safe summary
```

---

## Issue 3: [M4/T142] Feedback summary exporter

**Goal**
把反馈日志变成安全统计摘要。

**Acceptance Criteria**

```text
输出 action 分布
输出 reason_tags 分布
输出 candidate_type 选择率
不输出私密文本
```

---

## Issue 4: [M4.5/T150] Committed ReplyPlanner regression tests

**Goal**
把 M3 条件变成可重复测试。

**Acceptance Criteria**

```text
覆盖 boundary sensitivity
覆盖 thin context
覆盖 false positives
覆盖 subtle false negatives
覆盖 privacy leakage
覆盖 contact alignment
覆盖 ranking uniqueness
```

---

## Issue 5: [M4.5/T151] Policy fixture suite

**Goal**
把 T132/T133 的 synthetic cases 固化为安全 fixtures。

**Acceptance Criteria**

```text
fixtures 可提交
不含真实聊天
pytest 可跑
CI/local clean env 可复现
```

---

## Issue 6: [M5/T160] PreferencePatchCandidate schema

**Goal**
定义从反馈中提炼出的策略补丁候选。

**Acceptance Criteria**

```text
patch 包含 supporting_feedback_ids
patch 默认 candidate
patch 不自动进入 runtime
patch 可审查
```

---

## Issue 7: [M5/T162] Feedback-to-patch proposal CLI

**Goal**
基于多条相似反馈生成 PreferencePatchCandidate。

**Acceptance Criteria**

```text
可从 feedback log 聚合相似反馈
可生成 candidate patch
可保留 feedback refs
不自动 approve
```

---

## Issue 8: [M6/T170] ContactSkill decomposition design

**Goal**
设计 ContactSkill 到 PartnerPersona / CommunicationPolicy / BoundaryProfile / RelationshipState 的兼容式拆分。

**Acceptance Criteria**

```text
字段归属清晰
旧 ContactSkill 不废弃
迁移路径清晰
ReplyPlanner fallback 规则清晰
```

---

## Issue 9: [M6/T173] ContactSkill projection service

**Goal**
从 approved ContactSkill 生成 derived compact briefs。

**Acceptance Criteria**

```text
生成 PartnerPersonaBrief
生成 CommunicationPolicyBrief
生成 BoundaryProfileBrief
保留 evidence refs
旧上下文仍可运行
```

---

## Issue 10: [M7/T180] LLM candidate generator contract

**Goal**
定义 LLM-assisted candidate generator 的输入输出和安全约束。

**Acceptance Criteria**

```text
输出仍是 ReplyPlanCandidate
候选有 candidate_type
必须有 rationale / refs / boundary_reminders
不发送
不修改 memory
```

---

## Issue 11: [M8/T190] RelationshipState schema

**Goal**
定义多维关系状态，不使用单一好感度。

**Acceptance Criteria**

```text
包含 familiarity/trust/warmth/conflict/boundary/initiative 等维度
支持 evidence_refs
支持 delta candidate
默认不自动更新
```

---

## Issue 12: [M9/T200] MemoryRetriever interface

**Goal**
为后续本地检索、Mem0 adapter、vector retrieval 建立统一接口。

**Acceptance Criteria**

```text
local approved-store retriever 可实现
MemoryHit 保留 evidence_refs
不引入外部向量库
```

---

## Issue 13: [M10/T210] BehaviorPlanner schema

**Goal**
定义主动行为草稿模型，但不发送。

**Acceptance Criteria**

```text
AgentSelfState
BehaviorPolicy
CandidateAction
CandidateActionQueue
全部 draft-only
```

---

## Issue 14: [M11/T220] OutboundSendGate

**Goal**
建立所有平台发送前的安全阀。

**Acceptance Criteria**

```text
manual_only
rate limit
duplicate suppression
kill switch
quiet hours
audit log
```

---

## Issue 15: [M11/T223] Feishu sandbox adapter

**Goal**
在 send gate 后接入飞书作为第一个真实平台。

**Acceptance Criteria**

```text
Feishu inbound -> InboundEvent
OutboundMessageRequest -> Feishu send
不绕过 send gate
不写 memory
```

---

# 14. 最终建议

我建议你后续路线这样定：

```text
现在不要重构大架构。
现在不要接 Mem0。
现在不要接微信。
现在不要接飞书。
现在不要做主动行为。
现在不要废除 ContactSkill。

先完成：
T140 Feedback Schema CLI
T141 Feedback Validator
T142 Feedback Summary
T150 Regression Tests

然后做：
PreferencePatch
ContactSkill compatible decomposition
LLM-assisted ReplyPlanner

再做：
RelationshipState
MemoryRetriever abstraction
BehaviorPlanner draft-only

最后做：
OutboundSendGate
Feishu
WeChat
```

最关键的战略判断是：

**你的项目已经有了比大多数 companion demo 更好的安全骨架。接下来不要追“大而全”，而要把“反馈—修正—评估—再生成”这条小闭环做扎实。**

只要这条闭环跑通，后面的 RelationshipState、主动行为、平台接入都会自然很多；反过来，如果现在先接平台、先做主动行为、先引入 Mem0，项目会很快变成一个难以验证、难以回滚的通用 bot。
