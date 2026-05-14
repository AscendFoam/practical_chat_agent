# Distillation Output Contract

更新日期：2026-05-14

本文档定义离线蒸馏 MVP 在 T111 阶段的三类核心输出 contract：

- `ChunkSummary`
- `MemoryFactCandidate`
- `ContactSkillCandidate`

目标不是立即生成真实蒸馏结果，而是先为 T112 的 JSON 校验、T113 的 skill builder 与 review artifact 固定字段边界。所有 schema 都必须满足以下共性要求：

1. 所有 fact / claim / skill 相关结构都必须支持 `evidence_refs`。
2. 所有候选结构都必须包含 `confidence`、`sensitivity`、`status`。
3. `ContactSkillCandidate` 的用途必须严格限制在“辅助用户沟通”，明确禁止 persona clone / impersonation。
4. 可提交文档中不得包含真实聊天原文、真实联系人姓名或 `private/` 中的私密内容。

## 1. Status / Sensitivity Conventions

### 1.1 `status`

T111 固定的候选态约定如下：

- `candidate`: 尚未人工批准，默认状态。
- `approved`: 已通过人工 review，可进入下游使用。
- `rejected`: 明确不可信或不应使用。
- `frozen`: 暂停使用，等待更多证据或人工处理。
- `archived`: 历史版本，仅保留审计价值。

T111 只定义 contract，不实现状态流转逻辑。

### 1.2 `sensitivity`

- `low`: 普通话题、低风险事实或沟通偏好。
- `medium`: 关系状态、边界、情绪模式等需要谨慎处理的信息。
- `high`: 高敏感事实、脆弱情绪、第三方隐私或需要更强 review 的内容。

T112+ 不得因为字段存在就自动生成高敏感内容；仍需遵守 T101 隐私边界。

## 2. `ChunkSummary`

`ChunkSummary` 是单个 conversation chunk 的客观观察结果。它是 T110 `chunks.jsonl` 的下游结构，不是长期记忆，不应直接等价于稳定人格判断。

最小 JSON 形状：

```json
{
  "chunk_id": "chk_xxx",
  "contact_id": "contact_xxx",
  "conversation_id": "conv_xxx",
  "time_range": ["2026-05-01T10:00:00+08:00", "2026-05-01T10:30:00+08:00"],
  "event_ids": ["evt_a", "evt_b"],
  "message_count": 12,
  "chunking_reason": "time_gap",
  "summary": "本段对话主要围绕某件具体事情展开。",
  "topics": ["近况", "工作安排"],
  "evidence_refs": ["chk_xxx", "evt_a", "evt_b"],
  "confidence": 0.74,
  "sensitivity": "low",
  "status": "candidate",
  "important_facts": [
    {
      "claim": "对方提到最近在准备面试。",
      "evidence_refs": ["evt_a", "evt_b"],
      "confidence": 0.82,
      "sensitivity": "medium",
      "status": "candidate",
      "rationale": "同一段中有直接陈述。"
    }
  ],
  "communication_observations": [
    {
      "observation_type": "tone",
      "claim": "这一段回复节奏偏快，且语气较自然。",
      "evidence_refs": ["evt_c", "evt_d"],
      "confidence": 0.68,
      "sensitivity": "low",
      "status": "candidate"
    }
  ],
  "risk_notes": [
    "不要把单次积极回复直接升级为稳定关系结论。"
  ],
  "source_message_type_codes": [0, 25, 80],
  "interaction_flags": ["reply", "system_notice"],
  "risk_flags": ["message_type_mixed"]
}
```

字段约束：

| 字段 | 必填 | 说明 |
| --- | --- | --- |
| `chunk_id` | 是 | 对应 T110 输出的 chunk 主键 |
| `contact_id` | 是 | 联系人稳定 ID |
| `conversation_id` | 是 | 会话稳定 ID |
| `time_range` | 是 | chunk 起止时间，允许 `null` 占位 |
| `event_ids` | 是 | 该摘要覆盖的事件列表 |
| `message_count` | 是 | 覆盖事件数量 |
| `chunking_reason` | 是 | 继承 T110 的 chunking 原因 |
| `summary` | 是 | 客观摘要，不应包含夸张推断 |
| `topics` | 否 | 供 T113 / T114 使用的话题标签 |
| `evidence_refs` | 是 | 至少应能回指 `chunk_id` 或相关 `event_id` |
| `confidence` | 是 | 0~1 |
| `sensitivity` | 是 | `low|medium|high` |
| `status` | 是 | 默认 `candidate` |
| `important_facts` | 否 | 可被提升为记忆候选的原子结论 |
| `communication_observations` | 否 | 沟通风格或互动观察，不应直接写成长期人格 |
| `risk_notes` | 否 | 提醒后续 fact/skill builder 避免过度推断 |
| `source_message_type_codes` | 否 | 延续 T102/T110 不确定性信号 |
| `interaction_flags` | 否 | 延续 T102/T110 不确定性信号 |
| `risk_flags` | 否 | 延续 T102/T110 不确定性信号 |

## 3. `MemoryFactCandidate`

`MemoryFactCandidate` 是候选长期记忆。它比 `ChunkSummary` 更原子、更可复用，但仍然处于 review 前状态，不得默认视为真。

最小 JSON 形状：

```json
{
  "memory_id": "mem_xxx",
  "memory_type": "relationship",
  "subject_id": "contact_xxx",
  "claim": "对方对直接追问私人安排较谨慎。",
  "evidence_refs": ["chk_001", "evt_123", "evt_124"],
  "confidence": 0.71,
  "importance": 0.78,
  "sensitivity": "medium",
  "status": "candidate",
  "rationale": "多次出现短回复或回避式转移话题。",
  "conflicts_with": [],
  "source_chunk_ids": ["chk_001", "chk_004"]
}
```

字段约束：

| 字段 | 必填 | 说明 |
| --- | --- | --- |
| `memory_id` | 是 | 候选记忆 ID |
| `memory_type` | 是 | 建议值：`semantic|episodic|relationship|procedural|reflection` |
| `subject_id` | 是 | `contact_xxx|user|relationship_xxx` |
| `claim` | 是 | 原子化、可审计的结论 |
| `evidence_refs` | 是 | 必须可回指到 `event_id` 或 `chunk_id` |
| `confidence` | 是 | 0~1 |
| `importance` | 是 | 0~1，供后续排序与保留使用 |
| `sensitivity` | 是 | `low|medium|high` |
| `status` | 是 | 默认 `candidate` |
| `rationale` | 否 | 为什么给出这个结论 |
| `conflicts_with` | 否 | 与之冲突的记忆 ID |
| `source_chunk_ids` | 否 | 来源 chunk，方便后续审阅 |

规则：

1. `claim` 必须是“可审计结论”，不能写未来计划、主观 wishful thinking 或无证据人格推断。
2. `evidence_refs` 不能为空列表，除非后续 reviewer 明确允许极少数人工补录情况。
3. 单次现象默认不应直接升格为稳定 relationship fact，除非 `rationale` 说明证据充足。

## 4. `ContactSkillCandidate`

`ContactSkillCandidate` 是“如何与此人沟通”的候选关系技能，不是联系人人格模型，不是数字克隆，也不是替该联系人发言的授权对象。

最小 JSON 形状：

```json
{
  "schema_version": "contact_skill_candidate_v1",
  "contact_id": "contact_xxx",
  "relationship_type": "friend",
  "status": "candidate",
  "confidence": 0.73,
  "sensitivity": "medium",
  "evidence_refs": ["chk_001", "mem_002"],
  "source_chunk_ids": ["chk_001", "chk_004"],
  "source_memory_ids": ["mem_001", "mem_002"],
  "relationship_state": {
    "current_status": "low_frequency_but_continuing",
    "closeness": 0.45,
    "trust_level": 0.50,
    "interaction_frequency": "low",
    "initiative_balance": "user_leads_more",
    "confidence": 0.72,
    "evidence_refs": ["mem_002"],
    "sensitivity": "medium",
    "status": "candidate"
  },
  "communication_style": {
    "message_length": "short",
    "tone": "casual",
    "response_latency": "unstable",
    "directness": "medium",
    "confidence": 0.69,
    "evidence_refs": ["chk_003"],
    "sensitivity": "low",
    "status": "candidate"
  },
  "preferred_topics": [],
  "avoid_topics": [],
  "important_events": [],
  "stable_preferences": [],
  "emotional_patterns": [],
  "user_side_preferences": {
    "user_goal": "自然沟通，不施压",
    "boundaries": ["不要替用户发送过度亲密的话"],
    "preferred_reply_style": "真诚、轻量、留有余地"
  },
  "reply_strategy": {
    "default": "先回应对方内容，再补一个轻量问题。",
    "when_contact_is_cold": "降低追问密度，允许对话自然收束。",
    "when_contact_opens_topic": "优先接住对方主动展开的主题。",
    "for_sensitive_topics": "先确认对方是否愿意继续聊。"
  },
  "usage_boundary": {
    "allowed_uses": ["reply_assistance", "context_retrieval", "human_review"],
    "disallowed_uses": ["persona_clone", "impersonation", "autonomous_contact_simulation"],
    "notes": [
      "ContactSkillCandidate exists to help the user communicate with better context and boundaries.",
      "It must not be used to imitate, replace, or autonomously speak as the real contact."
    ]
  },
  "review_notes": [],
  "redaction_policy": {
    "store_raw_quotes": false,
    "max_quote_length": 30,
    "mask_names": true,
    "mask_phone_numbers": true
  }
}
```

字段约束：

| 字段 | 必填 | 说明 |
| --- | --- | --- |
| `schema_version` | 是 | 当前固定为 `contact_skill_candidate_v1` |
| `contact_id` | 是 | 联系人稳定 ID |
| `relationship_type` | 是 | 关系类别候选 |
| `status` | 是 | 默认 `candidate` |
| `confidence` | 是 | 0~1 |
| `sensitivity` | 是 | `low|medium|high` |
| `evidence_refs` | 是 | skill 级别的总证据引用 |
| `source_chunk_ids` | 否 | 来源 chunk |
| `source_memory_ids` | 否 | 来源记忆候选 |
| `relationship_state` | 是 | 当前关系状态候选 |
| `communication_style` | 是 | 沟通风格候选 |
| `preferred_topics` | 否 | 愿意展开的话题 |
| `avoid_topics` | 否 | 需谨慎的话题 |
| `important_events` | 否 | 关系里有参考价值的重要事件 |
| `stable_preferences` | 否 | 沟通或关系上的稳定偏好 |
| `emotional_patterns` | 否 | 仅用于辅助判断分寸，不等于人格诊断 |
| `user_side_preferences` | 否 | 用户自己的沟通目标与边界 |
| `reply_strategy` | 否 | 给 reply planner 的策略输入 |
| `usage_boundary` | 是 | 明确允许与禁止用途 |
| `review_notes` | 否 | 人工审阅附注 |
| `redaction_policy` | 是 | 私密信息处理策略 |

## 5. Anti-Impersonation Boundary

`ContactSkillCandidate` 必须满足以下硬边界：

1. 不得用于生成“像联系人本人一样持续说话”的系统 prompt。
2. 不得用于自动扮演、替代或模拟真实联系人。
3. 不得把“沟通策略”伪装成“联系人完整人格画像”。
4. 允许的用途仅限：
   - 帮助用户理解关系上下文
   - 约束 reply planner 的语气、边界和节奏
   - 支持人工 review / approve / reject

一句话原则：

> ContactSkillCandidate 是用户沟通辅助策略，不是数字分身，不是 persona clone，不是 impersonation asset。

## 6. 与 T112 / T113 的接口约束

T112 必须遵守：

1. LLM 输出必须能校验为上述 schema。
2. 若缺失 `evidence_refs`、`confidence`、`sensitivity` 或 `status`，该条输出应视为无效。
3. 不得把私密原文复制进可提交目录的示例或日志。

T113 必须遵守：

1. `ContactSkillBuilder` 只能消费通过 schema 校验的 `ChunkSummary` / `MemoryFactCandidate`。
2. review artifact 必须显式展示 `evidence_refs` 与 `usage_boundary`。
3. approve 前的 skill 不得直接进入 reply planner。
