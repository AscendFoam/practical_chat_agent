# Task T121: Evidence Validator

## Task ID

T121

## Goal

实现 evidence validator，检查 memory/skill claim 的 refs 是否存在并可选检查支持片段。

## Why now

证据链是防幻觉和可审计的核心。

## Allowed files

- `src/practical_chat_agent/services/evidence_validation.py`
- `src/practical_chat_agent/app/main.py`
- `docs/07_handoff.md`

## Forbidden scope

- 不自动改写 claim。
- 不读取未授权 private 输出到可提交目录。

## Inputs to read

- T120 models.
- normalized events/chunks contracts.

## Expected output

- CLI validates refs and reports missing/unsupported refs.
- Missing refs block approval.

## Verification

Run validator on redacted good/bad fixtures.

## Docs to update

- `docs/07_handoff.md`

## Reviewer type

adversarial

