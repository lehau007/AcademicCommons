# GitHub Copilot Instructions — Community Academic Knowledge System

## Project Context
This is a graduation thesis project: a course-centric academic knowledge platform where students upload learning documents, pass them through an AI + human review pipeline, and use approved materials through AI features (Virtual Tutor, Mindmap, Mock Tests).

## Shared Agent Context
**IMPORTANT**: Before starting any work, read the shared context files:
- **Project Specification**: `.agent/project_description.md` — the complete system design document.
- **Session Journal**: `.agent/context/JOURNAL.md` — recent session activity (read latest 2-3 entries).
- **Module Registry**: `.agent/context/REGISTRY.md` — what modules exist, where, and their status.
- **Architecture Decisions**: `.agent/architecture/` — non-obvious design choices already made.

When finishing a session, you MUST:
1. Append a journal entry to `.agent/context/JOURNAL.md` (use the template inside).
2. Update `.agent/context/REGISTRY.md` if any modules were created or modified.

## Tech Stack
- **Backend**: Python (FastAPI), LangChain/LlamaIndex
- **Frontend**: React / Next.js
- **Database**: Supabase PostgreSQL + pgvector
- **Queue**: Redis + BullMQ
- **LLM/OCR**: Gemini (primary), fallback providers
- **CI/CD**: GitHub Actions

## Code Conventions
- Backend code lives in `src/backend/`
- Frontend code lives in `src/frontend/`
- Shared types/constants live in `src/shared/`
- All AI/document operations must include `course_id` as a partition key
- All AI outputs must be traceable (citations, evaluation reports, decision logs)
- Use type hints in Python; use TypeScript (not plain JS) in frontend

## Architecture Key Points
- Documents follow a 2-tier model: official materials and community contributions
- OCR/parsing produces full normalized text (NOT chunked at this stage)
- Chunking happens AFTER document approval (semantic chunking, not naive overlap)
- RAG uses separate namespaces per course (`knowledge`, `exercise`); for community contributions, namespace is assigned after review based on reviewer-confirmed `final_contribution_type`
- See `.agent/architecture/` for detailed Architecture Decision Records
