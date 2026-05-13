# Task T151: Privacy Leakage Tests

## Task ID

T151

## Goal

建立 privacy leakage smoke test，扫描可提交目录中是否出现 private 原文或敏感模式。

## Why now

项目处理私密聊天记录，隐私泄露检查必须自动化。

## Allowed files

- `tests/**`
- `scripts/**` if a standalone scanner is preferred
- `docs/07_handoff.md`

## Forbidden scope

- 不把 private 数据复制到 tests。
- 不扫描 `.env` 内容输出。

## Inputs to read

- redaction rules and source_ref rules.

## Expected output

- Test/scanner catches phone numbers, ID-like strings, raw private filenames if present.
- CI/local command documented.

## Verification

Run privacy smoke test.

## Docs to update

- `docs/07_handoff.md`

## Reviewer type

adversarial

