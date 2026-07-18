# Hard-set table enrichment log

Applied by `scripts/enrich_table_chunks.py --apply` (inside the api container), which appends a
light `[Table: …]` description to the target chunk's `content` and re-embeds ONLY that chunk
(NVIDIA `nv-embedqa-e5-v5`, `input_type="passage"`, dim 1024). No re-OCR, no full reindex.
Figures/diagrams are NOT enriched — the pipeline already emits `[Diagram: …]` for them.

Idempotent: a chunk already containing `[Table:` is skipped, so re-running is safe.

Status: **APPLIED 2026-07-12** — all 4 chunks committed + re-embedded; verified in DB
(`content LIKE '%[Table:%'` = true, `embedding IS NOT NULL` = true for each). Re-runnable
safely (idempotent skip on the `[Table:` marker).

| chunk_id | course | table | appended description (summary) |
|---|---|---|---|
| a9b6e256-e2ef-4425-bbe2-4742c27af351 | IT3292E | student | columns student_id, first_name, last_name, dob, gender, clazz_id (FK to class) |
| b48aa1a6-c13e-4824-ac5b-47daaaabe515 | IT3292E | student (with gender) | same columns, notes gender M/F |
| c966cb75-ac1a-4497-9754-f83f923e20fe | IT3292E | student | student_id, first_name, last_name, clazz_id |
| 786cf68a-c479-46bf-9556-87695dc6e3d1 | IT3292E | DBMS definitions + examples | Wikipedia/Techtarget definitions; example products MySQL, MS Access, MS SQL Server, ORACLE, IBM DB2, PostgreSQL |

After an `--apply` run, paste the tool's `APPLY …` lines here as the authoritative record.
