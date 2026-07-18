# hard_ai_multi_04

## Question
Trả lời hai ý về tìm kiếm trong AI: (1) A* có đầy đủ (complete) không và độ phức tạp thời gian của nó ra sao; (2) tìm kiếm giới hạn độ sâu (depth-limited search) khắc phục nhược điểm gì của tìm kiếm theo chiều sâu (DFS)?

## Ground truth
(1) A* là đầy đủ (Completeness: YES); về độ phức tạp thời gian, số node được mở rộng vẫn tăng theo cấp số mũ theo độ dài của lời giải. (2) DFS có thể mắc kẹt trên một đường đi vô hạn trong khi một lựa chọn khác lại dẫn tới lời giải; depth-limited search chính là DFS có thêm giới hạn độ sâu, nhờ đó tránh đi theo nhánh vô hạn.

## Retrieved context (what the tutor saw)
- - Completeness: YES
- Time complexity: (exponential with path length)
- Space complexity: (all nodes are stored)
- Optimality: YES
  - Cannot expand $f_{i+1}$ until $f_i$ is finished.
  - A* expands all nodes with $f(n) < C^*$
  - A* expands some nodes with $f(n) = C^*$
  - A* expands no nodes with $f(n) > C^*$

Also optimally efficient (not including ties)
- - Some solutions to A* space problems (maintain completeness and optimality)
  - Iterative-deepening A* (IDA*)
    - Here cutoff information is the $f$-cost $(g+h)$ instead of depth
  - Recursive best-first search(RBFS)
    - Recursive algorithm that attempts to mimic standard best-first search with linear space.
  - (simple) Memory-bounded A* ((S)MA*)
    - Drop the worst-leaf node when memory is full
- [Diagram: The picture illustrates a heuristic landscape where Greedy Best-First Search moves toward the apparently most promising states, guided by estimated closeness to the goal. This explains why it can be fast in practice but also why it may get trapped in local choices and fail to find a complete or optimal solution.]

- What do we need to do to make it complete?
- $\Rightarrow$ A* search
- Can we make it optimal? $\rightarrow$ No
- - If the state space is finite and we avoid repeated states, the search is complete
- If the state space is finite and we do not avoid repeated states, the search is in general not complete
- If the state space is infinite, the search is in general not complete
- - Completeness: YES
- Time complexity: (exponential with path length)
- Space complexity:
  - It keeps all generated nodes in memory
  - Hence space is the major problem not time
- - Complete? No – can get stuck in loops, e.g., Iasi $\rightarrow$ Neamt $\rightarrow$ Iasi $\rightarrow$ Neamt $\rightarrow$ ...
- Time? $O(b^m)$, but a good heuristic can give dramatic improvement
- Space? $O(b^m)$ -- keeps all nodes in memory
- Optimal? No

```text
                b
               ↗
          [+-----------+]
          |      •      |
          |     /|\     |
          |    / | \    |
          |   /  |  \   |
          |  /   / \  \  |
          | /   /   \  \ |
          |/   /     \  \|
        [+-----------+]   [+-----------+]
        |      •      |   |      •      |
        +-------------+   +-------------+

                 m
        [ } bracket indicating search depth/levels ]

          [grey shaded heuristic contour]
          [nodes near the top are preferred by the heuristic]
```
- - Completeness: YES
- Time complexity:
  - Number of nodes expanded is still exponential in the length of the solution.
- - Use all available memory.
  - I.e. expand best leafs until available memory is full
  - When full, SMA* drops worst leaf node (highest $f$-value)
  - Like RBFS, we remember the best descendant in the branch we delete

- What if all leafs have the same $f$-value?
  - Same node could be selected for expansion and deletion.
  - SMA* solves this by expanding *newest* best leaf and deleting *oldest* worst leaf.

- The deleted node is regenerated when all other candidates look worse than the node.

- SMA* is complete if solution is reachable, optimal if optimal solution is reachable.

- Time can still be exponential.
- - Limit = 3

```text
Iterative deepening search at limit 3:
A
├─ B
│  ├─ D
│  │  ├─ H
│  │  └─ I
│  └─ E
│     ├─ J
│     └─ K
└─ C
   ├─ F
   │  ├─ L
   │  └─ M
   └─ G
      ├─ N
      └─ O
```

[Diagram: The sequence of panels shows depth-limited search repeated with increasing progress through the tree until the limit is reached. It illustrates how iterative deepening explores nodes in a depth-first manner while gradually expanding the search horizon, combining the low memory use of DFS with the completeness of BFS-like layer-by-layer discovery.]
- [Diagram: The figure illustrates progressively deepened search frontiers over the same tree, showing how the algorithm repeatedly reruns DFS with larger depth limits until the goal becomes reachable. This matters because it combines DFS’s low memory use with completeness, avoiding the “missed solution” problem of a fixed depth limit.]

```text
function ITERATIVE-DEEPENING-SEARCH(problem) returns a solution, or failure
    inputs: problem, a problem
    for depth ← 0 to ∞ do
        result ← DEPTH-LIMITED-SEARCH(problem, depth)
        if result ≠ cutoff then return result
```
- [Diagram: The pseudocode shows how depth-limited search preserves the systematic nature of depth-first search while preventing it from diving indefinitely. The special cutoff result lets the algorithm distinguish between “no solution found yet because the limit was reached” and true failure, which is crucial for iterative deepening and controlled exploration.]
- - Problem with depth-limited search: if the shallowest goal is beyond the depth limit, no solution is found.
- Iterative deepening search:
  1. Do a DFS which only searches for paths of length 1

(DFS gives up on any path of length 2)

2. If “1” failed, do a DFS which only searches paths of 2 or less.
  3. If “2” failed, do a DFS which only searches paths of 3 or less.
  4. ....and so on.

```text
        b
      /   \
     o     o
    / \   / \
   /   \ /   \
  /-----/-----\
 /             \
/               \
-----------------
      |
      |
      o
```
- ```text
[Diagram: A search tree of 8-puzzle states expanded up to depth 5. It illustrates how limited-depth search explores possible moves level by level, stopping before deeper states and showing why depth limits control search cost and completeness.]
```
- - Depth-first search can get stuck on infinite path when a different choice would lead to a solution
- [Formula: depth-limited search = depth-first search with depth limit l, nodes at depth l have no successors]
- ```text
Limit = 0
  A
Limit = 1
  A
 B   C
Limit = 2
    A
  B   C
 D E F G
```

[Diagram: The slide illustrates iterative deepening search as a sequence of depth-limited traversals, starting from shallow limits and increasing gradually. This approach combines the space efficiency of depth-first search with the completeness of breadth-first search for finding shallow solutions.]
- ```text
+----------------------------------------------------------------------------------+
| function DEPTH-LIMITED-SEARCH(problem, limit) returns soln/fail/cutoff           |
|     RECURSIVE-DLS(MAKE-NODE(INITIAL-STATE[problem]), problem, limit)              |
|                                                                                  |
| function RECURSIVE-DLS(node, problem, limit) returns soln/fail/cutoff            |
|     cutoff-occurred? ← false                                                     |
|     if GOAL-TEST[problem](STATE[node]) then return SOLUTION(node)                |
|     else if DEPTH[node] = limit then return cutoff                             |
|     else for each successor in EXPAND(node, problem) do                          |
|         result ← RECURSIVE-DLS(successor, problem, limit)                        |
|         if result = cutoff then cutoff-occurred? ← true                         |
|         else if result ≠ failure then return result                              |
|     if cutoff-occurred? then return cutoff else return failure                   |
+----------------------------------------------------------------------------------+
```

## Tutor answer
# Trả lời hai ý về tìm kiếm trong AI

## (1) A* có đầy đủ (complete) không? Độ phức tạp thời gian ra sao?

Theo tài liệu môn học, đặc tính của thuật toán **A* search** được đánh giá như sau:

| Tiêu chí | A* |
|---|---|
| **Completeness (đầy đủ)** | **YES** — A* là thuật toán tìm kiếm đầy đủ |
| **Time complexity** | **Số nút được mở rộng vẫn là hàm mũ theo chiều dài đường đi lời giải** (exponential in path length) |
| Space complexity | Bị giới hạn bởi bộ nhớ (giữ tất cả nút đã sinh trong bộ nhớ) |
| Optimality | YES (cũng optimally efficient, không tính các trường hợp hòa) |

**Giải thích thêm về tính đầy đủ:** Trong lý thuyết tổng quát, một tìm kiếm chỉ chắc chắn đầy đủ khi **không gian trạng thái hữu hạn và có tránh trạng thái lặp**. A* với heuristic chấp nhận được (admissible) đảm bảo sẽ tìm được lời giải nếu lời giải tồn tại, đồng thời mở rộng:
- Tất cả các nút có $f(n) < C^*$ (với $C^*$ là chi phí lời giải tối ưu)
- Một số nút có $f(n) = C^*$
- **Không mở rộng nút nào có $f(n) > C^*$**

> **Lưu ý thực tế:** Vấn đề lớn nhất của A* thường **không phải thời gian** mà là **bộ nhớ**, vì nó phải lưu tất cả các nút đã sinh. Do đó người ta thường dùng các biến thể giới hạn bộ nhớ như **IDA\***, **RBFS**, hay **SMA***.

---

## (2) Tìm kiếm giới hạn độ sâu (Depth-Limited Search) khắc phục nhược điểm gì của DFS?

**Định nghĩa:** Depth-limited search = **DFS có thêm giới hạn độ sâu $l$**; các nút ở độ sâu $l$ được coi là không có nút con kế tiếp.

**Nhược điểm của DFS mà Depth-Limited Search khắc phục:**

DFS thuần túy có thể **bị "kẹt" (get stuck) trên các đường đi vô hạn**, trong khi một lựa chọn khác ở nhánh khác lại dẫn tới lời giải. Nói cách khác, nếu cây tìm kiếm chứa nhánh sâu vô tận (hoặc rất sâu), DFS có thể đi mãi trên nhánh đó mà **không bao giờ quay lại** để thử lựa chọn tốt hơn, dẫn đến thuật toán chạy mãi không dừng hoặc không tìm ra lời giải.

Depth-Limited Search giải quyết vấn đề này bằng cách:
- **Đặt ngưỡng độ sâu $l$** — khi một nhánh đạt đến độ sâu $l$, thuật toán dừng đào sâu tiếp và **quay lui (backtrack)** để thử nhánh khác.
- Trả về một giá trị đặc biệt `cutoff` để phân biệt với `failure` (hết nhánh cần thử). Việc phân biệt này rất quan trọng vì nó cho phép cấp trên (ví dụ **Iterative Deepening Search**) biết rằng "chưa tìm thấy lời giải vì chạm giới hạn, chứ không phải là không tồn tại lời giải trong nhánh này".

**Lưu ý:** Depth-Limited Search vẫn có nhược điểm riêng — nếu **lời giải nông nhất nằm ngoài giới hạn $l$** thì sẽ không tìm được lời giải. Đây chính là lý do người ta kết hợp nó với Iterative Deepening: lặp lại DLS với $l$ tăng dần (0, 1, 2, …) cho đến khi tìm ra lời giải hoặc xác nhận không có.

---

### Tóm tắt nhanh

| Ý | Trả lời |
|---|---|
| A* complete? | **Có** (YES) |
| A* time complexity | **Hàm mũ theo chiều dài lời giải** (exponential in path length) |
| Depth-limited search khắc phục gì ở DFS? | Khắc phục việc DFS **bị kẹt trên đường đi sâu vô hạn**, bằng cách đặt giới hạn độ sâu $l$ để buộc thuật toán quay lui kịp thời và phân biệt được `cutoff` với `failure`. |

## Citations
```json
[
  {
    "chunk_id": "e502adf5-5421-449d-9d42-22d6ec561ece",
    "document_title": "lecture4-search.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "A* search, evaluation",
    "page_number": null,
    "chunk_order": 37,
    "excerpt": "- Completeness: YES\n- Time complexity: (exponential with path length)\n- Space complexity: (all nodes are stored)\n- Optimality: YES\n  - Cannot expand $f_{i+1}$ until $f_i$ is finished.\n  - A* expands a"
  },
  {
    "chunk_id": "b3c50da4-c71e-47a5-99d5-c335272ea963",
    "document_title": "lecture5-Advanced search methods.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "Memory-bounded heuristic search",
    "page_number": null,
    "chunk_order": 3,
    "excerpt": "- Some solutions to A* space problems (maintain completeness and optimality)\n  - Iterative-deepening A* (IDA*)\n    - Here cutoff information is the $f$-cost $(g+h)$ instead of depth\n  - Recursive best"
  },
  {
    "chunk_id": "bc7cf346-8804-4327-9d16-5526c6cd5e0c",
    "document_title": "lecture4-search.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "Greedy Best-First Search",
    "page_number": null,
    "chunk_order": 19,
    "excerpt": "[Diagram: The picture illustrates a heuristic landscape where Greedy Best-First Search moves toward the apparently most promising states, guided by estimated closeness to the goal. This explains why i"
  },
  {
    "chunk_id": "7b29c8aa-6966-4bc1-a230-e2edd01e97d2",
    "document_title": "lecture4-search.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "Can we Prove Anything?",
    "page_number": null,
    "chunk_order": 30,
    "excerpt": "- If the state space is finite and we avoid repeated states, the search is complete\n- If the state space is finite and we do not avoid repeated states, the search is in general not complete\n- If the s"
  },
  {
    "chunk_id": "bf3f647a-f779-4072-8ce4-dd41c6ed7dce",
    "document_title": "lecture4-search.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "A* search, evaluation",
    "page_number": null,
    "chunk_order": 36,
    "excerpt": "- Completeness: YES\n- Time complexity: (exponential with path length)\n- Space complexity:\n  - It keeps all generated nodes in memory\n  - Hence space is the major problem not time"
  },
  {
    "chunk_id": "a7d3a1ec-ee61-4086-90c5-a96f715eafb9",
    "document_title": "lecture4-search.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "Greedy Best-First Search",
    "page_number": null,
    "chunk_order": 18,
    "excerpt": "- Complete? No – can get stuck in loops, e.g., Iasi $\\rightarrow$ Neamt $\\rightarrow$ Iasi $\\rightarrow$ Neamt $\\rightarrow$ ...\n- Time? $O(b^m)$, but a good heuristic can give dramatic improvement\n- "
  },
  {
    "chunk_id": "a07782cc-a1c2-40c2-b7c5-0c73d817732d",
    "document_title": "lecture4-search.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "A* search, evaluation",
    "page_number": null,
    "chunk_order": 35,
    "excerpt": "- Completeness: YES\n- Time complexity:\n  - Number of nodes expanded is still exponential in the length of the solution."
  },
  {
    "chunk_id": "9ee7b3fd-eff2-4307-a48e-dfd4b858bfce",
    "document_title": "lecture5-Advanced search methods.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "(simplified) memory-bounded A*",
    "page_number": null,
    "chunk_order": 13,
    "excerpt": "- Use all available memory.\n  - I.e. expand best leafs until available memory is full\n  - When full, SMA* drops worst leaf node (highest $f$-value)\n  - Like RBFS, we remember the best descendant in th"
  },
  {
    "chunk_id": "5adfc234-57b6-41ed-b47b-ca834fe9704e",
    "document_title": "lecture3_search.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "Iterative deepening search (con’t)",
    "page_number": null,
    "chunk_order": 34,
    "excerpt": "- Limit = 3\n\n```text\nIterative deepening search at limit 3:\nA\n├─ B\n│  ├─ D\n│  │  ├─ H\n│  │  └─ I\n│  └─ E\n│     ├─ J\n│     └─ K\n└─ C\n   ├─ F\n   │  ├─ L\n   │  └─ M\n   └─ G\n      ├─ N\n      └─ O\n```\n\n[Di"
  },
  {
    "chunk_id": "931ef975-3849-4ada-8808-cbf9ae1fe222",
    "document_title": "lecture3_search.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "Iterative deepening search",
    "page_number": null,
    "chunk_order": 32,
    "excerpt": "[Diagram: The figure illustrates progressively deepened search frontiers over the same tree, showing how the algorithm repeatedly reruns DFS with larger depth limits until the goal becomes reachable. "
  },
  {
    "chunk_id": "81ae7bf8-2768-485b-8bee-1874db0615cd",
    "document_title": "lecture3_search.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "Depth-limited search",
    "page_number": null,
    "chunk_order": 29,
    "excerpt": "[Diagram: The pseudocode shows how depth-limited search preserves the systematic nature of depth-first search while preventing it from diving indefinitely. The special cutoff result lets the algorithm"
  },
  {
    "chunk_id": "da5b2bdc-de5f-483b-8577-69c765c5ff9e",
    "document_title": "lecture3_search.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "Iterative deepening search",
    "page_number": null,
    "chunk_order": 31,
    "excerpt": "- Problem with depth-limited search: if the shallowest goal is beyond the depth limit, no solution is found.\n- Iterative deepening search:\n  1. Do a DFS which only searches for paths of length 1\n\n(DFS"
  },
  {
    "chunk_id": "65ee7ce7-2cc0-4c7a-89b1-256f57c79120",
    "document_title": "lecture3_search.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "8-puzzle game with depth limit l = 5",
    "page_number": null,
    "chunk_order": 30,
    "excerpt": "```text\n[Diagram: A search tree of 8-puzzle states expanded up to depth 5. It illustrates how limited-depth search explores possible moves level by level, stopping before deeper states and showing why"
  },
  {
    "chunk_id": "e00eb634-2376-4696-8ba3-58c18c46372b",
    "document_title": "lecture3_search.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "Depth-limited search",
    "page_number": null,
    "chunk_order": 27,
    "excerpt": "- Depth-first search can get stuck on infinite path when a different choice would lead to a solution\n- [Formula: depth-limited search = depth-first search with depth limit l, nodes at depth l have no "
  },
  {
    "chunk_id": "494db24f-170c-42ea-8588-5a192e02e5b7",
    "document_title": "lecture3_search.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "Iterative deepening search (con’t)",
    "page_number": null,
    "chunk_order": 33,
    "excerpt": "```text\nLimit = 0\n  A\nLimit = 1\n  A\n B   C\nLimit = 2\n    A\n  B   C\n D E F G\n```\n\n[Diagram: The slide illustrates iterative deepening search as a sequence of depth-limited traversals, starting from sha"
  },
  {
    "chunk_id": "12505c55-76ad-42fb-98d3-87195df1d673",
    "document_title": "lecture3_search.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "Depth-limited search",
    "page_number": null,
    "chunk_order": 28,
    "excerpt": "```text\n+----------------------------------------------------------------------------------+\n| function DEPTH-LIMITED-SEARCH(problem, limit) returns soln/fail/cutoff           |\n|     RECURSIVE-DLS(MA"
  }
]
```
