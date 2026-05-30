# exports

会议纪要导出目录。每次会议会话可按不同模板格式生成多份导出文件。

## 命名规则

文件名格式：`meeting_session_{session_id}.{template}.md`

- `session_id` — 会话唯一标识
- `template` — 所用模板名称（`brief` / `standard` / `full` / 自定义）

## 文件说明

本目录以 `meeting_session_2c66c620dd7c4eab` 为例展示了不同模板的输出：

| 文件 | 模板 | 语言 | 说明 |
|------|------|------|------|
| `*.md` | 默认 | 中文 | 基础中文会议纪要 |
| `*.brief.md` | brief | 中文 | 精简版中文纪要（背景、结论、行动项、摘录） |
| `*.standard.md` | standard | 中文 | 标准版中文纪要 |
| `*.standard.v2.md` | standard v2 | 中文 | 标准模板的迭代版本 |
| `*.full.md` | full | 中文 | 完整版纪要，含逐字稿全文 |
| `*.history_test.md` | 测试 | 英文 | 开发调试用的英文格式模板 |

## 用途

- 归档会议内容，便于回溯
- 作为后续任务拆解和进度跟踪的输入
- 作为 agent 长期记忆的事实来源
