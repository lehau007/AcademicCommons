from __future__ import annotations

import io
from pathlib import Path
from typing import Any

import fitz  # type: ignore[import-untyped]
from PIL import Image, ImageDraw

from app.services.document_processing.metrics import LlmCallRecorder
from app.services.document_processing.progress import ProgressEmitter
from app.services.document_processing.providers.base import ProviderResponse, VisionLanguageProvider
from app.services.document_processing.providers.chain import ProviderChain


class ScriptedProvider(VisionLanguageProvider):
    """Returns canned text per ``operation``; an error response when none is scripted."""

    provider_name = "scripted"

    def __init__(self, responses: dict[str, str]) -> None:
        self._responses = responses
        self.calls: list[str] = []

    def complete(
        self,
        prompt: str,
        *,
        images: list[bytes] | None = None,
        operation: str = "text",
        **kwargs: Any,
    ) -> ProviderResponse:
        self.calls.append(operation)
        text = self._responses.get(operation)
        if text is None:
            return ProviderResponse("", "scripted", "fake", "error", 1, error="not scripted")
        return ProviderResponse(text, "scripted", "fake", "success", 1)


def make_chain(
    providers: list[VisionLanguageProvider] | None = None,
    *,
    enable_real_vision: bool = False,
    global_concurrency: int = 32,
) -> ProviderChain:
    """Build a ProviderChain with throwaway recorder/emitter for unit tests."""
    return ProviderChain(
        providers or [],
        recorder=LlmCallRecorder(),
        emitter=ProgressEmitter(),
        enable_real_vision=enable_real_vision,
        global_concurrency=global_concurrency,
    )


def png_bytes(width: int = 600, height: int = 500, *, color: str = "white") -> bytes:
    image = Image.new("RGB", (width, height), color)
    draw = ImageDraw.Draw(image)
    draw.rectangle([10, 10, width - 10, height - 10], outline="black", width=4)
    draw.line([10, 10, width - 10, height - 10], fill="black", width=3)
    buffer = io.BytesIO()
    image.save(buffer, "PNG")
    return buffer.getvalue()


FIGURE_COLORS = ("white", "yellow", "cyan", "magenta", "lightgray", "orange", "pink", "lightgreen")


def _draw_vector_figure(page: Any, rect: Any, variant: int) -> None:
    """A pure vector diagram (circles + lines + frame): no raster image, no text inside."""
    shape = page.new_shape()
    for k in range(6):
        x = rect.x0 + 50 + 40 * k
        shape.draw_circle(fitz.Point(x, rect.y0 + 100 + (k % 2) * 60), 15 + variant % 5)
        shape.draw_line(fitz.Point(x, rect.y0 + 100), fitz.Point(x + 40, rect.y0 + 160))
    shape.finish(color=(0, 0, 0), fill=(0.8, 0.8, 1 - 0.1 * (variant % 5)), width=2)
    shape.draw_rect(rect)
    shape.finish(color=(0, 0, 0), width=2)
    shape.commit()


def build_text_pdf(
    path: Path,
    pages: int = 3,
    *,
    banner: bool = False,
    same_position: bool = False,
    distinct_images: bool = False,
    vector: bool = False,
) -> Path:
    """Text-layer pages with one big figure each (plus a tiny logo).

    By default every page shows the same image at a slightly different position, so the figures
    are not "repeated". ``same_position`` pins the figure to one slot on every page,
    ``distinct_images`` gives each page a different raster image, and ``vector`` draws a pure
    vector diagram instead of a raster image.
    """
    doc = fitz.open()
    for i in range(pages):
        page = doc.new_page()
        page.insert_text((72, 72), f"Chapter {i + 1}: Graph theory basics", fontsize=18)
        page.insert_text((72, 110), "A graph G = (V, E) consists of vertices and edges.", fontsize=11)
        top = 200 if same_position else 200 + 20 * i  # distinct position per page so figures are not "repeated"
        rect = fitz.Rect(150, top, 450, top + 250)
        if vector:
            _draw_vector_figure(page, rect, i)
        else:
            color = FIGURE_COLORS[i % len(FIGURE_COLORS)] if distinct_images else "white"
            page.insert_image(rect, stream=png_bytes(color=color))
        page.insert_image(fitz.Rect(20, 20, 50, 40), stream=png_bytes(60, 40, color="red"))
        if banner:
            page.insert_image(fitz.Rect(50, 700, 550, 760), stream=png_bytes(1000, 120, color="blue"))
        page.insert_text((72, 520 + 20 * i), "Figure explanation text after the image.", fontsize=11)
    doc.save(str(path))
    doc.close()
    return path


def build_scanned_pdf(path: Path, pages: int = 1) -> Path:
    doc = fitz.open()
    for _ in range(pages):
        page = doc.new_page()
        page.insert_image(page.rect, stream=png_bytes(1200, 1600))
    doc.save(str(path))
    doc.close()
    return path
