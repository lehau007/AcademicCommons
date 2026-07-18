# Ground-truth Review Report — AI Tutor Evaluation

**Reviewed:** 2026-07-07, by Claude (cross-checked all 50 ground-truth answers against the
chunks actually indexed in `academic_kb.document_chunks` for the 3 courses).
**Status: RESOLVED** — at the gate the user chose to index the missing lectures first;
see the post-ingest update below. The original pre-ingest review is kept for the record.

## Post-ingest update (2026-07-07)

24 missing lecture decks from `data/sample/official/` were ingested through the real
pipeline (upload as admin → OCR → auto-APPROVED for official tier → INDEX); all 24 reached
INDEXED with no failures. Chunk counts: IT3020E 64→529, IT3160E 59→478, IT3292E 79→352.

Re-check (keyword-level verification of each previously NOT_COVERED topic against the new
chunks — the `context_recall` judge metric remains the per-question fine-grained check):

| Verdict | Count | Questions |
|---|---|---|
| COVERED | **46/50** | all except below |
| PARTIAL | 3 | discrete_math_08 (Floyd-Warshall Θ(n³) not stated explicitly), discrete_math_16 (spanning-*tree* def indexed, general "spanning subgraph" V(H)=V(G) def not found), discrete_math_19 (isomorphism example + properties indexed; formal one-to-one/onto definition unclear) |
| NOT_COVERED | 1 | discrete_math_07 — the IT3020E spanning-tree deck teaches **Prim only; no Kruskal section exists** in the course slides |

Scoring proceeds on all 50; expect legitimately low `context_recall` on discrete_math_07.

---

## Original pre-ingest review (historical)

## Headline finding

**Only 11 of 50 questions (+1 partial) are answerable from the indexed content.**
The Q&A set was authored from the *full* course material, but each course only has a few
lectures indexed:

| Course | Indexed documents | Covered / total |
|---|---|---|
| IT3160E (intro_to_ai) | lecture1_introduction, lecture2_agent, lecture13-MachineLearning | **5 / 20** |
| IT3020E (discrete_math) | 2_2-GraphPresentation, 2_5-ShortestPath | **3 / 20** (+1 partial) |
| IT3292E (database) | 05_entity_relationship_model, 06_Normalization, 2 midterm exams | **3 / 10** |

For the 38 NOT_COVERED questions the correct tutor behavior is to say the material doesn't
cover it — `context_recall` will legitimately be 1, and `answer_correctness` vs the ground
truth cannot be satisfied from the index. These questions measure **knowledge-base coverage +
honesty**, not answer quality.

**Ground-truth accuracy itself is good:** every COVERED answer matches the indexed chunks
verbatim or near-verbatim; no factual errors found. One nitpick noted at database_05.

## Per-question verdicts

`COVERED` = ground truth fully supported by indexed chunks. `PARTIAL` = supporting material
indexed but the specific fact is not stated. `NOT_COVERED` = topic absent from the index.

### IT3160E — intro_to_ai (5/20 covered)

| qid | Topic | Verdict | Note |
|---|---|---|---|
| 01 | PEAS | **COVERED** | lecture2 "PEAS" + taxi-driver chunks match GT exactly |
| 02 | Progression/regression planners | NOT_COVERED | no planning lecture indexed |
| 03 | A* search | NOT_COVERED | no search lecture indexed |
| 04 | Model-based vs simple reflex | **COVERED** | lecture2 "Simple reflex agent"/"Model-based reflex agents" chunks |
| 05 | CSP definition | NOT_COVERED | no CSP lecture indexed |
| 06 | Min-conflicts heuristic | NOT_COVERED | no CSP lecture indexed |
| 07 | Forward chaining | NOT_COVERED | no propositional-logic lecture indexed |
| 08 | Search problem vs game | NOT_COVERED | no game-search lecture indexed |
| 09 | FOL terms/predicates | NOT_COVERED | no FOL lecture indexed |
| 10 | NN training termination | NOT_COVERED | lecture13 is ML intro only; no NN training loop |
| 11 | Information Gain | NOT_COVERED | ID3/C4.5 only name-dropped in a list; no entropy/IG content |
| 12 | Mitchell T/P/E | **COVERED** | lecture13 "Learning = Improving with experience…" chunk |
| 13 | RL discount rate | NOT_COVERED | RL mentioned only as a learning type |
| 14 | Feed-forward vs recurrent NN | NOT_COVERED | no NN lecture indexed |
| 15 | Acting rationally | **COVERED** | lecture1 "Acting rationally" chunk matches GT |
| 16 | Fully observable env | **COVERED** | lecture2 "Environment types" chunk matches GT |
| 17 | Search problem 4 items | NOT_COVERED | no search lecture indexed |
| 18 | Local beam vs random-restart | NOT_COVERED | no local-search lecture indexed |
| 19 | Alpha-beta pruning | NOT_COVERED | no game-search lecture indexed |
| 20 | Logic = language+semantic+inference | NOT_COVERED | KB chunks exist but no logic-triplet definition |

### IT3020E — discrete_math (3/20 covered, 1 partial)

| qid | Topic | Verdict | Note |
|---|---|---|---|
| 01 | Articulation point / bridge | NOT_COVERED | traversal chapter not indexed |
| 02 | Cayley's theorem | NOT_COVERED | spanning-tree chapter not indexed |
| 03 | Strong/weak connectivity | NOT_COVERED | fundamentals chapter not indexed |
| 04 | BFS complexity | NOT_COVERED | traversal chapter not indexed |
| 05 | Incidence matrix | **COVERED** | GraphPresentation chunks state the exact n×m / m_ij definition |
| 06 | MST safe edge | NOT_COVERED | spanning-tree chapter not indexed |
| 07 | Kruskal | NOT_COVERED | spanning-tree chapter not indexed |
| 08 | Floyd-Warshall running time | **PARTIAL** | algorithm + triple-loop pseudocode indexed; Θ(n³) not stated explicitly |
| 09 | DFS edge types | NOT_COVERED | traversal chapter not indexed |
| 10 | Weight matrix θ | **COVERED** | "θ: special value… 0, +∞, −∞" chunk matches GT exactly |
| 11 | Generalized product rule | NOT_COVERED | combinatorics part not indexed |
| 12 | Pigeonhole principle | NOT_COVERED | combinatorics part not indexed |
| 13 | Big-O intuition | NOT_COVERED | complexity part not indexed |
| 14 | Branch and Bound | NOT_COVERED | combinatorial-optimization part not indexed |
| 15 | 0/1 knapsack representation | NOT_COVERED | combinatorial-optimization part not indexed |
| 16 | Spanning subgraph | NOT_COVERED | fundamentals chapter not indexed |
| 17 | Maximal acyclic graph | NOT_COVERED | tree chapter not indexed |
| 18 | Adjacency list | **COVERED** | "array Adjacency consisting of \|V\| lists" chunk matches GT |
| 19 | Graph isomorphism | NOT_COVERED | fundamentals chapter not indexed |
| 20 | Prim's near[v] | NOT_COVERED | spanning-tree chapter not indexed |

### IT3292E — database (3/10 covered)

| qid | Topic | Verdict | Note |
|---|---|---|---|
| 01 | Candidate key properties | NOT_COVERED | relational-model lesson not indexed; keys only in ER context |
| 02 | Intersection vs Difference | NOT_COVERED | relational-algebra lesson not indexed |
| 03 | SQL standard history | NOT_COVERED | SQL lessons not indexed |
| 04 | HAVING vs WHERE | NOT_COVERED | SQL lessons not indexed |
| 05 | n-m relationship mapping | **COVERED** | ER chunk "Mapping of n-m relationships". Nitpick: GT adds "used as foreign keys", slide doesn't say FK explicitly — factually fine |
| 06 | Multivalued attribute mapping | **COVERED** | ER chunk matches GT near-verbatim |
| 07 | Update anomaly | **COVERED** | Normalization "Update anomalies" chunk matches GT (same Databases example) |
| 08 | F+ closure | NOT_COVERED | FD lesson not indexed; exam mentions Armstrong axioms only |
| 09 | Query optimizer goal | NOT_COVERED | query-processing lesson not indexed |
| 10 | Join algorithms | NOT_COVERED | query-processing lesson not indexed |

## Options at the gate

1. **Score all 50, segment the report by COVERED / NOT_COVERED** *(recommended)* — measures
   the real system end-to-end: answer quality where the KB has content, honesty/refusal +
   retrieval behavior where it doesn't. `answer_correctness` and `context_recall` for the
   NOT_COVERED segment are reported separately so they don't unfairly drag the headline score.
2. **Score only the 11 covered (+1 partial) questions** — clean answer-quality numbers, but a
   small sample and throws away 38 authored questions.
3. **Index the missing lectures first, then run** — best coverage, but requires sourcing +
   processing many more documents through the OCR pipeline before any evaluation can start.
