"""Initial backend schema.

Revision ID: 20260602_0001
Revises:
Create Date: 2026-06-02
"""

from collections.abc import Sequence

from alembic import op

revision: str = "20260602_0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


ENUMS_SQL = """
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'doc_status') THEN
        CREATE TYPE doc_status AS ENUM (
            'UPLOADED', 'PARSING', 'EVALUATING', 'NEEDS_REVIEW',
            'APPROVED', 'INDEXING', 'INDEXED', 'REJECTED', 'FAILED'
        );
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'doc_tier') THEN
        CREATE TYPE doc_tier AS ENUM ('official', 'community');
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'material_type_enum') THEN
        CREATE TYPE material_type_enum AS ENUM ('syllabus', 'textbook', 'lecture_slides');
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'contribution_type_enum') THEN
        CREATE TYPE contribution_type_enum AS ENUM ('past_exam', 'summary_note', 'review_note', 'solved_exercise');
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'file_format_enum') THEN
        CREATE TYPE file_format_enum AS ENUM ('pdf', 'pptx', 'jpg', 'png');
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'language_enum') THEN
        CREATE TYPE language_enum AS ENUM ('vi', 'en', 'mixed');
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'ocr_quality_enum') THEN
        CREATE TYPE ocr_quality_enum AS ENUM ('high', 'medium', 'low');
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'rag_namespace_enum') THEN
        CREATE TYPE rag_namespace_enum AS ENUM ('knowledge', 'exercise');
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'eval_job_status') THEN
        CREATE TYPE eval_job_status AS ENUM ('PENDING', 'RUNNING', 'COMPLETED', 'FAILED');
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'processing_job_type') THEN
        CREATE TYPE processing_job_type AS ENUM ('ocr', 'index');
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'question_type_enum') THEN
        CREATE TYPE question_type_enum AS ENUM ('multiple_choice', 'short_answer', 'true_false');
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'difficulty_enum') THEN
        CREATE TYPE difficulty_enum AS ENUM ('easy', 'medium', 'hard');
    END IF;
END
$$;
"""


TABLES_SQL = """
CREATE TABLE IF NOT EXISTS courses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code VARCHAR(20) UNIQUE NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    topic_summary TEXT,
    short_description TEXT,
    topic_tags JSONB DEFAULT '[]',
    review_sla_hours INTEGER DEFAULT 48 CHECK (review_sla_hours BETWEEN 24 AND 72),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT UNIQUE NOT NULL,
    hashed_password TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('student', 'reviewer', 'admin')),
    full_name TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS course_reviewer_assignments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    course_id UUID NOT NULL REFERENCES courses(id),
    assigned_by UUID NOT NULL REFERENCES users(id),
    is_active BOOLEAN DEFAULT TRUE,
    assigned_at TIMESTAMPTZ DEFAULT NOW(),
    unassigned_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    course_id UUID NOT NULL REFERENCES courses(id),
    uploader_id UUID NOT NULL REFERENCES users(id),
    document_tier doc_tier NOT NULL,
    material_type material_type_enum,
    contribution_type contribution_type_enum,
    topic_tags JSONB DEFAULT '[]',
    status doc_status NOT NULL DEFAULT 'UPLOADED',
    version INTEGER DEFAULT 1,
    is_active_version BOOLEAN DEFAULT TRUE,
    permanently_failed BOOLEAN DEFAULT FALSE,
    original_filename TEXT NOT NULL,
    file_format file_format_enum NOT NULL,
    storage_raw_path TEXT,
    storage_md_path TEXT,
    no_reviewer_flag BOOLEAN DEFAULT FALSE,
    sla_breached BOOLEAN DEFAULT FALSE,
    sla_deadline TIMESTAMPTZ,
    uploaded_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT tier_type_check CHECK (
        (document_tier = 'official' AND material_type IS NOT NULL AND contribution_type IS NULL)
        OR
        (document_tier = 'community' AND contribution_type IS NOT NULL AND material_type IS NULL)
    )
);

CREATE TABLE IF NOT EXISTS document_summaries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID UNIQUE NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    schema_version TEXT DEFAULT '1.0',
    topic TEXT,
    concepts JSONB DEFAULT '[]',
    language language_enum,
    ocr_quality ocr_quality_enum,
    section_summaries JSONB DEFAULT '[]',
    overall_summary TEXT,
    summary_embedding vector(384),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS document_chunks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    course_id UUID NOT NULL REFERENCES courses(id),
    document_tier doc_tier NOT NULL,
    subtype TEXT,
    rag_namespace rag_namespace_enum NOT NULL,
    section_title TEXT,
    page_number INTEGER,
    chunk_order INTEGER NOT NULL,
    content TEXT NOT NULL,
    embedding vector(384),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS document_state_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID NOT NULL REFERENCES documents(id),
    from_state doc_status,
    to_state doc_status NOT NULL,
    actor_id UUID REFERENCES users(id),
    actor_type TEXT NOT NULL CHECK (actor_type IN ('system', 'student', 'reviewer', 'admin')),
    reason TEXT,
    transitioned_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS evaluation_jobs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID NOT NULL REFERENCES documents(id),
    run_number INTEGER NOT NULL DEFAULT 1,
    is_latest BOOLEAN NOT NULL DEFAULT TRUE,
    status eval_job_status DEFAULT 'PENDING',
    attempt_count INTEGER DEFAULT 0 CHECK (attempt_count <= 3),
    failure_reason TEXT,
    raw_failure_output JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE (id, document_id),
    UNIQUE (document_id, run_number)
);

CREATE TABLE IF NOT EXISTS evaluation_reports (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID NOT NULL REFERENCES documents(id),
    evaluation_job_id UUID UNIQUE NOT NULL,
    FOREIGN KEY (evaluation_job_id, document_id) REFERENCES evaluation_jobs(id, document_id),
    is_latest BOOLEAN NOT NULL DEFAULT TRUE,
    schema_version TEXT DEFAULT '1.0',
    agent1_output JSONB NOT NULL,
    agent2_output JSONB NOT NULL,
    agent3_output JSONB NOT NULL,
    final_recommendation TEXT NOT NULL CHECK (final_recommendation IN ('APPROVE', 'NEEDS_REVIEW', 'REJECT')),
    generated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS review_decisions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    evaluation_report_id UUID UNIQUE NOT NULL REFERENCES evaluation_reports(id),
    reviewer_id UUID NOT NULL REFERENCES users(id),
    initial_contribution_type contribution_type_enum,
    suggested_contribution_type contribution_type_enum,
    final_contribution_type contribution_type_enum,
    decision TEXT NOT NULL CHECK (decision IN ('APPROVE', 'REJECT', 'OVERRIDE_APPROVE', 'OVERRIDE_REJECT')),
    note TEXT,
    decided_at TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT final_type_required_on_approve CHECK (
        decision IN ('REJECT', 'OVERRIDE_REJECT') OR final_contribution_type IS NOT NULL
    )
);

CREATE TABLE IF NOT EXISTS citations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    chunk_id UUID NOT NULL REFERENCES document_chunks(id),
    document_title TEXT,
    document_tier doc_tier NOT NULL,
    document_subtype TEXT,
    section_title TEXT,
    page_number INTEGER,
    chunk_order INTEGER,
    relevance_score FLOAT CHECK (relevance_score BETWEEN 0 AND 1),
    excerpt TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS mindmap_artifacts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    course_id UUID NOT NULL REFERENCES courses(id),
    concept_graph JSONB NOT NULL,
    is_cached BOOLEAN DEFAULT TRUE,
    generated_at TIMESTAMPTZ DEFAULT NOW(),
    invalidated_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS mock_test_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    course_id UUID NOT NULL REFERENCES courses(id),
    question_text TEXT NOT NULL,
    question_type question_type_enum NOT NULL,
    difficulty difficulty_enum NOT NULL,
    topic TEXT,
    options JSONB DEFAULT '[]',
    correct_answer TEXT NOT NULL,
    explanation TEXT,
    citations JSONB DEFAULT '[]',
    generated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS contribution_scores (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    course_id UUID NOT NULL REFERENCES courses(id),
    points FLOAT DEFAULT 0,
    rank INTEGER,
    global_rank INTEGER,
    last_updated TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE (user_id, course_id)
);

CREATE TABLE IF NOT EXISTS community_votes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    document_id UUID NOT NULL REFERENCES documents(id),
    vote TEXT CHECK (vote IN ('up', 'down')),
    voted_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE (user_id, document_id)
);

CREATE TABLE IF NOT EXISTS admin_audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    actor_id UUID NOT NULL REFERENCES users(id),
    action_type TEXT NOT NULL,
    target_entity_type TEXT NOT NULL,
    target_entity_id UUID,
    from_state TEXT,
    to_state TEXT,
    reason TEXT,
    logged_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS processing_jobs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID NOT NULL REFERENCES documents(id),
    job_type processing_job_type NOT NULL,
    run_number INTEGER NOT NULL DEFAULT 1,
    is_latest BOOLEAN NOT NULL DEFAULT TRUE,
    status eval_job_status DEFAULT 'PENDING',
    attempt_count INTEGER DEFAULT 0 CHECK (attempt_count <= 3),
    failure_reason TEXT,
    raw_failure_output JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE (document_id, job_type, run_number)
);
"""


INDEXES_SQL = """
CREATE UNIQUE INDEX IF NOT EXISTS idx_cra_active_unique
    ON course_reviewer_assignments(user_id, course_id)
    WHERE is_active = TRUE;
CREATE INDEX IF NOT EXISTS idx_cra_course_active
    ON course_reviewer_assignments(course_id, is_active);

CREATE INDEX IF NOT EXISTS idx_doc_course_status_created
    ON documents(course_id, status, uploaded_at);
CREATE INDEX IF NOT EXISTS idx_doc_uploader ON documents(uploader_id);
CREATE INDEX IF NOT EXISTS idx_doc_status ON documents(status);
CREATE UNIQUE INDEX IF NOT EXISTS idx_doc_official_active_version
    ON documents(course_id, material_type)
    WHERE document_tier = 'official' AND is_active_version = TRUE;

CREATE INDEX IF NOT EXISTS idx_chunk_document ON document_chunks(document_id);
CREATE INDEX IF NOT EXISTS idx_chunk_course_namespace ON document_chunks(course_id, rag_namespace);
CREATE INDEX IF NOT EXISTS idx_chunk_embedding_hnsw
    ON document_chunks USING hnsw (embedding vector_cosine_ops)
    WITH (m = 16, ef_construction = 64);

CREATE INDEX IF NOT EXISTS idx_summary_embedding_hnsw
    ON document_summaries USING hnsw (summary_embedding vector_cosine_ops)
    WITH (m = 16, ef_construction = 64);

CREATE INDEX IF NOT EXISTS idx_state_log_document
    ON document_state_logs(document_id, transitioned_at);

CREATE UNIQUE INDEX IF NOT EXISTS idx_eval_job_latest
    ON evaluation_jobs(document_id)
    WHERE is_latest = TRUE;
CREATE INDEX IF NOT EXISTS idx_eval_job_status_updated ON evaluation_jobs(status, updated_at);
CREATE INDEX IF NOT EXISTS idx_eval_job_document ON evaluation_jobs(document_id, run_number DESC);
CREATE UNIQUE INDEX IF NOT EXISTS idx_eval_report_latest
    ON evaluation_reports(document_id)
    WHERE is_latest = TRUE;
CREATE INDEX IF NOT EXISTS idx_eval_report_document ON evaluation_reports(document_id, generated_at DESC);

CREATE INDEX IF NOT EXISTS idx_citation_chunk ON citations(chunk_id);
CREATE INDEX IF NOT EXISTS idx_mindmap_course ON mindmap_artifacts(course_id, is_cached, generated_at DESC);
CREATE INDEX IF NOT EXISTS idx_votes_document ON community_votes(document_id);
CREATE INDEX IF NOT EXISTS idx_audit_actor ON admin_audit_logs(actor_id, logged_at DESC);
CREATE INDEX IF NOT EXISTS idx_audit_target ON admin_audit_logs(target_entity_id, logged_at DESC);

CREATE UNIQUE INDEX IF NOT EXISTS idx_processing_job_latest
    ON processing_jobs(document_id, job_type)
    WHERE is_latest = TRUE;
CREATE INDEX IF NOT EXISTS idx_processing_job_status ON processing_jobs(status, updated_at);
"""


TRIGGER_STATEMENTS = [
    """
CREATE OR REPLACE FUNCTION fn_cra_role_check() RETURNS TRIGGER AS $$
BEGIN
    IF (SELECT role FROM users WHERE id = NEW.user_id) <> 'reviewer' THEN
        RAISE EXCEPTION 'course_reviewer_assignments.user_id must reference a user with role=reviewer';
    END IF;
    IF (SELECT role FROM users WHERE id = NEW.assigned_by) <> 'admin' THEN
        RAISE EXCEPTION 'course_reviewer_assignments.assigned_by must reference a user with role=admin';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
""",
    "DROP TRIGGER IF EXISTS trg_cra_role_check ON course_reviewer_assignments",
    """
CREATE TRIGGER trg_cra_role_check
    BEFORE INSERT OR UPDATE ON course_reviewer_assignments
    FOR EACH ROW EXECUTE FUNCTION fn_cra_role_check()
""",
    """
CREATE OR REPLACE FUNCTION fn_doc_uploader_role_check() RETURNS TRIGGER AS $$
DECLARE
    v_role TEXT;
BEGIN
    SELECT role INTO v_role FROM users WHERE id = NEW.uploader_id;
    IF NEW.document_tier = 'official' AND v_role NOT IN ('admin', 'reviewer') THEN
        RAISE EXCEPTION 'Official documents may only be uploaded by admin or reviewer (got role=%)', v_role;
    END IF;
    IF NEW.document_tier = 'community' AND v_role NOT IN ('student', 'admin') THEN
        RAISE EXCEPTION 'Community contributions may only be uploaded by student or admin (got role=%)', v_role;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
""",
    "DROP TRIGGER IF EXISTS trg_doc_uploader_role_check ON documents",
    """
CREATE TRIGGER trg_doc_uploader_role_check
    BEFORE INSERT ON documents
    FOR EACH ROW EXECUTE FUNCTION fn_doc_uploader_role_check()
""",
]


def execute_statements(sql: str) -> None:
    for statement in sql.split(";"):
        stripped = statement.strip()
        if stripped:
            op.execute(stripped)


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto")
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")
    op.execute(ENUMS_SQL)
    execute_statements(TABLES_SQL)
    execute_statements(INDEXES_SQL)
    for statement in TRIGGER_STATEMENTS:
        op.execute(statement)


def downgrade() -> None:
    op.execute("DROP TRIGGER IF EXISTS trg_doc_uploader_role_check ON documents")
    op.execute("DROP FUNCTION IF EXISTS fn_doc_uploader_role_check")
    op.execute("DROP TRIGGER IF EXISTS trg_cra_role_check ON course_reviewer_assignments")
    op.execute("DROP FUNCTION IF EXISTS fn_cra_role_check")
    for table in (
        "processing_jobs",
        "admin_audit_logs",
        "community_votes",
        "contribution_scores",
        "mock_test_items",
        "mindmap_artifacts",
        "citations",
        "review_decisions",
        "evaluation_reports",
        "evaluation_jobs",
        "document_state_logs",
        "document_chunks",
        "document_summaries",
        "documents",
        "course_reviewer_assignments",
        "users",
        "courses",
    ):
        op.execute(f"DROP TABLE IF EXISTS {table} CASCADE")
    for enum in (
        "difficulty_enum",
        "question_type_enum",
        "processing_job_type",
        "eval_job_status",
        "rag_namespace_enum",
        "ocr_quality_enum",
        "language_enum",
        "file_format_enum",
        "contribution_type_enum",
        "material_type_enum",
        "doc_tier",
        "doc_status",
    ):
        op.execute(f"DROP TYPE IF EXISTS {enum} CASCADE")
