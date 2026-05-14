# Review: T103 M0 Milestone Gate

Review date: 2026-05-14
Reviewer: Claude Code (milestone)
Task package: `docs/tasks/M0_weflow_data_contract/T103_m0_review.md`

## Scope

只读审查 worker 针对 T103 的所有产出。T103 是 M0 milestone gate review，不写代码。核心判断：是否接受 worker 草案给出的 Gate M0 `Conditional` 结论，以及是否允许进入 M1。

## Diff Summary

所有变更均为未提交状态（working tree），落在以下文件：

| 文件 | 变化类型 | 是否在 Allowed files 内 |
| --- | --- | --- |
| `docs/review/T103_milestone_review.md` | 新增 | 是 |
| `docs/04_task_board.md` | 修改 | 是 |
| `docs/05_decision_log.md` | 修改 | 是 |
| `docs/07_handoff.md` | 修改 | 是 |
| `docs/08_risks_and_open_questions.md` | 修改 | 是 |

零 `src/**` 变更。零 `private/` 读取或输出。T103 未被标记完成，`Current Unique Task` 仍指向 T103。

## Task Completion Check

| 任务包要求 | 状态 | 证据 |
| --- | --- | --- |
| `docs/review/T103_milestone_review.md` | **完成** | 新建文件，含 Evidence Summary、Gate Checklist、M1 Readiness、Non-Blocking Conditions、Verdict |
| Gate M0 verdict | **完成** | `Conditional` |
| 明确下一唯一任务 | **完成** | 建议 T110 |
| 更新 `04_task_board.md` | **完成** | T103 状态更新，未标完成，未切任务 |
| 更新 `05_decision_log.md` | **完成** | D011 新增，状态 `Proposed` |
| 更新 `07_handoff.md` | **完成** | 状态、reviewer prompt、下一步顺序全部更新 |
| 更新 `08_risks_and_open_questions.md` | **完成** | R011/R012/R014/R015 缓解措施更新，Q112 更新 |

## Gate M0 Checklist Verification

逐条核对 `docs/06_eval_protocol.md` 第 2 节 Gate M0 的硬性要求与 worker 草案的一致性：

| Eval Protocol Gate M0 要求 | Worker 草案对应行 | 实际证据 | Reviewer 确认 |
| --- | --- | --- | --- |
| 能读取 `private/chat_history` 的 JSONL 并输出字段统计 | Checklist 行 1 | T100 `weflow_schema_profile.md` 第 1-3 节 + T102 CLI 实际运行 | **PASS** |
| 不把真实聊天原文写入 docs | Checklist 行 2 | T100/T101/T102 review 的 privacy audit 全部 PASS | **PASS** |
| 明确 normalized event schema | Checklist 行 3 | T100 `normalized_event_contract.md` 第 2 节 | **PASS** |
| 至少生成一个脱敏 fixture | Checklist 行 4 | `examples/payloads/weflow_redacted_sample.jsonl` + T101 review PASS | **PASS** |
| 明确 source_ref、event_id、sender_role、timestamp、message_type 规则 | Checklist 行 5 | T100 contract 第 3-7 节 + T101 source_ref_rules 第 2-8 节 | **PASS** |

**Gate M0 全部 5 条硬性要求均已满足。**

## Verdict Assessment: `Conditional` vs `Allow`

Worker 草案给出 `Conditional`。核心理由是 T102 review 留下了 6 个 non-blocking issues 需要带入 M1。

Reviewer 独立评估：

**支持 `Conditional` 的理由：**
- T102 的 N01-N06 确实需要在 M1 阶段持续关注
- `Conditional` 创建了明确的问责：后续任务必须处理这些条件
- 不阻碍进度——`Conditional` 仍然允许进入 M1
- 更保守和透明的信号传递

**支持 `Allow` 的理由：**
- 全部 5 条硬性 Gate M0 要求已满足
- Non-blocking issues 已在 risks 文档中跟踪并 deferred 到具体任务
- 理论上这些条件在任何时候都可能存在，`Conditional` 可能被滥用为默认选项

**Reviewer 判断：`Conditional` 是恰当的。**

原因：T102 的 non-blocking issues 不是泛泛的风险陈述，而是来自已落地代码的具体技术债务（双次读取、内存缓存、timezone 静默降级、单文件 sender_role 退化）。在 M1 第一个任务（T110 chunker）会直接消费 T102 产物的背景下，用 `Conditional` 明确标注"进入 M1 时这些条件需要被追踪"比简单的 `Allow` 更负责任。这不是滥用保守判断——这是对 M1 worker 的合理预警。

## Non-Blocking Conditions Verification

Worker 草案列出了 5 个 non-blocking conditions。逐条验证其与 T102 review 的对应关系：

| Worker 条件 | 来源 | 对应任务 | Reviewer 确认 |
| --- | --- | --- | --- |
| 1. type=80/chatRecords fixture 与测试覆盖不足 | T100 N02, T101 N01, T102 无新补充 | T110/T150 | **合理** |
| 2. sender_role 单文件/额外 member 行稳健性 | T102 N06 | T114/T150 | **合理** |
| 3. timezone fallback、双次读取、全量缓存 | T102 N01/N02/N03 | T110/T150 | **合理** |
| 4. event_id 继续用 namespaced SHA-1 | T102 Q108 | T150 前可调整 | **合理** |
| 5. T112+ LLM-facing 步骤必须遵守 T101 隐私边界 | T102 N05 | T112+ | **合理** |

T102 的 N04（系统消息关键词硬编码）已被 Captain 在 D010 中 accepted，因此不在条件中列出，正确。

**5 个条件全部有来源、有目标任务、无遗漏。**

## Next Task Recommendation

Worker 建议下一唯一任务为 T110（conversation chunker v0）。

Reviewer 独立评估：

- T110 是 M1 的自然起点，直接消费 `normalized_events.jsonl`。
- T110 先于 T111（schema 定义）可以让 chunker 基于实际数据形态设计，而不是先设计 schema 再适配。
- T110 最适合承接 T102 的条件：chunker 直接面对双次读取/内存缓存问题，需要处理 risk_flags 和 message_type 的不确定性。

**Reviewer 确认：T110 是合理的下一唯一任务。**

## Governance Consistency Check

| 文档 | 一致性检查 | 结果 |
| --- | --- | --- |
| `04_task_board.md` | T103 仍是 `[ ]`，Current Unique Task 仍指向 T103，T102 已标 `[x]` | **一致** |
| `05_decision_log.md` | D011 状态 `Proposed`，不声称已接受 | **一致** |
| `07_handoff.md` | 状态"worker 草案已完成，待 reviewer 审查"，未切换任务 | **一致** |
| `07_handoff.md` reviewer prompt | 已从"worker 执行 gate review"改为"reviewer 审查 worker draft" | **一致** |
| `08_risks_and_open_questions.md` | R011/R012/R014/R015 缓解措施引用了 T103 worker draft 的判断 | **一致** |

## Pseudo-implementation / Mock / Stub / Hardcode Check

T103 是纯文档任务。所有内容基于 T100-T102 的实际 review 结论，无代码实现。不存在伪实现、mock、stub 或硬编码问题。

## Missing Verification

Worker 已运行：
1. 检查 review 文档是否引用了 T100/T101/T102 和 `06_eval_protocol.md` — 可确认
2. 读回治理文档确认状态一致 — 可确认
3. `git diff --check` — 无格式错误
4. `git status --short` — 确认涉及文件在 Allowed files 范围内

验证充分。

## Over-engineering Check

Milestone review 约 78 行，结构清晰（Evidence Summary → Checklist → M1 Readiness → Conditions → Verdict → Next Task）。Governance 文档更新是必要的增量变更，没有过度设计。

## Blocking Issues

无。

## Non-blocking Issues

1. **N01 — D011 状态应随 reviewer 结论更新**：当前 D011 状态为 `Proposed`。Reviewer 接受后，Captain 应将其更新为 `Accepted`。**严重度：低，Captain 后续处理。**

2. **N02 — Milestone review 第 6 节 `M1 Readiness Assessment` 可以更具体**：当前三条准备度评估是定性描述，如果能在每条后面附上具体的 normalized event 字段名（如 `source_message_type_code`、`risk_flags`），对后续 worker 的指导性更强。但作为 gate review 文档，当前详细程度已经足够。**严重度：低。**

## Suspicious Implementation Details

无。

## Milestone Gate Verdict

**Accept worker draft. Gate M0 = `Conditional`.**

理由：
1. `docs/06_eval_protocol.md` Gate M0 的 5 条硬性要求全部满足。
2. T100/T101/T102 均已 reviewer `PASS`，没有留下会直接阻止 M1 chunking 的 blocker。
3. T102 review 的 6 个 non-blocking issues 已被正确识别并映射到 M1/M5 的具体任务中，5 个 `Conditional` 条件都有明确的来源和目标任务。
4. `Conditional` 而非 `Allow` 是恰当的——它对 M1 worker 提供了合理的技术预警，而不是泛泛的风险重述。

## Recommended Next Action

1. Captain 将 T103 在 `04_task_board.md` 标记为完成。
2. 将 D011 状态从 `Proposed` 更新为 `Accepted`。
3. 将 `Current Unique Task` 切换为 **T110: 实现 conversation chunker v0**。
4. T110 worker 需注意的 M0 条件：
   - 评估是否需要流式处理（对应 N02 双次读取、N03 全量缓存）
   - 保留 `source_message_type_code`、`risk_flags`、`interaction_flags` 字段（对应不确定性信号的延续）
   - 对 `type=7`/`type=80` 消息的保守处理策略（对应 type=80/chatRecords 条件）
5. T112+ 任何面向 LLM 的蒸馏步骤必须继续执行 T101 隐私边界（对应条件 5）。
