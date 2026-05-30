# T233 WeCom Customer Service Provider Safety Gate - 解释文档

## 一、这个任务在做什么（通俗解释）

到了 M12 阶段，项目已经做完了两件事：

- **T230**：调研了各种微信接入方案，结论是"不能做个人微信自动化，只能走企业微信客服的官方渠道"
- **T231**：用假数据验证了企业微信客服的消息可以被解析成项目统一格式

但 T231 只解决了"收消息"的合约问题。在考虑"发消息"（出站）之前，还有一个关键问题：**企业微信客服有一系列官方限制**，比如：

- 客户发消息后，你只有 **48 小时** 的服务窗口来回复
- 在这个窗口内，你最多只能发 **5 条消息**
- 不能自动主动发消息，只能人工手动触发
- 不能通过消息的元数据偷偷塞入真实的 provider ID（如 `external_userid`、`access_token` 等）

T233 就是在出站链路上加一道"安全闸门"——在真正发送之前，检查这些限制条件是否满足。如果满足就放行（但"放行"不等于"已发送"，只是说"安全检查通过"），不满足就拦截。

用一个比喻：T233 就像机场安检。T231 是确认"你能听懂乘客在说什么"（入境语言检查），T233 是确认"乘客能不能登机"（出境安全检查）。安检通过不代表飞机已经起飞——那还需要后面的任务来实现。

## 二、任务实现详解

### 任务目标

实现一个纯本地的、确定性的企业微信客服出站安全闸门。这个闸门：

- 接收一个已经通过人工审批和通用发送闸门（`OutboundSendGate`）的出站请求
- 检查企业微信客服特有的限制条件
- 返回"允许"或"拦截"的决定
- **不准备实际的 API 负载、不调用任何 API、不读取凭据、不发送消息**

### 任务流程

1. **阅读现有架构**：Worker 阅读了 `OutboundSendGate`（通用发送闸门）和 `LocalFakeOutboundAdapter`（本地模拟适配器）作为参考模式，理解了 M11 阶段建立的出站安全链路。

2. **设计安全对象**：Worker 设计了 5 个核心对象：

   | 对象 | 作用 |
   |------|------|
   | `WeComCustomerServiceRecipient` | 收件人映射记录（contact_id → 企业微信客服别名）|
   | `WeComCustomerServiceSafetyConfig` | 安全配置（手动发送模式、kill switch、消息窗口限制等）|
   | `WeComCustomerServiceSafetyContext` | 安全上下文（当前时间、收件人映射表、已有审计记录）|
   | `WeComCustomerServiceSafetyDecision` | 安全决定（允许/拦截、原因码、审计记录）|
   | `WeComCustomerServiceSafetyGate` | 安全闸门（核心评估逻辑）|

3. **实现闸门逻辑**：`WeComCustomerServiceSafetyGate.evaluate()` 按顺序检查：

   - 请求是否可发送（`is_sendable()`）
   - 渠道是否为 `wechat`
   - 安全表面是否为 `wecom_customer_service`
   - 是否有 kill switch 启用
   - 元数据是否夹带了 provider ID/凭据
   - 收件人映射是否存在
   - 收件人是否允许手动发送
   - 服务窗口是否有效
   - 消息窗口配额是否用尽

   所有检查通过才返回 `allowed`，任何一项失败返回 `blocked`。

4. **编写测试**：25 个测试覆盖了任务包要求的所有 10 个场景，包括正常放行、各种拦截条件、映射输入与模型输入一致性、输入不被修改等。

5. **编写文档**：数据合约文档详细说明了设计选择、输入输出格式、阻塞规则、放行语义、审计行为和未解决的问题。

### 代码/配置变化

| 文件 | 变化 |
|------|------|
| `src/practical_chat_agent/services/wecom_customer_service_safety.py` | 新建：安全闸门实现（约 324 行）|
| `tests/test_wecom_customer_service_safety_gate.py` | 新建：25 个测试 |
| `docs/data_contracts/wecom_customer_service_safety_contract.md` | 新建：数据合约文档 |
| `docs/tasks/M12_wechat_adapter/T232_wechat_outbound_adapter.md` | 修改：T232 继续保持 blocked 状态 |
| `docs/worker_summary/T233_worker_summary.md` | 新建：Worker 总结 |
| `docs/07_handoff.md` | 修改：添加 T233 完成记录 |

### 对后续开发的意义

T233 建立了 M12 出站链路上的第一道安全防线：

- **确定性的安全边界**：未来的出站适配器（T232）必须通过 T233 的安全闸门才能执行任何操作
- **明确的限制清单**：服务窗口、消息配额、手动发送模式、kill switch、元数据走私检测——所有企业微信客服的出站限制都在这里集中管理
- **审计追踪**：每个决定都带有审计记录，明确标记 `provider_eligible_not_delivery`（安全放行不等于已发送）
- **T232 的前提条件**：T232 现在可以基于 T233 的 `WeComCustomerServiceSafetyDecision` 来设计干跑出站负载准备，不需要关心安全逻辑

对于项目整体来说：
- 出站安全链路现在是：`人工审批 → OutboundSendGate（通用安全）→ WeComCustomerServiceSafetyGate（平台特定安全）→ T232 出站适配器（干跑负载准备）`
- 每一层都是独立的、可测试的、确定性的
- 没有任何一层实际发送消息或调用外部 API

## 三、为什么给出 PASS 的评审结论

### 没有阻塞性问题

1. **任务目标完全达成**：任务包要求实现一个纯本地的、确定性的企业微信客服安全闸门，Worker 准确地实现了所有要求的安全对象、阻塞规则、放行语义、审计记录和测试。所有 10 个必需的测试场景都被覆盖。

2. **没有违反禁止范围**：没有实现 WeCom 出站适配器、没有准备 API 负载、没有调 API、没有读凭据、没有注册回调、没有轮询/同步、没有加调度器、没有加 CLI 命令、没有修改任务板。所有文件都在允许列表内。

3. **没有伪实现**：安全闸门是真正的、确定性的评估器。输入一个请求和上下文，输出完全由输入决定的 `WeComCustomerServiceSafetyDecision`。每个阻塞原因码都对应明确的输入条件检查。没有 mock、没有 stub、没有硬编码的假成功。

4. **没有破坏已有功能**：没有修改 `models.py`、`OutboundSendGate`、入站连接器、出站适配器、CLI 命令或运行时服务。61 个联合测试（T233 + 出站 schema + 发送闸门）全部通过。

5. **文档没有把计划写成事实**：数据合约明确标注 "Status: worker draft for review"，清楚地列出了所有未解决的问题。`allowed` 语义被明确限定为"provider eligibility only"，不等同于已发送、不等同于 API 兼容、不等同于凭据可用。

6. **测试质量良好**：25 个测试覆盖了所有必需场景，包括正确的字段映射验证、多种阻塞条件、映射/模型输入一致性、输入不可变性、元数据走私检测等。

### 非阻塞性观察

- 收件人映射缺失时提前返回，不会报告所有适用的阻塞原因。这是一个可接受的短路径设计，但与 `OutboundSendGate` 的全累积模式不同。
- 安全表面的配置验证只在 `evaluate()` 时检查，不在配置构造时检查。
- 元数据走私检测与 `models.py` 中已有的 Pydantic 验证有部分重叠（`open_id`、`access_token` 已经在模型层被拦截），但对于映射输入仍然有保护作用。
- `WECom_CUSTOMER_SERVICE_SURFACE` 常量命名有轻微的大小写不一致（`WECom` 而非 `WECOM`），纯粹是外观问题。
- 有一些次要的测试覆盖空缺（收件人字段验证、上下文键一致性、非默认配置值等），但都在任务范围内可以接受。

总的来说，这是一个干净、诚实、范围精准的安全闸门实现——它正确地在企业微信客服出站链路上建立了确定性的安全边界，同时清楚地标记了所有未解决的边界问题，并为 T232 的干跑出站负载准备任务提供了明确的前提条件。
