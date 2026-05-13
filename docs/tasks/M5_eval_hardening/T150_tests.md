# Task T150: Tests

## Task ID

T150

## Goal

建立 parser、chunker、evidence validator 和 ContactSkill schema 的自动化测试。

## Why now

离线蒸馏涉及隐私和证据链，必须有回归保护。

## Allowed files

- `tests/**`
- `examples/payloads/weflow_redacted_sample.jsonl`
- `pyproject.toml` if test config is needed
- `docs/07_handoff.md`

## Forbidden scope

- 不读取 private 数据作为测试 fixture。
- 不提交真实聊天内容。

## Inputs to read

- implemented services and redacted fixtures.

## Expected output

- pytest suite for parsing, chunking, evidence refs, schema validation.

## Verification

```powershell
$env:PYTHONPATH='src'
pytest
```

## Docs to update

- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md` if pytest cannot run

## Reviewer type

normal

