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
- ```text
Partial-Order Plan

+--------+                     +-----------+
| Start  |                     |           |
+--------+                     |           |
   /   \                       |           |
  v     v                      |           |
+----------+   +-----------+   |           |
| Left     |   | Right     |   |           |
| Sock     |   | Sock      |   |           |
+----------+   +-----------+   |           |
    |             |            |           |
    v             v            |           |
LeftSockOn     RightSockOn     |           |
    |             |            |           |
+----------+   +-----------+   |           |
| Left     |   | Right     |   |           |
| Shoe     |   | Shoe      |   |           |
+----------+   +-----------+   |           |
    \             /            |           |
     v           v             |           |
   LeftShoeOn, RightShoeOn     |           |
               |               |           |
               v               |           |
+--------+                     +-----------+
| Finish |                     +-----------+

Total-Order Plans

+--------+   +----------+   +----------+   +----------+   +----------+   +--------+
| Start  |-->| Right    |-->| Left     |-->| Right    |-->| Left     |-->| Finish |
|        |   | Sock     |   | Sock     |   | Shoe     |   | Shoe     |   |        |
+--------+   +----------+   +----------+   +----------+   +----------+   +--------+

+--------+   +----------+   +----------+   +----------+   +----------+   +--------+
| Start  |-->| Right    |-->| Left     |-->| Right    |-->| Left     |-->| Finish |
|        |   | Sock     |   | Sock     |   | Shoe     |   | Shoe     |   |        |
+--------+   +----------+   +----------+   +----------+   +----------+   +--------+

+--------+   +----------+   +----------+   +----------+   +----------+   +--------+
| Start  |-->| Left     |-->| Right    |-->| Left     |-->| Right    |-->| Finish |
|        |   | Sock     |   | Sock     |   | Shoe     |   | Shoe     |   |        |
+--------+   +----------+   +----------+   +----------+   +----------+   +--------+

+--------+   +----------+   +----------+   +----------+   +----------+   +--------+
| Start  |-->| Left     |-->| Right    |-->| Left     |-->| Right    |-->| Finish |
|        |   | Sock     |   | Sock     |   | Shoe     |   | Shoe     |   |        |
+--------+   +----------+   +----------+   +----------+   +
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
- - Persistence actions: Represent “inactions” by boxes: frame axiom
- Mutual exclusions (mutex) are represented between literals and actions.
- S1 represents multiple states
- Continue until two levels are identical. The graph levels off.
- The graph records the impossibility of certain choices using mutex links.
- Complexity of graph generation: polynomial in number of literals.
- [Diagram: The figure illustrates a planning graph that expands alternating layers of states and actions while preserving “no-op” actions for persistence. Mutex links encode which choices cannot coexist, allowing the graph to capture constraints and eventually level off when no new information is added.]
- ```text
+------+      +------+      +------+      +------+      +------+
| S0   | ---> | A0   | ---> | S1   | ---> | A1   | ---> | S2   |
+------+      +------+      +------+      +------+      +------+

S0:
  Have(Cake) --------------------\
                                   > [Eat(Cake)] -----> effects to S1
  ¬Eaten(Cake) ------------------/

S1:
  Have(Cake) --------------------\ 
                                   > [Bake(Cake)] -----> effects to S2
  ¬Have(Cake) -------------------/
  Eaten(Cake) -------------------\
                                   > [Eat(Cake)]  -----> effects to S2
  ¬Eaten(Cake) ------------------/

Mutex links (gray curved lines) connect incompatible literals/actions within each level.
```
- - A planning graph consists of a sequence of levels that correspond to time-steps in the plan
- Level 0 is the initial state.
- Each level contains a set of literals and a set of actions
- Literals are those that could be true at the time step.
- Actions are those that their preconditions could be satisfied at the time step.
- Works only for propositional planning.

## Tutor answer
# Phân tích Planning Graph cho bài toán thay lốp dự phòng tại S₂

## 1. Tính chất của S₂ cho phép trích xuất lời giải

Theo nội dung từ chunk `3ee13f47-a21d-4661-bcc7-def43f301313` và `9e35dead-7fd9-4935-a575-6dba4efd2a76`, tại mức S₂, planning graph có **hai tính chất quan trọng** đồng thời thỏa mãn:

| Tính chất | Ý nghĩa |
|-----------|---------|
| **Chứa tất cả các literal mục tiêu (goal)** | Literal `at(spare, axle)` đã xuất hiện trong S₂ (nhờ hành động `[PutOn, Spare, Axle]`) |
| **Các goal literal không bị mutex với nhau** | Không có liên kết mutex giữa chúng, nghĩa là có khả năng cùng tồn tại trong cùng một trạng thái |

Điều kiện này chính là tiêu chí kiểm tra trong thuật toán GRAPHPLAN (chunk `c2267876-167a-4c0b-8ffc-58ff737795c2`):

> *"if goals all non-mutex in last level of graph then do solution ← EXTRACT-SOLUTION(...)"*

Nói cách khác, việc **không có mutex** giữa các mục tiêu là dấu hiệu cần thiết (chưa đủ) để một lời giải **có khả năng tồn tại** tại mức đó. Nếu tồn tại mutex giữa các goal, ta biết chắc chắn không thể đạt được tất cả đồng thời và phải tiếp tục mở rộng đồ thị.

## 2. Các phương pháp trích xuất lời giải

Theo chunk `3ee13f47-a21d-4661-bcc7-def43f301313`, có **hai cách** để trích xuất lời giải:

### Cách 1: Giải bài toán thỏa mãn ràng buộc (CSP)
- Coi **các hành động (actions) là các biến**
- Mỗi biến được gán một hành động cụ thể (hoặc persistence action "no-op") tại mỗi mức
- Các ràng buộc (mutex, preconditions, effects) được biểu diễn thành các ràng buộc giữa các biến
- Sử dụng thuật toán CSP để tìm phép gán thỏa mãn

### Cách 2: Tìm kiếm lùi (Backward Search)
- Bắt đầu từ tập goal tại S₂
- Tại mỗi bước, chọn một hành động có thể đạt được một subgoal
- Kiểm tra rằng hành động được chọn **không bị mutex** với các hành động khác đã chọn ở cùng mức
- Tiếp tục lùi về các mức trước (S₁, S₀) cho đến khi đạt trạng thái khởi đầu

## Tóm tắt

```
S₂ chứa tất cả goal + không có mutex giữa các goal
         ↓
   ┌─────┴─────┐
   ↓           ↓
  CSP         Backward
(với actions  Search
là biến)    (lùi từ goal)
```

Lưu ý: nếu cả hai phương pháp đều thất bại, thuật toán GRAPHPLAN (chunk `c2267876`) sẽ tiếp tục mở rộng đồ thị sang S₃, trừ khi `NO-SOLUTION-POSSIBLE` được xác nhận.

---

**Chunk IDs đã sử dụng:**
```json

## Citations
```json
[
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
    "chunk_id": "891991f8-bac0-496d-a9d1-db47f94880e3",
    "document_title": "lecture12-Planning.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "Planning Graphs",
    "page_number": null,
    "chunk_order": 47,
    "excerpt": "- A planning graph consists of a sequence of levels that correspond to time-steps in the plan\n- Level 0 is the initial state.\n- Each level contains a set of literals and a set of actions\n- Literals ar"
  }
]
```
