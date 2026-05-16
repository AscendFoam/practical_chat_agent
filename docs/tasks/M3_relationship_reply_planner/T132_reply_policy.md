# Task T132: Reply Policy

## Task ID

T132

## Goal

为 T131 `ReplyPlanner` 增加显式 policy / boundary 检查，覆盖敏感话题、禁忌话题、过度主动、冒充和数字克隆风险。

输出仍然必须是 review-only 的 T130 `ReplyPlan`。本任务的目标是让风险场景在候选草稿中可见：通过更保守的候选、`risk_flags` 和 `boundary_reminders` 提醒人类 reviewer，而不是自动发送或替用户做自主联系决策。

## Why Now

T131 已作为安全 wiring baseline 通过 review，但 reviewer 明确指出候选文本仍偏模板化，relationship-awareness 还比较浅。进入 T133 holdout eval 前，planner 需要先有更强的安全层，避免边界场景被当成普通关系感知建议输出。

## Allowed Files

- `src/practical_chat_agent/services/reply_planner.py`
- `src/practical_chat_agent/services/policy.py`
- `docs/07_handoff.md`

## Forbidden Scope

- 不新增自动发送、delivery connector、实时平台接入、scheduler 或 outbound automation。
- 不新增数据库 migration、vector DB、pgvector、embedding 或持久化改动。
- 不读取 `private/chat_history/`。
- 不把完整 ContactSkill JSON、全部 memory facts、raw transcript text 或 private output 注入 prompt-facing / review-facing surface。
- 不降低 `policy.py` 里已有 outbound policy 的安全性。
- 不把 T131 重写成 LLM drafting 系统。
- 不推进 T133 或 M4。

## Inputs To Read

- `docs/review/T131_review.md`
- `docs/data_contracts/reply_plan_contract.md`
- `docs/tasks/M3_relationship_reply_planner/T131_reply_planner.md`
- 当前 `src/practical_chat_agent/services/reply_planner.py`
- 当前 `src/practical_chat_agent/services/policy.py`
- T123 compact fields exposed through `ChatContext.approved_store_context`，尤其是可用的 boundary reminders / avoid-topic 信息。

## Required Behavior

- 保留现有 `ReplyPlanner.generate(context=...) -> ReplyPlan` contract。
- 保留 T131 已实现的 `priority_rank` 唯一顺序校验和 `contact_id` 对齐校验。
- 至少显式处理以下风险类别：
  - `boundary_sensitive`: contact skill 或 runtime context 显示应谨慎、应保持边界或应避开某类话题。
  - `over_proactive`: 候选会推动行动、追问、亲密升级或超出当前上下文的主动联系。
  - `impersonation_risk`: 候选可能像是在替联系人说话，或预测联系人会怎么说。
  - `thin_context`: approved-store context 缺失或过弱，不足以支撑自信的关系特定表达。
- 高风险场景应至少产生一个保守候选或 no-pressure alternative。
- 候选的 `risk_flags` 和 `boundary_reminders` 必须用可审查语言说明原因。
- 候选文本必须保持从用户视角出发，不能模拟联系人，也不能输出第三方角色扮演。

## Expected Output

- T131 planner 仍输出合法的 T130 `ReplyPlan`，且至少包含 3 个候选。
- 敏感或边界较强的 context 会明显改变输出：
  - wording 更保守；
  - boundary reminders 更明确；
  - risk flags 能对应到 policy / boundary 原因。
- 普通安全 context 不应被过度拦截。
- `docs/07_handoff.md` 记录实现内容、验证命令和剩余风险。

## Verification

只使用 synthetic 或 redacted 输入。

最低验证要求：

- Compile changed modules:
  - `python -m compileall src/practical_chat_agent/services/reply_planner.py src/practical_chat_agent/services/policy.py src/practical_chat_agent/app/main.py`
- 运行一个 safe baseline synthetic context，确认仍输出 3 个候选。
- 运行至少一个 boundary / avoid-topic synthetic context，确认：
  - 输出仍是合法 `ReplyPlan`；
  - 至少一个候选包含相关 `risk_flags`；
  - `boundary_reminders` 包含对应 caution；
  - 没有 echo raw input text 或 disallowed private identifiers。
- 运行至少一个 thin-context synthetic context，确认 confidence / risk / boundary 行为保持保守。

## Reviewer Type

adversarial

Reviewer 重点检查 T132 是否真的增强 safety behavior，同时没有扩大 scope 到发送、持久化、LLM drafting 或平台接入。
