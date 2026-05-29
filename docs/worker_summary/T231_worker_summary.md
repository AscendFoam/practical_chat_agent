# T231 Worker Summary

Task: T231 WeCom Customer Service Inbound Contract Spike

## What Changed

- Added `WeComCustomerServiceInboundConnector`, a local deterministic parser for
  synthetic WeCom WeChat Customer Service message/event payloads.
- Exported the connector from `src/practical_chat_agent/connectors/inbound/__init__.py`.
- Added redacted synthetic fixtures for:
  - inbound text message;
  - unsupported non-text message;
  - provider send-failure event;
  - malformed WeCom-shaped payload;
  - personal-WeChat/desktop-like payload rejection.
- Added focused tests for can-handle behavior, text normalization, unsupported
  message behavior, event mapping, malformed rejection, and personal-WeChat
  rejection.
- Added `docs/data_contracts/wecom_customer_service_inbound_contract.md`.
- Updated `docs/07_handoff.md` with a T231 worker completion record.

## TDD Evidence

- RED:
  - `pytest tests/test_wecom_customer_service_inbound.py -q`
  - failed during collection with
    `ModuleNotFoundError: No module named 'practical_chat_agent.connectors.inbound.wecom_customer_service'`
    before implementation.
- GREEN:
  - `pytest tests/test_wecom_customer_service_inbound.py -q -o cache_dir=artifacts\t231_pytest_cache --basetemp=artifacts\t231_pytest_basetemp`
  - passed: 6 tests.

## Official Docs

Official WeCom docs were rechecked on 2026-05-28:

- <https://developer.work.weixin.qq.com/document/path/94670>
- <https://developer.work.weixin.qq.com/document/path/94677>

The implementation remains synthetic-only. The docs were used to align fixture
field names such as `msg_list`, `msgid`, `open_kfid`, `external_userid`,
`send_time`, `msgtype`, `text.content`, `event_type`, `fail_msgid`, and
`fail_type`.

## Explicit Non-Actions

- No live callback route, webhook server, polling loop, sync loop, scheduler,
  background job, or runtime ingestion hook.
- No WeChat, WeCom, Tencent, Feishu, or external platform API call.
- No package install, SDK clone, SDK vendoring, or unofficial SDK snippet.
- No real corpsecret, app secret, access token, callback Token, EncodingAESKey,
  tenant ID, app ID, OpenID, external user ID, open_kfid, chat ID, cookie, QR
  code, or private recipient.
- No encryption/decryption, real signature verification, OAuth, tenant setup,
  credential loading, environment-variable handling, or IP allowlist.
- No outbound payload preparation, sending, retry, or provider-delivery claim.
- No `private/chat_history/`, `private/distilled/`, or private artifact read.
- No memory, ContactSkill, RelationshipState, feedback log, approved store, or
  outbound request/gate mutation.
- No changes to `src/practical_chat_agent/core/models.py`, outbound adapters,
  send-gate behavior, CLI commands, runtime services, or task board.

## Verification

- `python -m py_compile src/practical_chat_agent/connectors/inbound/wecom_customer_service.py src/practical_chat_agent/connectors/inbound/__init__.py`:
  passed.
- `pytest tests/test_wecom_customer_service_inbound.py -q -o cache_dir=artifacts\t231_pytest_cache --basetemp=artifacts\t231_pytest_basetemp`:
  passed, 6 tests.
- `git diff --check`: passed. Git reported line-ending conversion warnings for
  `docs/07_handoff.md` and
  `src/practical_chat_agent/connectors/inbound/__init__.py`, but no whitespace
  errors.
- `git status --short`: ran successfully and showed only T231 allowed-file
  changes in this worker state.

## Remaining Risks

- The connector is synthetic-contract-only and does not prove live WeCom
  callback compatibility.
- Official docs may drift before live work.
- The parser handles one message per call; future batching is undefined.
- No recipient mapping exists from synthetic WeCom customer aliases to repo
  contacts.
- Provider credential flow, callback verification, encryption/decryption,
  service-window tracking, quota enforcement, and failure-event state mutation
  remain unresolved.
