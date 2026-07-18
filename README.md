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
- **LLM**: Moonshot Kimi K2.5
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
