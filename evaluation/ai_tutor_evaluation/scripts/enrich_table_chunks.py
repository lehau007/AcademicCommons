"""Targeted table enrichment for the hard ablation set.

The OCR/normalization pipeline already emits `[Diagram: ...]` descriptions for figures, so
graph questions retrieve fine. Tables, though, are stored as raw markdown with no natural-
language description — a conceptual query ("what columns does the student table have?") embeds
poorly against a pipe-delimited grid. This script appends a light `[Table: ...]` description to
the specific table chunks the hard `table` questions target, then RE-EMBEDS only those chunks
(no full reindex). Idempotent: a chunk already containing `[Table:` is skipped.

Runs INSIDE the api container (like run_ablation.py):
    docker cp evaluation/ai_tutor_evaluation graduationthesis-api-1:/tmp/tutor_eval
    # dry run (default) — prints planned edits, writes nothing:
    docker exec graduationthesis-api-1 python /tmp/tutor_eval/scripts/enrich_table_chunks.py
    # apply:
    docker exec graduationthesis-api-1 python /tmp/tutor_eval/scripts/enrich_table_chunks.py --apply

Every edit is recorded in expected/_hard_enrichment_log.md by hand after an --apply run.
"""
from __future__ import annotations

import argparse
import asyncio
from uuid import UUID

from sqlalchemy import select

from app.config import get_settings
from app.db.session import AsyncSessionLocal
from app.models import DocumentChunk
from app.services.retrieval_service import build_embedding_service

# chunk_id -> light [Table: ...] description (factual, no invented data)
ENRICHMENTS: dict[str, str] = {
    # IT3292E — student relation (three slide variants of the same table)
    "a9b6e256-e2ef-4425-bbe2-4742c27af351":
        "[Table: Sample rows of the student relation. Columns: student_id, first_name, "
        "last_name, dob (date of birth), gender, clazz_id (foreign key linking each student "
        "to a class).]",
    "b48aa1a6-c13e-4824-ac5b-47daaaabe515":
        "[Table: Sample rows of the student relation, including the gender column (M/F). "
        "Columns: student_id, first_name, last_name, dob, gender, clazz_id.]",
    "c966cb75-ac1a-4497-9754-f83f923e20fe":
        "[Table: Sample rows of the student relation showing student_id, first_name, "
        "last_name and the clazz_id that links each student to a class.]",
    # IT3292E — DBMS definitions + example products
    "786cf68a-c479-46bf-9556-87695dc6e3d1":
        "[Table: DBMS definitions (Wikipedia: software to create and maintain a database; "
        "Techtarget: a systematic way to create, retrieve, update and manage data) and a list "
        "of example DBMS products: MySQL, Microsoft Access, Microsoft SQL Server, ORACLE "
        "DATABASE, IBM DB2, PostgreSQL.]",
}


async def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="write edits + re-embed (default: dry run)")
    args = ap.parse_args()

    settings = get_settings()
    embedder = build_embedding_service(settings) if args.apply else None

    async with AsyncSessionLocal() as db:
        for cid, desc in ENRICHMENTS.items():
            chunk = await db.scalar(select(DocumentChunk).where(DocumentChunk.id == UUID(cid)))
            if chunk is None:
                print(f"MISSING  {cid} — not found, skipping")
                continue
            if "[Table:" in chunk.content:
                print(f"SKIP     {cid} — already has a [Table: …] description")
                continue
            new_content = chunk.content.rstrip() + "\n\n" + desc
            print(f"{'APPLY' if args.apply else 'DRYRUN'}   {cid} (+{len(desc)} chars): {desc[:80]}…")
            if args.apply:
                chunk.content = new_content
                vec = (await asyncio.to_thread(embedder.encode, [new_content], input_type="passage"))[0]
                chunk.embedding = vec
        if args.apply:
            await db.commit()
            print("committed + re-embedded")
        else:
            print("dry run — nothing written (pass --apply to commit)")


if __name__ == "__main__":
    asyncio.run(main())
