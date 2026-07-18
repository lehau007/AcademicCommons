"""Route decision. Ports experiment ``classify_pdf_type`` / ``expected_type_to_route`` /
``decide_route`` (lines ~226-394)."""

from __future__ import annotations

from pathlib import Path

from app.services.document_processing.models import RouteDecision

EXPECTED_TYPES = {"text_pdf", "scanned_pdf", "slide_pdf", "mixed_pdf", "pptx", "image"}
EXPECTED_ROUTES = {"direct_text", "hybrid", "vision_only"}
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}


class RouteDecider:
    def classify_pdf_type(self, pdf_path: Path) -> tuple[str, dict[str, object]]:
        """Return (inferred_type, evidence). Mirrors experiment ``classify_pdf_type``."""
        try:
            import fitz  # type: ignore[import-untyped]  # PyMuPDF
        except Exception:
            return "text_pdf", {
                "reason": "pymupdf_unavailable",
                "text_chars": None,
                "page_count": None,
                "image_count": None,
            }

        doc = fitz.open(pdf_path)
        page_count = len(doc)
        text_chars = 0
        image_count = 0
        landscape_count = 0

        for page in doc:
            text_chars += len((page.get_text("text") or "").strip())
            image_count += len(page.get_images(full=True))
            if page.rect.width > page.rect.height:
                landscape_count += 1

        doc.close()
        avg_chars_per_page = (text_chars / page_count) if page_count else 0
        images_per_page = (image_count / page_count) if page_count else 0
        is_landscape = (landscape_count / page_count) > 0.5 if page_count else False

        if text_chars < 80:
            guessed_type = "scanned_pdf"
        elif is_landscape and image_count > 0:
            guessed_type = "slide_pdf"
        elif avg_chars_per_page >= 120 and images_per_page <= 0.3:
            guessed_type = "text_pdf"
        elif image_count > 0 and avg_chars_per_page >= 80:
            guessed_type = "mixed_pdf"
        else:
            guessed_type = "text_pdf"

        evidence: dict[str, object] = {
            "text_chars": text_chars,
            "page_count": page_count,
            "image_count": image_count,
            "avg_chars_per_page": round(avg_chars_per_page, 2),
            "images_per_page": round(images_per_page, 3),
            "landscape_pages": landscape_count,
            "is_landscape": is_landscape,
        }
        return guessed_type, evidence

    def expected_type_to_route(self, expected_type: str) -> str:
        mapping = {
            "text_pdf": "direct_text",
            "scanned_pdf": "vision_only",
            "slide_pdf": "vision_only",
            "mixed_pdf": "hybrid",
            "pptx": "hybrid",
            "image": "vision_only",
        }
        return mapping.get(expected_type, "hybrid")

    def decide(self, input_file: Path) -> RouteDecision:
        """Mirrors experiment ``decide_route`` but returns a :class:`RouteDecision`."""
        ext = input_file.suffix.lower()
        if ext in IMAGE_EXTENSIONS:
            return RouteDecision(route="vision_only", evidence={"reason": "image_input"})
        if ext == ".pptx":
            return RouteDecision(
                route="hybrid", evidence={"reason": "pptx_text_plus_embedded_images"}
            )

        if ext == ".pdf":
            inferred_type, evidence = self.classify_pdf_type(input_file)
            return RouteDecision(
                route=self.expected_type_to_route(inferred_type),
                evidence={
                    "reason": "pdf_probe",
                    "inferred_type": inferred_type,
                    **evidence,
                },
            )

        return RouteDecision(route="hybrid", evidence={"reason": "fallback"})
