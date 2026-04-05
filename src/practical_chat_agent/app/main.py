from __future__ import annotations

import json
from pathlib import Path
from typing import Annotated

import typer

from practical_chat_agent.app.config import get_settings
from practical_chat_agent.app.container import AppContainer
from practical_chat_agent.core.enums import PersonaType, SafetyMode
from practical_chat_agent.core.models import AgentProfile, MeetingLivePreview

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
        "glm_ocr_model": settings.glm_ocr_model,
        "glm_ocr_api_key_present": bool(settings.glm_ocr_api_key),
        "desktop_ocr_enabled": settings.desktop_ocr_enabled,
        "desktop_capture_debug_dir": settings.desktop_capture_debug_dir,
        "meeting_transcribe_model": settings.meeting_transcribe_model,
        "meeting_transcribe_api_key_present": bool(settings.meeting_transcribe_api_key),
        "meeting_transcribe_enabled": settings.meeting_transcribe_enabled,
        "meeting_capture_debug_dir": settings.meeting_capture_debug_dir,
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
    payload_path: Annotated[Path, typer.Argument(help="Path to a JSON payload file.")],
    connector_name: Annotated[
        str | None,
        typer.Option(help="Inbound connector to use. If omitted, the service resolves it from file metadata or payload shape."),
    ] = None,
) -> None:
    """Load a JSON payload file and run it through the connector-based ingress flow."""

    container = AppContainer.build()
    payload = json.loads(payload_path.read_text(encoding="utf-8"))
    result = container.inbound_service.ingest(connector_name=connector_name, payload=payload)
    typer.echo(json.dumps(result.model_dump(mode="json"), indent=2))


@app.command("replay-payload-dir")
def replay_payload_dir(
    payload_dir: Annotated[Path, typer.Argument(help="Directory containing JSON payload files.")],
    connector_name: Annotated[
        str | None,
        typer.Option(help="Fallback connector. Each file can also specify connector_name in payload metadata."),
    ] = None,
) -> None:
    """Replay every JSON payload file in a directory through the ingress flow."""

    container = AppContainer.build()
    json_files = sorted(path for path in payload_dir.iterdir() if path.is_file() and path.suffix.lower() == ".json")
    if not json_files:
        raise typer.BadParameter(f"No JSON payload files found in {payload_dir}")

    results: list[dict[str, object]] = []
    for payload_path in json_files:
        try:
            payload = json.loads(payload_path.read_text(encoding="utf-8"))
            resolved_connector = container.inbound_service.resolve_connector_name(
                payload=payload,
                connector_name=connector_name,
            )
            turn_result = container.inbound_service.ingest(
                connector_name=resolved_connector,
                payload=payload,
            )
            results.append(
                {
                    "file": str(payload_path),
                    "status": "ok",
                    "connector_name": resolved_connector,
                    "event_id": turn_result.event_id,
                    "should_reply": turn_result.should_reply,
                    "action_count": len(turn_result.actions),
                },
            )
        except Exception as exc:  # noqa: BLE001
            results.append(
                {
                    "file": str(payload_path),
                    "status": "error",
                    "error": str(exc),
                },
            )

    typer.echo(
        json.dumps(
            {
                "default_connector_name": connector_name,
                "processed_files": len(results),
                "success_count": sum(1 for item in results if item["status"] == "ok"),
                "error_count": sum(1 for item in results if item["status"] == "error"),
                "results": results,
            },
            indent=2,
        ),
    )


@app.command("desktop-scan-preview")
def desktop_scan_preview(
    account_id: Annotated[str, typer.Argument(help="Desktop account identifier to associate with the scan.")],
    conversation_hint: Annotated[
        str | None,
        typer.Option(help="Optional visible conversation hint, title, or nickname."),
    ] = None,
    connector_name: Annotated[str, typer.Option(help="Desktop connector to use.")] = "wechat_desktop",
    force_ocr: Annotated[
        bool,
        typer.Option("--force-ocr", help="Skip accessible-text extraction and force the OCR screenshot path."),
    ] = False,
    save_capture: Annotated[
        bool,
        typer.Option("--save-capture", help="Persist the OCR screenshot artifact for manual debugging."),
    ] = False,
) -> None:
    """Run the desktop connector skeleton and print its current preview output."""

    container = AppContainer.build()
    result = container.desktop_service.scan(
        connector_name=connector_name,
        account_id=account_id,
        conversation_hint=conversation_hint,
        force_ocr=force_ocr,
        save_capture=save_capture,
    )
    typer.echo(json.dumps(result.model_dump(mode="json"), indent=2))


@app.command("meeting-live-preview")
def meeting_live_preview(
    account_id: Annotated[str, typer.Argument(help="Desktop account identifier to associate with the meeting session.")],
    meeting_hint: Annotated[
        str | None,
        typer.Option(help="Optional visible meeting title or window hint."),
    ] = None,
    connector_name: Annotated[str, typer.Option(help="Meeting connector to use.")] = "tencent_meeting_desktop",
    sample_audio_path: Annotated[
        Path | None,
        typer.Option(help="Optional local audio file to run through the transcription service for skeleton testing."),
    ] = None,
    capture_seconds: Annotated[
        float | None,
        typer.Option(help="Optional duration for live loopback capture. Defaults to the configured meeting capture duration."),
    ] = None,
    chunk_seconds: Annotated[
        float | None,
        typer.Option(help="Optional chunk size for splitting captured meeting audio into WAV segments."),
    ] = None,
    save_capture: Annotated[
        bool,
        typer.Option(help="Persist captured WAV chunks for manual debugging."),
    ] = False,
    speaker_name: Annotated[
        str | None,
        typer.Option(help="Optional speaker name override for loopback capture device selection."),
    ] = None,
) -> None:
    """Preview the Tencent Meeting desktop transcription skeleton and optional file-based transcription path."""

    container = AppContainer.build()
    result: MeetingLivePreview = container.meeting_service.preview(
        connector_name=connector_name,
        account_id=account_id,
        meeting_hint=meeting_hint,
        sample_audio_path=sample_audio_path,
        capture_seconds=capture_seconds,
        chunk_seconds=chunk_seconds,
        save_capture=save_capture,
        speaker_name=speaker_name,
    )
    typer.echo(json.dumps(result.model_dump(mode="json"), indent=2))


if __name__ == "__main__":
    app()
