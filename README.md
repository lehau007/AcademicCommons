# Community Academic Knowledge Digitization and Management System

A course-centric academic knowledge platform for SoICT students. Upload learning materials → AI + human review pipeline → use approved documents through Virtual Tutor (RAG), Mindmap, and Mock Test features.

## Graduation Thesis
- **Author**: Lê Văn Hậu
- **Institution**: SoICT, Hanoi University of Science and Technology
- **Advisors**: [Advisor names]

## Tech Stack
- **Backend**: Python / FastAPI / LangChain / LlamaIndex
- **Frontend**: React / Next.js
- **Database**: Supabase (PostgreSQL + pgvector)
- **Queue**: Redis + BullMQ
- **LLM**: Gemini 3.5 Flash Lite
- **OCR**: Gemini Vision / Google Cloud Vision

## Project Structure

```
GraduationThesis/
├── docs/                    # Human-facing thesis documents
│   ├── thesis/              #   Official plans, proposals
│   └── references/          #   Research papers, external refs
│
├── .agent/                  # Shared agent context (all AI agents read this)
│   ├── project_description.md    # Master project specification
│   ├── architecture/        #   Architecture Decision Records (ADRs)
│   ├── context/             #   Cross-session context
│   │   ├── REGISTRY.md      #     Module map (what exists, where, status)
│   │   └── JOURNAL.md       #     Session work log (append-only)
│   └── workflows/           #   Shared task workflows
│
├── src/                     # 📦 GIT REPO ROOT (all source code)
│   ├── backend/             #   Python FastAPI backend
│   ├── frontend/            #   Next.js frontend
│   └── .gitignore
│
├── data/                    # Private data (gitignored)
│   ├── schemas/             #   JSON schemas for pipeline contracts
│   ├── seed/                #   Course list, users, reviewer assignments
│   ├── sample/              #   Sample documents organized by tier
│   │   ├── official/        #     Tier 1: {course}/{material_type}/
│   │   └── community/       #     Tier 2: {course}/{contribution_type}/
│   └── pipeline_outputs/    #   Expected pipeline outputs (ground truth)
└── 
```

## Latest Results — Document Processing v4

Live benchmark of the current ingest pipeline (text-first extraction, figures kept as image assets, no LLM normalization), run on 2026-09-27 with real Vertex Gemini calls: 10 real course files (127 pages) + 2 synthetic stress documents.

- **Speed**: a 189-page slide deck in **91 s** (~0.5 s/page); a 40-page scanned PDF with full OCR in **43 s** (~1.1 s/page). The previous pipeline (v3) needed ~30 min for a 200-page document, so v4 is roughly **20× faster**. Wall time depends on Vertex latency (the same deck took 40 s in the previous run).
- **Quality**: token recall vs. human-written ground truth is **0.82** averaged over 10 files (v3: 0.85). Without the one standalone chart image, whose ground truth is mostly a free-form description, it is **0.88** (v3: 0.86).
- **Reliability**: 162 vision calls with 1 failure, recovered by the fallback model; 0 pages lost.
- **Gates**: G1 (~190 pages ≤ 180 s) PASS · G2 (scanned PDF ≤ 120 s) PASS · 

## Quick Start

The entire stack (Backend, Frontend, Database, Workers, etc.) can be run effortlessly using Docker Compose.

```bash
# 1. Setup environment variables (if not already done)
cp src/backend/.env.example src/backend/.env
# (Optional) Update src/backend/.env with your actual API keys

# 2. Build and start all services
docker compose up -d --build

# Alternatively, you can use the provided Makefile:
# make up
```

## License
Internal academic use only. Materials contributed through this platform are subject to sharing consent policies.
