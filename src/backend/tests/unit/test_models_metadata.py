from sqlalchemy import Index

from app.db.base import Base
from app.models import Document, DocumentChunk, DocumentSummary, EvaluationReport, Vector


def test_declares_all_initial_schema_tables() -> None:
    assert set(Base.metadata.tables) == {
        "admin_audit_logs",
        "chat_messages",
        "chat_sessions",
        "citations",
        "community_votes",
        "contribution_scores",
        "course_reviewer_assignments",
        "course_summaries_cache",
        "courses",
        "document_chunks",
        "document_state_logs",
        "document_summaries",
        "documents",
        "evaluation_jobs",
        "evaluation_reports",
        "mindmap_artifacts",
        "mock_test_items",
        "notifications",
        "processing_jobs",
        "review_decisions",
        "users",
    }


def test_document_supports_display_name() -> None:
    assert "display_name" in Document.__table__.c
    assert Document.__table__.c.display_name.nullable is True


def test_vector_columns_use_embedding_dimension() -> None:
    chunk_embedding = DocumentChunk.__table__.c.embedding.type
    summary_embedding = DocumentSummary.__table__.c.summary_embedding.type

    assert isinstance(chunk_embedding, Vector)
    assert isinstance(summary_embedding, Vector)
    assert chunk_embedding.dimension == 1024
    assert summary_embedding.dimension == 1024


def test_vector_type_serializes_python_lists_for_pgvector() -> None:
    vector = Vector(3)
    bind_processor = vector.bind_processor(dialect=None)
    result_processor = vector.result_processor(dialect=None, coltype=None)

    assert bind_processor([0.1, 2, -3.25]) == "[0.1,2.0,-3.25]"
    assert result_processor("[0.1,2,-3.25]") == [0.1, 2.0, -3.25]


def test_evaluation_report_allows_re_evaluation_history() -> None:
    table = EvaluationReport.__table__
    index_by_name = {index.name: index for index in table.indexes}

    assert table.c.evaluation_job_id.unique is True
    assert table.c.document_id.unique is None
    assert index_by_name["idx_eval_report_latest"].unique is True


def test_latest_indexes_are_partial_unique_indexes() -> None:
    expected_names = {
        "idx_cra_active_unique",
        "idx_doc_official_active_version",
        "idx_eval_job_latest",
        "idx_eval_report_latest",
        "idx_processing_job_latest",
    }

    actual: dict[str, Index] = {}
    for table in Base.metadata.tables.values():
        for index in table.indexes:
            if index.name in expected_names:
                actual[index.name] = index

    assert set(actual) == expected_names
    assert all(index.unique for index in actual.values())
    assert all(index.dialect_options["postgresql"]["where"] is not None for index in actual.values())
