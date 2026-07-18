# Software Requirements Specification (SRS)
## Community Academic Knowledge Digitization and Management System

**Version:** 1.6  
**Date:** 2026-06-15  
**Status:** Draft — Thesis Scope  
**Authors:** Thesis Team (SoICT — HUST)  
**Source Documents:**
- `.agent/project_description.md`
- `.agent/architecture/document_processing_pipeline.md`
- `.agent/architecture/document_evaluation_pipeline.md`
- `.agent/architecture/adr-001-semantic-chunking.md`
- `.agent/architecture/adr-002-rag-namespaces.md`

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Overall Description](#2-overall-description)
3. [User Classes and Characteristics](#3-user-classes-and-characteristics)
4. [System Features — Functional Requirements](#4-system-features--functional-requirements)
   - 4.1 Course Management
   - 4.2 Document Upload and Ingestion
   - 4.3 Document Processing Pipeline
   - 4.4 Document Summarization
   - 4.5 Document Evaluation Pipeline (3-Agent)
   - 4.6 Human-in-the-Loop (HITL) Review
   - 4.7 Post-Approval Chunking and Indexing
   - 4.8 Document Viewer
   - 4.9 Virtual Tutor (RAG)
   - 4.10 Mindmap Generation
   - 4.11 Mock Test Generation
   - 4.12 Contribution Ranking and Leaderboard
   - 4.13 Community Voting
   - 4.14 Admin Dashboard
5. [Non-Functional Requirements](#5-non-functional-requirements)
6. [External Interface Requirements](#6-external-interface-requirements)
7. [Data Model Requirements](#7-data-model-requirements)
8. [System Constraints and Assumptions](#8-system-constraints-and-assumptions)
9. [Appendix A: Document Lifecycle State Machine](#appendix-a-document-lifecycle-state-machine)
10. [Appendix B: Permission Matrix](#appendix-b-permission-matrix)
11. [Appendix C: Data Schemas and Contracts](#appendix-c-data-schemas-and-contracts)

---

## 1. Introduction

### 1.1 Purpose

This Software Requirements Specification (SRS) formally defines the functional and non-functional requirements for the *Community Academic Knowledge Digitization and Management System*, a course-centric academic platform enabling students of the School of Information and Communications Technology (SoICT), HUST, to contribute, review, and utilize learning materials supported by an AI agent pipeline.

### 1.2 Document Scope

This document covers:
- All features within the thesis scope: document upload, automated processing, 3-agent evaluation, human review, RAG-based AI features (Virtual Tutor, Mindmap, Mock Test), contribution ranking, and community voting.
- System boundaries, user roles, data model essentials, and API surface.
- Non-functional requirements pertaining to performance, security, reliability, and scalability.

### 1.3 Definitions and Acronyms

| Term | Definition |
|------|-----------|
| SRS | Software Requirements Specification |
| RAG | Retrieval-Augmented Generation |
| HITL | Human-in-the-Loop |
| OCR | Optical Character Recognition |
| SoICT | School of Information and Communications Technology |
| LLM | Large Language Model |
| MMR | Maximal Marginal Relevance |
| SLA | Service Level Agreement |
| ADR | Architecture Decision Record |
| arq | Python-native asyncio Redis queue (per ADR-003; supersedes BullMQ from v1.1) |
| pgvector | PostgreSQL extension for vector similarity search |
| Tier 1 | Official Materials (uploaded by Admin/Reviewer) |
| Tier 2 | Community Contributions (uploaded by Students) |

### 1.4 References

| Document | Location |
|----------|----------|
| Project Description (Coding-Agent Version) | `.agent/project_description.md` |
| Document Processing Pipeline | `.agent/architecture/document_processing_pipeline.md` |
| Document Evaluation Pipeline | `.agent/architecture/document_evaluation_pipeline.md` |
| ADR-001: Semantic Chunking | `.agent/architecture/adr-001-semantic-chunking.md` |
| ADR-002: RAG Namespace Routing | `.agent/architecture/adr-002-rag-namespaces.md` |
| JSON Schemas (pipeline contracts) | `data/schemas/` |
| Course Seed Data | `data/seed/courses.json` |

### 1.5 Overview

Section 2 provides product context. Sections 3–4 describe users and all functional requirements organized by feature. Section 5 defines non-functional requirements. Sections 6–7 specify external interfaces and the data model. Section 8 lists constraints and assumptions. Appendices contain state machine, permission matrix, and data contract references.

---

## 2. Overall Description

### 2.1 Product Perspective

The system is a standalone web application backed by a Python/FastAPI API server and a React/Next.js frontend. It integrates the validated LLM/OCR provider chain (AWS Bedrock primary, Gemini fallback, Groq text-only fallback), PostgreSQL with the pgvector extension, S3-compatible object storage, and an asynchronous job queue (Redis + `arq`) to form a complete academic knowledge pipeline.

```
┌─────────────────────────────────────────────────────┐
│                   Frontend (Next.js)                │
│  Course pages · Document viewer · AI features panel │
└─────────────────────────┬───────────────────────────┘
                          │ REST API
┌─────────────────────────▼───────────────────────────┐
│                  Backend (FastAPI)                   │
│  Auth · Courses · Upload · Review · AI orchestration │
└──────┬──────────────────────────────────┬────────────┘
       │ async jobs                        │ DB / vector
┌──────▼──────┐                  ┌────────▼────────────┐
│ Redis + arq │                  │  PostgreSQL         │
│  Job Queue  │                  │  + pgvector         │
└──────┬──────┘                  └─────────────────────┘
       │  workers
┌──────▼────────────────────────────────────────────┐
│  Processing Workers                               │
│  OCR/Parse · Evaluate (Agents 1-3) · Chunk/Embed  │
└──────────────────────────────────────────────────-┘
```

### 2.2 Product Functions (Summary)

1. **Document Ingestion**: multi-format upload (PDF, PPTX, JPG/PNG) with automated OCR/parsing to normalized Markdown.
2. **Evaluation Pipeline**: 3-agent AI pipeline (Course Context Aggregator, Internet Search, Quality Evaluation) on community contributions.
3. **HITL Review**: reviewer dashboard with full AI evaluation report; human override capability.
4. **RAG-Based AI Features**: Virtual Tutor, Mindmap Generation, Mock Test Generation — all scoped per course.
5. **Contribution Ranking**: community vote-driven ranking, badge system, and per-course leaderboards.
6. **Admin Controls**: course and reviewer management, failed-job handling, reprocess triggers.

### 2.3 User Needs

- **Students** need a friction-free way to share notes and past exams and receive AI-powered learning assistance grounded in verified course materials.
- **Reviewers (Senior Students / TAs)** need an efficient dashboard to assess AI-evaluated documents quickly without re-reading raw files.
- **Administrators** need full control over system configuration, course seeding, and pipeline health.

### 2.4 Operating Environment

- **Deployment target**: cloud-hosted containerized services (frontend + backend + workers).
- **Supported browsers**: modern evergreen browsers (Chrome, Firefox, Edge, Safari).
- **Languages**: Vietnamese and English (content and UI).
- **File formats accepted**: PDF (unencrypted), PPTX, JPG/PNG.
- **Database**: PostgreSQL + pgvector extension. Local deployment uses a PostgreSQL/pgvector container; cloud deployment targets AWS RDS for PostgreSQL + pgvector.
- **Queue**: Redis + `arq` (per ADR-003).

### 2.5 Design and Implementation Constraints

1. Course is the **primary partition key** for all features, data, and retrieval namespaces.
2. All AI output must be traceable with citations, decision logs, and actor identity.
3. Asynchronous background jobs must be used for all long-running processing (OCR, evaluation, indexing).
4. The system must support pilot growth from a small number of courses without architectural redesign.
5. Mathematical formula reliability is best-effort; guaranteed formula accuracy is out of scope.

### 2.6 Assumptions and Dependencies

- The LLM/OCR provider chain is available with sufficient quota: AWS Bedrock as primary, Gemini as fallback, and Groq as text-only fallback.
- A web search API (Tavily or SerpAPI) is available for Agent 2.
- PostgreSQL with pgvector and S3-compatible object storage are provisioned before deployment.
- Admin pre-populates official SoICT course list before any community uploads occur.
- Admin creates a Course Seed Document for each course before the full evaluation pipeline can operate.

---

## 3. User Classes and Characteristics

### 3.1 Student

| Attribute | Value |
|-----------|-------|
| Population | SoICT enrolled students |
| Technical skill | General web user |
| Frequency of use | Daily during semester |
| Access | Own-course contributions; all INDEXED course documents |

**Key characteristics:**
- Uploads community contributions (past exams, notes, exercises) to selected courses.
- Uses AI features (Tutor, Mindmap, Mock Test) on approved course documents.
- Views personal contribution score and leaderboard rank.
- Can upvote/downvote indexed documents.

### 3.2 Subject Reviewer

| Attribute | Value |
|-----------|-------|
| Population | Senior students or teaching assistants assigned by Admin |
| Technical skill | Domain-knowledgeable; familiar with course content |
| Frequency of use | Several times per week |
| Access | Documents in their assigned courses only |

**Key characteristics:**
- Reviews AI evaluation reports and makes approve/reject/override decisions.
- Can confirm or change `contribution_type` labels proposed by Agent 3.
- Can add professional comments on document quality.
- Cannot trigger reprocessing or manage courses.

### 3.3 Admin

| Attribute | Value |
|-----------|-------|
| Population | System administrator (typically thesis/project team) |
| Technical skill | Technical; familiar with system architecture |
| Frequency of use | As needed; higher at launch and on incidents |
| Access | Full system access |

**Key characteristics:**
- Manages courses and Course Seed Documents.
- Assigns/unassigns Reviewers to courses.
- **Handles escalated documents**: reviews documents routed to the Admin queue due to SLA breach (`sla_breached` flag) or absence of assigned reviewer (`no_reviewer` flag). Can review directly or first assign a reviewer then hand off.
- Uploads official materials (Tier 1).
- Resolves `FAILED` jobs: inspects failure reason and raw agent output, then triggers manual reprocess or marks document as permanently failed.
- Configures review SLA per course (default 48h; range 24h–72h).
- Can override any document decision and manage reviewer assignments at any time.

---

## 4. System Features — Functional Requirements

> **Requirement ID format:** `FR-{MODULE}-{NUMBER}`  
> Priority: **Must** = required for thesis scope, **Should** = high value, **Could** = desirable.

---

### 4.1 Course Management

**FR-CM-01** (Must): System must support a list of official SoICT course entities, each identified by a unique course code (e.g., `IT3040`, `IT4062`). Each course has: `name`, `code`, `description`, `topic_summary`.

**FR-CM-02** (Must): Only Admin can create, update, or deactivate courses.

**FR-CM-03** (Must): Each course must have a **Course Seed Document** (fields: `name`, `short_description`, `topic_summary`) that Admin creates and maintains. The Seed Document:
- Is required for the full 3-agent evaluation pipeline to operate on that course.
- Provides the canonical topic list for Mindmap and Mock Test generation.
- Provides predefined `topic_tags` that students may apply to their uploads.

**FR-CM-04** (Must): The system enforces a two-level gate for community contributions against an unprepared course:

- **Level 1 — No Seed Document (pipeline block)**: if a course has no Course Seed Document, community contributions **cannot enter the evaluation pipeline**. The system must reject the upload at the point of submission with a clear error message (e.g., "This course is not yet ready to accept community contributions"). Admin must create the Seed Document before any community uploads are processed.
- **Level 2 — Cold-start flag (Agent 1 signal)**: if the course *has* a Seed Document but has fewer than 3 approved documents (counting both tiers), Agent 1 sets `cold_start: true` in its output. In cold-start mode, all non-duplicate community contributions are routed directly to `NEEDS_REVIEW` regardless of Agent 3 scores. This flag auto-clears once the course reaches 3 approved documents.

> **Rationale for separation**: Agent 1 requires the Seed Document's `topic_summary` to compute topic coverage. Without a Seed Document, Agent 1 cannot run at all. The cold-start flag is a separate, runtime signal that handles the insufficient-baseline condition independently of Seed Document existence.

**FR-CM-05** (Must): Admin must be able to assign and unassign Reviewers to courses at any time via the Admin Dashboard. The mapping is stored in `CourseReviewerAssignment` (`user_id`, `course_id`, `assigned_at`, `assigned_by`, `is_active`).

**FR-CM-06** (Should): Admin must be able to configure review SLA duration per course (default: 48 hours; range: 24h–72h).

**FR-CM-07** (Must): When Admin creates or updates a Course Seed Document, the system must **automatically derive** the predefined `topic_tags` catalog from the `topic_summary` field using an LLM extraction call. The resulting tag list is stored on the Course record and presented to students as a selectable tag set during upload. Admin may manually edit the tag list after auto-generation.

---

### 4.2 Document Upload and Ingestion

#### 4.2.1 Official Material Upload (Tier 1)

**FR-UP-01** (Must): Admin and Reviewers (within their assigned courses) may upload official materials. The upload must require selection of:
- `course_id`
- `material_type`: one of `syllabus | textbook | lecture_slides`
- File (formats: PDF, PPTX, JPG/PNG only)

**FR-UP-02** (Must): The system must enforce **uniqueness**: only one active version per `material_type` per course. Uploading a new file of the same type must archive the previous version (version history is kept; previous version marked inactive).

**FR-UP-03** (Must): Official materials must bypass the 3-agent evaluation pipeline and HITL review. Their state path is:  
`UPLOADED → PARSING → APPROVED → INDEXING → INDEXED`

**FR-UP-04** (Must): All official materials must always be indexed into the **knowledge** RAG namespace.

#### 4.2.2 Community Contribution Upload (Tier 2)

**FR-UP-05** (Must): Students may upload community contributions. The upload must require selection of:
- `course_id`
- `contribution_type`: one of `past_exam | summary_note | review_note | solved_exercise`
- File (formats: PDF, PPTX, JPG/PNG only)
- (Optional) `topic_tags`: selected from course's predefined topic catalog derived from the Course Seed Document topic summary.

**FR-UP-06** (Must): Community contributions must go through the full 3-agent evaluation pipeline and HITL review. Their state path is:  
`UPLOADED → PARSING → EVALUATING → NEEDS_REVIEW → APPROVED → INDEXING → INDEXED`

**FR-UP-07** (Must): File format validation must occur at upload time. Unsupported formats must be rejected with a descriptive error message. Accepted: PDF (unencrypted), PPTX, JPG/PNG.

**FR-UP-08** (Must): File metadata (`course_id`, uploader, format, `contribution_type`/`material_type`, `topic_tags`, timestamps) must be persisted upon upload before any processing begins.

**FR-UP-09** (Must): The system must reject video, audio, encrypted PDF, and any other unsupported formats.

---

### 4.3 Document Processing Pipeline

> Based on `.agent/architecture/document_processing_pipeline.md`

**FR-PP-01** (Must): Immediately after a document is uploaded, the system must automatically enqueue an OCR/parsing job. The job must convert the raw file into **full normalized Markdown** before any downstream steps (evaluation or indexing).

**FR-PP-02** (Must): The pipeline must support format-specific processing routes:
- **PDF**: Classify into `text_pdf`, `scanned_pdf`, `slide_pdf`, or `mixed_pdf` using text density, image count, image/page ratio, and landscape-page evidence; then route as direct text, vision-only, or hybrid processing (see FR-PP-03).
- **PPTX**: Parse via `python-pptx`; extract slide text and speaker notes; classify embedded images and route each visual through skip/minimal-tag/extract handling.
- **JPG/PNG**: Classify the whole image and extract OCR/description through the live VLM provider chain.

**FR-PP-03** (Must): For **PDF** files, each page must be classified and processed independently:
- **Text-rich, no images** (extracted text > 50 characters, no embedded images): use extracted text layer directly.
- **Scanned / image-only** (little or no text layer): render page as image → extract via the VLM provider chain.
- **Slide PDF** (landscape, image-bearing PDF pages): render each page as a slide and extract with a slide-specific prompt.
- **Mixed content** (text + embedded images): keep extracted text; run hash-based repeat detection before VLM calls; classify each remaining visual as `table_or_matrix`, `graph_diagram`, `formula`, `general_visual`, or `decorative`; then route action as `skip`, `minimal_tag`, or `extract`. Insert extracted visual descriptions at corresponding positions.

**FR-PP-09** (Must): The production service must promote the optimized document-processing experiment as-is: AWS Bedrock is the primary live provider, Gemini is fallback, and Groq is final text-only fallback. It must persist the same core artifact classes as the experiment: raw and normalized Markdown, `quality_flags.json`, `visual_classification_trace.json`, `llm_metrics.json`, and aggregate processing metrics.

**FR-PP-04** (Must): All page outputs must be assembled into a single ordered Markdown document that preserves document structure.

**FR-PP-05** (Must): For documents exceeding 50 pages, processing must be split into batches (default 20 pages/batch), processed concurrently via `arq` workers, and merged into the final Markdown preserving page order.

**FR-PP-06** (Must): The OCR/parsing job must be idempotent: re-running it must overwrite (upsert) the existing Markdown output, not append.

**FR-PP-07** (Must): The job must retry up to **3 times** with exponential backoff (1s, 4s, 16s) on transient errors. After 3 failures, the document must transition to `FAILED` state and be moved to the dead-letter queue.

**FR-PP-08** (Must): Only one active processing job may run per document at a time (concurrency guard). New job requests for the same document while a job is running must be rejected.

---

### 4.4 Document Summarization

> Based on `.agent/architecture/document_evaluation_pipeline.md` — Document Summarization section

**FR-DS-01** (Must): After OCR/parsing completes, a **Document Summarization** step must run on the normalized Markdown for **every document** (both Tier 1 and Tier 2). This is the final substep of `PARSING`.

**FR-DS-02** (Must): The Document Summarization must produce a structured `DocumentSummary` record persisted in the database conforming to the Document Summary Contract (v1):

```jsonc
{
  "schema_version": "1.0",
  "topic": "string — primary topic of the document",
  "concepts": ["string — key concepts extracted"],
  "language": "vi | en | mixed",
  "ocr_quality": "high | medium | low",
  "section_summaries": [
    { "heading": "string", "summary": "string", "page_range": [int, int] }
  ],
  "overall_summary": "string — 200-500 word summary"
}
```

**FR-DS-03** (Must): If the normalized Markdown exceeds 50,000 tokens, the summarizer must use a **two-pass** hierarchical strategy:
1. Split Markdown by detected headings/sections → summarize each section independently (parallelizable).
2. Combine section summaries → produce the final structured summary.

**FR-DS-04** (Must): The `DocumentSummary` must be used:
- As primary input to the 3-agent evaluation pipeline (community contributions).
- As metadata source for Mindmap and Mock Test generation (all documents).

---

### 4.5 Document Evaluation Pipeline (3-Agent)

> Based on `.agent/architecture/document_evaluation_pipeline.md` — 3-Agent Pipeline section

**FR-EP-01** (Must): After Document Summarization, community contributions must transition to `EVALUATING` state and enter the 3-agent evaluation pipeline, executed asynchronously via Redis + `arq` workers.

**FR-EP-02** (Must): The pipeline must consume the pre-existing `DocumentSummary` as its primary input. No re-reading of raw Markdown is required.

**FR-EP-03** (Must): All agent outputs must conform to versioned JSON schemas. If an agent returns output that fails schema validation, the job must retry with a corrective prompt. After 3 schema failures, the job must transition to `FAILED`.

#### Agent 1: Course Context Aggregator

**FR-EP-04** (Must): Agent 1 receives: `DocumentSummary` + document metadata + course information.
Agent 1 must output: course context, duplicate indicators, and cold-start flag.

**FR-EP-05** (Must): **Duplicate detection**: The evaluation job must fetch the raw Markdown of the query document from storage, parse it into chunks in-memory, generate chunk embeddings, and compare them against database chunk embeddings of existing approved/indexed documents in the same course. A query document is flagged as a duplicate (`is_duplicate = true`) if its chunk overlap ratio $\ge 0.40$ (where a query chunk matches a candidate chunk if their cosine similarity $\ge 0.85$).

**FR-EP-06** (Must): **Cold-start flag**: `is_cold_start = true` when the course has fewer than 3 approved documents (counting both tiers). In cold-start mode, all non-duplicate community contributions are routed to `NEEDS_REVIEW` regardless of Agent 3 scores.

> **Note**: This flag is distinct from the Seed Document gate in FR-CM-04. By the time Agent 1 runs, the Seed Document is guaranteed to exist (the pipeline is blocked earlier if it does not). Agent 1's cold-start flag is purely a document-count signal.

**FR-EP-07** (Must): Agent 1 output must conform to Agent 1 Output Contract (v1) — see Appendix C.

#### Agent 2: Internet Search Agent

**FR-EP-08** (Must): Agent 2 receives: course identity + document topic (from `DocumentSummary`). Agent 2 must query external sources (using Tavily or SerpAPI) for authoritative references on the document topic.

**FR-EP-09** (Must): Agent 2 must have a **timeout of 15 seconds** and must degrade gracefully: on timeout or error, it returns empty references and does not block the pipeline.

**FR-EP-10** (Must): Agent 2 output must conform to Agent 2 Output Contract (v1) — see Appendix C.

**FR-EP-11** (Must): Agent 2 search results must be visible to Reviewers in the Evaluation Report (not exposed to students).

#### Agent 3: Quality Evaluation Agent

**FR-EP-12** (Must): Agent 3 receives: `DocumentSummary` + outputs from Agents 1–2 + uploader's `initial_contribution_type`. Agent 3 must output three scores (0–10 each):
- **Relevance**: primary metric for approve/reject logic.
- **Completeness**: supplementary metric for reviewer display only.
- **Quality**: supplementary metric for reviewer display only.

**FR-EP-13** (Must): Agent 3 must perform **contribution type verification**:
- Output `suggested_contribution_type` (best match from content analysis).
- Output `label_confidence` (0–1).
- Output `label_mismatch` boolean if suggested differs from initial.
- The agent must NOT override the label — the recommendation is for the reviewer.

**FR-EP-14** (Must): Agent 3 must produce a `recommendation` using the following priority-ordered rules (first matching rule wins):
1. `REJECT`: `is_duplicate = true` (highest priority)
2. `REJECT`: `relevance < 4.0` AND NOT `cold_start`
3. `NEEDS_REVIEW`: `cold_start = true` (overrides score-based APPROVE for non-duplicates)
4. `NEEDS_REVIEW`: `4.0 <= relevance < 7.0`
5. `APPROVE`: `relevance >= 7.0` AND NOT `duplicate` AND NOT `cold_start`

**FR-EP-15** (Must): Completeness and Quality scores must be used **strictly as internal signals** displayed to the Reviewer in the Evaluation Report. They must NOT be used for any public-facing ranking or rejection decisions.

**FR-EP-16** (Must): The `label_mismatch` flag must be strictly informational — it must NOT automatically route the document to `NEEDS_REVIEW`.

**FR-EP-17** (Must): Agent 3 output must conform to Agent 3 Output Contract (v1) — see Appendix C.

**FR-EP-18** (Must): The complete evaluation pipeline output must be persisted as an `EvaluationReport` record linked to the document.

---

### 4.6 Human-in-the-Loop (HITL) Review

**FR-HR-01** (Must): After the evaluation pipeline completes successfully, community contributions must transition to `NEEDS_REVIEW` state and be routed to the Reviewer queue.

**FR-HR-02** (Must): **Review routing logic**:
- System looks up all active `CourseReviewerAssignment` records for `document.course_id`.
- If active reviewers exist: document is added to all their queues. First-come-first-served — when one reviewer acts, the document is removed from other queues.
- If no active reviewer exists: document is routed directly to the Admin review queue with a `no_reviewer` flag. Escalation is immediate (no SLA wait).

**FR-HR-03** (Must): Reviewers must see the following information on the review interface:
- Uploader's initial `contribution_type`
- Agent 3's `suggested_contribution_type` and `label_confidence`
- `label_mismatch` flag (informational)
- Full AI Evaluation Report: Relevance score, Completeness score, Quality score, all recommendation reasons
- Agent 2 external references
- Document viewer (Raw + Markdown tabs, side-by-side available)

**FR-HR-04** (Must): Reviewer actions: **Approve**, **Reject**, or **Approve with Override**.

**FR-HR-05** (Must): When making a decision, the Reviewer must **confirm or override the `contribution_type` label**:
- If `label_mismatch = true`: the Reviewer must explicitly confirm or change the label before approving.
- If no mismatch: the uploader's initial label is pre-selected but remains editable.

**FR-HR-06** (Must): **Mandatory note requirement**: Reviewer must provide a note in the following cases:
- When overriding an AI recommendation of `REJECT` to **Approve** (i.e., the reviewer decides to approve despite the agent recommending rejection).
- When overriding an AI recommendation of `APPROVE` or `NEEDS_REVIEW` to **Reject** (i.e., the reviewer decides to reject despite the agent recommending approval or review).
- When changing the `contribution_type` label (overriding the uploader's or agent's suggested label).

> **Rationale**: Any case where a human decision contradicts AI output in either direction carries risk of bias or error. Mandatory notes create an audit trail for all cross-direction overrides, enabling future calibration of Agent 3 prompts and scoring rubric.

**FR-HR-07** (Must): The `final_contribution_type` confirmed by the Reviewer determines the RAG namespace for post-approval indexing.

**FR-HR-08** (Must): **SLA escalation**: After the configurable SLA expires (default: 48h), documents must be escalated to the Admin review queue with a `sla_breached` flag.

**FR-HR-09** (Must): Every Reviewer decision must be persisted in a `ReviewDecision` record including: `reviewer_id`, `initial_contribution_type`, `suggested_contribution_type`, `final_contribution_type`, decision, note, timestamp.

**FR-HR-10** (Must): All decisions (Approve/Reject/Override) must be logged for future improvement of Agent 3 prompts and scoring rubric.

---

### 4.7 Post-Approval Chunking and Indexing

> Based on ADR-001 (Semantic Chunking) and ADR-002 (RAG Namespace Routing)

**FR-CI-01** (Must): After a document receives final `APPROVED` status, the system must automatically trigger the chunking, embedding, and indexing job. Document transitions to `INDEXING` state.

**FR-CI-02** (Must): **Namespace routing** (tier-aware):
- Official materials (`syllabus`, `textbook`, `lecture_slides`): always indexed into the **knowledge** namespace.
- Community `summary_note`, `review_note`: **knowledge** namespace.
- Community `past_exam`, `solved_exercise`: **exercise** namespace.
- The namespace is determined by the **reviewer-confirmed `final_contribution_type`**, not by the uploader's initial label.

**FR-CI-03** (Must): **Semantic chunking strategy**:
1. **Structure-based splitting**: use document headings, section markers, and paragraph boundaries detected during OCR/normalization as primary split points.
2. **Semantic similarity grouping**: within each structural section, merge or split paragraphs based on embedding cosine similarity. Adjacent paragraphs with high cosine similarity stay together; low-similarity transitions become chunk boundaries.

**FR-CI-04** (Must): Each chunk must carry the following metadata:
- `source_document_id`: parent document ID
- `document_tier`: `official` or `community`
- `material_type` or `contribution_type`: specific subtype (e.g., `lecture_slides`, `past_exam`)
- `rag_namespace`: `knowledge` or `exercise`
- `section_title`: heading from the source document
- `page_number`: original page reference
- `chunk_order`: sequential position within the document

**FR-CI-05** (Must): The chunking/indexing job must be idempotent: re-running must delete existing chunks for the document, then re-create them (delete-then-insert).

**FR-CI-06** (Must): On successful completion, document transitions to `INDEXED` state and becomes available for AI features.

**FR-CI-07** (Must): Job retry policy: up to 3 retries with exponential backoff (1s, 4s, 16s). After 3 failures, document transitions to `FAILED`.

---

### 4.8 Document Viewer

**FR-DV-01** (Must): All `INDEXED` documents must be viewable by any authenticated student enrolled in the course.

**FR-DV-02** (Must): The Document Viewer must provide two tabs:
- **"Nội dung" (Content)** — default: rendered Markdown (`react-markdown` + `remark-gfm` + `remark-math` + `rehype-katex`). Includes heading outline/TOC sidebar for long documents.
- **"Bản gốc" (Original)**: raw uploaded file. PDF: embedded viewer (`react-pdf` or `<iframe>` with signed URL). PPTX: download button only. JPG/PNG: inline `<img>`.

**FR-DV-03** (Must): A **Download** button must always be available for the original file.

**FR-DV-04** (Must): Visibility by document state:

| State | Uploader (Student) | Other Students | Reviewer | Admin |
|-------|-------------------|----------------|----------|-------|
| `UPLOADED` → `PARSING` | Status: "Processing" | ❌ | ❌ | ✅ Raw |
| `EVALUATING` | Status: "Evaluating" | ❌ | ❌ | ✅ Raw + MD |
| `NEEDS_REVIEW` | Status: "Pending review" | ❌ | ✅ Raw + MD + Report | ✅ All |
| `APPROVED` / `INDEXING` | Status: "Approved" | ❌ | ✅ | ✅ |
| `INDEXED` | ✅ Raw + MD | ✅ Raw + MD | ✅ | ✅ |
| `REJECTED` | Status + rejection reason | ❌ | ✅ | ✅ |

**FR-DV-05** (Must): When reviewing a document in `NEEDS_REVIEW`, the Reviewer must see an additional **"Báo cáo đánh giá" (Evaluation Report)** tab showing: scores, label verification, duplicate check, Agent 2 references, and all recommendation reasons.

**FR-DV-06** (Must): Signed URLs for raw file access must have a **TTL of 15 minutes** and must be permission-checked before generation.

**FR-DV-07** (Must): API endpoints for the viewer:
- `GET /api/documents/{id}/markdown` → returns Markdown content (`text/markdown`).
- `GET /api/documents/{id}/raw-url` → returns signed URL for the original file (TTL: 15 min).
Both must enforce per-document, per-role permission checks.

---

### 4.9 Virtual Tutor (RAG)

**FR-VT-01** (Must): Students, Reviewers, and Admins may ask questions in the context of a selected course. The system will deploy a Virtual Tutor Agent operating at the Main Conversation level. The Agent runs a single unified Agent Loop (max 3 iterations), operates without internet access, maintains session-isolated conversation history (short-term buffer + running summary scoped strictly to the current active chat session), and resolves queries using a set of internal tools exposed via microservice APIs.

**FR-VT-02** (Must): The Virtual Tutor Agent must be equipped with the following 4 internal API-based tools:
1. `RAG Retrieval API Tool`: Semantically retrieves relevant text chunks from the course's `knowledge` (and optionally `exercise`) namespaces using the retrieval pipeline:
   ```
   Query → Embedding → MMR Search (k=8, λ=0.7) → Tier Boost (official × 1.15) → Re-rank → Top-k
   ```
2. `Course-Wide Summary Cache Tool`: Retrieves the pre-cached Markdown summary of the entire course curriculum and topics from the database cache.
3. `Document Summary Lookup API Tool`: Retrieves overall document summaries and concept lists.
4. `Course Metadata Explorer API Tool`: Reads the Course Seed and metadata catalog.

**FR-VT-03** (Must): The Virtual Tutor Agent must dynamically coordinate tool execution and decision-making within its loop based on instructions embedded in its system prompt, prioritizing information within local course documents, and compile the final cited response conforming to the Citation Object Contract (v1).
- **System Prompt Decision-Making**: The agent's decision to call a tool, answer directly from history, or rewrite queries must be guided dynamically by system prompt instructions, letting the LLM decide its next action natively.
- **Direct History Answering**: The system prompt instructs the agent that if the query can be fully and accurately answered using the session's conversation history, the LLM should answer directly without calling tools.
- **Query Rewriting**: The system prompt instructs the agent that if new information is needed, the LLM should contextually rewrite the user query (incorporating conversation history) before selecting and executing a tool.
- **Infinite Loop Protection**: The agent loop must enforce a maximum of 3 tool execution iterations.
- **Duplicate Call Detection**: The agent loop must immediately abort if duplicate or redundant tool calls (same tool with the same arguments) are detected.

**FR-VT-04** (Must): **Tier-aware score boost**: after MMR retrieval, official-tier chunks must receive a `score *= 1.15` multiplier before re-ranking. This is a post-retrieval reranking step; both tiers remain in the same index.

**FR-VT-05** (Must): Generator must produce answers using **only** the retrieved context (no hallucination of external knowledge).

**FR-VT-06** (Must): Every Tutor response must include **citation objects** conforming to the Citation Object Contract (v1):

```jsonc
{
  "document_id": "string",
  "document_title": "string",
  "document_tier": "official | community",
  "document_subtype": "string",
  "section_title": "string | null",
  "page_number": "integer | null",
  "chunk_id": "string",
  "chunk_order": "integer",
  "relevance_score": "float (0-1)",
  "excerpt": "string — max 200 chars"
}
```

**FR-VT-07** (Must): The retrieval pipeline must use the net community vote score as a **weighting factor** to prioritize higher community-endorsed documents in Virtual Tutor responses over time.

> **Canonical source**: This requirement is restated from FR-CV-03 for co-location with the Tutor retrieval pipeline spec. FR-CV-03 is the definitive definition; FR-VT-07 is the Tutor-layer view of the same obligation.
>
> **Implementation note**: Vote-weighted retrieval can be implemented as a post-retrieval reranking step (multiply MMR score by a normalized vote weight before final ranking) without requiring vector store re-indexing. This avoids architectural complexity while satisfying the requirement. The specific formula is: `boosted_score = retrieval_score * (1 + vote_weight_factor)` where `vote_weight_factor` is derived from the net vote count normalized against the course average.

**FR-VT-08** (Must): Tutor response latency target: **< 3 seconds** for common queries.

**FR-VT-09** (Must): **Course-Wide Summarization Flow (Cached)**: When a user requests a general course summary, the system must return pre-generated summary data:
1. **Pre-generation Pipeline**: The system automatically executes the summarization pipeline when official documents (Tier 1) are added, modified, or re-indexed:
   a. Collect the Course Seed topic summary and all approved official document summaries (`DocumentTier.OFFICIAL`) from the `knowledge` namespace.
   b. Call the LLM once with this consolidated high-level context.
   c. The LLM must output a structured Markdown summary of the entire course curriculum.
   d. Attach citation objects pointing to the source official documents.
2. **Caching**: Store the generated Markdown and citations in the `course_summaries_cache` table.
3. **Retrieval in Agent Loop**: The Virtual Tutor Agent detects the request for a general course summary, selects the `Course-Wide Summary Cache Tool` in the first iteration of the loop, retrieves the cached summary, and returns it directly, bypassing real-time LLM execution.

---

### 4.10 Mindmap Generation

**FR-MM-01** (Must): Mindmap generation must be available per course for any authenticated user. It generates a hierarchical concept map from all INDEXED documents in the course's **knowledge** namespace.

**FR-MM-02** (Must): The Mindmap pipeline must run the following 4-phase iterative map-reduce process:

**Phase 1 — Collect pre-extracted metadata** (no LLM call):
- Collect all `DocumentSummary` records for the course's knowledge-namespace documents.
- No additional LLM call needed; summaries contain `section_summaries`, `concepts`, `overall_summary`.

**Phase 2 — Build initial concept graph** (1 LLM call):
- Input: all collected summaries + Course Seed Document topic summary.
- Output: a structured concept graph JSON (nodes + edges).

```jsonc
// Concept Graph Node (v1)
{
  "nodes": [
    {
      "id": "string",
      "label": "string — concept name",
      "level": "integer (0=course, 1=topic, 2=subtopic, 3=concept)",
      "source_documents": ["document_ids"]
    }
  ],
  "edges": [
    { "source": "node_id", "target": "node_id", "relation": "contains | prerequisite | related" }
  ]
}
```

**Phase 3 — Selective deep-dive** (iterative; optional):
- For under-specified topics (too few child concepts relative to source document count):
  1. Retrieve relevant chunks for that topic from the vector store.
  2. Extract additional sub-concepts and relationships.
  3. Merge new nodes/edges into the existing graph.

**Phase 4 — Render**:
- Convert the final concept graph to an interactive mindmap in the UI (e.g., `reactflow`, `d3.js`, or `markmap`).

**FR-MM-03** (Must): The generated concept graph must be cached per course as a `MindmapArtifact` record.

**FR-MM-04** (Must): Cache must be invalidated when a new document reaches `INDEXED` state in the course.

**FR-MM-05** (Should): Users must be able to manually trigger mindmap regeneration.

---

### 4.11 Mock Test Generation

**FR-MT-01** (Must): Mock test generation must be available per course. Tests draw from both **knowledge** and **exercise** namespaces.

**FR-MT-02** (Must): The Mock Test pipeline must run the following 4-phase plan-then-generate process:

**Phase 1 — Topic inventory** (no LLM call):
- Collect document summaries for the course.
- Build a topic → source chunks mapping using Course Seed Document and `DocumentSummary.section_summaries`.

**Phase 2 — Test plan** (1 LLM call):
- Given topic inventory and user configuration (total questions, difficulty distribution), generate a test plan:
```jsonc
{
  "total_questions": "integer",
  "plan": [
    {
      "topic": "string",
      "question_count": "integer",
      "difficulty": "easy | medium | hard",
      "question_types": ["multiple_choice | short_answer | true_false"],
      "source_document_ids": ["string"]
    }
  ]
}
```

**Phase 3 — Per-topic question generation** (1 LLM call per topic):
- Retrieve relevant chunks for each topic (both namespaces).
- Generate questions with answer keys and citations.
- Output per question:
```jsonc
{
  "question_text": "string",
  "question_type": "multiple_choice | short_answer | true_false",
  "difficulty": "easy | medium | hard",
  "topic": "string",
  "options": ["string — for multiple choice, null otherwise"],
  "correct_answer": "string",
  "explanation": "string",
  "citations": ["Citation Object"]
}
```

**Phase 4 — Validation and assembly** (1 LLM call):
- Deduplicate questions (embedding similarity > 0.85 → remove duplicate).
- Verify answer consistency.
- Assemble final test ordered by topic then difficulty.
- Store as `MockTestItem` records for reuse and review.

**FR-MT-03** (Must): Each question must include source citations using the Citation Object Contract (v1).

**FR-MT-04** (Must): User must be able to configure: total number of questions, difficulty distribution.

---

### 4.12 Contribution Ranking and Leaderboard

**FR-CR-01** (Must): Each approved **community contribution** must earn the uploader contribution points using the formula:
```
points = base_points * (relevance / 10)
base_points: summary_note = 10, review_note = 8, past_exam = 7, solved_exercise = 7
```
where `relevance` is the Agent 3 Relevance score for the document.

**FR-CR-02** (Must): Points are only awarded for community contributions. Official materials uploaded by Admin/Reviewer do not earn points.

**FR-CR-03** (Must): Both **per-course** and **global** leaderboards must be displayed to all users.

**FR-CR-04** (Should): Top contributors must be highlighted on course pages.

**FR-CR-05** (Should): Ranking accumulation period (semester-based vs cumulative) must be configurable by Admin.

---

### 4.13 Community Voting

**FR-CV-01** (Must): Any authenticated student may **upvote or downvote** any `INDEXED` document. One vote per user per document.

**FR-CV-02** (Must): Net community vote score must be the **primary metric** for:
- Default UI sorting order for community contributions on course pages.
- "Highly Recommended" badge assignment (badge displayed on documents exceeding a configurable vote threshold).

**FR-CV-03** (Must): The RAG retrieval pipeline must use the net community vote score as a **weighting factor** to prioritize higher community-endorsed documents during Virtual Tutor responses over time.

**FR-CV-04** (Must): Community votes operate independently from the AI evaluation scores (Relevance, Completeness, Quality). AI scores must NOT influence public-facing ranking. Only community votes determine public ranking.

**FR-CV-05** (Must): AI-generated Completeness and Quality scores must only be visible to Reviewers in the Evaluation Report dashboard (internal signals only).

---

### 4.14 Admin Dashboard

**FR-AD-01** (Must): Admin must have a dedicated dashboard. The dashboard must provide at minimum the following sections:
- **Dead-Letter Queue**: list of all `FAILED` documents with failure reason and raw agent output visible per document.
- **Escalation Review Queue**: documents routed to Admin due to SLA breach (`sla_breached` flag) or missing assigned reviewer (`no_reviewer` flag). Admin can take one of two actions: (a) review and decide directly (Approve/Reject), or (b) first assign a reviewer to the course then transfer the document to the reviewer's queue.
- **Reviewer Management**: assign/unassign Reviewers to courses. View current active assignments per course.
- **Course & Seed Document Management**: create/update courses, create/update Course Seed Documents, trigger topic_tags catalog regeneration (see FR-CM-07).
- **SLA Configuration**: set review SLA duration per course (default 48h; range 24h–72h).

**FR-AD-02** (Must): Admin must be able to trigger the following **dead-letter job controls** per document:
- **Trigger reprocess**: re-enqueue the job from scratch (`FAILED → PARSING` for OCR failures, `FAILED → EVALUATING` for pipeline failures).
- **Mark as permanently failed**: exclude the document from further processing. Document stays in `FAILED` state with a `permanently_failed = true` flag.
- **Inspect raw failure**: view the complete failure reason and the raw agent output (or OCR error) that caused the failure.

**FR-AD-03** (Must): Admin must be able to trigger the following **state override transitions**, which are not available to Reviewers:
- `FAILED → PARSING`: trigger reprocess (OCR/parsing retry).
- `FAILED → EVALUATING`: trigger re-evaluation (agent pipeline retry, skipping re-OCR).
- `REJECTED → PARSING`: trigger reprocess (rare manual override — resets full processing chain).

**FR-AD-04** (Must): Admin must be able to **directly review and decide** (Approve/Reject with mandatory note) on documents in the following states:
- Documents in `NEEDS_REVIEW` state (including those in the escalation queue with `sla_breached` or `no_reviewer` flags).
- Documents in `FAILED` or `REJECTED` states before triggering a reprocess transition.

Admin does **not** bypass the `PARSING` or `EVALUATING` states mid-execution — documents currently being processed cannot be force-decided until the active job completes or transitions to `FAILED`. This preserves state machine integrity.

> **Rationale**: "Full authority" (project_description.md §3 Admin) means Admin can act wherever a human decision point exists, not that Admin can interrupt an in-flight async job. The state machine's async job states (`PARSING`, `EVALUATING`, `INDEXING`) are system-driven, not human-actor states.

**FR-AD-05** (Must): All admin-initiated actions (state transitions, reviewer assignments, course seed changes, SLA changes, escalation decisions) must be logged in the audit log: `{actor_id, action_type, target_entity, from_state, to_state, timestamp, reason}`.

---

## 5. Non-Functional Requirements

### 5.1 Performance

| Requirement | Target |
|-------------|--------|
| Virtual Tutor response latency | < 3 seconds for common queries |
| Document pipeline end-to-end | < 5 minutes for common file sizes (< 50 pages) |
| API endpoint response (non-AI) | < 500 ms (p95) |
| Mindmap generation (cached) | < 1 second |
| Mindmap generation (cold) | < 60 seconds |

### 5.2 Security

**NFR-SEC-01** (Must): All actions must require authentication. Unauthenticated requests must be rejected with `401 Unauthorized`.

**NFR-SEC-02** (Must): Role-based access control (RBAC) must be enforced at the API level. See Permission Matrix in Appendix B.

**NFR-SEC-03** (Must): Signed URLs for raw file access must have a TTL of 15 minutes.

**NFR-SEC-04** (Must): Student uploads are bound to academic-use only. Uploader must consent at upload time.

**NFR-SEC-05** (Must): Sensitive configuration (API keys, database credentials) must not be hardcoded. Use environment variables (`.env`).

### 5.3 Reliability

**NFR-REL-01** (Must): All async jobs must implement idempotency (see FR-PP-06, FR-CI-05).

**NFR-REL-02** (Must): Retry policy: up to 3 retries with exponential backoff (1s, 4s, 16s) for transient errors.

**NFR-REL-03** (Must): Failed jobs must be moved to the dead-letter queue and made visible to Admin.

**NFR-REL-04** (Must): Concurrency guard: only one active job per document at a time.

**NFR-REL-05** (Must): Schema validation: agent output that fails JSON schema validation triggers a corrective-prompt retry.

### 5.4 Traceability

**NFR-TRC-01** (Must): Every document state transition must be logged with: `{document_id, from_state, to_state, actor, timestamp, reason}`.

**NFR-TRC-02** (Must): All AI evaluation decisions must be persisted in `EvaluationReport` records.

**NFR-TRC-03** (Must): All HITL decisions must be persisted in `ReviewDecision` records.

**NFR-TRC-04** (Must): All admin actions (reprocess triggers, reviewer assignments, course seed changes) must be logged.

### 5.5 Scalability

**NFR-SCA-01** (Should): The architecture must support growth from pilot (< 5 courses) to full SoICT catalogue (> 50 courses) without major redesign.

**NFR-SCA-02** (Should): Background worker count must be horizontally scalable.

**NFR-SCA-03** (Should): Retrieval namespaces scoped per course prevent cross-course contamination and allow collection-level scaling.

### 5.6 Maintainability

**NFR-MNT-01** (Should): All pipeline contracts (agent inputs/outputs, Citation Object, Summary schema) must be versioned with `schema_version` fields.

**NFR-MNT-02** (Should): Source code lives exclusively in `src/` (Git repository root for code).

**NFR-MNT-03** (Should): Agent prompts and scoring thresholds (e.g., duplicate similarity threshold, cold-start document count, SLA duration, MMR parameters) must be configurable per deployment without code changes.

### 5.7 AI Quality Targets

| Metric | Target |
|--------|--------|
| Faithfulness | ≥ 0.80 |
| Answer Relevancy | ≥ 0.85 |
| Citation Accuracy | ≥ 0.90 |
| Hallucination Rate | < 5% |

**Evaluation strategy:**
- Automatic: RAGAS + DeepEval framework.
- Manual: Author audit on a sampled question set.

---

## 6. External Interface Requirements

### 6.1 User Interfaces

**FR-UI-01**: Course list page and course detail pages.  
**FR-UI-02**: **Official Materials tab** on course detail — Admin/Reviewer upload with `material_type`, version history display.  
**FR-UI-03**: **Community Contributions tab** on course detail — Student upload with `contribution_type` + `topic_tags`, status tracking, filters by type/topic, vote controls.  
**FR-UI-04**: **Document Viewer** (2 tabs: Markdown content + Raw original, download button).  
**FR-UI-05**: **Reviewer Dashboard** with Evaluation Report tab and side-by-side OCR verification mode.  
**FR-UI-06**: **Admin Dashboard** with dead-letter queue, reviewer management, course management.  
**FR-UI-07**: **Tutor tab** with chat interface, citations rendered per response, retrieval scope toggle (knowledge / knowledge + exercise).  
**FR-UI-08**: **Mindmap tab** with interactive concept graph and manual regeneration trigger.  
**FR-UI-09**: **Mock Test tab** with configuration form (total questions, difficulty distribution) and test display with answers and citations.  
**FR-UI-10**: **Leaderboard** — per-course and global, showing contribution points.

### 6.2 Software Interfaces

| Interface | Technology | Notes |
|-----------|-----------|-------|
| Database | PostgreSQL 15+ | Primary relational store; local container and AWS RDS PostgreSQL cloud target share the same schema |
| Vector store | pgvector | Embedding index, per-course + per-namespace collections |
| Object storage | S3-compatible object storage | MinIO locally; Cloudflare R2 in cloud deployment; raw files and Markdown files |
| Job queue | Redis + `arq` | Async pipeline workers (per ADR-003) |
| LLM/OCR provider chain | AWS Bedrock → Gemini → Groq text-only fallback | OCR vision, normalization, summarization, agent prompts, generation |
| Web search | Tavily or SerpAPI | Agent 2 external reference lookup |
| Frontend framework | React / Next.js | Web application |
| Backend framework | Python / FastAPI | REST API server |
| Embedding model | `sentence-transformers/all-MiniLM-L6-v2` for MVP; pgvector storage | Document and query embeddings; future Gemini embedding swap requires reindex |

### 6.3 Communication Interfaces

- All client-server communication over HTTPS REST API.
- Background job communication via Redis + `arq` queue.
- Signed storage URLs served with short TTL (15 minutes).

---

## 7. Data Model Requirements

### 7.1 Core Entities

| Entity | Key Fields | Notes |
|--------|-----------|-------|
| `Course` | `id`, `code`, `name`, `description`, `topic_summary` | Course Seed Document fields embedded |
| `User` | `id`, `role` (`student \| reviewer \| admin`), `email` | |
| `CourseReviewerAssignment` | `user_id`, `course_id`, `assigned_at`, `assigned_by`, `is_active` | Soft-delete for unassignment |
| `Document` | `id`, `course_id`, `uploader_id`, `document_tier`, `material_type \| contribution_type`, `topic_tags`, `status`, `version` | Status per state machine |
| `DocumentSummary` | `document_id`, `topic`, `concepts`, `language`, `ocr_quality`, `section_summaries`, `overall_summary` | 1:1 with Document |
| `DocumentChunk` | `document_id`, `section_title`, `chunk_order`, `document_tier`, `rag_namespace`, `embedding` | Many:1 with Document |
| `EvaluationJob` | `document_id`, `status`, `created_at`, `updated_at` | Community contributions only |
| `EvaluationReport` | `document_id`, `agent1_output`, `agent2_output`, `agent3_output`, `recommendation` | Community contributions only |
| `ReviewDecision` | `evaluation_report_id`, `reviewer_id`, `initial_contribution_type`, `suggested_contribution_type`, `final_contribution_type`, `decision`, `note`, `timestamp` | |
| `Citation` | `chunk_id`, `document_id`, `section_title`, `page_number`, `excerpt`, `relevance_score` | Used in Tutor + Mock Test |
| `MindmapArtifact` | `course_id`, `concept_graph_json`, `generated_at`, `is_cached` | Cached per course |
| `MockTestItem` | `course_id`, `question_text`, `question_type`, `difficulty`, `topic`, `correct_answer`, `explanation`, `citations` | |
| `ContributionScore` | `user_id`, `course_id`, `points`, `rank` | Community contributions only |
| `CommunityVote` | `user_id`, `document_id`, `vote` (`up \| down \| null`) | One vote per user per document |

### 7.2 Key Relationships

- `Document.course_id → Course.id` (required, partition key for all features)
- `DocumentSummary.document_id → Document.id` (1:1, every document has exactly one summary)
- `DocumentChunk.document_id → Document.id` (1:N)
- `EvaluationReport.document_id → Document.id` (community contributions only)
- `ReviewDecision.evaluation_report_id → EvaluationReport.id`
- `ReviewDecision.reviewer_id → User.id`
- `CourseReviewerAssignment.user_id → User.id`
- `CourseReviewerAssignment.course_id → Course.id`

### 7.3 Recommended Indexes

- `Document(course_id, status, created_at)` — for course-level document browsing
- Vector index on `DocumentChunk.embedding` — for semantic retrieval
- `EvaluationJob(status, updated_at)` — for job monitoring and dead-letter detection
- `CourseReviewerAssignment(course_id, is_active)` — for fast reviewer lookup during review routing

### 7.4 Storage Layout

```
S3-compatible object storage:
  documents/
    {course_id}/
      {document_id}/
        raw/           ← original uploaded file (PDF/PPTX/PNG) — immutable
        markdown/      ← normalized .md file from OCR/parsing — overwritten on reprocess
```

---

## 8. System Constraints and Assumptions

### 8.1 Scope Limitations

| In Scope | Out of Scope |
|----------|-------------|
| SoICT students | General public users |
| Official SoICT course list (pre-populated by Admin) | Non-course-based document ingestion |
| PDF (unencrypted), JPG/PNG, PPTX | Video/audio ingestion |
| Vietnamese and English | Other languages |
| Pilot scale (< 20 courses initially) | Large-scale production rollout |
| Best-effort formula rendering (LaTeX) | Guaranteed mathematical formula accuracy |

### 8.2 Operational Constraints

1. All file processing runs asynchronously. No synchronous long-running operations in user-facing flows.
2. Every state transition requires an authenticated actor and produces an audit log entry.
3. AI scores (Completeness, Quality) are internal reviewer signals only — never exposed publicly.
4. Community votes are the sole public-facing ranking mechanism.
5. **"Full evaluation mode" definition**: A course is in full evaluation mode when it has both a Course Seed Document AND at least 3 approved documents. In full evaluation mode, Agent 3's auto-approve path is active (relevance ≥ 7.0 → `APPROVE` directly). Without full evaluation mode (cold-start), the pipeline still runs but the auto-approve path is disabled — all non-duplicate contributions are forced to `NEEDS_REVIEW` regardless of Agent 3 scores. Without a Seed Document, the pipeline does not run at all (upload blocked at submission, per FR-CM-04 Level 1).
6. Only Admin can trigger job reprocessing and resolve dead-letter queue items.

### 8.3 Implementation Priority (Build Order)

1. Course model, role model, and authentication.
2. Upload + OCR/parsing → normalized Markdown (no chunking at this stage).
3. Evaluation pipeline with persisted reports.
4. HITL dashboard and decision loop.
5. Post-approval chunking, embedding, and indexing.
6. Virtual Tutor with citations.
7. Mindmap and Mock Test generation.
8. Evaluation harness (RAGAS/DeepEval + audit workflow).

### 8.4 Definition of Done

The system is considered complete for thesis scope when:
- Core features are functional end-to-end in a course context.
- Evaluation pipeline and HITL loop are operational with audit logs.
- Tutor answers include valid citations.
- Mindmap and Mock Test features run on approved course documents.
- Quality and performance targets are measured and reported.

---

## Appendix A: Document Lifecycle State Machine

```
                      ┌──────────────┐
Upload ─────────────▶ │   UPLOADED   │
                      └──────┬───────┘
                             │ OCR/parse job starts
                             ▼
                      ┌──────────────┐
                      │   PARSING    │──── error ───▶ FAILED
                      └──────┬───────┘
                             │ Markdown + Structured Summary ready
                      ┌──────┴──────────────────────────┐
                      │ (Community)                      │ (Official — skips evaluation)
                      ▼                                  ▼
               ┌──────────────┐                   ┌──────────┐
               │  EVALUATING  │──── error ──▶ FAILED│ APPROVED │
               └──────┬───────┘                   └────┬─────┘
                      │ Agent pipeline complete         │
                      ▼                                 │
               ┌──────────────┐                        │
               │ NEEDS_REVIEW │                        │
               └──────┬───────┘                        │
                      │ Reviewer action         ┌───────┘
             ┌────────┴────────┐                │
             ▼                 ▼                ▼
       ┌──────────┐     ┌──────────┐     ┌──────────┐
       │ APPROVED │     │ REJECTED │     │ INDEXING │──── error ─▶ FAILED
       └────┬─────┘     └──────────┘     └────┬─────┘
            │ Post-approval job               │
            ▼                                 ▼
       ┌──────────┐                     ┌──────────┐
       │ INDEXING │                     │  INDEXED │  (available for AI features)
       └────┬─────┘                     └──────────┘
            │
            ▼
       ┌──────────┐
       │  INDEXED │
       └──────────┘
```

**Allowed transitions:**

| From | To | Trigger |
|------|----|---------| 
| `UPLOADED` | `PARSING` | System auto-triggers OCR job |
| `PARSING` | `EVALUATING` | Markdown + structured summary ready (community) |
| `PARSING` | `APPROVED` | Markdown + structured summary ready (official) |
| `PARSING` | `FAILED` | OCR/parse error after retries |
| `EVALUATING` | `NEEDS_REVIEW` | Agent pipeline completes |
| `EVALUATING` | `FAILED` | Agent pipeline error after retries |
| `NEEDS_REVIEW` | `APPROVED` | Reviewer approves |
| `NEEDS_REVIEW` | `REJECTED` | Reviewer rejects |
| `APPROVED` | `INDEXING` | System auto-triggers chunking job |
| `INDEXING` | `INDEXED` | Chunks embedded successfully |
| `INDEXING` | `FAILED` | Embedding/indexing error after retries |
| `FAILED` | `PARSING` | Admin triggers reprocess |
| `FAILED` | `EVALUATING` | Admin triggers re-evaluation |
| `REJECTED` | `PARSING` | Admin triggers reprocess (rare) |

**Rules:**
- Only `INDEXED` documents are available for AI features (Tutor, Mindmap, Test).
- Only Admin can trigger transitions out of `FAILED` or `REJECTED` states.
- Every transition writes an audit log entry: `{document_id, from_state, to_state, actor, timestamp, reason}`.

---

## Appendix B: Permission Matrix

| Action | Student | Reviewer | Admin |
|--------|---------|----------|-------|
| Upload community contribution | ✅ Own courses | ❌ | ✅ |
| Upload official material | ❌ | ✅ Assigned courses | ✅ |
| View own uploads & status | ✅ | ✅ Assigned courses | ✅ All |
| View INDEXED documents (Raw + Markdown) | ✅ | ✅ | ✅ |
| Use AI features (Tutor/Mindmap/Test) | ✅ INDEXED docs | ✅ | ✅ |
| Review & approve/reject documents | ❌ | ✅ Assigned courses only | ✅ All |
| Override contribution type label | ❌ | ✅ (with note) | ✅ |
| Override AI recommendation² | ❌ | ✅ (with note) | ✅ |
| Trigger reprocess (re-OCR / re-evaluate) | ❌ | ❌ | ✅ |
| View external references (Agent 2) | ❌ | ✅ In eval report | ✅ |
| Assign/unassign reviewers to courses | ❌ | ❌ | ✅ |
| Manage courses & Course Seed Documents | ❌ | ❌ | ✅ |
| Resolve failed/dead-letter jobs | ❌ | ❌ | ✅ |
| View leaderboard | ✅ | ✅ | ✅ |
| Vote on documents (upvote/downvote) | ✅ | ⚠️ Not specified in source¹ | ❌ |

> ¹ **Reviewer voting**: The source `project_description.md` §6.10 grants vote access to "students" and does not address Reviewers. Marked as unspecified. Implementation team should confirm and update `project_description.md` before implementation.
>
> ² **"Override evaluation score" in source matrix** (project_description.md §4, line 69): This row was originally labeled "Override evaluation score" in the source, but no functional requirement for directly editing Agent 3 numeric scores exists. The correct interpretation — consistent with the system's design where scores are immutable AI outputs — is that Reviewers can **override the AI recommendation** (change Approve/Reject decision, change `contribution_type` label). The row has been renamed accordingly. Editing raw score values is not supported.
>
> **Voting actors resolution**: Source §6.10 restricts voting to students. Admin does not vote (❌) — Admin's role is system management, not content evaluation. This is consistent with the source permission matrix which does not include a voting row at all.


---

## Appendix C: Data Schemas and Contracts

All schemas are versioned and stored in `data/schemas/`. Key contracts referenced in this SRS:

### C.1 Document Summary Contract (v1)
Schema file: `data/schemas/document_summary.schema.json`

```jsonc
{
  "schema_version": "1.0",
  "topic": "string",
  "concepts": ["string"],
  "language": "vi | en | mixed",
  "ocr_quality": "high | medium | low",
  "section_summaries": [
    { "heading": "string", "summary": "string", "page_range": [int, int] }
  ],
  "overall_summary": "string (200-500 words)"
}
```

### C.2 Agent 1 Output Contract (v1)
Schema file: `data/schemas/agent1_output.schema.json`

```jsonc
{
  "schema_version": "1.0",
  "course_context": {
    "syllabus_topic_summary": "string",
    "existing_document_count": "integer",
    "topic_coverage": { "topic_name": "covered | partial | missing" }
  },
  "duplicate": {
    "is_duplicate": "boolean",
    "duplicate_of_document_id": "string | null",
    "similarity_score": "float (0-1)"
  },
  "cold_start": {
    "is_cold_start": "boolean",
    "reason": "string | null"
  }
}
```

### C.3 Agent 2 Output Contract (v1)
Schema file: `data/schemas/agent2_output.schema.json`

```jsonc
{
  "schema_version": "1.0",
  "references": [
    {
      "title": "string",
      "url": "string",
      "snippet": "string",
      "source_type": "textbook | course_page | paper | other"
    }
  ],
  "search_status": "success | timeout | error",
  "search_duration_ms": "integer"
}
```

### C.4 Agent 3 Output Contract (v1)
Schema file: `data/schemas/agent3_output.schema.json`

```jsonc
{
  "schema_version": "1.0",
  "scores": {
    "relevance": "float (0-10)",
    "completeness": "float (0-10)",
    "quality": "float (0-10)"
  },
  "label_verification": {
    "initial_contribution_type": "past_exam | summary_note | review_note | solved_exercise",
    "suggested_contribution_type": "past_exam | summary_note | review_note | solved_exercise",
    "label_confidence": "float (0-1)",
    "label_mismatch": "boolean"
  },
  "recommendation": "APPROVE | NEEDS_REVIEW | REJECT",
  "recommendation_reasons": ["string"],
  "duplicate_flag": "boolean",
  "cold_start_flag": "boolean"
}
```

### C.5 Citation Object Contract (v1)

```jsonc
{
  "document_id": "string",
  "document_title": "string",
  "document_tier": "official | community",
  "document_subtype": "string",
  "section_title": "string | null",
  "page_number": "integer | null",
  "chunk_id": "string",
  "chunk_order": "integer",
  "relevance_score": "float (0-1)",
  "excerpt": "string (max 200 chars)"
}
```

### C.6 RAG Namespace Routing Table

| Document Tier | Subtype | RAG Namespace |
|--------------|---------|---------------|
| Official | `syllabus`, `textbook`, `lecture_slides` | **knowledge** |
| Community | `summary_note`, `review_note` | **knowledge** |
| Community | `past_exam`, `solved_exercise` | **exercise** |

*Namespace for community contributions is determined by the **reviewer-confirmed `final_contribution_type`**, not the uploader's initial label.*

---

### Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-04-20 | Antigravity | Initial release — synthesized from all architecture docs |
| 1.1 | 2026-04-20 | Antigravity | Round-1 review fixes: cold-start two-level gate; FR-AD expanded; FR-HR-06 bidirectional note; FR-CM-07 topic_tags; permission matrix corrections |
| 1.1 | 2026-04-20 | Antigravity | Round-2 conflict resolution: FR-VT-07 restored to Must + impl note; Section 8.2 constraint 5 disambiguates "full eval mode"; FR-AD-04 scoped to NEEDS_REVIEW/escalation only; Admin voting corrected to ❌; "Override evaluation score" renamed to "Override AI recommendation²" with footnote |
| 1.2 | 2026-06-02 | Backend Manager | Queue runtime change: `BullMQ` → `arq` (per ADR-003). Updated FR-PP-05, FR-EP-01, §1.3 Acronyms, §2.1, §2.5, §6.2, §6.3. Rationale: backend Python-only stack — Node.js dispatcher adds runtime overhead without value. |
| 1.3 | 2026-06-02 | Codex | Align with `project_plan.md`: remove Supabase as default DB/storage stack; set PostgreSQL+pgvector local/Azure target and S3-compatible MinIO/R2 storage. Align processing requirements with optimized document-processing experiment: Azure primary, Gemini/Groq fallback, slide PDF routing, visual classification/action routing, and metrics/artifacts persistence. |
| 1.6 | 2026-06-15 | Thesis Team | Bump version to sync with module registry and backend architecture changes. Document state transitions updated. |

*End of SRS v1.6 — 2026-06-15*
