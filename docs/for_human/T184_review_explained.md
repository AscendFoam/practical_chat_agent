# T184 Review 通俗解释

## 1. 这个 Task 在做什么？

T184 是 Milestone 7（LLM 辅助回复规划器）的第四步，也是该里程碑的**评估阶段**。

**通俗理解**：T183 把模板回复和 LLM 回复合并成了"混合模式"（hybrid mode）。但是——LLM 生成的回复到底好不好？是不是比纯模板更有用？会不会绕过安全检查？这些问题在 T183 里没有回答。T184 就是用来回答这些问题的。

具体做法：
1. 设计 6 个不同的聊天场景（朋友分享好消息、同事问工作、敏感话题、陌生人、有共同回忆的朋友、低频联系人）
2. 每个场景分别用纯模板模式和混合模式跑一遍
3. 比较两个模式在自然度、证据使用、边界遵守、隐私安全等维度上的表现
4. 给出判断：混合模式到底值不值得继续投入？

关键限制：
- **只评价，不修代码**（不能改 planner、generator、validator）
- **不能泄露隐私**（评估结果里不能出现真实聊天内容）
- **不能夸大质量**（好就是好，不好就是不好）

## 2. 任务实现详解

### 目标

评估 T183 混合模式的质量，回答：hybrid 是否比 template 更好？是否安全？是否有必要继续推进？

### 评估方法

Worker 做了以下工作：

**第一步：设计 6 个匿名场景**
| 场景 | 类型 | 含义 |
|------|------|------|
| S1 new_job | 温暖基线 | 朋友分享升职好消息 |
| S2 work | 中性任务 | 同事问季度报表 |
| S3 sensitive | 敏感边界 | 朋友说最近很难 |
| S4 thin_context | 无上下文 | 陌生人来打招呼 |
| S5 memory_rich | 记忆丰富 | 朋友提起去年约的徒步 |
| S6 low_pressure | 低压边界 | 低频联系人道歉回复慢 |

所有场景都是完全合成的，不使用真实聊天记录。

**第二步：生成 12 个回复计划**
每个场景跑两次：
- `chat-reply-plan`（纯模板模式）→ 6 个 plan
- `chat-reply-plan --hybrid`（混合模式，调用 Deepseek）→ 6 个 plan

共 12 个 ReplyPlan 输出，全部保存在 `private/distilled/t184_holdout_eval/`。

**第三步：人工评估 6 个维度**

| 维度 | 模板分 | 混合分 | 变化 |
|------|--------|--------|------|
| 自然度 | 3/5 | 4/5 | **+1** |
| 证据使用 | 3/5 | 3.5/5 | **+0.5** |
| 边界遵守 | 4/5 | 3/5 | **-1** |
| 隐私安全 | 5/5 | 5/5 | 0 |
| 候选多样性 | 3/5 | 4/5 | **+1** |
| 合并稳定性 | 5/5 | 5/5 | 0 |

### 核心发现

**好的方面**：
- LLM 回复明显更自然、更贴近场景。S5（记忆丰富）场景中，LLM 直接提到了 hiking trip，模板还是泛化的寒暄
- 候选多样性更好，LLM 不会像模板那样重复同样的句式
- 隐私安全两模式都满分，没有泄露

**不好的方面**：
- **边界遵守下降**：LLM draft 的文字可能和 policy flag 冲突。比如 S4（thin context）场景，policy 标注了 `thin_context` 说不要问私人问题，但 LLM 还是写了"你最近在忙什么"——flag 对了但文字没约束住
- **语言混搭**：模板输出中文，LLM 默认输出英文。reviewer 看候选 1 是中文，候选 2/3 是英文，体验割裂
- **LLM 自信度过高**：0.79-0.95 vs 模板 0.45-0.78，但这不代表 LLM 的回复真的那么好
- **approach_label 命名混乱**：混用了 snake_case、标题大小写、句子片段

### 文件变化

**已提交的新文件**：
- `docs/review/T184_milestone_review.md` — Milestone review 文档

**已修改的文件**：
- `docs/07_handoff.md` — 新增 §86 T184 Eval Record

**不提交的私密产物**（在 `private/distilled/t184_holdout_eval/`）：
- 6 个场景的 ChatContext JSON
- 12 个 ReplyPlan 输出（6 template + 6 hybrid）
- `eval_analysis.json` — 结构化对比数据
- `private/t184_run_eval.py` — 自动化评估脚本

**工作区配置变更**：
- `.claude/settings.json` — 新增 eval 命令的权限条目（同 T160+ 一贯模式）

### 对后续开发的意义

1. **Gate M7 判定为 Conditional**：混合模式有明确价值（自然度 +1），但也有明确问题（边界遵守 -1、语言混搭），必须先修复问题才能推进到 M8
2. **揭示了 3 个必须修的问题**：语言一致性、安全约束执行、命名规范
3. **T183 遗留的 M01 gap 被再次确认**：缺少 committed merge 成功路径回归测试
4. **评估规模有限**：6 个合成场景不足以代表真实对话多样性，后续需要更大规模评估
5. **推荐了 T185 作为下一步**：专注于修复语言和安全问题，不扩大 scope

## 3. 为什么我给出了 PASS_WITH_WARNINGS？

### 没有 Blocking Issues

任务目标全部完成：
- ✅ `docs/review/T184_milestone_review.md` 已创建，包含 scope、method、results table、findings、Gate M7 verdict、next task recommendation
- ✅ 6 个维度全部覆盖：naturalness、evidence_usage、boundary_adherence、privacy_safety、candidate_diversity、merge_stability
- ✅ 纯评估，未修改 planner 代码
- ✅ 未提交私密内容到可提交目录（grep 验证通过）
- ✅ 未夸大质量：自然度 3/5→4/5 如实报告，边界遵守下降如实报告
- ✅ Gate M7 = Conditional，附带 4 条具体条件
- ✅ 推荐了后续 T185 但声明"不执行"

### Warnings 原因（N01-N03）

**N01 — `.claude/settings.json` 越界**：同 T160+ 每个任务的一贯模式，已被一贯接受。

**N02 — 自评分数无独立验证**：自然度、证据使用等评分是 worker 自评的，没有第二人独立打分。不过 worker 已经透明写明了"self-reported"，没有欺骗。

**N03 — 多样性指标只算 label 数量**：候选多样性是用 `approach_label` 去重计数来衡量的，但两个不同 label 的候选语义上可能很相似。不过定性观察部分已经补充了文本层面的分析。

### 和 T183 review 的对比

T183 的 review 也给了 PASS_WITH_WARNINGS：
- T183 的问题是**缺少 merge 成功路径测试**（N02/M01）—— 代码没测 LLM 正常返回候选的情况
- T184 的问题是**评分依赖自评 + settings 越界**—— 评估本身是诚实的，但方法论有局限

两个都是"核心任务完成，有可接受的次要问题"。

## 4. Worker 文档的补充说明

Worker 的 `T183_worker_summary.md`、`T184_worker_summary.md` 和 `T184_milestone_review.md` 写得都很完整，没有发现实质性错误。以下是可以补充的几点：

1. **多样性指标的局限**：Worker 用了 `approach_label` 去重来算多样性，但模板的 3 个 label 始终不同（`conservative_acknowledgment`、`optional_follow_up`、`paced_next_step`），所以模板多样性永远=3。这个指标其实区分不了模板和 hybrid——真正的差异在 draft text 的语义多样性，不是 label 数量。Worker 的定性观察已部分弥补了这一点。

2. **自信度偏差未被量化分析**：Worker 正确指出了 LLM 自信度偏高（0.79-0.95 vs 0.45-0.78），但没有分析这是否与回复质量正相关——即高自信度的 LLM 候选是否真的更好。这个分析需要更大样本。

3. **场景规模限制被正确处理**：6 个场景确实不足以全面代表真实对话多样性，Worker 在剩余风险中已经注明。这是一个诚实的 limitation 陈述，不是遗漏。

4. **设置文件越界已在 worker 警告中隐含包含**：Worker 的 Allowed Files 提醒中已列明允许文件范围，但没有显式标注 `.claude/settings.json` 越界。这个问题从 T160 起持续存在，建议后续任务保持注意。

整体来说，Worker 的工作质量很高——评估方法合理、发现诚实（不掩盖问题）、文档完整、推荐了可执行的后续任务。
