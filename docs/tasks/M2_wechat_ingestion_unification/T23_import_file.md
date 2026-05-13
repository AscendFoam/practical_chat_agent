# Task T23: WeChat Import File

## Task ID

T23

## Goal

实现微信手工导入文件的最小 parser 和 CLI，把用户导出的脱敏聊天记录送入 ingestion。

## Why now

历史补录不能依赖破解本地数据库，应支持用户可控导入。

## Allowed files

- `src/practical_chat_agent/services/wechat_import.py`
- `src/practical_chat_agent/services/ingestion.py`
- `src/practical_chat_agent/app/main.py`
- `examples/payloads/wechat_import_sample.*`
- `docs/07_handoff.md`

## Forbidden scope

- 不破解微信本地数据库。
- 不读取用户真实聊天导出，除非用户明确提供测试文件。

## Inputs to read

- T20/T21 ingestion work.
- `docs/02_experiment_plan.md` section 7.

## Expected output

- `wechat-import-file --agent-id <id> --path <file>` or dry-run equivalent.
- Parser supports at least one simple structured format documented in examples.

## Verification

Run import against a small脱敏 sample and show ingest stats.

## Docs to update

- `docs/07_handoff.md`

## Reviewer type

normal

