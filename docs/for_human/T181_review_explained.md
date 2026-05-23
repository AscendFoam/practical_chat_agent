# T181 Review Explained

## 1. 这个 Task 在做什么？（通俗版）

T181 是"给聊天助手加一个可选的 AI 草稿生成器"的第一步。

**背景故事**：项目里已经有一个「确定性回复规划器」（ReplyPlanner），它根据预设模板和规则生成 3 个回复候选。这个规划器很安全、可预测，但不够灵活。

T181 的任务是：**做一个独立的命令行工具**，让你可以把自己的聊天上下文（ChatContext）发给一个大语言模型（比如 GPT-4、DeepSeek 等），让 AI 帮忙生成回复草稿。

但有几个关键限制：

- **不是默认行为** — 这个工具是 opt-in 的，你需要主动调用它
- **不改原有功能** — 原来的确定性规划器完全不受影响
- **输出必须经过检查** — AI 生成的草稿要经过 7 道检查才能写文件
- **只能读安全的上下文** — 不能读原始聊天记录，只能读已经脱敏/摘要过的信息
- **不能冒充联系人** — 生成的草稿必须是"用户视角"，不能假装是对方在说话

简单说：**这是一个可选、离线、私密的 AI 草稿生成工具，输出要经过严格检查，不会影响现有功能。**

## 2. 实现详解

### 2.1 修改了哪些文件？

| 文件 | 变更类型 | 说明 |
|------|---------|------|
| `core/models.py` | 修改 | 新增 5 个模型：LLMGeneratorType、LLMGenerationMetadata、LLMReplyPlanRefusal、LLMReplyPlanCandidate、LLMReplyPlan |
| `services/llm_reply_generator.py` | **新建** | 核心服务：生成器服务 + 验证器 |
| `app/main.py` | 修改 | 新增 `chat-reply-generate-llm` CLI 命令 |
| `tests/test_llm_reply_generator.py` | **新建** | 26 项测试 |
| `docs/07_handoff.md` | 修改 | 添加 T181 完成记录 |

### 2.2 新增模型（core/models.py）

- **`LLMGeneratorType`** — 字面量类型：`"template_deterministic"` 或 `"llm_generated"`，用于标记候选是模板生成还是 AI 生成
- **`LLMGenerationMetadata`** — 生成元数据：provider 名称、模型名、温度、prompt 哈希、生成时间、延迟（毫秒）
- **`LLMReplyPlanRefusal`** — 结构化拒绝：当 AI 不可用或出错时，返回一个包含拒绝码、原因和是否可重试的对象
- **`LLMReplyPlanCandidate`** — AI 生成候选草稿：继承自 `ReplyPlanCandidate`，增加了 `generator_type` 字段
- **`LLMReplyPlan`** — AI 回复计划：包含生成类型、ID、联系人 ID、上下文快照、元数据、候选列表和拒绝信息

### 2.3 生成器服务（llm_reply_generator.py）

**LLMReplyGeneratorService** 的工作流程：

1. **可用性检查** — 检查 API key 和 base URL 是否配置，未配置直接返回拒绝
2. **构建输入** — 从 ChatContext 的 approved_store_context、derived_brief_context、approved_patch_context 等安全字段中提取压缩上下文
3. **调用 AI 供应商** — 通过 OpenAI-compatible API 调用，复用项目中已有的 `_post_json` / `_parse_json_content` 模式
4. **解析响应** — 把 AI 返回的 JSON 解析为候选列表
5. **构建候选** — 把原始候选人转换为 `LLMReplyPlanCandidate` 对象
6. **确定性后验证** — 调用 `LLMReplyPlanValidator` 进行 7 项检查

**LLMReplyPlanValidator** 的 7 项检查（逐候选）：

| # | 检查项 | 说明 |
|---|--------|------|
| 1 | `draft_text` 非空 | 草稿文本不能为空或空白 |
| 2 | `supporting_context_refs >= 1` | 必须有至少 1 个上下文引用 |
| 3 | `boundary_reminders >= 1` | 必须有至少 1 个边界提醒 |
| 4 | ref_type 在允许集合中 | 引用类型必须是预定义的 6 种之一 |
| 5 | `generator_type == "llm_generated"` | 生成器类型必须正确 |
| 6 | 无隐私泄露 | 草稿不能逐字照搬输入上下文文本 |
| 7 | 无冒充模式 | 草稿不能使用"我建议"、"对方会"等冒充表达 |

### 2.4 CLI 命令（app/main.py）

`chat-reply-generate-llm` 支持三个参数：

- `--input`（必需）— 输入的安全的 ChatContext JSON 文件
- `--output`（必需）— 输出路径（建议放在 `private/` 下）
- `--dry-run`（可选）— 只检查可用性，不调用 AI

**stdout 输出规则**：只输出安全元数据（action、路径、contact_id、候选数、generator_type、拒绝码等），不输出草稿文本。

**输出文件规则**：即使是拒绝结果，也会写入输出文件（包含拒绝码和原因），确保调用方始终能找到一个合法的 JSON 文件。

### 2.5 测试覆盖（26 项）

- **验证器接受有效候选**（3 测试）：单个有效、三个有效、空列表
- **验证器拒绝无效候选**（10 测试）：空文本、缺 refs、缺边界提醒、无效 ref 类型、非 llm_generated 类型、冒充（英文 I would/he would、中文"对方会"）、隐私泄露
- **排序重编号**（1 测试）：过滤后 rank 重新编号为 1..N
- **生成器拒绝行为**（3 测试）：disabled 返回拒绝、无 API key 返回拒绝、拒绝时元数据仍然存在
- **生成器构建候选**（4 测试）：从原始输出构建、跳过空文本、默认 refs、收集上下文文本、构建源快照
- **CLI 集成**（4 测试）：dry-run 打印可用性、无效 JSON 被拒绝、输出文件始终写入、输出是有效 JSON

### 2.6 对后续开发的意义

1. **T182（验证器提取/硬化）** — 可以把 LLMReplyPlanValidator 提取为独立模块，扩展冒充检测模式，实现输入大小预算检查
2. **T183（混合规划器）** — 在验证器就绪后，可以尝试将 AI 生成的候选与确定性候选合并排序
3. **T184（评估）** — 有了 AI 生成能力，可以在 holdout 场景中评估 AI 草稿的质量

这是 M7（LLM-Assisted ReplyPlanner）的实质性的第一步，但严格保持在"可选离线工具"的边界内。

## 3. 为什么给出 PASS_WITH_WARNINGS？

### 任务目标都完成了吗？✅

- ✅ 独立的离线 CLI — `chat-reply-generate-llm`
- ✅ 调用 AI 供应商 — OpenAI-compatible API
- ✅ 结构化拒绝 — 供应商不可用时优雅降级
- ✅ 确定性后验证 — 7 项检查，候选过滤
- ✅ 安全 stdout — 仅元数据
- ✅ 不修改现有规划器 — `chat-reply-plan` 不受影响
- ✅ 不修改运行时状态 — 不写 ContactSkill/Memory/数据库
- ✅ 不自称默认 — 需要主动调用
- ✅ 26 项测试，零回归

### 为什么不是 BLOCK？

没有功能性问题、没有安全漏洞、没有伪造实现、没有破坏现有功能。

### 为什么不是 PASS（无警告）？

有 9 个非阻塞问题（5 个代码层面的注意事项 + 4 个测试覆盖缺口），具体见 review 文档。其中最值得注意的是：

1. **越界修改了允许文件列表外的文件**（settings.json 和 AI_coding_workflow.md）— 虽然之前的任务也有类似情况且都被接受，但严格来说超出了 scope
2. **候选的 evidence refs 都是默认值** — 验证器检查 refs 的存在性，但因为生成器总是填充默认的 `policy_boundary` ref，这个检查对 AI 输出其实不构成有效约束
3. **隐私泄露检测只是子串匹配** — 只能防逐字照搬，不能防改写型泄露
4. **输入大小预算检查未实现** — `INPUT_TOO_LARGE` 拒绝码存在但从未触发

这些警告都不影响当前阶段的安全性和可用性，适合推迟到 T182 解决。

## 4. 对 Worker 文档的补充

Worker 已经在 `docs/07_handoff.md` 第 82 节中写了详细的 T181 完成记录，包含：

- CLI 名称和文件/输出合约
- LLM 专属逻辑位置
- 确定性后验证机制
- 供应商/运行时假设验证状态
- T182 可以提取或硬化的内容

无需补充。记录准确、完整，与实际情况一致。
