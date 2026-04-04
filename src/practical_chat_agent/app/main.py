from __future__ import annotations

import json
from typing import Annotated

import typer

from practical_chat_agent.app.config import get_settings
from practical_chat_agent.app.container import AppContainer
from practical_chat_agent.core.enums import (
    ChannelType,
    ContentType,
    Direction,
    PersonaType,
    Platform,
    SafetyMode,
    SourceType,
)
from practical_chat_agent.core.ids import new_id
from practical_chat_agent.core.models import AgentProfile, InboundEvent

app = typer.Typer(no_args_is_help=True, add_completion=False)


@app.command("show-config")
def show_config() -> None:
    """Print the effective runtime configuration without secrets."""

    settings = get_settings()
    safe_config = {
        "app_env": settings.app_env,
        "app_name": settings.app_name,
        "mysql_host": settings.mysql_host,
        "mysql_port": settings.mysql_port,
        "mysql_database": settings.mysql_database,
        "mysql_user": settings.mysql_user,
        "mysql_echo": settings.mysql_echo,
        "openai_base_url": settings.openai_base_url,
        "openai_api_key_present": bool(settings.openai_api_key),
    }
    typer.echo(json.dumps(safe_config, indent=2))


@app.command("init-db")
def init_db() -> None:
    """Create the MySQL database if missing and apply the initial schema."""

    container = AppContainer.build()
    container.init_database()
    typer.echo("Database schema initialized.")


@app.command("create-agent")
def create_agent(
    agent_id: Annotated[str, typer.Argument(help="Stable agent identifier.")],
    display_name: Annotated[str, typer.Argument(help="Display name shown by the agent.")],
    persona_type: Annotated[PersonaType, typer.Option(help="Configured persona flavor.")] = PersonaType.FRIEND,
    safety_mode: Annotated[SafetyMode, typer.Option(help="Safety posture for the agent.")] = SafetyMode.DISCLOSED_AI,
) -> None:
    """Persist a minimal agent profile in the repository."""

    container = AppContainer.build()
    profile = AgentProfile(
        agent_id=agent_id,
        display_name=display_name,
        persona_type=persona_type,
        safety_mode=safety_mode,
    )
    container.agent_repository.upsert(profile)
    typer.echo(f"Agent '{agent_id}' saved.")


@app.command("demo-turn")
def demo_turn(
    agent_id: Annotated[str, typer.Argument(help="Target agent identifier.")],
    channel_id: Annotated[str, typer.Argument(help="Conversation or room identifier.")],
    actor_id: Annotated[str, typer.Argument(help="External user identifier.")],
    text: Annotated[str, typer.Argument(help="Inbound text message to simulate.")],
    platform: Annotated[Platform, typer.Option(help="Source platform.")] = Platform.TELEGRAM,
) -> None:
    """Run one inbound event through the minimal agent runtime."""

    container = AppContainer.build()
    event = InboundEvent(
        event_id=new_id("evt"),
        source_type=SourceType.CHAT_MESSAGE,
        platform=platform,
        channel_id=channel_id,
        channel_type=ChannelType.DM,
        account_id=agent_id,
        actor_id=actor_id,
        actor_name=actor_id,
        direction=Direction.INBOUND,
        content_type=ContentType.TEXT,
        text=text,
    )
    result = container.runtime.handle_inbound_event(agent_id=agent_id, event=event)
    typer.echo(json.dumps(result.model_dump(mode="json"), indent=2))


if __name__ == "__main__":
    app()
