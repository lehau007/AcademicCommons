"""Generate ablation actuals: same as run_tutor.py but with an ablated retrieval source.

    docker cp evaluation/ai_tutor_evaluation graduationthesis-api-1:/tmp/tutor_eval
    docker exec graduationthesis-api-1 python /tmp/tutor_eval/scripts/run_ablation.py \
        --mode bm25_rerank \
        --questions /tmp/tutor_eval/dataset/questions.json \
        --out /tmp/tutor_eval/actual_bm25_rerank

Modes: dense_rerank | bm25_rerank | hybrid_norerank (see ablation_retrieval.py).
Resumable: existing <qid>.json files are skipped.
"""
from __future__ import annotations

import argparse
import asyncio
import json
import sys
import time
from pathlib import Path

from sqlalchemy import select

from app.config import get_settings
from app.db.session import AsyncSessionLocal
from app.llm.router import build_llm_router
from app.models import ChatSession, Course, User
from app.services.tutor_service import tutor_query, tutor_query_agent_loop

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ablation_retrieval import AblationRetrieval  # noqa: E402

ADMIN_EMAIL = "admin@soict.hust.edu.vn"

_MODE_SHORT = {
    "dense_rerank": "dense",
    "hybrid_rerank": "hybrid",
    "hybrid_norerank": "hybridnr",
    "bm25_rerank": "bm25",
}


def default_out_dir(pipeline: str, mode: str) -> str:
    return f"hard/actual_{pipeline}_{_MODE_SHORT[mode]}"


async def run_one(q: dict, mode: str, pipeline: str, out_dir: Path, sem: asyncio.Semaphore) -> str:
    async with sem:
        settings = get_settings()
        recorder = AblationRetrieval(settings, mode)
        started = time.time()
        async with AsyncSessionLocal() as db:
            admin = await db.scalar(select(User).where(User.email == ADMIN_EMAIL))
            course = await db.scalar(select(Course).where(Course.code == q["course_code"]))
            if admin is None or course is None:
                raise RuntimeError(f"admin/course missing for {q['qid']}")
            chat_session = ChatSession(user_id=admin.id, course_id=course.id, summary=None)
            db.add(chat_session)
            await db.flush()

            if pipeline == "agentic":
                res = await tutor_query_agent_loop(
                    session=db,
                    session_id=chat_session.id,
                    question=q["question"],
                    llm_router=build_llm_router(settings),
                    retrieval_service=recorder,
                    settings=settings,
                )
            else:  # traditional single-shot
                res = await tutor_query(
                    session=db,
                    course_code=q["course_code"],
                    question=q["question"],
                    include_exercise=False,
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
            "ablation_mode": mode,
            "pipeline": pipeline,
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
    parser.add_argument("--mode", required=True, choices=sorted(AblationRetrieval.MODES))
    parser.add_argument("--pipeline", required=True, choices=["agentic", "traditional"])
    parser.add_argument("--questions", required=True)
    parser.add_argument("--out", default=None)
    parser.add_argument("--concurrency", type=int, default=2)
    parser.add_argument("--only", help="comma-separated qids to run")
    args = parser.parse_args()

    questions = json.loads(Path(args.questions).read_text())
    if args.only:
        wanted = set(args.only.split(","))
        questions = [q for q in questions if q["qid"] in wanted]
    out_dir = Path(args.out or default_out_dir(args.pipeline, args.mode))
    out_dir.mkdir(parents=True, exist_ok=True)

    pending = [q for q in questions if not (out_dir / f"{q['qid']}.json").exists()]
    print(f"[{args.mode}] {len(pending)} to run ({len(questions) - len(pending)} already done)")

    sem = asyncio.Semaphore(args.concurrency)
    session_ids: dict[str, str] = {}
    failures: list[str] = []

    async def wrapped(q):
        try:
            sid = await run_one(q, args.mode, args.pipeline, out_dir, sem)
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
