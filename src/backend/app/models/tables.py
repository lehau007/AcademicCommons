from __future__ import annotations

from collections.abc import Callable
from datetime import datetime
from enum import StrEnum
from typing import Any
from uuid import UUID

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    Float,
    ForeignKey,
    ForeignKeyConstraint,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
    text,
)
from sqlalchemy.dialects.postgresql import ENUM, JSONB
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, MappedColumn, mapped_column, relationship
from sqlalchemy.types import UserDefinedType

from app.db.base import Base
from app.models.enums import (
    ChatRole,
    ContributionType,
    Difficulty,
    DocumentStatus,
    DocumentTier,
    FileFormat,
    JobStatus,
    Language,
    MaterialType,
    OcrQuality,
    ProcessingJobType,
    QuestionType,
    RagNamespace,
)


class Vector(UserDefinedType[Any]):
    cache_ok = True

    def __init__(self, dimension: int) -> None:
        self.dimension = dimension

    def get_col_spec(self, **kw: Any) -> str:
        return f"vector({self.dimension})"

    def bind_processor(self, dialect: Any) -> Callable[[Any], str | None]:
        del dialect

        def process(value: Any) -> str | None:
            if value is None:
                return None
            if isinstance(value, str):
                return value
            return "[" + ",".join(str(float(component)) for component in value) + "]"

        return process

    def result_processor(self, dialect: Any, coltype: Any) -> Callable[[Any], list[float] | None]:
        del dialect, coltype

        def process(value: Any) -> list[float] | None:
            if value is None:
                return None
            if isinstance(value, str):
                stripped = value.strip()
                if stripped.startswith("[") and stripped.endswith("]"):
                    stripped = stripped[1:-1]
                if not stripped:
                    return []
                return [float(component) for component in stripped.split(",")]
            return [float(component) for component in value]

        return process


def pg_enum(enum_class: type[StrEnum], name: str) -> ENUM:
    return ENUM(
        enum_class,
        name=name,
        values_callable=lambda values: [item.value for item in values],
        create_type=False,
    )


timestamp_now = text("now()")


def uuid_pk_col() -> MappedColumn[UUID]:
    return mapped_column(PG_UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))


class Course(Base):
    __tablename__ = "courses"

    id: Mapped[UUID] = uuid_pk_col()
    code: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    topic_summary: Mapped[str | None] = mapped_column(Text)
    short_description: Mapped[str | None] = mapped_column(Text)
    topic_tags: Mapped[list[str]] = mapped_column(JSONB, server_default=text("'[]'::jsonb"))
    review_sla_hours: Mapped[int] = mapped_column(Integer, server_default=text("48"))
    is_active: Mapped[bool] = mapped_column(Boolean, server_default=text("true"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=timestamp_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=timestamp_now)

    documents: Mapped[list[Document]] = relationship(back_populates="course")
    reviewer_assignments: Mapped[list[CourseReviewerAssignment]] = relationship(back_populates="course")
    chat_sessions: Mapped[list[ChatSession]] = relationship(
        back_populates="course", cascade="all, delete-orphan"
    )
    summary_cache: Mapped[CourseSummaryCache | None] = relationship(
        back_populates="course", cascade="all, delete-orphan", uselist=False
    )

    __table_args__ = (CheckConstraint("review_sla_hours BETWEEN 24 AND 72", name="ck_courses_review_sla_hours"),)


class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = uuid_pk_col()
    email: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(Text, nullable=False)
    role: Mapped[str] = mapped_column(Text, nullable=False)
    full_name: Mapped[str | None] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, server_default=text("true"))
    is_email_verified: Mapped[bool] = mapped_column(Boolean, server_default=text("false"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=timestamp_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=timestamp_now)

    uploaded_documents: Mapped[list[Document]] = relationship(back_populates="uploader")
    reviewer_assignments: Mapped[list[CourseReviewerAssignment]] = relationship(
        back_populates="reviewer",
        foreign_keys="CourseReviewerAssignment.user_id",
    )
    created_reviewer_assignments: Mapped[list[CourseReviewerAssignment]] = relationship(
        back_populates="assigner",
        foreign_keys="CourseReviewerAssignment.assigned_by",
    )
    chat_sessions: Mapped[list[ChatSession]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    __table_args__ = (CheckConstraint("role IN ('student', 'reviewer', 'admin')", name="ck_users_role"),)


class CourseReviewerAssignment(Base):
    __tablename__ = "course_reviewer_assignments"

    id: Mapped[UUID] = uuid_pk_col()
    user_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    course_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("courses.id"), nullable=False)
    assigned_by: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, server_default=text("true"))
    assigned_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=timestamp_now)
    unassigned_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    reviewer: Mapped[User] = relationship(
        back_populates="reviewer_assignments",
        foreign_keys=[user_id],
    )
    assigner: Mapped[User] = relationship(
        back_populates="created_reviewer_assignments",
        foreign_keys=[assigned_by],
    )
    course: Mapped[Course] = relationship(back_populates="reviewer_assignments")

    __table_args__ = (
        Index(
            "idx_cra_active_unique",
            "user_id",
            "course_id",
            unique=True,
            postgresql_where=text("is_active = TRUE"),
        ),
        Index("idx_cra_course_active", "course_id", "is_active"),
    )


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[UUID] = uuid_pk_col()
    course_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("courses.id"), nullable=False)
    uploader_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    document_tier: Mapped[DocumentTier] = mapped_column(pg_enum(DocumentTier, "doc_tier"), nullable=False)
    material_type: Mapped[MaterialType | None] = mapped_column(pg_enum(MaterialType, "material_type_enum"))
    contribution_type: Mapped[ContributionType | None] = mapped_column(
        pg_enum(ContributionType, "contribution_type_enum")
    )
    topic_tags: Mapped[list[str]] = mapped_column(JSONB, server_default=text("'[]'::jsonb"))
    status: Mapped[DocumentStatus] = mapped_column(
        pg_enum(DocumentStatus, "doc_status"),
        nullable=False,
        server_default=text("'UPLOADED'::doc_status"),
    )
    version: Mapped[int] = mapped_column(Integer, server_default=text("1"))
    is_active_version: Mapped[bool] = mapped_column(Boolean, server_default=text("true"))
    permanently_failed: Mapped[bool] = mapped_column(Boolean, server_default=text("false"))
    original_filename: Mapped[str] = mapped_column(Text, nullable=False)
    display_name: Mapped[str | None] = mapped_column(Text)
    file_format: Mapped[FileFormat] = mapped_column(pg_enum(FileFormat, "file_format_enum"), nullable=False)
    storage_raw_path: Mapped[str | None] = mapped_column(Text)
    storage_md_path: Mapped[str | None] = mapped_column(Text)
    no_reviewer_flag: Mapped[bool] = mapped_column(Boolean, server_default=text("false"))
    sla_breached: Mapped[bool] = mapped_column(Boolean, server_default=text("false"))
    sla_deadline: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    uploaded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=timestamp_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=timestamp_now)

    course: Mapped[Course] = relationship(back_populates="documents")
    uploader: Mapped[User] = relationship(back_populates="uploaded_documents")

    @property
    def course_code(self) -> str | None:
        from sqlalchemy.orm import attributes
        if "course" in attributes.instance_state(self).unloaded:
            return None
        return self.course.code if self.course else None

    @property
    def reviewer_note(self) -> str | None:
        from sqlalchemy.orm import attributes
        if "state_logs" in attributes.instance_state(self).unloaded:
            return None
        logs = sorted(self.state_logs, key=lambda l: l.uploaded_at if hasattr(l, 'uploaded_at') else (l.transitioned_at if hasattr(l, 'transitioned_at') else l.id), reverse=True)
        for log in logs:
            if log.to_state.value in ("REJECTED", "FAILED") and log.reason:
                return log.reason
            if log.to_state.value == "APPROVED" and log.reason:
                return log.reason
        return None
    summary: Mapped[DocumentSummary | None] = relationship(back_populates="document", cascade="all, delete-orphan")
    chunks: Mapped[list[DocumentChunk]] = relationship(back_populates="document", cascade="all, delete-orphan")
    state_logs: Mapped[list[DocumentStateLog]] = relationship(back_populates="document")
    evaluation_jobs: Mapped[list[EvaluationJob]] = relationship(back_populates="document")
    evaluation_reports: Mapped[list[EvaluationReport]] = relationship(back_populates="document")
    processing_jobs: Mapped[list[ProcessingJob]] = relationship(back_populates="document")

    __table_args__ = (
        CheckConstraint(
            """
            (document_tier = 'official' AND material_type IS NOT NULL AND contribution_type IS NULL)
            OR
            (document_tier = 'community' AND contribution_type IS NOT NULL AND material_type IS NULL)
            """,
            name="tier_type_check",
        ),
        Index("idx_doc_course_status_created", "course_id", "status", "uploaded_at"),
        Index("idx_doc_uploader", "uploader_id"),
        Index("idx_doc_status", "status"),
        Index(
            "idx_doc_official_active_version",
            "course_id",
            "material_type",
            unique=True,
            postgresql_where=text("document_tier = 'official' AND is_active_version = TRUE"),
        ),
    )


class DocumentSummary(Base):
    __tablename__ = "document_summaries"

    id: Mapped[UUID] = uuid_pk_col()
    document_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("documents.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )
    schema_version: Mapped[str] = mapped_column(Text, server_default=text("'1.0'"))
    topic: Mapped[str | None] = mapped_column(Text)
    concepts: Mapped[list[str]] = mapped_column(JSONB, server_default=text("'[]'::jsonb"))
    language: Mapped[Language | None] = mapped_column(pg_enum(Language, "language_enum"))
    ocr_quality: Mapped[OcrQuality | None] = mapped_column(pg_enum(OcrQuality, "ocr_quality_enum"))
    section_summaries: Mapped[list[dict[str, Any]]] = mapped_column(JSONB, server_default=text("'[]'::jsonb"))
    overall_summary: Mapped[str | None] = mapped_column(Text)
    summary_embedding: Mapped[list[float] | None] = mapped_column(Vector(1024))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=timestamp_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=timestamp_now)

    document: Mapped[Document] = relationship(back_populates="summary")

    __table_args__ = (
        Index(
            "idx_summary_embedding_hnsw",
            "summary_embedding",
            postgresql_using="hnsw",
            postgresql_with={"m": 16, "ef_construction": 64},
            postgresql_ops={"summary_embedding": "vector_cosine_ops"},
        ),
    )


class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id: Mapped[UUID] = uuid_pk_col()
    document_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("documents.id", ondelete="CASCADE"),
        nullable=False,
    )
    course_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("courses.id"), nullable=False)
    document_tier: Mapped[DocumentTier] = mapped_column(pg_enum(DocumentTier, "doc_tier"), nullable=False)
    subtype: Mapped[str | None] = mapped_column(Text)
    rag_namespace: Mapped[RagNamespace] = mapped_column(pg_enum(RagNamespace, "rag_namespace_enum"), nullable=False)
    section_title: Mapped[str | None] = mapped_column(Text)
    page_number: Mapped[int | None] = mapped_column(Integer)
    chunk_order: Mapped[int] = mapped_column(Integer, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    embedding: Mapped[list[float] | None] = mapped_column(Vector(1024))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=timestamp_now)

    document: Mapped[Document] = relationship(back_populates="chunks")
    course: Mapped[Course] = relationship()

    __table_args__ = (
        Index("idx_chunk_document", "document_id"),
        Index("idx_chunk_course_namespace", "course_id", "rag_namespace"),
        Index(
            "idx_chunk_embedding_hnsw",
            "embedding",
            postgresql_using="hnsw",
            postgresql_with={"m": 16, "ef_construction": 64},
            postgresql_ops={"embedding": "vector_cosine_ops"},
        ),
    )


class DocumentStateLog(Base):
    __tablename__ = "document_state_logs"

    id: Mapped[UUID] = uuid_pk_col()
    document_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("documents.id"), nullable=False)
    from_state: Mapped[DocumentStatus | None] = mapped_column(pg_enum(DocumentStatus, "doc_status"))
    to_state: Mapped[DocumentStatus] = mapped_column(pg_enum(DocumentStatus, "doc_status"), nullable=False)
    actor_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("users.id"))
    actor_type: Mapped[str] = mapped_column(Text, nullable=False)
    reason: Mapped[str | None] = mapped_column(Text)
    transitioned_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=timestamp_now)

    document: Mapped[Document] = relationship(back_populates="state_logs")
    actor: Mapped[User | None] = relationship()

    __table_args__ = (
        CheckConstraint("actor_type IN ('system', 'student', 'reviewer', 'admin')", name="ck_state_log_actor_type"),
        Index("idx_state_log_document", "document_id", "transitioned_at"),
    )


class EvaluationJob(Base):
    __tablename__ = "evaluation_jobs"

    id: Mapped[UUID] = uuid_pk_col()
    document_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("documents.id"), nullable=False)
    run_number: Mapped[int] = mapped_column(Integer, server_default=text("1"), nullable=False)
    is_latest: Mapped[bool] = mapped_column(Boolean, server_default=text("true"), nullable=False)
    status: Mapped[JobStatus] = mapped_column(
        pg_enum(JobStatus, "eval_job_status"),
        server_default=text("'PENDING'::eval_job_status"),
    )
    attempt_count: Mapped[int] = mapped_column(Integer, server_default=text("0"))
    failure_reason: Mapped[str | None] = mapped_column(Text)
    raw_failure_output: Mapped[dict[str, Any] | None] = mapped_column(JSONB)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=timestamp_now)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=timestamp_now)

    document: Mapped[Document] = relationship(back_populates="evaluation_jobs")
    report: Mapped[EvaluationReport | None] = relationship(
        back_populates="evaluation_job",
        overlaps="evaluation_reports",
    )

    __table_args__ = (
        UniqueConstraint("id", "document_id"),
        UniqueConstraint("document_id", "run_number"),
        CheckConstraint("attempt_count <= 3", name="ck_evaluation_jobs_attempt_count"),
        Index("idx_eval_job_latest", "document_id", unique=True, postgresql_where=text("is_latest = TRUE")),
        Index("idx_eval_job_status_updated", "status", "updated_at"),
        Index("idx_eval_job_document", "document_id", text("run_number DESC")),
    )


class EvaluationReport(Base):
    __tablename__ = "evaluation_reports"

    id: Mapped[UUID] = uuid_pk_col()
    document_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("documents.id"), nullable=False)
    evaluation_job_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), unique=True, nullable=False)
    is_latest: Mapped[bool] = mapped_column(Boolean, server_default=text("true"), nullable=False)
    schema_version: Mapped[str] = mapped_column(Text, server_default=text("'1.0'"))
    agent1_output: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)
    agent2_output: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)
    agent3_output: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)
    final_recommendation: Mapped[str] = mapped_column(Text, nullable=False)
    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=timestamp_now)

    document: Mapped[Document] = relationship(back_populates="evaluation_reports", overlaps="report")
    evaluation_job: Mapped[EvaluationJob] = relationship(
        back_populates="report",
        overlaps="document,evaluation_reports",
    )
    review_decision: Mapped[ReviewDecision | None] = relationship(back_populates="evaluation_report")

    __table_args__ = (
        ForeignKeyConstraint(
            ["evaluation_job_id", "document_id"],
            ["evaluation_jobs.id", "evaluation_jobs.document_id"],
        ),
        CheckConstraint(
            "final_recommendation IN ('APPROVE', 'NEEDS_REVIEW', 'REJECT')",
            name="ck_evaluation_reports_final_recommendation",
        ),
        Index("idx_eval_report_latest", "document_id", unique=True, postgresql_where=text("is_latest = TRUE")),
        Index("idx_eval_report_document", "document_id", text("generated_at DESC")),
    )


class ReviewDecision(Base):
    __tablename__ = "review_decisions"

    id: Mapped[UUID] = uuid_pk_col()
    evaluation_report_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("evaluation_reports.id"),
        unique=True,
        nullable=False,
    )
    reviewer_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    initial_contribution_type: Mapped[ContributionType | None] = mapped_column(
        pg_enum(ContributionType, "contribution_type_enum")
    )
    suggested_contribution_type: Mapped[ContributionType | None] = mapped_column(
        pg_enum(ContributionType, "contribution_type_enum")
    )
    final_contribution_type: Mapped[ContributionType | None] = mapped_column(
        pg_enum(ContributionType, "contribution_type_enum")
    )
    decision: Mapped[str] = mapped_column(Text, nullable=False)
    note: Mapped[str | None] = mapped_column(Text)
    decided_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=timestamp_now)

    evaluation_report: Mapped[EvaluationReport] = relationship(back_populates="review_decision")
    reviewer: Mapped[User] = relationship()

    __table_args__ = (
        CheckConstraint(
            "decision IN ('APPROVE', 'REJECT', 'OVERRIDE_APPROVE', 'OVERRIDE_REJECT')",
            name="ck_review_decisions_decision",
        ),
        CheckConstraint(
            "decision IN ('REJECT', 'OVERRIDE_REJECT') OR final_contribution_type IS NOT NULL",
            name="final_type_required_on_approve",
        ),
    )


class Citation(Base):
    __tablename__ = "citations"

    id: Mapped[UUID] = uuid_pk_col()
    chunk_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("document_chunks.id"), nullable=False)
    document_title: Mapped[str | None] = mapped_column(Text)
    document_tier: Mapped[DocumentTier] = mapped_column(pg_enum(DocumentTier, "doc_tier"), nullable=False)
    document_subtype: Mapped[str | None] = mapped_column(Text)
    section_title: Mapped[str | None] = mapped_column(Text)
    page_number: Mapped[int | None] = mapped_column(Integer)
    chunk_order: Mapped[int | None] = mapped_column(Integer)
    relevance_score: Mapped[float | None] = mapped_column(Float)
    excerpt: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=timestamp_now)

    chunk: Mapped[DocumentChunk] = relationship()

    __table_args__ = (
        CheckConstraint("relevance_score BETWEEN 0 AND 1", name="ck_citations_relevance_score"),
        Index("idx_citation_chunk", "chunk_id"),
    )


class MindmapArtifact(Base):
    __tablename__ = "mindmap_artifacts"

    id: Mapped[UUID] = uuid_pk_col()
    course_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("courses.id"), nullable=False)
    concept_graph: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)
    is_cached: Mapped[bool] = mapped_column(Boolean, server_default=text("true"))
    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=timestamp_now)
    invalidated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    course: Mapped[Course] = relationship()

    __table_args__ = (Index("idx_mindmap_course", "course_id", "is_cached", text("generated_at DESC")),)


class MockTestItem(Base):
    __tablename__ = "mock_test_items"

    id: Mapped[UUID] = uuid_pk_col()
    test_run_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    course_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("courses.id"), nullable=False)
    question_text: Mapped[str] = mapped_column(Text, nullable=False)
    question_type: Mapped[QuestionType] = mapped_column(pg_enum(QuestionType, "question_type_enum"), nullable=False)
    difficulty: Mapped[Difficulty] = mapped_column(pg_enum(Difficulty, "difficulty_enum"), nullable=False)
    topic: Mapped[str | None] = mapped_column(Text)
    options: Mapped[list[dict[str, Any]]] = mapped_column(JSONB, server_default=text("'[]'::jsonb"))
    correct_answer: Mapped[str] = mapped_column(Text, nullable=False)
    explanation: Mapped[str | None] = mapped_column(Text)
    citations: Mapped[list[dict[str, Any]]] = mapped_column(JSONB, server_default=text("'[]'::jsonb"))
    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=timestamp_now)

    course: Mapped[Course] = relationship()

    __table_args__ = (Index("idx_mock_test_run", "test_run_id"),)


class ContributionScore(Base):
    __tablename__ = "contribution_scores"

    id: Mapped[UUID] = uuid_pk_col()
    user_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    course_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("courses.id"), nullable=False)
    points: Mapped[float] = mapped_column(Float, server_default=text("0"))
    rank: Mapped[int | None] = mapped_column(Integer)
    global_rank: Mapped[int | None] = mapped_column(Integer)
    last_updated: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=timestamp_now)

    user: Mapped[User] = relationship()
    course: Mapped[Course] = relationship()

    __table_args__ = (UniqueConstraint("user_id", "course_id"),)


class CommunityVote(Base):
    __tablename__ = "community_votes"

    id: Mapped[UUID] = uuid_pk_col()
    user_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    document_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("documents.id"), nullable=False)
    vote: Mapped[str | None] = mapped_column(Text)
    voted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=timestamp_now)

    user: Mapped[User] = relationship()
    document: Mapped[Document] = relationship()

    __table_args__ = (
        UniqueConstraint("user_id", "document_id"),
        CheckConstraint("vote IN ('up', 'down')", name="ck_community_votes_vote"),
        Index("idx_votes_document", "document_id"),
    )


class AdminAuditLog(Base):
    __tablename__ = "admin_audit_logs"

    id: Mapped[UUID] = uuid_pk_col()
    actor_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    action_type: Mapped[str] = mapped_column(Text, nullable=False)
    target_entity_type: Mapped[str] = mapped_column(Text, nullable=False)
    target_entity_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True))
    from_state: Mapped[str | None] = mapped_column(Text)
    to_state: Mapped[str | None] = mapped_column(Text)
    reason: Mapped[str | None] = mapped_column(Text)
    logged_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=timestamp_now)

    actor: Mapped[User] = relationship()

    __table_args__ = (
        Index("idx_audit_actor", "actor_id", text("logged_at DESC")),
        Index("idx_audit_target", "target_entity_id", text("logged_at DESC")),
    )


class Notification(Base):
    __tablename__ = "notifications"

    id: Mapped[UUID] = uuid_pk_col()
    recipient_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    type: Mapped[str] = mapped_column(Text, nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    related_entity_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=timestamp_now)

    recipient: Mapped[User] = relationship()

    __table_args__ = (
        Index("idx_notifications_recipient_created", "recipient_id", text("created_at DESC")),
    )


class ProcessingJob(Base):
    __tablename__ = "processing_jobs"

    id: Mapped[UUID] = uuid_pk_col()
    document_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("documents.id"), nullable=False)
    job_type: Mapped[ProcessingJobType] = mapped_column(
        pg_enum(ProcessingJobType, "processing_job_type"),
        nullable=False,
    )
    run_number: Mapped[int] = mapped_column(Integer, server_default=text("1"), nullable=False)
    is_latest: Mapped[bool] = mapped_column(Boolean, server_default=text("true"), nullable=False)
    status: Mapped[JobStatus] = mapped_column(
        pg_enum(JobStatus, "eval_job_status"),
        server_default=text("'PENDING'::eval_job_status"),
    )
    attempt_count: Mapped[int] = mapped_column(Integer, server_default=text("0"))
    failure_reason: Mapped[str | None] = mapped_column(Text)
    raw_failure_output: Mapped[dict[str, Any] | None] = mapped_column(JSONB)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=timestamp_now)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=timestamp_now)

    document: Mapped[Document] = relationship(back_populates="processing_jobs")

    __table_args__ = (
        UniqueConstraint("document_id", "job_type", "run_number"),
        CheckConstraint("attempt_count <= 3", name="ck_processing_jobs_attempt_count"),
        Index(
            "idx_processing_job_latest",
            "document_id",
            "job_type",
            unique=True,
            postgresql_where=text("is_latest = TRUE"),
        ),
        Index("idx_processing_job_status", "status", "updated_at"),
    )


class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id: Mapped[UUID] = uuid_pk_col()
    user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    course_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("courses.id", ondelete="CASCADE"),
        nullable=False,
    )
    summary: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=timestamp_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=timestamp_now)

    user: Mapped[User] = relationship(back_populates="chat_sessions")
    course: Mapped[Course] = relationship(back_populates="chat_sessions")
    messages: Mapped[list[ChatMessage]] = relationship(
        back_populates="session",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        Index("idx_chat_sessions_user_course", "user_id", "course_id"),
    )


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id: Mapped[UUID] = uuid_pk_col()
    session_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("chat_sessions.id", ondelete="CASCADE"),
        nullable=False,
    )
    role: Mapped[ChatRole] = mapped_column(
        pg_enum(ChatRole, "chat_role"),
        nullable=False,
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)
    citations: Mapped[list[dict[str, Any]]] = mapped_column(
        JSONB,
        server_default=text("'[]'::jsonb"),
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=timestamp_now)

    session: Mapped[ChatSession] = relationship(back_populates="messages")

    __table_args__ = (
        Index("idx_chat_messages_session_created", "session_id", "created_at"),
    )


class CourseSummaryCache(Base):
    __tablename__ = "course_summaries_cache"

    course_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("courses.id", ondelete="CASCADE"),
        primary_key=True,
    )
    summary_markdown: Mapped[str] = mapped_column(Text, nullable=False)
    citations: Mapped[list[dict[str, Any]]] = mapped_column(
        JSONB,
        server_default=text("'[]'::jsonb"),
    )
    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=timestamp_now)

    course: Mapped[Course] = relationship(back_populates="summary_cache")

