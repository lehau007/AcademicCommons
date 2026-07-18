# hard_ai_multi_04

## Question
Trả lời hai ý về tìm kiếm trong AI: (1) A* có đầy đủ (complete) không và độ phức tạp thời gian của nó ra sao; (2) tìm kiếm giới hạn độ sâu (depth-limited search) khắc phục nhược điểm gì của tìm kiếm theo chiều sâu (DFS)?

## Ground truth
(1) A* là đầy đủ (Completeness: YES); về độ phức tạp thời gian, số node được mở rộng vẫn tăng theo cấp số mũ theo độ dài của lời giải. (2) DFS có thể mắc kẹt trên một đường đi vô hạn trong khi một lựa chọn khác lại dẫn tới lời giải; depth-limited search chính là DFS có thêm giới hạn độ sâu, nhờ đó tránh đi theo nhánh vô hạn.

## Retrieved context (what the tutor saw)
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
- | Criterion | Breadth-First | Uniform-Cost | Depth-First | Depth-Limited | Iterative Deepening |
|---|---|---|---|---|---|
| Complete? | Yes | Yes | No | No | Yes |
| Time | $O(b^{d+1})$ | $O(b^{\lceil C^*/\epsilon \rceil})$ | $O(b^m)$ | $O(b^l)$ | $O(b^d)$ |
| Space | $O(b^{d+1})$ | $O(b^{\lceil C^*/\epsilon \rceil})$ | $O(bm)$ | $O(bl)$ | $O(bd)$ |
| Optimal? | Yes | Yes | No | No | Yes |
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
- [Diagram: The pseudocode shows how depth-limited search preserves the systematic nature of depth-first search while preventing it from diving indefinitely. The special cutoff result lets the algorithm distinguish between “no solution found yet because the limit was reached” and true failure, which is crucial for iterative deepening and controlled exploration.]
- - Formulation as state-space search problem:
  - Initial state and goal test: obvious
  - Successor function: generate from applicable actions
  - Step cost = each action costs 1
- Any complete graph search algorithm is a complete planning algorithm.
  - E.g. A*
- Inherently inefficient:
  - (1) irrelevant actions lead to very broad search tree
  - (2) good heuristic required for efficient search

## Tutor answer
# Trả lời

## (1) A* có đầy đủ (complete) không và độ phức tạp thời gian?

**Có, A* là thuật toán đầy đủ (complete).**

- **Completeness: YES** — A* đảm bảo tìm được lời giải nếu lời giải tồn tại.
- **Time complexity: hàm mũ theo độ dài đường đi** (exponential with path length).
- Ngoài ra, A* còn **tối ưu (Optimal: YES)** và **tối ưu hiệu quả** (optimally efficient, không tính các trường hợp hòa). Cụ thể:
  - A* mở rộng tất cả các nút có $f(n) < C^*$
  - A* mở rộng một số nút có $f(n) = C^*$
  - A* không mở rộng nút nào có $f(n) > C^*$

Tuy nhiên, nhược điểm về không gian của A* là **phải lưu trữ tất cả các nút** (space complexity: all nodes are stored), vì vậy người ta đề xuất các biến thể như IDA*, RBFS, hay (S)MA* để khắc phục vấn đề bộ nhớ.

## (2) Tìm kiếm giới hạn độ sâu khắc phục nhược điểm gì của DFS?

Theo tài liệu, **DFS có thể bị "mắc kẹt" trên một đường đi vô hạn** (infinite path) khi mà chỉ cần chọn một nhánh khác thì đã có thể tìm ra lời giải:

> *"Depth-first search can get stuck on infinite path when a different choice would lead to a solution."*

**Depth-limited search** chính là **DFS được giới hạn độ sâu $l$** (depth-first search with depth limit $l$): các nút ở độ sâu $l$ không có nút con kế tiếp, tức là thuật toán **buộc phải dừng và quay lại (backtrack)** khi đạt đến giới hạn, thay vì đi mãi trên một nhánh vô tận.

Nhờ đó, depth-limited search khắc phục được nhược điểm "sa vào đường đi vô hạn" của DFS. Tuy nhiên, theo bảng tổng kết, nó vẫn **không đầy đủ (Complete? No)** vì có thể bỏ lỡ lời giải nếu lời giải nằm ở độ sâu lớn hơn giới hạn $l$ — đó chính là lý do người ta phát triển tiếp **iterative deepening search**.

---

```json

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
    "chunk_id": "a176b3fe-c3c0-4e3f-9d5e-b71b984ac92c",
    "document_title": "lecture3_search.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "Summary of algorithms",
    "page_number": null,
    "chunk_order": 37,
    "excerpt": "| Criterion | Breadth-First | Uniform-Cost | Depth-First | Depth-Limited | Iterative Deepening |\n|---|---|---|---|---|---|\n| Complete? | Yes | Yes | No | No | Yes |\n| Time | $O(b^{d+1})$ | $O(b^{\\lcei"
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
  }
]
```
