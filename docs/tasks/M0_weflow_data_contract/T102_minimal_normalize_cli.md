# Task T102: Minimal Normalize CLI

## Task ID

T102

## Goal

实现 WeFlow JSONL 到 normalized events 的最小 CLI，只输出到 `private/distilled/`，并保留脱敏 dry-run/report 能力。

## Why now

T100/T101 只是合约，T102 开始把合约落到可运行代码，但仍不做 chunking 和 LLM。

## Allowed files

- `src/practical_chat_agent/services/chatlog_ingestion.py`
- `src/practical_chat_agent/app/main.py`
- `docs/data_contracts/normalized_event_contract.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

## Forbidden scope

- 不输出到可提交目录。
- 不做 LLM 调用。
- 不做 ContactSkill。
- 不接数据库。

## Inputs to read

- T100/T101 outputs.
- existing Typer CLI patterns in `src/practical_chat_agent/app/main.py`.

## Expected output

- CLI 例如 `chatlog-normalize --input private/chat_history --output private/distilled/<run_id>`.
- 输出 `normalized_events.jsonl` 和 `run_report.json`。
- 支持 `--limit` 和 `--dry-run`。
- 不在 stdout 打印原文。

## Verification

运行 dry-run 或 limit 小样本，确认输出只在 `private/distilled/`。

## Docs to update

- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md` if needed

## Reviewer type

adversarial

