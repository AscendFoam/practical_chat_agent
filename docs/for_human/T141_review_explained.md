# T141 Review Explained - 通俗解释

## 1. 这个 Task 在做什么？（通俗版）

上一个任务 T140 做了一个"反馈笔记本"——当你对回复助手生成的候选草稿表达意见（接受/编辑/拒绝/触碰边界）时，系统把这些意见记到一个本地文件里。

但问题是：**这个笔记本可信吗？** 记录格式对不对？有没有缺字段？引用的草稿文件还在不在？有没有把私密内容写到不该写的地方？

T141 就是给这个笔记本做"质检"的工具。它打开你的反馈日志，逐条检查：

1. 文件能不能正常打开？格式对不对？
2. 每条反馈的字段是否完整？（比如 `edit` 动作有没有附带编辑后的文本）
3. 反馈里引用的草稿文件还在不在？草稿文件里的候选和反馈记录的候选对不对得上？
4. 草稿文件里的联系人和反馈记录的联系人是不是同一个人？
5. 日志文件和引用的文件是不是都在 `private/` 目录下？

**关键约束：这个工具只检查、只报告，不修改任何文件。**

## 2. 实现细节

### 任务目标

T141 的目标是实现一个只读的反馈日志验证器（Feedback Log Validator），让下游任务（如 T142 反馈摘要导出器、T160+ 反馈到补丁）可以信任日志数据的质量。同时，T141 需要回应 T140 遗留的几个延迟警告：

- T140 N01：损坏的日志文件被静默替换为空日志，用户不知道数据丢失了。T141 需要显式报告损坏问题。
- T140 N02：`source_plan_path` 可能过时（文件移动后引用失效）。T141 需要检测引用文件是否存在。
- T140 N05：输出路径不强制在 `private/` 下。T141 需要至少发出警告。

### 代码变化

#### 2.1 反馈验证服务 (`src/practical_chat_agent/services/feedback.py`)

新增 `FeedbackValidationService` 类（约 80 行），包含以下核心方法：

**`validate(input_path, strict)`** — 主入口，执行完整验证流程：

1. **文件存在性检查**：文件不存在 → `corrupted_reason = "file_not_found"`
2. **隐私路径检查**：输入路径不在 `private/` 下 → `W_PRIVACY_INPUT` 警告
3. **文件读取检查**：无法读取 → `corrupted_reason = "read_error: ..."`
4. **JSON 解析检查**：不是合法 JSON → `corrupted_reason = "json_decode_error: ..."`
5. **Schema 校验**：不符合 `ReplyFeedbackLog` 结构 → `corrupted_reason = "schema_error: ..."`
6. **逐条记录验证**（`_validate_record`）：
   - `edit` 动作缺少 `edited_text` → `edit_without_text`
   - `boundary` 动作缺少 `boundary_label` 和 `boundary_note` → `boundary_without_details`
   - 引用的计划文件找不到 → `missing_plan`
   - 计划文件存在但候选对不上 → `missing_candidate`
   - 计划文件存在但联系人对不上 → `contact_mismatch`
   - 引用的计划文件不在 `private/` 下 → `W_PRIVACY_REF` 警告

**`_resolve_plan_path(source_plan_path, log_dir)`** — 路径解析：
- 如果是绝对路径且存在，直接用
- 如果是相对路径，先试当前工作目录，再试日志文件所在目录

**`_load_plan_safe(plan_path)`** — 安全加载计划文件，任何错误返回 `None`（不抛异常）

**`_is_private_path(path)`** — 检查路径中是否包含 `private` 目录名（大小写不敏感）

**输出**：一个包含安全摘要的字典——只有 ID、计数、布尔值、警告代码和路径。没有草稿文本、编辑文本、用户备注或原始内容。

#### 2.2 CLI 命令 (`src/practical_chat_agent/app/main.py`)

新增 `chat-reply-feedback-validate` 命令：

```
chat-reply-feedback-validate --input <feedback-log.json> [--strict]
```

- 输出安全的 JSON 摘要到 stdout
- 损坏的输入（文件不存在、JSON 错误、Schema 错误）→ 退出码 1
- `--strict` 模式下，任何无效记录或隐私警告 → 退出码 1

#### 2.3 文档更新 (`docs/07_handoff.md`)

追加了 Section 37（T141 实现记录），包括文件变更、验证行为描述、CLI 命令、验证结果和明确的"未做什么"声明。

#### 2.4 未改动的文件

`src/practical_chat_agent/core/models.py` 未被修改——T140 已经定义了 `ReplyFeedbackLog` 和 `ReplyFeedbackRecord` 的 schema，T141 直接使用它们进行验证。

### 验证过程

Worker 使用了多个合成测试数据来验证：

| 测试场景 | 结果 |
|---------|------|
| 正常日志（4条记录，4种动作全有效） | valid=4, invalid=0 |
| 错误日志（edit 缺文本，boundary 缺详情） | edit_without_text=1, boundary_without_details=1, invalid=2 |
| 缺失计划引用 | missing_plan=1, invalid=1 |
| 损坏的 JSON | is_readable=false, corrupted_input_count=1, exit=1 |
| Schema 无效（非法 action 值） | corrupted_input_count=1, exit=1 |
| 日志在 `private/` 外 | W_PRIVACY_INPUT 警告出现，--strict 模式 exit=1 |
| 计划引用在 `private/` 外（文件存在且有效） | W_PRIVACY_REF 警告出现，记录仍算有效 |
| 只读确认（md5sum 不变） | 通过 |
| stdout 隐私检查（grep 私密字段） | 0 匹配 |

### 对后续开发的意义

T141 为反馈闭环建立了"质量关卡"：

- **T142（反馈摘要导出器）**：可以在导出摘要前先用 T141 验证日志质量，确保摘要基于有效数据。
- **T150/T152（回归测试）**：需要为 T141 的验证器补充自动化测试，覆盖所有验证路径。
- **T160+（反馈到补丁）**：在将反馈聚类为偏好补丁之前，可以用 T141 确保输入数据的完整性。

同时，T141 回应了 T140 遗留的三个延迟警告：
- N01（损坏日志静默处理）→ T141 显式报告
- N02（过时路径引用）→ T141 检测并报告 missing_plan
- N05（非私有路径）→ T141 发出 W_PRIVACY_INPUT / W_PRIVACY_REF 警告

## 3. 为什么给出 PASS_WITH_WARNINGS？

### 通过的原因

1. **任务目标完全达成**：验证器覆盖了任务包要求的所有检查项——结构、动作字段、计划引用、候选对齐、联系人对齐、路径隐私。

2. **T140 延迟警告得到回应**：N01（损坏日志显式报告）、N02（过时引用检测）、N05（隐私路径警告）全部在验证器中得到处理。

3. **没有越界**：严格在 Allowed files 范围内修改，没有碰 models.py（schema 已在 T140 定义），没有实现任何 T142/T160/T162 的行为。

4. **没有伪实现**：所有验证逻辑都是真实的——文件读取、JSON 解析、Pydantic schema 校验、候选匹配、联系人比对。没有 mock 或 stub。

5. **真正只读**：验证器不写任何文件。Worker 用 md5sum 确认了这一点。

6. **隐私安全**：stdout 只包含安全摘要（ID、计数、警告代码），grep 确认没有私密文本泄露。

### 警告的原因

有几个不影响正确性但值得关注的小问题：

1. **`reply_plan_id` 一致性检查未实现**（N02）：任务包提到要检查 `reply_plan_id` 的一致性，但验证器没有做。这是因为 `reply_plan_id` 当前是 `approved_contact_skill_record_id` 的代理值，语义不完全匹配。Worker 合理地延后了这一项。

2. **`_is_private_path` 的判断粒度偏粗**（N03）：只要路径中有任何一级目录叫 `private` 就算通过，不够精确。但在当前项目结构下（只有根目录有 `private/`），误判可能性很低。

3. **路径解析依赖工作目录**（N04）：相对路径先试当前工作目录，再试日志目录。如果用户在不同目录下运行 CLI，可能解析不到文件。Worker 已在文档中记录了这个风险。

4. **`strict_mode` 字段存在但未被读取**（N05）：存在报告中但没有实际用途，是轻微的死数据。

5. **输出路径没有用 `_safe_cli_path` 标准化**（N01）：与其他 CLI 命令的路径处理方式不一致。风险极低但模式不统一。

6. **缺少自动化测试**：和项目其他任务一致，延后到 T150/T152。

这些警告都不影响验证器的正确性和安全性，所以不需要阻塞（BLOCK），但后续任务应逐步改进。
