# Task T112: Summary And Fact Extraction

## Task ID

T112

## Goal

实现 chunk summary 与 fact extraction 的 LLM/JSON 校验管线，要求每条 claim 都有 evidence refs。

## Why now

这是验证聊天记录能否转化为可审计记忆的核心步骤。

## Allowed files

- `src/practical_chat_agent/services/contact_skill.py`
- `src/practical_chat_agent/services/chatlog_distillation.py`
- `src/practical_chat_agent/app/main.py`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

## Forbidden scope

- 不处理全量数据，先支持 limit/sample。
- 不保存 LLM 输入/输出原文到可提交目录。
- 不接受无 evidence_refs 的 LLM 输出。

## Inputs to read

- T110 chunks.
- T111 schemas.
- existing OpenAI-compatible request style in services.

## Expected output

- CLI can produce `chunk_summaries.jsonl` and `memory_facts.jsonl` under `private/distilled/<run_id>`.
- Evidence refs validator runs before writing accepted facts.
- Failed chunks recorded in run report.

## Verification

Run on a small private sample or mocked redacted sample; manually inspect at least 3 facts.

## Docs to update

- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md` if model unavailable

## Reviewer type

adversarial

