# T232 WeCom Customer Service Dry-Run Outbound Adapter - 解释文档

## 一、这个任务在做什么（通俗解释）

到了 M12 阶段，项目已经完成了三件事：

- **T230**：调研了微信接入方案，决定走企业微信客服官方渠道
- **T231**：用假数据验证了企业微信客服的消息可以被解析进来（入站方向）
- **T233**：在出站方向上加了一道安全闸门，检查"企业微信客服允不允许这条消息发出去"

T233 的安全闸门只回答"允许/不允许"，但它不回答"如果允许，实际要发给企业微信 API 的消息长什么样"。T232 就是补上这一步——在安全闸门放行之后，把出站请求组装成一个"演习用的消息包裹"（dry-run payload）。

用一个比喻来串起整个出站链路：

1. **人工审批**：你作为用户同意发这条消息
2. **通用安检（T221 OutboundSendGate）**：检查时间、频率、内容等通用规则
3. **平台安检（T233 SafetyGate）**：检查企业微信特有的限制（48小时窗口、5条上限、禁止主动发等）
4. **打包行李（T232 Dry-Run Adapter）**：如果安检全部通过，把消息装进"演习用的包裹"，贴上别名标签
5. **真正登机**：未来任务，T232 不做

T232 的"演习包裹"有几个关键特点：

- 只在内存里组装，**不调用任何外部 API**
- 只用别名（如 `recipient_alias_synthetic`），**不用真实的 provider ID**
- 包裹上写着 `dry_run: true`，明确标记"这只是演习"
- 原始请求中的 metadata 不会被复制到包裹里（防止夹带私货）

## 二、任务实现详解

### 任务目标

实现一个纯本地的、确定性的企业微信客服出站"干跑"适配器。这个适配器：

- 接收一个已经通过人工审批和通用发送闸门的出站请求
- 接收一个 T233 安全闸门返回的"允许"决定
- 把两者组合起来，组装一个演习用的消息包裹
- 返回"干跑就绪"或"被拦截"的结果
- **不调用任何 API、不读取凭据、不发送消息、不注册回调、不轮询同步**

### 任务流程

1. **阅读现有架构**：Worker 阅读了 `LocalFakeOutboundAdapter`（T222 本地模拟适配器）、`FeishuSandboxOutboundAdapter`（T223 飞书沙箱适配器）和 T233 安全闸门作为参考模式，理解了出站链路上各层的职责边界。

2. **设计核心对象**：Worker 设计了 3 个核心对象：

   | 对象 | 作用 |
   |------|------|
   | `WeComCustomerServiceDryRunConfig` | 干跑配置（强制 `dry_run_only=True`）|
   | `WeComCustomerServiceDryRunResult` | 干跑结果（状态、别名、审计记录、演习用包裹）|
   | `WeComCustomerServiceDryRunOutboundAdapter` | 干跑适配器（核心逻辑）|

3. **实现适配器逻辑**：`WeComCustomerServiceDryRunOutboundAdapter.prepare_dry_run()` 按顺序检查：

   - 输入是否是 `CandidateAction`（不允许直接用候选动作绕过）
   - 请求是否可解析为有效的 `OutboundMessageRequest`
   - 请求是否可发送（`is_sendable()`）
   - 渠道是否为 `wechat`
   - 安全决定是否存在
   - 安全决定是否可解析
   - 安全决定是否为 `allowed`
   - 安全决定的身份信息是否与请求匹配（request_id、contact_id、user_id）
   - 安全决定是否包含 T233 边界审计标记
   - 安全决定是否包含所有必需的别名

   所有检查通过后，构建一个包含别名、草稿文本、安全摘要和来源上下文的演习用包裹。

4. **编写测试**：23 个测试覆盖了任务包要求的所有 15 个场景，包括正常放行、各种拦截条件、映射输入与模型输入一致性、metadata 不被复制、输入不被修改、无 transport/send/deliver 接口等。

5. **编写文档**：数据合约文档详细说明了验证规则、干跑包裹结构、审计行为和未解决的问题。

### 代码/配置变化

| 文件 | 变化 |
|------|------|
| `src/practical_chat_agent/services/wecom_customer_service_outbound_adapter.py` | 新建：干跑适配器实现（约 354 行）|
| `tests/test_wecom_customer_service_outbound_adapter.py` | 新建：23 个测试 |
| `docs/data_contracts/wecom_customer_service_outbound_contract.md` | 新建：数据合约文档 |
| `docs/worker_summary/T232_worker_summary.md` | 新建：Worker 总结 |
| `docs/07_handoff.md` | 修改：添加 T232 完成记录 |

### 对后续开发的意义

T232 建立了 M12 出站链路上的"干跑负载准备"边界：

- **确定性的包裹组装**：未来的真正出站适配器可以基于 T232 的包裹结构来设计实际的 API 请求格式，但 T232 本身不承诺与任何官方 API 兼容
- **明确的安全依赖**：T232 必须消费一个 T233 的 `allowed` 安全决定，不能绕过安全闸门自行判断
- **严格的输入隔离**：T232 不复制请求的 metadata、不读取凭据、不暴露任何 transport/send/deliver 接口
- **M12 的最后一个实现任务**：T232 完成后，M12 的所有任务（T230 调研、T231 入站合约、T233 安全闸门、T232 干跑适配器）都已完成

对于项目整体来说：
- 出站安全链路现在是：`人工审批 → OutboundSendGate（通用安全）→ WeComCustomerServiceSafetyGate（平台安全）→ WeComCustomerServiceDryRunOutboundAdapter（干跑负载准备）`
- 每一层都是独立的、可测试的、确定性的
- 没有任何一层实际发送消息或调用外部 API
- M12 可以考虑做里程碑级别的评审和关闸

## 三、为什么给出 PASS 的评审结论

### 没有阻塞性问题

1. **任务目标完全达成**：任务包要求实现一个纯本地的、确定性的企业微信客服干跑出站适配器，Worker 准确地实现了所有要求的配置对象、结果对象、验证规则、包裹结构、审计行为和测试。所有 15 个必需的测试场景都被覆盖（实际上 Worker 还多写了一个 T233 边界审计缺失的测试）。

2. **没有违反禁止范围**：没有调用 WeCom/WeChat/Tencent API、没有加载凭据、没有添加 transport、没有注册回调、没有轮询/同步、没有加调度器/后台任务、没有加 CLI 命令、没有修改任务板。所有文件都在允许列表内。

3. **没有伪实现**：适配器是真正的、确定性的包裹组装器。输入一个请求和安全决定，输出完全由输入决定的 `WeComCustomerServiceDryRunResult`。每个拦截状态都对应明确的输入条件检查。没有 mock、没有 stub、没有硬编码的假成功。`wecom_dry_run_ready` 结果的 `delivered` 字段始终为 `False`，审计记录明确标记 `wecom_dry_run_only` 和 `no_provider_delivery`。

4. **没有破坏已有功能**：没有修改 `models.py`、`OutboundSendGate`、T233 安全闸门、入站连接器、出站适配器、CLI 命令或运行时服务。84 个联合测试（T232 + T233 + 出站 schema + 发送闸门）全部通过。

5. **文档没有把计划写成事实**：数据合约明确标注 "Status: worker draft for review"，清楚地列出了所有未解决的问题。干跑包裹被明确限定为"synthetic and review-safe"，不等于官方 API 请求格式。

6. **测试质量良好**：23 个测试覆盖了所有必需场景，包括正确的包裹结构验证、多种拦截条件、映射/模型输入一致性、输入不可变性、metadata 不被复制、无 transport 接口等。

### 非阻塞性观察

- 候选动作检测逻辑与 `LocalFakeOutboundAdapter` 和 `FeishuSandboxOutboundAdapter` 重复，未来可提取为共享工具函数。
- 安全决定的映射转换使用 dataclass 构造而非 Pydantic 验证，错误信息不够结构化，但在 `TypeError/ValueError` 的捕获范围内是正确的。
- `_build_payload` 中硬编码了 `"msg_type": "text"`，对于当前干跑范围是正确的，但未来如果支持多媒体消息需要扩展。
- 适配器引用了 `WECom_CUSTOMER_SERVICE_SURFACE` 常量作为默认值，但在 `_build_payload` 中也用了字符串字面量，存在轻微的不一致。
- 有一些次要的测试覆盖空缺（空配置表面、错误类型映射、空审计列表、非默认配置值等），但都在任务范围内可以接受。

总的来说，这是一个干净、诚实、范围精准的干跑适配器实现——它正确地在企业微信客服出站链路上建立了确定性的负载准备边界，严格依赖 T233 安全闸门的放行决定，清楚地标记了所有未解决的边界问题，并为 M12 的里程碑评审提供了完整的实现基础。
