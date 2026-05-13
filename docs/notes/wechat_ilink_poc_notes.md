# WeChat iLink POC Notes

更新日期：2026-05-13

## 1. 范围

本轮只验证仓库外 sandbox 的 SDK 安装、最小导入、构造和官方 QuickStart 登录入口是否能启动。

- 主仓库未改动 `src/practical_chat_agent/**`
- sandbox 路径：`D:\Codes\Social\wechatbot_sandbox`
- Python venv：`D:\Codes\Social\wechatbot_sandbox\.venv`

## 2. 参考来源

- 官方 Python 文档：<https://www.wechatbot.dev/en/python>
- 本地安装包：PyPI `wechatbot-sdk`

官方 Python 文档给出的关键入口与本地安装结果一致：

- 安装命令：`pip install wechatbot-sdk`
- 导入模块：`from wechatbot import WeChatBot`
- QuickStart 同时支持：
  - `bot.run()` 方式
  - `await bot.login(); await bot.start()` 方式

## 3. 本地环境

- 仓库内基线 `python --version`：`Python 3.12.7`
- SDK 安装版本：`wechatbot-sdk 0.2.1`
- 可导入模块名：`wechatbot`
- 安装位置：`D:\Codes\Social\wechatbot_sandbox\.venv\Lib\site-packages`

补充观察：

- 本地包元数据里 `Home-page` 和 `Project-URL` 为空。
- 本地包未暴露额外 CLI entry point，需要通过 Python 脚本方式调用。
- `pip show` 的 `Summary` 出现少量编码异常字符，但不影响安装与导入验证。

## 4. 实际执行命令

### 4.1 安装

```powershell
python --version
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install wechatbot-sdk
.\.venv\Scripts\python.exe -m pip show wechatbot-sdk
```

### 4.2 最小导入与构造验证

```powershell
.\.venv\Scripts\python.exe -c "from wechatbot import WeChatBot; bot = WeChatBot(cred_path='credentials.json'); print(type(bot).__name__)"
```

结果：

- 导入成功
- 构造成功
- 输出 `WeChatBot`

### 4.3 QuickStart 登录入口探测

本轮使用与官方 async QuickStart 一致的 `await bot.login()` 路径，并加 20 秒超时，只验证是否能进入二维码登录流程，不做真实发送。

结果摘要：

```text
EVENT:QR_URL_RECEIVED
RESULT:TIMEOUT_WAITING_FOR_LOGIN
STATES:['qr']
```

补充检查：

- 20 秒超时前已触发 `on_qr_url` 回调，说明 SDK 能进入二维码登录阶段。
- 未扫码确认前，sandbox 下未生成 `credentials.json`。

## 5. 当前结论

### 5.1 已确认

- `wechatbot-sdk` 可在独立 sandbox 中成功安装。
- 官方文档中的 Python 导入路径 `from wechatbot import WeChatBot` 与本地包一致。
- `WeChatBot` 构造成功。
- `login()` 能真实触发二维码 URL 回调，说明 QuickStart 登录流程至少已跑到扫码阶段。

### 5.2 仍未确认

- 未完成真实扫码登录，因此还不能确认凭据落盘与会话恢复机制。
- 未验证收消息、reply、主动 `send()`、媒体能力。
- 未验证 `context_token` 是否存在、字段名是什么、是否可复用。
- 未验证长轮询稳定性、超时行为和重登行为。
- 当前只在系统 `Python 3.12.7` sandbox 验证通过；项目后续若要求固定到其他 Python 环境，仍需补测。

## 6. 建议给 T01

- 继续复用 `D:\Codes\Social\wechatbot_sandbox`
- 使用测试微信账号和测试联系人做首次真实扫码
- 优先验证：
  - 扫码成功后是否生成 `credentials.json`
  - 进程重启后是否能复用凭据
  - 最小收消息链路是否可用
- 未完成 reviewer 审核前，不把本轮结果视为 Gate 0 通过
