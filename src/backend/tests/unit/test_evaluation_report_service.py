from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from app.llm import DeterministicEmbeddingService
from app.models import ContributionType, EvaluationReport
from app.services.evaluation_report_service import (
    ExistingSummaryEmbedding,
    build_agent1_output,
    build_agent3_output,
    build_empty_agent2_output,
    upsert_evaluation_report,
)


class FakeScalarResult:
    def __init__(self, items: list[EvaluationReport]) -> None:
        self._items = items

    def all(self) -> list[EvaluationReport]:
        return list(self._items)


class FakeEvaluationSession:
    def __init__(self, reports: list[EvaluationReport] | None = None) -> None:
        self.reports = reports or []
        self.added: list[object] = []
        self.flush_count = 0

    async def scalars(self, query) -> FakeScalarResult:
        return FakeScalarResult(self.reports)

    def add(self, item: object) -> None:
        self.added.append(item)
        if isinstance(item, EvaluationReport) and item not in self.reports:
            self.reports.append(item)

    async def flush(self) -> None:
        self.flush_count += 1


def test_build_agent1_output_detects_duplicate_and_cold_start_reason() -> None:
    embeddings = DeterministicEmbeddingService()
    current_vector = embeddings.encode(["consensus and quorum systems"])[0]
    duplicate_vector = embeddings.encode(["consensus and quorum systems"])[0]

    payload = build_agent1_output(
        syllabus_topic_summary="Consensus, replication, quorum systems",
        existing_document_count=1,
        has_seed_document=False,
        summary_embedding=current_vector,
        approved_summaries=[
            ExistingSummaryEmbedding(document_id=uuid4(), summary_embedding=duplicate_vector),
        ],
        topic_coverage={"consensus": "covered"},
    )

    assert payload.duplicate.is_duplicate is True
    assert payload.duplicate.duplicate_of_document_id is not None
    assert payload.cold_start.is_cold_start is True
    assert payload.cold_start.reason == "no_seed_document"


def test_build_agent3_output_prioritizes_duplicate_over_high_scores() -> None:
    agent1 = build_agent1_output(
        syllabus_topic_summary="Databases and transactions",
        existing_document_count=5,
        has_seed_document=True,
        summary_embedding=[1.0, 0.0, 0.0],
        approved_summaries=[ExistingSummaryEmbedding(document_id=uuid4(), summary_embedding=[1.0, 0.0, 0.0])],
    )

    payload = build_agent3_output(
        relevance=9.2,
        completeness=8.5,
        quality=8.0,
        initial_contribution_type=ContributionType.SUMMARY_NOTE,
        suggested_contribution_type=ContributionType.SUMMARY_NOTE,
        label_confidence=0.95,
        agent1_output=agent1,
    )

    assert payload.recommendation == "REJECT"
    assert payload.duplicate_flag is True
    assert "Duplicate" in payload.recommendation_reasons[0]


def test_build_agent3_output_prioritizes_cold_start_over_approve() -> None:
    agent1 = build_agent1_output(
        syllabus_topic_summary="Computer networks",
        existing_document_count=2,
        has_seed_document=True,
        summary_embedding=[0.0, 1.0, 0.0],
        approved_summaries=[],
    )

    payload = build_agent3_output(
        relevance=8.4,
        completeness=7.2,
        quality=7.0,
        initial_contribution_type="review_note",
        suggested_contribution_type="summary_note",
        label_confidence=0.62,
        agent1_output=agent1,
    )

    assert payload.recommendation == "NEEDS_REVIEW"
    assert payload.cold_start_flag is True
    assert "cold-start" in payload.recommendation_reasons[0]
    assert payload.label_verification.label_mismatch is True


async def test_upsert_evaluation_report_marks_previous_latest_false() -> None:
    document_id = uuid4()
    old_report = EvaluationReport(
        id=uuid4(),
        document_id=document_id,
        evaluation_job_id=uuid4(),
        is_latest=True,
        agent1_output={},
        agent2_output={},
        agent3_output={},
        final_recommendation="APPROVE",
    )
    session = FakeEvaluationSession(reports=[old_report])
    agent1 = build_agent1_output(
        syllabus_topic_summary="Distributed systems",
        existing_document_count=4,
        has_seed_document=True,
        summary_embedding=[0.0, 1.0, 0.0],
        approved_summaries=[],
    )
    agent3 = build_agent3_output(
        relevance=7.8,
        completeness=7.0,
        quality=7.1,
        initial_contribution_type="summary_note",
        suggested_contribution_type="summary_note",
        label_confidence=0.88,
        agent1_output=agent1,
    )

    report, envelope = await upsert_evaluation_report(
        session,
        document_id=document_id,
        evaluation_job_id=uuid4(),
        course_code="IT4062",
        agent1_output=agent1,
        agent2_output=build_empty_agent2_output(),
        agent3_output=agent3,
        generated_at=datetime(2026, 6, 3, 11, 0, tzinfo=UTC),
    )

    assert old_report.is_latest is False
    assert report.is_latest is True
    assert report.final_recommendation == "APPROVE"
    assert envelope.agent3_output.recommendation == "APPROVE"
    assert session.flush_count == 1


async def test_upsert_evaluation_report_updates_existing_job_report_in_place() -> None:
    document_id = uuid4()
    job_id = uuid4()
    existing_report = EvaluationReport(
        id=uuid4(),
        document_id=document_id,
        evaluation_job_id=job_id,
        is_latest=False,
        agent1_output={"stale": True},
        agent2_output={"stale": True},
        agent3_output={"stale": True},
        final_recommendation="APPROVE",
    )
    session = FakeEvaluationSession(reports=[existing_report])
    agent1 = build_agent1_output(
        syllabus_topic_summary="Software architecture",
        existing_document_count=3,
        has_seed_document=True,
        summary_embedding=[1.0, 0.0, 0.0],
        approved_summaries=[],
    )

    report, envelope = await upsert_evaluation_report(
        session,
        document_id=document_id,
        evaluation_job_id=job_id,
        course_code="IT3150",
        agent1_output=agent1,
        agent2_output=None,
        agent3_output={
            "schema_version": "1.0",
            "scores": {
                "relevance": 3.5,
                "completeness": 8.0,
                "quality": 8.0,
            },
            "label_verification": {
                "initial_contribution_type": "summary_note",
                "suggested_contribution_type": "summary_note",
                "label_confidence": 0.9,
                "label_mismatch": False,
            },
            "recommendation": "APPROVE",
            "recommendation_reasons": ["stale reason"],
            "duplicate_flag": False,
            "cold_start_flag": False,
        },
        generated_at=datetime(2026, 6, 3, 12, 0, tzinfo=UTC),
    )

    assert report is existing_report
    assert report.is_latest is True
    assert report.final_recommendation == "REJECT"
    assert envelope.agent3_output.recommendation == "REJECT"
    assert "reject threshold" in envelope.agent3_output.recommendation_reasons[0]
    assert session.flush_count == 1


def test_build_agent3_output_with_custom_justification() -> None:
    agent1 = build_agent1_output(
        syllabus_topic_summary="Algorithms",
        existing_document_count=5,
        has_seed_document=True,
        summary_embedding=[1.0, 0.0, 0.0],
        approved_summaries=[],
    )

    justification = {
        "relevance_rationale": "Perfect relevance match.",
        "completeness_rationale": "High completeness.",
        "quality_rationale": "Excellent quality.",
        "overall_rationale": "Document looks great."
    }

    payload = build_agent3_output(
        relevance=9.0,
        completeness=9.0,
        quality=9.0,
        initial_contribution_type=ContributionType.SUMMARY_NOTE,
        suggested_contribution_type=ContributionType.SUMMARY_NOTE,
        label_confidence=0.9,
        agent1_output=agent1,
        evaluation_justification=justification,
    )

    assert payload.evaluation_justification.relevance_rationale == "Perfect relevance match."
    assert payload.evaluation_justification.overall_rationale == "Document looks great."


def test_normalize_agent3_output_injects_fallback_justification() -> None:
    agent1 = build_agent1_output(
        syllabus_topic_summary="Algorithms",
        existing_document_count=5,
        has_seed_document=True,
        summary_embedding=[1.0, 0.0, 0.0],
        approved_summaries=[],
    )

    # Missing evaluation_justification dict
    agent3_dict = {
        "schema_version": "1.0",
        "scores": {
            "relevance": 8.0,
            "completeness": 8.0,
            "quality": 8.0,
        },
        "label_verification": {
            "initial_contribution_type": "summary_note",
            "suggested_contribution_type": "summary_note",
            "label_confidence": 0.9,
            "label_mismatch": False,
        },
        "recommendation": "APPROVE",
        "recommendation_reasons": ["Good doc"],
        "duplicate_flag": False,
        "cold_start_flag": False,
    }

    from app.services.evaluation_report_service import normalize_agent3_output
    payload = normalize_agent3_output(agent1, agent3_dict)

    assert payload.evaluation_justification is not None
    assert "Relevance score" in payload.evaluation_justification.relevance_rationale


def test_build_agent1_output_with_precalculated_duplicate() -> None:
    payload = build_agent1_output(
        syllabus_topic_summary="Algorithms",
        existing_document_count=5,
        has_seed_document=True,
        is_duplicate=True,
        duplicate_of_document_id=uuid4(),
        similarity_score=0.96,
    )

    assert payload.duplicate.is_duplicate is True
    assert payload.duplicate.duplicate_of_document_id is not None
    assert payload.duplicate.similarity_score == 0.96

