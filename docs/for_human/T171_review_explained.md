# T171 Review Explained: PartnerPersonaBrief Schema

## 1. 这个任务在做什么？（通俗解释）

想象你有一个非常详细的"联系人档案卡"（ContactSkill），上面记录了关于某个联系人的所有信息——关系状态、沟通风格、喜好话题、情绪模式、回复策略、边界规则等等。这张卡片很全面，但在实际使用时（比如帮你想回复消息的时候），你并不需要把整张卡片的信息全拿出来。

T171 做的事情就是从这张大卡片里"摘取"出**只跟"这个人是谁、关系怎么样、怎么沟通"相关的部分**，做成一张精简的小卡片，叫做 `PartnerPersonaBrief`（伙伴人像摘要）。

打个比方：ContactSkill 就像一份完整的员工档案，而 PartnerPersonaBrief 就像是你脑海中对这个同事的快速印象——"他是我的同事，关系还不错，说话简短直接，喜欢聊项目进展和周末计划，偶尔有点内敛。" 这个快速印象足够让你在回复他时调整语气和内容，但不需要你翻阅他的全部档案。

重要的是，这张小卡片是**附加的**，不是替代品。原来的完整档案还在，小卡片只是一个可选的补充。

## 2. 实现细节

### 2.1 任务目标

在 `src/practical_chat_agent/core/models.py` 中新增两个 Pydantic 模型：

1. **`CommunicationStyleSnapshot`**：结构化的沟通风格快照，包含 4 个可选字段（消息长度、语气、回复速度、直接程度）。
2. **`PartnerPersonaBrief`**：派生的人像摘要，包含 8 个字段。

同时编写契约文档和验证测试。

### 2.2 代码变化

#### models.py（新增 18 行）

在 `PreferencePatchCandidate` 之后、`ChatContext.model_rebuild()` 之前，新增了：

- `CommunicationStyleSnapshot`：4 个 `str | None` 字段，全部可选，默认 `None`。这是一个独立的辅助模型，用来结构化表达沟通风格。
- `PartnerPersonaBrief`：8 个字段，其中 3 个必填（`contact_id`、`relationship_state_summary`、`source_skill_record_id`）、1 个必填枚举（`relationship_type`）、4 个带默认值的列表/对象。

没有修改任何已有模型。新增代码是纯增量的。

#### contactskill_decomposition_contract.md（新增）

完整的契约文档，包含：
- 两个模型的字段定义和含义
- 从 ContactSkill 到 brief 的投影规则表
- 证据和源可追溯性规则
- 回退关系说明（PartnerPersonaBrief 不替代 ApprovedContactSkillBrief）
- 审批继承规则（brief 不自带审批状态，继承父记录的审批状态）
- 非目标清单

#### test_contactskill_persona_brief.py（新增，21 个测试）

覆盖：
- 有效构造（3 个）
- 必填字段验证（7 个）
- 默认值和可选字段（5 个）
- CommunicationStyleSnapshot 类型验证（5 个）
- 无效关系类型拒绝（1 个）

#### 07_handoff.md（更新）

新增第 70 节（T171 实现记录），原第 70 节（T170 Kickoff Notes）重编号为第 71 节。

### 2.3 关键设计决策

**communication_style_snapshot 的类型选择：**

T170 设计文档中暂定为 `dict[str, str]`。T171 经过考虑后选择了结构化的 Pydantic 子模型 `CommunicationStyleSnapshot`，原因：
- 4 个维度是已知且稳定的（对应 ContactSkillCommunicationStyle 的 4 个字段）
- 命名模型提供类型安全、IDE 自动补全和 Pydantic 验证
- 避免字典键拼写错误
- 与代码库中其他模型风格一致

这直接解决了 T170 评审意见 N02。

### 2.4 对后续开发的意义

- **T172**（下一个任务）将定义 `CommunicationPolicyBrief` 和 `BoundaryProfileBrief` 两个 schema，完成 ContactSkill 分解的三张精简卡片。
- **T173** 将实现投影服务，从已审批的 ContactSkill 自动生成这些精简卡片。
- **T174** 将把这些卡片集成到 `ChatContextAssembler` 中，让回复规划器可以利用更结构化的联系人信息。
- 长远来看，这种分解让回复规划器可以只获取它需要的上下文，而不是每次都加载完整的 ContactSkill，减少信息过载。

## 3. 为什么给出 PASS 的评审结果？

**评审结论是 PASS（通过），没有任何阻塞问题。**

### 通过的理由

1. **任务目标完成**：成功定义了 `PartnerPersonaBrief` 和 `CommunicationStyleSnapshot` 两个 Pydantic 模型，是纯增量添加。

2. **没有触碰已有功能**：210 个测试全部通过（189 个已有 + 21 个新增），零回归。没有修改 `ContactSkillCandidate`、`ContactSkillStoreRecord` 等任何已有模型。

3. **没有伪实现**：模型是真实的 Pydantic 数据类，不是 mock 或 stub。测试使用合成数据验证了真实的 Pydantic 校验行为。

4. **测试充分**：21 个合成测试覆盖了有效构造、必填字段、默认值、序列化往返、类型验证和无效输入拒绝。

5. **文档准确**：契约文档清晰记录了字段含义、投影规则、证据溯源、回退关系和非目标。没有把计划写成已完成的事实。

6. **范围严格**：没有投影服务、没有运行时集成、没有 CLI 入口、没有存储/迁移、没有 ContactSkill 变更。完全在任务包定义的允许范围内。

7. **T170 评审意见 N02 被解决**：明确选择了结构化子模型而非字典，并在契约中记录了理由。

### 记录的非阻塞问题

- `CommunicationStyleSnapshot` 的字段没有用 `Literal` 限制取值范围（当前可接受，T173 投影时可收紧）
- `relationship_state_summary` 是自由文本字符串（T173 需要定义投影规则）
- `evidence_refs` 合并后丢失了子模型级别的归属信息（设计折衷，记录在案）
- brief 没有独立的 `schema_version` 字段（低风险，父记录有自己的版本管理）

这些问题都不阻塞任务完成，适合在后续任务中处理。

## 4. 关于 Worker 写的文档

Worker 没有自行编写 review 文档或 explanation 文档（这是 reviewer 的职责），所以不存在需要检查或补充的 worker review/explanation 内容。

Worker 产出的实现记录（handoff Section 70）和契约文档内容准确，与实际代码一致。实现记录中的验证结果（21 个测试通过、210 个总测试通过、零回归）经 reviewer 独立运行确认属实。
