**改了什么**

- 新增 [feishu_outbound_adapter.py](/D:/Codes/Social/practical_chat_agent/src/practical_chat_agent/services/feishu_outbound_adapter.py:26)，实现 `FeishuSandboxRecipient`、`FeishuSandboxAdapterConfig`、`FeishuSandboxTransportResponse`、`FeishuSandboxDeliveryResult`、`FeishuSandboxOutboundAdapter`。它只接受已 `is_sendable()` 的 `OutboundMessageRequest`，拒绝 `CandidateAction`/candidate-shaped mapping，要求 `channel_preference=="feishu"`，要求显式 `contact_id -> open_id/chat_id` recipient mapping，默认只做 dry-run，只有显式关闭 dry-run 且注入 fake transport 时才会进入 sandbox send 路径。
- 在 [models.py](/D:/Codes/Social/practical_chat_agent/src/practical_chat_agent/core/models.py:864) 扩展了 outbound payload forbidden metadata，新增拦截 `open_id`、`chat_id`、`receive_id`、`receive_id_type`、`feishu_open_id`、`feishu_chat_id`，防止把 Feishu recipient target 从 payload metadata 偷渡进 adapter。
- 新增 [test_feishu_outbound_adapter.py](/D:/Codes/Social/practical_chat_agent/tests/test_feishu_outbound_adapter.py:138)，覆盖 non-sendable 阻断、`CandidateAction` model/mapping 拒绝、缺失 recipient mapping、错误 channel、dry-run payload 生成、fake transport 调用、transport failure、`existing_audit` 保留、payload 只使用 approved draft text、以及 metadata forbidden-key 边界。
- 补强了 [test_outbound_fake_adapter.py](/D:/Codes/Social/practical_chat_agent/tests/test_outbound_fake_adapter.py:100) 的 T222 hardening：`FakeOutboundAdapterConfig` 参数校验、`existing_audit` 保留、preview exact-boundary、不超过 3 字符时返回纯 `.` 截断行为。
- 更新了 [outbound_send_gate_contract.md](/D:/Codes/Social/practical_chat_agent/docs/data_contracts/outbound_send_gate_contract.md:314) 和 [07_handoff.md](/D:/Codes/Social/practical_chat_agent/docs/07_handoff.md:3720)，明确 T223 只是 Feishu sandbox payload/result boundary，不声明 production Feishu delivery；没有更新 `docs/04_task_board.md`。

**如何验证**

- 先按 TDD 补测试并先跑红：首次运行 `pytest tests/test_outbound_message_request_schema.py tests/test_outbound_send_gate.py tests/test_outbound_fake_adapter.py tests/test_feishu_outbound_adapter.py ...` 因 `practical_chat_agent.services.feishu_outbound_adapter` 不存在而失败。
- `python -m py_compile src/practical_chat_agent/core/models.py src/practical_chat_agent/services/outbound_send_gate.py src/practical_chat_agent/services/outbound_fake_adapter.py src/practical_chat_agent/services/feishu_outbound_adapter.py`
- `pytest tests/test_outbound_message_request_schema.py tests/test_outbound_send_gate.py tests/test_outbound_fake_adapter.py tests/test_feishu_outbound_adapter.py -q -o cache_dir=artifacts\t223_pytest_cache --basetemp=artifacts\t223_pytest_basetemp` -> `65 passed`
- `pytest tests/ -q -o cache_dir=artifacts\t223_pytest_cache --basetemp=artifacts\t223_pytest_basetemp` -> `845 passed`
- 所有 pytest 都使用了 workspace-local `TEMP/TMP=artifacts\t223_pytest_tmp`。

**剩余风险**

- T223 只证明 Feishu sandbox payload preparation 和 injected fake transport 边界，不代表 production Feishu API 兼容性、ack 语义、重试、恢复逻辑已经存在。
- recipient mapping 目前只是 adapter config 里的显式 `contact_id` 查找；后续 production 方案仍需要单独定义映射所有权、审核流和 secret handling。
- T221 遗留的 Windows named-timezone portability 风险仍然存在，因为本轮没有引入 `tzdata`。
