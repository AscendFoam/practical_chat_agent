# Handoff

## Captain Current State Override 2026-05-23 (T183 Review Decision)

- T183 review decision: `PASS_WITH_WARNINGS`.
- T183 warning disposition:
  - Accepted: N01 `.claude/settings.json` workspace-artifact overrun.
  - Deferred: N02 no committed test exercises the valid LLM-candidate merge success path, M01 no end-to-end hybrid success test, M02 no explicit reranked-order assertion after merge.
  - Rejected: none.
- T183 is complete as the opt-in hybrid planner integration M7 task.
- Current Unique Task: T184 Planner Holdout Eval.
- Current task package: `docs/tasks/M7_llm_reply_planner/T184_llm_planner_holdout_eval.md`.
- T184 must stay evaluation-only: no planner code changes, no send/platform integration, no raw private content in committed artifacts, and no quality claim without evidence.
- T184 may compare template vs hybrid outputs on anonymized scenarios, but it must distinguish private smoke evidence from committed tests and must not overclaim quality without holdout data.

## Captain Current State Override 2026-05-23 (T182 Review Decision)

- T182 review decision: `PASS_WITH_WARNINGS`.
- T182 warning disposition:
  - Accepted: N02 `.claude/settings.json` workspace-artifact overrun.
  - Deferred: N01 broken `INPUT_TOO_LARGE` preflight call-site bug, M01 missing regression test for the `INPUT_TOO_LARGE` refusal path.
  - Rejected: none.
- T182 is complete as the shared validator-hardening M7 task.
- Current Unique Task: T183 Hybrid ReplyPlanner.
- Current task package: `docs/tasks/M7_llm_reply_planner/T183_hybrid_reply_planner.md`.
- T183 must stay opt-in, additive, and review-only: no default LLM mode, no ReplyPlanner runtime mutation that bypasses gating, and no send/platform integration.
- T183 may integrate optional LLM candidates only behind explicit controls and must preserve shared deterministic validation, compact-context boundaries, and policy/boundary review.

## Captain Current State Override 2026-05-23 (T181 Review Decision)

- T181 review decision: `PASS_WITH_WARNINGS`.
- T181 warning disposition:
  - Accepted: N01 allowed-files overrun for `.claude/settings.json` and `docs/reference/AI_coding_workflow.md`, N02 default `policy_boundary` refs instead of LLM-provided supporting refs, N03 redundant `validate_ranks` call.
  - Deferred: N04 substring-only privacy leak detection, N05 dead `INPUT_TOO_LARGE` refusal path, M01 `_build_llm_input` output-shape coverage gap, M02 `_parse_provider_response` error-path coverage gap, M03 missing generator-to-validator pipeline test, M04 missing CLI stdout privacy regression test.
  - Rejected: none.
- T181 is complete as the first executable M7 task.
- Current Unique Task: T182 Candidate Validator.
- Current task package: `docs/tasks/M7_llm_reply_planner/T182_candidate_validator.md`.
- T182 must stay validator-only, additive, and private-by-default: no new candidate generation path, no hybrid planner behavior, no default LLM mode, no ReplyPlanner runtime mutation, and no send/platform integration.
- T182 may harden shared deterministic validation, explicit input-budget refusal handling, and regression coverage, but it must preserve the compact-context boundary and review-only gating.

## Captain Current State Override 2026-05-23 (T180 Review Decision)

- T180 review decision: `PASS`.
- T180 is complete as the contract-only M7 opening task.
- Current Unique Task: T181 LLM Candidate Offline CLI.
- Current task package: `docs/tasks/M7_llm_reply_planner/T181_llm_candidate_offline_cli.md`.
- T181 must stay offline, opt-in, additive, and private-output-only: no hybrid planner behavior, no default LLM mode, no ReplyPlanner mutation, and no send/platform integration.
- T181 may consume only safe synthetic/redacted `ChatContext` JSON that already respects the T123/T164/T174 compact-context boundary.
- T181 must output a validated private `LLMReplyPlan` artifact or structured refusal; it must not bypass deterministic validation or review-only gating.

## Captain Current State Override 2026-05-23 (M6 Review)

- Gate M6: `Allow`.
- Current Unique Task: T180 LLM Candidate Generator Contract.
- Current task package: `docs/tasks/M7_llm_reply_planner/T180_llm_candidate_contract.md`.
- M6 is complete: approved `ContactSkill` now supports additive decomposition through committed design, schema, projection, and context integration layers without breaking fallback behavior.
- T180 is contract-only: no LLM calls, no ReplyPlanner behavior changes, no platform/send integration, no runtime mutation, and no deprecation claim.
- Any M7 work must preserve review-only mode, privacy boundaries, and the compact-context contracts from T123/T164/T174.

## Captain Current State Override 2026-05-23 (T174 Review Decision)

- T174 review decision: `PASS`.
- T174 is complete as an additive context-integration-only task.
- Current Unique Task: T180 LLM Candidate Generator Contract.
- Current task package: `docs/tasks/M7_llm_reply_planner/T180_llm_candidate_contract.md`.
- M6 may now close after milestone review; no additional M6 worker repair pass is needed.
- T174 preserved `ApprovedContactSkillBrief` fallback, kept derived briefs additive, and coexisted cleanly with the T164 approved-patch compact-context path.

## Captain Current State Override 2026-05-23 (T173 Review Decision)

- T173 review decision: `PASS`.
- T173 is complete as an additive projection-only task.
- Current Unique Task: T174 Derived Briefs Context Integration.
- Current task package: `docs/tasks/M6_contactskill_decomposition/T174_derived_briefs_context.md`.
- M6 may now enter context integration work, but planner behavior and approved-store semantics remain unchanged.
- T174 is context-integration-only: no planner behavior changes, no ContactSkill mutation, no migration, no new storage, and no deprecation claim.
- T174 must preserve the `ApprovedContactSkillBrief` fallback, keep derived briefs additive, and coexist cleanly with the T164 approved-patch compact-context path.

## Captain Current State Override 2026-05-23 (T172 Review Decision)

- T172 review decision: `PASS`.
- T172 is complete as an additive schema-only task.
- Current Unique Task: T173 ContactSkill Projection Service.
- Current task package: `docs/tasks/M6_contactskill_decomposition/T173_projection_service.md`.
- M6 may now enter lazy projection work, but `ChatContext` and runtime behavior remain unchanged until T174.
- T173 is projection-only: no `ChatContext` integration, no `ReplyPlanner` or policy runtime changes, no ContactSkill mutation, no migration, no new storage, and no deprecation claim.
- T173 must preserve thin policy-brief evidence faithfully, compute sensitivity explicitly, and own the deterministic `important_event_summaries` formatting rule.

## Captain Current State Override 2026-05-23 (T171 Review Decision)

- T171 review decision: `PASS`.
- T171 is complete as an additive schema-only task.
- Current Unique Task: T172 CommunicationPolicyBrief + BoundaryProfileBrief Schemas.
- Current task package: `docs/tasks/M6_contactskill_decomposition/T172_communication_policy_brief_schema.md`.
- M6 may continue with schema work, but projection and runtime behavior remain unchanged until T173-T174.
- T172 is schema-only: no projection service, no `ChatContext` integration, no `ReplyPlanner` or policy runtime changes, no ContactSkill mutation, no migration, and no deprecation claim.
- T172 must formalize sensitivity reduction, important-event ownership, and derived-brief versioning strategy.
- T173 must later make the `unknown` -> `None` communication-style conversion and `relationship_state_summary` projection rules explicit.

## Captain Current State Override 2026-05-22 (T170 Review Decision)

- T170 review decision: `PASS`.
- T170 is complete as a design-only compatibility task.
- Current Unique Task: T171 PartnerPersonaBrief Schema.
- Current task package: `docs/tasks/M6_contactskill_decomposition/T171_partner_persona_brief_schema.md`.
- M6 may now enter additive schema work, but runtime behavior remains unchanged until T173-T174.
- T171 is schema-only: no projection service, no `ChatContext` integration, no `ReplyPlanner` or policy runtime changes, no ContactSkill mutation, no migration, and no deprecation claim.
- T171 must resolve `PartnerPersonaBrief.communication_style_snapshot` typing and keep `source_skill_record_id` / evidence ownership explicit.
- T172 must later formalize the boundary sensitivity reduction rule and any boundary semantics implied by approved patch hints.

## Captain Current State Override 2026-05-22 (T164 Review Decision)

- T164 review decision: `PASS_WITH_WARNINGS`.
- T164 warning disposition:
  - Accepted: N01 `.claude/settings.json` is a workspace artifact rather than a T164 scope violation, N02 duplicated `_compact_text` is low-risk refactor debt, N03 `ApprovedPatchContext.status` reuses a slightly broader enum than strictly necessary, N04 per-assemble `ApprovedPatchContextService()` instantiation is low-impact for the current offline workflow, N05 handoff test wording was inaccurate and is corrected here, N06 carrying deterministic `supporting_cluster_ids` through compact briefs is safe.
  - Deferred: M01 missing explicit frozen/archived exclusion tests, M02 missing `ChatContextAssembler` approved-patch path integration test, M03 missing empty/whitespace `behavior_instruction` edge-case coverage.
  - Rejected: none.
- Current Unique Task: T170 ContactSkill Decomposition Design.
- Current task package: `docs/tasks/M6_contactskill_decomposition/T170_decomposition_design.md`.
- M5 is functionally complete within approval-gated, review-only, non-mutating constraints.
- T170 is design-only: no code edits, no ContactSkill behavior changes, no migration, and no deprecation claim.
- Any M6 design must preserve the existing T120-T164 pipeline and keep ContactSkill runnable as the compatibility fallback aggregate.

## Captain Current State Override 2026-05-22 (T163 Review Decision)

- T163 review decision: `PASS_WITH_WARNINGS`.
- T163 warning disposition:
  - Accepted: N05 `.claude/settings.json` is workspace noise rather than a task-scope violation.
  - Deferred: N01 the contract still overclaims deterministic `patch_id` behavior, N02 no committed automated tests yet cover `PatchReviewService` / `chat-feedback-review-patch`, N03 write-back to the input file by default can risk in-place corruption on write failure, N04 review history can grow without bound.
  - Rejected: none.
- Current Unique Task: T164 Approved Patch Compact Context.
- Current task package: `docs/tasks/M5_feedback_to_patch/T164_approved_patch_context.md`.
- M5 remains approval-gated, compact, review-only, and non-mutating.
- T164 may consume only approved, runtime-ready patches into `ChatContext`, but it may not inject candidate/rejected/frozen/archived patches, mutate ContactSkill/Memory, or add outbound behavior.

## Captain Current State Override 2026-05-18 (T162 Review Decision)

- T162 review decision: `PASS_WITH_WARNINGS`.
- T162 warning disposition:
  - Accepted: N05 `.claude/settings.json` is workspace noise rather than a task-scope violation.
  - Deferred: N01 the patch contract still overclaims deterministic `patch_id` behavior, N02 raw `input_path` remains present in proposal stdout/output, N03 no committed automated proposal tests yet exist, N04 malformed cluster input with empty `contact_id` can still crash proposal generation instead of being skipped defensively.
  - Rejected: none.
- Current Unique Task: T163 Patch Review CLI.
- Current task package: `docs/tasks/M5_feedback_to_patch/T163_patch_review_cli.md`.
- M5 remains deterministic, review-only, and non-mutating.
- T163 may record human review decisions on `PreferencePatchCandidate` proposals, but it may not auto-approve, auto-apply, inject approved patches into runtime context, mutate ContactSkill/Memory, or add outbound behavior.

更新日期：2026-05-17

更新日期：2026-05-16

## Captain Current State Override 2026-05-18

- T161 review decision: `PASS_WITH_WARNINGS`.
- T161 warning disposition:
  - Accepted: N01 `reason_tag_summary` naming mismatch is acceptable for now because the contract documents the actual meaning, N03 `counts_by_approach_label` may safely degrade when plan files are unavailable, N05 `.claude/settings.json` is workspace noise rather than a T161 scope violation.
  - Deferred: N02 no committed automated tests yet cover the clusterer, N04 raw `input_path` remains present in cluster stdout/output and stays tracked as cross-task path/privacy debt.
  - Rejected: none.
- Current Unique Task: T162 Patch Proposal CLI.
- Current task package: `docs/tasks/M5_feedback_to_patch/T162_patch_proposal_cli.md`.
- M5 remains deterministic, review-only, and non-mutating.
- T162 may generate candidate-only `PreferencePatchCandidate` records from T161 cluster outputs, but it may not review them, approve them, apply them, or inject them into runtime context.

## Captain Current State 2026-05-16

- T133 review decision: `PASS_WITH_WARNINGS`.
- T133 warning disposition: N01/N02/N03/N04/N05 all accepted; no deferred or rejected warnings.
- Gate M3: `Conditional`, documented in `docs/review/M3_review.md`.
- Current Unique Task: T140 Feedback Schema CLI.
- Current task package: `docs/tasks/M4_feedback_loop/T140_feedback_schema_cli.md`.
- M4/T140 may proceed only under review-only constraints: no auto-send, no realtime platform integration, no LLM drafting expansion, no automatic ContactSkill/Memory mutation, and no relationship-aware maturity claim.
- T150 must add committed regression tests covering ReplyPlanner structure, boundary sensitivity, thin context, false positives, subtle false negatives, privacy leakage, contact alignment, and ranking.
- Roadmap update: `docs/reference/gpt的后续设计思路(更新版).md` is accepted as directionally aligned, but milestone/task ordering has been revised. M4 is feedback capture/validation/summary only; M4.5 is regression hardening; feedback-to-patch, ContactSkill-compatible decomposition, LLM planner, RelationshipState, MemoryRetriever, BehaviorPlanner, Feishu, and WeChat are delayed behind gates.

## 1. 当前状态

项目路线已切换。

旧路线：

- T00：WeChatBot/iLink SDK 安装和二维码阶段探测，review `PASS`。
- T01：登录/session 验证，review `BLOCK`。
- 用户已决定不修 T01，不再推进微信 SDK 登录、扫描或聊天记录读取路线。

新路线：

- 用户已通过 WeFlow 工具导出聊天记录。
- 私密数据位于 `private/chat_history/`，受 `.gitignore` 保护。
- 下一阶段直接做“对话记录驱动的长期关系感知 chat agent”。
- 当前目标是离线蒸馏 MVP：JSONL -> normalized events -> chunks -> memory facts -> ContactSkill -> review -> relationship-aware reply planner。
- T100 worker 已产出 schema profile、normalized event contract 和合成脱敏 fixture，并通过 reviewer `PASS`。
- Captain 已将 T100/T101/T102/T103/T110/T111/T112/T113/T114/T120/T121/T122/T123/T130/T131/T132 标记完成，Gate M1 = `Conditional`，Current Unique Task 推进到 T133。
- T101 worker 已产出隐私脱敏规则、source_ref 规则和补充了 `source_ref/raw_ref` 预览形态的合成 fixture，并通过 reviewer `PASS`。
- T102 worker 已产出最小 normalize CLI，并完成 dry-run 与 limit 小样本验证，reviewer 判定 `PASS`。
- T103 milestone review 已接受 Gate M0 = `Conditional`，允许进入 M1；T110 conversation chunker v0、T111 distillation schemas 和 T112 summary/fact extraction 均已通过 reviewer `PASS`，T113 ContactSkill builder 已通过 reviewer `PASS_WITH_WARNINGS`，T114 确认 Gate M1 = `Conditional`。
- T120 file store models 已通过 reviewer `PASS_WITH_WARNINGS`，允许进入 T121。
- T121 evidence validator 已通过 reviewer `PASS_WITH_WARNINGS`，允许进入 T122。
- T122 skill review CLI 已通过 reviewer `PASS_WITH_WARNINGS`，允许进入 T123。
- T123 context integration 已通过 reviewer `PASS_WITH_WARNINGS`，T130 ReplyPlan schema 已通过 reviewer `PASS_WITH_WARNINGS`，T131 ReplyPlanner 已通过 reviewer `PASS_WITH_WARNINGS`，T132 Reply Policy 已通过 reviewer `PASS_WITH_WARNINGS`，允许进入 T133。

## 2. 当前唯一任务

T133: 用历史 holdout 场景评估回复自然度和边界遵守。

任务包：`docs/tasks/M3_relationship_reply_planner/T133_holdout_eval.md`

状态：T132 已通过 `PASS_WITH_WARNINGS`，ReplyPlanner 已具备 review-only contract wiring 和 policy/boundary 风险层。T133 只做匿名 holdout eval 与 Gate M3 判断；不修改 planner 代码，不提交 holdout 原文，不自动发送、不接数据库、不引入向量数据库、不回读或泄露原始聊天记录。

## 3. T100 完成记录

- `docs/data_contracts/weflow_schema_profile.md`
- `docs/data_contracts/normalized_event_contract.md`
- `examples/payloads/weflow_redacted_sample.jsonl`

worker 侧当前已确认的高信号结论：

- 4 个 WeFlow JSONL 文件共 38,289 行，全部可解析，无坏行。
- 顶层行类型稳定分为 `header`、`member`、`message` 三类。
- 真正需要进入 normalized event 的是 `_type=message` 行，共 38,253 条。
- `timestamp` 稳定为 Unix epoch seconds。
- `type` 是消息类型主候选字段，其中 `0`、`7`、`25`、`80` 占绝大多数。
- `replyToMessageId` 可作为引用链路候选；`chatRecords` 可作为转发聊天记录候选。
- 脱敏/合成样例已生成，不包含真实原文、真实联系人姓名或真实文件名。

Reviewer 结论：

- `docs/review/T100_review.md` verdict 为 `PASS`。
- N01 accepted：Q100/Q104 关闭依据更新为 “T100 worker draft + review PASS”。
- N02 deferred：type=80/chatRecords fixture 覆盖留给 T102/T150。
- N03 deferred：event_id 的 SHA-1/SHA-256 取舍留给 T102。

## 4. T101 完成记录

- `docs/data_contracts/privacy_redaction_rules.md`
- `docs/data_contracts/source_ref_rules.md`
- `examples/payloads/weflow_redacted_sample.jsonl` 已加入 `eventIdPreview`、`sourceRefPreview`、`rawRefPreview`

Reviewer 结论：

- `docs/review/T101_review.md` verdict 为 `PASS`。
- N01 deferred：type=80/chatRecords fixture 覆盖继续留给 T102/T150。
- N02 accepted：fixture preview hex 值可作为注释占位，不要求返修。
- N03 deferred：结构化替换 token 与实际脱敏需求的对齐交给 T102 实现时校验。

T102 必须遵守：

- `docs/data_contracts/privacy_redaction_rules.md` 的 Field Handling Matrix。
- `docs/data_contracts/source_ref_rules.md` 的 Allowed Public Shape。
- normalize 输出只能进入 `private/distilled/`。
- stdout 和可提交目录不得出现真实聊天原文、真实文件名、真实联系人姓名或真实平台 ID。

## 5. T102 完成记录

- `src/practical_chat_agent/services/chatlog_ingestion.py`
- `src/practical_chat_agent/app/main.py`

Reviewer 结论：

- `docs/review/T102_review.md` verdict 为 `PASS`。
- N01 deferred：无效 timezone 静默降级 warning 留给 T103/T150 判断是否需要补。
- N02/N03 deferred：双次读取和全量内存缓存留给 T110/T150 处理。
- N04 accepted：系统消息关键词硬编码作为 MVP 兜底可接受。
- N05 deferred：结构化 PII token 替换推迟到 T112+ 蒸馏阶段。
- N06 deferred：单文件 sender_role 稳健性留给 T114/T150 验证。

已验证：

- `chatlog-normalize` 支持 `--input`、`--output`、`--limit`、`--dry-run`、`--timezone-name`。
- 输入限制在 `private/chat_history/**`，输出限制在 `private/distilled/**`。
- stdout/report 不包含真实原文、真实文件名、真实联系人姓名或真实平台 ID。
- normalized event 字段与 T100/T101 合约对齐。

## 6. T103 完成记录

- `docs/review/T103_milestone_review.md`
- `docs/review/T103_review.md`

Reviewer 结论：

- Gate M0 = `Conditional` accepted。
- M0 五条硬性要求全部满足。
- 允许进入 M1，下一唯一任务为 T110。

M1 必须承接的条件：

- T110/T150 继续覆盖 `type=80` / `chatRecords` 的保守处理与测试。
- T110/T114/T150 保留并验证 `sender_role`、timezone fallback、性能/内存相关不确定性。
- T112+ 任意 LLM-facing 蒸馏步骤继续遵守 T101 隐私边界，不把私有 normalize 文本扩散到可提交产物。

## 7. T110 完成记录

- 代码改动：
  - `src/practical_chat_agent/services/conversation_chunking.py`
  - `src/practical_chat_agent/app/main.py`
- 已实现内容：
  - 新增 `ConversationChunkingService`，消费 `private/distilled/**/normalized_events.jsonl`。
  - 新增 `chatlog-chunk` CLI，默认把 `chunks.jsonl` 和更新后的 `run_report.json` 写回同一个 `private/distilled/<run_id>/` 目录。
  - chunk v0 仅使用保守边界：`conversation/contact` 变化、时间间隔过大、单 chunk 消息数上限、输入结束。
  - 每个 chunk 保留 `chunk_id`、`contact_id`、`conversation_id`、`event_ids`、`time_range`、`message_count`、`chunking_reason`。
  - chunk 级产物继续传递 T102 的不确定性信号：`source_message_type_codes` / `source_message_type_counts`、`message_type_counts`、`interaction_flag_counts`、`risk_flag_counts`、`events_with_interaction_flags`、`events_with_risk_flags`。
  - 未引入 LLM、embedding、ContactSkill、数据库或实时平台接入；chunk 输出不写聊天原文。
- 已完成验证：
  - `& 'C:\ProgramData\anaconda3\envs\practical-chat-agent\python.exe' -m compileall src/practical_chat_agent/services/conversation_chunking.py src/practical_chat_agent/app/main.py`
  - `$env:PYTHONPATH='src'; & 'C:\ProgramData\anaconda3\envs\practical-chat-agent\python.exe' -m practical_chat_agent.app.main chatlog-chunk --input private/distilled/t102_smoke --limit 12`
  - 结果：成功写出 `private/distilled/t102_smoke/chunks.jsonl`，并把 chunking 报告写入 `private/distilled/t102_smoke/run_report.json`。
  - 该小样本共消费 12 条 normalized events，生成 1 个 chunk；`chunking_reason=manual`，`boundary_flags=["end_of_input"]`，且保留了 `type=7` / `type=80` 对应的 mixed/system 风险与交互统计。
- Reviewer 结论：
  - `docs/review/T110_review.md` verdict 为 `PASS`。
  - 确认 T110 只实现 conversation chunker v0，未越界引入 LLM、embedding、ContactSkill、数据库或实时平台。
  - 确认 chunk 输出不写聊天原文，stdout/report 未发现真实聊天内容泄露。
  - 确认 T102 的 `source_message_type_code`、`risk_flags`、`interaction_flags`、`message_type`、`sender_role` 等不确定性信号已被保留或汇总传递。
- Non-blocking 处理：
  - N01 accepted：`chunking_reason="manual"` 对结构边界表达偏粗，但当前 `boundary_flags` 已保留细节；后续 T112/T150 使用时不要只依赖 reason。
  - N02 accepted/deferred：non-monotonic timestamp warning 当前只进入 report，不阻塞；若后续样本出现排序问题，由 T150 增加诊断覆盖。
  - N03 accepted/deferred：`run_report.json` 的 chunking 报告形态足够 MVP 使用；T114/T150 可按实际抽查需求扩展。
  - N04 deferred：自动化测试仍留给 T150。
  - N05 accepted：`topic_hint` 是 optional，T110 不生成 topic hint 合理，后续由 T112+ 摘要/语义阶段补足。

## 8. T111 完成记录

- 代码 / 文档改动：
  - `src/practical_chat_agent/core/models.py`
  - `docs/data_contracts/distillation_output_contract.md`
  - `docs/07_handoff.md`
- 已实现内容：
  - 在 `core.models` 中新增可复用 schema：
    - `DistillationClaim`
    - `ChunkSummaryObservation`
    - `ChunkSummary`
    - `MemoryFactCandidate`
    - `ContactSkillTopicPreference`
    - `ContactSkillPattern`
    - `ContactSkillImportantEvent`
    - `ContactSkillRelationshipState`
    - `ContactSkillCommunicationStyle`
    - `ContactSkillUserSidePreferences`
    - `ContactSkillReplyStrategy`
    - `ContactSkillUsageBoundary`
    - `ContactSkillCandidate`
  - 所有 fact / claim / skill 相关结构均支持 `evidence_refs`、`confidence`、`sensitivity`、`status`。
  - `ContactSkillCandidate` 明确加入 `usage_boundary`，默认禁止 `persona_clone`、`impersonation`、`autonomous_contact_simulation`。
  - 新增 `docs/data_contracts/distillation_output_contract.md`，固定 T112/T113 所需 JSON contract、状态约定、敏感度约定和反 impersonation 边界。
  - 未调用 LLM、未生成真实蒸馏结果、未写数据库 migration。
- 已完成验证：
  - `& 'C:\ProgramData\anaconda3\envs\practical-chat-agent\python.exe' -m compileall src/practical_chat_agent/core/models.py`
  - 结果：模型文件编译通过。
- Reviewer 结论：
  - `docs/review/T111_review.md` verdict 为 `PASS`。
  - 确认 T111 完整定义 `ChunkSummary`、`MemoryFactCandidate`、`ContactSkillCandidate` 及辅助结构。
  - 确认所有 fact/claim/skill 结构强制或支持 `evidence_refs`、`confidence`、`sensitivity`、`status`。
  - 确认 `ContactSkillUsageBoundary` 默认禁止 `persona_clone`、`impersonation`、`autonomous_contact_simulation`。
  - 确认无 LLM 调用、无数据库 migration、无 `private/` 泄露。
- Non-blocking 处理：
  - N01 accepted：`ContactSkillRelationshipState` / `ContactSkillCommunicationStyle` 的部分字段保留自由字符串，MVP 阶段可接受；后续可按实际 LLM 输出收紧。
  - N02 accepted/deferred：`redaction_policy` 当前使用 `dict[str, Any]` 可接受；T120/T150 可视 store/review 需要改为结构化 model。
  - N03 deferred：`DistillationMemoryType` 与现有 `MemoryType` enum 的映射交给 T120。
  - N04 deferred：`created_at` / `updated_at` 由 T120 store 或产物写入层补充。
  - N05 deferred：Pydantic 约束自动化测试交给 T150。

## 9. T112 完成记录

- 代码 / 文档改动：
  - `src/practical_chat_agent/services/chatlog_distillation.py`
  - `src/practical_chat_agent/services/contact_skill.py`
  - `src/practical_chat_agent/app/main.py`
  - `docs/07_handoff.md`
  - `docs/08_risks_and_open_questions.md`
- 已实现内容：
  - 新增 `ChatlogDistillationService`，消费 `private/distilled/**/chunks.jsonl` 与同目录 `normalized_events.jsonl`。
  - 新增 `chatlog-distill` CLI，支持 `--input`、`--output`、`--limit`、`--sample`、`--dry-run`。
  - LLM 请求复用 OpenAI-compatible `/chat/completions` 调用风格。
  - distillation 输出先做 provider 兼容归一化，再强制校验为 T111 `ChunkSummary` / `MemoryFactCandidate` schema。
  - evidence refs 必须落在对应 chunk 的 `chunk_id + event_ids` 范围内；越界 refs 会导致 chunk 被拒绝，不写入 accepted 输出。
  - 产物只写入 `private/distilled/<run_id>/chunk_summaries.jsonl`、`memory_facts.jsonl` 和合并后的 `run_report.json`；不保存 LLM prompt 或 raw response。
  - `contact_skill.py` 当前仅含轻量辅助函数，为 T113 聚合 refs 预留，不包含 ContactSkill builder、review exporter 或 store 逻辑。
- 已完成验证：
  - `& 'C:\ProgramData\anaconda3\envs\practical-chat-agent\python.exe' -m compileall src/practical_chat_agent/services/chatlog_distillation.py src/practical_chat_agent/services/contact_skill.py src/practical_chat_agent/app/main.py`
  - `$env:PYTHONPATH='src'; & 'C:\ProgramData\anaconda3\envs\practical-chat-agent\python.exe' -m practical_chat_agent.app.main chatlog-distill --input private/distilled/t102_smoke --limit 1`
  - 首次因沙箱网络限制返回 `remote_request_failed`，worker 没有用 mock 冒充成功；提权复跑后 provider 可达。
  - 加入 provider 输出兼容归一化后，小样本成功写出 `chunk_summaries.jsonl`、`memory_facts.jsonl`、`run_report.json`。
  - 当前小样本结果：1 个 selected chunk，1 个 successful chunk，写出 1 条 chunk summary、7 条 memory facts，`distillation.failure_reasons` 为空。
  - reviewer 确认人工抽查 3+ 条 fact 的 evidence_refs，均能回指当前 chunk 事件。
- Reviewer 结论：
  - `docs/review/T112_review.md` verdict 为 `PASS`。
  - 确认 LLM 输出经过 provider 兼容归一化、T111 schema 校验和 evidence refs 范围校验后才写入。
  - 确认 prompt/raw response 不写入文件，stdout/report 只含统计和状态码。
  - 确认产物只写入 `private/distilled/`，没有真实聊天原文进入 docs/examples/tests/stdout。
  - 确认未越界做 ContactSkill builder、store、数据库 migration、实时平台接入或自动发送。
- Non-blocking 处理：
  - N01 deferred：`chunk_id` fallback 是合法粗粒度 evidence，但会降低证据精度；T114 全量/更大样本抽查时关注仅有 chunk_id 的比例。
  - N02 deferred：provider shape drift 已由 R024 记录；T114/T150 继续验证。
  - N03 accepted/deferred：sensitivity 关键词兜底作为 MVP 可接受；T150 可补充测试或后续收紧。
  - N04 accepted/deferred：memory_type fallback 作为 MVP 可接受；T114/T150 观察误分类。
  - N05 accepted：`contact_skill.py` 轻量辅助不越界，T113 可扩展或重写。
  - N06 deferred：schema 校验、evidence refs、PII 脱敏、provider 归一化的自动化测试留给 T150。
  - N07 accepted/deferred：prompt 层 PII token 替换已部分满足 T102 N05；T150 privacy leakage smoke test 继续覆盖。

## 10. T113 完成记录

- 代码 / 文档改动：
  - `src/practical_chat_agent/services/contact_skill.py`
  - `src/practical_chat_agent/exporters/contact_skill_markdown.py`
  - `src/practical_chat_agent/app/main.py`
  - `docs/07_handoff.md`
- 已实现内容：
  - `ContactSkillBuilderService` 消费 T112 的 `chunk_summaries.jsonl` 和 `memory_facts.jsonl`，通过 Pydantic `model_validate` 读取上游产物。
  - 生成 `ContactSkillCandidate`，并强制 `status="candidate"` 与非空 `evidence_refs`。
  - 输出 `private/distilled/<run_id>/contact_skill.candidate.json` 与 `contact_skill.review.md`。
  - Markdown review exporter 展示 relationship state、communication style、topics、important events、stable preferences、emotional patterns、reply strategy、usage boundary、evidence refs 与 anti-impersonation reminder。
  - 新增 `chatlog-build-contact-skill` CLI，支持 `--input`、`--output`、`--contact-id`、`--dry-run`。
  - 输出限制在 `private/distilled/`；无自动 approve、无 DB migration、无 realtime 平台、无自动发送。
- 已完成验证：
  - `& 'C:\ProgramData\anaconda3\envs\practical-chat-agent\python.exe' -m compileall src/practical_chat_agent/services/contact_skill.py src/practical_chat_agent/exporters/contact_skill_markdown.py src/practical_chat_agent/app/main.py`
  - `$env:PYTHONPATH='src'; & 'C:\ProgramData\anaconda3\envs\practical-chat-agent\python.exe' -m practical_chat_agent.app.main chatlog-build-contact-skill --input private/distilled/t102_smoke`
  - 样本确认生成 `contact_skill.candidate.json` 与 `contact_skill.review.md`，candidate 状态仍为 `candidate`，review artifact 可读并带 evidence refs / usage boundary。
- Reviewer 结论：
  - `docs/review/T113_review.md` verdict 为 `PASS_WITH_WARNINGS`。
  - 确认未越界自动 approve、保存 raw chat text、生成“contact speaking”内容、写 DB migration、接 realtime platform 或 auto-send。
  - 确认 evidence chain、candidate 状态、anti-impersonation guardrails 和 review artifact 均满足 T113 任务目标。
- Warning 处理：
  - N01 accepted：`_build_report` 重复调用是低影响重复工作，不要求返修。
  - N02 deferred：启发式 tokens/topic/relationship 推断偏当前小样本，T114 需用更大或不同样本暴露泛化缺口，T120+ 可考虑 LLM-assisted inference。
  - N03 deferred：confidence / closeness / trust 公式化且非 evidence-weighted，T114 需人工检查是否显得过度精确，T120+ 重新设计。
  - N04 accepted：`exporters/` 缺少 `__init__.py` 当前不影响 Python 3 namespace package 导入。
  - N05 accepted：未使用 helper 无当前风险，可在 T114+ 移除或使用。

## 11. T114 / M1 完成记录

- 文档改动：
  - `docs/review/T114_milestone_review.md`
  - `docs/review/T114_review.md`
  - `docs/review/M1_review.md`
  - `docs/07_handoff.md`
  - `docs/08_risks_and_open_questions.md`
- Worker milestone sample:
  - sample run directory: `private/distilled/t102_smoke`
  - artifact chain present: `normalized_events.jsonl`、`chunks.jsonl`、`chunk_summaries.jsonl`、`memory_facts.jsonl`、`contact_skill.candidate.json`、`contact_skill.review.md`、`run_report.json`
  - sample summary: 12 normalized events, 1 chunk, 1 chunk summary, 7 memory facts, candidate ContactSkill.
  - worker audited 7/7 memory facts, exceeding the required 5 facts.
- Reviewer conclusion:
  - `docs/review/T114_review.md` verdict 为 `PASS_WITH_WARNINGS`。
  - Gate M1 verdict = `Conditional` confirmed.
  - Reviewer independently checked all 7 memory facts against normalized events.
  - All Gate M1 hard requirements passed.
- Captain milestone review:
  - `docs/review/M1_review.md` verdict = `Conditional`。
  - M2 may proceed only with candidate-only / human-review-first semantics.
- Warning / condition handling:
  - T114 N01/N02 accepted：minor semantic elevation/paraphrase in candidate-only facts, handled by human review and R030.
  - T114 N03 accepted：sample too small for generalization, represented by Gate M1 `Conditional`.
  - T114 N04 accepted：no report inconsistency found; no action.
- R028/R029/R030 remain active into M2.

## 12. T120 完成记录

- 代码 / 文档改动：
  - `src/practical_chat_agent/core/models.py`
  - `src/practical_chat_agent/services/contact_skill.py`
  - `docs/07_handoff.md`
- 已实现内容：
  - 在 `core.models` 中新增 T120 file-store 相关模型：
    - `ContactSkillRedactionPolicy`
    - `DistilledArtifactReviewDecision`
    - `DistilledArtifactReviewMetadata`
    - `DistilledArtifactSourceMetadata`
    - `MemoryFactStoreRecord`
    - `MemoryFactStoreFile`
    - `ContactSkillStoreRecord`
    - `ContactSkillStoreFile`
  - 为 `MemoryFactCandidate` 增加显式映射 helper：
    - `to_runtime_memory_type()`
    - `to_memory_fact(...)`
    - 仅提供后续 T123/T121 可复用映射，不在本轮做 runtime 注入。
  - 将 `ContactSkillCandidate.redaction_policy` 从宽松 `dict[str, Any]` 收紧为结构化 `ContactSkillRedactionPolicy`。
  - 在 `contact_skill.py` 中新增 `ContactSkillFileStoreService`，支持：
    - 从 legacy `memory_facts.jsonl` 包装并加载 `MemoryFactStoreFile`
    - 从 legacy `contact_skill.candidate.json` 包装并加载 `ContactSkillStoreFile`
    - 保存 `memory_fact_store.json` / `contact_skill_store.json`
    - 保留 `status`、`evidence_refs`、`source_run_id`、source artifact path、source chunk/memory/event ids、review metadata
  - `review_metadata.is_runtime_ready(...)` / record-level `is_runtime_ready()` 只在 `status="approved"` 且 `reviewed_by_human=True` 时返回 true，保持 candidate-only / human-review-first 语义。
  - 未新增 CLI、未改数据库、未引入向量库、未做 runtime prompt 注入、未自动 approve。
- 已完成验证：
  - `& 'C:\ProgramData\anaconda3\envs\practical-chat-agent\python.exe' -m compileall src/practical_chat_agent/core/models.py src/practical_chat_agent/services/contact_skill.py`
  - 使用合成脱敏样例运行最小 load/save 闭环验证（未读取真实聊天原文）：
    - 生成 legacy fixture 于 `private/distilled/t120_store_smoke/legacy/`
    - 用 `ContactSkillFileStoreService` 加载 legacy `memory_facts.jsonl` / `contact_skill.candidate.json`
    - 写出 store 文件到 `private/distilled/t120_store_smoke/store/memory_fact_store.json`
    - 写出 store 文件到 `private/distilled/t120_store_smoke/store/contact_skill_store.json`
    - 再次回读并断言：
      - memory statuses = `candidate`, `approved`
      - skill statuses = `approved`
      - `evidence_refs` 未丢失
      - `source_memory_ids` / source event ids / source chunk ids 保留
      - approved record 的 `review_metadata.reviewed_by_human`、`last_decision`、history 保留
      - `is_runtime_ready()` 仅对 synthetic approved records 返回 true
- Reviewer 结论：
  - `docs/review/T120_review.md` verdict 为 `PASS_WITH_WARNINGS`。
  - 确认 T120 只实现 file store models 和 service，不做 CLI、DB migration、vector DB、runtime prompt injection 或 auto-approve。
  - 确认 `is_runtime_ready()` 需要 `status="approved"`、`reviewed_by_human=True`、`last_decision="approved"` 三重条件，保持 candidate-only / human-review-first。
  - 确认 legacy T112/T113 artifacts 可包装为 store records，且 evidence refs、source ids、review metadata 可 load/save round-trip 保留。
- Warning 处理：
  - N01 accepted：`updated_at` no-op normalization 低影响，不要求返修；T122 更新 review 状态时再明确 timestamp 语义。
  - N02 accepted：`ContactSkillBuilderService` 与 `ContactSkillFileStoreService` 的 path/helper duplication 对 MVP 可接受，暂不抽共享基类。
  - N03 accepted：single-record store shape 兼容入口便利迁移，Pydantic downstream validation 足够兜底。
  - N04 accepted：`DistillationMemoryType` 到 runtime `MemoryType` 的粗粒度映射符合 MVP granularity。
  - N05 deferred：自动化测试留给 T150，新增 R031 跟踪 store model validation、legacy wrapping、load/save round-trip、runtime-ready gate 和 path confinement 测试。
- 当前注意点：
  - 真实 approve / reject / freeze CLI 仍留给 T122。
  - evidence existence/support 校验由 T121 承接，missing refs 必须阻止 approval。

## 13. T121 完成记录

- 代码 / 文档改动：
  - `src/practical_chat_agent/services/evidence_validation.py`
  - `src/practical_chat_agent/app/main.py`
  - `docs/07_handoff.md`
- 已实现内容：
  - 新增 `EvidenceValidationService`，通过 T120 `ContactSkillFileStoreService` 加载 memory/contact-skill store records。
  - 从 same-run artifacts 建立 evidence id index：
    - `normalized_events.jsonl`
    - `chunks.jsonl`
    - `chunk_summaries.jsonl`
    - `memory_facts.jsonl`
    - `contact_skill.candidate.json`
    - T120 store records 自身
  - 递归扫描 serialized model payload 中所有 nested `evidence_refs`。
  - 输出每个 record 的 checked refs、missing refs、nested ref locations、provenance snapshot、review metadata snapshot、approval/runtime block reasons。
  - 状态规则：
    - `candidate` 默认 blocked from approval/runtime。
    - `approved` 若存在 missing refs，则 blocked from approval/runtime。
    - `rejected` / `frozen` / `archived` 不可 runtime-ready。
    - `approved` 且 refs OK 但未 human-reviewed，只能 approval-ready，不能 runtime-ready。
  - 新增 `chatlog-validate-evidence` CLI，支持 `--input`、`--output`、`--dry-run`。
  - Validator 只报告，不写回 store metadata，不自动 approve，不做 runtime integration。
- 已完成验证：
  - Compile passed：
    - `& 'C:\ProgramData\anaconda3\envs\practical-chat-agent\python.exe' -m compileall src\practical_chat_agent\services\evidence_validation.py src\practical_chat_agent\app\main.py`
  - Good case：`private/distilled/t102_smoke` dry-run。
    - `evidence_validation_status = passed`
    - `validated_record_count = 8`
    - `records_with_missing_refs = 0`
    - `missing_ref_count = 0`
    - `approval_blocked_records = 8`
    - `runtime_blocked_records = 8`
    - 解释：refs 全部存在，records 因仍为 candidate 被正确阻止。
  - Bad case：`private/distilled/t121_missing_ref_fixture/` synthetic fixture。
    - `evidence_validation_status = failed`
    - `validated_record_count = 3`
    - `records_with_missing_refs = 1`
    - `missing_ref_count = 1`
    - approved memory record 因 missing `evt_demo_2` 同时 blocked from approval/runtime。
  - Store-only case：`private/distilled/t120_store_smoke/store` dry-run。
    - `evidence_validation_status = failed`
    - `records_with_missing_refs = 3`
    - `missing_ref_count = 5`
    - 解释：store-only fixture without same-run evidence artifacts 被正确判定 evidence-incomplete。
- Reviewer 结论：
  - `docs/review/T121_review.md` verdict 为 `PASS_WITH_WARNINGS`。
  - 确认 T121 只实现 read-only evidence validator 与 CLI，不做 auto-approve、approve/reject/freeze CLI、DB migration、vector DB、runtime prompt injection、LLM call 或 `private/chat_history` 读取。
  - 确认 stdout/report 限制在 counts、safe relative paths 和 private `private/distilled/` report，未发现私密内容进入 docs/examples/tests/stdout。
- Warning 处理：
  - N01 accepted：当前 `ContactSkillCandidate` 没有 stable skill artifact id，`_extract_contact_skill_ids` 对现有 schema 为空；fallback 到 `contact_id` 不影响正确性。
  - N02 accepted/deferred：JSON/JSONL helper 已是第三份重复，MVP 可接受；T150 或后续 refactor 可统一 file IO 并回收 BOM handling。
  - N03 accepted：全 payload 递归找 `evidence_refs` 是 O(total dict nodes)，当前数据量无性能风险。
  - N04 accepted：validator read-only、不写回 `review_metadata.evidence_validation_status` 是正确设计；T122 决定是否根据 report 写入 review metadata。
  - N05 deferred：自动化测试留给 T150，新增 R032 跟踪 evidence index、nested refs、status rules、missing refs blocking、human review gate interaction 和 path confinement 测试。
- 当前注意点：
  - T122 approve 必须读取或要求通过 T121 evidence validation report。
  - T122 不得在 missing refs、未 human review 或 rejected/frozen/archived 状态下绕过 gate。

## 14. T122 完成记录

- 代码 / 文档改动：
  - `src/practical_chat_agent/services/contact_skill.py`
  - `src/practical_chat_agent/exporters/contact_skill_markdown.py`
  - `src/practical_chat_agent/app/main.py`
  - `docs/07_handoff.md`
- 已实现内容：
  - 新增 `ContactSkillStoreReviewService`，支持 list/apply decision/export review artifact。
  - 新增 `chatlog-review-store` CLI with actions:
  - `list`
  - `approve`
  - `reject`
  - `freeze`
  - `archive`
  - `export`
  - T122 scope kept to private file-store review only:
    - no runtime integration
    - no DB migration
    - no vector DB
    - no LLM call
    - no auto-send
  - Review flow implemented:
    - input/output confined to `private/distilled/**`
    - safe record listing with record id, artifact type/id, status, review state, evidence validation status, approval/runtime-ready summary, and safe relative path
    - `approve` requires T121 `evidence_validation_report.json`
    - `approve` blocks on report status != `passed`
    - `approve` blocks on target-record missing refs
    - `approve` blocks for current status in `rejected` / `frozen` / `archived`
    - `reject` / `freeze` / `archive` update payload status plus review metadata/history and keep runtime-ready false
    - decision metadata writes reviewer id/name, reviewed timestamp, notes, and evidence validation status into `review_metadata`
    - export writes markdown safe summaries only under `private/distilled/**`
  - legacy wrapped records now get deterministic stable `record_id` values derived from run id + artifact id, so T121 report lookup and T122 CLI targeting stay stable across reloads.
  - store save preserves store-level `generated_at`.
- Private fixtures / safe samples used:
  - safe sample: `private/distilled/t102_smoke`
  - missing-ref sample: `private/distilled/t121_missing_ref_fixture`
  - T122 private verification fixtures:
    - `private/distilled/t122_pass_fixture`
    - `private/distilled/t122_reject_fixture`
    - `private/distilled/t122_freeze_fixture`

- 已完成验证：
  - compile:
    - `& 'C:\ProgramData\anaconda3\envs\practical-chat-agent\python.exe' -m compileall src\practical_chat_agent\app\main.py src\practical_chat_agent\services\contact_skill.py src\practical_chat_agent\exporters\contact_skill_markdown.py`
    - result: passed
  - safe list:
    - `chatlog-review-store --input private/distilled/t120_store_smoke/store --action list`
    - result: stdout only contains safe ids, status fields, counts, and private-relative paths
  - passed validation fixture:
    - `chatlog-validate-evidence --input private/distilled/t122_pass_fixture`
    - result: `evidence_validation_status = passed`
  - approve happy path:
    - `chatlog-review-store --input private/distilled/t122_pass_fixture --action approve --record-id skillstore_bae8944df32d64b2 --reviewer-id worker_t122 --reviewer-name 'T122 Reviewer' --note 'Approved after passed evidence validation.'`
    - result: wrote `private/distilled/t122_pass_fixture/contact_skill_store.json`
    - confirmed `status = approved`, `reviewed_by_human = true`, `last_decision = approved`, reviewer fields set, `last_reviewed_at` populated, `evidence_validation_status = passed`, decision appended to `history`, and `updated_at` advanced
  - reject path:
    - `chatlog-validate-evidence --input private/distilled/t122_reject_fixture`
    - `chatlog-review-store --input private/distilled/t122_reject_fixture --action reject --record-id skillstore_0edb3e3030c16049 --reviewer-id worker_t122 --reviewer-name 'T122 Reviewer' --note 'Rejected for narrower human rewrite before approval.'`
    - result: wrote `private/distilled/t122_reject_fixture/contact_skill_store.json`
    - confirmed `status = rejected`, decision appended, runtime-ready summary remained false
  - freeze path:
    - `chatlog-validate-evidence --input private/distilled/t122_freeze_fixture`
    - `chatlog-review-store --input private/distilled/t122_freeze_fixture --action freeze --record-id skillstore_4e33506d02e1e966 --reviewer-id worker_t122 --reviewer-name 'T122 Reviewer' --note 'Frozen pending broader sample review.'`
    - result: wrote `private/distilled/t122_freeze_fixture/contact_skill_store.json`
    - confirmed `status = frozen`, decision appended, runtime-ready summary remained false
  - missing-ref approve block:
    - `chatlog-review-store --input private/distilled/t121_missing_ref_fixture --action approve --record-id memstore_37bae56b191844de --reviewer-id worker_t122 --reviewer-name 'T122 Reviewer' --note 'Should be blocked by missing refs.'`
    - result: correctly blocked with `Approve is blocked because the target record still has missing evidence refs in the validation report.`
    - checked target fixture file stayed unchanged after the blocked command
  - export path:
    - `chatlog-review-store --input private/distilled/t122_pass_fixture --action export --output private/distilled/t122_pass_fixture/review_exports`
    - result: wrote `private/distilled/t122_pass_fixture/review_exports/store_review_export.md`
    - checked exported markdown contains safe review metadata only, not raw chat transcript output

- Reviewer 结论：
  - `docs/review/T122_review.md` verdict 为 `PASS_WITH_WARNINGS`。
  - 确认 T122 只实现 private file-store review CLI，不做 auto-approve、runtime integration、DB migration、vector DB、LLM、auto-send 或 `private/chat_history` 读取。
  - 确认 approve gate 完整：需要 T121 validation report、report `passed`、target record present、0 missing refs、checked refs > 0，并阻止 rejected/frozen/archived re-approval。
  - 确认 review metadata history、safe export、path confinement、stable record_id 和 no private data stdout 均满足任务包。
- Warning 处理：
  - N01 accepted：`del current_status` 是低影响接口/风格问题，不影响 correctness。
  - N02 accepted：递归更新所有合法 `status` 字段符合当前 schema；若未来 schema 出现不同语义的 status 字段再重审。
  - N03 accepted：`store_runtime_ready` 提前计算只是轻微 style note。
  - N04 accepted/deferred：review service 访问 file store private helpers 对 MVP 可接受；未来可抽 public file/path utility。
  - N05 accepted：mutable `_StoreWorkspace` 当前局部可控。
  - N06 deferred：自动化测试留给 T150，新增 R033 跟踪 approval gate、reject/freeze/archive、review history、recursive status update、export path confinement、stable record_id 和 no-auto-approve 测试。
- 当前注意点：
  - T123 必须只读取 approved + runtime-ready records。
  - T123 不得注入 candidate/rejected/frozen/archived，不得加载完整 skill 或全部 memory 到 prompt。
  - T122 intentionally does not implement reopen; rejected/frozen/archived records remain non-approvable in this scope.

## 15. Worker 启动提示

```text
你是 Codex worker。

请先阅读：
- README.md
- AGENTS.md
- docs/02_experiment_plan.md
- docs/06_eval_protocol.md
- docs/04_task_board.md
- docs/07_handoff.md
- docs/review/T123_review.md
- docs/review/T130_review.md
- docs/review/T131_review.md
- docs/review/T132_review.md
- docs/data_contracts/reply_plan_contract.md
- docs/tasks/M3_relationship_reply_planner/T133_holdout_eval.md

本轮只完成：
- docs/tasks/M3_relationship_reply_planner/T133_holdout_eval.md

规则：
1. 只改 Allowed files。
2. 只做匿名 holdout eval 和 Gate M3 判断，不修改 planner 代码。
3. 评估 T130-T132 输出的自然度、边界遵守、证据使用、risk flags 可解释性和隐私安全。
4. 可以读取 private/distilled 下的私有评估输出，但不得把 holdout 原文、真实联系人名、真实平台 ID 或可识别内容写入 docs。
5. 不自动发送，不接数据库，不引入向量数据库，不读取 `private/chat_history/`。
6. 不修复代码缺陷；若发现 blocking code issue，只在 review 中记录并给出 Gate M3 `Block` 或 `Conditional` 理由。
7. 输出 `docs/review/T133_milestone_review.md`，并更新 `docs/07_handoff.md`。
8. 最后报告：评估样本形态、匿名指标、Gate M3 verdict、剩余风险。
```

## 16. Reviewer 启动提示

```text
你是 Claude Code reviewer。

请先阅读：
- docs/02_experiment_plan.md
- docs/04_task_board.md
- docs/07_handoff.md
- docs/06_eval_protocol.md
- docs/review/T123_review.md
- docs/review/T130_review.md
- docs/review/T131_review.md
- docs/review/T132_review.md
- docs/data_contracts/reply_plan_contract.md
- docs/tasks/M3_relationship_reply_planner/T133_holdout_eval.md

只读审查本次 diff，不要修改文件。

重点检查：
1. T133 是否只做 read-only / docs-only 的 holdout eval，不修改 planner 代码。
2. 是否回答 Gate M3 关键问题：自然度、边界遵守、证据使用、risk flags 可解释性、隐私安全。
3. 是否没有 holdout 原文、真实联系人名、真实平台 ID 或可识别 private content 进入 docs/examples/tests/stdout。
4. 是否如实记录 T131/T132 deterministic templates、keyword false positives 和缺少 committed tests 的限制。
5. Gate M3 verdict 是否为 `Allow` / `Conditional` / `Block`，并给出可执行条件。
6. 若 verdict 允许进入下一阶段，是否明确禁止自动发送和实时平台接入继续越界。

输出 Verdict: PASS / PASS_WITH_WARNINGS / BLOCK，并审查 `docs/review/T133_milestone_review.md`。
```

## 17. 下一步顺序

1. 可提交当前 T132 worker/reviewer 代码与 Captain 收口文档变更。
2. 下一轮 worker 只执行 T133，不要自领 M4。
3. 若 T133 review `BLOCK`，worker 只修 blocking issue 或补充 blocking evaluation evidence，并最多自动复审一次。
4. 若 T133 review `PASS` 或 `PASS_WITH_WARNINGS`，Captain 再更新治理文档并决定 Gate M3 是否允许进入 M4。
5. M3 仍保持 review-only；不要实现自动发送或实时平台接入。

## 18. 历史顺序

1. T100 review `PASS`，已完成 schema profile 与 normalized event contract。
2. T101 review `PASS`，已完成 privacy/source_ref rules。
3. T102 review `PASS`，已完成 `chatlog-normalize` 最小 CLI。
4. T103 Gate M0 = `Conditional` accepted，允许进入 M1。
5. T110 review `PASS`，已完成 `chatlog-chunk` conversation chunker v0。
6. T111 review `PASS`，已完成 distillation output schemas 和 JSON contract。
7. T112 review `PASS`，已完成小样本 summary/fact extraction 与 evidence refs 校验管线。
8. T113 review `PASS_WITH_WARNINGS`，已完成 ContactSkill candidate builder 和 Markdown review exporter。
9. T114 review `PASS_WITH_WARNINGS`，Gate M1 = `Conditional`，M2 可条件启动。
10. T120 review `PASS_WITH_WARNINGS`，已完成 file store models 与 human-review-first gate。
11. T121 review `PASS_WITH_WARNINGS`，已完成 evidence validator 与 missing-ref/status gate。
12. T122 review `PASS_WITH_WARNINGS`，已完成 skill review CLI 与 approval gate。
13. T123 review `PASS_WITH_WARNINGS`，已完成 approved-store compact `ChatContext` integration。
14. T130 review `PASS_WITH_WARNINGS`，已完成 ReplyPlan schema 与 prompt contract。
15. T131 review `PASS_WITH_WARNINGS`，已完成 review-only ReplyPlanner 与 `chat-reply-plan` CLI；T132 进入 policy/boundary validation。
16. T132 review `PASS_WITH_WARNINGS`，已完成 ReplyPlanner policy/boundary 风险层；T133 进入匿名 holdout eval。

## 19. 注意事项

- `.gitignore` 中已有 `private/`，保留这个安全措施。
- 不要还原用户手动迁移 docs 目录结构的操作。
- 不要读取或输出 `.env`。
- 不要把 `private/chat_history` 的真实文件名或聊天内容写入 docs。
- 当前阶段不做微调、不做自动发送、不做微信扫描。
- M2 可以推进，但必须带着 Gate M1 Conditional 条件继续验证，不要把 M1 写成无条件完成。

## 20. T123 Completion Record

- Files changed:
  - `src/practical_chat_agent/core/models.py`
  - `src/practical_chat_agent/services/chat_context.py`
  - `src/practical_chat_agent/app/container.py`
  - `docs/07_handoff.md`
- Implemented:
  - Added `approved_store_context` to `ChatContext`.
  - Added compact store brief models: `ApprovedStoreContext`, `ApprovedContactSkillBrief`, and `ApprovedMemoryFactBrief`.
  - Extended `ChatContextAssembler` with optional approved-store loading from `private/distilled/**`.
  - Context assembly now adds compact approved-store hints into `summary` and `memory_retrieval_notes`.
  - Filtering is conservative: only records that are approved, human-reviewed, evidence-valid, and `is_runtime_ready() == True` can enter runtime context.
  - Candidate, rejected, frozen, archived, missing-evidence, and not-human-reviewed records are excluded.
  - The brief stays compact: short relationship summary, short strategy / boundary reminders, record ids, and evidence refs only. No raw transcript, no full JSON dump, no runtime prompt injection.
  - `AppContainer` now supports optional injection through `PRACTICAL_CHAT_APPROVED_STORE_PATH` and `PRACTICAL_CHAT_APPROVED_MEMORY_LIMIT`.
- Verification:
  - Compile passed:
    - `& 'C:\ProgramData\anaconda3\envs\practical-chat-agent\python.exe' -m compileall src/practical_chat_agent/services/chat_context.py src/practical_chat_agent/core/models.py src/practical_chat_agent/app/container.py`
  - Approved fixture:
    - fixture: `private/distilled/t123_approved_fixture`
    - result: `approved_store_context.status = loaded`
    - loaded one approved contact-skill brief with safe record id / evidence refs, and summary / retrieval notes included compact approved-store hints
  - Exclusion fixture:
    - fixture: `private/distilled/t123_exclusion_fixture`
    - result: `approved_store_context.status = no_runtime_ready_records`
    - rejected store record did not enter context
  - Compatibility fixture:
    - fixture: `private/distilled/t123_memory_only_fixture`
    - result: approved contact-skill brief loaded correctly; approved memory record with missing refs stayed excluded
  - No-store compatibility:
    - direct `ChatContextAssembler()` run with no store path
    - result: `approved_store_context.status = not_configured`, and existing context assembly behavior stayed unchanged
- Remaining risk / assumption:
  - Current private fixtures verify the positive contact-skill path and the exclusion path. They do not yet provide a runtime-ready approved memory-only sample, so the positive memory-brief branch remains unobserved and should be re-checked when such a safe fixture exists.

## 21. T130 Completion Record

- Files changed:
  - `src/practical_chat_agent/core/models.py`
  - `docs/data_contracts/reply_plan_contract.md`
  - `docs/07_handoff.md`
- Implemented:
  - Added strongly typed reply-planning models:
    - `ReplyPlanContextRef`
    - `ReplyPlanSourceContext`
    - `ReplyPlanCandidate`
    - `ReplyPlan`
  - Added `ReplyPlanMode = "candidate_review_only"` to make the review-only usage explicit.
  - Added `ReplyPlanContextRefType` so candidates can cite:
    - approved contact-skill record ids
    - approved memory-fact record ids
    - approved store evidence refs
    - recent event ids
    - runtime memory hit ids
    - policy-boundary refs
  - `ReplyPlan` requires:
    - `contact_id`
    - `source_context`
    - `policy_boundary_summary`
    - `notes_on_candidate_differences`
    - at least 3 `candidates`
  - Each `ReplyPlanCandidate` requires:
    - `draft_text`
    - `rationale`
    - at least 1 `supporting_context_ref`
    - at least 1 `boundary_reminder`
    - optional `risk_flags` and `confidence`
  - Added `docs/data_contracts/reply_plan_contract.md` to document:
    - review-only usage boundary
    - anti-impersonation rule
    - conservative handling for uncertain/sensitive cases
    - compatibility with T123 `approved_store_context`
    - JSON shape and field semantics for T131/T132
- How T130 ties back to T123:
  - `ReplyPlanSourceContext.approved_store_status` directly reuses T123 `ApprovedStoreContextStatus`.
  - `ReplyPlanSourceContext` accepts T123 compact ids and refs:
    - `approved_contact_skill_record_id`
    - `approved_memory_record_ids`
    - `approved_store_evidence_refs`
  - The contract therefore consumes the compact approved-store brief from `ChatContext` instead of requiring full store JSON or raw transcript text.
- Verification:
  - Compile passed:
    - `& 'C:\ProgramData\anaconda3\envs\practical-chat-agent\python.exe' -m compileall src/practical_chat_agent/core/models.py`
  - Synthetic model validation passed with a safe inline sample:
    - validated one `ReplyPlan` containing 3 candidates
    - confirmed candidates can cite T123-style approved-store record ids / evidence refs
    - confirmed raw transcript text is not required by the schema
    - confirmed `approved_store_status="loaded"` is compatible with T123 context status values
- Remaining risk / assumption:
  - T130 defines the contract only. It does not yet prove that T131 generation logic will consistently populate distinct, high-quality candidates from real runtime context.
  - T123 reviewer warning about contact-id alignment still applies: T131 should verify that runtime `contact_id` routing stays aligned with approved-store records when the planner is wired in.

- Review decision:
  - `docs/review/T130_review.md` verdict = `PASS_WITH_WARNINGS`.
  - Warning handling:
    - N01 accepted: single-value `ReplyPlanMode` is correct for current review-only scope.
    - N02 deferred to R034: T131 must enforce stable unique `priority_rank` values.
    - N03 accepted: free-form `approach_label` is acceptable for MVP.
    - N04 deferred to R034: T131 must verify `contact_id` alignment during assembly.
  - Captain decision: T130 is complete; T131 is the next Current Unique Task.

## 22. T131 Kickoff Notes

- Task package:
  - `docs/tasks/M3_relationship_reply_planner/T131_reply_planner.md`
- Worker focus:
  - Implement a review-only ReplyPlanner service or CLI.
  - Consume only compact approved-store context from T123.
  - Output T130 `ReplyPlan` with at least 3 candidates.
  - Preserve safety: no raw transcript, no send logic, no DB, no vector DB.
- Reviewer focus:
  - Candidate distinctness.
  - Cited refs and boundary reminders.
  - Unique ranking and contact/source alignment.
  - No scope creep into automatic sending or platform integration.

## 23. T131 Implementation Record

- Files changed:
  - `src/practical_chat_agent/services/reply_planner.py`
  - `src/practical_chat_agent/app/main.py`
  - `docs/07_handoff.md`
- Implemented:
  - Added `ReplyPlanner` service with a review-only `generate(context=...) -> ReplyPlan` flow.
  - The planner consumes only `ChatContext` plus T123 compact `approved_store_context` fields already present at runtime.
  - Added hard checks for the two T130 warning items:
    - `ReplyPlan.contact_id` must match `ChatContext.user_id`.
    - `ApprovedStoreContext.contact_id` and approved contact-skill `contact_id` must align with the routed contact id.
    - `priority_rank` values must be unique and form a stable `1..N` sequence.
  - Added a safe `chat-reply-plan` CLI command that:
    - reads a redacted or synthetic `ChatContext` JSON file
    - generates a `ReplyPlan`
    - prints only the plan JSON or writes it to an output file
    - does not print the raw input context
  - Candidate generation stays offline and review-only:
    - exactly 3 distinct candidate shapes are generated
    - each candidate includes draft text, rationale, supporting refs, risk flags, boundary reminders, and confidence
    - refs are limited to approved compact ids, evidence refs, recent event ids, runtime memory ids, and policy-boundary ids
  - The planner ignores `source_record_ids` lists, so non-approved ids such as candidate/rejected/frozen/archived record ids do not leak into the plan surface.
  - `source_context.chat_context_summary` is rebuilt as a safe count/status summary instead of copying `ChatContext.summary`, so raw message text is not echoed back into the plan.
- Verification:
  - Compile passed:
    - `& 'C:\ProgramData\anaconda3\envs\practical-chat-agent\python.exe' -m compileall src/practical_chat_agent/services/reply_planner.py src/practical_chat_agent/app/main.py`
  - Safe synthetic context validation passed with an inline fixture:
    - contact id: `contact_lin`
    - approved contact-skill record id: `approved_skill_001`
    - approved memory record id: `approved_mem_001`
    - recent event id: `evt_recent_1`
    - runtime memory hit id: `mem_runtime_1`
    - extra non-approved ids were injected into `source_record_ids` only as a negative check
  - Validation results:
    - service emitted 3 candidates
    - CLI emitted 3 candidates through `chat-reply-plan --input <tempfile>`
    - candidate refs stayed within approved-store ids, evidence refs, recent event ids, runtime memory ids, and policy-boundary ids
    - injected `candidate_record_999` / `rejected_record_888` ids did not appear in the output plan
    - raw synthetic inbound text did not appear in the output plan JSON
    - contact-id mismatch raised `ReplyPlannerError` as expected
- Remaining risk / assumption:
  - T131 is heuristic and deterministic; it proves the safe planning surface and contract wiring, but not yet the final quality ceiling of relationship-aware wording.
  - The current verification used a synthetic safe context, not a larger runtime sample set, so candidate quality across more relationship types still needs review in T132 or manual evaluation.

## 24. T131 Review Decision

- Review file: `docs/review/T131_review.md`
- Verdict: `PASS_WITH_WARNINGS`
- Captain decision:
  - T131 is complete within task scope.
  - M3 is not complete yet; do not enter M4.
  - Current Unique Task moves to T132 Reply Policy.
- Warning handling:
  - N01 accepted/deferred: hardcoded templates and shallow relationship-awareness are acknowledged; deferred to R035 and T132/T133.
  - N02 accepted: hardcoded confidence values are acceptable for contract-wiring MVP.
  - N03 accepted/deferred: unused `strategy_hints` and `relationship_summary` are acknowledged; deferred to R035 and T132/T133.
  - N04 deferred: no committed tests/fixtures; deferred to R036 and T150.
  - N05 accepted: `_dedupe(values)` missing type annotation is low-risk style debt.
  - N06 accepted: enum fallback is sufficient for current MVP.

## 25. T132 Kickoff Notes

- Task package:
  - `docs/tasks/M3_relationship_reply_planner/T132_reply_policy.md`
- Worker focus:
  - Add boundary / avoid-topic / over-proactivity / impersonation risk checks to the existing T131 planner path.
  - Preserve review-only output and T130 `ReplyPlan` contract.
  - Keep the existing T131 contact alignment and ranking validation.
  - Use safe synthetic or redacted fixtures only.
- Reviewer focus:
  - Confirm no auto-send, DB, vector DB, realtime integration, raw transcript read, or full store JSON injection.
  - Confirm sensitive or boundary scenarios produce conservative candidates and explicit risk flags.
  - Confirm T132 does not claim final relationship-quality completion.

## 26. T132 Implementation Record

- Files changed:
  - `src/practical_chat_agent/services/reply_planner.py`
  - `src/practical_chat_agent/services/policy.py`
  - `docs/07_handoff.md`
- Implemented:
  - Added a reply-planning policy layer in `policy.py`:
    - `ReplyPlanPolicyProfile`
    - `ReplyCandidatePolicyAssessment`
    - `ReplyPlanPolicyEngine`
  - The new policy engine evaluates compact runtime context and candidate drafts for:
    - `boundary_sensitive`
    - `over_proactive`
    - `impersonation_risk`
    - `thin_context`
  - `ReplyPlanner` now builds a context-level policy profile before composing the plan, then applies candidate-level policy review when assembling each `ReplyPlanCandidate`.
  - Sensitive or boundary-heavy context now changes planner behavior in two ways:
    - policy-level summaries and boundary reminders become more explicit
    - draft templates switch to a more conservative, no-pressure wording set instead of the baseline T131 wording
  - Thin-context handling is now explicit through the policy layer rather than only through a generic boundary string:
    - candidate `risk_flags` carry `thin_context`
    - `policy_boundary_summary` explains that relationship-specific assumptions should be avoided
    - candidate confidence is reduced conservatively
  - Over-proactivity is now candidate-specific:
    - optional follow-up or next-step language is only escalated into `over_proactive` when the context is thin or boundary-sensitive
    - clearly no-pressure wording such as “先不往前推 / 不用现在展开” is exempted from false-positive `over_proactive` flags
  - Impersonation risk is now explicitly detectable at the candidate-text level, even though the current T131/T132 templates do not intentionally generate such text.
  - T131 checks remain intact:
    - `contact_id` alignment still enforced
    - `priority_rank` uniqueness and stable `1..N` ordering still enforced
    - output remains review-only `ReplyPlan`, not send logic
- Verification:
  - Compile passed:
    - `& 'C:\ProgramData\anaconda3\envs\practical-chat-agent\python.exe' -m compileall src/practical_chat_agent/services/reply_planner.py src/practical_chat_agent/services/policy.py src/practical_chat_agent/app/main.py`
  - Safe synthetic verification passed with three inline contexts:
    - baseline context:
      - approved contact-skill present
      - 3 candidates emitted
      - no raw input text echoed
      - no accidental `boundary_sensitive` / `over_proactive` over-blocking
    - boundary / avoid-topic context:
      - approved contact-skill carried explicit “give space / do not push” style reminders
      - 3 candidates emitted
      - at least one candidate carried `boundary_sensitive`
      - at least one candidate carried `over_proactive`
      - boundary reminders included explicit caution language
      - wording shifted to more conservative no-pressure drafts
    - thin-context context:
      - `approved_store_status = not_configured`
      - 3 candidates emitted
      - all candidates carried `thin_context`
      - boundary reminders explicitly warned against over-claiming familiarity
      - confidence stayed below the safe baseline and wording shifted to the conservative template set
  - Privacy / safety checks from the synthetic verification:
    - raw synthetic inbound text did not appear in the emitted `ReplyPlan`
    - output remained limited to compact ids, evidence refs, runtime ids, policy summaries, and candidate text
    - no `private/chat_history/` reads, no DB/persistence expansion, no vector DB, no send automation
- Remaining risk / assumption:
  - T132 improves safety behavior, but it is still heuristic keyword-based policy logic rather than evidence-weighted semantic classification.
  - The current policy layer does not yet use committed automated tests or committed synthetic fixtures; that regression coverage remains deferred to T150.
  - Relationship-aware wording quality is still limited by T131/T132 deterministic templates; T133 holdout evaluation is still needed before claiming strong reply quality.

## 27. T132 Review Decision

- Review file: `docs/review/T132_review.md`
- Verdict: `PASS_WITH_WARNINGS`
- Captain decision:
  - T132 is complete within task scope.
  - M3 is not complete yet; do not enter M4.
  - Current Unique Task moves to T133 Holdout Eval.
- Warning handling:
  - N01 accepted: runtime text is consumed for keyword detection only and is not echoed.
  - N02 accepted: broad keyword risk is mitigated by compound trigger logic.
  - N03 accepted/deferred: substring false-positive risk is acknowledged; deferred to R037 and T133/T150.
  - N04 accepted: `_dedupe` duplication is low-risk refactor debt.
  - N05 deferred: no committed tests/fixtures; folded into R036 and T150.
  - N06 accepted: duplicate terminal branch has no correctness impact.
  - N07 accepted: approved memory claim text is bounded and used for detection only.

## 28. T133 Kickoff Notes

- Task package:
  - `docs/tasks/M3_relationship_reply_planner/T133_holdout_eval.md`
- Worker focus:
  - Run an anonymized holdout evaluation of T130-T132 ReplyPlanner behavior.
  - Assess naturalness, boundary adherence, evidence/reference usage, policy risk flags, and privacy safety.
  - Produce `docs/review/T133_milestone_review.md` with Gate M3 verdict: `Allow`, `Conditional`, or `Block`.
  - Update `docs/07_handoff.md` with eval summary and remaining risks.
- Reviewer focus:
  - Confirm no private raw content or identifying details entered committed docs.
  - Confirm the eval did not modify planner code or advance M4.
  - Confirm Gate M3 verdict is supported by evidence rather than assertion.

## 29. T133 Eval Record

- Private eval artifacts produced under:
  - `private/distilled/t133_holdout_eval/contexts/*.context.json`
  - `private/distilled/t133_holdout_eval/plans/*.reply_plan.json`
  - `private/distilled/t133_holdout_eval/eval_summary.json`
- Eval coverage:
  - 6/6 synthetic anonymized scenarios produced valid 3-candidate ReplyPlans.
  - Baseline and work cases stayed low-pressure and review-only.
  - Sensitive and thin-context cases became more conservative, with explicit boundary flags.
  - False-positive probe showed the policy layer can still swing conservative on a normal-looking work prompt.
  - False-negative probe showed subtle pacing risk may still be under-detected when no explicit boundary cue is present.
- Gate M3 verdict:
  - `Conditional`
- Handoff note:
  - Keep T131/T132/T133 treated as review-only planning proof, not as final relationship-quality proof.
  - Next recommended action for Captain: review T133, carry the conditions into T150, and only then decide whether M4 can proceed.

## 30. T133 Review Decision

- Review file: `docs/review/T133_review.md`
- Verdict: `PASS_WITH_WARNINGS`
- Captain decision:
  - T133 is complete within task scope.
  - Gate M3 remains `Conditional`.
  - M4/T140 may proceed only under the conditions carried in `docs/review/M3_review.md`.
- Warning handling:
  - N01 accepted: self-reported ratings are acceptable for MVP milestone; T150 may add independent review.
  - N02 accepted: 6 synthetic scenarios are reasonable under task constraints.
  - N03 accepted: naturalness 3/5 is honestly reported; do not claim relationship-aware maturity.
  - N04 accepted: evidence usage 3/5 is honestly reported; structural wiring is correct.
  - N05 accepted: H01/H02 detail omission is minor because summary confirms all six scenarios produced valid plans.
  - No deferred warnings.
  - No rejected warnings.

## 31. M3 Review Decision

- Review file: `docs/review/M3_review.md`
- Verdict: `Conditional`
- Completion judgment:
  - M3 is structurally complete: T130 schema, T131 planner, T132 policy layer, and T133 holdout eval are all present.
  - M3 is not quality-mature: drafts remain deterministic/template-driven, naturalness is 3/5, and evidence usage is 3/5.
  - Clean-environment reproducibility is not fully proven because committed regression tests/fixtures are still missing.
- Conditions carried forward:
  - ReplyPlanner remains review-only; no auto-send, realtime platform integration, or LLM drafting expansion.
  - T150 must add committed regression tests for structure, boundary sensitivity, thin context, false positives, subtle false negatives, privacy leakage, contact alignment, and ranking.
  - Do not claim relationship-aware maturity until broader sample recalibration.

## 32. T140 Kickoff Notes

- Task package:
  - `docs/tasks/M4_feedback_loop/T140_feedback_schema_cli.md`
- Worker focus:
  - Define feedback log schema for accept/edit/reject/boundary feedback on `ReplyPlan` candidates.
  - Implement a minimal CLI that records feedback to a private log.
  - Validate candidate references against a supplied `ReplyPlan`.
  - Keep stdout safe and avoid printing full draft text, edited text, private notes, raw transcript, or private paths.
- Forbidden:
  - Do not auto-send.
  - Do not modify ContactSkill, MemoryFact, approved store records, or planner templates automatically.
  - Do not introduce DB/vector DB/realtime integration/LLM calls.
  - Do not read from `private/chat_history/`.
- Reviewer focus:
  - Confirm feedback is recorded but not applied.
  - Confirm all M3 conditional constraints remain intact.
  - Confirm invalid candidate references fail safely.
  - Confirm no private content enters committed docs.

## 33. Roadmap Alignment Decision

- Reference reviewed:
  - `docs/reference/gpt的后续设计思路(更新版).md`
- Captain judgment:
  - The document matches the project direction: review-first, ContactSkill compatibility, delayed platform integration, delayed external memory, and no automatic sending.
  - The task board needed modification because old T141/T142 moved too quickly into proposal/versioning, while M3 is still conditional and T140 has not produced validated feedback yet.
- Changes made:
  - M4 now contains T140 feedback capture, T141 feedback log validator, and T142 feedback summary exporter.
  - M4.5 now contains T150 ReplyPlanner regression tests, T151 policy fixture suite, and T152 feedback CLI regression tests.
  - M5 now starts feedback-to-patch with T160-T164.
  - M6-M12 now describe staged ContactSkill decomposition, optional LLM planner, RelationshipState, MemoryRetriever, BehaviorPlanner, OutboundSendGate/Feishu, and WeChat adapter.
- Current Unique Task remains:
  - T140 Feedback Schema CLI.
- Important non-goals:
  - Do not implement Mem0, Feishu, WeChat, BehaviorPlanner, LLM drafting, or ContactSkill replacement before their gated milestones.

## 34. T140 Implementation Record

- Files changed:
  - `src/practical_chat_agent/core/models.py`
  - `src/practical_chat_agent/services/feedback.py` (new)
  - `src/practical_chat_agent/app/main.py`
  - `docs/07_handoff.md`
- Schema/service/CLI behavior:
  - Added `ReplyFeedbackAction` = Literal["accept", "edit", "reject", "boundary"].
  - Added `ReplyFeedbackRecord` with feedback_id, created_at, contact_id, reply_plan_id, candidate_id, priority_rank, action, user_note, edited_text, boundary_label, boundary_note, source_plan_path.
  - Added `ReplyFeedbackLog` with schema_version, generated_at, records list.
  - `FeedbackService.record_feedback()` loads a ReplyPlan JSON, validates the chosen candidate exists by priority_rank, appends a feedback record to a JSON log file under a private output path.
  - `chat-reply-feedback` CLI: `--plan`, `--candidate-rank`, `--action`, `--output`, `--note`, `--edited-text`, `--boundary-label`, `--boundary-note`.
  - Edit action requires `--edited-text`. Boundary action requires at least one of `--boundary-label` or `--boundary-note`.
  - Invalid candidate rank is rejected with a clear error listing valid ranks.
  - stdout emits only safe summaries: feedback_id, contact_id, candidate_id, priority_rank, action, total_records, output_path. No draft text, edited text, private notes, raw transcript, or private chat path contents are printed.
- Verification:
  - Compile passed for models.py, feedback.py, main.py.
  - Synthetic fixture at `private/distilled/t140_feedback_fixture/synthetic_reply_plan.json`.
  - Accept: feedback record appended, total_records=1.
  - Edit with edited-text: feedback record appended with edited_text field, total_records=2.
  - Reject with note: feedback record appended, total_records=3.
  - Boundary with label+note: feedback record appended with boundary_label and boundary_note, total_records=4.
  - Invalid candidate-rank=99: rejected with error listing valid ranks [1, 2, 3].
  - Edit without --edited-text: rejected with error.
  - stdout contains no draft text, edited text, private notes, or raw transcript content.
  - No ContactSkill, MemoryFact, approved store record, or planner template was modified.
  - Output confined to requested private output path.
- Remaining risks:
  - Feedback log append is not atomic; concurrent writes could corrupt the JSON file. This is acceptable for a private single-user offline tool.
  - No committed automated tests yet; deferred to T150/T152.
  - Feedback records store `source_plan_path` as a string; if the plan file is moved, the path reference becomes stale.
- Explicit non-actions:
  - No memory, ContactSkill, or approved store update was added.
  - No auto-send, realtime integration, DB, vector DB, LLM call, or `private/chat_history/` read was added.

## 35. T140 Review Decision

- Review file:
  - `docs/review/T140_review.md`
- Verdict:
  - `PASS_WITH_WARNINGS`
- Captain decision:
  - T140 is complete within task scope.
  - M4 may continue, but only into validation/summary work; no automatic learning or downstream mutation is authorized.
  - Current Unique Task moves to T141 Feedback Log Validator.
- Warning handling:
  - Accepted:
    - N03 `_count_records` re-reads the log after append. Low-impact inefficiency only.
    - N04 `reply_plan_id` currently stands in for a source-plan identifier. Acceptable until a dedicated `plan_id` exists.
    - N06 `ReplyFeedbackAction` as `Literal[...]` matches current codebase style.
  - Deferred:
    - N01 corrupted-log silent reset/data loss risk. Carry into T141 and R042.
    - N02 `source_plan_path` can become stale or vary by caller path style. Carry into T141-or-later and R043.
    - N05 output path is user-controlled but not enforced to remain private. Carry into T141/T152 and R043.
  - Rejected:
    - none

## 36. T141 Kickoff Notes

- Task package:
  - `docs/tasks/M4_feedback_loop/T141_feedback_log_validator.md`
- Worker focus:
  - implement a read-only validator for T140 feedback logs
  - validate record structure, action-specific required fields, source-plan existence, candidate existence, contact alignment, and safe/private path behavior
  - emit only aggregate/id-based summaries to stdout
  - surface corrupted-log or unreadable-log problems explicitly instead of silently normalizing them away
- Explicit non-goals:
  - no proposal generation
  - no memory or ContactSkill updates
  - no feedback-log mutation
  - no sending, DB/vector DB, LLM, or realtime integration
- Reviewer focus:
  - confirm the validator is read-only
  - confirm broken references and malformed records fail safely
  - confirm stdout/docs do not leak edited text, notes, draft text, or raw private content
  - confirm T141 does not drift into T142/T160/T162 behavior

## 37. T141 Implementation Record

- Files changed:
  - `src/practical_chat_agent/services/feedback.py`
  - `src/practical_chat_agent/app/main.py`
  - `docs/07_handoff.md`
- Validator behavior:
  - Added `FeedbackValidationService` with read-only `validate()` method.
  - Validates feedback log JSON existence, readability, JSON parse, and ReplyFeedbackLog schema.
  - Corrupted or unreadable input is reported explicitly via `corrupted_reason` and `corrupted_input_count`, not silently treated as empty-success.
  - Per-record checks:
    - `edit` action requires `edited_text` (otherwise `edit_without_text` issue).
    - `boundary` action requires at least one of `boundary_label` or `boundary_note` (otherwise `boundary_without_details` issue).
    - If `source_plan_path` is set, resolves the path (absolute, relative to CWD, then relative to log directory) and loads the referenced ReplyPlan.
    - Missing or unparseable plan is reported as `missing_plan`.
    - Candidate not found in plan (by `candidate_id` and `priority_rank`) is reported as `missing_candidate`.
    - `contact_id` mismatch between plan and feedback record is reported as `contact_mismatch`.
  - Privacy checks:
    - `W_PRIVACY_INPUT`: input log path is outside `private/` directory.
    - `W_PRIVACY_REF`: resolved `source_plan_path` is outside `private/` directory.
  - Output is safe: only ids, counts, booleans, warning codes, and safe paths. No draft text, edited text, user notes, boundary notes, or raw transcript content is emitted to stdout.
  - `--strict` flag causes non-zero exit code when any invalid records or privacy warnings exist.
- CLI command:
  - `chat-reply-feedback-validate --input <feedback-log.json> [--strict]`
- Verification:
  - Compile passed for feedback.py and main.py.
  - Good log (T140 fixture, 4 records accept/edit/reject/boundary): `valid_record_count=4`, `invalid_record_count=0`, no issues.
  - Bad log (edit without text, boundary without details): `edit_without_text_count=1`, `boundary_without_details_count=1`, `invalid_record_count=2`.
  - Missing plan reference: `missing_plan_count=1`, record reported invalid.
  - Corrupted JSON: `is_readable=false`, `corrupted_input_count=1`, `corrupted_reason="json_decode_error: ..."`, exit code 1.
  - Schema-invalid log (invalid action value): `corrupted_input_count=1`, `corrupted_reason="schema_error: 1 validation failure(s)"`, exit code 1.
  - Log outside `private/`: `W_PRIVACY_INPUT` warning surfaced. With `--strict`, exit code 1.
  - Log referencing plan outside `private/` (plan exists and is valid): `W_PRIVACY_REF` warning surfaced, record remains valid.
  - Read-only confirmed: md5sums of all fixture files unchanged after running all validations.
  - stdout privacy confirmed: grep for private text fields (edited_text, user_note, boundary_note, draft_text, fixture text content) returned 0 matches.
- Explicit non-actions:
  - No proposal, preference, boundary, memory, or ContactSkill update was added.
  - No feedback log, ReplyPlan, ContactSkill, MemoryFact, approved store, or planner template was mutated.
  - No LLM call, auto-send, realtime platform integration, DB, vector DB, or `private/chat_history/` read was added.

## 38. T141 Review Decision

- Review file:
  - `docs/review/T141_review.md`
- Verdict:
  - `PASS_WITH_WARNINGS`
- Captain decision:
  - T141 is complete within task scope.
  - M4 may continue only into aggregate feedback summary work; no proposal generation or downstream mutation is authorized.
  - Current Unique Task moves to T142 Feedback Summary Exporter.
- Warning handling:
  - Accepted:
    - N01 raw `input_path` in CLI output. Low-risk style inconsistency only.
    - N03 `_is_private_path` uses a coarse directory-name heuristic. Acceptable for MVP.
    - N04 `_resolve_plan_path` depends on CWD for relative paths. Acceptable with the current private/offline workflow.
    - N05 `strict_mode` is stored in the report but not read by the service. Minor dead data only.
  - Deferred:
    - N02 `reply_plan_id` coherence is not cross-checked against the loaded plan context. Carry into T142 if the summary needs to surface it.
    - N06 `record_results` may grow large on bigger logs. Carry into T142 as a compact-output concern.
  - Rejected:
    - none

## 39. T142 Kickoff Notes

- Task package:
  - `docs/tasks/M4_feedback_loop/T142_feedback_summary_exporter.md`
- Worker focus:
  - export aggregate, privacy-safe summaries over T140/T141 feedback logs
  - prefer validated inputs or internally validated summary paths
  - keep stdout concise and aggregate-only
  - surface invalid/skipped/warning counts without echoing per-record private text
- Explicit non-goals:
  - no proposal generation
  - no feedback-to-patch logic
  - no versioning, rollback, or freeze flow
  - no ContactSkill or Memory mutation
  - no LLM call, auto-send, realtime platform integration, DB, vector DB, or `private/chat_history/` read
- Reviewer focus:
  - confirm output is aggregate and privacy-safe
  - confirm T142 stays within M4 capture/validation/summary scope only
  - confirm any `reply_plan_id` coherence handling remains descriptive and non-mutating

## 40. T142 Implementation Record

- Files changed:
  - `src/practical_chat_agent/services/feedback.py`
  - `src/practical_chat_agent/app/main.py`
  - `docs/07_handoff.md`
- Summary service behavior:
  - Added `FeedbackSummaryService` with read-only `summarize()` method.
  - Reads a T140 feedback log JSON file and computes aggregate counts.
  - Aggregate fields in summary output:
    - `total_records`: total feedback record count
    - `counts_by_action`: count by action type (accept/edit/reject/boundary)
    - `distinct_contact_ids`: number of distinct contact ids
    - `distinct_candidate_ids`: number of distinct candidate ids
    - `distinct_reply_plan_ids`: number of distinct reply_plan_ids
    - `distinct_source_plan_paths`: number of distinct source_plan_path values
    - `records_with_boundary_label`: count of records with a boundary_label set
    - `records_with_edited_text`: count of records with edited_text set
    - `records_with_user_note`: count of records with user_note set
    - `counts_by_approach_label`: count by candidate approach_label (best-effort, loaded from referenced plans; empty when plans are not resolvable)
    - `time_range`: earliest and latest record timestamps
    - `validation_summary`: merged T141 validation report aggregates (optional)
  - Corrupted or unreadable input is reported via `is_readable: false` and `corrupted_reason`, consistent with T141 handling.
  - Optional `--validation-report` reads a T141 validation report and merges only aggregate counts (valid/invalid counts, missing_plan_count, missing_candidate_count, contact_mismatch_count, edit_without_text_count, boundary_without_details_count, privacy_warning_count). Raw record payloads are not printed.
  - Optional `--output` writes the full summary JSON to a private output path.
  - No draft text, edited text, user notes, boundary notes, or raw transcript content appears in stdout or output file.
- CLI command:
  - `chat-reply-feedback-summary --input <feedback.json> [--output <private summary.json>] [--validation-report <report.json>]`
- Verification:
  - Compile passed for feedback.py and main.py.
  - Good log (T140 fixture, 4 records accept/edit/reject/boundary): `total_records=4`, `counts_by_action={accept:1, edit:1, reject:1, boundary:1}`, `distinct_candidate_ids=3`, `counts_by_approach_label={conservative_acknowledgment:2, light_follow_up:1, warm_but_guarded:1}`, approach labels loaded from referenced plan.
  - Good log with validation report and output file: `validation_summary.status=merged`, `valid_record_count=4`, `invalid_record_count=0`, summary JSON written to output path.
  - Bad log (edit without text, boundary without details): `total_records=2`, `counts_by_action={edit:1, boundary:1}`, approach labels loaded from referenced plan.
  - Missing plan log: `total_records=1`, `counts_by_approach_label={}` (plan not resolvable, approach_label unavailable). With validation report: `validation_summary.missing_plan_count=1`, `invalid_record_count=1`.
  - Corrupted JSON: `is_readable=false`, `corrupted_reason="json_decode_error: ..."`, exit code 1.
  - Non-existent validation report: `validation_summary.status=report_not_found`.
  - Privacy confirmed: grep for private text field values (edited text content, user note content, boundary note content) in stdout and output file returned 0 matches.
  - Read-only confirmed: md5sums of all input fixture files unchanged after all summary runs.
  - No ContactSkill, MemoryFact, approved store record, or planner template was modified.
- Explicit non-actions:
  - No proposal, preference, boundary, memory, or ContactSkill update was added.
  - No feedback log, ReplyPlan, ContactSkill, MemoryFact, approved store, or planner template was mutated.
  - No LLM call, auto-send, realtime platform integration, DB, vector DB, or `private/chat_history/` read was added.

## 41. T142 Review Decision

- Review file:
  - `docs/review/T142_review.md`
- Verdict:
  - `PASS_WITH_WARNINGS`
- Captain decision:
  - T142 is complete within task scope.
  - M4 implementation scope is now complete: feedback can be recorded, validated, and summarized in a review-only flow.
  - No T142 warning is blocking enough to require an automatic repair pass.
- Warning handling:
  - Accepted:
    - N01 duplicated `_resolve_plan_path` / `_load_plan_safe` helpers
    - N02 raw `input_path` in stdout
    - N03 low-risk aggregate existence-pattern counts
    - N04 unreadable input may still produce an output artifact
    - N05 untyped summary `dict`
    - N06 no `reason_tag` / `policy_risk_flag` aggregation because those fields do not yet exist
  - Deferred:
    - none
  - Rejected:
    - none

## 42. M4 Review Decision

- Review file:
  - `docs/review/M4_review.md`
- Verdict:
  - `Conditional`
- Completion judgment:
  - M4 is functionally complete for intended scope: T140/T141/T142 deliver feedback record, validation, and aggregate summary.
  - No blocking pseudo-completion was found.
  - Clean-environment reproducibility is still not proven from committed repo contents alone because committed tests and committed synthetic fixtures are still missing.
- Gate decision:
  - Do not proceed to M5 yet.
  - Proceed only to M4.5 regression hardening.

## 43. T150 Kickoff Notes

- Task package:
  - `docs/tasks/M4_5_regression_hardening/T150_replyplanner_regression_tests.md`
- Worker focus:
  - add committed deterministic tests for ReplyPlanner structure, privacy, ranking, contact alignment, thin-context behavior, and baseline policy behavior
  - use only synthetic or redacted fixtures
  - reduce the reproducibility gap that currently keeps M4 at `Conditional`
- Explicit non-goals:
  - no planner implementation changes unless Captain opens a bug-fix task
  - no T140-T142 feedback CLI regression work in this task
  - no LLM, auto-send, realtime integration, DB, vector DB, or UI work
- Reviewer focus:
  - confirm tests are committed, deterministic, and privacy-safe
  - confirm fixtures are synthetic/redacted
  - confirm M3/M4 gate obligations are actually encoded as tests rather than restated in docs

## 44. T150 Implementation Record

- Files changed:
  - `tests/__init__.py` (new)
  - `tests/helpers.py` (new)
  - `tests/conftest.py` (new)
  - `tests/test_reply_planner.py` (new)
  - `pyproject.toml` (added `[tool.pytest.ini_options]` with `pythonpath` and `testpaths`)
  - `docs/07_handoff.md`
  - `docs/08_risks_and_open_questions.md`
- Fixture shape:
  - All fixtures are synthetic Python objects constructed via `tests/helpers.py` helpers.
  - No JSON fixture files, no raw transcript text, no real names, real platform IDs, or private paths.
  - Seven reusable fixture contexts: baseline friend, colleague, thin, sensitive/boundary, false-positive probe, false-negative probe, privacy leakage probe.
  - Each fixture constructs `ChatContext` with appropriate `ApprovedStoreContext`, `ApprovedContactSkillBrief`, `ApprovedMemoryFactBrief`, events, and memory hits.
- Test command and result:
  - `PYTHONPATH='src' pytest tests -v`
  - 49 tests passed in 0.10s, 0 failures.
  - No LLM calls, no network access, no private file reads.
- Tests intentionally marking current limitations:
  - `TestFalseNegativeProbe`: documents that subtle inbound pacing pressure ("you should really call me sometime soon") is not detected by keyword-based policy. This is an accepted M3 Conditional limitation, not an xfail. The test asserts current expected behavior.
  - `TestFalsePositiveProbe`: documents that "money" in a work-budgeting context triggers `sensitive_topic=True` but does NOT escalate to `boundary_sensitive` because intent is GENERAL and no boundary cues exist. This is correct current behavior but documents the keyword proximity risk.
- Coverage of M3 Conditional obligations:
  - Candidate structure: `TestBaselineFriendContext`, `TestColleagueContext`, `TestStructureRegression::test_candidate_structure_regression_guard`
  - Privacy leakage: `TestPrivacyLeakage` (5 tests), `TestStructureRegression::test_privacy_regression_guard`
  - Contact alignment: `TestContactIdMismatch` (2 tests), `TestStructureRegression::test_contact_alignment_regression_guard`
  - Ranking invariants: `TestPriorityRank` (4 tests), `TestStructureRegression::test_ranking_invariant_regression_guard`
  - Thin-context behavior: `TestThinContext` (5 tests)
  - Boundary/sensitive behavior: `TestSensitiveContext` (4 tests)
  - False-positive boundedness: `TestFalsePositiveProbe` (4 tests)
  - False-negative documentation: `TestFalseNegativeProbe` (3 tests)
  - Not-configured path: `TestNotConfiguredPath` (5 tests)
  - Non-approved id isolation: `TestNonApprovedRecordIdIsolation` (2 tests)
- Which M3 risks were reduced:
  - R036 (no committed tests/fixtures): reduced. ReplyPlanner now has 49 committed deterministic tests and 7 synthetic fixture contexts.
  - R034 (priority_rank / contact alignment): regression-guarded. Both now have committed tests.
  - R037 (false-positive/false-negative keyword risk): documented with committed tests encoding current behavior.
- Which M3 risks remain open:
  - R035 (relationship-aware quality still template-driven): not addressed by T150. T150 tests the contract wiring and safety surface, not naturalness.
  - R037 (keyword-only policy): false-negative gap is documented but not fixed. A future semantic classifier could close this.
  - R046 (M3/M4 clean-environment reproducibility): partially reduced. T150 covers ReplyPlanner; T151/T152 must still cover policy fixtures and feedback CLI.

## 45. T150 Review Decision

- Review file:
  - `docs/review/T150_review.md`
- Verdict:
  - `PASS_WITH_WARNINGS`
- Captain decision:
  - T150 is complete within task scope.
  - The repo now has committed deterministic ReplyPlanner regression coverage and may move forward to T151.
  - No T150 warning is blocking enough to require an automatic repair pass.
- Warning handling:
  - Accepted:
    - N01 `TestNotConfiguredPath` overlaps with `thin_context`, but still checks a distinct invariant.
    - N02 no direct `ReplyPlanPolicyEngine` unit tests yet; this is better treated as T151 follow-up scope than as a T150 defect.
    - N03 `practical` summary wording assertion is intentionally brittle as a regression guard.
    - N04 false-negative probes intentionally encode current missed-detection behavior.
    - N05 `tests/helpers.py` constructors are simple enough that missing isolated helper tests is low risk.
    - N06 `notes_on_candidate_differences` is not yet asserted and remains optional coverage expansion.
  - Deferred:
    - none
  - Rejected:
    - none

## 46. T151 Kickoff Notes

- Task package:
  - `docs/tasks/M4_5_regression_hardening/T151_policy_fixture_suite.md`
- Worker focus:
  - turn policy behavior into an explicit committed fixture suite on top of the new T150 base
  - add direct policy-layer assertions where they materially improve auditability
  - keep all fixtures synthetic/redacted and keep the task non-mutating
- Specific follow-ups from T150 review:
  - add direct `ReplyPlanPolicyEngine` coverage where planner-only coverage is too indirect
  - separate missing-store-path or loaded-without-skill coverage more clearly from generic thin-context coverage
  - consider assertions for `notes_on_candidate_differences` when policy state should surface there
- Explicit non-goals:
  - no planner or policy behavior changes unless Captain opens a bug-fix task
  - no feedback CLI regression work in this task
  - no LLM, auto-send, realtime integration, DB, vector DB, or UI work
- Reviewer focus:
  - confirm direct policy expectations are genuinely encoded in committed tests
  - confirm fixtures remain synthetic and privacy-safe
  - confirm T151 narrows reproducibility risk without overstating relationship-aware maturity

## 47. T151 Implementation Record

- Files changed:
  - `tests/conftest.py` (added 3 new fixtures: `loaded_no_skill_context`, `degraded_store_context`, `over_proactivity_probe_context`; fixed `baseline_friend_context` to remove accidental boundary cue keywords)
  - `tests/test_policy_engine.py` (new: 67 direct policy engine tests)
  - `docs/07_handoff.md`
  - `docs/08_risks_and_open_questions.md`
- Fixture shape:
  - All fixtures are synthetic Python objects constructed via `tests/helpers.py` helpers.
  - No JSON fixture files, no raw transcript text, no real names, real platform IDs, or private paths.
  - 10 reusable fixture contexts: baseline friend, colleague, thin, sensitive/boundary, false-positive probe, false-negative probe, privacy leakage probe, loaded-but-no-skill, degraded-store (store_path_missing), over-proactivity probe.
  - `baseline_friend_context` was corrected: previous `strategy_hints=["keep warm but low pressure"]` and `boundary_reminders=["do not push for details"]` inadvertently contained "low pressure" and "do not push" which are in `_BOUNDARY_CUE_KEYWORDS` and `_AVOID_FOLLOW_UP_KEYWORDS`, making the fixture not a clean baseline. Changed to `strategy_hints=["keep warm"]` and `boundary_reminders=["stay friendly and relaxed"]`.
- Test command and result:
  - `PYTHONPATH='src' pytest tests -v`
  - 116 tests passed in 0.17s (49 T150 + 67 T151), 0 failures.
  - No LLM calls, no network access, no private file reads.
- Direct `ReplyPlanPolicyEngine.build_profile()` coverage:
  - `TestBuildProfileBaselineFriend`: thin_context=False, boundary_sensitive=False, conservative_mode=False, practical_tone=False, context_risk_flags=[], avoid_follow_up=False
  - `TestBuildProfileColleague`: practical_tone=True, thin_context=False, conservative_mode=False
  - `TestBuildProfileThinContext`: thin_context=True, conservative_mode=True, context_risk_flags=["thin_context"]
  - `TestBuildProfileLoadedNoSkill`: thin_context=True despite status="loaded", conservative_mode=True, boundary_sensitive=False (no boundary cues)
  - `TestBuildProfileDegradedStore`: thin_context=True for status="store_path_missing", conservative_mode=True
  - `TestBuildProfileSensitive`: boundary_sensitive=True, conservative_mode=True, avoid_follow_up=True
  - `TestBuildProfileFalsePositive`: boundary_sensitive=False, conservative_mode=False ("money" in work context)
  - `TestBuildProfileFalseNegative`: boundary_sensitive=False, conservative_mode=False (documented limitation)
  - `TestBuildProfileOverProactivity`: avoid_follow_up=True, boundary_sensitive=True, conservative_mode=True, thin_context=False
- Direct `ReplyPlanPolicyEngine.assess_candidate()` coverage:
  - `TestAssessCandidateActionPush`: action push cues ("call", "meet", "打电话", "schedule") always trigger over_proactive
  - `TestAssessCandidateOverProactiveConservativeMode`: optional_follow_up always triggers in conservative mode; paced_next_step with proactive cues triggers; conservative_acknowledgment without cues stays clean
  - `TestAssessCandidateNoPressureExemption`: "no rush" and Chinese "先不往前推" exempt from over_proactive; action push overrides no-pressure
  - `TestAssessCandidateImpersonationRisk`: "he would say", "she would say", "对方会" all detected; clean text produces no impersonation_risk
  - `TestAssessCandidateConfidencePenalty`: thin_context 0.10, boundary_sensitive 0.06, combined 0.16, impersonation 0.15, clean 0.0
- `notes_on_candidate_differences` coverage:
  - Baseline: 3 default notes about each candidate
  - Conservative mode (sensitive context): notes shifted to no-pressure/avoiding language
  - Thin not-loaded (thin_context fixture): extra "thin" note appended
  - Loaded-no-skill: conservative notes but NO extra "thin" note (status IS "loaded")
  - Boundary-sensitive: extra note about sensitive/boundary context
- Over-proactivity planner integration:
  - `TestOverProactivityPlannerIntegration`: over_proactivity_probe_context produces plan with at least one over_proactive risk flag in candidates; all candidates remain valid
- Tests intentionally marking current limitations:
  - `TestBuildProfileFalseNegative`: documents that "you should really call me sometime soon" is not detected. Accepted M3 Conditional limitation.
  - `TestBuildProfileFalsePositive`: documents that "money" in work context triggers sensitive_topic=True at the keyword level but does NOT escalate to boundary_sensitive. This is correct behavior.
- Coverage of T151 task requirements:
  - baseline friend: `TestBuildProfileBaselineFriend` (6 tests)
  - practical colleague: `TestBuildProfileColleague` (5 tests)
  - explicit sensitive boundary: `TestBuildProfileSensitive` (5 tests)
  - thin context: `TestBuildProfileThinContext` (5 tests)
  - false-positive policy probe: `TestBuildProfileFalsePositive` (4 tests)
  - subtle false-negative probe: `TestBuildProfileFalseNegative` (3 tests)
  - impersonation-risk probe: `TestAssessCandidateImpersonationRisk` (5 tests)
  - over-proactivity probe: `TestBuildProfileOverProactivity` (4 tests) + `TestOverProactivityPlannerIntegration` (2 tests)
  - loaded-but-skill-missing: `TestBuildProfileLoadedNoSkill` (4 tests)
  - degraded store: `TestBuildProfileDegradedStore` (4 tests)
  - direct policy engine coverage: all build_profile + all assess_candidate tests
  - notes_on_candidate_differences: `TestNotesOnCandidateDifferences` (5 tests)
- Which M3/M4 risks were reduced:
  - R036 further narrowed: policy layer now has 67 committed direct tests on top of T150's 49 planner-through-policy tests.
  - R037 further documented: false-positive, false-negative, over-proactivity, and impersonation detection behavior all have direct policy engine tests encoding current expected behavior.
  - R046 further narrowed: clean-environment reproducibility now covers both ReplyPlanner surface and direct policy engine behavior. T152 must still cover feedback CLI.
- Which risks remain open:
  - R035 (relationship-aware quality still template-driven): not addressed by T151.
  - R037 (keyword-only policy): false-negative gap is documented but not fixed.
  - R046 (clean-environment reproducibility): T152 must still cover feedback CLI regression tests.

## 48. T151 Review Decision

- Review file:
  - `docs/review/T151_review.md`
- Verdict:
  - `PASS_WITH_WARNINGS`
- Captain decision:
  - T151 is complete within task scope.
  - The repo now has committed deterministic direct policy-engine coverage in addition to T150 planner regression coverage.
  - No T151 warning is blocking enough to require an automatic repair pass.
- Warning handling:
  - Accepted:
    - N01 `_candidate_is_over_proactive` conservative fallback branch is not independently tested, but the uncovered branch is minor and functionally close to already-covered logic.
    - N02 confidence-penalty combinations are not exhaustively enumerated, but the penalty components and representative additive behavior are already covered.
    - N03 the baseline fixture contamination discovered during T151 is accepted as a useful correction uncovered by the new direct tests, not as a reason to reopen T150.
  - Deferred:
    - none
  - Rejected:
    - none

## 49. T152 Kickoff Notes

- Task package:
  - `docs/tasks/M4_5_regression_hardening/T152_feedback_cli_regression_tests.md`
- Worker focus:
  - add committed deterministic regression tests for the T140-T142 feedback capture, validation, and summary CLI loop
  - prove privacy-safe stdout behavior, explicit corrupted-log surfacing, compact validation/summary behavior, and non-mutation guarantees from committed repo contents alone
  - keep all fixtures synthetic/redacted and keep the task non-mutating
- Explicit non-goals:
  - no feedback-to-patch logic
  - no ContactSkill or Memory mutation
  - no planner, policy, or feedback implementation changes unless Captain opens a bug-fix task
  - no LLM, auto-send, realtime integration, DB, vector DB, or UI work
- Reviewer focus:
  - confirm tests prove M4 remains record/validate/summarize only
  - confirm stdout and artifacts do not leak draft text, edited text, notes, raw transcript content, or private chat paths
  - confirm the committed tests are sufficient to narrow or close the remaining clean-environment reproducibility gap for M4

## 50. T152 Implementation Record

- Files changed:
  - `tests/test_feedback_cli.py` (new: 60 feedback CLI regression tests)
  - `docs/07_handoff.md`
  - `docs/08_risks_and_open_questions.md`
- Fixture shape:
  - All fixtures are synthetic Python objects constructed via inline helpers in `tests/test_feedback_cli.py`.
  - No JSON fixture files, no raw transcript text, no real names, real platform IDs, or private paths.
  - `_synthetic_reply_plan()`: minimal 3-candidate ReplyPlan with safe ids and safe text.
  - `_write_plan()`: serializes a synthetic ReplyPlan to a temp file.
  - `_write_feedback_log()`: serializes synthetic feedback records to a temp file.
  - `_make_record()`: constructs a `ReplyFeedbackRecord` with sensible defaults.
  - Uses `pytest` `tmp_path` for all temp files; no committed filesystem artifacts.
- Test command and result:
  - `PYTHONPATH='src' pytest tests -v`
  - 176 tests passed in 1.30s (60 T152 + 67 T151 + 49 T150), 0 failures.
  - No LLM calls, no network access, no private file reads.
- Coverage of T152 task requirements:
  - `accept` feedback append: `TestFeedbackAppendAccept` (2 tests)
  - `edit` feedback append: `TestFeedbackAppendEdit` (3 tests)
  - `reject` feedback append: `TestFeedbackAppendReject` (2 tests)
  - `boundary` feedback append: `TestFeedbackAppendBoundary` (3 tests)
  - invalid candidate rank/id rejected: `TestFeedbackInvalidInputs` (4 tests)
  - invalid plan path rejected: `TestFeedbackInvalidInputs::test_missing_plan_file_rejected`, `test_invalid_plan_json_rejected`
  - validator catches invalid action-specific fields: `TestValidationActionSpecific` (3 tests)
  - summary exporter reports aggregate counts: `TestSummaryAggregateCounts` (5 tests)
  - validator report merge into summary: `TestSummaryValidationMerge` (3 tests)
  - stdout does not print private text: `TestPrivacySafety` (7 tests)
  - feedback flow does not mutate memory/ContactSkill/store: `TestNonMutation` (4 tests)
  - private output confinement: `TestPrivateOutputConfinement` (3 tests)
  - corrupted/unreadable input surfaced explicitly: `TestCorruptedInput` (7 tests)
  - compact validation/summary output: `TestCompactOutput` (4 tests)
  - end-to-end CLI regression: `TestCLIAppendRegression` (3 tests), `TestCLIValidateRegression` (2 tests), `TestCLISummarizeRegression` (3 tests)
- Coverage of T140/T141/T142 obligations:
  - T140 obligations tested: accept/edit/reject/boundary append, invalid rank rejection, invalid plan rejection, edit-without-text rejection, boundary-without-details rejection, output-only privacy, non-mutation of plan file.
  - T141 obligations tested: action-specific field validation (edit_without_text, boundary_without_details), missing-plan detection, missing-candidate detection, contact-mismatch detection, corrupted JSON/schema/missing-file surfacing, privacy warnings (W_PRIVACY_INPUT, W_PRIVACY_REF), read-only confirmation.
  - T142 obligations tested: aggregate counts (total, by action, distinct ids, boundary/edited/note counts, approach labels), validation report merge (aggregate-only, no raw record_results), corrupted input handling, output file writing, read-only confirmation.
- Which M4 risks were reduced:
  - R046 (clean-environment reproducibility): closed for M4.5. T150/T151/T152 together provide 176 committed deterministic tests covering ReplyPlanner, policy engine, and the full feedback CLI loop. Clean-environment reproducibility is now proven from committed repo contents alone.
  - R042 (corrupted-log silent reset): regression-guarded. Corrupted JSON, schema-invalid, and missing-file inputs are all tested to surface explicit errors rather than silent normalization.
  - R043 (path handling): regression-guarded. Privacy warnings for non-private input paths and non-private plan references are tested.
  - R044 (reply_plan_id coherence): remains active but is now regression-guarded for the paths T142 already covers (distinct counts in summary, reference tracking in validation).
  - R045 (verbose record_results): regression-guarded. Compact output tests verify that validation report and summary do not echo per-record private text.
- Which risks remain open:
  - R035 (relationship-aware quality still template-driven): not addressed by T152.
  - R037 (keyword-only policy): not addressed by T152; documented in T151 tests.
  - R038 (feedback log may be mistaken for automatic learning): not addressed by T152; M4 design constraint still applies.

## 51. T152 Review Decision

- Review file:
  - `docs/review/T152_review.md`
- Verdict:
  - `PASS_WITH_WARNINGS`
- Captain decision:
  - T152 is complete within task scope.
  - M4.5 regression hardening is now complete across T150/T151/T152.
  - No T152 warning is blocking enough to require an automatic repair pass.
- Warning handling:
  - Accepted:
    - N03 `--validation-report` flag coverage is service-level rather than full CLI end-to-end, but the underlying merge behavior is directly regression-tested and adequate.
    - N04 there is no single append->validate->summarize integration test, but the service/CLI slices are covered strongly enough to accept the task.
    - N05 `test_approach_labels_loaded` is intentionally brittle as a regression guard and acceptable.
  - Deferred:
    - N01 validation `record_results` still has no explicit size bound on large logs.
    - N02 service-level output-path confinement is still warning/convention based rather than hard-enforced.
  - Rejected:
    - none

## 52. M4.5 Milestone Review

- Review file:
  - `docs/review/M4_5_review.md`
- Verdict:
  - `Allow`
- Captain conclusion:
  - M4.5 has satisfied its purpose: M3/M4 behavior is now reproducible from committed repo contents alone.
  - The project may now enter M5, but only at the schema-only candidate layer.
  - M5 remains review-only: no auto-apply, no runtime injection, no automatic ContactSkill/Memory mutation, and no outbound send behavior.

## 53. T160 Kickoff Notes

- Task package:
  - `docs/tasks/M5_feedback_to_patch/T160_preference_patch_schema.md`
- Worker focus:
  - define a review-only `PreferencePatchCandidate` contract and its supporting enums/metadata shape
  - keep the output candidate-only and evidence-backed via `supporting_feedback_ids`
  - prepare later clustering/review/runtime tasks without implementing them
- Explicit non-goals:
  - no clustering
  - no proposal generation
  - no review CLI
  - no runtime injection
  - no auto-approve or auto-apply behavior
  - no LLM, no outbound send behavior, no platform integration
- Reviewer focus:
  - confirm the schema is explicit enough for later M5 tasks without smuggling in runtime behavior
  - confirm candidate-only status and review metadata are encoded structurally
  - confirm empty or missing supporting feedback evidence is rejected or marked unsafe

## 54. T160 Implementation Record

- Files changed:
  - `src/practical_chat_agent/core/models.py`
  - `docs/data_contracts/preference_patch_contract.md` (new)
  - `docs/07_handoff.md`
  - `docs/08_risks_and_open_questions.md`
- Model/enum names added:
  - `PreferencePatchType` (Literal with 8 values: tone_preference, length_preference, boundary_preference, topic_preference, question_style, humor_style, repair_style, proactivity_preference)
  - `PreferencePatchCandidate` (Pydantic BaseModel)
- Schema design:
  - `supporting_feedback_ids` has `min_length=1`, structurally requiring evidence. Empty list is rejected by Pydantic validation.
  - `status` defaults to `"candidate"` using existing `DistillationStatus` literal.
  - `review_metadata` reuses `DistilledArtifactReviewMetadata`, which defaults to `reviewed_by_human=False` and `last_decision=None`, so `is_runtime_ready()` returns `False` by default.
  - `is_runtime_ready()` on the model requires `status == "approved"` AND `reviewed_by_human == True` AND `last_decision == "approved"`.
  - No field stores raw transcript text, edited text, private notes, or raw feedback content.
  - `positive_examples` and `negative_examples` are free-form string lists for safe references or summaries only.
  - `supporting_cluster_ids` is optional for future T161 cluster output.
  - `affected_candidate_types` is a free-form string list for approach labels or candidate shapes this patch would influence.
- Synthetic validation example:
  - Created a `PreferencePatchCandidate` with `patch_type="tone_preference"`, `contact_id="contact_lin"`, `supporting_feedback_ids=["fb_abc123", "fb_def456"]`, `claim="Contact prefers concise replies"`, `behavior_instruction="Keep replies short and direct"`, `confidence=0.8`, `sensitivity="low"`.
  - Confirmed: `status == "candidate"`, `is_runtime_ready() == False`, `review_metadata.reviewed_by_human == False`.
  - Confirmed: creating with empty `supporting_feedback_ids=[]` raises Pydantic `ValidationError`.
- How the schema keeps M5 candidate-only:
  - Default status is `"candidate"`, not `"approved"`.
  - `is_runtime_ready()` is gated on human review, matching existing store/review pattern.
  - No field provides or implies a path to mutate ContactSkill, MemoryFact, or runtime prompts.
  - No auto-approve, auto-apply, or runtime injection capability is encoded in the model.
- Follow-up constraints for T161-T164:
  - T161 clustering must produce cluster IDs compatible with `supporting_cluster_ids`.
  - T162 proposal CLI must enforce `supporting_feedback_ids` non-empty; single-feedback patches without clustering are discouraged.
  - T163 review CLI must use the same approval gate as T122: status change requires human reviewer and valid evidence.
  - T164 compact context must only read patches where `is_runtime_ready() == True`, and must not inject `behavior_instruction` directly into runtime prompts without compact context layer.
  - None of T161-T164 may add a field that stores raw feedback text, edited text, or private note bodies.

## 55. T160 Review Decision

- Review file:
  - `docs/review/T160_review.md`
- Verdict:
  - `PASS_WITH_WARNINGS`
- Captain decision:
  - T160 is complete within task scope.
  - The repo now has an explicit candidate-only `PreferencePatchCandidate` contract for M5.
  - No T160 warning is blocking enough to require an automatic repair pass.
- Warning handling:
  - Accepted:
    - N01 `instruction_scope` remains free-form at schema stage. This is acceptable while actual downstream usage is still unknown and later tightening remains available.
    - N04 `schema_version` remains a plain string for consistency with the project's existing model/store pattern.
    - N05 broader working-tree modifications are treated as repository hygiene noise rather than a T160 scope violation, because the task-specific change itself stays within allowed files.
  - Deferred:
    - N02 `positive_examples` and `negative_examples` are not structurally constrained to safe-only summaries/references.
    - N03 no committed automated tests yet cover `PreferencePatchCandidate` validation.
  - Rejected:
    - none

## 56. T161 Kickoff Notes

- Task package:
  - `docs/tasks/M5_feedback_to_patch/T161_feedback_clusterer.md`
- Worker focus:
  - add a deterministic, privacy-safe feedback clustering layer on top of validated T140-T142 records
  - emit stable cluster ids, aggregate labels, counts, and supporting feedback ids only
  - prepare clustered evidence for later T162 patch proposal work without generating patches yet
- Explicit non-goals:
  - no `PreferencePatchCandidate` generation
  - no review CLI
  - no runtime injection
  - no ContactSkill/Memory mutation
  - no outbound send behavior, no realtime integration, no LLM use
- Reviewer focus:
  - confirm clustering is deterministic and aggregate-only
  - confirm stdout/artifacts do not leak draft text, edited text, user notes, boundary notes, or raw feedback text
  - confirm cluster outputs are explicit enough for T162 without silently smuggling in patch-generation behavior

## 57. T161 Implementation Record

- 代码 / 文档改动：
  - `src/practical_chat_agent/services/feedback.py`
  - `src/practical_chat_agent/app/main.py`
  - `docs/data_contracts/preference_patch_contract.md`
  - `docs/07_handoff.md`
  - `docs/08_risks_and_open_questions.md`
- 已实现内容：
  - 新增 `FeedbackClusterService`，消费 T140 `ReplyFeedbackLog` 并输出确定性、隐私安全的聚合聚类。
  - 新增 `chat-feedback-cluster` CLI，支持 `--feedback-log`、`--output`、`--validation-report`。
  - 聚类标签从反馈 action 类型确定性推导：
    - `accept` → `good_tone`
    - `reject` → `not_like_me`
    - `boundary` → `boundary_violation`（若 `boundary_label` 归一化后匹配已知标签则使用该标签）
    - `edit` → 当前无安全确定性标签，标记为 unlabeled
  - 聚类键为 `(contact_id, cluster_label)`，按排序顺序输出。
  - `cluster_id` 由 `sha256(contact_id:label)[:16]` 生成，确保相同分组键始终产生相同 ID。
  - 每个 cluster 输出包含：`cluster_id`、`contact_id`、`cluster_label`、`supporting_feedback_ids`、`record_count`、`counts_by_action`、`counts_by_approach_label`、`counts_by_priority_rank`、`time_range`、`reason_tag_summary`。
  - `--validation-report` 可选参数支持仅聚类 T141 验证通过的记录。
  - stdout 仅输出聚合统计和 ID，不输出原始反馈文本、编辑文本、用户备注或边界备注。
  - 未生成 `PreferencePatchCandidate`、未修改 ContactSkill/Memory/store records、未调用 LLM、未自动 approve 或 apply。
- 聚类输出 shape：
  - Schema: `feedback_cluster_v1`
  - CLI: `chat-feedback-cluster --feedback-log <path> --output <path> [--validation-report <path>]`
- 合成验证示例（将在 verification 阶段产出）：
  - 输入：10 条合成反馈记录（contact_test_001: 3 reject + 2 accept + 2 boundary + 1 edit, contact_test_002: 2 reject）
  - 输出：4 个 cluster（boundary_violation/2, good_tone/2, not_like_me/3 for contact_test_001, not_like_me/2 for contact_test_002）
  - 1 条 unlabeled（edit 记录），1 条 unclustered
  - Cluster ID 稳定性验证通过：相同输入两次运行产生相同的 cluster_id 集合
  - 隐私安全验证通过：输出 JSON 不含 edited_text/user_note/boundary_note/draft_text
  - 不同 contact_id 的相同 label 产生不同的 cluster_id
  - 176 已有测试全部通过，零回归
  - CLI `chat-feedback-cluster --feedback-log <path>` 正常运行
- Cluster ID 与 T160 的关系：
  - `cluster_id` 为 `cluster_<sha256_hex_16>` 格式的字符串，与 `PreferencePatchCandidate.supporting_cluster_ids: list[str]` 兼容
  - T162 可通过 `supporting_cluster_ids` 引用 T161 输出的 cluster
- T162-T164 必须保留的约束：
  - `edit` action 记录当前未被聚类（无安全确定性标签），T162 不可假设 edit 记录已被聚类覆盖
  - cluster label 集合当前为 3 个确定性标签（`good_tone`、`not_like_me`、`boundary_violation`），加上 boundary_label 归一化匹配的已知标签
  - `cluster_id` 依赖分组键内容，不可用随机 ID 替代
  - 输出不含任何原始文本，T162 也不得从 cluster 输出反查原始反馈内容

## 58. T161 Review Decision

- Review file:
  - `docs/review/T161_review.md`
- Verdict:
  - `PASS_WITH_WARNINGS`
- Captain decision:
  - T161 is complete within task scope.
  - The repo now has a deterministic, privacy-safe feedback clustering layer for M5.
  - No T161 warning is blocking enough to require an automatic repair pass.
- Warning handling:
  - Accepted:
    - N01 `reason_tag_summary` is a mildly misleading name, but the field meaning is documented and no data is lost.
    - N03 `counts_by_approach_label` may silently degrade when referenced plan files are unavailable. This is acceptable because the field is optional enrichment.
    - N05 `.claude/settings.json` is a workspace artifact rather than a task-scope violation.
  - Deferred:
    - N02 no committed automated tests yet cover `FeedbackClusterService` / `chat-feedback-cluster`.
    - N04 raw `input_path` remains present in cluster stdout/output.
  - Rejected:
    - none

## 59. T162 Kickoff Notes

- Task package:
  - `docs/tasks/M5_feedback_to_patch/T162_patch_proposal_cli.md`
- Worker focus:
  - convert T161 cluster outputs into deterministic, review-only `PreferencePatchCandidate` proposals
  - preserve explicit evidence via non-empty `supporting_feedback_ids` and `supporting_cluster_ids`
  - skip ambiguous or unlabeled clusters rather than generating speculative patches
- Explicit non-goals:
  - no human review actions yet
  - no auto-approve, auto-apply, or runtime injection
  - no ContactSkill/Memory mutation
  - no outbound send behavior, no realtime integration, no LLM use
  - no raw feedback text, edited text, private notes, or draft text in candidate fields
- Reviewer focus:
  - confirm proposals are deterministic, candidate-only, and evidence-backed
  - confirm ambiguous or edit-only signals are skipped explicitly instead of being over-interpreted
  - confirm stdout/artifacts remain privacy-safe and no runtime mutation behavior is smuggled into the proposal layer

## 60. T162 Implementation Record

- 代码 / 文档改动：
  - `src/practical_chat_agent/services/feedback.py`
  - `src/practical_chat_agent/app/main.py`
  - `docs/data_contracts/preference_patch_contract.md`
  - `docs/07_handoff.md`
  - `docs/08_risks_and_open_questions.md`
- 已实现内容：
  - 新增 `PatchProposalService`，消费 T161 cluster report 并输出确定性、candidate-only `PreferencePatchCandidate` 提案。
  - 新增 `chat-feedback-propose-patch` CLI，支持 `--cluster-report`（必需）和 `--output`（可选）。
  - 确定性标签映射：
    - `too_long` → `length_preference` / sensitivity=low
    - `too_formal` → `tone_preference` / sensitivity=low
    - `too_cold` → `tone_preference` / sensitivity=low
    - `too_eager` → `proactivity_preference` / sensitivity=medium
    - `too_intimate` → `boundary_preference` / sensitivity=high
    - `boundary_violation` → `boundary_preference` / sensitivity=high
  - 跳过规则：
    - `insufficient_support`: record_count < 2 或 supporting_feedback_ids 为空
    - `unlabeled_cluster`: cluster_label 缺失
    - `no_safe_mapping`: cluster_label 不在确定性映射表中（包括 `good_tone`、`not_like_me`、未知标签）
  - `good_tone` 和 `not_like_me` 被跳过而非猜测，因为其聚合信号不足以生成安全的 `behavior_instruction`。
  - 置信度公式：`min(0.3 + 0.15 * (record_count - 1), 0.9)`，与证据强度单调递增，不超过 0.9。
  - 所有生成的 patch 状态为 `candidate`，`review_metadata.reviewed_by_human` 为 `False`，`is_runtime_ready()` 返回 `False`。
  - `positive_examples` 和 `negative_examples` 始终为空列表（proposal 阶段不生成）。
  - `affected_candidate_types` 从 cluster 的 `counts_by_approach_label` 派生。
  - 未修改 ContactSkill/Memory/store records、未调用 LLM、未自动 approve 或 apply、未注入 runtime context。
- Proposal 输出 shape：
  - Schema: `patch_proposal_v1`
  - CLI: `chat-feedback-propose-patch --cluster-report <path> --output <path>`
- 合成验证示例：
  - 输入：含 4 个 cluster 的合成 cluster report（too_long/3、good_tone/2、not_like_me/2、boundary_violation/1）
  - 输出：1 个 candidate（too_long/3 → length_preference, confidence=0.6）
  - 跳过：3 个 cluster（good_tone → no_safe_mapping, not_like_me → no_safe_mapping, boundary_violation/1 → insufficient_support）
  - 每个 candidate 的 `supporting_feedback_ids` 非空
  - `positive_examples` / `negative_examples` 为空列表
  - 重复运行产生相同的 candidate（除时间戳外）
  - 隐私安全：输出不含原始反馈文本、编辑文本、用户备注或边界备注
- T163-T164 必须保留的约束：
  - 提案状态始终为 `candidate`，T163 review CLI 才能将其改为 `approved`
  - `is_runtime_ready()` 依赖 `status == "approved"` 且 `review_metadata.reviewed_by_human == True` 且 `review_metadata.last_decision == "approved"`
  - `positive_examples` / `negative_examples` 在 proposal 阶段为空，T163 review 或后续任务可补充安全摘要
  - `patch_id` 使用 `new_id("patch")` 生成（非确定性），但其他所有字段由 cluster 输入确定性决定
  - T164 只可消费 `status == "approved"` 且 `is_runtime_ready() == True` 的 patch
## 61. T162 Review Decision

- Review file:
  - `docs/review/T162_review.md`
- Verdict:
  - `PASS_WITH_WARNINGS`
- Captain decision:
  - T162 is complete within task scope.
  - The repo now has a deterministic, candidate-only patch proposal layer for M5.
  - No T162 warning is blocking enough to require an automatic repair pass.
- Warning handling:
  - Accepted:
    - N05 `.claude/settings.json` is a workspace artifact rather than a task-scope violation.
  - Deferred:
    - N01 the contract still overclaims deterministic `patch_id` behavior even though implementation uses UUID-based `new_id("patch")`.
    - N02 raw `input_path` remains present in proposal stdout/output.
    - N03 no committed automated tests yet cover `PatchProposalService` / `chat-feedback-propose-patch`.
    - N04 malformed cluster input with empty `contact_id` can still crash proposal generation instead of being skipped defensively.
  - Rejected:
    - none

## 62. T163 Kickoff Notes

- Task package:
  - `docs/tasks/M5_feedback_to_patch/T163_patch_review_cli.md`
- Worker focus:
  - add explicit human review actions for `PreferencePatchCandidate` proposal reports
  - preserve proposal evidence, review metadata, and decision history without mutating runtime state
  - keep approval semantics explicit and separate from runtime context wiring
- Explicit non-goals:
  - no auto-approve or auto-apply
  - no runtime injection or compact-context consumption yet
  - no ContactSkill/Memory mutation
  - no outbound send behavior, no realtime integration, no LLM use
  - no rewriting proposal content or inventing new evidence during review
- Reviewer focus:
  - confirm review actions are explicit, auditable, and human-gated
  - confirm rejected/frozen/archived patches do not become runtime-ready
  - confirm stdout/artifacts remain privacy-safe and no runtime mutation behavior is smuggled into the review layer

## 63. T163 Implementation Record

- 代码 / 文档改动：
  - `src/practical_chat_agent/services/feedback.py`
  - `src/practical_chat_agent/app/main.py`
  - `docs/data_contracts/preference_patch_contract.md`
  - `docs/07_handoff.md`
  - `docs/08_risks_and_open_questions.md`
- 已实现内容：
  - 新增 `PatchReviewService`，对 T162 提案报告中的 `PreferencePatchCandidate` 执行显式人工 review 决策。
  - 新增 `chat-feedback-review-patch` CLI，支持 `--input`（必需）、`--patch-id`（必需）、`--decision`（必需，approve/reject/freeze/archive）、`--reviewer`（必需）、`--note`（可选）、`--output`（可选）。
  - Review CLI 名称：`chat-feedback-review-patch`
  - 决策类型与状态映射：
    - `approve` → `approved`（`is_runtime_ready()` 返回 `True`）
    - `reject` → `rejected`（`is_runtime_ready()` 返回 `False`）
    - `freeze` → `frozen`（`is_runtime_ready()` 返回 `False`）
    - `archive` → `archived`（`is_runtime_ready()` 返回 `False`）
  - 每次决策追加 `DistilledArtifactReviewDecision` 到 `review_metadata.history`，历史不覆盖。
  - `review_metadata.reviewed_by_human`、`last_decision`、`last_reviewed_at`、`last_reviewer_id` 随最新决策更新。
  - Evidence 字段（`supporting_feedback_ids`、`supporting_cluster_ids`、`claim`、`behavior_instruction`、`confidence`、`sensitivity`）在 review 过程中不被修改。
  - 未修改 ContactSkill/Memory/store records、未调用 LLM、未自动 approve 或 apply、未注入 runtime context。
- 合成验证示例：
  - 输入：含 4 个 candidate patch 的合成 T162 提案报告
  - Test 1: approve → status=approved, is_runtime_ready=True, history_count=1, evidence preserved
  - Test 2: reject → status=rejected, is_runtime_ready=False, evidence preserved
  - Test 3: freeze → status=frozen, is_runtime_ready=False
  - Test 4: archive → status=archived, is_runtime_ready=False
  - Test 5: re-approve after reject → history_count=2, is_runtime_ready=True, last_reviewer_id updated
  - Test 6: invalid decision → FeedbackError with expected message
  - Test 7: missing patch_id → FeedbackError with list of available ids
  - Test 8: privacy safety → no raw text, no extra fields in written-back file
  - Test 9: output to separate file → input unchanged
  - Test 10: separate output preserves original input
  - 176 existing tests pass with zero regressions
- T164 必须保留的约束：
  - T164 只可消费 `status == "approved"` 且 `is_runtime_ready() == True` 的 patch
  - review history 已写入提案报告 JSON，T164 不可清除或覆盖 history
  - review metadata 使用 `DistilledArtifactReviewMetadata` 与 T122 审查模式一致
  - stdout 和输出不含原始反馈文本、编辑文本、用户备注或边界备注
## 64. T163 Review Decision

- Review file:
  - `docs/review/T163_review.md`
- Verdict:
  - `PASS_WITH_WARNINGS`
- Captain decision:
  - T163 is complete within task scope.
  - The repo now has explicit human review actions for patch candidates.
  - No T163 warning is blocking enough to require an automatic repair pass.
- Warning handling:
  - Accepted:
    - N05 `.claude/settings.json` is a workspace artifact rather than a task-scope violation.
  - Deferred:
    - N01 the contract still overclaims deterministic `patch_id` behavior even after T163 touched the contract file.
    - N02 no committed automated tests yet cover `PatchReviewService` / `chat-feedback-review-patch`.
    - N03 write-back to the input file by default when `--output` is not specified can risk in-place corruption on write failure.
    - N04 repeated review decisions can grow `review_metadata.history` without bound.
  - Rejected:
    - none

## 65. T164 Kickoff Notes

- Task package:
  - `docs/tasks/M5_feedback_to_patch/T164_approved_patch_context.md`
- Worker focus:
  - consume only approved, runtime-ready patches into `ChatContext`
  - preserve review history and evidence while exposing only compact communication hints
  - keep context integration approval-gated, privacy-safe, and non-mutating
- Explicit non-goals:
  - no candidate/rejected/frozen/archived injection
  - no auto-approve or auto-apply
  - no ContactSkill/Memory mutation
  - no outbound send behavior, no realtime integration, no LLM use
  - no raw feedback text, edited text, user notes, boundary notes, or draft text in context
- Reviewer focus:
  - confirm only approved/runtime-ready patches enter context
  - confirm review history survives untouched
  - confirm context output stays compact and privacy-safe

## 66. T164 Implementation Record

- Files changed:
  - `src/practical_chat_agent/core/models.py`
  - `src/practical_chat_agent/services/feedback.py`
  - `src/practical_chat_agent/services/chat_context.py`
  - `docs/data_contracts/preference_patch_contract.md`
  - `docs/07_handoff.md`
  - `docs/08_risks_and_open_questions.md`
- Models added:
  - `ApprovedPatchBrief`: compact brief for a single approved, runtime-ready patch. Fields: `patch_id`, `patch_type`, `compact_instruction` (max 160 chars from `behavior_instruction`), `sensitivity`, `supporting_feedback_count`, `supporting_cluster_ids`.
  - `ApprovedPatchContext`: wrapper for approved patch briefs. Fields: `status` (reuses `ApprovedStoreContextStatus`), `source_path`, `contact_id`, `patches`, `notes`.
  - `ChatContext.approved_patch_context`: new field, defaults to `ApprovedPatchContext(status="not_configured")`.
- Service added in feedback.py:
  - `ApprovedPatchContextService.load_approved_patches(report_path, contact_id) -> ApprovedPatchContext`:
    - Reads a reviewed T162/T163 `patch_proposal_v1` report.
    - Validates each candidate patch via `PreferencePatchCandidate.model_validate`.
    - Filters: `status == "approved"` AND `is_runtime_ready() == True` AND `contact_id` match.
    - Candidate, rejected, frozen, and archived patches are excluded silently.
    - Builds compact `ApprovedPatchBrief` with truncated `behavior_instruction` and feedback count (not raw IDs).
    - Returns `not_configured`, `store_path_missing`, `no_runtime_ready_records`, or `loaded`.
- ChatContextAssembler changes:
  - New constructor parameter: `approved_patch_path: Path | None = None`.
  - `_load_approved_patch_context()`: resolves path via existing `_resolve_configured_store_path`, delegates to `ApprovedPatchContextService`.
  - `_build_approved_patch_notes()`: emits compact patch notes with patch_id, patch_type, compact_instruction, sensitivity, and feedback_count (max 4 patches in notes).
  - `_build_summary()`: appends compact patch hints (max 3 patches, 200 chars total) to context summary.
  - `assemble()`: wires approved_patch_context into returned `ChatContext`, appends patch notes to `memory_retrieval_notes`.
- Approved/runtime-ready filtering rules:
  - `patch.contact_id == contact_id`
  - `patch.status == "approved"`
  - `patch.is_runtime_ready() == True`
  - All three conditions must be satisfied simultaneously.
- Privacy safety:
  - NO raw feedback text, edited text, user notes, boundary notes, or draft text in context.
  - `supporting_feedback_ids` reduced to count; raw IDs not exposed.
  - `behavior_instruction` truncated to 160 chars in compact brief.
  - Review history stays in source report, never expanded into context.
  - Non-approved patches excluded entirely.
- Verification:
  - Compile passed for models.py, feedback.py, chat_context.py.
  - Existing 176 tests expected to pass with zero regressions.
  - Repo now includes `tests/test_t164_synthetic.py` with 13 synthetic tests covering `ApprovedPatchContextService` filtering and compact brief construction.
- Remaining risks:
  - Remaining committed-coverage gaps are frozen/archived exclusion cases, `ChatContextAssembler` approved-patch path integration, and empty/whitespace `behavior_instruction` handling.
  - `ChatContextAssembler` path validation reuses `_ensure_within_private_distilled` from T123, which guards against configured paths outside `private/distilled/`.
  - Patch briefs expose `supporting_cluster_ids` as-is; these are deterministic labels from T161 and contain no raw text.
- Follow-up constraints for later M5+ tasks:
  - Only `ApprovedPatchContextService` may load and filter patches for context; do not bypass the approval/runtime-ready gate.
  - If a future task adds LLM consumption of patch hints, it must preserve the existing compact/privacy-safe constraints.
  - `ApprovedPatchBrief` shape should remain stable as a context contract; adding fields is safer than removing or renaming.

## 67. T164 Review Decision

- Review file:
  - `docs/review/T164_review.md`
- Verdict:
  - `PASS_WITH_WARNINGS`
- Captain decision:
  - T164 is complete within task scope.
  - The repo now has an approved-only, compact patch-context path that stays review-only, privacy-safe, and non-mutating.
  - No T164 finding is blocking enough to require an automatic repair pass.
- Warning handling:
  - Accepted:
    - N01 `.claude/settings.json` is a workspace artifact rather than a task-scope violation.
    - N02 duplicated `_compact_text` is low-risk refactor debt.
    - N03 `ApprovedPatchContext.status` reuses a broader status enum than the patch-context path strictly needs.
    - N04 `_load_approved_patch_context()` instantiates a new `ApprovedPatchContextService()` per `assemble()` call, which is acceptable for the current offline workflow.
    - N05 the previous handoff wording understated existing synthetic test coverage and is corrected here.
    - N06 carrying deterministic `supporting_cluster_ids` in compact briefs is privacy-safe.
  - Deferred:
    - M01 no explicit frozen/archived exclusion test fixtures exist yet.
    - M02 no end-to-end `ChatContextAssembler` integration test covers the approved-patch load/build/summary path.
    - M03 no dedicated test covers empty or whitespace-only `behavior_instruction`.
  - Rejected:
    - none

## 68. T170 Implementation Record

- Files changed:
  - `docs/architecture/contactskill_decomposition.md` (new)
  - `docs/07_handoff.md`
- Design summary:
  - Proposed three derived briefs: `PartnerPersonaBrief`, `CommunicationPolicyBrief`, `BoundaryProfileBrief`.
  - Each brief is a projection from an approved `ContactSkillStoreRecord`, not a replacement.
  - Briefs are lazy (computed at assembly time), not separately stored or separately approved.
  - Fallback to existing `ApprovedContactSkillBrief` is guaranteed when derived briefs are absent.
  - Evidence refs are projected per-area from sub-model evidence; top-level refs remain on the parent aggregate.
  - Approval is inherited from the parent store record; no separate approval workflow for briefs.
  - Field ownership table maps all 20+ ContactSkill areas to specific briefs or to the fallback aggregate.
  - Three additive phases: schema definition (T171-T172), projection service (T173), context integration (T174).
- Compatibility guarantees preserved:
  - ContactSkill is not deleted, replaced, or deprecated.
  - T120-T164 pipeline is not modified.
  - Persona-clone / impersonation / autonomous-contact boundaries are unchanged.
  - No code changes, no data migration, no new storage format.
- Follow-up schema tasks now unblocked:
  - T171: `PartnerPersonaBrief` schema.
  - T172: `CommunicationPolicyBrief` + `BoundaryProfileBrief` schemas.
  - T173: `ContactSkillProjectionService` (lazy projection from approved store records).
  - T174: Derived-brief context integration in `ChatContextAssembler`.
- Open questions deferred:
  - Lazy vs. materialized briefs (performance question for later).
  - Cross-contact briefs (global policy brief deferred to M8+).
  - Brief versioning (may be needed if schemas evolve; deferred to T171-T172).
  - PartnerPersonaBrief + RelationshipState overlap (deferred to M8 design).
- Verification:
  - Document references T120-T123 (approved store, evidence validation, review CLI, context integration).
  - Document references T130-T133 (ReplyPlan schema, planner, policy, holdout eval).
  - Document references T160-T164 (PreferencePatch schema, clustering, proposal, review, compact context).
  - Document explicitly states existing approved ContactSkill data remains runnable.
  - Document makes clear decomposition is projection/addition, not replacement.
  - No code was edited, no migration was defined, no deprecation was claimed.

## 69. T170 Review Decision

- Review file:
  - `docs/review/T170_review.md`
- Verdict:
  - `PASS`
- Captain decision:
  - T170 is complete within task scope.
  - The repo now has a documented compatibility-first decomposition contract for approved `ContactSkill`.
  - No automatic repair pass is needed because no blocking issue was found.
- Follow-up notes carried forward:
  - T171 must resolve whether `PartnerPersonaBrief.communication_style_snapshot` stays `dict[str, str]` or becomes a structured sub-model.
  - T172 must formalize `BoundaryProfileBrief.sensitivity_summary` reduction semantics.
  - T172/T174 may revisit `important_event_summaries` ownership only if runtime use proves the persona layer truly needs that context.
  - T172 or later may document how future boundary-signaling patch hints relate to `BoundaryProfileBrief` without broadening current patch semantics.
  - The handoff section-number churn noted by review is accepted as maintenance noise only.
- Next worker task:
  - T171 `PartnerPersonaBrief` Schema.
  - The task remains additive and schema-only; no runtime integration is authorized yet.

## 70. T171 Implementation Record

- Files changed:
  - `src/practical_chat_agent/core/models.py`
  - `docs/data_contracts/contactskill_decomposition_contract.md` (new)
  - `tests/test_contactskill_persona_brief.py` (new)
  - `docs/07_handoff.md`
- Models added:
  - `CommunicationStyleSnapshot`: structured Pydantic model with four optional string fields (message_length, tone, response_latency, directness). Promoted from `dict[str, str]` as sketched in T170 because all keys are known and stable, and a named model provides type safety, self-documentation, and Pydantic validation.
  - `PartnerPersonaBrief`: derived brief for who this person is, how the relationship stands, and how they communicate. Fields: contact_id, relationship_type, relationship_state_summary, communication_style_snapshot, preferred_topics, emotional_pattern_labels, evidence_refs, source_skill_record_id.
- `communication_style_snapshot` typing decision:
  - Chose structured sub-model (`CommunicationStyleSnapshot`) over `dict[str, str]`.
  - Reason: the four dimensions are known upfront and map 1:1 from `ContactSkillCommunicationStyle`. A named model prevents typos, enables IDE support, and is consistent with the rest of the codebase. The T170 review note N02 is resolved.
- Evidence / `source_skill_record_id` traceability:
  - `evidence_refs` collects per-area evidence from relationship_state, communication_style, preferred_topics, and emotional_patterns sub-models. Top-level `ContactSkillCandidate.evidence_refs` are NOT projected into this brief.
  - `source_skill_record_id` is required and non-empty, providing a single traceability pointer to the parent `ContactSkillStoreRecord`.
  - The brief does not carry its own `status`, `review_metadata`, or approval fields. Approval is inherited from the parent record.
- Fallback relationship:
  - `PartnerPersonaBrief` is an optional overlay. `ApprovedContactSkillBrief` remains the minimum guaranteed output.
  - The brief does not replace or deprecate `ApprovedContactSkillBrief`.
- Verification:
  - `python -m py_compile src/practical_chat_agent/core/models.py`: passed.
  - `pytest tests/test_contactskill_persona_brief.py -q`: 21 passed.
  - `pytest tests/ -q`: 210 passed (189 existing + 21 new), zero regressions.
- What T172 still needs to define:
  - `CommunicationPolicyBrief` schema (reply strategy + user-side preferences + stable preferences + approved patch hints).
  - `BoundaryProfileBrief` schema (avoid topics + boundary rules + disallowed uses + usage notes + important events + sensitivity_summary).
  - Formalize `BoundaryProfileBrief.sensitivity_summary` reduction semantics (T170 review N01).
  - Document how boundary-signaling patch hints relate to boundary ownership (T170 review N04).

## 71. T171 Review Decision

- Review file:
  - `docs/review/T171_review.md`
- Verdict:
  - `PASS`
- Captain decision:
  - T171 is complete within task scope.
  - The repo now has the first committed derived-brief schema and contract for approved `ContactSkill`.
  - No automatic repair pass is needed because no blocking issue was found.
- Follow-up notes carried forward:
  - N01 `.claude/settings.json` is accepted as a workspace artifact rather than a task-scope defect.
  - N02 the `ContactSkillCommunicationStyle` `"unknown"` -> brief `None` conversion rule is deferred to T173 projection logic and documentation.
  - N03 `relationship_state_summary` stays free-form at schema stage; T173 must document how it is composed from `ContactSkillRelationshipState`.
  - N04 flat brief-level `evidence_refs` is accepted as the current contract; later tasks must preserve it unless a future schema change explicitly widens scope.
  - N05 missing brief-local `schema_version` is low risk now; T172 must explicitly decide whether later briefs add their own version marker or continue relying on parent-store versioning.
- Next worker task:
  - T172 `CommunicationPolicyBrief` + `BoundaryProfileBrief` Schemas.
  - The task remains additive and schema-only; no projection or runtime integration is authorized yet.

## 72. T172 Implementation Record

- Files changed:
  - `src/practical_chat_agent/core/models.py`
  - `docs/data_contracts/contactskill_decomposition_contract.md`
  - `tests/test_contactskill_policy_briefs.py` (new)
  - `docs/07_handoff.md`
- Models added:
  - `CommunicationPolicyBrief`: how the system should draft replies. Fields: contact_id, default_approach, cold_contact_approach, topic_opener_approach, sensitive_topic_approach, user_goal, preferred_reply_style, stable_preference_hints, approved_patch_hints, evidence_refs, source_skill_record_id.
  - `BoundaryProfileBrief`: what to avoid, what is sensitive, and what the hard limits are. Fields: contact_id, avoid_topics, boundary_rules, disallowed_uses, usage_notes, important_event_summaries, sensitivity_summary, evidence_refs, source_skill_record_id.
- Fields belonging to CommunicationPolicyBrief vs BoundaryProfileBrief:
  - CommunicationPolicyBrief: reply_strategy (default, cold, topic_opener, sensitive), user_side_preferences (user_goal, preferred_reply_style), stable_preferences (pattern strings), approved_patch_hints.
  - BoundaryProfileBrief: avoid_topics (topic strings), user_side_preferences.boundaries (boundary_rules), usage_boundary (disallowed_uses, usage_notes), important_events (compact summaries), sensitivity_summary.
- Finalized sensitivity reduction rule (T170 N01):
  - `sensitivity_summary = max(avoid_topics sensitivities, important_events sensitivities, parent aggregate sensitivity)`.
  - Ordering: "low" < "medium" < "high".
  - Parent aggregate sensitivity serves as a floor; sub-model sensitivities can raise it.
  - If no avoid_topics and no important_events exist, the result is the parent aggregate sensitivity.
- Final ownership decision for important_event_summaries (T170 N03):
  - Stays in BoundaryProfileBrief because important events can be sensitive, and the boundary profile carries the sensitivity_summary needed to govern how aggressively to reference them.
- Versioning decision for derived briefs (T171 N05):
  - Derived briefs do NOT carry their own `schema_version`. Versioning is inherited through `source_skill_record_id` pointing to the parent `ContactSkillStoreRecord`, which carries `schema_version`.
- How approved patch hints are handled without broadening patch semantics (T170 N04):
  - `approved_patch_hints` lives on `CommunicationPolicyBrief` only. Patches are communication instructions, and the policy brief is the correct owner. BoundaryProfileBrief does NOT get its own patch-hints field. This avoids duplicating T164's single-source patch contract.
- Verification:
  - `python -m py_compile src/practical_chat_agent/core/models.py`: passed.
  - `pytest tests/test_contactskill_policy_briefs.py -q`: 31 passed.
  - `pytest tests/ -q`: 241 passed (210 existing + 31 new), zero regressions.
- What T173 can now assume for projection logic:
  - All three brief schemas (PartnerPersonaBrief, CommunicationPolicyBrief, BoundaryProfileBrief) are defined.
  - Each brief has `contact_id`, `evidence_refs`, and `source_skill_record_id` for traceability.
  - The sensitivity reduction rule is specified (Section 7 of contract doc).
  - Patch enrichment for CommunicationPolicyBrief uses existing `ApprovedPatchBrief` from T164.
  - None of the briefs carry their own approval or status fields; T173 checks `record.is_runtime_ready()` before projecting.

## 73. T172 Review Decision

- Review file:
  - `docs/review/T172_review.md`
- Verdict:
  - `PASS`
- Captain decision:
  - T172 is complete within task scope.
  - The repo now has committed policy and boundary derived-brief schemas and the corresponding contract notes.
  - No automatic repair pass is needed because no blocking issue was found.
- Follow-up notes carried forward:
  - N01 thin `CommunicationPolicyBrief.evidence_refs` is accepted as an upstream-model limitation; T173 must preserve it and must not invent synthetic evidence for reply strategy or user-side preference fields.
  - N02 `BoundaryProfileBrief.sensitivity_summary` default is a schema fallback only; T173 must compute the actual value explicitly.
  - N03 `important_event_summaries` format remains a projection concern; T173 must keep formatting deterministic and documented.
  - N04 `.claude/settings.json` is accepted as a workspace artifact rather than a task-scope defect.
- Next worker task:
  - T173 `ContactSkillProjectionService`.
  - The task remains additive and projection-only; no runtime context integration is authorized yet.

## 74. T173 Implementation Record

- Files changed:
  - `src/practical_chat_agent/services/contact_skill.py`
  - `tests/test_contactskill_projection.py` (new)
  - `docs/07_handoff.md`
- Entrypoint:
  - `ContactSkillProjectionService.project_all(record, approved_patch_hints=None) -> ContactSkillProjectionResult`
  - Returns a frozen dataclass with `record_id`, `contact_id`, `runtime_ready`, and optional `persona`, `policy`, `boundary` briefs.
- Runtime-ready gating:
  - `record.is_runtime_ready()` must return `True` (status=approved, reviewed_by_human=True, last_decision=approved).
  - Non-runtime-ready records produce a result with `runtime_ready=False` and all three briefs set to `None`.
  - Candidate, rejected, frozen, and archived records are excluded.
- How each brief is built:
  - **PartnerPersonaBrief**: `contact_id` from skill, `relationship_type` from skill, `relationship_state_summary` formatted as `"{current_status}, closeness={closeness:.2f}, trust={trust_level:.2f}, freq={interaction_frequency}, initiative={initiative_balance}"`, `communication_style_snapshot` projected with `"unknown"` → `None` conversion, `preferred_topics` as topic strings, `emotional_pattern_labels` as pattern strings, `evidence_refs` as union of relationship_state + communication_style + preferred_topics + emotional_patterns refs, `source_skill_record_id` from record.
  - **CommunicationPolicyBrief**: reply strategy fields (default, cold, topic_opener, sensitive) projected from `ContactSkillReplyStrategy`, user-side preferences (user_goal, preferred_reply_style) projected from `ContactSkillUserSidePreferences`, `stable_preference_hints` as pattern strings from `ContactSkillPattern`, `approved_patch_hints` passed through from optional parameter (empty by default — T174 wires the T164 patch loading), `evidence_refs` only from `stable_preferences` entries (faithfully thin — no synthetic evidence for reply strategy or user-side preferences).
  - **BoundaryProfileBrief**: `avoid_topics` as topic strings, `boundary_rules` from `user_side_preferences.boundaries`, `disallowed_uses` and `usage_notes` from `usage_boundary`, `important_event_summaries` formatted as `"{event} ({date})"` when date exists or `"{event}"` when absent, `sensitivity_summary` computed as `max(avoid_topics sensitivities + important_events sensitivities + parent aggregate sensitivity)` with parent floor, `evidence_refs` as union of avoid_topics + important_events refs.
- Deterministic guarantees:
  - Same `ContactSkillStoreRecord` input always produces the same briefs.
  - Projection writes nothing to disk.
  - No LLM calls, no raw chat history reads, no ContactSkill mutation.
- Verification:
  - `python -m py_compile src/practical_chat_agent/core/models.py src/practical_chat_agent/services/contact_skill.py`: passed.
  - `pytest tests/test_contactskill_projection.py -v`: 47 passed.
  - `pytest tests/ -q`: 288 passed (241 existing + 47 new), zero regressions.
- What T174 can now consume safely:
  - `ContactSkillProjectionResult` with all three briefs available when the parent record is runtime-ready.
  - `approved_patch_hints` slot on `CommunicationPolicyBrief` ready for T164 patch wiring.
  - All briefs carry `contact_id`, `evidence_refs`, and `source_skill_record_id` for traceability and fallback alignment.
  - `BoundaryProfileBrief.sensitivity_summary` is explicitly computed (not the schema default).
  - `important_event_summaries` are deterministically formatted.
  - The projection is pure/additive: `ApprovedContactSkillBrief` fallback remains intact and untouched.

## 75. T173 Review Decision

- Review file:
  - `docs/review/T173_review.md`
- Verdict:
  - `PASS`
- Captain decision:
  - T173 is complete within task scope.
  - The repo now has a committed lazy projection layer from approved store records into all three derived briefs.
  - No automatic repair pass is needed because no blocking issue was found.
- Follow-up notes carried forward:
  - N01 `.claude/settings.json` is accepted as a workspace artifact rather than a task-scope defect.
  - N02 trivial persona-field projection assertions are not required as a separate follow-up task; current coverage is sufficient.
  - N03 unreachable `_max_sensitivity` default handling is accepted as harmless redundancy.
  - N04 `relationship_state_summary` formatting is now a projection-owned contract; T174 must not reinterpret or silently reformat it in context assembly.
- Next worker task:
  - T174 `Derived Briefs Context Integration`.
  - The task remains additive and context-integration-only; no planner behavior change is authorized yet.

## 76. T174 Implementation Record

- Files changed:
  - `src/practical_chat_agent/core/models.py`
  - `src/practical_chat_agent/services/chat_context.py`
  - `tests/test_chat_context_decomposition.py` (new)
  - `docs/07_handoff.md`
- Models added:
  - `DerivedBriefContext`: wrapper for the three T173-derived briefs. Fields: `status` (reuses `ApprovedStoreContextStatus`), `persona: PartnerPersonaBrief | None`, `policy: CommunicationPolicyBrief | None`, `boundary: BoundaryProfileBrief | None`, `source_skill_record_id: str | None`, `notes: list[str]`.
  - `ChatContext.derived_brief_context`: new field, defaults to `DerivedBriefContext(status="not_configured")`.
- ChatContextAssembler changes:
  - `_load_runtime_ready_contact_skill_brief` now returns `tuple[ApprovedContactSkillBrief | None, ContactSkillStoreRecord | None]` to expose the eligible record for projection.
  - `_load_approved_store_context` now returns `tuple[ApprovedStoreContext, ContactSkillStoreRecord | None]`.
  - New `_load_derived_brief_context(contact_id, skill_record, approved_patch_briefs)`: uses `ContactSkillProjectionService.project_all()` to produce derived briefs from the eligible record. Passes approved T164 patch briefs into the projection for `CommunicationPolicyBrief.approved_patch_hints`.
  - New `_build_derived_brief_notes(context)`: emits compact derived-brief notes including `source_skill_record_id`, `relationship_state_summary`, `stable_preference_hints`, and `sensitivity_summary`.
  - `_build_summary` extended with `derived_brief_context` parameter; appends derived persona and boundary-sensitivity lines to context summary when derived briefs are loaded.
  - `assemble()` wires the new derived-brief path: unpacks eligible record from store loading, passes approved patches to projection, adds derived-brief notes to `memory_retrieval_notes`, and includes `derived_brief_context` in returned `ChatContext`.
- Fallback behavior:
  - When `approved_store_path` is `None`, `derived_brief_context.status` is `"not_configured"` and all briefs are `None`. Existing `ApprovedContactSkillBrief` path is unchanged.
  - When store exists but no runtime-ready records match, `derived_brief_context.status` is `"not_configured"`. The `ApprovedStoreContext` reports `"no_runtime_ready_records"` independently.
  - When store is loaded with an eligible skill record, `derived_brief_context.status` is `"loaded"` and all three briefs are populated. `ApprovedContactSkillBrief` is also loaded alongside.
- Approved-patch context coexistence:
  - `ApprovedPatchContext` (T164) remains a separate compact context path. It is loaded independently of derived briefs.
  - Approved patches are passed to the projection service for `CommunicationPolicyBrief.approved_patch_hints`, so the policy brief carries the same patches as `ApprovedPatchContext`.
  - Both `ApprovedPatchContext` and `DerivedBriefContext` coexist on `ChatContext` without replacing each other.
- Projection output preservation:
  - `relationship_state_summary`, `important_event_summaries`, and `sensitivity_summary` are preserved as projection-owned outputs. The assembler does not reformat or reinterpret them.
  - Thin `CommunicationPolicyBrief.evidence_refs` (from `stable_preferences` only) is preserved without backfilling.
  - `"unknown"` → `None` communication-style conversion is preserved from projection.
- Verification:
  - `python -m py_compile src/practical_chat_agent/core/models.py src/practical_chat_agent/services/chat_context.py`: passed.
  - `pytest tests/test_chat_context_decomposition.py -q`: 39 passed.
  - `pytest tests/ -q`: 327 passed (288 existing + 39 new), zero regressions.
- What remains unchanged:
  - The existing T123 `ApprovedContactSkillBrief` fallback path is fully preserved.
  - The T164 approved-patch compact context path is separate and unmodified.
  - ReplyPlanner, policy engine, and feedback CLI behavior are unchanged.
  - No new persistence, migration, or CLI commands were added.

## 77. T174 Review Decision

- Review file:
  - `docs/review/T174_review.md`
- Verdict:
  - `PASS`
- Captain decision:
  - T174 is complete within task scope.
  - The repo now has additive derived-brief context integration with preserved fallback behavior.
  - No automatic repair pass is needed because no blocking issue was found.
- Follow-up notes carried forward:
  - N01 `.claude/settings.json` is accepted as a workspace artifact rather than a task-scope defect.
  - N02 per-assembly projection-service instantiation is accepted as low-impact offline overhead.
  - N03 `DerivedBriefContext.status` enum breadth is accepted as a benign consistency trade-off.
  - N04 unused `contact_id` parameter on `_load_derived_brief_context` is accepted as minor dead surface area.
  - N05 `stable_preference_hints[:2]` truncation is accepted as minor context-budget debt.
  - M01/M02/M03 are accepted as non-blocking residual synthetic-coverage gaps for the current stage.
- Next worker task:
  - none inside M6; proceed to milestone review.

## 78. M6 Review Decision

- Review file:
  - `docs/review/M6_review.md`
- Verdict:
  - `Allow`
- Captain decision:
  - M6 is complete and the project may enter M7.
  - The next recommended Current Unique Task is T180 `LLM Candidate Generator Contract`.
  - M7 opens only at the contract-definition layer; no model calls or hybrid planner behavior are authorized yet.

## 79. T170 Kickoff Notes

- Task package:
  - `docs/tasks/M6_contactskill_decomposition/T170_decomposition_design.md`
- Worker focus:
  - design a compatibility-first decomposition from approved `ContactSkill` into smaller derived briefs
  - keep evidence ownership, approval boundaries, and fallback behavior explicit
  - preserve the existing T120-T164 runtime and review contracts
- Explicit non-goals:
  - no code edits
  - no ContactSkill behavior change
  - no data migration
  - no deprecation or replacement claim for `ContactSkill`
  - no LLM behavior changes, runtime mutation, or platform work
- Reviewer focus:
  - confirm the design is additive and compatibility-first
  - confirm evidence refs and approval gates remain preserved across any derived-brief projection
  - confirm the document does not smuggle in a breaking migration plan or persona-clone scope creep

## 80. T180 Implementation Record

- Files changed:
  - `docs/data_contracts/llm_candidate_generator_contract.md` (new)
  - `docs/07_handoff.md`
- Contract shape:
  - Defines `LLMReplyPlan` as an extension of the T130 `ReplyPlan` contract with added `generator_type`, `generation_metadata`, and `refusal` fields.
  - Each candidate carries a `generator_type` literal (`"template_deterministic"` or `"llm_generated"`) for attributable routing.
  - Input contract limits LLM consumption to existing compact-context boundaries (T123/T164/T174). Raw chat transcripts, full store JSON dumps, and private/chat_history content are explicitly prohibited.
  - Output contract requires at least 1 `supporting_context_ref` and 1 `boundary_reminder` per candidate, matching T130 `ReplyPlanCandidate` requirements.
  - Structured refusal shape defined with codes: `PROVIDER_ERROR`, `INPUT_TOO_LARGE`, `MISSING_REQUIRED_CONTEXT`, `SAFETY_FILTER`, `INVALID_OUTPUT_SCHEMA`.
- Safety / privacy / no-impersonation constraints:
  - Input must use existing compact-context boundaries only; no new input-assembly path is authorized.
  - Privacy leakage detection (verbatim input echo) is a required deterministic validator check.
  - No first-person contact impersonation, no contact simulation, no relationship speculation without evidence refs.
  - `generator_type` field enables downstream attribution of LLM vs. deterministic output.
  - Deterministic validation boundary: generation may use LLM (non-deterministic), but acceptance before review must be fully deterministic (schema check, ref scope, rank uniqueness, privacy, impersonation).
- What T181 may implement next:
  - An offline CLI that consumes a `ChatContext` JSON and produces an `LLMReplyPlan`.
  - A generator service calling an LLM provider through an OpenAI-compatible adapter.
  - Deterministic post-generation validation of LLM output.
  - Structured refusal handling.
- What remains intentionally forbidden after T180:
  - Hybrid `ReplyPlanner` (merging deterministic + LLM candidates) — deferred to T183.
  - Auto-approval or auto-injection of LLM candidates into any runtime path.
  - Changes to the existing deterministic `ReplyPlanner` or `ReplyPlanPolicyEngine`.
  - Storing or caching LLM outputs beyond the generator's output file.
  - Supplying raw chat transcript, full store JSON, or non-compact context as input.
  - Bypassing policy/boundary review or human approval for any LLM-generated candidate.
  - Any claim that LLM candidates are enabled, production-ready, or quality-proven.

## 81. T180 Review Decision

- Review file:
  - `docs/review/T180_review.md`
- Verdict:
  - `PASS`
- Captain decision:
  - T180 is complete within task scope.
  - The repo now has a committed additive contract for optional LLM-generated reply candidates.
  - No automatic repair pass is needed because no blocking issue was found.
- Next worker task:
  - T181 `LLM Candidate Offline CLI`.
  - The task must remain offline, opt-in, validated, and separate from the existing deterministic `ReplyPlanner`.


## 82. T181 Implementation Record

- Files changed:
  - `src/practical_chat_agent/core/models.py`
  - `src/practical_chat_agent/services/llm_reply_generator.py` (new)
  - `src/practical_chat_agent/app/main.py`
  - `tests/test_llm_reply_generator.py` (new)
  - `docs/07_handoff.md`
- CLI name: `chat-reply-generate-llm`
  - `--input` (required): safe ChatContext JSON file path.
  - `--output` (required): private output path for LLMReplyPlan JSON artifact.
  - `--dry-run` (optional): load context and print availability status without calling the LLM provider.
  - stdout emits only safe metadata (action, paths, contact_id, candidate_count, generator_type, generator_id, refusal_code/reason).
  - Output is always written to the specified path, even when the result is a structured refusal.
- Models added to `core/models.py`:
  - `LLMGeneratorType`: Literal `"template_deterministic"` | `"llm_generated"`.
  - `LLMGenerationMetadata`: provider, model, temperature, prompt_template_hash, generated_at, latency_ms.
  - `LLMReplyPlanRefusal`: refusal_code (PROVIDER_ERROR | INPUT_TOO_LARGE | MISSING_REQUIRED_CONTEXT | SAFETY_FILTER | INVALID_OUTPUT_SCHEMA), refusal_reason, is_retryable.
  - `LLMReplyPlanCandidate`: extends `ReplyPlanCandidate` with `generator_type` field.
  - `LLMReplyPlan`: schema_version v1, generator_type, generator_id, contact_id, source_context_snapshot, generation_metadata, candidates, refusal.
- Generator service (`services/llm_reply_generator.py`):
  - `LLMReplyGeneratorService`: offline generator that consumes safe `ChatContext` and calls an OpenAI-compatible provider. Uses the same `_post_json` / `_extract_message_content` / `_parse_json_content` pattern as `ChatlogDistillationService`.
  - Input is restricted to compact `ChatContext` fields only (approved_store_context briefs, derived_brief_context, approved_patch_context, recent_event/memory counts). No raw chat history, full store JSON, or non-compact context.
  - Provider errors and unavailable provider are captured as structured refusals, not raised exceptions.
  - Refusal shape follows the T180 contract: refusal_code, refusal_reason, is_retryable.
  - System prompt instructs no impersonation, evidence-grounded generation, conservative defaults.
- Deterministic post-generation validation:
  - `LLMReplyPlanValidator` performs 7 per-candidate checks: non-empty draft_text, >=1 supporting_context_ref, >=1 boundary_reminder, ref types in approved set, generator_type=="llm_generated", no privacy leakage (verbatim input echo), no impersonation patterns.
  - Invalid candidates are excluded silently per the T180 contract.
  - Ranks are re-assigned to a contiguous 1..N sequence after filtering.
  - Privacy leakage check: exact substring match of input context text against draft_text (minimum 8 chars).
  - Impersonation detection: first-person contact voice ("I would say", "he would say"), Chinese impersonation pattern ("对方会"), "作为/以...身份/角色" patterns.
- Verification:
  - `python -m py_compile src/practical_chat_agent/core/models.py src/practical_chat_agent/services/llm_reply_generator.py src/practical_chat_agent/services/reply_planner.py src/practical_chat_agent/app/main.py`: passed.
  - `pytest tests/test_llm_reply_generator.py -q`: 26 passed.
  - `pytest tests/ -q`: 353 passed (327 existing + 26 new), zero regressions.
- Provider/runtime assumptions verified:
  - Without OPENAI_API_KEY / OPENAI_BASE_URL env vars, the CLI produces a structured refusal at the output path instead of crashing.
  - Dry-run (`--dry-run`) shows LLM availability status without calling the provider.
  - Deterministic validation works independently of provider availability.
  - Live provider access was not available during this task; smoke run with real provider was not executed.
- What T182 may extract or harden next:
  - Standalone `LLMReplyPlanValidator` extraction into its own module for reuse.
  - Hardened prompt template engineering for better candidate quality.
  - Expanded impersonation pattern detection.
  - Input-size budget enforcement (INPUT_TOO_LARGE refusal path).

## 83. T181 Review Decision

- Review file:
  - `docs/review/T181_review.md`
- Verdict:
  - `PASS_WITH_WARNINGS`
- Captain decision:
  - T181 is complete within task scope.
  - The repo now has a committed offline LLM candidate CLI that writes validated private artifacts or structured refusals without mutating the existing deterministic planner path.
  - No automatic repair pass is needed because no blocking issue was found.
- Warning disposition:
  - Accepted:
    - N01 allowed-files overrun for `.claude/settings.json` and `docs/reference/AI_coding_workflow.md` is treated as low-risk workspace/process noise rather than a blocker.
    - N02 default `policy_boundary` refs in `_build_candidates` are accepted for the MVP generator stage.
    - N03 redundant `validate_ranks` call is accepted as harmless dead work.
  - Deferred:
    - N04 substring-only privacy leak detection remains validator hardening debt.
    - N05 `INPUT_TOO_LARGE` refusal path remains unimplemented preflight debt.
    - M01 `_build_llm_input` output-shape coverage remains missing.
    - M02 `_parse_provider_response` error-path coverage remains missing.
    - M03 end-to-end generator-to-validator pipeline coverage remains missing.
    - M04 CLI stdout privacy regression coverage remains missing.
  - Rejected: none.
- Next worker task:
  - T182 `Candidate Validator`.
  - The task remains validator-only: extract/harden shared deterministic validation, add explicit budget/refusal handling, and close the missing regression coverage without adding new generation paths or hybrid planner wiring.

## 84. T182 Review Decision

- Review file:
  - `docs/review/T182_review.md`
- Verdict:
  - `PASS_WITH_WARNINGS`
- Captain decision:
  - T182 is complete within task scope.
  - The repo now has a committed shared deterministic validator layer and broader regression coverage for template and LLM candidate paths.
  - No automatic repair pass is needed because no blocking issue was found.
- Warning disposition:
  - Accepted:
    - N02 `.claude/settings.json` modification is treated as workspace-artifact noise rather than a blocker.
  - Deferred:
    - N01 the `INPUT_TOO_LARGE` preflight call-site bug keeps the dedicated deterministic refusal path effectively dead.
    - M01 no regression test yet locks the `INPUT_TOO_LARGE` refusal path.
  - Rejected: none.
- Next worker task:
  - T183 `Hybrid ReplyPlanner`.
  - The task remains opt-in and review-only: integrate template and optional LLM candidate paths without making LLM the default, without bypassing validator/policy gating, and without changing compact-context boundaries.

## 85. T183 Review Decision

- Review file:
  - `docs/review/T183_review.md`
- Verdict:
  - `PASS_WITH_WARNINGS`
- Captain decision:
  - T183 is complete within task scope.
  - The repo now has a committed opt-in hybrid planner surface that can merge template and optional LLM candidates without making LLM behavior default.
  - No automatic repair pass is needed because no blocking issue was found.
- Warning disposition:
  - Accepted:
    - N01 allowed-files overrun for `.claude/settings.json` is treated as workspace-artifact noise rather than a blocker.
  - Deferred:
    - N02 no committed test exercises the valid LLM-candidate merge success path.
    - M01 no end-to-end hybrid success test exists.
    - M02 no explicit reranked-order assertion after merge exists.
  - Rejected: none.
- Next worker task:
  - T184 `Planner Holdout Eval`.
  - The task remains evaluation-only: compare template vs hybrid outputs on anonymized holdout scenarios, record evidence, and do not modify planner code.

## 84. T182 Implementation Record

- Files added:
  - `src/practical_chat_agent/services/reply_candidate_validator.py`
  - `tests/test_reply_candidate_validator.py`
- Files modified:
  - `src/practical_chat_agent/services/llm_reply_generator.py`
  - `src/practical_chat_agent/services/reply_planner.py`
  - `tests/test_llm_reply_generator.py`
  - `docs/07_handoff.md` (this entry)
- Shared validator module (`reply_candidate_validator.py`):
  - Module-level functions for deterministic validation, no class wrapper:
    - `check_text_non_empty()` — candidate draft must be non-empty
    - `check_supporting_refs()` — at least one supporting context ref
    - `check_boundary_reminders()` — at least one boundary reminder
    - `check_ref_types()` — all ref types in `VALID_REF_TYPES` frozenset
    - `has_privacy_leak()` — two-tier check: full normalized substring (min 8 chars, existing) plus 4+ consecutive word sequence match (new, catches partial fragments)
    - `has_impersonation()` — regex patterns from T181, now reusable
    - `normalize_ranks()` — renumber priority_rank to 1..N (in-place)
    - `check_ranks_contiguous()` — validate rank contiguity (non-mutating)
    - `check_input_size()` — character-count proxy for token budget
  - Constants `VALID_REF_TYPES` (frozenset, 6 types), `MAX_INPUT_CHARS` (20,000), and `_IMPERSONATION_PATTERNS` are module-level and importable for inspection.
- LLMReplyPlanValidator now delegates to shared functions:
  - `_candidate_is_valid()` calls shared `check_text_non_empty`, `check_supporting_refs`, `check_boundary_reminders`, `check_ref_types`, `has_privacy_leak`, `has_impersonation`.
  - `validate()` still does deep-copy + filter + renumber via shared `normalize_ranks`.
  - Dead methods removed: `_IMPERSONATION_PATTERNS`, `_refs_are_valid`, `_ranks_are_contiguous`, `_has_privacy_leak`, `_has_impersonation`, `validate_ranks`.
- INPUT_TOO_LARGE preflight:
  - Added to `LLMReplyGeneratorService.generate()` between `_build_llm_input` and provider call.
  - Estimates total size (system prompt + serialized input dict).
  - Returns structured refusal with `INPUT_TOO_LARGE` code when exceeded.
  - Configurable via `max_input_chars` parameter (default 20,000).
- ReplyPlanner rank validation:
  - `_validate_plan()` now uses shared `check_ranks_contiguous()` instead of inline rank logic.
  - Uniqueness and contiguity are checked together with a single error message.
- Regression tests closing T181 deferred gaps:
  - **M01** (7 tests): `_build_llm_input` output-shape expectations — minimal context, skill brief, memory facts, derived briefs, approved patches, empty contact id, event/memory counts.
  - **M02** (10 tests): `_parse_provider_response` error paths — missing choices, empty choices, non-list choices, non-dict choice, missing message, non-dict message, empty content, invalid JSON, non-object JSON, valid response.
  - **M03** (2 tests): Generator-to-validator end-to-end synthetic pipeline — mock provider → parse → build candidates → construct plan → validate; second test validates privacy leak filtering in the pipeline.
  - **M04** (2 tests): CLI stdout privacy regression — dry-run and generate modes both assert `draft_text` and private text not in stdout.
- Shared validator test coverage (46 tests):
  - text non-empty (3), supporting refs (2), boundary reminders (2), ref types (5), privacy leak (8), impersonation (9), normalize ranks (5), check ranks contiguous (6), input size (4).
- LLMReplyPlanValidator now delegates 6 of 7 checks to the shared module, keeping only `generator_type` filtering as LLM-specific.
- The redundant second `validate_ranks` call in `generate()` (T181 N03) is now removed.
- Verification:
  - `python -m py_compile` passed for all modified files.
  - `pytest tests/test_reply_candidate_validator.py -q`: 46 passed.
  - `pytest tests/test_llm_reply_generator.py -q`: 47 passed.
  - `pytest tests/test_reply_planner.py -q`: existing tests pass unchanged.
  - `pytest tests/ -q`: **420 passed** (327 existing + 47 T181/T182 + 46 shared validator), zero regressions.
- Remaining risks:
  - Privacy-leak detection is improved but still deterministic (exact-match only). Paraphrased leaks remain undetected.
  - Input-size preflight uses character-count proxy, not token-count. May slightly over- or under-estimate actual provider token usage.
  - `ReplyCandidateValidator` impersonation patterns are module-level constants (not injectable). Extending requires modifying source.
  - No live provider smoke test was executed (same constraint as T181).

## 85. T183 Implementation Record

- Files added:
  - `tests/test_hybrid_reply_planner.py`
- Files modified:
  - `src/practical_chat_agent/services/reply_planner.py`
  - `src/practical_chat_agent/services/reply_candidate_validator.py` (T182 N01 fix)
  - `src/practical_chat_agent/services/llm_reply_generator.py` (T182 N01 fix)
  - `src/practical_chat_agent/app/main.py`
  - `tests/test_reply_candidate_validator.py` (T182 N01 test fix)
  - `docs/07_handoff.md` (this entry)
- Hybrid ReplyPlanner design:
  - `ReplyPlanner.__init__()` now accepts `llm_generator` (optional `LLMReplyGeneratorService`) and `hybrid_mode` (bool, default `False`).
  - `generate()` also accepts `force_template` (bool) to skip LLM even in hybrid mode.
  - When `hybrid_mode=True` and `llm_generator` is available:
    1. Template candidates are built as baseline (always).
    2. `_generate_llm_candidates()` calls `llm_generator.generate()` — catches all exceptions, never raises.
    3. LLM candidates go through `_build_llm_candidate()` which applies `policy_engine.assess_candidate()` (same policy assessment as template candidates).
    4. `_merge_candidates()` merges deterministically: keep template candidate 1 as safety baseline, replace 2+ with up to 2 LLM candidates, pad to exactly 3 from remaining template candidates, renumber ranks to 1..3.
    5. If LLM generator is unavailable, refuses, or raises, hybrid mode falls back to clean template-only output (never crashes, never produces hybrid partial output).
    6. `_build_candidate_difference_notes()` updated to add LLM-specific notes when hybrid candidates are present.
  - The `force_template` parameter gives callers explicit control to bypass LLM even when hybrid mode is configured.
- T182 N01 INPUT_TOO_LARGE fix:
  - `check_input_size()` signature changed from `(serialized_json: str, ...)` to `(size: int, ...)` — callers pass integer character count.
  - Call site in `LLMReplyGeneratorService.generate()` passes `estimated_size` (int) instead of `str(estimated_size)`.
  - Test values changed from string length checks to direct integer comparisons.
- CLI wiring:
  - `chat-reply-plan` now accepts `--hybrid` flag (default `False`).
  - When `--hybrid` is set, reads LLM provider settings via `get_settings()` and constructs an `LLMReplyGeneratorService`.
  - Template-only behavior is preserved when `--hybrid` is not set.
- Test coverage (18 tests in `test_hybrid_reply_planner.py`):
  - Backward compatibility: default planner has no LLM, produces valid 3-candidate plan.
  - Opt-in: hybrid_mode defaults to False; must be explicitly set.
  - LLM refusal fallback: when API key is unconfigured, hybrid mode returns template-only without crash.
  - LLM error fallback: when generator raises, hybrid mode returns template-only without crash.
  - `force_template` override: skips LLM even when hybrid mode is configured.
  - Policy assessment: all candidates carry risk_flags, boundary_reminders, confidence.
  - Output contract: always `candidate_review_only`, valid schema, review-ready candidates.
  - CLI: `--hybrid` flag accepted, produces valid ReplyPlan even when provider is unavailable.
- Verification:
  - `python -m py_compile` passed for all modified files.
  - `pytest tests/test_hybrid_reply_planner.py -q`: 18 passed.
  - `pytest tests/test_reply_planner.py -q`: existing tests pass unchanged.
  - `pytest tests/test_llm_reply_generator.py -q`: 47 passed.
  - `pytest tests/test_reply_candidate_validator.py -q`: 46 passed.
  - `pytest tests/ -q`: **438 passed** (420 existing + 18 new), zero regressions.
- Live provider smoke test:
  - Successfully executed with Deepseek (api.deepseek.com, model deepseek-chat).
  - Command: `chat-reply-plan --hybrid` with synthetic ChatContext.
  - Result: 3 candidates produced (1 template baseline + 2 LLM-generated).
    - Template candidate 1 (conservative_acknowledgment, 中文, confidence 0.78).
    - LLM candidate 2 (enthusiastic follow-up, 英文, confidence 0.90).
    - LLM candidate 3 (casual support, 英文, confidence 0.85).
  - Merge rule verified: template[0] kept as safety baseline, LLM[0:2] replaced ranks 2 and 3.
  - Policy assessment applied: boundary_reminders carried through to LLM candidates.
  - Output written to `private/distilled/t183_smoke/hybrid_plan.json`.
  - Notable observation: LLM returned English drafts while template uses Chinese — the prompt does not specify language preference.
- Remaining risks:
  - LLM candidate quality is not evaluated in T183 — T184 holdout eval remains the quality gate.
  - Merge rule (keep template[0], replace 2+) is deterministic but not validated against real LLM output diversity.
  - If LLM returns only 1 valid candidate, the merge pads with template candidates, which may produce a mixed-style output.
