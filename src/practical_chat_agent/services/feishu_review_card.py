from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal, Mapping, Sequence

from pydantic import ValidationError

from practical_chat_agent.core.models import CandidateAction, OutboundMessageRequest
from practical_chat_agent.services.feishu_outbound_adapter import FeishuSandboxDeliveryResult


FeishuReviewIntentAction = Literal[
    "approve",
    "request_edit",
    "reject",
    "boundary_feedback",
]
FeishuReviewCardRenderStatus = Literal["card_rendered", "blocked_invalid_request"]
FeishuReviewIntentParseStatus = Literal["intent_parsed", "blocked_invalid_action"]

_REVIEW_INTENT_SCHEMA_VERSION = "feishu_review_intent_v1"
_ALLOWED_REVIEW_ACTIONS = {"approve", "request_edit", "reject", "boundary_feedback"}


@dataclass
class FeishuReviewCardConfig:
    """Deterministic config for local Feishu review-card rendering."""

    renderer_name: str = "feishu_review_card_builder"
    draft_preview_char_limit: int = 160
    max_gate_notes: int = 8
    max_sandbox_audit_notes: int = 8

    def __post_init__(self) -> None:
        if not self.renderer_name.strip():
            raise ValueError("FeishuReviewCardConfig.renderer_name must be non-empty.")
        if self.draft_preview_char_limit <= 0:
            raise ValueError("FeishuReviewCardConfig.draft_preview_char_limit must be > 0.")
        if self.max_gate_notes <= 0:
            raise ValueError("FeishuReviewCardConfig.max_gate_notes must be > 0.")
        if self.max_sandbox_audit_notes <= 0:
            raise ValueError("FeishuReviewCardConfig.max_sandbox_audit_notes must be > 0.")


@dataclass(frozen=True)
class FeishuReviewIntent:
    """Inert review-intent data encoded into card action values."""

    schema_version: str
    request_id: str
    action: FeishuReviewIntentAction

    def __post_init__(self) -> None:
        if self.schema_version != _REVIEW_INTENT_SCHEMA_VERSION:
            raise ValueError("FeishuReviewIntent.schema_version must match the supported review-intent version.")
        if not self.request_id.strip():
            raise ValueError("FeishuReviewIntent.request_id must be non-empty.")
        if self.action not in _ALLOWED_REVIEW_ACTIONS:
            raise ValueError("FeishuReviewIntent.action must be a supported review action.")


@dataclass
class FeishuReviewCardRenderResult:
    """Result of deterministic local review-card rendering."""

    renderer_name: str
    render_status: FeishuReviewCardRenderStatus
    rendered: bool
    request_id: str | None = None
    contact_id: str | None = None
    user_id: str | None = None
    channel_preference: str | None = None
    sendable: bool | None = None
    card_payload: dict[str, object] | None = None
    audit_notes: list[str] = field(default_factory=list)


@dataclass
class FeishuReviewIntentParseResult:
    """Deterministic parser result for synthetic Feishu card-action payloads."""

    parse_status: FeishuReviewIntentParseStatus
    accepted: bool
    intent: FeishuReviewIntent | None = None
    audit_notes: list[str] = field(default_factory=list)


class FeishuReviewCardBuilder:
    """Render a local Feishu-compatible review card without any side effects."""

    def __init__(self, *, config: FeishuReviewCardConfig | None = None) -> None:
        self.config = config or FeishuReviewCardConfig()

    def render(
        self,
        request: OutboundMessageRequest | CandidateAction | Mapping[str, Any],
        *,
        sandbox_result: FeishuSandboxDeliveryResult | Mapping[str, Any] | None = None,
        existing_audit: Sequence[str] | None = None,
    ) -> FeishuReviewCardRenderResult:
        if self._is_candidate_action_input(request):
            return self._blocked_invalid_request(
                contact_id=self._mapping_value(request, "contact_id"),
                user_id=self._mapping_value(request, "user_id"),
                channel_preference=self._mapping_value(request, "channel_preference"),
                audit_notes=[*self._clean_audit(existing_audit), "candidate_action_input_rejected"],
            )

        try:
            outbound_request = self._coerce_request(request)
        except ValidationError:
            return self._blocked_invalid_request(
                contact_id=self._mapping_value(request, "contact_id"),
                user_id=self._mapping_value(request, "user_id"),
                channel_preference=self._mapping_value(request, "channel_preference"),
                audit_notes=[*self._clean_audit(existing_audit), "request_validation_failed"],
            )

        sandbox_summary = self._coerce_sandbox_result(sandbox_result)
        card_payload = self._build_card(outbound_request, sandbox_summary)
        audit_notes = [
            *self._clean_audit(existing_audit),
            "review_card_rendered",
            "review_intent_actions_embedded",
            "no_approval_applied",
            "no_delivery_performed",
        ]
        if sandbox_summary is not None:
            audit_notes.append("sandbox_summary_included")

        return FeishuReviewCardRenderResult(
            renderer_name=self.config.renderer_name,
            render_status="card_rendered",
            rendered=True,
            request_id=outbound_request.request_id,
            contact_id=outbound_request.contact_id,
            user_id=outbound_request.user_id,
            channel_preference=outbound_request.channel_preference,
            sendable=outbound_request.is_sendable(),
            card_payload=card_payload,
            audit_notes=self._dedupe(audit_notes),
        )

    @staticmethod
    def _coerce_request(
        request: OutboundMessageRequest | Mapping[str, Any],
    ) -> OutboundMessageRequest:
        if isinstance(request, OutboundMessageRequest):
            return request
        return OutboundMessageRequest.model_validate(dict(request))

    @staticmethod
    def _coerce_sandbox_result(
        sandbox_result: FeishuSandboxDeliveryResult | Mapping[str, Any] | None,
    ) -> FeishuSandboxDeliveryResult | None:
        if sandbox_result is None:
            return None
        if isinstance(sandbox_result, FeishuSandboxDeliveryResult):
            return sandbox_result
        return FeishuSandboxDeliveryResult(**dict(sandbox_result))

    @staticmethod
    def _is_candidate_action_input(
        request: OutboundMessageRequest | CandidateAction | Mapping[str, Any],
    ) -> bool:
        if isinstance(request, CandidateAction):
            return True
        if not isinstance(request, Mapping):
            return False
        return (
            request.get("schema_version") == "candidate_action_v1"
            or "action_id" in request
            or "action_type" in request
        )

    def _build_card(
        self,
        request: OutboundMessageRequest,
        sandbox_result: FeishuSandboxDeliveryResult | None,
    ) -> dict[str, object]:
        elements: list[dict[str, object]] = [
            self._markdown_block(
                "**Request Identity**\n"
                f"- Request ID: `{request.request_id}`\n"
                f"- Contact ID: `{request.contact_id}`\n"
                f"- User ID: `{request.user_id}`\n"
                f"- Channel: `{request.channel_preference}`"
            ),
            self._markdown_block(
                "**Review State**\n"
                f"- Approval State: `{request.human_approval.review_state}`\n"
                f"- Gate State: `{request.send_gate.gate_state}`\n"
                f"- Sendable: `{self._bool_text(request.is_sendable())}`"
            ),
            self._markdown_block(
                "**Risk Flags**\n"
                f"{self._bullet_list(request.risk_flags, empty_label='(none)')}"
            ),
            self._markdown_block(
                "**Audit Notes**\n"
                f"{self._bullet_list(request.send_gate.gate_notes[: self.config.max_gate_notes], empty_label='(none)')}"
            ),
            self._markdown_block(
                "**Draft Preview**\n"
                f"{self._display_preview(request.payload.draft_text)}"
            ),
        ]
        if sandbox_result is not None:
            elements.append(self._sandbox_summary_block(sandbox_result))
        elements.append(self._action_buttons(request.request_id))

        return {
            "schema": "2.0",
            "config": {
                "wide_screen_mode": True,
            },
            "header": {
                "title": {
                    "tag": "plain_text",
                    "content": f"Outbound Review · {request.request_id}",
                },
            },
            "elements": elements,
        }

    def _sandbox_summary_block(self, sandbox_result: FeishuSandboxDeliveryResult) -> dict[str, object]:
        content = (
            "**Sandbox Result**\n"
            f"- Delivery Status: `{sandbox_result.delivery_status}`\n"
            f"- Delivered: `{self._bool_text(sandbox_result.delivered)}`\n"
            f"- Recipient Type: `{sandbox_result.recipient_type or 'unknown'}`\n"
            f"- Provider Message ID: `{sandbox_result.provider_message_id or 'none'}`\n"
            "- Audit Notes:\n"
            f"{self._bullet_list(sandbox_result.audit_notes[: self.config.max_sandbox_audit_notes], empty_label='(none)')}"
        )
        return self._markdown_block(content)

    def _action_buttons(self, request_id: str) -> dict[str, object]:
        return {
            "tag": "action",
            "actions": [
                self._button("Approve", "primary", request_id, "approve"),
                self._button("Request Edit", "default", request_id, "request_edit"),
                self._button("Reject", "danger", request_id, "reject"),
                self._button("Boundary Feedback", "default", request_id, "boundary_feedback"),
            ],
        }

    @staticmethod
    def _button(
        label: str,
        style: str,
        request_id: str,
        action: FeishuReviewIntentAction,
    ) -> dict[str, object]:
        return {
            "tag": "button",
            "type": style,
            "text": {
                "tag": "plain_text",
                "content": label,
            },
            "value": {
                "schema_version": _REVIEW_INTENT_SCHEMA_VERSION,
                "request_id": request_id,
                "action": action,
            },
        }

    @staticmethod
    def _markdown_block(content: str) -> dict[str, object]:
        return {
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": content,
            },
        }

    def _blocked_invalid_request(
        self,
        *,
        contact_id: str | None,
        user_id: str | None,
        channel_preference: str | None,
        audit_notes: Sequence[str],
    ) -> FeishuReviewCardRenderResult:
        return FeishuReviewCardRenderResult(
            renderer_name=self.config.renderer_name,
            render_status="blocked_invalid_request",
            rendered=False,
            contact_id=contact_id,
            user_id=user_id,
            channel_preference=channel_preference,
            sendable=None,
            card_payload=None,
            audit_notes=self._dedupe(audit_notes),
        )

    def _display_preview(self, draft_text: str) -> str:
        preview = " ".join(draft_text.split())
        if len(preview) <= self.config.draft_preview_char_limit:
            return preview
        if self.config.draft_preview_char_limit <= 3:
            return "." * self.config.draft_preview_char_limit
        cutoff = self.config.draft_preview_char_limit - 3
        return f"{preview[:cutoff]}..."

    @staticmethod
    def _bullet_list(values: Sequence[str], *, empty_label: str) -> str:
        if not values:
            return f"- {empty_label}"
        return "\n".join(f"- `{value}`" for value in values)

    @staticmethod
    def _bool_text(value: bool) -> str:
        return "true" if value else "false"

    @staticmethod
    def _dedupe(values: Sequence[str]) -> list[str]:
        seen: set[str] = set()
        result: list[str] = []
        for value in values:
            text = value.strip()
            if not text or text in seen:
                continue
            seen.add(text)
            result.append(text)
        return result

    @staticmethod
    def _clean_audit(values: Sequence[str] | None) -> list[str]:
        if values is None:
            return []
        return FeishuReviewCardBuilder._dedupe(list(values))

    @staticmethod
    def _mapping_value(
        request: OutboundMessageRequest | CandidateAction | Mapping[str, Any],
        key: str,
    ) -> str | None:
        if isinstance(request, Mapping):
            value = request.get(key)
            if isinstance(value, str) and value.strip():
                return value
        return None


class FeishuReviewIntentParser:
    """Parse synthetic Feishu card-action payloads into inert review intents."""

    def parse(
        self,
        action_payload: Mapping[str, Any],
        *,
        expected_request_id: str | None = None,
    ) -> FeishuReviewIntentParseResult:
        value = self._extract_value(action_payload)
        if not isinstance(value, Mapping):
            return self._blocked_invalid_action(["malformed_action_value"])

        schema_version = value.get("schema_version")
        if not isinstance(schema_version, str) or not schema_version.strip():
            return self._blocked_invalid_action(["missing_schema_version"])

        request_id = value.get("request_id")
        if not isinstance(request_id, str) or not request_id.strip():
            return self._blocked_invalid_action(["missing_request_id"])

        action = value.get("action")
        if not isinstance(action, str) or action not in _ALLOWED_REVIEW_ACTIONS:
            return self._blocked_invalid_action(["unknown_review_action"])

        if expected_request_id is not None and request_id != expected_request_id:
            return self._blocked_invalid_action(["request_id_mismatch"])

        try:
            intent = FeishuReviewIntent(
                schema_version=schema_version,
                request_id=request_id,
                action=action,
            )
        except ValueError as exc:
            return self._blocked_invalid_action([f"invalid_review_intent_{exc.__class__.__name__.casefold()}"])

        return FeishuReviewIntentParseResult(
            parse_status="intent_parsed",
            accepted=True,
            intent=intent,
            audit_notes=["review_intent_parsed"],
        )

    @staticmethod
    def _extract_value(action_payload: Mapping[str, Any]) -> Any:
        action = action_payload.get("action")
        if isinstance(action, Mapping):
            return action.get("value")
        return action_payload.get("value")

    @staticmethod
    def _blocked_invalid_action(audit_notes: Sequence[str]) -> FeishuReviewIntentParseResult:
        return FeishuReviewIntentParseResult(
            parse_status="blocked_invalid_action",
            accepted=False,
            intent=None,
            audit_notes=list(audit_notes),
        )
