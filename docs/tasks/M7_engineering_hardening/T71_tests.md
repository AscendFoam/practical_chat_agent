# Task T71: Tests

## Task ID

T71

## Goal

建立 tests 目录，覆盖微信 mapper、dedupe、ContactSkill schema、memory lifecycle、policy 和 delivery failure path。

## Why now

系统已进入多模块协作阶段，需要自动化回归保护。

## Allowed files

- `tests/**`
- `pyproject.toml` if test dependency/config required
- `docs/07_handoff.md`

## Forbidden scope

- 不依赖真实微信账号。
- 不在测试中访问真实 `.env` secrets。

## Inputs to read

- implemented services from M1-M6.

## Expected output

- Minimal pytest suite.
- Fixture data is脱敏 and local.

## Verification

```powershell
$env:PYTHONPATH='src'
pytest
```

If pytest not installed, document install requirement.

## Docs to update

- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md` if tests cannot run

## Reviewer type

adversarial

