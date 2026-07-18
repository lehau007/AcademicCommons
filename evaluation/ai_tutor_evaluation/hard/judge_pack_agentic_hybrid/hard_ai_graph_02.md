# hard_ai_graph_02

## Question
Trong sơ đồ planning graph cho bài toán thay lốp dự phòng (spare tire), trạng thái mức S2 có tính chất gì khiến ta có thể trích xuất lời giải, và có thể trích xuất bằng những cách nào?

## Ground truth
Ở mức S2 planning graph đã chứa tất cả các goal (ví dụ at(spare,axle)) và không có mutex giữa chúng, nên có thể thử trích xuất lời giải. Có thể trích xuất bằng thuật toán CSP với các action làm biến, hoặc bằng tìm kiếm lùi (search backwards) từ goal.

## Retrieved context (what the tutor saw)
- Figure 11.14 The planning graph for the spare tire problem after expansion to level $S_2$. Mutex links are shown as gray lines. Only some representative mutexes are shown, because the graph would be too cluttered if we showed them all. The solution is indicated by bold lines and outlines.
- goal: at(spare,axle)

- S2 has all goals and no mutex so we can try to extract solutions
- Use either CSP algorithm with actions as variables
- Or search backwards

```text
S0                     A0                     S1                     A1                     S2
|                      |                      |                      |                      |
at(spare,trunk)   ---> [RemoveSpare,Trunk] --> ¬at(spare,trunk)  ---> [RemoveSpare,Trunk] --> ¬at(spare,trunk)
at(flat,axle)     ---> [RemoveFlat,Axle]     --> ¬at(flat,axle)    ---> [RemoveFlat,Axle]     --> ¬at(flat,axle)
¬at(spare,axle)                                 [LeaveOvernight]    ---> ¬at(spare,axle)      ---> ¬at(spare,axle)
¬at(flat,ground)                                                                              [PutOn,Spare,Axle]
¬at(spare,ground)

[Diagram: This is a planning graph showing how actions are layered between successive state levels to achieve the goal of having the spare tire on the axle. It matters because it illustrates how goal satisfaction and mutex relationships can be used to extract a valid plan or reason backward from the goal state.]
```
- - Estimate the cost of achieving a goal by the level in the planning graph where it appears.
- To estimate the cost of a conjunction of goals use one of the following:
  - Max-level: take the maximum level of any goal (admissible)
  - Sum-cost: Take the sum of levels (inadmissible)
  - Set-level: find the level where they all appear without Mutex
- Graph plans are relaxation of the problem.
- Representing more than pair-wise mutex is not cost-effective
- ```text
+--------------------------------------------------------------+
| function GRAPHPLAN(problem) returns solution or failure      |
|                                                              |
|   graph ← INITIAL-PLANNING-GRAPH(problem)                    |
|   goals ← GOALS[problem]                                    |
|   loop do                                                    |
|     if goals all non-mutex in last level of graph then do    |
|       solution ← EXTRACT-SOLUTION(graph, goals, LENGTH(graph))|
|       if solution ≠ failure then return solution             |
|       else if NO-SOLUTION-POSSIBLE(graph) then return failure|
|     graph ← EXPAND-GRAPH(graph, problem)                     |
+--------------------------------------------------------------+
```

[Diagram: This pseudocode describes the GRAPHPLAN planning procedure, which alternates between building a layered planning graph and trying to extract a valid plan from it. The key idea is that the graph grows until either a solution is found by backward search or the algorithm proves no plan is possible.]
- [Diagram: The figure illustrates a planning graph that expands alternating layers of states and actions while preserving “no-op” actions for persistence. Mutex links encode which choices cannot coexist, allowing the graph to capture constraints and eventually level off when no new information is added.]
- **Figure 11.13** The GRAPHPLAN algorithm. GRAPHPLAN alternates between a solution extraction step and a graph expansion step. EXTRACT-SOLUTION looks for whether a plan can be found, starting at the end and searching backwards. EXPAND-GRAPH adds the actions for the current level and the state literals for the next level.
- - Literals increase monotonically
  - Once a literal is in a level it will persist to the next level
- Actions increase monotonically
  - Since the precondition of an action was satisfied at a level and literals persist the action’s precond will be satisfied from now on
- Mutexes decrease monotonically:
  - If two actions are mutex at level Si, they will be mutex at all previous levels at which they both appear
- Because literals increase and mutex decrease it is guaranteed that we will have a level where all goals are non-mutex
- ```text
function SATPLAN(problem, T_max) returns solution or failure
  inputs: problem, a planning problem
          T_max, an upper limit for plan length

  for T = 0 to T_max do
    cnf_mapping ← TRANSLATE-TO-SAT(problem, T)
    assignment ← SAT-SOLVER(cnf)
    if assignment is not null then
      return EXTRACT-SOLUTION(assignment, mapping)
  return failure
```

[Diagram: The algorithm incrementally searches for a valid plan by encoding the planning problem as a SAT instance for each time step. If a satisfiable model is found, the plan is extracted from the true action variables; otherwise, the time horizon is extended until the limit is reached.]

## Tutor answer
# Trích xuất lời giải từ mức S2 trong planning graph (bài toán thay lốp dự phòng)

## 1. Tính chất của mức S2 cho phép trích xuất lời giải

Trong sơ đồ planning graph của bài toán **spare tire**, mức trạng thái **S2** có hai tính chất quan trọng giúp ta có thể tiến hành trích xuất lời giải:

- **Chứa đầy đủ các goal literals**: Ở S2 xuất hiện toàn bộ các mệnh đề mục tiêu của bài toán. Cụ thể, goal `at(spare, axle)` đã xuất hiện tại mức này (thông qua hành động `PutOn(Spare, Axle)` ở mức A1).
  
- **Các goal không mutex với nhau**: Tại S2, không tồn tại cặp mutex nào giữa các goal literals, nghĩa là chúng có thể đạt được **đồng thời** mà không xung đột.

Chính hai điều kiện "**tất cả goal xuất hiện**" và "**không có goal nào mutex với goal khác**" là tiêu chí mà thuật toán **GRAPHPLAN** kiểm tra trước khi gọi bước `EXTRACT-SOLUTION` (xem vòng lặp chính của thuật toán GRAPHPLAN trong tài liệu).

> 📌 **Lưu ý về tính chất hội tụ**: Tính chất này được đảm bảo tồn tại nhờ các thuộc tính của planning graph — literals tăng đơn điệu, còn mutex giảm đơn điệu. Vì vậy chắc chắn sẽ tồn tại một mức mà ở đó mọi goal đều xuất hiện và không mutex với nhau (mức "level off" cho goal). Với bài toán spare tire, mức đó chính là S2.

## 2. Các cách trích xuất lời giải

Khi S2 thỏa mãn điều kiện trên, ta có thể dùng **một trong hai cách** sau:

### Cách 1: Giải bài toán **CSP** (Constraint Satisfaction Problem) với actions là biến

- Mỗi **action** ở một mức A_i được xem như một biến.
- **Miền giá trị** của biến: tập các action thỏa mãn preconditions tương ứng.
- **Ràng buộc (constraints)**: hai action được chọn ở cùng mức không được mutex với nhau; ngoài ra, với mỗi literal cần đạt được, phải có một action ở mức trước tạo ra nó (hoặc là no-op từ mức trước).
- Giải bài toán CSP này bằng các thuật toán CSP chuẩn (backtracking, AC-3, …) để tìm tổ hợp action hợp lệ ở mỗi mức, trích xuất ngược từ S2 về S0.

### Cách 2: **Tìm kiếm ngược** (backward search) từ mức S2 về S0

- Bắt đầu từ tập goal ở S2.
- Ở mỗi bước, chọn một tập con các action ở mức A_{i-1} có thể đạt được các goal ở S_i mà **không bị mutex** với nhau.
- Tiếp tục lùi về các mức trước, dùng preconditions của các action đã chọn làm "sub-goal" mới, cho đến khi về tới S0.
- Nếu tồn tại một chuỗi lựa chọn như vậy xuyên suốt từ S2 về S0 thì ta thu được một plan hợp lệ.

## 3. Kết quả áp dụng cho spare tire

Với mức S2, hai cách trên đều cho ra cùng một plan (chỉ ra bằng đường viền đậm trong hình 11.14), ví dụ:

| Mức | Hành động |
|------|------------|
| A0   | `RemoveSpare(Trunk)`, `RemoveFlat(Axle)` |
| A1   | `PutOn(Spare, Axle)` |

## Tóm tắt

> Ở S2, vì **mọi goal đều xuất hiện** và **không có cặp goal nào mutex**, nên ta có thể đảm bảo tồn tại một plan. Lời giải có thể được trích xuất bằng **(1) mô hình hóa thành bài toán CSP với action là biến**, hoặc **(2) tìm kiếm ngược từ goal ở S2 về S0**.

## Citations
```json
[
  {
    "chunk_id": "9e35dead-7fd9-4935-a575-6dba4efd2a76",
    "document_title": "lecture12-Planning.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "Planning graph for spare tire a S2",
    "page_number": null,
    "chunk_order": 57,
    "excerpt": "Figure 11.14 The planning graph for the spare tire problem after expansion to level $S_2$. Mutex links are shown as gray lines. Only some representative mutexes are shown, because the graph would be t"
  },
  {
    "chunk_id": "3ee13f47-a21d-4661-bcc7-def43f301313",
    "document_title": "lecture12-Planning.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "Planning graph for spare tire a S2",
    "page_number": null,
    "chunk_order": 56,
    "excerpt": "goal: at(spare,axle)\n\n- S2 has all goals and no mutex so we can try to extract solutions\n- Use either CSP algorithm with actions as variables\n- Or search backwards\n\n```text\nS0                     A0  "
  },
  {
    "chunk_id": "8d6df43e-a917-44fb-8e23-3c8af51b7ebb",
    "document_title": "lecture12-Planning.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "Planning graphs for heuristic estimation",
    "page_number": null,
    "chunk_order": 53,
    "excerpt": "- Estimate the cost of achieving a goal by the level in the planning graph where it appears.\n- To estimate the cost of a conjunction of goals use one of the following:\n  - Max-level: take the maximum "
  },
  {
    "chunk_id": "c2267876-167a-4c0b-8ffc-58ff737795c2",
    "document_title": "lecture12-Planning.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "The graphplan algorithm",
    "page_number": null,
    "chunk_order": 54,
    "excerpt": "```text\n+--------------------------------------------------------------+\n| function GRAPHPLAN(problem) returns solution or failure      |\n|                                                             "
  },
  {
    "chunk_id": "dbd562ea-0e6b-4c31-8ccc-ec3451358da0",
    "document_title": "lecture12-Planning.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "The Planning graphs for “have cake”,",
    "page_number": null,
    "chunk_order": 51,
    "excerpt": "[Diagram: The figure illustrates a planning graph that expands alternating layers of states and actions while preserving “no-op” actions for persistence. Mutex links encode which choices cannot coexis"
  },
  {
    "chunk_id": "2052fe08-76bc-4555-8dbe-a9692ac4577a",
    "document_title": "lecture12-Planning.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "The graphplan algorithm",
    "page_number": null,
    "chunk_order": 55,
    "excerpt": "**Figure 11.13** The GRAPHPLAN algorithm. GRAPHPLAN alternates between a solution extraction step and a graph expansion step. EXTRACT-SOLUTION looks for whether a plan can be found, starting at the en"
  },
  {
    "chunk_id": "33f01b67-5596-4ce7-9e63-70e8265730c6",
    "document_title": "lecture12-Planning.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "Properties of planning graphs; termination",
    "page_number": null,
    "chunk_order": 59,
    "excerpt": "- Literals increase monotonically\n  - Once a literal is in a level it will persist to the next level\n- Actions increase monotonically\n  - Since the precondition of an action was satisfied at a level a"
  },
  {
    "chunk_id": "2ef50526-63b8-46a3-81a7-389fa3cf99e6",
    "document_title": "lecture12-Planning.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "SATplan algorithm",
    "page_number": null,
    "chunk_order": 62,
    "excerpt": "```text\nfunction SATPLAN(problem, T_max) returns solution or failure\n  inputs: problem, a planning problem\n          T_max, an upper limit for plan length\n\n  for T = 0 to T_max do\n    cnf_mapping ← TR"
  }
]
```
