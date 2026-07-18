erDiagram

    Course {
        uuid id PK
        string code UK
        string name
        text description
        text topic_summary
        text short_description
        jsonb topic_tags
        integer review_sla_hours
        boolean is_active
        timestamptz created_at
        timestamptz updated_at
    }

    User {
        uuid id PK
        string email UK
        string hashed_password
        enum role "student|reviewer|admin"
        string full_name
        boolean is_active
        timestamptz created_at
        timestamptz updated_at
    }

    CourseReviewerAssignment {
        uuid id PK
        uuid user_id FK
        uuid course_id FK
        uuid assigned_by FK
        boolean is_active
        timestamptz assigned_at
        timestamptz unassigned_at
    }

    Document {
        uuid id PK
        uuid course_id FK
        uuid uploader_id FK
        enum document_tier "official|community"
        enum material_type "syllabus|textbook|lecture_slides|NULL"
        enum contribution_type "past_exam|summary_note|review_note|solved_exercise|NULL"
        jsonb topic_tags
        enum status "UPLOADED|PARSING|EVALUATING|NEEDS_REVIEW|APPROVED|INDEXING|INDEXED|REJECTED|FAILED"
        integer version
        boolean is_active_version
        boolean permanently_failed
        string original_filename
        enum file_format "pdf|pptx|jpg|png"
        string storage_raw_path
        string storage_md_path
        boolean no_reviewer_flag
        boolean sla_breached
        timestamptz sla_deadline
        timestamptz uploaded_at
        timestamptz updated_at
    }

    DocumentSummary {
        uuid id PK
        uuid document_id FK UK
        string schema_version
        string topic
        jsonb concepts
        enum language "vi|en|mixed"
        enum ocr_quality "high|medium|low"
        jsonb section_summaries
        text overall_summary
        timestamptz created_at
        timestamptz updated_at
    }

    DocumentChunk {
        uuid id PK
        uuid document_id FK
        uuid course_id FK "denormalized from documents.course_id"
        enum document_tier "official|community"
        string subtype
        enum rag_namespace "knowledge|exercise"
        string section_title
        integer page_number
        integer chunk_order
        text content
        vector embedding
        timestamptz created_at
    }

    DocumentStateLog {
        uuid id PK
        uuid document_id FK
        enum from_state
        enum to_state
        uuid actor_id FK
        string actor_type
        text reason
        timestamptz transitioned_at
    }

    EvaluationJob {
        uuid id PK
        uuid document_id FK
        integer run_number "monotonic per document"
        boolean is_latest "true for most recent job row"
        enum status "PENDING|RUNNING|COMPLETED|FAILED"
        integer attempt_count
        text failure_reason
        jsonb raw_failure_output
        timestamptz created_at
        timestamptz started_at
        timestamptz completed_at
        timestamptz updated_at
    }

    EvaluationReport {
        uuid id PK
        uuid document_id FK UK
        uuid evaluation_job_id FK
        string schema_version
        jsonb agent1_output
        jsonb agent2_output
        jsonb agent3_output
        enum final_recommendation "APPROVE|NEEDS_REVIEW|REJECT"
        timestamptz generated_at
    }

    ReviewDecision {
        uuid id PK
        uuid evaluation_report_id FK UK
        uuid reviewer_id FK
        enum initial_contribution_type
        enum suggested_contribution_type
        enum final_contribution_type "NULL when decision=REJECT"
        enum decision "APPROVE|REJECT|OVERRIDE_APPROVE|OVERRIDE_REJECT"
        text note
        timestamptz decided_at
    }

    Citation {
        uuid id PK
        uuid chunk_id FK "sole FK; document_id derived via join"
        string document_title "denormalized display field"
        enum document_tier "official|community"
        string document_subtype
        string section_title
        integer page_number
        integer chunk_order
        float relevance_score
        text excerpt
        timestamptz created_at
    }

    MindmapArtifact {
        uuid id PK
        uuid course_id FK
        jsonb concept_graph
        boolean is_cached
        timestamptz generated_at
        timestamptz invalidated_at
    }

    MockTestItem {
        uuid id PK
        uuid course_id FK
        string question_text
        enum question_type "multiple_choice|short_answer|true_false"
        enum difficulty "easy|medium|hard"
        string topic
        jsonb options
        string correct_answer
        text explanation
        jsonb citations
        timestamptz generated_at
    }

    ContributionScore {
        uuid id PK
        uuid user_id FK
        uuid course_id FK
        float points
        integer rank
        integer global_rank
        timestamptz last_updated
    }

    CommunityVote {
        uuid id PK
        uuid user_id FK
        uuid document_id FK
        enum vote "up|down|null"
        timestamptz voted_at
    }

    AdminAuditLog {
        uuid id PK
        uuid actor_id FK
        string action_type
        string target_entity_type
        uuid target_entity_id
        string from_state
        string to_state
        text reason
        timestamptz logged_at
    }

    ChatSession {
        uuid id PK
        uuid user_id FK
        uuid course_id FK
        text summary
        timestamptz created_at
        timestamptz updated_at
    }

    ChatMessage {
        uuid id PK
        uuid session_id FK
        enum role
        text content
        jsonb citations
        timestamptz created_at
    }

    CourseSummaryCache {
        uuid course_id PK
        text summary_markdown
        jsonb citations
        timestamptz generated_at
    }

    %% ─── RELATIONSHIPS ────────────────────────────────────────────────────────

    Course ||--o{ Document : "contains"
    Course ||--o{ CourseReviewerAssignment : "has_assignments"
    Course ||--o{ MindmapArtifact : "has_mindmaps"
    Course ||--o{ MockTestItem : "has_tests"
    Course ||--o{ ContributionScore : "has_scores"
    Course ||--o{ ChatSession : "has_sessions"
    Course ||--o| CourseSummaryCache : "has_cached_summary"

    User ||--o{ Document : "uploads"
    User ||--o{ CourseReviewerAssignment : "is_reviewer_for"
    User ||--o{ ReviewDecision : "makes"
    User ||--o{ CommunityVote : "casts"
    User ||--o{ ContributionScore : "earns"
    User ||--o{ DocumentStateLog : "triggers"
    User ||--o{ AdminAuditLog : "logs"
    User ||--o{ ChatSession : "starts_sessions"

    Document ||--|| DocumentSummary : "has_summary"
    Document ||--o{ DocumentChunk : "split_into"
    Document ||--o{ EvaluationJob : "has_jobs"
    Document ||--o| EvaluationReport : "has_report"
    Document ||--o{ DocumentStateLog : "has_transitions"
    Document ||--o{ CommunityVote : "receives_votes"
    Document ||--o{ Citation : "cited_by"

    EvaluationJob |o--o| EvaluationReport : "may_produce"
    EvaluationReport ||--o| ReviewDecision : "decided_by"

    DocumentChunk ||--o{ Citation : "cited_as"

    ChatSession ||--o{ ChatMessage : "contains_messages"