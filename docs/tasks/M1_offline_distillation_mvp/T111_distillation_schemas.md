# Task T111: Distillation Schemas

## Task ID

T111

## Goal

定义 ChunkSummary、MemoryFactCandidate、ContactSkillCandidate 的 Pydantic schema 和 JSON contract。

## Why now

LLM 抽取前必须先有强格式约束和 evidence_refs 要求。

## Allowed files

- `src/practical_chat_agent/core/models.py`
- `docs/data_contracts/distillation_output_contract.md`
- `docs/07_handoff.md`

## Forbidden scope

- 不调用 LLM。
- 不写数据库 migration。

## Inputs to read

- `docs/02_experiment_plan.md`
- `docs/reference/gpt关于后续chat agent设计的思路.md`

## Expected output

- Schema includes evidence_refs, confidence, sensitivity, status.
- ContactSkillCandidate explicitly disallows persona clone/impersonation usage.

## Verification

Compile Python files if models are added.

## Docs to update

- `docs/data_contracts/distillation_output_contract.md`
- `docs/07_handoff.md`

## Reviewer type

adversarial

