# System Architecture & Database Design (ERD)
## Community Academic Knowledge Digitization and Management System

**Version:** 1.9  
**Date:** 2026-06-15  
**Derived from:** SRS v1.3, `project_description.md`, `document_evaluation_pipeline.md`, `document_processing_pipeline.md`, ADR-001, ADR-002, ADR-003  
**Status:** Design — Thesis Scope

---

## Table of Contents

1. [High-Level System Architecture](#1-high-level-system-architecture)
2. [Deployment Architecture](#2-deployment-architecture)
3. [Component Architecture](#3-component-architecture)
4. [End-to-End Data Flow Diagrams](#4-end-to-end-data-flow-diagrams)
5. [Entity-Relationship Diagram (ERD)](#5-entity-relationship-diagram-erd)
6. [Database Schema Detail](#6-database-schema-detail)
7. [RAG Namespace Architecture](#7-rag-namespace-architecture)
8. [Technology Stack Map](#8-technology-stack-map)
9. [Document State Machine Reference](#9-document-state-machine-reference)

---

## 1. High-Level System Architecture

The system is a course-centric academic knowledge platform organized into four horizontal layers.

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                         PRESENTATION LAYER                                  ║
║                         Frontend (Next.js / React)                          ║
║                                                                              ║
║  ┌─────────────┐  ┌──────────────┐  ┌────────────────┐  ┌───────────────┐  ║
║  │ Course Pages │  │  Doc Viewer  │  │ Reviewer Dash  │  │ Admin Dash    │  ║
║  └─────────────┘  └──────────────┘  └────────────────┘  └───────────────┘  ║
║  ┌─────────────┐  ┌──────────────┐  ┌────────────────┐  ┌───────────────┐  ║
║  │  Tutor Chat │  │   Mindmap    │  │   Mock Test    │  │ Leaderboard   │  ║
║  └─────────────┘  └──────────────┘  └────────────────┘  └───────────────┘  ║
╚═══════════════════════════════╤══════════════════════════════════════════════╝
                                │ HTTPS REST API
╔═══════════════════════════════▼══════════════════════════════════════════════╗
║                           APPLICATION LAYER                                  ║
║                          Backend (FastAPI / Python)                          ║
║                                                                              ║
║  ┌──────────┐ ┌──────────┐ ┌──────────────┐ ┌──────────┐ ┌──────────────┐  ║
║  │   Auth   │ │ Courses  │ │   Document   │ │  HITL    │ │  AI Feature  │  ║
║  │  & RBAC  │ │ Metadata │ │  Upload/View │ │  Review  │ │  Services    │  ║
║  └──────────┘ └──────────┘ └──────────────┘ └──────────┘ └──────────────┘  ║
║  ┌──────────┐ ┌──────────┐ ┌──────────────┐ ┌──────────────────────────┐   ║
║  │ Ranking  │ │  Voting  │ │ Admin Control│ │  Job Queue Orchestration  │   ║
║  └──────────┘ └──────────┘ └──────────────┘ └──────────────────────────┘   ║
╚═══════════════════╤═══════════════════════════════╤════════════════════════╝
                    │ Async Job Dispatch             │ DB / Storage Queries
         ╔══════════▼═══════════╗          ╔════════▼════════════════════════╗
         ║   PROCESSING LAYER   ║          ║      DATA LAYER                 ║
         ║  Redis + arq         ║          ║  PostgreSQL + pgvector           ║
         ║                      ║          ║  S3-compatible Object Storage    ║
         ║  ┌───────────────┐   ║          ╚═════════════════════════════════╝
         ║  │  OCR/Parse    │   ║
         ║  │  Worker       │   ║                 ╔══════════════════════════╗
         ║  └───────────────┘   ║                 ║   EXTERNAL SERVICES      ║
         ║  ┌───────────────┐   ║                 ║  ┌──────────────────┐    ║
         ║  │  Eval Pipeline│   ║◄────────────────╢  │  Bedrock/Gemini/ │    ║
         ║  │  Worker       │   ║                 ║  │  Groq providers  │    ║
         ║  │  (Agents 1-3) │   ║                 ║  │  (LLM + Vision)  │    ║
         ║  └───────────────┘   ║                 ║  └──────────────────┘    ║
         ║  ┌───────────────┐   ║                 ║  ┌──────────────────┐    ║
         ║  │  Chunk/Embed  │   ║                 ║  │  Tavily/SerpAPI  │    ║
         ║  │  Worker       │   ║                 ║  │  (Agent 2 Search)│    ║
         ║  └───────────────┘   ║                 ║  └──────────────────┘    ║
         ║                      ║                 ╚══════════════════════════╝
         ╚══════════════════════╝
```

---

## 2. Deployment Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Cloud Deployment                                  │
│                                                                     │
│  ┌─────────────────────┐      ┌──────────────────────────────────┐  │
│  │   Container: Web    │      │   Container: API Server          │  │
│  │   (Next.js SSR)     │◄────►│   (FastAPI / Uvicorn)            │  │
│  │   Port: 3000        │ REST │   Port: 8000                     │  │
│  └─────────────────────┘      └──────────────┬───────────────────┘  │
│                                              │                      │
│                         ┌──────────────────────────────────┐  │
│                         │                                  │  │
│              ┌──────────▼──────┐  ┌──────────▼──────┐  ┌──▼──────────────┐  │
│              │  Container:     │  │  Container:     │  │  Container:     │  │
│              │  OCR Worker     │  │  Eval Worker    │  │  Chunk/Embed    │  │
│              │  (arq)          │  │  (arq)          │  │  Worker (arq)   │  │
│              └─────────────────┘  └─────────────────┘  └─────────────────┘  │
│                         │                   │                   │  │
│              ┌──────────▼───────────────────▼───────────────────▼──────┐│  │
│              │              Container: Redis (Job Queue)               ││  │
│              └─────────────────────────────────────────────────────────┘│  │
│                                                                          │  │
│  ┌──────────────────────────────────────────────────────────┐   │  │
│  │   AWS RDS PostgreSQL + Cloudflare R2                       │   │  │
│  │   ┌──────────────────┐  ┌───────────────────────────┐   │◄──┘  │
│  │   │  PostgreSQL DB   │  │  S3-compatible Storage    │   │      │
│  │   │  + pgvector      │  │  (raw files + markdown)   │   │      │
│  │   └──────────────────┘  └───────────────────────────┘   │      │
│  └──────────────────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 3. Component Architecture

### 3.1 Backend Service Modules

| Module | Responsibility | Key Endpoints |
|--------|---------------|---------------|
| **Auth & RBAC** | JWT auth, role enforcement, session management | `POST /auth/login`, `POST /auth/register` |
| **Course Management** | CRUD for courses + Course Seed Documents, topic_tags auto-generation, SLA config | `GET/POST/PUT /courses`, `POST /courses/{id}/seed` |
| **Reviewer Assignment** | Assign/unassign reviewers to courses | `POST /courses/{id}/reviewers`, `DELETE /courses/{id}/reviewers/{uid}` |
| **Document Upload** | Two-path upload (Official Tier 1 / Community Tier 2), format validation, metadata persistence, enqueue OCR job | `POST /documents/official`, `POST /documents/community` |
| **Document Viewer** | Permission-checked viewer access, signed URL generation, Markdown serving | `GET /documents/{id}/markdown`, `GET /documents/{id}/raw-url` |
| **HITL Review Service** | Reviewer queue management, approve/reject/override decisions, SLA timer, escalation routing | `GET /review/queue`, `POST /review/{doc_id}/decide` |
| **AI Feature — Tutor** | Q&A: MMR retrieval + tier boost + vote weighting → generation. Course-wide Summary: single-call LLM over Tier 1 summaries. | `POST /tutor/query`, `POST /tutor/summarize` |
| **AI Feature — Mindmap** | Map-reduce concept graph generation, cache management per course | `POST /mindmap/generate/{course_id}`, `GET /mindmap/{course_id}` |
| **AI Feature — Mock Test** | Plan-then-generate test pipeline, per-topic question generation, assembly | `POST /mocktest/generate/{course_id}` |
| **Contribution Ranking** | Points calculation on approval, leaderboard queries (per-course + global) | `GET /leaderboard/course/{id}`, `GET /leaderboard/global` |
| **Community Voting** | Up/downvote management (one vote per user per document) | `POST /documents/{id}/vote` |
| **Admin Dashboard** | Dead-letter queue inspection, reprocess triggers, state override, audit log | `GET /admin/dead-letter`, `POST /admin/reprocess/{doc_id}` |
| **Job Queue Orchestrator** | Enqueues / monitors `arq` jobs; concurrency guard via `processing_jobs`/`evaluation_jobs`; retry policy | Internal |

### 3.2 Processing Worker Modules

| Worker | Input Queue | Processing | Output |
|--------|------------|------------|--------|
| **OCR/Parse Worker** | `ocr-jobs` | Promote optimized document-processing experiment as-is: PDF/PPTX/image routing, `slide_pdf`, visual classification/action routing, AWS Bedrock primary with Gemini/Groq fallback → normalized Markdown → Document Summarization | `DocumentSummary` record; processing artifacts/metrics; status → `EVALUATING` (community) or `APPROVED` (official) |
| **Duplicate Check Worker** | `duplicate-jobs` | Run parallel non-LLM ML-based duplicate checking job immediately after raw parsing completes. Calculates cosine similarity of sentence embeddings between the overall summary of the uploaded document and existing documents in the course. | `is_duplicate` flag, `duplicate_of_document_id`, `similarity_score`; results merged into `EvaluationReport` |
| **Evaluation Pipeline Worker** | `eval-jobs` | Run Agent 1 (Course Knowledge State compiler) → Agent 2 → Agent 3 sequentially with JSON schema validation at each step | `EvaluationReport` record; status → `NEEDS_REVIEW` |
| **Chunk/Embed Worker** | `index-jobs` | Semantic chunking (structure-based split + similarity grouping; no table/mermaid splits) → embedding → pgvector upsert → award contribution points | `DocumentChunk` records; status → `INDEXED` |

> **Worker Runtime Architecture (`arq` Python-only — supersedes BullMQ per ADR-003):**  
> The job queue backbone is **`arq` (Python asyncio Redis queue)**. All processing logic — OCR/parse (PyMuPDF, python-pptx), Document Summarization, AI evaluation, parallel duplicate check, chunking + embedding — runs in Python workers consuming `arq` queues directly. No Node.js dispatcher.  
> - 4 logical queues: `ocr-jobs`, `duplicate-jobs`, `eval-jobs`, `index-jobs`.  
> - Concurrency per queue tunable via env (`WORKER_OCR_CONCURRENCY`, etc.).  
> - Retry: 3 attempts, exponential backoff (1s, 4s, 16s) — `arq` `max_tries`.  
> - Job tracking + dead-letter via app-level tables `processing_jobs(job_type)` (OCR+Index) and `evaluation_jobs` (eval).  
> - **Rationale (OD-6 resolved 2026-06-02)**: backend is Python-only end-to-end; introducing a Node.js dispatcher duplicates ops without capability gain. See ADR-003 for full rationale.

### 3.3 Frontend Pages / UI Surfaces

| Surface | Users | Key Components |
|---------|-------|---------------|
| **Course List** | All | Course cards, enrollment status |
| **Course Detail** | All | Official Materials tab, Community Contributions tab, Tutor/Mindmap/Mocktest/Leaderboard tabs |
| **My Contributions Dashboard** | Student | Personal uploads list with detailed processing status (PARSING, EVALUATING, NEEDS_REVIEW, APPROVED, INDEXED, REJECTED, FAILED) and failure/rejection reasons |
| **Document Viewer** | All | "Nội dung" (Markdown) tab, "Bản gốc" (Raw) tab, Download button |
| **Upload Modal** | Students / Admin / Reviewer | `material_type` or `contribution_type` selector, `topic_tags` multi-select, file drop-zone, consent checkbox |
| **Reviewer Dashboard** | Reviewer / Admin (escalation) | Review queue, Evaluation Report tab, side-by-side OCR verification, approve/reject/override form |
| **Admin Dashboard** | Admin | Dead-letter queue, Escalation queue, Reviewer management, Course + Seed management, SLA config |
| **Tutor Chat Panel** | All | Virtual Tutor Agent interface, chat input, response with citations, namespace toggle (Strictly internal tools, no internet access) |
| **Mindmap Panel** | All | Interactive graph (reactflow / d3.js) built from Document Summarization context, regenerate button |
| **Mock Test Panel** | All | Config form (count + difficulty), rendered test, MCQ-only answer key with citations |
| **Leaderboard** | All | Per-course rank table, global rank table |

---

## 4. End-to-End Data Flow Diagrams

### 4.1 Community Contribution Upload & Evaluation Flow

```
Student
  │
  │ POST /documents/community
  │ {course_id, contribution_type, topic_tags, file}
  ▼
┌──────────────────────────────────────────────────────────────────┐
│  Upload Service                                                   │
│  1. Validate format (PDF/PPTX/JPG/PNG)                           │
│  2. Check Seed Document exists (FR-CM-04 Level 1)                │
│     └─ NO SEED → HTTP 409 "Course not ready for contributions"   │
│        Response: {error: "COURSE_NOT_READY", course_id}          │
│        ✗ Upload is REJECTED. No document record created.         │
│  3. Persist Document record (status=UPLOADED)                    │
│  4. Store raw file → S3 storage documents/{cid}/{did}/raw/       │
│  5. Enqueue OCR job → Redis ocr-jobs queue                       │
└───────────────────────────────┬──────────────────────────────────┘
                                │ async
                        ┌───────▼───────────────────────────────────┐
                        │  OCR/Parse Worker (status=PARSING)         │
                        │                                            │
                        │  Format routing:                           │
                        │  ├─ PDF → hybrid page-level processing    │
                        │  │   ├─ text-rich: use text layer         │
                        │  │   ├─ scanned: provider-chain OCR       │
                        │  │   ├─ slide_pdf: slide page extraction  │
                        │  │   └─ mixed: visual classify + routing  │
                        │  ├─ PPTX → python-pptx + visual routing  │
                        │  └─ JPG/PNG → provider-chain extraction   │
                        │                                            │
                        │  Assemble → normalized Markdown            │
                        │  Store .md → documents/{cid}/{did}/markdown/ │
                        │                                            │
                        │  Document Summarization (LLM):             │
                        │  Produce DocumentSummary record            │
                        │                                            │
                        │  status → EVALUATING                       │
                        │  Enqueue parallel eval-jobs & duplicate    │
                        └───────────────┬───────────────────────────┘
                                        │ async (parallel jobs)
                          ┌─────────────▼─────────────────────────┐
                          │  Evaluation & Duplicate Check Workers  │
                          │  (status=EVALUATING)                   │
                          │                                        │
                          │  ┌──────────────────────────────────┐  │
                          │  │ Chunk-Level Set Matching         │  │
                          │  │ • Cosine >= 0.85 per chunk       │  │
                          │  │ • Duplicate if overlap >= 40%    │  │
                          │  └─────────────────┬────────────────┘  │
                          │                    │                   │
                          │  ┌─────────────────▼────────────────┐  │
                          │  │ Agent 1: Course Context          │  │
                          │  │ • Compile Course Knowledge State │  │
                          │  │ • FR-CM-04 Level 2 — Cold-start  │  │
                          │  │ • Topic coverage mapping         │  │
                          │  └─────────────────┬────────────────┘  │
                          │                    │                   │
                          │  ┌─────────────────▼────────────────┐  │
                          │  │ Agent 2: Internet Search (15s TO) │  │
                          │  │ • Tavily/SerpAPI lookup           │  │
                          │  │ • Returns references or []        │  │
                          │  └─────────────────┬────────────────┘  │
                          │                    │                   │
                          │  ┌─────────────────▼────────────────┐  │
                          │  │ Agent 3: Quality Evaluation       │  │
                          │  │ • Score: relevance/completeness/  │  │
                          │  │   quality (0-10 each)             │  │
                          │  │ • Label verification + mismatch   │  │
                          │  │ • Output evaluation_justification │  │
                          │  │ • Priority-ordered recommendation │  │
                          │  └──────────────────────────────────┘  │
                          │                                        │
                          │  Persist EvaluationReport              │
                          │  (Merge duplicate check results)       │
                          │  status → NEEDS_REVIEW                 │
                          │  Route to Reviewer queue (or Admin)    │
                          └───────────────────────────────────────┘
                                        │ async (SLA 48h default)
                          ┌─────────────▼─────────────────────────┐
                          │  Reviewer / Admin Decision             │
                          │  • Reads: eval report + doc viewer    │
                          │  • Confirms/changes contribution_type  │
                          │  • Approve / Reject / Override         │
                          │  → Persist ReviewDecision              │
                          │                                        │
                          │  status → APPROVED  or  REJECTED      │
                          └────────────┬──────────────────────────┘
                                       │ on APPROVED
                          ┌────────────▼──────────────────────────┐
                          │  Chunk/Embed Worker (status=INDEXING)  │
                          │                                        │
                          │  Namespace routing by                  │
                          │  final_contribution_type:              │
                          │  • summary_note/review_note → knowledge│
                          │  • past_exam/solved_exercise → exercise│
                          │                                        │
                          │  Semantic chunking:                    │
                          │  1. Structure-based split (headings)   │
                          │  2. Similarity grouping (cosine)       │
                          │  3. Embed chunks (MiniLM MVP)           │
                          │  4. Upsert → pgvector                 │
                          │  5. Award ContributionScore to uploader│
                          │                                        │
                          │  status → INDEXED                      │
                          └────────────────────────────────────────┘
```

### 4.2 Official Material Upload Flow (Tier 1 — Shortcut Path)

```
Admin / Reviewer
  │
  │ POST /documents/official
  │ {course_id, material_type, file}
  ▼
Upload Service
  1. Validate format
  2. Enforce uniqueness: archive any previous active version of same material_type
  3. Persist Document (status=UPLOADED, tier=official, version=N)
  4. Enqueue OCR job
  ▼
OCR/Parse Worker (status=PARSING)
  → Normalized Markdown + DocumentSummary
  [SKIP: Evaluation pipeline / HITL review]
  status → APPROVED  (direct)
  ▼
Chunk/Embed Worker (status=INDEXING)
  → Always namespace = knowledge
  status → INDEXED
```

### 4.3 Virtual Tutor (RAG) Query & Summarization Flow

The Virtual Tutor Agent operates at the Main Conversation Level with a unified, LLM-driven Agent Loop (max 3 iterations). Rather than executing hardcoded sequential stages or routing requests through separate programmatic pre-checks/rewriters, the LLM itself dynamically decides its actions based on instructions embedded in its system prompt.

```
User sends query / request in Course X (scoped to session_id)
  │
  ▼
Virtual Tutor Agent (Main Conversation Level):
  1. System Prompt Instruction Match: The LLM reads history, query, and system prompt guidelines.
  2. Dynamic LLM Decision Loop (max 3 iterations, checks loop safeguards):
     ├─ Decision: Answer directly or call a tool?
     │   ├─ If history is sufficient:
     │   │   └─ LLM generates response directly without tool call
     │   ├─ If Course Summary requested:
     │   │   └─ LLM calls Course-Wide Summary Cache Tool
     │   │   └─ Fetch pre-generated summary from `course_summaries_cache`
     │   │   └─ Direct return and terminate loop
     │   ├─ If Detailed Q&A requested:
     │   │   └─ LLM contextually rewrites query & calls RAG Retrieval API Tool
     │   │   │   └─ Embed query & run MMR search (k=8, λ=0.7, namespace=knowledge [+exercise if toggled])
     │   │   │   └─ Apply Tier Boost (official ×1.15) & Vote Weighting
     │   │   │   └─ Re-rank and return top-k chunks
     │   ├─ If Document Metadata/Catalog needed:
     │   │   └─ LLM calls Document Summary Lookup / Course Metadata Explorer Tools
     ├─ Check Loop Safeguards:
     │   └─ Verify iteration count < 3
     │   └─ Duplicate Call Detection: Abort loop if the same tool is called with identical arguments
  3. Synthesizer compiles the final cited answer using only retrieved context.
  4. Save user query & assistant response to session chat history DB.
  │
  ▼
Response: { answer: string, citations: CitationObject[] }
```

#### Pre-generation of Course-Wide Summaries (Background Worker)
To keep latency under 3 seconds, course-wide summaries are pre-generated in the background:
```
Triggered when Course Official Materials (Tier 1) change
  │
  ▼
Pre-generation Worker:
  1. Collect Course Seed and Tier 1 summaries in knowledge namespace.
  2. Single LLM call synthesizes structured Markdown course summary.
  3. Attach Citation Objects pointing to the source official documents.
  4. Cache generated summary and citations to `course_summaries_cache` table.
```

### 4.4 Mindmap Generation Flow (Iterative Map-Reduce)

```
Mindmap Request for Course X
  │
  ▼
Phase 1 — No LLM call:
  Collect all DocumentSummary records for Course X (knowledge namespace)
  │
  ▼
Phase 2 — 1 LLM call:
  Input: all summaries + Course.topic_summary (Seed Document)
  Output: ConceptGraph JSON { nodes[], edges[] }
  │
  ▼
Phase 3 — Iterative (optional, per under-specified topic):
  For each topic with too few child concepts:
    → RAG retrieval for that topic name (has a query now)
    → Extract sub-concepts + relationships
    → Merge into existing graph
  │
  ▼
Phase 4 — Render + Cache:
  Store as MindmapArtifact (course_id, concept_graph, is_cached=true)
  Render with reactflow / d3.js / markmap
  Cache invalidated when any new INDEXED document arrives in course
```

---

## 5. Entity-Relationship Diagram (ERD)

### 5.1 ERD — Mermaid Diagram

```mermaid
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
```

### 5.2 Cardinality Summary

| Relationship | Cardinality | Notes |
|-------------|-------------|-------|
| Course → Document | 1 : N | All documents belong to exactly one course |
| Course → CourseReviewerAssignment | 1 : N | A course may have 0 or more active reviewer assignments |
| User → CourseReviewerAssignment | 1 : N | A reviewer may be assigned to multiple courses |
| Document → DocumentSummary | **1 : 1** | Every document has exactly one summary — created at end of PARSING |
| Document → DocumentChunk | 1 : N | Created at INDEXING; deleted-then-reinserted on reprocess |
| Document → EvaluationJob | **1 : N** | Community contributions only; each re-evaluate creates a new row; `is_latest=TRUE` identifies the current job |
| Document → EvaluationReport | 1 : 0..1 | Exactly one report per document at most; always linked to the latest completed `EvaluationJob` |
| EvaluationReport → ReviewDecision | 1 : 0..1 | One human decision per evaluation report |
| Document → CommunityVote | 1 : N | Unique constraint: one vote per (user, document) pair |
| Course → MindmapArtifact | 1 : N | Cached record; new one generated on invalidation |
| User + Course → ContributionScore | N:N resolved | Unique (user_id, course_id) per record |
| Course → ChatSession | 1 : N | A course can have many chat sessions across various users |
| User → ChatSession | 1 : N | A user can start multiple independent chat sessions |
| ChatSession → ChatMessage | 1 : N | A chat session contains many ordered messages |
| Course → CourseSummaryCache | 1 : 0..1 | A course has at most one pre-generated curriculum summary |

---

## 6. Database Schema Detail

### 6.1 Table: `courses`

```sql
CREATE TABLE courses (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code            VARCHAR(20) UNIQUE NOT NULL,        -- e.g. "IT3040"
    name            TEXT NOT NULL,
    description     TEXT,
    topic_summary   TEXT,                               -- Course Seed Document
    short_description TEXT,                             -- Course Seed Document
    topic_tags      JSONB DEFAULT '[]',                 -- auto-derived tag catalog
    review_sla_hours INTEGER DEFAULT 48
        CHECK (review_sla_hours BETWEEN 24 AND 72),
    is_active       BOOLEAN DEFAULT TRUE,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);
```

### 6.2 Table: `users`

```sql
CREATE TABLE users (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email           TEXT UNIQUE NOT NULL,
    hashed_password TEXT NOT NULL,
    role            TEXT NOT NULL CHECK (role IN ('student', 'reviewer', 'admin')),
    full_name       TEXT,
    is_active       BOOLEAN DEFAULT TRUE,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);
```

### 6.3 Table: `course_reviewer_assignments`

```sql
-- Each row represents ONE assignment episode. A reviewer can be unassigned and
-- re-assigned to the same course later, producing a new row (audit history).
-- Uniqueness of the *active* assignment is enforced by a partial index below.
-- Role constraints:
--   user_id  MUST reference a user with role='reviewer'  (enforced by trigger trg_cra_role_check)
--   assigned_by MUST reference a user with role='admin'  (enforced by trigger trg_cra_role_check)
-- PostgreSQL cross-table CHECKs require triggers; a plain CHECK cannot reference other rows.
CREATE TABLE course_reviewer_assignments (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID NOT NULL REFERENCES users(id),
    course_id       UUID NOT NULL REFERENCES courses(id),
    assigned_by     UUID NOT NULL REFERENCES users(id),
    is_active       BOOLEAN DEFAULT TRUE,              -- false = soft-deleted (unassigned)
    assigned_at     TIMESTAMPTZ DEFAULT NOW(),
    unassigned_at   TIMESTAMPTZ
    -- NOTE: no global UNIQUE(user_id, course_id) — that would prevent history rows.
);

-- Enforce at most one *active* assignment per reviewer-course pair:
CREATE UNIQUE INDEX idx_cra_active_unique
    ON course_reviewer_assignments(user_id, course_id)
    WHERE is_active = TRUE;

-- Fast reviewer lookup for routing documents to reviewer queues:
CREATE INDEX idx_cra_course_active
    ON course_reviewer_assignments(course_id, is_active);

-- Trigger: reject insert/update if user_id is not a reviewer, or assigned_by is not an admin.
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

CREATE TRIGGER trg_cra_role_check
    BEFORE INSERT OR UPDATE ON course_reviewer_assignments
    FOR EACH ROW EXECUTE FUNCTION fn_cra_role_check();
```

### 6.4 Table: `documents`

```sql
CREATE TYPE doc_status AS ENUM (
    'UPLOADED', 'PARSING', 'EVALUATING', 'NEEDS_REVIEW',
    'APPROVED', 'INDEXING', 'INDEXED', 'REJECTED', 'FAILED'
);
CREATE TYPE doc_tier AS ENUM ('official', 'community');
CREATE TYPE material_type_enum AS ENUM ('syllabus', 'textbook', 'lecture_slides');
CREATE TYPE contribution_type_enum AS ENUM ('past_exam', 'summary_note', 'review_note', 'solved_exercise');
CREATE TYPE file_format_enum AS ENUM ('pdf', 'pptx', 'jpg', 'png');

CREATE TABLE documents (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    course_id           UUID NOT NULL REFERENCES courses(id),
    uploader_id         UUID NOT NULL REFERENCES users(id),
    document_tier       doc_tier NOT NULL,
    material_type       material_type_enum,             -- NULL for community docs
    contribution_type   contribution_type_enum,         -- NULL for official docs
    topic_tags          JSONB DEFAULT '[]',
    status              doc_status NOT NULL DEFAULT 'UPLOADED',
    version             INTEGER DEFAULT 1,              -- monotonic, official only
    is_active_version   BOOLEAN DEFAULT TRUE,           -- for official uniqueness enforcement
    permanently_failed  BOOLEAN DEFAULT FALSE,
    original_filename   TEXT NOT NULL,
    file_format         file_format_enum NOT NULL,
    storage_raw_path    TEXT,
    storage_md_path     TEXT,
    no_reviewer_flag    BOOLEAN DEFAULT FALSE,
    sla_breached        BOOLEAN DEFAULT FALSE,
    sla_deadline        TIMESTAMPTZ,
    uploaded_at         TIMESTAMPTZ DEFAULT NOW(),
    updated_at          TIMESTAMPTZ DEFAULT NOW(),

    CONSTRAINT tier_type_check CHECK (
        (document_tier = 'official'
            AND material_type IS NOT NULL
            AND contribution_type IS NULL)
        OR
        (document_tier = 'community'
            AND contribution_type IS NOT NULL
            AND material_type IS NULL)
    )
);

CREATE INDEX idx_doc_course_status_created
    ON documents(course_id, status, uploaded_at);
CREATE INDEX idx_doc_uploader ON documents(uploader_id);
CREATE INDEX idx_doc_status    ON documents(status);

-- Enforce "only one active official version per material_type per course" (FR-UP-02).
CREATE UNIQUE INDEX idx_doc_official_active_version
    ON documents(course_id, material_type)
    WHERE document_tier = 'official' AND is_active_version = TRUE;

-- Trigger: enforce uploader role matches document tier.
--   official  → uploader must be admin or reviewer
--   community → uploader must be student or admin
-- (Admin can upload either tier per permission matrix.)
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

CREATE TRIGGER trg_doc_uploader_role_check
    BEFORE INSERT ON documents
    FOR EACH ROW EXECUTE FUNCTION fn_doc_uploader_role_check();
```

### 6.5 Table: `document_summaries`

```sql
CREATE TYPE language_enum    AS ENUM ('vi', 'en', 'mixed');
CREATE TYPE ocr_quality_enum AS ENUM ('high', 'medium', 'low');

CREATE TABLE document_summaries (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id         UUID UNIQUE NOT NULL
                            REFERENCES documents(id) ON DELETE CASCADE,
    schema_version      TEXT DEFAULT '1.0',
    topic               TEXT,
    concepts            JSONB DEFAULT '[]',              -- string[]
    language            language_enum,
    ocr_quality         ocr_quality_enum,
    section_summaries   JSONB DEFAULT '[]',              -- SectionSummary[]
    overall_summary     TEXT,
    created_at          TIMESTAMPTZ DEFAULT NOW(),
    updated_at          TIMESTAMPTZ DEFAULT NOW()
);
```

### 6.6 Table: `document_chunks`

```sql
CREATE EXTENSION IF NOT EXISTS vector;
CREATE TYPE rag_namespace_enum AS ENUM ('knowledge', 'exercise');

-- course_id is denormalized here (it could be joined from documents) to allow
-- single-table vector queries filtered by (course_id, rag_namespace) without
-- an extra join on every retrieval call. Populated at chunk-creation time and
-- never updated (a chunk always belongs to the same course as its document).
CREATE TABLE document_chunks (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id     UUID NOT NULL
                        REFERENCES documents(id) ON DELETE CASCADE,
    course_id       UUID NOT NULL
                        REFERENCES courses(id),        -- denormalized for query efficiency
    document_tier   doc_tier NOT NULL,
    subtype         TEXT,                               -- value of material_type or contribution_type
    rag_namespace   rag_namespace_enum NOT NULL,
    section_title   TEXT,
    page_number     INTEGER,
    chunk_order     INTEGER NOT NULL,
    content         TEXT NOT NULL,
    embedding       vector(768),                        -- adjust dim to chosen embedding model
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_chunk_document
    ON document_chunks(document_id);

-- Scalar pre-filter index: used together with the HNSW index so the vector
-- search can be scoped to (course_id, rag_namespace) without a full table scan.
CREATE INDEX idx_chunk_course_namespace
    ON document_chunks(course_id, rag_namespace);

-- HNSW index for approximate nearest neighbour (ANN) vector search.
-- Adjust ef_construction and m based on benchmarking once data volume is known.
CREATE INDEX idx_chunk_embedding_hnsw
    ON document_chunks USING hnsw (embedding vector_cosine_ops)
    WITH (m = 16, ef_construction = 64);
```

### 6.7 Table: `document_state_logs`

```sql
CREATE TABLE document_state_logs (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id     UUID NOT NULL REFERENCES documents(id),
    from_state      doc_status,                         -- NULL for initial UPLOADED transition
    to_state        doc_status NOT NULL,
    actor_id        UUID REFERENCES users(id),          -- NULL = system-triggered transition
    actor_type      TEXT NOT NULL
                        CHECK (actor_type IN ('system', 'student', 'reviewer', 'admin')),
    reason          TEXT,
    transitioned_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_state_log_document
    ON document_state_logs(document_id, transitioned_at);
```

### 6.8 Table: `evaluation_jobs`

```sql
CREATE TYPE eval_job_status AS ENUM ('PENDING', 'RUNNING', 'COMPLETED', 'FAILED');

-- Each re-evaluate (Admin-triggered) creates a NEW row.
-- run_number is monotonically increasing per document.
-- is_latest=TRUE marks the current/active job for a document.
-- Constraint: at most ONE active (is_latest=TRUE) job per document at any time.
CREATE TABLE evaluation_jobs (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id         UUID NOT NULL REFERENCES documents(id),
    run_number          INTEGER NOT NULL DEFAULT 1,     -- monotonic per document
    is_latest           BOOLEAN NOT NULL DEFAULT TRUE,  -- flipped to FALSE when superseded
    status              eval_job_status DEFAULT 'PENDING',
    attempt_count       INTEGER DEFAULT 0 CHECK (attempt_count <= 3),
    failure_reason      TEXT,
    raw_failure_output  JSONB,
    created_at          TIMESTAMPTZ DEFAULT NOW(),
    started_at          TIMESTAMPTZ,
    completed_at        TIMESTAMPTZ,
    updated_at          TIMESTAMPTZ DEFAULT NOW(),
    -- Composite unique for cross-document FK integrity in evaluation_reports (see §6.9):
    UNIQUE (id, document_id),
    -- Monotonicity guarantee: no two jobs for the same document share a run_number.
    UNIQUE (document_id, run_number)
);

-- Enforce at most one active job per document:
CREATE UNIQUE INDEX idx_eval_job_latest
    ON evaluation_jobs(document_id)
    WHERE is_latest = TRUE;

CREATE INDEX idx_eval_job_status_updated
    ON evaluation_jobs(status, updated_at);
CREATE INDEX idx_eval_job_document
    ON evaluation_jobs(document_id, run_number DESC);
```

### 6.9 Table: `evaluation_reports`

```sql
-- evaluation_reports uses a COMPOSITE FOREIGN KEY on (evaluation_job_id, document_id)
-- to guarantee that the referenced job belongs to the same document as the report.
-- This relies on the UNIQUE(id, document_id) defined on evaluation_jobs (see §6.8).
-- Note on Evaluation Output Schema: 
-- The parallel duplicate checker calculates sentence embedding similarities and merges its
-- output ({is_duplicate: boolean, duplicate_of_document_id: UUID|null, similarity_score: float})
-- directly into the `agent1_output` JSONB column. This adheres to the Agent1Output v1 contract.
CREATE TABLE evaluation_reports (
    id                      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id             UUID UNIQUE NOT NULL REFERENCES documents(id),
    evaluation_job_id       UUID NOT NULL,
    -- Composite FK: ensures evaluation_job_id.document_id == this.document_id
    FOREIGN KEY (evaluation_job_id, document_id)
        REFERENCES evaluation_jobs(id, document_id),
    schema_version          TEXT DEFAULT '1.0',
    agent1_output           JSONB NOT NULL,             -- Agent1Output v1 contract
    agent2_output           JSONB NOT NULL,             -- Agent2Output v1 contract
    agent3_output           JSONB NOT NULL,             -- Agent3Output v1 contract
    final_recommendation    TEXT NOT NULL
        CHECK (final_recommendation IN ('APPROVE', 'NEEDS_REVIEW', 'REJECT')),
    generated_at            TIMESTAMPTZ DEFAULT NOW()
);
```

### 6.10 Table: `review_decisions`

```sql
-- final_contribution_type is nullable:
--   • APPROVE / OVERRIDE_APPROVE → NOT NULL (required to determine RAG namespace)
--   • REJECT / OVERRIDE_REJECT    → NULL allowed (labelling a rejected doc is meaningless
--     for indexing and may introduce noise in label analytics)
-- The CHECK below enforces this conditional NOT NULL at the DB level.
CREATE TABLE review_decisions (
    id                          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    evaluation_report_id        UUID UNIQUE NOT NULL
                                    REFERENCES evaluation_reports(id),
    reviewer_id                 UUID NOT NULL REFERENCES users(id),
    initial_contribution_type   contribution_type_enum,
    suggested_contribution_type contribution_type_enum,
    final_contribution_type     contribution_type_enum,          -- NULL when decision = REJECT/OVERRIDE_REJECT
    decision                    TEXT NOT NULL
        CHECK (decision IN ('APPROVE', 'REJECT', 'OVERRIDE_APPROVE', 'OVERRIDE_REJECT')),
    note                        TEXT,
    decided_at                  TIMESTAMPTZ DEFAULT NOW(),
    -- Conditional NOT NULL: final_contribution_type must be set when approving.
    CONSTRAINT final_type_required_on_approve CHECK (
        decision IN ('REJECT', 'OVERRIDE_REJECT')
        OR final_contribution_type IS NOT NULL
    )
);
```

### 6.11 Table: `citations`

```sql
-- document_id is NOT stored here as an independent FK.
-- Rationale: storing chunk_id + document_id independently creates a correctness
-- risk (chunk from doc A, document_id = doc B). Instead:
--   • chunk_id is the sole FK providing document identity.
--   • document_id can be derived via: SELECT dc.document_id FROM document_chunks dc WHERE dc.id = citations.chunk_id
--   • document_title, document_tier, document_subtype are DENORMALIZED display-only
--     fields copied at citation-creation time to avoid joins on every Tutor response render.
CREATE TABLE citations (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    chunk_id        UUID NOT NULL REFERENCES document_chunks(id),
    -- Denormalized display fields (copied from document at creation time; never updated):
    document_title  TEXT,
    document_tier   doc_tier NOT NULL,
    document_subtype TEXT,
    -- Chunk-level display fields:
    section_title   TEXT,
    page_number     INTEGER,
    chunk_order     INTEGER,
    relevance_score FLOAT CHECK (relevance_score BETWEEN 0 AND 1),
    excerpt         TEXT,                               -- max 200 chars per contract
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_citation_chunk ON citations(chunk_id);
```

### 6.12 Table: `mindmap_artifacts`

```sql
CREATE TABLE mindmap_artifacts (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    course_id       UUID NOT NULL REFERENCES courses(id),
    concept_graph   JSONB NOT NULL,                     -- ConceptGraph v1: {nodes[], edges[]}
    is_cached       BOOLEAN DEFAULT TRUE,
    generated_at    TIMESTAMPTZ DEFAULT NOW(),
    invalidated_at  TIMESTAMPTZ
);

CREATE INDEX idx_mindmap_course
    ON mindmap_artifacts(course_id, is_cached, generated_at DESC);
```

### 6.13 Table: `mock_test_items`

```sql
CREATE TYPE question_type_enum AS ENUM ('multiple_choice', 'short_answer', 'true_false');
CREATE TYPE difficulty_enum    AS ENUM ('easy', 'medium', 'hard');

CREATE TABLE mock_test_items (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    course_id       UUID NOT NULL REFERENCES courses(id),
    question_text   TEXT NOT NULL,
    question_type   question_type_enum NOT NULL,
    difficulty      difficulty_enum NOT NULL,
    topic           TEXT,
    options         JSONB DEFAULT '[]',                 -- string[] for multiple choice
    correct_answer  TEXT NOT NULL,
    explanation     TEXT,
    citations       JSONB DEFAULT '[]',                 -- CitationObject[] v1
    generated_at    TIMESTAMPTZ DEFAULT NOW()
);
```

### 6.14 Table: `contribution_scores`

```sql
CREATE TABLE contribution_scores (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID NOT NULL REFERENCES users(id),
    course_id       UUID NOT NULL REFERENCES courses(id),
    points          FLOAT DEFAULT 0,
    rank            INTEGER,                            -- per-course rank
    global_rank     INTEGER,
    last_updated    TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE (user_id, course_id)
);
```

### 6.15 Table: `community_votes`

```sql
-- vote = NULL represents an "unvote" (user cast a vote then retracted it).
-- The row is kept (not deleted) so voted_at/audit trail is preserved.
-- Application logic: INSERT ... ON CONFLICT (user_id, document_id) DO UPDATE SET vote = ..., voted_at = NOW().
-- Net vote count = COUNT(*) FILTER (WHERE vote = 'up') - COUNT(*) FILTER (WHERE vote = 'down'),
-- excluding NULL rows from both counts.
CREATE TABLE community_votes (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID NOT NULL REFERENCES users(id),
    document_id     UUID NOT NULL REFERENCES documents(id),
    vote            TEXT CHECK (vote IN ('up', 'down')),  -- NULL = unvoted/retracted
    voted_at        TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE (user_id, document_id)                         -- one vote-record per user per document
);

CREATE INDEX idx_votes_document ON community_votes(document_id);
```

### 6.16 Table: `admin_audit_logs`

```sql
CREATE TABLE admin_audit_logs (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    actor_id            UUID NOT NULL REFERENCES users(id),
    action_type         TEXT NOT NULL,
    -- examples: REPROCESS | ASSIGN_REVIEWER | UNASSIGN_REVIEWER | UPDATE_SLA |
    --           OVERRIDE_DECISION | MARK_PERMANENTLY_FAILED | UPDATE_SEED_DOC
    target_entity_type  TEXT NOT NULL,
    -- examples: Document | Course | User | CourseReviewerAssignment
    target_entity_id    UUID,
    from_state          TEXT,
    to_state            TEXT,
    reason              TEXT,
    logged_at           TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_audit_actor
    ON admin_audit_logs(actor_id, logged_at DESC);
CREATE INDEX idx_audit_target
    ON admin_audit_logs(target_entity_id, logged_at DESC);
```

### 6.17 Table: `chat_sessions`

```sql
-- Represents an independent chat session started by a student in a specific course
CREATE TABLE chat_sessions (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    course_id       UUID NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
    summary         TEXT,                               -- Rolling memory long-term summary
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

-- Index for user context loading:
CREATE INDEX idx_chat_sessions_user_course
    ON chat_sessions(user_id, course_id);
```

### 6.18 Table: `chat_messages`

```sql
CREATE TYPE chat_role AS ENUM ('user', 'assistant', 'system', 'tool');

-- Stores message exchanges inside a chat session, including LLM citation arrays
CREATE TABLE chat_messages (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id      UUID NOT NULL REFERENCES chat_sessions(id) ON DELETE CASCADE,
    role            chat_role NOT NULL,
    content         TEXT NOT NULL,
    citations       JSONB DEFAULT '[]'::jsonb,          -- CitationObject[] v1
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- Sequenced history retrieval index:
CREATE INDEX idx_chat_messages_session_created
    ON chat_messages(session_id, created_at ASC);
```

### 6.19 Table: `course_summaries_cache`

```sql
-- Caches pre-generated Markdown summaries and source citations for each course.
-- Summaries are regenerated ngầm only on official Tier 1 changes to prevent real-time LLM cost.
CREATE TABLE course_summaries_cache (
    course_id           UUID PRIMARY KEY REFERENCES courses(id) ON DELETE CASCADE,
    summary_markdown    TEXT NOT NULL,
    citations           JSONB DEFAULT '[]'::jsonb,      -- CitationObject[] v1 pointing to Tier 1 docs
    generated_at        TIMESTAMPTZ DEFAULT NOW()
);
```

---

## 7. RAG Namespace Architecture

### 7.1 Namespace Routing Table

| Document Tier | Subtype | RAG Namespace |
|--------------|---------|---------------|
| Official | `syllabus` | **knowledge** |
| Official | `textbook` | **knowledge** |
| Official | `lecture_slides` | **knowledge** |
| Community | `summary_note` | **knowledge** |
| Community | `review_note` | **knowledge** |
| Community | `past_exam` | **exercise** |
| Community | `solved_exercise` | **exercise** |

> **Critical rule**: For community contributions, namespace is determined by the **reviewer-confirmed `final_contribution_type`** from `review_decisions`, NOT the uploader's initial label.

### 7.2 Vector Store Organization (pgvector)

```
-- Retrieval query pattern (single-table, no join required):
--   SELECT id, content, embedding, document_tier, subtype
--   FROM document_chunks
--   WHERE course_id = $1            ← scalar pre-filter (idx_chunk_course_namespace)
--     AND rag_namespace = $2        ← scalar pre-filter
--   ORDER BY embedding <=> $3       ← HNSW ANN search (idx_chunk_embedding_hnsw)
--   LIMIT $4;
--
-- course_id is denormalized into document_chunks precisely to avoid a JOIN
-- on every vector query. The composite index (course_id, rag_namespace) lets
-- pgvector apply the scalar filter before the HNSW scan.

Logical groupings within the chunks table:

  course_id = 'X' AND rag_namespace = 'knowledge'
    ├─ official:  lecture_slides, textbook, syllabus chunks
    └─ community: summary_note, review_note chunks

  course_id = 'X' AND rag_namespace = 'exercise'
    └─ community: past_exam, solved_exercise chunks
```

### 7.3 Retrieval Score Pipeline

```
final_score = mmr_score
            * (if official_tier: 1.15 else 1.0)    ← tier boost
            * (1 + vote_weight_factor)               ← community vote weight
```

---

## 8. Technology Stack Map

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend | Next.js 14 + React | SSR web application |
| | react-markdown + remark-gfm + remark-math + rehype-katex | Markdown rendering with math |
| | reactflow / d3.js / markmap | Interactive mindmap visualization |
| | react-pdf | PDF embedded viewer |
| Backend | Python 3.11+ / FastAPI | REST API server |
| | LangChain / LlamaIndex | RAG pipeline orchestration |
| | Pydantic v2 | Request/response schema validation |
| Processing Workers | **`arq` (Python asyncio + Redis)** | Single Python runtime hosts OCR (PyMuPDF, python-pptx) + Summarization + AI pipeline + chunking/embedding. See §3.2 + ADR-003 for rationale. |
| Job Queue | Redis | Queue backend + pub/sub |
| Database | PostgreSQL 15+ | Relational data store; local pgvector container, AWS RDS for PostgreSQL in cloud |
| Vector Store | pgvector | Embedding index (HNSW) |
| Object Storage | S3-compatible storage | MinIO local, Cloudflare R2 cloud; raw files + Markdown files |
| LLM | AWS Bedrock → Gemini fallback → Groq text-only fallback | Summarization, agent prompts, generation |
| Vision OCR | AWS Bedrock primary → Gemini fallback → Groq text-only fallback | OCR/extraction, visual classification, diagram/table/formula descriptions |
| Embedding | `sentence-transformers/all-MiniLM-L6-v2` (384-d) for MVP | Document chunks + query vectors; future provider swap requires reindex |
| Web Search | Tavily / SerpAPI | Agent 2 Internet search |
| Document Parsing | PyMuPDF | PDF text extraction + rendering |
| | python-pptx | PPTX text + notes extraction |
| Evaluation Harness | RAGAS + DeepEval | Automated RAG quality evaluation |
| CI/CD | GitHub Actions | Build, test, deploy pipeline |

---

## 9. Document State Machine Reference

```
                      ┌──────────────┐
Upload ─────────────► │   UPLOADED   │
                      └──────┬───────┘
                             │ OCR job auto-enqueued
                             ▼
                      ┌──────────────┐
                      │   PARSING    │──────── error (3x) ────► FAILED ◄──────┐
                      └──────┬───────┘                                         │
                             │ Markdown + DocumentSummary ready                │
              ┌──────────────┴──────────────┐                                  │
              │ community                   │ official (skip eval)             │
              ▼                             ▼                                  │
       ┌──────────────┐             ┌──────────────┐                           │
       │  EVALUATING  │── error ───►│    FAILED    │                           │
       └──────┬───────┘             └──────────────┘                           │
              │ pipeline complete                                               │
              ▼                             ▼ (official direct→)               │
       ┌──────────────┐             ┌──────────────┐                           │
       │ NEEDS_REVIEW │             │   APPROVED   │◄──────────────────────────┘
       └──────┬───────┘             └──────┬───────┘
              │ Reviewer action             │ chunking job auto-enqueued
     ┌────────┴────────┐                   ▼
     ▼                 ▼            ┌──────────────┐
┌──────────┐     ┌──────────┐      │   INDEXING   │──── error (3x) ────► FAILED
│ APPROVED │     │ REJECTED │      └──────┬───────┘
└────┬─────┘     └──────────┘             ▼
     │ chunking job                 ┌──────────────┐
     ▼                             │    INDEXED   │  ← available for AI features
┌──────────┐                      └──────────────┘
│ INDEXING │── error (3x) ──────► FAILED
└────┬─────┘
     ▼
┌──────────┐
│  INDEXED │
└──────────┘

Admin-only recovery transitions:
  FAILED   ──► PARSING     (trigger full reprocess)
  FAILED   ──► EVALUATING  (re-evaluate only, skip re-OCR)
  REJECTED ──► PARSING     (rare manual override)
```

### State Transition Table

| From | To | Trigger |
|------|----|---------| 
| `UPLOADED` | `PARSING` | System auto-triggers OCR job |
| `PARSING` | `EVALUATING` | Markdown + summary ready (community tier) |
| `PARSING` | `APPROVED` | Markdown + summary ready (official tier — skip eval) |
| `PARSING` | `FAILED` | OCR/parse error after 3 retries |
| `EVALUATING` | `NEEDS_REVIEW` | Agent pipeline completes |
| `EVALUATING` | `FAILED` | Agent pipeline error after 3 retries |
| `NEEDS_REVIEW` | `APPROVED` | Reviewer/Admin approves |
| `NEEDS_REVIEW` | `REJECTED` | Reviewer/Admin rejects |
| `APPROVED` | `INDEXING` | System auto-triggers chunking job |
| `INDEXING` | `INDEXED` | All chunks embedded and indexed successfully |
| `INDEXING` | `FAILED` | Embedding/indexing error after 3 retries |
| `FAILED` | `PARSING` | **Admin only** — trigger reprocess |
| `FAILED` | `EVALUATING` | **Admin only** — trigger re-evaluation (skip re-OCR) |
| `REJECTED` | `PARSING` | **Admin only** — trigger reprocess (rare) |

---

---

## 10. Open Design Decisions (Pending Team Confirmation)

| # | Question | Default in this doc | Impact if changed |
|---|----------|--------------------|-----------------|
| OD-1 | **Reviewer assignment history**: store full history (multiple rows per reviewer-course) or only keep the current-state row? | Full history (one row per episode; is_active partial index enforces uniqueness of active state) | If only current-state is needed, replace partial index with `UNIQUE (user_id, course_id)` and remove history rows on re-assignment |
| OD-2 | **Unvote semantics**: does the system allow retracting a vote (NULL state), or only toggling between up/down? | NULL is allowed (row is retained, vote column set to NULL) | If unvote is not needed, add `NOT NULL` back to `vote` column and treat up↔down as a simple UPDATE |
| OD-3 | **course_id in document_chunks**: denormalized column (current design) or derived via JOIN at query time? | Denormalized — single-table retrieval query, no runtime join | If normalized instead, all vector retrieval queries must JOIN documents; add composite index on `documents(id, course_id, status)` for efficiency |
| OD-4 | **EvaluationJob re-evaluate history**: current design stores one row per run (1:N) with `is_latest` flag, allowing full audit trail of re-evaluations. Is this required, or can older job rows be deleted? | Keep all rows (history preserved) | If history is not needed, drop `run_number`/`is_latest` columns and add `UNIQUE(document_id)` instead |
| OD-5 | **final_contribution_type on REJECT**: current design allows NULL when rejecting (label analytics not polluted). Should the label still be captured on reject for analytics? | NULL allowed on REJECT — enforced by conditional CHECK | If analytics need the label on all decisions, remove the conditional CHECK and make `final_contribution_type NOT NULL` again |
| ~~OD-6~~ | ~~BullMQ + Python dispatch strategy~~ | ✅ **Resolved 2026-06-02**: adopt `arq` (Python-native), drop BullMQ. See ADR-003. | — |

---

### Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-04-20 | Antigravity | Initial release |
| 1.1 | 2026-04-21 | Antigravity | Fix: add `course_id` (denormalized) to `document_chunks` + composite scalar index; add partial unique index for official active-version uniqueness (FR-UP-02); replace `UNIQUE(user_id,course_id)` in `course_reviewer_assignments` with partial index on `is_active=TRUE` (preserves history); standardize storage path to `markdown/` (aligned with SRS); lock worker stack to BullMQ (aligned with SRS §6.2); add `NULL` to `community_votes.vote` CHECK with unvote semantics comment; update Section 7.2 pgvector query pattern to reflect denormalized `course_id`; add Open Design Decisions section. |
| 1.2 | 2026-04-21 | Antigravity | Fix: EvaluationJob changed to 1:N (re-evaluate history) with `run_number`+`is_latest` + partial unique index + `UNIQUE(id,document_id)` for composite FK; EvaluationReport composite FK added to enforce cross-document integrity; Citations drops independent `document_id` FK (derive via chunk join; display fields denormalized); `final_contribution_type` made nullable on REJECT via conditional CHECK `final_type_required_on_approve`; header version synced to 1.2; OD-4, OD-5 added to Open Design Decisions. |
| 1.3 | 2026-04-21 | Antigravity | Fix: upload flow rewritten to show FR-CM-04 Level 1 as hard HTTP 409 block with no document record created; Agent 1 block annotated with Level 2 cold-start forced-NEEDS_REVIEW behaviour; §3.2 gets hybrid BullMQ+Python worker architecture note; stack map row updated to show dispatcher+Python split; `course_reviewer_assignments` gets role-enforcement trigger (`trg_cra_role_check`); `documents` gets uploader-role trigger (`trg_doc_uploader_role_check`); `evaluation_jobs` gains `UNIQUE(document_id, run_number)` to guarantee monotonicity; OD-6 added. |
| 1.4 | 2026-06-02 | Backend Manager | OD-6 resolved: replace BullMQ Node dispatcher with `arq` (Python-native) per ADR-003. Updated §1 high-level architecture, §2 deployment diagram, §3.1 Job Queue Orchestrator, §3.2 worker runtime block, §8 stack map. Job tracking pattern updated to use `processing_jobs(job_type)` for OCR/Index and `evaluation_jobs` for eval (new bảng `processing_jobs` per backend plan D-8). Note: `processing_jobs` DDL detail lives in `backend_implementation_plan.md` §2.3 D-8 pending full propagation into §6. |
| 1.5 | 2026-06-02 | Codex | Align with `project_plan.md`: replace Supabase default stack with PostgreSQL+pgvector and S3-compatible storage (MinIO local, Azure PostgreSQL + Cloudflare R2 cloud). Sync processing architecture to optimized document-processing experiment: Azure primary, Gemini/Groq fallback, `slide_pdf`, visual classification/action routing, and artifact/metrics persistence. |
| 1.6 | 2026-06-11 | Antigravity | Align with real LLM provider credentials, AWS Bedrock-first provider chains, sentence-transformers embedding adapter, and Bedrock SSO. |
| 1.7 | 2026-06-15 | Antigravity | Restrict mindmaps & course knowledge state synthesis (Agent 1) to approved official materials (Tier 1) and Course Seeds to prevent redundancy and cost. |
| 1.8 | 2026-06-15 | Antigravity | Move Virtual Tutor Agent loop to main conversation level with 4 tools (RAG retrieval, summary lookup, metadata explorer, and cached course summary) and infinite loop safeguards (max 3 iterations, redundant arg detection). |
| 1.9 | 2026-06-15 | Antigravity | Add database schemas for `chat_sessions`, `chat_messages`, and `course_summaries_cache` to synchronize the ERD with the Virtual Tutor chatbot design, and document the parallel duplicate check mapping. |

*End of Architecture & ERD v1.9 — 2026-06-15*
