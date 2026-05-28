**改了什么**

- 新增 [feishu_review_card.py](/D:/Codes/Social/practical_chat_agent/src/practical_chat_agent/services/feishu_review_card.py:24)，实现 `FeishuReviewCardConfig`、`FeishuReviewIntent`、`FeishuReviewCardRenderResult`、`FeishuReviewIntentParseResult`、`FeishuReviewCardBuilder`、`FeishuReviewIntentParser`。它只负责渲染本地 Feishu-compatible review card 和解析 inert review-intent，不会 apply approval/edit/reject/boundary-feedback，也不会调用 adapter、send gate、callback 或外部服务。
- 新增 [test_feishu_review_card.py](/D:/Codes/Social/practical_chat_agent/tests/test_feishu_review_card.py:136)，覆盖 pending/non-sendable card、sendable card、blocked gate-state card、可选 sandbox result summary、`CandidateAction` model/mapping 拒绝、不 mutate 输入 request、不会触发 transport、forbidden recipient metadata 不出现在 card、display truncation exact-boundary、deterministic action values、以及 approve/request-edit/reject/boundary-feedback 的 parser 成功与 malformed/missing/unknown/cross-request 拒绝。
- 更新了 [outbound_send_gate_contract.md](/D:/Codes/Social/practical_chat_agent/docs/data_contracts/outbound_send_gate_contract.md:435) 和 [07_handoff.md](/D:/Codes/Social/practical_chat_agent/docs/07_handoff.md:3796)，把 T224 明确为 “presentation + inert review intent parsing” 层，继续和 gate `allowed`、fake `fake_delivered`、sandbox `feishu_dry_run_ready` / `feishu_sandbox_sent`、production delivery 分离。
- 没有修改 `docs/04_task_board.md`，也没有扩展到 callback server、approval application、feedback log、memory write、WeChat、CLI/runtime wiring。

**如何验证**

- 先按 TDD 补测试并先跑红：首次运行 `pytest tests/test_outbound_message_request_schema.py tests/test_outbound_send_gate.py tests/test_outbound_fake_adapter.py tests/test_feishu_outbound_adapter.py tests/test_feishu_review_card.py ...` 因 `practical_chat_agent.services.feishu_review_card` 不存在而失败。
- `python -m py_compile src/practical_chat_agent/core/models.py src/practical_chat_agent/services/outbound_send_gate.py src/practical_chat_agent/services/outbound_fake_adapter.py src/practical_chat_agent/services/feishu_outbound_adapter.py src/practical_chat_agent/services/feishu_review_card.py`
- `pytest tests/test_outbound_message_request_schema.py tests/test_outbound_send_gate.py tests/test_outbound_fake_adapter.py tests/test_feishu_outbound_adapter.py tests/test_feishu_review_card.py -q -o cache_dir=artifacts\t224_pytest_cache --basetemp=artifacts\t224_pytest_basetemp` -> `84 passed`
- `pytest tests/ -q -o cache_dir=artifacts\t224_pytest_cache --basetemp=artifacts\t224_pytest_basetemp` -> `864 passed`
- 所有 pytest 都使用了 workspace-local `TEMP/TMP=artifacts\t224_pytest_tmp`。

**剩余风险**

- T224 只证明本地 review-card rendering 和 inert intent parsing，不代表真实 Feishu callback payload 与事件流已经验证。
- card 上的 draft preview truncation 只是 display-only 行为，后续任务不能把它误当成 privacy redaction 或 delivery-safe payload。
- T221 遗留的 Windows named-timezone portability 风险仍然存在，因为本轮没有引入 `tzdata`。
