from __future__ import annotations

import base64
import re
from typing import Any

from practical_chat_agent.core.models import OcrDocumentResult, OcrTextBlock


class GlmOcrService:
    """Thin wrapper around the GLM OCR layout parsing API."""

    def __init__(
        self,
        *,
        api_key: str | None,
        model: str = "glm-ocr",
        timeout_seconds: float = 30.0,
        enabled: bool = True,
    ) -> None:
        self.api_key = (api_key or "").strip() or None
        self.model = model
        self.timeout_seconds = timeout_seconds
        self.enabled = enabled

    def is_available(self) -> bool:
        return self.enabled and bool(self.api_key)

    def availability_reason(self) -> str | None:
        if not self.enabled:
            return "desktop OCR is disabled by configuration"
        if not self.api_key:
            return "GLM OCR API key is not configured"
        return None

    def recognize_image(
        self,
        *,
        image_bytes: bytes,
        mime_type: str = "image/png",
        user_id: str | None = None,
    ) -> OcrDocumentResult:
        if not self.is_available():
            raise RuntimeError(self.availability_reason() or "GLM OCR is unavailable")

        encoded = base64.b64encode(image_bytes).decode("ascii")
        payload_variants = [encoded]
        if mime_type:
            payload_variants.append(f"data:{mime_type};base64,{encoded}")

        last_error: Exception | None = None
        for file_payload in payload_variants:
            try:
                response = self._create_client().layout_parsing.create(
                    model=self.model,
                    file=file_payload,
                    user_id=user_id,
                    timeout=self.timeout_seconds,
                )
                return self._to_document_result(response)
            except Exception as exc:  # noqa: BLE001
                last_error = exc

        raise RuntimeError(f"GLM OCR request failed: {last_error}") from last_error

    def _create_client(self) -> Any:
        from zai import ZhipuAiClient

        return ZhipuAiClient(api_key=self.api_key)

    def _to_document_result(self, response: Any) -> OcrDocumentResult:
        blocks: list[OcrTextBlock] = []
        layout_details = getattr(response, "layout_details", None) or []
        for page_index, page_details in enumerate(layout_details):
            for detail in page_details or []:
                text = self._normalize_text(getattr(detail, "content", None))
                if not text:
                    continue
                bbox = [float(value) for value in (getattr(detail, "bbox_2d", None) or [])]
                blocks.append(
                    OcrTextBlock(
                        text=text,
                        page_index=page_index,
                        label=getattr(detail, "label", None),
                        bbox=bbox,
                    ),
                )

        markdown_text = self._normalize_markdown(getattr(response, "md_results", None))
        if not blocks and markdown_text:
            blocks = [
                OcrTextBlock(text=line, page_index=0, label="markdown_line")
                for line in markdown_text.splitlines()
                if line.strip()
            ]

        full_text = "\n".join(block.text for block in blocks) if blocks else (markdown_text or "")
        return OcrDocumentResult(
            provider="glm_ocr",
            model=str(getattr(response, "model", None) or self.model),
            full_text=full_text,
            markdown_text=markdown_text,
            blocks=blocks,
            raw=response.model_dump(mode="json") if hasattr(response, "model_dump") else {},
        )

    @staticmethod
    def _normalize_text(value: Any) -> str:
        text = str(value or "").replace("\r", " ").replace("\n", " ")
        return re.sub(r"\s+", " ", text).strip()

    @staticmethod
    def _normalize_markdown(value: Any) -> str | None:
        text = str(value or "").strip()
        if not text:
            return None
        lines = [re.sub(r"\s+", " ", line).strip() for line in text.splitlines()]
        normalized = "\n".join(line for line in lines if line)
        return normalized or None
