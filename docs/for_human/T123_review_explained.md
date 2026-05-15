# T123 Review Explained: Context Integration

## 一、这个 Task 在做什么？（通俗解释）

继续用工厂的比喻：

- T120 建了仓库（file store），把半成品存起来。
- T121 建了质检中心（evidence validator），检查每个半成品的"证据来源"是否齐全。
- T122 建了审核站（review CLI），让人工审核员逐个批准或拒绝。
- **T123 做的是"运输到生产线"**：把已经通过所有质检和人工审核的产品，以精简包装（compact brief）的形式，送到生产线上，供后续的"回复策略师"（ReplyPlanner）使用。

关键安全规则：

1. **只有通过所有关卡的产品才能上生产线**：approved + 人工审核过 + 证据校验通过 + 运行时就绪。
2. **不能送整箱产品**：只能送"精简摘要"——短关系描述、策略提示、边界提醒、记录 ID 和证据引用。
3. **没有产品也能正常生产**：如果没有配置仓库路径，或者仓库里没有合格产品，生产线照常运转。

## 二、实现详解

### 2.1 任务目标

T123 的核心目标是让现有的 `ChatContext`（对话上下文）能够携带已审批的 ContactSkill 和 Memory Fact 信息，为后续 ReplyPlanner 提供安全、可控、可审计的输入。

用架构图表示：

```
之前:
  ChatContext = 最近消息 + 记忆命中 + 用户画像

之后:
  ChatContext = 最近消息 + 记忆命中 + 用户画像 + approved_store_context
                                                      ↓
                                              已审批的联系人技能摘要
                                              已审批的记忆事实摘要
                                              来源记录 ID + 证据引用
```

### 2.2 任务流程

当一条新消息到来，上下文组装的完整流程：

```
1. ChatContextAssembler.assemble() 被调用
   ├── 收集最近消息、记忆命中、用户画像（原有逻辑）
   └── 新增：_load_approved_store_context(contact_id=...)

2. _load_approved_store_context 执行流程:
   ├── 如果没有配置 store 路径 → 返回 status="not_configured"
   ├── 如果路径不存在 → 返回 status="store_path_missing"
   ├── 如果没有证据校验报告 → 返回 status="validation_report_missing"
   ├── 加载 memory store 和 contact skill store
   ├── 对每条记录做五重门禁检查
   │   ├── 门1: contact_id 匹配
   │   ├── 门2: status == "approved"
   │   ├── 门3: is_runtime_ready() == True
   │   ├── 门4: evidence_validation_status == "passed"
   │   └── 门5: 校验报告中 0 缺失引用 且 >0 已校验引用
   ├── 通过所有门禁的记录 → 生成紧凑摘要
   └── 如果没有合格记录 → 返回 status="no_runtime_ready_records"

3. 摘要被注入到 ChatContext:
   ├── approved_store_context 字段（完整结构化数据）
   ├── summary 字段（加入简短的关系描述和记忆摘要）
   └── memory_retrieval_notes 字段（加入来源、策略提示、边界提醒）
```

### 2.3 代码变化

#### 2.3.1 `src/practical_chat_agent/core/models.py`

新增 3 个紧凑模型和 1 个状态类型：

**`ApprovedStoreContextStatus`**（状态字面量）：
```
"not_configured"          — 没有配置仓库路径
"store_path_missing"      — 配置了路径但文件不存在
"validation_report_missing" — 没有证据校验报告
"no_runtime_ready_records" — 有仓库和报告但没有合格记录
"loaded"                  — 成功加载了合格记录
```

**`ApprovedMemoryFactBrief`**（记忆事实摘要）：
- `record_id`: 来源记录 ID
- `memory_id`: 记忆 ID
- `memory_type`: 记忆类型
- `claim`: 事实描述（截断到 140 字符）
- `evidence_refs`: 证据引用（最多 6 条）

**`ApprovedContactSkillBrief`**（联系人技能摘要）：
- `record_id`: 来源记录 ID
- `contact_id`: 联系人 ID
- `relationship_type`: 关系类型
- `relationship_summary`: 关系摘要（截断到 160 字符）
- `strategy_hints`: 策略提示（最多 4 条，每条 120 字符）
- `boundary_reminders`: 边界提醒（最多 4 条）
- `evidence_refs`: 证据引用（最多 6 条）

**`ApprovedStoreContext`**（完整上下文容器）：
- `status`: 上述状态之一
- `source_path`: 来源路径
- `validation_report_path`: 校验报告路径
- `contact_id`: 匹配的联系人
- `contact_skill`: 联系人技能摘要（0 或 1 个）
- `memory_facts`: 记忆事实摘要列表
- `source_record_ids`: 所有来源记录 ID
- `evidence_refs`: 所有证据引用
- `notes`: 备注

**`ChatContext`** 新增字段：
- `approved_store_context: ApprovedStoreContext`（默认为空，status="not_configured"）

#### 2.3.2 `src/practical_chat_agent/services/chat_context.py`

`ChatContextAssembler` 新增约 250 行代码：

**构造函数扩展**：
- `approved_store_path: Path | None` — 可选的仓库路径
- `approved_memory_limit: int` — 记忆事实加载上限（默认 4）

**`assemble()` 方法扩展**：
- 调用 `_load_approved_store_context()` 加载已审批上下文
- 将审批存储笔记合并到 `memory_retrieval_notes`
- 将审批技能/记忆摘要注入 `summary`

**五重门禁**（`_memory_record_eligible` / `_contact_skill_record_eligible`）：
```python
# 门1: contact_id 匹配
if record.contact_skill.contact_id != contact_id:
    return False
# 门2: 状态必须是 approved
if record.contact_skill.status != "approved":
    return False
# 门3: T120 的运行时就绪门禁（approved + human-reviewed + last_decision=approved）
if not record.is_runtime_ready():
    return False
# 门4: T122 写入的证据校验状态
if record.review_metadata.evidence_validation_status != "passed":
    return False
# 门5: 再次从 T121 校验报告确认（0 缺失引用 + >0 已校验引用）
if not self._validation_record_is_evidence_ready(
    validation_record=validation_records.get(record.record_id),
):
    return False
```

**摘要构建**：
- `_build_relationship_summary()`: 关系类型 + 状态 + 语气 + 直接程度，截断到 160 字符
- `_collect_strategy_hints()`: 从回复策略中提取 4 条策略提示
- 边界提醒：usage_boundary.notes + user_side_preferences.boundaries，共最多 4 条
- 所有文本都经过 `_compact_text()` 截断

**优雅降级**（4 种失败情况都有清晰状态）：
- 无路径 → `not_configured`
- 路径不存在 → `store_path_missing`
- 无校验报告 → `validation_report_missing`
- 无合格记录 → `no_runtime_ready_records`
- 所有情况下 `ChatContext` 仍然有效，只是没有审批存储内容

#### 2.3.3 `src/practical_chat_agent/app/container.py`

新增两个可选环境变量注入：
- `PRACTICAL_CHAT_APPROVED_STORE_PATH`: 指向 `private/distilled/<run_id>` 目录
- `PRACTICAL_CHAT_APPROVED_MEMORY_LIMIT`: 记忆事实加载上限（默认 4）

这两个环境变量都是可选的。不设置时行为与 T123 之前完全一致。

#### 2.3.4 `docs/07_handoff.md`

新增第 20 节 "T123 Completion Record"，记录代码变更、验证结果和剩余风险。

### 2.4 对后续开发的意义

T123 是 M2 里程碑（Memory/Skill Store 与证据校验）的最后一个任务。它完成后：

1. **M2 里程碑完成**：T120（存储）→ T121（校验）→ T122（审阅 CLI）→ T123（上下文集成）形成完整的"存储-校验-审阅-消费"链条。

2. **M3（ReplyPlanner）可以安全开始**：T130 可以直接从 `ChatContext.approved_store_context` 读取已审批的联系人技能和记忆事实，生成回复草稿。ReplyPlanner 不需要直接接触 store 文件或做任何门禁检查——这些都已经由 T123 完成。

3. **candidate-only / human-review-first 语义贯穿整个链路**：
   - T120 确保记录默认是 candidate
   - T121 确保缺失证据的记录被标记
   - T122 确保人工必须做决策
   - T123 确保只有全部通过的记录才能进入运行时上下文

4. **对现有功能零影响**：如果没有配置仓库路径，`ChatContext` 的行为与 T123 之前完全一致。Telegram/飞书/桌面扫描/会议等所有现有流程不受影响。

## 三、为什么给出 PASS_WITH_WARNINGS 的评审结果？

### 整体评价

T123 **完整且正确地实现了任务目标**，没有越界，没有伪实现，五重门禁严格且完整，优雅降级设计合理。但有几个不影响正确性但值得记录的小问题，因此给出 `PASS_WITH_WARNINGS`。

### 做对了什么

1. **五重门禁是最严格的过滤**：
   - 门1（contact_id 匹配）+ 门2（status=approved）+ 门3（is_runtime_ready）+ 门4（evidence_validation_status=passed）+ 门5（校验报告确认无缺失引用）。
   - Candidate 记录会在门2被排除。
   - Rejected/frozen/archived 记录会在门2或门3被排除。
   - Missing-evidence 记录会在门4或门5被排除。
   - Not-human-reviewed 记录会在门3（is_runtime_ready 需要 reviewed_by_human=True）被排除。
   - 不存在任何绕过路径。

2. **摘要确实紧凑**：所有文本都经过截断，引用数量受限，记忆事实数量受限。没有整份 JSON 或原始聊天内容。

3. **优雅降级**：5 种状态覆盖所有情况，每种都有清晰的 note 说明原因。没有异常抛出，没有中断现有流程。

4. **路径安全**：`_ensure_within_private_distilled` 确保只能读 `private/distilled/` 内的文件。

5. **容器注入非破坏性**：环境变量可选，默认值保持现有行为。

### 警告（Non-blocking Issues）

| 编号 | 问题 | 严重程度 | 为什么不是 BLOCK |
|---|---|---|---|
| N01 | `contact_id=event.actor_id` 假设入站事件发送者就是联系人，这在当前管线中正确但没有显式合约保证 | 中 | 当前管线中 ID 来源一致（都来自 WeFlow 导出），T130/T131 会验证 |
| N02 | `_load_approved_store_context` 中有死代码（line 185-187），`validation_report_path is None` 条件永远为 False 因为前面已经 early return | 低 | 行为正确（right message shown），只是代码有误导性 |
| N03 | `_build_approved_store_notes` 把 approved claim 文本写入 retrieval notes，这些 notes 可能出现在日志或 debug 输出中 | 低 | claims 来自人工 approved 记录，已截断，符合设计 |
| N04 | `_read_json_model` 用 `except Exception:` 吞掉所有 Pydantic 校验错误 | 低 | 优雅降级模式正确，MVP 阶段可接受 |
| N05 | 没有提交自动化测试 | 顺延 | 与项目惯例一致，T150 补充 |
| N06 | approved memory-only 正向路径没有真实 fixture 验证 | 低 | 代码结构与 approved skill 路径对称，风险低 |

### 没有给出的更差评价

- **不是 BLOCK**：没有阻断性问题。五重门禁正确、摘要紧凑、优雅降级、不破坏现有功能。
- **不是 PASS**：存在死代码（N02）、contact_id 对齐假设（N01）和未验证的代码路径（N06），虽然不影响正确性，但记录下来对后续维护有帮助。
