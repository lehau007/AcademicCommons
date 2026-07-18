# hard_ai_graph_02

## Question
Trong sơ đồ planning graph cho bài toán thay lốp dự phòng (spare tire), trạng thái mức S2 có tính chất gì khiến ta có thể trích xuất lời giải, và có thể trích xuất bằng những cách nào?

## Ground truth
Ở mức S2 planning graph đã chứa tất cả các goal (ví dụ at(spare,axle)) và không có mutex giữa chúng, nên có thể thử trích xuất lời giải. Có thể trích xuất bằng thuật toán CSP với các action làm biến, hoặc bằng tìm kiếm lùi (search backwards) từ goal.

## Retrieved context (what the tutor saw)
- [Diagram: Đây là thuật toán ra quyết định trong trò chơi đối kháng bằng cách luân phiên tối đa hóa và tối thiểu hóa giá trị trạng thái. Nó quan trọng vì cho phép chọn nước đi tối ưu khi giả định đối thủ cũng chơi tối ưu.]
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
- ```text
   +---+
   | C |
   +---+
   | A |
   +---+      +---+
              | B |
              +---+
========================
```

[Diagram: The initial configuration shows a stack with C on A and B separately on the table. It matters because planning actions must transform this arrangement into the desired goal state while respecting block-precondition constraints.]
- - Estimate the cost of achieving a goal by the level in the planning graph where it appears.
- To estimate the cost of a conjunction of goals use one of the following:
  - Max-level: take the maximum level of any goal (admissible)
  - Sum-cost: Take the sum of levels (inadmissible)
  - Set-level: find the level where they all appear without Mutex
- Graph plans are relaxation of the problem.
- Representing more than pair-wise mutex is not cost-effective

## Tutor answer
# Trích xuất lời giải từ Planning Graph ở mức S2

## Tính chất của S2 cho phép trích xuất lời giải

Theo nội dung trong tài liệu, ở mức trạng thái **S2**, ta có hai tính chất quan trọng cho phép việc trích xuất lời giải trở nên khả thi:

1. **S2 chứa tất cả các goal (mục tiêu)**: Cụ thể là `at(spare, axle)` — tức lốp dự phòng đã ở trên trục xe.
2. **Không còn mutex (mutual exclusion) giữa các goal**: Các mục tiêu tại S2 không mâu thuẫn với nhau, nghĩa là chúng có thể đạt được đồng thời.

Chính vì vậy, khi kiểm tra điều kiện `goals all non-mutex in last level of graph` trong thuật toán GRAPHPLAN là thỏa mãn, ta có thể tiến hành trích xuất lời giải.

## Các cách trích xuất lời giải

Có **hai phương pháp** chính được đề cập:

### 1. Sử dụng thuật toán CSP (Constraint Satisfaction Problem)
- Coi **các action là các biến** (variables).
- Các ràng buộc (constraints) giữa các action bao gồm:
  - Quan hệ tiền đề — kết quả (precondition-effect).
  - Quan hệ mutex giữa các action.
- Tìm một gán (assignment) thỏa mãn tất cả ràng buộc.

### 2. Tìm kiếm ngược (search backwards)
- Bắt đầu từ tập goal ở S2.
- Ở mỗi bước, chọn một action ở A1 (action level ngay trước) có thể đạt được một subgoal.
- Lùi dần về S0, đảm bảo rằng các action được chọn không mâu thuẫn (non-mutex) với nhau.

## Minh họa qua sơ đồ

Sơ đồ trong tài liệu cho thấy:
- Các đường **bold** (in đậm) đánh dấu lời giải: từ trạng thái ban đầu qua các action `RemoveSpare(Trunk)`, `RemoveFlat(Axle)`, `LeaveOvernight`, đến `PutOnSpare(Axle)` ở A1 → S2.
- Đây là một **partial-order plan** hợp lệ, cho thấy có thể rút ra kế hoạch từ S2 bằng cách lần ngược các liên kết.

## Tổng kết

| Tính chất của S2 | Ý nghĩa |
|---|---|
| Chứa tất cả goal | Mục tiêu đã xuất hiện trong graph |
| Không có mutex giữa các goal | Các goal có thể đạt đồng thời → có lời giải khả thi |

| Phương pháp trích xuất | Đặc điểm |
|---|---|
| CSP với actions là biến | Giải bài toán ràng buộc |
| Tìm kiếm ngược | Backward search từ goal về S0 |

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
  }
]
```
