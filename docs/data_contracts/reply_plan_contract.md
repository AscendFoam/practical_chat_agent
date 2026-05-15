# Reply Plan Contract

更新日期：2026-05-15

本文档定义 T130 引入的 `ReplyPlan` contract。它的用途是把 T123 已接入 `ChatContext` 的 approved-store brief、recent context 和 policy/boundary 提示，整理成可审计、可校验、可人工 review 的“候选回复规划”结构。

`ReplyPlan` 不是发送动作，不是自动回复，不是联系人的拟人化模拟，也不是“对方会怎么说”的角色扮演输出。它只服务于后续 T131/T132 的候选草稿生成与人工审阅。

## 1. Usage Boundary

`ReplyPlan` 必须满足以下边界：

1. 仅用于 candidate generation and review。
2. 只描述“用户可以考虑怎么回”，不代表系统已经决定发送。
3. 不得 impersonate contact，不得生成“像对方本人一样说话”的资产。
4. 不得声称掌握没有 evidence 的关系判断、偏好判断或边界判断。
5. 对 uncertain / sensitive cases 应优先给出 conservative options。

一句话原则：

> ReplyPlan is a review-first planning artifact, not an autonomous reply or impersonation asset.

## 2. Compatibility With T123

T123 已把 approved-store 信息压缩为 `ChatContext.approved_store_context`：

- `approved_store_context.contact_skill`
- `approved_store_context.memory_facts`
- `approved_store_context.source_record_ids`
- `approved_store_context.evidence_refs`
- `approved_store_context.status`

T130 的 `ReplyPlan` 不重新读取 store 文件，也不要求完整 skill JSON。它只要求上游能提供这些 compact brief 或对应的安全引用：

- approved contact-skill `record_id`
- approved memory-fact `record_id`
- approved store `evidence_refs`
- recent event ids
- existing runtime memory hit ids

因此，T131 可以只消费 `ChatContext` 与现有 runtime context，而不需要绕过 T123 的 runtime-ready / human-reviewed gate。

## 3. Schema Overview

`src/practical_chat_agent/core/models.py` 新增：

- `ReplyPlanContextRef`
- `ReplyPlanSourceContext`
- `ReplyPlanCandidate`
- `ReplyPlan`

以及两个 Literal type：

- `ReplyPlanMode = "candidate_review_only"`
- `ReplyPlanContextRefType`

支持的 `ref_type`：

- `approved_contact_skill_record`
- `approved_memory_fact_record`
- `approved_store_evidence_ref`
- `recent_event`
- `memory_hit`
- `policy_boundary`

## 4. JSON Shape

最小 JSON 形状如下：

```json
{
  "schema_version": "reply_plan_v1",
  "plan_mode": "candidate_review_only",
  "contact_id": "contact_xxx",
  "source_context": {
    "approved_store_status": "loaded",
    "chat_context_summary": "Approved store context is available for this contact.",
    "recent_event_ids": ["evt_recent_1", "evt_recent_2"],
    "memory_hit_ids": ["mem_runtime_1"],
    "approved_contact_skill_record_id": "skillstore_001",
    "approved_memory_record_ids": ["memstore_001", "memstore_002"],
    "approved_store_evidence_refs": ["evt_hist_1", "chk_hist_2"]
  },
  "policy_boundary_summary": [
    "Drafts are for human review only.",
    "Prefer low-pressure wording when evidence is thin."
  ],
  "notes_on_candidate_differences": [
    "Candidate 1 is the safest acknowledgment-only option.",
    "Candidate 2 adds a light follow-up question.",
    "Candidate 3 is warmer but should be reviewed more carefully."
  ],
  "candidates": [
    {
      "candidate_id": "replycand_001",
      "approach_label": "conservative_acknowledgment",
      "priority_rank": 1,
      "draft_text": "收到，我先跟上你这个点。",
      "rationale": "Use the approved contact-skill brief to keep the tone light and non-pushy.",
      "supporting_context_refs": [
        {
          "ref_type": "approved_contact_skill_record",
          "ref_id": "skillstore_001",
          "note": "relationship summary and boundary reminders"
        },
        {
          "ref_type": "recent_event",
          "ref_id": "evt_recent_1"
        }
      ],
      "risk_flags": [],
      "boundary_reminders": [
        "Do not sound overly intimate.",
        "Do not assume unverified emotional state."
      ],
      "confidence": 0.78
    },
    {
      "candidate_id": "replycand_002",
      "approach_label": "light_follow_up",
      "priority_rank": 2,
      "draft_text": "这个我接住了，如果你愿意的话也可以继续说说。",
      "rationale": "Adds a gentle invitation without pushing for more disclosure.",
      "supporting_context_refs": [
        {
          "ref_type": "approved_memory_fact_record",
          "ref_id": "memstore_001"
        },
        {
          "ref_type": "policy_boundary",
          "ref_id": "boundary_non_pushy"
        }
      ],
      "risk_flags": ["slightly_more_proactive"],
      "boundary_reminders": [
        "Keep the follow-up optional.",
        "Avoid escalating intimacy."
      ],
      "confidence": 0.7
    },
    {
      "candidate_id": "replycand_003",
      "approach_label": "warm_but_guarded",
      "priority_rank": 3,
      "draft_text": "我在，先把你这句认真接住，后面我们慢慢聊也行。",
      "rationale": "Offers warmth while still preserving pacing and review visibility.",
      "supporting_context_refs": [
        {
          "ref_type": "approved_store_evidence_ref",
          "ref_id": "evt_hist_1"
        },
        {
          "ref_type": "memory_hit",
          "ref_id": "mem_runtime_1"
        }
      ],
      "risk_flags": ["tone_may_feel_more_intimate"],
      "boundary_reminders": [
        "Review for over-closeness before use."
      ],
      "confidence": 0.62
    }
  ]
}
```

## 5. Field Semantics

### 5.1 `ReplyPlan`

| 字段 | 必填 | 说明 |
| --- | --- | --- |
| `schema_version` | 是 | 当前固定为 `reply_plan_v1` |
| `plan_mode` | 是 | 当前固定为 `candidate_review_only` |
| `contact_id` | 是 | 与 T123 compact context 对齐的 contact id |
| `source_context` | 是 | 说明本次规划依赖了哪些 compact context / ids |
| `policy_boundary_summary` | 是 | 回复规划层面的总体边界摘要，至少 1 条 |
| `notes_on_candidate_differences` | 是 | 解释候选为何不同，至少 1 条 |
| `candidates` | 是 | 至少 3 个 candidate |

规则：

1. `candidates` 不能少于 3 个。
2. `ReplyPlan` 本身不要求原始 transcript 文本。
3. `contact_id` 应与 T123 `ApprovedStoreContext.contact_id` / current runtime routing 保持一致。

### 5.2 `ReplyPlanSourceContext`

| 字段 | 必填 | 说明 |
| --- | --- | --- |
| `approved_store_status` | 是 | 直接复用 T123 的 `ApprovedStoreContextStatus` |
| `chat_context_summary` | 否 | 来自 `ChatContext.summary` 的安全摘要 |
| `recent_event_ids` | 否 | 本轮 recent context 引用的 event ids |
| `memory_hit_ids` | 否 | 现有 runtime memory hits 的 memory ids |
| `approved_contact_skill_record_id` | 否 | T123 approved contact-skill brief 的 `record_id` |
| `approved_memory_record_ids` | 否 | T123 approved memory briefs 的 `record_id` 列表 |
| `approved_store_evidence_refs` | 否 | T123 approved store evidence refs |

### 5.3 `ReplyPlanCandidate`

| 字段 | 必填 | 说明 |
| --- | --- | --- |
| `candidate_id` | 是 | 候选规划 id |
| `approach_label` | 是 | 候选策略标签，便于 review |
| `priority_rank` | 是 | 1 开始的排序信号 |
| `draft_text` | 是 | 候选回复草稿文本 |
| `rationale` | 是 | 为什么建议这个草稿 |
| `supporting_context_refs` | 是 | 至少 1 个上下文引用，不允许无依据候选 |
| `risk_flags` | 否 | 风险标签 |
| `boundary_reminders` | 是 | 至少 1 条边界提醒 |
| `confidence` | 否 | 0~1 的弱置信信号，可用于 review 排序，不代表 truth score |

规则：

1. 每个 candidate 都必须带 `draft_text` 和 `rationale`。
2. 每个 candidate 都必须带 `supporting_context_refs`。
3. 每个 candidate 都必须带 `boundary_reminders`。
4. `risk_flags` 允许为空，但 sensitive / uncertain option 应显式标记。
5. `confidence` 是 review 辅助信号，不得被描述为“确定性”。

### 5.4 `ReplyPlanContextRef`

| 字段 | 必填 | 说明 |
| --- | --- | --- |
| `ref_type` | 是 | 引用类型 |
| `ref_id` | 是 | 引用 id |
| `note` | 否 | 人类可读注释 |

它的目标不是装下全文证据，而是给 T131/T132 和 human reviewer 一条“这条草稿依据了什么”的安全索引链。

## 6. Prompt Contract Expectations

后续 T131 若基于 LLM 生成 `ReplyPlan`，prompt contract 必须明确：

1. 输出目标是 `ReplyPlan`，而不是最终发送消息。
2. 必须生成至少 3 个候选，并解释差异。
3. 每个候选都必须引用 supporting context refs。
4. 必须优先使用 T123 already-approved context，而不是猜测联系人的人格或心境。
5. 不得 impersonate contact。
6. 不得 claim knowledge without evidence。
7. uncertain / sensitive cases 要优先给 conservative drafts。
8. risk flags 和 boundary reminders 不能省略。

推荐的 planner-level instruction 核心句式：

> Generate review-only reply candidates for the user, not for autonomous sending.

> Do not imitate the contact, and do not claim relationship knowledge without cited context refs.

> When the context is uncertain or sensitive, prefer conservative, low-pressure options.

## 7. Validation Expectations

T130 的 schema-level validation 重点如下：

1. `ReplyPlan` 可表示 3 个及以上 candidate。
2. candidate 可引用 T123 approved-store brief ids 和 evidence refs。
3. schema 不强制原始 transcript text。
4. `approved_store_status` 直接兼容 T123 `ApprovedStoreContextStatus`。
5. `boundary_reminders` 与 `policy_boundary_summary` 都是显式字段，方便 T132 做 rule checks。

## 8. Non-Goals

本 contract 当前不负责：

- 真正调用 LLM
- 真实生成或发送消息
- 重新审批 ContactSkill / memory facts
- 直接读取 `private/chat_history/`
- 重新实现 store gate / evidence gate
- 数据库或向量库接入
