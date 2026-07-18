from __future__ import annotations

import math
from collections.abc import Iterable
from datetime import UTC, datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import ContributionType, EvaluationReport

EVALUATION_SCHEMA_VERSION = "1.0"
DEFAULT_PIPELINE_VERSION = "phase-c-deterministic-v1"
DUPLICATE_THRESHOLD = 0.92  # Legacy threshold for summary-level cosine similarity tests
REJECT_RELEVANCE_THRESHOLD = 4.0
APPROVE_RELEVANCE_THRESHOLD = 7.0


class ExistingSummaryEmbedding(BaseModel):
    model_config = ConfigDict(extra="forbid")

    document_id: UUID
    summary_embedding: list[float] | None = None


class Agent1CourseContextPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    syllabus_topic_summary: str
    existing_document_count: int = Field(ge=0)
    topic_coverage: dict[str, str]
    course_knowledge_state: str


class Agent1DuplicatePayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    is_duplicate: bool
    duplicate_of_document_id: UUID | None
    similarity_score: float = Field(ge=0, le=1)


class Agent1ColdStartPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    is_cold_start: bool
    reason: str | None = None


class Agent1OutputPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: str = Field(default=EVALUATION_SCHEMA_VERSION, pattern=r"^1\.0$")
    course_context: Agent1CourseContextPayload
    duplicate: Agent1DuplicatePayload
    cold_start: Agent1ColdStartPayload


class Agent2ReferencePayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str
    url: str
    snippet: str
    source_type: str


class Agent2OutputPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: str = Field(default=EVALUATION_SCHEMA_VERSION, pattern=r"^1\.0$")
    references: list[Agent2ReferencePayload]
    search_status: str = Field(pattern=r"^(success|timeout|error)$")
    search_duration_ms: int = Field(ge=0)


class EvaluationScoresPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    relevance: float = Field(ge=0, le=10)
    completeness: float = Field(ge=0, le=10)
    quality: float = Field(ge=0, le=10)


class LabelVerificationPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    initial_contribution_type: ContributionType
    suggested_contribution_type: ContributionType
    label_confidence: float = Field(ge=0, le=1)
    label_mismatch: bool


class EvaluationJustificationPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    relevance_rationale: str
    completeness_rationale: str
    quality_rationale: str
    overall_rationale: str


class Agent3OutputPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: str = Field(default=EVALUATION_SCHEMA_VERSION, pattern=r"^1\.0$")
    scores: EvaluationScoresPayload
    label_verification: LabelVerificationPayload
    recommendation: str = Field(pattern=r"^(APPROVE|NEEDS_REVIEW|REJECT)$")
    recommendation_reasons: list[str]
    duplicate_flag: bool
    cold_start_flag: bool
    evaluation_justification: EvaluationJustificationPayload


class EvaluationReportEnvelope(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: str = Field(default=EVALUATION_SCHEMA_VERSION, pattern=r"^1\.0$")
    document_id: UUID
    course_code: str
    pipeline_version: str
    created_at: datetime
    agent1_output: Agent1OutputPayload
    agent2_output: Agent2OutputPayload
    agent3_output: Agent3OutputPayload


def build_agent1_output(
    *,
    syllabus_topic_summary: str | None,
    existing_document_count: int,
    has_seed_document: bool,
    summary_embedding: Iterable[float] | None = None,
    approved_summaries: Iterable[ExistingSummaryEmbedding] = (),
    topic_coverage: dict[str, str] | None = None,
    duplicate_threshold: float = DUPLICATE_THRESHOLD,
    course_knowledge_state: str = "",
    is_duplicate: bool | None = None,
    duplicate_of_document_id: UUID | None = None,
    similarity_score: float | None = None,
) -> Agent1OutputPayload:
    if is_duplicate is not None:
        best_similarity = similarity_score if similarity_score is not None else (1.0 if is_duplicate else 0.0)
        best_id = duplicate_of_document_id
        is_dup = is_duplicate
    else:
        best_id = None
        best_similarity = 0.0
        current_embedding = list(summary_embedding) if summary_embedding is not None else None

        if current_embedding:
            for approved in approved_summaries:
                if approved.summary_embedding is None:
                    continue
                similarity = _cosine_similarity(current_embedding, approved.summary_embedding)
                if similarity > best_similarity:
                    best_similarity = similarity
                    best_id = approved.document_id
        is_dup = best_similarity >= duplicate_threshold

    cold_start_reason: str | None = None
    if not has_seed_document:
        cold_start_reason = "no_seed_document"
    elif existing_document_count < 3:
        cold_start_reason = "fewer_than_3_approved_docs"

    return Agent1OutputPayload(
        course_context=Agent1CourseContextPayload(
            syllabus_topic_summary=syllabus_topic_summary or "",
            existing_document_count=existing_document_count,
            topic_coverage=topic_coverage or {},
            course_knowledge_state=course_knowledge_state,
        ),
        duplicate=Agent1DuplicatePayload(
            is_duplicate=is_dup,
            duplicate_of_document_id=best_id,
            similarity_score=round(best_similarity, 6),
        ),
        cold_start=Agent1ColdStartPayload(
            is_cold_start=cold_start_reason is not None,
            reason=cold_start_reason,
        ),
    )


def build_empty_agent2_output(*, search_status: str = "error", duration_ms: int = 0) -> Agent2OutputPayload:
    return Agent2OutputPayload(
        references=[],
        search_status=search_status,
        search_duration_ms=duration_ms,
    )


def build_agent3_output(
    *,
    relevance: float,
    completeness: float,
    quality: float,
    initial_contribution_type: ContributionType | str,
    suggested_contribution_type: ContributionType | str,
    label_confidence: float,
    agent1_output: Agent1OutputPayload | dict[str, Any],
    evaluation_justification: EvaluationJustificationPayload | dict[str, Any] | None = None,
) -> Agent3OutputPayload:
    agent1 = Agent1OutputPayload.model_validate(agent1_output)
    initial = ContributionType(initial_contribution_type)
    suggested = ContributionType(suggested_contribution_type)
    recommendation, reasons = _recommendation_from_rules(
        relevance=relevance,
        duplicate=agent1.duplicate.is_duplicate,
        duplicate_id=agent1.duplicate.duplicate_of_document_id,
        similarity=agent1.duplicate.similarity_score,
        cold_start=agent1.cold_start.is_cold_start,
        cold_start_reason=agent1.cold_start.reason,
    )

    label_mismatch = initial != suggested
    if label_mismatch:
        reasons.append(
            "Contribution type mismatch: "
            f"uploader selected '{initial.value}', suggested '{suggested.value}'."
        )

    if evaluation_justification is None:
        relevance_rat = f"Relevance score of {relevance:.2f}/10.0 reflects document content alignment."
        completeness_rat = f"Completeness score of {completeness:.2f}/10.0 reflects coverage of syllabus topics."
        quality_rat = f"Quality score of {quality:.2f}/10.0 reflects academic depth and clarity of the content."
        overall_rat = f"Auto-generated evaluation recommendation: {recommendation} based on priority rules."
        justification = EvaluationJustificationPayload(
            relevance_rationale=relevance_rat,
            completeness_rationale=completeness_rat,
            quality_rationale=quality_rat,
            overall_rationale=overall_rat,
        )
    elif isinstance(evaluation_justification, dict):
        justification = EvaluationJustificationPayload.model_validate(evaluation_justification)
    else:
        justification = evaluation_justification

    return Agent3OutputPayload(
        scores=EvaluationScoresPayload(
            relevance=relevance,
            completeness=completeness,
            quality=quality,
        ),
        label_verification=LabelVerificationPayload(
            initial_contribution_type=initial,
            suggested_contribution_type=suggested,
            label_confidence=label_confidence,
            label_mismatch=label_mismatch,
        ),
        recommendation=recommendation,
        recommendation_reasons=reasons,
        duplicate_flag=agent1.duplicate.is_duplicate,
        cold_start_flag=agent1.cold_start.is_cold_start,
        evaluation_justification=justification,
    )


def build_evaluation_report_envelope(
    *,
    document_id: UUID,
    course_code: str,
    agent1_output: Agent1OutputPayload | dict[str, Any],
    agent2_output: Agent2OutputPayload | dict[str, Any] | None,
    agent3_output: Agent3OutputPayload | dict[str, Any],
    pipeline_version: str = DEFAULT_PIPELINE_VERSION,
    created_at: datetime | None = None,
) -> EvaluationReportEnvelope:
    parsed_agent1 = Agent1OutputPayload.model_validate(agent1_output)
    parsed_agent2 = (
        Agent2OutputPayload.model_validate(agent2_output)
        if agent2_output is not None
        else build_empty_agent2_output()
    )
    parsed_agent3 = normalize_agent3_output(parsed_agent1, agent3_output)

    return EvaluationReportEnvelope(
        document_id=document_id,
        course_code=course_code,
        pipeline_version=pipeline_version,
        created_at=created_at or datetime.now(UTC),
        agent1_output=parsed_agent1,
        agent2_output=parsed_agent2,
        agent3_output=parsed_agent3,
    )


def normalize_agent3_output(
    agent1_output: Agent1OutputPayload | dict[str, Any],
    agent3_output: Agent3OutputPayload | dict[str, Any],
) -> Agent3OutputPayload:
    agent1 = Agent1OutputPayload.model_validate(agent1_output)
    
    if isinstance(agent3_output, dict) and "evaluation_justification" not in agent3_output:
        scores = agent3_output.get("scores", {})
        relevance = scores.get("relevance", 0.0) if isinstance(scores, dict) else 0.0
        completeness = scores.get("completeness", 0.0) if isinstance(scores, dict) else 0.0
        quality = scores.get("quality", 0.0) if isinstance(scores, dict) else 0.0
        rec = agent3_output.get("recommendation", "APPROVE")
        agent3_output = dict(agent3_output)
        agent3_output["evaluation_justification"] = {
            "relevance_rationale": (
                f"Relevance score of {relevance:.2f}/10.0 "
                f"reflects document content alignment."
            ),
            "completeness_rationale": (
                f"Completeness score of {completeness:.2f}/10.0 "
                f"reflects coverage of syllabus topics."
            ),
            "quality_rationale": (
                f"Quality score of {quality:.2f}/10.0 "
                f"reflects academic depth and clarity of the content."
            ),
            "overall_rationale": (
                f"Auto-generated evaluation recommendation: {rec} "
                f"based on priority rules."
            ),
        }

    agent3 = Agent3OutputPayload.model_validate(agent3_output)
    return build_agent3_output(
        relevance=agent3.scores.relevance,
        completeness=agent3.scores.completeness,
        quality=agent3.scores.quality,
        initial_contribution_type=agent3.label_verification.initial_contribution_type,
        suggested_contribution_type=agent3.label_verification.suggested_contribution_type,
        label_confidence=agent3.label_verification.label_confidence,
        agent1_output=agent1,
        evaluation_justification=agent3.evaluation_justification,
    )


async def upsert_evaluation_report(
    session: AsyncSession,
    *,
    document_id: UUID,
    evaluation_job_id: UUID,
    course_code: str,
    agent1_output: Agent1OutputPayload | dict[str, Any],
    agent2_output: Agent2OutputPayload | dict[str, Any] | None,
    agent3_output: Agent3OutputPayload | dict[str, Any],
    pipeline_version: str = DEFAULT_PIPELINE_VERSION,
    generated_at: datetime | None = None,
) -> tuple[EvaluationReport, EvaluationReportEnvelope]:
    envelope = build_evaluation_report_envelope(
        document_id=document_id,
        course_code=course_code,
        agent1_output=agent1_output,
        agent2_output=agent2_output,
        agent3_output=agent3_output,
        pipeline_version=pipeline_version,
        created_at=generated_at,
    )

    existing_reports_result = await session.scalars(
        select(EvaluationReport).where(EvaluationReport.document_id == document_id)
    )
    existing_reports = list(existing_reports_result.all())
    report = next((item for item in existing_reports if item.evaluation_job_id == evaluation_job_id), None)

    for item in existing_reports:
        item.is_latest = False

    timestamp = generated_at or datetime.now(UTC)
    if report is None:
        report = EvaluationReport(
            document_id=document_id,
            evaluation_job_id=evaluation_job_id,
            generated_at=timestamp,
        )

    report.is_latest = True
    report.schema_version = envelope.schema_version
    report.agent1_output = envelope.agent1_output.model_dump(mode="json")
    report.agent2_output = envelope.agent2_output.model_dump(mode="json")
    report.agent3_output = envelope.agent3_output.model_dump(mode="json")
    report.final_recommendation = envelope.agent3_output.recommendation
    report.generated_at = timestamp

    session.add(report)
    await session.flush()
    return report, envelope


def _recommendation_from_rules(
    *,
    relevance: float,
    duplicate: bool,
    duplicate_id: UUID | None,
    similarity: float,
    cold_start: bool,
    cold_start_reason: str | None,
) -> tuple[str, list[str]]:
    if duplicate:
        target = f" of document {duplicate_id}" if duplicate_id is not None else ""
        return (
            "REJECT",
            [f"Duplicate{target} detected with similarity {similarity:.3f}."],
        )

    if relevance < REJECT_RELEVANCE_THRESHOLD and not cold_start:
        return (
            "REJECT",
            [f"Relevance score {relevance:.2f} is below the reject threshold {REJECT_RELEVANCE_THRESHOLD:.1f}."],
        )

    if cold_start:
        reason = cold_start_reason or "cold_start"
        return (
            "NEEDS_REVIEW",
            [f"Course is in cold-start mode ({reason})."],
        )

    if relevance < APPROVE_RELEVANCE_THRESHOLD:
        return (
            "NEEDS_REVIEW",
            [
                "Relevance score "
                f"{relevance:.2f} falls inside the reviewer buffer "
                f"[{REJECT_RELEVANCE_THRESHOLD:.1f}, {APPROVE_RELEVANCE_THRESHOLD:.1f})."
            ],
        )

    return (
        "APPROVE",
        [f"Relevance score {relevance:.2f} meets the auto-approve threshold {APPROVE_RELEVANCE_THRESHOLD:.1f}."],
    )


def _cosine_similarity(left: Iterable[float], right: Iterable[float]) -> float:
    left_values = list(left)
    right_values = list(right)
    if len(left_values) != len(right_values) or not left_values:
        return 0.0

    numerator = sum(a * b for a, b in zip(left_values, right_values, strict=False))
    left_norm = math.sqrt(sum(value * value for value in left_values))
    right_norm = math.sqrt(sum(value * value for value in right_values))
    if left_norm == 0 or right_norm == 0:
        return 0.0
    return max(0.0, min(1.0, numerator / (left_norm * right_norm)))


__all__ = [
    "Agent1OutputPayload",
    "Agent2OutputPayload",
    "Agent3OutputPayload",
    "DEFAULT_PIPELINE_VERSION",
    "EvaluationReportEnvelope",
    "EvaluationJustificationPayload",
    "ExistingSummaryEmbedding",
    "build_agent1_output",
    "build_agent3_output",
    "build_empty_agent2_output",
    "build_evaluation_report_envelope",
    "normalize_agent3_output",
    "upsert_evaluation_report",
]
