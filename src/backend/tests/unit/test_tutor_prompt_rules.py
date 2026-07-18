from __future__ import annotations

from app.services.tutor_service import (
    _FINAL_ANSWER_INSTRUCTION,
    _TUTOR_SYSTEM_PROMPT_TEMPLATE,
)


def test_template_still_formats_with_placeholders() -> None:
    rendered = _TUTOR_SYSTEM_PROMPT_TEMPLATE.format(
        course_code="IT3160E", course_name="Intro to AI", topic_summary="agents, search"
    )
    assert "IT3160E" in rendered


def test_forbids_outside_knowledge_with_greeting_exception() -> None:
    t = _TUTOR_SYSTEM_PROMPT_TEMPLATE.lower()
    assert "only the retrieved context" in t
    assert "general" in t and "knowledge" in t  # forbids general knowledge
    assert "greeting" in t  # explicit exception
    assert "general" in _FINAL_ANSWER_INSTRUCTION.lower()


def test_query_optimization_rule_with_example() -> None:
    t = _TUTOR_SYSTEM_PROMPT_TEMPLATE
    assert "rewrite" in t.lower()  # instruction to rewrite the query
    assert "Optimized query" in t  # the worked example is present
    # the example still parses as a format-safe template (no odd single braces)
    _ = t.format(course_code="X", course_name="Y", topic_summary="Z")
