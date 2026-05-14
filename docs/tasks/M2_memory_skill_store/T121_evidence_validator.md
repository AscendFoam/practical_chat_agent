# Task T121: Evidence Validator

## Task ID

T121

## Goal

实现离线 evidence validator，用于校验 T120 memory/skill store records 的 `evidence_refs` 是否存在、是否可追溯，并明确哪些状态可以或不可以进入后续 approval/runtime 路径。

## Why now

T120 已建立 memory/skill file store、review metadata、source metadata 和 human-review-first `is_runtime_ready()` gate。下一步在做 T122 review/approve/export CLI 之前，必须先有独立 validator 证明：

- `evidence_refs` 没有丢失或指向不存在对象。
- Missing evidence 会阻止 approval。
- `rejected` / `frozen` / `archived` 不会被误认为可进入 prompt/runtime。
- Validator report 不泄露私密聊天原文。

## Allowed files

- `src/practical_chat_agent/services/evidence_validation.py`
- `src/practical_chat_agent/app/main.py`
- `docs/07_handoff.md`

如果确实需要复用 T120 模型，优先从现有 `src/practical_chat_agent/core/models.py` import，不要修改模型文件；只有发现 blocking 级模型缺口时才停止并向 Captain 说明，不要自行扩大 allowed files。

## Forbidden scope

- 不自动 approve。
- 不自动改写 claim、summary、skill 或 memory。
- 不实现完整 review/approve/export CLI；那是 T122。
- 不接数据库，不做 migration，不引入向量数据库或 pgvector。
- 不做 runtime prompt 注入，不改 `ChatContextAssembler`，不把 candidate 接入 runtime。
- 不调用 LLM，不做 semantic entailment 评分。
- 不读取 `private/chat_history/` 原始聊天记录。
- 不把 `private/distilled/**` 的真实内容、聊天原文、真实文件名、真实联系人名或平台 ID 写入 docs/examples/tests/stdout。

## Inputs to read

- `docs/02_experiment_plan.md`
- `docs/04_task_board.md`
- `docs/06_eval_protocol.md`
- `docs/07_handoff.md`
- `docs/review/T120_review.md`
- `docs/tasks/M2_memory_skill_store/T120_file_store_models.md`
- `src/practical_chat_agent/core/models.py`
- `src/practical_chat_agent/services/contact_skill.py`
- Existing contracts:
  - `docs/data_contracts/normalized_event_contract.md`
  - `docs/data_contracts/distillation_output_contract.md`

## Expected output

Implement a small validator service and CLI path that can validate T120 store artifacts under `private/distilled/**`.

Minimum service behavior:

- Load `memory_fact_store.json` and/or `contact_skill_store.json` using T120 store models or service helpers.
- Load available evidence indexes from the same run directory when present:
  - `normalized_events.jsonl`
  - `chunks.jsonl`
  - `chunk_summaries.jsonl`
  - `memory_facts.jsonl`
  - `contact_skill.candidate.json`
- Build an evidence id index that includes event ids, chunk ids, summary ids if present, memory ids, and contact skill ids where applicable.
- Validate every record's `evidence_refs`.
- Preserve provenance in report output: record id, artifact type, status, missing refs, checked refs, and approval/runtime blocking reason.
- Enforce status rules:
  - `candidate` can be evidence-checked but is not approval-ready by default.
  - `approved` with missing refs is blocking.
  - `rejected`, `frozen`, and `archived` are never runtime-ready.
  - Runtime readiness must still require T120's human-review-first gate.

Minimum CLI behavior:

- Add a Typer command to `src/practical_chat_agent/app/main.py`.
- Suggested name: `chatlog-validate-evidence`.
- Input path must be confined to `private/distilled/**`.
- Output report should default to `private/distilled/<run_id>/evidence_validation_report.json` unless `--dry-run` is used.
- Stdout should only print counts and safe relative paths, never chat text or raw private content.

## Verification

Run compile verification:

```powershell
& 'C:\ProgramData\anaconda3\envs\practical-chat-agent\python.exe' -m compileall src/practical_chat_agent/services/evidence_validation.py src/practical_chat_agent/app/main.py
```

Run validator on at least one safe good case and one safe bad case:

- Good case: existing synthetic/private T120 store fixture or a newly created private synthetic fixture under `private/distilled/`.
- Bad case: private synthetic fixture with one missing `evidence_ref`.
- Confirm good case has zero missing refs.
- Confirm bad case reports missing refs and blocks approval/runtime.
- Do not commit the generated private fixture or report.

If a local fixture must be created, create it only under `private/distilled/t121_*` and mention it in handoff without copying contents into docs.

## Docs to update

- `docs/07_handoff.md`

The handoff update should include:

- What service/CLI was added.
- Which private synthetic fixture or safe sample was used.
- Compile command and validator command outcomes.
- Any remaining risks or assumptions.

Do not update `docs/04_task_board.md`, `docs/05_decision_log.md`, or `docs/08_risks_and_open_questions.md`; Captain updates those after review.

## Reviewer type

adversarial

Reviewer should specifically check:

- No private data leakage.
- No auto-approve or runtime integration.
- Missing refs block approval/runtime.
- Rejected/frozen/archived cannot pass runtime readiness.
- Validator actually uses T120 store records and does not silently drop evidence refs.
