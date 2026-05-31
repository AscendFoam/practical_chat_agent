"""Static asset helper for the local text-first web demo shell."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

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

    def build_review_workspace_qa_snapshot(
        self,
        *,
        user_id: str = "user_synthetic",
    ) -> dict[str, Any]:
        """Build deterministic local inspection data for review workspace QA."""

        paths = self.asset_paths()
        html = Path(paths["html"]).read_text(encoding="utf-8")
        js = Path(paths["js"]).read_text(encoding="utf-8")
        payload = json.loads(self.build_demo_payload_json(user_id=user_id))
        review = payload["review_workspace"]
        cards = list(review.get("cards", []))
        badge_labels = [
            badge.get("label", "")
            for card in cards
            for badge in card.get("status_badges", [])
        ]
        badge_tones = [
            badge.get("tone", "")
            for card in cards
            for badge in card.get("status_badges", [])
        ]
        blocker_text = [
            _friendly_label(code)
            for card in cards
            for code in card.get("blocking_issue_codes", [])
        ]
        export_cards = [card for card in cards if card.get("card_kind") == "export_summary"]
        return {
            "schema_version": "review_workspace_visual_qa_snapshot_v1",
            "user_id": user_id,
            "static_targets": {
                "tab_review": 'id="tab-review"' in html,
                "review_panel": 'id="review-panel"' in html,
                "review_filters": 'id="review-filters"' in html,
                "review_workspace_list": 'id="review-workspace-list"' in html,
                "review_export_summary": 'id="review-export-summary"' in html,
            },
            "projection_policy": review.get("projection_policy"),
            "filter_tabs": [tab.get("key") for tab in review.get("filter_tabs", [])],
            "card_count": len(cards),
            "card_titles": [card.get("title", "") for card in cards],
            "status_tones": sorted({tone for tone in badge_tones if tone}),
            "status_badge_text": " / ".join(label for label in badge_labels if label),
            "blocker_text": " / ".join(blocker_text),
            "safe_export_text": " / ".join(
                card.get("title", "") for card in export_cards
            ),
            "action_controls_present": _has_review_action_controls(html + "\n" + js),
            "browser_screenshot": False,
            "local_snapshot_only": True,
        }


def _has_review_action_controls(asset_text: str) -> bool:
    normalized = asset_text.lower()
    return any(
        marker in normalized
        for marker in (
            'data-action="approve"',
            'data-action="reject"',
            'data-action="deliver"',
            'data-action="publish"',
            'data-action="mutate"',
            "callprovider",
            "openwebhook",
        )
    )


def _friendly_label(value: str) -> str:
    return value.replace("_", " ").capitalize()
