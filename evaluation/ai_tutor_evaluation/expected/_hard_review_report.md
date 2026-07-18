# Hard dataset — coverage review

Every ground truth below was authored against actual indexed chunks (DB `academic_kb`,
`document_chunks`) inspected on 2026-07-12. Chunk ids are the covering chunks. Verdicts:
**covered** = ground truth fully present in the listed chunk(s); **partial** = core is
present, one sub-point is inferential; **enrich** = a table chunk that needs a light
`[Table: …]` description added before the question reliably retrieves it (see
`_hard_enrichment_log.md`).

Finding that shaped the dataset: the OCR/normalization pipeline already emits `[Diagram: …]`
descriptions for figures/diagrams (IT3020E 159, IT3160E 145 chunks), so **graph** questions
are retrievable as-is. **Tables**, however, mostly lack any NL description (100+ table chunks
per course with no `[Table: …]`), so table-targeted chunks are the enrichment set.

| qid | type | course | covering chunk(s) | verdict |
|---|---|---|---|---|
| hard_ai_graph_01 | graph | IT3160E | c247d5c4 (Drawbacks of hill climbing, `[Diagram]`) | covered |
| hard_ai_graph_02 | graph | IT3160E | 3ee13f47 / 9e35dead (Planning graph for spare tire a S2) | covered |
| hard_ai_multi_03 | multi_intent | IT3160E | Rational agents (agent function P*→A; agent perceives/acts) | covered |
| hard_ai_multi_04 | multi_intent | IT3160E | a07782cc (A* search, evaluation: Completeness YES, time exp) + e00eb634 (Depth-limited search) | covered |
| hard_db_table_05 | table | IT3292E | a9b6e256 / b48aa1a6 / c966cb75 (student) | covered — **enrich a9b6e256, b48aa1a6, c966cb75** |
| hard_db_table_06 | table | IT3292E | 786cf68a (DBMS Definitions table + examples) | covered — **enrich 786cf68a** |
| hard_db_multi_07 | multi_intent | IT3292E | 2.4 DBMS (defining/constructing/manipulating) + a9b6e256 (student) | covered |
| hard_db_table_08 | table | IT3292E | 2.4 DBMS ("Defining ~ specifying types of data …") | covered |
| hard_dm_graph_09 | graph | IT3020E | 2e91d694 (3-subset example, `[Diagram]`) | covered |
| hard_dm_long_10 | long_context | IT3020E | 4e6282ea + 01f46a29 + 2e91d694 (tuple rep → order def → example; 3 chunks) | covered |
| hard_dm_graph_11 | graph | IT3020E | 65f383ea (DFS(s) pseudocode) | covered |
| hard_dm_multi_12 | multi_intent | IT3020E | 65f383ea (DFS(s): pred[v], visited[v]) | covered |
| hard_dm_table_13 | table | IT3020E | 2e91d694 (3-subset listing) | covered |
| hard_ai_long_14 | long_context | IT3160E | c247d5c4 (Drawbacks of hill climbing) | **partial** — global/shoulder/local/flat all named in the `[Diagram]`; the shoulder-vs-flat "can continue past a shoulder" nuance (sub-point c) is standard AITMA framing, only implied by the chunk. Judge should not over-penalise if the tutor omits (c). |
| hard_db_long_15 | long_context | IT3292E | 786cf68a (definitions + examples) + 2.4 DBMS (functions) | covered |

Distribution: 15 questions — graph 4, table 4, multi_intent 4, long_context 3; courses
IT3160E ×6, IT3020E ×5, IT3292E ×4. All within a single course each (the runner scopes
retrieval to `q.course_code`).
