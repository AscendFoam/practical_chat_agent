# Goal 试验分支阶段总结 - 2026-06-01

更新时间：2026-06-06

本文总结本次 `/goal` 试验分支从 M12 之后开始，到当前暂停点为止已经完成的工作。当前可确认完成到 M43/T470：`source_draft_apply_readiness` 已完成 payload、静态 UI、Review Workspace linkage、responsive hardening 和 milestone review。M43 review 结论为 `PASS_WITH_WARNINGS`。

这份总结重点回答三个问题：

- 一开始 M12 留下了什么基础。
- 在这个基础上，后续 M13-M43 分别补了哪些产品、架构、UI、review 和安全能力。
- 目前暂时达到了什么程度，以及还没有达到什么程度。

结论先说清楚：当前项目已经从“研究微信/企微类平台能否接入和发送消息”的方向，转向了“本地、合成、文本优先、可审核、可解释的 AI companion 产品原型”。它已经具备 persona、memory、review workspace、manual apply preview、source intake、source evidence、persona proposal、persona draft 等一整套雏形链路；可以展示类似 TheOne、爱语这类陪伴式产品的关键结构，但还不是生产级聊天产品。它没有真实私聊读取，没有真实真人蒸馏，没有模型 provider 调用，没有 embedding/向量检索，没有外部平台收发，没有自动发消息，没有语音或 Live2D/avatar runtime，也没有支付、账号、生产鉴权或合规完成声明。

## 0. M12 开始时留下的基础

M12 的核心结论是 `Gate M12 Conditional`。它没有授权 live WeChat / WeCom 投产，而是证明了一条非常受限的本地合成干跑链路。

M12 已完成的关键工作包括：

- T230 做了 WeChat-family adapter 研究，明确阻断个人微信自动化、扫码登录复活、桌面自动化、实时个人号收发、非官方 SDK vendoring 等高风险路径。
- T231 做了合成 WeCom Customer Service inbound normalization，只允许把合成 fixture 规范化成本地 `InboundEvent`，不支持 live callback、webhook、polling、签名、解密或真实存储。
- T233 做了本地 provider safety eligibility gate，在 `OutboundMessageRequest.is_sendable()` 之后再检查 recipient alias、服务窗口、消息额度、kill switch、channel/surface 和 metadata smuggling。
- T232 做了本地 dry-run outbound payload preparation，只有请求 sendable 且 safety decision 匹配并允许时，才生成 review-safe dry-run payload；结果明确 `delivered=False`、`wecom_dry_run_only`、`no_provider_delivery`。

因此，M12 留下的不是“平台可发消息”的能力，而是后续所有工作的工程红线：

- 候选动作、人工审批、send gate、provider eligibility、dry-run payload、API acceptance、ack、retry、failure event、delivery 必须分层。
- outbound 行为必须先进入本地审核和安全 gate，不能因为某个候选动作被 review 就自动发送。
- 真实平台、真实账号、真实 recipient id、token、callback、自动发送都不能直接进入主线。
- 项目更适合先做本地、合成、可审核的 persona companion 产品能力，而不是继续硬推 WeChat/WeCom live adapter。

这个基础对后续非常关键：它把项目从“接入平台发消息”的高风险轨道，调整为“先把 persona、memory、review、control、trust 做扎实”的产品轨道。

## 1. M13：产品方向转向 AI companion

M13/T240 完成了商业陪伴式 agent 的产品定位和安全边界。

这一阶段确定了近期主线：不再把 live WeChat / WeCom 交付作为核心目标，而是建设一个透明、可控、文本优先的 AI persona companion。它的产品承诺是：

- 用户可以创建并共同塑造一个明确标注为 AI 的 persona。
- persona 有稳定身份、长期关系记忆、可解释成长、虚拟生活流和用户可控的 memory/persona 状态。
- 用户可以检查、编辑、冻结、删除和导出它记住的内容，以及它如何变化。

同时，M13 明确排除了若干不应该承诺的方向：

- 不承诺“克隆任何真人”。
- 不承诺“复活逝者”。
- 不承诺让 AI 与真人无法区分。
- 不承诺 live WeChat/WeCom/Feishu delivery。
- 不做隐藏式自动回复 agent。
- 不做未标注 AIGC 图片、语音、视频或社交动态。
- 不把危机干预、心理诊断、临床支持作为商业卖点。
- 不用内疚、依赖、占有欲或付费亲密升级来做 retention。

M13 也初步建立了商业化假设：免费层、订阅层、高级层、未来授权型 professional tier。但这些只是产品假设和定价方向，不是经过用户研究验证的商业模式。

## 2. M14：Persona Compiler 和人设卡基础

M14 开始把“用户深度自定义聊天对象”的目标落成结构化对象。

完成的能力包括：

- `PersonaCard v1` 方向和 schema 合同。
- 本地 persona compiler prototype。
- de-identification guard tests，避免未经处理的真人或私密内容直接进入人设卡。
- persona review-card contract，让人设变更先变成可审核卡片。
- persona version store，用于记录 persona 版本、比较和后续回滚。

这一阶段让项目开始拥有“AI 聊天对象”的结构化核心，而不是只靠 prompt 或一段描述。人设被设计成可审查、可版本化、可解释、可回滚的对象。

当前限制：

- 仍是本地合成原型。
- 没有读取真实私聊。
- 没有自动蒸馏真实对象。
- 没有 LLM provider 编译链路。

## 3. M15：Memory OS v2 基础

M15 建立了记忆机制的底层轮廓。它回应了最初目标里“记忆机制是很重要的一环”。

完成的能力包括：

- memory event schema。
- 本地 memory store v2。
- memory lifecycle policy。
- retrieval bundle contract。
- consolidation preview stub。

这一阶段把记忆拆成可治理对象，而不是简单把聊天记录塞进上下文。它为后续接近真人聊天体验打基础：真人感不只来自语气，还来自连续性、边界、共同经历、偏好记忆和可解释变化。

当前限制：

- 记忆仍是本地模型和合成测试。
- consolidation 还只是 preview/stub。
- 没有 embedding、向量检索或真实长期 memory runtime。
- 没有私聊记录 ingestion。

## 4. M16：关系上下文和对话消费

M16 把 persona 和 memory 放进对话使用链路里。

完成的能力包括：

- relationship context bundle。
- dialogue context planner。
- deterministic dialogue draft stub。

这一阶段的核心是：未来生成回复时，不应该只是拼接 persona 和 memory，而应该先形成可解释的 relationship/dialogue context，让系统知道当前关系状态、对话目的、边界和可用记忆。

当前限制：

- 仍是 deterministic stub。
- 没有真实模型生成。
- 没有端到端 live chat runtime。

## 5. M17：主动消息的 consent-first 基础

用户最初希望“最好能根据用户习惯和自身人设主动给用户发消息”。M17 做的是这个方向的安全基础，而不是直接自动发送。

完成的能力包括：

- proactive consent schema。
- proactive policy gate。
- quiet hours / frequency tests。
- proactive review card。
- crisis / low-mood policy。

这一阶段明确了主动行为的原则：

- 主动建议必须先是候选，而不是直接发出。
- 必须尊重同意、时间、频率和低压力语气。
- 低落或危机场景不能被商业化、依赖化或诱导留存。
- 主动消息不能等同于外部平台自动发送。

当前限制：

- 没有 scheduler。
- 没有 queue。
- 没有 webhook。
- 没有自动发送。
- 没有外部平台 adapter。

## 6. M18：虚拟生活流和朋友圈式内容基础

用户希望“可以根据人设自动生成朋友圈之类的，达到以假乱真的效果，但不是真的取代真人聊天”。M18 建立了这个方向的合成生活流基础，并把“以假乱真”约束为“可沉浸，但必须标注和可审核”。

完成的能力包括：

- role dynamic post schema。
- virtual life engine text generator。
- AIGC labeling metadata。
- imagined/factual contamination tests。
- dynamic review card。

这一阶段让 persona 不只存在于 chat 里，也可以有“虚拟生活动态”。但这些动态必须是 AI/imagined 内容，不能污染事实记忆，也不能伪装成真人真实经历。

当前限制：

- 只有文本动态。
- 没有图片/视频生成。
- 没有朋友圈平台发布。
- 没有未标注 AIGC。

## 7. M19：用户控制面

M19 把用户控制权具体化。

完成的能力包括：

- memory viewer data contract。
- persona version editor contract。
- delete / freeze / export local flow。
- deletion verification tests。

这一阶段确保项目不只是“系统自己记住和改变”，而是让用户能看见、冻结、删除、导出和审查。对 companion 产品来说，这是信任基础。

当前限制：

- 主要是 contract/local flow。
- 还不是完整生产 UI。
- 没有真实账户和权限系统。

## 8. M20：合规和安全 baseline

M20 建立了法规、平台政策和安全 baseline。

完成的能力包括：

- 中国合规 checklist。
- 国际 privacy/platform policy checklist。
- consent center data model。
- AIGC labeling plan。
- crisis / dependency policy tests。

这一阶段把后续所有“像真人”“主动关怀”“虚拟生活”“可能引用真人风格”的能力都放进更明确的安全边界里。

当前限制：

- 这些是工程红线和 checklist，不是法律意见。
- 没有声称合规已完成。
- 没有 App Store / 平台审核通过声明。

## 9. M21-M22：文本优先 UX 和语音/avatar 探索

M21 做了文本优先产品体验设计：

- text-first information architecture。
- onboarding / persona creation prototype。
- chat memory explanation prototype。
- life-stream prototype。
- proactive settings prototype。
- user study protocol。

M22 做了语音和 avatar 探索：

- voice technology survey。
- voice consent data model。
- ASR/TTS latency benchmark planning。
- avatar interaction survey。
- M22 milestone review。

这一阶段的产品判断是：先把文本 companion、记忆、控制、审查和信任链路做好，再谈语音和 Live2D/avatar。语音和 avatar 被保留为未来方向，但 runtime 被锁住。

当前限制：

- 没有 ASR/TTS runtime。
- 没有 voice cloning。
- 没有 Live2D runtime。
- 没有 camera/microphone。
- 没有真人 likeness。

## 10. M23-M24：集成文本 Web Demo 和本地服务

M23-M24 把前面的产品和安全设计汇成一个本地 web demo。

完成的能力包括：

- web demo scope。
- demo state adapter。
- static web demo shell。
- scenario switching。
- local server。
- `/demo-state.json`。
- friendly labels / accessibility contract。
- keyboard and responsive UI hardening。
- local browser QA / visual QA evidence。
- walkthrough 文档。

这使项目从纯文档和后端模型，进入可实际打开的本地 demo。用户可以看到 persona、chat memory、review workspace、proactive、life stream、controls、voice/avatar locked 等面板。

当前程度：

- 已有本地网页 demo。
- 用户当前 in-app browser 打开的本地地址是 `http://127.0.0.1:8786/text_first_web_demo.html`。
- demo 是合成状态驱动，不是生产前端。
- 没有登录、真实用户数据、平台消息或模型调用。

## 11. M25-M27：记忆、人设成长、review queue、dry-run apply

M25 进一步完善 memory/persona growth 设计：

- memory architecture design。
- persona growth policy。
- synthetic distillation input contract。
- retrieval/consolidation refresh。

M26 开始实现候选模型：

- memory governance candidate models。
- persona growth candidate models。
- synthetic distillation input models。
- memory retrieval explanation integration。

M27 建立 review queue 和干跑 apply：

- review queue candidate models。
- memory lifecycle dry-run apply。
- persona growth dry-run apply。
- distillation review readiness。

这一阶段的重要成果是：系统可以把“记忆变化”“人设成长”“潜在蒸馏输入”变成候选对象，然后进入 review queue，而不是直接改变 runtime persona 或 memory。

当前限制：

- apply 仍是 dry-run 和 reviewed preview。
- 没有自动写入生产 memory/persona。
- 没有真实蒸馏输入。

## 12. M28-M30：Review Workspace 成型和安全渲染

M28 建立本地 Review Workspace：

- candidate bindings。
- snapshot store。
- review decision impact preview。
- safe export。

M29 把 Review Workspace 接进 UI：

- presentation adapter。
- static panel。
- local server payload。

M30 做安全 DOM renderer 和投影边界测试：

- safe DOM renderer。
- projection boundary tests。
- local visual QA fallback。
- manual apply preview scope。

这一阶段让项目有了一个统一的“审核工作台”。后面所有 persona、memory、session、source intake、source evidence、proposal、draft 都能被转成 review cards，让用户或审核者看到每个候选变更的状态、风险、阻断原因和 preview-only 属性。

当前程度：

- Review Workspace 已经是 demo 中的关键面板。
- 多类卡片可以进入同一套过滤和渲染流程。
- 仍是本地合成 review workspace，不是多人审核后台。

## 13. M31-M33：Manual Apply Preview、风险 gate 和受控 apply executor

M31 建立手动 apply preview：

- manual apply preview records。
- manual apply eligibility gate。
- review workspace apply preview panel。

M32 建立 apply executor risk：

- apply executor risk records。
- approval gate。
- apply risk review panel。

M33 建立受控本地 apply executor：

- persona growth apply executor。
- memory lifecycle apply executor。
- apply executor audit manifest。
- review workspace apply audit panel。

这一阶段从“只能看候选”推进到“可以在本地、受控、可审计地模拟或执行某些 apply”。但仍保留强边界：必须 review，必须 gate，必须 audit，不能变成平台发送或不可见状态突变。

当前限制：

- apply executor 是本地受控链路。
- 没有生产 runtime 写入。
- 没有外部平台。
- 没有自动 outreach。

## 14. M34-M35：集成 companion 场景和本地会话模拟

M34 建立 integrated companion demo：

- scenario spine，把 persona、memory、review、proactive、life-stream、controls、voice/avatar locked 串成完整体验。
- trust/commercial positioning panel，展示订阅假设、价值支柱、信任控制、不可接受商业模式和 readiness gaps。
- responsive hardening。

M35 增加 local companion session simulator：

- deterministic chat turns。
- reviewed memory recalls。
- persona cues。
- safety notes。
- post-turn candidates，包括 memory candidate、persona growth patch、proactive suggestion、life-stream draft。
- session candidates linked into Review Workspace。
- session loop responsive hardening。

这一阶段已经开始接近“类人陪伴式 agent 体验”的雏形：它能展示一段有记忆引用、有角色语气、有边界声明、有后续候选、有 review 的本地会话。

当前程度：

- 可以看到一个合成 companion 如何在聊天中使用 reviewed memory 和 persona cue。
- 可以看到聊天后产生的候选改动如何进入 Review Workspace。
- 还没有真实 LLM 对话生成。
- 还没有真实用户长期会话。

## 15. M36：Persona Distillation Workbench

M36 针对“用户深刻自定义聊天对象”和“从描述/风格信号中打造人设”建立了 synthetic persona distillation workbench。

完成的能力包括：

- persona distillation workbench payload。
- static UI rendering。
- Review Workspace linkage。
- responsive hardening。
- M36 milestone review。

Workbench 能展示：

- 人设特征候选。
- 证据引用。
- 风险或 blocked request。
- preview-only 状态。
- 不自动修改 persona。

当前限制：

- 只使用 synthetic/review-safe 输入。
- 没有读取真实 chat history。
- 没有真实风格蒸馏模型。

## 16. M37：Persona Evolution Preview

M37 解决“聊天对象应该能在聊天过程中有一定改变，模拟成长或一定善变”的方向。

完成的能力包括：

- persona evolution preview payload。
- proposed patch candidates。
- risk labels。
- rollback notes。
- blocked source exclusions。
- static UI rendering。
- Review Workspace linkage。
- responsive hardening。
- M37 milestone review。

这一阶段让 persona 的变化变成可预览的 patch，而不是直接改动人设。它支持“稳定核心 + 受控成长”的思路。

当前限制：

- 变化仍是 preview。
- 不自动 apply。
- 不直接影响真实 runtime persona。

## 17. M38：Persona Version Draft Ledger

M38 针对“人设变化之后如何形成版本、如何处理冲突和回滚”建立了 version draft ledger。

完成的能力包括：

- persona version draft ledger payload。
- version drafts。
- conflict notes。
- rollback refs。
- review outcome labels。
- static UI rendering。
- Review Workspace linkage。
- responsive hardening。
- M38 milestone review。

这一阶段让 persona 不只是“当前状态”，而是有草稿、有冲突、有回滚引用、有审核结果的版本体系。

当前程度：

- 可以在 demo 中看到 persona version draft。
- 可以在 Review Workspace 中审查 version/conflict/rollback/outcome。
- 仍是本地合成 ledger。

## 18. M39：Persona Source Intake Manifest

M39 开始触碰“从用户提供内容或聊天记录提取真人对象特征，然后转换成新对象人设”的前置治理问题：什么来源可以进来，什么必须 blocked，什么只能作为 placeholder。

完成的能力包括：

- `persona_source_intake_manifest` payload。
- static UI rendering。
- Review Workspace linkage。
- responsive hardening。
- M39 milestone review。

Manifest 中包括五类 source candidate：

- detailed description：用户自己给出的详细描述。
- fuzzy seed：模糊设定或偏好种子。
- synthetic dialogue excerpt：合成对话片段。
- user-provided archive placeholder：用户提供 archive 的占位项。
- third-party private source placeholder：第三方私密来源占位项。

同时加入：

- consent gates。
- minimization gates。
- redaction profiles。
- blocked source categories。
- extraction eligibility。
- preview-only apply policy。
- non-execution flags。

这一阶段的关键不是“开始读真实聊天记录”，而是先把 source intake 的治理模型做出来：哪些来源理论上可用，哪些需要 consent/redaction/minimization，哪些必须排除，哪些不能进入 evidence。

当前限制：

- 没有 source reader。
- 没有 upload/import。
- 没有真实 archive read。
- 没有 raw retention。
- 没有 extraction。
- 没有 embedding。

## 19. M40：Persona Source Evidence Matrix

M40 在 M39 source intake 的基础上，建立了 source evidence matrix。它把“来源治理”推进到“证据与特征假设如何关联”的层级。

M40 任务范围包括：

- T447：M40 scope refinement，确定先做 payload-first 的 source evidence matrix。
- T448：添加 `persona_source_evidence_matrix` payload。
- T449：把 evidence matrix 渲染到静态 demo。
- T450：把 source evidence records 链接进 Review Workspace。
- T451：对 source evidence matrix 和 review cards 做 responsive hardening。
- T452：完成 M40 milestone review。

T448 payload 增加了：

- M39 source intake manifest ref。
- eligible source ids。
- excluded source refs。
- evidence rows。
- trait hypotheses。
- quality labels。
- review gate results。
- preview-only、non-extracting apply policy。
- non-execution flags。

T449 静态 UI 增加了：

- source evidence section。
- schema / non-execution labels。
- manifest summary。
- eligible source list。
- excluded source refs。
- evidence rows。
- trait hypotheses。
- quality labels。
- review gate results。

T450 Review Workspace 联动增加了：

- excluded source evidence cards。
- evidence row cards。
- trait hypothesis cards。
- quality label cards。
- review gate result cards。
- `Evidence` filter。
- 更新后的 `Source` filter count，使其同时覆盖 source intake cards 和 source evidence cards。

T451 补了 responsive hardening：

- source evidence review card 长 id 换行。
- item title、status badges、detail rows 和 meta rows 的宽度约束。
- 窄屏场景下 evidence review details 的布局规则。

T452 评审结论为 `PASS_WITH_WARNINGS`。M40 证明 demo 可以安全展示本地合成 source evidence matrix，并把它接进 UI 和 Review Workspace。警告是：浏览器级 responsive QA 未完成，evidence rows 是 fixture summaries，不是真实 extraction outputs。

当前限制：

- evidence rows 仍是 deterministic synthetic fixture summaries。
- 不读取真实文件。
- 不保留 raw content。
- 不做真实 extraction。
- 不做 embedding。
- 不写 persona card。
- 不写 memory store。
- 不自动 apply。

## 20. M41：Source Evidence 到 Persona Proposal

M41 在 M40 evidence matrix 的基础上，继续向“由证据形成可审核的人设建议”推进。

M41 任务范围包括：

- T453：M41 scope refinement，并打包 T454。
- T454：实现 `source_evidence_persona_proposal` payload。
- T455：把 proposal payload 渲染到静态 demo。
- T456：把 proposal records 接进 Review Workspace。
- T457：proposal UI 和 review cards responsive hardening。
- T458：完成 M41 milestone review。

T454 payload 增加了 `source_evidence_persona_proposal`，并链接到 `m40.persona_source_evidence_matrix.v1`。它为以下 persona paths 生成 proposal candidates：

- `style.tone`。
- `style.pacing`。
- `style.humor`。
- `relationship.boundary_style`。
- `memory.use_preference`。
- `growth.short_term_hint`。

每个 proposal candidate 都携带：

- M40 trait hypothesis refs。
- M40 evidence row refs。
- rationale summary。
- confidence band。
- risk labels。
- rollback notes。
- review gates。
- proposal outcomes。
- preview-only apply policy。
- strict non-execution flags。

T455 增加静态 UI：

- `#source-evidence-persona-proposal` section。
- matrix summary。
- proposal candidate list。
- risk label list。
- rollback note list。
- gate list。
- outcome list。
- non-execution labels。

T456 增加 Review Workspace 联动：

- `review_workspace.source_proposal_review_cards`。
- `Proposal` filter。
- proposal candidate / risk / rollback / gate / outcome cards。
- static fallback linkage。

T457 补了 proposal review cards 的 responsive hardening。

T458 评审结论为 `PASS_WITH_WARNINGS`。M41 证明 demo 可以把 M40 source evidence matrix 转成可审核 persona proposal candidates，并通过静态 UI 和 Review Workspace 展示出来。警告是：浏览器级布局 QA 未声称完成，proposal 仍是 synthetic-fixture-only，不是真实来源抽取结果，也不会应用到 PersonaCard。

当前限制：

- 不读取真实来源。
- 不做真实特征抽取。
- 不调用 provider。
- 不做 embedding。
- 不写 PersonaCard。
- 不写 version store / memory store / review store / runtime store。
- 不自动 apply。
- 不发消息。

## 21. M42：Source Proposal 到 Persona Draft

M42 用于把 M41 proposal candidates 继续转成“可检查的人设草稿预览”。这一阶段已经完成到 milestone review，结论为 `PASS_WITH_WARNINGS`。

M42 已完成任务包括：

- T459：M42 scope refinement，并打包 T460。
- T460：实现 `source_proposal_persona_draft` payload。
- T461：把 persona draft preview 渲染到静态 text-first web demo。
- T462：把 draft records 接入 Review Workspace。
- T463：补强 draft UI 和 draft review cards 的 responsive CSS。
- T464：完成 M42 milestone review，并创建 M43 scope。

T460 增加了 `source_proposal_persona_draft` 到 `TextFirstWebDemoState`，并生成 `m42.source_proposal_persona_draft.v1` payload。它链接回 `m41.source_evidence_persona_proposal.v1`，并为以下字段生成 draft field changes：

- `style.tone`。
- `style.pacing`。
- `style.humor`。
- `relationship.boundary_style`。
- `memory.use_preference`。
- `growth.short_term_hint`。

每个 draft field change 都携带：

- M41 proposal ids。
- M40 trait hypothesis ids。
- M40 evidence row ids。
- base persona snapshot 对照。
- unchanged field summaries。
- conflict notes。
- rollback refs。
- review gate results。
- draft outcome labels。
- preview-only apply policy。
- strict non-execution flags。

这一阶段的意义是：链路已经从“来源候选治理”推进到“证据矩阵”，再推进到“persona proposal”，再推进到“persona draft payload”。也就是说，本地 demo 已经能表达一个未来真实功能的大致路径：

```text
source intake -> source evidence matrix -> persona proposal -> persona draft preview
```

M42 之后，demo 不只拥有 payload，还能在页面中展示：

- draft section。
- source proposal summary。
- base persona snapshot。
- selected proposal ids。
- draft field changes。
- unchanged field summaries。
- conflict notes。
- rollback refs。
- review gate results。
- draft outcome labels。
- strict non-execution labels。

同时，Review Workspace 增加了：

- `review_workspace.source_draft_review_cards`。
- `Draft` filter。
- field change / unchanged field / conflict / rollback / gate / outcome cards。

但这个路径目前仍是合成、预览、可审核、非执行的。M42 不做真实 extraction，不应用 persona，不写 store，不调用 provider，不接平台。

## 22. M43：Persona Draft 到 Apply-Readiness Preview

M43 在 M42 的 persona draft preview 基础上，继续推进到“如果未来要 apply，这些字段现在处于什么 readiness 状态”。这一阶段已经完成到 T470，milestone review 结论为 `PASS_WITH_WARNINGS`。

M43 已完成任务包括：

- T465：细化 M43 scope，并创建 T466 payload package。
- T466：实现 `source_draft_apply_readiness` payload。
- T467：把 apply-readiness preview 渲染到静态 web demo。
- T468：把 readiness records 接入 Review Workspace。
- T469：补强 readiness UI 和 readiness review cards 的 responsive CSS。
- T470：完成 M43 milestone review，并创建 M44 scope。

T466 增加了 `source_draft_apply_readiness` 到 `TextFirstWebDemoState`，并生成 `m43.source_draft_apply_readiness.v1` payload。它只从 M42 draft field changes、conflict refs、review gates 和 rollback refs 派生，不读取真实来源内容。

M43 为同一组关键 persona 字段生成 readiness records：

- `style.tone`。
- `style.pacing`。
- `style.humor`。
- `relationship.boundary_style`。
- `memory.use_preference`。
- `growth.short_term_hint`。

每个 readiness record 都携带：

- draft change id。
- persona field path。
- readiness outcome。
- blocking condition ids。
- required review gate result ids。
- rollback ref ids。
- future apply design notes。
- preview-only / mutation-disallowed / review-required flags。

M43 的 readiness outcomes 包括：

- `blocked`：字段目前被 policy、anti-deception 或 memory write 边界阻断。
- `needs_manual_review`：字段可检查，但仍需要人工判断。
- `ready_for_future_apply_design`：字段形状可以为未来另行设计的 apply executor 提供参考，但现在不授权 mutation。

M43 之后，demo 新增了：

- `#source-draft-apply-readiness` 静态 section。
- draft linkage summary。
- apply policy summary。
- evaluated draft change ids。
- field readiness records。
- blocked condition records。
- required review gate refs。
- rollback dependency refs。
- readiness outcome labels。
- non-execution labels。

Review Workspace 增加了：

- `review_workspace.source_readiness_review_cards`。
- `Readiness` filter。
- field readiness / blocked condition / gate ref / rollback dependency / outcome cards。

M43 的意义是：项目已经不只是展示“人设草稿是什么”，还可以展示“这个草稿距离未来可控 apply 还差哪些人工审核、policy gate、rollback 依赖和阻断条件”。它把 deep persona customization 链路从 draft preview 推进到 apply-readiness preview，但仍然没有进入真正的 persona apply。

当前限制：

- 不读取真实 source。
- 不做真实 extraction。
- 不调用 provider。
- 不做 embedding。
- 不写 PersonaCard。
- 不写 PersonaVersionStore。
- 不写 memory/review/runtime store。
- 不自动 apply。
- 不发消息。
- 不接平台。
- 不启用 voice/avatar/media runtime。

## 23. 按最初目标逐项看，当前达到了什么程度

### 23.1 类人陪伴式 agent 体验

已经达到的程度：

- 有本地文本优先 demo。
- 有 persona identity、style/persona cues、reviewed memory recall。
- 有 deterministic chat turns，能展示一段有角色感、记忆引用和边界说明的本地会话。
- 聊天后可以产生 memory candidate、persona growth patch、proactive suggestion、life-stream draft，并进入 Review Workspace。
- 有 trust/commercial positioning panel，可以展示产品定位、信任边界和商业化假设。

暂未达到：

- 没有真实 LLM 聊天 runtime。
- 没有实时模型生成。
- 没有真实用户长期会话。
- 没有生产级前端和账户系统。

### 23.2 深度自定义聊天对象

已经达到的程度：

- 有 `PersonaCard v1`、persona compiler、persona version store。
- 有 persona distillation workbench，用于展示从合成/安全输入生成特征候选。
- 有 persona evolution preview，用于展示人设成长和可控变化。
- 有 persona version draft ledger，用于展示版本草稿、冲突和回滚。
- 有 M39-M43 的 source intake -> evidence matrix -> proposal -> draft -> apply-readiness preview 链路。

这已经覆盖了“详细描述 -> 特征候选 -> 人设 proposal -> 人设 draft -> apply-readiness review”的本地合成框架。模糊设定、渐进式成长和随机/模板 persona 在设计层面已有位置，但还不是完整生产功能。

暂未达到：

- 没有真实用户输入到生产 persona 的完整链路。
- 没有 provider 驱动的自动编译。
- 没有生产 PersonaCard 写入。
- 没有用户长期共同塑造后的真实版本系统。

### 23.3 从聊天记录或真人对象提取特征

已经达到的程度：

- 有 source intake manifest，可以表示 detailed description、fuzzy seed、synthetic dialogue excerpt、user-provided archive placeholder、third-party private source placeholder。
- 有 consent gates、minimization gates、redaction profiles、blocked source categories。
- 有 source evidence matrix，可以表达 eligible/excluded source、evidence row、trait hypothesis、quality label 和 review gates。
- 有 source-evidence-to-persona-proposal payload。
- 有 source-proposal-to-persona-draft payload。
- 有 source-draft-to-apply-readiness payload，可以表达字段进入未来 apply 设计前的 blocked / needs review / ready-for-future-design 状态。

暂未达到：

- 没有读取真实聊天记录。
- 没有读取 `private/chat_history/`。
- 没有真实 archive import/upload/read。
- 没有 raw retention。
- 没有真实抽取、embedding、向量检索或相似度排序。
- 没有把真人对象蒸馏成可上线 persona。

这个限制是有意保留的。该能力风险很高，必须先解决 consent、最小化、去标识化、source ownership、反欺骗、raw retention、第三方隐私和悲伤/依赖场景的边界。

### 23.4 聊天中的人设变化和“成长”

已经达到的程度：

- 有 persona growth policy。
- 有 persona growth candidate models。
- 有 persona evolution preview。
- 有 risk labels、rollback notes、blocked source exclusions。
- 有 persona version draft ledger。
- 有 manual apply preview、apply risk 和 controlled apply/audit manifest。
- M42 补上了从 source proposal 到 persona draft preview 的完整本地展示和 Review Workspace 链路。
- M43 补上了从 persona draft 到 apply-readiness preview 的完整本地展示和 Review Workspace 链路。

这已经形成“人设可变，但变化必须可解释、可审查、可回滚”的框架。

暂未达到：

- 没有生产 runtime 中的人设自动演化。
- 没有真实用户长期互动驱动的成长。
- 没有自动 apply。

### 23.5 记忆机制

已经达到的程度：

- 有 Memory OS v2 schema/store/lifecycle/retrieval bundle。
- 有 retrieval explanation integration。
- 有 memory governance candidate models。
- 有 memory lifecycle dry-run apply。
- 有 memory viewer/control/export/delete/freeze flows。
- 有 Review Workspace integration。

当前记忆系统是“本地可审核 memory framework”，不是生产级长期记忆 runtime。

暂未达到：

- 没有 embedding。
- 没有向量检索。
- 没有真实 consolidation。
- 没有真实多轮记忆写入。
- 没有跨设备、账号、权限、加密、备份等生产基础。

### 23.6 主动消息

已经达到的程度：

- 有 proactive consent schema。
- 有 proactive policy gate。
- 有 quiet hours / frequency tests。
- 有 proactive review cards。
- demo 中有 proactive candidate。

当前主动行为仍是 review-only candidate，不会自动发给用户，也不会进入外部平台。

暂未达到：

- 没有 scheduler。
- 没有 queue。
- 没有 delivery。
- 没有平台 adapter。
- 没有自动 outreach。

### 23.7 语音、视频和 Live2D/avatar

已经达到的程度：

- 有 voice technology survey。
- 有 voice consent data model。
- 有 ASR/TTS latency benchmark planning。
- 有 avatar interaction survey。
- demo 中有 locked voice/avatar surface，明确说明未启用。

暂未达到：

- 没有 ASR/TTS runtime。
- 没有 voice cloning。
- 没有 Live2D runtime。
- 没有 camera/microphone。
- 没有视频通话模拟。
- 没有真人 likeness。

### 23.8 朋友圈/虚拟生活流

已经达到的程度：

- 有 role dynamic post schema。
- 有 virtual life engine text generator。
- 有 AIGC labeling metadata。
- 有 imagined/factual contamination tests。
- 有 life-stream review card。
- demo 中能看到文本生活流草稿。

暂未达到：

- 没有图片生成。
- 没有视频生成。
- 没有真实社交平台发布。
- 没有未标注 AIGC。

### 23.9 商业化思路

已经达到的程度：

- 有 M13 commercial positioning。
- 有 competitor framing。
- 有 trust/commercial positioning panel。
- 有 pricing hypotheses。
- 有 unacceptable monetization patterns。
- 有 readiness gaps。

当前商业化思路大致是：以文本 companion 为核心，围绕高质量 persona、可控记忆、长期陪伴、审查和导出控制、生活流和高级体验做订阅分层；但避免把依赖、危机、悲伤、亲密操控或“冒充真人”作为变现点。

暂未达到：

- 没有用户研究验证。
- 没有支付。
- 没有订阅系统。
- 没有真实定价实验。
- 没有上线计划或合规完成声明。

## 24. 当前验证状态

最近几个关键验证结果如下。

M40 review focused verification：

```powershell
$env:PYTHONPATH='src'; pytest tests\test_persona_source_evidence_matrix_payload.py tests\test_static_persona_source_evidence_matrix.py tests\test_persona_source_evidence_review_linkage.py tests\test_persona_source_evidence_responsive_hardening.py tests\test_text_first_web_demo_local_server.py tests\test_text_first_web_demo_static.py tests\test_text_first_web_demo_state_switching.py -q -o cache_dir=artifacts\t452_pytest_cache --basetemp=artifacts\t452_pytest_basetemp
```

结果：`35 passed`。

M41 review focused verification：

```powershell
$env:PYTHONPATH='src'; pytest tests\test_source_evidence_persona_proposal_payload.py tests\test_static_source_evidence_persona_proposal.py tests\test_source_evidence_persona_proposal_review_linkage.py tests\test_source_evidence_persona_proposal_responsive_hardening.py tests\test_text_first_web_demo_local_server.py tests\test_text_first_web_demo_static.py tests\test_text_first_web_demo_state_switching.py -q -o cache_dir=artifacts\t458_pytest_cache --basetemp=artifacts\t458_pytest_basetemp
```

结果：`33 passed`。

M42 review focused verification：

```powershell
$env:PYTHONPATH='src'; pytest tests\test_source_proposal_persona_draft_payload.py tests\test_static_source_proposal_persona_draft.py tests\test_source_proposal_persona_draft_review_linkage.py tests\test_source_proposal_persona_draft_responsive_hardening.py tests\test_text_first_web_demo_local_server.py tests\test_text_first_web_demo_static.py tests\test_text_first_web_demo_state_switching.py -q -o cache_dir=artifacts\t464_pytest_cache --basetemp=artifacts\t464_pytest_basetemp
```

结果：`33 passed`。

M43 review focused verification：

```powershell
$env:PYTHONPATH='src'; pytest tests\test_source_draft_apply_readiness_payload.py tests\test_static_source_draft_apply_readiness.py tests\test_source_draft_apply_readiness_review_linkage.py tests\test_source_draft_apply_readiness_responsive_hardening.py tests\test_text_first_web_demo_local_server.py tests\test_text_first_web_demo_static.py tests\test_text_first_web_demo_state_switching.py -q -o cache_dir=artifacts\t470_pytest_cache --basetemp=artifacts\t470_pytest_basetemp
```

结果：`33 passed`。

M43 额外验证：

```powershell
python -m py_compile src\practical_chat_agent\ui\text_first_web_demo_adapter.py
```

结果：通过。

```powershell
git diff --check
```

结果：通过，仅有 Windows CRLF 转换警告。

```powershell
node --check src\practical_chat_agent\ui\static\text_first_web_demo.js
```

结果：通过。

需要说明：M41-M43 的浏览器级布局 QA 未声称完成，因为这些轮次没有可调用的 in-app browser DOM inspection 工具。静态 CSS/JS/pytest 检查已覆盖对应选择器和安全边界，但这不等价于真实浏览器视觉验证。

## 25. 当前暂停点和未完成事项

当前完成点：

- M40 已完成 review，结论 `PASS_WITH_WARNINGS`。
- M41 已完成 review，结论 `PASS_WITH_WARNINGS`。
- M42 已完成 review，结论 `PASS_WITH_WARNINGS`。
- M43 已完成 review，结论 `PASS_WITH_WARNINGS`。
- M44 已完成 scope 草案和 T471 planning task package，但尚未开始实现。

当前未完成点：

- M44 的 `source_draft_apply_plan_preview` 尚未实现。
- M44 静态 UI、Review Workspace linkage、responsive hardening 和 milestone review 尚未开始。
- 当前仍没有真实 source ingestion、真实 persona apply 或真实 runtime mutation。

核心未完成能力：

- 没有真实私聊数据读取。
- 没有真实 persona distillation。
- 没有 provider/model 调用。
- 没有 embedding / vector retrieval。
- 没有 production memory runtime。
- 没有 platform adapter。
- 没有自动发送。
- 没有 voice/avatar runtime。
- 没有 payments/auth/account system。
- 没有合规完成或上线审批。

## 26. 总体评价

从 M12 到 M43/T470，本项目完成了一次清晰转型：从“能否接入微信类平台发消息”的技术风险探索，转成“能否做出一个透明、可控、可审核、可长期成长的 AI companion 产品”的系统化原型建设。

当前已经具备：

- 产品定位和商业假设。
- persona schema、compiler、version、growth、evolution、distillation workbench。
- memory schema、lifecycle、retrieval explanation、control flows。
- proactive consent 和 review-only candidate。
- virtual life-stream 文本草稿和 AIGC 标注边界。
- Review Workspace、manual apply preview、apply risk、controlled apply、audit manifest。
- integrated local web demo。
- source intake manifest。
- source evidence matrix。
- source-evidence-to-persona-proposal preview。
- source-proposal-to-persona-draft preview。
- source-draft-to-apply-readiness preview。

当前完成度可以概括为：

```text
已达到：
本地、合成、文本优先、可审核、可解释的 companion 产品原型骨架。

正在形成：
从用户描述/来源治理到 evidence、proposal、draft、apply-readiness 的人设塑造预览链路。

尚未达到：
真实用户数据、真实蒸馏、真实模型聊天、真实平台收发、自动发消息、
语音/avatar、生产商业化、生产合规和上线能力。
```

这个状态已经足够用于继续做产品评审、架构评审、安全边界评审和下一阶段 demo 硬化；但还不能被包装成可上线产品，也不能被描述为可替代真人聊天或可克隆真人的系统。
