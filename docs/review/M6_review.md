# M6 Review: ContactSkill-Compatible Decomposition

Reviewer: Codex Captain
Date: 2026-05-23
Scope: T170-T174, compatibility-first ContactSkill decomposition design / schema / projection / context integration
Verdict: `Allow`

## 1. 当前功能是否真的完成

是，就 M6 的既定范围而言已经完成。

M6 需要证明的不是“换掉 ContactSkill”，而是“在不破坏既有 runtime contract 的前提下，把 approved ContactSkill 分解成更窄的 derived briefs”。这条链路现在已经完整存在：

- T170: 完成 compatibility-first decomposition design
- T171: 完成 `PartnerPersonaBrief` schema
- T172: 完成 `CommunicationPolicyBrief` + `BoundaryProfileBrief` schemas
- T173: 完成从 approved/runtime-ready `ContactSkillStoreRecord` 到三类 brief 的 lazy projection
- T174: 完成 `DerivedBriefContext` 接入 `ChatContext`，同时保留既有 `ApprovedContactSkillBrief` fallback 与 T164 approved-patch compact-context path

当前功能完成的是“design -> schema -> projection -> context integration”的 M6 结构目标，不是“LLM-assisted planner”目标，也不是“替换现有 planner”的目标。

## 2. 是否能从干净环境运行

可以，足以通过本里程碑 gate。

M6 这一层已经有完全 committed 的 synthetic tests，不依赖 private chat history 才能验证关键行为。review 记录显示：

- `tests/test_contactskill_persona_brief.py`: 21 passed
- `tests/test_contactskill_policy_briefs.py`: 31 passed
- `tests/test_contactskill_projection.py`: 47 passed
- `tests/test_chat_context_decomposition.py`: 39 passed
- `pytest tests/ -q`: 327 passed

这意味着：

- schema 行为可在干净环境验证
- projection 行为可在干净环境验证
- context integration 与 fallback / coexistence 行为可在干净环境验证

当前仍没有基于真实 `private/distilled/` 文件的 committed end-to-end test，但对 M6 这个 contract/integration 里程碑来说，不构成 gate 阻塞。

## 3. 是否有测试、demo 或实验结果

有，而且证据充分。

M6 当前可用证据包括：

- 138 个与 M6 直接相关的 committed synthetic tests（21 + 31 + 47 + 39）
- 多轮 compile / pytest 记录，见 `T171_review.md`、`T172_review.md`、`T173_review.md`、`T174_review.md`
- 代码级结构证据：`DerivedBriefContext`、`ContactSkillProjectionService`、相关 brief schemas、以及 `ChatContextAssembler` wiring 均已进入仓库

这对 M6 的目标已经足够。该里程碑本身不是实验性质量评估，而是结构兼容性与 context wiring 验证。

## 4. 是否存在伪完成

未发现阻塞性的伪完成。

当前实现没有把以下事情伪装成已完成：

- 没有把 derived briefs 写成 ContactSkill replacement
- 没有隐藏掉 `ApprovedContactSkillBrief` fallback
- 没有把 approved-patch compact-context path 偷偷并入 derived-brief path
- 没有把 planner 行为变化、LLM 调用、send gate、平台接入混入 M6
- 没有把 synthetic-only coverage 误写成 real-data quality completion

剩余的小问题主要是非阻塞性的工程细节，例如：

- `DerivedBriefContext.status` 复用较宽的 enum
- `_load_derived_brief_context` 的 `contact_id` 参数目前未使用
- synthetic coverage 仍有几个很窄的分支未单独断言

这些都属于真实债务，不属于伪完成。

## 5. 是否允许进入下一里程碑

允许，以 `Allow` 进入 M7，但只允许从 T180 这个 contract-only 入口开始。

允许进入：

- `docs/tasks/M7_llm_reply_planner/T180_llm_candidate_contract.md`

当前不允许进入：

- 真实 LLM 调用
- hybrid planner 行为切换
- planner runtime mutation
- outbound/send integration
- 任何绕过现有 review-only / boundary / privacy contract 的路径

也就是说，M7 现在只能开一个很窄的口：先定义 contract，再决定后续执行路径。

## Remaining Risks Carried Forward

- R039: 进入 M7 后可能重新引入 LLM scope creep
- R040: 未来 planner/context 变更仍可能破坏 M6 刚建立的 additive fallback contract
- R041: feedback / patch / derived brief 仍可能被误解为 automatic learning，必须继续维持 review-only interpretation

R061 可在 M6 范围内关闭：T174 committed tests 已经证明 derived briefs 是 additive overlay，且与 `ApprovedContactSkillBrief` fallback 和 T164 patch context 共存。

## Required Next Task

Proceed to `docs/tasks/M7_llm_reply_planner/T180_llm_candidate_contract.md`.
