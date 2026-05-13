# Practical Chat Agent

`practical_chat_agent` is an engineering prototype for a practical social chat agent. The current continuation line is WeChat-first: verify WeChatBot/iLink outside this repository, then connect stable WeChat ingestion, memory, contact skills, and controlled reply delivery into the existing runtime.

## Current Focus

The source of truth for the next phase is:

- `docs/02_experiment_plan.md`
- `docs/04_task_board.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

The project already has a Python package under `src/practical_chat_agent`, a Typer CLI, MySQL-backed repositories, chat memory/suggestion services, desktop WeChat scanning, meeting support, and a conservative outbound action flow.

## Typical Local Commands

```powershell
$env:PYTHONPATH='src'
& 'C:\ProgramData\anaconda3\envs\practical-chat-agent\python.exe' -m practical_chat_agent.app.main show-config
```

```powershell
$env:PYTHONPATH='src'
& 'C:\ProgramData\anaconda3\envs\practical-chat-agent\python.exe' -m practical_chat_agent.app.main action-list --text-only --limit 10
```

Do not print secrets from `.env`. Before editing code, inspect `git status --short` and preserve unrelated user changes.

