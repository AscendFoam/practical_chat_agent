# Task T24: Media Assets

## Task ID

T24

## Goal

新增 media asset 元数据模型、服务和 CLI，支持图片/语音/文件元数据归档与后续 fetch。

## Why now

媒体能力是微信主线验收项之一，但第一版只要求元数据可靠，不要求完整发送。

## Allowed files

- `src/practical_chat_agent/core/models.py`
- `src/practical_chat_agent/storage/mysql/models.py`
- `src/practical_chat_agent/storage/mysql/repositories.py`
- `src/practical_chat_agent/services/media_assets.py`
- `src/practical_chat_agent/app/main.py`
- `docs/07_handoff.md`

## Forbidden scope

- 不上传媒体。
- 不把真实媒体文件提交到仓库。
- 不把下载失败伪装成成功。

## Inputs to read

- `docs/02_experiment_plan.md` section 7.5
- T20 raw payload models.

## Expected output

- `media_assets` additive table/repository.
- CLI list/show/fetch or fetch placeholder with explicit unsupported status.
- Media metadata links to event/raw payload where available.

## Verification

Run fixture media payload ingestion and inspect media asset output.

## Docs to update

- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md` if media fetch is deferred

## Reviewer type

normal

