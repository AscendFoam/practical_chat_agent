# Task T110: Conversation Chunker v0

## Task ID

T110

## Goal

实现 ConversationChunker v0，基于联系人、时间间隔和消息数生成 chunks，不使用 LLM。

## Why now

chunk 是后续摘要、事实抽取和 ContactSkill 的输入粒度。

## Allowed files

- `src/practical_chat_agent/services/conversation_chunking.py`
- `src/practical_chat_agent/app/main.py`
- `docs/07_handoff.md`

## Forbidden scope

- 不做 LLM 调用。
- 不做 embedding 语义切分。
- 不输出私密内容到可提交目录。

## Inputs to read

- T102 normalized events output.
- `docs/data_contracts/normalized_event_contract.md`.

## Expected output

- CLI can build `chunks.jsonl` under `private/distilled/<run_id>`.
- 每个 chunk 有 event_ids、time_range、chunking_reason。

## Verification

Run chunker on a limited private sample and inspect run report.

## Docs to update

- `docs/07_handoff.md`

## Reviewer type

normal

