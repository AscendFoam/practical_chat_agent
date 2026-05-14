# T114 Review Explained: M1 Milestone Sample Run

## 1. 这个 Task 是什么？通俗解释

T114 是整个 M1（离线蒸馏 MVP）阶段的"期末考试"。

前面几个任务（T110-T113）分别实现了"切块"、"定义格式"、"AI 总结提取事实"、"组装联系人档案"。每个任务都用了同一个小样本验证过。但问题是：**这些步骤串在一起，真的能跑通吗？结果真的靠谱吗？**

T114 的任务就是：

1. 把整个管线跑出来的产物全部检查一遍
2. 随机抽查至少 5 条 AI 提取的"事实"，验证每条事实引用的证据是否真的能支撑这个说法
3. 给出 M1 阶段的总评：通过 / 有条件通过 / 不通过

**这是唯一一次在进入下一阶段之前，由独立审查者验证"AI 说的这些话，有没有凭据"的环节。**

打个比方：
- T110-T113 像是在造一条流水线——切块机、总结机、事实提取机、档案组装机
- T114 就是第一次打开整条流水线，检查最终产品是否合格

## 2. 实现详细解释

### 2.1 任务目标

T114 的目标不是写代码，而是**审计**。具体来说：

1. **验证产物完整性**：确认 `private/distilled/t102_smoke` 目录下有完整的 M1 产物链（从原始事件到最终档案）
2. **抽查证据链**：至少 5 条 memory fact，检查每条的 `evidence_refs` 是否真的指向支持该 claim 的原始事件
3. **评估 T113 的 warnings**：上次 T113 review 提出了三个警告（启发式泛化、置信度数值过度精确、话题提取覆盖窄），需要在实际样本上验证
4. **评估 review artifact**：检查 `contact_skill.review.md` 是否可人工审阅、是否泄露隐私、是否包含"模拟联系人说话"的内容
5. **给出 M1 gate verdict**：决定是否允许进入 M2

### 2.2 任务流程

```
读取 private/distilled/t102_smoke/ 下所有产物
       ↓
1. 确认 7 个文件都存在（normalized_events, chunks, summaries, facts, candidate, review, report）
2. 运行安全复查命令（dry-run 模式）
3. 逐条检查 7 条 memory facts 的 evidence_refs
4. 对照原始事件文本，判断 claim 是否有据
5. 读取 contact_skill.review.md，检查审阅可用性
6. 评估 T113 warnings 的实际影响
       ↓
输出 docs/review/T114_milestone_review.md
给出 Gate M1 = Conditional
更新 docs/07_handoff.md（T114 worker update）
更新 docs/08_risks_and_open_questions.md（新增 R030，关闭 Q105）
```

### 2.3 代码/文件变化详解

#### 文件 1: `docs/review/T114_milestone_review.md`（新文件）

这是最核心的产物——M1 里程碑评审文档。包含：

- **样本概述**：用了哪个样本、产物统计
- **证据审计表**：7 条 memory facts 逐条检查，每条给出 PASS / PASS_WITH_CAUTION
- **ContactSkill review 评估**：review artifact 是否可人工审阅
- **T113 warnings 跟踪**：三个警告在实际样本上的表现
- **Gate M1 检查清单**：对照 `docs/06_eval_protocol.md` 的 6 个硬性要求
- **Verdict: Conditional**：不是 Allow（因为泛化未证明），不是 Block（因为证据链本身可用）

关键发现：

- 7/7 facts 都有 event-level evidence
- 但 2 条事实出现了"短证据 -> 平滑 paraphrase"的压缩问题：
  - 一条把 73 条转发记录压缩成一句密集的 reflection（虽然内容准确，但压缩幅度大）
  - 一条把"我先看看[捂脸]"这种随口说说升级成了"review the materials first"这种正式意图

#### 文件 2: `docs/07_handoff.md`

新增第 16 节，记录 T114 worker update：
- 明确写成 "review pending"，没有把任务标成已完成
- 记录了证据审计结果和 draft 结论

#### 文件 3: `docs/08_risks_and_open_questions.md`

- **新增 R030**：记录了"短证据 -> 平滑 paraphrase"压缩风险。这意味着 AI 可能会把一句随口的话"美化"成一个严肃的判断，导致后续使用者高估事实的可靠性。
- **关闭 Q105**：回答了"第一轮 MVP 选哪个联系人？"——用的是 `t102_smoke` 样本。

### 2.4 对后续开发的意义

T114 的 Conditional verdict 意味着：

**可以进入 M2，但必须带着条件：**

1. **T120（文件存储）**：可以开始实现持久化存储，但所有存入的 skill 必须保持 candidate 状态
2. **T121（证据验证器）**：特别需要关注"仅 chunk_id 级证据"和"paraphrase 压缩"的检测
3. **T122（审阅 CLI）**：人工审阅时必须能看到 evidence refs 的原文，才能判断 paraphrase 是否过度
4. **T123（上下文集成）**：只有 approved 的 skill 才能进入 ChatContext——而目前还没有任何 skill 被 approve

**T114 确立了几个对后续所有任务都重要的原则：**

- ContactSkill 中的 confidence/closeness/trust 数字只是启发式，不是精确测量
- "candidate-only / human-review-first" 模式必须保持到更广样本验证通过
- 转发记录（forwarded records）和混合消息（mixed messages）需要特别谨慎处理
- AI 生成的 paraphrase 可能美化原始表述，审阅时必须对照原文

## 3. 为什么给出 PASS_WITH_WARNINGS？

### 总体判断

Worker 完成了 T114 的全部要求：

- 检查了 M1 产物链的完整性（7 个文件都在）
- 抽查了全部 7 条 memory facts（超过了"至少 5 条"的要求）
- 评估了 T113 的三个 warnings
- 给出了有理有据的 Gate M1 verdict（`Conditional`）
- 没有修改代码、没有泄露隐私、没有把计划写成事实

没有 blocking issue，所以不是 BLOCK。

### 我做了什么独立验证

作为 reviewer，我**独立读取了原始 normalized_events.jsonl**，逐条对照了 7 条 memory facts 的 claim 和 evidence_refs：

| 事实 | 我的判断 |
|---|---|
| "Contact introduces self as: power" → 事件原文 "我是power" | 直接匹配，PASS |
| "Contact shared exam prep background..." → 一个包含 73 条子记录的转发消息 | 内容准确但压缩幅度大，PASS_WITH_CAUTION |
| "Target school is Shanghai University of Technology" → 事件原文 "目标院校上海理工大学" | 直接匹配，PASS |
| "Estimated score 300-310, 320 unreachable" → 两个事件分别确认两部分 | 复合证据，PASS |
| "Fears not passing national line" → 事件原文 "过不了国家线了" | 直接匹配，PASS |
| "User offered tutoring support" → 事件原文 "辅导的话，需要先了解下你的基础..." | 用户说的是"如果要辅导的话，先了解一下"，不是"我提供辅导"——轻微夸大 |
| "User said they would review the materials first" → 事件原文 "欧克欧克，我先看看[捂脸]" | "我先看看"是随口说法，被提升为具体的学习计划——过度阐述 |

Worker 的审计**准确识别了两个 caution 项**。我还额外发现了第 6 条事实中的轻微夸大（"offered support" vs "proposed evaluation"），但这不构成阻塞问题。

### 为什么不是纯 PASS？

有 4 个非阻塞 issue 值得记录：

1. **N01**: `mem_b4731b7a6ce349ba` 轻微夸大了用户的意图——用户说的是"先了解基础再决定"，被表述为"offered tutoring support"。作为 candidate-only 的事实可接受，但审阅者需要知道这个区别。

2. **N02**: `mem_240b70cbad024a8e` 把随口的"我先看看"提升为"review the materials first"——这是 R030 所记录的"paraphrase 压缩"问题的具体实例。

3. **N03**: 样本太小（1 个联系人、12 条消息、1 个 chunk、7 条事实），不能证明管线的泛化能力。这不是 worker 的问题——是结构性限制。

4. **N04**: 我没有独立验证 `run_report.json` 的每个字段是否与产物一致，但抽查的数字都对得上。

### 为什么确认 worker 的 `Conditional` verdict？

Worker 给的是 `Conditional`，不是 `Allow`。我同意这个判断，原因是：

- **证据链可用，但只在当前样本上**：7/7 facts 都有 event-level evidence，这很好。但这是 T102 用 `--limit 12` 创建的超小样本，不代表性。
- **T113 的 warnings 没有被缓解**：启发式泛化没证明、置信度数字仍显过度精确、话题提取仍窄。
- **新的风险被确认**：paraphrase 压缩（R030）在至少 2 条事实上已经可见。

`Conditional` 的意思是：M1 的核心能力已验证（管线能跑通、证据链存在），但**已知限制必须在 M2 继续跟踪，不能被忽略**。这是对后续开发最负责任的判断。

### 结论

T114 作为 M1 milestone review，正确识别了 M1 管线的实际能力和已知限制。`Conditional` verdict 允许进入 M2 但保持了必要的审慎。所有非阻塞 issue 都是"当前样本太小"或"AI 会美化原始表述"这类已知的、被跟踪的 MVP 限制。

因此判定为 **PASS_WITH_WARNINGS**，Gate M1 = `Conditional` confirmed。
