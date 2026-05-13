# Task T100: WeFlow Schema Profile

## Task ID

T100

## Goal

读取 `private/chat_history/` 中的 WeFlow JSONL 导出，建立字段结构画像和 normalized event 合约，不泄露聊天原文或真实联系人标识。

## Why now

用户已决定跳过微信 SDK/扫描路线，直接基于 WeFlow 导出记录推进长期关系感知 chat agent。任何 parser、chunker、LLM 抽取和 ContactSkill 设计，都必须先建立可靠的数据合约。

## Allowed files

- `docs/data_contracts/weflow_schema_profile.md`
- `docs/data_contracts/normalized_event_contract.md`
- `examples/payloads/weflow_redacted_sample.jsonl`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

可以读取但不可修改/提交：

- `private/chat_history/**`

## Forbidden scope

- 不修改 `src/practical_chat_agent/**`。
- 不复制真实聊天原文到 `docs/`、`examples/`、`tests/`。
- 不写真实联系人姓名、真实原始文件名、手机号、地址、账号 ID。
- 不做 LLM 抽取。
- 不实现 chunker。
- 不新增数据库。
- 不恢复 iLink/微信扫描任务。

## Inputs to read

- `docs/02_experiment_plan.md`
- `docs/04_task_board.md`
- `docs/reference/gpt关于后续chat agent设计的思路.md`
- `docs/deep_research_reports/对话记录驱动的长期关系感知chat agent.md`
- `private/chat_history/**` 的 JSONL 字段结构和统计信息

## Expected output

### `docs/data_contracts/weflow_schema_profile.md`

必须包含：

- 文件数量、总行数、可解析 JSON 行数、失败行数。
- 字段名集合、字段类型统计、字段出现率。
- 消息类型字段候选。
- 时间戳字段候选和格式观察。
- 发送者/接收者/方向字段候选。
- 媒体/系统/撤回/引用等字段候选。
- 隐私风险字段清单。
- 不包含真实聊天原文或真实联系人名。

### `docs/data_contracts/normalized_event_contract.md`

必须包含：

- normalized event JSON schema 草案。
- event_id 生成规则。
- source_ref/raw_ref 规则。
- sender_role 判定规则。
- timestamp 解析规则。
- message_type 映射规则。
- 脱敏原则。
- 当前未决问题。

### `examples/payloads/weflow_redacted_sample.jsonl`

必须是手工脱敏或合成的最小样例：

- 2 到 5 行。
- 能代表主要字段结构。
- 不含真实内容。

## Verification

至少运行一个只输出统计、不输出原文的本地检查命令。可以用 PowerShell 或短 Python 脚本，但不要把脚本提交到主仓库，除非 Captain 另行安排。

验证要点：

- 文档中没有真实聊天原文。
- 文档中没有真实联系人文件名。
- sample fixture 是脱敏/合成内容。
- JSONL 样例可被 `python -m json.tool` 或等价方式逐行解析。

## Docs to update

- `docs/data_contracts/weflow_schema_profile.md`
- `docs/data_contracts/normalized_event_contract.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md` if needed

不要把 `docs/04_task_board.md` 的 T100 标成完成；由 Captain 在 review 后更新。

## Reviewer type

adversarial

