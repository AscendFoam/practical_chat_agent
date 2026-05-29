# T231 WeCom Customer Service Inbound Contract Spike - 解释文档

## 一、这个任务在做什么（通俗解释）

到了 M12 阶段，项目已经做完了 T230 调研，结论是：**不能做个人微信自动化**，只能走企业微信（WeCom）的官方渠道。但具体怎么接，还需要验证。

T231 就是这个"验证的第一步"——它不是真的去连微信服务器，而是：

1. 按照企业微信客服的官方文档格式，**造一些假数据**（叫"合成 fixture"），模拟企业微信客服可能收到的消息
2. 写一个**纯本地的解析器**，把这些假数据转换成项目已有的统一格式（`InboundEvent`）
3. 写测试确保解析器的行为是正确的、可预测的
4. 写文档说明这个合约的设计、限制和未解决的问题

用一个比喻：这就像在正式铺设铁轨之前，先用木头做了一个铁轨模型，测试火车模型能不能在上面跑。木头铁轨不是真的铁轨，但它能验证设计是否合理。

## 二、任务实现详解

### 任务目标

证明企业微信客服的消息格式可以被"规范化"到项目已有的 `InboundEvent` 体系中，但不接入真实 API、不使用真实凭据、不读取任何私密数据。

### 任务流程

1. **阅读现有架构**：Worker 阅读了项目的基础连接器抽象（`InboundConnector`）、飞书连接器（`feishu_bot.py`）作为参考模式，以及 `InboundEvent`、`InboundConnectorResult` 等核心模型。

2. **查阅官方文档**：Worker 重新查阅了企业微信客服的官方 API 文档（消息接收和发送），确认了字段命名和消息结构。

3. **创建合成 fixture**：Worker 创建了 5 个 JSON fixture 文件，模拟 5 种场景：

   | Fixture | 场景 |
   |---------|------|
   | `inbound_text_message.json` | 正常的文本客服消息 |
   | `non_text_message.json` | 图片等非文本消息 |
   | `send_failure_event.json` | 发送失败的系统事件 |
   | `malformed_missing_identity.json` | 缺少必要字段的不合规消息 |
   | `personal_wechat_desktop_like.json` | 模拟个人微信/桌面自动化的消息（必须被拒绝）|

   所有 fixture 都只包含假的合成 ID（如 `customer_alias_001`、`kf_alias_support`），不包含任何真实数据。

4. **实现连接器**：创建了 `WeComCustomerServiceInboundConnector` 类，实现两个核心方法：

   - `can_handle_payload()`：判断一个消息是否是企业微信客服格式
   - `parse_inbound_payload()`：将企业微信客服消息转换为统一的 `InboundEvent`

   关键设计决策：
   - 文本消息映射为 `ContentType.TEXT`
   - 非文本消息（图片等）映射为 `ContentType.SYSTEM`（保守处理）
   - 发送失败事件也映射为系统事件（作为入站证据，不改变出站状态）
   - 个人微信/桌面自动化格式的消息直接被拒绝
   - 所有 ID 都是确定性的（用 SHA-256 哈希生成），不是随机的

5. **编写测试**：6 个测试覆盖了所有 fixture 场景，包括正常解析、非法输入拒绝、确定性验证（同一输入多次解析结果一致）。

6. **编写数据合约文档**：详细说明了设计选择、字段映射关系、限制和未解决的问题。

### 代码/配置变化

| 文件 | 变化 |
|------|------|
| `src/practical_chat_agent/connectors/inbound/wecom_customer_service.py` | 新建：连接器实现（约 254 行）|
| `src/practical_chat_agent/connectors/inbound/__init__.py` | 修改：添加 WeCom 连接器导出 |
| `tests/test_wecom_customer_service_inbound.py` | 新建：6 个测试 |
| `tests/fixtures/wecom_customer_service_inbound/*.json` | 新建：5 个合成 fixture |
| `docs/data_contracts/wecom_customer_service_inbound_contract.md` | 新建：数据合约文档 |
| `docs/worker_summary/T231_worker_summary.md` | 新建：Worker 总结 |
| `docs/07_handoff.md` | 修改：添加 T231 完成记录 |

### 对后续开发的意义

这个任务建立了 M12 的第一个"桥梁"——项目现在有了：

- **一个可测试的入站合约**：未来如果真的接入企业微信客服，解析器的基础已经就位
- **一套清晰的限制清单**：数据合约文档明确列出了所有未解决的问题（凭据管理、回调验证、加密解密、48 小时服务窗口、收件人映射等）
- **一个安全边界**：T232（出站适配器）仍然被阻止，直到这些问题被解决

对于项目整体来说，这意味着：
- 个人微信路线仍然被严格封死
- 企业微信客服是唯一被允许探索的官方路径
- 但即使走这条路径，下一步也必须是纯合成的出站合约设计，而非真实发送

## 三、为什么给出 PASS 的评审结论

### 没有阻塞性问题

1. **任务目标完全达成**：任务包要求实现本地合成入站合约，Worker 准确地实现了连接器、fixture、测试和数据合约文档。所有 5 个必需的 fixture 场景都被覆盖。

2. **没有违反禁止范围**：没有写实时回调路由、没有调 API、没有装 SDK、没有用真实凭据、没有读私密数据、没有修改任务板。所有文件都在允许列表内。

3. **没有伪实现**：连接器是真正的、确定性的解析器。输入一个 fixture，输出一个完全由输入决定的 `InboundEvent`。没有 mock、没有 stub、没有硬编码的假成功。

4. **没有破坏已有功能**：没有修改 `models.py`、出站适配器、发送闸门、CLI 命令或运行时服务。`__init__.py` 的变更是纯增量的——现有的飞书和 Telegram 连接器通过 `container.py` 直接导入，不受影响。

5. **文档没有把计划写成事实**：数据合约明确标注 "Status: worker draft for review"，清楚地列出了所有未解决的问题。没有声称"已经兼容真实企业微信"。

6. **测试质量良好**：6 个测试覆盖了任务包要求的所有场景，包括正确的字段映射验证、确定性 ID 验证、非法输入拒绝和个人微信消息拒绝。

### 非阻塞性观察

- 时间戳解析器在字段缺失时会静默回退到 1970 年（Unix 纪元），而非报错。对于合成场景可以接受，但未来真实适配器应要求有效时间戳。
- 只解析 `msg_list` 中的第一条消息，多条消息的 payload 会被静默截断。这符合当前一次解析返回一个事件的设计，但未来的批量处理需要额外设计。
- 有一些次要的测试覆盖空缺（时间戳边界情况、空文本内容等），但都在 spike 范围内可以接受。

总的来说，这是一个干净、诚实、范围精准的合约 spike 实现——它正确地验证了"企业微信客服消息可以被规范化"这个假设，同时清楚地标记了所有未解决的边界问题。
