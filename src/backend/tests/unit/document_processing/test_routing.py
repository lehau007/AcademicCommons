from __future__ import annotations

from pathlib import Path

import fitz  # type: ignore[import-untyped]

from app.services.document_processing.routing import RouteDecider


def test_expected_type_to_route_all_six_types() -> None:
    decider = RouteDecider()
    assert decider.expected_type_to_route("text_pdf") == "direct_text"
    assert decider.expected_type_to_route("scanned_pdf") == "vision_only"
    assert decider.expected_type_to_route("slide_pdf") == "vision_only"
    assert decider.expected_type_to_route("mixed_pdf") == "hybrid"
    assert decider.expected_type_to_route("pptx") == "hybrid"
    assert decider.expected_type_to_route("image") == "vision_only"


def test_expected_type_to_route_unknown_defaults_to_hybrid() -> None:
    assert RouteDecider().expected_type_to_route("something_else") == "hybrid"


def test_decide_image_is_vision_only() -> None:
    decision = RouteDecider().decide(Path("x.jpg"))
    assert decision.route == "vision_only"
    assert decision.evidence["reason"] == "image_input"


def test_decide_pptx_is_hybrid() -> None:
    decision = RouteDecider().decide(Path("x.pptx"))
    assert decision.route == "hybrid"
    assert decision.evidence["reason"] == "pptx_text_plus_embedded_images"


def test_classify_text_pdf_and_decide_direct_text(tmp_path: Path) -> None:
    pdf_path = tmp_path / "sample.pdf"
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), "Hello " * 200)
    doc.save(str(pdf_path))
    doc.close()

    decider = RouteDecider()
    inferred_type, evidence = decider.classify_pdf_type(pdf_path)
    assert inferred_type == "text_pdf"
    assert evidence["page_count"] == 1

    decision = decider.decide(pdf_path)
    assert decision.route == "direct_text"
    assert decision.evidence["inferred_type"] == "text_pdf"


def test_decide_unknown_extension_falls_back_to_hybrid() -> None:
    decision = RouteDecider().decide(Path("x.txt"))
    assert decision.route == "hybrid"
    assert decision.evidence["reason"] == "fallback"
