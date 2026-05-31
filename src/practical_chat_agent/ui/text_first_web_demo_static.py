"""Static asset helper for the local text-first web demo shell."""

from __future__ import annotations

import json
from pathlib import Path

from practical_chat_agent.ui.text_first_web_demo_adapter import TextFirstWebDemoAdapter


class TextFirstWebDemoStaticShell:
    """Expose static shell assets and adapter-backed demo payload JSON."""

    def __init__(self, static_dir: Path | None = None) -> None:
        self._static_dir = static_dir or Path(__file__).with_name("static")

    def asset_paths(self) -> dict[str, str]:
        return {
            "html": str(self._static_dir / "text_first_web_demo.html"),
            "css": str(self._static_dir / "text_first_web_demo.css"),
            "js": str(self._static_dir / "text_first_web_demo.js"),
        }

    def build_demo_payload_json(self, *, user_id: str = "user_synthetic") -> str:
        state = TextFirstWebDemoAdapter().build_synthetic_demo_state(user_id=user_id)
        return json.dumps(state.model_dump(mode="json"), ensure_ascii=False, indent=2)

    def render_embedded_html(self, *, user_id: str = "user_synthetic") -> str:
        html = Path(self.asset_paths()["html"]).read_text(encoding="utf-8")
        payload = self.build_demo_payload_json(user_id=user_id)
        return html.replace(
            "window.TEXT_FIRST_WEB_DEMO_STATE = null;",
            f"window.TEXT_FIRST_WEB_DEMO_STATE = {payload};",
        )
