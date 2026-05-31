"""Dependency-free local preview routes for the text-first web demo."""

from __future__ import annotations

from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Mapping
from urllib.parse import unquote, urlsplit

from practical_chat_agent.ui.text_first_web_demo_static import TextFirstWebDemoStaticShell


@dataclass(frozen=True)
class LocalDemoResponse:
    status_code: int
    content_type: str
    body: bytes
    headers: Mapping[str, str]

    @property
    def text(self) -> str:
        return self.body.decode("utf-8")


class TextFirstWebDemoLocalServer:
    """Route local synthetic demo requests without external dependencies."""

    def __init__(self, shell: TextFirstWebDemoStaticShell | None = None) -> None:
        self._shell = shell or TextFirstWebDemoStaticShell()
        self._asset_routes = {
            "/text_first_web_demo.css": ("css", "text/css; charset=utf-8"),
            "/text_first_web_demo.js": ("js", "application/javascript; charset=utf-8"),
        }

    def route(self, path: str, *, user_id: str = "user_synthetic") -> LocalDemoResponse:
        clean_path = _clean_path(path)
        if clean_path is None:
            return _response(403, "text/plain; charset=utf-8", "forbidden")
        if clean_path in {"/", "/text_first_web_demo.html"}:
            return _response(200, "text/html; charset=utf-8", self._shell.render_embedded_html(user_id=user_id))
        if clean_path == "/demo-state.json":
            return _response(
                200,
                "application/json; charset=utf-8",
                self._shell.build_demo_payload_json(user_id=user_id),
            )
        if clean_path in self._asset_routes:
            asset_key, content_type = self._asset_routes[clean_path]
            asset_path = Path(self._shell.asset_paths()[asset_key])
            return _response(200, content_type, asset_path.read_text(encoding="utf-8"))
        return _response(404, "text/plain; charset=utf-8", "not found")

    def create_handler(self, *, user_id: str = "user_synthetic") -> type[BaseHTTPRequestHandler]:
        router = self

        class TextFirstWebDemoRequestHandler(BaseHTTPRequestHandler):
            def do_GET(self) -> None:  # noqa: N802 - stdlib handler API
                response = router.route(self.path, user_id=user_id)
                self.send_response(response.status_code)
                self.send_header("Content-Type", response.content_type)
                for name, value in response.headers.items():
                    self.send_header(name, value)
                self.end_headers()
                self.wfile.write(response.body)

            def log_message(self, format: str, *args: object) -> None:
                return

        return TextFirstWebDemoRequestHandler


def build_http_server(
    *,
    host: str = "127.0.0.1",
    port: int = 8767,
    user_id: str = "user_synthetic",
) -> ThreadingHTTPServer:
    local_server = TextFirstWebDemoLocalServer()
    handler = local_server.create_handler(user_id=user_id)
    return ThreadingHTTPServer((host, port), handler)


def _clean_path(path: str) -> str | None:
    decoded = unquote(urlsplit(path or "/").path or "/")
    if "\\" in decoded:
        return None
    parts = [part for part in decoded.split("/") if part]
    if any(part in {".", ".."} for part in parts):
        return None
    return "/" + "/".join(parts) if parts else "/"


def _response(status_code: int, content_type: str, text: str) -> LocalDemoResponse:
    return LocalDemoResponse(
        status_code=status_code,
        content_type=content_type,
        body=text.encode("utf-8"),
        headers={"Cache-Control": "no-store"},
    )

