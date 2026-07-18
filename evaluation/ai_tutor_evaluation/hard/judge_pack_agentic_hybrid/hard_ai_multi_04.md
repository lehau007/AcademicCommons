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
- - A* expands nodes in order of increasing $f$ value
- Gradually adds "$f$-contours" of nodes
- Contour $i$ has all nodes with $f=f_i$, where $f_i < f_{i+1}$

```text
                 o
                 |
                 z
                / \
               /   \
              A     S ---- F ---- B ---- U ---- H ---- E
             / \     \      \      \      |
            T   \     R      P       \     |
             \   \    |     /         \    |
              L   \   C    /           G    |
              |    \  |   /                 |
              M     \ |  /                  |
              |      D--                    |
```

```text
   --- contour around earlier / lower-nodes ---
```

[Diagram: The red dashed contours illustrate how A* reveals the search space in layers of increasing evaluation value $f=g+h$. This matters because it shows why A* can remain efficient while still guaranteeing optimality when the heuristic is admissible.]
- - If the state space is finite and we avoid repeated states, the search is complete
- If the state space is finite and we do not avoid repeated states, the search is in general not complete
- If the state space is infinite, the search is in general not complete
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
- Time complexity: (exponential with path length)
- Space complexity:
  - It keeps all generated nodes in memory
  - Hence space is the major problem not time
- - Completeness: YES
- Time complexity:
  - Number of nodes expanded is still exponential in the length of the solution.
- [Diagram: The pseudocode shows how depth-limited search preserves the systematic nature of depth-first search while preventing it from diving indefinitely. The special cutoff result lets the algorithm distinguish between “no solution found yet because the limit was reached” and true failure, which is crucial for iterative deepening and controlled exploration.]
- [Diagram: The figure illustrates progressively deepened search frontiers over the same tree, showing how the algorithm repeatedly reruns DFS with larger depth limits until the goal becomes reachable. This matters because it combines DFS’s low memory use with completeness, avoiding the “missed solution” problem of a fixed depth limit.]

```text
function ITERATIVE-DEEPENING-SEARCH(problem) returns a solution, or failure
    inputs: problem, a problem
    for depth ← 0 to ∞ do
        result ← DEPTH-LIMITED-SEARCH(problem, depth)
        if result ≠ cutoff then return result
```
- - Depth-first search can get stuck on infinite path when a different choice would lead to a solution
- [Formula: depth-limited search = depth-first search with depth limit l, nodes at depth l have no successors]
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
[Diagram: A search tree of 8-puzzle states expanded up to depth 5. It illustrates how limited-depth search explores possible moves level by level, stopping before deeper states and showing why depth limits control search cost and completeness.]
```

## Tutor answer
# Trả lời hai ý về tìm kiếm trong AI

## (1) A* search: tính đầy đủ và độ phức tạp thời gian

Theo tài liệu môn học, thuật toán **A\* search** có các đặc tính sau:

- **Tính đầy đủ (Completeness): CÓ (YES)** — A\* đảm bảo tìm được lời giải (khi không gian trạng thái hữu hạn và hàm heuristic chấp nhận được / admissible).
- **Tối ưu (Optimality): CÓ (YES)** — nhờ cơ chế:
  - Không mở rộng node có $f_{i+1}$ cho đến khi mở rộng xong tất cả node có $f_i$.
  - Mở rộng toàn bộ các node có $f(n) < C^*$ (với $C^*$ là chi phí lời giải tối ưu).
  - Mở rộng một số node có $f(n) = C^*$.
  - **Không** mở rộng bất kỳ node nào có $f(n) > C^*$.
- **Độ phức tạp thời gian: hàm mũ theo độ dài đường đi (exponential in the length of the solution)** — số node được mở rộng vẫn tăng theo hàm mũ của độ dài lời giải.
- **Hiệu quả tối ưu (Optimally efficient)** — không tính các trường hợp hòa (ties): không có thuật toán nào khác mở rộng ít node hơn A\* mà vẫn đảm bảo tối ưu.
- **Độ phức tạp không gian:** A\* lưu giữ tất cả các node đã sinh ra trong bộ nhớ → **không gian mới là vấn đề lớn, không phải thời gian**.

## (2) Depth-limited search khắc phục nhược điểm gì của DFS?

Tài liệu môn học nêu rõ:

- **Nhược điểm của DFS:** *Depth-first search có thể bị "kẹt" trên một đường đi vô hạn (infinite path) khi mà một lựa chọn khác lại dẫn tới lời giải.* Nói cách khác, DFS có thể đi sâu mãi theo một nhánh sai vô tận mà bỏ qua lời giải ở nhánh khác.
- **Cách depth-limited search khắc phục:** *Depth-limited search = depth-first search với giới hạn độ sâu $l$; các node ở độ sâu $l$ được coi là không có nút con (no successors).* Nhờ đặt ngưỡng độ sâu cố định, thuật toán **tránh được việc đi sâu vô hạn** dọc theo một nhánh, đảm bảo quá trình tìm kiếm luôn dừng.
- **Hạn chế còn lại (và cách khắc phục tiếp):** Nếu *goal nông nhất nằm ngoài giới hạn độ sâu* thì depth-limited search sẽ **không tìm thấy lời giải**. Đây chính là lý do **Iterative deepening search** ra đời: lặp lại depth-limited search với độ sâu tăng dần (1, 2, 3, …) cho đến khi tìm được lời giải, kết hợp được **ưu điểm bộ nhớ thấp của DFS** với **tính đầy đủ của BFS**.

---

**Tóm lại:**
- A\* **đầy đủ**, thời gian **hàm mũ theo độ dài lời giải**, vấn đề lớn nhất nằm ở **không gian bộ nhớ**.
- Depth-limited search khắc phục nhược điểm **bị kẹt trên đường đi vô hạn** của DFS bằng cách đặt giới hạn độ sâu, đảm bảo thuật toán luôn dừng.

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
    "chunk_id": "fa65614b-8fe0-4ce1-8623-c3565087ecbc",
    "document_title": "lecture4-search.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "Contours of A* Search",
    "page_number": null,
    "chunk_order": 32,
    "excerpt": "- A* expands nodes in order of increasing $f$ value\n- Gradually adds \"$f$-contours\" of nodes\n- Contour $i$ has all nodes with $f=f_i$, where $f_i < f_{i+1}$\n\n```text\n                 o\n               "
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
    "chunk_id": "65ee7ce7-2cc0-4c7a-89b1-256f57c79120",
    "document_title": "lecture3_search.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "8-puzzle game with depth limit l = 5",
    "page_number": null,
    "chunk_order": 30,
    "excerpt": "```text\n[Diagram: A search tree of 8-puzzle states expanded up to depth 5. It illustrates how limited-depth search explores possible moves level by level, stopping before deeper states and showing why"
  }
]
```
