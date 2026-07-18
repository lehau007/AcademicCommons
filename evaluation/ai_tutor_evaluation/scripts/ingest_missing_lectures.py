"""Ingest the lecture slides missing from the index, via the real product pipeline.

Runs INSIDE the `api` container. Official uploads skip HITL: OCR -> APPROVED -> INDEX
(see ocr_worker.py), so this just uploads as admin and polls until INDEXED/FAILED.

    docker exec graduationthesis-api-1 python /tmp/tutor_eval/scripts/ingest_missing_lectures.py \
        --manifest /tmp/tutor_eval_ingest/manifest.json --out /tmp/tutor_eval_ingest/created.json

manifest.json: [{"course_code": "IT3160E", "path": "/tmp/tutor_eval_ingest/files/..."}]
Resumable: documents already uploaded (same original_filename + course, any status) are skipped.
"""
from __future__ import annotations

import argparse
import asyncio
import json
from pathlib import Path

from sqlalchemy import select

from app.db.session import AsyncSessionLocal
from app.models import Course, Document, User
from app.models.enums import MaterialType
from app.services.document_service import upload_official_document
from app.storage import get_storage

ADMIN_EMAIL = "admin@soict.hust.edu.vn"
POLL_S = 20
TIMEOUT_S = 45 * 60


async def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    entries = json.loads(Path(args.manifest).read_text())
    storage = get_storage()
    created: dict[str, str] = {}

    async with AsyncSessionLocal() as session:
        admin = await session.scalar(select(User).where(User.email == ADMIN_EMAIL))
        for e in entries:
            filename = Path(e["path"]).name
            course = await session.scalar(select(Course).where(Course.code == e["course_code"]))
            existing = await session.scalar(
                select(Document).where(
                    Document.course_id == course.id,
                    Document.original_filename == filename,
                )
            )
            if existing is not None:
                print(f"skip (exists, {existing.status}): {filename}")
                created[filename] = str(existing.id)
                continue
            doc = await upload_official_document(
                session=session,
                storage=storage,
                course_code=e["course_code"],
                material_type=MaterialType.LECTURE_SLIDES,
                file_content=Path(e["path"]).read_bytes(),
                filename=filename,
                uploader=admin,
                display_name=Path(filename).stem,
            )
            created[filename] = str(doc.id)
            print(f"uploaded {e['course_code']} {filename} -> {doc.id}")

    Path(args.out).write_text(json.dumps(created, indent=2))

    # Poll until every document reaches a terminal state.
    waited = 0
    while waited < TIMEOUT_S:
        async with AsyncSessionLocal() as session:
            rows = (await session.execute(
                select(Document.original_filename, Document.status)
                .where(Document.id.in_(list(created.values())))
            )).all()
        by_status: dict[str, list[str]] = {}
        for name, status_ in rows:
            by_status.setdefault(str(status_.value if hasattr(status_, "value") else status_), []).append(name)
        pending = {s: n for s, n in by_status.items() if s not in {"INDEXED", "FAILED", "REJECTED"}}
        print(f"[{waited}s] " + ", ".join(f"{s}:{len(n)}" for s, n in sorted(by_status.items())))
        if not pending:
            break
        await asyncio.sleep(POLL_S)
        waited += POLL_S

    failed = by_status.get("FAILED", []) + by_status.get("REJECTED", [])
    print(f"finished; indexed={len(by_status.get('INDEXED', []))} failed={failed or 'none'}")


if __name__ == "__main__":
    asyncio.run(main())
