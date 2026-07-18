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
- **Figure 11.13** The GRAPHPLAN algorithm. GRAPHPLAN alternates between a solution extraction step and a graph expansion step. EXTRACT-SOLUTION looks for whether a plan can be found, starting at the end and searching backwards. EXPAND-GRAPH adds the actions for the current level and the state literals for the next level.
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
- [Diagram: The figure illustrates a planning graph that expands alternating layers of states and actions while preserving “no-op” actions for persistence. Mutex links encode which choices cannot coexist, allowing the graph to capture constraints and eventually level off when no new information is added.]
- ```text
+--------------------------------------------------------------+
| function Graph-Search(problem, fringe) returns a solution,   |
| or failure                                                   |
| fringe ← Insert(Make-Node(Initial-State(problem)), fringe);  |
| closed ← an empty set                                        |
| while (fringe not empty)                                     |
|   node ← RemoveFirst(fringe);                                |
|   if (Goal-Test(problem, State(node))) then return Solution(node); |
|   if (State(node) is not in closed) then                     |
|     add State(node) to closed                                |
|     fringe ← InsertAll(Expand(node, problem), fringe);       |
|   end if                                                     |
| end                                                         |
| return failure;                                              |
+--------------------------------------------------------------+
```

- Never expand a node twice!
- ```text
+-------+      +----------------------+
| start | ---> | set threshold as h(s) |
+-------+      +----------------------+
                      |
                      v
             +--------------------------+
             | put s in OPEN, compute f(s) |
             +--------------------------+
                      |
                      v
                 /----------------\
                |   OPEN empty ?   |
                 \----------------/
                   |            |
                 yes|            | no
                   v            v
      +-------------------------------+
      | threshold = min( f(.) )       |
      +-------------------------------+
                      |
                      └───────────────> back to "put s in OPEN, compute f(s)"

             +-----------------------------------------------------------+
             | Remove the node of OPEN whose f(.) value is smallest       |
             | and put it in CLOSE (call it n)                           |
             +-----------------------------------------------------------+
                      |
                      v
                 /---------------\
                |   n = goal ?    |
                 \---------------/
                   |          |
                 yes|          | no
                   v          v
              +----------+   +------------------------------------------------------+
              | Success  |   | Expand n. calculate f(.) of successor                 |
              +----------+   | if f(suc) < threshold then                           |
                             |   Put successors to OPEN if                           |
                             |   pointers back to n                                 |
                             +------------------------------------------------------+
                                      |
                                      └───────────────> back to "Remove the node of OPEN..."
```

## Tutor answer
# Trích xuất lời giải từ trạng thái S2 trong Planning Graph (bài toán thay lốp dự phòng)

## Tính chất của trạng thái S2 cho phép trích xuất lời giải

Trong sơ đồ planning graph của bài toán spare tire, khi mở rộng đến **mức S2**, hai điều kiện quan trọng được thỏa mãn đồng thời:

1. **Tất cả các literal của goal xuất hiện tại S2**: Cụ thể, goal `at(spare, axle)` đã có mặt ở mức trạng thái S2. Điều này có nghĩa là về mặt lý thuyết, một kế hoạch có độ dài phù hợp có khả năng tồn tại.

2. **Không có mutex giữa các literal của goal**: Các điều kiện đích không mâu thuẫn với nhau tại S2, nghĩa là chúng có thể được thỏa mãn đồng thời bởi một tập các hành động ở mức A1 (và kéo theo đó là các hành động ở mức A0).

Chính sự kết hợp giữa **"goals đều xuất hiện"** và **"goals không mutex với nhau"** mà thuật toán Graphplan kiểm tra trong vòng lặp chính:

```
if goals all non-mutex in last level of graph then do
    solution ← EXTRACT-SOLUTION(graph, goals, LENGTH(graph))
```

Đây chính là điều kiện cần để chuyển sang bước trích xuất lời giải.

## Các phương pháp trích xuất lời giải

Khi S2 thỏa mãn điều kiện trên, có **hai cách chính** để trích xuất lời giải:

### 1. Giải bài toán thỏa ràng buộc (CSP) với actions là biến

- Coi mỗi hành động ở một mức action layer là một **biến**.
- Tập giá trị của mỗi biến là các hành động (bao gồm cả no-op) có thể đạt được literal tương ứng.
- Các **ràng buộc** giữa các biến chính là:
  - **Preconditions**: tiền đề của mỗi hành động phải được thỏa mãn.
  - **Mutex**: hai hành động cùng mức không được mâu thuẫn.
  - **Persistence**: mỗi literal cần được "giữ" xuyên suốt bởi no-op (trừ khi bị thay đổi).
- Dùng thuật toán CSP (ví dụ backtracking với forward checking/arc consistency) để tìm tập hành động nhất quán tại mỗi mức, làm việc **từ S2 ngược về S0**.

### 2. Tìm kiếm lùi (search backwards) — hàm EXTRACT-SOLUTION

- Bắt đầu từ **goal ở mức S2**, chọn một tập hành động ở mức A1 có thể đạt được goal và không bị mutex lẫn nhau.
- Lấy **preconditions** của các hành động vừa chọn làm subgoal mới ở mức S1.
- Lặp lại quá trình ở mức A0 với subgoal ở S1, ... cho đến khi về tới S0.
- Nếu tại một mức nào đó **không tìm được tập hành động khả thi** (ví dụ do mutex), thì quay lui và thử lựa chọn khác ở mức trên.
- Trong pseudocode của Graphplan, đây chính là hàm `EXTRACT-SOLUTION(graph, goals, length)`.

## Tổng kết

- **Tính chất của S2**: chứa toàn bộ goal và các literal này không mutex với nhau.
- **Hai cách trích xuất**:
  1. **CSP** — coi mỗi action layer như một bài toán ràng buộc với các action là biến.
  2. **Backward search** — chọn action đạt goal, lùi dần qua các preconditions cho tới S0.

Nếu cả hai phương pháp đều thất bại, Graphplan sẽ tiếp tục **mở rộng đồ thị** thêm một mức nữa và thử lại — đây chính là vòng lặp "alternates between a solution extraction step and a graph expansion step" trong thuật toán Graphplan.

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
    "chunk_id": "2ef50526-63b8-46a3-81a7-389fa3cf99e6",
    "document_title": "lecture12-Planning.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "SATplan algorithm",
    "page_number": null,
    "chunk_order": 62,
    "excerpt": "```text\nfunction SATPLAN(problem, T_max) returns solution or failure\n  inputs: problem, a planning problem\n          T_max, an upper limit for plan length\n\n  for T = 0 to T_max do\n    cnf_mapping ← TR"
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
  }
]
```
