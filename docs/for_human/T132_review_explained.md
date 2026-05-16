# T132 Review Explained: Reply Policy（回复策略安全层）

## 一、这个 Task 在做什么？（通俗解释）

T131 实现了一个能生成回复草稿的 ReplyPlanner，但 reviewer 指出了一个关键问题：**如果当前场景很敏感怎么办？**

比如：
- 朋友刚提到分手、生病、家庭问题——回复太热情会显得冒犯
- 联系人的关系记录里明确标注了"不要追问"、"给空间"——回复还在追问就会越界
- 系统对这位联系人了解很少（thin context）——回复里假设很熟就显得不自然
- 草稿里出现了"对方会怎么想"这类话——这等于在替别人说话，是冒充风险

T132 就是给 T131 的 ReplyPlanner 加一层**安全检查**。在生成回复草稿之后，对每个草稿做"体检"：

1. 检查当前上下文是否敏感（家庭、感情、健康、金钱等话题）
2. 检查关系记录里有没有明确的边界提示（"不要追问"、"给空间"等）
3. 检查草稿本身有没有"过度主动"的措辞（催促见面、追问细节等）
4. 检查草稿有没有冒充联系人的嫌疑

如果检测到风险，系统会：
- 把草稿换成更保守的措辞（比如把"继续说说"改成"你不用现在展开"）
- 在草稿上标注具体的 `risk_flags`（风险标签），让人类 reviewer 知道哪里需要特别注意
- 添加更明确的 `boundary_reminders`（边界提醒）
- 降低置信度分数

**核心原则不变**：这些草稿仍然是只给你看的，系统**绝不自动发送**。

## 二、实现详解

### 2.1 任务目标

T132 的目标是在不改变 T131 输出格式（T130 `ReplyPlan`）的前提下，增加一个 policy/boundary 风险检测层，让敏感和边界场景在候选草稿中变得可见和可审查。

### 2.2 任务流程

```
T131 的 ChatContext 输入
  │
  ├─ T131 原有检查：contact_id 对齐、非空验证
  │
  ├─ 【T132 新增】build_profile()：上下文风险画像
  │   ├─ 检查 approved store 是否缺失 → thin_context
  │   ├─ 扫描关系摘要/策略提示/运行时文本 → sensitive_topic
  │   ├─ 扫描边界提示关键词 → boundary_sensitive
  │   ├─ 扫描"不要追问"关键词 → avoid_follow_up
  │   ├─ 检查关系类型/策略提示 → practical_tone
  │   └─ 综合判断 → conservative_mode（是否用保守模板）
  │
  ├─ 【T132 修改】选择草稿模板
  │   ├─ conservative_mode=True → 保守模板（"你不用现在展开"）
  │   └─ conservative_mode=False → T131 原始模板（"继续说说"）
  │
  ├─ 【T132 新增】对每个候选草稿做 assess_candidate()
  │   ├─ 继承上下文级风险标签
  │   ├─ 检查草稿文本是否过度主动 → over_proactive
  │   ├─ 检查草稿文本是否冒充联系人 → impersonation_risk
  │   └─ 计算置信度扣分
  │
  ├─ T131 原有检查：priority_rank 唯一顺序
  │
  └─ 输出 T130 ReplyPlan（3 个候选，带风险标签和边界提醒）
```

### 2.3 代码变化

#### `src/practical_chat_agent/services/policy.py`（新增 ~327 行）

在现有的 `PolicyEngine`（负责 outbound action 策略）旁边，新增了三个回复规划专用的结构：

- **`ReplyPlanPolicyProfile`**（dataclass）：上下文级的风险画像，包含：
  - `context_risk_flags`：上下文级风险标签（thin_context、boundary_sensitive）
  - `policy_boundary_summary`：策略边界摘要
  - `shared_boundary_reminders`：所有候选共享的边界提醒
  - `conservative_mode`、`avoid_follow_up`、`practical_tone`、`thin_context`、`boundary_sensitive`：布尔标志

- **`ReplyCandidatePolicyAssessment`**（dataclass）：候选级的风险评估结果，包含：
  - `risk_flags`：候选级风险标签
  - `boundary_reminders`：候选级边界提醒
  - `confidence_penalty`：置信度扣分

- **`ReplyPlanPolicyEngine`**：回复规划策略引擎，核心方法：
  - `build_profile(context)` → `ReplyPlanPolicyProfile`：分析上下文，检测风险
  - `assess_candidate(policy_profile, candidate_text, approach_label)` → `ReplyCandidatePolicyAssessment`：评估每个候选

引擎使用 8 组关键词列表做检测：
- 敏感话题关键词（家庭、感情、健康、金钱等 30+ 个中英文词）
- 边界提示关键词（"给空间"、"不要追问"等）
- 避免追问关键词
- 务实语气关键词
- 过度主动草稿关键词
- 行动推动关键词（见面、打电话等）
- 安全无压力关键词（"先不"、"等你方便"等 — 用作豁免）
- 冒充关键词（"对方会"、"替你回"等）

**关键设计**：`build_profile()` 会读取 `relationship_summary`、`strategy_hints`、`boundary_reminders`、运行时事件文本和记忆事实 claim 来做关键词匹配——但**只在内部做检测，不会把这些文本复制到输出里**。

#### `src/practical_chat_agent/services/reply_planner.py`（重构）

主要改动：

1. **构造函数增加 `policy_engine` 参数**：支持依赖注入，方便未来测试
2. **`generate()` 新增 `build_profile()` 调用**：在生成候选前先做风险画像
3. **`_draft_templates()` 增加 conservative_mode 分支**：敏感场景切换到保守模板
4. **新增 `_build_candidate()` 辅助方法**：替代原来直接构造 `ReplyPlanCandidate`，现在会先调用 `assess_candidate()` 做策略评估
5. **`_shared_boundary_reminders()` 扩展**：现在包含 `strategy_hints[:1]` 和策略引擎的 `shared_boundary_reminders`
6. **`_build_candidate_difference_notes()` 扩展**：保守模式下候选差异说明更明确
7. **新增 `_clamp_confidence()`**：确保扣分后的置信度仍在 [0.0, 1.0] 范围内

**原有功能完全保留**：
- `contact_id` 对齐检查不变
- `priority_rank` 唯一顺序校验不变
- 安全摘要重建不变
- 3 个候选结构不变
- CLI 命令不变

#### `docs/07_handoff.md`（追加 Section 26）

记录了 T132 的实现内容、3 组合成上下文验证结果和剩余风险。

### 2.4 对后续开发的意义

T132 在路线图中的位置：

```
M3: 回复规划
  T130: 定义 ReplyPlan schema     ✅
  T131: 实现 ReplyPlanner          ✅ (安全接线)
  T132: 增加策略安全层              ✅ ← 我们在这里
  T133: Holdout 评估               ← 下一步
```

**T132 的意义**：

1. **首次让"风险"在候选草稿中可见**。T131 只做了安全的接线，但不会区分"普通聊天"和"敏感话题"。T132 让高风险场景产生更保守的候选、明确的风险标签和边界提醒。

2. **为 T133 holdout 评估打下基础**。T133 要评估回复自然度和边界遵守，前提是边界遵守行为已经存在。T132 正是建立了这个行为。

3. **部分回应了 T131 的 reviewer warning**。T131 N03 指出 `strategy_hints` 和 `relationship_summary` 没有被使用。T132 的 `build_profile()` 现在消费了这些字段来做风险检测。

4. **为未来 LLM 草稿生成提供安全网**。当前草稿是硬编码模板，不包含冒充内容。但 `assess_candidate()` 中的 `impersonation_risk` 检测会在每次生成草稿时运行，当未来引入 LLM 生成的草稿时，这个安全网已经就位。

5. **当前局限性**：
   - 关键词匹配是子串匹配，不是词边界匹配（"space" 会匹配 "workspace"）
   - "关系" 这个关键词很宽泛，但通过复合触发条件缓解
   - 没有提交自动化测试（T150 负责）

## 三、为什么我给出了 PASS_WITH_WARNINGS 的 Review 结果？

### 通过（PASS）的部分

1. **任务包要求的四个风险类别全部实现**：`boundary_sensitive`、`over_proactive`、`impersonation_risk`、`thin_context` 都有明确的检测、标签和应对措施。

2. **保守模式切换是真实的行为变化**：不是仅仅加标签，而是真的换了草稿措辞（从"继续说说"变成"你不用现在展开"）。

3. **过度主动检测是上下文敏感的**：普通场景下"optional follow-up"不会被标记为 `over_proactive`；敏感场景下才会。无压力豁免机制正确（"先不往前推"不会被误标）。

4. **T131 所有功能保留**：contact_id 对齐、priority_rank 校验、安全摘要重建、CLI 命令都原封不动。

5. **没有违反任何禁止范围**：没有自动发送、没有数据库、没有向量库、没有降低现有 PolicyEngine 安全性。

6. **现有 PolicyEngine 完全不受影响**：新增的 `ReplyPlanPolicyEngine` 是独立的类，和原有的 outbound `PolicyEngine` 没有交集。

### 带有 Warning 的部分

Warning 1：**`build_profile()` 读取了运行时文本做关键词检测。**
- 包括 `latest_message_text`、事件文本、记忆事实的 claim
- 这些文本只用于内部关键词匹配，不会出现在输出里
- 这是合理的设计（类似垃圾邮件过滤器扫描邮件但不转发原文）
- 但值得注意，因为任务包说"不注入 raw transcript text"

Warning 2：**关键词匹配使用子串匹配，不是词边界匹配。**
- "space" 会匹配 "workspace"
- "loss" 会匹配 "glossary"
- 在当前紧凑输入下风险很低，但如果输入变得更多样可能产生误报

Warning 3：**代码中有三个重复的 `_dedupe` 实现。**
- `PolicyEngine`、`ReplyPlanPolicyEngine`、`ReplyPlanner` 各有一个
- 不影响正确性，但增加了维护成本

Warning 4：**没有提交自动化测试或 fixture。**
- 与 T131 相同的情况，T150 负责

### 总结

T132 在 T131 的安全接线之上增加了一个有意义的安全层。当检测到敏感话题、边界提示、薄弱上下文或冒充风险时，系统会切换到保守草稿、标注风险标签、添加边界提醒并降低置信度。这是从"只要不出错"到"主动标注风险"的重要进步。关键词匹配虽然粗糙，但对于 MVP 阶段是合理的选择。
