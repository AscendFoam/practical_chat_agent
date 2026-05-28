**改了什么**

- 新增 [outbound_fake_adapter.py](/D:/Codes/Social/practical_chat_agent/src/practical_chat_agent/services/outbound_fake_adapter.py:1)，实现 `FakeOutboundAdapterConfig`、`FakeOutboundDeliveryResult`、`LocalFakeOutboundAdapter`。它只接受 `OutboundMessageRequest` 或可稳定校验为该模型的 mapping；直接拒绝 `CandidateAction` 输入；对 `is_sendable()==false` 的请求返回本地阻断结果，对显式可发送请求返回 `fake_delivered` 的本地合成结果。
- 在 [test_outbound_fake_adapter.py](/D:/Codes/Social/practical_chat_agent/tests/test_outbound_fake_adapter.py:1) 新增适配器测试，覆盖 sendable 成功路径、stable mapping 输入、non-sendable 阻断、`CandidateAction` model/mapping 拒绝、invalid mapping 拒绝，以及输入请求不被 mutation。
- 另外补了 “human approval 未显式通过但 gate 已存在” 的阻断测试，确保 adapter 不会把 gate 结果误当成发送授权。
- 在 [test_outbound_send_gate.py](/D:/Codes/Social/practical_chat_agent/tests/test_outbound_send_gate.py:156) 补了 T221 的 clear-path 和多重阻断覆盖：`quiet_hours_clear`、`frequency_limit_clear`、`duplicate_check_clear`、`self_echo_clear`，以及 `human_approval_pending` + `kill_switch_enabled` 同时保留。
- 更新了 [outbound_send_gate_contract.md](/D:/Codes/Social/practical_chat_agent/docs/data_contracts/outbound_send_gate_contract.md:1) 和 [07_handoff.md](/D:/Codes/Social/practical_chat_agent/docs/07_handoff.md:3593)，把 T222 的 adapter boundary、结果形状、`allowed` vs `fake_delivered` vs real delivery 区分、以及禁止外部发送/调度行为写清楚。
- 时区选择上没有修改 `pyproject.toml`；T222 新增测试保持 UTC 路径，并在文档里明确保留 T221 的 Windows named-timezone portability 风险。

**如何验证**

- 先按 TDD 补测试并先跑红：首次运行 `pytest tests/test_outbound_send_gate.py tests/test_outbound_fake_adapter.py ...` 因 `practical_chat_agent.services.outbound_fake_adapter` 不存在而失败。
- `python -m py_compile src/practical_chat_agent/core/models.py src/practical_chat_agent/services/outbound_send_gate.py src/practical_chat_agent/services/outbound_fake_adapter.py`
- `pytest tests/test_outbound_send_gate.py tests/test_outbound_fake_adapter.py -q -o cache_dir=artifacts\t222_pytest_cache --basetemp=artifacts\t222_pytest_basetemp` -> `24 passed`
- `pytest tests/test_outbound_message_request_schema.py tests/test_outbound_send_gate.py tests/test_outbound_fake_adapter.py -q -o cache_dir=artifacts\t222_pytest_cache --basetemp=artifacts\t222_pytest_basetemp` -> `43 passed`
- `pytest tests/ -q -o cache_dir=artifacts\t222_pytest_cache --basetemp=artifacts\t222_pytest_basetemp` -> `823 passed`
- 所有 pytest 都使用了 workspace-local `TEMP/TMP=artifacts\t222_pytest_tmp`。

**剩余风险**

- T222 只证明本地 fake adapter 边界可消费 gate-approved request，不代表真实平台送达、ack、重试或恢复逻辑已经存在。
- `FakeOutboundDeliveryResult` 目前只保留截断 preview 和审计 note；后续真实 adapter 任务必须继续保持 review-safe 边界，不能把 raw/private transcript 带进结果层。
- T221 遗留的 Windows named-timezone portability 风险仍然存在，因为本轮明确选择不引入 `tzdata`。
