from __future__ import annotations

from pathlib import Path
from textwrap import wrap
from typing import Literal, Optional, TypedDict

from langgraph.graph import END, START, StateGraph


OUTPUT_DIR = Path(__file__).resolve().parent / "generated"

Recommendation = Literal["APPROVE", "NEEDS_REVIEW", "REJECT"]
QueueRoute = Literal["REVIEWER_QUEUE", "ADMIN_QUEUE"]
Decision = Literal["APPROVE", "REJECT"]
ContributionType = Literal[
    "past_exam",
    "summary_note",
    "review_note",
    "solved_exercise",
]


class EvaluationState(TypedDict, total=False):
    document_id: str
    course_id: str
    markdown_text: str
    initial_contribution_type: ContributionType
    document_summary: dict
    summary_valid: bool
    agent_1_output: dict
    agent_1_valid: bool
    agent_2_output: dict
    agent_2_valid: bool
    agent_3_output: dict
    agent_3_valid: bool
    recommendation: Recommendation
    evaluation_report_persisted: bool
    has_active_reviewer: bool
    sla_breached: bool
    queue_route: QueueRoute
    review_decision: Decision
    final_state: Literal["FAILED", "NEEDS_REVIEW", "APPROVED", "REJECTED"]


def summarize_document(state: EvaluationState) -> EvaluationState:
    markdown_text = state.get("markdown_text", "")
    return {
        "document_summary": {
            "schema_version": "1.0",
            "topic": "Detected topic placeholder",
            "concepts": ["key concept"],
            "language": "mixed",
            "ocr_quality": "high",
            "section_summaries": [
                {
                    "heading": "Introduction",
                    "summary": "Placeholder summary for the graph artifact.",
                    "page_range": [1, 2],
                }
            ],
            "overall_summary": markdown_text[:500]
            or "Summarized normalized Markdown content.",
        }
    }


def validate_document_summary(state: EvaluationState) -> EvaluationState:
    return {"summary_valid": bool(state.get("document_summary"))}


def run_agent_1(_: EvaluationState) -> EvaluationState:
    return {
        "agent_1_output": {
            "schema_version": "1.0",
            "course_context": {
                "syllabus_topic_summary": "Course topic summary placeholder",
                "existing_document_count": 2,
                "topic_coverage": {"Detected topic placeholder": "partial"},
            },
            "duplicate": {
                "is_duplicate": False,
                "duplicate_of_document_id": None,
                "similarity_score": 0.41,
            },
            "cold_start": {"is_cold_start": True, "reason": "Approved docs < 3"},
        }
    }


def validate_agent_1(state: EvaluationState) -> EvaluationState:
    return {"agent_1_valid": bool(state.get("agent_1_output"))}


def run_agent_2(state: EvaluationState) -> EvaluationState:
    summary = state.get("document_summary", {})
    topic = summary.get("topic", "Unknown topic")
    return {
        "agent_2_output": {
            "schema_version": "1.0",
            "references": [
                {
                    "title": f"Reference for {topic}",
                    "url": "https://example.edu/reference",
                    "snippet": "Supplementary authoritative reference placeholder.",
                    "source_type": "course_page",
                }
            ],
            "search_status": "timeout",
            "search_duration_ms": 15000,
        }
    }


def validate_agent_2(state: EvaluationState) -> EvaluationState:
    return {"agent_2_valid": bool(state.get("agent_2_output"))}


def run_agent_3(state: EvaluationState) -> EvaluationState:
    agent_1_output = state["agent_1_output"]
    duplicate = agent_1_output["duplicate"]["is_duplicate"]
    cold_start = agent_1_output["cold_start"]["is_cold_start"]
    relevance = 8.2

    if duplicate:
        recommendation: Recommendation = "REJECT"
        reasons = ["Duplicate contribution detected by Agent 1."]
    elif cold_start:
        recommendation = "NEEDS_REVIEW"
        reasons = ["Cold-start course requires reviewer confirmation."]
    elif relevance < 4.0:
        recommendation = "REJECT"
        reasons = ["Relevance below intake threshold."]
    elif relevance < 7.0:
        recommendation = "NEEDS_REVIEW"
        reasons = ["Relevance in reviewer buffer zone."]
    else:
        recommendation = "APPROVE"
        reasons = ["High relevance and no blocking flags."]

    initial_type = state["initial_contribution_type"]
    return {
        "agent_3_output": {
            "schema_version": "1.0",
            "scores": {
                "relevance": relevance,
                "completeness": 7.5,
                "quality": 7.8,
            },
            "label_verification": {
                "initial_contribution_type": initial_type,
                "suggested_contribution_type": initial_type,
                "label_confidence": 0.87,
                "label_mismatch": False,
            },
            "recommendation": recommendation,
            "recommendation_reasons": reasons,
            "duplicate_flag": duplicate,
            "cold_start_flag": cold_start,
        },
        "recommendation": recommendation,
    }


def validate_agent_3(state: EvaluationState) -> EvaluationState:
    return {"agent_3_valid": bool(state.get("agent_3_output"))}


def capture_recommendation(state: EvaluationState) -> EvaluationState:
    return {"recommendation": state["recommendation"]}


def recommendation_approve(_: EvaluationState) -> EvaluationState:
    return {}


def recommendation_needs_review(_: EvaluationState) -> EvaluationState:
    return {}


def recommendation_reject(_: EvaluationState) -> EvaluationState:
    return {}


def persist_evaluation_report(_: EvaluationState) -> EvaluationState:
    return {
        "evaluation_report_persisted": True,
        # SRS FR-HR-01: after successful pipeline, documents still enter NEEDS_REVIEW.
        "final_state": "NEEDS_REVIEW",
    }


def route_review_queue(state: EvaluationState) -> EvaluationState:
    route: QueueRoute = (
        "REVIEWER_QUEUE" if state.get("has_active_reviewer", True) else "ADMIN_QUEUE"
    )
    return {"queue_route": route}


def queue_reviewer(_: EvaluationState) -> EvaluationState:
    return {}


def queue_admin(_: EvaluationState) -> EvaluationState:
    return {}


def check_sla(_: EvaluationState) -> EvaluationState:
    return {}


def manual_review(_: EvaluationState) -> EvaluationState:
    return {}


def approve_after_review(_: EvaluationState) -> EvaluationState:
    return {"review_decision": "APPROVE", "final_state": "APPROVED"}


def reject_after_review(_: EvaluationState) -> EvaluationState:
    return {"review_decision": "REJECT", "final_state": "REJECTED"}


def failed(_: EvaluationState) -> EvaluationState:
    return {"final_state": "FAILED"}


def route_summary_validation(state: EvaluationState) -> str:
    return "run_agents" if state["summary_valid"] else "failed"


def route_agent_1_validation(state: EvaluationState) -> str:
    return "ready" if state["agent_1_valid"] else "failed"


def route_agent_2_validation(state: EvaluationState) -> str:
    return "ready" if state["agent_2_valid"] else "failed"


def route_agent_3_validation(state: EvaluationState) -> str:
    return "capture_recommendation" if state["agent_3_valid"] else "failed"


def route_recommendation(state: EvaluationState) -> str:
    recommendation = state["recommendation"]
    if recommendation == "APPROVE":
        return "recommendation_approve"
    if recommendation == "NEEDS_REVIEW":
        return "recommendation_needs_review"
    return "recommendation_reject"


def route_queue(state: EvaluationState) -> str:
    return "queue_reviewer" if state["queue_route"] == "REVIEWER_QUEUE" else "queue_admin"


def route_sla(state: EvaluationState) -> str:
    return "queue_admin" if state.get("sla_breached", False) else "manual_review"


def route_review_decision(state: EvaluationState) -> str:
    return (
        "approve_after_review"
        if state.get("review_decision", "APPROVE") == "APPROVE"
        else "reject_after_review"
    )


def build_graph():
    graph = StateGraph(EvaluationState)
    graph.add_node("summarize_document", summarize_document)
    graph.add_node("validate_document_summary", validate_document_summary)
    graph.add_node("run_agent_1", run_agent_1)
    graph.add_node("validate_agent_1", validate_agent_1)
    graph.add_node("run_agent_2", run_agent_2)
    graph.add_node("validate_agent_2", validate_agent_2)
    graph.add_node("run_agent_3", run_agent_3)
    graph.add_node("validate_agent_3", validate_agent_3)
    graph.add_node("capture_recommendation", capture_recommendation)
    graph.add_node("recommendation_approve", recommendation_approve)
    graph.add_node("recommendation_needs_review", recommendation_needs_review)
    graph.add_node("recommendation_reject", recommendation_reject)
    graph.add_node("persist_evaluation_report", persist_evaluation_report)
    graph.add_node("route_review_queue", route_review_queue)
    graph.add_node("queue_reviewer", queue_reviewer)
    graph.add_node("queue_admin", queue_admin)
    graph.add_node("check_sla", check_sla)
    graph.add_node("manual_review", manual_review)
    graph.add_node("approve_after_review", approve_after_review)
    graph.add_node("reject_after_review", reject_after_review)
    graph.add_node("failed", failed)

    graph.add_edge(START, "summarize_document")
    graph.add_edge("summarize_document", "validate_document_summary")
    graph.add_conditional_edges(
        "validate_document_summary",
        route_summary_validation,
        {"run_agents": "run_agent_1", "failed": "failed"},
    )
    graph.add_edge("validate_document_summary", "run_agent_2")
    graph.add_edge("run_agent_1", "validate_agent_1")
    graph.add_edge("run_agent_2", "validate_agent_2")
    graph.add_conditional_edges(
        "validate_agent_1",
        route_agent_1_validation,
        {"ready": "run_agent_3", "failed": "failed"},
    )
    graph.add_conditional_edges(
        "validate_agent_2",
        route_agent_2_validation,
        {"ready": "run_agent_3", "failed": "failed"},
    )
    graph.add_edge("run_agent_3", "validate_agent_3")
    graph.add_conditional_edges(
        "validate_agent_3",
        route_agent_3_validation,
        {"capture_recommendation": "capture_recommendation", "failed": "failed"},
    )
    graph.add_conditional_edges(
        "capture_recommendation",
        route_recommendation,
        {
            "recommendation_approve": "recommendation_approve",
            "recommendation_needs_review": "recommendation_needs_review",
            "recommendation_reject": "recommendation_reject",
        },
    )
    graph.add_edge("recommendation_approve", "persist_evaluation_report")
    graph.add_edge("recommendation_needs_review", "persist_evaluation_report")
    graph.add_edge("recommendation_reject", "persist_evaluation_report")
    graph.add_edge("persist_evaluation_report", "route_review_queue")
    graph.add_conditional_edges(
        "route_review_queue",
        route_queue,
        {
            "queue_reviewer": "queue_reviewer",
            "queue_admin": "queue_admin",
        },
    )
    graph.add_edge("queue_reviewer", "check_sla")
    graph.add_conditional_edges(
        "check_sla",
        route_sla,
        {"queue_admin": "queue_admin", "manual_review": "manual_review"},
    )
    graph.add_edge("queue_admin", "manual_review")
    graph.add_conditional_edges(
        "manual_review",
        route_review_decision,
        {
            "approve_after_review": "approve_after_review",
            "reject_after_review": "reject_after_review",
        },
    )
    graph.add_edge("approve_after_review", END)
    graph.add_edge("reject_after_review", END)
    graph.add_edge("failed", END)
    return graph.compile()


def save_text_artifacts(graph) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    drawable = graph.get_graph()
    (OUTPUT_DIR / "document_evaluation_langgraph.mmd").write_text(
        drawable.draw_mermaid(),
        encoding="utf-8",
    )
    try:
        ascii_graph = drawable.draw_ascii()
    except ImportError:
        ascii_graph = (
            "ASCII export unavailable: install optional dependency `grandalf` "
            "inside the project venv to enable draw_ascii()."
        )
    (OUTPUT_DIR / "document_evaluation_langgraph.txt").write_text(
        ascii_graph,
        encoding="utf-8",
    )


def _svg_box(
    x: int,
    y: int,
    width: int,
    height: int,
    text: str,
    fill: str,
    font_size: int = 15,
) -> str:
    lines = wrap(text, width=20) or [text]
    tspans = []
    for index, line in enumerate(lines):
        dy = 0 if index == 0 else 17
        tspans.append(
            f'<tspan x="{x + width / 2}" dy="{dy}">{escape_xml(line)}</tspan>'
        )
    return (
        f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="16" '
        f'fill="{fill}" stroke="#243b53" stroke-width="2"/>'
        f'<text x="{x + width / 2}" y="{y + 30}" text-anchor="middle" '
        f'font-family="Arial, sans-serif" font-size="{font_size}" fill="#102a43">'
        + "".join(tspans)
        + "</text>"
    )


def _svg_arrow(
    x1: int,
    y1: int,
    x2: int,
    y2: int,
    label: Optional[str] = None,
    dashed: bool = False,
) -> str:
    dash = ' stroke-dasharray="7 5"' if dashed else ""
    mid_x = (x1 + x2) / 2
    mid_y = (y1 + y2) / 2
    label_markup = ""
    if label:
        label_markup = (
            f'<text x="{mid_x}" y="{mid_y - 8}" text-anchor="middle" '
            f'font-family="Arial, sans-serif" font-size="13" fill="#334e68">'
            f"{escape_xml(label)}</text>"
        )
    return (
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#486581" '
        f'stroke-width="2.5" marker-end="url(#arrowhead)"{dash}/>'
        + label_markup
    )


def escape_xml(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def save_svg_artifact() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    width = 2300
    height = 1160
    nodes = {
        "start": (60, 500, 160, 70, "START", "#d9f99d"),
        "summary": (270, 470, 220, 110, "Document Summarization", "#bfdbfe"),
        "summary_validate": (550, 470, 220, 110, "Validate DocumentSummary schema", "#c7d2fe"),
        "agent1": (860, 230, 220, 120, "Agent 1 Course Context", "#fde68a"),
        "agent1_validate": (1140, 230, 220, 120, "Validate Agent 1 schema", "#fef3c7"),
        "agent2": (860, 710, 220, 120, "Agent 2 Internet Search", "#fde68a"),
        "agent2_validate": (1140, 710, 220, 120, "Validate Agent 2 schema", "#fef3c7"),
        "agent3": (1450, 470, 220, 120, "Agent 3 Quality Evaluation", "#fbcfe8"),
        "agent3_validate": (1730, 470, 220, 120, "Validate Agent 3 schema", "#f9a8d4"),
        "rec_approve": (1450, 190, 220, 90, "Recommendation APPROVE", "#bbf7d0"),
        "rec_review": (1730, 190, 220, 90, "Recommendation NEEDS_REVIEW", "#fed7aa"),
        "rec_reject": (2010, 190, 220, 90, "Recommendation REJECT", "#fecaca"),
        "persist": (2010, 470, 220, 120, "Persist EvaluationReport", "#bae6fd"),
        "route": (2010, 710, 220, 110, "Route review queue", "#d8b4fe"),
        "reviewer_queue": (1740, 920, 220, 95, "Reviewer queue", "#e9d5ff"),
        "admin_queue": (2010, 920, 220, 95, "Admin queue", "#e9d5ff"),
        "manual_review": (1450, 920, 220, 95, "Manual review + label confirmation", "#fdba74"),
        "approve_final": (1180, 920, 220, 95, "Final APPROVED", "#86efac"),
        "reject_final": (900, 920, 220, 95, "Final REJECTED", "#fca5a5"),
        "failed": (860, 470, 220, 90, "FAILED", "#fecdd3"),
    }

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        "<defs>",
        '<marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">',
        '<polygon points="0 0, 10 3.5, 0 7" fill="#486581"/>',
        "</marker>",
        "</defs>",
        '<rect width="100%" height="100%" fill="#f8fafc"/>',
        '<text x="50%" y="44" text-anchor="middle" font-family="Arial, sans-serif" font-size="28" fill="#102a43">Document Evaluation State Diagram</text>',
        '<text x="50%" y="74" text-anchor="middle" font-family="Arial, sans-serif" font-size="15" fill="#486581">Assumption: follow SRS FR-HR-01, so recommendations are internal and all successful pipeline runs enter NEEDS_REVIEW.</text>',
        '<text x="380" y="150" text-anchor="middle" font-family="Arial, sans-serif" font-size="18" fill="#334e68">Pipeline</text>',
        '<text x="1850" y="150" text-anchor="middle" font-family="Arial, sans-serif" font-size="18" fill="#334e68">Recommendation + HITL</text>',
    ]

    for x, y, w, h, text, fill in nodes.values():
        parts.append(_svg_box(x, y, w, h, text, fill))

    parts.extend(
        [
            _svg_arrow(220, 535, 270, 535),
            _svg_arrow(490, 535, 550, 535),
            _svg_arrow(770, 510, 860, 290, "valid"),
            _svg_arrow(770, 560, 860, 515, "invalid"),
            _svg_arrow(770, 560, 860, 770, "valid"),
            _svg_arrow(1080, 290, 1140, 290),
            _svg_arrow(1080, 770, 1140, 770),
            _svg_arrow(1360, 290, 1450, 530),
            _svg_arrow(1360, 770, 1450, 530),
            _svg_arrow(1360, 290, 860, 515, "schema fail", dashed=True),
            _svg_arrow(1360, 770, 860, 515, "schema fail", dashed=True),
            _svg_arrow(1670, 530, 1730, 530),
            _svg_arrow(1950, 500, 2010, 235, "APPROVE", dashed=True),
            _svg_arrow(1950, 530, 1730, 235, "NEEDS_REVIEW", dashed=True),
            _svg_arrow(1950, 560, 2010, 235, "REJECT", dashed=True),
            _svg_arrow(1560, 280, 2060, 470),
            _svg_arrow(1840, 280, 2120, 470),
            _svg_arrow(2120, 280, 2180, 470),
            _svg_arrow(2120, 590, 2120, 710),
            _svg_arrow(2010, 780, 1850, 920, "reviewer exists"),
            _svg_arrow(2120, 820, 2120, 920, "no reviewer"),
            _svg_arrow(1850, 1015, 1560, 967, "SLA ok"),
            _svg_arrow(1850, 1015, 2120, 920, "SLA breach", dashed=True),
            _svg_arrow(2120, 1015, 1560, 967),
            _svg_arrow(1450, 967, 1400, 967, "approve"),
            _svg_arrow(1450, 992, 1120, 967, "reject"),
        ]
    )

    parts.append("</svg>")
    (OUTPUT_DIR / "document_evaluation_langgraph.svg").write_text(
        "".join(parts),
        encoding="utf-8",
    )


def main() -> None:
    graph = build_graph()
    save_text_artifacts(graph)
    save_svg_artifact()
    print(f"Artifacts written to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
