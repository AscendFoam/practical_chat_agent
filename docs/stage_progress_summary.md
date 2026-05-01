# 项目阶段性进展总结

更新日期：2026-04-20

## 1. 文档目的

本文档用于记录 `practical_chat_agent` 从项目启动到当前阶段的实际落地情况，回答三个问题：

1. 已经做了哪些工作。
2. 这些工作对应到 `engineering_experiment_plan.md` 的哪个阶段。
3. 接下来最适合继续推进哪些方向。

本文档是阶段总结，不替代总实验方案。总方案仍以 [engineering_experiment_plan.md](/D:/Codes/Social/practical_chat_agent/docs/engineering_experiment_plan.md) 为准。

## 2. 当前总体判断

截至目前，项目呈现出一个比较清晰的状态：

- `P0 基础框架` 已完成，并且已经不是纯骨架，具备可运行的 CLI、配置、仓储、运行时与事件总线。
- `P1 聊天采集 MVP` 基本完成，且已经覆盖了两类接入方式：官方平台 webhook 类接入，以及桌面 UI/OCR 类接入。
- `P6 会议转写 MVP` 与 `P7 会议助手 MVP` 推进最快，已经明显超出“只做转写演示”的程度，形成了可调试、可落库、可导出、可回放、可在 UI 中使用的子系统。
- `P2 聊天分析与建议`、`P3 长期记忆`、`P4 自定义 chat-agent` 目前属于“基础能力已就位，但尚未打通完整产品链路”的状态。
- `P5 动态内容生成` 仍主要停留在架构设想与数据模型边界层面，尚未进入真正实现阶段。

如果用一句话概括当前项目状态：

这是一个“底层框架已经成形、聊天接入已经打开、会议子系统已经先跑通，但聊天智能体中间层仍需补齐”的工程化原型。

## 3. 阶段进展总览

| 计划阶段 | 当前状态 | 简述 |
| --- | --- | --- |
| P0 基础框架 | 已完成 | 统一模型、MySQL、仓储层、AgentRuntime、CLI、容器装配已建立 |
| P1 聊天采集 MVP | 基本完成 | Telegram/飞书入站连接器、payload 回放、微信桌面扫描/OCR 已落地 |
| P2 聊天分析与建议 MVP | 部分完成 | 运行时可生成最小回复草稿，但专门的聊天建议链路仍待加强 |
| P3 长期记忆 MVP | 部分完成 | MemoryFact 模型与基础写入/读取已具备，记忆抽取与固化流程未完成 |
| P4 自定义 chat-agent MVP | 部分完成 | AgentProfile、创建命令、运行时骨架已就位，主动触发与投递尚未落地 |
| P5 动态内容 MVP | 未开始 | 暂无动态草稿生成、内容日历、图片草稿链路 |
| P6 会议转写 MVP | 已完成且增强 | Windows loopback/microphone、转写、调试、落库、回放都已具备 |
| P7 会议助手 MVP | 已完成且增强 | 实时字幕小窗、AI 建议、纪要导出、版本历史与 diff 已具备 |
| P8 自主代理增强 | 未开始 | Scheduler、PolicyEngine、DeliveryConnector 仍缺核心实现 |

## 4. 已完成工作分阶段记录

### 4.1 阶段一：基础工程框架搭建

这一阶段对应计划中的 `P0`，核心目标是先把整个系统的“公共地基”搭起来，而不是一开始就堆功能脚本。

已完成内容：

- 建立了统一核心数据模型，覆盖入站事件、桌面扫描结果、OCR 结果、会议会话、会议片段、会议纪要、AgentProfile、MemoryFact、ActionPlan、AgentTurnResult 等对象。
- 建立了统一枚举体系，覆盖平台类型、内容类型、消息方向、会议音频来源、纪要模板、安全模式、人格类型等。
- 建立了 MySQL 配置与连接层，支持通过 `.env` 注入数据库参数。
- 建立了 MySQL schema 与 SQLAlchemy models，当前已覆盖：
  - `agents`
  - `agent_profiles`
  - `events`
  - `memories`
  - `audit_logs`
  - `meeting_sessions`
  - `meeting_segments`
  - `meeting_minutes`
- 建立了仓储层抽象与 MySQL 实现，包含事件、Agent、记忆、审计、会议数据等仓储。
- 建立了最小同步事件总线 `InMemoryEventBus`。
- 建立了最小 `AgentRuntime`，能够完成：
  - 入站事件持久化
  - 最近上下文读取
  - 简单记忆写入
  - 回复草稿生成
  - 审计日志写入
- 建立了容器装配层 `AppContainer`，把配置、仓储、连接器、服务、运行时统一装配。
- 建立了 CLI 入口，便于后续所有阶段持续扩展。

这一阶段的意义：

- 项目已经不是“零散脚本集合”，而是进入了“有明确边界和可复用模块”的工程状态。
- 后续聊天、会议、persona、内容生成等能力都可以复用同一套底层结构。

### 4.2 阶段二：入站连接器与 payload 调试链路

这一阶段对应 `P1` 的官方平台接入部分。

已完成内容：

- 实现了 `TelegramBotConnector` 的官方平台空实现与最小 payload 解析。
- 实现了 `FeishuBotConnector` 的官方平台空实现与最小 payload 解析。
- 建立了 `InboundEventService`，把连接器 payload 标准化后送入运行时。
- 将早期的 `demo-turn` 推进为真实的入站接入链路，不再只是手工构造一个 turn。
- 增强了 `replay-payload-dir`：
  - 支持从目录批量读取 JSON payload
  - 支持每个文件自行指定 connector
  - 支持混合目录批量回放
- 提供了官方平台示例 payload，便于本地 webhook 风格调试。

这一阶段的意义：

- 官方平台接入方式已经具备最小闭环。
- 后续若继续做飞书/Telegram 的主动聊天、草稿建议、审计回放，可以直接建立在这条链路之上。

### 4.3 阶段三：微信桌面扫描与 OCR 兜底

这一阶段对应 `P1` 的桌面连接器部分，并且已经明显超出“只做窗口探测”的范围。

已完成内容：

- 建立了 `WeChatDesktopConnector` 桌面连接器。
- 实现了 Windows 窗口探测与前台窗口识别。
- 接入 `pywinauto`，可以尝试从当前可见 WeChat 窗口读取 accessible text。
- 在 accessible text 不足时，提供截图 + OCR 兜底路径。
- 封装了 `GlmOcrService`，对接 GLM OCR 布局解析能力。
- `desktop-scan-preview` 已支持：
  - 预览桌面扫描结果
  - `--force-ocr`
  - `--save-capture`
- OCR 解析已经细化到更接近聊天 UI 的结构化抽取，当前可识别：
  - 发送者
  - 时间戳
  - 左右气泡侧
  - 进出消息
  - 引用回复
  - 系统消息
  - 撤回提示

当前判断：

- 微信桌面扫描已经具备“当前会话可见消息读取”的第一版可用能力。
- 但它仍是桌面 UI 自动化路径，稳定性会受到微信版本、窗口结构、分辨率和字体布局影响。

### 4.4 阶段四：聊天 runtime 与最小 agent 骨架

这一阶段主要对应 `P2`、`P3`、`P4` 的共同基础部分。

已完成内容：

- 实现了 `create-agent` 命令，可以创建最小 `AgentProfile`。
- `AgentProfile` 已具备以下基础字段：
  - `agent_id`
  - `display_name`
  - `persona_type`
  - `system_identity`
  - `public_disclosure`
  - `core_traits`
  - `speech_style`
  - `interests`
  - `relationship_mode`
  - `safety_mode`
  - `do_not_do`
- `MemoryFact` 与基础记忆仓储已经建立。
- `AgentRuntime` 能基于 recent events 与 memory hits 生成最小回复草稿。
- 会议转写片段也可以回放进 runtime，用于后续统一“会议信息进入 agent 上下文”。

当前判断：

- 项目已经拥有“agent 的最小实体”和“最小对话循环”。
- 但目前还没有真正的：
  - ContextAssembler
  - 记忆抽取/固化流水线
  - 主动触发器
  - 审批式发送执行器
  - 正式 DeliveryConnector

也就是说：

- `chat-agent` 的壳已经搭好。
- `chat-agent` 的“思考层”和“行为层”还没补完整。

### 4.5 阶段五：腾讯会议转写链路

这一阶段对应 `P6`，但实际完成度高于原始计划。

已完成内容：

- 建立了 `TencentMeetingDesktopConnector`。
- 打通了 `WindowsAudioCaptureService`，支持两条采集分支：
  - 系统输出 loopback
  - 麦克风输入 microphone
- 采集链路支持 chunk 化 WAV 保存。
- 接入了音频转写服务 `ZhipuAudioTranscriptionService`。
- 转写链路具备较强的现场调试信息，包含：
  - RMS
  - 峰值
  - 时长
  - 静音判断
  - 保存路径
  - retry 次数与策略
- 为 microphone 模式做了多轮增强：
  - 前置增益
  - 峰值归一化
  - 更稳的静音门限
  - 高通/去直流
  - 静音头尾裁剪
  - 压缩与限幅
- 为 empty chunk 增加了重试策略：
  - 不同 prompt 重试
  - 更长 chunk 重试
  - 跨 3 个 chunk 合并重试
  - 保留上一个 chunk 文本作为上下文 prompt
- 会议数据已落库为：
  - `meeting_sessions`
  - `meeting_segments`

这一阶段的意义：

- 会议转写已经不是单次 demo，而是形成了完整的“采集 -> 转写 -> 落库 -> 查询/回放”的工程链路。

### 4.6 阶段六：会议助手、纪要与导出体系

这一阶段对应 `P7`，并且是当前项目最完整的业务子系统。

已完成内容：

- 实现了 `MeetingAssistantService`：
  - 可走 OpenAI-compatible 远端模型
  - 不可用时自动退回 heuristic fallback
- 实现了 `MeetingMinutesService` 与 `MeetingMinutesExportService`：
  - 支持启发式纪要生成
  - 支持 LLM 重写为更像真人秘书整理的正式纪要
- 已支持多种纪要模板：
  - `brief`
  - `standard`
  - `full`
- 已支持纪要落库存档与版本历史。
- 已支持会议数据查询与回放命令：
  - `meeting-session-list`
  - `meeting-session-show`
  - `meeting-session-tail`
  - `meeting-session-replay`
  - `meeting-session-export`
  - `meeting-session-minutes-history`
  - `meeting-session-minutes-show`
  - `meeting-session-minutes-diff`
- 已支持按时间范围和最近 N 条做 replay/export。
- 已支持导出 Markdown 纪要，并按标准模板分区：
  - 背景
  - 结论
  - action items
  - 风险
  - 原始摘录

当前判断：

- 会议纪要链路已经具备“版本化文档产品”的雏形。
- 会议子系统目前已经包含采集、分析、展示、导出、归档、历史对比等多个环节。

### 4.7 阶段七：会议实时 UI 小窗

这是当前最强的演示层成果。

已完成内容：

- 建立了 `MeetingLiveCaptionWindow` 半透明小窗。
- 小窗支持：
  - 实时字幕条
  - AI 辅助建议区
  - Summary
  - Suggested Reply
  - Key Points
  - Follow-up Questions
  - Action Items
  - Minutes Export 状态
- 小窗支持：
  - 音频源切换
  - 设备名输入
  - 是否保存 WAV
  - 透明度调整
  - AI 建议刷新
  - 纪要导出
- 纪要导出已支持：
  - 模板选择
  - 导出目录选择
- 小窗内已经支持纪要历史能力：
  - 查看最新纪要
  - 对比上一个版本
  - 完整纪要历史面板
  - 任意两版 diff

这一阶段的意义：

- 项目已经拥有一个“看得见、能操作、能导出结果”的前台演示面。
- 这对于后续验证会议侧产品价值非常重要。

## 5. 当前缺口与未完成事项

虽然项目已经做了很多，但如果严格对照总方案，当前仍有几类重要缺口。

### 5.1 聊天智能中间层还没真正补齐

目前聊天侧更多是“接入 + 最小 runtime”，还没有完整做到：

- 聊天上下文编排
- 结构化偏好抽取
- 长期关系状态更新
- 候选回复排序
- 对建议质量的可解释调试

### 5.2 主动行为层还未真正开始

当前没有完整落地以下能力：

- DeliveryConnector
- 审批式发送
- 定时触发与 silence trigger
- 主动聊天 Planner
- PolicyEngine
- 限频和越界控制执行链

### 5.3 Persona 与长期记忆还不够“像一个持续存在的角色”

当前已有 Persona 数据结构，但还没有：

- persona prompt 编译器
- relationship state machine
- memory consolidation
- 用户偏好与事件抽取
- 基于记忆的连续会话体验

### 5.4 动态内容子系统尚未开始

计划中的“朋友圈/动态式内容生成”目前基本未进入实现阶段，仍停留在方案层。

### 5.5 工程完备性仍需补强

当前还缺少几类后续非常需要的基础设施：

- migration 工具链
- 系统化自动化测试
- 更清晰的运行日志与指标
- 更正式的错误恢复与告警机制

## 6. 结合总方案，接下来最适合推进的方向

由于腾讯会议侧已经先跑得比较深，而用户也明确表示会议侧可以暂时告一段落，因此接下来最适合推进的方向，不是继续堆会议能力，而是回到总方案的主干，把聊天智能体中间层补起来。

### 6.1 第一优先级：补 P2 + P3，做“聊天建议 + 记忆”中间层

这是我认为当前最值得推进的方向。

原因：

- 当前已经有官方平台入站连接器、桌面扫描连接器、统一事件模型和最小 runtime。
- 也就是说，“输入已经有了”。
- 现在最缺的是把输入变成“有质量的理解、建议、记忆”。

建议具体落地内容：

1. 新建 `chat_analysis` / `context_assembler` 相关服务。
2. 从 recent events 中抽取：
   - 摘要
   - 待办
   - 用户偏好
   - 关系线索
   - 风险信号
3. 将抽取结果写入 `MemoryFact`，并区分短期/长期。
4. 在 runtime 中引入真正的上下文拼装，而不是只统计 recent_events_count 和 memory_hits_count。
5. 输出更像真实产品的建议结果：
   - 一句话建议
   - 长回复草稿
   - 不回复建议
   - 风险提示

推进完这一层后，项目会从“能接消息”升级为“能理解对话”。

### 6.2 第二优先级：补 P4，做真正可用的自定义 chat-agent MVP

会议侧已经证明了“小窗 + AI 辅助”这种产品形态可行；聊天侧下一步应该把 persona 做成真正可用的 agent。

建议具体落地内容：

1. 扩展 `AgentProfile`：
   - persona prompt 模板
   - 语言风格细粒度参数
   - 主动行为边界
   - 长期目标
2. 引入 conversation/session 视角，而不只是单事件处理。
3. 做一个 `agent session debug` CLI 或面板，方便查看：
   - 当前 persona
   - 取到的记忆
   - 当前建议
   - 不回复原因
4. 支持半自动模式：
   - 先生成草稿
   - 用户确认后再发送

这一阶段不要急着直接做“全自动主动聊天”，而是先把“持续对话中的 persona 一致性”做出来。

### 6.3 第三优先级：补 DeliveryConnector 和受控发送链路

如果没有发送链路，agent 永远只是分析器；但如果过早做自动发送，又容易越界。

所以更合理的顺序是：

1. 先做 `DeliveryConnector` 抽象。
2. 优先接一个最安全的平台发送器：
   - Telegram bot 发送
   - Feishu bot 发送
3. 默认启用“草稿模式 / 审批模式”。
4. 再逐步增加：
   - 限频
   - quiet hours
   - 审计记录
   - deny list / do_not_do enforcement

这一步完成后，P4 才算真正从“会想”走到“能行动”。

### 6.4 第四优先级：再进入 P5 动态内容子系统

动态内容生成应该排在聊天记忆和行为层之后，而不是之前。

原因：

- 动态内容对 persona 一致性要求更高。
- 如果没有成熟的 persona、memory、policy，动态内容会显得很空，也容易漂移。

更合理的推进顺序是：

1. 先有 persona
2. 再有长期记忆
3. 再有内容规划器
4. 最后才有图文草稿与审批发布

### 6.5 并行建议：补工程硬化层

无论主线选择哪一条，建议都并行补一些工程能力：

- 引入 migration 管理，而不只是 `create_schema`
- 为关键服务补最小单元测试和样例回放测试
- 给入站、扫描、会议、纪要导出补结构化日志
- 补一个“系统状态总览”命令，便于查看当前配置和组件 availability

## 7. 推荐的下一阶段执行顺序

如果目标是尽快把项目从“多个功能点”推进成“一个真正开始像产品的系统”，我建议按下面顺序走。

### 路线 A：优先补聊天智能体主线

1. 做聊天建议与上下文编排。
2. 做长期记忆抽取与固化。
3. 做 persona 一致性的 chat-agent MVP。
4. 做受控发送链路。

适合原因：

- 和总方案主线最一致。
- 可以平衡当前“会议侧很强、聊天侧偏薄”的结构。

### 路线 B：优先把聊天侧做成一个闭环 demo

1. 选择一个官方平台作为主演示平台，优先推荐 Telegram。
2. 打通入站 -> 建议 -> 草稿发送。
3. 接入 persona 与 memory。
4. 再做主动触发。

适合原因：

- 更容易快速做出“一个 agent 真的在聊天”的演示闭环。

### 当前推荐

当前最推荐：

- 以 `Telegram / Feishu 官方连接器 + 聊天分析/记忆 + 受控草稿发送` 为下一主线。

原因是：

- 官方平台链路更稳。
- 可以更快验证 chat-agent 主线价值。
- 也最符合总方案中 `P2 -> P3 -> P4` 的推进逻辑。

## 8. 结论

截至目前，项目已经完成了从“工程底座”到“多源接入”再到“会议子系统可用化”的重要阶段。

最值得肯定的部分有两点：

1. 底层框架已经建立，后续不是推倒重来，而是继续叠加能力。
2. 腾讯会议子系统已经形成了一个相对完整的可演示闭环，为项目证明了“统一事件模型 + runtime + UI + 导出”的路线是可行的。

接下来最适合做的，不是继续把会议侧做得更深，而是回到总方案主干，优先把聊天分析、长期记忆和自定义 chat-agent 中间层补起来。这样整个项目才会从“若干强功能模块”进一步升级为“统一的智能社交代理平台”。
