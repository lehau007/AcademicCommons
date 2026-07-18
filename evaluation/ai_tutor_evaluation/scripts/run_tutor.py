"""Generate `actual/<qid>.json` for the AI tutor evaluation.

Runs INSIDE the `api` container (same code path as POST /tutor/query):

    docker cp evaluation/ai_tutor_evaluation graduationthesis-api-1:/tmp/tutor_eval
    docker exec graduationthesis-api-1 python /tmp/tutor_eval/scripts/run_tutor.py \
        --questions /tmp/tutor_eval/dataset/questions.json --out /tmp/tutor_eval/actual
    docker cp graduationthesis-api-1:/tmp/tutor_eval/actual evaluation/ai_tutor_evaluation/

For each question it creates a fresh ChatSession (admin user), wraps RetrievalService with a
recorder so ALL retrieved chunks are captured (not just cited ones), and calls
tutor_query_agent_loop. Resumable: existing <qid>.json files are skipped.
"""
from __future__ import annotations

import argparse
import asyncio
import json
import time
from pathlib import Path

from sqlalchemy import select

from app.config import get_settings
from app.db.session import AsyncSessionLocal
from app.llm.router import build_llm_router
from app.models import ChatSession, Course, User
from app.services.retrieval_service import get_retrieval_service
from app.services.tutor_service import tutor_query_agent_loop

ADMIN_EMAIL = "admin@soict.hust.edu.vn"


class RecordingRetrieval:
    """Wraps RetrievalService and records every search call + returned chunks."""

    def __init__(self, inner):
        self._inner = inner
        self.calls: list[dict] = []

    async def search(self, session, course_id, query, namespaces=None, k=8,
                     prefetch_k=40, document_ids=None):
        chunks = await self._inner.search(
            session, course_id=course_id, query=query, namespaces=namespaces,
            k=k, prefetch_k=prefetch_k, document_ids=document_ids,
        )
        self.calls.append({
            "query": query,
            "namespaces": namespaces,
            "chunks": [
                {
                    "chunk_id": str(c.id),
                    "document_id": str(c.document_id),
                    "section_title": c.section_title,
                    "chunk_order": c.chunk_order,
                    "cosine_sim": round(c.cosine_sim, 4),
                    "final_score": round(c.final_score, 4),
                    "content": c.content,
                }
                for c in chunks
            ],
        })
        return chunks


async def run_one(q: dict, out_dir: Path, sem: asyncio.Semaphore) -> str:
    async with sem:
        settings = get_settings()
        recorder = RecordingRetrieval(get_retrieval_service(settings))
        started = time.time()
        async with AsyncSessionLocal() as db:
            admin = await db.scalar(select(User).where(User.email == ADMIN_EMAIL))
            course = await db.scalar(select(Course).where(Course.code == q["course_code"]))
            if admin is None or course is None:
                raise RuntimeError(f"admin/course missing for {q['qid']}")
            chat_session = ChatSession(user_id=admin.id, course_id=course.id, summary=None)
            db.add(chat_session)
            await db.flush()

            res = await tutor_query_agent_loop(
                session=db,
                session_id=chat_session.id,
                question=q["question"],
                llm_router=build_llm_router(settings),
                retrieval_service=recorder,
                settings=settings,
            )
            await db.commit()
            session_id = str(chat_session.id)

        out = {
            "qid": q["qid"],
            "course_code": q["course_code"],
            "question": q["question"],
            "session_id": session_id,
            "answer": res.answer,
            "citations": [c.model_dump(mode="json") for c in res.citations],
            "retrieval_calls": recorder.calls,
            "elapsed_s": round(time.time() - started, 1),
        }
        (out_dir / f"{q['qid']}.json").write_text(
            json.dumps(out, indent=2, ensure_ascii=False)
        )
        return session_id


async def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--questions", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--concurrency", type=int, default=2)
    parser.add_argument("--only", help="comma-separated qids to run")
    args = parser.parse_args()

    questions = json.loads(Path(args.questions).read_text())
    if args.only:
        wanted = set(args.only.split(","))
        questions = [q for q in questions if q["qid"] in wanted]
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    pending = [q for q in questions if not (out_dir / f"{q['qid']}.json").exists()]
    print(f"{len(pending)} to run ({len(questions) - len(pending)} already done)")

    sem = asyncio.Semaphore(args.concurrency)
    session_ids: dict[str, str] = {}
    failures: list[str] = []

    async def wrapped(q):
        try:
            sid = await run_one(q, out_dir, sem)
            session_ids[q["qid"]] = sid
            print(f"done {q['qid']}")
        except Exception as exc:  # noqa: BLE001 - keep the batch going
            failures.append(q["qid"])
            print(f"FAILED {q['qid']}: {exc}")

    await asyncio.gather(*(wrapped(q) for q in pending))

    ids_path = out_dir / "_created_session_ids.json"
    existing = json.loads(ids_path.read_text()) if ids_path.exists() else {}
    existing.update(session_ids)
    ids_path.write_text(json.dumps(existing, indent=2))
    print(f"created sessions recorded: {len(existing)}; failures: {failures or 'none'}")


if __name__ == "__main__":
    asyncio.run(main())
